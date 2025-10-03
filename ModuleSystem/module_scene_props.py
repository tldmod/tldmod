from header_common import *
from header_scene_props import *
from header_operations import *
from header_triggers import *
from header_sounds import *
from module_constants import *
from header_mission_templates import *
from module_info import wb_compile_switch as is_a_wb_sceneprop
import string

####################################################################################################################
#  Each scene prop record contains the following fields:
#  1) Scene prop id: used for referencing scene props in other files. The prefix spr_ is automatically added before each scene prop id.
#  2) Scene prop flags. See header_scene_props.py for a list of available flags
#  3) Mesh name: Name of the mesh.
#  4) Physics object name:
#  5) Triggers: Simple triggers that are associated with the scene prop
####################################################################################################################

dead_marches_effect = [
 ] + (is_a_wb_sceneprop==1 and [ 
    (ti_on_init_scene_prop, [(store_trigger_param_1, ":instance_no"),
        #(neg|is_edit_mode_enabled),
        (scene_prop_set_visibility, ":instance_no", 0)
        ]),
    (ti_on_scene_prop_is_animating,[(store_trigger_param_1, ":instance_no"),
        (scene_prop_slot_eq, ":instance_no", slot_prop_active, 0), 
        (prop_instance_get_position, pos6, ":instance_no"), 
        (position_move_z, pos6, 200, 1), 
        (position_get_z, ":height", pos6), 
        (gt, ":height", 0), 
        (particle_system_burst, "psys_candle_light_small", pos6, 3),
    ]),
    
    (ti_on_scene_prop_animation_finished,[
        (store_trigger_param_1, ":instance_no"),
        (try_begin),
            (scene_prop_slot_eq, ":instance_no", slot_prop_active, 0),
            (scene_prop_set_slot, ":instance_no", slot_prop_active, 1),
            (particle_system_burst, "psys_candle_light_small", pos6, 60),
            (set_fixed_point_multiplier, 100),
            (prop_instance_get_position, pos6, ":instance_no"), 
            (position_move_z, pos6, -100), 
            (prop_instance_animate_to_position, ":instance_no", pos6, 700),
        (else_try),
            (scene_prop_set_visibility, ":instance_no", 0),
        (try_end),
    ])
 ] or []) + [      
    ]

scene_props = [
("invalid_object",0,"question_mark","0", []),
("inventory",sokf_type_container|sokf_place_at_origin,"package","bobaggage", []),
("empty", 0, "0", "0", []),
#MV: disabled container for all chests except inventory and player chest
#  ("chest_a",sokf_type_container,"chest_gothic","bochest_gothic", []),
("chest_a",0,"chest_gothic","bochest_gothic", []),
#  ("container_small_chest",sokf_type_container,"package","bobaggage", []),
("container_small_chest",0,"package","bobaggage", []),
#  ("container_chest_b",sokf_type_container,"chest_b","bo_chest_b", []),
("container_chest_b",0,"chest_b_new","bo_chest_b", []),
#  ("container_chest_c",sokf_type_container,"chest_c","bo_chest_c", []),
("container_chest_c",0,"chest_c_new","bo_chest_c", []),
("player_chest",sokf_type_container,"player_chest","bo_player_chest", []),
("locked_player_chest",0,"player_chest","bo_player_chest", []),

("light_sun",sokf_invisible,"light_sphere","0",  [
     (ti_on_init_scene_prop,
      [   (neg|is_currently_night),
          (store_trigger_param_1, ":prop_instance_no"),
          (set_fixed_point_multiplier, 100),
          (prop_instance_get_scale, pos5, ":prop_instance_no"),
          (position_get_scale_x, ":scale", pos5),
          (store_time_of_day,reg(12)),
          (try_begin),
            (is_between,reg(12),5,20),
            (store_mul, ":red", 5 * 200, ":scale"),
            (store_mul, ":green", 5 * 193, ":scale"),
            (store_mul, ":blue", 5 * 180, ":scale"),
          (else_try),
            (store_mul, ":red", 5 * 90, ":scale"),
            (store_mul, ":green", 5 * 115, ":scale"),
            (store_mul, ":blue", 5 * 150, ":scale"),
          (try_end),
          (val_div, ":red", 100),
          (val_div, ":green", 100),
          (val_div, ":blue", 100),
          (set_current_color,":red", ":green", ":blue"),
          (set_position_delta,0,0,0),
          (add_point_light, 0, 0),
      ])]),
  ("light",sokf_invisible,"light_sphere","0",  [
     (ti_on_init_scene_prop,
      [   (store_trigger_param_1, ":prop_instance_no"),
          (set_fixed_point_multiplier, 100),
          (prop_instance_get_scale, pos5, ":prop_instance_no"),
          (position_get_scale_x, ":scale", pos5),
          (store_mul, ":red", 3 * 200, ":scale"),
          (store_mul, ":green", 3 * 145, ":scale"),
          (store_mul, ":blue", 3 * 45, ":scale"),
          (val_div, ":red", 100),
          (val_div, ":green", 100),
          (val_div, ":blue", 100),
          (set_current_color,":red", ":green", ":blue"),
          (set_position_delta,0,0,0),
          (add_point_light, 10, 30),
      ])]),
("light_red",sokf_invisible,"light_sphere","0",  [
     (ti_on_init_scene_prop,
      [   (store_trigger_param_1, ":prop_instance_no"),
          (set_fixed_point_multiplier, 100),
          (prop_instance_get_scale, pos5, ":prop_instance_no"),
          (position_get_scale_x, ":scale", pos5),
          (store_mul, ":red", 2 * 170, ":scale"),
          (store_mul, ":green", 2 * 100, ":scale"),
          (store_mul, ":blue", 2 * 30, ":scale"),
          (val_div, ":red", 100),
          (val_div, ":green", 100),
          (val_div, ":blue", 100),
          (set_current_color,":red", ":green", ":blue"),
          (set_position_delta,0,0,0),
          (add_point_light, 20, 30),
      ])]),
("light_night",sokf_invisible,"light_sphere","0",  [
     (ti_on_init_scene_prop,
      [ #  (store_time_of_day,reg(12)),
#          (neg|is_between,reg(12),5,20),
          (is_currently_night, 0),
          (store_trigger_param_1, ":prop_instance_no"),
          (set_fixed_point_multiplier, 100),
          (prop_instance_get_scale, pos5, ":prop_instance_no"),
          (position_get_scale_x, ":scale", pos5),
          (store_mul, ":red", 3 * 160, ":scale"),
          (store_mul, ":green", 3 * 145, ":scale"),
          (store_mul, ":blue", 3 * 100, ":scale"),
          (val_div, ":red", 100),
          (val_div, ":green", 100),
          (val_div, ":blue", 100),
          (set_current_color,":red", ":green", ":blue"),
          (set_position_delta,0,0,0),
          (add_point_light, 10, 30),
      ])]),
("torch",0,"torch_a","0",
   [(ti_on_init_scene_prop,
    [   (set_position_delta,0,-35,48),
        (particle_system_add_new, "psys_torch_fire"),
        (particle_system_add_new, "psys_torch_smoke"),
        (particle_system_add_new, "psys_torch_fire_sparks"),
        #(play_sound, "snd_torch_loop", 0), #InVain disabled to prevent sound overflow
         ] + (is_a_wb_sceneprop==1 and [   
        (store_trigger_param_1, ":instance_no"),
        (scene_prop_set_slot, ":instance_no", slot_prop_sound, "snd_torch_loop"),
        ] or []) + [ 
        (set_position_delta,0,-35,56),
        (particle_system_add_new, "psys_fire_glow_1"),
#        (particle_system_emit, "psys_fire_glow_1",9000000),
#second method        
        (get_trigger_object_position, pos2),
        (set_position_delta,0,0,0),
        (position_move_y, pos2, -35),

        (position_move_z, pos2, 55),
        (particle_system_burst, "psys_fire_glow_fixed", pos2, 1),
    ])]),
("torch_night",0,"torch_a","0",
   [(ti_on_init_scene_prop,
    [#   (store_time_of_day,reg(12)),
#        (neg|is_between,reg(12),5,20),
        (is_currently_night, 0),
        (set_position_delta,0,-35,48),
        (particle_system_add_new, "psys_torch_fire"),
        (particle_system_add_new, "psys_torch_smoke"),
        (particle_system_add_new, "psys_torch_fire_sparks"),
        (set_position_delta,0,-35,56),
        (particle_system_add_new, "psys_fire_glow_1"),
        (particle_system_emit, "psys_fire_glow_1",9000000),
        #(play_sound, "snd_torch_loop", 0), #InVain disabled to prevent sound overflow
         ] + (is_a_wb_sceneprop==1 and [   
        (store_trigger_param_1, ":instance_no"),
        (scene_prop_set_slot, ":instance_no", slot_prop_sound, "snd_torch_loop"),
        ] or []) + [        
    ])]),
#  ("Baggage",sokf_place_at_origin|sokf_entity_body,"package","bobaggage"),
("barrier_20m",sokf_invisible|sokf_type_barrier,"barrier_20m","bo_barrier_20m", []),
("barrier_16m",sokf_invisible|sokf_type_barrier,"barrier_16m","bo_barrier_16m", []),
("barrier_8m" ,sokf_invisible|sokf_type_barrier,"barrier_8m" ,"bo_barrier_8m" , []),
("barrier_4m" ,sokf_invisible|sokf_type_barrier,"barrier_4m" ,"bo_barrier_4m" , []),
("barrier_2m" ,sokf_invisible|sokf_type_barrier,"barrier_2m" ,"bo_barrier_2m" , []),

("exit_4m" ,sokf_invisible|sokf_type_barrier_leave,"barrier_4m" ,"bo_barrier_4m" , []),
("exit_8m" ,sokf_invisible|sokf_type_barrier_leave,"barrier_8m" ,"bo_barrier_8m" , []),
("exit_16m" ,sokf_invisible|sokf_type_barrier_leave,"barrier_16m" ,"bo_barrier_16m" , []),

("ai_limiter_2m" ,sokf_invisible|sokf_type_ai_limiter,"barrier_2m" ,"bo_barrier_2m" , []),
("ai_limiter_4m" ,sokf_invisible|sokf_type_ai_limiter,"barrier_4m" ,"bo_barrier_4m" , []),
("ai_limiter_8m" ,sokf_invisible|sokf_type_ai_limiter,"barrier_8m" ,"bo_barrier_8m" , []),
("ai_limiter_16m",sokf_invisible|sokf_type_ai_limiter,"barrier_16m","bo_barrier_16m", []),
("barrier_player_8m",sokf_invisible|sokf_type_player_limiter|sokf_moveable,"barrier_8m","bo_barrier_8m", []),
("shelves",0,"shelves","boshelves", []),
("table_tavern",0,"table_tavern","botable_tavern", []),
("table_castle_a",0,"table_castle_a","bo_table_castle_a", []),
("chair_castle_a",0,"chair_castle_a","0", []),

("pillow_a",0,"pillow_a","bo_pillow", []),
("pillow_b",0,"pillow_b","bo_pillow", []),
("pillow_c",0,"pillow_c","0", []),

("interior_castle_g_square_keep_b",0,"0","0", []), #unused

("carpet_with_pillows_a",0,"carpet_with_pillows_a","bo_carpet_with_pillows", []),
("carpet_with_pillows_b",0,"carpet_with_pillows_b","bo_carpet_with_pillows", []),
#  ("table_round_a",0,"table_round_a","bo_table_round_a", []),
("table_round_b",0,"table_round_b","bo_table_round_b", []),
("fireplace_b",0,"fireplace_b","bo_fireplace_b", []),
("fireplace_c",0,"fireplace_c","bo_fireplace_c", []),
#  ("sofa_a",0,"sofa_a","bo_sofa", []),
("sofa_b",0,"sofa_b","bo_sofa", []),
("ewer_a",0,"ewer_a_new","bo_ewer_a", []),
("end_table_a",0,"end_table_a","bo_end_table_a", []),

#  ("fake_houses_steppe_a",0,"fake_houses_steppe_a","0", []),
#  ("fake_houses_steppe_b",0,"fake_houses_steppe_b","0", []),
#  ("fake_houses_steppe_c",0,"fake_houses_steppe_c","0", []),

("boat_destroy",0,"boat_destroy","bo_boat_destroy", []),
("destroy_house_a",0,"destroy_house_a","bo_destroy_house_a", []),
  ("destroy_house_a_E",0,"destroy_house_a","0", []),
("destroy_house_b",0,"destroy_house_b","bo_destroy_house_b", []),
  ("destroy_house_b_E",0,"destroy_house_b","0", []),
("destroy_house_c",0,"destroy_house_c","bo_destroy_house_c", []),
  ("destroy_house_c_E",0,"destroy_house_c","0", []),
("destroy_heap",0,"destroy_heap","bo_destroy_heap", []),
  ("destroy_heap_E",0,"destroy_heap","0", []),
("destroy_castle_a",0,"destroy_castle_a","bo_destroy_castle_a", []),
  ("destroy_castle_c_dwarf",0,"destroy_castle_c_dwarf","bo_destroy_castle_c", []),
("destroy_castle_b",0,"destroy_castle_b","bo_destroy_castle_b", []),
  ("destroy_castle_b_E",0,"destroy_castle_b","0", []),
("destroy_castle_c",0,"destroy_castle_c","bo_destroy_castle_c", []),
  ("destroy_castle_c_E",0,"destroy_castle_c","0", []),
("destroy_castle_d",0,"destroy_castle_d","bo_destroy_castle_d", []),
  ("destroy_castle_d_E",0,"destroy_castle_d","0", []),
("destroy_windmill",0,"destroy_windmill","bo_destroy_windmill", []),
  ("destroy_windmill_E",0,"destroy_windmill","0", []),
("destroy_tree_a",0,"destroy_tree_a","bo_destroy_tree_a", []),
  ("destroy_tree_a_E",0,"destroy_tree_a","0", []),
("destroy_tree_b",0,"destroy_tree_b","bo_destroy_tree_b", []),  
  ("destroy_tree_b_E",0,"destroy_tree_b","0", []),  
("destroy_bridge_a",0,"destroy_bridge_a","bo_destroy_bridge_a", []),  
  ("destroy_bridge_a_E",0,"destroy_bridge_a","0", []),  
("destroy_bridge_b",0,"destroy_bridge_b","bo_destroy_bridge_b", []),  
  ("destroy_bridge_b_E",0,"destroy_bridge_b","0", []), 
  
("Catapult",0,"Catapult","bo_Catapult", []),
("broom",0,"broom","0", []),
("garlic",0,"garlic","0", []),
("garlic_b",0,"garlic_b","0", []),

("destroy_a",0,"destroy_a","0", []),
("destroy_b",0,"destroy_b","0", []),

("bridge_wooden",0,"bridge_wooden","bo_bridge_wooden", []),
#  ("bridge_wooden_snowy",0,"bridge_wooden_snowy","bo_bridge_wooden", []),

("grave_a",0,"grave_a","bo_grave_a", []),

("village_house_e",0,"village_house_e","bo_village_house_e", []),
("arabian_house_a2",0,"arabian_house_a2","bo_arabian_house_a2", []),
("village_house_f",0,"village_house_f","bo_village_house_f", []),
("arabian_village_house_a",0,"arabian_village_house_a","bo_arabian_village_house_a", []),
("village_house_g",0,"village_house_g","bo_village_house_g", []),
("arabian_village_house_b",0,"arabian_village_house_b","bo_arabian_village_house_b", []),
("village_house_h",0,"village_house_h","bo_village_house_h", []),
("arabian_village_house_c",0,"arabian_village_house_c","bo_arabian_village_house_c", []),
("village_house_i",0,"village_house_i","bo_village_house_i", []),
("arabian_village_house_d",0,"arabian_village_house_d","bo_arabian_village_house_d", []),
("village_house_j",0,"village_house_j","bo_village_house_j", []),
("arabian_village_stable",0,"arabian_village_stable","bo_arabian_village_stable", []),
("village_wall_a",0,"village_wall_a","bo_village_wall_a", []),
("arabian_village_hut",0,"arabian_village_hut","bo_arabian_village_hut", []),
("village_wall_b",0,"village_wall_b","bo_village_wall_b", []),
("arabian_village_stairs",sokf_type_ladder,"arabian_village_stairs","bo_arabian_village_stairs", []),

("village_snowy_house_a",0,"village_snowy_house_a","bo_village_snowy_house_a", []),
("village_snowy_house_b",0,"village_snowy_house_b","bo_village_snowy_house_b", []),
("village_snowy_house_c",0,"village_snowy_house_c","bo_village_snowy_house_c", []),
("village_snowy_house_d",0,"village_snowy_house_d","bo_village_snowy_house_d", []),
("village_snowy_house_e",0,"village_snowy_house_e","bo_village_snowy_house_e", []),
("village_snowy_house_f",0,"village_snowy_house_f","bo_village_snowy_house_f", []),

#  ("town_house_steppe_a",0,"town_house_steppe_a","bo_town_house_steppe_a", []),
#  ("town_house_steppe_b",0,"town_house_steppe_b","bo_town_house_steppe_b", []),
#  ("town_house_steppe_c",0,"town_house_steppe_c","bo_town_house_steppe_c", []),
#  ("town_house_steppe_d",0,"town_house_steppe_d","bo_town_house_steppe_d", []),
#  ("town_house_steppe_e",0,"town_house_steppe_e","bo_town_house_steppe_e", []),
#  ("town_house_steppe_f",0,"town_house_steppe_f","bo_town_house_steppe_f", []),
#  ("town_house_steppe_g",0,"town_house_steppe_g","bo_town_house_steppe_g", []),
#  ("town_house_steppe_h",0,"town_house_steppe_h","bo_town_house_steppe_h", []),
#  ("town_house_steppe_i",0,"town_house_steppe_i","bo_town_house_steppe_i", []),

#  ("carpet_a",0,"carpet_a","0", []),
#  ("carpet_b",0,"carpet_b","0", []),
#  ("carpet_c",0,"carpet_c","0", []),
#  ("carpet_d",0,"carpet_d","0", []),
#  ("carpet_e",0,"carpet_e","0", []),
("carpet_f",0,"carpet_f_new","bo_carpet_f_new", []),

#  ("awning_a",0,"awning_a","bo_awning", []),
("awning_b",0,"awning_b","bo_awning", []),
#  ("awning_c",0,"awning_c","bo_awning", []),
#  ("awning_long",0,"awning_long","bo_awning_long", []),
#  ("awning_long_b",0,"awning_long_b","bo_awning_long", []),
("awning_d",0,"awning_d","bo_awning_d", []),

("snowy_barrel_a",0,"snowy_barrel_a","bo_snowy_barrel_a", []),
("snowy_fence",0,"snowy_fence","bo_snowy_fence", []),
("snowy_wood_heap",0,"snowy_wood_heap","bo_snowy_wood_heap", []),
("village_snowy_stable_a",0,"village_snowy_stable_a","bo_village_snowy_stable_a", []),
("village_straw_house_a",0,"village_straw_house_a","bo_village_straw_house_a", []),
("awning_long_b",0,"awning_long_b","bo_awning_long", []),
("village_stable_a",0,"village_stable_a","bo_village_stable_a", []),
("awning_long",0,"awning_long","bo_awning_long", []),
("village_shed_a",0,"village_shed_a","bo_village_shed_a", []),
("awning_a",0,"awning_a","bo_awning", []),
("village_shed_b",0,"village_shed_b","bo_village_shed_b", []),
("awning_c",0,"awning_c","bo_awning", []),

# ("trunks_snowy",0,"trunks_snowy","0", []),


("dungeon_door_cell_a",0,"dungeon_door_cell_a","bo_dungeon_door_cell_a", []),
("dungeon_door_cell_b",0,"dungeon_door_cell_b","bo_dungeon_door_cell_b", []),
("dungeon_door_entry_a",0,"dungeon_door_entry_a","bo_dungeon_door_entry_a", []),
("dungeon_door_entry_b",0,"dungeon_door_entry_b","bo_dungeon_door_entry_a", []),
("dungeon_door_entry_c",0,"dungeon_door_entry_c","bo_dungeon_door_entry_a", []),
("dungeon_door_direction_a",0,"dungeon_door_direction_a","bo_dungeon_door_direction_a", []),
("dungeon_door_direction_b",0,"dungeon_door_direction_b","bo_dungeon_door_direction_a", []),
("dungeon_door_stairs_a",0,"dungeon_door_stairs_a","bo_dungeon_door_stairs_a", []),
("dungeon_door_stairs_b",0,"dungeon_door_stairs_b","bo_dungeon_door_stairs_a", []),
("dungeon_bed_a",0,"dungeon_bed_a","0", []),
("dungeon_bed_b",0,"dungeon_bed_b","bo_dungeon_bed_b", []),
("torture_tool_a",0,"torture_tool_a","bo_torture_tool_a", []),
("torture_tool_b",0,"torture_tool_b","0", []),
("torture_tool_c",0,"torture_tool_c","bo_torture_tool_c", []),
("skeleton_head",0,"skeleton_head","0", []),
("skeleton_bone",0,"skeleton_bone","0", []),
("skeleton_a",0,"skeleton_a","bo_skeleton_a", []),
("dungeon_stairs_a",0,"dungeon_stairs_a","bo_dungeon_stairs_a", []),
("dungeon_stairs_b",0,"dungeon_stairs_b","bo_dungeon_stairs_a", []),
("dungeon_torture_room_a",0,"dungeon_torture_room_a","bo_dungeon_torture_room_a", []),
("dungeon_entry_a",0,"dungeon_entry_a","bo_dungeon_entry_a", []),
("dungeon_entry_b",0,"dungeon_entry_b","bo_dungeon_entry_b", []),
("dungeon_entry_c",0,"dungeon_entry_c","bo_dungeon_entry_c", []),
("dungeon_cell_a",0,"dungeon_cell_a","bo_dungeon_cell_a", []),
("dungeon_cell_b",0,"dungeon_cell_b","bo_dungeon_cell_b", []),
("dungeon_cell_c",0,"dungeon_cell_c","bo_dungeon_cell_c", []),
("dungeon_corridor_a",0,"dungeon_corridor_a","bo_dungeon_corridor_a", []),
("dungeon_corridor_b",0,"dungeon_corridor_b","bo_dungeon_corridor_b", []),
("dungeon_corridor_c",0,"dungeon_corridor_c","bo_dungeon_corridor_b", []),
("dungeon_corridor_d",0,"dungeon_corridor_d","bo_dungeon_corridor_b", []),
("dungeon_direction_a",0,"dungeon_direction_a","bo_dungeon_direction_a", []),
("dungeon_direction_b",0,"dungeon_direction_b","bo_dungeon_direction_a", []),
("dungeon_room_a",0,"dungeon_room_a","bo_dungeon_room_a", []),
("dungeon_tower_stairs_a",0,"dungeon_tower_stairs_a","bo_dungeon_tower_stairs_a", []),
("dungeon_tower_cell_a",0,"dungeon_tower_cell_a","bo_dungeon_tower_cell_a", []),
("tunnel_a",0,"new_tunnel_a","bo_new_tunnel_a", []),
("tunnel_salt",0,"new_tunnel_salt2","bo_new_tunnel_salt", []),
("salt_a",0,"salt_a","bo_salt_a", []),

("tutorial_door_a",sokf_moveable,"tutorial_door_a","bo_tutorial_door_a", []),

("tutorial_door_b",sokf_moveable,"tutorial_door_b","bo_tutorial_door_b", []),

("tutorial_flag_yellow",sokf_moveable,"tutorial_flag_yellow","0", []),
("tutorial_flag_red",sokf_moveable,"tutorial_flag_red","0", []),
("tutorial_flag_blue",sokf_moveable,"tutorial_flag_blue","0", []),

("interior_prison_a",0,"interior_prison_a","bo_interior_prison_a", []),
("interior_prison_b",0,"0","0", []),
("interior_prison_cell_a",0,"0","0", []),
#("interior_prison_c",0,"interior_prison_c","bo_interior_prison_c", []),
("interior_prison_d",0,"0","0", []),

("arena_archery_target_a",0,"arena_archery_target_a","bo_arena_archery_target_a", []),
("archery_butt_a",0,"archery_butt","bo_archery_butt", [
   (ti_on_scene_prop_hit,
    [   (store_trigger_param_1, ":instance_no"),
        (ge, "$tutorial_1_state", 1), #only in tutorial mission
        (prop_instance_get_position, pos2, ":instance_no"),
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos3, ":player_agent"),
        (get_distance_between_positions, ":player_distance", pos3, pos2),
        (position_transform_position_to_local, pos4, pos2, pos1),
        (position_set_y, pos4, 0),
        (position_set_x, pos2, 0),
        (position_set_y, pos2, 0),
        (position_set_z, pos2, 0),
        (get_distance_between_positions, ":target_distance", pos4, pos2),
        (assign, ":point_earned", 43), #Calculating a point between 0-12
        (val_sub, ":point_earned", ":target_distance"),
        (val_mul, ":point_earned", 1299),
        (val_div, ":point_earned", 4300),
        (try_begin),
          (lt, ":point_earned", 0),
          (assign, ":point_earned", 0),
        (try_end),
        (val_div, ":player_distance", 91), #Converting to yards
        (assign, reg60, ":point_earned"),
        (assign, reg61, ":player_distance"),
        (display_message, "str_archery_target_hit"),
    ])]),
("archery_target_with_hit_a",0,"arena_archery_target_a","bo_arena_archery_target_a", [
   (ti_on_scene_prop_hit,
    [   (store_trigger_param_1, ":instance_no"),
        (ge, "$tutorial_1_state", 1), #only in tutorial mission
        (prop_instance_get_position, pos2, ":instance_no"),
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos3, ":player_agent"),
        (get_distance_between_positions, ":player_distance", pos3, pos2),
        (position_transform_position_to_local, pos4, pos2, pos1),
        (position_set_y, pos4, 0),
        (position_set_x, pos2, 0),
        (position_set_y, pos2, 0),
        (position_set_z, pos2, 0),
        (get_distance_between_positions, ":target_distance", pos4, pos2),
        (assign, ":point_earned", 43), #Calculating a point between 0-12
        (val_sub, ":point_earned", ":target_distance"),
        (val_mul, ":point_earned", 1299),
        (val_div, ":point_earned", 4300),
        (try_begin),
          (lt, ":point_earned", 0),
          (assign, ":point_earned", 0),
        (try_end),
        (val_div, ":player_distance", 91), #Converting to yards
        (assign, "$g_last_archery_point_earned", ":point_earned"),
        (assign, reg60, ":point_earned"),
        (assign, reg61, ":player_distance"),
        (display_message, "str_archery_target_hit"),
    ])]),
("dummy_a",sokf_destructible|sokf_moveable,"arena_archery_target_b","bo_arena_archery_target_b",   [
   (ti_on_scene_prop_destroy,
    [   (store_trigger_param_1, ":instance_no"),
        (ge, "$tutorial_1_state", 1), #only in tutorial mission
        (prop_instance_get_starting_position, pos1, ":instance_no"),
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, 2, ":player_agent"),
        (assign, ":rotate_side", 80),
        (try_begin),
          (position_is_behind_position, 2, 1),
          (val_mul, ":rotate_side", -1),
        (try_end),
        (position_rotate_x, 1, ":rotate_side"),
        (prop_instance_animate_to_position, ":instance_no", 1, 70), #animate to position 1 in 0.7 second
        (val_add, "$tutorial_num_total_dummies_destroyed", 1),
        (play_sound, "snd_dummy_destroyed"),
    ]),
   (ti_on_scene_prop_hit,
    [   (store_trigger_param_1, ":instance_no"),
        (store_trigger_param_2, ":damage"),
        (store_trigger_param, ":agent", 3),
        (assign, reg60, ":damage"),
        (val_div, ":damage", 8),
        (prop_instance_get_position, pos2, ":instance_no"),
        (get_player_agent_no, ":player_agent"),
        (eq, ":agent", ":player_agent"),
        (agent_get_position, pos3, ":player_agent"),
        (try_begin),
          (position_is_behind_position, pos3, pos2),
          (val_mul, ":damage", -1),
        (try_end),
        (position_rotate_x, 2, ":damage"),
        (display_message, "str_delivered_damage"),
        (prop_instance_animate_to_position, ":instance_no", 2, 30), #animate to position 1 in 0.3 second
        (play_sound, "snd_dummy_hit"),
        #(particle_system_burst, "psys_blood_hit_1", pos1, 100), #littles
        #(particle_system_burst, "psys_blood_hit_2", pos1, 1),   #Massive blood part
        #(particle_system_burst, "psys_blood_hit_3", pos1, 10),   #3-4 part of blood
        #(set_position_delta,0,0,50),
        #(prop_instance_get_position, pos2, ":instance_no"),
        (particle_system_burst, "psys_dummy_smoke", pos1, 3),
        (particle_system_burst, "psys_dummy_straw", pos1, 10),
    ])]),

("band_a",0,"band_a","0", []),
("arena_sign",0,"arena_arms","0", []),

("castle_h_battlement_a",0,"castle_h_battlement_a","bo_castle_h_battlement_a", []),
("castle_h_battlement_c",0,"castle_h_battlement_c","bo_castle_h_battlement_c", []),
("castle_h_battlement_b",0,"castle_h_battlement_b","bo_castle_h_battlement_b", []),
("castle_h_corner_c",0,"castle_h_corner_c","bo_castle_h_corner_c", []),
("castle_h_battlement_a2",0,"castle_h_battlement_a2","bo_castle_h_battlement_a2", []),
("snowy_castle_battlement_b",0,"snowy_castle_battlement_b","bo_snowy_castle_battlement_b", []),
("castle_h_battlement_b2",0,"castle_h_battlement_b2","bo_castle_h_battlement_b2", []),
("snowy_castle_battlement_corner_a",0,"snowy_castle_battlement_corner_a","bo_snowy_castle_battlement_corner_a", []),
("castle_h_corner_a",0,"castle_h_corner_a","bo_castle_h_corner_a", []),
("snowy_castle_battlement_corner_b",0,"snowy_castle_battlement_corner_b","bo_snowy_castle_battlement_corner_b", []),
("castle_h_stairs_a",0,"castle_h_stairs_a","bo_castle_h_stairs_a", []),
("snowy_castle_battlement_corner_c",0,"snowy_castle_battlement_corner_c","bo_snowy_castle_battlement_corner_c", []),
("castle_h_stairs_b",0,"castle_h_stairs_b","bo_castle_h_stairs_b", []),
("snowy_castle_battlement_stairs_a",0,"snowy_castle_battlement_stairs_a","bo_snowy_castle_battlement_stairs_a", []),
("castle_h_gatehouse_a",0,"castle_h_gatehouse_a","bo_castle_h_gatehouse_a", []),
("snowy_castle_battlement_stairs_b",0,"snowy_castle_battlement_stairs_b","bo_snowy_castle_battlement_stairs_b", []),
("castle_h_keep_a",0,"castle_h_keep_a","bo_castle_h_keep_a", []),
("snowy_castle_gate_house_a",0,"snowy_castle_gate_house_a","bo_snowy_castle_gate_house_a", []),
("castle_h_keep_b",0,"castle_h_keep_b","bo_castle_h_keep_b", []),
("snowy_castle_round_tower_a",0,"snowy_castle_round_tower_a","bo_snowy_castle_round_tower_a", []),
("castle_h_house_a",0,"castle_h_house_a","bo_castle_h_house_a", []),
("snowy_castle_square_keep_a",0,"snowy_castle_square_keep_a","bo_snowy_castle_square_keep_a", []),
("castle_h_house_b",0,"castle_h_house_b","bo_castle_h_house_b", []),
("snowy_castle_stairs_a",sokf_type_ladder,"snowy_castle_stairs_a","bo_snowy_castle_stairs_a", []),
("castle_h_house_c",0,"castle_h_house_c","bo_castle_h_house_b", []),
("church_a",0,"church_a","bo_church_a", []),
("castle_h_battlement_barrier",0,"castle_h_battlement_barrier","bo_castle_h_battlement_barrier", []),
("church_tower_a",0,"church_tower_a","bo_church_tower_a", []),
  
("castle_f_keep_a",0,"castle_f_keep_a","bo_castle_f_keep_a", []),
] + (is_a_wb_sceneprop==1 and [
  ("full_keep_b",0,"full_keep_b","bo_full_keep_b", []),
] or [
  ("full_keep_b",0,"castle_f_keep_a","0", []),
]) + [
("castle_f_battlement_a",0,"castle_f_battlement_a","bo_castle_f_battlement_a", []),
("castle_f_battlement_c",0,"castle_f_battlement_c","bo_castle_f_battlement_c", []),
("castle_f_battlement_a_destroyed",0,"castle_f_battlement_a_destroyed","bo_castle_f_battlement_a_destroyed", []),
("castle_f_battlement_d",0,"castle_f_battlement_d","bo_castle_f_battlement_d", []),
("castle_f_battlement_b",0,"castle_f_battlement_b","bo_castle_f_battlement_b", []),
("castle_f_battlement_e",0,"castle_f_battlement_e","bo_castle_f_battlement_e", []),
("castle_f_battlement_corner_a",0,"castle_f_battlement_corner_a","bo_castle_f_battlement_corner_a", []),
("castle_f_battlement_corner_c",0,"castle_f_battlement_corner_c","bo_castle_f_battlement_corner_c", []),
("castle_f_battlement_corner_b",0,"castle_f_battlement_corner_b","bo_castle_f_battlement_corner_b", []),
("castle_f_battlement_d",0,"castle_f_battlement_d","bo_castle_f_battlement_d", []),
("castle_f_stairs_a",0,"castle_f_stairs_a","bo_castle_f_stairs_a", []),
("castle_f_sally_port_elevation",0,"castle_f_sally_port_elevation","bo_castle_f_sally_port_elevation", []),
("castle_f_tower_a",0,"castle_f_tower_a","bo_castle_f_tower_a", []),
("castle_f_door_a",0,"castle_f_tower_a","bo_castle_f_door_a", []),
("castle_f_wall_stairs_a",0,"castle_f_wall_stairs_a","bo_castle_f_wall_stairs_a", []),
("castle_f_sally_door_a",0,"castle_f_sally_door_a","bo_castle_f_sally_door_a", []),
("castle_f_wall_stairs_b",0,"castle_f_wall_stairs_b","bo_castle_f_wall_stairs_b", []),
("castle_f_doors_top_a",0,"castle_f_doors_top_a","bo_castle_f_doors_top_a", []),
("castle_f_wall_way_a",0,"castle_f_wall_way_a","bo_castle_f_wall_way_a", []),
("mosque_a",0,"mosque_a","bo_mosque_a", []),
("castle_f_wall_way_b",0,"castle_f_wall_way_b","bo_castle_f_wall_way_b", []),
("square_keep_b",0,"square_keep_b","bo_square_keep_b", []),
("castle_f_gatehouse_a",0,"castle_f_gatehouse_a","bo_castle_f_gatehouse_a", []),
("square_keep_c",0,"square_keep_c","bo_square_keep_c", []),
#("castle_g_battlement_a",0,"castle_g_battlement_a","bo_castle_g_battlement_a", []),
#("castle_g_corner_a",0,"castle_g_corner_a","bo_castle_g_corner_a", []),
#("castle_g_tower_a",0,"castle_g_tower_a","bo_castle_g_tower_a", []),
#("castle_g_gate_house",0,"castle_g_gate_house","bo_castle_g_gate_house", []),
#("castle_g_gate_house_door_a",0,"castle_g_gate_house_door_a","bo_castle_g_gate_house_door_a", []),
#("castle_g_gate_house_door_b",0,"castle_g_gate_house_door_b","bo_castle_g_gate_house_door_b", []),
#("castle_g_square_keep_a",0,"castle_g_square_keep_a","bo_castle_g_square_keep_a", []),

#("mosque_a",0,"mosque_a","bo_mosque_a", []),
("stone_minaret_a",0,"stone_minaret_a","bo_stone_minaret_a", []),
("square_keep_d",0,"square_keep_d","bo_square_keep_d", []),
#("stone_house_a",0,"stone_house_a","bo_stone_house_a", []),
#("stone_house_b",0,"stone_house_b","bo_stone_house_b", []),
#("stone_house_c",0,"stone_house_c","bo_stone_house_c", []),
#("stone_house_d",0,"stone_house_d","bo_stone_house_d", []),
#("stone_house_e",0,"stone_house_e","bo_stone_house_e", []),
#("stone_house_f",0,"stone_house_f","bo_stone_house_f", []),

("banner_pole", 0, "banner_pole", "bo_banner_pole", []),

("square_keep_e",0,"square_keep_e","bo_square_keep_e", []),
("square_keep_f",0,"square_keep_f","bo_square_keep_f", []),

("banner_a",0,"b_arms_gondor","0", []), #gondor
("banner_b",0,"b_arms_rohan","0", []), #rohan
("banner_c",0,"b_mordor","0", []), #mordor
("banner_d",0,"b_harad","0", []), #harad
("banner_e",0,"b_arms_khand","0", []), #khand
("banner_f",0,"b_rhun","0", []), #rhun
("banner_g",0,"b_arms_umbar","0", []), #umbar
("banner_h",0,"b_arms_lorien","0", []), #lorien
("banner_i",0,"b_arms_imladris","0", []), #imladris
("banner_j",0,"b_arms_woodelf","0", []), #woodelf
("banner_k",0,"b_moria","0", []), #moria
("banner_l",0,"b_guldur","0", []), #guldur
("banner_m",0,"b_beorn","0", []), #beorn
("banner_n",0,"b_gundabad","0", []), #gunda
("banner_o",0,"b_arms_dale","0", []), #dale
("banner_p",0,"b_arms_erebor","0", []), #erebor
("banner_r",0,"b_dunland","0", []), #dunland
("banner_s",0,"b_isengard","0", []), #isengard
# banners B C D not used

("banner_ea",0,"banner_e01","0", []),
("banner_eb",0,"banner_e02","0", []),
("banner_ec",0,"banner_e03","0", []),
("banner_ed",0,"banner_e04","0", []),
("banner_ee",0,"banner_e05","0", []),
("banner_ef",0,"banner_e06","0", []),
("banner_eg",0,"banner_e07","0", []),
("banner_eh",0,"banner_e08","0", []),
("banner_ei",0,"banner_e09","0", []),
("banner_ej",0,"banner_e10","0", []),
("banner_ek",0,"banner_e11","0", []),
("banner_el",0,"banner_e12","0", []),
("banner_em",0,"banner_e13","0", []),
("banner_en",0,"banner_e14","0", []),
("banner_eo",0,"banner_e15","0", []),
("banner_ep",0,"banner_e16","0", []),
("banner_eq",0,"banner_e17","0", []),
("banner_er",0,"banner_e18","0", []),
("banner_es",0,"banner_e19","0", []),
("banner_et",0,"banner_e20","0", []),
("banner_eu",0,"banner_e21","0", []),

("banner_f01", 0, "banner_f01", "0", []),
("banner_f02", 0, "banner_f02", "0", []),
#("banner_f03", 0, "banner_f03", "0", []), #bad banner. others are better and enough for Rohan lords
("banner_f04", 0, "banner_f04", "0", []),
("banner_f05", 0, "banner_f05", "0", []),
("banner_f06", 0, "banner_f06", "0", []),
("banner_f07", 0, "banner_f07", "0", []),
("banner_f08", 0, "banner_f08", "0", []),
("banner_f09", 0, "banner_f09", "0", []),
("banner_f10", 0, "banner_f10", "0", []),
("banner_f11", 0, "banner_f11", "0", []),
("banner_f12", 0, "banner_f12", "0", []),
("banner_f13", 0, "banner_f13", "0", []),
("banner_f14", 0, "banner_f14", "0", []),
("banner_f15", 0, "banner_f15", "0", []),
("banner_f16", 0, "banner_f16", "0", []),
("banner_f17", 0, "banner_f17", "0", []),
("banner_f18", 0, "banner_f18", "0", []),
("banner_f19", 0, "banner_f19", "0", []),
("banner_f21", 0, "b_arms_los", "0", []), #lossarnach
("banner_f20", 0, "banner_f20", "0", []),


("tavern_chair_a",0,"tavern_chair_a","0", []),
("tavern_chair_b",0,"tavern_chair_b","0", []),
("tavern_table_a",0,"tavern_table_a","bo_tavern_table_a", []),
("tavern_table_b",0,"tavern_table_b","bo_tavern_table_b", []),
("fireplace_a",0,"fireplace_a","bo_fireplace_a", []),
("barrel",0,"barrel","bobarrel", []),
("bench_tavern",0,"bench_tavern","0", []),
("bench_tavern_b",0,"bench_tavern_b","0", []),
("bowl_wood",0,"bowl_wood","0", []),
("chandelier_table",0,"chandelier_table","0", []),
#  ("chandelier_tavern",0,"chandelier_tavern","0", []),
("chest_gothic",0,"chest_gothic","bochest_gothic", []),
("chest_b",0,"chest_b","bo_chest_b", []),
("chest_c",0,"chest_c","bo_chest_c", []),
("counter_tavern",0,"counter_tavern","bocounter_tavern", []),
("cup",0,"cup_new","0", []),
("dish_metal",0,"dish_metal_new","0", []),
("gothic_chair",0,"gothic_chair","0", []),
("gothic_stool",0,"gothic_stool","0", []),
("grate",0,"grate_new","bograte", []),
("jug",0,"jug_new","0", []),
("potlamp",0,"potlamp_new","0", []),
("weapon_rack",0,"weapon_rack","boweapon_rack", []),
("weapon_rack_big",0,"weapon_rack_big","boweapon_rack_big", []),
("tavern_barrel",0,"barrel_new","bobarrel", []),
("tavern_barrel_b",0,"tavern_barrel_b","bo_tavern_barrel_b", []),
("merchant_sign",0,"merchant_sign","bo_tavern_sign", []),
("tavern_sign",0,"tavern_sign","bo_tavern_sign", []),
("sack",0,"sack_new","0", []),
("skull_a",0,"skull_a","0", []),
("skull_b",0,"skull_b","0", []),
("skull_c",0,"skull_c","0", []),
("skull_d",0,"skull_d","0", []),
("skeleton_cow",0,"skeleton_cow","0", []),
("cupboard_a",0,"cupboard_a","bo_cupboard_a", []),
("box_a",0,"box_new","bo_box_a", []),
("bucket_a",0,"bucket_a","bo_bucket_a", []),
("straw_a",0,"straw_a","0", []),
("straw_b",0,"straw_b","0", []),
("straw_c",0,"straw_c","0", []),
("cloth_a",0,"cloth_a_new_animated","0", [
 ] + (is_a_wb_sceneprop==1 and [   
 (ti_on_scene_prop_init,[
     (store_trigger_param_1, ":instance_no"),
    (store_random_in_range,":r",0,100), # Random animations time
            (try_begin),
      (ge, ":r", 50),
      (try_begin),
      (ge, ":r", 75),
      (prop_instance_deform_in_cycle_loop, ":instance_no", 1,25, 2000),
      #(display_message, "@cloth_a ANIM + Fast"),
      (else_try),
      (prop_instance_deform_in_cycle_loop, ":instance_no", 1,25, 2500),
      #(display_message, "@cloth_a ANIM + Slow"),
      (try_end),
    (else_try),
    (try_begin),
      (ge, ":r", 25),
     (prop_instance_deform_in_cycle_loop, ":instance_no", 25,1, 2000),
     #(display_message, "@cloth_a ANIM - Fast"),
      (else_try),
      (prop_instance_deform_in_cycle_loop, ":instance_no", 25,1, 2500),
      #(display_message, "@cloth_a ANIM - Slow"),
      (try_end),
    (try_end),
]),
] or []) + [ 
 ]),

("cloth_b",0,"cloth_b_new_animated","0", [
 ] + (is_a_wb_sceneprop==1 and [   
 (ti_on_scene_prop_init,[
     (store_trigger_param_1, ":instance_no"),
    (store_random_in_range,":r",0,100), # Random animations time
            (try_begin),
      (ge, ":r", 50),
      (try_begin),
      (ge, ":r", 75),
      (prop_instance_deform_in_cycle_loop, ":instance_no", 1,25, 2000),
      #(display_message, "@cloth_b ANIM + Fast"),
      (else_try),
      (prop_instance_deform_in_cycle_loop, ":instance_no", 1,25, 3500),
      #(display_message, "@cloth_b ANIM + Slow"),
      (try_end),
    (else_try),
    (try_begin),
      (ge, ":r", 25),
     (prop_instance_deform_in_cycle_loop, ":instance_no", 25,1, 2000),
     #(display_message, "@cloth_b ANIM - Fast"),
      (else_try),
      (prop_instance_deform_in_cycle_loop, ":instance_no", 25,1, 3500),
      #(display_message, "@cloth_b ANIM - Slow"),
      (try_end),
    (try_end),
]),
] or []) + [ 
 ]),
 
("mat_a",0,"mat_a","0", []),
("mat_b",0,"mat_b","0", []),
("mat_c",0,"Gutek_mat_c","0", []),
("mat_d",0,"Gutek_mat_d","0", []),

("wood_a",0,"wood_a","bo_wood_a", []),
  ("wood_a_E",0,"wood_a","0", []),
("wood_b",0,"wood_b","bo_wood_b", []),
  ("wood_b_E",0,"wood_b","0", []),
("wood_heap",0,"Gutek_wood_heap_a","bo_wood_heap_a", []),
  ("wood_heap_E",0,"wood_heap_a","0", []),
("wood_heap_b",0,"wood_heap_b","bo_wood_heap_b", []),
  ("wood_heap_b_E",0,"wood_heap_b","0", []),
("water_well_a",0,"water_well_a","bo_water_well_a", []),
("net_a",0,"net_a","bo_net_a", []),
("net_b",0,"net_b","0", []),

("meat_hook",0,"meat_hook","0", []),
("cooking_pole",0,"cooking_pole","0", []),
("bowl_a",0,"bowl_a","0", []),
("bucket_b",0,"bucket_b","0", []),
("washtub_a",0,"washtub_a_new","bo_washtub_a", []),
("washtub_b",0,"washtub_b_new","bo_washtub_b", []),

("table_trunk_a",0,"table_trunk_a","bo_table_trunk_a", []),
("chair_trunk_a",0,"chair_trunk_a","0", []),
("chair_trunk_b",0,"chair_trunk_b","0", []),
("chair_trunk_c",0,"chair_trunk_c","0", []),

("table_trestle_long",0,"table_trestle_long","bo_table_trestle_long", []),
("table_trestle_small",0,"table_trestle_small","bo_table_trestle_small", []),
("chair_trestle",0,"chair_trestle","0", []),

("wheel",0,"wheel","bowheel", []),
("ladder",0,"ladder","boladder_new", []),
("cart",0,"cart","bo_cart_new", []),
("village_stand",0,"village_stand","bovillage_stand", []),
("wooden_stand",0,"wooden_stand","bowooden_stand", []),
("table_small",0,"table_small","botable_small", []),
("table_small_b",0,"table_small_b","bo_table_small_b", []),
#("small_timber_frame_house_a",0,"small_timber_frame_house_a","bo_small_timber_frame_house_a", []),
#("timber_frame_house_b",0,"tf_house_b","bo_tf_house_b", []),
#("timber_frame_house_c",0,"tf_house_c","bo_tf_house_c", []),
#("timber_frame_extension_a",0,"timber_frame_extension_a","bo_timber_frame_extension_a", []),
#("timber_frame_extension_b",0,"timber_frame_extension_b","bo_timber_frame_extension_b", []),
#("stone_stairs_a",0,"stone_stairs_a","bo_stone_stairs_a", []),
("stone_stairs_b",0,"stone_stairs_b","bo_stone_stairs_b", []),
("railing_a",0,"railing_a","bo_railing_a", []),
#("side_building_a",0,"side_building_a","bo_side_building_a_tld", []),
("battlement_a",0,"battlement_a","bo_battlement_a", []),
("castle_battlement_c",0,"castle_battlement_c","bo_castle_battlement_c", []),
("battlement_a_destroyed",0,"battlement_a_destroyed","bo_battlement_a_destroyed", []),
("castle_battlement_corner_c",0,"castle_battlement_corner_c","bo_castle_battlement_corner_c", []),

("round_tower_a",0,"round_tower_a","bo_round_tower_a", []),
("castle_battlement_c",0,"castle_battlement_c","bo_castle_battlement_c", []),
("small_round_tower_a",0,"small_round_tower_a","bo_small_round_tower_a", []),
("small_round_tower_roof_a",0,"small_round_tower_roof_a","bo_small_round_tower_roof_a", []),
("square_keep_a",0,"square_keep_a","bo_square_keep_a", []),
("square_tower_roof_a",0,"square_tower_roof_a","0", []),
("gate_house_a",0,"gate_house_a","bo_gate_house_a", []),
("castle_battlement_corner_c",0,"castle_battlement_corner_c","bo_castle_battlement_corner_c", []),
("gate_house_b",0,"gate_house_b","bo_gate_house_b", []),
("arena_wall_a",0,"arena_wall_a","bo_arena_wall_ab", []),
("small_wall_a",0,"small_wall_a","bo_small_wall_a", []),
("small_wall_b",0,"small_wall_b","bo_small_wall_b", []),
("small_wall_c",0,"small_wall_c","bo_small_wall_c", []),
  ("small_wall_c_E",0,"small_wall_c","0", []),
("small_wall_c_destroy",0,"small_wall_c_destroy","bo_small_wall_c_destroy", []),
  ("small_wall_c_destroy_E",0,"small_wall_c_destroy","0", []),
("small_wall_d",0,"small_wall_d","bo_small_wall_d", []),
("small_wall_connect_a",0,"small_wall_connect_a","bo_small_wall_connect_a", []),
("small_wall_e",0,"small_wall_e","bo_small_wall_d", []),
("castle_courtyard_house_extension_a",0,"castle_courtyard_house_extension_a","bo_castle_courtyard_house_extension_a", []),

("town_house_a",0,"town_house_a","bo_town_house_a", []),
("castle_courtyard_house_extension_b",0,"castle_courtyard_house_extension_b","bo_castle_courtyard_house_extension_b", []),
("town_house_b",0,"town_house_b","bo_town_house_b", []),
("castle_f_door_a",sokf_moveable|sokf_show_hit_point_bar|sokf_destructible|spr_use_time(0),"castle_f_door_a","bo_castle_f_door_a",  []),
("town_house_c",0,"town_house_c","bo_town_house_c", []),
("castle_e_sally_door_a",sokf_moveable|sokf_show_hit_point_bar|sokf_destructible|spr_use_time(0),"castle_e_sally_door_a","bo_castle_e_sally_door_a",  []),
("town_house_d",0,"town_house_d","bo_town_house_d", []),
("arabian_house_a",0,"arabian_house_a","bo_arabian_house_a", []),
("town_house_e",0,"town_house_e","bo_town_house_e", []),
("arabian_house_b",0,"arabian_house_b","bo_arabian_house_b", []),
("town_house_f",0,"town_house_f","bo_town_house_f", []),
("arabian_house_c",0,"arabian_house_c","bo_arabian_house_c", []),
("town_house_g",0,"town_house_g","bo_town_house_g", []),
("arabian_house_d",0,"arabian_house_d","bo_arabian_house_d", []),
("town_house_h",0,"town_house_h","bo_town_house_h", []),
("arabian_house_e",0,"arabian_house_e","bo_arabian_house_e", []),
("town_house_i",0,"town_house_i","bo_town_house_i", []),
("arabian_house_f",0,"arabian_house_f","bo_arabian_house_f", []),
("town_house_j",0,"town_house_j","bo_town_house_j", []),
("arabian_house_g",0,"arabian_house_g","bo_arabian_house_g", []),
("town_house_l",0,"town_house_l","bo_town_house_l", []),
("arabian_house_h",0,"arabian_house_h","bo_arabian_house_h", []),
("town_house_m",0,"town_house_m","bo_town_house_m", []),
("arabian_house_i",0,"arabian_house_i","bo_arabian_house_i", []),
("town_house_n",0,"town_house_n","bo_town_house_n", []),
("instrument_lyre",0,"lyre","0", []),
("town_house_o",0,"town_house_o","bo_town_house_o", []),
("instrument_lute",0,"lute","0", []),
("town_house_p",0,"town_house_p","bo_town_house_p", []),
("stone_house_a",0,"stone_house_a","bo_stone_house_a", []),
("town_house_q",0,"town_house_q","bo_town_house_q", []),
("stone_house_b",0,"stone_house_b","bo_stone_house_b", []),
#("passage_house_a",0,"passage_house_a","bo_passage_house_a_tld", []),
("passage_house_b",0,"passage_house_b","bo_passage_house_b", []),
("stone_house_c",0,"stone_house_c","bo_stone_house_c", []),
("passage_house_c",0,"passage_house_c","bo_passage_house_c", []),
("stone_house_d",0,"stone_house_d","bo_stone_house_d", []),
#("passage_house_d",0,"passage_house_d","bo_passage_house_d", []),
("passage_house_c_door",0,"passage_house_c_door","bo_passage_house_c_door", []),
("stone_house_e",0,"stone_house_e","bo_stone_house_e", []),
#("house_extension_a",0,"house_extension_a","bo_house_extension_a", []),
#("house_extension_b",0,"house_extension_b","bo_house_extension_b", []),
("house_extension_c",0,"house_extension_c","bo_house_extension_a", []),
("stone_house_f",0,"stone_house_f","bo_stone_house_f", []),
#("house_extension_d",0,"house_extension_d","bo_house_extension_d", []),
#("house_extension_e",0,"house_extension_e","bo_house_extension_e", []),
#("house_extension_f",0,"house_extension_f","bo_house_extension_f", []),
#("house_extension_f2",0,"house_extension_f2","bo_house_extension_f", []),
#("house_extension_g",0,"house_extension_g","bo_house_extension_g", []),
#("house_extension_g2",0,"house_extension_g2","bo_house_extension_g", []),
#("house_extension_h",0,"house_extension_h","bo_house_extension_h", []),

("house_roof_door",0,"house_roof_door","bo_house_roof_door", []),

("door_extension_a",0,"door_extension_a","bo_door_extension_a", []),
("stairs_arch_a",0,"stairs_arch_a","bo_stairs_arch_a", []),
("arena_circle_a",0,"arena_circle_a","bo_arena_circle_a", []),
("town_house_r",0,"town_house_r","bo_town_house_r", []),
("house_extension_e",0,"house_extension_e","bo_house_extension_e", []),
("town_house_s",0,"town_house_s","bo_town_house_s", []),
("house_extension_f",0,"house_extension_f","bo_house_extension_f", []),
("town_house_t",0,"town_house_t","bo_town_house_t", []),
("house_extension_g",0,"house_extension_g","bo_house_extension_g", []),
("town_house_u",0,"town_house_u","bo_town_house_u", []),
("house_extension_h",0,"house_extension_h","bo_house_extension_h", []),
("town_house_v",0,"town_house_v","bo_town_house_v", []),
("house_extension_i",0,"house_extension_i","bo_house_extension_i", []),
("town_house_w",0,"town_house_w","bo_town_house_w", []),
("passage_house_d",0,"passage_house_d","bo_passage_house_d", []),
("town_house_y",0,"town_house_y","bo_town_house_y", []),
("brewery_pool", 0,"brewery_pool","bo_brewery_pool", []), #wb
("town_house_z",0,"town_house_z","bo_town_house_z", []),
("weavery_loom_a",0,"weavery_loom_a","bo_weavery_loom_a", []), #wb
#("town_house_za",0,"town_house_za","bo_town_house_za", []),
  
("windmill",0,"windmill","bo_windmill", []),
("weavery_spinning_wheel",0,"weavery_spinning_wheel","bo_weavery_spinning_wheel", []), #wb
("windmill_fan_turning",sokf_moveable,"windmill_fan_turning","bo_windmill_fan_turning", []),
("windmill_fan",0,"windmill_fan","bo_windmill_fan", []),
("winery_barrel_shelf",0,"winery_barrel_shelf","bo_winery_barrel_shelf", []), #wb
#("fake_house_a",0,"fake_house_a","bo_fake_house_a", []),
#("fake_house_b",0,"fake_house_b","bo_fake_house_b", []),
#("fake_house_c",0,"fake_house_c","bo_fake_house_c", []),
#("fake_house_d",0,"fake_house_d","bo_fake_house_d", []),
#("fake_house_e",0,"fake_house_e","bo_fake_house_e", []),
#("fake_house_f",0,"fake_house_f","bo_fake_house_f", []),

#("fake_house_snowy_a",0,"fake_house_snowy_a","bo_fake_house_a", []),
#("fake_house_snowy_b",0,"fake_house_snowy_b","bo_fake_house_b", []),
#("fake_house_snowy_c",0,"fake_house_snowy_c","bo_fake_house_c", []),
#("fake_house_snowy_d",0,"fake_house_snowy_d","bo_fake_house_d", []),

#("fake_house_far_a",0,"fake_house_far_a","0", []),
#("fake_house_far_b",0,"fake_house_far_b","0", []),
#("fake_house_far_c",0,"fake_house_far_c","0", []),
#("fake_house_far_d",0,"fake_house_far_d","0", []),
#("fake_house_far_e",0,"fake_house_far_e","0", []),
#("fake_house_far_f",0,"fake_house_far_f","0", []),

#("fake_house_far_snowycrude_a",0,"fake_house_far_snowy_a","0", []),
#("fake_house_far_snowy_b",0,"fake_house_far_snowy_b","0", []),
#("fake_house_far_snowy_c",0,"fake_house_far_snowy_c","0", []),
#("fake_house_far_snowy_d",0,"fake_house_far_snowy_d","0", []),

("earth_wall_a",0,"earth_wall_a","bo_earth_wall_a", []),
("earth_wall_b",0,"earth_wall_b","bo_earth_wall_b", []),
("earth_stairs_b",0,"earth_stairs_b","bo_earth_stairs_b", []),
("earth_stairs_a",0,"earth_stairs_a","bo_earth_stairs_a", []),
("earth_tower_small_b",0,"earth_tower_small_b","bo_earth_tower_small_b", []),
("earth_tower_small_a",0,"earth_tower_small_a","bo_earth_tower_small_a", []),
("earth_gate_house_a",0,"earth_gate_house_a","bo_earth_gate_house_a", []),
("earth_gate_house_b",0,"earth_gate_house_b","bo_earth_gate_house_b", []),
("earth_gate_a",0,"earth_gate_a","bo_earth_gate_a", []),
("earth_tower_a",0,"earth_tower_a","bo_earth_tower_a", []),
("earth_square_keep_a",0,"earth_square_keep_a","bo_earth_square_keep_a", []),
("earth_stairs_c",0,"earth_stairs_c","bo_earth_stairs_c", []),
("earth_house_a",0,"earth_house_a","bo_earth_house_a", []),
("earth_sally_gate_right",0,"earth_sally_gate_right","bo_earth_sally_gate_right", []),
("earth_house_b",0,"earth_house_b","bo_earth_house_b", []),
("siege_wall_a",0,"siege_wall_a","bo_siege_wall_a", []), #WB
("earth_house_c",0,"earth_house_c","bo_earth_house_c", []),
("earth_wall_a2",0,"earth_wall_a2","bo_earth_wall_a2", []),
("earth_house_d",0,"earth_house_d","bo_earth_house_d", []),
("earth_wall_b2",0,"earth_wall_b2","bo_earth_wall_b2", []),

#("village_steppe_a",0,"village_steppe_a","bo_village_steppe_a", []),
#("village_steppe_b",0,"village_steppe_b","bo_village_steppe_b", []),
#("village_steppe_c",0,"village_steppe_c","bo_village_steppe_c", []),
#("village_steppe_d",0,"village_steppe_d","bo_village_steppe_d", []),
#("village_steppe_e",0,"village_steppe_e","bo_village_steppe_e", []),
#("village_steppe_f",0,"village_steppe_f","bo_village_steppe_f", []),
("town_house_aa",0,"town_house_aa","bo_town_house_aa", []), #unused?
("siege_large_shield_a",0,"siege_large_shield_a","bo_siege_large_shield_a", []), #WB

("snowy_house_a",0,"snowy_house_a","bo_snowy_house_a", []),
("snowy_house_b",0,"snowy_house_b","bo_snowy_house_b", []),
("snowy_house_c",0,"snowy_house_c","bo_snowy_house_c", []),
("snowy_house_d",0,"snowy_house_d","bo_snowy_house_d", []),
("snowy_house_e",0,"snowy_house_e","bo_snowy_house_e", []),
("snowy_house_f",0,"snowy_house_f","bo_snowy_house_f", []),
("snowy_house_g",0,"snowy_house_g","bo_snowy_house_g", []),
("snowy_house_h",0,"snowy_house_h","bo_snowy_house_h", []),
("snowy_house_i",0,"snowy_house_i","bo_snowy_house_i", []),
#("snowy_wall_a",0,"snowy_wall_a","bo_snowy_wall_a", []),
("snowy_stand",0,"snowy_stand","bo_snowy_stand", []),
("snowy_heap_a",0,"snowy_heap_a","bo_snowy_heap_a", []),
("snowy_trunks_a",0,"snowy_trunks_a","bo_snowy_trunks_a", []),

#("snowy_castle_tower_a",0,"snowy_castle_tower_a","bo_snowy_castle_tower_a", []),
#("snowy_castle_battlement_a",0,"snowy_castle_battlement_a","bo_snowy_castle_battlement_a", []),
#("snowy_castle_battlement_a_destroyed",0,"snowy_castle_battlement_a_destroyed","bo_snowy_castle_battlement_a_destroyed", []),
#("snowy_castle_battlement_b",0,"snowy_castle_battlement_b","bo_snowy_castle_battlement_b", []),
#("snowy_castle_battlement_corner_a",0,"snowy_castle_battlement_corner_a","bo_snowy_castle_battlement_corner_a", []),
#("snowy_castle_battlement_corner_b",0,"snowy_castle_battlement_corner_b","bo_snowy_castle_battlement_corner_b", []),
#("snowy_castle_battlement_stairs_a",0,"snowy_castle_battlement_stairs_a","bo_snowy_castle_battlement_stairs_a", []),
#("snowy_castle_battlement_stairs_b",0,"snowy_castle_battlement_stairs_b","bo_snowy_castle_battlement_stairs_b", []),
#("snowy_castle_gate_house_a",0,"snowy_castle_gate_house_a","bo_snowy_castle_gate_house_a", []),
#("snowy_castle_round_tower_a",0,"snowy_castle_round_tower_a","bo_snowy_castle_round_tower_a", []),
#("snowy_castle_square_keep_a",0,"snowy_castle_square_keep_a","bo_snowy_castle_square_keep_a", []),
#("snowy_castle_stairs_a",0,"snowy_castle_stairs_a","bo_snowy_castle_stairs_a", []),

#("square_keep_b",0,"square_keep_b","bo_square_keep_b", []),
#("square_keep_c",0,"square_keep_c","bo_square_keep_c", []),
#("square_keep_d",0,"square_keep_d","bo_square_keep_d", []),
#("square_keep_e",0,"square_keep_e","bo_square_keep_e", []),
#("square_keep_f",0,"square_keep_f","bo_square_keep_f", []),

("square_stairs_a",0,"square_stairs_a","bo_square_stairs_a", []),
("square_extension_a",0,"square_extension_a","bo_square_extension_a", []),
  
("castle_courtyard_house_a",0,"castle_courtyard_house_a","bo_castle_courtyard_house_a", []),
("courtyard_gate_a",0,"courtyard_entry_a","bo_courtyard_entry_a", []),
("castle_courtyard_house_b",0,"castle_courtyard_house_b","bo_castle_courtyard_house_b", []),
("courtyard_gate_b",0,"courtyard_entry_b","bo_courtyard_entry_b", []),
("castle_courtyard_house_c",0,"castle_courtyard_house_c","bo_castle_courtyard_house_c", []),
("courtyard_gate_c",0,"courtyard_entry_c","bo_courtyard_entry_c", []),
("castle_courtyard_a",0,"castle_courtyard_a","bo_castle_courtyard_a", []),
("courtyard_gate_snowy",0,"courtyard_entry_snowy","bo_courtyard_entry_a", []),
("gatehouse_b",0,"gatehouse_b","bo_gatehouse_b", []),
("castle_e_battlement_a",0,"castle_e_battlement_a","bo_castle_e_battlement_a", []),
("castle_gaillard",0,"castle_gaillard","bo_castle_gaillard", []),
("castle_e_battlement_c",0,"castle_e_battlement_c","bo_castle_e_battlement_c", []),
("castle_e_tower",0,"castle_e_tower","bo_castle_e_tower", []),
("castle_e_battlement_a_destroyed",0,"castle_e_battlement_a_destroyed","bo_castle_e_battlement_a_destroyed", []),
("stand_thatched",0,"stand_thatched","bo_stand_thatched", []),
#("stand_cloth",0,"stand_cloth","bo_stand_cloth", []),

("arena_block_c",0,"arena_block_c","bo_arena_block_c", []),
("castle_e_corner",0,"castle_e_corner","bo_castle_e_corner", []),
("arena_block_f",0,"arena_block_f","bo_arena_block_def", []),
("castle_e_corner_b",0,"castle_e_corner_b","bo_castle_e_corner_b", []),
("arena_block_i",0,"arena_block_i","bo_arena_block_ghi", []),
("castle_e_corner_c",0,"castle_e_corner_c","bo_castle_e_corner_c", []),

("arena_palisade_a",0,"arena_palisade_a_new","bo_arena_palisade_a_new", []),
("castle_e_gate_house_a",0,"castle_e_gate_house_a","bo_castle_e_gate_house_a", []),
("arena_barrier_a",0,"arena_barrier_a_new","bo_arena_barrier_a_new", []),
("castle_e_keep_a",0,"castle_e_keep_a","bo_castle_e_keep_a", []),
("arena_barrier_b",0,"arena_barrier_b_new","bo_arena_barrier_bc_new", []),
("castle_e_house_a",0,"castle_e_house_a","bo_castle_e_house_a", []),
("arena_tower_c",0,"arena_tower_c","bo_arena_tower_abc", []),
("castle_e_house_b",0,"castle_e_house_b","bo_castle_e_house_b", []),
("arena_spectator_a",0,"arena_spectator_a","0", []),
("arena_spectator_b",0,"arena_spectator_b","0", []),
("arena_spectator_c",0,"arena_spectator_c","0", []),
("arena_spectator_sitting_a",0,"arena_spectator_sitting_a","0", []),
("arena_spectator_sitting_b",0,"arena_spectator_sitting_b","0", []),
("arena_spectator_sitting_c",0,"arena_spectator_sitting_c","0", []),

#("castle_tower_a",0,"castle_tower_a","bo_castle_tower_a", []),
("castle_battlement_a",0,"castle_battlement_a","bo_castle_battlement_a", []),
("castle_battlement_b",0,"castle_battlement_b","bo_castle_battlement_b", []),
("castle_battlement_a_destroyed",0,"castle_battlement_a_destroyed","bo_castle_battlement_a_destroyed", []),
("castle_battlement_b_destroyed",0,"castle_battlement_b_destroyed","bo_castle_battlement_b_destroyed", []),
("castle_battlement_corner_a",0,"castle_battlement_corner_a","bo_castle_battlement_corner_a", []),
("castle_battlement_corner_b",0,"castle_battlement_corner_b","bo_castle_battlement_corner_b", []),
("castle_battlement_stairs_a",0,"castle_battlement_stairs_a","bo_castle_battlement_stairs_a", []),
("castle_battlement_stairs_b",0,"castle_battlement_stairs_b","bo_castle_battlement_stairs_b", []),
("castle_gate_house_a",0,"castle_gate_house_a","bo_castle_gate_house_a", []),
("castle_round_tower_a",0,"castle_round_tower_a","bo_castle_round_tower_a", []),
("castle_square_keep_a",0,"castle_square_keep_a","bo_castle_square_keep_a", []),
("castle_stairs_a",0,"castle_stairs_a","bo_castle_stairs_a", []),

("castle_drawbridge_open",0,"castle_drawbridges_open","bo_castle_drawbridges_open", []),
("castle_drawbridge_closed",0,"castle_drawbridges_closed","bo_castle_drawbridges_closed", []),
("spike_group_a",0,"spike_group_a","bo_spike_group_a", []),
("spike_a",0,"spike_a","bo_spike_a", []),
("belfry_a",sokf_moveable,"belfry_a","bo_belfry_a", []),
#("belfry_old",0,"belfry_a","bo_belfry_a", []),
("belfry_platform_a",sokf_moveable,"belfry_platform_a","bo_belfry_platform_a", []),
("belfry_platform_b",sokf_moveable,"belfry_platform_b","bo_belfry_platform_b", []),
("belfry_platform_old",0,"belfry_platform_b","bo_belfry_platform_b", []),
("belfry_wheel",sokf_moveable,"belfry_wheel",0, []),
("belfry_wheel_old",0,"belfry_wheel",0, []),

("mangonel",0,"mangonel","bo_mangonel", []),
#("trebuchet_old",0,"trebuchet_old","bo_trebuchet_old", []),
("trebuchet_new",0,"trebuchet_new","bo_trebuchet_old", []),
("stone_ball",0,"stone_ball","0", []),

("village_house_a",0,"village_house_a","bo_village_house_a", []),
("village_wall_manger",0,"wall_manger_a","bo_wall_manger_a", []),
("village_house_b",0,"village_house_b","bo_village_house_b", []),
("granary_a",0,"granary_a","bo_granary_a", []),
("village_house_c",0,"village_house_c","bo_village_house_c", []),
("full_stable_a",0,"full_stable_a","bo_full_stable_a", []),
("village_house_d",0,"village_house_d","bo_village_house_d", []),
("full_stable_b",0,"full_stable_b","bo_full_stable_b", []),
("farm_house_a",0,"farm_house_a","bo_farm_house_a", []),
("full_stable_c",0,"full_stable_c","bo_full_stable_c", []),
("farm_house_b",0,"farm_house_b","bo_farm_house_b", []),
("full_stable_d",0,"full_stable_d","bo_full_stable_d", []),
("farm_house_c",0,"farm_house_c","bo_farm_house_c", []),
("village_steppe_a",0,"village_steppe_a","bo_village_steppe_a", []),
("mountain_house_a",0,"mountain_house_a","bo_mountain_house_a", []),
("village_steppe_b",0,"village_steppe_b","bo_village_steppe_b", []),
("mountain_house_b",0,"mountain_house_b","bo_mountain_house_b", []),
("village_steppe_c",0,"village_steppe_c","bo_village_steppe_c", []),
("village_hut_a",0,"village_hut_a","bo_village_hut_a", []),
("village_steppe_d",0,"village_steppe_d","bo_village_steppe_d", []),
("crude_fence",0,"fence","bo_fence", []),
("crude_fence_curved",0,"fence_curved","bo_fence_curved", []),
("crude_fence_small",0,"crude_fence_small","bo_crude_fence_small", []),
 ("crude_fence_small_E",0,"crude_fence_small",0, []),
("crude_fence_small_b",0,"crude_fence_small_b","bo_crude_fence_small_b", []),
 ("crude_fence_small_b_E",0,"crude_fence_small_b",0, []),

("ramp_12m",0,"ramp_12m","bo_ramp_12m", []),
("ramp_14m",0,"ramp_14m","bo_ramp_14m", []),

("siege_ladder_12m",0,"siege_leadder_12m","bo_siege_leadder_12m", []),
("siege_ladder_14m",0,"siege_ladder_evil_14m","bo_siege_leadder_14m", []),

("portcullis",0,"portcullis_a","bo_portcullis_a", []),
("portcullis_new",0,"portculis_new","bo_portcullis_a", []), #WB
("bed_a",0,"bed_a","bo_bed_a", []),
("bed_b",0,"bed_b","bo_bed_b", []),
("bed_c",0,"bed_c","bo_bed_c", []),
("bed_d",0,"bed_d","bo_bed_d", []),
("bed_e",0,"bed_e","bo_bed_e", []),

("bed_f",0,"bed_f","bo_bed_f", []),

("towngate_door_left",0,"door_g_left","bo_door_left", []),
("towngate_door_right",0,"door_g_right","bo_door_right", []),
("towngate_rectangle_door_left",0,"towngate_rectangle_door_left","bo_towngate_rectangle_door_left", []),
("towngate_rectangle_door_right",0,"towngate_rectangle_door_right","bo_towngate_rectangle_door_right", []),

("door_screen",0,"door_screen_new","0", []),
("door_a",0,"door_a","bo_door_a", []),
("door_b",0,"door_b","bo_door_a", []),
("door_c",0,"door_c","bo_door_a", []),
("door_d",0,"door_d","bo_door_a", []),
("tavern_door_a",0,"tavern_door_a","bo_tavern_door_a", []),
("tavern_door_b",0,"tavern_door_b","bo_tavern_door_a", []),
("door_e_left",0,"door_e_left","bo_door_left", []),
("door_e_right",0,"door_e_right","bo_door_right", []),
("door_f_left",0,"door_f_left","bo_door_left", []),
("door_f_right",0,"door_f_right","bo_door_right", []),
("door_h_left",0,"door_g_left","bo_door_left", []),
("door_h_right",0,"door_g_right","bo_door_right", []),
("draw_bridge_a",0,"draw_bridge_a","bo_draw_bridge_a", []),
("chain_1m",0,"chain_1m","0", []),
("chain_2m",0,"chain_2m","0", []),
("chain_5m",0,"chain_5m","0", []),
("chain_10m",0,"chain_10m","0", []),
("bridge_modular_a",0,"bridge_modular_a","bo_bridge_modular_a", []),
("village_steppe_e",0,"village_steppe_e","bo_village_steppe_e", []),
("bridge_modular_b",0,"bridge_modular_b","bo_bridge_modular_b", []),
("village_steppe_f",0,"village_steppe_f","bo_village_steppe_f", []), 
("stone_step_a",0,"floor_stone_a","bo_floor_stone_a", []),
("stone_step_b",0,"stone_step_b_new","0", []),
("stone_step_c",0,"stone_step_c_new","0", []),
("stone_heap",0,"stone_heap","bo_stone_heap", []),
("stone_heap_b",0,"stone_heap_b","bo_stone_heap", []),

#("panel_door_a",0,"house_door_a","bo_house_door_a", []),
#("panel_door_b",0,"house_door_b","bo_house_door_a", []),
("smoke_stain",0,"soot_a_new","0", []),
("brazier_with_fire",0,"brazier_new","bo_brazier",    [
  (ti_on_scene_prop_init,
  [   (set_position_delta,0,0,85),
    (particle_system_add_new, "psys_brazier_fire_1"),
    (particle_system_add_new, "psys_fire_sparks_1"),
    (set_position_delta,0,0,100),
    (particle_system_add_new, "psys_fire_glow_1"),
    (particle_system_emit, "psys_fire_glow_1",9000000),
    #(particle_system_add_new, "psys_fire_glow_1"),
    #(set_position_delta,0,0,95),
    #(particle_system_add_new, "psys_cooking_smoke"),
     ] + (is_a_wb_sceneprop==1 and [   
    (store_trigger_param_1, ":instance_no"),
    (scene_prop_set_slot, ":instance_no", slot_prop_sound, "snd_torch_loop"),
    ] or []) + [ 
  ]),
]),
("cooking_fire",0,"fire_floor","0",
   [(ti_on_scene_prop_init,
    [   (set_position_delta,0,0,12),
        (particle_system_add_new, "psys_cooking_fire_1"),
        (particle_system_add_new, "psys_fire_sparks_1"),
        (particle_system_add_new, "psys_cooking_smoke"),
        (set_position_delta,0,0,50),
        (particle_system_add_new, "psys_fire_glow_1"),
        (particle_system_emit, "psys_fire_glow_1",9000000),
        ] + (is_a_wb_sceneprop==1 and [   
        (store_trigger_param_1, ":instance_no"),
        (scene_prop_set_slot, ":instance_no", slot_prop_sound, "snd_torch_loop"),
        ] or []) + [ 
    ]),
]),
("cauldron_a",0,"cauldron_a","bo_cauldron_a", []),
("fry_pan_a",0,"fry_pan_a","0", []),

# Mark7's Dynamic Props
("tripod_cauldron_a",0,"tripod_cauldron_a_new","bo_tripod_cauldron_a", [
    ] + (is_a_wb_sceneprop==1 and [  
     (ti_on_scene_prop_init,[
         (store_trigger_param_1, ":instance_no"),
        (store_random_in_range,":r",0,100), # Random animations time
				(try_begin),
          (ge, ":r", 50),
          (try_begin),
          (ge, ":r", 75),
          (prop_instance_deform_in_cycle_loop, ":instance_no", 1,24, 3000),
          #(display_message, "@tripod_cauldron_a ANIM + Fast"),
          (else_try),
          (prop_instance_deform_in_cycle_loop, ":instance_no", 1,24, 4000),
          #(display_message, "@tripod_cauldron_a ANIM + Slow"),
          (try_end),
        (else_try),
        (try_begin),
          (ge, ":r", 25),
         (prop_instance_deform_in_cycle_loop, ":instance_no", 24,1, 3000),
         #(display_message, "@tripod_cauldron_a ANIM - Fast"),
          (else_try),
          (prop_instance_deform_in_cycle_loop, ":instance_no", 24,1, 4000),
          #(display_message, "@tripod_cauldron_a ANIM - Slow"),
          (try_end),
        (try_end),
    ]),
    ] or []) + [ 
     ]),
("tripod_cauldron_b",0,"tripod_cauldron_b_new","bo_tripod_cauldron_b", [
     ] + (is_a_wb_sceneprop==1 and [  
     (ti_on_scene_prop_init,[
         (store_trigger_param_1, ":instance_no"),
        (store_random_in_range,":r",0,100), # Random animations time
				(try_begin),
          (ge, ":r", 50),
          (try_begin),
          (ge, ":r", 75),
          (prop_instance_deform_in_cycle_loop, ":instance_no", 1,24, 3000),
          #(display_message, "@tripod_cauldron_b ANIM + Fast"),
          (else_try),
          (prop_instance_deform_in_cycle_loop, ":instance_no", 1,24, 4000),
          #(display_message, "@tripod_cauldron_b ANIM + Slow"),
          (try_end),
        (else_try),
        (try_begin),
          (ge, ":r", 25),
         (prop_instance_deform_in_cycle_loop, ":instance_no", 24,1, 3000),
         #(display_message, "@tripod_cauldron_b ANIM - Fast"),
          (else_try),
          (prop_instance_deform_in_cycle_loop, ":instance_no", 24,1, 4000),
          #(display_message, "@tripod_cauldron_b ANIM - Slow"),
          (try_end),
        (try_end),
    ]),
    ] or []) + [ 
     ]),
# Mark7's Dynamic Props end     
    
("open_stable_a",0,"Gutek_open_stable_a","bo_open_stable_a", []),
("open_stable_b",0,"Gutek_open_stable_b","bo_open_stable_b", []),
("plate_a",0,"plate_a","0", []),
("plate_b",0,"plate_b","0", []),
("plate_c",0,"plate_c","0", []),
("lettuce",0,"lettuce","0", []),
("hanger",0,"hanger","0", []),
("knife_eating",0,"knife_eating","0", []),
("colander",0,"colander","0", []),
("ladle",0,"ladle","0", []),
("spoon",0,"spoon","0", []),
("skewer",0,"skewer","0", []),
("grape_a",0,"grape_a","0", []),
("grape_b",0,"grape_b","0", []),
("apple_a",0,"apple_a","0", []),
("apple_b",0,"apple_b","0", []),
("maize_a",0,"maize_a","0", []),
("maize_b",0,"maize_b","0", []),
("cabbage",0,"cabbage","0", []),
("athelas_plant",0,"athelas_plant","0", []),
("galadriel_light",0,"galadriel_light","0", []),
("middle_earth_map",0,"middle_earth_map","0", []),

("cabbage_b",0,"cabbage_b","0", []),
("bean",0,"bean","0", []),
("basket_a",0,"basket_a","bo_basket_a", []),
("feeding_trough_a",0,"feeding_trough_a","bo_feeding_trough_a", []),

("marrow_a",0,"marrow_a","0", []),
("marrow_b",0,"marrow_b","0", []),
("squash_plant",0,"marrow_c","0", []),

("cheese_a",0,"cheese_a","0", []),
("cheese_b",0,"cheese_b","0", []),
("cheese_slice_a",0,"cheese_slice_a","0", []),
("bread_a",0,"bread_a","0", []),
("bread_b",0,"bread_b","0", []),
("bread_slice_a",0,"bread_slice_a","0", []),
("fish_a",0,"fish_a","0", []),
("fish_roasted_a",0,"fish_roasted_a","0", []),
("chicken_roasted",0,"chicken_roasted","0", []),
("food_steam",0,"0","0",
   [(ti_on_scene_prop_init,
    [(set_position_delta,0,0,0),
     (particle_system_add_new, "psys_food_steam"),
    ]),
   ]),
  ########################
  ("city_smoke",0,"0","0",
   [(ti_on_scene_prop_init,
    [(store_time_of_day,reg(12)),
     (neg|is_between,reg(12),5,20),
     (set_position_delta,0,0,0),
     (particle_system_add_new, "psys_night_smoke_1"),
    ]),
   ]),
   ("city_fire_fly_night",0,"0","0",
   [(ti_on_scene_prop_init,
    [(store_time_of_day,reg(12)),
     (neg|is_between,reg(12),5,20),
     (set_position_delta,0,0,0),
     (particle_system_add_new, "psys_fire_fly_1"),
    ]),
   ]),
("city_fly_day",0,"0","0",[(ti_on_scene_prop_init,[(particle_system_add_new, "psys_bug_fly_1"),])]),
("flue_smoke_tall",0,"0","0",[(ti_on_scene_prop_init,[(particle_system_add_new, "psys_flue_smoke_tall")])]),
("flue_smoke_short",0,"0","0",[(ti_on_scene_prop_init,[(particle_system_add_new, "psys_flue_smoke_short")])]),
("moon_beam",0,"0","0",[(ti_on_scene_prop_init,
    [(particle_system_add_new, "psys_moon_beam_1"),
    #(particle_system_add_new, "psys_moon_beam_paricle_1") #separate prop now
    ])]),
("fire_small",0,"0","0",[(ti_on_scene_prop_init,[(particle_system_add_new, "psys_fireplace_fire_small")])]),
("fire_big",0,"0","0",[(ti_on_scene_prop_init,[(particle_system_add_new, "psys_fireplace_fire_big")])]),
("battle_field_smoke",0,"0","0",[(ti_on_scene_prop_init,[(particle_system_add_new, "psys_war_smoke_tall")])]),
("Village_fire_big",0,"0","0",
   [(ti_on_scene_prop_init,
    [(particle_system_add_new, "psys_village_fire_big"),
     (set_position_delta,0,0,100),
     (particle_system_add_new, "psys_village_fire_smoke_big"),
    ]),
]),
#########################
("candle_a",0,"candle_a","0",[(ti_on_scene_prop_init,[(set_position_delta,0,0,27),(particle_system_add_new, "psys_candle_light")])]),
("candle_b",0,"candle_b","0",[(ti_on_scene_prop_init,[(set_position_delta,0,0,25),(particle_system_add_new, "psys_candle_light")])]),
("candle_c",0,"candle_c","0",[(ti_on_scene_prop_init,[(set_position_delta,0,0,10),(particle_system_add_new, "psys_candle_light_small")])]),
("lamp_a",0,"lamp_a_new","0",[(ti_on_scene_prop_init,[(set_position_delta,66,0,2),(particle_system_add_new, "psys_candle_light")])]),
("lamp_b",0,"lamp_b_new","0",[(ti_on_scene_prop_init,
    [(set_position_delta,65,0,-7),
     (particle_system_add_new, "psys_lamp_fire"),
     (set_position_delta,70,0,-5),
     (particle_system_add_new, "psys_fire_glow_1"),
     (particle_system_emit, "psys_fire_glow_1",9000000),
     #(play_sound, "snd_torch_loop", 0), #InVain: disabled to prevent sound overflow
         ] + (is_a_wb_sceneprop==1 and [   
        (store_trigger_param_1, ":instance_no"),
        (scene_prop_set_slot, ":instance_no", slot_prop_sound, "snd_torch_loop"),
        ] or []) + [ 
    ]),
]),

("hook_a",0,"hook_a_new","0", []),
("window_night",0,"window_night","0", []),
("fried_pig",0,"fried_pig","0", []),
("village_oven",0,"village_oven","bo_village_oven", []),
("dungeon_water_drops",0,"0","0",
   [(ti_on_scene_prop_init,
    [(particle_system_add_new, "psys_dungeon_water_drops"),
    ]),
   ]),
("shadow_circle_1",0,"shadow_circle_1","0", []),
("shadow_circle_2",0,"shadow_circle_2","0", []),
("shadow_square_1",0,"shadow_square_1","0", []),
("shadow_square_2",0,"shadow_square_2","0", []),
("wheelbarrow",0,"wheelbarrow","bo_wheelbarrow", []),
("gourd",sokf_destructible|spr_hit_points(1),"gourd","bo_gourd",
   [(ti_on_scene_prop_destroy,
      [ (store_trigger_param_1, ":instance_no"),
        #(val_add, "$g_last_destroyed_gourds", 1),
        (prop_instance_get_position, pos1, ":instance_no"),
        (copy_position, pos2, pos1),
        (position_set_z, pos2, -100000),
        (particle_system_burst, "psys_gourd_smoke", pos1, 2),
        (particle_system_burst, "psys_gourd_piece_1", pos1, 1),
        (particle_system_burst, "psys_gourd_piece_2", pos1, 5),
        (prop_instance_animate_to_position, ":instance_no", pos2, 1),
        (play_sound, "snd_dummy_destroyed"),
  ])]),

("gourd_spike",0,"gourd_spike","bo_gourd_spike",[]),

("obstacle_fence_1",0,"fence","bo_fence", []),
("obstacle_fallen_tree_a",0,"destroy_tree_a","bo_destroy_tree_a_new", []), #high-res collision
("obstacle_fallen_tree_b",0,"destroy_tree_b","bo_destroy_tree_b_new", []), #high-res collision  

#####TLD SCENE PROPS##########
("invisible_pillar",0,"invisible_pillar","bo_invisible_pillar", []), # useful to block player out of forbidden zones
 
##GONDOR#####
("gon_castle_h_battlement_a",0,"gon_castle_h_battlement_a","bo_castle_h_battlement_a_tld", []),
("arabian_castle_battlement_a",0,"arabian_castle_battlement_a","bo_arabian_castle_battlement_a", []),
("gon_castle_h_battlement_b",0,"gon_castle_h_battlement_b","bo_castle_h_battlement_b", []),
("arabian_castle_battlement_b_destroyed",0,"arabian_castle_battlement_b_destroyed","bo_arabian_castle_battlement_b_destroyed", []),
("gon_castle_h_battlement_a2",0,"gon_castle_h_battlement_a2","bo_castle_h_battlement_a_tld", []),
("arabian_castle_battlement_c",0,"arabian_castle_battlement_c","bo_arabian_castle_battlement_c", []),
("gon_castle_h_battlement_b2",0,"gon_castle_h_battlement_b2","bo_castle_h_battlement_b2", []),
("arabian_castle_battlement_d",0,"arabian_castle_battlement_d","bo_arabian_castle_battlement_d", []),
("gon_castle_h_corner_a",0,"gon_castle_h_corner_a","bo_castle_h_corner_a", []),
("arabian_castle_corner_a",0,"arabian_castle_corner_a","bo_arabian_castle_corner_a", []),
("gon_castle_h_stairs_a",0,"gon_castle_h_stairs_a","bo_castle_h_stairs_a_tld", []),
("arabian_castle_stairs",sokf_type_ladder,"arabian_castle_stairs","bo_arabian_castle_stairs", []),
("gon_castle_h_stairs_b",0,"gon_castle_h_stairs_b","bo_castle_h_stairs_b", []),
("arabian_castle_stairs_b",sokf_type_ladder,"arabian_castle_stairs_b","bo_arabian_castle_stairs_b", []),
("gon_castle_h_gatehouse_a",0,"gon_castle_h_gatehouse_a","bo_castle_h_gatehouse_a_tld", []),
("arabian_castle_stairs_c",sokf_type_ladder,"arabian_castle_stairs_c","bo_arabian_castle_stairs_c", []),
("gon_castle_h_keep_a",0,"gon_castle_h_keep_a","bo_castle_h_keep_a", []),
("arabian_castle_battlement_section_a",0,"arabian_castle_battlement_section_a","bo_arabian_castle_battlement_section_a", []),
("gon_castle_h_keep_b",0,"gon_castle_h_keep_b","bo_castle_h_keep_b", []),
("arabian_castle_gate_house_a",0,"arabian_castle_gate_house_a","bo_arabian_castle_gate_house_a", []),
("gon_castle_h_house_a",0,"gon_castle_h_house_a","bo_castle_h_house_a", []),
("arabian_castle_house_a",0,"arabian_castle_house_a","bo_arabian_castle_house_a", []),
("gon_castle_h_house_b",0,"gon_castle_h_house_b","bo_castle_h_house_b", []),
("arabian_castle_house_b",0,"arabian_castle_house_b","bo_arabian_castle_house_b", []),
("gon_castle_h_house_c",0,"gon_castle_h_house_c","bo_castle_h_house_b", []),
("arabian_castle_keep_a",0,"arabian_castle_keep_a","bo_arabian_castle_keep_a", []),
("gon_castle_h_battlement_barrier",0,"gon_castle_h_battlement_barrier","bo_castle_h_battlement_barrier", []),
  ("gon_castle_h_battlement_barrier_E",0,"gon_castle_h_battlement_barrier","0", []),

("gon_small_wall_d",0,"gon_small_wall_d","bo_small_wall_d", []),
  ("gon_small_wall_d_E",0,"gon_small_wall_d","0", []),
("gon_small_wall_e",0,"gon_small_wall_e","bo_small_wall_d", []),
  ("gon_small_wall_e_E",0,"gon_small_wall_e","0", []),
("gon_upper_apt",0,"gon_upper_apt_a","0", []),
  ("gon_upper_apt_E",0,"gon_upper_apt_a","0", []),

##GONDOR RUINS###
("gon_ruined_wall_a",0,"ruined_wall","bo_ruined_wall", []),
("gon_ruined_castle_b",0,"gon_destroy_castle_b","bo_destroy_castle_b", []),
("gon_ruined_arch",0,"ruined_arch","bo_ruined_arch", []),
("gon_ruined_small_wall_c",0,"gon_small_wall_c","bo_small_wall_c", []),
("gon_ruined_stone",0,"ruined_stone","bo_ruined_stone", []),
("gon_ruined_stone_heap",0,"gon_stone_heap","bo_stone_heap", []),
("gon_ruined_debris_a",0,"ruined_debris_a","bo_ruined_debris_a", []),
  ("gon_ruined_debris_a_E",0,"ruined_debris_a","0", []),
("gon_ruined_debris_b",0,"ruined_debris_b","bo_ruined_debris_b", []),
  ("gon_ruined_debris_b_E",0,"ruined_debris_b","0", []),
("gon_ruined_debris_c",0,"ruined_debris_c","bo_ruined_debris_c", []),
  ("gon_ruined_debris_c_E",0,"ruined_debris_c","0", []),
("gon_ruined_door",0,"ruined_door","bo_ruined_door", []),
("gon_ruined_stone_step_b",0,"gon_stone_step_b","0", []),
("gon_ruined_stairs_a",0,"ruined_stairs_a","bo_ruined_stairs_a", []),
("gon_ruined_small_wall_destroy",0,"gon_small_wall_c_destroy","bo_small_wall_c_destroy", []),
("gon_ruined_stairs_b",0,"ruined_stairs_b","bo_ruined_stairs_b", []),
  ("gon_ruined_stairs_b_E",0,"ruined_stairs_b","0", []),
("gon_ruined_pillar",0,"ruined_pillar","bo_ruined_pillar", []),
  ("gon_ruined_pillar_E",0,"ruined_pillar","0", []),
("gon_ruined_arches",0,"ruined_arches","bo_ruined_arches", []),
("gon_ruined_castle_d",0,"gon_destroy_castle_d","bo_destroy_castle_d", []),
("gon_ruined_house_a",0,"ruined_house_a","bo_ruined_house_a", []),
("gon_ruined_house_d",0,"gon_destroy_house_a","bo_destroy_house_a", []),
("gon_ruined_house_b",0,"ruined_house_b","bo_ruined_house_b", []),
("gon_ruined_house_e",0,"gon_destroy_house_b","bo_destroy_house_b", []),
("gon_ruined_house_c",0,"ruined_house_c","bo_ruined_house_c", []),
("gon_ruined_house_c_E",0,"ruined_house_c","0", []),
("gon_ruined_battlement",0,"ruined_battlement","bo_ruined_battlement", []),
("gon_ruined_castle_battlement",0,"gon_castle_e_battlement_a_destroyed","bo_castle_e_battlement_a_destroyed", []),
("gon_ruined_tower",0,"ruined_tower","bo_ruined_tower", []),
("gon_ruined_castle_c",0,"gon_destroy_castle_c","bo_destroy_castle_c", []),
("gon_ruined_wallgate",0,"ruined_wallgate","bo_ruined_wallgate", []),
("gon_ruined_castle_a",0,"gon_destroy_castle_a","bo_destroy_castle_a", []),
("gon_ruined_bridge_a",0,"ruined_bridge_a","bo_ruined_bridge_a", []),
("gon_ruined_tower_b",0,"gon_ruins_tower","bo_ruins_tower", []),
("gon_ruined_bridge_b",0,"ruined_bridge_b","bo_ruined_bridge_b", []),
  ("gon_ruined_bridge_b_E",0,"ruined_bridge_b","0", []),
("gon_ruined_fem",0,"statue_female_ruined","bo_statue_female_marble", []),
  ("gon_ruined_fem_E",0,"statue_female_ruined","0", []),
("gon_statue_fem",0,"statue_female_marble","bo_statue_female_marble", []),
  ("gon_statue_fem_E",0,"statue_female_marble","0", []),
("gon_ruined_warrior",0,"statue_warrior_ruined","bo_statue_ruined_warrior", []),
  ("gon_ruined_warrior_E",0,"statue_warrior_ruined","0", []),
("gon_statue_warrior",0,"statue_warrior_marble","bo_statue_ruined_warrior", []),
  ("gon_statue_warrior_E",0,"statue_warrior_marble","0", []),
("gon_statue_king_a",0,"statue_gondor1","bo_statue_gondor", []),
("gon_statue_king_b",0,"statue_gondor2","bo_statue_gondor", []),
("gon_statue_king_c",0,"gondor_king1","bo_gondor_king", []),
("gon_statue_king_d",0,"gondor_king2","bo_gondor_king", []),
("gon_statue_king_e",0,"gondor_king3","bo_gondor_king", []),
  
###GONDOR - LLEW#####
("gondor_colonnade_1",0,"gondor_colonnade_1","bo_gondor_colonnade_1", []),
  ("gondor_colonnade_1_E",0,"gondor_colonnade_1","0", []),
("gondor_colonnade_corner_1",0,"gondor_colonnade_corner_1","bo_gondor_colonnade_corner_1", []),
  ("gondor_colonnade_corner_1_E",0,"gondor_colonnade_corner_1","0", []),
("gondor_copula_1",0,"gondor_copula_1","bo_gondor_copula_1", []),
  ("gondor_copula_1_E",0,"gondor_copula_1","0", []),
("gondor_copula_2",0,"gondor_copula_2","bo_gondor_copula_2", []),
  ("gondor_copula_2_E",0,"gondor_copula_2","0", []),
("gondor_copula_3",0,"gondor_copula_3","bo_gondor_copula_3", []),
  ("gondor_copula_3_E",0,"gondor_copula_3","0", []),
("gondor_house_1",0,"gondor_house_1","bo_gondor_house_1", []),
  ("gondor_house_1_E",0,"gondor_house_1","0", []),
("gondor_house_2",0,"gondor_house_2","bo_gondor_house_2", []),
  ("gondor_house_2_E",0,"gondor_house_2","0", []),
("gondor_house_3",0,"gondor_house_3","bo_gondor_house_3", []),
  ("gondor_house_3_E",0,"gondor_house_3","0", []),
("gondor_house_4",0,"gondor_house_4","bo_gondor_house_4", []),
  ("gondor_house_4_E",0,"gondor_house_4","0", []),
("gondor_house_5",0,"gondor_house_5","bo_gondor_house_5", []),
  ("gondor_house_5_E",0,"gondor_house_5","0", []),
("gondor_large_house_1",0,"gondor_large_house_1","bo_gondor_large_house_1", []),
  ("gondor_large_house_1_E",0,"gondor_large_house_1","0", []),
("gondor_large_house_2",0,"gondor_large_house_2","bo_gondor_large_house_2", []),
  ("gondor_large_house_2_E",0,"gondor_large_house_2","0", []),
("gondor_large_house_3",0,"gondor_large_house_3","bo_gondor_large_house_3", []),
  ("gondor_large_house_3_E",0,"gondor_large_house_3","0", []),
("gondor_short_tower",0,"gondor_short_tower_1","bo_gondor_short_tower_1", []),
  ("gondor_short_tower_E",0,"gondor_short_tower_1","0", []),
("gondor_stable",0,"gondor_stable_1","bo_gondor_stable_1", []),
  ("gondor_stable_E",0,"gondor_stable_1","0", []),
("gondor_standing_colonnade_corner_1",0,"gondor_standing_colonnade_corner_1","bo_gondor_standing_colonnade_corner_1", []),
  ("gondor_standing_colonnade_corner_1_E",0,"gondor_standing_colonnade_corner_1","0", []),
("gondor_standing_colonnade_doorway_1",0,"gondor_standing_colonnade_doorway_1","bo_gondor_standing_colonnade_doorway_1", []),
  ("gondor_standing_colonnade_doorway_1_E",0,"gondor_standing_colonnade_doorway_1","0", []),
("gondor_standing_colonnade_end_1",0,"gondor_standing_colonnade_end_1","bo_gondor_standing_colonnade_end_1", []),
  ("gondor_standing_colonnade_end_1_E",0,"gondor_standing_colonnade_end_1","0", []),
("gondor_standing_colonnade_mid_1",0,"gondor_standing_colonnade_mid_1","bo_gondor_standing_colonnade_mid_1", []),
  ("gondor_standing_colonnade_mid_1_E",0,"gondor_standing_colonnade_mid_1","0", []),
("gondor_tower_1",0,"gondor_tower_1","bo_gondor_tower_1", []),
  ("gondor_tower_1_E",0,"gondor_tower_1","0", []),
("gondor_tower_2",0,"gondor_tower_2","bo_gondor_tower_2", []),
  ("gondor_tower_2_E",0,"gondor_tower_2","0", []),
("gondor_tower_3",0,"gondor_tower_3","bo_gondor_tower_3", []),
  ("gondor_tower_3_E",0,"gondor_tower_3","0", []),
("gondor_tower_4",0,"gondor_tower_4","bo_gondor_tower_4", []),
  ("gondor_tower_4_E",0,"gondor_tower_4","0", []),
("gondor_tower_5",0,"gondor_tower_5","bo_gondor_tower_5", []),
  ("gondor_tower_5_E",0,"gondor_tower_5","0", []),
("gondor_tower_6",0,"gondor_tower_6","bo_gondor_tower_6", []),
  ("gondor_tower_6_E",0,"gondor_tower_6","0", []),
("gondor_tower_7",0,"gondor_tower_7","bo_gondor_tower_7", []),
  ("gondor_tower_7_E",0,"gondor_tower_7","0", []),
("gondor_tower_part_1",0,"gondor_tower_part_1","bo_gondor_tower_part_1", []),
  ("gondor_tower_part_1_E",0,"gondor_tower_part_1","0", []),
("gondor_tower_part_2",0,"gondor_tower_part_2","bo_gondor_tower_part_2", []),
  ("gondor_tower_part_2_E",0,"gondor_tower_part_2","0", []),
("gondor_tower_part_3",0,"gondor_tower_part_3","bo_gondor_tower_part_3", []),
  ("gondor_tower_part_3_E",0,"gondor_tower_part_3","0", []),
("gondor_tower_part_4",0,"gondor_tower_part_4","bo_gondor_tower_part_4", []),
  ("gondor_tower_part_4_E",0,"gondor_tower_part_4","0", []),
("gondor_tower_part_5",0,"gondor_tower_part_5","bo_gondor_tower_part_5", []),
  ("gondor_tower_part_5_E",0,"gondor_tower_part_5","0", []),
("gondor_wall_copula_1",0,"gondor_wall_copula_1","bo_gondor_wall_copula_1", []),
  ("gondor_wall_copula_1_E",0,"gondor_wall_copula_1","0", []),

] + (is_a_wb_sceneprop==1 and [
("gondor_citadel_main",0,"minastirith","bo_minastirith", []),
  ("gondor_citadel_main_E",0,"gondor_citadel_main_2","0", []),
] or [
("gondor_citadel_main",0,"gondor_citadel_main","bo_gondor_citadel_main", []),
  ("gondor_citadel_main_E",0,"gondor_citadel_main","0", []),
]) + [

("gondor_citadel_main_hall",0,"gondor_citadel_main_hall_1","bo_gondor_citadel_main_hall_1", []),
  ("gondor_citadel_main_hall_E",0,"gondor_citadel_main_hall_1","0", []),
("gondor_citadel_side_building_1",0,"gondor_citadel_side_building_1","bo_gondor_citadel_side_building_1", []),
  ("gondor_citadel_side_building_1_E",0,"gondor_citadel_side_building_1","0", []),
("gondor_citadel_side_building_2",0,"gondor_citadel_side_building_2","bo_gondor_citadel_side_building_2", []),
  ("gondor_citadel_side_building_2_E",0,"gondor_citadel_side_building_2","0", []),
("gondor_citadel_side_building_3",0,"gondor_citadel_side_building_3","bo_gondor_citadel_side_building_3", []),
  ("gondor_citadel_side_building_3_E",0,"gondor_citadel_side_building_3","0", []),
("gondor_citadel_tower",0,"gondor_citadel_tower","bo_gondor_citadel_tower", []),
  ("gondor_citadel_tower_E",0,"gondor_citadel_tower_lod","0", []),
("gondor_citadel_tree",0,"gondor_citadel_tree","bo_gondor_citadel_tree", []),
  ("gondor_citadel_tree_E",0,"gondor_citadel_tree","0", []),
  
("gondor_wall",0,"gondor_wall","bo_gondor_wall", []),
  ("gondor_wall_E",0,"gondor_wall","0", []),
("gondor_wall_double_sided",0,"gondor_wall_double_sided","bo_gondor_wall_double_sided", []),
  ("gondor_wall_double_sided_E",0,"gondor_wall_double_sided","0", []),
("gondor_walls_gate_turret",0,"gondor_walls_gate_turret","bo_gondor_walls_gate_turret", []),
  ("gondor_walls_gate_turret_E",0,"gondor_walls_gate_turret","0", []),
("gondor_wall_tower",0,"gondor_wall_tower","bo_gondor_wall_tower", []),
  ("gondor_wall_tower_E",0,"gondor_wall_tower","0", []),
("gondor_wall_end",0,"gondor_wall_end","bo_gondor_wall_end", []),
  ("gondor_wall_end_E",0,"gondor_wall_end","0", []),
("gondor_wall_main_gate",0,"gondor_wall_main_gate","bo_gondor_wall_main_gate", []),
  ("gondor_wall_main_gate_E",0,"gondor_wall_main_gate","0", []),
("gondor_wall_stair",0,"gondor_wall_stair","bo_gondor_wall_stair", []),
  ("gondor_wall_stair_E",0,"gondor_wall_stair","0", []),
("gondor_wall_tower_med",0,"gondor_wall_tower_med","bo_gondor_wall_tower_med", []),
  ("gondor_wall_tower_med_E",0,"gondor_wall_tower_med","0", []),
("gondor_wall_tower_small",0,"gondor_wall_tower_small","bo_gondor_wall_tower_small", []),
  ("gondor_wall_tower_small_E",0,"gondor_wall_tower_small","0", []),

# evil gondor props
("evil_gondor_short_tower",0,"gondor_short_tower_1_evil","bo_gondor_short_tower_1", []),
("evil_gondor_tower_1",0,"gondor_tower_1_evil","bo_gondor_tower_1", []),
("evil_gondor_tower_2",0,"gondor_tower_2_evil","bo_gondor_tower_2", []),
("evil_gondor_tower_3",0,"gondor_tower_3_evil","bo_gondor_tower_3", []),
("evil_gondor_tower_4",0,"gondor_tower_4_evil","bo_gondor_tower_4", []),
("evil_gondor_tower_7",0,"gondor_tower_7_evil","bo_gondor_tower_7", []),
("evil_gondor_wall",0,"mt_wall_evil", "bo_mt_wall_evil", []), #InVain: New collision mesh
("evil_gondor_gate_tower",0,"mt_gate_tower_evil", "bo_mt_tower", []),
("evil_gondor_gate_house",0,"mt_gate_house_evil", "bo_mt_gate_house_evil", [(ti_on_scene_prop_init,
            [(set_fixed_point_multiplier, 100),
            (try_begin),(is_currently_night), (eq, "$bright_nights", 1), (set_fog_distance,450,0x07291D),
            (else_try), (is_currently_night), (set_fog_distance,200,0x07291D), 
             ] + (is_a_wb_sceneprop==1 and [ (set_startup_ambient_light, 40, 40, 50),(set_startup_sun_light, 5, 5, 10),(set_startup_ground_ambient_light, 25, 25, 25), ] or []) + [ 
       (else_try),                      (set_fog_distance,700,0x4DB08D), 
       (try_end),])]), #InVain: New collision mesh
  
# old MT props  
("gondor_mt_bridge_modular_a",0,"mt_bridge_modular_a", "bo_bridge_modular_a", []),
  ("gondor_mt_bridge_modular_a_E",0,"mt_bridge_modular_a", "0", []),
("gondor_mt_bridge_modular_b",0,"mt_bridge_modular_b", "bo_bridge_modular_b", []),
  ("gondor_mt_bridge_modular_b_E",0,"mt_bridge_modular_b", "0", []),
#("gondor_mt_door_extension_a",0,"mt_door_extension_a", "bo_door_extension_a", []),
# ("gondor_mt_door_extension_a_E",0,"mt_door_extension_a", "0", []),
("gondor_mt_gate",0,"mt_gate", "bo_mt_gate_new", []),
  ("gondor_mt_gate_E",0,"mt_gate", "0", []),
("gondor_mt_gate_tower",0,"mt_gate_tower", "bo_mt_gate_tower", []),
  ("gondor_mt_gate_tower_E",0,"mt_gate_tower", "0", []),
("gondor_mt_gate_house",0,"mt_gate_house", "bo_mt_gate_house", []),
  ("gondor_mt_gate_house_E",0,"mt_gate_house", "0", []),
#("gondor_mt_house_extension_a",0,"mt_house_extension_a", "bo_house_extension_a", []),
# ("gondor_mt_house_extension_a_E",0,"mt_house_extension_a", "0", []),
#("gondor_mt_house_extension_b",0,"mt_house_extension_b", "bo_house_extension_b", []),
# ("gondor_mt_house_extension_b_E",0,"mt_house_extension_b", "0", []),
("gondor_mt_house_extension_c",0,"mt_house_extension_c", "bo_house_extension_a", []),
  ("gondor_mt_house_extension_c_E",0,"mt_house_extension_c", "0", []),
#("gondor_mt_house_extension_d",0,"mt_house_extension_d", "bo_house_extension_d", []),
# ("gondor_mt_house_extension_d_E",0,"mt_house_extension_d", "0", []),
#  ("gondor_mt_mini_town_house_a",0,"mt_mini_town_house_a", 0, []),
#  ("gondor_mt_mini_town_house_b",0,"mt_mini_town_house_b", 0, []),
#  ("gondor_mt_mini_town_house_c",0,"mt_mini_town_house_c", 0, []),
#  ("gondor_mt_mini_town_house_d",0,"mt_mini_town_house_d", 0, []),
("gondor_mt_passage_house_b",0,"mt_passage_house_b", "bo_passage_house_b", []),
  ("gondor_mt_passage_house_b_E",0,"mt_passage_house_b", "0", []),
("gondor_mt_short_tower",0,"mt_short_tower", "bo_mt_short_tower", []),
  ("gondor_mt_short_tower_E",0,"mt_short_tower", "0", []),
("gondor_mt_small_wall_a",0,"mt_small_wall_a", "bo_small_wall_a", []),
  ("gondor_mt_small_wall_a_E",0,"mt_small_wall_a", "0", []),
("gondor_mt_stairs_arch_a",0,"mt_stairs_arch_a", "bo_stairs_arch_a", []),
  ("gondor_mt_stairs_arch_a_E",0,"mt_stairs_arch_a", "0", []),
("gondor_mt_town_house_a",0,"mt_town_house_a", "bo_town_house_a", []),
("town_house_steppe_a",0,"town_house_steppe_a","bo_town_house_steppe_a", []),
("gondor_mt_town_house_b",0,"mt_town_house_b", "bo_town_house_b", []),
("town_house_steppe_b",0,"town_house_steppe_b","bo_town_house_steppe_b", []),
("gondor_mt_town_house_c",0,"mt_town_house_c", "bo_town_house_c", []),
("town_house_steppe_c",0,"town_house_steppe_c","bo_town_house_steppe_c", []),
("gondor_mt_town_house_d",0,"mt_town_house_d", "bo_town_house_d", []),
("town_house_steppe_d",0,"town_house_steppe_d","bo_town_house_steppe_d", []),
("gondor_mt_town_house_f",0,"mt_town_house_f", "bo_town_house_f", []),
("town_house_steppe_e",0,"town_house_steppe_e","bo_town_house_steppe_e", []),
("gondor_mt_town_house_h",0,"mt_town_house_h", "bo_town_house_h", []),
("town_house_steppe_f",0,"town_house_steppe_f","bo_town_house_steppe_f", []),
("gondor_mt_town_house_i",0,"mt_town_house_i", "bo_town_house_i", []),
("town_house_steppe_g",0,"town_house_steppe_g","bo_town_house_steppe_g", []),
("gondor_mt_town_house_j",0,"mt_town_house_j", "bo_town_house_j", []),
("town_house_steppe_h",0,"town_house_steppe_h","bo_town_house_steppe_h", []),
("gondor_mt_town_house_l",0,"mt_town_house_l", "bo_town_house_l", []),
("town_house_steppe_i",0,"town_house_steppe_i","bo_town_house_steppe_i", []),
("gondor_mt_wall",0,"mt_wall", "bo_mt_wall", []),
  ("gondor_mt_wall_E",0,"mt_wall", "0", []),
("gondor_tirith_gate",0,"tirith_gate", "bo_tirith_gate", []),

##OSGILIATH ruins by Llew###
("osgiliath_bridge",0,"osgiliath_bridge","bo_osgiliath_bridge", []),
  ("osgiliath_bridge_E",0,"osgiliath_bridge","0", []),
("osgiliath_broken_bridge",0,"osgiliath_broken_bridge","bo_osgiliath_broken_bridge", []),
  ("osgiliath_broken_bridge_E",0,"osgiliath_broken_bridge","0", []),
("osgiliath_rubble_one",0,"osgiliath_rubble_one","bo_osgiliath_rubble_one", []),
  ("osgiliath_rubble_one_E",0,"osgiliath_rubble_one","0", []),
("osgiliath_ruin_one",0,"osgiliath_ruin_one","bo_osgiliath_ruin_one", []),
  ("osgiliath_ruin_one_E",0,"osgiliath_ruin_one","0", []),
("osgiliath_ruins_eight",0,"osgiliath_ruins_eight","bo_osgiliath_ruins_eight", []),
  ("osgiliath_ruins_eight_E",0,"osgiliath_ruins_eight","0", []),
("osgiliath_ruins_eleven",0,"osgiliath_ruins_eleven","bo_osgiliath_ruins_eleven", []),
  ("osgiliath_ruins_eleven_E",0,"osgiliath_ruins_eleven","0", []),
("osgiliath_ruins_fifteen",0,"osgiliath_ruins_fifteen","bo_osgiliath_ruins_fifteen", []),
  ("osgiliath_ruins_fifteen_E",0,"osgiliath_ruins_fifteen","0", []),
("osgiliath_ruins_five",0,"osgiliath_ruins_five","bo_osgiliath_ruins_five", []),
  ("osgiliath_ruins_five_E",0,"osgiliath_ruins_five","0", []),
("osgiliath_ruins_four",0,"osgiliath_ruins_four","bo_osgiliath_ruins_four", []),
  ("osgiliath_ruins_four_E",0,"osgiliath_ruins_four","0", []),
("osgiliath_ruins_fourteen",0,"osgiliath_ruins_fourteen","bo_osgiliath_ruins_fourteen", []),
  ("osgiliath_ruins_fourteen_E",0,"osgiliath_ruins_fourteen","0", []),
("osgiliath_ruins_nine",0,"osgiliath_ruins_nine","bo_osgiliath_ruins_nine", []),
  ("osgiliath_ruins_nine_E",0,"osgiliath_ruins_nine","0", []),
("osgiliath_ruins_set_one",0,"osgiliath_ruins_set_one","bo_osgiliath_ruins_set_one", []),
  ("osgiliath_ruins_set_one_E",0,"osgiliath_ruins_set_one","0", []),
("osgiliath_ruins_seven",0,"osgiliath_ruins_seven","bo_osgiliath_ruins_seven_new", []),
  ("osgiliath_ruins_seven_E",0,"osgiliath_ruins_seven","0", []),
("osgiliath_ruins_seventeen",0,"osgiliath_ruins_seventeen","bo_osgiliath_ruins_seventeen", []),
  ("osgiliath_ruins_seventeen_E",0,"osgiliath_ruins_seventeen","0", []),
("osgiliath_ruins_six",0,"osgiliath_ruins_six","bo_osgiliath_ruins_six", []),
  ("osgiliath_ruins_six_E",0,"osgiliath_ruins_six","0", []),
("osgiliath_ruins_sixteen",0,"osgiliath_ruins_sixteen","bo_osgiliath_ruins_sixteen", []),
  ("osgiliath_ruins_sixteen_E",0,"osgiliath_ruins_sixteen","0", []),
("osgiliath_ruins_ten",0,"osgiliath_ruins_ten","bo_osgiliath_ruins_ten", []),
  ("osgiliath_ruins_ten_E",0,"osgiliath_ruins_ten","0", []),
("osgiliath_ruins_thirteen",0,"osgiliath_ruins_thirteen","bo_osgiliath_ruins_thirteen", []),
  ("osgiliath_ruins_thirteen_E",0,"osgiliath_ruins_thirteen","0", []),
("osgiliath_ruins_three",0,"osgiliath_ruins_three","bo_osgiliath_ruins_three", []),
  ("osgiliath_ruins_three_E",0,"osgiliath_ruins_three","0", []),
("osgiliath_ruins_twelve",0,"osgiliath_ruins_twelve","bo_osgiliath_ruins_twelve", []),
  ("osgiliath_ruins_twelve_E",0,"osgiliath_ruins_twelve","0", []),
("osgiliath_ruins_two",0,"osgiliath_ruins_two","bo_osgiliath_ruins_two", []),
  ("osgiliath_ruins_two_E",0,"osgiliath_ruins_two","0", []),
##PELARGIR
("pel_street_long",0,"pel_street_long","bo_pel_street_long", []),
("pel_street_med",0,"pel_street_med","bo_pel_street_med", []),
("pel_street_short",0,"pel_street_short","bo_pel_street_short", []),
("pel_street_corner",0,"pel_street_corner","bo_pel_street_corner", []),
("pel_street_three_way",0,"pel_street_three_way","bo_pel_street_three_way", []),
("pel_street_four_way",0,"pel_street_four_way","bo_pel_street_four_way", []),
("pel_bridge",0,"pel_bridge","bo_pel_bridge", []),
("pelargir",0,"pelargir","bo_pelargir", []),
("pel_lighthouse",0,"pel_lighthouse","0", []),
## octo gondor props
("gondor_tower_b_vp",0,"gondor_tower_b_color","bo_gondor_tower_b", []),
("arabian_ramp_a",0,"arabian_ramp_a","bo_arabian_ramp_a", []), #WB
("gondor_ship_vp",0,"gondor_ship_color","bo_gondor_ship", []),
("arabian_ramp_b",0,"arabian_ramp_b","bo_arabian_ramp_b", []), #WB
("gondor_ship_oars",0,"gondor_ship_oars","0", []),
("gondor_building_a_vp",0,"gondor_building_a_color","bo_gondor_building_a", []),
  ("gondor_building_a_vp_E",0,"gondor_building_a_color","0", []),
("gondor_building_b_vp",0,"gondor_building_b_color","bo_gondor_building_b", []),
  ("gondor_building_b_vp_E",0,"gondor_building_b_color","0", []),
("gondor_building_c_vp",0,"gondor_building_c_color","bo_gondor_building_c", []),
  ("gondor_building_c_vp_E",0,"gondor_building_c_color","0", []),

### Orc contrievances by Llew
("orc_cage"        ,0,"orc_cage"        ,"bo_orc_cage", []),
("orc_filth_pile"  ,0,"orc_filth_pile"  ,"bo_orc_filth_pile", []),
("orc_gate"        ,0,"orc_gate"        ,"bo_orc_gate", []),
("orc_lean_to"     ,0,"orc_lean_to"     ,"bo_orc_lean_to", []),
("orc_palisade_1"  ,0,"orc_palisade_1"  ,"bo_orc_palisade_1", []),
("orc_palisade_2"  ,0,"orc_palisade_2"  ,"bo_orc_palisade_2", []),
("orc_palisade_3"  ,0,"orc_palisade_3"  ,"bo_orc_palisade_3", []),
("orc_platform"    ,0,"orc_platform"    ,"bo_orc_platform", []),
("orc_shelter_1"   ,0,"orc_shelter_1"   ,"bo_orc_shelter_1", []),
("orc_shelter_2"   ,0,"orc_shelter_2"   ,"bo_orc_shelter_2", []),
("orc_stake"       ,0,"orc_stake"       ,"bo_orc_stake", []),
("orc_stakes"      ,0,"orc_stakes"      ,"bo_orc_stakes", []),
("orc_tanning_rack",0,"orc_tanning_rack","bo_orc_tanning_rack", []),
("orc_tower_1"     ,0,"orc_tower_1"     ,"bo_orc_tower_1", []),
("orc_tower_2"     ,0,"orc_tower_2"     ,"bo_orc_tower_2", []),
("orc_tower_3"     ,0,"orc_tower_3"     ,"bo_orc_tower_3", []),
("orc_tower_4"     ,0,"orc_tower_4"     ,"bo_orc_tower_4", []),
("orc_warg_pit"    ,0,"orc_warg_pit"    ,"bo_orc_warg_pit", []),
### UMBAR PROPS #####
("umbar_anchor",0,"umbar_prop_anchor","0", []),
("umbar_ship",0,"umbar_prop_ship","bo_umbar_prop_ship", []),
("umbar_shipwrecked",0,"umbar_prop_shipwrecked","bo_umbar_prop_shipwrecked", []),
("umbar_smallboat",0,"umbar_prop_smallboat","0", []),
("umbar_smallboatoar",0,"umbar_prop_smallboatoar","0", []),
# Moria
] + (is_a_wb_sceneprop==1 and [
("moria",0,"moria_hall","bo_moria_hall", 
    [(ti_on_scene_prop_init,
        [(set_rain, 0,100), (set_fixed_point_multiplier, 10000), (set_skybox, 10, 11),
        (try_begin), 
            (eq, "$bright_nights", 1), (set_fog_distance,60,0x01D261D),(set_startup_sun_light, 5, 5, 5), (set_startup_ambient_light, 300, 400, 300), 
         (else_try), 
            (get_startup_ambient_light, pos5),
            (position_get_x, reg5, pos5),
            (set_fog_distance,60,0x030403),
            (set_startup_sun_light, 5, 5, 5),
            (set_startup_ambient_light, 60, 80, 60), 
            (set_startup_ground_ambient_light, 60, 80, 60),
            (get_startup_ambient_light, pos5),
            (position_get_x, reg5, pos5),
         (try_end)
    ])]),
    ] or [
("moria",0,"moria_hall","bo_moria_hall", [(ti_on_scene_prop_init,[(set_fog_distance,70,0x0B0F0B),(set_rain, 0,100)])]) #new fog, slightly greenish and minimally brighter
]) + [
#("moria",0,"moria_hall","bo_moria_hall", [(ti_on_scene_prop_init,[(set_fog_distance,50,0x010101)])]), #old fog, dark as fuck
#("moria",0,"moria_hall","bo_moria_hall", []), #no fog, for working on scene
("moria_dimrill_gate",0,"dimrill_gate","bo_dimrill_gate", []),                

######ROHAN SCENE PROPS##########
("rohan_gate"      ,0,"rohan_gate"      ,"bo_rohan_gate"      , []),
  ("rohan_gate_E"      ,0,"rohan_gate"      ,"0"      , []),
("rohan_tower2"    ,0,"rohan_tower2"    ,"bo_rohan_tower2"    , []),
  ("rohan_tower2_E"    ,0,"rohan_tower2"    ,"0"    , []),
("rohan_tower3"    ,0,"rohan_tower3"    ,"bo_rohan_tower3"    , []),
  ("rohan_tower3_E"    ,0,"rohan_tower3"    ,"0"    , []),
("rohan_wall_stair",0,"rohan_wall_stair","bo_rohan_wall_stair", []),
  ("rohan_wall_stair_E",0,"rohan_wall_stair","0", []),
("rohan_long_stair",0,"rohan_long_stair","bo_rohan_long_stair", []),
  ("rohan_long_stair_E",0,"rohan_long_stair","0", []),
("rohan_wall"      ,0,"rohan_wall_curved"      ,"bo_rohan_wall_curved"      , []),
  ("rohan_wall_straight"      ,0,"rohan_wall"      ,"bo_rohan_wall"      , []),

#Helms Deep
("HD",0,"helms_deep","bo_helms_deep", []),
("ballista",0,"ballista","0",[]),
("ballista_empty",0,"ballista_empty","0",[]),
("ballista_missile",0,"ballista_missile","0",[]),
("throwing_stone",0,"throwing_stone","0",[]),
("Village_fire_big_no_smoke",0,"0","0",[(ti_on_scene_prop_init,[(particle_system_add_new, "psys_village_fire_big"),]),]),

("gate_destructible",sokf_destructible,"gate_tld","bo_gate_tld",   [ 
   (ti_on_scene_prop_init, [
   (store_trigger_param_1, ":instance_no"),
   
    ] + (is_a_wb_sceneprop==1 and [ 
   (prop_instance_get_variation_id_2, ":health", ":instance_no"),
    (try_begin),
        (gt, ":health", 0), #if not assigned, get fallback health from scene prop entry (WB only)
        (val_mul, ":health", 100),
        (scene_prop_set_hit_points, ":instance_no", ":health"),
    (try_end),
    ] or []) + [
    
    (eq, "$gate_aggravator_agent", 1),
    (prop_instance_get_starting_position, pos1, ":instance_no"),
    (set_fixed_point_multiplier, 100),
    (position_move_z, pos1, 100,1), #safeguard against aggravators spawning underground
    (set_spawn_position, pos1),
    (spawn_agent,"trp_gate_aggravator"),
    (assign, ":gate_aggravator", reg0),
    (agent_set_speed_limit, ":gate_aggravator", 0),
    (agent_set_team, ":gate_aggravator", 2),
    ] + (is_a_wb_sceneprop==1 and [               # make aggravator a statue (WB Only)
    (agent_set_no_dynamics, ":gate_aggravator",1),
    (agent_set_no_death_knock_down_only, ":gate_aggravator", 1),
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, ":gate_aggravator"),
    ] or []) + [
    #(team_give_order, 7, grc_everyone, mordr_stand_ground),
  ]),
   
   (ti_on_scene_prop_destroy, [
    (store_trigger_param_1, ":gate_no"),
    (prop_instance_get_starting_position, pos1, ":gate_no"),
    (particle_system_burst,"psys_game_hoof_dust",pos1,40),
    (particle_system_burst,"psys_dummy_smoke",pos1,30),
    #(particle_system_burst,"psys_pistol_smoke",pos1,200),
    (position_rotate_x, pos1, -90),
    (prop_instance_animate_to_position, ":gate_no", pos1, 400), #animate in 4 second
    (play_sound, "snd_dummy_destroyed"),
    (display_message,"@Gate is breached!"),
    #(assign, ":gate_aggravator_found", 0),

    ] + (is_a_wb_sceneprop==1 and [        
    (scene_prop_get_slot, ":gate_aggravator", ":gate_no", slot_prop_agent_1),
    (call_script, "script_remove_agent", ":gate_aggravator"), 
    ] or [    
    (assign, ":gate_aggravator_found", 0),
    (try_for_agents, ":agent_no"), #find and remove gate aggravator agent
        (eq, ":gate_aggravator_found", 0),
        (gt, ":agent_no", 0),
        (agent_is_alive, ":agent_no"),  
        (agent_get_troop_id, ":troop_id", ":agent_no"),
        (eq, ":troop_id", "trp_gate_aggravator"),
        (agent_get_position, pos2, ":agent_no"),
        (set_fixed_point_multiplier, 100),
        (get_distance_between_positions, ":distance", pos1, pos2),
        (le, ":distance", 200),
        #(display_message, "@gate_aggravator found"),
        (call_script, "script_remove_agent", ":agent_no"), 
        (assign, ":gate_aggravator_found", 1),
    (try_end),
    ]) + [
    
    (scene_prop_get_num_instances,":max_barriers","spr_ai_limiter_gate_breached"),  #move away all dependent barriers
    (try_begin),
      (gt, ":max_barriers",0),
      (try_for_range,":count",0,":max_barriers"),
        (scene_prop_get_instance,":barrier_no", "spr_ai_limiter_gate_breached", ":count"),
        (prop_instance_get_starting_position, pos1, ":barrier_no"),
        ] + (is_a_wb_sceneprop==1 and [  #different methods of finding dependent barriers in WB and MB
        (prop_instance_get_variation_id, ":var1", ":barrier_no"),
        (prop_instance_get_variation_id, ":var1_gate", ":gate_no"),
        (eq, ":var1", ":var1_gate"),
        ] or [
        (prop_instance_get_starting_position, pos2, ":gate_no"),
        (set_fixed_point_multiplier, 100),
        (get_distance_between_positions, ":distance", pos1, pos2),
        (le, ":distance", 1000),
        ]) + [
        (position_move_z,pos1,-10000),
        (prop_instance_set_position,":barrier_no",pos1),
      (try_end),
    (try_end),
   ]),

   (ti_on_scene_prop_hit,
    [(play_sound, "snd_dummy_hit"),
  (particle_system_burst, "psys_dummy_smoke", pos1, 3),
  (particle_system_burst, "psys_dummy_straw", pos1, 10),
  #(entry_point_get_position,pos1,39),
  #(agent_set_position, "$gate_aggravator_agent", pos1), # place gate aggravator agent to proper position
    ]),
], 4000),

("HD_gate_destructible",sokf_destructible|sokf_moveable,"HD_gate_closed_repositioned","bo_HD_gate_closed_repositioned",   [ 
   (ti_on_scene_prop_init, [
   (store_trigger_param_1, ":gate_no"),
   
    ] + (is_a_wb_sceneprop==1 and [ 
   (prop_instance_get_variation_id_2, ":health", ":gate_no"),
    (try_begin),
        (gt, ":health", 0), #if not assigned, get fallback health from scene prop entry (WB only)
        (scene_prop_set_hit_points, ":gate_no", ":health"),
    (try_end),
    ] or []) + [
    
    (eq, "$gate_aggravator_agent", 1),
    (prop_instance_get_starting_position, pos1, ":gate_no"),
    (position_move_z, pos1, 100,1), #safeguard against aggravators spawning underground
    (set_spawn_position, pos1),
    (spawn_agent,"trp_gate_aggravator"),
    (assign, ":gate_aggravator", reg0),
    (agent_set_speed_limit, ":gate_aggravator", 0),
    (agent_set_team, ":gate_aggravator", 2),
    ] + (is_a_wb_sceneprop==1 and [               # make aggravator a statue (WB Only)
    (agent_set_no_dynamics, ":gate_aggravator",1),
    (agent_set_no_death_knock_down_only, ":gate_aggravator", 1),
    (scene_prop_set_slot, ":gate_no", slot_prop_agent_1, ":gate_aggravator"),
    ] or []) + [
    #(team_give_order, 7, grc_everyone, mordr_stand_ground),
  ]),
   
   (ti_on_scene_prop_destroy, [
    (store_trigger_param_1, ":gate_no"),
    (prop_instance_get_starting_position, pos1, ":gate_no"),
    (particle_system_burst,"psys_game_hoof_dust",pos1,40),
    (particle_system_burst,"psys_dummy_smoke",pos1,30),
    #(particle_system_burst,"psys_pistol_smoke",pos1,200),
    (position_rotate_x, pos1, 95),
    (position_move_z, pos1, -100,1),
    (prop_instance_animate_to_position, ":gate_no", pos1, 400), #animate in 4 second
    (play_sound, "snd_dummy_destroyed"),
    (display_message,"@Gate is breached!"),
    
    ] + (is_a_wb_sceneprop==1 and [        
    (scene_prop_get_slot, ":gate_aggravator", ":gate_no", slot_prop_agent_1),
    (call_script, "script_remove_agent", ":gate_aggravator"), 
    ] or [    
    (assign, ":gate_aggravator_found", 0),
    (try_for_agents, ":agent_no"), #find and remove gate aggravator agent
        (eq, ":gate_aggravator_found", 0),
        (gt, ":agent_no", 0),
        (agent_is_alive, ":agent_no"),  
        (agent_get_troop_id, ":troop_id", ":agent_no"),
        (eq, ":troop_id", "trp_gate_aggravator"),
        (agent_get_position, pos2, ":agent_no"),
        (set_fixed_point_multiplier, 100),
        (get_distance_between_positions, ":distance", pos1, pos2),
        (le, ":distance", 200),
        #(display_message, "@gate_aggravator found"),
        (call_script, "script_remove_agent", ":agent_no"), 
        (assign, ":gate_aggravator_found", 1),
    (try_end),
    ]) + [
    
    (scene_prop_get_num_instances,":max_barriers","spr_ai_limiter_gate_breached"),  #move away all dependent barriers
    (try_begin),
      (gt, ":max_barriers",0),
      (try_for_range,":count",0,":max_barriers"),
        (scene_prop_get_instance,":barrier_no", "spr_ai_limiter_gate_breached", ":count"),
        (prop_instance_get_starting_position, pos1, ":barrier_no"),
        ] + (is_a_wb_sceneprop==1 and [  #different methods of finding dependent barriers in WB and MB
        (prop_instance_get_variation_id, ":var1", ":barrier_no"),
        (prop_instance_get_variation_id, ":var1_gate", ":gate_no"),
        (eq, ":var1", ":var1_gate"),
        ] or [
        (prop_instance_get_starting_position, pos2, ":gate_no"),
        (set_fixed_point_multiplier, 100),
        (get_distance_between_positions, ":distance", pos1, pos2),
        (le, ":distance", 1000),
        ]) + [
        (position_move_z,pos1,-10000),
        (prop_instance_set_position,":barrier_no",pos1),
      (try_end),
    (try_end),
   ]),
   
   (ti_on_scene_prop_hit,
    [(play_sound, "snd_dummy_hit"),
  (particle_system_burst, "psys_dummy_smoke", pos1, 3),
  (particle_system_burst, "psys_dummy_straw", pos1, 10),
  #(entry_point_get_position,pos1,39),
  #(agent_set_position, "$gate_aggravator_agent", pos1), # place gate aggravator agent to proper position
    ]),
], 4000),

("tree_destructible",sokf_destructible|spr_hit_points(600),"tree_e_2","bo_tree_e_2",   [
   (ti_on_scene_prop_destroy,
    [(store_trigger_param_1, ":instance_no"),
  (prop_instance_get_starting_position, pos1, ":instance_no"),
    (position_rotate_x, pos1, 85),
    (prop_instance_animate_to_position, ":instance_no", pos1, 400), #animate in 4 second
    (play_sound, "snd_dummy_destroyed"),
    ]),
   (ti_on_scene_prop_hit, [(play_sound, "snd_dummy_hit"), (particle_system_burst, "psys_dummy_straw", pos1, 10),]),
]),
  
###DWARVEN PROPS###
("dwarf_statue",0,"statue_dwarf","0", []),
("dwarf_statue_a",0,"statue_dwarf1","0", []),
("dwarf_statue_b",0,"statue_dwarf2","0", []),
("dwarf_statue_c",0,"statue_dwarf3","0", []),
("dwarf_statue_d",0,"statue_dwarf4","0", []),
("dwarf_statue_e",0,"statue_dwarf5","0", []),
("dwarf_statue_hill_a",0,"statue_dwarf_hill_a","bo_statue_dwarf_hill_a", []),
("dwarf_statue_hill_b",0,"statue_dwarf_hill_b","bo_statue_dwarf_hill_b", []),

#("distant_mountain4",sokf_moveable|sokf_place_at_origin,"rom_mountain4","0",[]),
("mordor_clouds",sokf_moveable|sokf_place_at_origin,"skybox_cloud_overlay","0",[]),
("distant_mountain1",sokf_moveable|sokf_place_at_origin,"kkk","0",[]),
("distant_mountain2",sokf_moveable|sokf_place_at_origin,"kkk2","0",[]),

#####DALE PROPS#####
("laketown",0,"laketown","bo_laketown", []),

("lktn_building_a",0,"dale_frame_house_a","bo_dale_frame_house_a", []),
("lktn_building_b",0,"dale_house_b","bo_dale_house_b", []),
("lktn_building_c",0,"dale_side_building_a","bo_side_building_a_tld", []),
("lktn_building_d",0,"dale_house_c","bo_dale_house_c", []),
("lktn_building_e",0,"dale_door_extension_a","0", []),
("lktn_building_f",0,"dale_passage_house_a","bo_passage_house_a_tld", []),
("lktn_building_g",0,"dale_passage_house_b","bo_dale_passage_house_b", []),
("lktn_building_h",0,"dale_town_house_a","bo_dale_town_house_a", []),
("lktn_building_i",0,"dale_town_house_b","bo_dale_town_house_b", []),
("lktn_building_j",0,"dale_town_house_c","bo_dale_town_house_c", []),
("lktn_building_k",0,"dale_town_house_d","bo_dale_town_house_d", []),
("lktn_building_l",0,"dale_town_house_e","bo_dale_town_house_e", []),
("lktn_building_m",0,"dale_town_house_f","bo_dale_town_house_f", []),
("lktn_building_n",0,"dale_town_house_g","bo_dale_town_house_g", []),
("lktn_building_o",0,"dale_town_house_h","bo_dale_town_house_h", []),
("lktn_building_p",0,"dale_town_house_i","bo_dale_town_house_i", []),
("lktn_building_q",0,"dale_town_house_j","bo_dale_town_house_j", []),
("lktn_building_r",0,"dale_town_house_l","bo_dale_town_house_l", []),
("lktn_building_s",0,"dale_town_house_m","bo_dale_town_house_m", []),
("lktn_building_t",0,"dale_town_house_n","bo_dale_town_house_n", []),
("lktn_building_u",0,"dale_town_house_o","bo_dale_town_house_o", []),
("lktn_building_v",0,"dale_town_house_p","bo_dale_town_house_p", []),
("lktn_building_w",0,"dale_town_house_q","bo_dale_town_house_q", []),
("lktn_building_x",0,"dale_town_house_s","bo_dale_town_house_s", []),
("lktn_building_y",0,"dale_town_house_t","bo_dale_town_house_t", []),
("lktn_building_z",0,"dale_town_house_u","bo_dale_town_house_u", []),
("lktn_building_aa",0,"dale_town_house_v","bo_dale_town_house_v", []),
("lktn_building_ab",0,"dale_town_house_y","bo_dale_town_house_y", []),
("lktn_building_ac",0,"dale_town_house_z","bo_dale_town_house_z", []),
("lktn_building_ad",0,"dale_town_house_za","bo_dale_town_house_za", []),

("lktn_extension_a",0,"dale_house_extension_a","0", []),
("lktn_extension_b",0,"dale_house_extension_b","0", []),
("lktn_extension_c",0,"dale_house_extension_c","0", []),
("lktn_extension_d",0,"dale_house_extension_d","0", []),
("lktn_extension_e",0,"dale_extension_a","0", []),
("lktn_extension_f",0,"dale_extension_b","0", []),

("lktn_awning_a",0,"dale_awning","bo_awning", []),
("lktn_awning_b",0,"dale_cloth_awning","bo_arena_block_j_awning", []),
("lktn_door_a",0,"laketown_door_a","bo_laketown_door", []),
("lktn_door_b",0,"laketown_door_b","bo_laketown_door", []),
("lktn_door_c",0,"laketown_door_c","bo_laketown_door", []),
("lktn_platform",0,"esgaroth_stilts","bo_esgaroth_stilts_new", []),
("lktn_stairs",0,"esgaroth_steps","bo_esgaroth_steps", []),

########## SMALL PLANTS FOR CHANGEABLE TREES #################################
# pointers for generated trees
("zz_pointer00", 0, "spike_a", "0", []),("zz_pointer01", 0, "spike_a", "0", []),("zz_pointer02", 0, "spike_a", "0", []),("zz_pointer03", 0, "spike_a", "0", []),  
("zz_pointer04", 0, "spike_a", "0", []),("zz_pointer05", 0, "spike_a", "0", []),("zz_pointer06", 0, "spike_a", "0", []),("zz_pointer07", 0, "spike_a", "0", []),  
("zz_pointer08", 0, "spike_a", "0", []),("zz_pointer09", 0, "spike_a", "0", []),("zz_pointer10", 0, "spike_a", "0", []),("zz_pointer11", 0, "spike_a", "0", []),  
("zz_pointer12", 0, "spike_a", "0", []),("zz_pointer13", 0, "spike_a", "0", []),("zz_pointer14", 0, "spike_a", "0", []),("zz_pointer15", 0, "spike_a", "0", []),  
("zz_pointer16", 0, "spike_a", "0", []),("zz_pointer17", 0, "spike_a", "0", []),("zz_pointer18", 0, "spike_a", "0", []),("zz_pointer19", 0, "spike_a", "0", []),  
("zz_pointerend",0, "0", "0", []),
# pointers for landmarks
("zz_landmark00", 0, "cabbage", "0", []),("zz_landmark01", 0, "cabbage", "0", []),("zz_landmark02", 0, "cabbage", "0", []),("zz_landmark03", 0, "cabbage", "0", []),
("zz_landmark04", 0, "cabbage", "0", []),("zz_landmark05", 0, "cabbage", "0", []),("zz_landmark06", 0, "cabbage", "0", []),("zz_landmark07", 0, "cabbage", "0", []),
("zz_landmark08", 0, "cabbage", "0", []),("zz_landmark09", 0, "cabbage", "0", []),("zz_landmarkend", 0, "cabbage", "0", []),
# trees, bushes and rocks props

("tree0_yellow_flower", 0, "yellow_flower", "0", []),
("tree1_yellow_flower", 0, "tree_e_2","bo_tree_e_2", []),
#("tree_seedy_plant_a", 0, "seedy_plant_a", "0", []),
#("tree_ground_bush", 0, "ground_bush", "0", []),
#("tree1_ground_bush", 0, "tree_e_2", "bo_tree_e_2", []),
#("tree_bushes07_a", 0, "bushes07_a", "0", []),
#("tree1_bushes07_a", 0, "tree_e_1", "0", []),
#("tree_bushes04_a", 0, "bushes04_a", "0", []),
#("tree1_bushes04_a", 0, "tree_e_3", "0", []),
("tree1_aspen_a", 0, "aspen_a", "bo_aspen_a", []),
("tree1_aspen_b", 0, "aspen_b", "bo_aspen_b", []),
("tree1_aspen_c", 0, "aspen_c", "bo_aspen_c", []),
("tree1_pine_1_a", 0, "pine_1_a", "bo_pine_1_a", []),
("tree1_pine_1_b", 0, "pine_1_b", "bo_pine_1_b", []),
("tree1_pine_2_a", 0, "pine_2_a", "bo_pine_2_a", []),
("tree1_pine_3_a", 0, "pine_3_a", "bo_pine_3_a", []),
("tree1_pine_4_a", 0, "pine_4_a", "bo_pine_4_a", []),
("tree1_rock_c", 0, "rock_c", "bo_rock_c", []),
("tree1_beech_d", 0, "beech_d", "bo_beech_d", []),
("tree1_beech_e", 0, "beech_e", "bo_beech_e", []),
("trees_end", 0, "spike_a", "0", []), 
("fireplace_d_interior",0,"fireplace_d","bo_fireplace_d", []),
("harbour_a",0,"harbour_a","bo_harbour_a", []),
("ramp_small_a",0,"ramp_small_a","bo_ramp_small_a", []),
("football_ball",0,"stone_ball","0", []),
("dolguldur_copy",0,"dolguldur_copy","0", []),
("morannon_gate",0,"morannon_gate","bo_morannon_gate", [
     (ti_on_scene_prop_init,[ (set_fixed_point_multiplier, 100), 
         (try_begin),(is_currently_night),(eq, "$bright_nights", 1), (set_fog_distance,450,0x150101),
         (else_try),(is_currently_night),(set_fog_distance,450,0x150101), 
         ] + (is_a_wb_sceneprop==1 and [ (set_startup_ambient_light, 25, 25, 25),(set_startup_sun_light, 5, 5, 5),(set_startup_ground_ambient_light, 12, 12, 12), ] or []) + [ 
         (else_try),(set_fog_distance,800,0x150101),         
         ] + (is_a_wb_sceneprop==1 and [ (set_startup_ambient_light, 40, 40, 40),(set_startup_sun_light, 10, 10, 10),(set_startup_ground_ambient_light, 12, 12, 12), ] or []) + [ 
         (try_end),
     ])]),
("mor_tower_a",0,"mor_tower_a","bo_mor_tower_a", []),
("evil_element",0,"evil_element","0", []),
("evil_tunnel_a",0,"evil_tunnel_a","bo_evil_tunnel_a", []),
("minas_tirith_copy",0,"minas_tirith_new","0", []),

##### CENTER GUARDS ##### 
#InVain: Changed helper meshes for all of these and randomized animation times; 
#You can choose a tier by scaling up; allow spawning in siege defenses
("troop_guard",sokf_invisible,"arrow_helper_blue","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),
    (party_get_slot, ":troop", "$current_town", slot_town_guard_troop),
    (assign, ":var1", 0),
    (assign, ":var2", 0),
    ] + (is_a_wb_sceneprop==1 and [
    (prop_instance_get_variation_id, ":var1", ":instance_no"),
    (prop_instance_get_variation_id_2, ":var2", ":instance_no"),
    ] or []) + [ 
    (set_fixed_point_multiplier, 100),
    (prop_instance_get_scale, pos2, ":instance_no"),
    (position_get_scale_y, ":tier", pos2),
    (val_sub, ":tier", 100),
    (val_div, ":tier", 10),
    (try_begin),
        (ge, ":tier", 1),
        (try_begin),
            (eq, ":var1", 0),
            (try_for_range, ":unused", 0, ":tier"),
                (troop_get_upgrade_troop, ":upgrade_troop", ":troop", 1), #try secondary upgrade path first - favours spearmen
                (gt, ":upgrade_troop", 0),
                (neg|troop_is_guarantee_ranged, ":upgrade_troop"),
                (neg|troop_is_guarantee_horse, ":upgrade_troop"),
                (assign, ":troop", ":upgrade_troop"),
            (else_try), 
                (troop_get_upgrade_troop, ":upgrade_troop", ":troop", 0),
                (gt, ":upgrade_troop", 0),
                (assign, ":troop", ":upgrade_troop"),
            (try_end),
        (else_try), #secondary update path
            (try_for_range, ":unused", 0, ":tier"),
                (troop_get_upgrade_troop, ":upgrade_troop", ":troop", 0),
                (gt, ":upgrade_troop", 0),
                (neg|troop_is_guarantee_ranged, ":upgrade_troop"),
                (neg|troop_is_guarantee_horse, ":upgrade_troop"),
                (assign, ":troop", ":upgrade_troop"),
            (else_try), 
                (troop_get_upgrade_troop, ":upgrade_troop", ":troop", 1),
                (gt, ":upgrade_troop", 0),
                (assign, ":troop", ":upgrade_troop"),
            (try_end),
         (try_end),
    (try_end),
            
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),  (spawn_agent, ":troop"),

] + (is_a_wb_sceneprop==1 and [  
    (try_begin), #remove horse
        (agent_get_horse, ":horse", reg0),
        (gt, ":horse", 0),
        (remove_agent, ":horse"),
        (agent_set_visibility, ":horse", 0),
    (try_end),
    ] or []) + [     
       
    (try_begin),
        (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
        (agent_set_team, reg0, 0),
        (agent_set_slot, reg0, slot_agent_target_entry_point, ":instance_no"), #home position
        (agent_set_slot, reg0, slot_agent_walker_type, 2), #patrol
        (store_random_in_range,reg10,1,3), 
        (agent_set_speed_limit, reg0, reg10),
        (assign, ":polearm_found", 0),

] + (is_a_wb_sceneprop==1 and [     
        (try_for_range, ":weapon_slot", 0, 4), #find polearm
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (item_get_type, ":item_type", ":item"),
            (eq, ":item_type", itp_type_polearm),
            #(agent_equip_item, reg0, ":item", 1),
            (agent_set_wielded_item, reg0, ":item"),
            (assign, ":polearm_found", 1),
                (eq, ":var2", 0), #not a patrol
                (try_for_range, ":weapon_slot", 0, 4), #find shield
                    (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
                    (gt, ":item", 1),
                    (item_get_type, ":item_type", ":item"),
                    (eq, ":item_type", itp_type_shield),
                    (agent_set_wielded_item, reg0, ":item"),
                (try_end),
        (try_end),
    ] or []) + [    
        (try_begin),
            (eq, ":polearm_found", 1),
            (eq, ":var2", 0), #not a patrol
            #(neg|troop_is_guarantee_horse, ":troop"),
            (agent_set_position, reg0, pos1),
            (agent_set_animation, reg0, "anim_stand_townguard_polearm"),
        (else_try),
            #(neg|troop_is_guarantee_horse, ":troop"),
            (agent_set_stand_animation, reg0, "anim_stand_townguard"),
        (try_end),
        
        (store_random_in_range, reg6, 0, 100),
        (agent_set_animation_progress, reg0, reg6),
    (else_try),
        (agent_set_team, reg0, 2), #non-player defender team
] + (is_a_wb_sceneprop==1 and [          
        (agent_set_division, reg0, grc_archers), #set them to archers, so they stand ground
        #(agent_set_scripted_destination, reg0, pos1, 0, 1), #make sure
        (agent_ai_set_aggressiveness, reg0, 1), #test
    ] or []) + [        
    (try_end),               
    ])]),

("troop_archer",sokf_invisible,"arrow_helper_blue","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"), 
    (party_get_slot, ":troop", "$current_town", slot_town_archer_troop),
    (set_fixed_point_multiplier, 100),
    (prop_instance_get_scale, pos2, ":instance_no"),
    (position_get_scale_y, ":tier", pos2),
    (val_sub, ":tier", 100),
    (val_div, ":tier", 10),
    (try_begin),
        (ge, ":tier", 1),
        (try_for_range, ":unused", 0, ":tier"),
            (troop_get_upgrade_troop, ":upgrade_troop", ":troop", 0),
            (gt, ":upgrade_troop", 0),
            (troop_is_guarantee_ranged, ":upgrade_troop"),
            (assign, ":troop", ":upgrade_troop"),
        (else_try),
            (troop_get_upgrade_troop, ":upgrade_troop", ":troop", 1),
            (gt, ":upgrade_troop", 0),
            (troop_is_guarantee_ranged, ":upgrade_troop"),
            (assign, ":troop", ":upgrade_troop"),
        (try_end),
    (try_end),
            
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),  (spawn_agent, ":troop"),
    (try_begin),
        (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
        (agent_set_slot, reg0, slot_agent_target_entry_point, ":instance_no"), #home position
        (agent_set_slot, reg0, slot_agent_walker_type, 2), #patrol
        (agent_set_team, reg0, 0),
        (store_random_in_range,reg10,1,3), 
        (agent_set_speed_limit, reg0, reg10),        

] + (is_a_wb_sceneprop==1 and [   
        (assign, ":bow_found", 0),  
        (try_for_range, ":weapon_slot", 0, 4), #find bow
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (item_get_type, ":item_type", ":item"),
            (eq, ":item_type", itp_type_bow),
            #(agent_equip_item, reg0, ":item", 1),
            (agent_set_wielded_item, reg0, ":item"),
            (assign, ":bow_found", 1),
        (try_end),    
        (try_begin),
            (neq, ":bow_found", 1),
            (agent_set_stand_animation, reg0, "anim_stand_townguard"),
        (try_end),
        
        (store_random_in_range, reg6, 0, 100),
        (agent_set_animation_progress, reg0, reg6),
    (else_try),
        (agent_set_team, reg0, 2), #non-player defender team
        (try_for_range, ":weapon_slot", 0, 4), #check if they have a bow
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (item_get_type, ":item_type", ":item"),
            (this_or_next|eq, ":item_type", itp_type_bow),
            (eq, ":item_type", itp_type_thrown),
            (assign, ":bow_found", 1),
        (try_end),
        (neq, ":bow_found", 1),
        (agent_equip_item, reg0, itm_regular_bow, 3),
        (agent_equip_item, reg0, itm_arrows, 4),
        (agent_set_wielded_item, reg0, itm_regular_bow),
    ] or []) + [        
    (try_end),
    ])]),
    
 ("troop_castle_guard",sokf_invisible,"arrow_helper_blue","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),
    (party_get_slot, ":troop", "$current_town", slot_town_castle_guard_troop),
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),  (spawn_agent, ":troop"),
    (try_begin),
        (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
        (agent_set_team, reg0, 0),(agent_set_stand_animation, reg0, "anim_stand_townguard"),(store_random_in_range, reg6, 0, 100),(agent_set_animation_progress, reg0, reg6),
    (else_try),
        (agent_set_team, reg0, 2), #non-player defender team
] + (is_a_wb_sceneprop==1 and [          
        (agent_set_division, reg0, grc_archers), #set them to archers, so they stand ground
        (agent_ai_set_aggressiveness, reg0, 3), #test
    ] or []) + [    
    (try_end),
    ])]),
    
##### TROLLS #####
("troop_troll",sokf_invisible,"arrow_helper_blue","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),
    (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
    (store_faction_of_party, ":fac", "$current_town"),
    (faction_get_slot, ":troop", ":fac", slot_faction_troll_troop),    
    (gt, ":troop", 0),
    (spawn_agent, ":troop"),(agent_set_team, reg0, 0),(agent_set_stand_animation, reg0, "anim_stand"),])]),
  

# ("ZT_mb_", 0, "mesh", "bo_", []), for vanilla flora
# ("ZT_pl_", 0, "mesh", "bo_", []), for gutek's flora
# tree_meshes.brf from vanilla
("ZT_mb_chestnut", 0, "chestnut", "bosimple_tree", []), 
("ZT_mb_oak", 0, "oak_a", "bosimple_tree", []), 
("ZT_mb_oak_wide", 0, "oak_b", "bosimple_tree", []), 
("ZT_mb_lowpoly1", 0, "plane_tree_a", "0", []),   ("ZT_mb_lowpoly2", 0, "plane_tree_b", "0", []),   ("ZT_mb_lowpoly3", 0, "plane_tree_c", "0", []), 
("ZT_mb_pine_wide", 0, "pine", "bosimple_tree", []), 
("ZT_mb_maple", 0, "tree_6_a", "bo_tree_6_a", []), 
# tree_e_meshes.brf from vanilla
("ZT_mb_oak1", 0, "tree_e_1", "bo_tree_e_1", []), ("ZT_mb_oak2", 0, "tree_e_2", "bo_tree_e_2", []), ("ZT_mb_oak3", 0, "tree_e_3", "bo_tree_e_3", []), 
("ZT_mb_poplar1", 0, "tree_f_1", "bo_tree_f_1", []), ("ZT_mb_poplar2", 0, "tree_f_2", "bo_tree_f_1", []), ("ZT_mb_poplar3", 0, "tree_f_3", "bo_tree_f_1", []), 
# xtree_meshes.brf from vanilla
("ZT_mb_chestnut_tall", 0, "tree_2_b", "bo_tree_2_b", []), ("ZT_mb_chestnut_tall2", 0, "tree_2_a", "bo_tree_2_a", []), 
("ZT_mb_plane4", 0, "plane_d", "bo_plane_d", []), 
("ZT_mb_plane1", 0, "tree_plane_a", "bo_tree_plane_a", []), ("ZT_mb_plane2", 0, "tree_plane_b", "bo_tree_plane_b", []), ("ZT_mb_plane3", 0, "tree_plane_c", "bo_tree_plane_c", []), 

("ZT_mb_pine", 0, "pine_1_a", "bo_pine_1_a", []), 
("ZT_mb_pine_blurry", 0, "pine_2_a", "bo_pine_2_a", []), 
("ZT_mb_pine_uppy", 0, "pine_3_a", "bo_pine_3_a", []), 
("ZT_mb_pine_wideuppy", 0, "pine_4_a", "bo_pine_4_a", []), 
("ZT_mb_pine_wideuppy2", 0, "pine_6_a", "bo_pine_6_a", []), 
("ZT_mb_pine_tall", 0, "pine_1_b", "bo_pine_1_b", []), 

("ZT_mb_acacia1", 0, "tree_5_a", "bo_tree_5_a", []), ("ZT_mb_acacia2", 0, "tree_5_b", "bo_tree_5_b", []), ("ZT_mb_acacia3", 0, "tree_5_c", "bo_tree_5_c", []), ("ZT_mb_acacia4", 0, "tree_5_d", "bo_tree_5_d", []), 
("ZT_mb_acacia5", 0, "tree_7_a", "bo_tree_7_a", []), ("ZT_mb_acacia6", 0, "tree_7_b", "bo_tree_7_b", []), ("ZT_mb_acacia7", 0, "tree_7_c", "bo_tree_7_c", []), 

("ZT_mb_maple1", 0, "tree_6_a", "bo_tree_6_a", []), ("ZT_mb_maple2", 0, "tree_6_b", "bo_tree_6_b", []), ("ZT_mb_maple3", 0, "tree_6_c", "bo_tree_6_c", []), ("ZT_mb_maple4", 0, "tree_6_d", "bo_tree_6_d", []), 
# xtree_meshes_b.brf from vanilla  
("ZT_mb_oak_big1", 0, "tree_8_a", "bo_tree_8_a", []), ("ZT_mb_oak_big2", 0, "tree_8_b", "bo_tree_8_b", []), ("ZT_mb_oak_big3", 0, "tree_8_c", "bo_tree_8_c", []), 
("ZT_mb_ash1", 0, "tree_9_a", "bo_tree_9_a", []), ("ZT_mb_ash2", 0, "tree_9_b", "bo_tree_9_a", []), ("ZT_mb_ash3", 0, "tree_9_c", "bo_tree_9_a", []), 
("ZT_mb_slim1", 0, "tree_10_a", "bo_tree_10_a", []), ("ZT_mb_slim2", 0, "tree_10_b", "bo_tree_10_a", []), ("ZT_mb_slim3", 0, "tree_10_c", "bo_tree_10_a", []), 
# xtree_meshes_c.brf from vanilla 
("ZT_mb_yew1", 0, "tree_17_a", "bo_tree_17_a", []), ("ZT_mb_yew2", 0, "tree_17_b", "bo_tree_17_b", []), ("ZT_mb_yew3", 0, "tree_17_c", "bo_tree_17_c", []), ("ZT_mb_yew4", 0, "tree_17_d", "bo_tree_17_d", []), 
("ZT_mb_yew_big", 0, "tree_19_a", "bo_tree_19_a", []), 
# gutek's flora  (does not mix well with vanilla!!)

#MV: removed missing ("ZT_pl_fir4", 0, "PL_fur4", "0", [])
("ZT_pl_fir1", 0, "PL_fur1", "0", []), ("ZT_pl_fir2", 0, "PL_fur2", "0", []), ("ZT_pl_fir3", 0, "PL_fur3", "0", []), 
("ZT_pl_fir_bush1", 0, "PW_bushes09_a", "0", []), ("ZT_pl_fir_bush2", 0, "PW_bushes09_b", "0", []), ("ZT_pl_fir_bush3", 0, "PW_bushes09_c", "0", []), 
("ZT_pl_fir_tall1", 0, "PL_fur_tall1", "0", []), ("ZT_pl_fir_tall2", 0, "PL_fur_tall2", "0", []), ("ZT_pl_fir_tall3", 0, "PL_fur_tall3", "0", []), 

("ZT_pl_fir_shubby1", 0, "PL_fur_tall1", "0", []), ("ZT_pl_fir_shubby2", 0, "PL_fur_tall2", "0", []), ("ZT_pl_fir_shubby3", 0, "PL_fur_tall3", "0", []), 
("ZT_pl_fir_shubby_sm1", 0, "PW_tree_2_a", "bo_PW_tree_2_a", []), ("ZT_pl_fir_shubby_sm2", 0, "PW_tree_2_b", "bo_pw_tree_2_b", []), 
("ZT_pl_birch_y1", 0, "PW_tree_4_a", "bo_pw_tree_4_a", []), ("ZT_pl_birch_y2", 0, "PW_tree_4_b", "bo_pw_tree_4_b", []), 
("ZT_pl_birch_yg1", 0, "PW_tree_18_a", "bo_pw_tree_18_a", []), ("ZT_pl_birch_yg2", 0, "PW_tree_18_b", "bo_pw_tree_18_b", []), 
("ZT_pl_birch_g1", 0, "PW_tree_5_a", "bo_pw_tree_5_a", []), ("ZT_pl_birch_g2", 0, "PW_tree_5_b", "bo_pw_tree_5_b", []), ("ZT_pl_birch_g3", 0, "PW_tree_5_c", "bo_pw_tree_5_c", []), ("ZT_pl_birch_g4", 0, "PW_tree_5_d", "bo_pw_tree_5_d", []), 
("ZT_pl_birch_gg1", 0, "PW_tree_17_a", "bo_pw_tree_17_a", []), ("ZT_pl_birch_gg2", 0, "PW_tree_17_b", "bo_pw_tree_17_b", []), ("ZT_pl_birch_gg3", 0, "PW_tree_17_c", "bo_pw_tree_17_c", []), 
("ZT_pl_birch_gb1", 0, "PW_bushes10_a", "bo_pw_bushes10_a", []), ("ZT_pl_birch_gb2", 0, "PW_bushes10_b", "bo_pw_bushes10_b", []), ("ZT_pl_birch_gb3", 0, "PW_bushes10_c", "bo_pw_bushes10_c", []), ("ZT_pl_birch_gb4", 0, "PW_bushes10_c", "bo_pw_bushes10_c", []), 
("ZT_pl_aspen_yg1", 0, "PW_tree_f_1", "bo_pw_tree_f_1", []), ("ZT_pl_aspen_yg2", 0, "PW_tree_f_2", "bo_pw_tree_f_2", []), ("ZT_pl_aspen_yg3", 0, "PW_tree_f_3", "bo_pw_tree_f_3", []), 
("ZT_pl_aspen_yb1", 0, "PL_aspen_yellowbush1", "0", []), ("ZT_pl_aspen_yb2", 0, "PL_aspen_yellowbush2", "0", []), ("ZT_pl_aspen_yb3", 0, "PL_aspen_yellowbush3", "0", []), 

("ZT_pl_oak_gr1", 0, "PL_oak_group1", "bo_pl_oak_group1", []), ("ZT_pl_oak_gr2", 0, "PL_oak_group2", "bo_pl_oak_group2", []), ("ZT_pl_oak_gr3", 0, "PL_oak_group3", "bo_pl_oak_group3", []), 
("ZT_pl_willow_b1", 0, "PW_bushes02_a", "bo_pw_bushes02_a", []), ("ZT_pl_willow_b2", 0, "PW_bushes02_b", "bo_pw_bushes02_a", []), ("ZT_pl_willow_b3", 0, "PW_bushes02_c", "bo_pw_bushes02_a", []), 

("ZT_pl_shalebush1", 0, "PW_bushes11_a", "0", []), ("ZT_pl_shalebush2", 0, "PW_bushes11_b", "0", []), ("ZT_pl_shalebush3", 0, "PW_bushes11_c", "0", []), 
("ZT_pl_fern1", 0, "PW_fern_a_xx", "0", []), ("ZT_pl_fern2", 0, "PW_fern_b_xx", "0", []), 


#  ("test_vertex_paint_prop", 0, "test_vp_color", "0", []),
("light_green",sokf_invisible,"light_sphere","0",  [ (ti_on_init_scene_prop,
      [   (store_trigger_param_1, ":prop_instance_no"),
          (set_fixed_point_multiplier, 100),
          (prop_instance_get_scale, pos5, ":prop_instance_no"),
          (position_get_scale_x, ":scale", pos5),
          (store_mul, ":red", 2 * 128, ":scale"),
          (store_mul, ":green", 2 * 250, ":scale"),
          (store_mul, ":blue", 2 * 180, ":scale"),
          (val_div, ":red", 100),
          (val_div, ":green", 100),
          (val_div, ":blue", 100),
          (set_current_color,":red", ":green", ":blue"),
          (set_position_delta,0,0,0),
          (add_point_light, 30, 30),
      ]),
    ]),
("door_aw_tomb",sokf_destructible|spr_hit_points(1),"door_a","bo_door_a",   [
   (ti_on_scene_prop_destroy,
    [(store_trigger_param_1, ":instance_no"),
  (prop_instance_get_starting_position, pos1, ":instance_no"),
    (position_move_x, pos1, -100),
    (position_move_y, pos1, 50),
    (position_rotate_z, pos1, 130),
    (prop_instance_animate_to_position, ":instance_no", pos1, 600), #animate in 4 second
    (play_sound, "snd_elf_song"), #dummy_destroyed"),
    (display_message,"@Gate opens... You have reached the most sacred place in Middle Earth!"),
    (scene_slot_eq, "scn_aw_tomb", slot_scene_visited, 0),
    (add_xp_as_reward, 2000),
    (scene_set_slot, "scn_aw_tomb", slot_scene_visited, 1),  ]),
  ]),
## isengard props
("isen_orthanc_tower", 0, "isen_orthanc_tower", "bo_isen_orthanc_tower", []),
("isen_circular_wall", 0, "isen_circular_wall_new", "0", []),
("isen_roof_door", 0, "isen_roof_door", "bo_isen_roof_door", []),
("isen_wood_construction", 0, "isen_wood_construction", "0", []),
("isen_crane", 0, "isen_crane", "bo_isen_crane", []),
("isen_awning", 0, "isen_awning", "bo_arena_block_j_awning", []),
("isen_tower_a", 0, "isen_tower_a", "bo_isen_tower_a", []),
("isen_tower_b", 0, "isen_tower_b", "bo_isen_tower_b", []),
("isen_stairs", 0, "isen_stairs", "bo_isen_stairs", []),
("isen_battlement_corner", 0, "isen_battlement_corner", "bo_isen_battlement_corner", []),
("isen_square_keep_a", 0, "isen_square_keep_a", "bo_isen_square_keep_a", []),
("isen_gate_house_a", 0, "isen_gate_house_a", "bo_isen_gate_house_a", []),
("isen_post_a", 0, "isen_post_a", "bo_isen_post_a", []),
("isen_gate_big", 0, "isen_gate", "bo_isen_gate", []),
("isen_passage_house", 0, "isen_passage_house", "bo_isen_passage_house", []),
("isen_good_ring_10", 0, "isen_good_ring_10", "bo_isen_good_ring_10", []),
  
("isen_isengard_throne", 0, "isengard_throne", "bo_isengard_throne", []),
 
 ] + (is_a_wb_sceneprop==1 and [ 
("dead_marshes_a",sokf_moveable,"deadmarshes_1","0",dead_marches_effect),
("dead_marshes_b",sokf_moveable,"deadmarshes_2","0",dead_marches_effect),
("dead_marshes_c",sokf_moveable,"deadmarshes_3","0",dead_marches_effect),
("dead_marshes_d",sokf_moveable,"deadmarshes_4","0",dead_marches_effect),
("dead_marshes_e",sokf_moveable,"deadmarshes_5","0",dead_marches_effect),
 ] or [
("dead_marshes_a",0,"dead_a","0",[(ti_on_init_scene_prop,[(set_position_delta,0,0,47),(particle_system_add_new,"psys_candle_light_small")])]),
("dead_marshes_b",0,"dead_b","0",[(ti_on_init_scene_prop,[(set_position_delta,0,0,47),(particle_system_add_new,"psys_candle_light_small")])]),
("dead_marshes_c",0,"dead_c","0",[(ti_on_init_scene_prop,[(set_position_delta,0,0,47),(particle_system_add_new,"psys_candle_light_small")])]),
("dead_marshes_d",0,"dead_d","0",[(ti_on_init_scene_prop,[(set_position_delta,0,0,47),(particle_system_add_new,"psys_candle_light_small")])]),
("dead_marshes_e",0,"dead_e","0",[(ti_on_init_scene_prop,[(set_position_delta,0,0,47),(particle_system_add_new,"psys_candle_light_small")])]),
 ]) + [  


("isen_wood_construction_b", 0, "isen_wood_construction_b", "bo_isen_wood_construction_b", []),
("prop_cage_rusty", 0, "prop_cage_rusty", "0", []),
("wagon_c", 0, "wagon_c", "0", []),
("mt_fountain", 0, "mt_fountain", "bo_mt_fountain", []),
("gondor_ruined_fountain", 0, "ruined_fountain", "bo_ruined_fountain", []),
("palantir", 0, "palantir", "bo_palantir", []),
("mt_horse_statue", 0, "mt_horse_statue", "bo_mt_statue", []),
("gondor_ruined_horse_statue", 0, "ruined_horse_statue", "0", []),
("gondor_ruined_horse_statue_head", 0, "ruined_horse_statue_head", "0", []),
("large_fire_pit", 0, "large_fire_pit", "0", []),
("gondor_altar", 0, "altar", "bo_altar", []),
("tree_mallorn_a", 0, "tree_mallorn_a", "bo_tree_mallorn_a", []),
("tree_mallorn_b", 0, "tree_mallorn_b", "bo_tree_mallorn_b", []),
("tree_mallorn_c", 0, "tree_mallorn_c", "bo_tree_mallorn_c", []),
("tree_mallorn_roots_1", 0, "tree_mallorn_roots_1", "0", []),
("tree_mallorn_roots_2", 0, "tree_mallorn_roots_2", "0", []),
("tree_mallorn_roots_3", 0, "tree_mallorn_roots_3", "0", []),
("tree_mallorn_roots_4", 0, "tree_mallorn_roots_4", "0", []),
("tent_a", 0, "tent_a", "bo_tent_a", []),
("tent_b", 0, "tent_b", "bo_tent_b", []),
("tent_c", 0, "tent_c", "bo_tent_c", []),
("tent_d", 0, "tent", "bo_tent", []),
("gondor_man_statue", 0, "gondor_statue", "bo_gondor_statue", []),
("gondor_ruined_man_statue", 0, "ruined_man_statue", "0", []),
("gondor_ruined_man_torso", 0, "ruined_man_torso", "0", []),
("rohan_tapestry_a", 0, "tapestry_rohirrim_a", "0", []),
("rohan_tapestry_b", 0, "tapestry_rohirrim_b", "0", []),
("rohan_tapestry_c", 0, "tapestry_rohirrim_c", "0", []),

("osgiliath_broken_bridge_beams", 0, "osgiliath_broken_bridge_beams", "bo_osgiliath_broken_bridge_beams", []),

("banner_stand_a", 0, "battle_banner_stand_a", "0", []),
("banner_stand_b", 0, "battle_banner_stand_b", "0", []),
("banner_stand_orc", 0, "orc_banner_stand", "0", []),
## Brutus tents
("elf_tent_short", 0, "elfTentShort", "bo_elfTentShort", []),
("elf_tent_tall", 0, "elfTentTall", "bo_elfTentTall", []),
("orc_tent_small", 0, "orcTentSmall", "bo_orcTentSmall", []),
("rhun_tent_large", 0, "rhunTentLarge", "bo_rhunTentLarge", []),
("rhun_yurt", 0, "rhunYurt", "bo_rhunYurt", []),
("khand_tent_a", 0, "khandTent_a", "bo_khandTent_a", []),
("khand_tent_b", 0, "khandTent_b", "bo_khandTent_a", []),
("harad_tent_tusks", 0, "haradTentTusks", "bo_haradTentTusks", []),
("harad_tent_a", 0, "haradTent_a_new", "bo_khandTent_a", []),
("harad_tent_b", 0, "haradTent_b_new", "bo_khandTent_a", []),

# Romainoir Rohan buildings
("rohan_birdhouse",0,"rohan_birdhouse","bo_birdhouse",[]),
  ("rohan_birdhouse_E",0,"rohan_birdhouse","0",[]),
("rohan_platform",0,"rohan_platform","bo_rangefoin",[]),
  ("rohan_platform_E",0,"rohan_platform","0",[]),
("rohan_meduseld",0,"rohan_meduseld","bo_meduseld",[]),
("rohan_house1",0,"rohan_house1","bo_house1",[]),
  ("rohan_house1_E",0,"rohan_house1","0",[]),
("rohan_house2",0,"rohan_house2","bo_house2",[]),
  ("rohan_house2_E",0,"rohan_house2","0",[]),
("rohan_house3",0,"rohan_house3","bo_house3",[]),
  ("rohan_house3_E",0,"rohan_house3","0",[]),
("rohan_house4",0,"rohan_house4","bo_house4",[]),
  ("rohan_house4_E",0,"rohan_house4","0",[]),
("rohan_house5",0,"rohan_house5","bo_house5",[]),
  ("rohan_house5_E",0,"rohan_house5","0",[]),
("rohan_stables",0,"rohan_stables","bo_stables",[]),
  ("rohan_stables_E",0,"rohan_stables","0",[]),
("rohan_watchtower",0,"rohan_watchtower","bo_tourrohan",[]),
  ("rohan_watchtower_E",0,"rohan_watchtower","0",[]),
("rohan_stonebase",0,"rohan_stonebase","bo_rohan_stonebase",[]),
  ("rohan_stonebase_E",0,"rohan_stonebase","0",[]),
("rohan_fountain",0,"edoras_fountain","bo_edoras_fountain",[]),
 
# Llew Rohan buildings
("rohan_palisade",0,"rohan_palisade_a","bo_rohan_palisade_a",[]),
  ("rohan_palisade_E",0,"rohan_palisade_a","0",[]),
("rohan_palisade_slope",0,"rohan_palisade_b","bo_rohan_palisade_b",[]),
  ("rohan_palisade_slope_E",0,"rohan_palisade_b","0",[]),
("rohan_house6",0,"rohan_house6","bo_house6",[]),
  ("rohan_house6_E",0,"rohan_house6","0",[]),
("rohan_house7",0,"rohan_house7","bo_house7",[]),
  ("rohan_house7_E",0,"rohan_house7","0",[]),

# Kolba Erebor dungeon stuff  
("spear_trap_1",0,"spear_trap","bo_spear_trap", []),
("erebor_dungeon_01",0,"dungeon_a","bo_dungeon_a",[]),
("barrier_cylinder", sokf_invisible, "cyl","bo_cyl",[]), 
("LMH_ground_a",0,"LMH_ground_a","bo_LMH_ground_a",[]),
("LMH_ground_b",0,"LMH_ground_b","bo_LMH_ground_b",[]),
("LMH_ground_c",0,"LMH_ground_c","bo_LMH_ground_c",[]),
("LMH_pillar_a",0,"LMH_pillar_a","bo_LMH_pillar_a",[]),
("LMH_pillar_b",0,"LMH_pillar_b","bo_LMH_pillar_b",[]),
("LMH_pillar_c",0,"LMH_pillar_c","bo_LMH_pillar_c",[]),
("LMH_arch",0,"LMH_arch","bo_LMH_arch",[]),
("LMH_base",0,"LMH_base","bo_LMH_base",[]),
("LMH_wall_a",0,"LMH_wall_a","bo_LMH_wall_a",[]),
  
("thranduil_hall",0,"thranduil_hall","bo_thranduil_hall", [(ti_on_scene_prop_init,[(set_fog_distance,210,0x015050),]),]),
("thranduil_helm1",0,"statuemirk_helm1","0",[]),
("thranduil_helm2",0,"statuemirk_helm2","0",[]),
("thranduil_helm3",0,"statuemirk_helm3","0",[]),
("thranduil_bow",0,"statuemirk_bow","0",[]),
("thranduil_longsword",0,"statuemirk_longsword","0",[]),
("thranduil_whiteknife",0,"statuemirk_white_knife","0",[]),
("thranduil_greatspear",0,"statuemirk_great_spear","0",[]),
("thranduil_warspear",0,"statuemirk_war_spear","0",[]),
("thranduil_medshield",0,"statuemirk_med_shield","0",[]),

("door_erebor",sokf_destructible|spr_hit_points(5001),"door_a","bo_door_a",   [
   (ti_on_scene_prop_destroy,
    [(store_trigger_param_1, ":instance_no"),
  (prop_instance_get_starting_position, pos1, ":instance_no"),
    (position_move_x, pos1, -100),
    (position_move_y, pos1, 50),
    (position_rotate_z, pos1, 130),
    (prop_instance_animate_to_position, ":instance_no", pos1, 600), #animate in 4 second
    (play_sound, "snd_dummy_destroyed"),
  (display_message,"@Secret place discovered!"),
    (try_for_agents, ":cur_agent"),
      (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
      (this_or_next|eq, ":cur_agent_troop", "trp_i1_gunda_goblin"),
      (this_or_next|eq, ":cur_agent_troop", "trp_i4_gunda_orc_warrior"),
      (eq, ":cur_agent_troop", "trp_i3_gunda_orc_fighter"),
      (agent_set_team, ":cur_agent", 1),
    (try_end)])]),

("moria_altar",0,"moria_altar","bo_moria_altar",[]),
("moria_rubble",0,"moria_rubble","bo_moria_rubble",[]),
("moria_rubble_wall",0,"moria_rubble_wall","bo_moria_rubble_wall",[]),
("moria_rubble_blocks",0,"moria_rubble_blocks","bo_moria_rubble_blocks",[]),

("elf_bridge",0,"elf_bridge","bo_elf_bridge",[]),  
("elf_ramp",0,"elf_ramp","bo_elf_ramp",[]),  
("elf_treehouse",0,"elf_treehouse","bo_elf_treehouse",[]),  

("rohan_woodstairs",0,"rohan_woodstairs","bo_rohan_woodstairs",[]),
("arabian_lighthouse_a",0,"arabian_lighthouse_a","bo_arabian_lighthouse_a", []), #WB

("thranduil_hall_entrance",0,"thranduil_hall_entrance","bo_thranduil_hall_entrance",[]),
("thranduil_throne",0,"thranduil_throne","bo_thranduil_throne",[]),
("distant_mountain_white",sokf_place_at_origin|sokf_moveable,"mountains_outer","0",[]),
("distant_mountain_white_farther",sokf_place_at_origin|sokf_moveable,"mountains_outer_farther","0",[]),
  
("rock_cliff",0,"cliff","bo_cliff",[]),
("rock_cliff_a",0,"cliff_a","bo_cliff_a",[]),
("rock_cliff_b",0,"cliff_b","bo_cliff_b",[]),
("rock_cliff_c",0,"cliff_distant_1","bo_cliff_distant_1",[]),
("rock_cliff_d",0,"cliff_distant_2","bo_cliff_distant_2",[]),
("rock_cliff_e",0,"cliff_distant_3","bo_cliff_distant_3",[]),
("rock_cliff_f",0,"cliff_distant_4","bo_cliff_distant_4",[]),
("rock_cliff_g",0,"cliff_distant_5","bo_cliff_distant_5",[]),
("rock_cliff_h",0,"cliff_distant_6","bo_cliff_distant_6",[]),
("rock_cliff_i",0,"cliff_distant_7","bo_cliff_distant_7",[]),
("rock_cliff_j",0,"cliff_distant_8","bo_cliff_distant_8",[]),
("rock_mountain",0,"mountain_scene","bo_mountain_scene",[]), 
#("rock_cliff_1",0,"rock_cliff_1","bo_rock_cliff_1",[]),
#("rock_boulder_1",0,"rock_boulder_1","bo_rock_boulder_1",[]),
#("rock_flat_1",0,"rock_flat_1","bo_rock_flat_1",[]),

("argo1",0,"argo1","bo_argo1",[]),
("argo2",0,"argo2","bo_argo2",[]),
#("argo3",0,"argo3","0",[]),
("mist_a",sokf_moveable,"mist_a","0",[]),
("mist_b",sokf_moveable,"mist_b","0",[]),

###InVain added treeline collision better usability in editor

("treeline_a",0,"treeline_a","bo_treeline_b",[]),
("treeline_b",0,"treeline_b","bo_treeline_b",[]),
("treeline_c",0,"treeline_c","bo_treeline_b",[]),

("ruins_amon_hen",0,"ruins_amon_hen","bo_ruins_amon_hen",[]),
("ruins_tower",0,"ruins_tower","bo_ruins_tower",[]),

###TLD Tunnel System###
("tunnel_short",0,"tunnel_short","bo_tunnel_short", []),
("tunnel_straight",0,"tunnel_straight","bo_tunnel_straight", []),
("tunnel_curved",0,"tunnel_curved","bo_tunnel_curved", []),
("tunnel_support",0,"tunnel_support","bo_tunnel_support", []),
("tunnel_sloped",0,"tunnel_sloped","bo_tunnel_sloped", []),
("tunnel_split",0,"tunnel_split","bo_tunnel_split", []),
("tunnel_crossing",0,"tunnel_crossing","bo_tunnel_crossing", []),
("tunnel_chasm",0,"chasm","bo_chasm", []),
  
("rohan_burial_mound",0,"roh_burial_mound","bo_roh_burial_mound", []), 
("tree_huorn",0,"tree_huorn","0", []), 
("waterfall_stream",0,"waterfall_stream","0", [(ti_on_init_scene_prop,[(play_sound, "snd_waterfall")])]),
("waterfall",0,"waterfall","bo_waterfall", []),
("tunnel_cave",0,"tunnel_cave","bo_tunnel_cave", []), 

("moria_a",0,"moria_hall","bo_moria_hall", []), 
("moria_entry_a",0,"moria_entry_a","bo_moria_entry_a", []), 
("moria_stairs_a",0,"moria_stairs_a","bo_moria_stairs_a", []), 
("moria_corridor_a",0,"moria_corridor_a","bo_moria_corridor_a", []), 
("moria_direction_a",0,"moria_direction_a","bo_moria_direction_a", []), 
("moria_corridor_b",0,"moria_corridor_b","bo_moria_corridor_b", []), 
("moria_cell_a",0,"moria_cell_a","bo_moria_cell_a", []), 
("moria_entry_b",0,"moria_entry_b","bo_moria_entry_b", []), 
("moria_room_a",0,"moria_room_a","bo_moria_room_a", []), 
("moria_stairs_b",0,"moria_stairs_b","bo_moria_stairs_a", []), 
("moria_cell_b",0,"moria_cell_b","bo_moria_cell_b", []), 
("moria_tower_stairs_a",0,"moria_tower_stairs_a","bo_moria_tower_stairs_a", []), 
("moria_tower_cell_a",0,"moria_tower_cell_a","bo_moria_tower_cell_a", []), 
#fog triggers
("light_fog_black0",sokf_invisible,"f0_pointer","0",  []),
("light_fog_black1",sokf_invisible,"f1_pointer","0",  []),
("light_fog_black2",sokf_invisible,"f2_pointer","0",  []),
("light_fog_black3",sokf_invisible,"f3_pointer","0",  []),
("light_fog_black4",sokf_invisible,"f4_pointer","0",  []),
("light_fog_black5",sokf_invisible,"f5_pointer","0",  []),
("moria_rock",0,"moria_rock","bo_moria_rock", []),

("tunnel_sunshield", 0, "tunnel_sunshield", "0", []),
("darkness_portal",0,"darkness_portal","0", []), 


#horse spawns
("horse_riv_warhorse",sokf_invisible,"rivendell_warhorse01","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_riv_warhorse", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_riv_warhorse2",sokf_invisible,"rivendell_warhorse02","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_riv_warhorse2", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_sumpter_horse",sokf_invisible,"sumpter_horse","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_sumpter_horse", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_saddle_horse",sokf_invisible,"saddle_horse","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_saddle_horse", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_steppe_horse",sokf_invisible,"steppe_horse","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_steppe_horse", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_courser",sokf_invisible,"courser","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_courser", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_hunter",sokf_invisible,"hunting_horse","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_hunter", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_rohirrim_courser",sokf_invisible,"rohan_horse01","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_rohirrim_courser", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_rohirrim_hunter",sokf_invisible,"rohan_horse02","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_rohirrim_hunter", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_rohirrim_courser2",sokf_invisible,"rohan_horse03","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_rohirrim_courser2", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_rohan_warhorse",sokf_invisible,"rohan_warhorse01","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_rohan_warhorse", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_thengel_warhorse",sokf_invisible,"rohan_warhorse02","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_thengel_warhorse", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_rhun_horse_a",sokf_invisible,"rhunhorselight1","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_rhun_horse_a", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_rhun_horse_b",sokf_invisible,"rhunhorselight2","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_rhun_horse_b", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_rhun_horse_d",sokf_invisible,"rhunhorselight4","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_rhun_horse_d", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_rhun_horse_e",sokf_invisible,"rhunhorseheav1","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_rhun_horse_e", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_harad_horse",sokf_invisible,"harad_horse01","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_harad_horse", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_harad_warhorse",sokf_invisible,"harad_horse02","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_harad_warhorse", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_variag_pony",sokf_invisible,"horse_c","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_variag_pony", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_variag_kataphrakt",sokf_invisible,"easterling_warhorse01","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_variag_kataphrakt", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_mordor_warhorse",sokf_invisible,"mordor_warhorse01","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_mordor_warhorse", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_gondor_courser",sokf_invisible,"gondor_horse02","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_gondor_courser", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_gondor_hunter",sokf_invisible,"gondor_horse01","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_gondor_hunter", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_dol_amroth_warhorse",sokf_invisible,"da_warhorse02","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_dol_amroth_warhorse", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_dol_amroth_warhorse2",sokf_invisible,"da_warhorse01","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_dol_amroth_warhorse2", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_gondor_warhorse",sokf_invisible,"gondor_warhorse01","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_gondor_warhorse", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_gondor_lam_horse",sokf_invisible,"lam_warhorse01","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_gondor_lam_horse", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("horse_pony",sokf_invisible,"pony","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_pony", 0),(agent_set_stand_animation, reg0, "anim_horse_stand"),])]),
("harad_oliphant",sokf_invisible,"oliphant_base","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_oliphant", 0),
  (agent_set_speed_limit, reg0, 0),
  (agent_set_stand_animation, reg0, "anim_oliphant_stand"),(agent_set_animation, reg0, "anim_oliphant_stand")])]),
("spiderweb",0,"0","0", []), #unused
("tunnel_dirt",0,"dirt","0", []),
("tunnel_liana",0,"liana_new","0", []),
("tunnel_liana2",0,"liana2","0", []),
("tunnel_mushroom1",0,"mushroom1","0", []),
("tunnel_mushroom2",0,"mushroom2","0", []),
("tunnel_mushroom3",0,"mushroom3","0", []),
("tunnel_mushroom4",0,"mushroom4","0", []),
("tunnel_mushroom5",0,"mushroom5","0", []),
("tunnel_root",0,"root","0", []),
("tunnel_spiderweb1",0,"spiderweb1","0", []),
("tunnel_spiderweb2",0,"spiderweb2","0", []),
("tunnel_spiderweb3",0,"spiderweb3","0", []),
("tunnel_crystal1",0,"crystal1","bo_crystal134", []),
("tunnel_crystal2",0,"crystal2","bo_crystal256", []),
("tunnel_crystal3",0,"crystal3","bo_crystal134", []),
("tunnel_crystal4",0,"crystal4","bo_crystal134", []),
("tunnel_crystal5",0,"crystal5","bo_crystal256", []),
("tunnel_crystal6",0,"crystal6","bo_crystal256", []),
("smith_anvil",0,"anvil","0",[]),
("smith_hammer",0,"smith_hammer","0",[]),
("book_open",0,"JIKBookOpen","0",[]),
("book_closed",0,"JIKBookClosed","0",[]),
#("book_open",0,"big_book","0",[]),
("book_scroll",0,"quenya_scroll","0",[]),
("prop_cage_wheeled", 0, "wheeled_cage", "bo_wheeled_cage", []),
("door_iron", 0, "door_iron", "bo_door_iron", []),
("rock_elf", 0, "rock_elf", "bo_rock_elf", []),
("rohan_horn", 0, "horn", "0", []),
("tunnel_stalactite", 0, "tunnel_stalactite", "bo_tunnel_stalactite", []),
("fog_scene",0,"0","0",[(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),
  (prop_instance_get_position, pos1, ":instance_no"),
  (particle_system_add_new,"psys_scene_fog",pos1)]),]), #InVain changed this so the fog actually shows up!
("elf_galadriel_table", 0, "galadriel_table", "0", []),
("elf_lamp_lorien_1", 0, "lamp_lorien_1", "0", []),
("elf_lamp_lorien_2", 0, "lamp_lorien_2", "0", []),
("elf_waterplant", 0, "waterplant", "0", []),
("elf_statue", 0, "statue", "0", []),
("distant_mountain_mordor",sokf_place_at_origin|sokf_moveable,"mountains_outer_mordor","0",[]),
("tunnel_henneth_annun",0,"mesh_henneth_annun","bo_henneth_annun",[]),

("horse_player_horse",sokf_invisible,"mearh","0", [(ti_on_init_scene_prop,[
  (eq, "$spawn_horse", 1),
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"),
    (troop_get_inventory_slot, ":horse", "trp_player", 8),
  (gt, ":horse", 1),
  (set_spawn_position, pos1),(spawn_horse,":horse", 0),(agent_set_stand_animation, reg0, "anim_horse_stand")])]),
  
("mt_tirith_gate",0,"tirith_gate","bo_tirith_gate", []),
("rohan_meduseld_table",0,"rohan_meduseld_int_table","bo_rohan_meduseld_int_table", []),
("handsign",0,"handsign_prop","bo_handsign",[]),

("ai_limiter_gate_breached" ,sokf_invisible|sokf_type_ai_limiter|sokf_moveable,"barrier_8m" ,"bo_barrier_8m" , []), # all instances moved away when gate_destructible is destroyed
("barrier_cube" ,sokf_invisible,"collision_cube" ,"bo_collision_cube", []), #a poli-efficient replacement for some colmeshes 

("fog_elven_settlement",sokf_invisible|sokf_place_at_origin,"collision_cube", "0", [(ti_on_scene_prop_init,[(set_fixed_point_multiplier, 100),
  (try_begin),(is_currently_night),(set_fog_distance,3000,0xeFFF3D),(else_try),(set_fog_distance,3000,0xeFFF3D),] + (is_a_wb_sceneprop==1 and [ (set_startup_ambient_light, 95, 95, 75), ] or []) + [  (try_end)])]),
("fog_darkish_glow",sokf_invisible|sokf_place_at_origin,"collision_cube", "0", [ #Mordor and Minas Tirith siege, Erebor
     (ti_on_scene_prop_init,[ (store_trigger_param_1, ":instance_no"),(set_fixed_point_multiplier, 1000), (prop_instance_get_position, pos2, ":instance_no"), (position_move_z, pos2, 2000), (prop_instance_set_position, ":instance_no", pos2),
     (prop_instance_get_scale, pos1, ":instance_no"), (position_get_scale_x, ":scale", pos1),
         (try_begin),(is_currently_night),(eq, "$bright_nights", 1), (val_mul, ":scale", 2),(val_div, ":scale", 3),
         (else_try),(is_currently_night),(set_fog_distance,130,0x010101), (val_div, ":scale", 2),
         ] + (is_a_wb_sceneprop==1 and [ (set_startup_ambient_light, 25, 25, 25),(set_startup_sun_light, 5, 5, 5),(set_startup_sun_light, 2, 2, 2),(set_startup_ground_ambient_light, 12, 12, 12), ] or []) + [ 
         (else_try),
         (set_fog_distance,200,0x010101), ] + (is_a_wb_sceneprop==1 and [  (set_startup_ambient_light, 40, 40, 40),(set_startup_sun_light, 10, 10, 10),(set_startup_ground_ambient_light, 12, 12, 12), ] or []) + [ 
         (try_end),
         (set_fog_distance,":scale",0x010101),
         (eq, ":scale", 1000), #only show tutorial message if scale is unchanged
          ] + (is_a_wb_sceneprop==1 and [ (is_edit_mode_enabled), ] or []) + [ 
         (display_message, "@{!} debug: scale up down to increase/decrease fog distance, default is 1000m."),
        (display_message, "@{!} debug: scale prop to disable this message"),
     ])]),
("fog_reddish_glow",sokf_invisible|sokf_place_at_origin,"collision_cube", "0", [# Goblin town and Isengard underground
    (ti_on_scene_prop_init,[(set_fixed_point_multiplier, 100),
        (set_fog_distance,80,0x0F0200),
        ] + (is_a_wb_sceneprop==1 and [ (set_startup_ambient_light, 12, 9, 9),(set_startup_sun_light, 75, 75, 75), ] or []) + [
  ])]),
("fog_greenish_glow",sokf_invisible|sokf_place_at_origin,"collision_cube", "0", [ #Mirkwood
    (ti_on_scene_prop_init,[(set_fixed_point_multiplier, 100),
  (try_begin),(is_currently_night),(eq, "$bright_nights", 1), (set_fog_distance,300,0x0F190F),(else_try),(is_currently_night),(set_fog_distance,250,0x090F09),(else_try),(set_fog_distance,400,0x172617),(try_end)])]),
  
("isen_furnace",0,"isen_furnace","bo_isen_furnace", []),
("isen_wall",0,"isen_wall","bo_isen_wall", []),
("isen_sink",0,"isen_sink","bo_isen_sink", []),
("isen_forge",0,"isen_forge","bo_isen_forge", []),
("isen_metal",0,"isen_metal","bo_isen_metal", []),
("isen_cave",0," isen_cave","bo_isen_cave", []),
("isen_chasm",0,"isen_chasm","bo_isen_chasm", []),
("horse_warg_1C",sokf_invisible,"warg_1C","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_warg_1c", 0),(agent_set_stand_animation, reg0, "anim_horse_stand")])]),
("horse_warg_1D",sokf_invisible,"warg_1D","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
  (spawn_horse,"itm_warg_1d", 0),(agent_set_stand_animation, reg0, "anim_horse_stand")])]),
("troop_human_prisoner",sokf_invisible,"arrow_helper_blue","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
    (spawn_agent, "trp_human_prisoner"),(agent_set_team, reg0, 0),(agent_set_stand_animation, reg0, "anim_sit_on_ground")])]),
("troop_guard_sitting",sokf_invisible,"sitting","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),
    (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
    (party_get_slot, ":troop", "$current_town", slot_town_guard_troop),
  (spawn_agent, ":troop"),(agent_set_team, reg0, 0),(agent_set_stand_animation, reg0, "anim_sit_on_ground"),
  
  #for better clip control
  ] + (is_a_wb_sceneprop==1 and [ 
        (agent_set_no_dynamics, reg0, 1),
        (agent_ai_set_interact_with_player, reg0, 0),       
        (troop_get_type, ":race", ":troop"),
        (try_begin), 
            (eq, ":race", tf_orc),
            (position_move_z, pos1, 15), #small races move 30cm upwards
        (else_try),
            (eq, ":race", tf_dwarf),
            (position_move_z, pos1, 40),
        (try_end),
        (agent_set_position, reg0, pos1),
    ] or []) + [  
  ])]),

("sound_waterfall"       ,sokf_invisible,"collision_cube","0", [(ti_on_init_scene_prop,[(set_position_delta,0,0,0),(play_sound, "snd_waterfall", 0)])]),
("sound_water_wavesplash",sokf_invisible,"collision_cube","0", [(ti_on_init_scene_prop,[(set_position_delta,0,0,0),(play_sound, "snd_water_wavesplash_source", 0)])]),
("sound_water_waves"     ,sokf_invisible,"collision_cube","0", [(ti_on_init_scene_prop,[(set_position_delta,0,0,0),(play_sound, "snd_water_waves_source", 0)])]),
("sound_water_splash"    ,sokf_invisible,"collision_cube","0", [(ti_on_init_scene_prop,[(set_position_delta,0,0,0),(play_sound, "snd_water_splash_source", 0)])]),

("distant_outer_tirith",sokf_place_at_origin|sokf_moveable,"outer_tirith","0",[]),

("gothic_chair_nocol",0,"gothic_chair",  "0", []), #swy--disabled collision so Denethor can sit correctly on Minas Tirith's castle without looking funny.
("smaug_skeleton",    0,"smaug_skeleton","0", []), #swy--added unused but otherwise pretty cool (both technically and artistically) Smaug skeleton, for the Lone Mountain I guess.

("dorwinion_sack",sokf_type_container,"dorwinion_sack","bo_dorwinion_sack", []), # Kham - for Spears quest 
("pointer_arrow", 0, "pointer_arrow", "0", []),

#InVain props start

("fake_house_a",0,"MT_fake_house_a","bo_fake_house_a", []),
("fake_house_b",0,"MT_fake_house_b","bo_fake_house_b", []),
("fake_house_c",0,"MT_fake_house_c","bo_fake_house_c", []),
("fake_house_d",0,"MT_fake_house_d","bo_fake_house_d", []),
("fake_house_e",0,"MT_fake_house_e","bo_fake_house_e", []),
("fake_house_f",0,"MT_fake_house_f","bo_fake_house_f", []),

("fake_house_far_a",0,"MT_fake_house_far_a","bo_fake_house_far_a", []),
("fake_house_far_b",0,"MT_fake_house_far_b","bo_fake_house_far_b", []),
("fake_house_far_c",0,"MT_fake_house_far_c","bo_fake_house_far_c", []),
("fake_house_far_d",0,"MT_fake_house_far_d","bo_fake_house_far_d", []),
("fake_house_far_e",0,"MT_fake_house_far_e","bo_fake_house_far_e", []),
("fake_house_far_f",0,"MT_fake_house_far_f","bo_fake_house_far_f", []),

("Dale_fake_house_a",0,"Dale_fake_house_a","bo_fake_house_a", []),
("Dale_fake_house_b",0,"Dale_fake_house_b","bo_fake_house_b", []),
("Dale_fake_house_c",0,"Dale_fake_house_c","bo_fake_house_c", []),
("Dale_fake_house_d",0,"Dale_fake_house_d","bo_fake_house_d", []),
("Dale_fake_house_e",0,"Dale_fake_house_e","bo_fake_house_e", []),
("Dale_fake_house_f",0,"Dale_fake_house_f","bo_fake_house_f", []),

("Dale_fake_house_far_a",0,"Dale_fake_house_far_a","bo_fake_house_far_a", []),
("Dale_fake_house_far_b",0,"Dale_fake_house_far_b","bo_fake_house_far_b", []),
("Dale_fake_house_far_c",0,"Dale_fake_house_far_c","bo_fake_house_far_c", []),
("Dale_fake_house_far_d",0,"Dale_fake_house_far_d","bo_fake_house_far_d", []),


("Dale_castle_small_round_tower",0,"Dale_small_round_tower_a","bo_arabian_castle_corner_b", []),
("Dale_castle_small_round_tower_roof",0,"Dale_small_round_tower_roof_a","bo_small_round_tower_roof_a", []),
("Dale_castle_Stone_Stairs",0,"Dale_stone_stairs_b","bo_stone_stairs_b", []),
("Dale_tower_top_a",0,"dale_tower_top_1","0", []),
("Dale_tower_top_c",0,"dale_tower_top_3","0", []),
("Dale_castle_Gate_House",0,"Dale_gate_house_b","bo_Dale_gate_house_b", []),
("Dale_castle_High_Tower",0,"Dale_castle_e_tower","bo_castle_e_tower", []),
("Dale_Bell_Tower",0,"Dale_church_tower_a","bo_Dale_church_tower_a", []),
("Dale_Minaret",0,"Dale_stone_minaret_a","bo_stone_minaret_a", []),
("Dale_Hall",0,"novgorod_sofiya","bo_novgorod_sofiya", []),
("Dale_Palace",0,"sobor","bo_sobor", []),
("Dale_Market",0,"Dale_castle_courtyard_a","bo_castle_courtyard_a", []),
("Dale_castle_Gaillard",0,"Dale_castle_gaillard","bo_castle_gaillard", []),
("Dale_castle_Battlement",0,"Dale_castle_battlement_b","bo_arabian_castle_battlement_a", []),
( "Dale_copula_1"                              ,0,"dale_cupola_1","0",[]),
( "Dale_town_house_b"                          ,0,"Dale_town_house_b","bo_town_house_b",[]),
( "Dale_copula_2"                              ,0,"dale_cupola_2","0",[]),
( "Dale_town_house_d"                          ,0,"Dale_town_house_d","bo_town_house_d",[]),
( "Dale_town_house_f"                          ,0,"Dale_town_house_f","bo_town_house_f",[]),
( "Dale_copula_3"                          ,0,"dale_cupola_3","0",[]),
( "Dale_tower_top_b"                          ,0,"dale_tower_top_2","0",[]),
( "Dale_copula_4"                          ,0,"dale_cupola_5","0",[]),
( "Dale_copula_5"                          ,0,"dale_cupola_7","0",[]),
( "Dale_copula_6"                          ,0,"dale_cupola_8","0",[]),

("Dale_small_wall",0,"Dale_small_wall","bo_small_wall_d", []),
("Dale_passage_house_b",0,"Dale_new_passage_house","bo_passage_house_b", []),
("Dale_Plaza",0,"Dale_Plaza","bo_Dale_Plaza", []),
("Dale_street_short",0,"Dale_street_short","bo_Dale_street_short", []),
("Dale_castle_battlement_d",0,"Dale_castle_battlement_d","bo_arabian_castle_battlement_d", []),
("Dale_castle_courtyard_house_extension_a_E",0,"Dale_castle_courtyard_house_extension_a","0", []),
("Dale_castle_courtyard_house_extension_b_E",0,"Dale_castle_courtyard_house_extension_b","0", []),
("Dale_castle_courtyard_entry_b",0,"Dale_courtyard_entry_b","bo_Dale_courtyard_entry_b", []),
("Dale_castle_courtyard_house_b",0,"Dale_castle_courtyard_house_a","bo_castle_courtyard_house_b", []),


#InVain: WB only props below, hidden (no asset) in M&B
("ship"                                       ,0,"ship","bo_ship",[]),
("ship_b"                                     ,0,"ship_b","bo_ship_b",[]),
("ship_d"                                     ,0,"ship_d","bo_ship_d",[]),
("ship_c"                                     ,0,"ship_c","bo_ship_c",[]),
("ship_sail_off"                              ,0,"ship_sail_off","bo_ship_sail_off",[]),
("ship_sail_off_b"                            ,0,"ship_sail_off_b","bo_ship_sail_off",[]),
("ship_c_sail_off"                            ,0,"ship_c_sail_off","bo_ship_c_sail_off",[]),

("distant_mountain_snow_1",sokf_place_at_origin|sokf_moveable,"distant_mountain_snow_1","0", []),
("distant_mountain_snow_2",sokf_place_at_origin|sokf_moveable,"distant_mountain_snow_2","0", []),

("osgiliath_far_f",0,"osgiliath_far","0", []),   
("hill",0,"hill_steppe","bo_hill", []),
("water_river",0,"TLD_water_plane","0", []),
("water_fall",0,"water_fall","0", []),
("distant_street_a",0,"distant_street_a_new","bo_distant_street_a_new", []),
("distant_street_b",0,"distant_street_b_new","bo_distant_street_b_new", []),
("distant_mountain_a",0,"distant_mountain3","bo_cliff_distant_3", []),
("distant_mountain_b",0,"distant_mountain8","bo_cliff_distant_8", []),
("distant_mountain_c",0,"distant_mountain4","bo_cliff_distant_4", []),
("distant_soldiers_a",0,"distant_soldiers_men_a","0", []),
("distant_orcs_a",0,"distant_soldiers_orcs_a","0", []),
("distant_soldiers_uruks_a",0,"distant_soldiers_uruks_a","0", []),

    ("water_splash_a", 0, "0", "0", [
  (ti_on_init_scene_prop,
    [
    (particle_system_add_new, "psys_water_splash_1"),
    ]),
    ]),
  ("water_splash_b", 0, "0", "0", [
  (ti_on_init_scene_prop,
    [
    (particle_system_add_new, "psys_water_splash_2"),
    ]),
    ]),
  ("water_splash_c", 0, "0", "0", [
  (ti_on_init_scene_prop,
    [
    (particle_system_add_new, "psys_water_splash_3"),
    ]),
    ]),
 
    ("water_fall_2", 0, "0", "0", [
  (ti_on_init_scene_prop,
    [
    (particle_system_add_new, "psys_water_fall_2"),
    #(play_sound,"snd_water_running", 0),
    ]),
    ]),
  
    ("water_foam", 0, "0", "0", [
  (ti_on_init_scene_prop,
    [
    (particle_system_add_new, "psys_water_foam"),
    ]),
    ]),
  
      ("water_run", 0, "0", "0", [
  (ti_on_init_scene_prop,
    [
    (particle_system_add_new, "psys_water_run"),
    ]),
    ]),

#InVain re-used map icons for ambience scenes start
("distant_place_dolamroth",0,"prop_dolamroth","0", []),
("distant_place_edoras",0,"prop_Edoras","0", []),
("distant_place_Helmsdeep",0,"prop_Helms_Deep","0", []),
] + (is_a_wb_sceneprop==1 and [
("distant_place_Morannon",0,"prop_Morannon", "0", [(ti_on_scene_prop_init,[
  (try_begin),(is_currently_night),(eq, "$bright_nights", 1), (set_fog_distance,1200,0x191919),(else_try),(is_currently_night),(set_fog_distance,1000,0x191919),(else_try),(set_fog_distance,1500,0x191919),(set_startup_sun_light, 80, 50, 50),(try_end)])]), 
    ] or [
("distant_place_Morannon",0,"prop_Morannon", "0", [(ti_on_scene_prop_init,[
  (try_begin),(is_currently_night),(set_fog_distance,1000,0x333333),(else_try),(set_fog_distance,1500,0x333333),(try_end)])]),
]) + [

("distant_place_Dolguldur",0,"prop_dolguldur", "0", [(ti_on_scene_prop_init,
            [(try_begin),(is_currently_night),(eq, "$bright_nights", 1), (set_fog_distance,550,0x10593E),
            (else_try),(is_currently_night),(set_fog_distance,450,0x07291D),
       (else_try),                      (set_fog_distance,700,0x77BBB2),
       (try_end),])]),	   
#InVain re-used map icons for ambience scenes end
	
( "honey_pot",0,"honey_pot_new","0",[]),
( "butter_pot",0,"butter_pot_new","0",[]),
( "apple_basket",0,"apple_basket_new","bo_apple_basket",[]),
( "sausages",0,"sausages","0",[]),
( "wine",0,"amphora_slim_new","0",[]),
( "oil",0,"oil_new","0",[]),

( "boat_sail_on",0,"new_boat_sail_on","bo_new_boat_sail_on",[]),
( "boat_sail_off",0,"new_boat_sail_off","bo_new_boat_sail_off",[]),
( "tree_mirkwood_a",0,"tree_mirkwood_a","bo_tree_mallorn_a",[]),
( "tree_mirkwood_b",0,"tree_mirkwood_b","bo_tree_mallorn_b",[]),
( "tree_mirkwood_c",0,"tree_mirkwood_c","bo_tree_mallorn_c",[]),
( "tree_mirkwood_roots_1",0,"tree_mirkwood_roots_1","0",[]),
( "tree_mirkwood_roots_2",0,"tree_mirkwood_roots_2","0",[]),
( "tree_mirkwood_roots_3",0,"tree_mirkwood_roots_3","0",[]),
( "tree_mirkwood_roots_4",0,"tree_mirkwood_roots_4","0",[]),
( "dolmen",0,"dolmen","0",[]),

("orc_gate_destructible",sokf_destructible,"orc_gate_destructible","bo_orc_gate_destructible",   [ 
   (ti_on_scene_prop_init, [
   (store_trigger_param_1, ":gate_no"),
   
    ] + (is_a_wb_sceneprop==1 and [ 
   (prop_instance_get_variation_id_2, ":health", ":gate_no"),
    (try_begin),
        (gt, ":health", 0), #if not assigned, get fallback health from scene prop entry (WB only)
        (val_mul, ":health", 100),
        (scene_prop_set_hit_points, ":gate_no", ":health"),
    (try_end),
    ] or []) + [
    
    (eq, "$gate_aggravator_agent", 1),
    (prop_instance_get_starting_position, pos1, ":gate_no"),
    (position_move_z, pos1, 100,1), #safeguard against aggravators spawning underground
    (set_spawn_position, pos1),
    (spawn_agent,"trp_gate_aggravator"),
    (assign, ":gate_aggravator", reg0),
    (agent_set_speed_limit, ":gate_aggravator", 0),
    (agent_set_team, ":gate_aggravator", 2),
    ] + (is_a_wb_sceneprop==1 and [               # make aggravator a statue (WB Only)
    (agent_set_no_dynamics, ":gate_aggravator",1),
    (agent_set_no_death_knock_down_only, ":gate_aggravator", 1),
    (scene_prop_set_slot, ":gate_no", slot_prop_agent_1, ":gate_aggravator"),
    ] or []) + [
    #(team_give_order, 7, grc_everyone, mordr_stand_ground),
  ]),
   
   (ti_on_scene_prop_destroy, [
    (store_trigger_param_1, ":gate_no"),
    (prop_instance_get_starting_position, pos1, ":gate_no"),
    (particle_system_burst,"psys_game_hoof_dust",pos1,40),
    (particle_system_burst,"psys_dummy_smoke",pos1,30),
    #(particle_system_burst,"psys_pistol_smoke",pos1,200),
    (position_rotate_x, pos1, 85),
    (prop_instance_animate_to_position, ":gate_no", pos1, 400), #animate in 4 second
    (play_sound, "snd_dummy_destroyed"),
    (display_message,"@Gate is breached!"),
    
    ] + (is_a_wb_sceneprop==1 and [        
    (scene_prop_get_slot, ":gate_aggravator", ":gate_no", slot_prop_agent_1),
    (call_script, "script_remove_agent", ":gate_aggravator"), 
    ] or [    
    (assign, ":gate_aggravator_found", 0),
    (try_for_agents, ":agent_no"), #find and remove gate aggravator agent
        (eq, ":gate_aggravator_found", 0),
        (gt, ":agent_no", 0),
        (agent_is_alive, ":agent_no"),  
        (agent_get_troop_id, ":troop_id", ":agent_no"),
        (eq, ":troop_id", "trp_gate_aggravator"),
        (agent_get_position, pos2, ":agent_no"),
        (set_fixed_point_multiplier, 100),
        (get_distance_between_positions, ":distance", pos1, pos2),
        (le, ":distance", 200),
        #(display_message, "@gate_aggravator found"),
        (call_script, "script_remove_agent", ":agent_no"), 
        (assign, ":gate_aggravator_found", 1),
    (try_end),
    ]) + [

    (scene_prop_get_num_instances,":max_barriers","spr_ai_limiter_gate_breached"),  #move away all dependent barriers
    (try_begin),
      (gt, ":max_barriers",0),
      (try_for_range,":count",0,":max_barriers"),
        (scene_prop_get_instance,":barrier_no", "spr_ai_limiter_gate_breached", ":count"),
        (prop_instance_get_starting_position, pos1, ":barrier_no"),
        ] + (is_a_wb_sceneprop==1 and [  #different methods of finding dependent barriers in WB and MB
        (prop_instance_get_variation_id, ":var1", ":barrier_no"),
        (prop_instance_get_variation_id, ":var1_gate", ":gate_no"),
        (eq, ":var1", ":var1_gate"),
        ] or [
        (prop_instance_get_starting_position, pos2, ":gate_no"),
        (set_fixed_point_multiplier, 100),
        (get_distance_between_positions, ":distance", pos1, pos2),
        (le, ":distance", 1000),
        ]) + [
        (position_move_z,pos1,-10000),
        (prop_instance_set_position,":barrier_no",pos1),
      (try_end),
    (try_end),
   ]),
   
   (ti_on_scene_prop_hit,
    [(play_sound, "snd_dummy_hit"),
  (particle_system_burst, "psys_dummy_smoke", pos1, 3),
  (particle_system_burst, "psys_dummy_straw", pos1, 10),
  #(entry_point_get_position,pos1,39),
  #(agent_set_position, "$gate_aggravator_agent", pos1), # place gate aggravator agent to proper position
    ]),
], 2500), 

("rope_bridge",0,"rope_bridge_new","bo_rope_bridge_new", []),
("arena_awning",0,"arena_block_j_awning","bo_arena_block_j_awning", []),

#WB only props below, replaced or hidden in M&B
("tree_shelter",0,"tree_shelter_a","bo_tree_shelter_a", []),
("tree_house",0,"tree_house_a","bo_tree_house_a", []),
("suspension_bridge",0,"suspension_bridge_a","bo_suspension_bridge_a", []),
("arabian_tent_umbar",0,"arabian_tent_umbar","bo_arabian_tent", []),
("arabian_tent_umbar_b",0,"arabian_tent_umbar_b","bo_arabian_tent_b", []),

( "winery_barrel_shelf"                        ,0,"winery_barrel_shelf","bo_winery_barrel_shelf",[]),
( "winery_huge_barrel"                         ,0,"winery_huge_barrel","bo_winery_huge_barrel",[]),
( "winery_middle_barrel"                       ,0,"winery_middle_barrel","bo_winery_middle_barrel",[]),
( "winery_wine_cart_small_loaded"              ,0,"winery_wine_cart_small_loaded","bo_winery_wine_cart_small_loaded",[]),
( "winery_wine_cart_loaded"                    ,0,"winery_wine_cart_loaded","bo_winery_wine_cart_loaded",[]),
( "winery_wine_cart_empty"                     ,0,"winery_wine_cart_empty","bo_winery_wine_cart_empty",[]),
( "winery_wine_cart_small_empty"               ,0,"winery_wine_cart_small_empty","bo_winery_wine_cart_small_empty",[]),
( "smithy_grindstone_wheel"                    ,0,"smithy_grindstone_wheel","bo_smithy_grindstone_wheel",[]),
( "smithy_forge_bellows"                       ,0,"smithy_forge_bellows","bo_smithy_forge_bellows",[]),
( "smithy_forge"                               ,0,"smithy_forge","bo_smithy_forge",[]),
( "smithy_anvil"                               ,0,"smithy_anvil","0",[]),
( "tannery_hide_a"                             ,0,"tannery_hide_a","bo_tannery_hide_a",[]),
( "tannery_hide_b"                             ,0,"tannery_hide_b","bo_tannery_hide_b",[]),
#WB only props end

	( "woodplanks_exima"                           ,0,"exima_woodplanks","bo_exima_woodplanks",[]),
	( "khazad_dwarf_erebor_lake_boat"              ,0,"khazad_dwarf_erebor_lake_boat","bo_khazad_dwarf_erebor_lake_boat",[]),
	( "khazad_dwarf_forge_stand_tools"             ,0,"khazad_dwarf_forge_stand_tools","0",[]),
	( "khazad_dwarf_forge_anvil"                   ,0,"khazad_dwarf_forge_anvil","0",[]),
	( "khazad_dwarf_forge_forging_barrel"          ,0,"khazad_dwarf_forge_forging_barrel","bo_khazad_dwarf_forge_forging_barrel",[]),
	( "khazad_dwarf_forge_tools_1"                 ,0,"khazad_dwarf_forge_tools_1","0",[]),
	( "khazad_dwarf_forge_tools_2"                 ,0,"khazad_dwarf_forge_tools_2","0",[]),
	( "khazad_dwarf_forge_tools_3"                 ,0,"khazad_dwarf_forge_tools_3","0",[]),
	( "khazad_dwarf_forge_tools_4"                 ,0,"khazad_dwarf_forge_tools_4","0",[]),
	( "khazad_dwarf_forge_tools_5"                 ,0,"khazad_dwarf_forge_tools_5","0",[]),
	( "khazad_dwarf_forge_tools_6"                 ,0,"khazad_dwarf_forge_tools_6","0",[]),
	( "khazad_dwarf_forge_tools_7"                 ,0,"khazad_dwarf_forge_tools_7","0",[]),
	( "khazad_dwarf_tobacco_pipe"                  ,0,"khazad_dwarf_tobacco_pipe","0",[]),
	( "khazad_dwarf_tobacco_pouch"                 ,0,"khazad_dwarf_tobacco_pouch","0",[]),
	( "khazad_dwarf_flask"                         ,0,"khazad_dwarf_flask","0",[]),
	( "khazad_dwarf_cram"                          ,0,"khazad_dwarf_cram","0",[]),
	( "khazad_dwarf_animals_skins_boar"            ,0,"khazad_dwarf_animals_skins_boar","0",[]),
	( "khazad_dwarf_animals_skins_wolf"            ,0,"khazad_dwarf_animals_skins_wolf","0",[]),
	( "khazad_dwarf_animals_skins_fox"             ,0,"khazad_dwarf_animals_skins_fox","0",[]),
	( "khazad_dwarf_table_1"                       ,0,"khazad_dwarf_table_1","bo_khazad_dwarf_table_1",[]),
	( "khazad_dwarf_tree_1"                        ,0,"khazad_dwarf_tree_1","0",[]),
	( "khazad_dwarf_bench_1"                       ,0,"khazad_dwarf_bench_1","bo_khazad_dwarf_bench_1",[]),
	( "khazad_orcish_temporary_camp_spit_2"        ,0,"khazad_orcish_temporary_camp_spit_2","0",[]),
	( "khazad_orcish_temporary_camp_bonfire_2"     ,0,"khazad_orcish_temporary_camp_bonfire_2","0",[]),
	( "khazad_orcish_temporary_camp_burduk_1"      ,0,"khazad_orcish_temporary_camp_burduk_1","0",[]),
	( "khazad_dwarf_tower"     					   ,0,"khazad_dwarf_tower","bo_khazad_dwarf_tower",[]),
	( "khazad_dwarf_mech"     					   ,0,"khazad_dwarf_mech_1","bo_khazad_dwarf_mech_1",[]),



("troop_civilian",sokf_invisible,"arrow_helper_blue","0", [(ti_on_init_scene_prop,[												 
    (store_trigger_param_1, ":instance_no"),
    (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
	(store_random_in_range, ":civilian_slot", 0, 5),
    (val_add, ":civilian_slot", slot_center_walker_0_troop),
    (party_get_slot, ":troop", "$current_town", ":civilian_slot"),					 

    (spawn_agent, ":troop"),(agent_set_team, reg0, 0),
  ] + (is_a_wb_sceneprop==1 and [     
    #randomize animation
    (assign, ":animation", "anim_stand"),
    (store_random_in_range, ":rnd", 0, 5),
    (try_begin),
        (eq, ":rnd", 0),
        (assign, ":animation", "anim_stand_cutscene"),
     (else_try),
        (eq, ":rnd", 1),
        (assign, ":animation", "anim_stand"),
        #(assign, ":animation", anim_stand_shopkeeper), #not implemented yet
     (else_try),
        (eq, ":rnd", 2),
        (assign, ":animation", "anim_stand_man"),
     (else_try),
        (eq, ":rnd", 3),
        (assign, ":animation", "anim_stand_townguard"),
     (else_try),
        (eq, ":rnd", 4),
        (assign, ":animation", "anim_stand_lord"),
    (try_end),
    (agent_set_stand_animation, reg0, ":animation"),
    
    (store_random_in_range, reg6, 0, 100),(agent_set_animation_progress, reg0, reg6),
        
    #remove weapons and helms    
        (try_for_range, ":weapon_slot", 0, 4), 
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),
        (try_begin),
            (agent_get_item_slot, ":helm", reg0, ek_head),
            (gt, ":helm", 1),
            (neg|item_has_property, ":helm", itp_civilian),
            (agent_unequip_item, reg0, ":helm", ek_head),
        (try_end),
    ] or []) + [
  ])]),
	
("troop_civ_sitting_ground",sokf_invisible,"sitting","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),
    (set_fixed_point_multiplier, 100),
    (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
	(store_random_in_range, ":civilian_slot", 0, 5),
    (val_add, ":civilian_slot", slot_center_walker_0_troop),
    (party_get_slot, ":troop", "$current_town", ":civilian_slot"),
    
    (spawn_agent, ":troop"),(agent_set_team, reg0, 0),(agent_set_stand_animation, reg0, "anim_sit_on_ground"),
    
        #remove weapons and helms
  ] + (is_a_wb_sceneprop==1 and [ 
        (try_for_range, ":weapon_slot", 0, 4), 
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),
        (try_begin),
            (agent_get_item_slot, ":helm", reg0, ek_head),
            (gt, ":helm", 1),
            (neg|item_has_property, ":helm", itp_civilian),
            (agent_unequip_item, reg0, ":helm", ek_head),
        (try_end),
        
        #for better clip control
        (agent_set_no_dynamics, reg0, 1),
        (agent_ai_set_interact_with_player, reg0, 0),
        (troop_get_type, ":race", ":troop"),
        (try_begin), 
            (eq, ":race", tf_orc),
            (position_move_z, pos1, 15),
        (else_try),
            (eq, ":race", tf_dwarf),
            (position_move_z, pos1, 40),
        (try_end),
        (agent_set_position, reg0, pos1),
    ] or []) + [  
    ])]),
	
("troop_civ_sitting_chair",sokf_invisible,"sit","bo_sitting", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),
    (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),

	(store_random_in_range, ":civilian_slot", 0, 5),
    (val_add, ":civilian_slot", slot_center_walker_0_troop),
    (party_get_slot, ":troop", "$current_town", ":civilian_slot"),
    (spawn_agent, ":troop"),(agent_set_team, reg0, 0),(agent_set_stand_animation, reg0, "anim_sit_on_throne"),
    
        #remove weapons and helms
  ] + (is_a_wb_sceneprop==1 and [     
    (agent_set_no_dynamics, reg0, 1),
    (agent_ai_set_interact_with_player, reg0, 0),        
        (try_for_range, ":weapon_slot", 0, 3), 
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),
        (try_begin),
            (agent_get_item_slot, ":helm", reg0, ek_head),
            (gt, ":helm", 1),
            (neg|item_has_property, ":helm", itp_civilian),
            (agent_unequip_item, reg0, ":helm", ek_head),
        (try_end),
        
        #for better clip control
        (troop_get_type, ":race", ":troop"),
        (try_begin), 
            (eq, ":race", tf_orc),
            (position_move_z, pos1, 15),
        (else_try),
            (eq, ":race", tf_dwarf),
            (position_move_z, pos1, 40),
        (try_end),
        (agent_set_position, reg0, pos1),        
    ] or []) + [  
    ])]),
	
("water_fall_big", 0, "0", "0", [
	(ti_on_init_scene_prop,
		[
		(particle_system_add_new, "psys_water_fall"),
		#(play_sound,"snd_waterfall", 0),
		(set_position_delta, 0, 120, -100),
		(particle_system_add_new, "psys_water_fall_3"),
		]),
    ]),

("umbar_smallboatoar_new",0,"umbar_prop_smallboatoar_new","0", []), #corrected position and rotation, easier to use in editor. Kept the old one for scene compatibility.

("morgul_tower_7",0,"morgul_gondor_tower_7_evil","bo_gondor_tower_7", []),
("morgul_wall",0,"morgul_mt_wall_evil","bo_morgul_mt_wall_evil", []),
("morgul_gate_tower",0,"morgul_mt_gate_tower_evil","bo_mt_tower", []),
("morgul_gate_house",0,"morgul_mt_gate_house_evil","bo_morgul_mt_gate_house_evil", [
     (ti_on_scene_prop_init,[ (set_fixed_point_multiplier, 100), 
         (try_begin),(is_currently_night),(eq, "$bright_nights", 1), (set_fog_distance,450,0x07291D),
         (else_try),(is_currently_night),(set_fog_distance,450,0x07291D), 
         ] + (is_a_wb_sceneprop==1 and [ (set_startup_ambient_light, 25, 30, 25),(set_startup_sun_light, 5, 5, 5),(set_startup_ground_ambient_light, 12, 18, 12), ] or []) + [ 
         (else_try),(set_fog_distance,700,0x10261E),         
         ] + (is_a_wb_sceneprop==1 and [ (set_startup_ambient_light, 40, 40, 40),(set_startup_sun_light, 10, 10, 10),(set_startup_ground_ambient_light, 12, 18, 12), ] or []) + [ 
         (try_end),
     ])]),
("morgul__gate",0,"morgul_gate","bo_morgul_gate", []),
("morgul_short_tower",0,"morgul_short_tower","bo_morgul_short_tower", []),	
("morgul_tower_b_vp_E",0,"morgul_tower_b_color","0", []),
("morgul_stone_minaret_a",0,"morgul_stone_minaret_a","bo_stone_minaret_a", []),

( "mordor_cliff_distant_3",0,"mordor_cliff_distant_3","bo_mordor_cliff_distant_3",[]),
( "mordor_cliff_distant_1",0,"mordor_cliff_distant_1","bo_mordor_cliff_distant_1",[]),
( "mordor_cliff_distant_6",0,"mordor_cliff_distant_6","bo_mordor_cliff_distant_6",[]),
( "mordor_cliff_distant_7",0,"mordor_cliff_distant_7","bo_mordor_cliff_distant_7",[]),
( "mordor_cliff_distant_8",0,"mordor_cliff_distant_8","bo_mordor_cliff_distant_8",[]),

( "beorn_hall",0,"beorn_hall","bo_beorn_hall",[]),
( "beorn_side_house",0,"beorn_side_house","bo_house6",[]),

("riven_wall",0,"riven_wall","bo_riven_wall", []),
("riven_tower",0,"riven_tower","bo_rohan_tower2"    , []),
("riven_bridge_modular_a",0,"riven_bridge_modular_a","bo_bridge_modular_a", []),
("isen_pillar_adorno",0,"isen_pillar_adorno","bo_isen_pillar_adorno", []),

("khazad_dwarf_cup_1",0,"khazad_dwarf_cup_1","0",[]),
("khazad_dwarf_ale_keg_1",0,"khazad_dwarf_ale_keg_1","0",[]),
("khazad_dwarf_ale_pint_1",0,"khazad_dwarf_ale_pint_1","0",[]),
("khazad_dwarf_ale_pint_2",0,"khazad_dwarf_ale_pint_2","0",[]),

( "CWE_kitchen_herbs_a",0,"CWE_kitchen_herbs_a","0",[]),
( "CWE_kitchen_herbs_b",0,"CWE_kitchen_herbs_b","0",[]),
( "CWE_kitchen_herbs_c",0,"CWE_kitchen_herbs_c","0",[]),
( "CWE_kitchen_herbs_d",0,"CWE_kitchen_herbs_d","0",[]),
( "CWE_refined_pitcher_a",0,"CWE_refined_pitcher_a","0",[]),
( "CWE_refined_pitcher_b",0,"CWE_refined_pitcher_b","0",[]),
( "CWE_refined_pitcher_c",0,"CWE_refined_pitcher_c","0",[]),
( "CWE_refined_pitcher_d",0,"CWE_refined_pitcher_d","0",[]),
( "CWE_refined_pitcher_e",0,"CWE_refined_pitcher_e","0",[]),
( "CWE_refined_pitcher_f",0,"CWE_refined_pitcher_f","0",[]),
( "CWE_exquisite_dish_a",0,"CWE_exquisite_dish_a","0",[]),
( "CWE_exquisite_dish_b",0,"CWE_exquisite_dish_b","0",[]),
( "CWE_exquisite_dish_c",0,"CWE_exquisite_dish_c","0",[]),
( "CWE_exquisite_dish_d",0,"CWE_exquisite_dish_d","0",[]),
( "CWE_exquisite_dish_e",0,"CWE_exquisite_dish_e","0",[]),
( "CWE_exquisite_cup_a",0,"CWE_exquisite_cup_a","0",[]),
( "CWE_exquisite_cup_b",0,"CWE_exquisite_cup_b","0",[]),
( "CWE_elegant_lamp_a",0,"CWE_elegant_lamp_a","bo_CWE_elegant_lamp_a_col",[]),
( "CWE_elegant_lamp_b",0,"CWE_elegant_lamp_b","bo_CWE_elegant_lamp_b_col",[]),
( "CWE_elegant_lamp_c",0,"CWE_elegant_lamp_c","0",[]),
( "CWE_elegant_lamp_d",0,"CWE_elegant_lamp_d","0",[]),
( "CWE_svet_tower_a",0,"CWE_svet_tower_a","bo_CWE_svet_tower_a_col",[]),
( "CWE_svet_tower_b",0,"CWE_svet_tower_b","bo_CWE_svet_tower_b_col",[]),

( "Gutek_straw_a"                              ,0,"Gutek_straw_a","0",[]),
( "Gutek_straw_b"                              ,0,"Gutek_straw_b","0",[]),
( "Gutek_straw_c"                              ,0,"Gutek_straw_c","0",[]),
( "Gutek_cart"                                 ,0,"Gutek_cart","bo_cart_new",[]),
( "Gutek_awning_d"                             ,0,"Gutek_awning_d","bo_awning_d",[]),
( "Gutek_stand_cloth"                          ,0,"Gutek_stand_cloth","bo_stand_cloth",[]),
( "Gutek_stand_thatched"                       ,0,"Gutek_stand_thatched","bo_stand_thatched",[]),

( "durins_stone"           			            ,0,"durins_stone","bo_durins_stone",[]),

( "gon_stone_house_a",0,"gondor_stone_house_a","bo_gondor_stone_house_a",[]),
( "gon_stone_house_b",0,"gondor_stone_house_b","bo_gondor_stone_house_b",[]),
( "gon_stone_house_c",0,"gondor_stone_house_c","bo_gondor_stone_house_c",[]),
( "gon_stone_house_d",0,"gondor_stone_house_d","bo_gondor_stone_house_d",[]),
( "gon_stone_house_e",0,"gondor_stone_house_e","bo_gondor_stone_house_e",[]),
( "gon_stone_house_f",0,"gondor_stone_house_f_new","bo_gondor_stone_house_f",[]),
( "gon_stone_house_g",0,"gondor_stone_house_g","bo_gondor_stone_house_g",[]),
( "gon_stone_house_h",0,"gondor_stone_house_h","bo_gondor_stone_house_h",[]),
( "gon_stone_house_i",0,"gondor_stone_house_i","bo_gondor_stone_house_i",[]),
( "gon_stone_house_j",0,"gondor_stone_house_j","bo_gondor_stone_house_j",[]),
( "gon_stone_house_k",0,"gondor_stone_house_k","bo_gondor_stone_house_k",[]),
( "gon_stone_house_l",0,"gondor_stone_house_l","bo_gondor_stone_house_l",[]),
( "gon_stone_house_m",0,"gondor_stone_house_m","bo_gondor_stone_house_m",[]),
( "gon_stone_house_n",0,"gondor_stone_house_n","bo_gondor_stone_house_n",[]),
( "gon_stone_house_o",0,"gondor_stone_house_o","bo_gondor_stone_house_o",[]),
( "gon_stone_keep",0,"gondor_stone_keep","bo_gondor_stone_keep",[]),
( "gon_stone_passage_house_a",0,"gondor_stone_passage_house_a","bo_gondor_stone_passage_house_a",[]),
( "gon_stone_house_p_cwe"    ,0,"CWE_house_a","bo_CWE_house_a",[]),
( "gon_stone_house_q_cwe"     ,0,"damask_arabian_house_extension_a","bo_damask_arabian_house_extension_a",[]),
( "gon_stone_house_r_cwe"     ,0,"damask_arabian_house_extension_b","bo_damask_arabian_house_extension_b",[]),
( "gon_stone_house_block_a_cwe"     ,0,"damask_house_block_a","bo_damask_house_block_a",[]),
( "gon_stone_house_block_c_cwe"     ,0,"damask_house_block_c","bo_damask_house_block_c",[]),
( "gon_stone_house_block_b_cwe"     ,0,"damask_house_block_b","bo_damask_house_block_b",[]),
( "gon_stone_passage_house_b_cwe" ,0,"damask_passage_house_b","bo_damask_passage_house_b",[]),
( "gon_stone_bridge",0,"gondor_stone_bridge","bo_gondor_stone_bridge", []),

("gon_fake_house_stone_a",0,"MT_stone_fake_house_far_a","bo_fake_house_far", []),
("gon_fake_house_stone_b",0,"MT_stone_fake_house_far_b","bo_fake_house_far", []),
("gon_fake_house_stone_c",0,"MT_stone_fake_house_far_c","bo_fake_house_far", []),
("gon_fake_house_stone_d",0,"MT_stone_fake_house_far_d","bo_fake_house_far", []),
("gon_fake_house_stone_e",0,"MT_stone_fake_house_far_e","bo_fake_house_far", []),
("gon_fake_house_stone_f",0,"MT_stone_fake_house_far_f","bo_fake_house_far", []),

( "khazad_dwarf_wall_decor_1",0,"khazad_dwarf_wall_decor_1","bo_khazad_dwarf_wall_decor_1",[]),
( "khazad_dwarf_wall_decor_2",0,"khazad_dwarf_wall_decor_2","bo_khazad_dwarf_wall_decor_2",[]),
( "khazad_dwarf_bench_2",0,"khazad_dwarf_bench_2","bo_khazad_dwarf_bench_2",[]),

("blood_decal_1",0,"prop_mesh_blood_1","0",[]),
("blood_decal_2",0,"prop_mesh_blood_2","0",[]),
("blood_decal_3",0,"prop_mesh_blood_3","0",[]),
("chain_hanging_5m",0,"chain_hanging_5m","0",[]),
("chain_hanging_10m",0,"chain_hanging_10m","0",[]),
("isen_sarustaff",0,"sarustaff","0",[]),
("isen_pillar_marble_adorno",0,"isen_pillar_marble_adorno","bo_isen_pillar_adorno", []),
("isen_pillar_iron_adorno",0,"isen_pillar_iron_adorno","bo_isen_pillar_adorno", []),
("isen_pillar_bronze_adorno",0,"isen_pillar_bronze_adorno","bo_isen_pillar_adorno", []),
("isen_pillar_steel_adorno",0,"isen_pillar_steel_adorno","bo_isen_pillar_adorno", []),

("umbar_corsair_ship",0,"corsair_ship","bo_corsair", []),

#Adorno's wood props OSP (renamed for easier findability)
( "fence_barrier_small_ado"                     ,0,"ado_wood_arena_barrier","bo_ado_wood_arena_barrier",[]),
( "arena_full_ado"                   		 ,0,"ado_wood_arena_training","bo_ado_wood_arena_training",[]),
( "bench_fine_ado"                        ,0,"ado_wood_bench_fine","0",[]),
( "bench_plain_ado"                       ,0,"ado_wood_bench_plain","0",[]),
( "bench_stone_roman_ado"                      ,0,"ado_stone_bench_roman","0",[]),
( "bridge_long_ado"                       ,0,"ado_wood_bridge_long","bo_ado_wood_bridge_long",[]),
( "bridge_long_ramp_ado"                  ,0,"ado_wood_bridge_long_ramp","bo_ado_wood_bridge_long_ramp",[]),
( "bridge_tall_ado"                       ,0,"ado_wood_bridge_tall","bo_ado_wood_bridge_tall",[]),
( "village_cabin_ado"                         ,0,"ado_wood_cabin_log","bo_ado_wood_cabin_log",[]),
( "cart_ado"                              ,0,"ado_wood_cart","bo_ado_wood_cart",[]),
( "cart_ado_2"                            ,0,"ado_wood_cart_2","bo_ado_wood_cart_2",[]),
( "cart_ado_2_broken"                     ,0,"ado_wood_cart_2_broken","bo_ado_wood_cart_2_broken",[]),
( "cart_ado_3"                            ,0,"ado_wood_cart_3","bo_ado_wood_cart_3",[]),
( "cart_ado_wheel"                        ,0,"ado_wood_cart_wheel","bo_ado_wood_cart_wheel",[]),
( "chair_ado_1"                            ,0,"ado_wood_chair1","0",[]),
( "chair_ado_2"                            ,0,"ado_wood_chair2","0",[]),
( "chair_ado_fine"                        ,0,"ado_wood_chair_fine","0",[]),
( "cradle_ado"                            ,0,"ado_wood_cradle","bo_ado_wood_cradle",[]),
( "crate_1_ado"                           ,0,"ado_wood_crate_1","bo_ado_wood_crate_1",[]),
( "crate_2_ado"                           ,0,"ado_wood_crate_2","bo_ado_wood_crate_2",[]),
( "crate_broken_ado"                      ,0,"ado_wood_crate_broken","bo_ado_wood_crate_broken",[]),
( "crate_closed_ado"                      ,0,"ado_wood_crate_closed","bo_ado_wood_crate_closed",[]),
( "crate_lid_ado"                         ,0,"ado_wood_crate_lid","bo_ado_wood_crate_lid",[]),
( "crate_tall_ado"                        ,0,"ado_wood_crate_tall","bo_ado_wood_crate_tall",[]),
( "table_ado"                              ,0,"ado_wood_desk","bo_ado_wood_desk",[]),
( "table_tall_ado"                         ,0,"ado_wood_desk_tall","bo_ado_wood_desk_tall",[]),
( "fence_short_ado"                       ,0,"ado_wood_fence_short","bo_ado_wood_fence_short",[]),
( "fence_long_ado"                        ,0,"ado_wood_fence_long","bo_ado_wood_fence_long",[]),
( "gate_ado_left"                         ,0,"ado_wood_gate_left","bo_ado_wood_gate_left",[]),
( "gate_ado_right"                        ,0,"ado_wood_gate_right","bo_ado_wood_gate_right",[]),
( "gate_ado_lock"                         ,0,"ado_wood_gate_lock","bo_ado_wood_gate_lock",[]),
( "gate_ado_locked"                      ,0,"ado_wood_gates_locked","bo_ado_wood_gates_locked",[]),
( "village_wood_house_ado"                             ,0,"ado_wood_house","bo_ado_wood_house",[]),
( "village_wood_house_planks_ado"                      ,0,"ado_wood_house_planks","bo_ado_wood_house_planks",[]),
( "village_wood_house_small_ado"                       ,0,"ado_wood_house_small","bo_ado_wood_house_small",[]),
( "village_wood_house_small_v2_ado"                    ,0,"ado_wood_house_small_v2","bo_ado_wood_house_small_v2",[]),
( "village_wood_house_small_shingles_ado"              ,0,"ado_wood_house_small_shingles","bo_ado_wood_house_small_shingles",[]),
( "village_wood_barn_ado"                              ,0,"ado_wood_barn","bo_ado_wood_barn",[]),
( "village_wood_dovecote_ado"                     ,0,"ado_wood_dovecote_tall","bo_ado_wood_dovecote_tall",[]),
( "torture_tool_judas_cradle_ado"                      ,0,"ado_wood_judas_cradle","bo_ado_wood_judas_cradle",[]),
( "torture_tool_pillory_ado"                           ,0,"ado_wood_pillory","bo_ado_wood_pillory",[]),
( "toture_tool_spanish_donkey_ado"                    ,0,"ado_wood_spanish_donkey","bo_ado_wood_spanish_donkey",[]),
( "ladder_simple_ado"                     ,0,"ado_wood_ladder_simple","bo_ado_wood_ladder_simple",[]),
( "ladder_simple_broken_ado"              ,0,"ado_wood_ladder_simple_broken","bo_ado_wood_ladder_simple_broken",[]),
#( "ado_wood_log_1"                             ,0,"ado_wood_log_1","bo_ado_wood_log_1",[]),
#( "ado_wood_log_2"                             ,0,"ado_wood_log_2","bo_ado_wood_log_2",[]),
#( "ado_wood_log_3"                             ,0,"ado_wood_log_3","bo_ado_wood_log_3",[]),
#( "ado_wood_log_4"                             ,0,"ado_wood_log_4","bo_ado_wood_log_4",[]),
( "wood_heap_ado"                         ,0,"ado_wood_logs_pile","bo_ado_wood_logs_pile",[]),
( "wood_heap_ado_2"                       ,0,"ado_wood_logs_pile_2","bo_ado_wood_logs_pile_2",[]),
( "palisade_long_ado"                     ,0,"ado_wood_palisade_long","bo_ado_wood_palisade_long",[]),
( "palisade_long_decay_ado"               ,0,"ado_wood_palisade_long_decay","bo_ado_wood_palisade_long_decay",[]),
( "palisade_long_destroyed_ado"           ,0,"ado_wood_palisade_long_destroyed","bo_ado_wood_palisade_long_destroyed",[]),
( "palisade_plain_ado"                    ,0,"ado_wood_palisade_plain","bo_ado_wood_palisade_plain",[]),
( "palisade_short_ado"                    ,0,"ado_wood_palisade_short","bo_ado_wood_palisade_short",[]),
( "palisade_stake_ado"                    ,0,"ado_wood_palisade_stake","bo_ado_wood_palisade_stake",[]),
( "palisade_stake_broken_ado"             ,0,"ado_wood_palisade_stake_broken","bo_ado_wood_palisade_stake_broken",[]),
( "wood_pile_ado"                              ,0,"ado_wood_pile","bo_ado_wood_pile",[]),

( "village_wood_stable_ado"                            ,0,"ado_wood_stable","bo_ado_wood_stable",[]),
( "village_wood_stable_simple_ado"                     ,0,"ado_wood_stable_simple","bo_ado_wood_stable_simple",[]),
( "village_wood_stockade_bend_ado"                  ,0,"ado_wood_stockade_bending","bo_ado_wood_stockade_bending",[]),
( "village_wood_stockade_long_ado"                     ,0,"ado_wood_stockade_long","bo_ado_wood_stockade_long",[]),
( "village_wood_stockade_long_broken_ado"              ,0,"ado_wood_stockade_long_broken","bo_ado_wood_stockade_long_broken",[]),
( "village_wood_stockade_short_ado"                    ,0,"ado_wood_stockade_short","bo_ado_wood_stockade_short",[]),
( "village_wood_stockade_plank_ado"                    ,0,"ado_wood_stockade_plank","bo_ado_wood_stockade_plank",[]),
( "village_wood_stockade_plank_broken_ado"             ,0,"ado_wood_stockade_plank_broken","bo_ado_wood_stockade_plank_broken",[]),
( "chair_stool_ado"                             ,0,"ado_wood_stool","0",[]),
( "table_plain_ado"                       ,0,"ado_wood_table_plain","bo_ado_wood_table_plain",[]),
( "table_round_ado"                       ,0,"ado_wood_table_round","bo_ado_wood_table_round",[]),
( "table_round_ado_2"                     ,0,"ado_wood_table_round_2","bo_ado_wood_table_round_2",[]),
( "table_round_ado_small"                 ,0,"ado_wood_table_round_small","bo_ado_wood_table_round_small",[]),
( "tourney_arch_ado"                      ,0,"ado_wood_tourney_arch","bo_ado_wood_tourney_arch",[]),
( "tourney_arch_ado_painted"              ,0,"ado_wood_tourney_arch_painted","bo_ado_wood_tourney_arch_painted",[]),
( "tourney_arch_ado_painted_dark"         ,0,"ado_wood_tourney_arch_painted_dark","bo_ado_wood_tourney_arch_painted_dark",[]),
( "tourney_barrier_ado"                   ,0,"ado_wood_tourney_barrier","bo_ado_wood_tourney_barrier",[]),
( "tourney_barrier_ado_painted"           ,0,"ado_wood_tourney_barrier_painted","bo_ado_wood_tourney_barrier_painted",[]),
( "tourney_barrier_ado_painted_dark"      ,0,"ado_wood_tourney_barrier_painted_dark","bo_ado_wood_tourney_barrier_painted_dark",[]),
( "tourney_barrier_ado_post"              ,0,"ado_wood_tourney_barrier_post","bo_ado_wood_tourney_barrier_post",[]),
( "tourney_barrier_ado_short"             ,0,"ado_wood_tourney_barrier_short","bo_ado_wood_tourney_barrier_short",[]),
( "tourney_barrier_ado_short_painted"     ,0,"ado_wood_tourney_barrier_short_painted","bo_ado_wood_tourney_barrier_short_painted",[]),
( "tourney_barrier_ado_short_painted_dark",0,"ado_wood_tourney_barrier_short_painted_dark","bo_ado_wood_tourney_barrier_short_painted_dark",[]),
( "fence_simple_ado"                     ,0,"ado_wood_tourney_fence","bo_ado_wood_tourney_fence",[]),
( "fence_simple_ado_post"                ,0,"ado_wood_tourney_fence_post","bo_ado_wood_tourney_fence_post",[]),
( "fence_simple_ado_short"               ,0,"ado_wood_tourney_fence_short","bo_ado_wood_tourney_fence_short",[]),
( "tourney_podium_ado"                    ,0,"ado_wood_tourney_podium","bo_ado_wood_tourney_podium",[]),
( "tourney_podium_ado_painted"            ,0,"ado_wood_tourney_podium_painted","bo_ado_wood_tourney_podium_painted",[]),
( "tourney_podium_ado_painted_dark"       ,0,"ado_wood_tourney_podium_painted_dark","bo_ado_wood_tourney_podium_painted_dark",[]),
( "tourney_post_ado"                      ,0,"ado_wood_tourney_post","bo_ado_wood_tourney_post",[]),
( "tourney_scaffold_ado_short"            ,0,"ado_wood_tourney_scaffold_short","bo_ado_wood_tourney_scaffold_short",[]),
( "tourney_scaffold_ado_tall"             ,0,"ado_wood_tourney_scaffold_tall","bo_ado_wood_tourney_scaffold_tall",[]),
( "tourney_scaffold_ado_tall_painted"     ,0,"ado_wood_tourney_scaffold_tall_painted","bo_ado_wood_tourney_scaffold_tall_painted",[]),
( "tourney_scaffold_ado_tall_painted_dark",0,"ado_wood_tourney_scaffold_tall_painted_dark","bo_ado_wood_tourney_scaffold_tall_painted_dark",[]),
( "wood_wall_tower_lookout_ado"             ,0,"ado_wood_tower_lookout_defence","bo_ado_wood_tower_lookout_defence",[]),
( "wood_wall_section_ado"                      ,0,"ado_wood_wall_section","bo_ado_wood_wall_section",[]),
( "wood_wall_section_ado_2"                    ,0,"ado_wood_wall_section_2","bo_ado_wood_wall_section_2",[]),
( "wood_wall_section_ado_destroyed"            ,0,"ado_wood_wall_section_destroyed","bo_ado_wood_wall_section_destroyed",[]),
( "wood_wall_section_ado_bending"              ,0,"ado_wood_wall_section_bending","bo_ado_wood_wall_section_bending",[]),
( "wood_wall_section_ado_corner"               ,0,"ado_wood_wall_section_corner","bo_ado_wood_wall_section_corner",[]),
( "wood_wall_section_ado_short"                ,0,"ado_wood_wall_section_short","bo_ado_wood_wall_section_short",[]),
( "wood_wall_tower_ado"                        ,0,"ado_wood_wall_tower","bo_ado_wood_wall_tower",[]),
( "wood_wall_gatehouse_ado"                         ,0,"ado_wood_gatehouse","bo_ado_wood_gatehouse",[]),
( "wood_wall_gatehouse_ado_large"                   ,0,"ado_wood_gatehouse_large","bo_ado_wood_gatehouse_large",[]),
( "wood_wall_gatehouse_ado_twins"                   ,0,"ado_wood_gatehouse_twins","bo_ado_wood_gatehouse_twins",[]),
( "wood_wall_stairs_ado"                            ,0,"ado_wood_stairs","bo_ado_wood_stairs",[]),
( "wood_wall_stairs_long_ado"                       ,0,"ado_wood_stairs_long","bo_ado_wood_stairs_long",[]),
( "wood_wall_stairs_short_ado"                      ,0,"ado_wood_stairs_short","bo_ado_wood_stairs_short",[]),
( "wood_wall_platform_ado"                          ,0,"ado_wood_platform","bo_ado_wood_platform",[]),
( "wood_wall_platform_raised_ado"                   ,0,"ado_wood_platform_raised","bo_ado_wood_platform_raised",[]),
( "village_well_stone_ado"                ,0,"ado_wood_well_stone_village","bo_ado_wood_well_stone_village",[]),
( "village_well_wood_ado"                      ,0,"ado_wood_well_village","bo_ado_wood_well_village",[]),
( "wheelbarrow_ado"                       ,0,"ado_wood_wheelbarrow","bo_ado_wood_wheelbarrow",[]),
( "windmill_post_ado"                     ,0,"ado_wood_windmill_post","bo_ado_wood_windmill_post",[]),
( "windmill_post_ado_full_sail"           ,0,"ado_wood_windmill_post_full_sail","bo_ado_wood_windmill_post_full_sail",[]),
( "windmill_post_ado_full_sail_red"       ,0,"ado_wood_windmill_post_full_sail_red","bo_ado_wood_windmill_post_full_sail_red",[]),
( "windmill_post_ado_sails_off"           ,0,"ado_wood_windmill_post_sails_off","bo_ado_wood_windmill_post_sails_off",[]),

("Dale_Bell_Tower_wood",0,"Dale_church_tower_wood","bo_Dale_church_tower_a", []),
("Dale_Bell",0,"Dale_bell","0", []),

( "village_wall"                               ,0,"village_wall","bo_village_wall",[]), #some more native WB props (replace in MB)
( "well_shaft"                                 ,0,"well_shaft_new","bo_well_shaft",[]),
( "small_wall_f"                               ,0,"small_wall_f_new","bo_small_wall_f",[]),
( "small_wall_f2"                              ,0,"small_wall_f2_new","bo_small_wall_f2",[]),
( "gon_small_wall_a_1"                           ,0,"arabian_wall_a_gon","bo_arabian_wall_a",[]),
( "stairs_a"                                   ,0,"stairs_a_new","bo_stairs_a",[]),


("animal_goat",sokf_invisible,"bry_goat","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),

    ] + (is_a_wb_sceneprop==1 and [ 
	(store_random_in_range, ":animal_var", 0, imod_cracked+1),														 
	(spawn_horse,"itm_animal_small", ":animal_var"),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, 0), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, "anim_wolf_snap"), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, snd_goat), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, snd_goat), #sound 2
    (agent_set_slot, reg0, slot_agent_mount_dead, 10), #chance to move per second, minimum 5%
    ] or []) + [          
    ])]),

("animal_cow",sokf_invisible,"bry_cow_a","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),

    ] + (is_a_wb_sceneprop==1 and [ 
	(store_random_in_range, ":animal_var", imod_cracked, imod_bent+1),														 
	(spawn_horse,"itm_animal_big", ":animal_var"),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, 0), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, 0), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, 0), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, snd_cow_moo), #sound 2
    ] or []) + [          
    ])]),

("animal_cow_b",sokf_invisible,"CWE_cow_mod_a","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),

    ] + (is_a_wb_sceneprop==1 and [ 													 
	(spawn_horse,"itm_animal_big", imod_chipped),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, 0), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, 0), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, 0), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, snd_cow_moo), #sound 2
    ] or []) + [          
    ])]),  

("animal_donkey",sokf_invisible,"bry_wild_donkey","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),

    ] + (is_a_wb_sceneprop==1 and [ 													 
	(spawn_horse,"itm_animal_big", imod_rotten),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, 0), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, 0), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, snd_horse_breath), #sound 1 
    (agent_set_slot, reg0, slot_agent_mount_side, snd_donkey), #sound 2
    ] or []) + [          
    ])]),
    
("animal_aurochs",sokf_invisible,"spak_yak1","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),

    ] + (is_a_wb_sceneprop==1 and [ 
	(store_random_in_range, ":animal_var", 1, 4),														 
    (try_begin),
        (eq, ":animal_var",1),
        (spawn_horse,"itm_animal_big", imod_smelling),
    (else_try),
        (spawn_horse,"itm_animal_big", imod_large_bag),
    (try_end),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, 0), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, 0), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, 0), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, 0), #sound 2
    ] or []) + [          
    ])]),

("animal_wolf",sokf_invisible,"wolf","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
    ] + (is_a_wb_sceneprop==1 and [ 
	(spawn_horse,"itm_animal_wolf", 0),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, 0), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, "anim_wolf_snap"), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, 0), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, "snd_warg_lone_woof"), #sound 2
    (agent_set_slot, reg0, slot_agent_mount_dead, 15), #chance to move per second, minimum 5%
    ] or []) + [          
    ])]),

("animal_bear",sokf_invisible,"bear","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
    ] + (is_a_wb_sceneprop==1 and [ 
	(spawn_horse,"itm_animal_bear", 0),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, "anim_bear_slam"), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, "anim_wolf_snap"), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, snd_bear_strike), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, snd_bear_strike), #sound 2
    (agent_set_slot, reg0, slot_agent_mount_dead, 15), #chance to move per second, minimum 5%
    ] or []) + [          
    ])]),
    
("animal_spider",sokf_invisible,"arrow_helper_blue","0", [(ti_on_init_scene_prop,[
    ] + (is_a_wb_sceneprop==1 and [
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),    
    (scene_prop_set_slot, ":instance_no", slot_prop_playing_sound, "itm_animal_spider"),
    ] or []) + [
    ])]),

("animal_werewolf",sokf_invisible,"mm_warg_a","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
    ] + (is_a_wb_sceneprop==1 and [ 
	(spawn_horse,"itm_animal_werewolf", 0),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, "anim_bear_slam"), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, "anim_bear_slam"), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, 0), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, "snd_warg_lone_woof"), #sound 2
    (agent_set_slot, reg0, slot_agent_mount_dead, 15), #chance to move per second, minimum 5%
    ] or []) + [          
    ])]),
 
("animal_sheep",sokf_invisible,"CWE_sheep_mod_a","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
    ] + (is_a_wb_sceneprop==1 and [ 
	(store_random_in_range, ":animal_var", imod_rusty, imod_bent+1),														 
	(spawn_horse,"itm_animal_small", ":animal_var"),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, 0), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, "anim_wolf_snap"), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, snd_sheep), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, snd_sheep), #sound 2
    ] or []) + [          
    ])]),

("animal_horse",sokf_invisible,"CWE_horse_light_a","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),

    ] + (is_a_wb_sceneprop==1 and [ 
	(store_random_in_range, ":animal_var", imod_cracked, imod_bent+1),														 
	(spawn_horse,"itm_animal_horse", ":animal_var"),
    #(agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, 0), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, 0), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, snd_horse_breath), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, snd_horse_low_whinny1), #sound 2
    (agent_set_slot, reg0, slot_agent_mount_dead, 5), #chance to move per second, minimum 5%
    ] or []) + [          
    ])]),

("rock_cliff_k_bb",0,"beefbacon_cliff_01","bo_terrain_cliff_01",[]),
("rock_cliff_l_bb",0,"beefbacon_cliff_02","bo_terrain_cliff_02",[]),
("rock_cliff_m_bb",0,"beefbacon_cliff_03","bo_terrain_cliff_03",[]),
("rock_cliff_n_bb",0,"beefbacon_cliff_04","bo_terrain_cliff_04",[]),
("rock_cliff_o_bb",0,"beefbacon_cliff_05","bo_terrain_cliff_05",[]),
("rock_cliff_p_bb",0,"beefbacon_cliff_06","bo_terrain_cliff_06",[]),

	
#Ruthven - CWE props 
] + (is_a_wb_sceneprop==1 and [
  ("birds_crebain", sokf_moveable|sokf_dynamic_physics, "woron_flight", "0", [
    (ti_on_scene_prop_init,[
      (store_trigger_param_1, ":instance_no"),
      (store_random_in_range, ":var3", 0, 16),
      (prop_instance_deform_to_time, ":instance_no", ":var3"),      
      (val_mul, ":var3", 80),
      (scene_prop_set_slot, ":instance_no", 39, ":var3"), #height offset
      (scene_prop_set_slot, ":instance_no", 43, 11), #dead frame
      (prop_instance_deform_in_cycle_loop, ":instance_no", 1, 17, 1700),
    ]), ]),

  ("birds_thrush", sokf_moveable|sokf_dynamic_physics, "thrush_flight", "0", [
    (ti_on_scene_prop_init,[
      (store_trigger_param_1, ":instance_no"),
      (store_random_in_range, ":var3", 0, 16),
      (prop_instance_deform_to_time, ":instance_no", ":var3"),      
      (val_mul, ":var3", 80),
      (scene_prop_set_slot, ":instance_no", 39, ":var3"), #height offset
      (scene_prop_set_slot, ":instance_no", 43, 12), #dead frame
      (prop_instance_deform_in_cycle_loop, ":instance_no", 1, 18, 1700),
    ]),]),

  ("birds_pigeon", sokf_moveable|sokf_dynamic_physics, "golub_flight", "0", [
    (ti_on_scene_prop_init,[
      (store_trigger_param_1, ":instance_no"),
      (store_random_in_range, ":var3", 0, 16),
      (prop_instance_deform_to_time, ":instance_no", ":var3"),      
      (val_mul, ":var3", 80),
      (scene_prop_set_slot, ":instance_no", 39, ":var3"), #height offset
      (scene_prop_set_slot, ":instance_no", 43, 12), #dead frame
      (prop_instance_deform_in_cycle_loop, ":instance_no", 1, 18, 1700),
    ]),]),

    ] or [	
  ("birds_crebain", sokf_invisible, "woron_flight", "0", []),
  ("birds_thrush",  sokf_invisible, "woron_flight", "0", []),
  ("birds_pigeon",  sokf_invisible, "woron_flight", "0", []),
	]) + [
  
  ("birds_end", sokf_moveable|sokf_dynamic_physics, "woron_flight", "bo_woron_flight", [  ]),

#more tents
("tent_d_old", 0, "old_tent", "bo_tent", []),
( "khand_tent_a_open"                            ,0,"khandTentOpen_a","bo_tent_1_open",[]),
( "khand_tent_b_open"                            ,0,"khandTentOpen_b","bo_tent_1_open",[]),
( "orc_tent_large"                               ,0,"orcTentLarge","bo_orcTentLarge",[]),
( "rhun_tent_1"                                ,0,"rhun_tent_1","bo_Rhun_tent_1",[]),
( "rhun_tent_2"                                ,0,"rhun_tent_2","bo_Rhun_tent_2",[]),
( "tent_1_a"                                   ,0,"tent_1_a","bo_tent_1_a",[]),
( "tent_1_open"                                ,0,"tent_1_open","bo_tent_1_open",[]),
( "tent_2_a"                                   ,0,"tent_2_a","bo_tent_1_a",[]),
( "tent_2_open"                                ,0,"tent_2_open","bo_tent_1_open",[]),
( "tent_3_open"                                ,0,"tent_3_open","bo_tent_3_open",[]),
( "tent_4"                                     ,0,"tent_4","bo_tent_4",[]),
( "tent_4_open"                                ,0,"tent_4_open","bo_tent_4_open",[]),
( "tent_a2"                                 ,0,"new_tent_a","bo_new_tent_a",[]),
( "tent_b2"                                 ,0,"new_tent_b","bo_new_tent_b",[]),
( "tent_c2"                                 ,0,"new_tent_c","bo_new_tent_c",[]),
( "orc_shelter_1b"                             ,0,"orc_shelter_1b","bo_orc_shelter_1",[]),
( "orc_shelter_2b"                             ,0,"orc_shelter_2b","bo_orc_shelter_2",[]),
("arabian_tent_harad",0,"arabian_tent_harad","bo_arabian_tent", []), #wb only
("arabian_tent_harad_b",0,"arabian_tent_harad_b","bo_arabian_tent_b", []), #wb only

#Zachary Foster - Mossy rock props
( "stone_wall_mossy_1"                                  ,0,"zf_wall_1","bo_zf_wall_1",[]),
( "stone_wall_mossy_2"                                  ,0,"zf_wall_2","bo_zf_wall_2",[]),
( "stone_wall_mossy_3"                                  ,0,"zf_wall_3","bo_zf_wall_3",[]),
( "stone_block_mossy_1"                           ,0,"zf_block_0","bo_zf_block_0",[]),
( "stone_block_mossy_2"                          ,0,"zf_block_1","bo_zf_block_1",[]),
( "stone_block_mossy_3"                           ,0,"zf_block_2","bo_zf_block_2",[]),
( "stone_block_mossy_4"                           ,0,"zf_block_3","bo_zf_block_3",[]),

( "fence_new"                           ,0,"fence_new","bo_fence_new",[]),

("MT_wall",0,"Gondor_wall_final","bo_MT_circular_wall",[]),
("MT_wall_part_lowpoly",0,"Gondor_wall_final_lowpoly",0,[]),

#CWE props
( "gon_small_wall_a_1_var_cwe"            ,0,"damask_arabian_wall_a_1_var1","bo_damask_arabian_wall_a_1_var1",[]),
( "gon_small_wall_b_1_cwe"           ,0,"eastern_wall_b_1","bo_eastern_wall_b_1",[]),
( "gon_small_wall_b_2_cwe"           ,0,"eastern_wall_b_2","bo_eastern_wall_b_2",[]),
( "gon_small_wall_b_3_cwe"           ,0,"eastern_wall_b_3","bo_eastern_wall_b_3",[]),
( "gon_well_a_cwe"                          ,0,"damask_kolodec_a","bo_damask_kolodec_a",[]),
( "gon_well_b_cwe"                          ,0,"damask_kolodec_b","bo_damask_kolodec_b",[]),
( "gon_well_c_cwe"                          ,0,"damask_kolodec_c","bo_damask_kolodec_c",[]),
( "gon_well_d_cwe"                               ,0,"damask_kolodec_d","bo_damask_kolodec_d",[]),
( "gon_well_e_cwe"                       ,0,"df","bo_df",[]),
( "gon_well_f"                           ,0,"fountain_gon","bo_fountain",[]),

( "gondor_palace_cwe"                       ,0,"cwe_royal_Palace_a","bo_cwe_royal_Palace_a",[]),
( "gondor_tower_8_cwe"                      ,0,"damask_watch_tower_a","bo_damask_watch_tower_a",[]),
( "gondor_arch_1_cwe"                               ,0,"damask_arka_b","bo_damask_arka_b",[]),
( "gondor_arch_2"                               ,0,"gondor_arches","bo_gondor_arches",[]), #TLD
( "gondor_arch_2_bend"                               ,0,"gondor_arches_bend","bo_gondor_arches_bend",[]), #TLD
( "gondor_arch_3"                               ,0,"gondor_arches_2","bo_gondor_arches_2",[]), #TLD
( "gondor_mt_stairs_cwe"                        ,0,"damask_dom_a_ladder","bo_damask_dom_a_ladder",[]),
( "gondor_column_a_cwe"                     ,0,"damask_klumba_a","bo_damask_klumba_a",[]),

( "gondor_copula_4_cwe"                     ,0,"damask_superstructure_b","bo_damask_superstructure_b",[]),
( "gondor_copula_5_cwe"                             ,0,"Capellas_a","bo_Capellas_a",[]),
( "gondor_copula_6_cwe"                             ,0,"Capellas_d","bo_capellas_d",[]),
( "gondor_copula_7_cwe"                             ,0,"Capellas_c","bo_capellas_c",[]),
( "gondor_copula_8_cwe"                             ,0,"Capellas_b","bo_capellas_b",[]),

( "crane_a_cwe"                                     ,0,"mechanism_for_sieges","0",[]),
( "crane_b_cwe"                                     ,0,"cargo_crane","0",[]),
( "basket_cwe"                              ,0,"korzina_1","bo_korzina_1",[]),

#Khazad mod props
( "khazad_dwarf_mech_stand"                    ,0,"khazad_dwarf_mech_stand","bo_khazad_dwarf_mech_stand",[]),
( "khazad_dwarf_mech_wheel"                    ,0,"khazad_dwarf_mech_wheel","0",[]),
( "khazad_dwarf_mech_water"                    ,0,"khazad_dwarf_mech_water","0",[]),

#Spak props
( "fish_barrel_spak"                           ,0,"spak_barrel_fish","0",[]),
( "fish_box_01_spak"                           ,0,"spak_boxfish_01","bo_spak_boxfish_01",[]),
( "fish_box_02_spak"                           ,0,"spak_boxfish_02","bo_spak_boxfish_01",[]),
( "gear_wheel_spak_2"                          ,0,"spak_gear_wheel_2","0",[]),
( "gear_wheel_spak_1"                          ,0,"spak_gear_wheel_1","0",[]),
( "water_wheel_spak"                           ,0,"spak_water_weel","0",[]),


("fog_scene_black",0,"0","0",[(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),
  (prop_instance_get_position, pos1, ":instance_no"),
  (particle_system_add_new,"psys_scene_fog_black",pos1)]),]), 
("fog_scene_red",0,"0","0",[(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),
  (prop_instance_get_position, pos1, ":instance_no"),
  (particle_system_add_new,"psys_scene_fog_red",pos1)]),]),
("fog_scene_grey",0,"0","0",[(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),
  (prop_instance_get_position, pos1, ":instance_no"),
  (particle_system_add_new,"psys_scene_fog_grey",pos1)]),]),

("fire_glow",0,"0","0",[(ti_on_scene_prop_init,
    [(set_position_delta,0,0,0),
     (particle_system_add_new, "psys_fire_glow_1"), ]),]),
("fire_sparks",0,"0","0",[(ti_on_scene_prop_init,
    [(set_position_delta,0,0,0),
     (particle_system_add_new, "psys_torch_fire_sparks"), ]),]),
("fire_sparks_b",0,"0","0",[(ti_on_scene_prop_init,
    [(set_position_delta,0,0,0),
     (particle_system_add_new, "psys_fire_sparks_1"), ]),]),
("moon_sparks",0,"0","0",[(ti_on_scene_prop_init,
    [(set_position_delta,0,0,0),
     (particle_system_add_new, "psys_moon_beam_paricle_1"), ]),]),
("Village_fire_big_lowpoly",0,"0","0",
   [(ti_on_scene_prop_init,
    [(particle_system_add_new, "psys_village_fire_big_lowres"),
     (set_position_delta,0,0,100),
     (particle_system_add_new, "psys_village_fire_smoke_big_lowres"),
    ]),]),
("fire_glow_white",0,"0","0",[(ti_on_scene_prop_init,
    [(set_position_delta,0,0,0),
     (particle_system_add_new, "psys_fire_glow_1_white"), ]),]),

("mordor_clouds_2",sokf_moveable|sokf_place_at_origin,"skybox_cloud_overlay_2","0",[]),
("mordor_clouds_3",sokf_moveable|sokf_place_at_origin,"skybox_cloud_overlay_3","0",[]),

# retreat gates open at mission start and close when the assigned rally point in var_id_2 is lost. Place closed.
("gate_destructible_retreat",sokf_destructible|sokf_moveable,"gate_tld_displaced","bo_gate_tld_displaced",   [ 
   
   (ti_on_scene_prop_init,
    [(store_trigger_param_1, ":instance_no"),
    ] + (is_a_wb_sceneprop==1 and [ (is_edit_mode_enabled), ] or []) + [ 
    (set_fixed_point_multiplier, 10000),
    (prop_instance_get_scale, pos2, ":instance_no"),
    (position_get_scale_x, ":scale_x", pos2),
    (eq, ":scale_x", 10000), #only show tutorial message if scale is unchanged
    (display_message, "@{!} debug: retreat gates open at mission start and close when the assigned rally point in var_id_2 is lost. Place closed. var_id 1 checks AI limiters."),
    (display_message, "@{!} debug: scale prop to disable this message"),
    ]),
   
   (ti_on_scene_prop_destroy, [
    (store_trigger_param_1, ":gate_no"),
    (set_fixed_point_multiplier, 100),
    ] + (is_a_wb_sceneprop==1 and [   
    (scene_prop_set_slot, ":gate_no", scene_prop_open_or_close_slot, 2),
    ] or []) + [
    (prop_instance_get_starting_position, pos1, ":gate_no"),
    (particle_system_burst,"psys_game_hoof_dust",pos1,40),
    (particle_system_burst,"psys_dummy_smoke",pos1,30),
    #(particle_system_burst,"psys_pistol_smoke",pos1,200),
    (position_rotate_x, pos1, -180),
    (prop_instance_animate_to_position, ":gate_no", pos1, 400), #animate in 4 second
    (play_sound, "snd_dummy_destroyed"),
    (display_message,"@Gate is breached!"),
    #(assign, ":gate_aggravator_found", 0),

    ] + (is_a_wb_sceneprop==1 and [        
    (scene_prop_get_slot, ":gate_aggravator", ":gate_no", slot_prop_agent_1),
    (call_script, "script_remove_agent", ":gate_aggravator"), 
    ] or [    
    (assign, ":gate_aggravator_found", 0),
    (try_for_agents, ":agent_no"), #find and remove gate aggravator agent
        (eq, ":gate_aggravator_found", 0),
        (gt, ":agent_no", 0),
        (agent_is_alive, ":agent_no"),  
        (agent_get_troop_id, ":troop_id", ":agent_no"),
        (eq, ":troop_id", "trp_gate_aggravator"),
        (agent_get_position, pos2, ":agent_no"),
        (set_fixed_point_multiplier, 100),
        (get_distance_between_positions, ":distance", pos1, pos2),
        (le, ":distance", 200),
        #(display_message, "@gate_aggravator found"),
        (call_script, "script_remove_agent", ":agent_no"), 
        (assign, ":gate_aggravator_found", 1),
    (try_end),
    ]) + [
       
    (scene_prop_get_num_instances,":max_barriers","spr_ai_limiter_gate_breached"),  #move away all dependent barriers
    (try_begin),
      (gt, ":max_barriers",0),
      (try_for_range,":count",0,":max_barriers"),
        (scene_prop_get_instance,":barrier_no", "spr_ai_limiter_gate_breached", ":count"),
        (prop_instance_get_starting_position, pos1, ":barrier_no"),
        ] + (is_a_wb_sceneprop==1 and [  #different methods of finding dependent barriers in WB and MB
        (prop_instance_get_variation_id, ":var1", ":barrier_no"),
        (prop_instance_get_variation_id, ":var1_gate", ":gate_no"),
        (eq, ":var1", ":var1_gate"),
        ] or [
        (prop_instance_get_starting_position, pos2, ":gate_no"),
        (set_fixed_point_multiplier, 100),
        (get_distance_between_positions, ":distance", pos1, pos2),
        (le, ":distance", 1000),
        ]) + [
        (position_move_z,pos1,-10000),
        (prop_instance_set_position,":barrier_no",pos1),
      (try_end),
    (try_end),
   ]),

   (ti_on_scene_prop_hit,
    [(play_sound, "snd_dummy_hit"),
      (particle_system_burst, "psys_dummy_smoke", pos1, 3),
      (particle_system_burst, "psys_dummy_straw", pos1, 10),
    ]),
], 2500),

("spike_group_a_destructible",sokf_destructible,"spike_group_a","bo_spike_group_a_big",   [ 
   (ti_on_scene_prop_init, [
   (store_trigger_param_1, ":instance_no"),
   (eq, "$gate_aggravator_agent", 1),    
    (prop_instance_get_starting_position, pos1, ":instance_no"),
    (set_fixed_point_multiplier, 100),
    (position_move_z, pos1, 100,1), #safeguard against aggravators spawning underground
    (set_spawn_position, pos1),
    (spawn_agent,"trp_gate_aggravator"),
    (agent_get_position, pos1, reg0),      
    (assign, ":gate_aggravator", reg0),
    (agent_set_speed_limit, ":gate_aggravator", 0),
    (agent_set_team, ":gate_aggravator", 2),
    ] + (is_a_wb_sceneprop==1 and [               # make aggravator a statue (WB Only)
    (agent_set_no_dynamics, ":gate_aggravator",1),
    (agent_set_no_death_knock_down_only, ":gate_aggravator", 1),
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, ":gate_aggravator"),
    ] or []) + [
  ]),
   
   (ti_on_scene_prop_destroy, [
    (store_trigger_param_1, ":gate_no"),
    (prop_instance_get_starting_position, pos1, ":gate_no"),
    (particle_system_burst,"psys_dummy_smoke",pos1,10),
    (position_rotate_x, pos1, -80),
    (position_move_z, pos1, -200,1),
    (prop_instance_animate_to_position, ":gate_no", pos1, 400), #animate in 4 second
    (play_sound, "snd_dummy_destroyed"),
    
    ] + (is_a_wb_sceneprop==1 and [        
    (scene_prop_get_slot, ":gate_aggravator", ":gate_no", slot_prop_agent_1),
    (call_script, "script_remove_agent", ":gate_aggravator"), 
    ] or [    
    (assign, ":gate_aggravator_found", 0),
    (try_for_agents, ":agent_no"), #find and remove gate aggravator agent
        (eq, ":gate_aggravator_found", 0),
        (gt, ":agent_no", 0),
        (agent_is_alive, ":agent_no"),  
        (agent_get_troop_id, ":troop_id", ":agent_no"),
        (eq, ":troop_id", "trp_gate_aggravator"),
        (agent_get_position, pos2, ":agent_no"),
        (set_fixed_point_multiplier, 100),
        (get_distance_between_positions, ":distance", pos1, pos2),
        (le, ":distance", 200),
        #(display_message, "@gate_aggravator found"),
        (call_script, "script_remove_agent", ":agent_no"), 
        (assign, ":gate_aggravator_found", 1),
    (try_end),
    ]) + [
    
    (scene_prop_get_num_instances,":max_barriers","spr_ai_limiter_spikes_broken"),  #move away all dependent barriers
    (try_begin),
      (gt, ":max_barriers",0),
      (try_for_range,":count",0,":max_barriers"),
        (scene_prop_get_instance,":barrier_no", "spr_ai_limiter_spikes_broken", ":count"),
        (prop_instance_get_starting_position, pos1, ":barrier_no"),
        (prop_instance_get_starting_position, pos2, ":gate_no"),
        (set_fixed_point_multiplier, 100),
        (get_distance_between_positions, ":distance", pos1, pos2),
        (le, ":distance", 200), #two meters
        (position_move_z,pos1,-10000),
        (prop_instance_set_position,":barrier_no",pos1),
      (try_end),
    (try_end),
    
   ]),

   (ti_on_scene_prop_hit,    [
    (try_begin),
        (store_trigger_param, ":attacker_agent",3),
        (store_trigger_param, ":missile", 6), 
        (agent_get_team, ":team", ":attacker_agent"),
        (this_or_next|neg|teams_are_enemies, 2, ":team"),
        (gt, ":missile", 0),
        (set_trigger_result, 0),
    (else_try),
        (play_sound, "snd_dummy_hit"),
        (particle_system_burst, "psys_dummy_smoke", pos1, 3),
        (particle_system_burst, "psys_dummy_straw", pos1, 10),
    (try_end),
    ]),
], 500),

("orc_stakes_destructible",sokf_destructible,"orc_stakes","bo_orc_stakes_new",   [ 
   (ti_on_scene_prop_init, [
   (store_trigger_param_1, ":instance_no"),
   (eq, "$gate_aggravator_agent", 1),      
    (prop_instance_get_starting_position, pos1, ":instance_no"),
    (set_fixed_point_multiplier, 100),
    (position_move_z, pos1, 100,1), #safeguard against aggravators spawning underground
    (set_spawn_position, pos1),
    (spawn_agent,"trp_gate_aggravator"),
    (agent_get_position, pos1, reg0),      
    (assign, ":gate_aggravator", reg0),
    (agent_set_speed_limit, ":gate_aggravator", 0),
    (agent_set_team, ":gate_aggravator", 2),
    ] + (is_a_wb_sceneprop==1 and [               # make aggravator a statue (WB Only)
    (agent_set_no_dynamics, ":gate_aggravator",1),
    (agent_set_no_death_knock_down_only, ":gate_aggravator", 1),
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, ":gate_aggravator"),
    ] or []) + [
  ]),
   
   (ti_on_scene_prop_destroy, [
    (store_trigger_param_1, ":gate_no"),
    (prop_instance_get_starting_position, pos1, ":gate_no"),
    (particle_system_burst,"psys_dummy_smoke",pos1,10),
    (position_rotate_x, pos1, -80),
    (position_move_z, pos1, -200,1),
    (prop_instance_animate_to_position, ":gate_no", pos1, 400), #animate in 4 second
    (play_sound, "snd_dummy_destroyed"),
    
    ] + (is_a_wb_sceneprop==1 and [        
    (scene_prop_get_slot, ":gate_aggravator", ":gate_no", slot_prop_agent_1),
    (call_script, "script_remove_agent", ":gate_aggravator"), 
    ] or [    
    (assign, ":gate_aggravator_found", 0),
    (try_for_agents, ":agent_no"), #find and remove gate aggravator agent
        (eq, ":gate_aggravator_found", 0),
        (gt, ":agent_no", 0),
        (agent_is_alive, ":agent_no"),  
        (agent_get_troop_id, ":troop_id", ":agent_no"),
        (eq, ":troop_id", "trp_gate_aggravator"),
        (agent_get_position, pos2, ":agent_no"),
        (set_fixed_point_multiplier, 100),
        (get_distance_between_positions, ":distance", pos1, pos2),
        (le, ":distance", 200),
        #(display_message, "@gate_aggravator found"),
        (call_script, "script_remove_agent", ":agent_no"), 
        (assign, ":gate_aggravator_found", 1),
    (try_end),
    ]) + [
    
    (scene_prop_get_num_instances,":max_barriers","spr_ai_limiter_spikes_broken"),  #move away all dependent barriers
    (try_begin),
      (gt, ":max_barriers",0),
      (try_for_range,":count",0,":max_barriers"),
        (scene_prop_get_instance,":barrier_no", "spr_ai_limiter_spikes_broken", ":count"),
        (prop_instance_get_starting_position, pos1, ":barrier_no"),
        (prop_instance_get_starting_position, pos2, ":gate_no"),
        (set_fixed_point_multiplier, 100),
        (get_distance_between_positions, ":distance", pos1, pos2),
        (le, ":distance", 200), #two meters
        (position_move_z,pos1,-10000),
        (prop_instance_set_position,":barrier_no",pos1),
      (try_end),
    (try_end),
    
   ]),

   (ti_on_scene_prop_hit,    [
    (try_begin),
        (store_trigger_param, ":attacker_agent",3),
        (store_trigger_param, ":missile", 6), 
        (agent_get_team, ":team", ":attacker_agent"),
        (this_or_next|neg|teams_are_enemies, 2, ":team"),
        (gt, ":missile", 0),
        (set_trigger_result, 0),
    (else_try),
        (play_sound, "snd_dummy_hit"),
        (particle_system_burst, "psys_dummy_smoke", pos1, 3),
        (particle_system_burst, "psys_dummy_straw", pos1, 10),
    (try_end),
    ]),
    
], 200),

("elf_treehouse_b",0,"elf_treehouse_b","bo_elf_treehouse_b",[]),  

("troop_rider",sokf_invisible,"arrow_helper_blue","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),
    (store_faction_of_party, ":faction", "$current_town"),
    (faction_get_slot, ":troop", ":faction", slot_faction_rider_troop),
    (set_fixed_point_multiplier, 100),
    (prop_instance_get_scale, pos2, ":instance_no"),
    (position_get_scale_y, ":tier", pos2),
    (val_sub, ":tier", 100),
    (val_div, ":tier", 10),
    (try_begin),
        (ge, ":tier", 1),
        (try_for_range, ":unused", 0, ":tier"),
            (troop_get_upgrade_troop, ":upgrade_troop", ":troop", 0),
            (gt, ":upgrade_troop", 0),
            (assign, ":troop", ":upgrade_troop"),
        (try_end),
    (try_end),
            
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),  (spawn_agent, ":troop"),
    (lt, "$g_encountered_party_2", 0), #don't spawn riders in siege battles
    (agent_set_slot, reg0, slot_agent_target_entry_point, ":instance_no"), #home position
    (agent_set_slot, reg0, slot_agent_walker_type, 2), #patrol
    (store_random_in_range,reg10,5,12), 
    (agent_set_speed_limit, reg0, reg10),
    (agent_set_team, reg0, 0),

] + (is_a_wb_sceneprop==1 and [     
        (try_for_range, ":weapon_slot", 0, 4), #find polearm
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (item_get_type, ":item_type", ":item"),
            (eq, ":item_type", itp_type_polearm),
            #(agent_equip_item, reg0, ":item", 1),
            (agent_set_wielded_item, reg0, ":item"),
                (try_for_range, ":weapon_slot", 0, 4), #find shield
                    (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
                    (gt, ":item", 1),
                    (item_get_type, ":item_type", ":item"),
                    (eq, ":item_type", itp_type_shield),
                    (agent_set_wielded_item, reg0, ":item"),
                (try_end),
        (try_end),
    ] or []) + [            
        (store_random_in_range, reg6, 0, 100),
        (agent_set_animation_progress, reg0, reg6),
    ])]),

("troop_messenger",sokf_invisible,"arrow_helper_blue","0", [
    (ti_on_init_scene_prop,[
    (store_random_in_range, ":chance", 0, 100),
    (lt, ":chance", 40),
    (store_trigger_param_1, ":instance_no"),
    (store_faction_of_party, ":faction", "$current_town"),
    (faction_get_slot, ":troop", ":faction", slot_faction_rider_troop),
    (set_fixed_point_multiplier, 100),
    (prop_instance_get_scale, pos2, ":instance_no"),
    (position_get_scale_y, ":tier", pos2),
    (val_sub, ":tier", 100),
    (val_div, ":tier", 10),
    (try_begin),
        (ge, ":tier", 1),
        (try_for_range, ":unused", 0, ":tier"),
            (troop_get_upgrade_troop, ":upgrade_troop", ":troop", 0),
            (gt, ":upgrade_troop", 0),
            (assign, ":troop", ":upgrade_troop"),
        (try_end),
    (try_end),
            
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),  (spawn_agent, ":troop"),
    (lt, "$g_encountered_party_2", 0), #don't spawn riders in siege battles
    (agent_set_team, reg0, 0),
    (agent_set_slot, reg0, slot_agent_walker_type, 3), #messenger  
    
    #send them out
    (scene_prop_get_num_instances, ":num_messenger_exits", "spr_troop_messenger_exit"),
    (gt, ":num_messenger_exits", 0),
    (store_random_in_range, ":rand_exit", 0, ":num_messenger_exits"),
    (scene_prop_get_instance, ":instance_no_target", "spr_troop_messenger_exit", ":rand_exit"),
    (prop_instance_get_position, pos2, ":instance_no_target"),
    (agent_set_scripted_destination, reg0, pos2),
    (agent_set_slot, reg0, slot_agent_is_running_away, 1), #needed for tracking
    (agent_set_speed_limit, reg0, 12),
    ])
    ]),

("troop_guard_patrol_target_var2",sokf_invisible,"arrow_helper_blue","0", []),

("troop_messenger_exit",sokf_invisible,"arrow_helper_blue","0", []),

("troop_civ_walker",sokf_invisible,"arrow_helper_blue","0", [(ti_on_init_scene_prop,[												 
    (store_trigger_param_1, ":instance_no"),
    (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
	(store_random_in_range, ":rand", 0, 9),
    (store_add, ":troop_slot", slot_center_walker_0_troop, ":rand"),
    (party_get_slot, ":troop", "$current_town", ":troop_slot"),

    (spawn_agent, ":troop"),
    (agent_set_team, reg0, 0),
    (store_random_in_range, reg6, 0, 100),
    (agent_set_animation_progress, reg0, reg6),
    
    (agent_set_slot, reg0, slot_agent_walker_type, 4), #prop walker
    (store_random_in_range, ":speed", 2, 6), 
    (agent_set_speed_limit, reg0, ":speed"),
    ] + (is_a_wb_sceneprop==1 and [     
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    ] or []) + [    
  ])]),

("light_white",sokf_invisible,"light_sphere","0",  [
     (ti_on_init_scene_prop,
      [   (store_trigger_param_1, ":prop_instance_no"),
          (set_fixed_point_multiplier, 100),
          (prop_instance_get_scale, pos5, ":prop_instance_no"),
          (position_get_scale_x, ":scale", pos5),
          (store_mul, ":red", 3 * 200, ":scale"),
          (store_mul, ":green", 3 * 200, ":scale"),
          (store_mul, ":blue", 3 * 200, ":scale"),
          (val_div, ":red", 100),
          (val_div, ":green", 100),
          (val_div, ":blue", 100),
          (set_current_color,":red", ":green", ":blue"),
          (set_position_delta,0,0,0),
          (add_point_light, 10, 30),
      ])]),

("light_rgb",sokf_invisible,"light_sphere","0",  [
     (ti_on_init_scene_prop,
      [   (store_trigger_param_1, ":prop_instance_no"),      
          (set_fixed_point_multiplier, 100),
          (prop_instance_get_scale, pos5, ":prop_instance_no"),
          (position_get_scale_x, ":scale_x", pos5),
          (position_get_scale_y, ":scale_y", pos5),
          (position_get_scale_z, ":scale_z", pos5),
          (store_mul, ":red", 3 * 150, ":scale_x"),
          (store_mul, ":green", 3 * 150, ":scale_y"),
          (store_mul, ":blue", 3 * 150, ":scale_z"),
          (val_div, ":red", 100),
          (val_div, ":green", 100),
          (val_div, ":blue", 100),
          (set_current_color,":red", ":green", ":blue"),
          (set_position_delta,0,0,0),
          (assign, ":flicker_magnitude", 0),
          (assign, ":flicker_interval", 0),
             ] + (is_a_wb_sceneprop==1 and [
            (prop_instance_get_variation_id, ":flicker_magnitude", ":prop_instance_no"),
            (prop_instance_get_variation_id_2, ":flicker_interval", ":prop_instance_no"),
             ] or []) + [  
          (add_point_light, ":flicker_magnitude", ":flicker_interval"),
      ])]),

("glow_a", 0, "glow_a", "0", []),

# Mark7's Dynamic Props
      # ("glow_a", 0, "glow_a_new", "0", [
      # ] + (is_a_wb_sceneprop==1 and [
     # (ti_on_scene_prop_init,[
         # (store_trigger_param_1, ":instance_no"),
        # (store_random_in_range,":r",0,100), # Random animations time
				# (try_begin),
          # (ge, ":r", 50),
          # (try_begin),
          # (ge, ":r", 75),
          # (prop_instance_deform_in_cycle_loop, ":instance_no", 1,24, 3000),
          # #(display_message, "@glow_a ANIM + Fast"),
          # (else_try),
          # (prop_instance_deform_in_cycle_loop, ":instance_no", 1,24, 4000),
          # #(display_message, "@glow_a ANIM + Slow"),
          # (try_end),
        # (else_try),
        # (try_begin),
          # (ge, ":r", 25),
         # (prop_instance_deform_in_cycle_loop, ":instance_no", 24,1, 3000),
         # #(display_message, "@glow_a ANIM - Fast"),
          # (else_try),
          # (prop_instance_deform_in_cycle_loop, ":instance_no", 24,1, 4000),
          # #(display_message, "@glow_a ANIM - Slow"),
          # (try_end),
        # (try_end),
    # ]),
    # ] or []) + [ 
     # ]),
     
("glow_a_daytime_specific", 0, "glow_a", "0", [ #important: place according to current daytime (noon = point north)
     (ti_on_init_scene_prop,
      [   (store_trigger_param_1, ":prop_instance_no"),
          (store_time_of_day, ":daytime"), #0-24h
          (val_mul, ":daytime", 15), #0-360
          (prop_instance_get_position, pos1, ":prop_instance_no"),
          #(position_get_rotation_around_z, ":rotation", pos1),
          (position_rotate_z, pos1, ":daytime"),
          (prop_instance_set_position, ":prop_instance_no", pos1),
      ])]),
      
 ("glow_b", 0, "glow_b_new", "0", [
     ] + (is_a_wb_sceneprop==1 and [
     (ti_on_scene_prop_init,[
         (store_trigger_param_1, ":instance_no"),
        (store_random_in_range,":r",0,100), # Random animations time
				(try_begin),
          (ge, ":r", 50),
          (try_begin),
          (ge, ":r", 75),
          (prop_instance_deform_in_cycle_loop, ":instance_no", 1,24, 3000),
          #(display_message, "@glow_b ANIM + Fast"),
          (else_try),
          (prop_instance_deform_in_cycle_loop, ":instance_no", 1,24, 4000),
          #(display_message, "@glow_b ANIM + Slow"),
          (try_end),
        (else_try),
        (try_begin),
          (ge, ":r", 25),
         (prop_instance_deform_in_cycle_loop, ":instance_no", 24,1, 3000),
         #(display_message, "@glow_b ANIM - Fast"),
          (else_try),
          (prop_instance_deform_in_cycle_loop, ":instance_no", 24,1, 4000),
          #(display_message, "@glow_b ANIM - Slow"),
          (try_end),
        (try_end),
    ]),
     ] or []) + [ 
     ]),
# Mark7's Dynamic Props end

("ai_fadeout_sphere",sokf_invisible,"sphere_1m","0", []),
("ai_limiter_spikes_broken" ,sokf_invisible|sokf_type_ai_limiter|sokf_moveable,"barrier_2m" ,"bo_barrier_2m" , []),

] + (is_a_wb_sceneprop==1 and [ 
("ammo_stack_good", spr_use_time(2), "ammo_stack", "bo_ammo_barrel", [
     (ti_on_scene_prop_use,
      [(store_trigger_param_2, ":scene_prop"),
      (get_player_agent_no, ":player_agent"),   
      (agent_refill_ammo, ":player_agent"),
      (scene_prop_enable_after_time, ":scene_prop", 500),  
      ])]),
("ammo_stack_evil", spr_use_time(2), "ammo_stack_evil", "bo_ammo_barrel", [
     (ti_on_scene_prop_use,
      [(store_trigger_param_2, ":scene_prop"),
      (get_player_agent_no, ":player_agent"),   
      (agent_refill_ammo, ":player_agent"),
      (scene_prop_enable_after_time, ":scene_prop", 500),  
      ])]),      
       ] or [("ammo_stack_good", 0, "ammo_stack", "bo_ammo_barrel", []),("ammo_stack_evil", 0, "ammo_stack_evil", "bo_ammo_barrel", []),]) + [      



("inventory_static",sokf_type_container,"package","bobaggage", []),

#Helms Deep
("HD_breached",0,"HD_breached","bo_helms_deep_breached", []),

("troop_civ_lying",sokf_invisible,"man_body_lie","bo_man_body_lie", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),
    (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
    (store_faction_of_party, ":fac", "$current_town"),
    (faction_get_slot, ":troop", ":fac", slot_faction_tier_1_troop), #get a tier 1 troop so they don't wear heavy armour
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
    (store_random_in_range, ":anim", 0, 3),
    (val_add, ":anim", "anim_fall_face_hold"),
	(spawn_agent, ":troop"),
    (agent_set_team, reg0, 0),(agent_set_animation, reg0, ":anim"),(agent_set_animation_progress, reg0, 100),
    (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk
    
        #remove weapons and helms
  ] + (is_a_wb_sceneprop==1 and [    
        (try_for_range, ":weapon_slot", 0, 5), #weapons and helm
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),
        (try_begin),
            (agent_get_item_slot, ":gloves", reg0, ek_gloves),
            (gt, ":gloves", 1),
            (agent_unequip_item, reg0, ":gloves", ek_gloves),
        (try_end),        
        (store_random_in_range, ":chance", 0, 10),
        (try_begin), 
            (ge, ":chance", 3),
            (agent_get_item_slot, ":boots", reg0, ek_foot),
            (gt, ":boots", 1),
            (agent_unequip_item, reg0, ":boots", ek_foot),
        (try_end),    
        (try_begin),
            (ge, ":chance", 8),
            (agent_get_item_slot, ":armour", reg0, ek_body),
            (gt, ":armour", 1),
            (agent_unequip_item, reg0, ":armour", ek_body),
        (try_end),
        
        #for better clip control
        (agent_set_no_dynamics, reg0, 1),
        (agent_ai_set_interact_with_player, reg0, 0),
        (troop_get_type, ":race", ":troop"),
        (try_begin), 
            (eq, ":race", tf_orc),
            (position_move_z, pos1, 10),
        (else_try),
            (eq, ":race", tf_dwarf),
            (position_move_z, pos1, 35),
        (try_end),
        (agent_set_position, reg0, pos1),
    ] or []) + [  
    ])]),

("troop_guard_fight_duel",sokf_invisible,"arrow_helper_blue","0", [(ti_on_init_scene_prop,[
  ] + (is_a_wb_sceneprop==1 and [  
    (store_trigger_param_1, ":instance_no"),
    (set_fixed_point_multiplier, 100),
    (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
    (party_get_slot, ":troop", "$current_town", slot_town_guard_troop),
    (spawn_agent, ":troop"), (assign, ":fighter_1", reg0),(agent_set_team, ":fighter_1", 0),(agent_ai_set_interact_with_player, ":fighter_1", 0),(agent_set_is_alarmed, ":fighter_1", 1),(agent_set_no_death_knock_down_only, ":fighter_1", 1),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, ":fighter_1"),
    (agent_set_slot, ":fighter_1", slot_agent_walker_type, 5), #don't talk
    
    (position_move_y, pos1, 500,0),
    (position_rotate_z, pos1, 180),
    (set_spawn_position, pos1),
    (spawn_agent, ":troop"),(assign, ":fighter_2", reg0),
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_2, ":fighter_2"),
    (agent_set_team, ":fighter_2", 0),(agent_ai_set_interact_with_player, ":fighter_2", 0),(agent_set_is_alarmed, ":fighter_2", 1),(agent_set_no_death_knock_down_only, ":fighter_2", 1),
    (agent_add_relation_with_agent, ":fighter_2", ":fighter_1", -1),(agent_add_relation_with_agent, ":fighter_1", ":fighter_2", -1),
    (agent_set_slot, ":fighter_2", slot_agent_walker_type, 5), #don't talk

    (try_begin),
        (faction_slot_eq,"$ambient_faction", slot_faction_side, faction_side_good),
        (assign, ":weapon_to_use", itm_practice_staff),
    (else_try),
        (store_random_in_range, ":rand", 0, 100),
        (assign, ":weapon_to_use", itm_wood_club),
        (ge, ":rand", 50),
        (assign, ":weapon_to_use", itm_twohand_wood_club),
    (try_end),
    (try_begin),
        (prop_instance_get_variation_id, ":var1", ":instance_no"),
        (eq, ":var1", 0),
        (try_for_range, ":weapon_slot", 0, 4), #remove weapons
            (agent_get_item_slot, ":item", ":fighter_1", ":weapon_slot"),
            (gt, ":item", 1),
            (agent_unequip_item, ":fighter_1", ":item", ":weapon_slot"),
            (agent_get_item_slot, ":item", ":fighter_2", ":weapon_slot"),
            (gt, ":item", 1),
            (agent_unequip_item, ":fighter_2", ":item", ":weapon_slot"),            
        (try_end), 
        (agent_equip_item, ":fighter_1", ":weapon_to_use", 1),
        (agent_set_wielded_item, ":fighter_1", ":weapon_to_use"),
        (agent_equip_item, ":fighter_2", ":weapon_to_use", 1),
        (agent_set_wielded_item, ":fighter_2", ":weapon_to_use"),
    (try_end),
    ] or []) + [  
  ])]),
  
("troop_guard_fight_single",0,"wood_a","bo_wood_a_bigger", [(ti_on_init_scene_prop,[
  ] + (is_a_wb_sceneprop==1 and [  
    (store_trigger_param_1, ":instance_no"),
    (set_fixed_point_multiplier, 100),
    (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
    (prop_instance_get_position, pos1, ":instance_no"),
    (party_get_slot, ":troop", "$current_town", slot_town_guard_troop),
    
    (position_move_y, pos1, -80,0),(set_spawn_position, pos1),
    (spawn_agent, ":troop"),(agent_set_team, reg0, 0),
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_scripted_destination, reg0, pos1), 
    (agent_set_damage_modifier, reg0, 0),
    (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk

    (assign, ":weapon_found", 0),
    (try_for_range, ":weapon_slot", 0, 4), #find weapon, non-polearm first
        (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
        (gt, ":item", 1),
        (item_get_type, ":item_type", ":item"),
        (this_or_next|eq, ":item_type", itp_type_one_handed_wpn),
        (eq, ":item_type", itp_type_two_handed_wpn),
        #(agent_equip_item, reg0, ":item", 1),
        (agent_set_wielded_item, reg0, ":item"),
        (assign, ":weapon_found", 1),
    (try_end),
    (try_for_range, ":weapon_slot", 0, 4), #find shield
        (eq, ":weapon_found", 1),
        (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
        (gt, ":item", 1),
        (item_get_type, ":item_type", ":item"),
        (eq, ":item_type", itp_type_shield),
        #(agent_equip_item, reg0, ":item", 1),
        (agent_set_wielded_item, reg0, ":item"),
    (try_end),
    
    (eq, ":weapon_found", 0), #no non-polearm weapon found? equip polearm w/o shield
    (try_for_range, ":weapon_slot", 0, 4),      
        (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
        (gt, ":item", 1),
        (item_get_type, ":item_type", ":item"),
        (neq, ":item_type", itp_type_shield),
        #(agent_equip_item, reg0, ":item", 1),
        (agent_set_wielded_item, reg0, ":item"),
        (item_get_weapon_length, ":length", ":item"), #polearm users need more space
        (val_add, ":length", 50),
        (val_mul, ":length", -1),
        # (assign, reg78, ":length"),
        # (display_message, "@length {reg78}"),
        (prop_instance_get_position, pos1, ":instance_no"),
        (position_move_y, pos1, ":length",0),
        (agent_set_position, reg0, pos1),
        (agent_set_scripted_destination, reg0, pos1), 
    (try_end), 
    ] or []) + [          ]),
        
   (ti_on_scene_prop_hit,
    [   (set_fixed_point_multiplier, 100), #sound is pretty loud, avoid hearingit from across the map
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos4, ":player_agent"),
        (get_distance_between_positions, ":distance", pos1, pos4),
        (le, ":distance", 20000), #20m  
        (play_sound, "snd_dummy_hit"),
        (particle_system_burst, "psys_dummy_smoke", pos1, 2),
        (particle_system_burst, "psys_dummy_straw", pos1, 10),
    ])]),

("troop_troll_fight_duel",sokf_invisible,"arrow_helper_blue","0", [(ti_on_init_scene_prop,[
  ] + (is_a_wb_sceneprop==1 and [  
    (store_trigger_param_1, ":instance_no"),
    (set_fixed_point_multiplier, 100),
    (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
    (store_faction_of_party, ":fac", "$current_town"),
    (faction_get_slot, ":troop", ":fac", slot_faction_troll_troop),
    (gt, ":troop", 0),
    (spawn_agent, ":troop"), (assign, ":fighter_1", reg0),
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, ":fighter_1"),(agent_set_team, ":fighter_1", 0),(agent_ai_set_interact_with_player, ":fighter_1", 0),(agent_set_is_alarmed, ":fighter_1", 1),(agent_set_no_death_knock_down_only, ":fighter_1", 1),
    (position_move_y, pos1, 300,0),
    (position_rotate_z, pos1, 180),
    (set_spawn_position, pos1),
    (spawn_agent, ":troop"),(assign, ":fighter_2", reg0),
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_2, ":fighter_2"),
    (agent_set_team, ":fighter_2", 0),(agent_ai_set_interact_with_player, ":fighter_2", 0),(agent_set_is_alarmed, ":fighter_2", 1),(agent_set_no_death_knock_down_only, ":fighter_2", 1),
    (agent_add_relation_with_agent, ":fighter_2", ":fighter_1", -1),(agent_add_relation_with_agent, ":fighter_1", ":fighter_2", -1),
    ] or []) + [  
  ])]),

("troop_archer_fight_single",sokf_invisible,"arrow_helper_blue","bo_man_body_lie_lower", [(ti_on_init_scene_prop,[
  ] + (is_a_wb_sceneprop==1 and [  
    (store_trigger_param_1, ":instance_no"),
    (set_fixed_point_multiplier, 100),
    (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
    (prop_instance_get_position, pos1, ":instance_no"), 
    (set_spawn_position, pos1),
    #(position_set_z_to_ground_level, pos1),
    (position_move_z, pos1, -150),
    (spawn_agent, "trp_i1_isen_orc_snaga"), #get a small troop
    (assign, ":target", reg0),
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_2, ":target"),
    (agent_set_team, ":target", 0),     
    (agent_set_no_dynamics, ":target", 1), 
    (agent_set_position, ":target", pos1),
    (agent_ai_set_interact_with_player, ":target", 0),
    (agent_set_is_alarmed, ":target", 0),
    (agent_set_no_death_knock_down_only, ":target", 1),
    (agent_set_visibility, ":target", 0),
    (agent_set_animation, ":target", "anim_fall_face_hold"),(agent_set_animation_progress, ":target", 100),
    #(agent_set_stand_animation, ":target", "anim_sit_on_throne"),
    # (agent_ai_set_can_crouch, ":target", 1),
    # (agent_set_crouch_mode, ":target", 1),
    
    (prop_instance_get_position, pos1, ":instance_no"),
    (position_move_y, pos1, -1000,0),(set_spawn_position, pos1),
    (party_get_slot, ":troop", "$current_town", slot_town_archer_troop),    
    (spawn_agent, ":troop"),(agent_set_team, reg0, 0),
    #(agent_set_no_dynamics, reg0, 1),
    (agent_set_scripted_destination, reg0, pos1), 
    (agent_add_relation_with_agent, reg0, ":target", -1),(agent_ai_set_interact_with_player, reg0, 0),(agent_set_is_alarmed, reg0, 1),(agent_set_no_death_knock_down_only, reg0, 1),
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk
    
    (assign, ":bow_found", 0),    
    (try_for_range, ":weapon_slot", 0, 4), #check if they have a bow or throwing weapon
        (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
        (gt, ":item", 1),
        (item_get_type, ":item_type", ":item"),
        (this_or_next|eq, ":item_type", itp_type_bow),
        (eq, ":item_type", itp_type_thrown),
        (assign, ":bow_found", 1),
    (try_end),
    (try_begin),        
        (neq, ":bow_found", 1),
        (agent_equip_item, reg0, itm_regular_bow, 3),
        (agent_equip_item, reg0, itm_arrows, 4),
    (try_end),
    ] or []) + [ 
  ])]),
  
("barrier_2m_horizontal" ,sokf_invisible|sokf_type_barrier,"barrier_2m_horizontal" ,"bo_barrier_2m_horizontal" , []),

("troop_work_wood_hacker_1h",0,"prop_wood_chopper","bo_prop_wood_chopper",   [
  ] + (is_a_wb_sceneprop==1 and [
    (ti_on_init_scene_prop,[
        (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100),
        (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
        (prop_instance_get_position, pos1, ":instance_no"), 
        (copy_position, pos2, pos1),
        (position_move_y, pos2, -95,0),(set_spawn_position, pos2),
        (store_random_in_range, ":walker_type", 0, 2), #only use first two town walkers, make sure they're not "rich" walkers
        (val_add, ":walker_type", slot_center_walker_0_troop),
        (party_get_slot, ":troop", "$current_town", ":walker_type"),
        (spawn_agent, ":troop"), 
        (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
        (try_for_range, ":weapon_slot", 0, 5), #remove weapons and helms
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (neg|item_has_property, ":item", itp_civilian),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),
        (agent_set_no_dynamics, reg0, 1),  
        (agent_equip_item, reg0, "itm_civilian_woodaxe_1h", 1),
        (agent_set_wielded_item, reg0, "itm_civilian_woodaxe_1h"),
        (agent_set_look_target_position, reg0, pos2),
        (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk
        ]),
        
   (ti_on_scene_prop_hit,
    [   (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100), #sound is pretty loud, avoid hearingit from across the map
        (prop_instance_get_variation_id, ":var1", ":instance_no"),
        (try_begin),
            (ge, ":var1", 1),
            (store_mul, ":sound_dist", ":var1", 100),
        (else_try),
            (assign, ":sound_dist", 1500),
        (try_end),
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos4, ":player_agent"),
        (get_distance_between_positions, ":distance", pos1, pos4),
        # (assign, reg66, ":distance"),
        # (display_message, "@distance: {reg66}"),
        (le, ":distance", ":sound_dist"), 
        (play_sound, "snd_dummy_hit"),
        (particle_system_burst, "psys_dummy_smoke", pos1, 2),
        (particle_system_burst, "psys_dummy_straw", pos1, 10),
    ])
    ] or []) + [
    ]),
    
("troop_work_wood_hacker_2h",0,"prop_wood_chopper","bo_prop_wood_chopper",   [
  ] + (is_a_wb_sceneprop==1 and [
    (ti_on_init_scene_prop,[
        (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100),
        (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
        (prop_instance_get_position, pos1, ":instance_no"), 
        (copy_position, pos2, pos1),
        (position_move_y, pos2, -130,0),(set_spawn_position, pos2),
        (store_random_in_range, ":walker_type", 0, 2), #only use first two town walkers, make sure they're not "rich" walkers
        (val_add, ":walker_type", slot_center_walker_0_troop),
        (party_get_slot, ":troop", "$current_town", ":walker_type"),
        (spawn_agent, ":troop"),
        (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
        (try_for_range, ":weapon_slot", 0, 5), #remove weapons and helms
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (neg|item_has_property, ":item", itp_civilian),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),
        (agent_set_no_dynamics, reg0, 1),  
        (agent_equip_item, reg0, "itm_civilian_woodaxe_2h", 1),
        (agent_set_wielded_item, reg0, "itm_civilian_woodaxe_2h"),
        (agent_set_look_target_position, reg0, pos2),
        (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk
        ]),
        
   (ti_on_scene_prop_hit,
    [   (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100), #sound is pretty loud, avoid hearingit from across the map
        (prop_instance_get_variation_id, ":var1", ":instance_no"),
        (try_begin),
            (ge, ":var1", 1),
            (store_mul, ":sound_dist", ":var1", 100),
        (else_try),
            (assign, ":sound_dist", 1500),
        (try_end),
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos4, ":player_agent"),
        (get_distance_between_positions, ":distance", pos1, pos4),
        # (assign, reg66, ":distance"),
        # (display_message, "@distance: {reg66}"),
        (le, ":distance", ":sound_dist"),
        (play_sound, "snd_dummy_hit"),
        (particle_system_burst, "psys_dummy_smoke", pos1, 2),
        (particle_system_burst, "psys_dummy_straw", pos1, 10),
    ])
    ] or []) + [    
    ]),
    
("troop_work_tree_feller",0,"wood_a","bo_wood_a_bigger",   [
  ] + (is_a_wb_sceneprop==1 and [
        (ti_on_init_scene_prop,[
        (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100),
        (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
        (prop_instance_get_position, pos1, ":instance_no"), 
        (copy_position, pos2, pos1),
        (position_move_y, pos2, -160,0),(set_spawn_position, pos2),
        (store_random_in_range, ":walker_type", 0, 2), #only use first two town walkers, make sure they're not "rich" walkers
        (val_add, ":walker_type", slot_center_walker_0_troop),
        (party_get_slot, ":troop", "$current_town", ":walker_type"),
        (spawn_agent, ":troop"),
        (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
        (try_for_range, ":weapon_slot", 0, 5), #remove weapons and helms
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (neg|item_has_property, ":item", itp_civilian),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),  
        (agent_set_no_dynamics, reg0, 1),  
        (agent_equip_item, reg0, "itm_civilian_woodaxe_2h", 1),
        (agent_set_wielded_item, reg0, "itm_civilian_woodaxe_2h"),
        (agent_set_look_target_position, reg0, pos2),
        (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk
        ]),
        
   (ti_on_scene_prop_hit,
    [   (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100), #sound is pretty loud, avoid hearingit from across the map
        (prop_instance_get_variation_id, ":var1", ":instance_no"),
        (try_begin),
            (ge, ":var1", 1),
            (store_mul, ":sound_dist", ":var1", 100),
        (else_try),
            (assign, ":sound_dist", 1500),
        (try_end),
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos4, ":player_agent"),
        (get_distance_between_positions, ":distance", pos1, pos4),
        # (assign, reg66, ":distance"),
        # (display_message, "@distance: {reg66}"),
        (le, ":distance", ":sound_dist"),
        (play_sound, "snd_dummy_hit"),
        (particle_system_burst, "psys_dummy_smoke", pos1, 2),
        (particle_system_burst, "psys_dummy_straw", pos1, 10),
    ])
        ] or []) + [ 
    ]),  
    
("troop_work_miner",0,"PW_rock_a","bo_PW_rock_a",   [
  ] + (is_a_wb_sceneprop==1 and [  
    (ti_on_init_scene_prop,[
        (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100),
        (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
        (prop_instance_get_position, pos1, ":instance_no"),
        (copy_position, pos2, pos1),
        (position_move_y, pos2, -150,0),(set_spawn_position, pos2),
        (store_random_in_range, ":walker_type", 0, 2), #only use first two town walkers, make sure they're not "rich" walkers       
        (val_add, ":walker_type", slot_center_walker_0_troop),
        (party_get_slot, ":troop", "$current_town", ":walker_type"),
        (spawn_agent, ":troop"),  
        (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
        (try_for_range, ":weapon_slot", 0, 5), #remove weapons and helms
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (neg|item_has_property, ":item", itp_civilian),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),  
        (agent_set_no_dynamics, reg0, 1),  
        (agent_equip_item, reg0, "itm_civilian_pickaxe", 1),
        (agent_set_wielded_item, reg0, "itm_civilian_pickaxe"),
        (agent_set_look_target_position, reg0, pos2),
        (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk
        ]), 
    
   (ti_on_scene_prop_hit,
    [   (play_sound, "snd_footstep_horse_1b"), 
        #(play_sound, "snd_jump_end"),
        (particle_system_burst, "psys_dummy_smoke", pos1, 3),
        #(particle_system_burst, "psys_dummy_straw", pos1, 10),
    ])
    ] or []) + [     
    ]),  

("troop_smith",0,"prop_smith","bo_prop_smith",   [
  ] + (is_a_wb_sceneprop==1 and [ 
    (ti_on_init_scene_prop,[
        (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100),
        (lt, "$g_encountered_party_2", 0), 
        (prop_instance_get_position, pos1, ":instance_no"), 
        
        #spawn smith
        (copy_position, pos2, pos1),
        (position_move_x, pos2, -100,0),(set_spawn_position, pos2),
        (store_faction_of_party, ":fac", "$current_town"),
        (faction_get_slot, ":troop", ":fac", slot_faction_tier_1_troop), #get a tier 1 troop so they don't wear heavy armour
        (spawn_agent, ":troop"),   
        (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
        (try_for_range, ":weapon_slot", 0, 5), #remove weapons and helms
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (neg|item_has_property, ":item", itp_civilian),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),  
        (agent_set_no_dynamics, reg0, 1),  
        (agent_equip_item, reg0, "itm_civilian_hammer", 1),
        (agent_set_wielded_item, reg0, "itm_civilian_hammer"),
        (agent_set_look_target_position, reg0, pos1),
        (agent_set_scripted_destination, reg0, pos2, 0, 1),
        (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk
        ]),
        
   (ti_on_scene_prop_hit,
    [   (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100), #sound is pretty loud, avoid hearingit from across the map
        (prop_instance_get_variation_id, ":var1", ":instance_no"),
        (try_begin),
            (ge, ":var1", 1),
            (store_mul, ":sound_dist", ":var1", 100),
        (else_try),
            (assign, ":sound_dist", 3500),
        (try_end),
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos4, ":player_agent"),
        (get_distance_between_positions, ":distance", pos1, pos4),
        # (assign, reg66, ":distance"),
        # (display_message, "@distance: {reg66}"),
        (le, ":distance", ":sound_dist"),
        (play_sound, "snd_sword_clash_1"),
        (particle_system_burst, "psys_fire_glow_1", pos1, 3),
        (particle_system_burst, "psys_torch_fire_sparks", pos1, 10),
    ])
    ] or []) + [      
    ]), 


("troop_smith_helper",sokf_invisible,"defend_twohanded_WB_frame","bo_defend_twohanded_WB_frame", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),
    (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
    (store_faction_of_party, ":fac", "$current_town"),
    (faction_get_slot, ":troop", ":fac", slot_faction_tier_1_troop), #get a tier 1 troop so they don't wear heavy armour
    (prop_instance_get_position, pos3, ":instance_no"), (set_spawn_position, pos1),
    # (position_move_y, pos3, 30,0),
    # (position_move_x, pos3, 30,0),
    # (position_rotate_z, pos3, 120),
    (set_spawn_position, pos3),
    #(party_get_slot, ":troop", "$current_town", slot_town_guard_troop),        
    (spawn_agent, ":troop"),  
    (agent_set_animation, reg0, "anim_defend_forward_greatsword_keep"), 
    (agent_set_stand_animation, reg0, "anim_defend_forward_greatsword_keep"), 
    ] + (is_a_wb_sceneprop==1 and [         
    #(scene_prop_set_slot, ":instance_no", 99, reg0), #just a random slot for this single scene prop
    (try_for_range, ":weapon_slot", 0, 5), #remove weapons and helms
        (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
        (gt, ":item", 1),
        (neg|item_has_property, ":item", itp_civilian),
        (agent_unequip_item, reg0, ":item", ":weapon_slot"),
    (try_end),
    (agent_set_no_dynamics, reg0, 1),
    (agent_set_position, reg0, pos3),
    #(agent_set_scripted_destination, reg0, pos3, 0, 1),
    (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk
    ] or []) + [   
    ])]),

("troop_work_hammer",0,"prop_hammerer","bo_prop_hammerer",   [
    ] + (is_a_wb_sceneprop==1 and [ 
    (ti_on_init_scene_prop,[
        (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100),
        (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
        (prop_instance_get_position, pos1, ":instance_no"),
        (copy_position, pos2, pos1),
        (position_move_y, pos2, -90,0),(set_spawn_position, pos2),
        (store_random_in_range, ":walker_type", 0, 2), #only use first two town walkers, make sure they're not "rich" walkers
        (val_add, ":walker_type", slot_center_walker_0_troop),
        (party_get_slot, ":troop", "$current_town", ":walker_type"),
        (spawn_agent, ":troop"),          
        (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
        (try_for_range, ":weapon_slot", 0, 5), #remove weapons and helms
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (neg|item_has_property, ":item", itp_civilian),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),  
        (agent_set_no_dynamics, reg0, 1),  
        (agent_equip_item, reg0, "itm_civilian_hammer", 1),
        (agent_set_wielded_item, reg0, "itm_civilian_hammer"),
        (agent_set_look_target_position, reg0, pos1),
        (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk
        ]),
        
   (ti_on_scene_prop_hit,
    [   (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100), #sound is pretty loud, avoid hearingit from across the map
        (prop_instance_get_variation_id, ":var1", ":instance_no"),
        (try_begin),
            (ge, ":var1", 1),
            (store_mul, ":sound_dist", ":var1", 100),
        (else_try),
            (assign, ":sound_dist", 1500),
        (try_end),
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos4, ":player_agent"),
        (get_distance_between_positions, ":distance", pos1, pos4),
        # (assign, reg66, ":distance"),
        # (display_message, "@distance: {reg66}"),
        (le, ":distance", ":sound_dist"),
        (play_sound, "snd_shield_hit_metal_wood"),
        (particle_system_burst, "psys_dummy_smoke", pos1, 1),
        #(particle_system_burst, "psys_dummy_straw", pos1, 10),
    ])
    ] or []) + [
    ]),

("troop_work_farmer_mattock",0,"earth_heap","bo_earth_heap",   [
  ] + (is_a_wb_sceneprop==1 and [
    (ti_on_init_scene_prop,[
        (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100),
        (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
        (prop_instance_get_position, pos1, ":instance_no"), 
        (copy_position, pos2, pos1),
        (position_move_y, pos2, -100,0),(set_spawn_position, pos2),
        (store_random_in_range, ":walker_type", 0, 2), #only use first two town walkers, make sure they're not "rich" walkers
        (val_add, ":walker_type", slot_center_walker_0_troop),
        (party_get_slot, ":troop", "$current_town", ":walker_type"),
        (spawn_agent, ":troop"),
        (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
        (try_for_range, ":weapon_slot", 0, 5), #remove weapons and helms
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (neg|item_has_property, ":item", itp_civilian),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),  
        (agent_set_no_dynamics, reg0, 1),  
        (store_random_in_range, ":item_to_equip", 0, 3),
        (val_add, ":item_to_equip", itm_civilian_war_mattock),
        (agent_equip_item, reg0, ":item_to_equip", 1),
        (agent_set_wielded_item, reg0, ":item_to_equip"),
        (agent_set_look_target_position, reg0, pos1),
        (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk
        ]),
        
   (ti_on_scene_prop_hit,
    [   (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100), #sound is pretty loud, avoid hearingit from across the map
        (prop_instance_get_variation_id, ":var1", ":instance_no"),
        (try_begin),
            (ge, ":var1", 1),
            (store_mul, ":sound_dist", ":var1", 100),
        (else_try),
            (assign, ":sound_dist", 1500),
        (try_end),
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos4, ":player_agent"),
        (get_distance_between_positions, ":distance", pos1, pos4),
        # (assign, reg66, ":distance"),
        # (display_message, "@distance: {reg66}"),
        (le, ":distance", ":sound_dist"),
        (play_sound, "snd_wooden_hit_high_armor_low_damage"),
        (particle_system_burst, "psys_dummy_smoke", pos1, 3),
        (particle_system_burst, "psys_dummy_straw", pos1, 10),
    ])
    ] or []) + [
    ]),

#doesn't work so good, somehow the agent often doesn't aim at the target prop
("troop_work_farmer_shovel",0,"earth_heap","bo_earth_heap",   [
  ] + (is_a_wb_sceneprop==1 and [
    (ti_on_init_scene_prop,[
        (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100),
        (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
        (prop_instance_get_position, pos1, ":instance_no"), 
        (copy_position, pos2, pos1),
        (position_move_y, pos2, -120,0),(set_spawn_position, pos2),
        (store_random_in_range, ":walker_type", 0, 2), #only use first two town walkers, make sure they're not "rich" walkers
        (val_add, ":walker_type", slot_center_walker_0_troop),
        (party_get_slot, ":troop", "$current_town", ":walker_type"),
        (spawn_agent, ":troop"),
        (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
        (try_for_range, ":weapon_slot", 0, 5), #remove weapons and helms
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (neg|item_has_property, ":item", itp_civilian),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),  
        #(agent_set_no_dynamics, reg0, 1),  
        (agent_equip_item, reg0, "itm_civilian_shovel", 1),
        (agent_set_wielded_item, reg0, "itm_civilian_shovel"),
        (agent_set_look_target_position, reg0, pos1),
        (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk
        ]),
        
   (ti_on_scene_prop_hit,
    [   (set_fixed_point_multiplier, 100), #sound is pretty loud, avoid hearingit from across the map
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos4, ":player_agent"),
        (get_distance_between_positions, ":distance", pos1, pos4),
        (le, ":distance", 1500), #15m
        #(play_sound, "snd_wooden_hit_high_armor_low_damage"), #no sound needed
        (particle_system_burst, "psys_dummy_smoke", pos1, 3),
        (particle_system_burst, "psys_dummy_straw", pos1, 10),
    ])
    ] or []) + [ 
    ]),

("troop_work_butcher",0,"raw_meat","bo_wood_a_bigger",   [
  ] + (is_a_wb_sceneprop==1 and [
    (ti_on_init_scene_prop,[
        (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100),
        (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
        (prop_instance_get_position, pos1, ":instance_no"), 
        (copy_position, pos2, pos1),
        (position_move_x, pos2, -95,0),(set_spawn_position, pos2),
        (store_random_in_range, ":walker_type", 0, 2), #only use first two town walkers, make sure they're not "rich" walkers
        (val_add, ":walker_type", slot_center_walker_0_troop),
        (party_get_slot, ":troop", "$current_town", ":walker_type"),
        (spawn_agent, ":troop"), 
        (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
        (try_for_range, ":weapon_slot", 0, 5), #remove weapons and helms
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (neg|item_has_property, ":item", itp_civilian),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),
        (agent_set_no_dynamics, reg0, 1),  
        (agent_equip_item, reg0, "itm_orc_axe", 1),
        (agent_set_wielded_item, reg0, "itm_orc_axe"),
        (agent_set_look_target_position, reg0, pos2),
        (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk
         ]),
        
   (ti_on_scene_prop_hit,
    [   (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100), #sound is pretty loud, avoid hearingit from across the map
        (prop_instance_get_variation_id, ":var1", ":instance_no"),
        (try_begin),
            (ge, ":var1", 1),
            (store_mul, ":sound_dist", ":var1", 100),
        (else_try),
            (assign, ":sound_dist", 500),
        (try_end),
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos4, ":player_agent"),
        (get_distance_between_positions, ":distance", pos1, pos4),
        # (assign, reg66, ":distance"),
        # (display_message, "@distance: {reg66}"),
        (le, ":distance", ":sound_dist"),
        (play_sound, "snd_wooden_hit_high_armor_low_damage", sf_vol_1),
        (particle_system_burst, "psys_game_blood_rand_2", pos1, 100),
        #(particle_system_burst, "psys_dummy_smoke", pos1, 1),
    ])
    ] or []) + [
    ]),

("troop_work_stand",sokf_invisible,"arrow_helper_blue","0",   [
    (ti_on_init_scene_prop,[
        (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100),
        (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
        (prop_instance_get_position, pos1, ":instance_no"),
        (set_spawn_position, pos1),
        (store_random_in_range, ":walker_type", 0, 2), #only use first two town walkers, make sure they're not "rich" walkers
        (val_add, ":walker_type", slot_center_walker_0_troop),
        (party_get_slot, ":troop", "$current_town", ":walker_type"),
        (spawn_agent, ":troop"),
        ] + (is_a_wb_sceneprop==1 and [           
        (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
        (try_for_range, ":weapon_slot", 0, 5), #remove weapons and helms
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (neg|item_has_property, ":item", itp_civilian),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),  
        (agent_set_no_dynamics, reg0, 1),  
        (agent_set_position, reg0, pos1),
        (agent_set_scripted_destination, reg0, pos1), #so they turn back
        #(agent_set_look_target_position, reg0, pos1),
        (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk
        ] or []) + [          ]),
        ]),

("troop_work_table",sokf_invisible,"arrow_helper_blue","0",   [
    (ti_on_init_scene_prop,[
        (store_trigger_param_1, ":instance_no"),
        (set_fixed_point_multiplier, 100),
        (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
        (prop_instance_get_position, pos1, ":instance_no"),
        (copy_position, pos2, pos1),
        (position_move_y, pos2, -40,0),(set_spawn_position, pos2),
        (store_random_in_range, ":walker_type", 0, 2), #only use first two town walkers, make sure they're not "rich" walkers
        (val_add, ":walker_type", slot_center_walker_0_troop),
        (party_get_slot, ":troop", "$current_town", ":walker_type"),
        (spawn_agent, ":troop"),
        ] + (is_a_wb_sceneprop==1 and [           
        (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
        (try_for_range, ":weapon_slot", 0, 5), #remove weapons and helms
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (neg|item_has_property, ":item", itp_civilian),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),  
        (agent_set_no_dynamics, reg0, 1),  
        #(agent_set_position, reg0, pos2),
        (agent_set_scripted_destination, reg0, pos2), #so they turn back
        (agent_set_look_target_position, reg0, pos1),
        (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk
        ] or []) + [          ]),
        ]),

("troop_human_prisoner_oh_no",sokf_invisible,"arrow_helper_blue","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
    (spawn_agent, "trp_human_prisoner"),(agent_set_team, reg0, 0), 
    (agent_set_animation, reg0, "anim_nazgul_noooo_short"),
  ] + (is_a_wb_sceneprop==1 and [(scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0), ] or []) + [      
    ])]),

("troop_civ_cheer",sokf_invisible,"arrow_helper_blue","0", [(ti_on_init_scene_prop,[												 
    (store_trigger_param_1, ":instance_no"),
    (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
	(store_random_in_range, ":slot", 0, 4),
    (val_add, ":slot", slot_center_walker_0_troop),
    (party_get_slot, ":troop", "$current_town", ":slot"),
    (spawn_agent, ":troop"),(agent_set_team, reg0, 0),(store_random_in_range, reg6, 0, 100),(agent_set_animation_progress, reg0, reg6),

    #remove weapons and helms
  ] + (is_a_wb_sceneprop==1 and [   
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),  
        (try_for_range, ":weapon_slot", 0, 4), 
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),
    ] or []) + [  
 
  ])]),

("troop_priest",sokf_invisible,"arrow_helper_blue","0", [(ti_on_init_scene_prop,[												 
    (store_trigger_param_1, ":instance_no"),
    (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
    (spawn_agent, "trp_evil_priest"),(agent_set_team, reg0, 0),(store_random_in_range, reg6, 0, 100),(agent_set_animation_progress, reg0, reg6),
    (agent_set_slot, reg0, slot_agent_walker_type, 5), #don't talk

    #remove weapons and helms (for old savegames)
  ] + (is_a_wb_sceneprop==1 and [  
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),  
        (agent_set_is_alarmed, reg0, 1),
        (try_for_range, ":weapon_slot", 0, 9), 
            (agent_get_item_slot, ":item", reg0, ":weapon_slot"),
            (gt, ":item", 1),
            (agent_unequip_item, reg0, ":item", ":weapon_slot"),
        (try_end),
        (agent_equip_item, reg0, "itm_nazgul_robe_wb", ek_body),
        (agent_equip_item, reg0, "itm_hood_black", ek_head),
        (agent_equip_item, reg0, "itm_leather_boots_dark", ek_foot),            
    ] or []) + [  
 
  ])]),

# var1 x 100 + var2 is sound_no; (scale_x -1) x 100 is range in metres
# only really works for looping sounds
("sound_emitter_var1x10_plus_var2_scalable" ,sokf_invisible,"collision_cube","0", [(ti_on_init_scene_prop,[												 
    (store_trigger_param_1, ":instance_no"),
    (set_fixed_point_multiplier, 10000),
    (prop_instance_get_scale, pos2, ":instance_no"),
    (position_get_scale_x, ":scale_x", pos2),
    (eq, ":scale_x", 10000), #only show tutorial message if scale is unchanged
    (display_message, "@{!} debug: sound emitter: var1 x 10 + var2 is sound_no; first two digits after comma in scale x is range in metres"),
    (display_message, "@{!} debug: scale prop to disable this message"),
  ])]),

# var1 x 100 + var2 is sound_no; (scale_x -1) x 100 is range in metres
# only really works for looping sounds
("sound_emitter_ambient_var1x10_plus_var2_scalable" ,sokf_invisible,"collision_cube","0", [(ti_on_init_scene_prop,[												 
    (store_trigger_param_1, ":instance_no"),
    (set_fixed_point_multiplier, 10000),
    (prop_instance_get_scale, pos2, ":instance_no"),
    (position_get_scale_x, ":scale_x", pos2),
    (eq, ":scale_x", 10000), #only show tutorial message if scale is unchanged
    (display_message, "@{!} debug: sound emitter: var1 x 10 + var2 is sound_no; first two digits after comma in scale x is range in metres"),
    (display_message, "@{!} debug: ambient sound emitter: stops all looping sounds, sets a new ambient sound while in range"),
    (display_message, "@{!} debug: scale prop to disable this message"),
  ])]),

# var1 x 100 + var2 is sound_no;
# works for single sounds, but only checks every 3 seconds (=fastest interval)
("sound_emitter_occasional_var1x10_plus_var2_scalable" ,sokf_invisible,"collision_cube","0", [(ti_on_init_scene_prop,[												 
    (store_trigger_param_1, ":instance_no"),
    (set_fixed_point_multiplier, 10000),
    (prop_instance_get_scale, pos2, ":instance_no"),
    (position_get_scale_x, ":scale_x", pos2),
    (eq, ":scale_x", 10000), #only show tutorial message if scale is unchanged
    (display_message, "@{!} sound emitter: var1 x 10 + var2 is sound_no; scale x is chance per 3 seconds"),
    (display_message, "@{!} suggestions: 247 = moria_ambiance; 207 = horror_scream_man; 13 = sword_clash_1"),
    (display_message, "@{!} scale prop to disable this message"),
  ])]),

#("sound_fire_big_scalable" ,sokf_invisible,"collision_cube","0", []),
("sound_fire_big"       ,sokf_invisible,"collision_cube","0", [(ti_on_init_scene_prop,[(set_position_delta,0,0,0),(play_sound, "snd_fire_loop", 0)])]),

("ai_melee_on_off_var1",sokf_invisible,"sphere_1m","0", []), #var 1 sets agent_ai_set_always_attack_in_melee

("secret_point_of_interest",sokf_invisible,"sphere_1m","0", [(ti_on_scene_prop_init,
    [(particle_system_add_new, "psys_moon_beam_1"),
    #(particle_system_add_new, "psys_moon_beam_paricle_1") #separate prop now
    ])]),
    
("secret_guardian",sokf_invisible,"arrow_helper_blue","0", [
    (ti_on_init_scene_prop,[
    ] + (is_a_wb_sceneprop==1 and [     
    (lt, "$g_encountered_party_2", 0), #don't spawn guards in siege battles												 
    (store_trigger_param_1, ":instance_no"),
    (prop_instance_get_variation_id_2, ":var2", ":instance_no"),
    (try_begin),
        (gt, ":var2", 1),
        (assign, ":troop", ":var2"),
    (else_try),
        (party_get_slot, ":troop", "$current_town", slot_town_castle_guard_troop),
    (try_end),
    (prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),  (spawn_agent, ":troop"),
    (assign, ":agent", reg0),
    (try_begin), #remove horse
        (agent_get_horse, ":horse", reg0),
        (gt, ":horse", 0),
        (remove_agent, ":horse"),
        (agent_set_visibility, ":horse", 0),
    (try_end),
    
    (agent_set_team, ":agent", 0),(agent_set_stand_animation, ":agent", "anim_stand"),
    (store_random_in_range, reg6, 0, 100),(agent_set_animation_progress, ":agent", reg6),
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, ":agent"),
    (agent_set_slot, ":agent", slot_agent_secret_guardian, 1),

    #tutorial
    (set_fixed_point_multiplier, 10000),
    (prop_instance_get_scale, pos1, ":instance_no"), 
    (position_get_scale_z, ":scale", pos1),
    (try_begin),
        (eq, ":scale", 10000), #only show tutorial message if scale is unchanged
        (is_edit_mode_enabled),
        (display_message, "@{!} debug: var1 = check number for script; var2 = rank requirement"),
        (display_message, "@{!} debug: scale prop to disable this message"),
    (try_end),
    ] or []) + [  
 
  ])]),

("rock_bridge",0,"rock_bridge_tld","bo_rock_bridge_tld", []),
("basket_grain",0,"basket_grain","bo_apple_basket",[]),
("basket_coal",0,"basket_coal","bo_apple_basket",[]),
("basket_earth",0,"basket_earth","bo_apple_basket",[]),
("basket_cloth",0,"basket_cloth","bo_apple_basket",[]),

("animal_dog",sokf_invisible,"wolf_dog","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
    ] + (is_a_wb_sceneprop==1 and [ 
	(spawn_horse,"itm_animal_dog", imod_chipped),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, "anim_horse_rear"), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, "anim_wolf_snap"), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, "snd_distant_dog_bark"), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, "snd_warg_lone_woof"), #sound 2
    ] or []) + [          
    ])]),

("animal_pig",sokf_invisible,"pk_pig","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),

    ] + (is_a_wb_sceneprop==1 and [ 												 
	(spawn_horse,"itm_animal_small", imod_battered),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, 0), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, "anim_wolf_snap"), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, snd_pig), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, 0), #sound 2
    ] or []) + [          
    ])]),

("animal_boar",sokf_invisible,"boar","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),

    ] + (is_a_wb_sceneprop==1 and [ 												 
	(spawn_horse,"itm_animal_boar", imod_battered),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, 0), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, "anim_wolf_snap"), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, snd_pig), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, 0), #sound 2
    ] or []) + [
    ])]),

("animal_boar_big",sokf_invisible,"boar","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),

    ] + (is_a_wb_sceneprop==1 and [ 												 
	(spawn_horse,"itm_animal_boar_big", imod_battered),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, 0), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, "anim_wolf_snap"), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, snd_bear_strike), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, snd_troll_grunt), #sound 2
    ] or []) + [
    ])]),

#from sclavinia mod
 ("animal_chicken",0,"scla_kura_combine",0,   [
    ] + (is_a_wb_sceneprop==1 and [   
   (ti_on_scene_prop_init,
    [(store_trigger_param_1, ":instance_no"),
    (store_random_in_range, ":random", 0, 220),  
    (prop_instance_deform_to_time, ":instance_no", ":random"),
    (store_random_in_range, ":random", 4000, 8000),
    (prop_instance_deform_in_cycle_loop, ":instance_no", 0, 220, ":random"),
    ])
    ] or []) + [    
    ]),


("animal_pony",sokf_invisible,"CWE_horse_light_a","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),

    ] + (is_a_wb_sceneprop==1 and [ 
	(store_random_in_range, ":animal_var", imod_cracked, imod_bent+1),														 
	(spawn_horse,"itm_animal_pony", ":animal_var"),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, 0), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, 0), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, snd_horse_breath), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, snd_neigh1), #sound 2
    ] or []) + [
    ])]),

("animal_deer",sokf_invisible,"scla_reddeer","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),

    ] + (is_a_wb_sceneprop==1 and [ 													 
	(spawn_horse,"itm_animal_deer", 0),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, "anim_wolf_snap"), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, 0), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, snd_horse_breath), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, 0), #sound 2
    ] or []) + [
    ])]),

("animal_camel",sokf_invisible,"giles_evil_camel_brown","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),

    ] + (is_a_wb_sceneprop==1 and [ 													 
	(spawn_horse,"itm_animal_camel", 0),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, 0), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, 0), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, 0), #sound 1
    (agent_set_slot, reg0, slot_agent_last_hp, 0), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, snd_camel_sounds), #sound 2
    ] or []) + [
    ])]),

("animal_rat",0,"earth_heap","0", [(ti_on_init_scene_prop,[
    ] + (is_a_wb_sceneprop==1 and [
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),    
    (scene_prop_set_slot, ":instance_no", slot_prop_playing_sound, itm_animal_rat),
    ] or []) + [
    ])]),

("animal_warg",sokf_invisible,"warg_1B","0", [(ti_on_init_scene_prop,[
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
    ] + (is_a_wb_sceneprop==1 and [ 
	(store_random_in_range, ":animal_var", imod_cracked, imod_bent+1),														 
	(spawn_horse,"itm_animal_warg", ":animal_var"),
    (agent_set_stand_animation, reg0, "anim_horse_stand"),    
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    (agent_set_slot, reg0, slot_agent_assigned_prop, ":instance_no"),
    (agent_set_slot, reg0, slot_agent_troll_swing_status, "anim_bear_slam"), #animation 1   
    (agent_set_slot, reg0, slot_agent_troll_swing_move, "anim_wolf_snap"), #animation 2
    (agent_set_slot, reg0, slot_agent_last_hp, "snd_warg_lone_woof"), #sound 1
    (agent_set_slot, reg0, slot_agent_mount_side, "snd_warg_lone_woof"), #sound 2
    (agent_set_slot, reg0, slot_agent_mount_dead, 15), #chance to move per second, minimum 5%
    ] or []) + [          
    ])]),
            
] + (is_a_wb_sceneprop==1 and [ 
  ("fellbeast", sokf_moveable|sokf_destructible, "fellbeast_anim", "bo_Fellbeast_Full", [
    (ti_on_scene_prop_init,[
      (store_trigger_param_1, ":instance_no"),
      (store_random_in_range, ":var3", 0, 16),
      (prop_instance_deform_to_time, ":instance_no", ":var3"),      
      (val_mul, ":var3", 200),
      (scene_prop_set_slot, ":instance_no", 39, ":var3"), #height offset
      (scene_prop_set_slot, ":instance_no", 43, 11), #dead frame
      (scene_prop_set_slot, ":instance_no", 41, 0), #circling mode
      (scene_prop_set_slot, ":instance_no", 42, -1), #target agent
      (prop_instance_deform_in_cycle_loop, ":instance_no", 0, 49, 2000),
      (scene_prop_set_slot, ":instance_no", slot_prop_temp_hp_1, 4),
      (scene_prop_set_slot, ":instance_no", slot_prop_temp_hp_2, 3),
      (assign, "$nazgul_in_battle", ":instance_no"),
    ]),
    (ti_on_scene_prop_hit,
    [   (store_trigger_param_1, ":instance_no"),
        (store_trigger_param_2, ":damage"),
        (store_trigger_param, ":dealer", 3),
        (store_trigger_param, ":weapon", 4),
        (get_player_agent_no, ":player_agent"),
        
        # (assign, reg78, ":damage"),
        # (display_message, "@damage: {reg78}!"),
        #(scene_prop_slot_eq, ":instance_no", 41, 2), #in attack mode?
        (scene_prop_get_slot, ":health", ":instance_no", slot_prop_temp_hp_1),
        (val_sub, ":health", ":damage"),
        (scene_prop_set_slot, ":instance_no", slot_prop_temp_hp_1, ":health"),
        (scene_prop_get_slot, ":health2", ":instance_no", slot_prop_temp_hp_2),
        (val_sub, ":health2", ":damage"),
        (scene_prop_set_slot, ":instance_no", slot_prop_temp_hp_2, ":health2"),        
        (particle_system_burst, "psys_dummy_smoke", pos1, 3),
        (particle_system_burst, "psys_dummy_straw", pos1, 10),
        
        # (assign, reg78, ":health"),
        # (display_message, "@health: {reg78}!"),
        # (assign, reg78, ":health2"),
        # (display_message, "@health2: {reg78}!"),
        (lt, ":health", 1),
        (prop_instance_play_sound, ":instance_no", "snd_nazgul_skreech_long" ),
        #(display_message, "@hit!"),
        (scene_prop_set_slot, ":instance_no", 41, 4), #retreat
        (prop_instance_get_position, pos2, ":instance_no"),
        (position_get_rotation_around_x, ":tilt", pos2), #reset x rotation
        (val_mul, ":tilt", -1),
        (position_rotate_x, pos2, ":tilt"),
        (position_move_y, pos2, 7000),
        (position_set_z_to_ground_level, pos2),
        (position_move_z, pos2, 5000, 1),
        (position_rotate_x, pos2, 45),
        (prop_instance_animate_to_position, ":instance_no", pos2, 300),
        (agent_get_position, pos69, ":dealer"),
        (try_for_agents, ":agent", pos69, 2000), #morale effect
            (agent_get_team, ":agent_team", ":agent"),
            (teams_are_enemies, ":agent_team", "$nazgul_team"),
            (agent_get_slot, ":morale_bonus", ":agent", slot_agent_morale_modifier),
            (val_add, ":morale_bonus", 25),
            (agent_set_slot, ":agent", slot_agent_morale_modifier, ":morale_bonus"),
        (try_end),
        (try_begin),
            (eq, ":dealer", ":player_agent"),
            (add_xp_as_reward, 200),
            (item_get_type, ":item_type", ":weapon"),
            (try_begin),
                (eq, ":item_type", itp_type_bow),
                (troop_raise_proficiency_linear, trp_player, wpt_archery, 10),
            (else_try),
                (eq, ":item_type", itp_type_thrown),
                (troop_raise_proficiency_linear, trp_player, wpt_throwing, 10),
            (try_end),
        (try_end),
        #TODO: Add notifier, XP and proficiency bonus, temporary morale consequences
    ])    
    ], 10000),
       ] or [("fellbeast", 0, "beest", "0", []),]) + [  

("fallen_king_base",0,"FK_Base_combined","bo_apple_basket",[]),
("fallen_king_head",0,"FK_Head","bo_apple_basket",[]),
("fallen_king_evil_head",0,"FK_evil_head","bo_apple_basket",[]),

("water_stream_a",0,"water_stream_a","bo_water_stream_a", []),
("water_stream_b",0,"water_stream_b","bo_water_stream_b", []),
("water_way",0,"water_way","bo_isen_forge", []),
("barrel_water",0,"barrel_water","bo_barrel_a_repositioned", []),
("bridge_b",0,"bridge_b","bo_bridge_b", []),

("banner_stand_auto",0,"battle_banner_stand_a_auto","0", [(ti_on_init_scene_prop,[
    (party_get_slot, ":cur_leader", "$current_town", slot_town_lord),
    (troop_get_slot, ":troop_banner_object", ":cur_leader", slot_troop_banner_scene_prop),
    (gt, ":troop_banner_object", 0),
    (store_trigger_param_1, ":instance_no"),(prop_instance_get_position, pos1, ":instance_no"), (set_spawn_position, pos1),
    ] + (is_a_wb_sceneprop==1 and [ 
    (spawn_scene_prop, ":troop_banner_object"),
    (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, reg0),
    ] or []) + [
    ])]),

("secret_loot_prop",sokf_invisible|sokf_moveable|spr_use_time(2),"sphere_30cm","bo_sphere_30cm", [ 
    
    (ti_on_scene_prop_init,[ 
        (store_trigger_param_1, ":scene_prop"),
        (set_fixed_point_multiplier, 10000),
        (prop_instance_get_scale, pos1, ":scene_prop"),
        (store_mission_timer_a, ":time"),
        (try_begin),
            ] + (is_a_wb_sceneprop==1 and [ (is_edit_mode_enabled), ] or []) + [ 
            (gt, ":time", 5),
            (display_message, "@{!} debug: closest nearby scene item is given as reward; set var1 as item modifier"),
        (try_end),

        ] + (is_a_wb_sceneprop==1 and [
        (store_current_scene, ":cur_scene"),
        (prop_instance_get_position, pos2, ":scene_prop"),
        (try_for_range, ":count", 0, 10), #check which prop instance number, compare to slot number. 9 slots allow up to 9 secrets
            (scene_prop_get_instance, ":instance_no", "spr_secret_loot_prop", ":count"), 
            (eq, ":scene_prop", ":instance_no",),
            (store_add, ":loot_slot", slot_scene_loot_1, ":count"),
            (scene_slot_eq, ":cur_scene", ":loot_slot", 0), #0 = not looted; -1 = looted
            (scene_prop_set_slot, ":scene_prop", slot_prop_active, 1),
        (try_end),
        
        (assign, ":min_dist", 60),
        (try_for_prop_instances, ":scene_item", -1, somt_item),
            (scene_prop_slot_eq, ":scene_prop", slot_prop_active, 1),
            (prop_instance_get_position, pos1, ":scene_item"),
            (get_distance_between_positions, ":dist", pos1, pos2),
            (le, ":dist", ":min_dist"),
            (assign, ":min_dist", ":dist"),
            (prop_instance_get_scene_prop_kind, ":item_type", ":scene_item"),
            (scene_prop_set_slot, ":scene_prop", slot_prop_agent_1, ":item_type"),
            (scene_prop_set_slot, ":scene_prop", slot_prop_agent_2, ":scene_item"),
        (try_end),
        
        (try_begin),
            (is_edit_mode_enabled), 
            (is_between, ":item_type", 0, 980),
            (str_store_item_name, s9, ":item_type"),
            (display_message, "@{!} debug: secret item: {s9}"),
        (try_end),
        
        (store_random_in_range, ":timer", 70, 110),
        (prop_instance_animate_to_position, ":scene_prop", pos2, ":timer"), #using Dalion's animation workaround for better particle control
        ] or []) + [
    ]),   
         
    ] + (is_a_wb_sceneprop==1 and [
    (ti_on_scene_prop_animation_finished,[  #using Dalion's animation workaround for better particle control
        (store_trigger_param_1, ":scene_prop"),
        (scene_prop_slot_eq, ":scene_prop", slot_prop_active, 1),
        (prop_instance_get_position, pos2, ":scene_prop"),
        (particle_system_burst, "psys_fire_glow_1_white", pos2, 4),
        (store_random_in_range, ":timer", 70, 110),
        (prop_instance_animate_to_position, ":scene_prop", pos2, ":timer"),
    ]),         
    
    (ti_on_scene_prop_use,[
        (store_trigger_param_2, ":scene_prop"),
        (prop_instance_get_scale, pos1, ":scene_prop"), 
        (set_fixed_point_multiplier, 100),
        (scene_prop_enable_after_time, ":scene_prop", 99999),
        (store_current_scene, ":cur_scene"),
        (try_for_range, ":count", 0, 9), #check which prop instance number, compare to slot number. 9 slots allow up to 9 secrets
            (scene_prop_get_instance, ":instance_no", "spr_secret_loot_prop", ":count"), 
            (eq, ":scene_prop", ":instance_no",),
            (store_add, ":loot_slot", slot_scene_loot_1, ":count"),
            (scene_get_slot, ":loot", ":cur_scene", ":loot_slot"),
        (try_end),
        (try_begin), #looted already or slot disabled?
            (eq, ":loot", -1), 
            (display_message, "@Nothing of interest..."),
        (else_try), #free inventory capacity?
            (store_free_inventory_capacity, ":inventory", trp_player),
            (lt, ":inventory", 1),
            (assign, ":loot", -1), 
            (display_message, "@No inventory space..."),
        (try_end),

        (eq, ":loot", 0), #loot available? 
        #get item
        (scene_prop_get_slot, ":item_type", ":scene_prop", slot_prop_agent_1),
        (prop_instance_get_variation_id, ":modifier", ":scene_prop"),
        (try_begin), #backup
            (lt, ":item_type", 1),
            (assign, ":item_type", "itm_metal_scraps_bad"),
            (assign, ":modifier", 0),
        (try_end),
        
        #check conditions
        (party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
        (val_div, ":center_relation", 5), #center relation /5 adds one rank 
        (call_script, "script_get_faction_rank", "$ambient_faction"), 
        (val_add, ":center_relation", reg0),
        (item_get_abundance, ":rank_req", ":item_type"), #usually 90 to 100, but 100 equals 0
        (try_begin),
            (eq, ":rank_req", 100),
            (assign, ":rank_req", 90),
        (try_end),        
        (val_sub, ":rank_req", 91), #-1 to 9, with one rank discount
        (val_max, ":rank_req", 1), #1 to 9
        # (assign, reg78, ":rank_req"),
        # (display_message, "@rank req: {reg78}"),
        # (assign, reg78, ":center_relation"),
        # (display_message, "@center_relation: {reg78}"),
        
        (try_begin), #not a town visit? Just take it
            (store_relation, ":reln", "$g_encountered_party_faction", "fac_player_supporters_faction"),
            (this_or_next|lt, ":reln", 0),
            (neg|is_between, "$g_encountered_party", centers_begin, centers_end),
            (troop_add_item, trp_player, ":item_type", ":modifier"),
            (str_store_string, s9,"str_empty_string"),
            (scene_prop_get_slot, ":scene_item", ":scene_prop", slot_prop_agent_2),
            (gt, ":scene_item", 0),
            (scene_prop_fade_out, ":scene_item", 100),
        (else_try),
            (lt, ":center_relation", ":rank_req"), 
            (str_store_string, s9,"@We don't know you enough to give you this..."),
        (else_try),
            (ge, ":center_relation", ":rank_req"),  
            (troop_add_item, trp_player, ":item_type", ":modifier"),
            (try_begin),
                (faction_slot_eq, "$ambient_faction", slot_faction_side, faction_side_good),
                (str_store_string, s9,"@Take it, friend, it's yours."),
            (else_try),
                (str_store_string, s9,"@Take it, we don't need it anyway."),
            (try_end),
            (scene_prop_get_slot, ":scene_item", ":scene_prop", slot_prop_agent_2),
            (gt, ":scene_item", 0),
            (scene_prop_fade_out, ":scene_item", 100),
            (scene_set_slot, ":cur_scene", ":loot_slot", -1),
        (try_end),
        (display_message, "@{!}{s9}"),
        (scene_prop_set_slot, ":scene_prop", slot_prop_active, 0),
    ])
    ] or []) + [            
          ]),

] + (is_a_wb_sceneprop==1 and [ 
  ("secret_viewpoint", sokf_invisible|sokf_moveable|spr_use_time(1), "arrow_helper_blue", "bo_spike_a", [
    (ti_on_scene_prop_init,[
        (store_trigger_param_1, ":instance_no"),
        (prop_instance_deform_in_range, ":instance_no", 0, 100, 1000), #workaround for particle effect
        (set_fixed_point_multiplier, 10000),
        (prop_instance_get_scale, pos1, ":instance_no"), 
        (position_get_scale_z, ":scale", pos1),
        (try_begin),
            (eq, ":scale", 10000), #only show tutorial message if scale is unchanged
            (is_edit_mode_enabled),
            (display_message, "@{!} debug: scale y = radius // scale z = elevation"),
            (display_message, "@{!} debug: scale prop to disable this message"),
        (try_end),
    ]),

    (ti_scene_prop_deformation_finished,[ #workaround for particle effect
        (store_trigger_param_1, ":instance_no"),
        (scene_prop_slot_eq, ":instance_no", slot_prop_active, 0),
        (scene_prop_slot_eq, ":instance_no", slot_prop_playing_sound, 0),
        (prop_instance_get_position, pos2, ":instance_no"),
        (particle_system_burst, "psys_moon_beam_1", pos2, 4),
        (store_random_in_range, ":timer", 700, 1100),    
        (prop_instance_deform_in_range, ":instance_no", 0, 100, ":timer"), #workaround for particle effect
    ]),
    
    (ti_on_scene_prop_use,[
      (store_trigger_param_2, ":instance_no"),
      (get_player_agent_no, "$current_player_agent"),
      #(scene_prop_set_visibility, ":instance_no", 0),
      (set_fixed_point_multiplier, 100),
      (scene_prop_enable_after_time, ":instance_no", 10),
      (prop_instance_get_position, pos5, ":instance_no"),
      (prop_instance_get_scale, pos2, ":instance_no"),
      (position_get_scale_y, ":radius", pos2),
      (val_mul, ":radius", 10),
      (position_get_scale_z, ":elevation", pos2),
      (val_mul, ":elevation", 10),
      (val_sub, ":elevation", 1000),
      (store_div, ":tilt", ":elevation", -100), #camera tilts against elevation
      (position_rotate_z, pos5, 45), #starting rotation offset
      (position_move_y, pos5, ":radius"), #radius
      (position_move_z, pos5, ":elevation"),
      (position_rotate_z, pos5, 180), #look back
      (position_rotate_x, pos5, ":tilt"),
      (prop_instance_animate_to_position, ":instance_no", pos5, 160),
      (scene_prop_set_slot, ":instance_no", slot_prop_active, -1), #starting rotation
      (mission_cam_set_mode, 1, 0, 0),
      (agent_set_speed_modifier, "$current_player_agent", 0),
      (set_camera_in_first_person, 0), 
      (mission_cam_animate_to_position, pos5, 1700, 0),
      (call_script, "script_scene_viewpoint_effect", ":instance_no", 0),
      # (set_spawn_position, pos5),
      # (spawn_scene_prop, "spr_arrow_helper_blue"),
    ]),
    
    (ti_on_scene_prop_animation_finished,[
      (store_trigger_param_1, ":instance_no"),
      (set_fixed_point_multiplier, 100),
      (prop_instance_get_variation_id_2, ":time", ":instance_no"), #animation in seconds
      (try_begin),
        (eq, ":time", 0),
        (assign, ":time", 12), #default duration
      (try_end),
      (val_mul, ":time", 100),
      (val_div, ":time", 22), #time per 10° tick, need 23 ticks for full animation
      (prop_instance_get_starting_position, pos5, ":instance_no"),
      (prop_instance_get_scale, pos2, ":instance_no"),
      (position_get_scale_y, ":radius", pos2),
      (val_mul, ":radius", 10),
      (position_get_scale_z, ":elevation", pos2),
      (val_mul, ":elevation", 10),
      (val_sub, ":elevation", 1000),
      # (assign, reg78, ":elevation"),
      # (display_message, "@elevation: {reg78}"),      
      (store_div, ":tilt", ":elevation", -100),  #camera tilts against elevation
      # (assign, reg78, ":tilt"),
      # (display_message, "@tilt: {reg78}"),
      (scene_prop_get_slot, ":rotation", ":instance_no", slot_prop_active),
      (try_begin),
        (gt, ":rotation", -10),
        (call_script, "script_scene_viewpoint_effect", ":instance_no", 1),
      (try_end),
      (le, ":rotation", -1),
      (val_sub, ":rotation", 10), #counter-clockwise
      (position_rotate_z, pos5, 45), #starting rotation offset
      (position_rotate_z, pos5, ":rotation"),
      (position_move_y, pos5, ":radius"), #radius
      (position_move_z, pos5, ":elevation"),
      (position_rotate_z, pos5, 180), #look back
      (position_rotate_x, pos5, ":tilt"),
      (prop_instance_animate_to_position, ":instance_no", pos5, ":time"),      
      # (set_spawn_position, pos5),
      # (spawn_scene_prop, "spr_arrow_helper_blue"),
      # (position_get_z, reg78, pos5),
      # (display_message, "@camera height: {reg78}"),
      (mission_cam_animate_to_position, pos5, 600, 0),
      # (assign, reg78, ":rotation"),
      # (display_message, "@rotation: {reg78}"),
      (scene_prop_set_slot, ":instance_no", slot_prop_active, ":rotation"),
      (lt, ":rotation", -225), #don't go a full circle
      (scene_prop_set_slot, ":instance_no", slot_prop_active, 0),
      (prop_instance_get_starting_position, pos5, ":instance_no"),
      (prop_instance_stop_animating, ":instance_no"),
      (prop_instance_set_position, ":instance_no", pos5),
      (mission_cam_set_mode, 0, 1600, 0),
      (agent_set_speed_modifier, "$current_player_agent", "$tld_town_player_speed_multi"), #assuming we're not in battle
      (prop_instance_deform_in_range, ":instance_no", 0, 100, 100),
      (call_script, "script_scene_viewpoint_effect", ":instance_no", 2),
    ]),
    ]),
       ] or [("secret_viewpoint", sokf_invisible|sokf_moveable, "arrow_helper_blue", "bo_sphere_30cm", []),]) + [  

("door_metal_a",0,"door_metal_a","bo_door_left", []),
("door_metal_b",0,"door_metal_b","bo_door_left", []),

("arrow_helper_blue",0,"arrow_helper_blue","0", []),
("save_compartibility4",0,"0","0", []),
("save_compartibility5",0,"0","0", []),
("save_compartibility6",0,"0","0", []),
("save_compartibility7",0,"0","0", []),
("save_compartibility8",0,"0","0", []),
("save_compartibility9",0,"0","0", []),
("save_compartibility10",0,"0","0", []),
("save_compartibility11",0,"0","0", []),
("save_compartibility12",0,"0","0", []),
("save_compartibility13",0,"0","0", []),
("save_compartibility14",0,"0","0", []),
("save_compartibility15",0,"0","0", []),
("save_compartibility16",0,"0","0", []),
("save_compartibility17",0,"0","0", []),
("save_compartibility18",0,"0","0", []),
("save_compartibility19",0,"0","0", []),
("save_compartibility20",0,"0","0", []),

]
