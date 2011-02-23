from module_constants import *
from header_items import  *
from header_operations import *
from header_triggers import *
from header_factions import *


####################################################################################################################
### Each item record contains the following fields:
### 1) Item id: used for referencing items in other files.
###    The prefix itm_ is automatically added before each item id.
### 2) Item name. Name of item as it'll appear in inventory window
### 3) List of meshes.  Each mesh record is a tuple containing the following fields:
###   3.1) Mesh name.
###   3.2) Modifier bits that this mesh matches.
###    Note that the first mesh record is the default.
### 4) Item flags. See header_items.py for a list of available flags.
### 5) Item capabilities. Used for which animations this item is used with. See header_items.py for a list of available flags.
### 6) Item value.
### 7) Item stats: Bitwise-or of various stats about the item such as:
###     weight, abundance, difficulty, head_armor, body_armor,leg_armor, etc...
### 8) Modifier bits: Modifiers that can be applied to this item.
### 9) [Optional] Triggers: List of simple triggers to be associated with the item.
####################################################################################################################

###Some constants for ease of use.
imodbits_none = 0
imodbits_horse_basic = imodbit_swaybacked|imodbit_lame|imodbit_spirited|imodbit_heavy|imodbit_stubborn
imodbits_cloth  = 0 #imodbit_tattered | imodbit_ragged | imodbit_sturdy | imodbit_thick | imodbit_hardened
imodbits_armor  = 0 #imodbit_rusty | imodbit_battered | imodbit_crude | imodbit_thick | imodbit_reinforced |imodbit_lordly
imodbits_plate  = 0 #imodbit_cracked | imodbit_rusty | imodbit_battered | imodbit_crude | imodbit_thick | imodbit_reinforced |imodbit_lordly
imodbits_polearm = 0#imodbit_cracked | imodbit_bent | imodbit_balanced
imodbits_shield  = 0 #imodbit_cracked | imodbit_battered |imodbit_thick | imodbit_reinforced
imodbits_sword   = 0#imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_tempered
imodbits_sword_high   = 0#imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_tempered|imodbit_masterwork
imodbits_axe   = 0#imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_heavy
imodbits_mace   = 0#imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_heavy
imodbits_pick   = 0#imodbit_rusty | imodbit_chipped | imodbit_balanced | imodbit_heavy
imodbits_bow = 0#imodbit_cracked | imodbit_bent | imodbit_strong |imodbit_masterwork
imodbits_crossbow = 0#imodbit_cracked | imodbit_bent | imodbit_masterwork
imodbits_missile   = 0#imodbit_bent | imodbit_large_bag
imodbits_thrown   = 0#imodbit_bent | imodbit_heavy| imodbit_balanced| imodbit_large_bag

imodbits_horse_good = imodbit_spirited|imodbit_heavy
imodbits_good   = 0#imodbit_sturdy | imodbit_thick | imodbit_hardened | imodbit_reinforced
imodbits_bad    = 0#imodbit_rusty | imodbit_chipped | imodbit_tattered | imodbit_ragged | imodbit_cracked | imodbit_bent
###Replace winged mace/spiked mace with: Flanged mace / Knobbed mace?
###Fauchard (majowski glaive) 
items = [
###item_name, mesh_name, item_properties, item_capabilities, slot_no, cost, bonus_flags, weapon_flags, scale, view_dir, pos_offset
 ["no_item","INVALID ITEM", [("practice_sword",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary, itc_longsword, 3,weight(1.5)|spd_rtng(103)|weapon_length(90)|swing_damage(16,blunt)|thrust_damage(10,blunt),imodbits_none],
 ["horse_meat","Horse Meat", [("raw_meat",0)], itp_type_goods|itp_consumable|itp_food, 0, 12,weight(40)|food_quality(30)|max_ammo(40),imodbits_none],
###Items before this point are hardwired and their order should not be changed!
 ["practice_sword","Practice Sword", [("practice_sword",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_wooden_parry|itp_wooden_attack, itc_longsword, 3,weight(1.5)|spd_rtng(103)|weapon_length(90)|swing_damage(16,blunt)|thrust_damage(10,blunt),imodbits_none],
 ["heavy_practice_sword","Heavy Practice Sword", [("heavy_practicesword",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_greatsword,
    21, weight(6.25)|spd_rtng(94)|weapon_length(128)|swing_damage(26,blunt)|thrust_damage(18,blunt),imodbits_none],
# ["practice_axe", "Practice Axe", [("hatchet",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 24 , weight(2) | spd_rtng(95) | weapon_length(75) | swing_damage(20, blunt) | thrust_damage(0, pierce), imodbits_axe],
 ["arena_axe", "Axe", [("arena_axe",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
 137 , weight(1.5)|spd_rtng(100) | weapon_length(69)|swing_damage(23 , blunt) | thrust_damage(0 ,  pierce),imodbits_axe ],
 ["arena_sword", "Sword", [("arena_sword_one_handed",0),("sword_medieval_b_scabbard", ixmesh_carry),], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 243 , weight(1.5)|spd_rtng(99) | weapon_length(95)|swing_damage(21 , blunt) | thrust_damage(20 ,  blunt),imodbits_sword_high ],
 ["arena_sword_two_handed",  "Two Handed Sword", [("arena_sword_two_handed",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back,
 670 , weight(2.75)|spd_rtng(93) | weapon_length(110)|swing_damage(29 , blunt) | thrust_damage(24 ,  blunt),imodbits_sword_high ],
 ["arena_lance",         "Lance", [("arena_lance",0)], itp_type_polearm|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear,
 90 , weight(2.5)|spd_rtng(96) | weapon_length(150)|swing_damage(20 , blunt) | thrust_damage(25 ,  blunt),imodbits_polearm ],
 ["practice_staff","Practice Staff", [("wooden_staff",0)],itp_type_polearm|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack,itc_staff|itcf_carry_sword_back,9, weight(2.5)|spd_rtng(103) | weapon_length(118)|swing_damage(16,blunt) | thrust_damage(16,blunt),imodbits_none],
# ["practice_lance","Practice Lance", [("joust_of_peace",0)], itp_type_polearm|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack, itc_greatlance, 18,weight(4.25)|spd_rtng(58)|weapon_length(218)|swing_damage(0,blunt)|thrust_damage(15,blunt),imodbits_none],
# ["practice_shield","Practice Shield", [("shield_round_a",0)], itp_type_shield|itp_wooden_parry|itp_wooden_attack, 0, 20,weight(3.5)|body_armor(1)|hit_points(200)|spd_rtng(100)|weapon_length(50),imodbits_none],
 ["practice_bow","Practice Bow", [("hunting_bow",0), ("hunting_bow_carry",ixmesh_carry)], itp_type_bow |itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bow_back, 0, weight(1.5)|spd_rtng(90) | shoot_speed(40) | thrust_damage(19, blunt),imodbits_bow ],
####                                                    ("hunting_bow",0)],                  itp_type_bow|itp_two_handed|itp_primary|itp_attach_left_hand, itcf_shoot_bow, 4,weight(1.5)|spd_rtng(90)|shoot_speed(40)|thrust_damage(19,blunt),imodbits_none],

###A treatise on The Method of Mechanical Theorems Archimedes
 
#This book must be at the beginning of readable books
# ["book_tactics","De Re Militari", [("book_a",0)], itp_type_book, 0, 4000,weight(2)|abundance(100),imodbits_none],
# ["book_persuasion","Rhetorica ad Herennium", [("book_b",0)], itp_type_book, 0, 5000,weight(2)|abundance(100),imodbits_none],
# ["book_leadership","The Life of Alixenus the Great", [("book_d",0)], itp_type_book, 0, 4200,weight(2)|abundance(100),imodbits_none],
# ["book_intelligence","Essays on Logic", [("book_e",0)], itp_type_book, 0, 2900,weight(2)|abundance(100),imodbits_none],
# ["book_trade","A Treatise on the Value of Things", [("book_f",0)], itp_type_book, 0, 3100,weight(2)|abundance(100),imodbits_none],
# ["book_weapon_mastery", "On the Art of Fighting with Swords", [("book_d",0)], itp_type_book, 0, 4200,weight(2)|abundance(100),imodbits_none],
# ["book_engineering","Method of Mechanical Theorems", [("book_open",0)], itp_type_book, 0, 4000,weight(2)|abundance(100),imodbits_none],

#Reference books
#This book must be at the beginning of reference books
# ["book_wound_treatment_reference","The Book of Healing", [("book_c",0)], itp_type_book, 0, 3500,weight(2)|abundance(100),imodbits_none],
# ["book_training_reference","Manual of Arms", [("book_open",0)], itp_type_book, 0, 3500,weight(2)|abundance(100),imodbits_none],
# ["book_surgery_reference","The Great Book of Surgery", [("book_c",0)], itp_type_book, 0, 3500,weight(2)|abundance(100),imodbits_none],

###["dry_bread", "wheat_sack", itp_type_goods|itp_consumable, 0, slt_none,view_goods,95,weight(2),max_ammo(50),imodbits_none],
#foods (first one is smoked_fish)
 ["human_meat","Human Meat", [("raw_meat",0)], itp_type_goods|itp_consumable|itp_food, 0, 103,weight(20)|abundance(100)|food_quality(80)|max_ammo(70),imodbits_none],
 ["lembas","Lembas", [("lembas",0)], itp_type_goods|itp_consumable|itp_food, 0, 200,weight(1.3)|food_quality(70)|max_ammo(70),imodbits_none],
 ["smoked_fish","Smoked Fish", [("smoked_fish",0)], itp_shop|itp_type_goods|itp_consumable|itp_food, 0, 59,weight(15)|abundance(110)|food_quality(50)|max_ammo(50),imodbits_none],
 ["dried_meat","Dried Meat", [("smoked_meat",0)], itp_shop|itp_type_goods|itp_consumable|itp_food, 0, 72,weight(15)|abundance(100)|food_quality(70)|max_ammo(50),imodbits_none],
 ["cattle_meat","Beef", [("raw_meat",0)], itp_shop|itp_type_goods|itp_consumable|itp_food, 0, 103,weight(20)|abundance(100)|food_quality(80)|max_ammo(70),imodbits_none],


# ["pork","Pork", [("fried_pig",0)], itp_shop|itp_type_goods|itp_consumable|itp_food, 0, 85,weight(15)|abundance(100)|food_quality(70)|max_ammo(50),imodbits_none],
# ["bread","Bread", [("bread_a",0)], itp_shop|itp_type_goods|itp_consumable|itp_food, 0, 32,weight(20)|abundance(110)|food_quality(40)|max_ammo(50),imodbits_none],
# ["apples","Apples", [("apple_basket",0)], itp_shop|itp_type_goods|itp_consumable|itp_food, 0, 44,weight(20)|abundance(110)|food_quality(40)|max_ammo(50),imodbits_none],
# ["cheese","Cheese", [("cheese_b",0)], itp_shop|itp_type_goods|itp_consumable|itp_food, 0, 95,weight(6)|abundance(110)|food_quality(40)|max_ammo(30),imodbits_none],
# ["chicken","Chicken", [("chicken_roasted",0)], itp_shop|itp_type_goods|itp_consumable|itp_food, 0, 75,weight(10)|abundance(110)|food_quality(40)|max_ammo(50),imodbits_none],
# ["honey","Honey", [("honey_pot",0)], itp_shop|itp_type_goods|itp_consumable|itp_food, 0, 136,weight(5)|abundance(110)|food_quality(40)|max_ammo(30),imodbits_none],
# ["sausages","Sausages", [("sausages",0)], itp_shop|itp_type_goods|itp_consumable|itp_food, 0, 60,weight(10)|abundance(110)|food_quality(40)|max_ammo(40),imodbits_none],
# ["cabbages","Cabbages", [("cabbage",0)], itp_shop|itp_type_goods|itp_consumable|itp_food, 0, 30,weight(15)|abundance(110)|food_quality(40)|max_ammo(50),imodbits_none],
# ["butter","Butter", [("butter_pot",0)], itp_shop|itp_type_goods|itp_consumable|itp_food, 0, 150,weight(6)|abundance(110)|food_quality(40)|max_ammo(30),imodbits_none],

#other trade goods (first one is wine)
# ["wine","Wine", [("amphora_slim",0)], itp_shop|itp_type_goods|itp_consumable, 0, 141,weight(30)|abundance(60)|max_ammo(50),imodbits_none],
# ["ale","Ale", [("ale_barrel",0)], itp_shop|itp_type_goods|itp_consumable, 0, 84,weight(30)|abundance(70)|max_ammo(50),imodbits_none],
# ["spice","Spice", [("spice_sack",0)], itp_shop|itp_type_goods, 0, 880,weight(40)|abundance(25),imodbits_none],
# ["salt","Salt", [("salt_sack",0)], itp_shop|itp_type_goods, 0, 255,weight(50)|abundance(120),imodbits_none],
 ["grain","Wheat", [("wheat_sack",0)], itp_shop|itp_type_goods|itp_consumable, 0, 77,weight(50)|abundance(110)|food_quality(40)|max_ammo(50),imodbits_none],
# ["flour","Flour", [("salt_sack",0)], itp_shop|itp_type_goods|itp_consumable, 0, 91,weight(50)|abundance(100)|food_quality(45)|max_ammo(50),imodbits_none],
# ["iron","Iron", [("iron",0)], itp_shop|itp_type_goods, 0,264,weight(60)|abundance(60),imodbits_none],
# ["oil","Oil", [("oil",0)], itp_shop|itp_type_goods, 0, 484,weight(50)|abundance(60),imodbits_none],
# ["pottery","Pottery", [("jug",0)], itp_shop|itp_type_goods, 0, 126,weight(50)|abundance(90),imodbits_none],
# ["linen","Linen", [("linen",0)], itp_shop|itp_type_goods, 0, 250,weight(40)|abundance(90),imodbits_none],
# ["furs","Furs", [("fur_pack",0)], itp_shop|itp_type_goods, 0, 391,weight(40)|abundance(90),imodbits_none],
# ["wool","Wool", [("wool_sack",0)], itp_shop|itp_type_goods, 0, 130,weight(40)|abundance(90),imodbits_none],
# ["velvet","Velvet", [("velvet",0)], itp_shop|itp_type_goods, 0, 1025,weight(40)|abundance(30),imodbits_none],
 ["tools","Tools", [("iron_hammer",0)], itp_shop|itp_type_goods, 0, 410,weight(50)|abundance(90),imodbits_none],


#************************************************************************************************
###ITEMS before this point are hardcoded into item_codes.h and their order should not be changed!
#************************************************************************************************

###Quest Items

 ["siege_supply","Supplies", [("ale_barrel",0)], itp_type_goods, 0, 96,weight(40)|abundance(70),imodbits_none],
 ["quest_wine","Wine", [("amphora_slim",0)], itp_type_goods, 0, 46,weight(40)|abundance(60)|max_ammo(50),imodbits_none],
 ["quest_ale","Ale", [("ale_barrel",0)], itp_type_goods, 0, 31,weight(40)|abundance(70)|max_ammo(50),imodbits_none],

# magin items begin
 ["ent_water","Strange_bowl_of_water", [("ent_water",0)], itp_type_goods, 0, 0,weight(15)|abundance(0),imodbits_none],
 ["map","Maps of Middle Earth", [("middle_earth_map",0)], itp_type_goods, 0, 5000,weight(0.2)|abundance(0),imodbits_none],
 ["orc_brew","Orc_Brew", [("orc_brew",0)], itp_type_goods|itp_consumable, 0, 1000,weight(0.2)|abundance(0)|max_ammo(100),imodbits_none],
 ["rohan_saddle","Saddle of Rohan", [("RohanSaddle",0)], itp_type_goods, 0, 5000,weight(4)|abundance(0),imodbits_none],
# magin items end: l
 
 ["metal_scraps_bad","Low grade metal scraps", [("weapon_scraps_a",0)], itp_type_goods, 0, 10,weight(40)|abundance(0),imodbits_none],
 ["metal_scraps_medium","Usable metal scraps", [("weapon_scraps_b",0)], itp_type_goods, 0, 50,weight(40)|abundance(0),imodbits_none],
 ["metal_scraps_good","Good quality metal scraps", [("weapon_scraps_b",0)], itp_type_goods, 0, 250,weight(40)|abundance(0),imodbits_none],

###Horses: sumpter horse/ pack horse, saddle horse, steppe horse, warm blood, geldling, stallion,   war mount, charger, 
###Carthorse, hunter, heavy hunter, hackney, palfrey, courser, destrier.
 ["sumpter_horse","Sumpter Horse", [("sumpter_horse",0)], itp_shop|itp_type_horse, 0, 64,abundance(90)|hit_points(110)|body_armor(17)|difficulty(1)|horse_speed(34)|horse_maneuver(33)|horse_charge(9),imodbits_horse_basic],
 ["saddle_horse","Saddle Horse", [("saddle_horse",0),("horse_c",imodbits_horse_good)], itp_shop|itp_type_horse, 0, 112,abundance(90)|body_armor(14)|difficulty(1)|horse_speed(39)|horse_maneuver(36)|horse_charge(8),imodbits_horse_basic],
 ["steppe_horse","Steppe Horse", [("steppe_horse",0)], itp_shop|itp_type_horse, 0, 92,abundance(80)|body_armor(15)|difficulty(2)|horse_speed(37)|horse_maneuver(41)|horse_charge(7),imodbits_horse_basic],
 ["courser","Courser", [("courser",0)], itp_shop|itp_type_horse, 0, 323,abundance(70)|body_armor(16)|difficulty(2)|horse_speed(43)|horse_maneuver(37)|horse_charge(11),imodbits_horse_basic|imodbit_champion],
 ["hunter","Hunter", [("hunting_horse",0),("hunting_horse",imodbits_horse_good)], itp_shop|itp_type_horse, 0, 434,abundance(60)|hit_points(130)|body_armor(29)|difficulty(3)|horse_speed(40)|horse_maneuver(36)|horse_charge(18),imodbits_horse_basic|imodbit_champion],

 
#whalebone crossbow, yew bow, war bow, arming sword 
 ["arrows","Arrows", [("plain_arrow",0),("flying_missile",ixmesh_flying_ammo),("common_quiver", ixmesh_carry)], itp_type_arrows|itp_shop, itcf_carry_quiver_front_right , 72,weight(3)|abundance(160)|weapon_length(95)|thrust_damage(1,bow_damage)|max_ammo(30),imodbits_missile],
 ["gondor_arrows","Gondorian Arrows", [("gondor_arrow",0),("flying_missile",ixmesh_flying_ammo),("gondor_quiver", ixmesh_carry)], itp_type_arrows|itp_shop, itcf_carry_quiver_front_right , 72,weight(3)|abundance(160)|weapon_length(95)|thrust_damage(1,bow_damage)|max_ammo(30),imodbits_missile],
 ["gondor_auxila_arrows","Gondorian Arrows", [("gondor_arrow",0),("flying_missile",ixmesh_flying_ammo),("gondor_quiver", ixmesh_carry)], itp_type_arrows|itp_shop, itcf_carry_quiver_front_right , 72,weight(3)|abundance(160)|weapon_length(95)|thrust_damage(1,bow_damage)|max_ammo(30),imodbits_missile],
 ["barbed_arrows","Barbed Arrows", [("barbed_arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver_d", ixmesh_carry)], itp_type_arrows|itp_shop, itcf_carry_quiver_front_right , 124,weight(3)|abundance(70)|weapon_length(95)|thrust_damage(2,bow_damage)|max_ammo(30),imodbits_missile],

 ["khergit_arrows","Rohirrim Arrows", [("rohan_arrow2",0),("flying_missile",ixmesh_flying_ammo),("rohan_quiver", ixmesh_carry)], itp_type_arrows|itp_shop, itcf_carry_quiver_front_right , 410,weight(3.5)|abundance(30)|weapon_length(95)|thrust_damage(3,bow_damage)|max_ammo(30),imodbits_missile],
 ["rohan_arrows_2","Rohirrim Arrows", [("rohan_arrow1",0),("flying_missile",ixmesh_flying_ammo),("rohan_quiver2", ixmesh_carry)], itp_type_arrows|itp_shop, itcf_carry_quiver_front_right , 410,weight(3.5)|abundance(30)|weapon_length(95)|thrust_damage(3,bow_damage)|max_ammo(30),imodbits_missile],

 ["harad_arrows","Haradrim Arrows", [("harad_arrow",0),("flying_missile",ixmesh_flying_ammo),("harad_quiver", ixmesh_carry)], itp_type_arrows|itp_shop, itcf_carry_quiver_front_right , 124,weight(3)|abundance(70)|weapon_length(95)|thrust_damage(2,bow_damage)|max_ammo(30),imodbits_missile],
 ["corsair_arrows","Corsair Arrows", [("corsair_arrow",0),("flying_missile",ixmesh_flying_ammo),("corsair_quiver", ixmesh_carry)], itp_type_arrows|itp_shop, itcf_carry_quiver_front_right , 350,weight(3)|abundance(50)|weapon_length(91)|thrust_damage(3,bow_damage)|max_ammo(29),imodbits_missile],
 
 ["ithilien_arrows","Ithilien Arrows", [("ilithien_arrow",0),("flying_missile",ixmesh_flying_ammo),("ithilien_quiver", ixmesh_carry)], itp_type_arrows|itp_shop, itcf_carry_quiver_front_right , 350,weight(3)|abundance(50)|weapon_length(91)|thrust_damage(3,bow_damage)|max_ammo(29),imodbits_missile],
 #["corsair_bolts","Corsair Bolts", [("bolt",0),("flying_missile",ixmesh_flying_ammo),("bolt_bag_b", ixmesh_carry),("bolt_bag_b", ixmesh_carry|imodbit_large_bag)], itp_type_bolts|itp_shop, itcf_carry_quiver_right_vertical, 64,weight(2.25)|abundance(90)|weapon_length(55)|thrust_damage(1,bow_damage)|max_ammo(25),imodbits_missile],

 #["bolts","Bolts", [("bolt",0),("flying_missile",ixmesh_flying_ammo),("bolt_bag", ixmesh_carry),("bolt_bag_b", ixmesh_carry|imodbit_large_bag)], itp_type_bolts|itp_shop, itcf_carry_quiver_right_vertical, 64,weight(2.25)|abundance(90)|weapon_length(55)|thrust_damage(1,bow_damage)|max_ammo(25),imodbits_missile],
 #["steel_bolts","Steel Bolts", [("bolt",0),("flying_missile",ixmesh_flying_ammo),("bolt_bag_c", ixmesh_carry)], itp_type_bolts|itp_shop, itcf_carry_quiver_right_vertical, 210,weight(2.5)|abundance(20)|weapon_length(55)|thrust_damage(2,bow_damage)|max_ammo(25),imodbits_missile],
 # ["cartridges","Cartridges", [("cartridge_a",0)], itp_type_bullets|itp_shop, 0, 41,weight(2.25)|abundance(90)|weapon_length(3)|thrust_damage(1,bow_damage)|max_ammo(40),imodbits_missile],

["pilgrim_disguise", "Pilgrim Disguise", [("tld_robe_generic_dress",0)], 0|itp_type_body_armor |itp_covers_legs |itp_civilian ,0, 25 , weight(2)|abundance(100)|head_armor(0)|body_armor(19)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["pilgrim_hood", "Pilgrim Hood", [("pilgrim_hood",0)], 0|itp_type_head_armor |itp_civilian  ,0, 35 , weight(1.25)|abundance(100)|head_armor(14)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],

###ARMOR
#handwear
["leather_gloves","Leather Gloves", [("lthr_glove_L",0)], itp_shop|itp_type_hand_armor,0, 130, weight(0.25)|abundance(120)|body_armor(2)|difficulty(0),imodbits_cloth],
["mail_mittens","Mail Mittens", [("mail_mitten_L",0)], itp_shop|itp_type_hand_armor,0, 550, weight(0.5)|abundance(100)|body_armor(4)|difficulty(0),imodbits_armor],
#["scale_gauntlets","Scale Gauntlets", [("scale_gaunt_L",0)], itp_shop|itp_type_hand_armor,0, 910, weight(0.75)|abundance(100)|body_armor(5)|difficulty(0),imodbits_armor],
#["gauntlets","Gauntlets", [("gauntlet_a_L",0),("gauntlet_b_L",imodbit_reinforced)], itp_shop|itp_type_hand_armor,0, 1940, weight(1.0)|abundance(100)|body_armor(6)|difficulty(0),imodbits_armor],

#footwear
#["wrapping_boots", "Wrapping Boots", [("shoe_fur",0)], itp_shop|itp_type_foot_armor |itp_civilian |itp_attach_armature ,0,
# 3 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(3)|difficulty(0) ,imodbits_cloth ],
["woolen_hose", "Woolen Hose", [("woolen_hose",0)], itp_shop|itp_type_foot_armor |itp_civilian |itp_attach_armature ,0,
 6 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(4)|difficulty(0) ,imodbits_cloth ],
#["blue_hose", "Blue Hose", [("blue_leggings",0)], itp_shop|itp_type_foot_armor |itp_civilian |itp_attach_armature ,0,
# 11 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
#["hunter_boots", "Hunter Boots", [("boot_hunter",0)], itp_shop|itp_type_foot_armor |itp_civilian |itp_attach_armature,0,
# 19 , weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(9)|difficulty(0) ,imodbits_cloth ],
#["hide_boots", "Hide Boots", [("boot_nomad_a",0)], itp_shop|itp_type_foot_armor |itp_civilian  |itp_attach_armature,0,
# 34 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
#["ankle_boots", "Ankle Boots", [("ankle_boots_a",0)], itp_shop|itp_type_foot_armor |itp_civilian  |itp_attach_armature,0,
# 75 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(12)|difficulty(0) ,imodbits_cloth ],
#["nomad_boots", "Nomad Boots", [("boot_nomad_b",0)], itp_shop|itp_type_foot_armor  |itp_civilian |itp_attach_armature,0,
# 116 , weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(14)|difficulty(0) ,imodbits_cloth ],
["leather_boots", "Leather Boots", [("boots",0)], itp_shop|itp_type_foot_armor  |itp_civilian |itp_attach_armature,0,
 174 , weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(16)|difficulty(0) ,imodbits_cloth ],
["mail_chausses", "Mail Chausses", [("chausses_cm",0)], itp_shop|itp_type_foot_armor |itp_attach_armature  ,0,
 410 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(21)|difficulty(0) ,imodbits_armor ],
#["splinted_leather_greaves", "Splinted Leather Greaves", [("lthr_greaves",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0,
# 760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],
["splinted_greaves", "Splinted Greaves", [("spl_greaves",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0,
 1153 , weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(28)|difficulty(7) ,imodbits_armor ],
["mail_boots", "Mail Boots", [("shoe_cm",0)], itp_shop|itp_type_foot_armor |itp_attach_armature  ,0,
 1746 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(8) ,imodbits_armor ],
["iron_greaves", "Iron Greaves", [("iron_greaves",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0,
 2374 , weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(33)|difficulty(9) ,imodbits_armor ],
#["black_greaves", "Black Greaves", [("black_greaves",0)], itp_type_foot_armor  |itp_attach_armature,0,
# 3561 , weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(35)|difficulty(0) ,imodbits_armor ],

#bodywear
#["lady_dress_ruby", "Lady Dress", [("lady_dress_r",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth],
#["lady_dress_green", "Lady Dress", [("lady_dress_g",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth],
#["lady_dress_blue", "Lady Dress", [("lady_dress_b",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth],

# TLD civilian wear
["black_dress"   , "Black Dress" , [("gondor_dress_a" ,0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth],
["blackwhite_dress","Lady Dress" , [("gondor_dress_b" ,0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth],
["white_tunic_a" , "White Tunic" , [("generic_tunic_a",0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 47 , weight(2)|abundance(100)|head_armor(0)|body_armor(11)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["white_tunic_b" , "Simple Tunic", [("gondor_tunic_b" ,0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 47 , weight(2)|abundance(100)|head_armor(0)|body_armor(11)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["white_tunic_c" , "Tunic Jacket", [("generic_tunic_c",0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 47 , weight(2)|abundance(100)|head_armor(0)|body_armor(11)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["blue_tunic"    , "Blue Tunic"  , [("dale_tunic"     ,0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 47 , weight(2)|abundance(100)|head_armor(0)|body_armor(11)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["black_tunic"   , "Black Tunic" , [("gondor_tunic"   ,0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 47 , weight(2)|abundance(100)|head_armor(0)|body_armor(11)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["green_tunic"   , "Green Tunic" , [("rohan_tunic"    ,0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 47 , weight(2)|abundance(100)|head_armor(0)|body_armor(11)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["red_tunic"     , "Red Tunic"   , [("woodman_tunic"  ,0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 47 , weight(2)|abundance(100)|head_armor(0)|body_armor(11)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["leather_apron" ,"Leather Apron", [("smith_leather_apron",0)], itp_type_body_armor|itp_civilian|itp_covers_legs ,0,61 , weight(3)|abundance(100)|head_armor(0)|body_armor(12)|leg_armor(7)|difficulty(0) ,imodbits_cloth ],
["leather_jerkin","Leather_Jerkin",[("generic_leather_jerkin",0)], itp_shop|itp_type_body_armor|itp_civilian|itp_covers_legs ,0,321 , weight(6)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["fur_coat"      , "Dale Coat"   , [("dale_coat"      ,0)], itp_shop|itp_type_body_armor  |itp_covers_legs |itp_civilian,0, 117 , weight(6)|abundance(100)|head_armor(0)|body_armor(13)|leg_armor(6)|difficulty(0) ,imodbits_armor ],
["green_dress"   , "Green Dress" , [("rohan_dress"    ,0)], itp_shop|itp_type_body_armor  |itp_covers_legs |itp_civilian,0, 500 , weight(6)|abundance(100)|head_armor(0)|body_armor(13)|leg_armor(6)|difficulty(0) ,imodbits_armor ],
["rich_outfit"   , "Rich Outfit" , [("merchant_outf"  ,0)], itp_type_body_armor|itp_covers_legs|itp_civilian   ,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(4)|difficulty(0) ,imodbits_cloth ],
["tld_tunic"     , "Tunic"       , [("tld_tunic",      0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 47 , weight(2)|abundance(100)|head_armor(0)|body_armor(11)|leg_armor(6)|difficulty(0) ,imodbits_cloth,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_initialize_civilian_clothes", "tableau_tld_tunic", ":agent_no", ":troop_no")])]],
#combos
["gondor_fine_outfit_dress"    , "Fine Outfit", [("gondor_fine_outfit_dress"    ,0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth],
["rohan_fine_outfit_dale_dress", "Fine Outfit", [("rohan_fine_outfit_dale_dress",0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth],
["robe_generic_dress"          , "Robe"       , [("tld_robe_generic_dress"      ,0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth],
#civ headgear
["court_hat", "Turret Hat", [("court_hat",0)], itp_type_head_armor  |itp_civilian|itp_fit_to_head ,0, 80 , weight(0.5)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ], 
["wimple_a", "Wimple", [("gondor_wimple_a",0)],itp_shop|itp_type_head_armor|itp_civilian|itp_fit_to_head,0,10, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],
["wimple_with_veil", "Wimple", [("gondor_wimple_b",0)],itp_shop|itp_type_head_armor|itp_civilian|itp_fit_to_head,0,10, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],
["fine_hat", "Fine Hat", [("gondor_fine_fem_hat",0)],itp_shop|itp_type_head_armor|itp_civilian|itp_fit_to_head,0,10, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],
#MV commented out duplicate ["fine_hat", "Fine Hat", [("gondor_fine_fem_hat",0)],itp_shop|itp_type_head_armor|itp_civilian|itp_fit_to_head,0,10, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],

["courtly_outfit", "Courtly Outfit", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian   ,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["nobleman_outfit", "Nobleman Outfit", [("nobleman_outfit_b",0)], itp_type_body_armor|itp_covers_legs|itp_civilian   ,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(12)|difficulty(0) ,imodbits_cloth ], 
#["fur_coat", "Dale Coat", [("dale_coat",0)], itp_shop|itp_type_body_armor  |itp_covers_legs |itp_civilian,0, 117 , weight(6)|abundance(100)|head_armor(0)|body_armor(13)|leg_armor(6)|difficulty(0) ,imodbits_armor ],
#["leather_jerkin", "Leather Jerkin", [("woodsman_jerkin",0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 50 , weight(3)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#["nomad_armor", "Nomad Armor", [("armor_nomad",0)], itp_shop|itp_type_body_armor   ,0, 25 , weight(2)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#["khergit_armor", "Khergit Armor", [("armor_nomad_b",0)], itp_shop|itp_type_body_armor ,0, 38 , weight(2)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#["rawhide_coat", "Rawhide Coat", [("tunic_fur",0)], itp_shop|itp_type_body_armor |itp_civilian |itp_covers_legs ,0, 12 , weight(5)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#["leather_armor", "Leather Armor", [("lthr_armor_a",0)], itp_shop|itp_type_body_armor |itp_covers_legs  ,0, 65 , weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],

#for future:
# ["coat", "Coat", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["leather_coat", "Leather Coat", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["mail_coat", "Coat of Mail", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["long_mail_coat", "Long Coat of Mail", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["sleeveless_mail_coat", "Sleeveless Coat of Mail", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["sleeveless_coat", "Sleeveless Coat", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["hide_coat", "Hide Coat", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["merchant_outfit", "Merchant Outfit", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["homespun_dress", "Homespun Dress", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["thick_coat", "Thick Coat", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["coat_with_cape", "Coat_with_Cape", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["steppe_outfit", "Steppe Outfit", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["nordic_outfit", "Nordic Outfit", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["nordic_armor", "Nordic Armor", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["hide_armor", "Hide Armor", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["cloaked_tunic", "Cloaked Tunic", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["sleeveless_tunic", "Sleeveless Tunic", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["sleeveless_leather_tunic", "Sleeveless Leather Tunic", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
#["linen_shirt", "Linen_Shirt", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
# ["wool_coat", "Wool_Coat", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
#end

#["dress", "Dress", [("dress",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 6 , weight(1)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(2)|difficulty(0) ,imodbits_cloth ],
["blue_dress", "Blue Dress", [("blue_dress",0)], itp_shop|itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 6 , weight(1)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(2)|difficulty(0) ,imodbits_cloth ],
["peasant_dress", "Peasant Dress", [("peasant_dress_b",0)], itp_shop|itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 6 , weight(1)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(2)|difficulty(0) ,imodbits_cloth ], 
#["woolen_dress", "Woolen Dress", [("woolen_dress",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 10 , weight(1.75)|abundance(100)|head_armor(0)|body_armor(8)|leg_armor(2)|difficulty(0) ,imodbits_cloth ],
#["shirt", "Shirt", [("shirt",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 3 , weight(1)|abundance(100)|head_armor(0)|body_armor(5)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["linen_tunic", "Linen Tunic", [("linen_tunic",0)], itp_type_body_armor |itp_civilian |itp_covers_legs ,0,6 , weight(1)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(1)|difficulty(0) ,imodbits_cloth ],
["short_tunic", "Rich Tunic", [("cvl_costume_a",0)], itp_type_body_armor |itp_civilian |itp_covers_legs ,0,10 , weight(1)|abundance(100)|head_armor(0)|body_armor(7)|leg_armor(1)|difficulty(0) ,imodbits_cloth ],
["robe", "Robe", [("robe",0)], itp_shop|itp_type_body_armor  |itp_covers_legs |itp_civilian,0, 31 , weight(1.5)|abundance(100)|head_armor(0)|body_armor(8)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
#["generic_tunic_a", "Simple Tunic", [("generic_tunic_a",0)], itp_type_body_armor  |itp_covers_legs ,0, 47 , weight(2)|abundance(100)|head_armor(0)|body_armor(11)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
#["leather_apron", "Leather Apron", [("smith_leather_apron",0)], itp_type_body_armor |itp_civilian |itp_covers_legs ,0,61 , weight(3)|abundance(100)|head_armor(0)|body_armor(12)|leg_armor(7)|difficulty(0) ,imodbits_cloth ],
#["tabard", "Tabard", [("tabard_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 107 , weight(3)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
#["leather_vest", "Leather Vest", [("leather_vest",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 146 , weight(4)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(7)|difficulty(0) ,imodbits_cloth ],
#["steppe_armor", "Steppe Armor", [("lamellar_leather",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 195 , weight(5)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["gambeson", "Gambeson", [("white_gambeson",0)], itp_shop|itp_type_body_armor|itp_covers_legs|itp_civilian,0, 260 , weight(5)|abundance(100)|head_armor(0)|body_armor(20)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
#["blue_gambeson", "Blue Gambeson", [("blue_gambeson",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0, 270 , weight(5)|abundance(100)|head_armor(0)|body_armor(21)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
#["red_gambeson", "Red Gambeson", [("red_gambeson",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0, 275 , weight(5)|abundance(100)|head_armor(0)|body_armor(21)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
#["padded_cloth", "Padded Cloth", [("aketon_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 297 , weight(11)|abundance(100)|head_armor(0)|body_armor(22)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
#["leather_jerkin", "Woodsman_Jerkin", [("woodsman_jerkin",0)], itp_shop|itp_type_body_armor |itp_civilian |itp_covers_legs ,0,321 , weight(6)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
#["nomad_vest", "Nomad Vest", [("nomad_vest_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 360 , weight(7)|abundance(50)|head_armor(0)|body_armor(22)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
#["ragged_outfit", "Ragged Outfit", [("ragged_outfit_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 390 , weight(7)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(9)|difficulty(0) ,imodbits_cloth ],
#["padded_leather", "Padded Leather", [("padded_leather",0)], itp_shop|itp_type_body_armor  |itp_covers_legs,0, 454 , weight(12)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
#["tribal_warrior_outfit", "Tribal Warrior Outfit", [("tribal_warrior_outfit_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 520 , weight(14)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
#["nomad_robe", "Nomad Robe", [("nomad_robe_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 610 , weight(15)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
#["heraldric_armor", "Heraldric Armor", [("tourn_armor_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 442 , weight(17)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(8)|difficulty(7) ,imodbits_armor ],
#["studded_leather_coat", "Studded Leather Coat", [("std_lthr_coat",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 690 , weight(14)|abundance(100)|head_armor(0)|body_armor(34)|leg_armor(10)|difficulty(7) ,imodbits_armor ],

#["byrnie", "Byrnie", [("byrnie_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 795 , weight(17)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(6)|difficulty(7) ,imodbits_armor ],
#["blackwhite_surcoat", "Black and White Surcoat", [("surcoat_blackwhite",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 348 , weight(16)|abundance(100)|head_armor(0)|body_armor(33)|leg_armor(8)|difficulty(7) ,imodbits_armor ],
#["green_surcoat", "Green Surcoat", [("surcoat_green",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 348 , weight(16)|abundance(100)|head_armor(0)|body_armor(33)|leg_armor(8)|difficulty(7) ,imodbits_armor ],
#["blue_surcoat", "Blue Surcoat", [("surcoat_blue",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 350 , weight(16)|abundance(100)|head_armor(0)|body_armor(33)|leg_armor(8)|difficulty(7) ,imodbits_armor ],
#["red_surcoat", "Red Surcoat", [("surcoat_red",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 350 , weight(16)|abundance(100)|head_armor(0)|body_armor(33)|leg_armor(8)|difficulty(7) ,imodbits_armor ],
#["haubergeon", "Haubergeon", [("haubergeon_a",0),("haubergeon_b",imodbits_good)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 863 , weight(18)|abundance(100)|head_armor(0)|body_armor(41)|leg_armor(6)|difficulty(6) ,imodbits_armor ],
#["mail_shirt", "Mail Shirt", [("mail_shirt",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0,920 , weight(19)|abundance(100)|head_armor(0)|body_armor(37)|leg_armor(12)|difficulty(7) ,imodbits_armor ],
["mail_hauberk", "Mail Hauberk", [("hauberk_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0,1190 , weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7) ,imodbits_armor ],
#["lamellar_vest", "Lamellar Vest", [("nmd_warrior_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 1370 , weight(18)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(8)|difficulty(7) ,imodbits_cloth ],

["headcloth", "Headcloth", [("headcloth",0)], itp_shop|itp_type_head_armor  |itp_civilian ,0, 1 , weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["female_hood", "Lady's Hood", [("woolen_hood",0)], itp_type_head_armor |itp_civilian  ,0, 9 , weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#["skullcap", "Skullcap", [("skull_cap_new_a",0)], itp_shop|itp_type_head_armor   ,0, 60 , weight(1.0)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
 
#WEAPONS
["wooden_stick","Wooden Stick", [("wooden_stick",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_attack|itp_no_parry, itc_scimitar, 4 , weight(2.5)|difficulty(0)|spd_rtng(99) | weapon_length(90)|swing_damage(13 , blunt) | thrust_damage(0 ,  pierce),imodbits_none ],
#["cudgel",         "Cudgel", [("club",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 4 , weight(2.5)|difficulty(0)|spd_rtng(99) | weapon_length(90)|swing_damage(13 , blunt) | thrust_damage(0 ,  pierce),imodbits_none ],
#["hammer",         "Hammer", [("iron_hammer",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry, itc_scimitar, 7 , weight(2)|difficulty(0)|spd_rtng(100) | weapon_length(55)|swing_damage(14 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["club",         "Club", [("club",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 11 , weight(2.5)|difficulty(0)|spd_rtng(95) | weapon_length(95)|swing_damage(15 , blunt) | thrust_damage(0 ,  pierce),imodbits_none ],
#["winged_mace",         "Winged Mace", [("winged_mace",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 122 , weight(3.5)|difficulty(0)|spd_rtng(99) | weapon_length(80)|swing_damage(21 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
#["spiked_mace",         "Spiked Mace", [("spiked_mace",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 180 , weight(3.5)|difficulty(0)|spd_rtng(95) | weapon_length(90)|swing_damage(22 , blunt) | thrust_damage(0 ,  pierce),imodbits_pick ],
#["military_hammer", "Military Hammer", [("iron_hammer",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 317 , weight(4)|difficulty(0)|spd_rtng(92) | weapon_length(90)|swing_damage(25 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
#["maul",         "Maul", [("maul_b",0)], itp_type_two_handed_wpn|itp_shop|itp_primary|itp_two_handed|itp_wooden_parry|itp_wooden_attack, itc_nodachi|itcf_carry_spear, 97 , weight(6)|difficulty(11)|spd_rtng(84) | weapon_length(79)|swing_damage(33 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
#["sledgehammer", "Sledgehammer", [("maul_c",0)], itp_type_two_handed_wpn|itp_shop|itp_primary|itp_two_handed|itp_wooden_parry|itp_wooden_attack, itc_nodachi|itcf_carry_spear, 101 , weight(7)|difficulty(12)|spd_rtng(82) | weapon_length(82)|swing_damage(35 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["warhammer",         "Warhammer", [("maul_d",0)], itp_type_two_handed_wpn|itp_shop|itp_primary|itp_two_handed|itp_wooden_parry|itp_wooden_attack, itc_nodachi|itcf_carry_spear, 309 , weight(9)|difficulty(14)|spd_rtng(85) | weapon_length(75)|swing_damage(38 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
#["pickaxe",         "Pickaxe", [("rusty_pick",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 27 , weight(3)|difficulty(0)|spd_rtng(96) | weapon_length(80)|swing_damage(19 , pierce) | thrust_damage(0 ,  pierce),imodbits_pick ],
["spiked_club",         "Spiked Club", [("spiked_club",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 83 , weight(3)|difficulty(0)|spd_rtng(97) | weapon_length(97)|swing_damage(21 , pierce) | thrust_damage(0 ,  pierce),imodbits_mace ],
#["fighting_pick", "Fighting Pick", [("rusty_pick",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 108 , weight(3.5)|difficulty(0)|spd_rtng(94) | weapon_length(90)|swing_damage(25 , pierce) | thrust_damage(0 ,  pierce),imodbits_pick ],
#["military_pick", "Military Pick", [("steel_pick",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 142 , weight(4)|difficulty(0)|spd_rtng(90) | weapon_length(90)|swing_damage(27 , pierce) | thrust_damage(0 ,  pierce),imodbits_pick ],
#["morningstar",         "Morningstar", [("mace_morningstar",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 205 , weight(5.5)|difficulty(13)|spd_rtng(75) | weapon_length(98)|swing_damage(29 , pierce) | thrust_damage(0 ,  pierce),imodbits_mace ],
#["sickle",         "Sickle", [("sickle",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_no_parry|itp_wooden_parry, itc_cleaver, 1 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(40)|swing_damage(20 , cut) | thrust_damage(0 ,  pierce),imodbits_none ],
#["cleaver",         "Cleaver", [("cleaver",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_no_parry|itp_wooden_parry, itc_cleaver, 3 , weight(1.5)|difficulty(0)|spd_rtng(103) | weapon_length(30)|swing_damage(24 , cut) | thrust_damage(0 ,  pierce),imodbits_none ],
["knife",         "Knife", [("peasant_knife",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_no_parry, itc_dagger|itcf_carry_dagger_front_left, 4 , weight(0.5)|difficulty(0)|spd_rtng(110) | weapon_length(40)|swing_damage(21 , cut) | thrust_damage(13 ,  pierce),imodbits_sword ],
#["butchering_knife", "Butchering Knife", [("khyber_knife",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_no_parry, itc_dagger|itcf_carry_dagger_front_right, 13 , weight(0.75)|difficulty(0)|spd_rtng(108) | weapon_length(60)|swing_damage(24 , cut) | thrust_damage(17 ,  pierce),imodbits_sword ],
["dagger",         "Dagger", [("dagger",0),("scab_dagger",ixmesh_carry),("dagger_b",imodbits_good),("dagger_b_scabbard",ixmesh_carry|imodbits_good)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_no_parry, itc_dagger|itcf_carry_dagger_front_left|itcf_show_holster_when_drawn, 17 , weight(0.75)|difficulty(0)|spd_rtng(112) | weapon_length(47)|swing_damage(22 , cut) | thrust_damage(19 ,  pierce),imodbits_sword_high ],
#["nordic_sword", "Nordic Sword", [("viking_sword",0),("scab_vikingsw", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 142 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(98)|swing_damage(27 , cut) | thrust_damage(19 ,  pierce),imodbits_sword ],
#["arming_sword", "Arming Sword", [("b_long_sword",0),("scab_longsw_b", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 156 , weight(1.5)|difficulty(0)|spd_rtng(101) | weapon_length(100)|swing_damage(25 , cut) | thrust_damage(22 ,  pierce),imodbits_sword ],
#["sword",         "Sword", [("long_sword",0),("scab_longsw_a", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 148 , weight(1.5)|difficulty(0)|spd_rtng(100) | weapon_length(102)|swing_damage(26 , cut) | thrust_damage(23 ,  pierce),imodbits_sword ],
["falchion",         "Falchion", [("falchion",0)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(73)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
#["broadsword",         "Broadsword", [("broadsword",0),("scab_broadsword", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 122 , weight(2.5)|difficulty(8)|spd_rtng(91) | weapon_length(101)|swing_damage(27 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["scimitar",         "Scimitar", [("scimeter",0),("scab_scimeter", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 108 , weight(1.5)|difficulty(0)|spd_rtng(105) | weapon_length(97)|swing_damage(29 , cut) | thrust_damage(0 ,  pierce),imodbits_sword_high ],
["nomad_sabre",         "Nomad Sabre", [("shashqa",0),("scab_shashqa", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 115 , weight(1.75)|difficulty(0)|spd_rtng(101) | weapon_length(100)|swing_damage(27 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
#["bastard_sword", "Bastard Sword", [("bastard_sword",0),("scab_bastardsw", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 279 , weight(2.25)|difficulty(9)|spd_rtng(102) | weapon_length(120)|swing_damage(33 , cut) | thrust_damage(27 ,  pierce),imodbits_sword ],
#["great_sword",         "Great Sword", [("b_bastard_sword",0),("scab_bastardsw_b", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back|itcf_show_holster_when_drawn,
# 423 , weight(2.75)|difficulty(10)|spd_rtng(95) | weapon_length(125)|swing_damage(39 , cut) | thrust_damage(31 ,  pierce),imodbits_sword_high ],
#["sword_of_war", "Sword of War", [("b_bastard_sword",0),("scab_bastardsw_b", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back|itcf_show_holster_when_drawn,
# 524 , weight(3)|difficulty(11)|spd_rtng(93) | weapon_length(130)|swing_damage(40 , cut) | thrust_damage(31 ,  pierce),imodbits_sword_high ],
#["hatchet",         "Hatchet", [("hatchet",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 3 , weight(2)|difficulty(0)|spd_rtng(97) | weapon_length(60)|swing_damage(23 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["hand_axe",         "Hand Axe", [("hatchet",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 24 , weight(2)|difficulty(7)|spd_rtng(95) | weapon_length(75)|swing_damage(27 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["fighting_axe", "Fighting Axe", [("fighting_ax",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 77 , weight(2.5)|difficulty(9)|spd_rtng(92) | weapon_length(90)|swing_damage(31 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["axe",                 "Axe", [("iron_ax",0)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 65 , weight(4)|difficulty(8)|spd_rtng(91) | weapon_length(108)|swing_damage(32 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["voulge",         "Voulge", [("voulge",0)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 129 , weight(4.5)|difficulty(8)|spd_rtng(87) | weapon_length(119)|swing_damage(35 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["battle_axe",         "Battle Axe", [("battle_ax",0)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 240 , weight(5)|difficulty(9)|spd_rtng(88) | weapon_length(108)|swing_damage(41 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["war_axe",         "War Axe", [("war_ax",0)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 264 , weight(5)|difficulty(10)|spd_rtng(86) | weapon_length(110)|swing_damage(43 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["double_axe",         "Double Axe", [("dblhead_ax",0)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 359 , weight(6.5)|difficulty(12)|spd_rtng(85) | weapon_length(95)|swing_damage(43 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["great_axe",         "Great Axe", [("great_ax",0)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 415 , weight(7)|difficulty(13)|spd_rtng(82) | weapon_length(120)|swing_damage(45 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],

#["sword_two_handed_b",         "Two Handed Sword", [("sword_two_handed_b",0)], itp_type_two_handed_wpn|itp_shop|itp_always_loot|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back,
# 670 , weight(2.75)|difficulty(10)|spd_rtng(93) | weapon_length(110)|swing_damage(40 , cut) | thrust_damage(27 ,  pierce),imodbits_sword_high ],
["sword_two_handed_a",         "Great Sword", [("sword_two_handed_a",0)], itp_type_two_handed_wpn|itp_shop|itp_always_loot|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back,
 1123 , weight(2.75)|difficulty(10)|spd_rtng(89) | weapon_length(120)|swing_damage(42 , cut) | thrust_damage(28 ,  pierce),imodbits_sword_high ],

["bastard_sword_a", "Bastard Sword", [("bastard_sword_a",0),("bastard_sword_a_scabbard", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 294 , weight(2.25)|difficulty(9)|spd_rtng(98) | weapon_length(101)|swing_damage(37 , cut) | thrust_damage(26 ,  pierce),imodbits_sword_high ],
#["bastard_sword_b", "Heavy Bastard Sword", [("bastard_sword_b",0),("bastard_sword_b_scabbard", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 526 , weight(2.25)|difficulty(9)|spd_rtng(96) | weapon_length(105)|swing_damage(37 , cut) | thrust_damage(28 ,  pierce),imodbits_sword_high ],

["one_handed_war_axe_a", "One Handed War Axe", [("one_handed_war_axe_a",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
 87 , weight(1.5)|difficulty(9)|spd_rtng(100) | weapon_length(60)|swing_damage(32 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["one_handed_war_axe_b", "One Handed War Axe", [("one_handed_war_axe_b",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
# 137 , weight(1.5)|difficulty(9)|spd_rtng(98) | weapon_length(61)|swing_damage(34 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["one_handed_battle_axe_a", "One Handed Battle Axe", [("one_handed_battle_axe_a",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
# 102 , weight(1.5)|difficulty(9)|spd_rtng(97) | weapon_length(69)|swing_damage(34 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["one_handed_battle_axe_b", "One Handed Battle Axe", [("one_handed_battle_axe_b",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
# 171 , weight(1.75)|difficulty(9)|spd_rtng(96) | weapon_length(70)|swing_damage(36 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["one_handed_battle_axe_c", "One Handed Battle Axe", [("one_handed_battle_axe_c",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
# 294 , weight(2.0)|difficulty(9)|spd_rtng(95) | weapon_length(72)|swing_damage(38 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],


["two_handed_axe",         "Two_Handed_Axe", [("two_handed_battle_axe_a",0)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back,
 110 , weight(4.5)|difficulty(10)|spd_rtng(90) | weapon_length(90)|swing_damage(40 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["two_handed_battle_axe_2",         "Two_Handed_War_Axe", [("two_handed_battle_axe_b",0)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back,
# 202 , weight(4.5)|difficulty(10)|spd_rtng(92) | weapon_length(92)|swing_damage(47 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["two_handed_battle_axe_3",         "Voulge", [("two_handed_battle_axe_c",0)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back,
# 258 , weight(4.5)|difficulty(10)|spd_rtng(87) | weapon_length(100)|swing_damage(48 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["bardiche",         "Bardiche", [("two_handed_battle_axe_d",0)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back,
# 311 , weight(4.5)|difficulty(10)|spd_rtng(87) | weapon_length(102)|swing_damage(50 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["great_axe",         "Great_Axe", [("two_handed_battle_axe_e",0)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back,
# 446 , weight(4.5)|difficulty(10)|spd_rtng(90) | weapon_length(96)|swing_damage(51 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
 
#["great_bardiche",         "Great_Bardiche", [("two_handed_battle_axe_f",0)], itp_type_two_handed_wpn|itp_always_loot|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back,
# 617 , weight(4.5)|difficulty(10)|spd_rtng(90) | weapon_length(116)|swing_damage(47 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["shortened_military_scythe",         "Shortened Military Scythe", [("two_handed_battle_scythe_a",0)], itp_type_two_handed_wpn|itp_shop|itp_always_loot|itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back,
# 264 , weight(3.0)|difficulty(10)|spd_rtng(90) | weapon_length(112)|swing_damage(44 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],

#["sword_medieval_a", "Sword", [("sword_medieval_a",0),("sword_medieval_a_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 163 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(95)|swing_damage(27 , cut) | thrust_damage(22 ,  pierce),imodbits_sword_high ],
#["sword_medieval_a_long", "Sword", [("sword_medieval_a_long",0),("sword_medieval_a_long_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 156 , weight(1.5)|difficulty(0)|spd_rtng(97) | weapon_length(105)|swing_damage(25 , cut) | thrust_damage(22 ,  pierce),imodbits_sword ],
#["sword_medieval_b", "Sword", [("sword_medieval_b",0),("sword_medieval_b_scabbard", ixmesh_carry),("sword_rusty_a",imodbit_rusty),("sword_rusty_a_scabbard", ixmesh_carry|imodbit_rusty)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 243 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(95)|swing_damage(28 , cut) | thrust_damage(23 ,  pierce),imodbits_sword_high ],
["sword_medieval_b_small", "Short Sword", [("sword_medieval_b_small",0),("sword_medieval_b_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 152 , weight(1.5)|difficulty(0)|spd_rtng(102) | weapon_length(85)|swing_damage(26, cut) | thrust_damage(24, pierce),imodbits_sword_high ],
["sword_medieval_c", "Arming Sword", [("sword_medieval_c",0),("sword_medieval_c_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 410 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(95)|swing_damage(29 , cut) | thrust_damage(24 ,  pierce),imodbits_sword_high ,
 #[(ti_on_weapon_attack, [ (display_message,"@DEBUG: Sword hit!!!"),(display_message,"@DEBUG: Sowrf hit!!!") ]) ] 
],
#["sword_medieval_c", "Short Arming Sword", [("sword_medieval_c",0),("sword_medieval_c_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 243 , weight(1.5)|difficulty(0)|spd_rtng(103) | weapon_length(86)|swing_damage(26, cut) | thrust_damage(24 ,  pierce),imodbits_sword_high ],
#["sword_medieval_d", "sword_medieval_d", [("sword_medieval_d",0),("sword_medieval_d_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
###131 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(95)|swing_damage(24 , cut) | thrust_damage(21 ,  pierce),imodbits_sword ],
#["sword_medieval_d_long", "sword_medieval_d_long", [("sword_medieval_d_long",0),("sword_medieval_d_long_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
###156 , weight(1.5)|difficulty(0)|spd_rtng(97) | weapon_length(105)|swing_damage(25 , cut) | thrust_damage(22 ,  pierce),imodbits_sword ],
#["sword_medieval_e", "sword_medieval_e", [("sword_medieval_e",0),("sword_medieval_e_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
###131 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(95)|swing_damage(24 , cut) | thrust_damage(21 ,  pierce),imodbits_sword ],

["sword_viking_1", "Nordic Sword", [("sword_viking_c",0),("sword_viking_c_scabbard ", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 147 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(94)|swing_damage(28 , cut) | thrust_damage(20 ,  pierce),imodbits_sword_high ] ,
#["sword_viking_2", "Nordic Sword", [("sword_viking_b",0),("sword_viking_b_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 276 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(95)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
#["sword_viking_2_small", "Nordic Short Sword", [("sword_viking_b_small",0),("sword_viking_b_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(85)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
#["sword_viking_3", "Nordic Sword", [("sword_viking_a",0),("sword_viking_a_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 394 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(95)|swing_damage(30 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
#["sword_viking_a_long", "sword_viking_a_long", [("sword_viking_a_long",0),("sword_viking_a_long_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
###142 , weight(1.5)|difficulty(0)|spd_rtng(97) | weapon_length(105)|swing_damage(27 , cut) | thrust_damage(19 ,  pierce),imodbits_sword ],
#["sword_viking_3_small", "Nordic Sword", [("sword_viking_a_small",0),("sword_viking_a_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 280 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(86)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
#["sword_viking_c_long", "sword_viking_c_long", [("sword_viking_c_long",0),("sword_viking_c_long_scabbard ", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
###142 , weight(1.5)|difficulty(0)|spd_rtng(95) | weapon_length(105)|swing_damage(27 , cut) | thrust_damage(19 ,  pierce),imodbits_sword ] ,

#["scythe",         "Scythe", [("scythe",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear, 43 , weight(3)|difficulty(0)|spd_rtng(79) | weapon_length(182)|swing_damage(19 , cut) | thrust_damage(14 ,  pierce),imodbits_polearm ],
["pitch_fork",         "Pitch Fork", [("pitch_fork",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_spear, 19 , weight(3.5)|difficulty(0)|spd_rtng(83) | weapon_length(154)|swing_damage(0 , blunt) | thrust_damage(18 ,  pierce),imodbits_polearm ],
#["military_fork", "Military Fork", [("military_fork",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_spear, 153 , weight(4.5)|difficulty(0)|spd_rtng(88) | weapon_length(135)|swing_damage(0 , blunt) | thrust_damage(23 ,  pierce),imodbits_polearm ],
#["battle_fork",         "Battle Fork", [("battle_fork",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_spear, 282 , weight(4.5)|difficulty(0)|spd_rtng(87) | weapon_length(142)|swing_damage(0 , blunt) | thrust_damage(24 ,  pierce),imodbits_polearm ],
#["boar_spear",         "Boar Spear", [("spear",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_spear|itcf_carry_spear, 76 , weight(4)|difficulty(0)|spd_rtng(81) | weapon_length(157)|swing_damage(0 , cut) | thrust_damage(23 ,  pierce),imodbits_polearm ],
#["spear",         "Spear", [("spear",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear|itcf_carry_spear, 173 , weight(4.5)|difficulty(0)|spd_rtng(80) | weapon_length(158)|swing_damage(17 , blunt) | thrust_damage(23 ,  pierce),imodbits_polearm ],


#["jousting_lance", "Jousting Lance", [("joust_of_peace",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_greatlance, 158 , weight(5)|difficulty(0)|spd_rtng(61) | weapon_length(218)|swing_damage(0 , cut) | thrust_damage(17 ,  blunt),imodbits_polearm ],
#["lance",         "Lance", [("pike",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_spear, 196 , weight(5)|difficulty(0)|spd_rtng(72) | weapon_length(170)|swing_damage(0 , cut) | thrust_damage(20 ,  pierce),imodbits_polearm ],
#["great_lance",         "Great Lance", [("heavy_lance",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_greatlance, 237 , weight(5)|difficulty(0)|spd_rtng(55) | weapon_length(215)|swing_damage(0 , cut) | thrust_damage(21 ,  pierce),imodbits_polearm ],
#["double_sided_lance", "Double Sided Lance", [("lance_dblhead",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff, 261 , weight(5.5)|difficulty(0)|spd_rtng(80) | weapon_length(130)|swing_damage(0 , cut) | thrust_damage(27 ,  pierce),imodbits_polearm ],
#["pike",         "Pike", [("pike",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_spear,
###212 , weight(6)|difficulty(0)|spd_rtng(77) | weapon_length(167)|swing_damage(0 , blunt) | thrust_damage(23 ,  pierce),imodbits_polearm ],
["glaive",         "Glaive", [("glaive",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_staff|itcf_carry_spear,
 352 , weight(4.5)|difficulty(0)|spd_rtng(83) | weapon_length(157)|swing_damage(38 , cut) | thrust_damage(21 ,  pierce),imodbits_polearm ],
#["poleaxe",         "Poleaxe", [("pole_ax",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_staff,
# 384 , weight(6.5)|difficulty(0)|spd_rtng(77) | weapon_length(180)|swing_damage(37 , cut) | thrust_damage(21 ,  pierce),imodbits_polearm ],
#["polehammer",         "Polehammer", [("pole_hammer",0)], itp_type_polearm|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_staff,
# 169 , weight(7)|difficulty(14)|spd_rtng(73) | weapon_length(130)|swing_damage(29 , blunt) | thrust_damage(25 ,  blunt),imodbits_polearm ],
#["staff",         "Staff", [("wooden_staff",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack, itc_staff|itcf_carry_sword_back,
 #36 , weight(1.5)|difficulty(0)|spd_rtng(100) | weapon_length(130)|swing_damage(18 , blunt) | thrust_damage(19 ,  blunt),imodbits_polearm ],
["quarter_staff", "Quarter Staff", [("quarter_staff",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack, itc_staff|itcf_carry_sword_back,
 60 , weight(2)|difficulty(0)|spd_rtng(104) | weapon_length(140)|swing_damage(20 , blunt) | thrust_damage(20 ,  blunt),imodbits_polearm ],
#["quarter_staff",         "Iron Staff", [("quarter_staff",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield, itc_staff|itcf_carry_sword_back,
# 202 , weight(2)|difficulty(0)|spd_rtng(97) | weapon_length(140)|swing_damage(25 , blunt) | thrust_damage(26 ,  blunt),imodbits_polearm ],

["shortened_spear",         "Shortened_Spear", [("spear_g_1-9m",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_back,
 53 , weight(2.0)|difficulty(0)|spd_rtng(102) | weapon_length(120)|swing_damage(19 , blunt) | thrust_damage(25 ,  pierce),imodbits_polearm ],
["spear",         "Spear", [("spear_h_2-15m",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear,
 75 , weight(2.25)|difficulty(0)|spd_rtng(98) | weapon_length(135)|swing_damage(20 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm ],
["war_spear",         "War_Spear", [("spear_i_2-3m",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear,
 90 , weight(2.5)|difficulty(0)|spd_rtng(96) | weapon_length(150)|swing_damage(20 , blunt) | thrust_damage(27 ,  pierce),imodbits_polearm ],
#TODO:["shortened_spear",         "shortened_spear", [("spear_e_2-1m",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear,
###65 , weight(2.0)|difficulty(0)|spd_rtng(98) | weapon_length(110)|swing_damage(17 , blunt) | thrust_damage(23 ,  pierce),imodbits_polearm ],
#TODO:["spear_2-4m",         "spear", [("spear_e_2-25m",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear,
###67 , weight(2.0)|difficulty(0)|spd_rtng(95) | weapon_length(125)|swing_damage(17 , blunt) | thrust_damage(23 ,  pierce),imodbits_polearm ],
#["spear_e_2-5m",         "Military Scythe", [("spear_e_2-5m",0),("spear_c_2-5m",imodbits_bad)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear|itcf_carry_spear,
# 145 , weight(2.5)|difficulty(10)|spd_rtng(93) | weapon_length(155)|swing_damage(36 , cut) | thrust_damage(25 ,  pierce),imodbits_polearm ],
["light_lance",         "Light Lance", [("spear_b_2-75m",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear,
 89 , weight(2.5)|difficulty(0)|spd_rtng(90) | weapon_length(175)|swing_damage(16 , blunt) | thrust_damage(27 ,  pierce),imodbits_polearm ],
["lance",         "Lance", [("spear_d_2-8m",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear,
 110 , weight(2.5)|difficulty(0)|spd_rtng(88) | weapon_length(180)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm ],
["heavy_lance",         "Heavy Lance", [("spear_f_2-9m",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear,
 130 , weight(2.75)|difficulty(10)|spd_rtng(85) | weapon_length(190)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm ],
["pike",         "Pike", [("spear_a_3m",0)], itp_type_polearm|itp_shop|itp_cant_use_on_horseback|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear,
 125 , weight(3.0)|difficulty(0)|spd_rtng(81) | weapon_length(245)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm ],
##["spear_e_3-25m",         "Spear_3-25m", [("spear_e_3-25m",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear|itcf_carry_spear,
####150 , weight(4.5)|difficulty(0)|spd_rtng(81) | weapon_length(225)|swing_damage(19 , blunt) | thrust_damage(23 ,  pierce),imodbits_polearm ],
#["ashwood_pike", "Ashwood Pike", [("pike",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_cutting_spear,
# 205 , weight(3.5)|difficulty(11)|spd_rtng(90) | weapon_length(170)|swing_damage(19 , blunt) | thrust_damage(29,  pierce),imodbits_polearm ],
#["awlpike",         "Awlpike", [("pike",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_cutting_spear|itcf_carry_spear,
# 378 , weight(3.5)|difficulty(12)|spd_rtng(92) | weapon_length(160)|swing_damage(30 , cut) | thrust_damage(31 ,  pierce),imodbits_polearm ],


###SHIELDS

["wooden_shield", "Wooden Shield", [("shield_round_a",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  42 , weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(50),imodbits_shield ],

#["round_shield", "Round Shield", [("shield_round_c",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  64 , weight(2)|hit_points(400)|body_armor(1)|spd_rtng(100)|weapon_length(50),imodbits_shield ],
["nordic_shield", "Nordic Shield", [("shield_round_b",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  95 , weight(2)|hit_points(440)|body_armor(1)|spd_rtng(100)|weapon_length(50),imodbits_shield ],
["fur_covered_shield",  "Fur Covered Shield", [("shield_kite_m",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  227 , weight(3.5)|hit_points(600)|body_armor(1)|spd_rtng(76)|weapon_length(81),imodbits_shield ],
["hide_covered_round_shield", "Hide_Covered_Round_Shield", [("shield_round_f",0)], itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  40 , weight(2)|hit_points(260)|body_armor(3)|spd_rtng(100)|weapon_length(40),imodbits_shield ],
["shield_heater_c", "Heater Shield", [("shield_heater_c",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  277 , weight(3.5)|hit_points(410)|body_armor(2)|spd_rtng(80)|weapon_length(50),imodbits_shield ],
#["tab_shield_round_a", "Old Round Shield", [("tableau_shield_round_5",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  26 , weight(2.5)|hit_points(350)|body_armor(0)|spd_rtng(93)|weapon_length(50),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_round_shield_5", ":agent_no", ":troop_no")])]],
#["tab_shield_round_b", "Plain Round Shield", [("tableau_shield_round_3",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  65 , weight(3)|hit_points(460)|body_armor(2)|spd_rtng(90)|weapon_length(50),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_round_shield_3", ":agent_no", ":troop_no")])]],
#["tab_shield_round_c", "Round_Shield", [("tableau_shield_round_2",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  105 , weight(3.5)|hit_points(540)|body_armor(4)|spd_rtng(87)|weapon_length(50),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner","tableau_round_shield_2", ":agent_no", ":troop_no")])]],
#["tab_shield_round_d", "Heavy Round_Shield", [("tableau_shield_round_1",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  210 , weight(4)|hit_points(600)|body_armor(6)|spd_rtng(84)|weapon_length(50),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_round_shield_1", ":agent_no", ":troop_no")])]],
#["tab_shield_round_e", "Huscarl's Round_Shield", [("tableau_shield_round_4",0)], itp_shop|itp_type_shield, itcf_carry_round_shield,  430 , weight(4.5)|hit_points(690)|body_armor(8)|spd_rtng(81)|weapon_length(50),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_round_shield_4", ":agent_no", ":troop_no")])]],

#["tab_shield_kite_a", "Old Kite Shield",   [("tableau_shield_kite_1" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  33 , weight(2)|hit_points(285)|body_armor(0)|spd_rtng(96)|weapon_length(60),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_kite_shield_1", ":agent_no", ":troop_no")])]],
#["tab_shield_kite_b", "Plain Kite Shield",   [("tableau_shield_kite_3" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  70 , weight(2.5)|hit_points(365)|body_armor(2)|spd_rtng(93)|weapon_length(60),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_kite_shield_3", ":agent_no", ":troop_no")])]],
#["tab_shield_kite_c", "Kite Shield",   [("tableau_shield_kite_2" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  156 , weight(3)|hit_points(435)|body_armor(5)|spd_rtng(90)|weapon_length(60),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_kite_shield_2", ":agent_no", ":troop_no")])]],
#["tab_shield_kite_d", "Heavy Kite Shield",   [("tableau_shield_kite_2" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  320 , weight(3.5)|hit_points(515)|body_armor(8)|spd_rtng(87)|weapon_length(60),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_kite_shield_2", ":agent_no", ":troop_no")])]],
#["tab_shield_kite_cav_a", "Horseman's Kite Shield",   [("tableau_shield_kite_4" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  205 , weight(2)|hit_points(310)|body_armor(10)|spd_rtng(103)|weapon_length(40),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_kite_shield_4", ":agent_no", ":troop_no")])]],
#["tab_shield_kite_cav_b", "Knightly Kite Shield",   [("tableau_shield_kite_4" ,0)], itp_shop|itp_type_shield, itcf_carry_kite_shield,  360 , weight(2.5)|hit_points(370)|body_armor(16)|spd_rtng(100)|weapon_length(40),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_kite_shield_4", ":agent_no", ":troop_no")])]],

#["tab_shield_heater_a", "Old Heater Shield",   [("tableau_shield_heater_1" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  36 , weight(2)|hit_points(280)|body_armor(1)|spd_rtng(96)|weapon_length(60),imodbits_shield,
 #[(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heater_shield_1", ":agent_no", ":troop_no")])]],
#["tab_shield_heater_b", "Plain Heater Shield",   [("tableau_shield_heater_1" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  74 , weight(2.5)|hit_points(360)|body_armor(3)|spd_rtng(93)|weapon_length(60),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heater_shield_1", ":agent_no", ":troop_no")])]],
#["tab_shield_heater_c", "Heater Shield",   [("tableau_shield_heater_1" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  160 , weight(3)|hit_points(430)|body_armor(6)|spd_rtng(90)|weapon_length(60),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heater_shield_1", ":agent_no", ":troop_no")])]],
#["tab_shield_heater_d", "Heavy Heater Shield",   [("tableau_shield_heater_1" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  332 , weight(3.5)|hit_points(510)|body_armor(9)|spd_rtng(87)|weapon_length(60),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heater_shield_1", ":agent_no", ":troop_no")])]],
#["tab_shield_heater_cav_a", "Horseman's Heater Shield",   [("tableau_shield_heater_2" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  229 , weight(2)|hit_points(300)|body_armor(12)|spd_rtng(103)|weapon_length(40),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heater_shield_2", ":agent_no", ":troop_no")])]],
#["tab_shield_heater_cav_b", "Knightly Heater Shield",   [("tableau_shield_heater_2" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  390 , weight(2.5)|hit_points(360)|body_armor(18)|spd_rtng(100)|weapon_length(40),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heater_shield_2", ":agent_no", ":troop_no")])]],

#["tab_shield_pavise_a", "Old Board Shield",   [("tableau_shield_pavise_2" ,0)], itp_shop|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield,  60 , weight(3.5)|hit_points(510)|body_armor(0)|spd_rtng(89)|weapon_length(84),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_pavise_shield_2", ":agent_no", ":troop_no")])]],
#["tab_shield_pavise_b", "Plain Board Shield",   [("tableau_shield_pavise_2" ,0)], itp_shop|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield,  114 , weight(4)|hit_points(640)|body_armor(1)|spd_rtng(85)|weapon_length(84),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_pavise_shield_2", ":agent_no", ":troop_no")])]],
#["tab_shield_pavise_c", "Board Shield",   [("tableau_shield_pavise_1" ,0)], itp_shop|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield,  210 , weight(4.5)|hit_points(760)|body_armor(2)|spd_rtng(81)|weapon_length(84),imodbits_shield,
 #[(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_pavise_shield_1", ":agent_no", ":troop_no")])]],
#["tab_shield_pavise_d", "Heavy Board Shield",   [("tableau_shield_pavise_1" ,0)], itp_shop|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield,  370 , weight(5)|hit_points(980)|body_armor(3)|spd_rtng(78)|weapon_length(84),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_pavise_shield_1", ":agent_no", ":troop_no")])]],

#["tab_shield_small_round_a", "Plain Cavalry Shield", [("tableau_shield_small_round_3",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  96 , weight(2)|hit_points(310)|body_armor(3)|spd_rtng(105)|weapon_length(40),imodbits_shield,
#[(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_small_round_shield_3", ":agent_no", ":troop_no")])]],
["tab_shield_small_round_b", "Round Cavalry Shield", [("tableau_shield_small_round_1",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  195 , weight(2.5)|hit_points(370)|body_armor(9)|spd_rtng(103)|weapon_length(40),imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_shield_item_set_banner", "tableau_small_round_shield_1", ":agent_no", ":troop_no")])]],
#["tab_shield_small_round_c", "Elite Cavalry Shield", [("tableau_shield_small_round_2",0)], itp_shop|itp_type_shield, itcf_carry_round_shield,  370 , weight(3)|hit_points(420)|body_armor(14)|spd_rtng(100)|weapon_length(40),imodbits_shield,
# [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_small_round_shield_2", ":agent_no", ":troop_no")])]],


#RANGED
["javelin",         "Javelin", [("javelin",0),("javelins_quiver", ixmesh_carry)], itp_type_thrown |itp_shop|itp_primary|itp_bonus_against_shield ,itcf_throw_javelin|itcf_carry_quiver_back_right |itcf_show_holster_when_drawn, 75 , weight(5)|difficulty(1)|spd_rtng(91) | shoot_speed(28) | thrust_damage(28 ,  pierce)|max_ammo(3)|weapon_length(75),imodbits_thrown ],
#["stones",         "Stones", [("throwing_stone",0)], itp_type_thrown |itp_shop|itp_primary ,itcf_throw_stone, 1 , weight(4)|difficulty(0)|spd_rtng(97) | shoot_speed(30) | thrust_damage(11 ,  blunt)|max_ammo(18)|weapon_length(8),imodbit_large_bag ],
["throwing_knives", "Throwing Knives", [("throwing_knife",0)], itp_type_thrown |itp_shop|itp_primary ,itcf_throw_knife, 76 , weight(3.5)|difficulty(0)|spd_rtng(121) | shoot_speed(25) | thrust_damage(19 ,  cut)|max_ammo(15)|weapon_length(0),imodbits_thrown ],
#["throwing_daggers", "Throwing Daggers", [("throwing_dagger",0)], itp_type_thrown |itp_shop|itp_primary ,itcf_throw_knife, 193 , weight(3.5)|difficulty(0)|spd_rtng(110) | shoot_speed(24) | thrust_damage(25 ,  cut)|max_ammo(14)|weapon_length(0),imodbits_thrown ],
["throwing_axes", "Throwing Axes", [("francisca",0)], itp_type_thrown |itp_shop|itp_primary|itp_bonus_against_shield,itcf_throw_axe,241, weight(5)|difficulty(1)|spd_rtng(99) | shoot_speed(20) | thrust_damage(38,cut)|max_ammo(2)|weapon_length(53),imodbits_thrown ],
["short_bow",         "Short Bow", [("small_bow",0),("small_bow_carry",ixmesh_carry)], itp_type_bow |itp_shop|itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bow_back, 17 , weight(1)|difficulty(0)|spd_rtng(100) | shoot_speed(48) | thrust_damage(15 ,  bow_damage),imodbits_bow ],
["regular_bow",         "Bow", [("regular_bow",0),("regular_bow_carry",ixmesh_carry)], itp_type_bow |itp_shop|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 58 , weight(1)|difficulty(1)|spd_rtng(98) | shoot_speed(52) | thrust_damage(18 ,  bow_damage  ),imodbits_bow ],
["nomad_bow",         "Nomad Bow", [("nomad_bow",0),("nomad_bow_case", ixmesh_carry)], itp_type_bow |itp_shop|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 164 , weight(1.25)|difficulty(2)|spd_rtng(96) | shoot_speed(53) | thrust_damage(20 ,  bow_damage),imodbits_bow ],
["gondor_bow",         "Gondor Bow", [("gondor_bow",0),("gondor_bow_carry",ixmesh_carry)], itp_type_bow |itp_shop|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 145 , weight(1.75)|difficulty(3)|spd_rtng(82) | shoot_speed(54) | thrust_damage(22 ,  bow_damage),imodbits_bow ],
#["khergit_bow",       "Haradrim Bow", [("khergit_bow",0),("khergit_bow_case", ixmesh_carry)], itp_type_bow |itp_shop|itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 269 , weight(1.25)|difficulty(3)|spd_rtng(95) | shoot_speed(56) | thrust_damage(21 ,bow_damage),imodbits_bow ],
["strong_bow",         "Rohan Bow", [("strong_bow",0),("strong_bow_case", ixmesh_carry)], itp_type_bow |itp_shop|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 437 , weight(1.25)|difficulty(3)|spd_rtng(94) | shoot_speed(57) | thrust_damage(23 ,bow_damage),imodbit_cracked | imodbit_bent | imodbit_masterwork ],
["elven_bow",         "Elven Bow", [("elven_bow",0),("elven_bow_carry",ixmesh_carry)],itp_type_bow|itp_shop|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 728 , weight(1.5)|difficulty(4)|spd_rtng(93) | shoot_speed(58) | thrust_damage(25 ,bow_damage),imodbits_bow,],
["corsair_bow",         "Corsair Bow", [("corsair_bow",0),("corsair_bow_carry",ixmesh_carry)],itp_type_bow|itp_shop|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 728 , weight(1.5)|difficulty(4)|spd_rtng(93) | shoot_speed(58) | thrust_damage(25 ,bow_damage),imodbits_bow,],
#["hunting_crossbow", "Hunting Crossbow", [("crossbow",0)], itp_type_crossbow |itp_shop|itp_primary|itp_two_handed ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 22 , weight(2.25)|difficulty(0)|spd_rtng(47) | shoot_speed(50) | thrust_damage(28 ,  bow_damage)|max_ammo(1),imodbits_crossbow ],
#["light_crossbow", "Light Crossbow", [("light_crossbow",0)], itp_type_crossbow |itp_shop|itp_primary|itp_two_handed ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 67 , weight(2.5)|difficulty(8)|spd_rtng(45) | shoot_speed(59) | thrust_damage(34 ,  bow_damage)|max_ammo(1),imodbits_crossbow ],
#["crossbow",         "Crossbow",         [("crossbow",0)], itp_type_crossbow |itp_shop|itp_primary|itp_two_handed|itp_cant_use_on_horseback ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 182 , weight(3)|difficulty(8)|spd_rtng(43) | shoot_speed(68) | thrust_damage(38,bow_damage)|max_ammo(1),imodbits_crossbow ],
#["heavy_crossbow", "Heavy Crossbow", [("heavy_crossbow",0)], itp_type_crossbow |itp_shop|itp_primary|itp_two_handed|itp_cant_use_on_horseback ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 349 , weight(3.5)|difficulty(9)|spd_rtng(41) | shoot_speed(72) | thrust_damage(46 ,bow_damage)|max_ammo(1),imodbits_crossbow ],
#["sniper_crossbow", "Siege Crossbow", [("heavy_crossbow",0)], itp_type_crossbow |itp_shop|itp_primary|itp_two_handed|itp_cant_use_on_horseback ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 683 , weight(3.75)|difficulty(10)|spd_rtng(37) | shoot_speed(74) | thrust_damage(49 ,bow_damage)|max_ammo(1),imodbits_crossbow ],
#["flintlock_pistol", "Flintlock Pistol", [("flintlock_pistol",0)], itp_type_pistol |itp_shop|itp_primary ,itcf_shoot_pistol|itcf_reload_pistol, 230 , weight(1.5)|difficulty(0)|spd_rtng(38) | shoot_speed(160) | thrust_damage(41 ,bow_damage)|max_ammo(1)|accuracy(65),imodbits_none,
# [(ti_on_weapon_attack, [(play_sound,"snd_pistol_shot"),(position_move_x, pos1,27),(position_move_y, pos1,36),(particle_system_burst, "psys_pistol_smoke", pos1, 15)])]],
#["torch",         "Torch", [("club",0)], itp_type_one_handed_wpn|itp_primary, itc_scimitar, 11 , weight(2.5)|difficulty(0)|spd_rtng(95) | weapon_length(95)|swing_damage(11 , blunt) | thrust_damage(0 ,  pierce),imodbits_none,
# [(ti_on_init_item, [(set_position_delta,0,60,0),(particle_system_add_new, "psys_torch_fire"),(particle_system_add_new, "psys_torch_smoke"),(set_current_color,150, 130, 70),(add_point_light, 10, 30),
#])]],

##########TLD ITEMS START##########
#####TLD RIVENDELL/DUNEDAIN ITEMS##########
	###ARNOR HELMS########
["arnor_helm_a", "Arnor Helm", [("dunedain_helm_a",0)], itp_shop|itp_type_head_armor,0, 320 , weight(1.35)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["arnor_helm_b", "Arnor Helm", [("dunedain_helm_b",0)], itp_shop|itp_type_head_armor,0, 330 , weight(1.35)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["arnor_helm_c", "Arnor Helm", [("dunedain_helm_c",0)], itp_shop|itp_type_head_armor,0, 340 , weight(1.75)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["dunedain_helm_a", "Dunedain Hood", [("arnor_hood",0)], itp_shop|itp_type_head_armor,0, 350 , weight(1.35)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["dunedain_helm_b", "Arnor Helm", [("arnor_helm_a",0)], itp_shop|itp_type_head_armor,0, 360 , weight(1.35)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
#["dunedain_helm_c", "Dunedain Helm", [("dunedain_helm_a",0)], itp_shop|itp_type_head_armor,0, 380 , weight(1.75)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
	
	#ARNOR ARMORS########
["arnor_armor_a",  "Arnorian Armor", [("arnor_blue",0)],             itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 2854 , weight(20)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(13)|difficulty(7) ,imodbits_armor],
["arnor_armor_b",  "Arnorian Armor", [("arnor_brown",0)],            itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 2854 , weight(20)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(13)|difficulty(7) ,imodbits_armor],
["arnor_armor_c",  "Dunedain Ranger Leather", [("arnor_ranger",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,1530 , weight(19)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(10)|difficulty(0) ,imodbits_armor ],
["arnor_armor_d",  "Dunedain Ranger Leather", [("arnor_ranger_b",0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,1930 , weight(19)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(13)|difficulty(0) ,imodbits_armor ],
["arnor_armor_e", "Arnorian Reinforced Jerkin", [("arnor_reinf_jerkin",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 2710 , weight(23)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(14)|difficulty(8) ,imodbits_armor ],
["arnor_armor_f",  "Arnorian High Armor", [("arnor_knight",0)],   itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 3100 , weight(24)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(15)|difficulty(8) ,imodbits_armor ],

["arnor_greaves", "Arnorian Greaves", [("arnor_greaves",0)],itp_shop|itp_type_foot_armor |itp_attach_armature,0, 760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],
["arnor_splinted", "Arnorian Splinted Greaves", [("arnor_splinted",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0, 1153 , weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(28)|difficulty(7) ,imodbits_armor ],

	#ARNOR SHIELDS########
["arnor_shield_a", "Arnor Shield", [("arnor_shield_inf",0)], itp_shop|itp_type_shield|itp_wooden_parry,  itcf_carry_round_shield,  118 , weight(1.3)|hit_points(380)|body_armor(1)|spd_rtng(100)|weapon_length(39),imodbits_shield ],
#["arnor_shield_b", "Arnor Buckler", [("arnor_buckler",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  118 , weight(1.3)|hit_points(380)|body_armor(1)|spd_rtng(100)|weapon_length(39),imodbits_shield ],
["arnor_shield_c", "Arnor Cavalry Shield", [("arnor_cav_shield",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  118 , weight(1.3)|hit_points(380)|body_armor(1)|spd_rtng(100)|weapon_length(39),imodbits_shield ],
["arnor_shield_b", "Arnor Shield", [("arnor_shield_inf_b",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  118 , weight(1.3)|hit_points(380)|body_armor(1)|spd_rtng(100)|weapon_length(39),imodbits_shield ],
["arnor_shield_d", "Arnor Cavalry Shield", [("arnor_cav_shield_b",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  118 , weight(1.3)|hit_points(380)|body_armor(1)|spd_rtng(100)|weapon_length(39),imodbits_shield ],

	#ARNOR MOUNTS########
["arnor_warhorse","Arnorian Warhorse", [("arnor_mail",0)], itp_shop|itp_type_horse, 0, 724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
["dunedain_warhorse","Dunedain Warhorse", [("arnor_leather",0)],itp_shop|itp_type_horse, 0, 1411,abundance(40)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25),imodbits_horse_basic|imodbit_champion],

	##########ARNOR WEAPONS########
["arnor_sword_a", "Arnor Bastard Sword", [("dunedain_bastard_a",0),("scab_dunedain_bastard_a", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 294 , weight(2.05)|difficulty(9)|spd_rtng(99) | weapon_length(100)|swing_damage(36 , cut) | thrust_damage(27 ,  pierce),imodbits_sword_high ],
#["arnor_sword_b", "Arnor Bastard Sword", [("dunedain_bastard_c",0),("bastard_sword_a_scabbard", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 #324 , weight(2.25)|difficulty(9)|spd_rtng(97) | weapon_length(110)|swing_damage(38 , cut) | thrust_damage(27 ,  pierce),imodbits_sword_high ],
["arnor_sword_c", "Arnor Bastard Sword", [("dunedain_bastard_d",0),("scab_dunedain_bastard_d", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 294 , weight(2.25)|difficulty(9)|spd_rtng(98) | weapon_length(109)|swing_damage(37 , cut) | thrust_damage(26 ,  pierce),imodbits_sword_high ],
#["arnor_sword_d", "Arnor Bastard Sword", [("dunedain_bastard_d",0),("bastard_sword_a_scabbard", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 294 , weight(2.25)|difficulty(9)|spd_rtng(99) | weapon_length(97)|swing_damage(36 , cut) | thrust_damage(27 ,  pierce),imodbits_sword_high ],
#["arnor_sword_e", "Arnor Shortsword", [("dunedain_1h",0),("sword_medieval_b_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 #152 , weight(1.5)|difficulty(0)|spd_rtng(102) | weapon_length(85)|swing_damage(26, cut) | thrust_damage(24, pierce),imodbits_sword_high ],
["arnor_sword_f", "Arnor Shortsword", [("dunedain_1h",0),("scab_dunedain_1h", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(83)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
 
 ["sword_of_arathorn", "Sword of Arathorn", [("aragorn_sword",0),("scab_aragorn_sword", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 294 , weight(2.05)|difficulty(9)|spd_rtng(99) | weapon_length(96)|swing_damage(36 , cut) | thrust_damage(27 ,  pierce),imodbits_sword_high ],

	#RIVENDELL HELMS##########
["riv_helm_a", "Rivendell Coif", [("rivendell_coif",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
["riv_helm_b", "Rivendell Helm", [("rivendellarcherhelmet",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
["riv_helm_c", "Rivendell Helm", [("rivendellswordfighterhelmet",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
#["riv_helm_d", "Rivendell Helm", [("elvenhelm_b",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
	
	##########RIVENDELL SHIELDS##########
["riv_shield_a", "Rivendell Shield", [("riv_inf_shield",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  318 , weight(2.5)|hit_points(440)|body_armor(1)|spd_rtng(85)|weapon_length(82),imodbits_shield ],
["riv_shield_b", "Rivendell Shield", [("riv_cav_shield",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  418 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#["riv_shield_c", "Rivendell Shield", [("riv_inf_shield_long_a",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  218 , weight(2.0)|hit_points(380)|body_armor(1)|spd_rtng(99)|weapon_length(50),imodbits_shield ],
#["riv_shield_d", "Rivendell Shield", [("riv_inf_shield_long_b",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  318 , weight(2.5)|hit_points(440)|body_armor(1)|spd_rtng(85)|weapon_length(82),imodbits_shield ],
#["riv_shield_e", "Rivendell Shield", [("riv_inf_shield_short_a",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  418, weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#["riv_shield_f", "Rivendell Shield", [("riv_inf_shield_short_b",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  218 , weight(2.0)|hit_points(380)|body_armor(1)|spd_rtng(99)|weapon_length(50),imodbits_shield  ],
 
	#####RIVENDELL WEAPONS########
["riv_bas_sword", "Rivendell Bastard Sword", [("rivendell_handandahalf1",0),("scab_rivendell_handandahalf1", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 294 , weight(2.25)|abundance(100)|difficulty(9)|spd_rtng(98) | weapon_length(106)|swing_damage(37 , cut) | thrust_damage(26 ,  pierce),imodbits_sword_high ],
["riv_1h_sword", "Rivendell Sword", [("rivendellsword1",0),("scab_rivendell_sword1", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 162 , weight(1.25)|abundance(100)|difficulty(0)|spd_rtng(103) | weapon_length(94)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["riv_riding_sword", "Rivendell Cavalry Sword", [("rivendelllongsword1",0),("scab_rivendelllongsword1", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 162 , weight(1.25)|abundance(100)|difficulty(0)|spd_rtng(103) | weapon_length(104)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["riv_archer_sword", "Rivendell Archer's Sword", [("rivendellshortsword1",0),("scab_rivendell_shortsword1", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 162 , weight(1.25)|abundance(100)|difficulty(0)|spd_rtng(103) | weapon_length(80)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["riv_bow",         "Rivendell Bow", [("rivendellbow",0),("rivendellbow_carry",ixmesh_carry)], itp_type_bow |itp_shop|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 145 , weight(1.75)|difficulty(3)|spd_rtng(82) | shoot_speed(54) | thrust_damage(22 ,  bow_damage),imodbits_bow ],

["riv_spear",         "Rivendell Spear", [("elf_spear_2",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_wooden_parry, itc_staff|itcf_carry_spear,
 175 , weight(2.25)|difficulty(0)|spd_rtng(102) | weapon_length(171)|swing_damage(20 , cut) | thrust_damage(30 ,  pierce),imodbits_polearm ],

	########RIVENDELL ARMORS########
["riv_armor_light",   "Rivendell Armor", [("rivendellrecruitarcher"     ,0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 1259 , weight(18)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(19)|difficulty(7) ,imodbits_armor ],
["riv_armor_light_inf",   "Rivendell Armor", [("rivendellrecruitswordfighter"     ,0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 1259 , weight(18)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(19)|difficulty(7) ,imodbits_armor ],
["riv_armor_archer",  "Rivendell Armor", [("rivendellnormalarcher"      ,0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 1259 , weight(18)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(19)|difficulty(7) ,imodbits_armor ],
["riv_armor_m_archer","Rivendell Armor", [("rivendellelitearcher"       ,0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 1259 , weight(18)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(19)|difficulty(7) ,imodbits_armor ],
["riv_armor_med",     "Rivendell Armor", [("rivendellnormalswordfighter",0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 1259 , weight(18)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(19)|difficulty(7) ,imodbits_armor ],
["riv_armor_heavy",   "Rivendell Armor", [("rivendelleliteswordfighter" ,0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 1259 , weight(18)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(19)|difficulty(7) ,imodbits_armor ],
["riv_armor_h_archer","Rivendell Armor", [("rivendellmountedarcher"     ,0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 1259 , weight(18)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(19)|difficulty(7) ,imodbits_armor ],

	#######RIVENDELL MOUNTS##########
["riv_warhorse","Warhorse", [("rivendell_warhorse01",0)], itp_shop|itp_type_horse, 0, 824,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(38)|horse_maneuver(36)|horse_charge(20),imodbits_horse_basic|imodbit_champion],
["riv_warhorse2","Warhorse", [("rivendell_warhorse02",0)], itp_shop|itp_type_horse, 0, 824,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(38)|horse_maneuver(36)|horse_charge(20),imodbits_horse_basic|imodbit_champion],

 

#####TLD GONDOR ITEMS##########
 
	####ARMORS
["gon_footman", "Gondor Mail Shirt", [("gondor_footman",0)],itp_shop|itp_type_body_armor  |itp_covers_legs ,0,995 , weight(17)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(6)|difficulty(7) ,imodbits_armor ],
["gon_jerkin", "Gondor Jerkin", [("gondor_jerkin",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0, 830 , weight(10)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(8)|difficulty(0) ,imodbits_armor ],
["gon_regular", "Gondor Heavy Mail", [("gondor_regular",0)],itp_shop|itp_type_body_armor  |itp_covers_legs ,0,1295 , weight(17)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(12)|difficulty(7) ,imodbits_armor ],
["gon_bowman", "Gondor Gambeson", [("gondor_bowman",0)], itp_shop|itp_type_body_armor|itp_covers_legs|itp_civilian,0,280 , weight(5)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["gon_archer", "Gondor Gambeson with Cloak", [("gondor_archer",0)], itp_shop|itp_type_body_armor|itp_covers_legs|itp_civilian,0,300 , weight(5)|abundance(100)|head_armor(0)|body_armor(26)|leg_armor(8)|difficulty(0) ,imodbits_cloth  ],
["gon_noble_cloak", "Gondor Noble's Jerkin", [("gondor_noble_cloak",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0, 830 , weight(10)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(8)|difficulty(0) ,imodbits_armor ],
["gon_squire", "Gondor Mail with Cloak", [("gondor_squire",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0,1020 , weight(17)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(9)|difficulty(7) ,imodbits_armor ],
["gon_knight", "Gondor Heavy Mail and Cloak", [("gondor_knight",0)],itp_shop|itp_type_body_armor  |itp_covers_legs ,0,1295 , weight(17)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(12)|difficulty(7) ,imodbits_armor ],
["gon_ranger_cloak", "Gondor Ranger Cloak", [("gondor_ranger_cloak",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0, 830 , weight(10)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(8)|difficulty(0) ,imodbits_armor ],
["gon_ranger_skirt", "Gondor Ranger Skirt", [("gondor_ranger_skirt",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0, 990 , weight(10)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(12)|difficulty(0) ,imodbits_armor ],
["gon_steward_guard", "Gondor Steward Guard Armor", [("gondor_steward_guard",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 1720 , weight(22)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(14)|difficulty(9) ,imodbits_armor ],
["gon_tower_guard", "Gondor Tower Guard Armor", [("gondor_tower_guard",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 1720 , weight(22)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(14)|difficulty(9) ,imodbits_armor],
["gon_tower_knight", "Gondor Tower Knight Armor", [("gon_tower_knight",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 1820 , weight(22)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(15)|difficulty(9) ,imodbits_armor],
["gon_leader_surcoat_cloak", "Gondor Leader's Surcoat", [("gon_leader_surcoat_cloak",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 1342 , weight(17)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(10)|difficulty(7) ,imodbits_armor],

["gondor_ranger_hood", "Green Hood", [("gondor_ranger_hood",0)], 0|itp_shop|itp_type_head_armor,0,60, weight(0.5)|abundance(100)|head_armor(13)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],
["gondor_ranger_hood_mask", "Gondor Ranger Hood", [("gondor_ranger_hood_mask",0)], 0|itp_shop|itp_type_head_armor,0,90, weight(0.6)|abundance(100)|head_armor(15)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth ],

["gondor_light_greaves", "Gondorian Leather Greaves", [("gondor_light_greaves",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0,
 760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor],
["gondor_heavy_greaves", "Gondorian Mailed Greaves", [("gondor_heavy_greaves",0)], itp_shop|itp_type_foot_armor |itp_attach_armature  ,0,
 1746 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(8) ,imodbits_armor],
["gondor_med_greaves", "Gondorian Medium Greaves", [("gondor_medium_greaves",0)],  itp_shop|itp_type_foot_armor |itp_attach_armature,0,
 1153 , weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(28)|difficulty(7) ,imodbits_armor  ],

####Helms

["gondorian_light_helm"      ,"Gondorian_Footman_Helm",[("gondor_footman_helm"         ,0)],itp_shop|itp_type_head_armor,0, 95,weight(1.50)|abundance(100)|head_armor(24)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["gondor_infantry_helm"      ,"Gondor_Infantry_Helm"  ,[("gondor_regular_helm"         ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["gondor_auxila_helm"        ,"Gondorian_Auxilia_Helm",[("gondor_auxila_helm"          ,0)],itp_shop|itp_type_head_armor,0, 60,weight(1.00)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate],
["gondorian_light_helm_b"    ,"Gondorian_Bowman_Helm" ,[("gondor_bowman_helm"          ,0)],itp_shop|itp_type_head_armor,0, 90,weight(1.50)|abundance(100)|head_armor(23)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["gondorian_archer_helm"     ,"Gondorian_Archer_Helm" ,[("gondor_archer_helm"          ,0)],itp_shop|itp_type_head_armor,0,233,weight(1.75)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate],
["tower_archer_helm"         ,"Tower_Guard_Helm"      ,[("gondor_tower_archer_helm"    ,0)],itp_shop|itp_type_head_armor,0,511,weight(2.00)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate],
["gondor_leader_helm"        ,"Gondor High Helmet"    ,[("gondor_leader_helm"          ,0)],itp_shop|itp_type_head_armor,0,910,weight(2.50)|abundance(100)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate],
["tower_guard_helm"          ,"Tower_Guard_Helm"      ,[("gondor_tower_guard_helm"     ,0)],itp_shop|itp_type_head_armor,0,980,weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate],
["gondor_citadel_knight_helm","Citadel_Knight_Helm"   ,[("gondor_citadel_knight_helm"  ,0)],itp_shop|itp_type_head_armor,0,980,weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate],
["gondor_squire_helm"        ,"Gondor Squire Helm"    ,[("gondor_squire_helm"          ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["gondor_knight_helm"        ,"Gondor Knight Helm"    ,[("gondor_knight_helm"          ,0)],itp_shop|itp_type_head_armor,0,638,weight(2.75)|abundance(100)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate],
["gondor_dolamroth_helm"     ,"Dol Amroth Helm,"      ,[("gondor_dolamroth_helm"       ,0)],itp_shop|itp_type_head_armor,0,555,weight(2.50)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate  ],
["swan_knight_helm"          ,"Swan_Knight_Helm,"     ,[("gondor_dolamroth_knight_helm",0)],itp_shop|itp_type_head_armor,0,638,weight(2.75)|abundance(100)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate ],
["gondor_lamedon_helm"       ,"Lamedon_Helm"          ,[("gondor_lamedon_helm"         ,0)],itp_shop|itp_type_head_armor,0,439,weight(2.25)|abundance(100)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["gondor_lamedon_leader_helm","Lamedon High Helmet"   ,[("gondor_lamedon_leader_helm"  ,0)],itp_shop|itp_type_head_armor,0,910,weight(2.50)|abundance(100)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate],
 	##GONDOR MOUNTS########da_warhorse02
["gondor_courser"      ,"Gondor_Courser"           ,[("gondor_horse02"   ,0)],itp_shop|itp_type_horse,0, 323,abundance(70)|hit_points( 90)|body_armor(16)|difficulty(2)|horse_speed(43)|horse_maneuver(37)|horse_charge(11),imodbits_horse_basic|imodbit_champion],
["gondor_hunter"       ,"Gondor_Hunter"            ,[("gondor_horse01"   ,0)],itp_shop|itp_type_horse,0, 434,abundance(60)|hit_points(130)|body_armor(29)|difficulty(3)|horse_speed(40)|horse_maneuver(36)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
["dol_amroth_warhorse" ,"Dol_Amroth_Warhorse"      ,[("da_warhorse02"    ,0)],itp_shop|itp_type_horse,0,1411,abundance(40)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(33)|horse_charge(25),imodbits_horse_basic|imodbit_champion],
["dol_amroth_warhorse2","Dol_Amroth_Heavy_Warhorse",[("da_warhorse01"    ,0)],itp_shop|itp_type_horse,0,1411,abundance(40)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(33)|horse_charge(25),imodbits_horse_basic|imodbit_champion],
["gondor_warhorse"     ,"Warhorse"                 ,[("gondor_warhorse01",0)],itp_shop|itp_type_horse,0, 724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
["gondor_lam_horse"    ,"Warhorse"                 ,[("lam_warhorse01"   ,0)],itp_shop|itp_type_horse,0, 724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
	###BRV
["blackroot_archer", "Blackroot Vale Archer Armor", [("blackroot_archer",0)], itp_shop|itp_type_body_armor |itp_civilian |itp_covers_legs ,0, 321 , weight(6)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["blackroot_bowman", "Blackroot Vale Bowman Armor", [("blackroot_bowman",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0, 730 , weight(10)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(8)|difficulty(0) ,imodbits_armor ],
["blackroot_footman", "Blackroot Vale Footman Armor", [("blackroot_footman",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0, 690 , weight(10)|abundance(100)|head_armor(0)|body_armor(34)|leg_armor(7)|difficulty(0) ,imodbits_armor ],
["blackroot_warrior", "Blackroot Vale Warrior Armor", [("blackroot_warrior",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 795 , weight(17)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(6)|difficulty(7) ,imodbits_armor ],
["blackroot_leader", "Blackroot Vale Leader Armor", [("blackroot_leader",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 820 , weight(17)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(8)|difficulty(7) ,imodbits_armor ],

["blackroot_hood", "Blackroot Hood", [("blackroot_hood",0)], 0|itp_shop|itp_type_head_armor   ,0, 30 , weight(1)|abundance(100)|head_armor(12)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth],
#["blackroot_helm", "Blackroot Helm", [("blackroot_helm",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
      ###DOL AMROTH
["dol_hauberk"        , "Dol Amroth Hauberk", [("dol_hauberk",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 1190 , weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7) ,imodbits_armor ],
["dol_heavy_mail"     , "Dol Amroth Heavy Mail", [("dol_heavy_mail",0)],itp_shop|itp_type_body_armor |itp_civilian |itp_covers_legs ,0, 1370 , weight(18)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(8)|difficulty(7) ,imodbits_cloth],
["dol_padded_coat"    , "Dol Amroth Padded Coat", [("dol_padded_coat",0)],itp_shop|itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 520 , weight(14)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["dol_shirt"          , "Dol Amroth Shirt", [("dol_shirt",0)],  itp_shop|itp_type_body_armor|itp_covers_legs|itp_civilian,0, 260 , weight(5)|abundance(100)|head_armor(0)|body_armor(20)|leg_armor(5)|difficulty(0) ,imodbits_cloth  ],
["dol_very_heavy_mail", "Dol Amroth Very Heavy Mail", [("dol_very_heavy_mail",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 3300 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor  ],
	
["dol_greaves"        , "Dol Amroth Greaves", [("dol_greaves",0)],itp_shop|itp_type_foot_armor |itp_attach_armature  ,0, 1746 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(8) ,imodbits_armor  ],
["dol_shoes"          , "Dol Amroth Light Boots", [("dol_shoes",0)], itp_shop|itp_type_foot_armor |itp_civilian  |itp_attach_armature,0, 75 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(12)|difficulty(0) ,imodbits_cloth ],
     ######LAMEDON
["lamedon_clansman"   , "Lamedon Clansman Armor"       , [("lamedon_clansman"   ,0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 795 , weight(17)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(6)|difficulty(7) ,imodbits_armor ],
["lamedon_footman"    , "Lamedon Footman Armor"        , [("lamedon_footman"    ,0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 810 , weight(17)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(6)|difficulty(7) ,imodbits_armor ],
["lamedon_knight"     , "Lamedon Knight Armor"         , [("lamedon_knight"     ,0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 1820 , weight(22)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(15)|difficulty(9) ,imodbits_armor ],
["lamedon_leader_surcoat_cloak","Lamedon Leader Armor",[("lamedon_leader_surcoat_cloak",0)],itp_shop|itp_type_body_armor|itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["lamedon_warrior"    , "Lamedon Warrior Armor"        , [("lamedon_warrior"    ,0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["lamedon_veteran"    , "Lamedon Veteran Armor"        , [("lamedon_veteran"    ,0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["lamedon_vet_warrior", "Lamedon Veteran Warrior Armor", [("lamedon_vet_warrior",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],

["lamedon_hood", "Lamedon Hood", [("lamedon_hood",0)], 0|itp_type_head_armor |itp_civilian  ,0, 35 , weight(1.25)|abundance(100)|head_armor(14)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#["lamedon_helmet", "Lamedon Helm", [("lamedon_helmet",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
    #####PINNATH GELIN
["pinnath_archer", "Pinnath Gelin Archer Armor", [("pinnath_archer",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["pinnath_footman", "Pinnath Gelin Footman Armor", [("pinnath_footman",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["pinnath_leader", "Pinnath Gelin Leader Armor", [("pinnath_leader",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["pinnath_vet_footman", "Pinnath Gelin Veteran Footman Armor", [("pinnath_vet_footman",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["pinnath_warrior", "Pinnath Gelin Warrior Armor", [("pinnath_warrior",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
#["pinnath_hood", "Pinnath Gelin Hood", [("pinnath_hood",0)], 0|itp_type_head_armor |itp_civilian  ,0, 35 , weight(1.25)|abundance(100)|head_armor(14)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
    ######PEL
["pel_footman", "Pelargir Footman Armor", [("pelargir_footman",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["pel_jerkin", "Pelargir Jerkin", [("pelargir_jerkin",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["pel_leader", "Pelargir Leader Armor", [("pelargir_leader",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["pel_marine", "Pelargir Marine", [("pelargir_marine",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["pelargir_marine_leader", "Pelargir Marine Leader", [("pelargir_marine_leader",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["pelargir_regular", "Pelargir Regular", [("pelargir_regular",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],

["pelargir_hood"        , "Pelargir Hood"      , [("pelargir_hood"        ,0)], itp_shop|itp_type_head_armor|itp_civilian  ,0, 35 , weight(1.25)|abundance(100)|head_armor(14)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["pelargir_helmet_light", "Pelargir Helm"      , [("pelargir_helmet_light",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
["pelargir_helmet_heavy", "Pelargir Heavy Helm", [("pelargir_helmet_heavy",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],

["pelargir_greaves", "Pelargir Greaves", [("pelargir_greaves",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0, 760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],
	######	LOS
["lossarnach_shirt"      ,"Lossarnach Shirt", [("lossarnach_shirt",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["lossarnach_axeman"     ,"Lossarnach Axeman Armor", [("lossarnach_axeman",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["lossarnach_leader"     ,"Lossarnach Leader Armor", [("lossarnach_leader",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["lossarnach_vet_axeman" ,"Lossarnach Veteran Axeman Armor", [("lossarnach_vet_axeman",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["lossarnach_vet_warrior","Lossarnach Veteran Warrior Armor", [("lossarnach_vet_warrior",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["lossarnach_warrior"    ,"Lossarnach Warrior Armor", [("lossarnach_warrior",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
	
["lossarnach_cloth_cap"  ,"Lossarnach Cloth Cap"  , [("lossarnach_cloth_cap"  ,0)], itp_shop|itp_type_head_armor,0,980, weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
["lossarnach_leather_cap","Lossarnach Leather Cap", [("lossarnach_leather_cap",0)], itp_shop|itp_type_head_armor,0,980, weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
["lossarnach_scale_cap"  ,"Lossarnach Scale Cap"  , [("lossarnach_scale_cap"  ,0)], itp_shop|itp_type_head_armor,0,980, weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],

["lossarnach_greaves"    ,"Lossarnach Greaves"    , [("lossarnach_greaves"    ,0)], itp_shop|itp_type_foot_armor|itp_attach_armature,0,760, weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],
	####SHIELDS#####
["gondor_shield_a", "Gondor Square Shield", [("gondor_square_shield" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["gondor_shield_b", "Gondor Kite Shield", [("gondor_point_shield"  ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["gondor_shield_c", "Gondor Tower Shield", [("gondor_tower_shield"  ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["gondor_shield_d", "Gondor Kite Shield", [("gondorian_kite_shield",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["gondor_shield_e", "Gondor Royal Shield", [("denethor_shield",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],

["gon_tab_shield_a", "Heraldic Gondor Round Shield", [("tableau_shield_round",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  96 , weight(2)|hit_points(310)|body_armor(3)|spd_rtng(105)|weapon_length(40),imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_gondor_round_shield_banner", "tableau_gon_shield_round", ":agent_no", ":troop_no")])]],
["gon_tab_shield_b", "Heraldic Gondor Square Shield",   [("tableau_shield_square" ,0)], itp_shop|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield,  210 , weight(4.5)|hit_points(760)|body_armor(2)|spd_rtng(81)|weapon_length(84),imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_gondor_square_shield_banner", "tableau_gon_shield_square", ":agent_no", ":troop_no")])]],
["gon_tab_shield_c", "Heraldic Gondor Kite Shield",   [("tableau_shield_kite" ,0)], itp_shop|itp_type_shield, itcf_carry_kite_shield,  360 , weight(2.5)|hit_points(370)|body_armor(16)|spd_rtng(100)|weapon_length(40),imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_gondor_kite_shield_banner", "tableau_gon_shield_kite", ":agent_no", ":troop_no")])]],
["gon_tab_shield_d", "Heraldic Gondor Tower Shield",   [("tableau_shield_tower" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  332 , weight(3.5)|hit_points(510)|body_armor(9)|spd_rtng(87)|weapon_length(60),imodbits_shield,
 [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_TLD_gondor_tower_shield_banner", "tableau_gon_shield_tower", ":agent_no", ":troop_no")])]],

	#######WEAPONS##########
["amroth_sword_a", "Dol Amroth Sword" , [("DA_sword_a",0),("scab_DA_sword_a", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(88)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["amroth_sword_b", "Dol Amroth Knight Sword", [("DA_sword_b",0),("scab_DA_sword_b", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(100)|swing_damage(28 , cut) | thrust_damage(23 ,  pierce),imodbits_sword_high ],
["gondor_sword","Gondor Infantry Sword"   , [("gondor_inf_new",0),("scab_gondor_inf_new", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(95)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["amroth_bastard", "Dol Amroth Heavy Sword"    , [("DA_bastard",0),("scab_DA_bastard", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 294 , weight(2.25)|difficulty(9)|spd_rtng(98) | weapon_length(109)|swing_damage(37 , cut) | thrust_damage(26 ,  pierce),imodbits_sword_high ],

["gondor_short_sword", "Gondor Short Sword", [("linhir_eket",0),("scab_linhir_eket", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(53)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["pelargir_eket", "Pelargir Short Sword", [("pelargir_eket",0),("scab_pelargir_eket", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(49)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["pelargir_sword", "Pelargir Sword", [("pelargir_sword",0),("scab_pelargir_sword", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(61)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],

["gondor_ranger_sword", "Gondor Ranger Sword", [("gondor_bastard",0),("scab_gondor_ranger", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_back|itcf_show_holster_when_drawn,
 162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(104)|swing_damage(37 , cut) | thrust_damage(26 ,  pierce),imodbits_sword_high ],
#["lamedon_bastard",         "Gondor War Sword", [("gondor_bastard",0),("scab_gondor_bastard", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 #294 , weight(2.25)|difficulty(9)|spd_rtng(98) | weapon_length(101)|swing_damage(37 , cut) | thrust_damage(26 ,  pierce),imodbits_sword_high ],
["gondor_bastard",         "Gondor War Sword", [("gondor_bastard",0),("scab_gondor_bastard", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 294 , weight(2.25)|difficulty(9)|spd_rtng(98) | weapon_length(104)|swing_damage(37 , cut) | thrust_damage(26 ,  pierce),imodbits_sword_high ],
#["gondor_bastard_b",         "Dagmor", [("Dagmor",0),("scab_bastardsw_b", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 #294 , weight(2.25)|difficulty(9)|spd_rtng(98) | weapon_length(101)|swing_damage(37 , cut) | thrust_damage(26 ,  pierce),imodbits_sword_high ],
["gondor_citadel_sword", "Gondor Citadel Sword", [("gondor_citadel",0),("scab_gondor_citadel", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(94)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["gondor_cav_sword", "Gondor Cavalry Sword", [("gondor_riding_sword",0),("scab_gondor_riding_sword", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(100)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],

["gondor_spear",         "Gondorian Spear", [("gondor_spear",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_wooden_parry, itc_staff|itcf_carry_spear,
 175 , weight(2.25)|difficulty(0)|spd_rtng(102) | weapon_length(149)|swing_damage(20 , cut) | thrust_damage(30 ,  pierce),imodbits_polearm ],
["gondor_tower_spear",   "Gondorian Tower Spear", [("gondor_tower_spear",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear,
 375 , weight(2.35)|difficulty(0)|spd_rtng(99) | weapon_length(166)|swing_damage(23 , cut) | thrust_damage(33 ,  pierce),imodbits_polearm ],
["gondor_lance",   "Gondor Lance", [("amroth_lance",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear,
 375 , weight(2.35)|difficulty(0)|spd_rtng(89) | weapon_length(204)|swing_damage(20 , blunt) | thrust_damage(34 ,  pierce),imodbits_polearm ],
["loss_axe", "Lossarnach_Fighting_Axe", [("loss_axe",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
 524 , weight(2.0)|difficulty(9)|spd_rtng(97) | weapon_length(46)|swing_damage(40 , cut) | thrust_damage(0 ,  bow_damage),imodbits_axe ],
["loss_war_axe",   "Lossarnach War Axe", [("loss_axe_2h",0)], itp_type_polearm|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back,
 129 , weight(4.5)|difficulty(8)|spd_rtng(87) | weapon_length(75)|swing_damage(35 , cut) | thrust_damage(0 ,  bow_damage),imodbits_axe ],

["loss_throwing_axes", "Lossarnach Throwing Axes", [("loss_throwing_axe",0)], itp_type_thrown |itp_shop|itp_primary|itp_bonus_against_shield,itcf_throw_axe,
 241 , weight(5)|difficulty(1)|spd_rtng(99) | shoot_speed(20) | thrust_damage(38,cut)|max_ammo(3)|weapon_length(53),imodbits_thrown ],
["gondor_javelin",   "Gondor Javelin", [("gondor_javelin",0),("jarid_quiver", ixmesh_carry)], itp_type_thrown |itp_shop|itp_primary|itp_bonus_against_shield ,itcf_throw_javelin|itcf_carry_quiver_back_right |itcf_show_holster_when_drawn, 
 209 , weight(4)|difficulty(2)|spd_rtng(89) | shoot_speed(27) | thrust_damage(33 ,  pierce)|max_ammo(3)|weapon_length(65),imodbits_thrown ],



###########TLD LORIEN ITEMS##########
	#######LORIEN WEAPONS########
["lorien_bow"    ,"Galadhrim Bow", [("Elfbow",0),("Elfbow_carry",ixmesh_carry)],itp_type_bow|itp_shop|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 728 , weight(1.5)|difficulty(4)|spd_rtng(93) | shoot_speed(58) | thrust_damage(25 ,bow_damage),imodbits_bow ],
["lorien_sword_a", "Lorien Longsword", [("lorien_sword_long",0),("scab_lorien_sword_long", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
394 , weight(1.5)|abundance(100)|difficulty(0)|spd_rtng(107) | weapon_length(87)|swing_damage(30 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["lorien_sword_b", "Lorien Shortsword", [("lorien_sword_short",0),("scab_lorien_sword_short", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
394 , weight(1.5)|abundance(100)|difficulty(0)|spd_rtng(99) | weapon_length(65)|swing_damage(30 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["lorien_sword_c", "Lorien War Sword", [("lorien_sword_hand_and_half",0),("scab_lorien_sword_hand_and_half", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
394 , weight(1.5)|abundance(100)|difficulty(0)|spd_rtng(99) | weapon_length(92)|swing_damage(30 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
	###########LORIEN ARMORS########
#["lorien_armor_a", "Lorien Armor",[("loth_half_leather"       ,0)], itp_shop|itp_type_body_armor|itp_covers_legs|itp_civilian,0,454, weight(12)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["lorien_armor_a", "Lorien Armor",[("lorien_infantry_01"      ,0)], itp_shop|itp_type_body_armor|itp_covers_legs|itp_civilian,0,454, weight(12)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["lorien_armor_b", "Lorien Armor",[("lorien_vetinfantry_01"   ,0)], itp_shop|itp_type_body_armor|itp_covers_legs|itp_civilian,0,454, weight(12)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
#["lorien_armor_d", "Lorien Armor",[("loth_full_leather"       ,0)], itp_shop|itp_type_body_armor|itp_covers_legs|itp_civilian,0,454, weight(12)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
#["lorien_armor_e", "Lorien Armor",[("loth_half_scale"         ,0)], itp_shop|itp_type_body_armor|itp_covers_legs|itp_civilian,0,454, weight(12)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
#["lorien_armor_f", "Lorien Armor",[("loth_full_scale"         ,0)], itp_shop|itp_type_body_armor|itp_covers_legs|itp_civilian,0,454, weight(12)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["lorien_armor_c", "Lorien Armor",[("lorien_royalarcher_01"   ,0)], itp_shop|itp_type_body_armor|itp_covers_legs|itp_civilian,0,454, weight(12)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["lorien_armor_d", "Lorien Armor",[("lorien_royalswordsman_01",0)], itp_shop|itp_type_body_armor|itp_covers_legs|itp_civilian,0,454, weight(12)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["lorien_armor_e", "Lorien Armor",[("lorien_warden_cloak"     ,0)], itp_shop|itp_type_body_armor|itp_covers_legs|itp_civilian,0,454, weight(12)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["lorien_armor_f", "Lorien Armor",[("lorien_eliteinfantry_01" ,0)], itp_shop|itp_type_body_armor|itp_covers_legs|itp_civilian,0,454, weight(12)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],

["lorien_boots", "Lothlorien Boots", [("lorien_boots",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0,760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],
	########LORIEN SHIELDS#####
["lorien_shield_a", "Lorien Shield", [("loth_long_shield_a" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["lorien_shield_b", "Lorien Shield", [("lorien_kite"        ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["lorien_shield_c", "Lorien Shield", [("lorien_kite_small"  ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#["lorien_shield_d", "Lorien Shield", [("lorien_round_shield",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
 
["elven_arrows","Elven_Arrows", [("white_elf_arrow",0),("flying_missile",ixmesh_flying_ammo),("lothlorien_quiver", ixmesh_carry)], itp_type_arrows|itp_shop, itcf_carry_quiver_back_right , 350,weight(3)|abundance(50)|weapon_length(91)|thrust_damage(3,bow_damage)|max_ammo(29),imodbits_missile],
#["loth_arrows","Ghaladrim Arrows", [("white_elf_arrow",0),("flying_missile",ixmesh_flying_ammo),("lothlorien_quiver", ixmesh_carry)], itp_type_arrows|itp_shop, itcf_carry_quiver_back_right , 350,weight(3)|abundance(50)|weapon_length(91)|thrust_damage(3,bow_damage)|max_ammo(29),imodbits_missile],
	########LORIEN HELMS#######
["lorien_helm_a", "Lorien Archer Helm", [("lorienhelmetarcherlow" ,0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
["lorien_helm_b", "Lorien Archer Helm", [("lorienhelmetarcherhigh",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
#["lorien_helm_c", "Lorien Helm"         , [("lorien_helm"           ,0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
["lorien_helm_c", "Lorien Infantry Helm", [("lorienhelmetinf"       ,0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
#["lorien_helm_e", "Lorien Hood"         , [("elven_cloth_hood_blue" ,0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
	#########LORIEN MOUNTS##########
["lorien_warhorse","Lothlorien Warhorse", [("loth_warhorse01",0)], itp_shop|itp_type_horse, 0, 724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],

    #########WARGS#########
#first farg in list: warg_1b (see in module_constants)
#["warg_1a","Warg", [("warg_1A",0)], itp_shop|itp_type_horse, 0, 92,abundance(80)|body_armor(15)|difficulty(2)|horse_speed(31)|horse_maneuver(61)|horse_charge(27),imodbits_horse_basic],
["warg_1b"       ,"Warg"        , [("warg_1B"       ,0)], itp_shop|itp_type_horse, 0, 92,abundance(80)|body_armor(15)|difficulty(2)|horse_speed(31)|horse_maneuver(61)|horse_charge(47),imodbits_horse_basic],
["warg_1c"       ,"Warg"        , [("warg_1C"       ,0)], itp_shop|itp_type_horse, 0, 92,abundance(80)|body_armor(15)|difficulty(2)|horse_speed(31)|horse_maneuver(61)|horse_charge(47),imodbits_horse_basic],
["warg_1d"       ,"Warg"        , [("warg_1D"       ,0)], itp_shop|itp_type_horse, 0, 92,abundance(80)|body_armor(15)|difficulty(2)|horse_speed(31)|horse_maneuver(61)|horse_charge(47),imodbits_horse_basic],
#["wargarmored_1a","Armored_Warg", [("wargArmored_1A",0)], itp_shop|itp_type_horse, 0, 92,abundance(80)|body_armor(15)|difficulty(2)|horse_speed(31)|horse_maneuver(61)|horse_charge(27),imodbits_horse_basic],
["wargarmored_1b","Armored_Warg", [("wargArmored_1B",0)], itp_shop|itp_type_horse, 0, 92,abundance(80)|body_armor(15)|difficulty(2)|horse_speed(31)|horse_maneuver(61)|horse_charge(47),imodbits_horse_basic],
["wargarmored_1c","Armored_Warg", [("wargArmored_1C",0)], itp_shop|itp_type_horse, 0, 92,abundance(80)|body_armor(15)|difficulty(2)|horse_speed(31)|horse_maneuver(61)|horse_charge(47),imodbits_horse_basic],
#["wargarmored_2a","Armored_Warg", [("wargArmored_2A",0)], itp_shop|itp_type_horse, 0, 92,abundance(80)|body_armor(15)|difficulty(2)|horse_speed(31)|horse_maneuver(61)|horse_charge(27),imodbits_horse_basic],
["wargarmored_2b","Armored_Warg", [("wargArmored_2B",0)], itp_shop|itp_type_horse, 0, 92,abundance(80)|body_armor(15)|difficulty(2)|horse_speed(31)|horse_maneuver(61)|horse_charge(47),imodbits_horse_basic],
["wargarmored_2c","Armored_Warg", [("wargArmored_2C",0)], itp_shop|itp_type_horse, 0, 92,abundance(80)|body_armor(15)|difficulty(2)|horse_speed(31)|horse_maneuver(61)|horse_charge(47),imodbits_horse_basic],
["wargarmored_3a","Armored_Warg", [("wargArmored_3A",0)], itp_shop|itp_type_horse, 0, 92,abundance(80)|body_armor(15)|difficulty(2)|horse_speed(31)|horse_maneuver(61)|horse_charge(47),imodbits_horse_basic],
#["wargarmored_3b","Armored_Warg", [("wargArmored_3B",0)], itp_shop|itp_type_horse, 0, 92,abundance(80)|body_armor(15)|difficulty(2)|horse_speed(31)|horse_maneuver(61)|horse_charge(27),imodbits_horse_basic],

#first non WARG item: troll_feet_boots (see in module_constants)

  #TROLL "ITEMS"#########
["troll_feet_boots" , "Troll Feet",[("troll_feet"  ,0)], itp_type_foot_armor ,0, 500 , weight(250)|abundance(0)|difficulty(40)|head_armor(40)|body_armor(55)|leg_armor(55) ,0 ],
["troll_head_helm"  , "Troll Head",[("troll_head"  ,0)], itp_type_head_armor ,0, 500 , weight(250)|abundance(0)|difficulty(30) ,0 ],
["troll_head_helm_b", "Troll Head",[("troll_head_b",0)], itp_type_head_armor ,0, 500 , weight(250)|abundance(0)|difficulty(30) ,0 ],
["troll_head_helm_c", "Troll Head",[("troll_head_c",0)], itp_type_head_armor ,0, 500 , weight(250)|abundance(0)|difficulty(30) ,0 ],

["tree_trunk_club_a","Tree Trunk"       ,[("troll_club"     ,0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_big_weapon, 11 , weight(250)|spd_rtng(87) | weapon_length(186)|swing_damage(75 , blunt) | thrust_damage(75,  blunt),imodbits_none,],
["tree_trunk_club_b","Tree Trunk"       ,[("tree_trunk_club",0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_big_weapon, 11 , weight(250)|spd_rtng(92) | weapon_length(175)|swing_damage(75 , blunt) | thrust_damage(75 ,  blunt),imodbits_none,],
["giant_hammer"     ,"Giant Hammer"     ,[("giant_hammer"   ,0)], itp_type_one_handed_wpn|itp_primary, itc_big_weapon, 11 , weight(250)|spd_rtng(96) | weapon_length(150)|swing_damage(80 , blunt) | thrust_damage(80 ,  blunt),imodbits_none,],
["giant_mace"       ,"Giant Mace"       ,[("giant_mace"     ,0)], itp_type_one_handed_wpn|itp_primary, itc_big_weapon, 11 , weight(250)|spd_rtng(96) | weapon_length(150)|swing_damage(90, blunt) | thrust_damage(90 ,  blunt),imodbits_none,],
["giant_mace_b"     ,"Giant Spiked Mace",[("giant_mace_b"   ,0)], itp_type_one_handed_wpn|itp_primary, itc_big_weapon, 11 , weight(250)|spd_rtng(96) | weapon_length(150)|swing_damage(90 , pierce) | thrust_damage(90 ,  pierce),imodbits_none,],

["olog_feet_boots" , "Olog Hai Feet" ,[("olog_feet"  ,0)],itp_type_foot_armor                 ,0,500, weight(250)|abundance(0)|leg_armor(62)|difficulty(30) ,0 ],
["olog_head_helm"  , "Olog Hai Head" ,[("olog_head"  ,0)],itp_type_head_armor                 ,0,500, weight(250)|abundance(0)|head_armor(62)|difficulty(30) ,0 ],
["olog_head_helm_b", "Olog Hai Head" ,[("olog_head_b",0)],itp_type_head_armor                 ,0,500, weight(250)|abundance(0)|head_armor(62)|difficulty(30) ,0 ],
["olog_head_helm_c", "Olog Hai Head" ,[("olog_head_c",0)],itp_type_head_armor                 ,0,500, weight(250)|abundance(0)|head_armor(62)|difficulty(30) ,0 ],
["olog_body"       , "Olog Hai Armor",[("olog_body"  ,0)],itp_type_body_armor|itp_covers_legs ,0,2010,weight(248)|abundance(0)|body_armor(62)|difficulty(30) ,imodbits_armor],
["olog_body_b"     , "Olog Hai Armor",[("olog_body_b",0)],itp_type_body_armor|itp_covers_legs ,0,2010,weight(248)|abundance(0)|body_armor(62)|difficulty(30) ,imodbits_armor],
["olog_hands"      , "Olog Hai Hands",[("olog_hand_L",0)],itp_type_hand_armor                 ,0, 130,weight(225)|abundance(0)|body_armor(1)|difficulty(30),imodbits_cloth],

########GENERIC ORC ITEMS#####
["orc_chain_greaves", "Chain Greaves", [("orc_chain_greaves_lr",0)],itp_shop|itp_type_foot_armor,0,760, weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],
["orc_coif"         , "Orc Coif"     , [("orc_coif"            ,0)],itp_shop|itp_type_head_armor,0,980, weight(2.3)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
["orc_greaves"      , "Orc Greaves"  , [("orc_chain_greaves_lr",0)],itp_shop|itp_type_foot_armor,0,760, weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(15)|difficulty(0) ,imodbits_armor ],
["orc_ragwrap"      , "Orc Ragwrap"  , [("orc_ragwrap_lr"      ,0)],itp_shop|itp_type_foot_armor,0,10 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(6)|difficulty(0) ,imodbits_armor ],
["orc_furboots"     , "Orc Fur Boots", [("orc_furboot_lr"      ,0)],itp_shop|itp_type_foot_armor,0,10 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(12)|difficulty(0) ,imodbits_armor ],
["orc_furboot_tall" , "Orc Fur Boots", [("orc_furboot_tall"    ,0)],itp_shop|itp_type_foot_armor,0,10 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(12)|difficulty(0) ,imodbits_armor ],

["orc_tribal_a", "Untreated Skin", [("orc_tribal_a",0)], itp_type_body_armor|itp_covers_legs ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(8)|leg_armor(0)|difficulty(0) ,imodbits_armor ],
["orc_tribal_b", "Untreated Skin", [("orc_tribal_b",0)], itp_type_body_armor|itp_covers_legs ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(7)|leg_armor(1)|difficulty(0) ,imodbits_armor ],
["orc_tribal_c", "Untreated Skin", [("orc_tribal_c",0)], itp_type_body_armor|itp_covers_legs ,0, 500 , weight(2)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(3)|difficulty(0) ,imodbits_armor ],

  
####TLD ISENGARD ITEMS##########
	##########ARMORS##########
["isen_orc_armor_a" , "Isengard Orc Armor"  , [("orc_isen_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 31 , weight(1.5)|abundance(100)|head_armor(0)|body_armor(8)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["isen_orc_armor_b" , "Isengard Orc Armor"  , [("orc_isen_b",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 284 , weight(6)|abundance(100)|head_armor(0)|body_armor(19)|leg_armor(7)|difficulty(0) ,imodbits_cloth ],
["isen_orc_armor_c" , "Isengard Orc Armor"  , [("orc_isen_c",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 454 , weight(12)|abundance(100)|head_armor(0)|body_armor(31)|leg_armor(9)|difficulty(0) ,imodbits_cloth ],
["isen_orc_armor_d" , "Isengard Orc Armor"  , [("orc_isen_d",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 1190, weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(10)|difficulty(7) ,imodbits_armor ],
["isen_orc_armor_e" , "Isengard Orc Armor"  , [("orc_isen_e",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0,1290 , weight(21)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(15)|difficulty(7) ,imodbits_armor ],
["isen_orc_armor_f" , "Isengard Orc Armor"  , [("orc_isen_f",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 2410 , weight(25)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(13)|difficulty(8) ,imodbits_armor],
["isen_orc_armor_g" , "Isengard Orc Armor"  , [("orc_isen_g",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 2010 , weight(24)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(8) ,imodbits_armor],
	
["isen_uruk_light_a", "Isengard Light Armor", [("urukhai_isen_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 60 , weight(1.5)|abundance(100)|head_armor(0)|body_armor(9)|leg_armor(7)|difficulty(0) ,imodbits_cloth ],
["isen_uruk_light_b", "Isengard Light Armor", [("urukhai_isen_b",0)], itp_shop|itp_type_body_armor  |itp_covers_legs,0, 384 , weight(10)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["isen_uruk_light_c", "Isengard Light Armor", [("urukhai_isen_c",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 454 , weight(12)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(9)|difficulty(0) ,imodbits_cloth ],
["isen_uruk_light_d", "Isengard Light Armor", [("urukhai_isen_d",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 1190, weight(21)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(10)|difficulty(7) ,imodbits_armor ],
["isen_uruk_light_e", "Isengard Light Armor", [("urukhai_isen_e",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 1690, weight(22)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(10)|difficulty(7) ,imodbits_armor ],

["isen_uruk_heavy_a", "Isengard Heavy Armor", [("urukhai_isen_f",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 2410 , weight(25)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(13)|difficulty(8) ,imodbits_armor],
["isen_uruk_heavy_b", "Isengard Heavy Armor", [("urukhai_isen_g",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 2910 , weight(25)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(17)|difficulty(8) ,imodbits_armor],
["isen_uruk_heavy_c", "Isengard Heavy Armor", [("urukhai_isen_h",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 3410 , weight(25)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(17)|difficulty(8) ,imodbits_armor],
["isen_uruk_heavy_d", "Isengard Tracker Leather", [("urukhai_isen_tracker_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0,690 , weight(14)|abundance(100)|head_armor(0)|body_armor(34)|leg_armor(10)|difficulty(7) ,imodbits_armor ],
["isen_uruk_heavy_e", "Isengard Tracker Leather", [("urukhai_isen_tracker_b",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0,790 , weight(15)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(10)|difficulty(7) ,imodbits_armor ],

["uruk_tracker_boots", "Uruk Tracker Boots", [("uruk_furboot_lr"     ,0)], itp_shop|itp_type_foot_armor,0, 760 , weight(2.2)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(12)|difficulty(0) ,imodbits_armor ],
["uruk_greaves"      , "Uruk Greaves"      , [("uruk_greave_lr"      ,0)], itp_shop|itp_type_foot_armor,0, 760 , weight(4)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(20)|difficulty(0) ,imodbits_armor ],
["uruk_chain_greaves", "Uruk Chain Greaves", [("uruk_chain_greave_lr",0)], itp_shop|itp_type_foot_armor,0, 760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(15)|difficulty(0) ,imodbits_armor ],
["uruk_ragwrap"      , "Uruk Ragwrap"      , [("uruk_ragwrap_lr"     ,0)], itp_shop|itp_type_foot_armor,0, 10 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(6)|difficulty(0) ,imodbits_armor ],

["isengard_surcoat", "Isengard Surcoat", [("uruk_body",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(13)|difficulty(8) ,imodbits_armor ],

	#########HELMS##########
["isen_orc_helm_a" , "Isengard Helm", [("orc_isen_helm_a",0)],itp_shop|itp_type_head_armor   ,0, 121 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate],
["isen_orc_helm_b" , "Isengard Helm", [("orc_isen_helm_b",0)],itp_shop|itp_type_head_armor|itp_fit_to_head ,0, 147 , weight(1.25)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["isen_orc_helm_c" , "Isengard Helm", [("orc_isen_helm_c",0)],itp_shop|itp_type_head_armor,0, 193 , weight(1.5)|abundance(100)|head_armor(33)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["isen_orc_helm_i" , "Isengard Helm", [("orc_helm_i"     ,0)],itp_shop|itp_type_head_armor   ,0, 233 , weight(1.75)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["isen_uruk_helm_a", "Isengard Helm", [("urukhai_helm_a"       ,0)],itp_shop|itp_type_head_armor,0,233,weight(1.8)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["isen_uruk_helm_b", "Isengard Helm", [("urukhai_helm_b"       ,0)],itp_shop|itp_type_head_armor,0,278,weight(2)  |abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["isen_uruk_helm_c", "Isengard Helm", [("urukhai_helm_c"       ,0)],itp_shop|itp_type_head_armor,0,340,weight(2)  |abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["isen_uruk_helm_d", "Isengard Helm", [("urukhai_captainhelm"  ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.3)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["isen_uruk_helm_e", "Isengard Helm", [("urukhai_trackerhelm_a",0)],itp_shop|itp_type_head_armor,0,340,weight(2)  |abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["isen_uruk_helm_f", "Isengard Helm", [("urukhai_trackerhelm_b",0)],itp_shop|itp_type_head_armor,0,411,weight(2)  |abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],

	##############WEAPONS##########
	########Uruk Weapons
["uruk_pike_a",     "Uruk Pike"       , [("isengard_pike",0)], itp_type_polearm|itp_shop|itp_cant_use_on_horseback|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_cutting_spear,
 125 , weight(3.0)|difficulty(0)|spd_rtng(81) | weapon_length(227)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm ],
["uruk_pike_b",     "Uruk Pike"       , [("uruk_skull_spear",0)], itp_type_polearm|itp_shop|itp_cant_use_on_horseback|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_cutting_spear,
 125 , weight(3.0)|difficulty(0)|spd_rtng(81) | weapon_length(176)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm ],
["uruk_falchion_a", "Uruk_Falchion_a" , [("uruk_falchion_a",0)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(72)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["uruk_falchion_b", "Uruk_Falchion_b" , [("uruk_falchion_b",0)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(67)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["uruk_spear",      "Uruk Spear"      , [("uruk_spear",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_staff, 90 , weight(2.5)|difficulty(0)|spd_rtng(96) | weapon_length(168)|swing_damage(20 , blunt) | thrust_damage(27 ,  pierce),imodbits_polearm ],
["uruk_skull_spear","Uruk Skull Spear", [("uruk_skull_spear",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_staff,90 , weight(2.5)|difficulty(0)|spd_rtng(96) | weapon_length(176)|swing_damage(20 , blunt) | thrust_damage(27 ,  pierce),imodbits_polearm ],
["uruk_voulge",     "Uruk_Voulge"     , [("uruk_voulge",0)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 129 , weight(4.5)|difficulty(8)|spd_rtng(87) | weapon_length(108)|swing_damage(35 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["uruk_heavy_axe",  "Uruk_Heavy_Axe"  , [("uruk_heavy_axe",0)], itp_type_polearm|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 110 , weight(4.5)|difficulty(10)|spd_rtng(90) | weapon_length(99)|swing_damage(40 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
     ############Isengard Weapons
["isengard_sword"      ,"Isengard_Sword"      ,[("isengard_sword"      ,0)],itp_shop|itp_type_two_handed_wpn|itp_primary, itc_bastardfalchion|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(75)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["isengard_axe"        ,"Isengard_Axe"        ,[("isengard_axe"        ,0)],itp_shop|itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,294 , weight(2.0)|difficulty(9)|spd_rtng(95) | weapon_length(73)|swing_damage(38 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["isengard_hammer"     ,"Isengard_Hammer"     ,[("isengard_hammer"     ,0)],itp_shop|itp_type_one_handed_wpn|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip,212 , weight(2.5)|difficulty(0)|spd_rtng(98) | weapon_length(61)|swing_damage(24 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["isengard_halberd"    ,"Isengard_Halberd"    ,[("isengard_halberd"    ,0)],itp_shop|itp_type_polearm|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_staff,352 , weight(4.5)|difficulty(0)|spd_rtng(83) | weapon_length(156)|swing_damage(38 , cut) | thrust_damage(21 ,  pierce),imodbits_polearm ],
["isengard_mallet"     ,"Isengard_Mallet"     ,[("isengard_mallet"     ,0)],itp_shop|itp_type_polearm|itp_primary|itp_two_handed|itp_wooden_parry|itp_wooden_attack, itc_nodachi, 101 , weight(7)|difficulty(12)|spd_rtng(82) | weapon_length(83)|swing_damage(35 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["isengard_heavy_axe"  ,"Isengard_Heavy_Axe"  ,[("isengard_heavy_axe"  ,0)],itp_shop|itp_type_polearm|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 129 , weight(4.5)|difficulty(8)|spd_rtng(87) | weapon_length(116)|swing_damage(35 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["isengard_heavy_sword","Isengard_Heavy_Sword",[("isengard_heavy_sword",0)],itp_shop|itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_sword_left_hip,110 , weight(4.5)|difficulty(10)|spd_rtng(90) | weapon_length(102)|swing_damage(40 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["isengard_spear"      ,"Isengard_Spear"      ,[("isengard_spear"      ,0)],itp_shop|itp_type_polearm|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_staff,90 , weight(2.5)|difficulty(0)|spd_rtng(96) | weapon_length(150)|swing_damage(20 , blunt) | thrust_damage(27 ,  pierce),imodbits_polearm ],
["isengard_pike"       ,"Isengard_Pike"       ,[("isengard_pike"       ,0)],itp_shop|itp_type_polearm|itp_spear|itp_primary|itp_cant_use_on_horseback|itp_two_handed|itp_wooden_parry, itc_cutting_spear, 378 , weight(3.5)|difficulty(12)|spd_rtng(92) | weapon_length(226)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm ],
["isengard_large_bow"  ,"Isengard_Large_Bow"  ,[("isengard_large_bow"  ,0),("isengard_large_bow_carry",ixmesh_carry)],itp_shop|itp_type_bow|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 728 , weight(1.5)|difficulty(4)|spd_rtng(93) | shoot_speed(58) | thrust_damage(25 ,pierce),imodbits_bow ],
["isengard_arrow"      ,"Isengard_Arrows"     ,[("isengard_arrow"      ,0),("flying_missile",ixmesh_flying_ammo),("isengard_quiver", ixmesh_carry)], itp_type_arrows|itp_shop, itcf_carry_quiver_back_right , 72,weight(3)|abundance(160)|weapon_length(95)|thrust_damage(1,pierce)|max_ammo(30),imodbits_missile],
      ########shields
["isen_orc_shield_a" , "Isen_Orc_Shield" , [("isen_orc_shield_a" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["isen_orc_shield_b" , "Isen_Orc_Shield" , [("isen_orc_shield_b" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["isen_uruk_shield_b", "Isen_Uruk_Shield", [("isen_uruk_shield_b",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  227 , weight(3.5)|hit_points(600)|body_armor(1)|spd_rtng(76)|weapon_length(81),imodbits_shield ],

########Orc Weapons
["bone_cudgel", "Bone_Cudgel", [("bone_cudgel",0)],itp_type_one_handed_wpn|itp_shop|itp_primary|    itp_no_parry|itp_wooden_attack, itc_scimitar, 11 , weight(2.5)|difficulty(0)|spd_rtng(95) | weapon_length(53)|swing_damage(15 , blunt) | thrust_damage(0 ,  pierce),imodbits_none ],
["skull_club" , "Skull_Club" , [("skull_club" ,0)],itp_type_one_handed_wpn|itp_shop|itp_primary|    itp_no_parry|itp_wooden_attack, itc_scimitar, 11 , weight(2.5)|difficulty(0)|spd_rtng(95) | weapon_length(55)|swing_damage(15 , blunt) | thrust_damage(0 ,  pierce),imodbits_none ],
["wood_club"  , "Wood_Club"  , [("wood_club"  ,0)],itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 11 , weight(2.5)|difficulty(0)|spd_rtng(95) | weapon_length(60)|swing_damage(15 , blunt) | thrust_damage(0 ,  pierce),imodbits_none ],
["orc_club_a" , "Orc_Club"   , [("orc_club_a" ,0)],itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 11 , weight(2.5)|difficulty(0)|spd_rtng(95) | weapon_length(62)|swing_damage(15 , blunt) | thrust_damage(0 ,  pierce),imodbits_none ],
["orc_club_b" , "Orc_Club"   , [("orc_club_b" ,0)],itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 11 , weight(2.5)|difficulty(0)|spd_rtng(95) | weapon_length(65)|swing_damage(15 , blunt) | thrust_damage(0 ,  pierce),imodbits_none ],
["orc_club_c" , "Orc_Club"   , [("orc_club_c" ,0)],itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 11 , weight(2.5)|difficulty(0)|spd_rtng(95) | weapon_length(75)|swing_damage(15 , blunt) | thrust_damage(0 ,  pierce),imodbits_none ],
["orc_club_d" , "Orc_Club"   , [("orc_club_d" ,0)],itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 11 , weight(2.5)|difficulty(0)|spd_rtng(95) | weapon_length(67)|swing_damage(15 , blunt) | thrust_damage(0 ,  pierce),imodbits_none ],
["orc_sledgehammer", "Orc_Sledgehammer", [("orc_sledgehammer",0)],itp_type_polearm|itp_shop|itp_primary|itp_two_handed|itp_no_parry|itp_wooden_attack, itc_nodachi|itcf_carry_back, 101 , weight(7)|difficulty(12)|spd_rtng(82) | weapon_length(75)|swing_damage(35 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["orc_simple_spear", "Orc_Spear"       , [("orc_simple_spear",0)],itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_two_handed|itp_no_parry, itc_staff,90 , weight(2.5)|difficulty(0)|spd_rtng(96) | weapon_length(152)|swing_damage(20 , blunt) | thrust_damage(27 ,  pierce),imodbits_polearm ],
["orc_skull_spear" , "Orc_Skull_Spear" , [("orc_skull_spear" ,0)],itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_staff,90 , weight(2.5)|difficulty(0)|spd_rtng(96) | weapon_length(162)|swing_damage(20 , blunt) | thrust_damage(27 ,  pierce),imodbits_polearm ],
["orc_bill"    ,"Orc_Bill"    , [("orc_bill"    ,0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_staff|itcf_carry_spear, 352 , weight(4.5)|difficulty(0)|spd_rtng(83) | weapon_length(122)|swing_damage(38 , cut) | thrust_damage(21 ,  pierce),imodbits_polearm ],
["orc_slasher" ,"Orc_Slasher" , [("orc_slasher" ,0)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(54)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["orc_falchion","Orc_Falchion", [("orc_falchion",0)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(65)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["orc_scimitar","Orc_Scimitar", [("orc_scimitar",0)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(56)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["orc_sabre"   ,"Orc_Sabre"   , [("orc_sabre"   ,0)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 108 , weight(1.5)|difficulty(0)|spd_rtng(105) | weapon_length(71)|swing_damage(29 , cut) | thrust_damage(0 ,  pierce),imodbits_sword_high ],
["orc_machete" ,"Orc_Machete" , [("orc_machete" ,0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_no_parry, itc_scimitar|itcf_carry_sword_left_hip, 108 , weight(1.5)|difficulty(0)|spd_rtng(105) | weapon_length(55)|swing_damage(29 , cut) | thrust_damage(0 ,  pierce),imodbits_sword_high ],
["orc_axe"     ,"Orc_Axe"     , [("orc_axe"     ,0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 294 , weight(2.0)|difficulty(9)|spd_rtng(95) | weapon_length(61)|swing_damage(38 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["orc_throwing_arrow", "Orc_Darts", [("orc_throwing_arrow",0),("orc_throwing_arrow_bag", ixmesh_carry)], itp_type_thrown |itp_shop|itp_primary|itp_bonus_against_shield ,itcf_throw_javelin|itcf_carry_quiver_back_right |itcf_show_holster_when_drawn, 209 , weight(4)|difficulty(2)|spd_rtng(89) | shoot_speed(27) | thrust_damage(33 ,  pierce)|max_ammo(7)|weapon_length(65),imodbits_thrown ],
["orc_hook_arrow","Orc_Hook_Arrows", [("orc_hook_arrow",0),("flying_missile",ixmesh_flying_ammo),("orc_quiver", ixmesh_carry)], itp_type_arrows|itp_shop, itcf_carry_quiver_back_right , 72,weight(3)|abundance(160)|weapon_length(95)|thrust_damage(1,pierce)|max_ammo(30),imodbits_missile],
["orc_two_handed_axe",  "Orc_Double_Handed_Axe", [("orc_twohanded_axe",0)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 110 , weight(4.5)|difficulty(10)|spd_rtng(90) | weapon_length(84)|swing_damage(40 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["orc_throwing_axes", "Orc_Throwing_Axes", [("orc_throwing_axe",0)], itp_type_thrown |itp_shop|itp_primary|itp_bonus_against_shield,itcf_throw_axe,241, weight(5)|difficulty(1)|spd_rtng(99) | shoot_speed(20) | thrust_damage(38,cut)|max_ammo(7)|weapon_length(53),imodbits_thrown ],
["orc_bow",     "Orc_Bow", [("orc_bow",0),("orc_bow_carry", ixmesh_carry)], itp_type_bow |itp_shop|itp_primary|itp_two_handed ,itcf_shoot_ganstabow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 437 , weight(1.25)|difficulty(3)|spd_rtng(94) | shoot_speed(57) | thrust_damage(23 ,bow_damage),imodbit_cracked | imodbit_bent | imodbit_masterwork ],
# uruk_bow is a orc_bow intended for uruks/humans (vertical shooting position)
["uruk_bow",     "Orc_Bow", [("orc_bow",0),("orc_bow_carry", ixmesh_carry)], itp_type_bow |itp_shop|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 437 , weight(1.25)|difficulty(3)|spd_rtng(94) | shoot_speed(57) | thrust_damage(23 ,bow_damage),imodbit_cracked | imodbit_bent | imodbit_masterwork ],
 
    ####Orc Shields
["orc_shield_a", "Orc_Shield", [("orc_shield_a",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["orc_shield_b", "Orc_Shield", [("orc_shield_b",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["orc_shield_c", "Orc_Shield", [("orc_shield_c",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  227 , weight(3.5)|hit_points(600)|body_armor(1)|spd_rtng(76)|weapon_length(81),imodbits_shield ],
["mordor_orc_shield_a" , "Mordor_Orc_Shield" , [("mordor_orc_shield_a" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["mordor_orc_shield_b" , "Mordor_Orc_Shield" , [("mordor_orc_shield_b" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["mordor_orc_shield_c" , "Mordor_Orc_Shield" , [("mordor_orc_shield_c" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["mordor_orc_shield_d" , "Mordor_Orc_Shield" , [("mordor_orc_shield_d" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["mordor_orc_shield_e" , "Mordor_Orc_Shield" , [("mordor_orc_shield_e" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["mordor_uruk_shield_a", "Mordor_Uruk_Shield", [("mordor_uruk_shield_a",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["mordor_uruk_shield_b", "Mordor_Uruk_Shield", [("mordor_uruk_shield_b",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["mordor_uruk_shield_c", "Mordor_Uruk_Shield", [("mordor_uruk_shield_c",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["mordor_man_shield_a" , "Mordor_Man_Shield" , [("mordor_man_shield_a" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["mordor_man_shield_b" , "Mordor_Man_Shield" , [("mordor_man_shield_b" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["angmar_shield"       , "Angmar_Shield"     , [("angmar_shield"       ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
     #### Generic orc helmets
["orc_helm_a", "Orc Skullcap", [("orc_helm_a",0)],itp_shop|itp_type_head_armor   ,0, 60 , weight(1.0)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate],
["orc_helm_b", "Orc Skullcap", [("orc_helm_b",0)],itp_shop|itp_type_head_armor   ,0, 14 , weight(1)|abundance(100)|head_armor(18)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth],
["orc_helm_c", "Orc Helm"    , [("orc_helm_c",0)],itp_shop|itp_type_head_armor   ,0, 174 , weight(1.25)|abundance(100)|head_armor(31)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate],
["orc_helm_d", "Orc Helm"    , [("orc_helm_d",0)],itp_shop|itp_type_head_armor   ,0, 278 , weight(2)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["orc_helm_e", "Orc Helm"    , [("orc_helm_e",0)],itp_shop|itp_type_head_armor   ,0, 278 , weight(2)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["orc_helm_f", "Orc Helm"    , [("orc_helm_f",0)],itp_shop|itp_type_head_armor   ,0, 233 , weight(1.75)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate],
["orc_helm_g", "Orc Helm"    , [("orc_helm_g",0)],itp_shop|itp_type_head_armor   ,0, 233 , weight(1.75)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate],
["orc_helm_h", "Orc Helm"    , [("orc_helm_h",0)],itp_shop|itp_type_head_armor   ,0, 340 , weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
# orc_helm_i used for isengard
["orc_helm_j", "Orc Helm"    , [("orc_helm_j",0)],itp_shop|itp_type_head_armor   ,0, 174 , weight(1.25)|abundance(100)|head_armor(31)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate],
["orc_helm_k", "Orc Helm"    , [("orc_helm_k",0)],itp_shop|itp_type_head_armor   ,0, 310 , weight(2)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],

 #TLD MORDOR ITEMS##########
	###ORC ARMORS##########
["m_orc_light_a", "Mordor Orc Light Armor", [("orc_mordor_a",0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 31 , weight(1.5)|abundance(100)|head_armor(0)|body_armor(8)|leg_armor(3)|difficulty(0) ,imodbits_cloth ],
["m_orc_light_b", "Mordor Orc Light Armor", [("orc_mordor_b",0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 61 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
["m_orc_light_c", "Mordor Orc Light Armor", [("orc_mordor_c",0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 161 , weight(3)|abundance(100)|head_armor(0)|body_armor(11)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["m_orc_light_d", "Mordor Orc Light Armor", [("orc_mordor_d",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0, 260 , weight(5)|abundance(100)|head_armor(0)|body_armor(20)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
["m_orc_light_e", "Mordor Orc Light Armor", [("orc_mordor_e",0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0,321 , weight(6)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["m_orc_heavy_a", "Mordor Orc Heavy Armor", [("orc_mordor_f",0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 610 , weight(15)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(10)|difficulty(0) ,imodbits_cloth  ],
["m_orc_heavy_b", "Mordor Orc Heavy Armor", [("orc_mordor_g",0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 442 , weight(17)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(8)|difficulty(7) ,imodbits_armor],
["m_orc_heavy_c", "Mordor Orc Heavy Armor", [("orc_mordor_h",0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 690 , weight(14)|abundance(100)|head_armor(0)|body_armor(34)|leg_armor(10)|difficulty(7) ,imodbits_armor ],
["m_orc_heavy_d", "Mordor Orc Heavy Armor", [("orc_mordor_i",0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0,1190 , weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7) ,imodbits_armor  ],
["m_orc_heavy_e", "Mordor Orc Heavy Armor", [("orc_mordor_j",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,1830 , weight(19)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(12)|difficulty(0) ,imodbits_armor],
["m_uruk_light_a", "Mordor Uruk Light Armor", [("uruk_body",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(10)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(8)|difficulty(8) ,imodbits_armor ],
["m_uruk_light_b", "Mordor Uruk Light Armor", [("uruk_mordor_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(10)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(8)|difficulty(8) ,imodbits_armor ],
["m_uruk_heavy_a", "Mordor Uruk Heavy Armor", [("uruk_mordor_a",0)], itp_shop|itp_type_body_armor |itp_covers_legs ,0,61 , weight(3)|abundance(100)|head_armor(0)|body_armor(12)|leg_armor(7)|difficulty(0) ,imodbits_cloth ],
["m_uruk_heavy_b", "Mordor Uruk Heavy Armor", [("uruk_mordor_b",0)], itp_shop|itp_type_body_armor |itp_covers_legs ,0, 107 , weight(3)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["m_uruk_heavy_c", "Mordor Uruk Heavy Armor", [("uruk_mordor_c",0)], itp_shop|itp_type_body_armor |itp_covers_legs ,0,321 , weight(6)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["m_uruk_heavy_d", "Mordor Uruk Heavy Armor", [("uruk_mordor_d",0)], itp_shop|itp_type_body_armor |itp_covers_legs ,0, 520 , weight(14)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["m_uruk_heavy_e", "Mordor Uruk Heavy Armor", [("uruk_mordor_e",0)], itp_shop|itp_type_body_armor |itp_covers_legs ,0, 442 , weight(17)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(8)|difficulty(7) ,imodbits_armor],
["m_uruk_heavy_f", "Mordor Uruk Heavy Armor", [("uruk_mordor_f",0)], itp_shop|itp_type_body_armor |itp_covers_legs ,0, 795 , weight(17)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(6)|difficulty(7) ,imodbits_armor ],
["m_uruk_heavy_g", "Mordor Uruk Heavy Armor", [("uruk_mordor_g",0)], itp_shop|itp_type_body_armor |itp_covers_legs ,0, 863 , weight(18)|abundance(100)|head_armor(0)|body_armor(41)|leg_armor(6)|difficulty(6) ,imodbits_armor],
["m_uruk_heavy_h", "Mordor Uruk Heavy Armor", [("uruk_mordor_h",0)], itp_shop|itp_type_body_armor |itp_covers_legs ,0, 1720 , weight(22)|abundance(100)|head_armor(0)|body_armor(43)|leg_armor(14)|difficulty(7) ,imodbits_armor  ],
["m_uruk_heavy_i", "Mordor Uruk Heavy Armor", [("uruk_mordor_i",0)], itp_shop|itp_type_body_armor |itp_covers_legs,0, 1020 , weight(25)|abundance(100)|head_armor(0)|body_armor(43)|leg_armor(15)|difficulty(9) ,imodbits_armor ],
["m_uruk_heavy_j", "Mordor Uruk Heavy Armor", [("uruk_mordor_j",0)], itp_shop|itp_type_body_armor |itp_covers_legs ,0, 2410 , weight(25)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(13)|difficulty(0) ,imodbits_armor],
["m_uruk_heavy_k", "Mordor Uruk Heavy Armor", [("uruk_mordor_k",0)], itp_shop|itp_type_body_armor |itp_covers_legs ,0, 2710 , weight(23)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(14)|difficulty(8) ,imodbits_armor ],
["m_cap_armor"    , "Mordor Captain Armor"  , [("mordor_captain_armor",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(15)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(18)|difficulty(8) ,imodbits_armor ],
["black_num_armor", "Black Numenorean Armor", [("black_numenor_armor" ,0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(15)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(18)|difficulty(8) ,imodbits_armor ],
["m_armor_a"      , "Mordor Armor"          , [("mordor_armor_a"      ,0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(15)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(18)|difficulty(8) ,imodbits_armor ],
["m_armor_b"      , "Mordor Armor"          , [("mordor_armor_b"      ,0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(15)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(18)|difficulty(8) ,imodbits_armor ],
#WORKING THIS SECTION	
    ######HELMS##########
["uruk_helm_a", "Mordor Uruk Helm", [("uruk_helm_a",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate],
["uruk_helm_b", "Mordor Uruk Helm", [("uruk_helm_b",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate],
["uruk_helm_c", "Mordor Uruk Helm", [("uruk_helm_c",0)], itp_shop|itp_type_head_armor   ,0, 340 , weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["uruk_helm_d", "Mordor Uruk Helm", [("uruk_helm_d",0)], itp_shop|itp_type_head_armor   ,0, 278 , weight(2)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["uruk_helm_e", "Mordor Uruk Helm", [("uruk_helm_e",0)], itp_shop|itp_type_head_armor   ,0, 555 , weight(2.5)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate ],
["uruk_helm_f", "Mordor Uruk Helm", [("uruk_helm_f",0)], itp_shop|itp_type_head_armor   ,0, 505 , weight(2.5)|abundance(100)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate ],
	#####HELMS##########
["mordor_cap_helm", "Mordor Captain Helm", [("mordor_captain_helmet",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
["mordor_helm"    , "Mordor Helm", [("mordor_helmet_a",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
["black_num_helm" , "Black Numenorean Helm", [("black_numenor_helmet",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],

	#######WEAPONS##########
["mordor_sword"    , "Mordor Sword"   ,[("mordor_sword"   ,0)                                       ], itp_type_two_handed_wpn|itp_shop|itp_primary, itc_bastardsword|itcf_carry_sword_back, 294 , weight(2.25)|difficulty(9)|spd_rtng(98) | weapon_length(109)|swing_damage(37 , cut) | thrust_damage(26 ,  pierce),imodbits_sword_high ],
["mordor_longsword", "Sword of Mordor",[("sword_of_mordor",0),("scab_sword_of_mordor", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back|itcf_show_holster_when_drawn, 423 , weight(2.75)|difficulty(10)|spd_rtng(95) | weapon_length(125)|swing_damage(39 , cut) | thrust_damage(31 ,  pierce),imodbits_sword_high ],
    ########MOUNTS
["mordor_warhorse"," Mordor_Warhorse", [("mordor_warhorse01",0)], itp_shop|itp_type_horse, 0, 724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],

 ##TLD MORIA ITEMS##########
#["goblin_king_sword",         "Goblin King's Sword", [("orc_slasher",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back|itcf_show_holster_when_drawn, 423 , weight(2.75)|difficulty(10)|spd_rtng(95) | weapon_length(125)|swing_damage(39 , cut) | thrust_damage(31 ,  pierce),imodbits_sword_high ],
#["moria_sword", "Goblin Slasher", [("orc_slasher",0)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(85)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
	#########ARMORS##########
["moria_armor_a", "Moria Armor", [("orc_moria_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(8)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(6)|difficulty(8) ,imodbits_armor ],
["moria_armor_b", "Moria Armor", [("orc_moria_b",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(8)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(6)|difficulty(8) ,imodbits_armor ],
["moria_armor_c", "Moria Armor", [("orc_moria_c",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(8)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(6)|difficulty(8) ,imodbits_armor ],
["moria_armor_d", "Moria Armor", [("orc_moria_d",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(8)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(6)|difficulty(8) ,imodbits_armor ],
["moria_armor_e", "Moria Armor", [("orc_moria_e",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(8)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(6)|difficulty(8) ,imodbits_armor ],
    #######SHIELDS##########
["moria_orc_shield_a", "Moria_Orc_Shield", [("moria_orc_shield_a",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["moria_orc_shield_b", "Moria_Orc_Shield", [("moria_orc_shield_b",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
["moria_orc_shield_c", "Moria_Orc_Shield", [("moria_orc_shield_c",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],

 ###TLD GUNDABAD ITEMS##########
	#ARMORS##########
["gundabad_armor_a", "Gundabad Orc Armor", [("orc_gunda_a",0)], itp_shop|itp_type_body_armor  |itp_covers_legs, 0, 31 , weight(1.5)|abundance(100)|head_armor(0)|body_armor(8)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["gundabad_armor_b", "Gundabad Orc Armor", [("orc_gunda_b",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 195 , weight(5)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["gundabad_armor_c", "Gundabad Orc Armor", [("orc_gunda_c",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 321 , weight(6)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(7)|difficulty(0) ,imodbits_cloth ],
["gundabad_armor_d", "Gundabad Orc Armor", [("orc_gunda_d",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 381 , weight(6)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["gundabad_armor_e", "Gundabad Orc Armor", [("orc_gunda_e",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 795 , weight(17)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(6)|difficulty(7) ,imodbits_armor ],
	#HELMS##########
["gundabad_helm_a", "Gundabad Helm", [("orc_gunda_cap"     ,0)],itp_shop|itp_type_head_armor   ,0, 6 , weight(1)|abundance(100)|head_armor(11)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth],
["gundabad_helm_b", "Gundabad Helm", [("orc_gunda_helm_a"  ,0)],itp_shop|itp_type_head_armor   ,0, 51 , weight(1)|abundance(100)|head_armor(16)|body_armor(0)|leg_armor(0) ,imodbits_cloth],
["gundabad_helm_c", "Gundabad Helm", [("orc_gunda_helm_b"  ,0)],itp_shop|itp_type_head_armor   ,0, 60 , weight(1.0)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate  ],
["gundabad_helm_d", "Gundabad Helm", [("orc_gunda_helm_c"  ,0)],itp_shop|itp_type_head_armor   ,0, 60 , weight(1.0)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["gundabad_helm_e", "Gundabad Helm", [("orc_wargrider_helm",0)],itp_shop|itp_type_head_armor|itp_fit_to_head ,0, 147 , weight(1.25)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
	#WEAPONS##########
#["gundabad_sabre", "Gundabad Sabre", [("orc_sabre",0),("scab_orc_sabre", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(85)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],

 
####DUNLAND ITEMS##########
 ["dunland_wolfboots", "Dunland_Wolfboots", [("dunland_wolfboots",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0, 153 , weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(11)|difficulty(7) ,imodbits_armor ],
    ##ARMORS########
["dunland_armor_a", "Dunnish Fur Armor", [("dunland_fur_a"    ,0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 83 , weight(7)|abundance(100)|head_armor(0)|body_armor(12)|leg_armor(4)|difficulty(8) ,imodbits_armor ],
["dunland_armor_b", "Dunnish Fur Armor", [("dunland_fur_b"    ,0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 120 , weight(8)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(5)|difficulty(8) ,imodbits_armor ],
["dunland_armor_c", "Dunnish Fur Armor", [("dunland_fur_c"    ,0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 150 , weight(8)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6)|difficulty(8) ,imodbits_armor ],
["dunland_armor_d", "Dunnish Fur Armor", [("dunland_fur_d"    ,0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 234 , weight(8)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(8)|difficulty(8) ,imodbits_armor ],
["dunland_armor_e", "Dunnish Fur Armor", [("dunland_fur_e"    ,0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 443 , weight(9)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(8)|difficulty(8) ,imodbits_armor ],
["dunland_armor_g", "Dunnish Fur Armor", [("dunland_fur_f"    ,0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 512 , weight(9)|abundance(100)|head_armor(0)|body_armor(31)|leg_armor(7)|difficulty(8) ,imodbits_armor ],
["dunland_armor_h", "Dunnish Fur Armor", [("dunland_long_fur" ,0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 235 , weight(8)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(9)|difficulty(8) ,imodbits_armor ],
["dunland_armor_i", "Dunnish_Hauberk"  , [("dunland_hauberk_a",0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 970 , weight(15)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(9)|difficulty(8) ,imodbits_armor ],
["dunland_armor_j", "Dunland_Hauberk"  , [("dunland_hauberk_b",0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 1141 , weight(16)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(12)|difficulty(8) ,imodbits_armor ],
["dunland_armor_k", "Dunland Armor"    , [("dunland_chieftain",0)], itp_shop|itp_type_body_armor|itp_covers_legs ,0, 1250 , weight(8)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(13)|difficulty(8) ,imodbits_armor ],
    #######HELMS##########
["dun_helm_a", "Dunnish Wolf Cap"  , [("dunland_wolfcap"  ,0)], itp_shop|itp_type_head_armor,0, 280 , weight(1)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
["dun_helm_b", "Dunnish Antler Cap", [("dunland_antlercap",0)], itp_shop|itp_type_head_armor,0, 120 , weight(1.25)|abundance(100)|head_armor(21)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
["dun_helm_c", "Dunnish Tall Helm" , [("dunland_helm_a"   ,0)], itp_shop|itp_type_head_armor,0, 383 , weight(1.75)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
["dun_helm_d", "Dunnish Tall Helm" , [("dunland_helm_c"   ,0)], itp_shop|itp_type_head_armor,0, 442 , weight(2.00)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
["dun_helm_e", "Dun Tall War Helm" , [("dunland_helm_b"   ,0)], itp_shop|itp_type_head_armor,0, 565 , weight(2.75)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
#["dun_helm_f", "Dunnish Helm", [("dunland_helm_c",0)], itp_shop|itp_type_head_armor,0, 980 , weight(2.75)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
    #######SHIELDS##########
["dun_shield_a", "Dunnish Shield", [("dun_roundshield"  ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["dun_shield_b", "Dunnish Shield", [("dun_roundshield_b",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#["dun_shield_c", "Dunnish Shield", [("dunland_shield_c",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#["dun_shield_z", "Dunnish Shield", [("dunland_shield_d",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#["dun_shield_e", "Dunnish Shield", [("dunland_shield_e",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#["dun_shield_f", "Dunnish Shield", [("dunland_shield_f_spike",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#["dun_shield_g", "Dunnish Shield", [("dunland_shield_g",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
	#WEAPONS##########
["dun_berserker"     ,"Dunland Chieftain Sword",[("dunland_sword",0),("dunland_sword", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(98)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["dunnish_antler_axe","Dunnish Antler Axe"     ,[("dunland_antleraxe",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 524 , weight(2.0)|difficulty(9)|spd_rtng(97) | weapon_length(73)|swing_damage(40 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["dunnish_war_axe"   ,"Dunnish War Axe"        ,[("dunland_axe_a"    ,0)], itp_type_polearm|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 524 , weight(2.0)|difficulty(9)|spd_rtng(97) | weapon_length(47)|swing_damage(40 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["dunnish_axe"       ,"Dunnish Battle Axe"     ,[("dunland_axe_b"    ,0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 524 , weight(2.0)|difficulty(9)|spd_rtng(97) | weapon_length(34)|swing_damage(40 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["dunnish_pike"      ,"Dunnish Pike"           ,[("dunland_pike"     ,0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear, 125 , weight(3.0)|difficulty(0)|spd_rtng(95) | weapon_length(205)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm ],
["dunland_javelin"   ,"Dunland_Javelins"       ,[("dunland_javelin"  ,0)], itp_type_thrown|itp_shop|itp_primary|itp_bonus_against_shield ,itcf_throw_javelin, 209 , weight(4)|difficulty(2)|spd_rtng(89) | shoot_speed(27) | thrust_damage(63 ,  pierce)|max_ammo(2)|weapon_length(65),imodbits_thrown ],


####TLD ROHAN ITEMS##########
    #########MOUNTS#############
["rohirrim_courser" ,"Rohirrim_Courser"     ,[("rohan_horse01"   ,0)], itp_shop|itp_type_horse, 0, 724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
["rohirrim_hunter"  ,"Rohirrim_Hunter"      ,[("rohan_horse02"   ,0)], itp_shop|itp_type_horse, 0, 724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
["rohirrim_courser2","Rohirrim_Courser"     ,[("rohan_horse03"   ,0)], itp_shop|itp_type_horse, 0, 724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
["rohan_warhorse"   ,"Rohirrim Warhorse"    ,[("rohan_warhorse01",0)], itp_shop|itp_type_horse, 0, 724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
["thengel_warhorse","Thengel_Guard_Warhorse",[("rohan_warhorse02",0)], itp_shop|itp_type_horse, 0, 724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
     ########ARMORS##########
["rohan_armor_a","Rohan Armor", [("L_roh_shirt_M1"                  ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_b","Rohan Armor", [("L_roh_shirt_cape_M2"             ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_c","Rohan Armor", [("L_roh_long_shirt_cape_M4"        ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_d","Rohan Armor", [("LH_roh_hauberk_cape_a_M6"        ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_e","Rohan Armor", [("LH_roh_hauberk_cape_b_M7"        ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_f","Rohan Armor", [("LH_roh_hauberk_cape_c_M5"        ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_g","Rohan Armor", [("M_roh_shirt_cape_b_M2"           ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_h","Rohan Armor", [("M_roh_long_shirt_cape_b_M4"      ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_i","Rohan Armor", [("M_roh_long_shirt_cape_c_M3"      ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_j","Rohan Armor", [("MH_roh_hauberk_leather_cape_a_M6",0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_k","Rohan Armor", [("MH_roh_hauberk_leather_cape_b_M7",0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_l","Rohan Armor", [("MH_roh_hauberk_leather_cape_c_M8",0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_m","Rohan Armor", [("H_roh_scale_cape_a_M10"          ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_n","Rohan Armor", [("H_roh_scale_cape_b_M11"          ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_o","Rohan Armor", [("H_roh_scale_cape_c_M12"          ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_p","Rohan Armor", [("E_roh_hauberk_a_cape_M13"        ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_q","Rohan Armor", [("E_roh_hauberk_b_cape_M14"        ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_r","Rohan Armor", [("E_roh_hauberk_c_cape_M15"        ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(40)|leg_armor(9),imodbits_none],
["rohan_armor_s","Heraldric_Mail",[("VH_heraldic_rohan_armor_M16"   ,0)],itp_type_body_armor|itp_covers_legs ,0,3520 , weight(22)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(16)|difficulty(7) ,imodbits_armor,
[(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heraldic_armor_b", ":agent_no", ":troop_no")])]],
	##HELMS##########
["rohan_helmet_a", "Rohan Helmet", [("rohan_inf_helmet_a"   ,0)], itp_shop|itp_type_head_armor,0,340,weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["rohan_helmet_b", "Rohan Helmet", [("rohan_inf_helmet_b"   ,0)], itp_shop|itp_type_head_armor,0,340,weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["rohan_helmet_c", "Rohan Helmet", [("rohan_archer_helmet_a",0)], itp_shop|itp_type_head_armor,0,340,weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["rohan_helmet_d", "Rohan Helmet", [("rohan_archer_helmet_b",0)], itp_shop|itp_type_head_armor,0,340,weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["rohan_helmet_e", "Rohan Helmet", [("rohan_cav_helmet_a"   ,0)], itp_shop|itp_type_head_armor,0,340,weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["rohan_helmet_f", "Rohan Helmet", [("rohan_cav_helmet_b"   ,0)], itp_shop|itp_type_head_armor,0,340,weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["rohan_helmet_g", "Rohan Helmet", [("rohan_cav_helmet_c"   ,0)], itp_shop|itp_type_head_armor,0,340,weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["rohan_helmet_h", "Rohan Helmet", [("rohan_captain_helmet" ,0)], itp_shop|itp_type_head_armor,0,340,weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
    ##SHIELDS##########
["rohan_shield_a", "Rohan Shield", [("rohan_shield_green"     ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,80, weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield,[(ti_on_init_item, [(store_random_in_range,":p",0,7), (val_add,":p","mesh_rohan_paint_1"),(cur_item_set_tableau_material, "tableau_rohan_plain_shield",":p")])]],
["rohan_shield_b", "Rohan Shield", [("rohan_shield_red"       ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,80, weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield,[(ti_on_init_item, [(store_random_in_range,":p",0,7), (val_add,":p","mesh_rohan_paint_1"),(cur_item_set_tableau_material, "tableau_rohan_plain_shield",":p")])]],
["rohan_shield_c", "Rohan Shield", [("rohan_shield_plain"     ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,80, weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield,[(ti_on_init_item, [(store_random_in_range,":p",0,7), (val_add,":p","mesh_rohan_paint_1"),(cur_item_set_tableau_material, "tableau_rohan_plain_shield",":p")])]],
["rohan_shield_d", "Rohan Shield", [("rohan_shield_green_boss",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,80, weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield,[(ti_on_init_item, [(store_random_in_range,":p",4,7), (val_add,":p","mesh_rohan_paint_1"),(cur_item_set_tableau_material, "tableau_rohan_boss_shield" ,":p")])]],
["rohan_shield_e", "Rohan Shield", [("rohan_shield_red_boss"  ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,80, weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield,[(ti_on_init_item, [(store_random_in_range,":p",4,7), (val_add,":p","mesh_rohan_paint_1"),(cur_item_set_tableau_material, "tableau_rohan_boss_shield" ,":p")])]],
["rohan_shield_f", "Rohan Shield", [("rohan_shield_plain_boss",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,80, weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield,[(ti_on_init_item, [(store_random_in_range,":p",4,7), (val_add,":p","mesh_rohan_paint_1"),(cur_item_set_tableau_material, "tableau_rohan_boss_shield" ,":p")])]],
["rohan_shield_g", "Rohan Royal Shield",[("rohan_shield_royal",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,80, weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield,[(ti_on_init_item, [(store_random_in_range,":p",4,7), (val_add,":p","mesh_rohan_paint_1"),(cur_item_set_tableau_material, "tableau_rohan_boss_shield" ,":p")])]],
#["rohan_shield_h", "Rohan Shield", [("rohanshield_iron"   ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
#["rohan_shield_i","Rohan Shield",[("rohanshield_noble_gilt",0)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
#["rohan_shield_j","Rohan Shield",[("rohanshield_oval_gilt",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
#["rohan_shield_k", "Rohan Noble Shield", [("rohanshield_noble_a",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
#["rohan_shield_l", "Rohan Noble Shield", [("rohanshield_noble_b",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield ],
     ##FOOTGEAR##########
["rohan_light_greaves" , "Rohan_Light_Greaves" , [("M_rohan_light_greaves",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0, 1153 , weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(28)|difficulty(7) ,imodbits_armor ],
["rohirrim_war_greaves", "Rohirrim_War_Greaves", [("H_rohan_scale_greaves",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0, 1153 , weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(28)|difficulty(7) ,imodbits_armor ],
["rohan_shoes"         , "Leather_Shoes"       , [("L_rohan_shoes"        ,0)], itp_shop|itp_type_foot_armor |itp_civilian  |itp_attach_armature,0, 34 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
     ##WEAPONS##########
["rohan_cav_sword","Rohan Riding Sword", [("rohan_sword_a",0),("scab_rohan_sword_a", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 394 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(95)|swing_damage(31 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["rohan_inf_sword","Rohan Sword"       , [("rohan_sword_b",0),("scab_rohan_sword_b", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 280 , weight(1.25)|difficulty(0)|spd_rtng(100) | weapon_length(95)|swing_damage(29 , cut) | thrust_damage(22 ,  pierce),imodbits_sword_high ],
["rohan_spear"    ,"Rohan Spear"       , [("rohan_spear",0)                                       ], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_rohan_spear, 189 , weight(2.5)|difficulty(0)|spd_rtng(92) | weapon_length(172)|swing_damage(16 , blunt) | thrust_damage(27 ,  pierce),imodbits_polearm ],
["rohan_sword_c"  ,"Rohan_Sword"       , [("rohan_sword_c",0),("scab_rohan_sword_c", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 280 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(96)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["rohirrim_short_axe"      , "Rohirrim_Short_Axe"      , [("rohan_1haxe",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 524 , weight(2.0)|difficulty(9)|spd_rtng(97) | weapon_length(50)|swing_damage(40,cut)|thrust_damage(0,pierce),imodbits_axe ],
["rohirrim_long_hafted_axe", "Rohirrim_Long_Hafted_Axe", [("rohan_2haxe",0)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 524 , weight(2.0)|difficulty(9)|spd_rtng(97) | weapon_length(53)|swing_damage(40,cut)|thrust_damage(0,pierce),imodbits_axe ],
["heavy_throwing_spear",  "Heavy_Throwing_Spear", [("rohan_throwing_spear",0)], itp_type_thrown |itp_shop|itp_primary|itp_bonus_against_shield ,itcf_throw_javelin, 209 , weight(4)|difficulty(2)|spd_rtng(89) | shoot_speed(27) | thrust_damage(63 ,  pierce)|max_ammo(2)|weapon_length(65),imodbits_thrown ],
["rohirrim_throwing_axe", "Rohirrim_Throwing_Axe", [("rohan_throwing_axe",0)], itp_type_thrown |itp_shop|itp_primary|itp_bonus_against_shield,itcf_throw_axe,241, weight(5)|difficulty(1)|spd_rtng(99) | shoot_speed(20) | thrust_damage(38,cut)|max_ammo(7)|weapon_length(53),imodbits_thrown ],

 ###TLD WOODELF ITEMS##########
	#ARMORS##########
["mirkwood_light_scale","Light Woodelf Scale"      ,[("mirkwood_light_scale"         ,0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["mirkwood_armor_a"    ,"Light Leather"            ,[("mirkwood_leather"             ,0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["mirkwood_armor_b","Light Quilted and Scale Armor",[("mirkwood_scalequilted_01"     ,0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["mirkwood_armor_c"    ,"Light Scale over Mail"    ,[("mirkwood_scaleovermaille_01"  ,0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["mirkwood_armor_d"    ,"Light Quilted Surcoat"    ,[("mirkwood_quiltedsurcoat_01"   ,0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
["mirkwood_armor_e"    ,"Light Mail and Surcoat"   ,[("mirkwood_maillewithsurcoat_01",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
#["mirkwood_armor_f", "Light Archer's Tabard", [("mirkwood_archer_cloth",0)], itp_shop|itp_type_body_armor  |itp_covers_legs ,0, 500 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8) ,imodbits_armor ],
	#WEAPONS##########
["mirkwood_great_spear","Mirkwood Great Spear",[("mirkwood_great_spear_large",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_wooden_parry, itc_staff|itcf_carry_spear, 90 , weight(2.5)|difficulty(0)|spd_rtng(101) | weapon_length(148)|swing_damage(20 , blunt) | thrust_damage(27 ,  pierce),imodbits_polearm ],
["mirkwood_war_spear"  ,"Mirkwood War Spear"  ,[("mirkwood_war_spear",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear, 290 , weight(2.5)|difficulty(0)|spd_rtng(99) | weapon_length(150)|swing_damage(20 , blunt) | thrust_damage(31 ,  pierce),imodbits_polearm ],
["mirkwood_short_spear","Mirkwood Spear"      ,[("mirkwood_short_spear",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear, 90 , weight(2.5)|difficulty(0)|spd_rtng(96) | weapon_length(117)|swing_damage(20 , blunt) | thrust_damage(27 ,  pierce),imodbits_polearm ],
["mirkwood_bow"        ,"Mirkwood Bow"        ,[("mirkwood_bow",0),("mirkwood_bow_carry",ixmesh_carry)],itp_type_bow|itp_shop|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 728 , weight(1.5)|difficulty(4)|spd_rtng(93) | shoot_speed(58) | thrust_damage(25 ,bow_damage),imodbits_bow ],
["mirkwood_knife"      ,"Mirkwood White Knife",[("mirkwood_white_knife",0),("scab_mirkwood_white_knife",ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_no_parry, itc_dagger|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn, 13 , weight(0.75)|difficulty(0)|spd_rtng(108) | weapon_length(51)|swing_damage(24 , cut) | thrust_damage(17 ,  pierce),imodbits_sword ],
["woodelf_arrows"      ,"Woodelf_Arrows"      ,[("mirkwood_arrow",0),("flying_missile",ixmesh_flying_ammo),("mirkwood_quiver_new", ixmesh_carry)], itp_type_arrows|itp_shop, itcf_carry_quiver_back_right , 350,weight(3)|abundance(50)|weapon_length(91)|thrust_damage(3,bow_damage)|max_ammo(29),imodbits_missile],
#["mirkwood_arrows","Mirkwood Arrows", [("green_elf_arrow",0),("flying_missile",ixmesh_flying_ammo),("mirkwood_quiver", ixmesh_carry)], itp_type_arrows|itp_shop, itcf_carry_quiver_back_right , 350,weight(3)|abundance(50)|weapon_length(91)|thrust_damage(3,bow_damage)|max_ammo(29),imodbits_missile],
#["elf_war_spear", "Elf War Spear", [("elf_spear_1",0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear,
 #390 , weight(2.5)|difficulty(0)|spd_rtng(97) | weapon_length(185)|swing_damage(20 , cut) | thrust_damage(27 ,  pierce),imodbits_polearm ],
["mirkwood_sword","Mirkwood Sword", [("mirkwood_longsword",0),("scab_mirkwood_longsword", ixmesh_carry)],  itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(92)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
	#SHIELDS##########
["mirkwood_spear_shield_a", "Mirkwood Spearman Shield", [("mirkwood_spear_shield",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["mirkwood_spear_shield_b", "Mirkwood War Shield", [("mirkwood_med_shield"  ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["mirkwood_spear_shield_c", "Mirkwood Swordsman Shield", [("mirkwood_royal_round" ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#["mirkwood_spear_shield_d", "Mirkwood Spearman Shield", [("elven_oval_a"         ,0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
	#HELMETS##########
["mirkwood_helm_a", "Mirkwood Archer Helm", [("mirkwood_helm",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["mirkwood_helm_b", "Mirkwood Helm", [("mirkwoodnormalspearman",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["mirkwood_helm_c", "Mirkwood Helm", [("mirkwoodroyalspearman",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["mirkwood_helm_d", "Mirkwood Royal Archer Helm", [("mirkwoodroyalarcher",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
	####BOOTS
["mirkwood_boots", "Mirkwood boots", [("mirkwood_boots",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0, 760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],
["mirkwood_leather_greaves", "Mirkwood_Leather_Greaves", [("lthr_greaves",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0, 760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],

#####TLD HARAD ITEMS##########
	############ARMOR##########
			#########HARONDOR##
["harad_armor_b", "Harondor Hauberk"     ,[("harad_hauberk"   ,0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["harad_armor_c", "Harondor Padded Armor",[("harad_padded"   ,0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#needs texturing
["harad_armor_d", "Harondor Tunic"       ,[("harondor_tunic"   ,0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#need meshes
["harad_armor_f", "Karka Armor"          ,[("harad_heavy",0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["harad_armor_g", "Kiloka Armor"         ,[("harad_padded"    ,0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
			###########HARAD##
["harad_armor_a", "Harad Swordsman Armor" ,[("harad_heavy"     ,0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#need 1 mesh
["harad_armor_e", "Harad Cuirass Armor",[("harad_hauberk",0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["harad_armor_h", "Maranka Armor"  , [("black_snake_armor",0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#need 1 mesh
["harad_armor_i", "Harad Padded Armor" , [("harad_padded",0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["harad_armor_m", "Serjala Armor"   , [("lion_guard",0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#waiting for mesh from giles...
["harad_armor_n", "Varujala Armor", [("harad_padded",0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#need 1 mesh
["harad_armor_o", "Harasjala Armor"  , [("harad_lamellar",0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#needs texturing
["harad_armor_p", "Harad Tunic"        , [("harad_tunic",0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
	###########FAR HARAD##
#need meshes
["harad_armor_j", "Far Harad Tribesman", [("harad_padded",0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["harad_armor_k", "Far Harad Champion" , [("far_harad_champion",0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["harad_armor_l", "Parsanah Armor", [("harad_padded",0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
   ###########HELMS##########
			#HARONDOR
["harad_helm_a"    , "Kiloka Helm"  , [("harad_dragon_helm" ,0)],itp_shop|itp_type_head_armor,0,479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
   #need meshes for these 2
["harad_cap_b","Harondor Embroidered Cap",[("harad_heavy_inf_helm",0)],itp_shop|itp_type_head_armor,0,479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["harad_cap_c","Harondor Leather Cap",[("harad_cav_helm_b",0)],itp_shop|itp_type_head_armor,0,479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["harad_helm_e"    , "Harondor Cavalry Helm" , [("harad_cav_helm_b"   ,0)],itp_shop|itp_type_head_armor,0,479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["harad_helm_c"  ,"Harondor Cavalry Helm",[("harad_cav_helm_a",0)],itp_shop|itp_type_head_armor,0,479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["harad_helm_i"    , "Maranka Helm" , [("black_snake_helm"   ,0)],itp_shop|itp_type_head_armor,0,479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
			#GREAT HARAD
["harad_helm_b"    , "Great Harad Helmet"     , [("harad_finhelm"     ,0)],itp_shop|itp_type_head_armor,0,479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["harad_helm_j", "Great Harad Helmet" , [("harad_heavy_inf_helm"  ,0)],itp_shop|itp_type_head_armor,0,479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["harad_helm_k", "Great Harad Helmet" , [("harad_wavy_helm"  ,0)],itp_shop|itp_type_head_armor,0,479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
  #waiting for mesh from giles...
["harad_helm_g"    , "Leopard Guard Helm" , [("harad_wavy_helm"   ,0)],itp_shop|itp_type_head_armor,0,479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
  #need meshes for these 3
["harad_helm_h"    , "Eagle Guard Helm"   , [("harad_wavy_helm"   ,0)],itp_shop|itp_type_head_armor,0,479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["harad_cap_a"     , "Harad Cloth Cap"  , [("harad_heavy_inf_helm",0)],itp_shop|itp_type_head_armor,0,479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["harad_cap_d"     , "Harad Cloth Covered Helmet"  , [("black_snake_helm",0)],itp_shop|itp_type_head_armor,0,479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["harad_helm_f"    , "Lion Guard Helm"    , [("lion_helm"   ,0)],itp_shop|itp_type_head_armor,0,479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
			#FAR HARAD - need mesh
["harad_panther_guard"    , "Panther Guard Cap"    , [("harad_wavy_helm"   ,0)],itp_shop|itp_type_head_armor,0,479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
	##########WEAPONS##########
["harad_khopesh",    "Harad Khopesh"       ,[("harad_khopesh",0)],        itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(80)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["black_snake_sword","Harad Heavy Falchion",[("black_snake_sword",0)],  itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(71)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["harad_heavy_sword","Harad Heavy Sword"   ,[("harad_heavy_sword",0)],   itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(80)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["harondor_a",       "Harad Scimitar"      ,[("horandor_a",0)],             itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(90)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["skirmisher_sword", "Harad Skirmisher Sword",[("skirmisher_sword",0)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(69)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["harad_sabre",      "Harad Sabre"         ,[("harad_sabre",0)],              itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(92)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
#["harad_mace",       "Harad Mace"          ,[("winged_mace",0)],                itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(73)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["harad_club",       "Harad Club"          ,[("mace_e",0)],                     itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(73)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
#["harad_axe",        "Harad Axe"           ,[("one_handed_war_axe_b",0)],         itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(73)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["far_harad_mace",   "Far Harad Mace"      ,[("harad_mace",0)],        itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(73)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["harad_2h_mace",    "Far Harad Two Handed Mace",[("iron_hammer",0)],        itp_type_polearm|itp_shop|itp_two_handed|itp_primary|itp_wooden_parry, itc_scimitar, 7 , weight(2)|difficulty(0)|spd_rtng(100) | weapon_length(55)|swing_damage(14 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["harad_dagger"     ,"Harad Knife"         ,[("harad_dagger",0),("scab_dagger",ixmesh_carry),("dagger_b",imodbits_good),("dagger_b_scabbard",ixmesh_carry|imodbits_good)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_no_parry, itc_dagger|itcf_carry_dagger_front_left|itcf_show_holster_when_drawn, 17 , weight(0.75)|difficulty(0)|spd_rtng(112) | weapon_length(47)|swing_damage(22 , cut) | thrust_damage(19 ,  pierce),imodbits_sword_high ],
#["harad_heavy_javelin","Harad Heavy Javelin",[("jarid_new",0),("jarid_quiver", ixmesh_carry)], itp_type_thrown |itp_shop|itp_primary|itp_bonus_against_shield ,itcf_throw_javelin|itcf_carry_quiver_back_right |itcf_show_holster_when_drawn, 209 , weight(4)|difficulty(2)|spd_rtng(89) | shoot_speed(27) | thrust_damage(33 ,  pierce)|max_ammo(1)|weapon_length(65),imodbits_thrown ],
#["harad_javelin"    ,"Nomad Javelin"       ,[("javelin",0),("javelins_quiver", ixmesh_carry)], itp_type_thrown |itp_shop|itp_primary|itp_bonus_against_shield ,itcf_throw_javelin|itcf_carry_quiver_back_right |itcf_show_holster_when_drawn, 75 , weight(5)|difficulty(1)|spd_rtng(91) | shoot_speed(28) | thrust_damage(28 ,  pierce)|max_ammo(3)|weapon_length(75),imodbits_thrown ],

["harad_bow",         "Harad Curved Bow", [("harad_bow",0),("khergit_bow_case", ixmesh_carry)], itp_type_bow |itp_shop|itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 269 , weight(1.25)|difficulty(3)|spd_rtng(95) | shoot_speed(56) | thrust_damage(21 ,bow_damage),imodbits_bow ],
["karka_bow",         "Karka Bow", [("khergit_bow",0),("khergit_bow_case", ixmesh_carry)], itp_type_bow |itp_shop|itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 269 , weight(1.25)|difficulty(3)|spd_rtng(95) | shoot_speed(56) | thrust_damage(21 ,bow_damage),imodbits_bow ],
["eagle_bow",         "Leopard Guard Bow", [("lg_bow",0),("khergit_bow_case", ixmesh_carry)], itp_type_bow |itp_shop|itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 269 , weight(1.25)|difficulty(3)|spd_rtng(95) | shoot_speed(56) | thrust_damage(21 ,bow_damage),imodbits_bow ],

["harad_spear_a", "Harad Spear", [("harad_short_spear" ,0)], itp_type_polearm|itp_shop|itp_cant_use_on_horseback|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear, 125 , weight(3.0)|difficulty(0)|spd_rtng(81) | weapon_length(245)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm ],
["harad_spear_b", "Harad Spear", [("harad_long_spear",0)], itp_type_polearm|itp_shop|itp_cant_use_on_horseback|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear, 125 , weight(3.0)|difficulty(0)|spd_rtng(81) | weapon_length(245)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm ],
["eagle_guard_spear", "Harasjala Polearm", [("eagle_guard_spear",0)], itp_type_polearm|itp_shop|itp_cant_use_on_horseback|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear, 125 , weight(3.0)|difficulty(0)|spd_rtng(81) | weapon_length(245)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm ],
	###########SHIELDS##########
["harad_shield_a"   ,"Harad Snake Shield", [("great_harad_long_shield_a",0)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["harad_shield_b"        ,"Harad Buckler"     , [("great_harad_long_shield_b"     ,0)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["harad_shield_c"  ,"Harad Shield", [("great_harad_long_shield_c"     ,0)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["harad_shield_d","Harad Shield", [("great_harad_long_shield_d"     ,0)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["harad_shield_e","Harad Shield", [("great_harad_long_shield_e"     ,0)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],

["harondor_shield_a"    ,"Harondor Shield", [("harad_shield_a"     ,0)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["harondor_shield_b"    ,"Harondor Shield", [("harad_shield_b"     ,0)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#["harondor_buckler"     ,"Harondor Buckler"  , [("harad_yellow_shield",0)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],

["far_harad_shield_a"     ,"Far Harad Shield", [("harad_tribal_a"     ,0)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["far_harad_shield_b"   ,"Far Harad Shield", [("harad_tribal_b"     ,0)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["far_harad_shield_c"   ,"Far Harad Shield", [("harad_yellow_shield",0)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
	############BOOTS##########
["harad_greaves", "Harad Greaves", [("harad_boots",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0, 760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],
["harad_desert_boots", "Harad Desert Boots", [("desert_boots",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0, 760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],
["harad_boots", "Harad Boots", [("black_snake_boots",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0, 760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],
	############MOUNTS##########
["harad_light_horse","horse", [("saddle_horse",0)], itp_shop|itp_type_horse, 0, 724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
["harad_horse"      ,"horse", [("harad_horse01",0)], itp_shop|itp_type_horse, 0, 724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
["harad_warhorse"   ,"horse", [("harad_horse02"      ,0)], itp_shop|itp_type_horse, 0, 724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
#["camel","Far Harad Camel", [("camel",0)], itp_shop|itp_type_horse, 0, 92,abundance(80)|body_armor(15)|difficulty(2)|horse_speed(22)|horse_maneuver(32)|horse_charge(27),imodbits_horse_basic],

#####TLD KHAND ITEMS##########
	###HELMS###########
["khand_helmet_a1", "Khand Helm", [("Khand_Helmet_A1",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_a2", "Khand Helm", [("Khand_Helmet_A2",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_a3", "Khand Helm", [("Khand_Helmet_A3",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_b1", "Khand Helm", [("Khand_Helmet_B1",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_b2", "Khand Helm", [("Khand_Helmet_B2",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_b3", "Khand Helm", [("Khand_Helmet_B3",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_b4", "Khand Helm", [("Khand_Helmet_B4",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
#["khand_helmet_c1", "Khand Helm", [("Khand_Helmet_C1",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
#["khand_helmet_c2", "Khand Helm", [("Khand_Helmet_C2",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_c3", "Khand Helm", [("Khand_Helmet_C3",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_c4", "Khand Helm", [("Khand_Helmet_C4",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
#["khand_helmet_c5", "Khand Helm", [("Khand_Helmet_C5",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_d1", "Khand Helm", [("Khand_Helmet_D1",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_d2", "Khand Helm", [("Khand_Helmet_D2",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_d3", "Khand Helm", [("Khand_Helmet_D3",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_e1", "Khand Helm", [("Khand_Helmet_E1",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_e2", "Khand Helm", [("Khand_Helmet_E2",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_e3", "Khand Helm", [("Khand_Helmet_E3",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_e4", "Khand Helm", [("Khand_Helmet_E4",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_f1", "Khand Helm", [("Khand_Helmet_F1",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
#["khand_helmet_f2", "Khand Helm", [("Khand_Helmet_F2",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
#["khand_helmet_f3", "Khand Helm", [("Khand_Helmet_F3",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
#["khand_helmet_f4", "Khand Helm", [("Khand_Helmet_F4",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_mask1", "Khand Helm", [("Khand_Helmet_Mask1",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["khand_helmet_mask2", "Khand Helm", [("Khand_Helmet_Mask2",0)], itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
	#########ARMOR##########
["khand_foot_lam_a", "Khand Armor", [("khand_foot_lam_a",0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65,weight(7)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(0) ,imodbits_cloth ],
["khand_foot_lam_b", "Khand Armor", [("khand_foot_lam_b",0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65,weight(7)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(0) ,imodbits_cloth ],
["khand_foot_lam_c", "Khand Armor", [("khand_foot_lam_c",0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65,weight(7)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(0) ,imodbits_cloth ],
["khand_heavy_lam" , "Khand Armor", [("khand_heavy_lam" ,0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65,weight(7)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(0) ,imodbits_cloth ],
["khand_light_lam" , "Khand Armor", [("khand_light_lam" ,0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65,weight(7)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(0) ,imodbits_cloth ],
#["khand_med_lam_a", "Khand Armor", [("khand_med_lam_a" ,0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65,weight(7)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(0) ,imodbits_cloth ],
["khand_med_lam_b" , "Khand Armor", [("khand_med_lam_b" ,0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65,weight(7)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(0) ,imodbits_cloth ],
["khand_med_lam_c" , "Khand Armor", [("khand_med_lam_c" ,0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65,weight(7)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(0) ,imodbits_cloth ],
["khand_med_lam_d" , "Khand Armor", [("khand_med_lam_d" ,0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65,weight(7)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(0) ,imodbits_cloth ],
["khand_noble_lam" , "Khand Armor", [("khand_noble_lam" ,0)],itp_shop|itp_type_body_armor|itp_covers_legs,0,65,weight(7)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(0) ,imodbits_cloth ],

["variag_greaves", "Variag_Greaves", [("variag_boots",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0, 760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],
	#########WEAPONS##########
["khand_axe_great"  ,"Khand Great Axe"  ,[("Khand_Weapon_Axe_Great"  ,0)],itp_type_polearm|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 129 , weight(4.5)|difficulty(8)|spd_rtng(87) | weapon_length(109)|swing_damage(35 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["khand_axe_winged" ,"Khand Winged Axe" ,[("Khand_Weapon_Axe_Winged" ,0)],itp_type_polearm|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 129 , weight(4.5)|difficulty(8)|spd_rtng(87) | weapon_length(96)|swing_damage(35 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["khand_glaive"    ,"Khand Glaive"     ,[("Khand_Weapon_Glaive"     ,0)],itp_type_polearm       |itp_shop|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_staff|itcf_carry_spear, 352 , weight(4.5)|difficulty(0)|spd_rtng(88) | weapon_length(183)|swing_damage(38 , cut) | thrust_damage(21 ,  pierce),imodbits_polearm ],
["khand_halberd"    ,"Khand Halberd"    ,[("Khand_Weapon_Halberd"    ,0)],itp_type_polearm       |itp_shop|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_staff|itcf_carry_spear, 352 , weight(4.5)|difficulty(0)|spd_rtng(88) | weapon_length(164)|swing_damage(38 , cut) | thrust_damage(21 ,  pierce),imodbits_polearm ],
["khand_trident"    ,"Khand Trident"    ,[("Khand_Weapon_Trident"    ,0)],itp_type_polearm       |itp_shop|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_staff|itcf_carry_spear, 352 , weight(4.5)|difficulty(0)|spd_rtng(88) | weapon_length(164)|swing_damage(38 , cut) | thrust_damage(21 ,  pierce),imodbits_polearm ],
["khand_voulge"     ,"Khand Voulge"     ,[("Khand_Weapon_Voulge"     ,0)],itp_type_polearm       |itp_shop|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_staff|itcf_carry_spear, 352 , weight(4.5)|difficulty(0)|spd_rtng(88) | weapon_length(126)|swing_damage(38 , cut) | thrust_damage(21 ,  pierce),imodbits_polearm ],
["khand_mace1"      ,"Khand Mace"       ,[("Khand_Weapon_Mace1"      ,0)],itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 122 , weight(3.5)|difficulty(0)|spd_rtng(99) | weapon_length(77)|swing_damage(21 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["khand_mace2"      ,"Khand Mace"       ,[("Khand_Weapon_Mace2"      ,0)],itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 122 , weight(3.5)|difficulty(0)|spd_rtng(99) | weapon_length(77)|swing_damage(21 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
#["khand_mace3"     ,"Khand Mace"       ,[("Khand_Weapon_Mace3"      ,0)],itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 122 , weight(3.5)|difficulty(0)|spd_rtng(99) | weapon_length(77)|swing_damage(21 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["khand_mace_spiked","Khand Spiked Mace",[("Khand_Weapon_Mace_Spiked",0)],itp_type_one_handed_wpn|itp_shop|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 122 , weight(3.5)|difficulty(0)|spd_rtng(99) | weapon_length(82)|swing_damage(21 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["khand_rammace"    ,"Khand Ram Mace"   ,[("Khand_Weapon_Mace_Ram"   ,0)],itp_type_polearm|itp_shop|itp_primary|itp_two_handed|itp_wooden_parry|itp_wooden_attack, itc_nodachi|itcf_carry_back, 97 , weight(6)|difficulty(11)|spd_rtng(84) | weapon_length(102)|swing_damage(33 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["khand_pitsword"   ,"Pit Fighter Sword",[("Khand_Weapon_Sword_Pit"  ,0),("sword_viking_a_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,280 , weight(1.25)|difficulty(0)|spd_rtng(65) | weapon_length(66)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["khand_tulwar"     ,"Khand Tulwar"     ,[("Khand_Weapon_Tulwar"     ,0),("sword_viking_a_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 280 , weight(1.25)|difficulty(0)|spd_rtng(94) | weapon_length(94)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["khand_2h_tulwar"  ,"Khand Tulwar"     ,[("Khand_Weapon_Tulwar_Long",0)],itp_type_two_handed_wpn|itp_shop|itp_always_loot|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back, 1123 , weight(2.75)|difficulty(10)|spd_rtng(89) | weapon_length(116)|swing_damage(42 , cut) | thrust_damage(28 ,  pierce),imodbits_sword_high ],
["khand_lance"      ,"Khand_Lance"      ,[("khand_lance"             ,0)],itp_type_polearm       |itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear, 210 , weight(2.5)|difficulty(0)|spd_rtng(88) | weapon_length(218)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm ],
     ###KHAND HORSES
["variag_pony"      ,"Variag Pony"        , [("rhunhorselight1"      ,0)], itp_shop|itp_type_horse, 0, 724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
["variag_kataphrakt","Easterling Warhorse", [("easterling_warhorse01",0)], itp_shop|itp_type_horse, 0, 724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
     ####KHAND SHIELDS
["easterling_round_horseman","Easterling_Round_Shield", [("eastershield_b",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["variag_gladiator_shield"  ,"Variag_Gladiator_Shield", [("eastershield_c",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["variag_plated_shield"     ,"Variag_Plated_Shield"   , [("eastershield_e",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["easterling_hawk_shield"   ,"Easterling_Hawk_Shield" , [("eastershield_d",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],

 ###TLD RHUN ITEMS##########
["furry_boots", "Furry Boots", [("furry_boots",0)], itp_shop|itp_type_foot_armor,0, 10 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(12)|difficulty(0) ,imodbits_armor ],
 ###ARMOR##########
["rhun_armor_a", "Rhun Armor", [("RhunArmorLight1" ,0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["rhun_armor_b", "Rhun Armor", [("RhunArmorLight2" ,0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#["rhun_armor_c", "Rhun Armor", [("RhunArmorLight3",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["rhun_armor_d", "Rhun Armor", [("RhunArmorLight4" ,0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#["rhun_armor_e", "Rhun Armor", [("RhunArmorLight5",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#["rhun_armor_f", "Rhun Armor", [("RhunArmorHeavy1",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["rhun_armor_g", "Rhun Armor", [("RhunArmorHeavy2" ,0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["rhun_armor_h", "Rhun Armor", [("RhunArmorHeavy3" ,0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#["rhun_armor_i", "Rhun Armor", [("RhunArmorHeavy4",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["rhun_armor_j", "Rhun Armor", [("RhunArmorMedium1",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#["rhun_armor_l", "Rhun Armor",[("RhunArmorMedium2",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["rhun_armor_m", "Rhun Armor", [("RhunArmorMedium3",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["rhun_armor_n", "Rhun Armor", [("RhunArmorMedium4",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["rhun_armor_o", "Rhun Armor", [("RhunArmorMedium5",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["rhun_armor_p", "Rhun Armor", [("RhunArmorNoble1A",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["rhun_armor_k", "Rhun Armor", [("RhunArmorNoble1B",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
	#########Helms##########
["rhun_helm_a", "Rhun Helm", [("RhunHelmConical1"  ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["rhun_helm_b", "Rhun Helm", [("RhunHelmConical2"  ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["rhun_helm_c", "Rhun Helm", [("RhunHelmHorde1"    ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
#["rhun_helm_d", "Rhun Helm", [("RhunHelmHorde2"   ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["rhun_helm_e", "Rhun Helm", [("RhunHelmHorde3"    ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
#["rhun_helm_f", "Rhun Helm", [("RhunHelmPot1"     ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["rhun_helm_g", "Rhun Helm", [("RhunHelmPot2"      ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["rhun_helm_h", "Rhun Helm", [("RhunHelmPot3"      ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["rhun_helm_i", "Rhun Helm", [("RhunHelmRound1"    ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["rhun_helm_j", "Rhun Helm", [("RhunHelmRound2"    ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["rhun_helm_k", "Rhun Helm", [("RhunHelmLeather1"  ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["rhun_helm_l", "Rhun Helm", [("RhunHelmLeather2"  ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["rhun_helm_m", "Rhun Helm", [("RhunHelmLeather3"  ,0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["rhun_helm_n","Rhun Helm",[("RhunHelmDeathDealer1",0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["rhun_helm_o","Rhun Helm",[("RhunHelmDeathDealer2",0)],itp_shop|itp_type_head_armor,0,479,weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
	########WEAPONS##########
["rhun_greataxe",     "Rhun Great Axe",     [("rhun_greataxe"     ,0)],itp_type_polearm|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 264 , weight(5)|difficulty(10)|spd_rtng(89) | weapon_length(115)|swing_damage(43 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["rhun_battleaxe",    "Rhun Battle Axe",    [("rhun_battle_axe"   ,0)],itp_type_polearm|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 264 , weight(5)|difficulty(10)|spd_rtng(86) | weapon_length(108)|swing_damage(43 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["rhun_falchion",     "Rhun Falchion",      [("rhun_falchion"     ,0)],itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip,                                                    105 , weight(2.5)|difficulty(8)|spd_rtng(96) | weapon_length(77)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["rhun_glaive",       "Rhun Glaive",        [("rhun_glaive"       ,0)],itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_staff|itcf_carry_spear,                            352 , weight(4.5)|difficulty(0)|spd_rtng(83) | weapon_length(156)|swing_damage(38 , cut) | thrust_damage(21 ,  pierce),imodbits_polearm ],
#["rhun_bill",        "Rhun Bill",          [("rhun_bill"         ,0)],itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_two_handed|itp_wooden_parry, itc_staff|itcf_carry_spear,                            352 , weight(4.5)|difficulty(0)|spd_rtng(83) | weapon_length(166)|swing_damage(38 , cut) | thrust_damage(21 ,  pierce),imodbits_polearm ],
#["rhun_knife",       "Rhun Knife",         [("rhun_knife"        ,0)],itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_no_parry, itc_dagger|itcf_carry_dagger_front_left, 4 , weight(0.5)|difficulty(0)|spd_rtng(110) | weapon_length(40)|swing_damage(21 , cut) | thrust_damage(13 ,  pierce),imodbits_sword ],
["rhun_greatfalchion","Rhun Great Falchion",[("rhun_greatfalchion",0),("scab_bastardsw_b", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back|itcf_show_holster_when_drawn, 524 , weight(3)|difficulty(11)|spd_rtng(92) | weapon_length(102)|swing_damage(42 , cut) | thrust_damage(31 ,  pierce),imodbits_sword_high ],
["rhun_greatsword",   "Rhun Great Sword",   [("rhun_greatsword"   ,0),("scab_bastardsw_b", ixmesh_carry)], itp_type_two_handed_wpn|itp_shop|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back|itcf_show_holster_when_drawn,524 , weight(3)|difficulty(11)|spd_rtng(94) | weapon_length(101)|swing_damage(40 , cut) | thrust_damage(31 ,  pierce),imodbits_sword_high ],
["rhun_shortsword",   "Rhun Shortsword",    [("rhun_shortsword"   ,0)],itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip,                                                    105 , weight(2.5)|difficulty(6)|spd_rtng(98) | weapon_length(70)|swing_damage(30, cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["rhun_sword",        "Rhun Sword",         [("rhun_sword"        ,0)],itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip,                                                    105 , weight(2.9)|difficulty(8)|spd_rtng(92) | weapon_length(89)|swing_damage(32 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
	########shields##########
["rhun_shield",         "Rhun Shield", [("rhun_shield",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
	##########MOUNTS##########
["rhun_horse_a","Rhun Horse", [("rhunhorselight1",0)], itp_shop|itp_type_horse, 0, 1411,abundance(40)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25),imodbits_horse_basic|imodbit_champion],
["rhun_horse_b","Rhun Horse", [("rhunhorselight2",0)], itp_shop|itp_type_horse, 0, 1411,abundance(40)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25),imodbits_horse_basic|imodbit_champion],
#["rhun_horse_c","Rhun Horse", [("rhunhorselight3",0)], itp_shop|itp_type_horse, 0, 1411,abundance(40)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25),imodbits_horse_basic|imodbit_champion],
["rhun_horse_d","Rhun Horse", [("rhunhorselight4",0)], itp_shop|itp_type_horse, 0, 1411,abundance(40)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25),imodbits_horse_basic|imodbit_champion],
["rhun_horse_e","Rhun Horse", [("rhunhorseheav1" ,0)], itp_shop|itp_type_horse, 0, 1411,abundance(40)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25),imodbits_horse_basic|imodbit_champion],
["rhun_horse_f","Rhun Horse", [("rhunhorseheav2" ,0)], itp_shop|itp_type_horse, 0, 1411,abundance(40)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25),imodbits_horse_basic|imodbit_champion],
["rhun_horse_g","Rhun Horse", [("rhunhorseheav3" ,0)], itp_shop|itp_type_horse, 0, 1411,abundance(40)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25),imodbits_horse_basic|imodbit_champion],
["rhun_horse_h","Rhun Horse", [("rhunhorseheav4" ,0)], itp_shop|itp_type_horse, 0, 1411,abundance(40)|hit_points(140)|body_armor(65)|difficulty(4)|horse_speed(35)|horse_maneuver(32)|horse_charge(25),imodbits_horse_basic|imodbit_champion],

	
  
 #TLD DALE ITEMS##########
    ########MOUNTS##########
["dale_horse"   ,"Dale Horse"   , [("sumpter_horse",0)], itp_shop|itp_type_horse,0,724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
["dale_warhorse","Dale Warhorse", [("warhorse"     ,0)], itp_shop|itp_type_horse,0,724,abundance(50)|hit_points(135)|body_armor(52)|difficulty(4)|horse_speed(36)|horse_maneuver(34)|horse_charge(18),imodbits_horse_basic|imodbit_champion],
	########ARMORS##########
["dale_armor_a", "Dale Armor", [("dale_footman"       ,0)], itp_shop|itp_type_body_armor|itp_covers_legs  ,0, 65 , weight(7)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["dale_armor_b","Dale Armor",[("WIP_dale_footman_cloak",0)],itp_shop|itp_type_body_armor|itp_covers_legs  ,0, 65 , weight(7)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["dale_armor_c", "Dale Armor", [("dale_new_archer_c"  ,0)], itp_shop|itp_type_body_armor|itp_covers_legs  ,0, 65 , weight(7)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["dale_armor_d", "Dale Armor", [("dale_new_archer_f"  ,0)], itp_shop|itp_type_body_armor|itp_covers_legs  ,0, 65 , weight(7)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["dale_armor_e", "Dale Armor", [("dale_heavy_lvam_a"  ,0)], itp_shop|itp_type_body_armor|itp_covers_legs  ,0, 65 , weight(7)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["dale_armor_f", "Dale Armor", [("dale_heavy_lvam_b"  ,0)], itp_shop|itp_type_body_armor|itp_covers_legs  ,0, 65 , weight(7)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["dale_armor_g", "Dale Armor", [("dale_heavy_lvam_d"  ,0)], itp_shop|itp_type_body_armor|itp_covers_legs  ,0, 65 , weight(7)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["dale_armor_h", "Dale Armor", [("dale_heavy_cloak_a" ,0)], itp_shop|itp_type_body_armor|itp_covers_legs  ,0, 65 , weight(7)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["dale_armor_i", "Dale Armor", [("dale_heavy_cloak_b" ,0)], itp_shop|itp_type_body_armor|itp_covers_legs  ,0, 65 , weight(7)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["dale_armor_j", "Dale Armor", [("dale_heavy_cloak_d" ,0)], itp_shop|itp_type_body_armor|itp_covers_legs  ,0, 65 , weight(7)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["dale_armor_k", "Dale Armor", [("dale_heavy_belt_a"  ,0)], itp_shop|itp_type_body_armor|itp_covers_legs  ,0, 65 , weight(7)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["dale_armor_l", "Dale Armor", [("dale_noble_gorget_b",0)], itp_shop|itp_type_body_armor|itp_covers_legs  ,0, 65 , weight(7)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
	###########HELMS##########
["dale_helmet_a", "Dale Helmet", [("DwarfHelmConical_BChain"  ,0)], itp_shop| itp_type_head_armor   ,0, 340 , weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["dale_helmet_b", "Dale Helmet", [("DwarfHelmConical_BLeather",0)], itp_shop| itp_type_head_armor   ,0, 340 , weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["dale_helmet_c", "Dale Helmet", [("DwarfHelmRoundChain"      ,0)], itp_shop| itp_type_head_armor   ,0, 340 , weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["dale_helmet_d", "Dale Helmet", [("DwarfHelmRoundLeather"    ,0)], itp_shop| itp_type_head_armor   ,0, 340 , weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["dale_helmet_e", "Dale Helmet", [("DwarfHelmConicalLeather"  ,0)], itp_shop| itp_type_head_armor   ,0, 340 , weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["dale_helmet_f", "Dale Helmet", [("DwarfHelmConicalChain"    ,0)], itp_shop| itp_type_head_armor   ,0, 340 , weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
#["dale_hood", "Dale Hood", [("dale_hood",0)], itp_shop| itp_type_head_armor   ,0, 340 , weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
#########	WEAPONS##########
["dale_sword",      "Dale Shortsword",[("dale_sword_b" ,0),("scab_dale_sword_b",ixmesh_carry)],itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(88)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["dale_sword_long", "Dale Longsword" ,[("dale_sword_a" ,0),("scab_dale_sword_a",ixmesh_carry)],itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(95)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["dale_sword_broad","Dale Broadsword",[("dale_sword_c" ,0),("scab_dale_sword_c",ixmesh_carry)],itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,162 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(77)|swing_damage(28 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["dale_bow",        "Dale Bow"       ,[("dale_bow"     ,0),("dale_bow_carry"   ,ixmesh_carry)],itp_type_bow|itp_shop|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 728 , weight(1.5)|difficulty(4)|spd_rtng(93) | shoot_speed(58) | thrust_damage(25 ,bow_damage),imodbits_bow ],
["dale_pike",       "Dale Spear"     ,[("dale_spear"   ,0)                                   ],itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear, 125 , weight(3.0)|difficulty(0)|spd_rtng(95) | weapon_length(171)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm ],
["dale_billhook",   "Dale Billhook"  ,[("dale_billhook",0)                                   ],itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear, 125 , weight(3.0)|difficulty(0)|spd_rtng(95) | weapon_length(185)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm ],
#####SHIELDS##########
["dale_shield_a", "Dale Shield", [("arena_shield_blue",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,42,weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60),imodbits_shield ],
["dale_shield_b", "Dale Shield", [("arena_shield_blue",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,42,weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60),imodbits_shield ],
["dale_shield_c", "Dale Shield", [("arena_shield_blue",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,42,weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60),imodbits_shield ],
["dale_shield_d", "Dale Shield", [("arena_shield_blue",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,42,weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60),imodbits_shield ],


 #TLD UMBAR ITEMS##########
 ##ARMOR##########
["umb_armor_a", "Corsair Leather Armor"      , [("corsair_leather"         ,0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,65 ,weight(7) |abundance(100)|head_armor(0)|body_armor(20)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["umb_armor_a1","Corsair Heavy Leather Armor", [("corsair_leather_pauldron",0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,165,weight(8) |abundance(100)|head_armor(0)|body_armor(25)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["umb_armor_b", "Corsair Raider Armor"       , [("corsair_leather_cape"    ,0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,125,weight(7) |abundance(100)|head_armor(0)|body_armor(23)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["umb_armor_c", "Corsair Padded Armor"       , [("corsair_padded"          ,0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,355,weight(10)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["umb_armor_d", "Corsair Heavy Padded Armor" , [("corsair_padded_pauldron" ,0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,395,weight(11)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["umb_armor_e", "Corsair Padded Raider Armor", [("corsair_padded_cape"     ,0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,365,weight(10)|abundance(100)|head_armor(0)|body_armor(37)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["umb_armor_f", "Corsair Hauberk"            , [("corsair_chain"           ,0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,965,weight(7) |abundance(100)|head_armor(0)|body_armor(47)|leg_armor(9)|difficulty(9) ,imodbits_cloth ],
["umb_armor_g", "Corsair Hauberk Pauldrons"  , [("corsair_chain_pauldron"  ,0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,965,weight(7) |abundance(100)|head_armor(0)|body_armor(51)|leg_armor(9)|difficulty(0) ,imodbits_cloth ],
["umb_armor_h", "Corsair Heavy Raider Armor" , [("corsair_chain_cape"      ,0)], itp_shop|itp_type_body_armor|itp_covers_legs,0,965,weight(7) |abundance(100)|head_armor(0)|body_armor(48)|leg_armor(9)|difficulty(0) ,imodbits_cloth ],
	#######HELMS##########
["umb_helm_a", "Corsair Shell Helm"  ,[("shell_helmet"          ,0)],itp_shop|itp_type_head_armor,0,340,weight(2)|abundance(100)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["umb_helm_b", "Corsair Shell Helm"  ,[("shell_helmet_blue"     ,0)],itp_shop|itp_type_head_armor,0,340,weight(2)|abundance(100)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["umb_helm_c", "Corsair Militia Helm",[("umbar_militia_helmet"  ,0)],itp_shop|itp_type_head_armor,0,340,weight(2)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["umb_helm_d", "Corsair Militia Helm",[("umbar_militia_helmet_b",0)],itp_shop|itp_type_head_armor,0,340,weight(2)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["umb_helm_e", "Corsair Raider Helm" ,[("raider_helmet"         ,0)],itp_shop|itp_type_head_armor,0,340,weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["umb_helm_f", "Corsair Raider Helm" ,[("raider_helmet_b"       ,0)],itp_shop|itp_type_head_armor,0,340,weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["umb_hood"  , "Umbar Hood"          ,[("umbar_hood"            ,0)],itp_shop|itp_type_head_armor,0,340,weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],

["corsair_boots", "Corsair_Boots", [("corsair_boots",0)], itp_shop|itp_type_foot_armor  |itp_civilian |itp_attach_armature,0, 174 , weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(16)|difficulty(0) ,imodbits_cloth ],
	########SHIELDS##########
["umb_shield_a", "Corsair Buckler",[("corsair_buckler_long_a" ,0),("corsair_buckler_long_a_carry" ,ixmesh_carry)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_buckler_left,  42 , weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60),imodbits_shield ],
["umb_shield_b", "Corsair Buckler",[("corsair_buckler_round_a",0),("corsair_buckler_round_a_carry",ixmesh_carry)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_buckler_left,  42 , weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60),imodbits_shield ],
["umb_shield_c", "Corsair Buckler",[("corsair_buckler_round_b",0),("corsair_buckler_round_b_carry",ixmesh_carry)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_buckler_left,  42 , weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60),imodbits_shield ],
["umb_shield_d", "Corsair Buckler",[("corsair_buckler_round_c",0),("corsair_buckler_round_c_carry",ixmesh_carry)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_buckler_left,  42 , weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60),imodbits_shield ],
["umb_shield_e", "Corsair Buckler",[("corsair_buckler_long_b" ,0),("corsair_buckler_long_b_carry" ,ixmesh_carry)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_buckler_left,  42 , weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60),imodbits_shield ],
	##########WEAPONS##########umbar_weapon_rapier
["umbar_cutlass"  ,"Umbar Cutlass"  ,[("corsair_cutlass",0),("scab_corsair_cutlass",ixmesh_carry|imodbits_good)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 158 , weight(1.5)|difficulty(0)|spd_rtng(103) | weapon_length(86)|swing_damage(28 , cut) | thrust_damage(0 ,  pierce),imodbits_sword_high ],
["kraken"         ,"Kraken Cutlass" ,[("umbar_weapon_kraken_cutlass",0),("scab_kraken_cutlass",ixmesh_carry|imodbits_good)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 158 , weight(1.5)|difficulty(0)|spd_rtng(103) | weapon_length(103)|swing_damage(30 , cut) | thrust_damage(0 ,  pierce),imodbits_sword_high ],
["umbar_rapier"   ,"Umbar Sword"    ,[("corsair_sword_a",0),("scab_corsair_sword_a",ixmesh_carry|imodbits_good)],   itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip, 363 , weight(1.5)|difficulty(0)|spd_rtng(105) | weapon_length(81)|swing_damage(23 , cut) | thrust_damage(31 ,  pierce),imodbits_sword_high ],
#["corsair_eket"   ,"Umbarian Eket"  ,[("dagger_b",imodbits_good),("dagger_b_scabbard",ixmesh_carry|imodbits_good)], itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_no_parry, itc_dagger|itcf_carry_dagger_front_left|itcf_show_holster_when_drawn, 47 , weight(0.75)|difficulty(0)|spd_rtng(112) | weapon_length(47)|swing_damage(22 , cut) | thrust_damage(19 ,  pierce),imodbits_sword_high ],
["corsair_harpoon","Corsair_Harpoon",[("corsair_harpoon",0)], itp_type_thrown |itp_shop|itp_primary|itp_bonus_against_shield ,itcf_throw_javelin|itcf_show_holster_when_drawn, 209 , weight(4)|difficulty(2)|spd_rtng(89) | shoot_speed(27) | thrust_damage(63 ,  pierce)|max_ammo(2)|weapon_length(87),imodbits_thrown ],
["corsair_sword"  ,"Corsair Eket"   ,[("corsair_sword",0),("scab_corsair_sword", ixmesh_carry)],   itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 363 , weight(1.5)|difficulty(0)|spd_rtng(101) | weapon_length(90)|swing_damage(29 , cut) | thrust_damage(24 ,  pierce),imodbits_sword_high ],
["corsair_throwing_dagger", "Umbarian Throwing Daggers", [("corsair_throwing_dagger",0)], itp_type_thrown |itp_shop|itp_primary ,itcf_throw_knife, 193 , weight(3.5)|difficulty(0)|spd_rtng(110) | shoot_speed(24) | thrust_damage(35 ,  cut)|max_ammo(10)|weapon_length(0),imodbits_thrown ],
["umbar_pike"     ,"Umbar Pike"     ,[("corsair_pike",0)], itp_type_polearm|itp_shop|itp_cant_use_on_horseback|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_pike,125 , weight(3.0)|difficulty(0)|spd_rtng(81) | weapon_length(191)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm ],

 #TLD NORTHMENMEN ITEMS##########
 ######ARMOR##########
["woodman_tunic" ,"Woodman Tunic"            ,[("woodman_tunic"  ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(20)|leg_armor(6),imodbits_none],
["woodman_scout" ,"Woodman Scout Cape"       ,[("woodman_scout"  ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(20)|leg_armor(6),imodbits_none],
["woodman_padded","Woodman Padded Armor"     ,[("woodman_padded" ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(20)|leg_armor(6),imodbits_none],
["beorn_tunic"   ,"Beorning Tunic"           ,[("beorn_tunic"    ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(20)|leg_armor(6),imodbits_none],
["beorn_padded"  ,"Beorning Padded Armor"    ,[("beorn_padded"   ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(20)|leg_armor(6),imodbits_none],
["beorn_heavy"   ,"Beorning Heavy Armor"     ,[("beorn_heavy"    ,0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(20)|leg_armor(6),imodbits_none],
["beorn_berserk" ,"Beorning Berserker Kit"   ,[("beorn_berserker",0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(20)|leg_armor(6),imodbits_none],
["beorn_chief"   ,"Beorning Chieftan's Tunic",[("beorn_chieftain",0)],itp_shop|itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(20)|leg_armor(6),imodbits_none],
	######HELMS##########
["beorn_helmet", "North Skullcap", [("beorn_helmet",0)], itp_shop|itp_type_head_armor   ,0, 340 , weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
#["northm_helm_b", "Northmen Helm", [("skull_cap_new",0)], itp_shop|itp_type_head_armor   ,0, 340 , weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
	#####SHIELDS##########
["beorn_shield","North Shield", [("shield_round_g",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
#["northm_shield_b","Northmen Shield", [("shield_round_g",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
	######WEAPONS###########
["beorn_axe"    ,"Beorning Axe"    ,[("beorning_axe"    ,0)], itp_type_polearm|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 240 , weight(5)|difficulty(9)|spd_rtng(88) | weapon_length(76)|swing_damage(41 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
# use itm_dale_sword, itm_dwarf_sword_a, itm_dwarf_sword_b for Beorning's imported swords
#["northm_sword" ,"Northman Sword"  ,[("sword_medieval_a",0),("sword_medieval_a_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 163 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(95)|swing_damage(27 , cut) | thrust_damage(22 ,  pierce),imodbits_sword_high ],
["beorn_staff"  ,"Woodman's Staff" ,[("woodman_staff"   ,0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack, itc_staff|itcf_carry_sword_back, 60 , weight(2)|difficulty(0)|spd_rtng(104) | weapon_length(104)|swing_damage(20 , blunt) | thrust_damage(20 ,  blunt),imodbits_polearm ],
#["beorn_stave"  ,"Woodman's Stave" ,[("woodman_stave"   ,0)], itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack, itc_staff|itcf_carry_sword_back, 60 , weight(2)|difficulty(0)|spd_rtng(104) | weapon_length(100)|swing_damage(20 , blunt) | thrust_damage(20 ,  blunt),imodbits_polearm ],
["beorn_battle_axe","Beorning War Axe",[("beorning_war_axe",0)], itp_type_polearm|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 240 , weight(5)|difficulty(9)|spd_rtng(88) | weapon_length(71)|swing_damage(41 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],

###TLD DWARF ITEMS##########
	########SHIELDS##########
["dwarf_shield_a", "Dwarven Shield", [("dwarf_shield_a",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["dwarf_shield_b", "Dwarven Shield", [("dwarf_shield_b",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["dwarf_shield_c", "Dwarven Shield", [("dwarf_shield_c",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["dwarf_shield_d", "Dwarven Shield", [("dwarf_shield_d",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["dwarf_shield_e", "Dwarven Shield", [("dwarf_shield_e",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["dwarf_shield_f", "Dwarven Shield", [("dwarf_shield_f",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["dwarf_shield_g", "Dwarven Shield", [("dwarf_shield_g",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
# duplicate ["dwarf_shield_h",         "Dwarven Shield", [("dwarf_shield_h",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["dwarf_shield_i", "Dwarven Shield", [("dwarf_shield_i",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["dwarf_shield_j", "Dwarven Shield", [("dwarf_shield_j",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["dwarf_shield_k", "Dwarven Shield", [("dwarf_shield_k",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["dwarf_shield_l", "Dwarven Shield", [("dwarf_shield_l",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["dwarf_shield_m", "Dwarven Shield", [("dwarf_shield_m",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],
["dwarf_shield_n", "Dwarven Shield", [("dwarf_shield_n",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield ],

	#WEAPONS###########
["dwarf_sword_a", "Dwarf Sword", [("dwarf_sword_a",0),("scab_dwarf_sword_a", ixmesh_carry)],itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_dagger_front_right |itcf_show_holster_when_drawn, 280 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(62)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["dwarf_sword_b", "Dwarf Sword", [("dwarf_sword_b",0),("scab_dwarf_sword_b", ixmesh_carry)],itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_dagger_front_right |itcf_show_holster_when_drawn, 280 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(66)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["dwarf_sword_c", "Dwarf Sword", [("dwarf_sword_c",0),("scab_dwarf_sword_c", ixmesh_carry)],itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_dagger_front_right |itcf_show_holster_when_drawn, 280 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(66)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
["dwarf_sword_d", "Dwarf Sword", [("dwarf_sword_d",0),("scab_dwarf_sword_d", ixmesh_carry)],itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_dagger_front_right |itcf_show_holster_when_drawn, 280 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(58)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
#["dwarf_sword_e", "Dwarf Sword", [("dwarf_sword107",0),("sword_viking_a_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 280 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(96)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
#["dwarf_sword_f", "Dwarf Sword", [("dwarf_sword110",0),("sword_viking_a_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 280 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(100)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
#["dwarf_sword_g", "Dwarf Sword", [("dwarf_sword111",0),("sword_viking_a_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 280 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(91)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
#["dwarf_sword_h", "Dwarf Sword", [("dwarf_sword16",0),("sword_viking_a_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 280 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(91)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
#["dwarf_sword_i", "Dwarf Sword", [("dwarf_sword18",0),("sword_viking_a_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 280 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(92)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
#["dwarf_sword_j", "Dwarf Sword", [("dwarf_sword20",0),("sword_viking_a_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 280 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(97)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
#["dwarf_sword_k", "Dwarf Sword", [("dwarf_sword123",0),("sword_viking_a_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_shop|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
# 280 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(86)|swing_damage(29 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],

["dwarf_adz",          "Dwarf_Adz"          ,[("dwarf_adz"          ,0)],itp_type_polearm|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 264 , weight(5)|difficulty(10)|spd_rtng(86) | weapon_length(68)|swing_damage(43 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["dwarf_great_axe",    "Dwarf_Great_Axe"    ,[("dwarf_great_axe"    ,0)],itp_type_polearm|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 264 , weight(5)|difficulty(10)|spd_rtng(86) | weapon_length(102)|swing_damage(43 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["dwarf_great_mattock","Dwarf_Great_Mattock",[("dwarf_great_mattock",0)],itp_type_polearm|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 264 , weight(5)|difficulty(10)|spd_rtng(86) | weapon_length(94)|swing_damage(43 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["dwarf_great_pick",   "Dwarf_Great_Pick"   ,[("dwarf_great_pick"   ,0)],itp_type_polearm|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 264 , weight(5)|difficulty(10)|spd_rtng(86) | weapon_length(93)|swing_damage(43 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["dwarf_war_pick",     "Dwarf_War_Pick"     ,[("dwarf_war_pick"     ,0)],itp_type_polearm|itp_shop|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 264 , weight(5)|difficulty(10)|spd_rtng(86) | weapon_length(94)|swing_damage(43 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["dwarf_mattock",      "Dwarf_Mattock"      ,[("dwarf_mattock"      ,0)],itp_type_polearm|itp_shop|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 27 , weight(3)|difficulty(0)|spd_rtng(96) | weapon_length(99)|swing_damage(19 , pierce) | thrust_damage(0 ,  pierce),imodbits_pick ],
["dwarf_hand_axe",     "Dwarf_Short_Axe"    ,[("dwarf_1h_axe"       ,0)],itp_type_one_handed_wpn|itp_shop|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 524 , weight(2.0)|difficulty(9)|spd_rtng(97) | weapon_length(54)|swing_damage(40 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["dwarf_throwing_axe", "Dwarf_Throwing_Axe" ,[("dwarf_throw_axe"    ,0)],itp_type_thrown |itp_shop|itp_primary|itp_bonus_against_shield,itcf_throw_axe,241, weight(5)|difficulty(1)|spd_rtng(99) | shoot_speed(20) | thrust_damage(48,cut)|max_ammo(4)|weapon_length(53),imodbits_thrown ],
["dwarf_spear",        "Dwarf_Spear"        ,[("dwarf_spear"        ,0)],itp_type_polearm|itp_shop|itp_spear|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear, 75 , weight(2.25)|difficulty(0)|spd_rtng(98) | weapon_length(140)|swing_damage(20 , blunt) | thrust_damage(26, pierce),imodbits_polearm ],

["dwarf_horn_bow" ,"Dwarf_Horn_Bow" ,[("dwarf_horn_bow" ,0),("khergit_bow_case",ixmesh_carry)],itp_type_bow|itp_shop|itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 269 , weight(1.25)|difficulty(3)|spd_rtng(95) | shoot_speed(56) | thrust_damage(21 ,bow_damage),imodbits_bow ],
["dwarf_short_bow","Dwarf_Short_Bow",[("dwarf_short_bow",0),("nomad_bow_case"  ,ixmesh_carry)],itp_type_bow|itp_shop|itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 164 , weight(1.25)|difficulty(2)|spd_rtng(96) | shoot_speed(53) | thrust_damage(20 ,bow_damage),imodbits_bow ],

	#HELMS#########
["dwarf_helm_a", "Dwarf Helm", [("DwarfHelmCoif",0)],             itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["dwarf_helm_b", "Dwarf Helm", [("DwarfHelmCoifMask",0)],         itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["dwarf_helm_c", "Dwarf Helm", [("DwarfHelmCoifMask_B",0)],       itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["dwarf_helm_h", "Dwarf Helm", [("DwarfHelmConicalMask",0)],      itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["dwarf_helm_i", "Dwarf Helm", [("DwarfHelmFrisianChain",0)],     itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["dwarf_helm_j", "Dwarf Helm", [("DwarfHelmFrisianMask_A",0)],    itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
#["dwarf_helm_k", "Dwarf Helm", [("DwarfHelmFrisianMask_B",0)],    itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["dwarf_helm_l", "Dwarf Helm", [("DwarfHelmHood",0)],             itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["dwarf_helm_m", "Dwarf Helm", [("DwarfHelmIronheadFace",0)],     itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
#["dwarf_helm_n", "Dwarf Helm", [("DwarfHelmIronheadLeather",0)],  itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["dwarf_helm_o", "Dwarf Helm", [("DwarfHelmIronheadNasal",0)],    itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["dwarf_helm_p", "Dwarf Helm", [("DwarfHelmKingCrown",0)],        itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["dwarf_helm_q", "Dwarf Helm", [("DwarfHelmMiner",0)],            itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["dwarf_helm_r", "Dwarf Helm", [("DwarfHelmMinerCap",0)],         itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["dwarf_helm_u", "Dwarf Helm", [("DwarfHelmRoundMask",0)],        itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["dwarf_helm_v", "Dwarf Helm", [("DwarfHelmSalletChain",0)],      itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
#["dwarf_helm_w", "Dwarf Helm", [("DwarfHelmSalletLeather",0)],    itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["dwarf_helm_x", "Dwarf Helm", [("DwarfHelmSalletSargeant",0)],   itp_shop|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
	#########ARMOR##########
["dwarf_armor_a"      ,"Dwarven Tunic over Mail",[("dwarf_tunicmail"      ,0)],itp_shop|itp_type_body_armor|itp_covers_legs ,0,2410 , weight(25)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(13)|difficulty(0) ,imodbits_armor ],
["leather_dwarf_armor","Dwarven Pad over Mail"  ,[("dwarf_padmail"        ,0)],itp_shop|itp_type_body_armor|itp_covers_legs ,0, 195 , weight(5)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["dwarf_vest"         ,"Dwarven Archer Armor"   ,[("dwarf_tunicmailarcher",0)],itp_shop|itp_type_body_armor|itp_covers_legs ,0,1370 , weight(18)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(8)|difficulty(7) ,imodbits_cloth ],
["dwarf_armor_b"      ,"Dwarven Pad over Tunic" ,[("dwarf_padtunic"       ,0)],itp_shop|itp_type_body_armor|itp_covers_legs ,0, 348 , weight(14)|abundance(100)|head_armor(0)|body_armor(34)|leg_armor(8)|difficulty(0) ,imodbits_armor ],
["dwarf_armor_c"      ,"Dwarven Scale over Mail",[("dwarf_scalemail"      ,0)],itp_shop|itp_type_body_armor|itp_covers_legs ,0, 2410, weight(25)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(13)|difficulty(0) ,imodbits_armor ],
["leather_dwarf_armor_b","Dwarven Tunic"        ,[("dwarf_tunicbkp"       ,0)],itp_shop|itp_type_body_armor|itp_covers_legs ,0, 195 , weight(5)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["dwarf_vest_b"       ,"Iron Hills Tunic"    ,[("dwarf_tunic_ironhillsbkp",0)],itp_shop|itp_type_body_armor|itp_covers_legs ,0, 1370, weight(18)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(8)|difficulty(7) ,imodbits_cloth ],

#["dwarf_dol_greaves", "Dwarven Plate Boots", [("dwarf_dol_greaves",0)], itp_shop|itp_type_foot_armor |itp_attach_armature,0, 760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],
["dwarf_pad_boots"  , "Dwarven Padded Boots" ,[("dwarf_pad_boots"  ,0)],itp_shop|itp_type_foot_armor|itp_attach_armature,0, 760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],
["dwarf_chain_boots", "Dwarven Mail Chausses",[("dwarf_chain_boots",0)],itp_shop|itp_type_foot_armor|itp_attach_armature,0, 760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],
["dwarf_scale_boots", "Dwarven Scale Boots"  ,[("dwarf_scale_boots",0)],itp_shop|itp_type_foot_armor|itp_attach_armature,0, 760 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor ],
 
 ###VARIOUS RANDOM MESHES FROM OLD TLD NEEDED FOR TROOPS
#["woodsman_jerkin", "Woodsman's Jerkin", [("woodsman_jerkin",0)], itp_shop|itp_type_body_armor |itp_civilian |itp_covers_legs ,0, 321 , weight(6)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
#["white_robe", "White_Robe", [("robe",0)],itp_type_body_armor  |itp_covers_legs |itp_civilian,0, 31 , weight(1.5)|abundance(100)|head_armor(0)|body_armor(8)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
 ["far_harad_shield_paint", "Wicker Shield", [("far_harad_c_giles",0)], itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),imodbits_shield,[(ti_on_init_item, [(cur_item_set_tableau_material, "tableau_far_harad_shield",0),])],"fac_harad"],
#["rohan_shield_a"        , "Rohan Shield" , [("rohan_shield_green",0)],itp_shop|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 80  , weight(2.5)|hit_points(310)|body_armor(8)|spd_rtng(96)|weapon_length(40),imodbits_shield,[(ti_on_init_item, [(cur_item_set_tableau_material, "tableau_rohan_plain_shield",0)])]],

["witchking_helmet", "Witchking Helmet", [("witchking_helmet",0)], itp_type_head_armor  |itp_covers_head ,0, 2755 , weight(2.5)|abundance(100)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate ],
# let   witchking_helmet  be the last item (mtarini)

]
