from module_info import *
import string

dword      = 0x8000000000000000
dword_mask = 0xffffffffffffffff

density_bits      = 32
fkf_density_mask  = 0xFFFF #16K

#terain condition flags
fkf_plain             = 0x00000004 	#Gondor; Green ground, spawns mediterranean flora
fkf_steppe            = 0x00000008	#Rohan, northern regions, wilderness; dry grass, spawns occasional bushes, rocks, small trees
fkf_snow              = 0x00000010	#Marshland; currently no grass assigned, spawns dead brownish trees and bushes
fkf_desert            = 0x00000020	#Currently: Dagorlad, Emyn Muil, Brown Lands - all these could/should be replaced by custom scenes. Needs better ground texture
fkf_plain_forest      = 0x00000400	#only used for small forests in Gondor and Rohan --> Could be used for Vale of Anduin, maybe more green Rohan areas (reduce trees)
fkf_steppe_forest     = 0x00000800	#basically unused (only for some rare randomized Ithilien scenes) --> Use as an alternative for northern regions
fkf_snow_forest       = 0x00001000	#unused --> Use for deep forest random scenes (Fangorn, Mirkwood)?
fkf_desert_forest     = 0x00002000	#unused --> Could be used for mountain foothills / Emyn Muil, but that would need worldmap adjustment
fkf_terrain_mask      = 0x0000ffff

fkf_realtime_ligting  = 0x00010000 #deprecated
fkf_point_up          = 0x00020000 #uses auto-generated point-up(quad) geometry for the flora kind
fkf_align_with_ground = 0x00040000 #align the flora object with the ground normal
fkf_grass             = 0x00080000 #is grass
fkf_on_green_ground   = 0x00100000 #populate this flora on green ground
fkf_rock              = 0x00200000 #is rock (does not do anything)
fkf_tree              = 0x00400000 #is tree -> note that if you set this parameter, you should pass additional alternative tree definitions
fkf_snowy             = 0x00800000 # (does not do anything)
fkf_guarantee         = 0x01000000

fkf_speedtree         = 0x02000000  #NOT FUNCTIONAL: we have removed speedtree support on M&B Warband

fkf_has_colony_props  = 0x04000000  # if fkf_has_colony_props -> then you can define colony_radius and colony_treshold of the flora kind


def density(g):
  if (g > fkf_density_mask):
    g = fkf_density_mask
  return ((dword | g) << density_bits)


fauna_kinds = [

###GRASS TYPES BUSHES

 ('grass', #regular grass
  fkf_plain|fkf_point_up|fkf_align_with_ground|fkf_grass|fkf_on_green_ground|fkf_guarantee|density(1500),
  [['PW_grass_yellow_e', '0'],
   ['PW_grass_a_xx', '0'],
   ['PW_grass_b_xx', '0'],
   ['PW_grass_b_xx', '0'],
   ['PW_grass_b_xx', '0'],
   ['PW_grass_e_xx', '0']]),
   
 ('grass_steppe',
  fkf_steppe|fkf_steppe_forest|fkf_point_up|fkf_align_with_ground|fkf_grass|fkf_on_green_ground|fkf_guarantee|density(1500),
  [['PW_grass_e_xx', '0'],
   ['PW_grass_yellow_b_xx', '0'],
   ['PW_grass_yellow_b_xx', '0'],
   ['PW_grass_e_xx', '0']]),
   
 ('ga_grass_snow',
  fkf_snow|fkf_snow_forest|fkf_align_with_ground|fkf_grass|fkf_guarantee|density(1666),
  [['PW_grass_a_xx', '0'],
   ['PW_grass_b_xx', '0'],
   ['PW_grass_b_xx', '0'],
   ['PW_grass_b_xx', '0'],
   ['PW_grass_e_xx', '0']]),
   
 ('ga_grass_desert', #desert grass must not be flagged as grass and must not use the grass shader
 #fkf_desert|fkf_desert_forest|fkf_align_with_ground|fkf_grass|fkf_on_green_ground|fkf_guarantee|fkf_has_colony_props|density(2012),
  fkf_desert|fkf_desert_forest|fkf_align_with_ground|fkf_guarantee|density(2012),
  [['PW_grass_e_xx', '0'],
   ['PW_grass_yellow_b_xx', '0'],
   ['PW_grass_yellow_b_xx', '0'],
   ['PW_grass_e_xx', '0']]),
   
 ('grass_bush', #stinging nettle
  fkf_plain|fkf_steppe|fkf_desert|fkf_steppe_forest|fkf_plain_forest|fkf_align_with_ground|fkf_grass|fkf_point_up|density(100),
  [['PW_grass_bush_a_xx', '0'], ['PW_grass_bush_b_xx', '0']]),
  
 ('grass_saz', #white flowers
  fkf_plain|fkf_steppe_forest|fkf_on_green_ground|density(198),
  [['PW_grass_bush_c_xx', '0'], ['PW_grass_bush_c_xx', '0']]),
  
 ('grass_purple', #purple flowers
  fkf_plain|fkf_steppe_forest|fkf_grass|density(500),
  [['PW_grass_bush_e_xx', '0'], ['PW_grass_bush_e_xx', '0']]),
  
 ('fern',
  fkf_plain_forest|fkf_snow_forest|fkf_align_with_ground|fkf_grass|density(1000),
  [['PW_fern_big', '0'],['PW_fern_a_xx', '0'], ['PW_fern_b_xx', '0']]),
   
 ('grass_bush_g', #bundles of seedy grass
  fkf_plain|fkf_steppe|fkf_plain_forest|fkf_steppe_forest|fkf_align_with_ground|fkf_grass|density(400),
  [['PW_grass_bush_g01_xx', '0'],
   ['PW_grass_bush_g02_xx', '0'],
   ['PW_grass_bush_g03_xx', '0']]),
   
 ('grass_bush_h', #leafy ground plants, similar to bushes04_a
  fkf_plain|fkf_plain_forest|fkf_align_with_ground|fkf_grass|density(400),
  [['PW_grass_bush_h01_xx', '0'],
   ['PW_grass_bush_h02_xx', '0'],
   ['PW_grass_bush_h03_xx', '0']]),
   
 ('grass_bush_i', #bushes of dry, red-flowered grass
  fkf_plain|fkf_plain_forest|fkf_align_with_ground|fkf_grass|density(400),
  [['PW_grass_bush_i01_xx', '0'], ['PW_grass_bush_i02_xx', '0']]),
  
 ('grass_bush_j', #ilex like leafy bushes
  fkf_plain|fkf_steppe|fkf_plain_forest|fkf_steppe_forest|fkf_align_with_ground|fkf_grass|density(50),
  [['PW_grass_bush_j01_xx', '0'], ['PW_grass_bush_j02_xx', '0']]),
  
 ('grass_bush_k', #dry brown grass
  fkf_plain|fkf_steppe|fkf_align_with_ground|fkf_grass|density(400),
  [['PW_grass_bush_k01_xx', '0'], ['PW_grass_bush_k02_xx', '0']]),


### BUSHES
  
 ('grass_bush_l', #zl_bush_white_flowers zl_white_flowers
  fkf_plain|fkf_plain_forest|fkf_align_with_ground|density(50),
  [['PW_grass_bush_l01', '0'], ['PW_grass_bush_l02', '0']]),
  
 ('zl_white_flowers', #zl_bush_white_flowers grass_bush_l
  fkf_align_with_ground|density(2),
  [['PW_grass_bush_l01', '0'], ['PW_grass_bush_l02', '0']]),

 ('zl_bush_white_flowers', #grass_bush_l
  0,
  [['PW_grass_bush_l01', '0'], ['PW_grass_bush_l02', '0']]),

 ('thorn_a', #green leafed "thorny" bushes
  fkf_plain|fkf_plain_forest|fkf_steppe|fkf_align_with_ground|density(50),
  [['PW_thorn_a', '0'],
   ['PW_thorn_b', '0'],
   ['PW_thorn_c', '0'],
   ['PW_thorn_d', '0']]),
   
 ('basak', #dry brown grass
  fkf_steppe|fkf_desert|fkf_steppe_forest|fkf_desert_forest|density(70),
  [['PW_basak_xx', '0']]),
  
 ('common_plant', #single dry brown grass bush, smaller version of bushes05_a
  fkf_steppe|fkf_desert|fkf_steppe_forest|fkf_desert_forest|density(70),
  [['PW_common_plant_xx', '0']]),
  
 ('small_plant',
  fkf_plain|fkf_steppe|fkf_plain_forest|fkf_steppe_forest|fkf_align_with_ground|density(50),
  [['PW_big_bush_xx', '0']]),
  
#DUPLICATE
 ('seedy_plant', 
  fkf_plain|fkf_steppe|fkf_plain_forest|fkf_steppe_forest|density(50),
  [['PW_big_bush_xx', '0']]),

#DUPLICATE
 ('big_bush',
  fkf_plain|fkf_steppe|fkf_plain_forest|fkf_steppe_forest|density(30),
  [['PW_big_bush_xx', '0']]),
  
 ('buddy_plant', #white flowered bush
  fkf_plain|fkf_plain_forest|fkf_steppe_forest|density(50),
  [['PW_buddy_plant_xx', '0'], ['PW_buddy_plant_b_xx', '0']]),

 ('yellow_flower', #low yellow flower
  fkf_plain|fkf_align_with_ground|density(50),
  [['PW_yellow_flower', '0'], ['PW_yellow_flower_b', '0']]),

 ('spiky_plant', #zl_yellow_flowers
  fkf_plain|fkf_align_with_ground|density(50),
  [['PW_spiky_plant', '0']]),

#DUPLICATE
 ('zl_yellow_flowers', #spiky_plant
  fkf_align_with_ground|density(2),
  [['PW_spiky_plant', '0']]),

 ('blue_flower',
  fkf_plain|fkf_plain_forest|density(30),
  [['PW_blue_flower_xx', '0']]),

 ('bushes02_a', #willowy bushes
  fkf_plain|fkf_snow|fkf_steppe_forest|density(20),
  [['PW_bushes02_a', 'bo_pw_bushes02_a'],
   ['PW_bushes02_b', 'bo_pw_bushes02_a'],
   ['PW_bushes02_c', 'bo_pw_bushes02_a']]),

 ('bushes03_a', #pine-like small bush
  fkf_steppe|fkf_snow|fkf_desert|fkf_plain_forest|fkf_desert_forest|density(54),
  [['PW_bushes03_a_xx', '0'],
   ['PW_bushes03_b_xx', '0'],
   ['PW_bushes03_c_xx', '0']]),

 ('bushes04_a', #leafy low grass bushes, very similar to grass_bush_h, same as ga_bushes04_a_snow
  fkf_plain|fkf_steppe|fkf_snow|fkf_desert|fkf_plain_forest|fkf_steppe_forest|fkf_desert_forest|density(102),
  [['PW_bushes04_a_xx', '0'],
   ['PW_bushes04_b_xx', '0'],
   ['PW_bushes04_c_xx', '0']]),

#DUPLICATE
 ('ga_bushes04_a_snow', 
  fkf_snow|fkf_snow_forest|fkf_align_with_ground|density(390),
  [['PW_bushes04_a_xx', '0'],
   ['PW_bushes04_b_xx', '0'],
   ['PW_bushes04_c_xx', '0']]),

 ('bushes05_a', #dry brown grass bush, just a larger version of common_plant
  fkf_steppe|fkf_desert|fkf_steppe_forest|density(70),
  [['PW_bushes05_a_xx', '0']]),

 ('bushes06_a', #thistle bushes
  fkf_plain|fkf_steppe|fkf_snow|fkf_desert|fkf_plain_forest|fkf_steppe_forest|fkf_desert_forest|density(102),
  [['PW_bushes06_a_xx', '0'],
   ['PW_bushes06_b_xx', '0'],
   ['PW_bushes06_c_xx', '0']]),

 ('bushes07_a', #small pines
  fkf_snow|fkf_desert|fkf_plain_forest|fkf_desert_forest|density(102),
  [['PW_bushes07_a_xx', '0'],
   ['PW_bushes07_b_xx', '0'],
   ['PW_bushes07_c_xx', '0']]),

 ('bushes08_a', #ilex bushes like grass_bush_j, but not grass, same as zl_bush_08
  fkf_plain|fkf_steppe|fkf_plain_forest|fkf_steppe_forest|density(70),
  [['PW_bushes08_a_xx', '0'],
   ['PW_bushes08_b_xx', '0'],
   ['PW_bushes08_c_xx', '0']]),

#DUPLICATE
 ('zl_bush_08',
  0,
  [['PW_bushes08_a_xx', '0'],
   ['PW_bushes08_b_xx', '0'],
   ['PW_bushes08_c_xx', '0']]),

 ('bushes09_a', #fir bushes, same as zl_fir_bush
  fkf_snow|fkf_steppe_forest|fkf_desert|fkf_desert_forest|density(102),
  [['PW_bushes09_a', '0'], ['PW_bushes09_b', '0'], ['PW_bushes09_c', '0']]),

#DUPLICATE
 ('zl_fir_bush',
  fkf_steppe|fkf_desert|fkf_desert_forest|density(10),
  [['PW_bushes09_a', '0'], ['PW_bushes09_b', '0'], ['PW_bushes09_c', '0']]),

 ('bushes10_a', #birch bushes , same as zl_birch_green_bush
  fkf_plain_forest|fkf_steppe_forest|density(70),
  [['PW_bushes10_a', 'bo_pw_bushes10_a'],
   ['PW_bushes10_b', 'bo_pw_bushes10_b'],
   ['PW_bushes10_c', 'bo_pw_bushes10_c']]),

#DUPLICATE
 ('zl_birch_green_bush',
  0,
  [['PW_bushes10_a', '0'], ['PW_bushes10_b', '0'], ['PW_bushes10_c', '0']]),

 ('bushes11_a', #low mountain pines, same as zl_shalebush
  fkf_steppe|fkf_steppe_forest|fkf_snow|fkf_desert|fkf_plain_forest|fkf_desert_forest|density(70),
  [['PW_bushes11_a', '0'], ['PW_bushes11_b', '0'], ['PW_bushes11_c', '0']]),
  
#DUPLICATE
 ('zl_shalebush', #same as bushes11_a
  fkf_desert_forest|density(2),
  [['PW_bushes11_a', '0'], ['PW_bushes11_b', '0'], ['PW_bushes11_c', '0']]),

 ('bushes12_a', #dry brown grass, same as zl_bush_steppe_wheat
  fkf_steppe|fkf_steppe_forest|fkf_align_with_ground|density(50),
  [['PW_bushes12_a_xx', '0'],
   ['PW_bushes12_b_xx', '0'],
   ['PW_bushes12_c_xx', '0']]),

#DUPLICATE
 ('zl_bush_steppe_wheat', #same as bushes12_a
  0,
  [['PW_bushes12_a_xx', '0'],
   ['PW_bushes12_b_xx', '0'],
   ['PW_bushes12_c_xx', '0']]),

 ('pw_gray_bush',
  fkf_snow|fkf_desert|fkf_snow_forest|fkf_realtime_ligting|fkf_tree|density(5),
  [['PW_tree_3_a_gray', '0'], ['PW_tree_3_b_gray', '0']]),

#duplicate
 ('pw_snow_bushes', density(4), [['PW_tree_19_a', '0']]), #similar to ga_tree_3_a_brown
 
 ('ga_tree_3_a_brown', #similar to pw_snow_bushes
  fkf_desert|fkf_desert_forest|density(22),
  [['PW_tree_3_a_brown', '0'], ['PW_tree_3_b_brown', '0']]),
  
 ('pw_ground_thorn', #same as tree_1
  0,
  [['PW_tree_9_a_xx', '0'], ['PW_tree_9_a_xx', '0'], ['PW_tree_9_a_xx', '0']]),



### ROCKS and OBJECTS

 ('pw_small_rock_group',
  fkf_steppe|fkf_desert|fkf_steppe_forest|fkf_desert_forest|fkf_align_with_ground|fkf_realtime_ligting|fkf_rock|density(22),
  [['PW_small_rock_group_a', '0'], ['PW_small_rock_group_b', '0'], ['PW_small_rock_group_c', '0']]),

 ('rock', #same as pw_fir
  fkf_plain_forest|fkf_tree|density(30),
  [['PW_pine_1_a', 'bo_pw_pine_1_a'],
   ['PW_pine_1_b', 'bo_pw_pine_1_b']]),
   
 ('small_rock',
  fkf_steppe|fkf_plain_forest|fkf_steppe_forest|fkf_tree|density(4),
  [['PW_rock_a', 'bo_PW_rock_a'],
   ['PW_rock_b', 'bo_PW_rock_b']]),
   
 ('rock_snowy',
  fkf_tree,
  [['rock_snowy_a', 'bo_rock_snowy_a'],
   ['rock_snowy_b', 'bo_rock_snowy_b'],
   ['rock_snowy_c', 'bo_rock_snowy_c'],]),
   
# ('rock_snowy', #actual snowy pines
#  fkf_tree,
#  [['PW_rock_snowy_a', 'bo_pw_rock_snowy_a'],
#   ['PW_rock_snowy_b', 'bo_pw_rock_snowy_b'],
#   ['PW_rock_snowy_c', 'bo_pw_rock_snowy_c']]),

 ('rock_snowy2', fkf_tree, [['PW_tree_snowy_b', 'bo_pw_tree_snowy_b']]), #single tree version of snowy_pine

 ('pw_man_skeleton',
  0,
  [['PW_tree_7_a_color', '0'],
   ['PW_tree_7_b_color', '0'],
   ['PW_tree_7_c_color', '0']]),


### VANILLA TREES

 ('aspen',
  fkf_realtime_ligting|fkf_rock|density(22),
  [['aspen_a', 'bo_aspen_a'],
   ['aspen_b', 'bo_aspen_b'],
   ['aspen_c', 'bo_aspen_c']]),

 ('pine_1',
  fkf_plain_forest|fkf_steppe_forest|fkf_desert_forest|fkf_tree|density(4),
  [['pine_1_a', 'bo_pine_1_a'], ['pine_1_b', 'bo_pine_1_b']]),

 ('pine_2',
  fkf_plain_forest|fkf_steppe_forest|fkf_desert_forest|fkf_tree|density(4),
  [['pine_2_a', 'bo_pine_2_a']]),

 ('pine_3',
  fkf_plain_forest|fkf_steppe_forest|fkf_desert_forest|fkf_tree|density(4),
  [['pine_3_a', 'bo_pine_3_a']]),

 ('pine_4',
  fkf_plain_forest|fkf_desert_forest|fkf_tree|density(4),
  [['pine_4_a', 'bo_pine_4_a']]),

 ('pine_6',
  fkf_plain_forest|fkf_desert_forest|fkf_tree|density(4),
  [['pine_6_a', 'bo_pine_6_a']]),

#DUPLICATE
 ('tree_1', fkf_plain_forest|density(6), [['PW_tree_9_a_xx', '0']]), #same as pw_ground_thorn

 ('tree_2', 0, [['tree_2_a', 'bo_tree_2_a'], ['tree_2_b', 'bo_tree_2_b']]),

 ('tree_3',
  fkf_plain|fkf_realtime_ligting|fkf_tree|density(5),
  [['tree_3_a', 'bo_tree_3_a'], ['tree_3_b', 'bo_tree_3_b']]),

 ('tree_4',
  fkf_plain_forest|fkf_tree|density(4),
  [['tree_4_a', 'bo_tree_4_a'], ['tree_4_b', 'bo_tree_4_b']]),

 ('tree_5',
  fkf_plain_forest|density(70),
  [['tree_5_a', 'bo_tree_5_a'],
   ['tree_5_b', 'bo_tree_5_b'],
   ['tree_5_c', 'bo_tree_5_c'],
   ['tree_5_d', 'bo_tree_5_d']]),
   
 ('tree_6',
  fkf_plain|fkf_tree|density(5),
  [['tree_6_a', 'bo_tree_6_a'],
   ['tree_6_b', 'bo_tree_6_b'],
   ['tree_6_c', 'bo_tree_6_c'],
   ['tree_6_d', 'bo_tree_6_d']]),

 ('tree_7',
  0,
  [['tree_7_a', 'bo_tree_7_a'],
   ['tree_7_b', 'bo_tree_7_b'],
   ['tree_7_c', 'bo_tree_7_c']]),

 ('tree_8',
  fkf_plain|fkf_plain_forest|fkf_tree|density(4),
  [['tree_8_a', 'bo_tree_8_a'],
   ['tree_8_b', 'bo_tree_8_b'],
   ['tree_8_c', 'bo_tree_8_c']]),

 ('tree_9',
  fkf_plain_forest|fkf_tree|density(50),
  [['tree_9_a', 'bo_tree_9_a'],
   ['tree_9_b', 'bo_tree_9_a'],
   ['tree_9_c', 'bo_tree_9_a']]),

 ('tree_10',
  fkf_plain_forest|fkf_tree|density(4),
  [['tree_10_a', 'bo_tree_10_a'],
   ['tree_10_b', 'bo_tree_10_a'],
   ['tree_10_c', 'bo_tree_10_a']]),

 ('tree_11',
  fkf_plain_forest|fkf_plain|fkf_tree|density(4),
  [['tree_11_a', 'bo_tree_11_a'],
   ['tree_11_b', 'bo_tree_11_a'],
   ['tree_11_c', 'bo_tree_11_a']]),

 ('tree_12',
  fkf_tree|density(4),
  [['tree_12_a', 'bo_tree_12_a'],
   ['tree_12_b', 'bo_tree_12_b'],
   ['tree_12_c', 'bo_tree_12_c']]),

 ('tree_14',
  fkf_tree,
  [['tree_14_a', 'bo_tree_14_a'],
   ['tree_14_b', 'bo_tree_14_b'],
   ['tree_14_c', 'bo_tree_14_c']]),

 ('tree_15',
  fkf_tree|density(64),
  [['tree_15_a', 'bo_tree_15_a'],
   ['tree_15_b', 'bo_tree_15_b'],
   ['tree_15_c', 'bo_tree_15_c']]),

 ('tree_16',
  fkf_plain_forest|fkf_tree|density(38),
  [['tree_16_a', 'bo_tree_16_a'], ['tree_16_b', 'bo_tree_16_b']]),

 ('tree_17',
  fkf_plain_forest|fkf_tree|density(4),
  [['tree_17_a', 'bo_tree_17_a'],
   ['tree_17_b', 'bo_tree_17_b'],
   ['tree_17_c', 'bo_tree_17_c'],
   ['tree_17_d', 'bo_tree_17_d']]),

 ('tree_19',
  fkf_plain_forest|fkf_tree|density(4),
  [['tree_19_a', 'bo_tree_19_a']]),

 ('beech',
  fkf_plain_forest|fkf_tree|density(3),
  [['tree_20_a', 'bo_tree_20_a'], ['tree_20_b', 'bo_tree_20_b']]),

 ('tree_plane',
  fkf_plain_forest|fkf_tree|density(4),
  [['tree_18_a', 'bo_tree_18_a'], ['tree_18_b', 'bo_tree_18_b']]),

 ('tall_tree',
  fkf_plain_forest|fkf_plain|fkf_tree|density(4),
  [['tall_tree_a', 'bo_tall_tree_a']]),

 ('tree_e',
  fkf_plain|fkf_plain_forest|fkf_tree|density(4),
  [['tree_e_1', 'bo_tree_e_1'],
   ['tree_e_2', 'bo_tree_e_2'],
   ['tree_e_3', 'bo_tree_e_3']]),

 ('tree_f',
  fkf_tree,
  [['tree_f_1', 'bo_tree_f_1'],
   ['tree_f_2', 'bo_tree_f_1'],
   ['tree_f_3', 'bo_tree_f_1']]),

 ('grape_vineyard', 0, [['grape_vineyard', 'bo_grape_vineyard']]),

 ('grape_vineyard_stake',
  0,
  [['grape_vineyard_stake', 'bo_grape_vineyard_stake']]),

 ('wheat',
  0,
  [['wheat_a', '0'], ['wheat_b', '0'], ['wheat_c', '0'], ['wheat_d', '0']]),


### GUTEK TREES

 ('pw_fir', #same as rock
  fkf_steppe_forest|fkf_tree|density(4),
  [['PW_pine_1_a', 'bo_pw_pine_1_a'],
   ['PW_pine_1_b', 'bo_pw_pine_1_b']]),

 ('pw_fir2', fkf_tree|density(4), [['PW_pine_2_a', 'bo_pw_pine_2_a']]),
 
 ('pw_fir3', fkf_tree|density(4), [['PW_pine_3_a', 'bo_pw_pine_3_a']]),

 ('snowy_pine', fkf_tree, [['PW_tree_snowy_a', 'bo_pw_tree_snowy_a']]), #Not really snowy pines, but tall, dead looking tree

 ('snowy_pine_2', fkf_tree, [['PW_snowy_pine_2', 'bo_pw_snowy_pine_2']]), #actual snowy pine

# ('rock_snowy', #actual snowy pines
#  fkf_tree,
#  [['PW_rock_snowy_a', 'bo_pw_rock_snowy_a'],
#   ['PW_rock_snowy_b', 'bo_pw_rock_snowy_b'],
#   ['PW_rock_snowy_c', 'bo_pw_rock_snowy_c']]),

 # ('rock_snowy2', fkf_tree, [['PW_tree_snowy_b', 'bo_pw_tree_snowy_b']]), #single tree version of snowy_pine

 ('pw_pine_group1', #shares model with zl_pink_tree
  fkf_desert_forest|fkf_tree|density(2),
  [['PW_pine_6_a', 'bo_pw_pine_6_a']]),
  
 ('pw_pine_group2', #shares model with zl_pink_tree
  fkf_desert_forest|fkf_tree|density(2),
  [['PW_pine_4_a', 'bo_pw_pine_4_a']]),

 ('pw_pine_group3', #shares model with zl_pink_tree
  fkf_desert_forest|fkf_tree|density(2),
  [['PW_tall_tree_a', 'bo_pw_tall_tree_a']]),

 ('zl_pink_tree', #actual tall pines, similar but different to pw_pine_small_group
  fkf_tree|fkf_plain|density(4),					#InVain: added to plain (Gondor)
  [['PW_tall_tree_a', 'bo_pw_tall_tree_a'],
   ['PW_pine_4_a', 'bo_pw_pine_4_a'],
   ['PW_pine_6_a', 'bo_pw_pine_6_a']]),

 ('zl_fir', #except for last tree, uses different firs from pw_fir1-3, slightly taller, more trees per group
  fkf_tree|density(5),
  [['PL_fur1', 'bo_pl_fur1'],
   ['PL_fur2', 'bo_pl_fur2'],
   ['PL_fur3', 'bo_pl_fur3'],
   ['PW_pine_3_a', 'bo_pw_pine_3_a']]),

 ('zl_fir_tall',
  fkf_desert_forest|fkf_tree|density(5),
  [['PL_fur_tall1', 'bo_pl_fur_tall1'],
   ['PL_fur_tall2', 'bo_pl_fur_tall2'],
   ['PL_fur_tall3', 'bo_pl_fur_tall3']]),

 ('zl_fir_shubby', #similar to pw_fir_shubby_small_group, shares models with pw_fir_shibby
  fkf_desert_forest|fkf_tree|density(1),
  [['PW_tree_2_a', 'bo_PW_tree_2_a'], #smaller group
   ['PW_tree_2_b', 'bo_pw_tree_2_b'], #smaller group
   ['PW_tree_e_1', 'bo_pw_tree_e_1'], #bigger group
   ['PW_tree_e_2', 'bo_pw_tree_e_2'], #bigger group
   ['PW_tree_e_3', 'bo_pw_tree_e_3']]), #bigger group

 ('zl_fir_shubby_group', #same as pw_fir_shubby_group
  fkf_desert_forest|fkf_tree|density(2),
  [['PW_tree_6_a', 'bo_pw_tree_6_a'],
   ['PW_tree_6_b', 'bo_pw_tree_6_b'],
   ['PW_tree_6_c', 'bo_pw_tree_6_c'],
   ['PW_tree_6_d', 'bo_pw_tree_6_d']]),

 ('pw_fir_shubby_small_group', #similar to zl_fir_shubby
  fkf_desert_forest|fkf_tree|density(4),
  [['PW_tree_e_1', 'bo_pw_tree_e_1'],
   ['PW_tree_e_2', 'bo_pw_tree_e_2'],
   ['PW_tree_e_3', 'bo_pw_tree_e_3']]),

 ('pw_fir_shubby_group', #same as zl_fir_shubby_group
  fkf_tree,
  [['PW_tree_6_a', 'bo_pw_tree_6_a'],
   ['PW_tree_6_b', 'bo_pw_tree_6_b'],
   ['PW_tree_6_c', 'bo_pw_tree_6_c'],
   ['PW_tree_6_d', 'bo_pw_tree_6_d']]),
   
 ('pw_fir_shibby', #shares models with zl_fir_shubby
  fkf_desert_forest|fkf_tree|density(4),
  [['PW_tree_2_a', 'bo_PW_tree_2_a'],
   ['PW_tree_2_b', 'bo_pw_tree_2_b']]),

 ('zl_fir_shubby_single', #single standing trees, no fallen logs
  fkf_snow|fkf_desert_forest|fkf_tree|density(5),
  [['PW_tree_2_a_single1', 'bo_pw_tree_2_a_single1'],
   ['PW_tree_2_a_single2', '0'],
   ['PW_tree_2_a_single3', 'bo_pw_tree_2_a_single3'],
   ['PW_tree_2_a_single2_dark', '0']]),

 ('zl_birch_yellow', #same as pw_birch_yellow
  fkf_tree,
  [['PW_tree_4_a', 'bo_pw_tree_4_a'],
   ['PW_tree_4_b', 'bo_pw_tree_4_b']]),

#duplicate
 ('pw_birch_yellow',
  fkf_steppe_forest|fkf_tree|density(4),
  [['PW_tree_4_a', 'bo_pw_tree_4_a'],
   ['PW_tree_4_b', 'bo_pw_tree_4_b']]),

 ('zl_birch_green', #same as pw_birch_green
  fkf_tree,
  [['PW_tree_5_a', 'bo_pw_tree_5_a'],
   ['PW_tree_5_b', 'bo_pw_tree_5_b'],
   ['PW_tree_5_c', 'bo_pw_tree_5_c'],
   ['PW_tree_5_d', 'bo_pw_tree_5_d']]),

 ('pw_birch_green', #same as zl_birch_green, last model is a duplicate
  fkf_steppe_forest|fkf_tree|density(4),
  [['PW_tree_5_a', 'bo_pw_tree_5_a'],
   ['PW_tree_5_b', 'bo_pw_tree_5_b'],
   ['PW_tree_5_c', 'bo_pw_tree_5_c'],
   ['PW_tree_5_d', 'bo_pw_tree_5_d'],
   ['PW_tree_5_a_yellow', 'bo_pw_tree_5_a']]),

 ('zl_green2_group', #same as pw_leaf_green_group
  fkf_tree,
  [['PW_tree_8_a', 'bo_pw_tree_8_a'],
   ['PW_tree_8_b', 'bo_pw_tree_8_b'],
   ['PW_tree_8_c', 'bo_pw_tree_8_c']]),

 ('pw_leaf_green_group', #zl_green2_group
  0,
  [['PW_tree_8_a', 'bo_pw_tree_8_a'],
   ['PW_tree_8_b', 'bo_pw_tree_8_b'],
   ['PW_tree_8_c', 'bo_pw_tree_8_c']]),

 ('zl_skeleton_man',
  0,
  [['PW_tree_7_a', '0'], ['PW_tree_7_b', '0'], ['PW_tree_7_c', '0']]),

 ('zl_green_group_small', #pw_branchy_green_group
  fkf_tree,
  [['PW_tree_10_a', 'bo_pw_tree_10_a'],
   ['PW_tree_10_b', 'bo_pw_tree_10_b'],
   ['PW_tree_10_c', 'bo_pw_tree_10_c']]),

 ('zl_green_group_large', #pw_branchy_green_group2
  fkf_tree,
  [['PW_tree_11_a', 'bo_pw_tree_11_a'],
   ['PW_tree_11_b', 'bo_pw_tree_11_b'],
   ['PW_tree_11_c', 'bo_pw_tree_11_c']]),

 ('pw_branchy_green_group', #zl_green_group_small
  fkf_tree|density(4),
  [['PW_tree_10_a', 'bo_pw_tree_10_a'],
   ['PW_tree_10_b', 'bo_pw_tree_10_b'],
   ['PW_tree_10_c', 'bo_pw_tree_10_c']]),

 ('pw_branchy_green_group2', #zl_green_group_large
  fkf_tree|density(4),
  [['PW_tree_11_a', 'bo_pw_tree_11_a'],
   ['PW_tree_11_b', 'bo_pw_tree_11_b'],
   ['PW_tree_11_c', 'bo_pw_tree_11_c']]),

 ('zl_tree_12', #pw_pine_bushes_group , group of young firs
  fkf_plain_forest|fkf_tree|density(4),
  [['PW_tree_12_a', 'bo_pw_tree_12_a'],
   ['PW_tree_12_b', 'bo_pw_tree_12_b'],
   ['PW_tree_12_c', 'bo_pw_tree_12_c']]),

 ('pw_pine_bushes_group', #desert version of zl_tree_12
  fkf_desert|fkf_desert_forest|density(12),
  [['PW_tree_12_a', 'bo_pw_tree_12_a'],
   ['PW_tree_12_b', 'bo_pw_tree_12_b'],
   ['PW_tree_12_c', 'bo_pw_tree_12_c']]),

 ('zl_birch_tall', #same as pw_tall_leaf
  fkf_steppe_forest|fkf_tree|density(4),
  [['PW_tree_14_a', 'bo_pw_tree_14_a'],
   ['PW_tree_14_b', 'bo_pw_tree_14_b'],
   ['PW_tree_14_c', 'bo_pw_tree_14_c']]),

 ('pw_tall_leaf', #same as zl_birch_tall
  fkf_tree|density(4),
  [['PW_tree_14_a', 'bo_pw_tree_14_a'],
   ['PW_tree_14_b', 'bo_pw_tree_14_b'],
   ['PW_tree_14_c', 'bo_pw_tree_14_c']]),

 ('zl_tree_15', #same as pw_leaf_yellow2
  fkf_plain_forest|fkf_tree|density(4),
  [['PW_tree_15_a', 'bo_pw_tree_15_a'],
   ['PW_tree_15_b', 'bo_pw_tree_15_b'],
   ['PW_tree_15_c', 'bo_pw_tree_15_c']]),

 ('pw_leaf_yellow2', #same as zl_tree_15
  fkf_steppe_forest|fkf_tree|density(4),
  [['PW_tree_15_a', 'bo_pw_tree_15_a'],
   ['PW_tree_15_b', 'bo_pw_tree_15_b'],
   ['PW_tree_15_c', 'bo_pw_tree_15_c']]),

 ('zl_tree_16', #same as pw_pine_small_group, similar but different to pink_tree
  fkf_plain_forest|fkf_tree|density(4),
  [['PW_tree_16_a', 'bo_pw_tree_16_a'],
   ['PW_tree_16_b', 'bo_pw_tree_16_b']]),

 ('pw_pine_small_group', #same as zl_tree_16, similar to but smaller than pink_tree
  fkf_desert_forest|fkf_tree|density(38),
  [['PW_tree_16_a', 'bo_pw_tree_16_a'],
   ['PW_tree_16_b', 'bo_pw_tree_16_b']]),

 ('zl_birch_green_group', #same as pw_birch_green_group
  fkf_tree,
  [['PW_tree_17_a', 'bo_pw_tree_17_a'],
   ['PW_tree_17_b', 'bo_pw_tree_17_b'],
   ['PW_tree_17_c', 'bo_pw_tree_17_c'],
   ['PW_tree_17_d', 'bo_pw_tree_17_d']]),

 ('pw_birch_green_group', #same as zl_birch_green_group
  fkf_tree|density(4),
  [['PW_tree_17_a', 'bo_pw_tree_17_a'],
   ['PW_tree_17_b', 'bo_pw_tree_17_b'],
   ['PW_tree_17_c', 'bo_pw_tree_17_c'],
   ['PW_tree_17_d', 'bo_pw_tree_17_d']]),

 ('zl_birch_yellow_group', #same as pw_birch_yellow_group
  fkf_tree,
  [['PW_tree_18_a', 'bo_pw_tree_18_a'],
   ['PW_tree_18_b', 'bo_pw_tree_18_b']]),

 ('pw_birch_yellow_group', #same as zl_birch_yellow_group
  fkf_tree|density(4),
  [['PW_tree_18_a', 'bo_pw_tree_18_a'],
   ['PW_tree_18_b', 'bo_pw_tree_18_b']]),

 ('zl_aspen_yellow', #same as pw_leaf_yellow_group
  fkf_tree,
  [['PW_tree_f_1', 'bo_pw_tree_f_1'],
   ['PW_tree_f_2', 'bo_pw_tree_f_2'],
   ['PW_tree_f_3', 'bo_pw_tree_f_3']]),

 ('pw_leaf_yellow_group', #same as zl_aspen_yellow, big groups
  fkf_tree|density(4),
  [['PW_tree_f_1', 'bo_pw_tree_f_1'],
   ['PW_tree_f_2', 'bo_pw_tree_f_2'],
   ['PW_tree_f_3', 'bo_pw_tree_f_3']]),

 ('zl_aspen_yellow_group', #same as pw_leaf_yellow2_group
  fkf_tree,
  [['PW_tree_20_a', 'bo_pw_tree_20_a'], ['PW_tree_20_b', 'bo_pw_tree_20_b']]),

 ('pw_leaf_yellow2_group', #same as zl_aspen_yellow_group
  fkf_tree|density(3),
  [['PW_tree_20_a', 'bo_pw_tree_20_a'], ['PW_tree_20_b', 'bo_pw_tree_20_b']]),

 ('zl_aspen_yellow_bush',
  fkf_steppe|fkf_steppe_forest|fkf_tree|density(3),
  [['PL_aspen_yellowbush1', '0'],
   ['PL_aspen_yellowbush2', '0'],
   ['PL_aspen_yellowbush3', '0']]),

 ('zl_oak_group',
  fkf_plain|fkf_tree|density(2),
  [['PL_oak_group1', 'bo_pl_oak_group1'],
   ['PL_oak_group2', 'bo_pl_oak_group2'],
   ['PL_oak_group3', 'bo_pl_oak_group3']]),


 ('zl_rockformation',
  fkf_desert|fkf_desert_forest|fkf_steppe|fkf_realtime_ligting|fkf_rock|density(3),
  [['PW_rock_c', 'bo_pw_rock_c'],
   ['PW_rock_e', 'bo_pw_rock_e'],
   ['PW_rock_k', 'bo_pw_rock_k']]),

 ('zl_reed', fkf_snow|density(194), [['GA_reed1', '0']]),

 ('zl_fir_tall_hs',
  fkf_steppe_forest|fkf_desert_forest|fkf_tree|density(5),
  [['PW_fir_tall_d', 'bo_PW_fir_tall_d'],
   ['PW_fir_tall_f', 'bo_PW_fir_tall_f'],
   ['PW_fir_tall_h', 'bo_PW_fir_tall_h'],
   ['PW_fir_tall_i', 'bo_PW_fir_tall_i']]),

###CWE trees  
 ('CWE_oliva',
    fkf_tree|fkf_plain|density(2),					#InVain: added to plain (Gondor),
  [['cwe_oliva_tree_a', 'oliva_tree_a_col'],
   ['cwe_oliva_tree_b', 'oliva_tree_b_col'],
   ['cwe_oliva_tree_c', 'oliva_tree_c_col'],
   ['cwe_oliva_tree_d', 'oliva_tree_d_col'],
   ['cwe_oliva_tree_e', 'oliva_tree_e_col']]),  
  
 ('CWE_pihta',
    fkf_tree|fkf_plain|density(6),					#InVain: added to plain (Gondor),
  [['cwe_pihta_a', 'pihta_a_col'],
   ['cwe_pihta_b', 'pihta_b_col'],
   ['cwe_pihta_c', 'pihta_c_col']
   ]),    
  
 ('CWE_apple_tree',
  0,
  [['cwe_sp_apple_tree_1', 'bo_sp_apple_tree_1'],
   ['cwe_sp_apple_tree_2', 'bo_sp_apple_tree_2'],
   ['cwe_sp_apple_tree_3', 'bo_sp_apple_tree_3'],
   ['cwe_sp_apple_tree_4', 'bo_sp_apple_tree_4'],
   ['cwe_sp_apple_tree_5', 'bo_sp_apple_tree_5'],
   ['cwe_sp_apple_tree_6', 'bo_sp_apple_tree_6']
   ]),   
  
 ('CWE_magnolia',
    fkf_tree|fkf_plain|density(2),					#InVain: added to plain (Gondor)
  [['cwe_sp_magnolia_1', 'bo_sp_magnolia_1'],
   ['cwe_sp_magnolia_2', 'bo_sp_magnolia_2'],
   ['cwe_sp_magnolia_3', 'bo_sp_magnolia_3'],
   ['cwe_sp_magnolia_4', 'bo_sp_magnolia_4'],
   ['cwe_sp_magnolia_5', 'bo_sp_magnolia_5'],
   ]),     
  
 ('CWE_magnolia_large',
    fkf_tree|fkf_plain|density(2),					#InVain: added to plain (Gondor)
  [['cwe_sp_magnolia_large_1', 'bo_sp_magnolia_large_1'],
   ['cwe_sp_magnolia_large_2', 'bo_sp_magnolia_large_2'],
   ]),   
  
 ('CWE_peach_tree',
  0,
  [['cwe_sp_peach_tree_1', 'bo_sp_peach_tree_1'],
   ['cwe_sp_peach_tree_2', 'bo_sp_peach_tree_2'],
   ['cwe_sp_peach_tree_3', 'bo_sp_peach_tree_3'],
   ['cwe_sp_peach_tree_4', 'bo_sp_peach_tree_4'],
   ['cwe_sp_peach_tree_5', 'bo_sp_peach_tree_5'],
   ]),   

 ('CWE_bush_a',
    fkf_plain|density(10),					#InVain: added to plain (Gondor),
  [['cwe_sp_bush_a_1', '0'],
   ['cwe_sp_bush_a_2', '0'],
   ['cwe_sp_bush_a_3', '0'],
   ['cwe_sp_bush_a_4', '0'],
   ['cwe_sp_bush_a_5', '0'],
   ['cwe_sp_bush_a_6', '0'],
   ['cwe_sp_bush_a_7', '0'],
   ['cwe_sp_bush_a_8', '0'],
   ['cwe_sp_bush_a_9', '0'],
   ['cwe_sp_bush_a_10', '0']]),     
  
 ('CWE_bush_b',
    fkf_plain|density(10),					#InVain: added to plain (Gondor),
  [['cwe_sp_bush_b_1', '0'],
   ['cwe_sp_bush_b_2', '0'],
   ['cwe_sp_bush_b_3', '0'],
   ['cwe_sp_bush_b_4', '0'],
   ['cwe_sp_bush_b_5', '0'],
   ['cwe_sp_bush_b_6', '0'],
   ['cwe_sp_bush_b_7', '0'],
   ['cwe_sp_bush_b_8', '0'],
   ['cwe_sp_bush_b_9', '0'],
   ['cwe_sp_bush_b_10', '0']]), 

 ('CWE_small_bush_a',
    fkf_plain|density(10),					#InVain: added to plain (Gondor),
  [['cwe_sp_small_bush_a_1', '0'],
   ['cwe_sp_small_bush_a_2', '0'],
   ['cwe_sp_small_bush_a_3', '0'],
   ['cwe_sp_small_bush_a_4', '0'],
   ['cwe_sp_small_bush_a_5', '0'],
   ]),   

 ('CWE_small_bush_b',
    fkf_plain|density(10),					#InVain: added to plain (Gondor),
  [['cwe_sp_small_bush_b_1', '0'],
   ['cwe_sp_small_bush_b_2', '0'],
   ['cwe_sp_small_bush_b_3', '0'],
   ['cwe_sp_small_bush_b_4', '0'],
   ['cwe_sp_small_bush_b_5', '0'],
   ]), 

 ('CWE_juniper',
    fkf_plain|density(20),					#InVain: added to plain (Gondor),
  [['cwe_sp_juniper_1', '0'],
   ['cwe_sp_juniper_2', '0'],
   ['cwe_sp_juniper_3', '0'],
   ['cwe_sp_juniper_4', '0'],
   ]), 

 ('CWE_myrtle_a',
  0,
  [['cwe_sp_myrtle_a_1', 'bo_sp_myrtle_a_1'],
   ['cwe_sp_myrtle_a_2', 'bo_sp_myrtle_a_2'],
   ['cwe_sp_myrtle_a_3', 'bo_sp_myrtle_a_3'],
   ]),   

 ('CWE_myrtle_b',
    fkf_tree|fkf_plain|density(3),					#InVain: added to plain (Gondor),
  [['cwe_sp_myrtle_b_1', 'bo_sp_myrtle_b_1'],
   ['cwe_sp_myrtle_b_2', 'bo_sp_myrtle_b_2'],
   ['cwe_sp_myrtle_b_3', 'bo_sp_myrtle_b_3'],
   ['cwe_sp_myrtle_b_4', 'bo_sp_myrtle_b_4'],
   ['cwe_sp_myrtle_b_5', 'bo_sp_myrtle_b_5'],
   ]), 

 ('CWE_azalia',
    fkf_tree|fkf_plain|density(4),					#InVain: added to plain (Gondor),
  [['cwe_sp_azalia_1', '0'],
   ['cwe_sp_azalia_2', '0'],
   ['cwe_sp_azalia_3', '0'],
   ]),

 ('CWE_beech',
    fkf_tree|fkf_plain|density(2),	
  [['cwe_sp_beech_1', 'bo_sp_beech_1'],
   ['cwe_sp_beech_2', 'bo_sp_beech_2'],
   ['cwe_sp_beech_3', 'bo_sp_beech_3'],
   ['cwe_sp_beech_4', 'bo_sp_beech_4'],
   ['cwe_sp_beech_5', 'bo_sp_beech_5'],
   ]),    
   
 ('CWE_pine',
  0,
  [['cwe_sp_pine_1', 'bo_sp_pine_1'],
   ['cwe_sp_pine_2', 'bo_sp_pine_2'],
   ['cwe_sp_pine_3', 'bo_sp_pine_3'],
   ]),    

 ('CWE_pine_b',
  0,
  [['cwe_sp_pine_b_1', 'bo_sp_pine_b_1'],
   ['cwe_sp_pine_b_2', 'bo_sp_pine_b_2'],
   ['cwe_sp_pine_b_3', 'bo_sp_pine_b_3'],
   ['cwe_sp_pine_b_4', 'bo_sp_pine_b_4'],
   ]),   

 ('CWE_desert_flora_b',
  0,
  [['cwe_desert_flora_b_1', '0'],
   ['cwe_desert_flora_b_2', '0'],
   ['cwe_desert_flora_b_3', '0'],
   ['cwe_desert_flora_b_4', '0'],
   ['cwe_desert_flora_b_5', '0'],
   ]),
   
 ('CWE_desert_flora_c',
    fkf_plain|fkf_align_with_ground|density(3),	
  [['cwe_desert_flora_c_1', '0'],
   ['cwe_desert_flora_c_2', '0'],
   ['cwe_desert_flora_c_3', '0'],
   ]),   

 ('CWE_lavender',
  fkf_plain|fkf_align_with_ground|density(5),
  [['cwe_plain_flowers_lavender', '0'],
   ]),   

 ('CWE_tulips_red',
  0,
  [['cwe_plain_flowers_tulips', '0'],
   ]),  

 ('CWE_tulips_white',
  0,
  [['cwe_plain_flowers_white', '0'],
   ]),     
   
 ('CWE_sagebrush',
  fkf_plain|fkf_align_with_ground|density(6),
  [['cwe_sagebrush', '0'],
   ]),    
   
 ('CWE_reed',
  0,
  [['cwe_sedge_a_1', '0'],
   ['cwe_sedge_a_2', '0'],
   ['cwe_sedge_a_3', '0'],
   ['cwe_sedge_a_4', '0'],
   ['cwe_sedge_a_5', '0'],
   ['cwe_sedge_a_6', '0'],
   ['cwe_sedge_a_7', '0'],
   ]),   

 ('CWE_tropical_flora_a',
  0,
  [['cwe_tropical_flora_a_1', '0'],
   ['cwe_tropical_flora_a_2', '0'],
   ['cwe_tropical_flora_a_3', '0'],
   ['cwe_tropical_flora_a_4', '0'],
   ]), 

 ('CWE_yellow_flower_small',
  0,
  [['cwe_weed_11-111', '0'],
   ['cwe_weed_11a-111', '0'],
   ['cwe_weed_11b---111', '0'],
   ]),       
   
 ('CWE_yellow_flower_big',
  0,
  [['cwe_weed_14', '0'],
   ['cwe_weed_14a', '0'],
   ['cwe_weed_14b', '0'],
   ['cwe_weed_14c', '0'],
   ]),    
   
 ('CWE_weed_b_2',
  0,
  [['cwe_weed_b_2', '0'],
   ['cwe_weed_b_2a', '0'],
   ['cwe_weed_b_2b', '0'],
   ['cwe_weed_b_2c', '0'],
   ]), 
   
 ('CWE_weed_2',
  0,
  [['cwe_weed_2', '0'],
   ['cwe_weed_2a', '0'],
   ['cwe_weed_2b', '0'],
   ]), 

 ('CWE_weed_other',
  0,
  [['cwe_weed_5', '0'],
   ['cwe_weed_1', '0'],
   ['cwe_sa_kust_3', '0'],
   ['cwe_sa_kust_4', '0'],
   ]),    
   
 ('CWE_ivy',
  0,
  [['cwe_ivy_1', '0'],
  ['cwe_ivy_2', '0'],
   ]), 

 ('CWE_ivy_wall',
  0,
  [['cwe_ivy_wall', '0'],
   ]), 

 ('Jaakko_new_tree_a',
	fkf_plain|fkf_tree|density(4),
  [['Jaakko_new_tree_a', 'bo_Jaakko_new_tree_a'],
   ['Jaakko_new_tree_a_double', 'bo_Jaakko_new_tree_a_double'],
   ]),    
   
 ('Jaakko_new_cypress',
    fkf_plain|fkf_tree|density(4),					#InVain: added to plain (Gondor), 
  [['Jaakko_new_cypress', 'bo_Jaakko_new_cypress'],
   ['Jaakko_new_cypress2', 'bo_Jaakko_new_cypress2'],
   ]),    

 ('grass_flower_white_nofade',
  0,
  [['PW_grass_flower_c_xx', '0'], ['PW_grass_flower_c_xx', '0']]),

 ('grass_flower_yellow_nofade',
  0,
  [['PW_grass_flower_e_xx', '0'], ['PW_grass_flower_e_xx', '0']]),
  
 ('thranduil_ivy_single',
  0,
  [['thranduil_ivy_single', '0'],
   ]),
      
 ('dead_uruk',
  0,
  [['dead_uruk_1', '0'],
   ['dead_uruk_2', '0'],
   ['dead_uruk_3', '0'],
   ['dead_uruk_4', '0'],
   ['dead_uruk_5', '0'],
   ['dead_uruk_6', '0'],
   ['dead_uruk_7', '0'],
   ['dead_uruk_8', '0'],]), 
   
 ('dead_uruk_sitting',
  0,
  [['dead_uruk_sitting_1', '0'],
   ['dead_uruk_sitting_2', '0'],
   ['dead_uruk_sitting_3', '0'],]), 
 
 ('dead_orc',
  0,
  [['dead_orc_1', '0'],
   ['dead_orc_2', '0'],
   ['dead_orc_3', '0'],
   ['dead_orc_4', '0'],
   ['dead_orc_5', '0'],
   ['dead_orc_6', '0'],
   ['dead_orc_7', '0'],
   ['dead_orc_8', '0'],]), 
   
 ('dead_orc_sitting',
  0,
  [['dead_orc_sitting_1', '0'],
   ['dead_orc_sitting_2', '0'],
   ['dead_orc_sitting_3', '0'],]), 

 ('dead_man_corsair',
  0,
  [['dead_man_corsair_1', '0'],
   ['dead_man_corsair_2', '0'],
   ['dead_man_corsair_3', '0'],
   ['dead_man_corsair_4', '0'],
   ['dead_man_corsair_5', '0'],
   ['dead_man_corsair_6', '0'],
   ['dead_man_corsair_7', '0'],
   ['dead_man_corsair_8', '0'],]), 
   
 ('dead_man_corsair_sitting',
  0,
  [['dead_man_corsair_sitting_1', '0'],
   ['dead_man_corsair_sitting_2', '0'],
   ['dead_man_corsair_sitting_3', '0'],]), 
   
 ('dead_man_gondor',
  0,
  [['dead_man_gondor_1', '0'],
   ['dead_man_gondor_2', '0'],
   ['dead_man_gondor_3', '0'],
   ['dead_man_gondor_4', '0'],
   ['dead_man_gondor_5', '0'],
   ['dead_man_gondor_6', '0'],
   ['dead_man_gondor_7', '0'],
   ['dead_man_gondor_8', '0'],]), 
   
 ('dead_man_gondor_sitting',
  0,
  [['dead_man_gondor_sitting_1', '0'],
   ['dead_man_gondor_sitting_2', '0'],
   ['dead_man_gondor_sitting_3', '0'],]), 

 ('tree_stump',
  0,
  [['tree_stump_a', 'bo_tree_stump_a'],
   ['tree_stump_b', 'bo_tree_stump_b'],
   ['tree_stump_c', 'bo_tree_stump_c'],]),    

 ('tree_old',
  0,
  [['tree_huorn', 'bo_tree_huorn'],
   ['PL_oak_group_big_1', 'bo_pl_oak_group_big_1'],
   ['PL_oak_group_big_2', 'bo_pl_oak_group_big_2'],
   ['PL_oak_group_big_3', 'bo_pl_oak_group_big_3'],
   ['PL_oak_group_big_b_1', 'bo_pl_oak_group_big_1'],
   ['PL_oak_group_big_b_2', 'bo_pl_oak_group_big_2'],
   ['PL_oak_group_big_b_3', 'bo_pl_oak_group_big_3'],]),
 
 ('mirkwood_tree',
  0,
  [['tree_mirkwood_a', 'bo_tree_mallorn_a'],
   ['tree_mirkwood_b', 'bo_tree_mallorn_b'],
   ['tree_mirkwood_c', 'bo_tree_mallorn_c'],]),
   
 ('mushroom',
  fkf_plain_forest|density(4),
  [['mushroom1', '0'],
   ['mushroom2', '0'],
   ['mushroom3', '0'],
   ['mushroom4', '0'],
   ['mushroom5', '0'],]),
   

 ('fern_big',
  0,
  [['PW_fern_big', '0']]),

 ('mirkwood_roots',
  0,
  [['tree_mirkwood_roots_1', 'bo_tree_mirkwood_roots_1'],
   ['tree_mirkwood_roots_2', 'bo_tree_mirkwood_roots_2'],
   ['tree_mirkwood_roots_3', 'bo_tree_mirkwood_roots_3'],
   ['tree_mirkwood_roots_4', 'bo_tree_mirkwood_roots_4'],
   ['tree_mirkwood_roots_b_1', 'bo_tree_mirkwood_roots_1'],
   ['tree_mirkwood_roots_b_2', 'bo_tree_mirkwood_roots_2'],
   ['tree_mirkwood_roots_b_3', 'bo_tree_mirkwood_roots_3'],
   ['tree_mirkwood_roots_b_4', 'bo_tree_mirkwood_roots_4']]),   
]

def save_fauna_kinds():
  file = open("../"+export_dir+"/data/flora_kinds.txt","w")
  file.write("%d\n"%len(fauna_kinds))
  for fauna_kind in fauna_kinds:
    meshes_list = fauna_kind[2]
    file.write("%s %d %d\n"%(fauna_kind[0], (dword_mask & fauna_kind[1]), len(meshes_list)))
    for m in meshes_list:
      file.write(" %s "%(m[0]))
      if (len(m) > 1):
        file.write(" %s\n"%(m[1]))
      else:
        file.write(" 0\n")
      #print(fauna_kind)
      if ( fauna_kind[1] & (fkf_tree|fkf_speedtree) ):  #if this fails make sure that you have entered the alternative tree definition (NOT FUNCTIONAL in Warband)
        #swyter-- lolwtfbbq tw??
        #speedtree_alternative = m[2]
        #file.write(" %s %s\n"%(speedtree_alternative[0], speedtree_alternative[1]))
        file.write(" %s %s\n"%(0, 0))
    #if ( fauna_kind[1] & fkf_has_colony_props ):
    #  file.write(" %s %s\n"%(fauna_kind[3], fauna_kind[4]))
  file.close()

def two_to_pow(x):
  result = 1
  for i in xrange(x):
    result = result * 2
  return result

fauna_mask = 0x80000000000000000000000000000000
low_fauna_mask =             0x8000000000000000
def save_python_header():
  file = open("./fauna_codes.py","w")
  for i_fauna_kind in xrange(len(fauna_kinds)):
    file.write("%s_1 = 0x"%(fauna_kinds[i_fauna_kind][0]))
    file.write("%x\n"%(fauna_mask | two_to_pow(i_fauna_kind)))
    file.write("%s_2 = 0x"%(fauna_kinds[i_fauna_kind][0]))
    file.write("%x\n"%(fauna_mask | ((low_fauna_mask|two_to_pow(i_fauna_kind)) << 64)))
    file.write("%s_3 = 0x"%(fauna_kinds[i_fauna_kind][0]))
    file.write("%x\n"%(fauna_mask | ((low_fauna_mask|two_to_pow(i_fauna_kind)) << 64) | two_to_pow(i_fauna_kind)))
  file.close()

print "Exporting flora data..."
save_fauna_kinds()
