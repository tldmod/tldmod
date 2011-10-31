from header_map_icons import *
from module_constants import *
from header_operations import *
from header_triggers import *
from ID_sounds import *

from module_map_icons_mapscribbler import *

####################################################################################################################
#  Each map icon record contains the following fields:
#  1) Map icon id: used for referencing map icons in other files.
#     The prefix icon_ is automatically added before each map icon id.
#  2) Map icon flags. See header_map icons.py for a list of available flags
#  3) Mesh name.
#  4) Scale. 
#  5) Sound.
#  6) Offset x position for the flag icon.
#  7) Offset y position for the flag icon.
#  8) Offset z position for the flag icon.
####################################################################################################################

banner_scale = 0.3
avatar_scale = 0.15
tld_scale = 0.5

map_icons = map_icons_scribbler + [

  ("player",0,"player", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("player_horseman",0,"player_horseman", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("generic_knight",0,"knight_a", avatar_scale, snd_gallop, 0.15, 0.173, 0),
#  ("vaegir_knight",0,"knight_b", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  #("flagbearer_a",0,"flagbearer_a", avatar_scale, snd_gallop, 0.15, 0.173, 0),
#  ("flagbearer_b",0,"flagbearer_b", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("peasant",0,"peasant_a", avatar_scale,snd_footstep_grass, 0.15, 0.173, 0),
  #("khergit",0,"khergit_horseman", avatar_scale,snd_gallop, 0.15, 0.173, 0),
  #("khergit_horseman_b",0,"khergit_horseman_b", avatar_scale,snd_gallop, 0.15, 0.173, 0),
  ("axeman",0,"bandit_a", avatar_scale,snd_footstep_grass, 0.15, 0.173, 0),
  #("woman",0,"woman_a", avatar_scale,snd_footstep_grass, 0.15, 0.173, 0),
  #("woman_b",0,"woman_b", avatar_scale,snd_footstep_grass, 0.15, 0.173, 0),
#TLD army icons begin
  ("brigand",0,"brigand", avatar_scale, snd_gallop, 0.15, 0.173, 0),

  # combined icons: used for HOSTS and WAR PARTIES 
  # ATTENTION: please keep them in the same order as factions! 
  ("knight_gondo_trot_x3",0,"knight_gondo_trot_x3", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("dwarf_x3",0,"dwarf_x3", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("knight_rohan_x3",0,"knight_rohan_x3", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("uruk_x4",0,"uruk_x4", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),  # moria
  ("wargrider_walk_x4",0,"wargrider_walk_x4", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("lorien_elf_b_x3",0,"lorien_elf_b_x3", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("rivendell_elf_x3",0,"rivendell_elf_x3", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("mirkwood_elf_x3",0,"mirkwood_elf_x3", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("generic_knight_x3",0,"generic_knight_x3", avatar_scale, snd_gallop, 0.15, 0.173, 0), # dale: TODO: better icon needed
  ("harad_horseman_x3",0,"harad_horseman_x3", avatar_scale,snd_gallop, 0.15, 0.173, 0),
  ("easterling_horseman_x3",0,"easterling_horseman_x3", avatar_scale, snd_gallop, 0.15, 0.173, 0), # rhur  TODO: better icon needed
  ("cataphract_x3",0,"cataphract_x3", avatar_scale, snd_gallop, 0.15, 0.173, 0), # easeterlings ( khand)
  ("umbar_corsair_x3",0,"umbar_corsair_x3", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("orc_tribal_x4",0,"orc_tribal_x4", avatar_scale,snd_footstep_grass, 0.15, 0.173, 0), # moria
  ("orc_x4",0,"orc_x4", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),  # guldur 
  ("theoden_x3",0,"theoden_x3", avatar_scale, snd_gallop, 0.15, 0.173, 0),  # gundabad (**ordeirng exception** -- will use tribal orc x4)
  ("dunlander_x3",0,"dunlander_x3", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("dunlander",0,"dunlander", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0), # beorn (**ordering exception**-- will use generic x3) , TODO: better icon needed
  # combined icons end
  
   # unused combined icons!
   
  #  ("uruk_x6",0,"uruk_x6", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  
  
  ("dunland_captain",0,"dunland_captain", avatar_scale, snd_gallop, 0.15, 0.173, 0),

  ("easterling_horseman",0,"easterling_horseman", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("cataphract",0,"cataphract", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("harad_horseman",0,"harad_horseman", avatar_scale,snd_gallop, 0.15, 0.173, 0),
  ("isengard_captain",0,"isengard_captain", avatar_scale,snd_gallop, 0.15, 0.173, 0),
  
  ("umbar_captain",0,"umbar_captain", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("umbar_corsair",0,"umbar_corsair", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
 
  ("footman_gondor",0,"footman_gondor", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("footman_lamedon",0,"footman_lamedon", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("footman_pinnath",0,"footman_pinnath", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("lossarnach_axeman_icon",0,"lossarnach_axeman_icon", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("ithilien_ranger",0,"ithilien_ranger", avatar_scale,snd_footstep_grass, 0.15, 0.173, 0),

  ("knight_dolamroth",0,"knight_dolamroth", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  #("knight_gondo_trot",0,"knight_gondo_trot", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("knight_gondor",0,"knight_gondor", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("lamedon_horseman",0,"lamedon_horseman", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("knight_rivendell",0,"knight_rivendell", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("knight_rohan",0,"knight_rohan", avatar_scale, snd_gallop, 0.15, 0.173, 0),
#  ("knight_rohan_x5",0,"knight_rohan_x5", avatar_scale, snd_gallop, 0.15, 0.173, 0),

  ("dwarf",0,"dwarf", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),

  ("lorien_elf_a",0,"lorien_elf_a", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("lorien_elf_b",0,"lorien_elf_b", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("mirkwood_elf",0,"mirkwood_elf", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("dunadan_horseman",0,"dunadan_horseman", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("rivendell_elf",0,"rivendell_elf", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),

  ("mordor_captain",0,"mordor_captain", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("pikeman_isengard",0,"pikeman_isengard", avatar_scale,snd_footstep_grass, 0.15, 0.173, 0),

  ("orc",0,"orc", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("orc_isengard",0,"orc_isengard", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
#  ("orc_x6",0,"orc_x6", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("orc_tribal",0,"orc_tribal", avatar_scale,snd_footstep_grass, 0.15, 0.173, 0),
  #("wargrider_furshield_run",0,"wargrider_furshield_run", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("wargrider_run",0,"wargrider_run", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  #("wargrider_walk",0,"wargrider_walk", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0), # no need
                          
  ("uruk",0,"uruk", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("uruk_isengard",0,"uruk_isengard", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),

  ("wild_troll",0,"wild_troll", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),

  ("slaver_isengard",0,"slaver_isengard", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("slaver_mordor",0,"slaver_mordor", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  #("spy_isengard",0,"spy_isengard", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  #("spy_mordor",0,"spy_mordor", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("supply_gondor",0,"supply_gondor", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("supply_rohan",0,"supply_rohan", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("supply_isengard",0,"supply_isengard", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
  ("supply_mordor",0,"supply_mordor", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),

#TLD end 

  ("town",mcn_no_shadow,"map_town_a", 0.35,0),
#  ("town_steppe",mcn_no_shadow,"map_town_steppe_a", 0.35,0),
  ("village_a",mcn_no_shadow,"map_village_a", 0.45, 0),
#  ("village_burnt_a",mcn_no_shadow,"map_village_burnt_a", 0.45, 0),
#  ("village_deserted_a",mcn_no_shadow,"map_village_deserted_a", 0.45, 0),

  ("camp",mcn_no_shadow,"camp_tent", 0.25, 0),
  ("ship",mcn_no_shadow,"boat_sail_on", 0.23, snd_footstep_grass, 0.0, 0.05, 0),
  ("ship_on_land",mcn_no_shadow,"boat_sail_off", 0.23, 0),

#  ("castle_a",mcn_no_shadow,"map_castle_a", 0.35,0),
#  ("castle_b",mcn_no_shadow,"map_castle_b", 0.35,0),
  ("castle_c",mcn_no_shadow,"map_castle_c", 0.35,0),
#  ("castle_d",mcn_no_shadow,"map_castle_d", 0.35,0),
#  ("town_snow",mcn_no_shadow,"map_town_snow_a", 0.35,0),

#  ("village_snow_a",mcn_no_shadow,"map_village_snow_a", 0.45, 0),
#  ("village_snow_burnt_a",mcn_no_shadow,"map_village_snow_burnt_a", 0.45, 0),
#  ("village_snow_deserted_a",mcn_no_shadow,"map_village_snow_deserted_a", 0.45, 0),

#  ("castle_snow_a",mcn_no_shadow,"map_castle_snow_a", 0.35,0),
#  ("castle_snow_b",mcn_no_shadow,"map_castle_snow_b", 0.35,0),
  ("mule",0,"icon_mule", 0.2,snd_footstep_grass, 0.15, 0.173, 0),
#  ("cattle",0,"icon_cow", 0.2,snd_footstep_grass, 0.15, 0.173, 0),
#  ("training_ground",mcn_no_shadow,"training", 0.35,0),
  #("bridge_a",mcn_no_shadow,"map_river_bridge_a", 1.27,0),
  #("bridge_b",mcn_no_shadow,"map_river_bridge_b", 0.7,0),
  #("bridge_snow_a",mcn_no_shadow,"map_river_bridge_snow_a", 1.27,0),


#TLD MAP ICONS BEGIN # BEGIN PLACE ICONS

  ("ancient_ruins",mcn_no_shadow,"ancient_ruins", 1.0,0),
  ("argonath",mcn_no_shadow,"argonath", 1,0),
  ("baraddur",mcn_no_shadow,"baraddur", 1,0),
  ("cirithungol",mcn_no_shadow,"cirithungol", 1,0),
  ("orodruin",0,"orodruin", 1.5,0),

  ("cairandros",mcn_no_shadow,"cairandros", 1.0,0),
  ("castle_gondor_small",mcn_no_shadow,"Castle", 1.5,0,[(ti_on_init_map_icon,[(store_trigger_param_1,":center"),(party_slot_eq,":center",slot_center_destroyed,1),(cur_map_icon_set_tableau_material, "tableau_icon_burnable","mesh_icon_castle1")])]),
  ("castle__gondor_full",mcn_no_shadow,"Castle_Full", 1.0,0,[(ti_on_init_map_icon,[(store_trigger_param_1,":center"),(party_slot_eq,":center",slot_center_destroyed,1),(cur_map_icon_set_tableau_material, "tableau_icon_burnable","mesh_icon_castle1")])]),
  ("castle__gondor_wall",mcn_no_shadow,"Castle_Wall", 1.0,0,[(ti_on_init_map_icon,[(store_trigger_param_1,":center"),(party_slot_eq,":center",slot_center_destroyed,1),(cur_map_icon_set_tableau_material, "tableau_icon_burnable","mesh_icon_castle1")])]),
  ("corsaircamp",mcn_no_shadow,"corsaircamp", 1.0,0),
  ("dolamroth",mcn_no_shadow,"dolamroth", 1.0,0,[(ti_on_init_map_icon,[(store_trigger_param_1,":center"),(party_slot_eq,":center",slot_center_destroyed,1),(cur_map_icon_set_tableau_material, "tableau_icon_burnable","mesh_icon_dolamroth")])]),
  ("dolguldur",mcn_no_shadow,"dolguldur", 1.0,0),
  ("east_osgilliath",mcn_no_shadow,"east_osgilliath", 0.8,0),
  ("west_osgilliath",mcn_no_shadow,"west_osgilliath", 0.8,0),
  ("edoras",mcn_no_shadow,"Edoras", 1.0,0,[(ti_on_init_map_icon,[(store_trigger_param_1,":center"),(party_slot_eq,":center",slot_center_destroyed,1),(cur_map_icon_set_tableau_material, "tableau_icon_burnable","mesh_icon_edoras")])]),
  ("field",mcn_no_shadow,"Fielda", 1.0,0),
  # ("field_b",mcn_no_shadow,"Fieldb", 1.0,0),
  # ("field_c",mcn_no_shadow,"Fieldc", 1.0,0),
  ("gondortown",mcn_no_shadow,"gondortown", 1.0,0,[(ti_on_init_map_icon,[(store_trigger_param_1,":center"),(party_slot_eq, ":center",slot_center_destroyed,1),(cur_map_icon_set_tableau_material, "tableau_icon_burnable","mesh_icon_gondor_town")])]),
  ("grove",mcn_no_shadow,"Grove", 0.45,0),
  ("hand_isen",mcn_no_shadow,"handsign", 0.26,0),
  ("haradcamp",mcn_no_shadow,"haradcamp", 1.0,0),
  ("helms_deep",mcn_no_shadow,"Helms_Deep", 0.7,0,[(ti_on_init_map_icon,[(store_trigger_param_1,":center"),(party_slot_eq,":center",slot_center_destroyed,1),(cur_map_icon_set_tableau_material, "tableau_icon_burnable","mesh_icon_helmsdeep")])]),
  ("henneth_annun",mcn_no_shadow,"henneth_annun", 0.4,0),
  ("isengard",mcn_no_shadow,"Isengard", 0.55,0,  1.8,1.8,0.0),
  ("minas_tirith",mcn_no_shadow,"Minas_Tirith", 0.8,0, 0.0,-0.75,3.6,[(ti_on_init_map_icon,[(store_trigger_param_1,":center"),(party_slot_eq,":center",slot_center_destroyed,1),(cur_map_icon_set_tableau_material, "tableau_icon_burnable","mesh_icon_minastirith")])]),
  
  ("minasmorgul",mcn_no_shadow,"minasmorgul", 0.7,0),
  ("morannon",mcn_no_shadow,"Morannon", 1.0,0),
  ("moria",mcn_no_shadow,"moria", 1.0,0),
  ("moria_bak",mcn_no_shadow,"moria_bak", 1.0,0),
  ("nomadcamp",mcn_no_shadow,"nomadcamp", 1.0,0),
  ("nomadcamp_b",mcn_no_shadow,"nomadcamp_b", 1.0,0),
  #("north_bridge",mcn_no_shadow,"North_Bridge", 1.0,0),
  #("nw_bridge",mcn_no_shadow,"NW_bridge", 1.0,0),
  ("orctower",mcn_no_shadow,"orctower", 0.5,0),
  
  ("rohantown1",mcn_no_shadow,"RohanTown1", 1.0,0,[(ti_on_init_map_icon,[(store_trigger_param_1,":center"),(party_slot_eq,":center",slot_center_destroyed,1),(cur_map_icon_set_tableau_material, "tableau_icon_burnable","mesh_icon_edoras")])]),
  ("smallvillage",mcn_no_shadow,"smallvillage", 2.0,0),
  ("tree",mcn_no_shadow,"Tree", 0.5,0),
  
  ("burial_mound",mcn_no_shadow,"burial_mound", 1.0,0),
  ("tree_low",mcn_no_shadow,"Tree_low", 1.0,0),

  ("custom_banner_01",0,"custom_map_banner_01", banner_scale, 0,
   [(ti_on_init_map_icon,
      [ (store_trigger_param_1, ":party_no"),
        (party_get_slot, ":leader_troop", ":party_no", slot_town_lord),
        (try_begin),
          (ge, ":leader_troop", 0),
          (cur_map_icon_set_tableau_material, "tableau_custom_banner_square", ":leader_troop"),
        (try_end),
        ]),
     ]),
  ("custom_banner_02",0,"custom_map_banner_02", banner_scale, 0,
   [(ti_on_init_map_icon,
      [ (store_trigger_param_1, ":party_no"),
        (party_get_slot, ":leader_troop", ":party_no", slot_town_lord),
        (try_begin),
          (ge, ":leader_troop", 0),
          (cur_map_icon_set_tableau_material, "tableau_custom_banner_short", ":leader_troop"),
        (try_end),
        ]),
     ]),
  ("custom_banner_03",0,"custom_map_banner_03", banner_scale, 0,
   [(ti_on_init_map_icon,
      [ (store_trigger_param_1, ":party_no"),
        (party_get_slot, ":leader_troop", ":party_no", slot_town_lord),
        (try_begin),
          (ge, ":leader_troop", 0),
          (cur_map_icon_set_tableau_material, "tableau_custom_banner_tall", ":leader_troop"),
        (try_end),
        ]),
     ]),
		
  #indication for fords
  ("ford_rocks",0,"ford_rocks", 0.6, 0),

  # party map banners, each followed by king vesion
   ("mfp_gondor",    0,"map_flag_gondor_lord", banner_scale,0),
   ("mfp_gondor_k",  0,"map_flag_gondor_king", banner_scale,0),
   ("mfp_rohan",     0,"map_flag_rohan_lord", banner_scale,0),
   ("mfp_rohan_k",   0,"map_flag_rohan_king", banner_scale,0),
   ("mfp_isengard",  0,"map_flag_isengard_lord", banner_scale,0),
   ("mfp_isengard_k",0,"map_flag_isengard_king", banner_scale,0),
   ("mfp_mordor",    0,"map_flag_mordor_lord", banner_scale,0),
   ("mfp_mordor_k",  0,"map_flag_mordor_king", banner_scale,0),
   ("mfp_harad",     0,"map_flag_harad_lord", banner_scale,0),
   ("mfp_harad_k",   0,"map_flag_harad_king", banner_scale,0),
   ("mfp_khand",     0,"map_flag_khand_lord", banner_scale,0),
   ("mfp_khand_k",   0,"map_flag_khand_king", banner_scale,0),
   ("mfp_rhun",      0,"map_flag_rhun_lord", banner_scale,0),
   ("mfp_rhun_k",    0,"map_flag_rhun_king", banner_scale,0),
   ("mfp_umbar",     0,"map_flag_umbar_lord", banner_scale,0),
   ("mfp_umbar_k",   0,"map_flag_umbar_king", banner_scale,0),
   ("mfp_lorien",    0,"map_flag_lorien_lord", banner_scale,0),
   ("mfp_lorien_k",  0,"map_flag_lorien_king", banner_scale,0),

   # no king flags from now on...
   ("mfp_woodelf",   0,"map_flag_woodelf_lord", banner_scale,0),
   ("mfp_guldur",    0,"map_flag_guldur_lord", banner_scale,0),
   ("mfp_imladris",  0,"map_flag_imladris_lord", banner_scale,0),
   ("mfp_moria",     0,"map_flag_moria_lord", banner_scale,0),
   ("mfp_dwarf",     0,"map_flag_dwarf_lord", banner_scale,0),
   ("mfp_northmen",  0,"map_flag_northmen_lord", banner_scale,0),
   ("mfp_dale",      0,"map_flag_dale_lord", banner_scale,0),
   ("mfp_gundabad",  0,"map_flag_gundabad_lord", banner_scale,0),
   ("mfp_dunland",   0,"map_flag_dunland_lord", banner_scale,0),
   
   # alternative rohan lords (mtarini)
   ("mfp_rohan_a",0,"map_flag_rohan_lord_a", banner_scale,0),
   ("mfp_rohan_b",0,"map_flag_rohan_lord_b", banner_scale,0),
   ("mfp_rohan_c",0,"map_flag_rohan_lord_c", banner_scale,0),
   ("mfp_rohan_d",0,"map_flag_rohan_lord_d", banner_scale,0),
   ("mfp_rohan_e",0,"map_flag_rohan_lord_e", banner_scale,0),

   # gondor subfactions (same ordering as subfac_ constnant)
   ("mfp_pelargir",0,"map_flag_pelargir_lord", banner_scale,0),
   ("mfp_dol_amroth",0,"map_flag_dolamroth_lord", banner_scale,0),
   ("mfp_ethring",0,"map_flag_ethring_lord", banner_scale,0),
   ("mfp_lossarnach",0,"map_flag_lossarnach_lord", banner_scale,0),
   ("mfp_pinnath",0,"map_flag_pinnath_lord", banner_scale,0),
   ("mfp_erech",0,"map_flag_erech_lord", banner_scale,0),

	  
  ("banner_126",0,"custom_map_banner_01", banner_scale,0), 

 # centers map banners
   ("mfc_gondor",0,"map_flag_gondor_center", banner_scale,0),
   ("mfc_rohan",0,"map_flag_rohan_center", banner_scale,0),
   ("mfc_isengard",0,"map_flag_isengard_center", banner_scale,0),
   ("mfc_mordor",0,"map_flag_mordor_center", banner_scale,0),
   ("mfc_harad",0,"map_flag_harad_center", banner_scale,0),
   ("mfc_khand",0,"map_flag_khand_center", banner_scale,0),
   ("mfc_rhun",0,"map_flag_rhun_center", banner_scale,0),
   ("mfc_umbar",0,"map_flag_umbar_center", banner_scale,0),
   ("mfc_lorien",0,"map_flag_lorien_center", banner_scale,0),
   ("mfc_woodelf",0,"map_flag_woodelf_center", banner_scale,0),
   ("mfc_guldur",0,"map_flag_guldur_center", banner_scale,0),
   ("mfc_imladris",0,"map_flag_imladris_center", banner_scale,0),
   ("mfc_moria",0,"map_flag_moria_center", banner_scale,0),
   ("mfc_dwarf",0,"map_flag_dwarf_center", banner_scale,0),
   ("mfc_northmen",0,"map_flag_northmen_center", banner_scale,0),
   ("mfc_dale",0,"map_flag_dale_center", banner_scale,0),
   ("mfc_gundabad",0,"map_flag_gundabad_center", banner_scale,0),
   ("mfc_dunland",0,"map_flag_dunland_center", banner_scale,0),
 # for gondor subfactions,...
   ("mfc_pelargir",0,"map_flag_pelargir_center", banner_scale,0),
   ("mfc_dol_amroth",0,"map_flag_dolamroth_center", banner_scale,0),
   ("mfc_erech",0,"map_flag_erech_center", banner_scale,0),
   ("mfc_ethring",0,"map_flag_ethring_center", banner_scale,0),
   ("mfc_lossarnach",0,"map_flag_lossarnach_center", banner_scale,0),
   ("mfc_pinnath",0,"map_flag_pinnath_center", banner_scale,0),

  ("thranduil",mcn_no_shadow,"thranduilhall", 1.0,0),
  ("esgaroth",mcn_no_shadow,"esgaroth", 1.0,0),
  ("debris",0,"debris", 0.6,0),
  ("empty",0,"0", 0.6,0),
  ("gandalf", 0, "white_rider", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("nazgul" , 0, "black_rider", avatar_scale, snd_gallop, 0.15, 0.173, 0),
  ("shrubbery",0,"icon_shrubbery", 1,0), # for designating impassable forest

]
