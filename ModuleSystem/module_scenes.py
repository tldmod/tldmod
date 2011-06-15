from header_common import *
from header_operations import *
from header_triggers import *
from header_scenes import *
from module_constants import *

####################################################################################################################
#  Each scene record contains the following fields:
#  1) Scene id {string}: used for referencing scenes in other files. The prefix scn_ is automatically added before each scene-id.
#  2) Scene flags {int}. See header_scenes.py for a list of available flags
#  3) Mesh name {string}: This is used for indoor scenes only. Use the keyword "none" for outdoor scenes.
#  4) Body name {string}: This is used for indoor scenes only. Use the keyword "none" for outdoor scenes.
#  5) Min-pos {(float,float)}: minimum (x,y) coordinate. Player can't move beyond this limit.
#  6) Max-pos {(float,float)}: maximum (x,y) coordinate. Player can't move beyond this limit.
#  7) Water-level {float}. 
#  8) Terrain code {string}: You can obtain the terrain code by copying it from the terrain generator screen
#  9) List of other scenes accessible from this scene {list of strings}.
#     (deprecated. This will probably be removed in future versions of the module system)
#     (In the new system passages are used to travel between scenes and
#     the passage's variation-no is used to select the game menu item that the passage leads to.)
# 10) List of chest-troops used in this scene {list of strings}. You can access chests by placing them in edit mode.
#     The chest's variation-no is used with this list for selecting which troop's inventory it will access.
####################################################################################################################

scenes = [
  ("random_scene"              ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),(240,240),-0.5,"0x0000000329602800000691a400003efe00004b34000059be",[],[]),
  ("conversation_scene",0,"encounter_spot", "bo_encounter_spot", (-40,-40),(40,40),-100,"0",   [],[]),
  ("random_scene_steppe"       ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),(240,240),-0.5,"0x000000022c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_rohan"),
  ("random_scene_steppe_small" ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),( 90, 90),-0.5,"0x000000012c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
  ("random_scene_plain"        ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),(220,220),-0.5,"0x000000023c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_plain"),
  ("random_scene_plain_small"  ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_plain"),
  ("random_scene_snow"         ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),(200,200),-0.5,"0x000000024c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_plain"),
  ("random_scene_snow_small"   ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),( 90, 90),-0.5,"0x000000014c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_plain"),
  ("random_scene_desert"       ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),(240,240),-0.5,"0x000000025c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_steppe"),
  ("random_scene_desert_small" ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),( 90, 90),-0.5,"0x000000015c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_steppe"),
  ("random_scene_steppe_forest",sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),(140,140),-0.5,"0x00000002ac6028000003e8fa0000034e00004b34000059be",[],[],"outer_terrain_forest"),
  ("random_scene_plain_forest" ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),(100,100),-0.5,"0x00000001bc60280000034cd30000034e00004b34000059be",[],[],"outer_terrain_forest"),
  ("random_scene_snow_forest"  ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),(100,100),-0.5,"0x00000001cc6028000003e8fa0000034e00004b34000059be",[],[],"outer_terrain_forest"),
  ("random_scene_desert_forest",sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),(150,150),-0.5,"0x00000001dc6028000003e8fa0000034e00004b34000059be",[],[],"outer_terrain_forest"),

  ("camp_scene"                ,sf_generate                     ,"none","none",(0,0),(100,100),-0.5,"0x000000003004cd26800354d70000618700003c3300007a8c",[],["camp_chest_faction","camp_chest_none"], "outer_terrain_plain"),
  ("camp_scene_horse_track"    ,sf_generate|sf_auto_entry_points,"none","none",(0,0),(240,240),-0.5,"0x300028000003e8fa0000034e00004b34000059be",    [],[], "outer_terrain_plain"),
  ("four_ways_inn" ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x0230817a00028ca300007f4a0000479400161992",[],[],"outer_terrain_plain"),
  ("test_scene"    ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x0230817a00028ca300007f4a0000479400161992",[],[],"outer_terrain_plain"),
  ("quick_battle_1",sf_generate,"none", "none", (0,0),(120,120),-100,"0x30401ee300059966000001bf0000299a0000638f",[],[],"outer_terrain_plain"),
  ("quick_battle_2",sf_generate,"none", "none", (0,0),(120,120),-100,"0xa0425ccf0004a92a000063d600005a8a00003d9a",[],[],"outer_terrain_steppe"),
  ("quick_battle_3",sf_generate,"none", "none", (0,0),(120,120),-100,"0x4c6024e3000691a400001b7c0000591500007b52",[],[],"outer_terrain_snow"),
  ("quick_battle_4",sf_generate,"none", "none", (0,0),(120,120),-100,"0x00000006b007a2320005114300006228000053bf00004eb9",[],[]),# 0x00001d63c005114300006228000053bf00004eb9
  ("quick_battle_5",sf_generate,"none", "none", (0,0),(120,120),-100,"0x3a078bb2000589630000667200002fb90000179c",[],[],"outer_terrain_plain"),
  ("quick_battle_6",sf_generate,"none", "none", (0,0),(120,120),-100,"0xa0425ccf0004a92a000063d600005a8a00003d9a",[],[],"outer_terrain_steppe"),
  ("quick_battle_7",sf_generate,"none", "none", (0,0),(100,100),-100,"0x314d060900036cd70000295300002ec9000025f3",[],[],"outer_terrain_plain"),

################## TLD QUICK BATTLES 0x00000002b007a2320005114300006228000053bf00004eb9
  ("quick_battle_ambush"  ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x00000002b007a2320002589600002fc700004068000049dc",[],[], "outer_terrain_plain"),
  ("quick_battle_corsair" ,sf_generate,"none", "none", (0,0),(200,200),-100,"0x0000000320014500800a6e9800007dd98000250100006dde",[],[]),
  ("town_1_arena_football",sf_generate,"none", "none", (0,0),(100,100),-100,"0xa0001d9300031ccb0000156f000048ba0000361c"        ,[],[], "outer_terrain_plain"),
  ("quick_battle_random"  ,sf_generate|sf_randomize,"none", "none", (0,0),(300,300),-100,"0x000000033c64cb1e0006d5b50000307900001e7500004547", [],[], "outer_terrain_plain"),
  ("starting_quest"       ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x30401ee300059966000001bf0000299a0000638f",[],[], "outer_terrain_plain"),
######## END TLD
  #("quick_battle_TEST_TROLL",sf_generate|sf_auto_entry_points,"none", "none", (0,0),(200,200),-100,"0x000000003a0a8fb24002308c000006660000120c00005627",[],[], "outer_terrain_plain"),

  ("salt_mine"    ,sf_generate,"none", "none", (-200,-200),(200,200),-100,"0x2a07b23200025896000023ee00007f9c000022a8", [],[], "outer_terrain_steppe"),
  ("novice_ground",sf_indoors,"training_house_a", "bo_training_house_a", (-100,-100),(100,100),-100,"0",    [],[]),
  ("zendar_arena" ,sf_generate,"none", "none", (0,0),(100,100),-100,"0xa0001d9300031ccb0000156f000048ba0000361c",    [],[], "outer_terrain_plain"),
  ("dhorak_keep"  ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x33a7946000028ca300007f4a0000479400161992",    ["exit"],[]),
  ("reserved4"    ,sf_generate,"none", "none", (0,0),(120,120),-100,"28791",    [],[]),
  ("reserved5"    ,sf_generate,"none", "none", (0,0),(120,120),-100,"117828",    [],[]),
  ("reserved6"    ,sf_generate,"none", "none", (0,0),(100,100),-100,"6849",    [],[]),
  ("reserved7"    ,sf_generate,"none", "none", (0,0),(100,100),-100,"6849",    [],[]),
  ("reserved8"    ,sf_generate,"none", "none", (0,0),(100,100),-100,"13278",    [],[]),
  ("reserved9"    ,sf_indoors,"thirsty_lion", "bo_thirsty_lion", (-100,-100),(100,100),-100,"0",    [],[]),
  ("reserved10"   ,0,"none", "none", (-100,-100),(100,100),-100,"0",    [],[]),
  ("reserved11"   ,0,"none", "none", (-100,-100),(100,100),-100,"0",    [],[]),
  ("reserved12"   ,sf_indoors,"thirsty_lion", "bo_thirsty_lion", (-100,-100),(100,100),-100,"0",    [],[]),
  ("training_ground",sf_generate,"none", "none", (0,0),(120,120),-100,"0x30000500400360d80000189f00002a8380006d91",    [],["tutorial_chest_1", "tutorial_chest_2"], "outer_terrain_plain"),
  ("tutorial_1"   ,sf_indoors,"tutorial_1_scene", "bo_tutorial_1_scene", (-100,-100),(100,100),-100,"0",    [],[]),
  ("tutorial_2"   ,sf_indoors,"tutorial_2_scene", "bo_tutorial_2_scene", (-100,-100),(100,100),-100,"0",    [],[]),
  ("tutorial_3"   ,sf_indoors,"tutorial_3_scene", "bo_tutorial_3_scene", (-100,-100),(100,100),-100,"0",    [],[]),
  ("tutorial_4"   ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x30000500400360d80000189f00002a8380006d91",    [],[], "outer_terrain_plain"),
  ("tutorial_5"   ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x3a06dca80005715c0000537400001377000011fe",    [],[], "outer_terrain_plain"),


  ("training_ground_horse_track_1" ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x00000000337553240004d53700000c0500002a0f80006267",[],[], "outer_terrain_plain"),
  ("training_ground_horse_track_2" ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x00000000301553240004d5370000466000002a0f800073f1",[],[], "outer_terrain_plain"),
  ("training_ground_horse_track_3" ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x00000000400c12b2000515470000216b0000485e00006928",[],[], "outer_terrain_snow"),
  ("training_ground_horse_track_4" ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x00000000200b60320004a5290000180d0000452f00000e90",[],[], "outer_terrain_steppe"),
  ("training_ground_horse_track_5" ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x000000003008208e0006419000000f730000440f00003c86",[],[], "outer_terrain_plain"),
  ("training_ground_ranged_melee_1",sf_generate,"none", "none", (0,0),(120,120),-100,"0x00000001350455c20005194a000041cb00005ae800000ff5",[],[], "outer_terrain_plain"),
  ("training_ground_ranged_melee_2",sf_generate,"none", "none", (0,0),(120,120),-100,"0x0000000532c8dccb0005194a000041cb00005ae800001bdd",[],[], "outer_terrain_plain"),
  ("training_ground_ranged_melee_3",sf_generate,"none", "none", (0,0),(120,120),-100,"0x000000054327dcba0005194a00001b1d00005ae800004d63",[],[], "outer_terrain_snow"),
  ("training_ground_ranged_melee_4",sf_generate,"none", "none", (0,0),(120,120),-100,"0x000000012247dcba0005194a000041ef00005ae8000050af",[],[], "outer_terrain_steppe"),
  ("training_ground_ranged_melee_5",sf_generate,"none", "none", (0,0),(120,120),-100,"0x00000001324a9cba0005194a000041ef00005ae800003c55",[],[], "outer_terrain_plain"),

  ("zendar_center",sf_generate,"none", "none", (0,0),(100,100),-100,"0x300bc5430001e0780000448a0000049f00007932", ["the_happy_boar","","zendar_merchant"],["bonus_chest_2"], "outer_terrain_plain"),
  ("the_happy_boar" ,sf_indoors,"interior_town_house_i", "bo_interior_town_house_i", (-100,-100),(100,100),-100,"0",   ["zendar_center"],["zendar_chest"]),
  ("zendar_merchant",sf_indoors,"interior_town_house_i", "bo_interior_town_house_i", (-100,-100),(100,100),-100,"0",  [],[]),

# city centers
  ("minas_tirith_center"    ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_tirith_1"),
  ("minas_tirith_center_mid",sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_tirith_1"),
  ("minas_tirith_center_top",sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_tirith_1"),
  ("pelargir_center"        ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000006300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_seaside_1"),
  ("linhir_center"          ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x000000042005591e00040506000059a100002cd500005052",[],[],"outer_terrain_steppe"),
  ("dol_amroth_center"      ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000005200005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_seaside_1"),
  ("edhellond_center"       ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000004300798b2000380e3000037960000573900003f48",[],[],"outer_terrain_seaside_1"),
  ("lossarnach_center"      ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000007300005000006ada4000051a90000386b00003791",[],[],"outer_mountains2west"),
  ("tarnost_center"         ,sf_generate,"none", "none",(0,0),(200,200),-100,        "0x30050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_mountains2east"),
  ("erech_center"           ,sf_generate,"none", "none",(0,0),(200,200),-100,        "0x3000148000025896000074e600006c260000125a",[],[],"outer_mountains2north"),
  ("pinnath_gelin_center"   ,sf_generate,"none", "none",(0,0),(200,200),-100,        "0x300416a600035cd600007ee80000012100003fbc",[],[],"outer_terrain_plain"),
  ("ethring_center"         ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x000000042005591e00040506000059a100002cd500005052",[],[],"outer_terrain_steppe"),
  ("east_osgiliath_center"  ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_osgiliath_9"),
  ("west_osgiliath_center"  ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_osgiliath_9"),
  ("henneth_annun_center"   ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005000002b4ac00002ccd800026dc00000c1d",[],[],"outer_mountains2south"),
  ("cair_andros_center"     ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_osgiliath_9"),
  ("edoras_center"          ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000007200005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_rohan"),
  ("aldburg_center"         ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000072007956000025896000037e800000e860000674b",[],[],"outer_mountains2south"),
  ("hornburg_center"        ,sf_generate,"none", "none",(0,0),(100,100),-100,        "0x00001d63c005114300006228000053bf00004eb9",[],[],"outer_mountains2south"),
  ("east_emnet_center"      ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000720045abc000308c4000029d9000033bd000009b9",[],[],"outer_terrain_rohan"),
  ("westfold_center"        ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000620049cbd00025896000048e90000164400002b3f",[],[],"outer_terrain_rohan"),
  ("west_emnet_center"      ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000720045abc000308c4000029d9000033bd000009b9",[],[],"outer_terrain_rohan"),
  ("eastfold_center"        ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007a009c7070002589600002b6300001ef60000122e",[],[],"outer_mountains2south"),
  ("barad_dur_center"       ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000072005591e00040506000059a100002cd500005052",[],[],"outer_terrain_steppe"),
  ("morannon_center"        ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_mountains2west_mordor"),
  ("minas_morgul_center"    ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_mountains2west_mordor"),
  ("mount_doom_center"      ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000073000148000025896000074e600006c260000125a",[],[],"outer_terrain_plain"),
  ("cirith_ungol_center"    ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_plain"),
  ("orc_sentry_camp_center" ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_osgiliath_9"),
  ("isengard_center"        ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_mountains2north"),
  ("uruk_hai_outpost_center",sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000073000148000025896000074e600006c260000125a",[],[],"outer_terrain_rohan"),
  ("uruk_hai_h_camp_center" ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007400790b20002c8b0000050d500006f8c00006dbd",[],[],"outer_terrain_plain"),
  ("uruk_hai_r_camp_center" ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000073000148000025896000074e600006c260000125a",[],[],"outer_terrain_rohan"),
  ("caras_galadhon_center"  ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],["player_chest"],"outer_terrain_forest"),#Kolba
  ("cerin_dolen_center"     ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"),#Kolba
  ("cerin_amroth_center"    ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"),#Kolba
  ("thranduils_halls_center",sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"),#Kolba
  ("woodelf_camp_center"    ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300798b2000380e3000037960000573900003f48",[],[],"outer_terrain_forest"),
  ("woodsmen_village_center",sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000073000148000025896000074e600006c260000125a",[],[],"outer_terrain_plain"),
  ("moria_center"           ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005000004a92a00000f768000576c00001d2c",[],["player_chest"]),
  ("troll_cave_center"      ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"),#Kolba
  ("dale_center"            ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000003200005000007a9ea000006810000219700002120",[],[],"outer_terrain_plain"),
  ("esgaroth_center"        ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x0000000730000500000c8f2100002ca5000022aa000031a8",[],[],"outer_terrain_seaside_1"),
  ("erebor_center"          ,sf_indoors ,"hallfini", "bo_hallfini",(-100,-200),(100,200),-100,"0",[],[]),
  ("dunland_camp_center"    ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007a009c7070002589600002b6300001ef60000122e",[],["player_chest"],"outer_terrain_rohan"),
  ("harad_camp_center"      ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000072005591e00040506000059a100002cd500005052",[],["player_chest"],"outer_terrain_steppe"),
  ("khand_camp_center"      ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730001d9300031ccb0000156f000048ba0000361c",[],["player_chest"],"outer_terrain_flat"),
  ("umbar_camp_center"      ,sf_generate,"none", "none",(0,0),(100,100),-100,"        0x3002898a80051d440000154e000026f300004e2d",[],["player_chest"]),
  ("rivendell_camp_center"  ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000073000148000025896000074e600006c260000125a",[],["player_chest"],"outer_terrain_plain"),
  ("dol_guldur_center"      ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"),
  ("north_rhun_camp_center" ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000073000148000025896000074e600006c260000125a",[],["player_chest"],"outer_terrain_flat"),
  ("gundabad_camp_center"   ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007400790b20002c8b0000050d500006f8c00006dbd",[],["player_chest"],"outer_mountains2north"),
  ("ironhill_camp_center"   ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007200016da000364d9000060f500007591000064e7",[],[],"outer_terrain_steppe"),

### GA stub scenes
  ("gondor_castle"      ,sf_indoors, "interior_castle_v", "bo_interior_castle_v", (-100,-100),(100,100),-100,"0",["exit"],[]),
  ("minas_tirith_castle",sf_indoors|sf_force_skybox, "throne_room", "bo_throne_room", (-1000,-1000),(1000,1000),-100,"0",["exit"],["player_chest"]),
  ("rohan_castle"       ,sf_indoors, "interior_castle_t", "bo_interior_castle_t", (-100,-100),(100,100),-100,"0",["exit"],["player_chest"]),
  ("elf_castle"         ,sf_indoors, "interior_castle_t", "bo_interior_castle_t", (-100,-100),(100,100),-100,"0",["exit"],[]),
  ("mordor_castle"      ,sf_indoors, "interior_castle_t", "bo_interior_castle_t", (-100,-100),(100,100),-100,"0",["exit"],["player_chest"]),
  ("edoras_castle"      ,sf_indoors, "rohan_meduseld_int", "bo_rohan_meduseld_int", (-100,-100),(100,100),-100,"0",["exit"],["player_chest"]),

  ("gondor_tavern" ,sf_indoors, "interior_tavern_b"    ,"bo_interior_tavern_b"    , (-100,-100),(100,100),-100,"0",["exit"],[]),
  ("rohan_tavern"  ,sf_indoors, "interior_tavern_b"    ,"bo_interior_tavern_b"    , (-100,-100),(100,100),-100,"0",["exit"],[]),
  ("elf_tavern"    ,sf_indoors, "interior_tavern_b"    ,"bo_interior_tavern_b"    , (-100,-100),(100,100),-100,"0",["exit"],[]),
  ("mordor_tavern" ,sf_indoors, "interior_tavern_b"    ,"bo_interior_tavern_b"    , (-100,-100),(100,100),-100,"0",["exit"],[]),
	
  ("gondor_prison",sf_indoors,"interior_prison_a", "bo_interior_prison_a", (-100,-100),(100,100),-100,"0",[],[]),
  ("rohan_prison" ,sf_indoors,"interior_prison_a", "bo_interior_prison_a", (-100,-100),(100,100),-100,"0",["exit"],[]),
  ("mordor_prison",sf_indoors,"interior_prison_a", "bo_interior_prison_a", (-100,-100),(100,100),-100,"0",[],[]),
  ("elf_prison"   ,sf_indoors,"interior_prison_a", "bo_interior_prison_a", (-100,-100),(100,100),-100,"0",[],[]),

  ("zendar_arena",sf_generate,"none", "none", (0,0),(100,100),-100,"0xa0001d9300031ccb0000156f000048ba0000361c",[],[],"outer_terrain_plain"),
  ("gondor_arena",sf_generate,"none", "none", (0,0),(100,100),-100,"0xa0001d9300031ccb0000156f000048ba0000361c",[],[],"outer_terrain_plain"),
  ("rohan_arena",sf_generate,"none", "none", (0,0),(120,120),-100,"0x00000001324a9cba0005194a000041ef00005ae800003c55",[],[], "outer_terrain_rohan"),
  ("dale_arena" ,sf_generate,"none", "none", (0,0),(100,100),-100,"0xa0001d9300031ccb0000156f000048ba0000361c",[],[],"outer_terrain_rohan"),
  ("elf_arena"   ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),
  ("dwarf_arena",sf_indoors ,"interior_gondor_training_room_b", "bo_interior_gondor_training_room_b", (-40,-40),(40,40),-100,"0",[],[]),
  ("mordor_arena",sf_generate,"none","none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_mountains2west_mordor"),
  ("isengard_arena",sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000073000148000025896000074e600006c260000125a",[],[],"outer_terrain_rohan"),
  ("khand_arena",sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730001d9300031ccb0000156f000048ba0000361c",[],[],"outer_terrain_flat"),
  ("rhun_arena",sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000073000148000025896000074e600006c260000125a",[],[],"outer_terrain_flat"),

# stub leftovers
  ("town_store",sf_indoors ,"interior_town_house_i", "bo_interior_town_house_i", (-100,-100),(100,100),-100,"0",    [],[]),
  ("town_alley",sf_generate,"none", "none", (0,0),(100,100),-100,"0x300bc5430001e0780000448a0000049f00007932",    [],[],"outer_terrain_plain"),
  ("town_walls",sf_generate,"none", "none", (0,0),(100,100),-100,"0x0000000130028e320005e17b00004a14000006d70000019d",    [],[],"outer_terrain_plain"),
# 1 Steppe
  ("castle_1_exterior",sf_generate,"none", "none", (0,0),(100,100),-100,"0x30054da28004050000005a76800022aa00002e3b", [],[],"outer_terrain_steppe"),
  ("castle_1_interior",sf_indoors, "dungeon_entry_a", "bo_dungeon_entry_a", (-100,-100),(100,100),-100,"0",  ["exit"],[]),
  ("castle_1_prison",sf_indoors,"interior_prison_a", "bo_interior_prison_a", (-100,-100),(100,100),-100,"0", [],[]),

#!!Villages !!#
  ("village_1" ,sf_generate,"none", "none", (0,0),(100,100),-100,"0x0000000030081763000589620000338e00004f2c00005cfb",   [],[],"outer_terrain_plain"),
  ("rivercross",sf_generate,"none", "none", (0,0),(100,100),-100,"0x0000000030081763000989a20000338e00004f2c00005cfb",   [],[],"outer_terrain_plain"),
  ("village_2",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000003007a21c0003ecfe000001f0000073b100000fd2",    [],[],"outer_terrain_plain"),
  ("village_3",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000023003dc4e0006118b000029f8000034670000105f",    [],[],"outer_terrain_plain"),
  ("village_4",sf_generate,"none", "none", (0,0),(100,100),-100,"0x0000000230079732000651a00000044c0000177200000234",    [],[],"outer_terrain_plain"),
  ("village_5",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000003001ce100006097d0000134c000016d8000042a2",    [],[],"outer_terrain_plain"),
  ("village_6",sf_generate,"none", "none", (0,0),(100,100),-100,"0x0000000230035598000761df000058ea000006f3000005e7",    [],[],"outer_terrain_plain"),
  ("village_7",sf_generate,"none", "none", (0,0),(100,100),-100,"0x0000000031059a0d0004792000005c3a00004df500000dbc",    [],[],"outer_terrain_plain"),
  ("village_8",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000002300798320006499200002acc000040d70000421d",    [],[],"outer_terrain_plain"),
  ("village_9",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000004300005008005b57000004e31800017d80000754b",    [],[],"outer_terrain_plain"),
  ("village_10",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000013005dad40005f57b0000543e0000279d000052b4",    [],[],"outer_terrain_plain"),

  ("field_1",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000033a059a5a0009525600002005000060e300001175",    [],[],"outer_terrain_plain"),
  ("field_2",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000033a079a3f000a3a8000006dfd000030a100006522",    [],[],"outer_terrain_steppe"),
  ("field_3",sf_generate,"none", "none", (0,0),(100,100),-100,"0x30054da28004050000005a76800022aa00002e3b",    [],[],"outer_terrain_steppe"),
  ("field_4",sf_generate,"none", "none", (0,0),(100,100),-100,"0x30054da28004050000005a76800022aa00002e3b",    [],[],"outer_terrain_steppe"),
  ("field_5",sf_generate,"none", "none", (0,0),(100,100),-100,"0x30054da28004050000005a76800022aa00002e3b",    [],[],"outer_terrain_steppe"),

#  ("rivercross_kazzan",sf_generate,"none", "none", (0,0),(100,100),-100,"0x0000000030081763000589620000338e00004f2c00005cfb",    [],[],"outer_terrain_plain"),

## Abhuva TLD Battlefield Scenes
## Plain Battle Field with a small farm and a road crossing the map
  ("battle_scene_plain_01",sf_generate|sf_auto_entry_points,"none", "none", (0,0),(240,240),-0.5,"0x000000023001c600000691a400003efe00004b34000059be",[],[], "outer_terrain_plain"),
## Plain Battle Field with a road crossing the map and a river with small bridge, lake with a fisher-house    
  ("battle_scene_plain_02",sf_generate|sf_auto_entry_points,"none", "none", (0,0),(240,240),-0.5,"0x0000000230054800000691a400003efe00004b34000011d9",[],[], "outer_terrain_plain"),
## Plain Bridge Battle with destroyed buildings    
  ("bridge_1",sf_generate,"none", "none", (0,0),(120,120),-100,"0x3a078bb2000589630000667200002fb90000179c",[],[], "outer_terrain_plain"),
## Mountain Forest with mines    
  ("battle_scene_mountain_forest_01",sf_generate|sf_auto_entry_points,"none", "none", (0,0),(240,240),-0.5,"0x0000000230054800000691a400003efe00004b34000011d9",[],[], "outer_terrain_plain"),
  ("aw_tomb"              ,sf_indoors,"aw_tomb"                       , "bo_aw_tomb"                  , (-100,-100),(240,240),-100,"0",[],[]),
  ("dol_amroth_castle"    ,sf_indoors,"interior_castle_dolamroth"     , "bo_interior_castle_dolamroth", (-100,-100),(100,100),-100,"0",[],[]),
  ("isengard_castle"      ,sf_indoors,"interior_throneroom_isengard_a", "bo_interior_castle_gondor_d" , (-100,-100),(100,100),-100,"0",[],["player_chest"]),
  ("gondor_castle_a"      ,sf_indoors,"interior_castle_gondor_a"      , "bo_interior_castle_gondor_a" , (-100,-100),(100,100),-100,"0",[],[]),
  ("gondor_castle_b"      ,sf_indoors,"interior_castle_gondor_b"      , "bo_interior_castle_gondor_b" , (-100,-100),(100,100),-100,"0",[],[]),
  ("gondor_castle_c"      ,sf_indoors,"interior_castle_gondor_c"      , "bo_interior_castle_gondor_c" , (-100,-100),(100,100),-100,"0",[],[]),
  ("gondor_castle_c"      ,sf_indoors,"interior_castle_gondor_c"      , "bo_interior_castle_gondor_c" , (-100,-100),(100,100),-100,"0",[],[]),
  ("cair_andros_castle"   ,sf_indoors,"interior_castle_gondor_d"      , "bo_interior_castle_gondor_d" , (-100,-100),(100,100),-100,"0",[],[]),
  ("west_osgiliath_castle",sf_indoors,"interior_castle_gondor_d"      , "bo_interior_castle_gondor_d" , (-100,-100),(100,100),-100,"0",[],[]),
  ("henneth_annun_castle" ,sf_indoors,"mesh_henneth_annun"            , "bo_henneth_annun"            , (-100,-100),(100,100),-100,"0",[],[]),
  ("rohan_castle_a"       ,sf_indoors,"interior_castle_rohan_a"       , "bo_interior_castle_i"        , (-100,-100),(100,100),-100,"0",[],[]),
  ("rohan_castle_b"       ,sf_indoors,"interior_castle_rohan_b"       , "bo_interior_castle_j"        , (-100,-100),(100,100),-100,"0",[],[]),
  ("mordor_castle_a"      ,sf_indoors,"interior_castle_mordor_a"      , "bo_interior_castle_mordor_a" , (-100,-100),(100,100),-100,"0",[],[]),
  ("mordor_castle_b"      ,sf_indoors,"interior_castle_mordor_b"      , "bo_interior_castle_mordor_b" , (-100,-100),(100,100),-100,"0",[],["player_chest"]),

  ("rhun_south_camp_center"         ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000730001d9300031ccb0000156f000048ba0000361c",[],[],"outer_terrain_flat"),
  ("rhun_north_camp_center"         ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000730001d9300031ccb0000156f000048ba0000361c",[],[],"outer_terrain_flat"),
  ("gundabad_ne_outpost_center"     ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000730001d9300031ccb0000156f000048ba0000361c",[],[],"outer_mountains2north"),
  ("gundabad_nw_outpost_center"     ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000730001d9300031ccb0000156f000048ba0000361c",[],[],"outer_mountains2north"),
  ("dol_guldur_north_outpost_center",sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"), #Kolba

  ("erebor_dungeon_01",sf_indoors,"dungeon_a","bo_dungeon_a",(-100,-100),(100,100),-100,"0",[],[]),
  ("gundabad_mirkwood_outpost"  ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"),#Kolba

  ("thranduil_hall_room"     ,sf_indoors|sf_force_skybox,"thranduil_hall", "bo_thranduil_hall", (-100,-100),(100,100),-100,"0",[],["player_chest"]),
  ("random_scene_parade"  ,sf_generate|sf_randomize,"none","none",(0,0),(220,220),-0.5,"0x000000023c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_forest"),#GA, faction troops parade
 
  ("woodelf_west_camp_center"   ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000007300798b2000380e3000037960000573900003f48",[],[],"outer_terrain_forest"),
  ("goblin_north_outpost_center",sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000730001d9300031ccb0000156f000048ba0000361c",[],[],"outer_mountains2west"),
  ("goblin_south_outpost_center",sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000730001d9300031ccb0000156f000048ba0000361c",[],[],"outer_mountains2west"),
  ("woodsmen_village2_center"   ,sf_generate,"none","none",(0,0),(100,100),-100,"0x000000073000148000025896000074e600006c260000125a",[],[],"outer_terrain_plain"),
  ("beorning_village_center"    ,sf_generate,"none","none",(0,0),(100,100),-100,"0x000000073000148000025896000074e600006c260000125a",[],[],"outer_terrain_plain"),
  ("isengard_center_flooded"    ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_mountains2north"),

  ("beorn_castle",sf_indoors,"interior_castle_rohan_b","bo_interior_castle_j",(-100,-100),(100,100),-100,"0",[],["player_chest"]),
  ("moria_castle",sf_indoors,"interior_round_isengard","bo_interior_round_isengard",(-100,-100),(100,100),-100,"0",[],[]),

# Legendary places  
  ("amon_hen"   ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000630000500000c2304000003ce000047ca0000794b",[],[],"outer_terrain_osgiliath_9"),
  ("deadmarshes",sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_flat"),
  ("mirkwood"   ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),
  ("fangorn"    ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),

# Siege scenes  
("cair_andros_siege",sf_generate,"none","none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_osgiliath_9"),
("dale_siege"       ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000003200005000007a9ea000006810000219700002120",[],[],"outer_terrain_plain"),
("west_emnet_siege" ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000720045abc000308c4000029d9000033bd000009b9",[],[],"outer_terrain_rohan"),

# various battlefield scenes
  ("battlefield1" ,sf_generate|sf_auto_entry_points,"none","none",(0,0),(200,200),-0.5,"0x0000000240004d634005c96d0000734a00004b340000734a",[],[],"outer_terrain_plain"),
  ("battlefield2" ,sf_generate|sf_auto_entry_points,"none","none",(0,0),(200,200),-0.5,"0x0000000240002800000691a400003efe00004b34000059be",[],[],"outer_terrain_plain"),
  ("battlefield3" ,sf_generate|sf_auto_entry_points,"none","none",(0,0),(200,200),-0.5,"0x0000000240002800000691a400003efe00004b34000059be",[],[],"outer_terrain_plain"),
  ("battlefield4" ,sf_generate|sf_auto_entry_points,"none","none",(0,0),(200,200),-0.5,"0x0000000240002800000691a400003efe00004b34000059be",[],[],"outer_terrain_plain"),
  ("battlefield5" ,sf_generate|sf_auto_entry_points,"none","none",(0,0),(200,200),-0.5,"0x0000000240002800000691a400003efe00004b34000059be",[],[],"outer_terrain_plain"),
  ("battlefield6" ,sf_generate|sf_auto_entry_points,"none","none",(0,0),(200,200),-0.5,"0x000000024c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_plain"),
  ("battlefield7" ,sf_generate|sf_auto_entry_points,"none","none",(0,0),(200,200),-0.5,"0x000000024c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_plain"),
  ("battlefield8" ,sf_generate|sf_auto_entry_points,"none","none",(0,0),(200,200),-0.5,"0x000000024c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_plain"),
  ("battlefield9" ,sf_generate|sf_auto_entry_points,"none","none",(0,0),(200,200),-0.5,"0x000000024c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_plain"),
  ("battlefield10",sf_generate|sf_auto_entry_points,"none","none",(0,0),(200,200),-0.5,"0x000000024c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_plain"),
  ("small_ford"   ,sf_generate|sf_auto_entry_points,"none","none",(0,0),(200,200),-0.5,"0x0000000235864d634005c96d0000734a00004b340000734a",[],[],"outer_terrain_plain"),

  ("hornburg_castle",sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000240002800000691a400003efe00004b34000059be",[],[]),
  ("morannon_castle",sf_generate,"none","none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_mountains2west_mordor"),
  ("west_osgiliath_center1",sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_osgiliath_9"),

  ("moria_secret_entry" ,sf_generate|sf_auto_entry_points,"none","none",(0,0),(200,200),-0.5,"0x0000000240004d634005c96d0000734a00004b340000734a",[],[],"outer_terrain_plain"),

  ]

