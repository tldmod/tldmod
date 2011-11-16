from header_skins import *
from ID_particle_systems import *
####################################################################################################################
#  Each skin record contains the following fields:
#  1) Skin id: used for referencing skins.
#  2) Skin flags. Not used yet. Should be 0.
#  3) Body mesh.
#  4) Calf mesh (left one).
#  5) Hand mesh (left one).
#  6) Head mesh.
#  7) Face keys (list)
#  8) List of hair meshes.
#  9) List of beard meshes.
# 10) List of hair textures.
# 11) List of beard textures.
# 12) List of face textures.
# 13) List of voices.
# 14) Skeleton name
# 15) Scale (doesn't fully work yet)
# 16) Blood particles 1 (do not add this if you wish to use the default particles)
# 17) Blood particles 2 (do not add this if you wish to use the default particles)
# 17) Face key constraints (do not add this if you do not wish to use it)
####################################################################################################################

#TLD - significantly modified module_skins.py (Hokie)

uruk_face_keys = [
(10,0,-0.5,1.5, "Wieght"),
(20,0,-0.5,1.5, "Mouth Shape"),
(30,0,-0.5,1.25, "Eyelids"),
(40,0,1.25,-0.25, "Eye to Eye Dist"),
(50,0,-0.5,1.5, "Eye Size"),
(60,0,-0.5,1.5, "Eye Slant"),
(70,0, 1.0,-1.0, "Frawn"),
(80,0,-0.5,1.5, "Eyebrow Position"),
(90,0, 1.5,-0.5, "Mouth Width"),

(100,0,-0.5,1.5, "Mouth Vert Pos"),
(110,0,-0.5,1.5, "Mouth to Nose Dist"),

(120,0,-0.5,1.5, "Nose Size"),
(130,0,-0.5,1.5, "Nose Width"),
(140,0,-0.5,1.5, "Cheeks"),

(150,0,-0.5,1.5, "Chin Width"),
(160,0,-0.5,1.5, "Chin Size"),
(170,0,-0.5,1.5, "Cheek Bones"),

(180,0,0.0,1.0, "Post-Edit"),
]

man_face_keys = [
(20,0, 0.7,-0.6, "Chin Size"),
(260,0, -0.6,1.4, "Chin Shape"),
(10,0,-0.5,0.9, "Chin Forward"),
(240,0,0.9,-0.8, "Jaw Width"),
(210,0,-0.5,1.0, "Jaw Position"),
(250,0,0.8,-1.0, "Mouth-Nose Distance"),
(200,0,-0.3,1.0, "Mouth Width"),
(50,0,-1.5,1.0, "Cheeks"),

(60,0,-0.4,1.35, "Nose Height"),
(70,0,-0.6,0.7, "Nose Width"),
(80,0,1.0,-0.1, "Nose Size"),
(270,0,-0.5,1.0, "Nose Shape"),
(90,0,-0.2,1.4, "Nose Bridge"),

(100,0,-0.3,1.5, "Cheek Bones"),
(150,0,-0.2,3.0, "Eye Width"),
(110,0,1.5,-0.9, "Eye to Eye Dist"),
(120,0,1.9,-1.0, "Eye Shape"),
(130,0,-0.5, 1.1, "Eye Depth"),
(140,0,1.0,-1.2, "Eyelids"),

(160,0,1.3,-0.2, "Eyebrow Position"),
(170,0,-0.1,1.9, "Eyebrow Height"),
(220,0,-0.1,0.9, "Eyebrow Depth"),
(180,0,-1.1,1.6, "Eyebrow Shape"),
(230,0,1.2,-0.7, "Temple Width"),

(30,0,-0.6,0.9, "Face Depth"),
(40,0,0.9,-0.6, "Face Ratio"),
(190,0,0.0,0.95, "Face Width"),

(280,0,0.0,1.0, "Post-Edit"),
]

elf_face_keys = [
(20,0, 0.7,-0.6, "Chin Size"),
(260,0, -0.6,1.4, "Chin Shape"),
(10,0,-0.5,0.9, "Chin Forward"),
(240,0,0.9,-0.3, "Jaw Width"),
(210,0,-0.5,0.5, "Jaw Position"),
(250,0,0.8,-1.0, "Mouth-Nose Distance"),
(200,0,-0.3,0.4, "Mouth Width"),
(50,0,-1.5,0.5, "Cheeks"),

(60,0,-0.4,1.35, "Nose Height"),
(70,0,-0.6,-0.2, "Nose Width"),
(80,0,1.0,0.2, "Nose Size"),
(270,0,-0.5,1.0, "Nose Shape"),
(90,0,-0.2,1.4, "Nose Bridge"),

(100,0,-0.3,1.5, "Cheek Bones"),
(150,0,-0.2,3.0, "Eye Width"),
(110,0,1.1,-0.5, "Eye to Eye Dist"),
(120,0,0.9,-1.0, "Eye Shape"),
(130,0,-0.5, 1.1, "Eye Depth"),
(140,0,1.0,-1.2, "Eyelids"),

(160,0,1.0,-0.2, "Eyebrow Position"),
(170,0,-0.1,1.9, "Eyebrow Height"),
(220,0,-0.1,0.9, "Eyebrow Depth"),
(180,0,-0.5,1.6, "Eyebrow Shape"),
(230,0,1.2,-0.7, "Temple Width"),

(30,0,-0.6,0.9, "Face Depth"),
(40,0,0.9,-0.6, "Face Ratio"),
(190,0,0.0,0.95, "Face Width"),

(280,0,0.0,1.0, "Post-Edit"),
]


orc_face_keys = [
(20,0, 0.7,-0.6, "Chin Size"),
(260,0, -0.6,1.4, "Chin Shape"),
(10,0,-0.5,0.9, "Chin Forward"),
(240,0,0.9,-0.8, "Jaw Width"),
(210,0,-0.5,1.0, "Jaw Position"),
(250,0,0.8,-1.0, "Mouth-Nose Distance"),
(200,0,-0.3,1.0, "Mouth Width"),
(50,0,-1.5,1.0, "Cheeks"),

(60,0,-0.4,1.35, "Snout Height"),
(70,0,-0.6,0.7, "Snout Width"),
(80,0,1.0,-1.0, "Snout Size"),
(270,0,-0.5,1.0, "Snout Shape"),
(90,0,-0.2,1.4, "Nose Bridge"),

(100,0,-0.3,1.5, "Cheek Bones"),
(150,0,-0.2,3.0, "Eye Width"),
(110,0,1.5,-0.9, "Eye to Eye Dist"),
(120,0,1.9,-1.0, "Eye Shape"),
(130,0,-0.5, 1.1, "Eye Depth"),
(140,0,1.0,-1.2, "Eyelids"),

(160,0,1.3,-0.2, "Eyebrow Position"),
(170,0,-0.1,1.9, "Eyebrow Height"),
(220,0,-0.1,0.9, "Eyebrow Depth"),
(180,0,-1.1,1.6, "Eyebrow Shape"),
(230,0,1.2,-0.7, "Temple Width"),

(30,0,-0.6,0.9, "Face Depth"),
(40,0,0.9,-0.6, "Face Ratio"),
(190,0,0.0,0.95, "Face Width"),

(280,0,0.0,1.0, "Post-Edit"),
]

dwarf_face_keys = [
(20,0, 0.7,-0.6, "Chin Size"),
(260,0, -0.6,1.4, "Chin Shape"),
(10,0,-0.5,0.9, "Chin Forward"),
(240,0,0.9,-0.8, "Jaw Width"),
(210,0,-0.5,1.0, "Jaw Position"),
(250,0,0.8,-1.0, "Mouth-Nose Distance"),
(200,0,-0.3,1.0, "Mouth Width"),
(50,0,-1.5,1.0, "Cheeks"),

(60,0,-0.4,1.35, "Nose Height"),
(70,0,-0.6,0.7, "Nose Width"),
(80,0,1.0,-0.1, "Nose Size"),
(270,0,-0.5,1.0, "Nose Shape"),
(90,0,-0.2,1.4, "Nose Bridge"),

(100,0,-0.3,1.5, "Cheek Bones"),
(150,0,-0.2,3.0, "Eye Width"),
(110,0,1.5,-0.9, "Eye to Eye Dist"),
(120,0,1.9,-1.0, "Eye Shape"),
(130,0,-0.5, 1.1, "Eye Depth"),
(140,0,1.0,-1.2, "Eyelids"),

(160,0,1.3,-0.2, "Eyebrow Position"),
(170,0,-0.1,1.9, "Eyebrow Height"),
(220,0,-0.1,0.9, "Eyebrow Depth"),
(180,0,-1.1,1.6, "Eyebrow Shape"),
(230,0,1.2,-0.7, "Temple Width"),

(30,0,-0.6,0.9, "Face Depth"),
(40,0,0.9,-0.6, "Face Ratio"),
(190,0,0.0,0.95, "Face Width"),

(280,0,0.0,1.0, "Post-Edit"),
]

# Face width-Jaw width Temple width
woman_face_keys = [
(230,0,0.8,-1.0, "Chin Size"), 
(220,0,-1.0,1.0, "Chin Shape"), 
(10,0,-1.2,1.0, "Chin Forward"),
(20,0, -0.6, 1.2, "Jaw Width"), 
(40,0,-0.7,1.0, "Jaw Position"),
(270,0,0.9,-0.9, "Mouth-Nose Distance"),
(30,0,-0.5,1.0, "Mouth Width"),
(50,0, -0.5,1.0, "Cheeks"),

(60,0,-0.5,1.0, "Nose Height"),
(70,0,-0.5,1.1, "Nose Width"),
(80,0,1.5,-0.3, "Nose Size"),
(240,0,-1.0,0.8, "Nose Shape"),
(90,0, 0.0,1.1, "Nose Bridge"),

(100,0,-0.5,1.5, "Cheek Bones"),
(150,0,-0.4,1.0, "Eye Width"),
(110,0,1.0,0.0, "Eye to Eye Dist"),
(120,0,-0.2,1.0, "Eye Shape"),
(130,0,-0.1,1.6, "Eye Depth"),
(140,0,-0.2,1.0, "Eyelids"),


(160,0,-0.2,1.2, "Eyebrow Position"),
(170,0,-0.2,0.7, "Eyebrow Height"),
(250,0,-0.4,0.9, "Eyebrow Depth"),
(180,0,-1.5,1.2, "Eyebrow Shape"),
(260,0,1.0,-0.7, "Temple Width"),

(200,0,-0.5,1.0, "Face Depth"),
(210,0,-0.5,0.9, "Face Ratio"),
(190,0,-0.4,0.8, "Face Width"),

(280,0,0.0,1.0, "Post-Edit"),
]


gondor_face_keys = man_face_keys
rohan_face_keys = man_face_keys
dunlander_face_keys = man_face_keys
haradrim_face_keys = man_face_keys
easterling_face_keys = man_face_keys
troll_face_keys = []
dunedain_face_keys = man_face_keys
lothlorien_face_keys = elf_face_keys
rivendell_face_keys = elf_face_keys
mirkwood_face_keys = elf_face_keys
evil_male_face_keys = man_face_keys

chin_size = 0
chin_shape = 1
chin_forward = 2
jaw_width = 3
jaw_position = 4
mouth_nose_distance = 5
mouth_width = 6
cheeks = 7
nose_height = 8
nose_width = 9
nose_size = 10
nose_shape = 11
nose_bridge = 12
cheek_bones = 13
eye_width = 14
eye_to_eye_dist = 15
eye_shape = 16
eye_depth = 17
eyelids = 18
eyebrow_position = 19
eyebrow_height = 20
eyebrow_depth = 21
eyebrow_shape = 22
temple_width = 23
face_depth = 24
face_ratio = 25
face_width = 26

comp_less_than = -1;
comp_greater_than = 1;

skins = [
 ( "man", 0,
   "man_body", "man_calf_l", "m_handL",
   "male_head", man_face_keys,
   ["man_hair_s","man_hair_m","man_hair_n","man_hair_o", "man_hair_y10", "man_hair_y12","man_hair_p","man_hair_r","man_hair_q","man_hair_v","man_hair_t","man_hair_y6","man_hair_y3","man_hair_y7","man_hair_y9","man_hair_y11","man_hair_u","man_hair_y","man_hair_y2","man_hair_y4"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",
   ["beard_e","beard_d","beard_k","beard_l","beard_i","beard_j","beard_z","beard_m","beard_n","beard_y","beard_p","beard_o",   "beard_v", "beard_f", "beard_b", "beard_c","beard_t","beard_u","beard_r","beard_s","beard_a","beard_h","beard_g",], #beard meshes ,"beard_q"
   ["hair_blonde"], #hair textures
   ["beard_blonde"], #beard_materials
   [("manface_young_2" ,0xffcbe0e0,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff502a19]),
    ("manface_midage"  ,0xffdfefe1,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),
    ("manface_young"   ,0xffd0e0e0,["hair_blonde"],[0xff83301a, 0xff502a19, 0xff19100c, 0xff0c0d19]),     
    ("manface_young_3" ,0xffdceded,["hair_blonde"],[0xff2f180e, 0xff171313, 0xff07080c]),
    ("manface_7"       ,0xffc0c8c8,["hair_blonde"],[0xff171313, 0xff07080c]),
    ("manface_midage_2",0xfde4c8d8,["hair_blonde"],[0xff502a19, 0xff19100c, 0xff0c0d19]),
    ("manface_rugged"  ,0xffb0aab5,["hair_blonde"],[0xff171313, 0xff07080c]),
    ], #man_face_textures,
    [(voice_die,"snd_man_die"),(voice_hit,"snd_man_hit"),(voice_grunt,"snd_man_grunt"),(voice_grunt_long,"snd_man_grunt_long"),(voice_yell,"snd_man_yell"),(voice_victory,"snd_man_victory")], #voice sounds
    "skel_human", 1.0,
    psys_game_blood,psys_game_blood_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),  
#1  
  ( "woman", skf_use_morph_key_30,
    "woman_body",  "woman_calf_l", "f_handL",
    "female_head", woman_face_keys,
    ["woman_hair_p","woman_hair_n","woman_hair_o","woman_hair_q","woman_hair_r","woman_hair_t","woman_hair_s","welf_hair_1","welf_hair_2","welf_hair_3","welf_hair_4","welf_hair_5","welf_hair_6", "welf_hair_7","welf_hair_8"], #woman_hair_meshes
    [],
    ["hair_blonde"], #hair textures
    [],
    [("womanface_young",0xffe3e8ef,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c]),
     ("womanface_b"    ,0xffdfdfdf,["hair_blonde"],[0xffa5481f, 0xff502a19, 0xff19100c, 0xff0c0d19]), #0xffa5481f, 0xff502a19, 0xff19100c, 0xff0c0d19
     ("womanface_a"    ,0xffe8dfe5,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c]), #0xff502a19, 0xff19100c, 0xff0c0d19
     ("womanface_brown",0xffaf9f7e,["hair_blonde"],[0xff19100c, 0xff0c0d19, 0xff07080c]),
	 ("womanface_elf"  ,0xffe3e8ef,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c]),
     ],#woman_face_textures
    [(voice_die,"snd_woman_die"),(voice_hit,"snd_woman_hit")], #voice sounds
    "skel_human", 1.0,
    psys_game_blood,psys_game_blood_2,
  ),

########################################################################################################################  
#2
  ( "gondor", 0,
    "man_body", "man_calf_l", "m_handL",
    "male_head", gondor_face_keys,
    ["man_hair_s","man_hair_m","man_hair_n","man_hair_o", "man_hair_y10", "man_hair_y12","man_hair_p","man_hair_r","man_hair_q","man_hair_v","man_hair_t","man_hair_y6","man_hair_y3","man_hair_y7","man_hair_y9","man_hair_y11","man_hair_u","man_hair_y","man_hair_y2","man_hair_y4"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",
    ["beard_e","beard_d","beard_k","beard_l","beard_i","beard_j","beard_z","beard_m","beard_n","beard_y","beard_p","beard_o",   "beard_v", "beard_f", "beard_b", "beard_c","beard_t","beard_u","beard_r","beard_s","beard_a","beard_h","beard_g",], #beard meshes ,"beard_q"
    ["hair_blonde"], #hair textures
    ["beard_blonde"], #beard_materials
    [("manface_young_2" ,0xffcbe0e0,["hair_blonde"],[0xff120808, 0xff502a19, 0xffb04717,]),
     ("manface_midage"  ,0xffdfefe1,["hair_blonde"],[0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),
     ("manface_young"   ,0xffd0e0e0,["hair_blonde"],[0xff502a19, 0xff19100c, 0xff0c0d19]),     
     ("manface_young_3" ,0xffdceded,["hair_blonde"],[0xff2f180e, 0xff171313, 0xff07080c]),
     ("manface_7"       ,0xffc0c8c8,["hair_blonde"],[0xff171313, 0xff07080c]),
     ("manface_midage_2",0xfde4c8d8,["hair_blonde"],[0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("manface_rugged"  ,0xffb0aab5,["hair_blonde"],[0xff171313, 0xff07080c]),
     ], #man_face_textures,
    [(voice_die,"snd_man_die"),(voice_hit,"snd_man_hit"),(voice_grunt,"snd_man_grunt"),(voice_grunt_long,"snd_man_grunt_long"),(voice_yell,"snd_gondor_yell"),(voice_victory,"snd_gondor_victory")], #voice sounds
    "skel_human", 1.0,
    psys_game_blood,psys_game_blood_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),  
########################################################################################################################  
#3
  ( "rohan", 0,
    "man_body", "man_calf_l", "m_handL",
    "male_head", rohan_face_keys,
    ["man_hair_o", "man_hair_n","man_hair_q","man_hair_r", "man_hair_p"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",
    ["beard_i","beard_r","beard_q","beard_b","beard_u","beard_c","beard_e","beard_h","beard_m","beard_n","beard_o","beard_v","beard_y"], #beard meshes
    ["hair_blonde"], #hair textures
    ["beard_blonde"], #beard_materials
	[("manface_young"   ,0xffd0e0e0,["hair_blonde"],[0xffffffff, 0xfffffbaf, 0xfffff98e, 0xfffff67f, 0xffffd999, 0xffffc896]),     
	 ("manface_young_2" ,0xffcbe0e0,["hair_blonde"],[0xffffffff, 0xfffffbaf, 0xfffff98e, 0xfffff67f, 0xffffd999, 0xffffc896]),
     ("rohan_face_a"    ,0xffcbe0e0,["hair_blonde"],[0xffffffff, 0xfffffbaf, 0xfffff98e, 0xfffff67f, 0xffffd999, 0xffffc896]),
     ("rohan_face_b"    ,0xffdfefe1,["hair_blonde"],[0xffffffff, 0xfffffbaf, 0xfffff98e, 0xfffff67f, 0xffffd999, 0xffffc896]),
     ("manface_midage"  ,0xffdfefe1,["hair_blonde"],[0xffffffff, 0xfffffbaf, 0xfffff98e, 0xfffff67f, 0xffffd999, 0xffffc896]),
#     ("rohan_face_c",0xffd0e0e0,["hair_blonde"],[0xffffffff, 0xfffffbaf, 0xfffff98e, 0xfffff67f, 0xffffd999, 0xffffc896]),     
#     ("rohan_face_d",0xffdceded,["hair_blonde"],[0xffffffff, 0xfffffbaf, 0xfffff98e, 0xfffff67f, 0xffffd999, 0xffffc896]),    
#     ("rohan_face_e",0xffdceded,["hair_blonde"],[0xffffffff, 0xfffffbaf, 0xfffff98e, 0xfffff67f, 0xffffd999, 0xffffc896]),    
#     ("rohan_face_f",0xffdceded,["hair_blonde"],[0xffffffff, 0xfffffbaf, 0xfffff98e, 0xfffff67f, 0xffffd999, 0xffffc896]),    
#     ("rohan_face_g",0xffdceded,["hair_blonde"],[0xffffffff, 0xfffffbaf, 0xfffff98e, 0xfffff67f, 0xffffd999, 0xffffc896]),    
#     ("rohan_face_h",0xffdceded,["hair_blonde"],[0xffffffff, 0xfffffbaf, 0xfffff98e, 0xfffff67f, 0xffffd999, 0xffffc896]),    
     ], #man_face_textures,
    [(voice_die,"snd_man_die"),(voice_hit,"snd_man_hit"),(voice_grunt,"snd_man_grunt"),(voice_grunt_long,"snd_man_grunt_long"),(voice_yell,"snd_rohan_yell"),(voice_victory,"snd_rohan_victory")], #voice sounds
    "skel_human", 1.0,
    psys_game_blood,psys_game_blood_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),  
########################################################################################################################  
#4 
 (  "dunland", 0,
    "man_body", "man_calf_l", "m_handL",
    "male_head", dunlander_face_keys,
    ["man_hair_s","man_hair_m","man_hair_n","man_hair_o", "man_hair_p","man_hair_r","man_hair_q"], #man_hair_meshes
    ["beard_r","beard_n","beard_m","beard_j","beard_i","beard_g","beard_e",  "beard_z","beard_y","beard_v",], #beard meshes
    ["hair_blonde"], #hair textures
    ["beard_blonde"], #beard_materials
    [("manface_midage"    ,0xffdfefe1,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),
     ("manface_rugged"    ,0xffb0aab5,["hair_blonde"],[0xff171313, 0xff07080c]),
     ("east_bandit_face_a",0xfde4c8d8,["hair_blonde"],[0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("east_bandit_face_b",0xffb0aab5,["hair_blonde"],[0xff171313, 0xff07080c]),
     ("east_bandit_face_c",0xff807c8a,["hair_blonde"],[0xff120808, 0xff07080c]),     
     ("wildman_face_a"    ,0xffdceded,["hair_blonde"],[0xff2f180e, 0xff171313, 0xff07080c]),
     ("wildman_face_b"    ,0xffc0c8c8,["hair_blonde"],[0xff171313, 0xff07080c]),
     ], #man_face_textures,
    [(voice_die,"snd_man_die"),(voice_hit,"snd_man_hit"),(voice_grunt,"snd_man_grunt"),(voice_grunt_long,"snd_man_grunt_long"),(voice_yell,"snd_dunlender_yell"),(voice_victory,"snd_dunlender_victory")], #voice sounds
    "skel_human", 0.9,
    psys_game_blood,psys_game_blood_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),    
########################################################################################################################  
#5
  ( "orc", skf_use_morph_key_20,
    "orc_body", "orc_calf_l", "o_handL",
    "orc_head", orc_face_keys,
    ["orc_ears01","orc_ears02","orc_ears03","orc_ears04", "orc_hair01","orc_hair02","orc_hair03","orc_hair04","orc_hair05","orc_hair06","orc_hair07","orc_hair08","orc_hair09","orc_hair10","orc_hair11"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",
    [], #beard meshes ,
    ["orc_hair_ears"], #hair textures
    ["orc_hair_ears"], #beard_materials
    [("face_orc_a",0xffffffff,["orc_hair_ears"],[0xffffffff]),
     ("face_orc_b",0xffffffff,["orc_hair_ears"],[0xffffffff]),
     ("face_orc_c",0xffffffff,["orc_hair_ears"],[0xffffffff]),     
     ], #man_face_textures,
    [(voice_die,"snd_orc_die"),(voice_hit,"snd_orc_hit"),(voice_grunt,"snd_orc_grunt"),(voice_grunt_long,"snd_orc_grunt_long"),(voice_yell,"snd_orc_yell"),(voice_victory,"snd_orc_victory")], #voice sounds
    "skel_orc", 1.0,
    psys_game_blood_black,psys_game_blood_black_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ), 
########################################################################################################################  
#6
  ( "urukhai", 0,
    "urukhai_body", "urukhai_calf_l", "uh_handL",
    "urukhai_head", uruk_face_keys,
    ["uruk_ears01","uruk_ears02","uruk_hair01","uruk_hair02","uruk_hair03","uruk_hair04","uruk_hair05"], 
    ["uruk_teeth01","uruk_teeth02","uruk_teeth03","uruk_teeth04","uruk_teeth05","uruk_teeth06","uruk_teeth07","uruk_teeth08",], #beard meshes
    ["orc_hair_ears"], #hair textures
    ["orc_hair_ears"], #beard_materials
	[("face_urukhai_a",0xffffffff,["orc_hair_ears"],[0xffffffff]),     
     ("face_urukhai_b",0xffffffff,["orc_hair_ears"],[0xffffffff]),     
     ("face_urukhai_c",0xffffffff,["orc_hair_ears"],[0xffffffff]), 
     ], #man_face_textures,
    [(voice_die,"snd_uruk_die"),(voice_hit,"snd_uruk_hit"),(voice_grunt,"snd_uruk_grunt"),(voice_grunt_long,"snd_uruk_grunt_long"),(voice_yell,"snd_uruk_yell"),(voice_victory,"snd_uruk_victory")], #voice sounds
    "skel_uruk", 1.0,
    psys_game_blood_black,psys_game_blood_black_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),  
########################################################################################################################  
#7
  ( "uruk", 0,
    "uruk_body", "uruk_calf_l", "u_handL",
    "uruk_head", uruk_face_keys,
    ["uruk_ears01","uruk_ears02","uruk_hair01","uruk_hair02","uruk_hair03","uruk_hair04","uruk_hair05"], 
    ["uruk_teeth01","uruk_teeth02","uruk_teeth03","uruk_teeth04","uruk_teeth05","uruk_teeth06","uruk_teeth07","uruk_teeth08",], #beard meshes
    ["orc_hair_ears"], #hair textures
    ["orc_hair_ears"], #beard_materials
	[("face_uruk_a",0xffffffff,["orc_hair_ears"],[0xffffffff]),
     ("face_uruk_b",0xffffffff,["orc_hair_ears"],[0xffffffff]),
     ("face_uruk_c",0xffffffff,["orc_hair_ears"],[0xffffffff]),     
     ], #man_face_textures,
    [(voice_die,"snd_uruk_die"),(voice_hit,"snd_uruk_hit"),(voice_grunt,"snd_uruk_grunt"),(voice_grunt_long,"snd_uruk_grunt_long"),(voice_yell,"snd_uruk_yell"),(voice_victory,"snd_uruk_victory")], #voice sounds
    "skel_uruk", 0.9,
    psys_game_blood_black,psys_game_blood_black_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),  ########################################################################################################################  
#8 
 (  "harad", 0,
    "harad_tribesman", "harad_man_calf_l", "harad_m_handL",
    "male_head", haradrim_face_keys,
    ["man_hair_s","man_hair_m","man_hair_n","man_hair_o", "man_hair_y10", "man_hair_y12","man_hair_p","man_hair_r","man_hair_q","man_hair_v","man_hair_t","man_hair_y6","man_hair_y3","man_hair_y7","man_hair_y9","man_hair_y11","man_hair_u","man_hair_y","man_hair_y2","man_hair_y4"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",
    [], #beard meshes ,"beard_q"
    ["hair_blonde"], #hair textures
    ["beard_blonde"], #beard_materials
    [("harad_face_a",0xffcbe0e0,["hair_blonde"],[0xff120808, 0xff07080c]),
     ("harad_face_b",0xffdfefe1,["hair_blonde"],[0xff120808, 0xff07080c]),
     ("harad_face_c",0xffd0e0e0,["hair_blonde"],[0xff120808, 0xff07080c]),     
     ("harad_face_d",0xffdceded,["hair_blonde"],[0xff120808, 0xff07080c]),
     ("harad_face_e",0xffc0c8c8,["hair_blonde"],[0xff120808, 0xff07080c]),
     ], #man_face_textures,
    [(voice_die,"snd_haradrim_die"),(voice_hit,"snd_man_hit"),(voice_grunt,"snd_man_grunt"),(voice_grunt_long,"snd_man_grunt_long"),(voice_yell,"snd_haradrim_yell"),(voice_victory,"snd_haradrim_victory")], #voice sounds
    "skel_human", 1.0,
    psys_game_blood,psys_game_blood_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),  
########################################################################################################################  
#9   Dwarf
  ( "dwarf", skf_use_morph_key_10 ,
    "dwarf_body", "dwarf_calf_l", "dwarf_handL",
    "dwarf_head", dwarf_face_keys,
    ["man_hair_s","man_hair_n","man_hair_p","man_hair_r","man_hair_q","man_hair_v","man_hair_y9"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",
    ["beard_dwarf_1","beard_dwarf_2", "beard_dwarf_3", "beard_dwarf_4","beard_dwarf_5","beard_dwarf_6","beard_dwarf_7","beard_dwarf_8",], #beard meshes ,
    ["hair_blonde_dwarf"], #hair textures
    ["dwarf_beard_blonde"], #beard_materials
    [("manface_young"   ,0xffd0e0e0,["hair_blonde"],[0xffb04717, 0xffb04717, 0xff502a19]),
     ("manface_young_2" ,0xffcbe0e0,["hair_blonde"],[0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),
     ("manface_7"       ,0xffc0c8c8,["hair_blonde"],[0xff83301a, 0xff502a19, 0xff19100c, 0xff0c0d19]),     
     ("manface_midage"  ,0xffdfefe1,["hair_blonde"],[0xff2f180e, 0xff171313, 0xff07080c]),
     ("manface_midage_2",0xfde4c8d8,["hair_blonde"],[0xff2f180e, 0xff171313, 0xff07080c]),
     ("manface_rugged"  ,0xffb0aab5,["hair_blonde"],[0xff171313, 0xff07080c]),
	], #man_face_textures,
    [(voice_die,"snd_man_die"),(voice_hit,"snd_man_hit"),(voice_grunt,"snd_man_grunt"),(voice_grunt_long,"snd_man_grunt_long"),(voice_yell,"snd_dwarf_yell"),(voice_victory,"snd_dwarf_victory")], #voice sounds
    "skel_dwarf", 1.0,
    psys_game_blood,psys_game_blood_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),  
########################################################################################################################  
#10 Troll
  ( "troll", 0,
    "troll_body", "dummy_mesh", "troll_handL",
    "dummy_mesh", troll_face_keys,
    [], #hair meshes
    [], #beard meshes
    ["hair_blonde"], #hair textures NOTE - you MUST have a hair texture (even if it is not used) for the game not to crash
    [], #beard materials
    [
	  ("troll",0xffffffff,[])	#face material, skin hue, hair color (we must put a value for hair color since limit_hair_color = 1 in the module.ini)
    ], #face textures,
	[(voice_die,"snd_troll_die"),(voice_hit,"snd_troll_hit"),(voice_grunt,"snd_troll_grunt"),(voice_grunt_long,"snd_troll_grunt_long"),(voice_yell,"snd_troll_yell"),(voice_victory,"snd_troll_victory")], #voice sounds
    "skel_troll", 1.0,	#1.0 is the hitbox size, can be made slightly bigger/smaller but large changes may cause the game to crash
    psys_game_blood_black,psys_game_blood_black_2,
  ),  
########################################################################################################################  
#11 Dunedain
  ( "dunedain", 0,
    "man_body", "man_calf_l", "m_handL",
    "male_head", dunedain_face_keys,
    ["man_hair_s","man_hair_m","man_hair_n","man_hair_o", "man_hair_y10", "man_hair_y12","man_hair_p","man_hair_r","man_hair_q","man_hair_v","man_hair_t","man_hair_y6","man_hair_y3","man_hair_y7","man_hair_y9","man_hair_y11","man_hair_u","man_hair_y","man_hair_y2","man_hair_y4"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",
    ["beard_e","beard_d","beard_k","beard_l","beard_i","beard_j","beard_z","beard_m","beard_n","beard_y","beard_p","beard_o",   "beard_v", "beard_f", "beard_b", "beard_c","beard_t","beard_u","beard_r","beard_s","beard_a","beard_h","beard_g",], #beard meshes ,"beard_q"
    ["hair_blonde"], #hair textures
    ["beard_blonde"], #beard_materials
    [("manface_young_2" ,0xffcbe0e0,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff502a19]),
     ("manface_midage"  ,0xffdfefe1,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),
     ("manface_young"   ,0xffd0e0e0,["hair_blonde"],[0xff83301a, 0xff502a19, 0xff19100c, 0xff0c0d19]),     
     ("manface_young_3" ,0xffdceded,["hair_blonde"],[0xff2f180e, 0xff171313, 0xff07080c]),
     ("manface_7"       ,0xffc0c8c8,["hair_blonde"],[0xff171313, 0xff07080c]),
     ("manface_midage_2",0xfde4c8d8,["hair_blonde"],[0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("manface_rugged"  ,0xffb0aab5,["hair_blonde"],[0xff171313, 0xff07080c]),
#     ("manface_african" ,0xff807c8a,["hair_blonde"],[0xff120808, 0xff007080c]),     
     ], #man_face_textures,
    [(voice_die,"snd_man_die"),(voice_hit,"snd_man_hit"),(voice_grunt,"snd_man_grunt"),(voice_grunt_long,"snd_man_grunt_long"),(voice_yell,"snd_dunedain_yell"),(voice_victory,"snd_dunedain_victory")], #voice sounds
    "skel_human", 1.0,
    psys_game_blood,psys_game_blood_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),    
########################################################################################################################  
#12
  ( "lorien", 0,
    "man_body", "man_calf_l", "m_handL",
    "elf_head", lothlorien_face_keys,
    ["elf_hair_4","elf_hair_3","elf_hair_1","elf_hair_2","man_hair_p","elf_hair_6", "elf_hair_7","man_hair_r","man_hair_q","elf_hair_5","elf_hair_8"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",
    [], #beard meshes ,"beard_q"
    ["hair_blonde_elf"], #hair textures
    ["beard_blonde"], #beard_materials
    [("elfface_young"  ,0xffcbe0e0,["hair_blonde_elf"],[0xffffffff, 0xffb04717, 0xff502a19]),
     ("elfface_young_2",0xffdfefe1,["hair_blonde_elf"],[0xffffffff, 0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),
     ("elfface_young_4",0xffd0e0e0,["hair_blonde_elf"],[0xff83301a, 0xff502a19, 0xff19100c, 0xff0c0d19]),     
     ("elfface_young_3",0xffdceded,["hair_blonde_elf"],[0xff2f180e, 0xff171313, 0xff07080c]),
     ], #elf_face_textures,
    [(voice_die,"snd_man_die"),(voice_hit,"snd_man_hit"),(voice_grunt,"snd_man_grunt"),(voice_grunt_long,"snd_man_grunt_long"),(voice_yell,"snd_lothlorien_yell"),(voice_victory,"snd_lothlorien_victory")], #voice sounds
    "skel_elf", 1.0,
    psys_game_blood,psys_game_blood_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),  
########################################################################################################################  
#13
  ( "imladris", 0,
    "man_body", "man_calf_l", "m_handL",
    "elf_head", rivendell_face_keys,
    ["elf_hair_4","elf_hair_3","elf_hair_1","elf_hair_2","man_hair_p","elf_hair_6", "elf_hair_7","man_hair_r","man_hair_q","elf_hair_5","elf_hair_8"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",
    [], #beard meshes ,"beard_q"
    ["hair_blonde_elf"], #hair textures
    ["beard_blonde"], #beard_materials
    [("elfface_young"  ,0xffcbe0e0,["hair_blonde_elf"],[0xffffffff, 0xffb04717, 0xff502a19]),
     ("elfface_young_2",0xffdfefe1,["hair_blonde_elf"],[0xffffffff, 0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),
     ("elfface_young_4",0xffd0e0e0,["hair_blonde_elf"],[0xff83301a, 0xff502a19, 0xff19100c, 0xff0c0d19]),     
     ("elfface_young_3",0xffdceded,["hair_blonde_elf"],[0xff2f180e, 0xff171313, 0xff07080c]),
     ], #man_face_textures,
    [(voice_die,"snd_man_die"),(voice_hit,"snd_man_hit"),(voice_grunt,"snd_man_grunt"),(voice_grunt_long,"snd_man_grunt_long"),(voice_yell,"snd_rivendell_yell"),(voice_victory,"snd_rivendell_victory")], #voice sounds
    "skel_elf", 1.0,
    psys_game_blood,psys_game_blood_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),  
########################################################################################################################  
#14
 (  "woodelf", 0,
    "man_body", "man_calf_l", "m_handL",
    "elf_head", mirkwood_face_keys,
    ["elf_hair_1","elf_hair_2","elf_hair_3","elf_hair_4","man_hair_p","elf_hair_5", "elf_hair_6","man_hair_r","man_hair_q","elf_hair_7","elf_hair_8"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",
    [], #beard meshes ,"beard_q"
    ["hair_blonde_elf"], #hair textures
    [], #beard_materials"beard_blonde"
    [("elfface_young"  ,0xffcbe0e0,["hair_blonde_elf"],[0xffffffff, 0xffb04717, 0xff502a19]),
     ("elfface_young_2",0xffdfefe1,["hair_blonde_elf"],[0xffffffff, 0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),
     ("elfface_young_4",0xffd0e0e0,["hair_blonde_elf"],[0xff83301a, 0xff502a19, 0xff19100c, 0xff0c0d19]),     
     ("elfface_young_3",0xffdceded,["hair_blonde_elf"],[0xff2f180e, 0xff171313, 0xff07080c]),
     ], #man_face_textures,
    [(voice_die,"snd_man_die"),(voice_hit,"snd_man_hit"),(voice_grunt,"snd_man_grunt"),(voice_grunt_long,"snd_man_grunt_long"),(voice_yell,"snd_mirkwood_yell"),(voice_victory,"snd_mirkwood_victory")], #voice sounds
    "skel_elf", 1.0,
    psys_game_blood,psys_game_blood_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),  
 
########################################################################################################################  
#15    Khand   +  Rhun   +   Easterling
  ( "evil_man", 0,
    "man_body", "man_calf_l", "m_handL",
    "male_head", easterling_face_keys,
    ["man_hair_s","man_hair_m","man_hair_n","man_hair_o", "man_hair_y10", "man_hair_y12","man_hair_p","man_hair_r","man_hair_q","man_hair_v","man_hair_t","man_hair_y6","man_hair_y3","man_hair_y7","man_hair_y9","man_hair_y11","man_hair_u","man_hair_y","man_hair_y2","man_hair_y4"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",
    ["beard_e","beard_d","beard_k","beard_l","beard_i","beard_j","beard_z","beard_m","beard_n","beard_y","beard_p","beard_o",   "beard_v", "beard_f", "beard_b", "beard_c","beard_t","beard_u","beard_r","beard_s","beard_a","beard_h","beard_g",], #beard meshes ,"beard_q"
    ["hair_blonde"], #hair textures
    ["beard_blonde"], #beard_materials
    [#("manface_young_2"   ,0xffcbe0e0,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff502a19]),
#     ("manface_midage"    ,0xffdfefe1,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),
#     ("manface_young"     ,0xffd0e0e0,["hair_blonde"],[0xff83301a, 0xff502a19, 0xff19100c, 0xff0c0d19]),     
#     ("manface_young_3"   ,0xffdceded,["hair_blonde"],[0xff2f180e, 0xff171313, 0xff07080c]),
#     ("manface_7"         ,0xffc0c8c8,["hair_blonde"],[0xff171313, 0xff07080c]),
#     ("manface_midage_2"  ,0xfde4c8d8,["hair_blonde"],[0xff502a19, 0xff19100c, 0xff0c0d19]),
#     ("manface_rugged"    ,0xffb0aab5,["hair_blonde"],[0xff171313, 0xff07080c]),
#     ("manface_african"   ,0xff807c8a,["hair_blonde"],[0xff120808, 0xff07080c]),     
     ("mordor_face_a"     ,0xffb0aab5,["hair_blonde"],[0xff171313, 0xff07080c]),
     ("mordor_face_b"     ,0xff807c8a,["hair_blonde"],[0xff120808, 0xff07080c]),     
     ("mordor_face_c"     ,0xffb0aab5,["hair_blonde"],[0xff171313, 0xff07080c]),
     ("face_camo_a"       ,0xffdceded,["hair_blonde"],[0xff2f180e, 0xff171313, 0xff07080c]),
     ("face_camo_b"       ,0xffc0c8c8,["hair_blonde"],[0xff171313, 0xff07080c]),
     ("face_camo_c"       ,0xfde4c8d8,["hair_blonde"],[0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("face_camo_d"       ,0xffb0aab5,["hair_blonde"],[0xff171313, 0xff07080c]),
     ("face_camo_e"       ,0xff807c8a,["hair_blonde"],[0xff120808, 0xff07080c]),     
     ("berserker_face_a"  ,0xffcbe0e0,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff502a19]),
     ("berserker_face_b"  ,0xffdfefe1,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),
     ("berserker_face_c"  ,0xffd0e0e0,["hair_blonde"],[0xff83301a, 0xff502a19, 0xff19100c, 0xff0c0d19]),     
     ("east_bandit_face_a",0xfde4c8d8,["hair_blonde"],[0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("east_bandit_face_b",0xffb0aab5,["hair_blonde"],[0xff171313, 0xff07080c]),
     ("east_bandit_face_c",0xff807c8a,["hair_blonde"],[0xff120808, 0xff07080c]),     

     ], #man_face_textures,
    [(voice_die,"snd_man_die"),(voice_hit,"snd_man_hit"),(voice_grunt,"snd_man_grunt"),(voice_grunt_long,"snd_man_grunt_long"),(voice_yell,"snd_man_warcry"),(voice_victory,"snd_man_victory")], #voice sounds
    "skel_human", 0.95,
    psys_game_blood,psys_game_blood_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),   
]
