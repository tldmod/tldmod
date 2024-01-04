from header_common import *
from header_operations import *
from header_triggers import *
from header_scenes import *
from module_constants import *

from module_info import wb_compile_switch as is_a_wb_scene

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
("random_scene"      ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),(240,240),-0.5,"0x0000000329602800000691a400003efe00004b34000059be",[],[]),
("conversation_scene",sf_generate,"none", "none", (-40,-40),(40,40),-100,"0x00000006300005000002308c00003005000018b300001d92",[],[],"outer_terrain_plain"),

# scenes from native terrain types... (one for each terrain types)
("random_scene_steppe"          ,sf_generate|sf_randomize,"none","none",(0,0),(240,240),-0.5,"0x000000022c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("random_scene_plain"           ,sf_generate|sf_randomize,"none","none",(0,0),(220,220),-0.5,"0x000000023c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_plain"),
("random_scene_snow"            ,sf_generate|sf_randomize,"none","none",(0,0),(200,200),-0.5,"0x000000024c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_flat"),
("random_scene_desert"          ,sf_generate|sf_randomize,"none","none",(0,0),(240,240),-0.5,"0x000000025c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_desert"),
#("random_scene_north"          ,sf_generate|sf_randomize,"none","none",(0,0),(240,240),-0.5,"0x000000025c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_plain"),
# gap!!!
("random_scene_steppe_forest"   ,sf_generate|sf_randomize,"none","none",(0,0),(120,120),-0.5,"0x000000022c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_plain"),
("random_scene_plain_forest"    ,sf_generate|sf_randomize,"none","none",(0,0),(100,100),-0.5,"0x000000023c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_plain"),
("random_scene_snow_forest"     ,sf_generate|sf_randomize,"none","none",(0,0),(100,100),-0.5,"0x000000024c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_flat"),
("random_scene_desert_forest"   ,sf_generate|sf_randomize,"none","none",(0,0),(150,150),-0.5,"0x000000025c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_desert"),
#("random_scene_north_forest"   ,sf_generate|sf_randomize,"none","none",(0,0),(150,150),-0.5,"0x00000001dc6028000003e8fa0000034e00004b34000059be",[],[],"outer_terrain_plain"),
# ...small versions...
("random_scene_steppe_small" ,sf_generate|sf_randomize,"none","none",(0,0),( 90, 90),-0.5,"0x000000012c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("random_scene_plain_small"  ,sf_generate|sf_randomize,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_plain"),
("random_scene_snow_small"   ,sf_generate|sf_randomize,"none","none",(0,0),( 90, 90),-0.5,"0x000000014c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_flat"),
("random_scene_desert_small" ,sf_generate|sf_randomize,"none","none",(0,0),( 90, 90),-0.5,"0x000000015c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_flat"),
#("random_scene_north_small" ,sf_generate|sf_randomize,"none","none",(0,0),( 90, 90),-0.5,"0x000000015c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_plain"),

("random_scene_steppe_forest_small"   ,sf_generate|sf_randomize,"none","none",(0,0),(120,120),-0.5,"0x00000002ac6028000003e8fa0000034e00004b34000059be",[],[],"outer_terrain_plain"),
("random_scene_plain_forest_small"    ,sf_generate|sf_randomize,"none","none",(0,0),(100,100),-0.5,"0x00000001bc60280000034cd30000034e00004b34000059be",[],[],"outer_terrain_plain"),
("random_scene_snow_forest_small"     ,sf_generate|sf_randomize,"none","none",(0,0),(100,100),-0.5,"0x00000001c00005000003e8fa0000034e00004b34000059be",[],[],"outer_terrain_flat"),
("random_scene_desert_forest_small"   ,sf_generate|sf_randomize,"none","none",(0,0),(150,150),-0.5,"0x00000001dc6028000003e8fa0000034e00004b34000059be",[],[],"outer_terrain_flat"),

#("handsign" ,sf_generate|sf_auto_entry_points,"none","none",(0,0),( 90, 90),-0.5,"0x314d060900036cd70000295300002ec9000025f3",[],[],"outer_terrain_rohan"), #unused

("camp_scene",sf_generate,"none","none",(0,0),(100,100),-0.5,"0x000000003004cd26800354d70000618700003c3300007a8c",[],["camp_chest_faction","camp_chest_none"], "outer_terrain_plain"),
#("camp_scene_horse_track"    ,sf_generate|sf_auto_entry_points,"none","none",(0,0),(240,240),-0.5,"0x300028000003e8fa0000034e00004b34000059be",    [],[], "outer_terrain_plain"),
#("four_ways_inn" ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x0230817a00028ca300007f4a0000479400161992",[],[],"outer_terrain_plain"),
("test_scene"    ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x0230817a00028ca300007f4a0000479400161992",[],[],"outer_terrain_plain"),
("quick_battle_1",sf_generate,"none", "none", (0,0),(120,120),-100,"0x30401ee300059966000001bf0000299a0000638f",[],[],"outer_terrain_plain"),
("quick_battle_2",sf_generate,"none", "none", (0,0),(120,120),-100,"0xa0425ccf0004a92a000063d600005a8a00003d9a",[],[],"outer_terrain_steppe"),
("quick_battle_3",sf_generate,"none", "none", (0,0),(120,120),-100,"0x4c6024e3000691a400001b7c0000591500007b52",[],[],"outer_terrain_snow"),
("quick_battle_4",sf_generate,"none", "none", (0,0),(120,120),-100,"0x00000006b007a2320005114300006228000053bf00004eb9",[],[]),# 0x00001d63c005114300006228000053bf00004eb9
("quick_battle_5",sf_generate,"none", "none", (0,0),(120,120),-100,"0x3a078bb2000589630000667200002fb90000179c",[],[],"outer_terrain_plain"),
("quick_battle_6",sf_generate,"none", "none", (0,0),(120,120),-100,"0xa0425ccf0004a92a000063d600005a8a00003d9a",[],[],"outer_terrain_steppe"),
("quick_battle_7",sf_generate,"none", "none", (0,0),(100,100),-100,"0x314d060900036cd70000295300002ec9000025f3",[],[],"outer_terrain_plain"),

################## TLD QUICK BATTLES 0x00000002b007a2320005114300006228000053bf00004eb9
("quick_battle_ambush"  ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x00000002b007a2320002589600002fc700004068000049dc",[],[], "outer_mountains2east"),
("quick_battle_corsair" ,sf_generate,"none", "none", (0,0),(200,200),-100,"0x0000000320014500800a6e9800007dd98000250100006dde",[],[]),
#("town_1_arena_football",sf_generate,"none", "none", (0,0),(100,100),-100,"0xa0001d9300031ccb0000156f000048ba0000361c"        ,[],[], "outer_terrain_plain"),
("quick_battle_random"  ,sf_generate|sf_randomize,"none", "none", (0,0),(300,300),-100,"0x000000033c64cb1e0006d5b50000307900001e7500004547", [],[], "outer_terrain_plain"),
("starting_quest"       ,sf_generate,"none", "none", (0,0),(120,120),-100,"0x000000003007dae3000378de000001bf0000299a000048be",[],[], "outer_terrain_plain"),

# city centers
  ] + (is_a_wb_scene==1 and [
  ("minas_tirith_center"    ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x0000000330000500000d234800007e03000001780000021b",[],[],"New_outer_terrain_tirith_2"),
  ("minas_tirith_center_mid",sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"New_outer_terrain_tirith_2"),
  ("minas_tirith_center_top",sf_generate,"none", "none",(0,0),(200,200),-100,"0x0000000330000500000d234800007e03000001780000021b",[],[],"New_outer_terrain_tirith_2"),
  ] or [
  ("minas_tirith_center"    ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_tirith_1"),
  ("minas_tirith_center_mid",sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_tirith_1"),
  ("minas_tirith_center_top",sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_tirith_1"),
  ]) + [

  ("pelargir_center"        ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000006300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_seaside_1"),
  ("linhir_center"          ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x000000042005591e00040506000059a100002cd500005052",[],[],"outer_terrain_steppe"),
  ("dol_amroth_center"      ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x0000000130000500000d234800000f5200005bd50000739d",[],[],"New_outer_terrain_seaside_east_1"),
  ("edhellond_center"       ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000000300798b2000380e3000037960000573900003f48",[],[],"New_outer_terrain_seaside_north_1"),
  ("lossarnach_center"      ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000007300005000006ada4000051a90000386b00003791",[],[],"outer_mountains2west"),
  ("tarnost_center"         ,sf_generate,"none", "none",(0,0),(200,200),-100,        "0x30050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_mountains2east"),
  ("erech_center"           ,sf_generate,"none", "none",(0,0),(200,200),-100,        "0x3000148000025896000074e600006c260000125a",[],[],"outer_mountains2north"),
  ("pinnath_gelin_center"   ,sf_generate,"none", "none",(0,0),(200,200),-100,        "0x300416a600035cd600007ee80000012100003fbc",[],[],"outer_terrain_plain"),
  ("ethring_center"         ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x000000042005591e00040506000059a100002cd500005052",[],[],"outer_terrain_steppe"),
  ("east_osgiliath_center"  ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_osgiliath_9"),
  ("west_osgiliath_center"  ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_osgiliath_9"),
  ("henneth_annun_center"   ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005000002b4ac00002ccd800026dc00000c1d",[],[],"outer_mountains2south"),
  ("cair_andros_center"     ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_osgiliath_9"),
  ("edoras_center"          ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x00000003200005000009c5a200000f5200005bd50000739d",[],[],"outer_terrain_rohan"),
  ("aldburg_center"         ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000072007956000025896000037e800000e860000674b",[],[],"outer_mountains2south"),
  ("hornburg_center"        ,sf_generate,"none", "none",(0,0),(100,100),-100,        "0x0000000330000500000d234800006228000053bf00004eb9",[],[],"outer_terrain_helms_deep"),
  #("hornburg_center"        ,sf_generate,"none", "none",(0,0),(100,100),-100,        "0x00001d63c005114300006228000053bf00004eb9",[],[],"outer_mountains2south"),
  ("east_emnet_center"      ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000320045abc000308c4000029d9000033bd000009b9",[],[],"outer_terrain_rohan"),
  ("westfold_center"        ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000620049cbd00025896000048e90000164400002b3f",[],[],"outer_terrain_rohan"),
  ("west_emnet_center"      ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000320045abc000308c4000029d9000033bd000009b9",[],[],"outer_terrain_rohan"),
  ("eastfold_center"        ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007a009c7070002589600002b6300001ef60000122e",[],[],"outer_mountains2south"),
  ("morannon_center"        ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_mountains2west_mordor"),
  ("minas_morgul_center"    ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x0000000330000500000d23480000274f00005bd50000739d",[],[],"New_outer_mountains2east_mordor"),
  #("minas_morgul_center"    ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_mountains2west_mordor"), 
  ("cirith_ungol_center"    ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x00000002200e95140006398d0000372f00004a8900005ff2",[],[],"outer_terrain_rohan"),
  ("orc_sentry_camp_center" ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000003300005000009c5a200000f5200005bd50000739d",[],[],"outer_terrain_osgiliath_9"),
  ("isengard_center"        ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x0000000320000500000d234800002ba680005bd500005b5d",[],[],"outer_terrain_isen"),
  ("uruk_hai_outpost_center",sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x00000007300014800002b4aa000074e600006c260000125a",[],[],"outer_terrain_rohan"),
  ("uruk_hai_h_camp_center" ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x0000000020054b320004390d00003b3500006f8c00006dbd",[],[],"outer_terrain_plain"),
  ("uruk_hai_r_camp_center" ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000003200014800002b4aa000074e600006c260000125a",[],[],"New_outer_terrain_anduin"),
  ("caras_galadhon_center"  ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000030000500000985dc00000e2f000027d200005f66",[],["player_chest"],"outer_terrain_forest"),#Kolba
#  ("caras_galadhon_center"  ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],["player_chest"],"outer_terrain_forest"),#Kolba  
  ("cerin_dolen_center"     ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"),#Kolba
  ("cerin_amroth_center"    ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"),#Kolba
  ("thranduils_halls_center",sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"),#Kolba
  ("woodelf_camp_center"    ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000001b01918d980058d66000023ad0000751200006b67",[],[],"outer_terrain_forest"),
  ("woodsmen_village_center",sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000000200005d000057d5e000074e600006c2600006d0d",[],[],"outer_terrain_plain"), #
  ("moria_center"           ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005000008160b00000f768000576c00001d2c",[],["player_chest"]),
  ("troll_cave_center"      ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000001b00005000005a16c00006794000027d200006794",[],[],"outer_mountains2north"),#Kolba

  ] + (is_a_wb_scene==1 and [
  ("dale_center"            ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000330000500000d2348000006810000219700002120",[],[],"New_outer_terrain_tirith_1"),
  ("esgaroth_center"        ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x0000000730000500000c8f2100002ca5000022aa000031a8",[],[],"New_outer_terrain_seaside_1"),
  ("erebor_center"          ,sf_indoors ,"hallfini_wb", "bo_hallfini_wb_inner_tld",(-100,-200),(100,200),-100,"0",[],[]),
  ] or [
  ("dale_center"            ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000003200005000007a9ea000006810000219700002120",[],[],"outer_terrain_plain"),
  ("esgaroth_center"        ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x0000000730000500000c8f2100002ca5000022aa000031a8",[],[],"outer_terrain_seaside_1"),
  ("erebor_center"          ,sf_indoors ,"hallfini", "bo_hallfini_inner_tld",(-100,-200),(100,200),-100,"0",[],[]),

  ]) + [

  ("dunland_camp_center"    ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x0000000120000500000691a40000065c00004b34000070b7",[],["player_chest"],"outer_terrain_rohan"),
  ("harad_camp_center"      ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x000000072005591e00040506000059a100002cd500005052",[],["player_chest"],"outer_terrain_steppe"),
  ("khand_camp_center"      ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x0000000020040de3000699aa00005234000048ba000004b5",[],["player_chest"],"outer_terrain_rohan"),
  ("umbar_camp_center"      ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000002001c9a50007e1ed0000154e800026f300004e2d",[],["player_chest"],"New_outer_terrain_seaside_west"),  
  #("umbar_camp_center"      ,sf_generate,"none", "none",(0,0),(100,100),-100,"        0x3002898a80051d440000154e000026f300004e2d",[],["player_chest"]), #old corsair camp
  ("rivendell_camp_center"  ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000000300349e300084e1600005afd00006c26000063e2",[],["player_chest"],"outer_terrain_plain"),
#  ("rivendell_camp_center"  ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000073000148000025896000074e600006c260000125a",[],["player_chest"],"outer_terrain_plain"), #old_rivendell camp

  ("dol_guldur_center"      ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x00000003b0050d0d0004b12c000072f5000027d200005f66",[],[],"New_outer_terrain_forest"),
#  ("dol_guldur_center"      ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"),

  ("north_rhun_camp_center" ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x00000001200005000006d9e10000065c00004b3400000dfd",[],["player_chest"],"outer_terrain_rohan"),
  ("gundabad_camp_center"   ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x00000003200005000009c5a200000f5200005bd50000739d",[],["player_chest"],"New_outer_mountains2south_helmsdeep"),
  ] + (is_a_wb_scene==1 and [
  ("ironhill_camp_center"   ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000001a0000500000691a400000fc200004b34000070b7",[],[],"outer_terrain_steppe"),
  ] or [
  ("ironhill_camp_center"   ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007200016da000364d9000060f500007591000064e7",[],[],"outer_terrain_steppe"),
  ]) + [

### GA stub scenes
  ("gondor_castle"      ,sf_indoors, "interior_castle_v", "bo_interior_castle_v", (-100,-100),(100,100),-100,"0",["exit"],[]),
  ] + (is_a_wb_scene==1 and [
  ("minas_tirith_castle",sf_indoors|sf_force_skybox, "mt_hall", "bo_mt_hall", (-1000,-1000),(1000,1000),-100,"0",["exit"],["player_chest"]),
  ] or [
  ("minas_tirith_castle",sf_indoors|sf_force_skybox, "throne_room", "bo_throne_room", (-1000,-1000),(1000,1000),-100,"0",["exit"],["player_chest"]),
  ]) + [
  ("rohan_castle"       ,sf_indoors, "interior_castle_t", "bo_interior_castle_t", (-100,-100),(100,100),-100,"0",["exit"],["player_chest"]),
  ("elf_castle"         ,sf_indoors, "interior_castle_t", "bo_interior_castle_t", (-100,-100),(100,100),-100,"0",["exit"],[]),
  ("mordor_castle"      ,sf_indoors, "interior_castle_t", "bo_interior_castle_t", (-100,-100),(100,100),-100,"0",["exit"],["player_chest"]),
  ("edoras_castle"      ,sf_indoors, "rohan_meduseld_int", "bo_rohan_meduseld_int", (-200,-200),(200,200),-100,"0",["exit"],["player_chest"]),
  ("erebor_castle",sf_indoors ,"erebor_throne_room_b", "bo_erebor_throne_room_b", (-40,-40),(40,40),-100,"0",[],["player_chest"]),  
  #("erebor_castle",sf_indoors ,"interior_gondor_training_room_b", "bo_interior_gondor_training_room_b", (-40,-40),(40,40),-100,"0",[],["player_chest"]),

  ("gondor_tavern" ,sf_indoors, "interior_tavern_b"    ,"bo_interior_tavern_b"    , (-100,-100),(100,100),-100,"0",["exit"],[]),
  ("rohan_tavern"  ,sf_indoors, "interior_tavern_b"    ,"bo_interior_tavern_b"    , (-100,-100),(100,100),-100,"0",["exit"],[]),
  ("elf_tavern"    ,sf_indoors, "interior_tavern_b"    ,"bo_interior_tavern_b"    , (-100,-100),(100,100),-100,"0",["exit"],[]),
  ("mordor_tavern" ,sf_indoors, "interior_tavern_b"    ,"bo_interior_tavern_b"    , (-100,-100),(100,100),-100,"0",["exit"],[]),

  ("gondor_prison",sf_indoors,"interior_prison_a", "bo_interior_prison_a", (-100,-100),(100,100),-100,"0",[],[]),
  ("rohan_prison" ,sf_indoors,"interior_prison_a", "bo_interior_prison_a", (-100,-100),(100,100),-100,"0",["exit"],[]),
  ("mordor_prison",sf_indoors,"interior_prison_a", "bo_interior_prison_a", (-100,-100),(100,100),-100,"0",[],[]),
  ("elf_prison"   ,sf_indoors,"interior_prison_a", "bo_interior_prison_a", (-100,-100),(100,100),-100,"0",[],[]),

# Arenas (these are defined per party in module_constants, we can have individual arenas for special cities if we want!)
  ("gondor_arena",sf_generate,"none", "none", (0,0),(100,100),-100,"0xa0001d9300031ccb0000156f000048ba0000361c",[],[],"outer_terrain_plain"),
  ("rohan_arena",sf_generate,"none", "none", (0,0),(120,120),-100,"0x00000001324a9cba0005194a000041ef00005ae800003c55",[],[], "outer_terrain_rohan"),
  ("dale_arena",sf_generate,"none", "none", (0,0),(100,100),-100,"0xa0001d9300031ccb0000156f000048ba0000361c",[],[],"outer_terrain_rohan"),
  ("elf_arena",sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),
  ("beorn_arena",sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),
  ("dwarf_arena",sf_indoors ,"interior_gondor_training_room_b", "bo_interior_gondor_training_room_b", (-40,-40),(40,40),-100,"0",[],[]),
  ("mordor_arena",sf_generate,"none","none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_mountains2west_mordor"),
  ("isengard_arena",sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000073000148000025896000074e600006c260000125a",[],[],"outer_terrain_rohan"),
  ("khand_arena",sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730001d9300031ccb0000156f000048ba0000361c",[],[],"outer_terrain_flat"),
  ("rhun_arena",sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000073000148000025896000074e600006c260000125a",[],[],"outer_terrain_flat"),
  ("harad_arena",sf_generate,"none", "none",(0,0),(100,100),-100,"0x000000072005591e00040506000059a100002cd500005052",[],[],"outer_terrain_steppe"),
  ("umbar_arena",sf_generate,"none", "none",(0,0),(100,100),-100,"0x3002898a80051d440000154e000026f300004e2d",[],[]),

# stub leftovers (unused, clear them up in the code)
  ("town_store",sf_indoors ,"interior_town_house_i", "bo_interior_town_house_i", (-100,-100),(100,100),-100,"0",    [],[]),
  ("town_alley",sf_generate,"none", "none", (0,0),(100,100),-100,"0x300bc5430001e0780000448a0000049f00007932",    [],[],"outer_terrain_plain"),
  ("town_walls",sf_generate,"none", "none", (0,0),(100,100),-100,"0x0000000130028e320005e17b00004a14000006d70000019d",    [],[],"outer_terrain_plain"),
  ("castle_1_exterior",sf_generate,"none", "none", (0,0),(100,100),-100,"0x30054da28004050000005a76800022aa00002e3b", [],[],"outer_terrain_steppe"),
  ("castle_1_interior",sf_indoors, "dungeon_entry_a", "bo_dungeon_entry_a", (-100,-100),(100,100),-100,"0",  ["exit"],[]),
  ("castle_1_prison",sf_indoors,"interior_prison_a", "bo_interior_prison_a", (-100,-100),(100,100),-100,"0", [],[]),

#!!Villages !!#
("village_1"   ,sf_generate,"none","none",(0,0),(100,100),-100,"0x000000033000148000025896000074e600006c260000125a",[],[],"outer_terrain_plain"), #InVain Former woodsmen village was nice, we keep it for the village quest.
#("village_1" ,sf_generate,"none", "none", (0,0),(100,100),-100,"0x0000000030081763000589620000338e00004f2c00005cfb",   [],[],"outer_terrain_plain"),
# put this instead of village2 to preserve number of scenes
("esgaroth_old_ruins",sf_generate,"none", "none",(0,0),(200,200),-100,"0x0000000730000500000c8f2100002ca5000022aa000031a8",[],[],"outer_terrain_seaside_1"), #Empty scene, can be replaced

#Leftover scenes / not implemented? Except first one, all are simply autogenerated
("field_1",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000033a059a5a0009525600002005000060e300001175",    [],[],"outer_terrain_plain"),
("field_2",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000033a079a3f000a3a8000006dfd000030a100006522",    [],[],"outer_terrain_steppe"),
("field_3",sf_generate,"none", "none", (0,0),(100,100),-100,"0x30054da28004050000005a76800022aa00002e3b",    [],[],"outer_terrain_steppe"),
("field_4",sf_generate,"none", "none", (0,0),(100,100),-100,"0x30054da28004050000005a76800022aa00002e3b",    [],[],"outer_terrain_steppe"),
("field_5",sf_generate,"none", "none", (0,0),(100,100),-100,"0x30054da28004050000005a76800022aa00002e3b",    [],[],"outer_terrain_steppe"),

## Abhuva TLD Battlefield Scenes (unused, use for interiors?)
("battle_scene_plain_01",sf_generate|sf_auto_entry_points,"none", "none", (0,0),(240,240),-0.5,"0x000000023001c600000691a400003efe00004b34000059be",[],[], "outer_terrain_plain"), ## Plain Battle Field with a small farm and a road crossing the map
("battle_scene_plain_02",sf_generate|sf_auto_entry_points,"none", "none", (0,0),(240,240),-0.5,"0x0000000230054800000691a400003efe00004b34000011d9",[],[], "outer_terrain_plain"), ## Plain Battle Field with a road crossing the map and a river with small bridge, lake with a fisher-house
("bridge_1",sf_generate,"none", "none", (0,0),(120,120),-100,"0x3a078bb2000589630000667200002fb90000179c",[],[], "outer_terrain_plain"), ## Plain Bridge Battle with destroyed buildings
("battle_scene_mountain_forest_01",sf_generate|sf_auto_entry_points,"none", "none", (0,0),(240,240),-0.5,"0x0000000230054800000691a400003efe00004b34000011d9",[],[], "outer_terrain_plain"), ## Mountain Forest with mines

("aw_tomb"              ,sf_indoors,"aw_tomb"                       , "bo_aw_tomb"                  , (-100,-100),(240,240),-100,"0",[],[]),
("dol_amroth_castle"    ,sf_indoors,"interior_castle_dolamroth"     , "bo_interior_castle_dolamroth", (-100,-100),(100,100),-100,"0",[],[]),
("isengard_castle"      ,sf_indoors,"interior_throneroom_isengard_a", "bo_interior_castle_gondor_d" , (-100,-100),(100,100),-100,"0",[],["player_chest"]),
("gondor_castle_a"      ,sf_indoors,"interior_castle_gondor_a"      , "bo_interior_castle_gondor_a" , (-100,-100),(100,100),-100,"0",[],[]),
("gondor_castle_b"      ,sf_indoors,"interior_castle_gondor_b"      , "bo_interior_castle_gondor_b" , (-100,-100),(100,100),-100,"0",[],[]),
("gondor_castle_c"      ,sf_indoors,"interior_castle_gondor_c"      , "bo_interior_castle_gondor_c" , (-100,-100),(100,100),-100,"0",[],[]),
("cair_andros_castle"   ,sf_indoors,"interior_castle_gondor_d"      , "bo_interior_castle_gondor_d" , (-100,-100),(100,100),-100,"0",[],[]),
("west_osgiliath_castle",sf_indoors,"interior_castle_gondor_d"      , "bo_interior_castle_gondor_d" , (-100,-100),(100,100),-100,"0",[],[]),
("east_osgiliath_castle",sf_indoors,"interior_castle_gondor_b"      , "bo_interior_castle_gondor_b" , (-100,-100),(100,100),-100,"0",[],[]),
("henneth_annun_castle" ,sf_indoors,"mesh_henneth_annun"            , "bo_henneth_annun"            , (-100,-100),(100,100),-100,"0",[],[]),
("rohan_castle_a"       ,sf_indoors,"interior_castle_rohan_a"       , "bo_interior_castle_i"        , (-100,-100),(100,100),-100,"0",[],[]),
("rohan_castle_b"       ,sf_indoors,"interior_castle_rohan_b"       , "bo_interior_castle_j"        , (-100,-100),(100,100),-100,"0",[],[]),
("esgaroth_castle"      ,sf_indoors,"interior_castle_rohan_b"       , "bo_interior_castle_j"        , (-100,-100),(100,100),-100,"0",[],[]),
("mordor_castle_a"      ,sf_indoors,"interior_castle_mordor_a"      , "bo_interior_castle_mordor_a" , (-100,-100),(100,100),-100,"0",[],[]),
("mordor_castle_b"      ,sf_indoors,"interior_castle_morgul"      , "bo_interior_castle_gondor_d" , (-100,-100),(100,100),-100,"0",[],["player_chest"]),

("rhun_south_camp_center"         ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x0000000730001d9300031ccb0000156f000048ba0000361c",[],[],"outer_terrain_flat"),

  ] + (is_a_wb_scene==1 and [
("rhun_north_camp_center"         ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001a0000500000d2348000032a500003c7f00007714",[],[],"outer_terrain_steppe"), #by Aiden
  ] or [
("rhun_north_camp_center"         ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x0000000730001d9300031ccb0000156f000048ba0000361c",[],[],"outer_terrain_flat"),
  ]) + [

("gundabad_ne_outpost_center"     ,sf_generate,"none","none",(0,0),(100,100),-100,"0x000000032000050000035d470000156f000048ba0000361c",[],[],"outer_mountains2north"),
("gundabad_nw_outpost_center"     ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000120054c97000615820000538a00007bcc00005284",[],[],"outer_mountains2north"),
("gundabad_mirkwood_outpost"      ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"),#Kolba
("dol_guldur_north_outpost_center",sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"), #Kolba
("woodelf_west_camp_center"   ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000007300798b2000380e3000037960000573900003f48",[],[],"outer_terrain_forest"),
("goblin_north_outpost_center",sf_generate|sf_no_horses|sf_indoors,"none","none",(0,0),(100,100),-100,"0x00000007300005000008160b00000f768000576c00001d2c",[],[],"0"), #Goblin-town
("goblin_south_outpost_center",sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000320001d9300031ccb000041be000048ba0000361c",[],[],"outer_mountains2west"),
("woodsmen_village2_center"   ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000b0000500000461190000482500006c26000038f2",[],[],"outer_terrain_forest"),
#backup("woodsmen_village2_center"   ,sf_generate,"none","none",(0,0),(100,100),-100,"0x000000073000148000025896000074e600006c260000125a",[],[],"outer_terrain_plain"),
("beorning_village_center"    ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000b00893e30004851f0000457900001af000004ca7",[],[],"outer_terrain_plain"),
#backup ("beorning_village_center"    ,sf_generate,"none","none",(0,0),(100,100),-100,"0x000000073000148000025896000074e600006c260000125a",[],[],"outer_terrain_plain"),
("isengard_center_flooded"    ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000320000500000d234800002ba680005bd500005b5d",[],[],"outer_terrain_isen_low_1"),

] + (is_a_wb_scene==1 and [
("erebor_gate"   ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000130000500000d23480000755000005bd50000739d",[],[],"outer_mountains2west"),
] or [
("erebor_gate"   ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_mountains2west"),
]) + [

#("erebor_dungeon_01",sf_indoors,"dungeon_a","bo_dungeon_a",(-100,-100),(100,100),-100,"0",[],[]),

("thranduil_hall_room"     ,sf_indoors|sf_force_skybox,"thranduil_hall", "bo_thranduil_hall", (-100,-100),(100,100),-100,"0",[],["player_chest"]),
("random_scene_parade"  ,sf_generate,"none","none",(0,0),(220,220),-0.5,"0x00000002362011800004411a00003efe00004b34000059be",[],[],"outer_terrain_forest"),#GA, faction troops parade (custom battle)

("beorn_castle",sf_indoors,"lofotrinterior2","bo_lofotrinterior2",(-100,-100),(100,100),-100,"0",[],["player_chest"]),
("moria_castle",sf_indoors|sf_muddy_water,"interior_round_isengard","bo_interior_round_isengard",(-100,-100),(100,100),-100,"0",[],[]), #unused
("hornburg_castle",sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000240002800000691a400003efe00004b34000059be",[],[]),
("morannon_castle",sf_generate,"none","none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],["player_chest"],"outer_mountains2west_mordor"),

# Legendary places
("amon_hen"   ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000630000500000c2304000003ce000047ca0000794b",[],[],"outer_terrain_osgiliath_9"),
("deadmarshes",sf_generate|sf_auto_entry_points|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_flat"),
("mirkwood"   ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),
("fangorn"    ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),

# Siege scenes
("cair_andros_siege"   ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_osgiliath_9"),

] + (is_a_wb_scene==1 and [
("dale_siege"          ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000330000500000d2348000006810000219700002120",[],[],"New_outer_terrain_tirith_1"),
] or [
("dale_siege"          ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000003200005000007a9ea000006810000219700002120",[],[],"outer_terrain_plain"),
]) + [

("west_emnet_siege"    ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000320045abc000308c4000029d9000033bd000009b9",[],[],"outer_terrain_rohan"),

] + (is_a_wb_scene==1 and [
("minas_tirith_siege"  ,sf_generate,"none","none",(0,0),(200,200),-100,"0x0000000330000500000d234800007e03000001780000021b",[],[],"New_outer_terrain_tirith_2"),
] or [
("minas_tirith_siege"  ,sf_generate,"none","none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_tirith_1"),
]) + [

("pelargir_siege"      ,sf_generate,"none","none",(0,0),(200,200),-100,"0x00000006300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_seaside_1"),
("linhir_siege"        ,sf_generate,"none","none",(0,0),(200,200),-100,"0x000000042005591e00040506000059a100002cd500005052",[],[],"outer_terrain_steppe"),
("dol_amroth_siege"    ,sf_generate,"none","none",(0,0),(200,200),-100,"0x0000000130000500000d234800000f5200005bd50000739d",[],[],"New_outer_terrain_seaside_east_1"),
("edhellond_siege"     ,sf_generate,"none","none",(0,0),(200,200),-100,"0x00000000300798b2000380e3000037960000573900003f48",[],[],"New_outer_terrain_seaside_north_1"),
("lossarnach_siege"    ,sf_generate,"none","none",(0,0),(200,200),-100,"0x00000007300005000006ada4000051a90000386b00003791",[],[],"outer_mountains2west"),
("tarnost_siege"       ,sf_generate,"none","none",(0,0),(200,200),-100,        "0x30050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_mountains2east"),
("erech_siege"         ,sf_generate,"none","none",(0,0),(200,200),-100,        "0x3000148000025896000074e600006c260000125a",[],[],"outer_mountains2north"),
("pinnath_gelin_siege" ,sf_generate,"none","none",(0,0),(200,200),-100,        "0x300416a600035cd600007ee80000012100003fbc",[],[],"outer_terrain_plain"),
("ethring_siege"       ,sf_generate,"none","none",(0,0),(200,200),-100,"0x000000042005591e00040506000059a100002cd500005052",[],[],"outer_terrain_steppe"),
("west_osgiliath_siege",sf_generate,"none","none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_osgiliath_9"),
("edoras_siege"        ,sf_generate,"none","none",(0,0),(200,200),-100,"0x00000007200005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_rohan"),
("aldburg_siege"       ,sf_generate,"none","none",(0,0),(100,100),-100,"0x000000072007956000025896000037e800000e860000674b",[],[],"outer_mountains2south"),
("hornburg_siege"      ,sf_generate,"none","none",(0,0),(100,100),-100,        "0x0000000330000500000d234800006228000053bf00004eb9",[],[],"outer_terrain_helms_deep"),
#("hornburg_siege"      ,sf_generate,"none","none",(0,0),(100,100),-100,        "0x00001d63c005114300006228000053bf00004eb9",[],[],"outer_mountains2south"),
("east_emnet_siege"    ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000320045abc000308c4000029d9000033bd000009b9",[],[],"outer_terrain_rohan"),
("westfold_siege"      ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000620049cbd00025896000048e90000164400002b3f",[],[],"outer_terrain_rohan"),
("eastfold_siege"      ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000007a009c7070002589600002b6300001ef60000122e",[],[],"outer_mountains2south"),
("east_osgiliath_siege",sf_generate,"none","none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_osgiliath_9"),
("cirith_ungol_siege"    ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000002200e95140006398d0000372f00004a8900005ff2",[],[],"outer_terrain_rohan"),
# various battlefield scenes, use these slots for future sieges
("custom_1" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x0000000230000500000691a4000009e100004b34000070b7",[],[],"outer_terrain_plain"), #plain big
("custom_2" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x0000000130000500000691a4000009e100004b34000070b7",[],[],"outer_terrain_plain"), #plain med
("custom_3" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000001300005000003d8f600003efe00004b34000059be",[],[],"outer_terrain_plain"), #plain small
("custom_4" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x0000000220000500000691a40000065c00004b34000070b7",[],[],"outer_terrain_rohan"), 	#steppe big
("custom_5" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x0000000120000500000691a40000065c00004b34000070b7",[],[],"outer_terrain_rohan"),	#steppe med
("custom_6" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000001200005000003d8f600003efe00004b34000059be",[],[],"outer_terrain_rohan"),	#steppe small
("custom_7" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000002b0000500000691a40000065c00004b3400000dfd",[],[],"outer_terrain_forest"),	#forest big
("custom_8" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000001b0000500000691a40000065c00004b34000039d4",[],[],"outer_terrain_forest"),	#forest med
("custom_9" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000001b00005000003d8f60000442500004b340000152d",[],[],"outer_terrain_forest"),	#forest small
#("battlefield10",sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000001b119134800058d66000023ad000035de0000292a",[],[],"outer_terrain_forest"),
("small_ford"   ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x0000000235864d634005c96d0000734a00004b340000734a",[],[],"outer_terrain_plain"),
("rivercross"   ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000030081763000989a20000338e00004f2c00005cfb",[],[],"outer_terrain_plain"),

("tld_sorcerer_forest_a" ,sf_generate|sf_muddy_water,"none","none",(0,0),(200,200),-0.5,"0x00000001b01917000004e93c00007b15000077bd00004d24",[],[],"outer_terrain_forest"),
("tld_sorcerer_forest_b" ,sf_generate|sf_muddy_water,"none","none",(0,0),(200,200),-0.5,"0x00000000b00ed9260002c8b000007af400006f7d00001e9c",[],[],"outer_terrain_forest"),
("tld_sorcerer_forest_c" ,sf_generate|sf_muddy_water,"none","none",(0,0),(200,200),-0.5,"0x00000000b00c9c1c0004691300007af400005f5f00007f2f",[],[],"outer_terrain_forest"),

("moria_secret_entry" ,sf_generate|sf_auto_entry_points|sf_muddy_water,"none","none",(0,0),(200,200),-0.5,"0x0000000240004d634005c96d0000734a00004b340000734a",[],[],"outer_terrain_plain"),

("moria_deep_mines" ,sf_generate|sf_auto_entry_points|sf_muddy_water,"none","none",(0,0),(200,200),-0.5,"0x0000000640002800000691a400003efe00004b34000059be",[],[]),

("advcamp_good" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_bad" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("isengard_underground" ,sf_generate|sf_muddy_water,"none","none",(0,0),(200,200),-100,"0x0000000440000500000c9b2600003efe00004b34000059be",[],[]),

#forest scenes for using in rnd
("forest_fangorn1"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),
("forest_fangorn2"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),
("forest_fangorn3"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),
("forest_fangorn4"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),
("forest_fangorn5"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),

("forest_ithilien_small1"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest_ithilien_small2"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest_ithilien_small3"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest_ithilien_small4"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest_ithilien_small5"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),

("forest_lorien1"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest_lorien2"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest_lorien3"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest_lorien4"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest_lorien5"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),

#big mirkwood scenes (+placeholders) moved to end of file
("forest_mirkwood_small1"  ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000b002c90d0002308c00005a8f0000786900001ef5",[],[],"outer_terrain_forest"), #0x00000000b6a2c90d0002308c00005a8f0000786900001ef5
("forest_mirkwood_small2"  ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000b002c90d0002308c000010a90000786900001ef5",[],[],"outer_terrain_forest"), #0x00000000b262c90d0002308c000010a90000786900001ef5
("forest_mirkwood_small3"  ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000b002c90d0002308c000010a90000786900001ef5",[],[],"outer_terrain_forest"),
("forest_mirkwood_small4"  ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000b142c90d0002308c000010a90000786900001ef5",[],[],"outer_terrain_forest"),
("forest_mirkwood_small5"  ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000b002c90d0002308c00005c5a0000786900001ef5",[],[],"outer_terrain_forest"), #old terrain code for all mirkwood scenes: 0x00000000bc62c90d0002308c000048850000786900001ef5

("forest_firien1"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest_firien2"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest_firien3"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),

("forest_end"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest_some1"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest_some2"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),

("forest1"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest2"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest3"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest4"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("forest5"  ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),

("duel_scene",sf_generate,"none", "none", (-40,-40),(40,40),-100,"0x00000006300005000002308c00003005000018b300001d92",[],[],"outer_terrain_plain"),

("ford_big1" ,sf_generate,"none","none",(0,0),(100,100),-100,"0x000000023c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_anduin"),
("ford_big2" ,sf_generate,"none","none",(0,0),(100,100),-100,"0x000000023c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_anduin"),
("ford_big3" ,sf_generate,"none","none",(0,0),(100,100),-100,"0x000000023c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_anduin"),

("ford_small1"  ,sf_generate,"none","none",(0,0),( 40, 40),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_river_middle"),
("ford_small2"  ,sf_generate,"none","none",(0,0),( 40, 40),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_river_middle"),
("ford_small3"  ,sf_generate,"none","none",(0,0),( 40, 40),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_river_middle"),

  ] + (is_a_wb_scene==1 and [
("erebor_siege"   ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000130000500000d23480000755000005bd50000739d",[],[],"outer_mountains2west"),
("gundabad_siege" ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x00000003200005000009c5a200000f5200005bd50000739d",[],[],"New_outer_mountains2south_helmsdeep"),
("dol_guldur_siege",sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x00000003b0050d0d0004b12c000072f5000027d200005f66",[],[],"New_outer_terrain_forest"),
("umbar_camp_siege",sf_generate,"none", "none",(0,0),(100,100),-100,"0x3002898a80051d440000154e000026f300004e2d",[],[],"New_outer_terrain_seaside_east_1"),
  ] or [
("erebor_siege"   ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_mountains2north"),
("gundabad_siege" ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x00000003200005000009c5a200000f5200005bd50000739d",[],[],"New_outer_mountains2south_helmsdeep"),  
("dol_guldur_siege",sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x00000003b0050d0d0004b12c000072f5000027d200005f66",[],[],"New_outer_terrain_forest"),
("umbar_camp_siege",sf_generate,"none", "none",(0,0),(100,100),-100,"        0x3002898a80051d440000154e000026f300004e2d",[],[],"New_outer_terrain_seaside_east_1"),
  ]) + [

("advcamp_good_siege",sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("moria_siege"      ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005000008160b00000f768000576c00001d2c",[],[]),
("minas_morgul_siege",sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x0000000330000500000d23480000274f00005bd50000739d",[],[],"New_outer_mountains2east_mordor"),
	#("minas_morgul_siege",sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_mountains2west_mordor"),
("morannon_siege"    ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_mountains2west_mordor"),

] + (is_a_wb_scene==1 and [
("minas_tirith_outside" ,sf_generate|sf_auto_entry_points,"none","none",(84,457),( 339, 532),-100.0,"0x0000000330000500000d234800007e03000001780000021b",[],[],"New_outer_terrain_tirith_2"), #InVain changed terrain code: Has grass now!
] or [
("minas_tirith_outside" ,sf_generate|sf_auto_entry_points,"none","none",(84,457),( 339, 532),-100.0,"0x00000003300005000009c5a20000348600005bd50000739d",[],[],"outer_terrain_tirith_1"), #InVain changed terrain code: Has grass now!
]) + [

("isengard_outside" ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),( 90, 90),-100.0,"0x000000032001c500000791fd0000738000005bd50000739d",[],[],"outer_terrain_isen_low_far"),

  ] + (is_a_wb_scene==1 and [
("erebor_outside" ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000001a0000500000691a4000009e100004b34000070b7",[],[],"outer_terrain_rohan"),
  ] or [
("erebor_outside" ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000001a0000500000691a4000009e100004b34000070b7",[],[],"outer_terrain_rohan"),
  ]) + [

("old_forest_road"  ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000b002c90d0002308c00000a060000786900001ef5",[],[],"outer_terrain_forest"),
("great_east_road"  ,sf_generate|sf_randomize,"none","none",(0,0),(90,90),-0.5,"0x000000025c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_flat"),

#CC: Scenes for lost spears quest (based on moria)

("underground_warehouse" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013440050000050d4500003efe00004b34000059be",[],[],"outer_terrain_plain"),
("amath_dollen_fortress",sf_generate,"none","none",(0,0),(90,90),-0.5,"0x000000025c602800000691a400003efe00004b34000059be",[],[],"outer_terrain_flat"),

("mirkwood_ambush"  ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),
("mountain_ambush" ,sf_generate|sf_randomize,"none","none",(0,0),( 90, 90),-0.5,"0x000000012c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),

##Kham Quest Scenes

("lair_forest_bandits",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000000b00326d90003ecfb0000657e0000213500002461",  [],[],"outer_terrain_plain"), #Ring Hunters Lair
("start_lorien"  ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),
("start_woodelf"  ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000bc62c90d0002308c000048850000786900001ef5",[],[],"outer_terrain_forest"),
("start_rivendell"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),

("village_rohan",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000000200a98d00009aa68000069df000021f700001290",  [],[],"outer_terrain_rohan"),
("village_rohan_2" ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000120090a9200052d4f00005c3000004b3400004e30",[],[],"outer_terrain_rohan"),


("scout_camp_mirk_evil_small",sf_generate|sf_muddy_water,"none", "none", (0,0),(100,100),-100,"0x00000001b00a11bd8002b8b6000059ce000067f400007f2e",  [],[],"outer_terrain_forest"),
("scout_camp_mirk_evil_big",sf_generate|sf_muddy_water,"none", "none", (0,0),(100,100),-100,"0x00000001b00a11bd8002b8b6000059ce000067f400007f2e",  [],[],"outer_terrain_forest"),
("scout_camp_mirk_good_small",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000001b00a11bd8002b8b6000059ce000067f400007f2e",  [],[],"outer_terrain_forest"),
("scout_camp_mirk_good_big",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000001b00a11bd8002b8b6000059ce000067f400007f2e",  [],[],"outer_terrain_forest"),

("scout_camp_rohan_evil_small",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000000200f96d700025896000074ef000021f700007ddd",  [],[],"outer_terrain_rohan"),
("scout_camp_rohan_evil_big",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000000200f96d700025896000074ef000021f700007ddd",  [],[],"outer_terrain_rohan"),
("scout_camp_rohan_good_small",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000000200f96d700025896000074ef000021f700007ddd",  [],[],"outer_terrain_rohan"),
("scout_camp_rohan_good_big",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000000200f96d700025896000074ef000021f700007ddd",  [],[],"outer_terrain_rohan"),

("scout_camp_north_good_small",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000001328b9d0b0002c4ab00003e4d00004b34000048a2",  [],[],"outer_mountains2north"),
("scout_camp_north_good_big",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000001328b9d0b0002c4ab00003e4d00004b34000048a2",  [],[],"outer_mountains2north"),
("scout_camp_north_evil_small",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000001328b9d0b0002c4ab00003e4d00004b34000048a2",  [],[],"outer_mountains2north"),
("scout_camp_north_evil_big",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000001328b9d0b0002c4ab00003e4d00004b34000048a2",  [],[],"outer_mountains2north"),

("scout_camp_gondor_good_small",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000001a6681da50003ccef00005c3000004b34000071fb",  [],[],"outer_mountains2south"),
("scout_camp_gondor_good_big",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000001a6681da50003ccef00005c3000004b34000071fb",  [],[],"outer_mountains2south"),
("scout_camp_gondor_evil_small",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000001a6681da50003ccef00005c3000004b34000071fb",  [],[],"outer_mountains2south"),
("scout_camp_gondor_evil_big",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000001a6681da50003ccef00005c3000004b34000071fb",  [],[],"outer_mountains2south"),

("black_shield_fortress" ,sf_generate,"none","none",(84,457),( 339, 532),-100.0,"0x00000001200005000009325a00006ec70000053f00001892",[],[],"outer_mountains2north"),
("black_shield_fortress_siege_easterlings" ,sf_generate,"none","none",(84,457),( 339, 532),-100.0,"0x00000001200005000009325a00006ec70000053f00001892",[],[],"outer_mountains2north"),
("black_shield_fortress_siege_player" ,sf_generate,"none","none",(84,457),( 339, 532),-100.0,"0x00000001200005000009325a00006ec70000053f00001892",[],[],"outer_mountains2north"),

## In Vain Dale / Esgaroth interiors
("dale_castle"          ,sf_indoors|sf_force_skybox, "interior_castle_dale",   "bo_interior_castle_m", (-100,-100),(100,100),-100,"0",["exit"],["player_chest"]),
("esgaroth_castle"      ,sf_indoors|sf_force_skybox, "interior_castle_rohan_a", "bo_interior_castle_i",(-100,-100),(100,100),-100,"0",[],[]),

## In Vain New Ambience Scenes
("osgiliath_outskirts" ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000030000500000334cc000025df00004ec1000041e7 ",[],[],"outer_terrain_flat"),


## In Vain New Siege Scenes

("esgaroth_siege"        ,sf_generate,"none", "none",(0,0),(200,200),-100,"0x0000000730000500000c8f2100002ca5000022aa000031a8",[],[],"New_outer_terrain_seaside_1"),
("woodelf_camp_siege"    ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000001b01918d980058d66000023ad0000751200006b67",[],[],"outer_terrain_forest"),
("woodsmen_village_siege",sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000000200005d000057d5e000074e600006c2600006d0d",[],[],"outer_terrain_plain"),
("woodelf_west_camp_siege"   ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000007300798b2000380e3000037960000573900003f48",[],[],"outer_terrain_forest"),
("rivendell_camp_siege"  ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000000300349e300084e1600005afd00006c26000063e2",[],["player_chest"],"outer_terrain_plain"),

("woodsmen_village2_siege"   ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000b0000500000461190000482500006c26000038f2",[],[],"outer_terrain_forest"),
("beorning_village_siege"    ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000000b00893e30004851f0000457900001af000004ca7",[],[],"outer_terrain_plain"),
("troll_cave_siege"      ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x00000001b00005000005a16c00006794000027d200006794",[],[],"outer_mountains2north"),#Kolba
("dunland_camp_siege"    ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x0000000120000500000691a40000065c00004b34000070b7",[],["player_chest"],"outer_terrain_rohan"),
("harad_camp_siege"      ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x000000072005591e00040506000059a100002cd500005052",[],["player_chest"],"outer_terrain_steppe"),
("khand_camp_siege"      ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x0000000020040de3000699aa00005234000048ba000004b5",[],["player_chest"],"outer_terrain_rohan"),
("north_rhun_camp_siege" ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x00000001200005000006d9e10000065c00004b3400000dfd",[],["player_chest"],"outer_terrain_rohan"),
("rhun_south_camp_siege"         ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x0000000730001d9300031ccb0000156f000048ba0000361c",[],[],"outer_terrain_flat"),

  ] + (is_a_wb_scene==1 and [
("rhun_north_camp_siege"         ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001a0000500000d2348000032a500003c7f00007714",[],[],"outer_terrain_steppe"), #by Aiden
  ] or [
("rhun_north_camp_siege"         ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x0000000730001d9300031ccb0000156f000048ba0000361c",[],[],"outer_terrain_flat"),
  ]) + [

## In Vain Village Scenes

("village_gondor",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000000a00005000006118400005c3000004b3400005792",  [],[],"outer_mountains2south"),
("village_gondor_2",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000000200a98d00009aa68000069df000021f700001290",  [],[],"outer_terrain_rohan"),

("orc_sentry_camp_center_siege" ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000003300005000009c5a200000f5200005bd50000739d",[],[],"outer_terrain_osgiliath_9"),
("uruk_hai_outpost_center_siege",sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x00000007300014800002b4aa000074e600006c260000125a",[],[],"outer_terrain_rohan"),
("uruk_hai_h_camp_center_siege" ,sf_generate|sf_muddy_water,"none", "none",(0,0),(100,100),-100,"0x0000000020054b320004390d00003b3500006f8c00006dbd",[],[],"outer_terrain_plain"),
("uruk_hai_r_camp_center_siege" ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000003200014800002b4aa000074e600006c260000125a",[],[],"New_outer_terrain_anduin"),
("gundabad_ne_outpost_center_siege"     ,sf_generate,"none","none",(0,0),(100,100),-100,"0x000000032000050000035d470000156f000048ba0000361c",[],[],"outer_mountains2north"),
("gundabad_nw_outpost_center_siege"     ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000120054c97000615820000538a00007bcc00005284",[],[],"outer_mountains2north"),
("gundabad_mirkwood_outpost_siege"      ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"),#Kolba
("dol_guldur_north_outpost_center_siege",sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"), #Kolba
("goblin_north_outpost_center_siege",sf_generate,"none","none",(0,0),(100,100),-100,"0x00000007300005000008160b00000f768000576c00001d2c",[],[],"0"),
("goblin_south_outpost_center_siege",sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000320001d9300031ccb000041be000048ba0000361c",[],[],"outer_mountains2west"),

## In Vain Village Scenes Cont'd
("village_anduin",sf_generate,"none", "none", (0,0),(100,100),-100,"0x0000000037220db18006a5aa000061bc80003a9600004852",  [],[],"outer_terrain_plain"),
("village_north",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000003386c9370007b5ed000041800000026d00001a96",  [],[],"outer_terrain_plain"),

## In Vain New Ambience Scenes Cont'd (Most versions are identical scenes with changed spawn positions)

("osgiliath_outskirts_2",sf_generate,"none", "none", (0,0),(100,100),-100,"0x0000000030000500000334cc000025df00004ec1000041e7",  [],[],"outer_terrain_flat"),
("osgiliath_outskirts_3",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000000300005000003d4f1000025df00004ec1000041e7",  [],[],"outer_terrain_flat"),
("osgiliath_outskirts_4",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000000300005000003d4f1000025df00004ec1000041e7",  [],[],"outer_terrain_flat"),
("edoras_outside_1",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000002002cab4000765d700007e16000021f700001290",  [],[],"outer_terrain_rohan"),
("edoras_outside_2",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000002002cab4000765d700007e16000021f700001290",  [],[],"outer_terrain_rohan"),
("hornburg_outside_1",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000002002cab4000765d700007e16000021f700001290",  [],[],"outer_terrain_helmsdeep_far"),
("hornburg_outside_2",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000002002cab4000765d700007e16000021f700001290",  [],[],"outer_terrain_helmsdeep_far"),
("dolamroth_outside_1",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000023c6794b10005153c00005c3000004b3400005792",  [],[],"outer_terrain_seaside_1"), #Dublicates for now, might make the scenes non-randomized, later, so I'll need two for variety
("dolamroth_outside_2",sf_generate|sf_randomize|sf_auto_entry_points,"none", "none", (0,0),(100,100),-100,"0x000000023c6794b10005153c00005c3000004b3400005792",  [],[],"outer_terrain_seaside_1"), #randomized
("morannon_outside_1",sf_generate|sf_muddy_water,"none", "none", (0,0),(100,100),-100,"0x00000000b01489340005014000002601000021f700001290",  [],[],"New_outer_mountains2south_morannon"),
("morannon_outside_2",sf_generate|sf_muddy_water,"none", "none", (0,0),(100,100),-100,"0x00000000b01489340005014000002601000021f700001290",  [],[],"New_outer_mountains2south_morannon"),
("dolguldur_outside_1",sf_generate|sf_muddy_water,"none", "none", (0,0),(100,100),-100,"0x00000001b01917000004e93c00007b15000077bd00004d24",  [],[],"outer_terrain_forest"),
("dolguldur_outside_2",sf_generate|sf_muddy_water,"none", "none", (0,0),(100,100),-100,"0x00000001b01917000004e93c00007b15000077bd00004d24",  [],[],"outer_terrain_forest"),
("beorn_outside_1",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000000b062c90d0005a96a000075f30000786900001ef5",  [],[],"outer_terrain_plain"),
("beorn_outside_2",sf_generate,"none", "none", (0,0),(100,100),-100,"0x00000000b062c90d0005a96a000075f30000786900001ef5",  [],[],"outer_terrain_plain"),
("moria_outside_1",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000002000050000075dde00000863000041e20000070c",  [],[],"outer_terrain_dimrill"),
("moria_outside_2",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000002000050000075dde00000863000041e20000070c",  [],[],"outer_terrain_dimrill"),
("dimrill_dale" ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),( 100, 100),-100.0,"0x00000002d00d16e38005c57300000863000041e20000739d",[],[],"outer_terrain_dimrill"),
("carrock_nearby_1",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000002002cab4000765d700007e16000021f700001290",  [],[],"outer_terrain_rohan"),
("carrock_nearby_2",sf_generate,"none", "none", (0,0),(100,100),-100,"0x000000002002cab4000765d700007e16000021f700001290",  [],[],"outer_terrain_rohan"),
("esgaroth_outside_1",sf_generate|sf_randomize,"none", "none", (0,0),(100,100),-100,"0x00000003a7268ca70005715f00003feb00005bd50000739d",  [],[],"New_outer_terrain_seaside_west"),
("esgaroth_outside_2",sf_generate|sf_randomize,"none", "none", (0,0),(100,100),-100,"0x00000003a7268ca70005715f00003feb00005bd50000739d",  [],[],"New_outer_terrain_seaside_west"),
("s_erebor" ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),( 100, 100),-100.0,"0x00000003a7268ca70005715f00003feb00005bd50000739d",[],[],"outer_terrain_plain"),
("hornburg_near" ,sf_generate,"none", "none",(0,0),(100,100),-100,        "0x0000000330000500000d234800006228000053bf00004eb9",[],[],"outer_terrain_helms_deep"), #right in front of hornburg
	#("hornburg_near" ,sf_generate,"none", "none",(0,0),(100,100),-100,        "0x000000002000056300075d6700004d84800053bf00004eb9",[],[],"outer_terrain_rohan"), #right in front of hornburg
("lebennin_1" ,sf_generate,"none","none",(0,0),( 100, 100),-100.0,"0x000000013c640c2d0007d1ef00007a7400005bd5000035b2",[],[],"outer_mountains2south"),  #flower hills 1
("lebennin_2" ,sf_generate,"none","none",(0,0),( 100, 100),-100.0,"0x000000013c640c2d0007d1ef0000339200005bd5000035b2",[],[],"outer_terrain_plain"), #flower hills 1 v2
("lebennin_3" ,sf_generate,"none","none",(0,0),( 100, 100),-100.0,"0x000000013c640c120007d1ef00007a7400005bd5000039bf",[],[],"outer_terrain_plain"), #flower hills 2
("lebennin_4" ,sf_generate,"none","none",(0,0),( 100, 100),-100.0,"0x000000013c640c120007d1ef0000339200005bd5000039bf",[],[],"outer_mountains2south"), #flower hills 2 v2
("lebennin_coast_1" ,sf_generate,"none","none",(0,0),( 100, 100),-100.0,"0x000000003c6005000006cdb000007a7400005bd50000739d",[],[],"New_outer_terrain_seaside_north_1"), #non_random_coast 1
("lebennin_coast_2" ,sf_generate,"none","none",(0,0),( 100, 100),-100.0,"0x000000003c6005000006cdb00000339200005bd50000739d",[],[],"New_outer_terrain_seaside_north_1"), #non_random_coast 2
("lebennin_coast_3" ,sf_generate|sf_randomize,"none","none",(0,0),( 100, 100),-100.0,"0x000000003c6005000006cdb000007a7400005bd50000739d",[],[],"New_outer_terrain_seaside_north_1"), #randomized coast
("lebennin_coast_4" ,sf_generate|sf_randomize,"none","none",(0,0),( 100, 100),-100.0,"0x000000003c6005000006cdb00000339200005bd50000739d",[],[],"New_outer_terrain_seaside_north_1"), #randomized coast
("pelennor_1" ,sf_generate,"none","none",(0,0),( 100, 100),-100.0,"0x00000003300005000009c5a20000132600005bd50000739d",[],[],"New_outer_terrain_tirith_1"), #Minas Tirith in the distance
("pelennor_2" ,sf_generate,"none","none",(0,0),( 100, 100),-100.0,"0x00000000300009b500058d63000062dc00005bd50000739d",[],[],"New_outer_terrain_tirith_1"), #Minas Tirith in the distance
("village_gondor_battlefield_1" ,sf_generate,"none","none",(0,0),( 100, 100),-100.0,"0x00000000a00005000006118400005c3000004b3400005792",[],[],"outer_mountains2south"), # Gondor village
("village_gondor_battlefield_2" ,sf_generate,"none","none",(0,0),( 100, 100),-100.0,"0x00000000a00005000006118400005c3000004b3400005792",[],[],"outer_mountains2south"), # Gondor village
("scout_camp_gondor_battlefield_1" ,sf_generate,"none","none",(0,0),( 100, 100),-100.0,"0x00000001a6681da50003ccef00005c3000004b34000071fb",[],[],"outer_mountains2south"), # Gondor village ruins
("scout_camp_gondor_battlefield_2" ,sf_generate,"none","none",(0,0),( 100, 100),-100.0,"0x00000001a6681da50003ccef00005c3000004b34000071fb",[],[],"outer_mountains2south"), # Gondor village ruins

#sea battle scenes
("sea_battle_south" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000073000050000084e13000006b700007d8d000025fd",[],[],"New_outer_terrain_seaside_east_1"),
("sea_battle_north" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000073000050000084e13000006b700007d8d000025fd",[],[],"New_outer_terrain_seaside_1"),

("dale_village_battlefield_1" ,sf_generate,"none","none",(0,0),( 100, 100),-100.0,"0x000000012000050000075dd200003efe00004b34000059be",[],[],"outer_terrain_plain"), # Dale rural area, by Darnokthemage
("old_tutorial_2",sf_indoors,"tutorial_2_scene", "bo_tutorial_2_scene", (-100,-100),(100,100),-100,"0",[],[]),
("old_tutorial_3",sf_indoors,"tutorial_3_scene", "bo_tutorial_3_scene", (-100,-100),(100,100),-100,"0",[],[]),
("old_tutorial_4",sf_generate,"none", "none", (0,0),(120,120),-100,"0x30000500400360d80000189f00002a8380006d91",[],[], "outer_terrain_plain"),
("thranduils_halls_siege",sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000001400ddb4200058d66000023ad0000751200000359",[],[],"outer_terrain_forest"), 

# some more missing siege scenes

("caras_galadhon_siege"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x0000000030000500000985dc00000e2f000027d200005f66",[],[],"outer_terrain_forest"),
#("caras_galadhon_siege"  ,sf_generate,"none","none",(0,0),( 90, 90),-0.5,"0x000000013c60280000034cd300003efe00004b34000059be",[],[],"outer_terrain_forest"),
("cerin_dolen_siege"     ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"),#Kolba
("cerin_amroth_siege"    ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000730050d0d0002d4b300000e2f000027d200005f66",[],[],"outer_terrain_forest"),#Kolba
  ] + (is_a_wb_scene==1 and [
("ironhill_camp_siege"   ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000001a0000500000691a400000fc200004b34000070b7",[],[],"outer_terrain_steppe"),
  ] or [
("ironhill_camp_siege"   ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007200016da000364d9000060f500007591000064e7",[],[],"outer_terrain_steppe"),
  ]) + [
("isengard_siege"        ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000320000500000d234800002ba680005bd500005b5d",[],[],"outer_terrain_isen"),
  
#Inner siege placeholders
("thranduils_halls_siege_inner",sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000001400ddb4200058d66000023ad0000751200000359",[],[],"outer_terrain_forest"), 
("minas_tirith_siege_inner"  ,sf_generate,"none","none",(0,0),(200,200),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_tirith_1"),
("edoras_siege_inner"        ,sf_generate,"none","none",(0,0),(200,200),-100,"0x00000007200005004009c5a200000f5200005bd50000739d",[],[],"outer_terrain_rohan"),
("hornburg_siege_inner"      ,sf_generate,"none","none",(0,0),(100,100),-100,        "0x00001d63c005114300006228000053bf00004eb9",[],[],"outer_mountains2south"),
("erebor_siege_inner"   ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_mountains2north"),
("morannon_siege_inner"    ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000007300005004009c5a200000f5200005bd50000739d",[],[],"outer_mountains2west_mordor"),
("gundabad_siege_inner" ,sf_generate,"none", "none",(0,0),(100,100),-100,"0x00000003200005000009c5a200000f5200005bd50000739d",[],[],"New_outer_mountains2south_helmsdeep"),
  ] + (is_a_wb_scene==1 and [
("minas_morgul_siege_inner",sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000330000500000d23480000274f00005bd50000739d",[],[],"New_outer_mountains2east_mordor"),
("umbar_camp_siege_inner",sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000740000500000a1e8a000034f880004b040000583d",[],[],"outer_terrain_seaside_north_1"),
("dale_siege_inner"          ,sf_generate,"none","none",(0,0),(100,100),-100,"0x0000000330000500000d2348000006810000219700002120",[],[],"New_outer_terrain_tirith_1"),
  ] or [
("minas_morgul_siege_inner",sf_generate,"none", "none",(0,0),(100,100),-100,"0x0000000330000500000d23480000274f00005bd50000739d",[],[],"New_outer_mountains2east_mordor"),
("umbar_camp_siege_inner",sf_generate,"none", "none",(0,0),(100,100),-100,"        0x3002898a80051d440000154e000026f300004e2d",[],[]),
("dale_siege_inner"          ,sf_generate,"none","none",(0,0),(100,100),-100,"0x00000003200005000007a9ea000006810000219700002120",[],[],"outer_terrain_plain"),
  ]) + [

#Advance Camp placeholders
("advcamp_gondor" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_rohan" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_lorien" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_imladris" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_beorn" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_mirkwood" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_dale" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_erebor" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),

("advcamp_mordor" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_isengard" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_umbar" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_harad" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_khand" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_dunland" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_moria" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_guldur" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_gundabad" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_rhun" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),

("advcamp_gondor_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_rohan_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_lorien_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_imladris_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_beorn_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_mirkwood_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_dale_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_erebor_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),

("advcamp_mordor_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_isengard_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_umbar_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_harad_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_khand_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_dunland_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_moria_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_guldur_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_gundabad_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),
("advcamp_rhun_siege" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013000050000034cd300003efe00004b34000059be",[],[],"outer_terrain_rohan"),

("forest_mirkwood0"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x0000000145d10f8000058d6600007add0000751200007a86",[],[],"outer_terrain_forest"), #beeches
("forest_mirkwood0b"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001b0110f8080058d6600007add80000ff000007a86",[],[],"outer_terrain_forest"), #beeches variant (river)
("forest_mirkwood1"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001b01918d980058d66000023ad0000751200006b67",[],[],"outer_terrain_forest"), #ravine
("forest_mirkwood1b"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001401918d980058d66000023ad0000751200006b67",[],[],"outer_terrain_forest"), #ravine variant (firs)
("forest_mirkwood2"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x0000000140190c8000058d66000023ad0000047f0000292a",[],[],"outer_terrain_forest"), #flat
("forest_mirkwood2b"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001b0190c8080058d66000061450000047f0000292a",[],[],"outer_terrain_forest"), #flat variant (river)
("forest_mirkwood3"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001b019135900058d66000046d4000035de00005298",[],[],"outer_terrain_forest"), #puddles
("forest_mirkwood3b"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x000000014019135980058d66000023ad80004b1a00005298",[],[],"outer_terrain_forest"), #puddles variant (river)
("forest_mirkwood4"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001b019134800058d66000047a8000035de0000292a",[],[],"outer_terrain_forest"), #slope
("forest_mirkwood4b"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x000000014019134800058d66000023ad0000254b0000292a",[],[],"outer_terrain_forest"), #slope (swamp terrain)
("forest_mirkwood5"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001490b56cb00058d66000023ad0000751200006218",[],[],"outer_terrain_forest"), #fir mix
("forest_mirkwood6"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x0000000145d6d18000058d66000037c600005f9900002ad0",[],[],"outer_terrain_forest"), #firs pure + rocks
("forest_mirkwood6b"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001b016d18080058d6600007c11800030cf00002ad0",[],[],"outer_terrain_forest"), #firs pure + rocks variant (river)
("forest_mirkwood7"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x000000014019056300058d66000037c60000416c0000385d",[],[],"outer_terrain_forest"), #swamp
("forest_mirkwood8"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001401917000004e93c00000aeb000077bd00004d24",[],[],"outer_terrain_forest"), #re-used sorcerer battle (swamp terrain)
("forest_mirkwood9"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001401917000004e93c00002d3e000077bd00004d24",[],[],"outer_terrain_forest"),    #re-used Dol Guldur outside

#placeholders
("forest_mirkwood_b5"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001490b56cb00058d66000023ad0000751200006218",[],[],"outer_terrain_forest"), #fir mix
("forest_mirkwood_b6"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001490b56cb00058d66000023ad0000751200006218",[],[],"outer_terrain_forest"), #fir mix
("forest_mirkwood_b7"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x000000014019056300058d66000037c60000416c0000385d",[],[],"outer_terrain_forest"), #swamp
("forest_mirkwood_b8"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001401917008004e93c000050338000345b00004d24",[],[],"outer_terrain_forest"), #re-used sorcerer battle variant (river)
("forest_mirkwood_b9"  ,sf_generate|sf_muddy_water,"none","none",(0,0),(100,100),-100,"0x00000001401917000004e93c00002d3e000077bd00004d24",[],[],"outer_terrain_forest"),    #re-used Dol Guldur outside


  ] + (is_a_wb_scene==1 and [
("gondor_battlefield_morgul" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x0000000120000500000691a40000065c00004b34000070b7",[],[],"outer_terrain_isen_low_far"),	#Gondor mountains battlefield by Morgul (WB only)
  ] or [
("gondor_battlefield_morgul" ,sf_generate|sf_randomize,"none", "none",(0,0),(100,100),-100,"0x0000000120000500000691a40000065c00004b34000070b7",[],[],"outer_terrain_isen_low_far"),
  ]) + [

("dagorlad_random"          ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),(240,240),-0.5,"0x000000025c600500000691a400003efe00004b34000059be",[],[],"outer_terrain_desert"),
("dagorlad_random_small" ,sf_generate|sf_randomize|sf_auto_entry_points,"none","none",(0,0),( 90, 90),-0.5,"0x000000015c60050000034cd300003efe00004b34000059be",[],[],"outer_terrain_desert"),

#swamps go from friendly (swamp_1) to evil (swamp_6)
("swamp_1"            ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000024c600500000691a400006ba200004b34000059be",[],[],"outer_terrain_flat"),
("swamp_2"            ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000002cc600563800691a400002787000068c2000054da",[],[],"outer_terrain_flat"),
("swamp_3"            ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000002cc600563800691a400005d4a000061f900006c8e",[],[],"outer_terrain_flat"),
("swamp_4"            ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000002cc600500000691a400001fb900004b34000059be",[],[],"outer_terrain_flat"),
("swamp_5"            ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000002cc600563800691a400005d4a000061f900006c8e",[],[],"outer_terrain_flat"),
("swamp_6"            ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000002cc600500000691a400001fb900004b34000059be",[],[],"outer_terrain_flat"),
("swamp_small"        ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000001cc60050000034cd300003efe00004b34000059be",[],[],"outer_terrain_flat"),
("swamp_7"            ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000002cc600563800691a400005d4a000061f900006c8e",[],[],"outer_terrain_flat"), #placeholder
("swamp_8"            ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000002cc600500000691a400001fb900004b34000059be",[],[],"outer_terrain_flat"), #placeholder
("swamp_9"            ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000002cc600563800691a400005d4a000061f900006c8e",[],[],"outer_terrain_flat"), #placeholder
("swamp_10"            ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000002cc600500000691a400001fb900004b34000059be",[],[],"outer_terrain_flat"), #placeholder

("forest_ithilien1" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000001388450d800058d6600006272000005a2000005ef",[],[],"New_outer_mountains2east_ithilien"), #plain big
("forest_ithilien2" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000001388458b600058d6600006272000005a200006f64",[],[],"New_outer_mountains2east_ithilien"), #plain med
("forest_ithilien3" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x00000001388454c500058d6600000fc7000005a20000635b",[],[],"New_outer_mountains2east_ithilien"), #plain small
("forest_ithilien4" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013885113680058d6600000fc700005acd0000635b",[],[],"New_outer_mountains2east_ithilien"), 	#steppe big
("forest_ithilien5" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013887184400058d6600000fa2000005a200007078",[],[],"New_outer_mountains2east_ithilien"),	#steppe med
("forest_ithilien6" ,sf_generate,"none","none",(0,0),(200,200),-0.5,"0x000000013887124480058d6600000fa280000ec300007078",[],[],"New_outer_mountains2east_ithilien"),	#steppe small

# Non-campaign scenes (these can savely be kept at the end of the file and moved with each extension, whereas campaign scenes are stored within savegame files, for whatever reason)
# Tutorial Scenes
("tutorial_1",sf_indoors,"tutorial_1_scene", "bo_tutorial_1_scene", (-100,-100),(100,100),-100,"0",
  [],[]),
("tutorial_2",sf_indoors,"tutorial_2_scene", "bo_tutorial_2_scene", (-100,-100),(100,100),-100,"0",
  [],[]),
("tutorial_3",sf_indoors,"tutorial_3_scene", "bo_tutorial_3_scene", (-100,-100),(100,100),-100,"0",
  [],[]),
("tutorial_4",sf_generate,"none", "none", (0,0),(120,120),-100,"0x30000500400360d80000189f00002a8380006d91",
  [],[], "outer_terrain_plain"),
("tutorial_5",sf_generate,"none", "none", (0,0),(120,120),-100,"0x3a06dca80005715c0000537400001377000011fe",
  [],[], "outer_terrain_plain"),

#Moria custom mission
("erebor_castle_2",sf_indoors ,"erebor_throne_room_b", "bo_erebor_throne_room_b", (-40,-40),(40,40),-100,"0",[],["player_chest"]), 

#Ghost custom mission
("random_scene_plain_forest_custom_5",sf_generate,"none", "none", (0,0),(240,240),-0.5,"0x00000000bc618a63000d234800004a3e00005cd6000045cc",
  [],[], "outer_terrain_forest"),
]

