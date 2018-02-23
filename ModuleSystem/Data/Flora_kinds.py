from module_info import *
import string

dword      = 0x8000000000000000
dword_mask = 0xffffffffffffffff

density_bits      = 32
fkf_density_mask  = 0xFFFF #16K

#terain condition flags
fkf_plain             = 0x00000004
fkf_steppe            = 0x00000008
fkf_snow              = 0x00000010
fkf_desert            = 0x00000020
fkf_plain_forest      = 0x00000400
fkf_steppe_forest     = 0x00000800
fkf_snow_forest       = 0x00001000
fkf_desert_forest     = 0x00002000
fkf_terrain_mask      = 0x0000ffff

fkf_realtime_ligting  = 0x00010000 #deprecated
fkf_point_up          = 0x00020000 #uses auto-generated point-up(quad) geometry for the flora kind
fkf_align_with_ground = 0x00040000 #align the flora object with the ground normal
fkf_grass             = 0x00080000 #is grass
fkf_on_green_ground   = 0x00100000 #populate this flora on green ground
fkf_rock              = 0x00200000 #is rock 
fkf_tree              = 0x00400000 #is tree -> note that if you set this parameter, you should pass additional alternative tree definitions
fkf_snowy             = 0x00800000
fkf_guarantee         = 0x01000000

fkf_speedtree         = 0x02000000  #NOT FUNCTIONAL: we have removed speedtree support on M&B Warband

fkf_has_colony_props  = 0x04000000  # if fkf_has_colony_props -> then you can define colony_radius and colony_treshold of the flora kind


def density(g):
  if (g > fkf_density_mask):
    g = fkf_density_mask
  return ((dword | g) << density_bits)


fauna_kinds = [
 ('grass',
  fkf_plain|fkf_plain_forest|fkf_point_up|fkf_align_with_ground|fkf_grass|fkf_on_green_ground|fkf_guarantee|density(1500),
  [['PW_grass_yellow_e', '0'],
   ['PW_grass_a_xx', '0'],
   ['PW_grass_b_xx', '0'],
   ['PW_grass_b_xx', '0'],
   ['PW_grass_b_xx', '0'],
   ['PW_grass_e_xx', '0']]),
   
 ('grass_bush',
  fkf_plain|fkf_steppe|fkf_desert|fkf_steppe_forest|fkf_snow_forest|fkf_align_with_ground|fkf_grass|density(10),
  [['PW_grass_bush_a_xx', '0'], ['PW_grass_bush_b_xx', '0']]),
  
 ('grass_saz',
  fkf_plain|fkf_steppe|fkf_snow|fkf_steppe_forest|fkf_snow_forest|fkf_on_green_ground|fkf_guarantee|density(198),
  [['PW_grass_bush_c_xx', '0'], ['PW_grass_bush_c_xx', '0']]),
  
 ('grass_purple',
  fkf_plain|fkf_steppe|fkf_steppe_forest|fkf_grass|density(500),
  [['PW_grass_bush_e_xx', '0'], ['PW_grass_bush_e_xx', '0']]),
  
 ('fern',
  fkf_plain_forest|fkf_snow_forest|fkf_align_with_ground|fkf_grass|density(1000),
  [['PW_fern_a_xx', '0'], ['PW_fern_b_xx', '0']]),
  
 ('grass_steppe',
  fkf_steppe|fkf_desert|fkf_steppe_forest|fkf_desert_forest|fkf_point_up|fkf_align_with_ground|fkf_grass|fkf_on_green_ground|fkf_guarantee|density(1500),
  [['PW_grass_e_xx', '0'],
   ['PW_grass_yellow_b_xx', '0'],
   ['PW_grass_yellow_b_xx', '0'],
   ['PW_grass_e_xx', '0']]),
   
 ('grass_bush_g',
  fkf_plain|fkf_steppe|fkf_plain_forest|fkf_steppe_forest|fkf_align_with_ground|fkf_grass|density(400),
  [['PW_grass_bush_g01_xx', '0'],
   ['PW_grass_bush_g02_xx', '0'],
   ['PW_grass_bush_g03_xx', '0']]),
   
 ('grass_bush_h',
  fkf_plain|fkf_plain_forest|fkf_align_with_ground|fkf_grass|density(400),
  [['PW_grass_bush_h01_xx', '0'],
   ['PW_grass_bush_h02_xx', '0'],
   ['PW_grass_bush_h03_xx', '0']]),
   
 ('grass_bush_i',
  fkf_plain|fkf_plain_forest|fkf_align_with_ground|fkf_grass|density(400),
  [['PW_grass_bush_i01_xx', '0'], ['PW_grass_bush_i02_xx', '0']]),
  
 ('grass_bush_j',
  fkf_plain|fkf_steppe|fkf_plain_forest|fkf_steppe_forest|fkf_align_with_ground|fkf_grass|density(400),
  [['PW_grass_bush_j01_xx', '0'], ['PW_grass_bush_j02_xx', '0']]),
  
 ('grass_bush_k',
  fkf_plain|fkf_plain_forest|fkf_align_with_ground|fkf_grass|density(400),
  [['PW_grass_bush_k01_xx', '0'], ['PW_grass_bush_k02_xx', '0']]),
  
 ('grass_bush_l',
  fkf_plain|fkf_plain_forest|fkf_align_with_ground|density(50),
  [['PW_grass_bush_l01', '0'], ['PW_grass_bush_l02', '0']]),
  
 ('thorn_a',
  fkf_plain|fkf_plain_forest|fkf_align_with_ground|density(50),
  [['PW_thorn_a', '0'],
   ['PW_thorn_b', '0'],
   ['PW_thorn_c', '0'],
   ['PW_thorn_d', '0']]),
   
 ('basak',
  fkf_steppe|fkf_desert|fkf_steppe_forest|fkf_desert_forest|density(70),
  [['PW_basak_xx', '0']]),
  
 ('common_plant',
  fkf_steppe|fkf_desert|fkf_steppe_forest|fkf_desert_forest|density(70),
  [['PW_common_plant_xx', '0']]),
  
 ('small_plant',
  fkf_plain|fkf_steppe|fkf_plain_forest|fkf_steppe_forest|fkf_align_with_ground|density(50),
  [['PW_big_bush_xx', '0']]),
  
 ('buddy_plant',
  fkf_plain|fkf_plain_forest|density(50),
  [['PW_buddy_plant_xx', '0'], ['PW_buddy_plant_b_xx', '0']]),

 ('yellow_flower',
  fkf_plain|fkf_plain_forest|fkf_align_with_ground|density(50),
  [['PW_yellow_flower', '0'], ['PW_yellow_flower_b', '0']]),

 ('spiky_plant',
  fkf_plain|fkf_plain_forest|fkf_snow_forest|fkf_align_with_ground|density(50),
  [['PW_spiky_plant', '0']]),

 ('seedy_plant',
  fkf_plain|fkf_steppe|fkf_plain_forest|fkf_steppe_forest|density(50),
  [['PW_big_bush_xx', '0']]),

 ('blue_flower',
  fkf_plain|fkf_plain_forest|density(30),
  [['PW_blue_flower_xx', '0']]),

 ('big_bush',
  fkf_plain|fkf_steppe|fkf_plain_forest|fkf_steppe_forest|density(30),
  [['PW_big_bush_xx', '0']]),

 ('bushes02_a',
  fkf_plain|fkf_snow|fkf_steppe_forest|density(30),
  [['PW_bushes02_a', 'bo_pw_bushes02_a'],
   ['PW_bushes02_b', 'bo_pw_bushes02_a'],
   ['PW_bushes02_c', 'bo_pw_bushes02_a']]),

 ('bushes03_a',
  fkf_snow|fkf_desert|fkf_plain_forest|fkf_snow_forest|fkf_desert_forest|density(54),
  [['PW_bushes03_a_xx', '0'],
   ['PW_bushes03_b_xx', '0'],
   ['PW_bushes03_c_xx', '0']]),

 ('bushes04_a',
  fkf_plain|fkf_steppe|fkf_snow|fkf_desert|fkf_plain_forest|fkf_steppe_forest|fkf_desert_forest|density(102),
  [['PW_bushes04_a_xx', '0'],
   ['PW_bushes04_b_xx', '0'],
   ['PW_bushes04_c_xx', '0']]),

 ('bushes05_a',
  fkf_steppe|fkf_desert|fkf_steppe_forest|density(70),
  [['PW_bushes05_a_xx', '0']]),

 ('bushes06_a',
  fkf_plain|fkf_steppe|fkf_snow|fkf_desert|fkf_plain_forest|fkf_steppe_forest|fkf_desert_forest|density(102),
  [['PW_bushes06_a_xx', '0'],
   ['PW_bushes06_b_xx', '0'],
   ['PW_bushes06_c_xx', '0']]),

 ('bushes07_a',
  fkf_snow|fkf_desert|fkf_plain_forest|fkf_snow_forest|fkf_desert_forest|density(102),
  [['PW_bushes07_a_xx', '0'],
   ['PW_bushes07_b_xx', '0'],
   ['PW_bushes07_c_xx', '0']]),

 ('bushes08_a',
  fkf_plain|fkf_steppe|fkf_plain_forest|fkf_steppe_forest|density(70),
  [['PW_bushes08_a_xx', '0'],
   ['PW_bushes08_b_xx', '0'],
   ['PW_bushes08_c_xx', '0']]),

 ('bushes09_a',
  fkf_snow|fkf_desert|fkf_snow_forest|fkf_desert_forest|density(102),
  [['PW_bushes09_a', '0'], ['PW_bushes09_b', '0'], ['PW_bushes09_c', '0']]),

 ('bushes10_a',
  fkf_plain_forest|density(70),
  [['PW_bushes10_a', 'bo_pw_bushes10_a'],
   ['PW_bushes10_b', 'bo_pw_bushes10_b'],
   ['PW_bushes10_c', 'bo_pw_bushes10_c']]),

 ('bushes11_a',
  fkf_steppe|fkf_steppe_forest|fkf_snow|fkf_desert|fkf_plain_forest|fkf_snow_forest|fkf_desert_forest|density(70),
  [['PW_bushes11_a', '0'], ['PW_bushes11_b', '0'], ['PW_bushes11_c', '0']]),

 ('bushes12_a',
  fkf_steppe|fkf_steppe_forest|fkf_align_with_ground|density(50),
  [['PW_bushes12_a_xx', '0'],
   ['PW_bushes12_b_xx', '0'],
   ['PW_bushes12_c_xx', '0']]),

 ('aspen',
  fkf_steppe|fkf_steppe_forest|fkf_realtime_ligting|fkf_rock|density(22),
  [['aspen_a', 'bo_aspen_a'],
   ['aspen_b', 'bo_aspen_b'],
   ['aspen_c', 'bo_aspen_c']]),

 ('pw_small_rock_group',
  fkf_steppe|fkf_desert|fkf_steppe_forest|fkf_desert_forest|fkf_realtime_ligting|fkf_rock|density(22),
  [['PW_aspen_a', '0'], ['PW_aspen_b', '0'], ['PW_aspen_c', '0']]),

 ('pine_1',
  fkf_plain_forest|fkf_desert_forest|fkf_tree|density(4),
  [['pine_1_a', 'bo_pine_1_a'], ['pine_1_b', 'bo_pine_1_b']]),

 ('pw_fir',
  fkf_tree|density(4),
  [['PW_pine_1_a_xx', 'bo_pw_pine_1_a'],
   ['PW_pine_1_b_xx', 'bo_pw_pine_1_b']]),

 ('pine_2',
  fkf_plain_forest|fkf_desert_forest|fkf_tree|density(4),
  [['pine_2_a', 'bo_pine_2_a']]),

 ('pw_fir2', fkf_tree|density(4), [['PW_pine_2_a_xx', 'bo_pw_pine_2_a']]),

 ('pine_3',
  fkf_plain_forest|fkf_desert_forest|fkf_tree|density(4),
  [['pine_3_a', 'bo_pine_3_a']]),

 ('pw_fir3', fkf_tree|density(4), [['PW_pine_3_a_xx', 'bo_pw_pine_3_a']]),

 ('pine_4',
  fkf_plain_forest|fkf_desert_forest|fkf_tree|density(4),
  [['pine_4_a', 'bo_pine_4_a']]),

 ('pw_pine_group2',
  fkf_desert_forest|fkf_tree|density(2),
  [['PW_pine_4_a', 'bo_pw_pine_4_a_cyl']]),

 ('pine_6',
  fkf_plain_forest|fkf_desert_forest|fkf_tree|density(4),
  [['pine_6_a', 'bo_pine_6_a']]),

 ('pw_pine_group1',
  fkf_desert_forest|fkf_tree|density(2),
  [['PW_pine_6_a', 'bo_pw_pine_6_a_cyl']]),

 ('snowy_pine', fkf_tree, [['PW_tree_snowy_a', 'bo_pw_tree_snowy_a']]),

 ('snowy_pine_2', fkf_tree, [['PW_snowy_pine_2', 'bo_pw_snowy_pine_2']]),

 ('small_rock',
  fkf_steppe|fkf_plain_forest|fkf_steppe_forest|fkf_tree|density(4),
  [['PW_rock_a', 'bo_PW_rock_a'],
   ['PW_rock_b', 'bo_PW_rock_b']]),

 ('rock_snowy',
  fkf_tree,
  [['PW_rock_snowy_a', 'bo_pw_rock_snowy_a'],
   ['PW_rock_snowy_b', 'bo_pw_rock_snowy_b'],
   ['PW_rock_snowy_c', 'bo_pw_rock_snowy_c']]),

 ('tree_1', fkf_plain_forest|density(6), [['PW_tree_9_a_xx', '0']]),

 ('tree_2', 0, [['tree_2_a', 'bo_tree_2_a'], ['tree_2_b', 'bo_tree_2_b']]),

 ('pw_fir_shibby',
  fkf_snow_forest|fkf_desert_forest|fkf_tree|density(4),
  [['PW_tree_2_a', 'bo_pw_tree_2_a_cyl'],
   ['PW_tree_2_b', 'bo_pw_tree_2_b_cyl']]),

 ('tree_3',
  fkf_plain|fkf_realtime_ligting|fkf_tree|density(5),
  [['tree_3_a', 'bo_tree_3_a'], ['tree_3_b', 'bo_tree_3_b']]),

 ('pw_gray_bush',
  fkf_snow|fkf_desert|fkf_snow_forest|fkf_realtime_ligting|fkf_tree|density(5),
  [['PW_tree_3_a_gray', '0'], ['PW_tree_3_b_gray', '0']]),

 ('tree_4',
  fkf_plain_forest|fkf_tree|density(4),
  [['tree_4_a', 'bo_tree_4_a'], ['tree_4_b', 'bo_tree_4_b']]),

 ('pw_birch_yellow',
  fkf_tree|density(4),
  [['PW_tree_4_a', 'bo_pw_tree_4_a_cyl'],
   ['PW_tree_4_b', 'bo_pw_tree_4_b_cyl']]),

 ('tree_5',
  fkf_plain_forest|density(70),
  [['tree_5_a', 'bo_tree_5_a'],
   ['tree_5_b', 'bo_tree_5_b'],
   ['tree_5_c', 'bo_tree_5_c'],
   ['tree_5_d', 'bo_tree_5_d']]),

 ('pw_birch_green',
  density(70),
  [['PW_tree_5_a', 'bo_pw_tree_5_a_cyl'],
   ['PW_tree_5_b', 'bo_pw_tree_5_b_cyl'],
   ['PW_tree_5_c', 'bo_pw_tree_5_c_cyl'],
   ['PW_tree_5_d', 'bo_pw_tree_5_d_cyl'],
   ['PW_tree_5_a_yellow', 'bo_pw_tree_5_a_cyl']]),

 ('tree_6',
  fkf_plain|fkf_tree|density(5),
  [['tree_6_a', 'bo_tree_6_a'],
   ['tree_6_b', 'bo_tree_6_b'],
   ['tree_6_c', 'bo_tree_6_c'],
   ['tree_6_d', 'bo_tree_6_d']]),

 ('pw_fir_shubby_group',
  fkf_tree,
  [['PW_tree_6_a', 'bo_pw_tree_6_a'],
   ['PW_tree_6_b', 'bo_pw_tree_6_b'],
   ['PW_tree_6_c', 'bo_pw_tree_6_c'],
   ['PW_tree_6_d', 'bo_pw_tree_6_d']]),

 ('tree_7',
  0,
  [['tree_7_a', 'bo_tree_7_a'],
   ['tree_7_b', 'bo_tree_7_b'],
   ['tree_7_c', 'bo_tree_7_c']]),

 ('pw_man_skeleton',
  0,
  [['PW_tree_7_a_color', '0'],
   ['PW_tree_7_b_color', '0'],
   ['PW_tree_7_c_color', '0']]),

 ('tree_8',
  fkf_plain|fkf_plain_forest|fkf_tree|density(4),
  [['tree_8_a', 'bo_tree_8_a'],
   ['tree_8_b', 'bo_tree_8_b'],
   ['tree_8_c', 'bo_tree_8_c']]),

 ('pw_leaf_green_group',
  0,
  [['PW_tree_8_a', 'bo_pw_tree_8_a'],
   ['PW_tree_8_b', 'bo_pw_tree_8_b'],
   ['PW_tree_8_c', 'bo_pw_tree_8_c']]),

 ('tree_9',
  fkf_plain_forest|fkf_tree|density(50),
  [['tree_9_a', 'bo_tree_9_a'],
   ['tree_9_b', 'bo_tree_9_a'],
   ['tree_9_c', 'bo_tree_9_a']]),

 ('pw_ground_thorn',
  0,
  [['PW_tree_9_a_xx', '0'], ['PW_tree_9_a_xx', '0'], ['PW_tree_9_a_xx', '0']]),

 ('tree_10',
  fkf_plain_forest|fkf_tree|density(4),
  [['tree_10_a', 'bo_tree_10_a'],
   ['tree_10_b', 'bo_tree_10_a'],
   ['tree_10_c', 'bo_tree_10_a']]),

 ('pw_branchy_green_group',
  fkf_steppe_forest|fkf_tree|density(4),
  [['PW_tree_10_a', 'bo_pw_tree_10_a'],
   ['PW_tree_10_b', 'bo_pw_tree_10_a'],
   ['PW_tree_10_c', 'bo_pw_tree_10_a']]),

 ('tree_11',
  fkf_plain_forest|fkf_plain|fkf_tree|density(4),
  [['tree_11_a', 'bo_tree_11_a'],
   ['tree_11_b', 'bo_tree_11_a'],
   ['tree_11_c', 'bo_tree_11_a']]),

 ('pw_branchy_green_group2',
  fkf_steppe_forest|fkf_tree|density(4),
  [['PW_tree_11_a', 'bo_pw_tree_11_a'],
   ['PW_tree_11_b', 'bo_pw_tree_11_a'],
   ['PW_tree_11_c', 'bo_pw_tree_11_a']]),

 ('tree_12',
  fkf_steppe_forest|fkf_tree|density(4),
  [['tree_12_a', 'bo_tree_12_a'],
   ['tree_12_b', 'bo_tree_12_b'],
   ['tree_12_c', 'bo_tree_12_c']]),

 ('pw_pine_bushes_group',
  fkf_desert|fkf_desert_forest|fkf_guarantee|density(12),
  [['PW_tree_12_a_xx', 'bo_pw_tree_12_a'],
   ['PW_tree_12_b_xx', 'bo_pw_tree_12_b'],
   ['PW_tree_12_c_xx', 'bo_pw_tree_12_c']]),

 ('tree_14',
  fkf_tree,
  [['tree_14_a', 'bo_tree_14_a'],
   ['tree_14_b', 'bo_tree_14_b'],
   ['tree_14_c', 'bo_tree_14_c']]),

 ('pw_tall_leaf',
  fkf_tree,
  [['PW_tree_14_a', 'bo_pw_tree_14_a_cyl'],
   ['PW_tree_14_b', 'bo_pw_tree_14_b_cyl'],
   ['PW_tree_14_c', 'bo_pw_tree_14_c_cyl']]),

 ('tree_15',
  fkf_tree|density(64),
  [['tree_15_a', 'bo_tree_15_a'],
   ['tree_15_b', 'bo_tree_15_b'],
   ['tree_15_c', 'bo_tree_15_c']]),

 ('pw_leaf_yellow2',
  fkf_steppe_forest|fkf_tree|density(70),
  [['PW_tree_15_a', 'bo_pw_tree_15_a_cyl'],
   ['PW_tree_15_b', 'bo_pw_tree_15_b_cyl'],
   ['PW_tree_15_c', 'bo_pw_tree_15_c_cyl']]),

 ('tree_16',
  fkf_plain_forest|fkf_tree|density(38),
  [['tree_16_a', 'bo_tree_16_a'], ['tree_16_b', 'bo_tree_16_b']]),

 ('pw_pine_small_group',
  fkf_snow_forest|fkf_desert_forest|fkf_tree|density(38),
  [['PW_tree_16_a', 'bo_pw_tree_16_a_cyl'],
   ['PW_tree_16_b', 'bo_pw_tree_16_b_cyl']]),

 ('tree_17',
  fkf_plain_forest|fkf_tree|density(4),
  [['tree_17_a', 'bo_tree_17_a'],
   ['tree_17_b', 'bo_tree_17_b'],
   ['tree_17_c', 'bo_tree_17_c'],
   ['tree_17_d', 'bo_tree_17_d']]),

 ('pw_birch_green_group',
  fkf_tree|density(4),
  [['PW_tree_17_a', 'bo_pw_tree_17_a'],
   ['PW_tree_17_b', 'bo_pw_tree_17_b'],
   ['PW_tree_17_c', 'bo_pw_tree_17_c'],
   ['PW_tree_17_d', 'bo_pw_tree_17_d']]),

 ('tree_plane',
  fkf_plain_forest|fkf_tree|density(4),
  [['tree_18_a', 'bo_tree_18_a'], ['tree_18_b', 'bo_tree_18_b']]),

 ('pw_birch_yellow_group',
  fkf_tree|density(4),
  [['PW_tree_18_a', 'bo_pw_tree_18_a_cyl'],
   ['PW_tree_18_b', 'bo_pw_tree_18_b_cyl']]),

 ('tree_19',
  fkf_plain_forest|fkf_tree|density(4),
  [['tree_19_a', 'bo_tree_19_a']]),

 ('pw_snow_bushes', density(4), [['PW_tree_19_a', '0']]),

 ('beech',
  fkf_plain_forest|fkf_tree|density(3),
  [['tree_20_a', 'bo_tree_20_a'], ['tree_20_b', 'bo_tree_20_b']]),

 ('pw_leaf_yellow2_group',
  fkf_steppe_forest|fkf_tree|density(3),
  [['PW_tree_20_a', 'bo_pw_tree_20_a'], ['PW_tree_20_b', 'bo_pw_tree_20_b']]),

 ('tall_tree',
  fkf_plain_forest|fkf_plain|fkf_tree|density(4),
  [['tall_tree_a', 'bo_tall_tree_a']]),

 ('pw_pine_group3',
  fkf_desert_forest|fkf_tree|density(2),
  [['PW_tall_tree_a', 'bo_pw_tall_tree_a_cyl']]),

 ('tree_e',
  fkf_plain|fkf_plain_forest|fkf_tree|density(4),
  [['tree_e_1', 'bo_tree_e_1'],
   ['tree_e_2', 'bo_tree_e_2'],
   ['tree_e_3', 'bo_tree_e_3']]),

 ('pw_fir_shubby_small_group',
  fkf_steppe_forest|fkf_desert_forest|fkf_tree|density(4),
  [['PW_tree_e_1', 'bo_pw_tree_e_1'],
   ['PW_tree_e_2', 'bo_pw_tree_e_2'],
   ['PW_tree_e_3', 'bo_pw_tree_e_3']]),

 ('tree_f',
  fkf_tree,
  [['tree_f_1', 'bo_tree_f_1'],
   ['tree_f_2', 'bo_tree_f_1'],
   ['tree_f_3', 'bo_tree_f_1']]),

 ('pw_leaf_yellow_group',
  fkf_steppe_forest|fkf_tree|density(4),
  [['PW_tree_f_1', 'bo_pw_tree_f_1'],
   ['PW_tree_f_2', 'bo_pw_tree_f_1'],
   ['PW_tree_f_3', 'bo_pw_tree_f_1']]),

 ('grape_vineyard', 0, [['grape_vineyard', 'bo_grape_vineyard']]),

 ('grape_vineyard_stake',
  0,
  [['grape_vineyard_stake', 'bo_grape_vineyard_stake']]),

 ('wheat',
  0,
  [['wheat_a', '0'], ['wheat_b', '0'], ['wheat_c', '0'], ['wheat_d', '0']]),

 ('zl_fir',
  fkf_tree|density(5),
  [['PL_fur1', 'bo_pl_fur1'],
   ['PL_fur2', 'bo_pl_fur2'],
   ['PL_fur3', 'bo_pl_fur3'],
   ['PW_pine_3_a_xx', 'bo_pw_pine_3_a']]),

 ('zl_fir_tall',
  fkf_steppe|fkf_snow_forest|fkf_desert_forest|fkf_tree|density(5),
  [['PL_fur_tall1', 'bo_pl_fur_tall1'],
   ['PL_fur_tall2', 'bo_pl_fur_tall2'],
   ['PL_fur_tall3', 'bo_pl_fur_tall3']]),

 ('zl_fir_shubby',
  fkf_snow_forest|fkf_desert_forest|fkf_tree|density(1),
  [['PW_tree_2_a', 'bo_pw_tree_2_a_cyl'],
   ['PW_tree_2_b', 'bo_pw_tree_2_b_cyl'],
   ['PW_tree_e_1', 'bo_pw_tree_e_1'],
   ['PW_tree_e_2', 'bo_pw_tree_e_2'],
   ['PW_tree_e_3', 'bo_pw_tree_e_3']]),

 ('zl_birch_yellow',
  fkf_tree,
  [['PW_tree_4_a', 'bo_pw_tree_4_a_cyl'],
   ['PW_tree_4_b', 'bo_pw_tree_4_b_cyl']]),

 ('zl_birch_green',
  fkf_tree,
  [['PW_tree_5_a', 'bo_pw_tree_5_a_cyl'],
   ['PW_tree_5_b', 'bo_pw_tree_5_b_cyl'],
   ['PW_tree_5_c', 'bo_pw_tree_5_c_cyl'],
   ['PW_tree_5_d', 'bo_pw_tree_5_d_cyl']]),

 ('zl_fir_shubby_group',
  fkf_desert_forest|fkf_tree|density(2),
  [['PW_tree_6_a', 'bo_pw_tree_6_a'],
   ['PW_tree_6_b', 'bo_pw_tree_6_b'],
   ['PW_tree_6_c', 'bo_pw_tree_6_c'],
   ['PW_tree_6_d', 'bo_pw_tree_6_d']]),

 ('zl_green2_group',
  fkf_tree,
  [['PW_tree_8_a', 'bo_pw_tree_8_a'],
   ['PW_tree_8_b', 'bo_pw_tree_8_b'],
   ['PW_tree_8_c', 'bo_pw_tree_8_c']]),

 ('zl_skeleton_man',
  0,
  [['PW_tree_7_a', '0'], ['PW_tree_7_b', '0'], ['PW_tree_7_c', '0']]),

 ('zl_green_group_small',
  fkf_tree,
  [['PW_tree_10_a', 'bo_pw_tree_10_a'],
   ['PW_tree_10_b', 'bo_pw_tree_10_b'],
   ['PW_tree_10_c', 'bo_pw_tree_10_c']]),

 ('zl_green_group_large',
  fkf_tree,
  [['PW_tree_11_a', 'bo_pw_tree_11_a'],
   ['PW_tree_11_b', 'bo_pw_tree_11_b'],
   ['PW_tree_11_c', 'bo_pw_tree_11_c']]),

 ('zl_tree_12',
  fkf_plain_forest|fkf_steppe_forest|fkf_tree|density(4),
  [['PW_tree_12_a_xx', 'bo_pw_tree_12_a'],
   ['PW_tree_12_b_xx', 'bo_pw_tree_12_b'],
   ['PW_tree_12_c_xx', 'bo_pw_tree_12_c']]),

 ('zl_birch_tall',
  fkf_tree|density(4),
  [['PW_tree_14_a', 'bo_pw_tree_14_a_cyl'],
   ['PW_tree_14_b', 'bo_pw_tree_14_b_cyl'],
   ['PW_tree_14_c', 'bo_pw_tree_14_c_cyl']]),

 ('zl_tree_15',
  fkf_plain_forest|fkf_steppe_forest|fkf_tree|density(4),
  [['PW_tree_15_a', 'bo_pw_tree_15_a_cyl'],
   ['PW_tree_15_b', 'bo_pw_tree_15_b_cyl'],
   ['PW_tree_15_c', 'bo_pw_tree_15_c_cyl']]),

 ('zl_tree_16',
  fkf_plain_forest|fkf_tree|density(4),
  [['PW_tree_16_a', 'bo_pw_tree_16_a_cyl'],
   ['PW_tree_16_b', 'bo_pw_tree_16_b_cyl']]),

 ('zl_birch_green_group',
  fkf_tree,
  [['PW_tree_17_a', 'bo_pw_tree_17_a'],
   ['PW_tree_17_b', 'bo_pw_tree_17_b'],
   ['PW_tree_17_c', 'bo_pw_tree_17_c'],
   ['PW_tree_17_d', 'bo_pw_tree_17_d']]),

 ('zl_birch_yellow_group',
  fkf_tree,
  [['PW_tree_18_a', 'bo_pw_tree_18_a_cyl'],
   ['PW_tree_18_b', 'bo_pw_tree_18_b_cyl']]),

 ('zl_aspen_yellow',
  fkf_tree,
  [['PW_tree_f_1', 'bo_pw_tree_f_1'],
   ['PW_tree_f_2', 'bo_pw_tree_f_2'],
   ['PW_tree_f_3', 'bo_pw_tree_f_3']]),

 ('zl_aspen_yellow_group',
  fkf_tree,
  [['PW_tree_20_a', 'bo_pw_tree_20_a'], ['PW_tree_20_b', 'bo_pw_tree_20_b']]),

 ('zl_aspen_yellow_bush',
  fkf_tree,
  [['PL_aspen_yellowbush1', '0'],
   ['PL_aspen_yellowbush2', '0'],
   ['PL_aspen_yellowbush3', '0']]),

 ('zl_oak_group',
  fkf_plain|fkf_tree|density(2),
  [['PL_oak_group1', 'bo_pl_oak_group1'],
   ['PL_oak_group2', 'bo_pl_oak_group2'],
   ['PL_oak_group3', 'bo_pl_oak_group3']]),

 ('zl_bush_white_flowers',
  0,
  [['PW_grass_bush_l01', '0'], ['PW_grass_bush_l02', '0']]),

 ('zl_bush_08',
  0,
  [['PW_bushes08_a_xx', '0'],
   ['PW_bushes08_b_xx', '0'],
   ['PW_bushes08_c_xx', '0']]),

 ('zl_fir_bush',
  fkf_steppe|fkf_desert|fkf_snow_forest|fkf_desert_forest|density(10),
  [['PW_bushes09_a', '0'], ['PW_bushes09_b', '0'], ['PW_bushes09_c', '0']]),

 ('zl_birch_green_bush',
  0,
  [['PW_bushes10_a', '0'], ['PW_bushes10_b', '0'], ['PW_bushes10_c', '0']]),

 ('zl_shalebush',
  fkf_desert_forest|density(2),
  [['PW_bushes11_a', '0'], ['PW_bushes11_b', '0'], ['PW_bushes11_c', '0']]),

 ('zl_bush_steppe_wheat',
  0,
  [['PW_bushes12_a_xx', '0'],
   ['PW_bushes12_b_xx', '0'],
   ['PW_bushes12_c_xx', '0']]),

 ('zl_pink_tree',
  fkf_tree|fkf_plain|density(10),					#InVain: added to plain (Gondor)
  [['PW_tall_tree_a', 'bo_pw_tall_tree_a_cyl'],
   ['PW_pine_4_a', 'bo_pw_pine_4_a_cyl'],
   ['PW_pine_6_a', 'bo_pw_pine_6_a_cyl']]),

 ('zl_rockformation',
  fkf_desert|fkf_desert_forest|fkf_realtime_ligting|fkf_rock|density(1),
  [['PW_rock_c', 'bo_pw_rock_c'],
   ['PW_rock_e', 'bo_pw_rock_e']]),

 ('zl_white_flowers',
  fkf_align_with_ground|fkf_grass|density(2),
  [['PW_grass_bush_l01', '0'], ['PW_grass_bush_l02', '0']]),

 ('zl_yellow_flowers',
  fkf_align_with_ground|fkf_grass|density(2),
  [['PW_spiky_plant', '0']]),

 ('rock',
  fkf_plain_forest|fkf_snow_forest|fkf_tree|density(70),
  [['PW_pine_1_a_xx', 'bo_pw_pine_1_a'],
   ['PW_pine_1_b_xx', 'bo_pw_pine_1_b']]),

 ('rock_snowy2', fkf_tree, [['PW_tree_snowy_b', 'bo_pw_tree_snowy_b']]),

 ('zl_reed', fkf_snow|fkf_guarantee|density(194), [['GA_reed1', '0']]),

 ('ga_grass_snow',
  fkf_snow|fkf_snow_forest|fkf_align_with_ground|fkf_grass|fkf_on_green_ground|fkf_guarantee|density(1666),
  [['PW_grass_a_xx', '0'],
   ['PW_grass_b_xx', '0'],
   ['PW_grass_b_xx', '0'],
   ['PW_grass_b_xx', '0'],
   ['PW_grass_e_xx', '0']]),

 ('ga_bushes04_a_snow',
  fkf_snow|fkf_snow_forest|fkf_align_with_ground|fkf_guarantee|density(390),
  [['PW_bushes04_a_xx', '0'],
   ['PW_bushes04_b_xx', '0'],
   ['PW_bushes04_c_xx', '0']]),

 ('ga_grass_desert',
 #fkf_desert|fkf_desert_forest|fkf_align_with_ground|fkf_grass|fkf_on_green_ground|fkf_guarantee|fkf_has_colony_props|density(2012),
  fkf_desert|fkf_desert_forest|fkf_align_with_ground|fkf_grass|fkf_on_green_ground|fkf_guarantee|density(2012),
  [['PW_grass_e_xx', '0'],
   ['PW_grass_yellow_b_xx', '0'],
   ['PW_grass_yellow_b_xx', '0'],
   ['PW_grass_e_xx', '0']]),

 ('zl_fir_tall_hs',
  fkf_snow_forest|fkf_desert_forest|fkf_tree|density(5),
  [['PW_rock_d', 'bo_pw_rock_d'],
   ['PW_rock_f', 'bo_pw_rock_f'],
   ['PW_rock_i', 'bo_pw_rock_i'],
   ['PW_pine_1_a_xx', 'bo_pw_rock_f']]),

 ('zl_fir_shubby_single',
  fkf_snow|fkf_desert_forest|fkf_tree|density(5),
  [['PW_tree_2_a_single1', 'bo_pw_tree_2_a_single1'],
   ['PW_tree_2_a_single2', '0'],
   ['PW_tree_2_a_single3', 'bo_pw_tree_2_a_single3'],
   ['PW_tree_2_a_single2_dark', '0']]),

 ('ga_tree_3_a_brown',
  fkf_desert|fkf_desert_forest|density(22),
  [['PW_tree_3_a_brown', '0'], ['PW_tree_3_b_brown', '0']]),
  

###CWE trees  
 ('CWE_oliva',
    fkf_tree|density(2),					#InVain: added to plain (Gondor), #removed due to terrain bug
  [['cwe_oliva_tree_a', 'oliva_tree_a_col'],
   ['cwe_oliva_tree_b', 'oliva_tree_b_col'],
   ['cwe_oliva_tree_c', 'oliva_tree_c_col'],
   ['cwe_oliva_tree_d', 'oliva_tree_d_col'],
   ['cwe_oliva_tree_e', 'oliva_tree_e_col']]),  
  
 ('CWE_pihta',
    fkf_tree|density(6),					#InVain: added to plain (Gondor),#removed due to terrain bug
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
    fkf_tree|density(2),					#InVain: added to plain (Gondor),#removed due to terrain bug
  [['cwe_sp_magnolia_1', 'bo_sp_magnolia_1'],
   ['cwe_sp_magnolia_2', 'bo_sp_magnolia_2'],
   ['cwe_sp_magnolia_3', 'bo_sp_magnolia_3'],
   ['cwe_sp_magnolia_4', 'bo_sp_magnolia_4'],
   ['cwe_sp_magnolia_5', 'bo_sp_magnolia_5'],
   ]),     
  
 ('CWE_magnolia_large',
    fkf_tree|density(2),					#InVain: added to plain (Gondor), #removed due to terrain bug
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
    fkf_tree|density(7),					#InVain: added to plain (Gondor),
  [['cwe_sp_myrtle_b_1', 'bo_sp_myrtle_b_1'],
   ['cwe_sp_myrtle_b_2', 'bo_sp_myrtle_b_2'],
   ['cwe_sp_myrtle_b_3', 'bo_sp_myrtle_b_3'],
   ['cwe_sp_myrtle_b_4', 'bo_sp_myrtle_b_4'],
   ['cwe_sp_myrtle_b_5', 'bo_sp_myrtle_b_5'],
   ]), 

 ('CWE_azalia',
    fkf_tree|density(7),					#InVain: added to plain (Gondor),
  [['cwe_sp_azalia_1', '0'],
   ['cwe_sp_azalia_2', '0'],
   ['cwe_sp_azalia_3', '0'],
   ]),

 ('CWE_beech',
  0,
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
  0,
  [['cwe_desert_flora_c_1', '0'],
   ['cwe_desert_flora_c_2', '0'],
   ['cwe_desert_flora_c_3', '0'],
   ]),   

 ('CWE_lavender',
  fkf_align_with_ground|density(50),
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
  fkf_align_with_ground|density(50),
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
   
 ('cwe_weed_2',
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
  0,
  [['Jaakko_new_tree_a', 'bo_Jaakko_new_tree_a'],
   ['Jaakko_new_tree_a_double', 'bo_Jaakko_new_tree_a_double'],
   ]),    
   
 ('Jaakko_new_cypress',
    fkf_tree|density(4),					#InVain: added to plain (Gondor), #aaand removed due to terrain showing up in other regions (bug)
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
