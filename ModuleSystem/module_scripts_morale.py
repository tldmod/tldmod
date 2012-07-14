from header_common import *
from header_operations import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from ID_animations import *
from ID_troops import *
from ID_factions import *
from module_troops import *

morale_scripts = [


# MORALE SCRIPTS:
  #script_healthbars
    ("healthbars",
    [
	(assign,reg1,"$allies_coh_base"),
	(assign,reg2,"$enemies_coh"),
	(assign,reg3,"$new_kills"),
	(display_message,"@Your troops are at {reg1}% cohesion (+{reg3}% bonus), the enemy at {reg2}%!",0x6495ed),
     ]),

  #script_morale_check
    ("morale_check",
    [
            (try_begin),
              (lt,"$allies_coh",80),
              (store_random_in_range,":routed",1,101),
              (assign,":chance_ply",85),
              (val_sub,":chance_ply","$allies_coh"),
                (try_begin),            
                  (le,":routed",":chance_ply"),             
                  (display_message,"@Morale of your troops wavers!",color_bad_news),            
                  (call_script, "script_flee_allies"),
                (try_end),
            (try_end),

            (try_begin),
              (lt,"$enemies_coh",80),
              (store_random_in_range,":routed",1,101),
              (assign,":chance_ply",85),
              (val_sub,":chance_ply","$enemies_coh"),
                (try_begin),  
                  (le,":routed",":chance_ply"),             
                  (display_message,"@Morale of your enemies wavers!",color_good_news),            
                  (call_script, "script_flee_enemies"),
                (try_end),            
            (try_end),
     ]),

  #script_rout_check
    ("rout_check",
    [
(assign,":ally","$allies_coh"),
(assign,":enemy","$enemies_coh"),
(val_sub,":ally",":enemy"),

                (try_begin),
                   (ge,":ally",40),
                  (display_message,"@Your enemies flee in terror!",color_good_news),  
                  (call_script, "script_rout_enemies"),
                  (assign,"$airout",1),
               (try_end),

                (try_begin),
                   (le,":ally",-40),
                  (display_message,"@Your troops flee in terror!",color_bad_news),  
                  (call_script, "script_rout_allies"),
                  (assign,"$rout",1),
               (try_end),
     ]),

	 
	 
## script_flee
    ("flee_allies",
    [
(get_scene_boundaries, pos3, pos4),

(position_get_x,":xmin",pos3),
(position_get_y,":ymin",pos3),
(position_get_x,":xmax",pos4),
(position_get_y,":ymax",pos4),
	   
	   (val_div,":xmin",100),
	   (val_div,":xmax",100),
	   
(store_random_in_range,":xrout_point3",":xmin",":xmax"),
    (val_mul,":xrout_point3",100),
(store_random_in_range,":yrout_point3",":xmin",":xmax"),
	(val_mul,":yrout_point3",100),
(store_random_in_range,":xrout_point4",":xmin",":xmax"),
	(val_mul,":xrout_point4",100),
(store_random_in_range,":yrout_point4",":xmin",":xmax"),
	(val_mul,":yrout_point4",100),

	   (val_mul,":xmin",100),
	   (val_mul,":xmax",100),

(val_add,":xrout_point3",":xmin"),
(val_add,":xrout_point3",":xmin"),
(val_add,":xrout_point3",":xmin"),
(val_div,":xrout_point3",4),
(position_set_x,pos3,":xrout_point3"),
(val_add,":yrout_point3",":ymin"),
(val_add,":yrout_point3",":ymin"),
(val_add,":yrout_point3",":ymin"),
(val_div,":yrout_point3",4),
(position_set_y,pos3,":yrout_point3"),

(val_add,":xrout_point4",":xmax"),
(val_add,":xrout_point4",":xmax"),
(val_add,":xrout_point4",":xmax"),
(val_div,":xrout_point4",4),
(position_set_x,pos4,":xrout_point4"),
(val_add,":yrout_point4",":ymax"),
(val_add,":yrout_point4",":ymax"),
(val_add,":yrout_point4",":ymax"),
(val_div,":yrout_point4",4),
(position_set_y,pos4,":yrout_point4"),

		 
(store_skill_level,":leader","skl_leadership","trp_player"),
(try_for_agents,":agent"),
         (agent_is_alive,":agent"),
         (agent_is_human,":agent"),
         (agent_is_ally,":agent"),
         (store_agent_hit_points,":hitpoints",":agent",0),
		 (agent_get_troop_id,":troop_type", ":agent"),
		 (store_character_level, ":troop_level", ":troop_type"),
		 (val_div,":troop_level",10),
		 (val_add,":hitpoints",":troop_level"),		 
         (assign,":chance_ply",100),
         (val_sub,":chance_ply",":hitpoints"),
         (val_sub,":chance_ply",":leader"),
         (val_div,":chance_ply",2),
         (store_random_in_range,":routed",1,101),
              (try_begin),
                   (le,":routed",":chance_ply"),
#                  (display_message,"@One ally runs!"),  
                	 (agent_get_position,pos2,":agent"),
		 (position_move_z,pos2,200,0),
                         (agent_clear_scripted_mode,":agent"),
                         (agent_set_scripted_destination,":agent",pos4,1),
               (try_end),
(end_try),	
     ]),

    ("flee_enemies",
    [
(get_scene_boundaries, pos3, pos4),

(position_get_x,":xmin",pos3),
(position_get_y,":ymin",pos3),
(position_get_x,":xmax",pos4),
(position_get_y,":ymax",pos4),
	   
	   (val_div,":xmin",100),
	   (val_div,":xmax",100),
	   
(store_random_in_range,":xrout_point3",":xmin",":xmax"),
    (val_mul,":xrout_point3",100),
(store_random_in_range,":yrout_point3",":xmin",":xmax"),
	(val_mul,":yrout_point3",100),
(store_random_in_range,":xrout_point4",":xmin",":xmax"),
	(val_mul,":xrout_point4",100),
(store_random_in_range,":yrout_point4",":xmin",":xmax"),
	(val_mul,":yrout_point4",100),

	   (val_mul,":xmin",100),
	   (val_mul,":xmax",100),

(val_add,":xrout_point3",":xmin"),
(val_add,":xrout_point3",":xmin"),
(val_add,":xrout_point3",":xmin"),
(val_div,":xrout_point3",4),
(position_set_x,pos3,":xrout_point3"),
(val_add,":yrout_point3",":ymin"),
(val_add,":yrout_point3",":ymin"),
(val_add,":yrout_point3",":ymin"),
(val_div,":yrout_point3",4),
(position_set_y,pos3,":yrout_point3"),

(val_add,":xrout_point4",":xmax"),
(val_add,":xrout_point4",":xmax"),
(val_add,":xrout_point4",":xmax"),
(val_div,":xrout_point4",4),
(position_set_x,pos4,":xrout_point4"),
(val_add,":yrout_point4",":ymax"),
(val_add,":yrout_point4",":ymax"),
(val_add,":yrout_point4",":ymax"),
(val_div,":yrout_point4",4),
(position_set_y,pos4,":yrout_point4"),


(try_for_agents,":agent"),
         (agent_is_alive,":agent"),
         (agent_is_human,":agent"),
         (neg|agent_is_ally,":agent"),
         (store_agent_hit_points,":hitpoints",":agent",0),
		 (agent_get_troop_id,":troop_type", ":agent"),
		 (store_character_level, ":troop_level", ":troop_type"),
		 (val_div,":troop_level",10),
		 (val_add,":hitpoints",":troop_level"),		 
         (assign,":chance_ply",100),
         (val_sub,":chance_ply",":hitpoints"),
         (val_sub,":chance_ply",4),
         (val_div,":chance_ply",2),
         (store_random_in_range,":routed",1,101),
	 (try_begin),
                   (le,":routed",":chance_ply"),
#                  (display_message,"@One enemy runs!"),  
                	 (agent_get_position,pos2,":agent"),
		 (position_move_z,pos2,200,0),
                         (agent_clear_scripted_mode,":agent"),
                         (agent_set_scripted_destination,":agent",pos3,1),
               (try_end),
(end_try),	
     ]),

## script_rout
    ("rout_allies",
    [
(get_scene_boundaries, pos3, pos4),	

(position_get_x,":xmin",pos3),
(position_get_y,":ymin",pos3),
(position_get_x,":xmax",pos4),
(position_get_y,":ymax",pos4),
	   
	   (val_div,":xmin",100),
	   (val_div,":xmax",100),
	   
(store_random_in_range,":xrout_point3",":xmin",":xmax"),
    (val_mul,":xrout_point3",100),
(store_random_in_range,":yrout_point3",":xmin",":xmax"),
	(val_mul,":yrout_point3",100),
(store_random_in_range,":xrout_point4",":xmin",":xmax"),
	(val_mul,":xrout_point4",100),
(store_random_in_range,":yrout_point4",":xmin",":xmax"),
	(val_mul,":yrout_point4",100),

	   (val_mul,":xmin",100),
	   (val_mul,":xmax",100),

(val_add,":xrout_point3",":xmin"),
(val_add,":xrout_point3",":xmin"),
(val_add,":xrout_point3",":xmin"),
(val_div,":xrout_point3",4),
(position_set_x,pos3,":xrout_point3"),
(val_add,":yrout_point3",":ymin"),
(val_add,":yrout_point3",":ymin"),
(val_add,":yrout_point3",":ymin"),
(val_div,":yrout_point3",4),
(position_set_y,pos3,":yrout_point3"),

(val_add,":xrout_point4",":xmax"),
(val_add,":xrout_point4",":xmax"),
(val_add,":xrout_point4",":xmax"),
(val_div,":xrout_point4",4),
(position_set_x,pos4,":xrout_point4"),
(val_add,":yrout_point4",":ymax"),
(val_add,":yrout_point4",":ymax"),
(val_add,":yrout_point4",":ymax"),
(val_div,":yrout_point4",4),
(position_set_y,pos4,":yrout_point4"),


	 
(store_skill_level,":leader","skl_leadership","trp_player"),
(try_for_agents,":agent"),
         (agent_is_alive,":agent"),
         (agent_is_human,":agent"),
         (agent_is_ally,":agent"),
         (store_agent_hit_points,":hitpoints",":agent",0),
		 (agent_get_troop_id,":troop_type", ":agent"),
		 (store_character_level, ":troop_level", ":troop_type"),
		 (val_div,":troop_level",10),
         (val_div,":hitpoints",3),
         (assign,":chance_ply",100),
         (val_sub,":chance_ply",":hitpoints"),
         (val_sub,":chance_ply",":leader"),
         (val_sub,":chance_ply",":troop_level"),
         (store_random_in_range,":routed",1,101),
              (try_begin),
                   (le,":routed",":chance_ply"),
#                  (display_message,"@One ally runs!"),  
                	 (agent_get_position,pos2,":agent"),
		 (position_move_z,pos2,200,0),
                         (agent_clear_scripted_mode,":agent"),
                         (agent_set_scripted_destination,":agent",pos4,1),
               (try_end),
(end_try),	
     ]),

    ("rout_enemies",
    [
(get_scene_boundaries, pos3, pos4),

(position_get_x,":xmin",pos3),
(position_get_y,":ymin",pos3),
(position_get_x,":xmax",pos4),
(position_get_y,":ymax",pos4),
	   
	   (val_div,":xmin",100),
	   (val_div,":xmax",100),
	   
(store_random_in_range,":xrout_point3",":xmin",":xmax"),
    (val_mul,":xrout_point3",100),
(store_random_in_range,":yrout_point3",":xmin",":xmax"),
	(val_mul,":yrout_point3",100),
(store_random_in_range,":xrout_point4",":xmin",":xmax"),
	(val_mul,":xrout_point4",100),
(store_random_in_range,":yrout_point4",":xmin",":xmax"),
	(val_mul,":yrout_point4",100),

	   (val_mul,":xmin",100),
	   (val_mul,":xmax",100),

(val_add,":xrout_point3",":xmin"),
(val_add,":xrout_point3",":xmin"),
(val_add,":xrout_point3",":xmin"),
(val_div,":xrout_point3",4),
(position_set_x,pos3,":xrout_point3"),
(val_add,":yrout_point3",":ymin"),
(val_add,":yrout_point3",":ymin"),
(val_add,":yrout_point3",":ymin"),
(val_div,":yrout_point3",4),
(position_set_y,pos3,":yrout_point3"),

(val_add,":xrout_point4",":xmax"),
(val_add,":xrout_point4",":xmax"),
(val_add,":xrout_point4",":xmax"),
(val_div,":xrout_point4",4),
(position_set_x,pos4,":xrout_point4"),
(val_add,":yrout_point4",":ymax"),
(val_add,":yrout_point4",":ymax"),
(val_add,":yrout_point4",":ymax"),
(val_div,":yrout_point4",4),
(position_set_y,pos4,":yrout_point4"),


(try_for_agents,":agent"),
         (agent_is_alive,":agent"),
         (agent_is_human,":agent"),
         (neg|agent_is_ally,":agent"),
         (store_agent_hit_points,":hitpoints",":agent",0),
		 (agent_get_troop_id,":troop_type", ":agent"),
		 (store_character_level, ":troop_level", ":troop_type"),
		 (val_div,":troop_level",10),
         (val_div,":hitpoints",3),
         (assign,":chance_ply",100),
         (val_sub,":chance_ply",":hitpoints"),
         (val_sub,":chance_ply",3), ## AI's Leadership bonus
         (val_sub,":chance_ply",":troop_level"),
         (store_random_in_range,":routed",1,101),
	 (try_begin),
                   (le,":routed",":chance_ply"),
#                  (display_message,"@One enemy runs!"),  
                	 (agent_get_position,pos2,":agent"),
		 	 (position_move_z,pos2,200,0),
                         (agent_clear_scripted_mode,":agent"),
                         (agent_set_scripted_destination,":agent",pos3,1),
               (try_end),
(end_try),
    ]),  

  

  #script_coherence
    ("coherence",
    [
(get_scene_boundaries, pos3, pos4),		 
(assign,":num_allies",0),
(assign,":coh_allies",0),
(assign,":num_enemies",0),
(assign,":coh_enemies",0),
     (try_for_agents,":agent"),
         (agent_is_ally,":agent"),
         (agent_is_human,":agent"),
		 (store_agent_hit_points,":hitpoints",":agent",0),
		 (agent_get_troop_id,":troop_type", ":agent"),
		 (store_character_level, ":troop_level", ":troop_type"),
#		 (val_div,":troop_level",10),
		 (val_mul,":hitpoints",":troop_level"),
		 (val_add,":num_allies",":troop_level"),
         (val_add,":coh_allies",":hitpoints"),
      (else_try),
         (agent_is_human,":agent"),
		 (store_agent_hit_points,":hitpoints",":agent",0),
		 (agent_get_troop_id,":troop_type", ":agent"),
		 (store_character_level, ":troop_level", ":troop_type"),
#		 (val_div,":troop_level",10),
		 (val_mul,":hitpoints",":troop_level"),
		 (val_add,":num_enemies",":troop_level"),
         (val_add,":coh_enemies",":hitpoints"),
      (end_try),
(val_div,":coh_allies",":num_allies"),
(assign,"$allies_coh_base",":coh_allies"),
(assign,"$allies_coh","$allies_coh_base"),
(val_add,"$allies_coh","$new_kills"),
(val_div,":coh_enemies",":num_enemies"),
(assign,"$enemies_coh",":coh_enemies"),
     ]),  
]