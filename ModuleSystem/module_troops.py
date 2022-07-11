#OUTPUT troops.py
import random
 
from header_common import *
from header_items import *
from header_troops import *
from header_item_modifiers import *
from header_skills import *
from ID_factions import *
from ID_items import *
from ID_scenes import *
from module_constants import *
from module_info import wb_compile_switch as is_a_wb_troop
 
####################################################################################################################
#  Each troop contains the following fields:
#  1) Troop id (string): used for referencing troops in other files. The prefix trp_ is automatically added before each troop-id .
#  2) Toop name (string).
#  3) Plural troop name (string).
#  4) Troop flags (int). See header_troops.py for a list of available flags
#  5) Scene (int) (only applicable to heroes) For example: scn_reyvadin_castle|entry(1) puts troop in reyvadin castle's first entry point
#  6) Reserved (int). Put constant "reserved" or 0.
#  7) Faction (int)
#  8) Inventory (list): Must be a list of items
#  9) Attributes (int): Example usage:
#           str_6|agi_6|int_4|cha_5|level(5)
# 10) Weapon proficiencies (int): Example usage:
#           wp_one_handed(55)|wp_two_handed(90)|wp_polearm(36)|wp_archery(80)|wp_crossbow(24)|wp_throwing(45)
#     The function wp(x) will create random weapon proficiencies close to value x.
#     To make an expert archer with other weapon proficiencies close to 60 you can use something like:
#           wp_archery(160)| wp(60)
# 11) Skills (int): See header_skills.py to see a list of skills. Example:
#           knows_ironflesh_3|knows_power_strike_2|knows_athletics_2|knows_riding_2
# 12) Face code (int): You can obtain the face code by pressing ctrl+E in face generator screen
# 13) Face code (int)(2) (only applicable to regular troops
#     The game will create random faces between Face code 1 and face code 2 for generated troops
####################################################################################################################
# Some constant and function declarations to be used below...
 
def wp(x):
  n = 0
#  r = 10 + int(x / 10)
  n|= wp_one_handed(x)
  n|= wp_two_handed(x)
  n|= wp_polearm(x)
  n|= wp_archery(x)
#  n|= wp_crossbow(x)
  n|= wp_throwing(x)
  return n
 
def wp_melee(x):
  n = 0
#  r = 10 + int(x / 10)
  n|= wp_one_handed(x)
  n|= wp_two_handed(x)
  n|= wp_polearm(x)
  return n
 
#Skills
knows_common = knows_riding_1|knows_reserved_10_15|knows_reserved_11_15|knows_reserved_12_15 #add unused dummy skills
knows_common_dwarf = knows_riding_10|knows_horse_archery_10|knows_reserved_10_15|knows_reserved_11_15|knows_reserved_12_15 #add unused dummy skills
def_attrib = str_21| agi_5| int_4| cha_4
 
itm_hunting_bow = itm_short_bow
 
knows_lord_1 = knows_riding_4|knows_trade_2|knows_inventory_management_2|knows_tactics_4|knows_prisoner_management_4|knows_leadership_7
 
knows_warrior_npc = knows_weapon_master_2|knows_ironflesh_1|knows_athletics_1|knows_power_strike_2|knows_riding_2|knows_shield_1|knows_inventory_management_2
knows_merchant_npc = knows_riding_2|knows_trade_3|knows_inventory_management_3 #knows persuasion
knows_tracker_npc = knows_weapon_master_1|knows_athletics_2|knows_spotting_2|knows_pathfinding_2|knows_tracking_2|knows_ironflesh_1|knows_inventory_management_2
 
lord_attrib = str_20|agi_20|int_20|cha_20|level(38)
 
knight_attrib_1 = str_15|agi_14|int_8|cha_16|level(22)
knight_attrib_2 = str_16|agi_16|int_10|cha_18|level(26)
knight_attrib_3 = str_18|agi_17|int_12|cha_20|level(30)
knight_attrib_4 = str_19|agi_19|int_13|cha_22|level(35)
knight_attrib_5 = str_20|agi_20|int_15|cha_25|level(41)
knight_skills_1 = knows_ironflesh_2|knows_power_strike_3|knows_shield_5|knows_athletics_1|knows_tactics_2|knows_prisoner_management_1|knows_leadership_3
knight_skills_2 = knows_ironflesh_3|knows_power_strike_4|knows_shield_5|knows_athletics_2|knows_tactics_3|knows_prisoner_management_2|knows_leadership_5
knight_skills_3 = knows_ironflesh_4|knows_power_strike_5|knows_shield_5|knows_athletics_3|knows_tactics_4|knows_prisoner_management_2|knows_leadership_6
knight_skills_4 = knows_ironflesh_5|knows_power_strike_6|knows_shield_5|knows_athletics_4|knows_tactics_5|knows_prisoner_management_3|knows_leadership_7
knight_skills_5 = knows_ironflesh_6|knows_power_strike_7|knows_shield_5|knows_athletics_5|knows_tactics_6|knows_prisoner_management_3|knows_leadership_9
 

#Kham Gondor Buff Test
gondor_skills_1 = knows_riding_4|knows_ironflesh_2|knows_power_strike_3|knows_shield_5|knows_athletics_1|knows_tactics_2|knows_prisoner_management_1|knows_leadership_5
gondor_skills_2 = knows_riding_4|knows_ironflesh_3|knows_power_strike_4|knows_shield_5|knows_athletics_2|knows_tactics_3|knows_prisoner_management_2|knows_leadership_7
gondor_skills_3 = knows_riding_4|knows_ironflesh_4|knows_power_strike_5|knows_shield_5|knows_athletics_3|knows_tactics_4|knows_prisoner_management_2|knows_leadership_8
gondor_skills_4 = knows_riding_4|knows_ironflesh_5|knows_power_strike_6|knows_shield_5|knows_athletics_4|knows_tactics_5|knows_prisoner_management_3|knows_leadership_9
gondor_skills_5 = knows_riding_4|knows_ironflesh_6|knows_power_strike_7|knows_shield_5|knows_athletics_5|knows_tactics_6|knows_prisoner_management_3|knows_leadership_10

#TLD troop attributes #For reference, vanilla players start with 28 attribute points, 14 skill points
attr_tier_1 =  str_8| agi_6| int_6| cha_7|level(5)  #=27; Recruits, 53 matches
attr_tier_2 = str_10| agi_8| int_6| cha_7|level(10) #=31; Militia, guardsmen, tribal warriors, scouts, squires, 37 matches
attr_tier_3 = str_13|agi_10| int_6| cha_7|level(15) #=37 low-tier professionals / high-tier militia 47 matches
attr_tier_4 = str_15|agi_13| int_6| cha_7|level(20) # Standard professionals. These are the "backbone" troops 52 matches
attr_tier_5 = str_18|agi_16| int_8| cha_8|level(30) # Elite or high-tier professionals
attr_tier_6 = str_20|agi_18|int_20|cha_20|level(40) # Super elite Rohan, Gondor, some captains
attr_tier_7 = str_27|agi_22|int_22|cha_22|level(45) #Lords and captains

attr_fief_tier_1 =  str_8| agi_6| int_6| cha_7|level(4)  #=27; Recruits, 53 matches
attr_fief_tier_2 = str_10| agi_8| int_6| cha_7|level(8) #=31; Militia, guardsmen, tribal warriors, scouts, squires, 37 matches
attr_fief_tier_3 = str_13|agi_10| int_6| cha_7|level(12) #=37 low-tier professionals / high-tier militia 47 matches
attr_fief_tier_4 = str_15|agi_13| int_6| cha_7|level(16) # Standard professionals. These are the "backbone" troops 52 matches

attr_elf_tier_1 = str_10|agi_10| int_6| cha_6|level(6) #=32
attr_elf_tier_2 = str_12|agi_12| int_6| cha_6|level(12) #=36
attr_elf_tier_3 = str_18|agi_18| int_6| cha_6|level(18)
attr_elf_tier_4 = str_18|agi_24| int_6| cha_6|level(26)
attr_elf_tier_5 = str_24|agi_27| int_7| cha_7|level(38) #GA upped higher levels a bit
attr_elf_tier_6 = str_30|agi_30|int_20|cha_20|level(50)

attr_dwarf_tier_1 = str_10| agi_6| int_7| cha_5|level(6) #=28
attr_dwarf_tier_2 = str_14| agi_6| int_7| cha_5|level(11) #=32
attr_dwarf_tier_3 = str_15| agi_9| int_7| cha_5|level(16) #=36 (players can start as ironhills t3 warriors)
attr_dwarf_tier_4 = str_18|agi_11| int_7| cha_6|level(21)
attr_dwarf_tier_5 = str_24|agi_15| int_8| cha_7|level(35) #GA upped 2 highest levels a bit
attr_dwarf_tier_6 = str_30|agi_18| int_20| cha_20|level(48)

# InVain: Not in yet, we need more tests if we can savely reduce elven and dwarf armies' size.

#attr_elf_tier_1 = str_12|agi_12| int_4| cha_4|level(11)
#attr_elf_tier_2 = str_14|agi_14| int_4| cha_4|level(16)
#attr_elf_tier_3 = str_18|agi_18| int_4| cha_4|level(23)
#attr_elf_tier_4 = str_18|agi_24| int_4| cha_4|level(34)
#attr_elf_tier_5 = str_24|agi_27| int_4| cha_4|level(47) 
#attr_elf_tier_6 = str_30|agi_30|int_20|cha_20|level(60)

#attr_dwarf_tier_1 =  str_9| agi_6| int_4| cha_4|level(9)
#attr_dwarf_tier_2 = str_12| agi_9| int_4| cha_4|level(14)
#attr_dwarf_tier_3 = str_15|agi_11| int_4| cha_4|level(21)
#attr_dwarf_tier_4 = str_18|agi_13| int_4| cha_4|level(31)
#attr_dwarf_tier_5 = str_18|agi_18| int_4| cha_4|level(43) 
#attr_dwarf_tier_6 = str_24|agi_18| int_4| cha_4|level(57)																																																		 

# InVain: ~halfed orc levels, worse in autocalc, but easier to train and cheaper.
attr_orc_tier_1 =  str_6| agi_7| int_6| cha_6|level(2) #=25
attr_orc_tier_2 =  str_8| agi_9| int_6| cha_6|level(5) #=29
attr_orc_tier_3 =  str_9| agi_9| int_6| cha_6|level(8)
attr_orc_tier_4 = str_11| agi_9| int_7| cha_7|level(17) #elite orcs
attr_orc_tier_5 = str_16|agi_11| int_9| cha_9|level(26) #super-elite, Moria and Gundabad only #upped lvl by a lot, because these troops are quite strong
attr_orc_tier_6 = str_22|agi_12| int_9| cha_9|level(45) #lords only

# InVain: Uruks and evil men (except black numenoreans): Middle ground between orcs and good men, their level simulating their worse equipment in autocalc, but easier to train and cheaper. Elites are good.
attr_evil_tier_1 =  str_8| agi_6| int_6| cha_6|level(3) #=26
attr_evil_tier_2 = str_11| agi_7| int_6| cha_6|level(7) #=30
attr_evil_tier_3 = str_13|agi_10| int_6| cha_6|level(11) #=35
attr_evil_tier_4 = str_15|agi_15| int_6| cha_6|level(19) #=42 Mordor Uruk top tier, almost human level
attr_evil_tier_5 = str_18|agi_18| int_4| cha_6|level(28) #evil men elites are strong, Isen Uruk Champions too #upped lvl a bit
attr_evil_tier_6 = str_20|agi_20|int_20|cha_20|level(36) #only Isengard berserkers and Rhun Nobles

#TLD weapon proficiencies
wp_tier_1 = wp(70)
wp_tier_2 = wp(100)
wp_tier_3 = wp(135)
wp_tier_4 = wp(170)
wp_tier_5 = wp(200)
wp_tier_6 = wp(300)
wp_tier_7 = wp(400)

wp_tier_bow_2 = wp_archery(100) | wp_melee(70)
wp_tier_bow_3 = wp_archery(135) | wp_melee(100)
wp_tier_bow_4 = wp_archery(150) | wp_melee(135)
wp_tier_bow_5 = wp_archery(170) | wp_melee(150) #higher tier archers are more specialised
wp_tier_bow_6 = wp_archery(220) | wp_melee(170)

wp_elf_tier_1 = wp_melee(240) | wp_archery(160)
wp_elf_tier_2 = wp_melee(280) | wp_archery(180)
wp_elf_tier_3 = wp_melee(310) | wp_archery(200)
wp_elf_tier_4 = wp_melee(360) | wp_archery(220)
wp_elf_tier_5 = wp_melee(410) | wp_archery(240)
wp_elf_tier_6 = wp_melee(460) | wp_archery(280)

wp_elf_tier_bow_1 = wp_archery(200) | wp_melee(200)
wp_elf_tier_bow_2 = wp_archery(240) | wp_melee(220)
wp_elf_tier_bow_3 = wp_archery(270) | wp_melee(240)
wp_elf_tier_bow_4 = wp_archery(300) | wp_melee(280)
wp_elf_tier_bow_5 = wp_archery(320) | wp_melee(300) 
wp_elf_tier_bow_6 = wp_archery(340) | wp_melee(320)

wp_dwarf_tier_1 = wp_melee(100) | wp_archery(140)
wp_dwarf_tier_2 = wp_melee(160) | wp_archery(160)
wp_dwarf_tier_3 = wp_melee(210) | wp_archery(190)
wp_dwarf_tier_4 = wp(240)
wp_dwarf_tier_5 = wp(300)
wp_dwarf_tier_6 = wp(350)

wp_orc_tier_1 = wp(70)
wp_orc_tier_2 = wp(95)
wp_orc_tier_3 = wp(125)
wp_orc_tier_4 = wp(150)
wp_orc_tier_5 = wp(170)
wp_orc_tier_6 = wp(300)

wp_orc_tier_bow_2 = wp_archery(95) | wp_melee(70)
wp_orc_tier_bow_3 = wp_archery(125) | wp_melee(95)
wp_orc_tier_bow_4 = wp_archery(150) | wp_melee(115)
wp_orc_tier_bow_5 = wp_archery(170) | wp_melee(130) 

#These face codes are generated by the in-game face generator.
#Enable edit mode and press ctrl+E in face generator screen to obtain face codes.
 
reserved = 0
no_scene = 0
 
swadian_face_younger_1 = 0x0000000000000001124000000020000000000000001c00800000000000000000
swadian_face_young_1   = 0x0000000400000001124000000020000000000000001c00800000000000000000
swadian_face_middle_1  = 0x0000000800000001124000000020000000000000001c00800000000000000000
swadian_face_old_1     = 0x0000000d00000001124000000020000000000000001c00800000000000000000
swadian_face_older_1   = 0x0000000fc0000001124000000020000000000000001c00800000000000000000

swadian_face_younger_2 = 0x00000000000062c76ddcdf7feefbffff00000000001efdbc0000000000000000
swadian_face_young_2   = 0x00000003c00062c76ddcdf7feefbffff00000000001efdbc0000000000000000
swadian_face_middle_2  = 0x00000007c00062c76ddcdf7feefbffff00000000001efdbc0000000000000000
swadian_face_old_2     = 0x0000000bc00062c76ddcdf7feefbffff00000000001efdbc0000000000000000
swadian_face_older_2   = 0x0000000fc00062c76ddcdf7feefbffff00000000001efdbc0000000000000000
 
vaegir_face_younger_1  = 0x0000000000000001124000000020000000000000001c00800000000000000000
vaegir_face_young_1    = 0x0000000400000001124000000020000000000000001c00800000000000000000
vaegir_face_middle_1   = 0x0000000800000001124000000020000000000000001c00800000000000000000
vaegir_face_old_1      = 0x0000000d00000001124000000020000000000000001c00800000000000000000 #retard face
vaegir_face_older_1    = 0x0000000fc0000001124000000020000000000000001c00800000000000000000
 
vaegir_face_younger_2  = 0x000000003f00230c4deeffffffffffff00000000001efff90000000000000000
vaegir_face_young_2    = 0x00000003bf00230c4deeffffffffffff00000000001efff90000000000000000
vaegir_face_middle_2   = 0x00000007bf00230c4deeffffffffffff00000000001efff90000000000000000
vaegir_face_old_2      = 0x0000000cbf00230c4deeffffffffffff00000000001efff90000000000000000 #mongol face
vaegir_face_older_2    = 0x0000000ff100230c4deeffffffffffff00000000001efff90000000000000000
 
khergit_face_younger_1 = 0x0000000009003109207000000000000000000000001c80470000000000000000
khergit_face_young_1   = 0x00000003c9003109207000000000000000000000001c80470000000000000000
khergit_face_middle_1  = 0x00000007c9003109207000000000000000000000001c80470000000000000000
khergit_face_old_1     = 0x0000000b89003109207000000000000000000000001c80470000000000000000
khergit_face_older_1   = 0x0000000fc9003109207000000000000000000000001c80470000000000000000
 
khergit_face_younger_2 = 0x000000003f0061cd6d7ffbdf9df6ebee00000000001ffb7f0000000000000000
khergit_face_young_2   = 0x00000003bf0061cd6d7ffbdf9df6ebee00000000001ffb7f0000000000000000
khergit_face_middle_2  = 0x000000077f0061cd6d7ffbdf9df6ebee00000000001ffb7f0000000000000000
khergit_face_old_2     = 0x0000000b3f0061cd6d7ffbdf9df6ebee00000000001ffb7f0000000000000000
khergit_face_older_2   = 0x0000000fff0061cd6d7ffbdf9df6ebee00000000001ffb7f0000000000000000
 
nord_face_younger_1    = 0x0000000000000001124000000020000000000000001c00800000000000000000
nord_face_young_1      = 0x0000000400000001124000000020000000000000001c00800000000000000000
nord_face_middle_1     = 0x0000000800000001124000000020000000000000001c00800000000000000000
nord_face_old_1        = 0x0000000d00000001124000000020000000000000001c00800000000000000000
nord_face_older_1      = 0x0000000fc0000001124000000020000000000000001c00800000000000000000
 
nord_face_younger_2    = 0x00000000310023084deeffffffffffff00000000001efff90000000000000000
nord_face_young_2      = 0x00000003b10023084deeffffffffffff00000000001efff90000000000000000
nord_face_middle_2     = 0x00000008310023084deeffffffffffff00000000001efff90000000000000000
nord_face_old_2        = 0x0000000c710023084deeffffffffffff00000000001efff90000000000000000
nord_face_older_2      = 0x0000000ff10023084deeffffffffffff00000000001efff90000000000000000
 
rhodok_face_younger_1  = 0x0000000009002003140000000000000000000000001c80400000000000000000
rhodok_face_young_1    = 0x0000000449002003140000000000000000000000001c80400000000000000000
rhodok_face_middle_1   = 0x0000000849002003140000000000000000000000001c80400000000000000000
rhodok_face_old_1      = 0x0000000cc9002003140000000000000000000000001c80400000000000000000
rhodok_face_older_1    = 0x0000000fc9002003140000000000000000000000001c80400000000000000000
 
rhodok_face_younger_2  = 0x00000000000062c76ddcdf7feefbffff00000000001efdbc0000000000000000
rhodok_face_young_2    = 0x00000003c00062c76ddcdf7feefbffff00000000001efdbc0000000000000000
rhodok_face_middle_2   = 0x00000007c00062c76ddcdf7feefbffff00000000001efdbc0000000000000000
rhodok_face_old_2      = 0x0000000bc00062c76ddcdf7feefbffff00000000001efdbc0000000000000000
rhodok_face_older_2    = 0x0000000fc00062c76ddcdf7feefbffff00000000001efdbc0000000000000000
 
man_face_younger_1     = 0x0000000000000001124000000020000000000000001c00800000000000000000
man_face_young_1       = 0x0000000400000001124000000020000000000000001c00800000000000000000
man_face_middle_1      = 0x0000000800000001124000000020000000000000001c00800000000000000000
man_face_old_1         = 0x0000000d00000001124000000020000000000000001c00800000000000000000
man_face_older_1       = 0x0000000fc0000001124000000020000000000000001c00800000000000000000
 
man_face_younger_2     = 0x000000003f0052064deeffffffffffff00000000001efff90000000000000000
man_face_young_2       = 0x00000003bf0052064deeffffffffffff00000000001efff90000000000000000
man_face_middle_2      = 0x00000007bf0052064deeffffffffffff00000000001efff90000000000000000
man_face_old_2         = 0x0000000bff0052064deeffffffffffff00000000001efff90000000000000000
man_face_older_2       = 0x0000000fff0052064deeffffffffffff00000000001efff90000000000000000
 
merchant_face_1        = man_face_young_1
merchant_face_2        = man_face_older_2
 
woman_face_1           = 0x0000000000000001000000000000000000000000001c00000000000000000000
woman_face_2           = 0x00000003bf0030067ff7fbffefff6dff00000000001f6dbf0000000000000000
 
refugee_face1  = woman_face_1
refugee_face2  = woman_face_2
girl_face1     = woman_face_1
girl_face2     = woman_face_2
 
mercenary_face_1       = 0x0000000000000000000000000000000000000000001c00000000000000000000
mercenary_face_2       = 0x0000000cff00730b6db6db6db7fbffff00000000001efffe0000000000000000
 
vaegir_face2   = vaegir_face_older_2
 
bandit_face1   = man_face_young_1
bandit_face2   = man_face_older_2
 
# Many troops have these faces
gondor_face1           = 0x000000017f00018122dc71b96c8cb6e300000000001d45330000000000000000
gondor_face2           = 0x00000009bf00200942ec7096e3a9b69c00000000001d47330000000000000000
gondor_face3           = 0x000000002400200942ec7096e3a9b49c00000000001d47330000000000000000
gondor_younger_1       = 0x00000004ef00200f070c6a374b40452c00000000001cc6690000000000000000 
gondor_older_1         = 0x000000072e002585209c6e399260532c00000000001cd6720000000000000000 

#MV: default Rohan face (blond, beard+moustache)
rohan_face_younger_1   = 0x0000000000000001124000000025120900000000001c00800000000000000000
rohan_face_young_1     = 0x0000000400000001124000000025120900000000001c00800000000000000000
rohan_face_middle_1    = 0x0000000800000141124000000025120900000000001c00800000000000000000
rohan_face_old_1       = 0x0000000d00000180124000000025120900000000001c00800000000000000000
rohan_face_older_1     = 0x0000000fc00001c0124000000025120900000000001c00800000000000000000

rohan_face_younger_2   = 0x00000000310031c24deeffffffffffff00000000001efff90000000000000000
rohan_face_young_2     = 0x00000003b10031c34deeffffffffffff00000000001efff90000000000000000
rohan_face_middle_2    = 0x00000008310031c54deeffffffffffff00000000001efff90000000000000000
rohan_face_old_2       = 0x0000000cf10033054deeffffffffffff00000000001efff90000000000000000
rohan_face_older_2     = 0x0000000ff10033054deeffffffffffff00000000001efff90000000000000000

rohan_woman_face_1     = 0x0000000000000001000000000000000000000000001c00000000000000000000
rohan_woman_face_2     = 0x00000004040020087ff7fbffefff6dff00000000001f6dbf0000000000000000
#TEXTUR_BIT_remind     = 0x0000000000001000000000000000000000000000000000000000000000000000 # UNUSED: but just a reminder of which one is the texture bit -- mtarini
#HAIR_BIT_remind       = 0x0000000000000001000000000000000000000000000000000000000000000000 # UNUSED: but just a reminder of which one is the hair bit -- GA
#BEARD_BIT_remind      = 0x0000000000000110000000000000000000000000000000000000000000000000 # UNUSED: but just a reminder of which one is the beard bit -- GA
#AGE_BITS_remind       = 0x0000000fc0000000000000000000000000000000000000000000000000000000 # UNUSED: but just a reminder of which one is the age bits -- GA
#HAIR_COLOR_BITS_remind= 0x000000003f000000000000000000000000000000000000000000000000000000 # UNUSED: but just a reminder of which one is the age bits -- GA
             

beorn_face1 = rohan_face_young_1
beorn_face2 = rohan_face_old_2
arnor_face_middle_1    = 0x00000001bd00214748ed6e47238dd70d00000000001d36f30000000000000000
arnor_face_middle_2    = 0x000000054000418744ec6e47238dd70d00000000001d38f10000000000000000
 
arnor_face_older_1     = 0x00000009e100418814ed6e47238dd70d00000000001d38e10000000000000000
arnor_face_older_2     = 0x0000000df200214814ed6e45238e498e00000000001d38e10000000000000000
 
rivendell_elf_face_1   = 0x000000000d00000754d44da9148d272400000000001d36f00000000000000000
rivendell_elf_face_2   = 0x000000008e00200905553159146da68300000000001d36b00000000000000000

lorien_elf_face_1      = 0x0000000ec0001007256d3159348da69300000000001d36b40000000000000000
lorien_elf_face_2      = 0x000000001400000836dd51589c88a69300000000001cd9340000000000000000
mirkwood_elf_face_1    = 0x000000000000014148ed6e47238dd70d00000000001d36f30000000000000000
mirkwood_elf_face_2    = 0x0000000df200314914ed6e45238e498e00000000001d38e10000000000000000
haradrim_face_1        = 0x0000000239000008209072d1708d38ab00000000001d37240000000000000000
haradrim_face_2        = 0x0000000cff00200a6bac976dbcb6db3500000000001edb640000000000000000
far_harad_face1        = 0x0000000cf100300b209072d1708d38ab00000000001d37240000000000000000
far_harad_face2        = 0x00000001bf00400b36db6db6db6db6db00000000001db6db0000000000000000
 
dwarf_face_1           = 0x00000001a3002083375c6eddad6db6db00000000001db7230000000000000000
dwarf_face_2           = 0x0000000aff005104069d91bd2c6dbada00000000001db6e90000000000000000
dwarf_face_3           = 0x0000000180001103375c6eddad6db6db00000000001db7230000000000000000
dwarf_face_4           = 0x00000005ea001183069b926d2c6dbada00000000001d29690000000000000000
dwarf_face_5           = 0x00000005ff002204069a936d2c6dbada00000000001d29510000000000000000
dwarf_face_6           = 0x0000000fff0020c3069a936d2c6dbada00000000001d29510000000000000000
dwarf_face_7           = 0x0000000fff002004069a936d2c6dbada00000000001d29510000000000000000
 
# orc random faces.
# 0 and 1 are all extreme
# always use EVEN-number ODD-number for roops, to maximixe harcut-texture variations
orc_face_normal        = 0x000000018000000236db6db6db6db6db00000000001db6db0000000000000000
orc_face1              = 0x0000000180000000200000000000000000000000001c00800000000000000000  # extreme 0 
orc_face2              = 0x0000000fff00200f6dffffffffffffff00000000001effff0000000000000000  # extreme 1 
orc_face3              = 0x00000001b20000001b0386a58b51daaa00000000001dd7a30000000000000000
orc_face4              = 0x00000001b900200f386b6e18a3b1499d00000000001e66ab0000000000000000
orc_face5              = 0x00000001930000003b1b3a472d6ec8d200000000001de6f40000000000000000
orc_face6              = 0x000000018b00200f56dc66378c6db95d00000000001ebbab0000000000000000
orc_face7              = 0x0000000184000000481c9254b486e86c00000000001d4e940000000000000000
orc_face8              = 0x00000001a700200f4e9b7a111aa736cb00000000001dc46d0000000000000000
orc_face9              = 0x00000001be000000251b74b761cea75300000000001edd330000000000000000

troll_face1        = 0x000000018000000236db6db6db6db6db00000000001db6db0000000000000000  # no effects
troll_face2        = 0x000000018000000236db6db6db6db6db00000000001db6db0000000000000000  # no effects
 
#urukhai_face_low1      = 0x0000000180000001003b6db6db6db6db00000000000000000000000000000000
#urukhai_face_low2      = 0x00000001932021c3003a8e53356a271200000000000000000000000000000000
#urukhai_face_mid1      = 0x0000000193000205003a8e53356a271a00000000000000000000000000000000
#urukhai_face_mid2      = 0x0000000193202046003a8fd31d0a2f1a00000000000000000000000000000000
#urukhai_face_high1     = 0x000000003f000084003a8ff32e6a7f0200000000000000000000000000000000
#urukhai_face_high2     = 0x0000000193202205003a8e53356a271a00000000000000000000000000000000
uruk_hai_face1         = 0x0000000400000000003800000000000000000000000000000000000000000000
uruk_hai_face2         = 0x0000000400002207003fffffffffffff00000000000000000000000000000000

evil_man_face1         = man_face_young_1
evil_man_face2         = man_face_older_2
dunland_face1          = 0x000000001f001001124161829880300200000000001c00800000000000000000
dunland_face2          = 0x0000000dff0062875d7fd3ffffffffff00000000001edffe0000000000000000
nord_face_younger_1    = 0x0000000000000001124000000020000000000000001c00800000000000000000


easterling_face1       = khergit_face_middle_2
easterling_face2       = khergit_face_middle_1
rhun_man1              = 0x000000020000318723acb7639104bbb600000000001e44720000000000000000
rhun_man2              = 0x0000000ebf00734d39fefff7db52ffff00000000001ee6bb0000000000000000
khand_man1             = 0x00000009bf00838a242ea7515044d37e00000000001d54b80000000000000000
khand_man2             = 0x0000000fff00d4cd6bf7d3f5fb9179ff00000000001de6f90000000000000000
mordor_man1            = 0x000000013f00000013045438c402929200000000001d4ab00000000000000000
mordor_man2            = 0x0000000fff00200429cd7d495667732e00000000001d5cf90000000000000000

#Items hidden behind imod modifiers:
itm_whiterobe = (itm_rohan_armor_th, imod_bent)
itm_whiterobe_saru = (itm_rohan_armor_th, imod_bent)
itm_nazgulrobe = (itm_rohan_armor_th, imod_cheap)
itm_galadriel = (itm_rohan_armor_th, imod_rusty)
itm_merry_outfit = (itm_rohan_armor_th, imod_chipped)
itm_pippin_outfit = (itm_rohan_armor_th, imod_battered)
itm_denethor_robe = (itm_rohan_armor_th, imod_well_made)
itm_riv_helm_glorfi = (itm_witchking_helmet, imod_rotten)
itm_riv_tiara = (itm_tiara_reward, imod_lordly)

#civilian items

# itm_tabard_b = itm_white_tunic_a
# itm_nobleman_outfit_b_new = (itm_white_tunic_a, imod_large_bag)
# itm_peasant_man_a = itm_black_tunic
# itm_fur_hat_a_new = itm_hood_black
# itm_noel_hat_a = itm_hood_black

itm_blue_tunic = (itm_white_tunic_a, imod_well_made) #dale_tunic, basic blue
itm_green_tunic = (itm_white_tunic_a, imod_sharp) #rohan_tunic, basic green
itm_black_dress = (itm_white_tunic_a, imod_poor) #gondor_dress_a, basic black dress, suits all factions
itm_leather_apron = (itm_white_tunic_a, imod_deadly) #smith_leather_apron, only use for smiths, not walkers
itm_white_tunic_b = (itm_white_tunic_a, imod_day_old)   #generic_tunic_a, white
itm_blackwhite_dress = (itm_white_tunic_a, imod_old) #gondor_dress_b fine dress
itm_white_tunic_c = (itm_white_tunic_a, imod_cheap)  # generic_tunic_c, tunic and vest
itm_leather_jerkin = (itm_white_tunic_a, imod_exquisite) #generic_leather_jerkin, all factions
itm_fur_coat = (itm_white_tunic_a, imod_powerful) #dale_coat
itm_green_dress = (itm_white_tunic_a, imod_rough) #rohan_dress, could also serve dale, northemen
itm_gondor_fine_outfit_dress = (itm_white_tunic_a, imod_large_bag) #gondor_fine_outfit_dress, black and white gondor noble outfit
itm_rohan_fine_outfit_dale_dress = (itm_white_tunic_a, imod_rotten) #rohan_fine_outfit_dale_dress
itm_robe_generic_dress = (itm_white_tunic_a, imod_fresh) #brown robe, brown dress
itm_wimple_a = (itm_hood_black, imod_smelling)
itm_wimple_with_veil = (itm_hood_black, imod_rotten)
itm_fine_hat = (itm_hood_black, imod_large_bag)
itm_rohan_tunic_a = (itm_white_tunic_a, imod_two_day_old)
itm_rohan_tunic_b = (itm_white_tunic_a, imod_smelling)

#Trolls
itm_troll_feet = (itm_ent_feet_boots, imod_cracked)
itm_troll_head_a = (itm_troll_head, imod_rotten)
itm_troll_head_b = (itm_troll_head, imod_day_old)
itm_troll_head_c = (itm_troll_head, imod_two_day_old)
itm_troll_body_a = (itm_troll_head, imod_rotten)
itm_troll_hands = (itm_ent_hands, imod_cracked)

itm_ent_head = (itm_ent_head_helm, imod_rotten)
itm_ent_head_2 = (itm_ent_head_helm, imod_rotten)
itm_ent_head_3 = (itm_ent_head_helm, imod_two_day_old)

itm_tree_trunk_club = (itm_tree_trunk_club_a, imod_bent) #full tree trunk
itm_giant_bone_cudgel = (itm_tree_trunk_club_a, imod_crude)
itm_tree_trunk_club_b = (itm_tree_trunk_club_a, imod_fine) #crude club
itm_giant_club = (itm_tree_trunk_club_a, imod_heavy)
itm_giant_spiked_mace = (itm_tree_trunk_club_a, imod_strong)

itm_tree_trunk_invis = (itm_troll_weapon_dmg, imod_cracked)
itm_giant_hammer = (itm_troll_weapon_dmg, imod_strong)
itm_giant_mace_b = (itm_troll_weapon_dmg, imod_plain)
itm_giant_sledgehammer = (itm_troll_weapon_dmg, imod_bent)

itm_troll_shield_b = (itm_troll_shield_a, imod_poor)

itm_olog_body = (itm_ent_body, imod_rusty)
itm_olog_body_b = (itm_ent_body, imod_tattered)
itm_olog_head_a = (itm_ent_head_helm, imod_hardened)
itm_olog_head_b = (itm_ent_head_helm, imod_reinforced)
itm_olog_head_c = (itm_ent_head_helm, imod_lordly)
itm_olog_hands = (itm_ent_hands, imod_large_bag)
itm_olog_feet = (itm_ent_feet_boots, imod_hardened)

itm_isen_olog_body = (itm_ent_body, imod_old)
itm_isen_olog_body_b = (itm_ent_body, imod_cheap)
itm_isen_olog_head_a = (itm_ent_head_helm, imod_bent)
itm_isen_olog_head_b = (itm_ent_head_helm, imod_old)
itm_isen_olog_head_c = (itm_ent_head_helm, imod_cheap)
itm_isen_olog_hands = (itm_ent_hands, imod_rotten)
itm_isen_olog_feet = (itm_ent_feet_boots, imod_thick)

itm_gunda_troll_body = (itm_troll_body, imod_thick)
itm_gunda_troll_body_berta = (itm_troll_body, imod_rotten)
itm_gunda_troll_head_a = (itm_troll_head, imod_smelling)
itm_gunda_troll_head_b = (itm_troll_head, imod_fresh)
itm_gunda_troll_head_c = (itm_troll_head, imod_large_bag)
itm_gunda_troll_hands = (itm_ent_hands, imod_rusty)
itm_gunda_troll_feet = (itm_ent_feet_boots, imod_rusty)

itm_mordor_troll_body = (itm_troll_body, imod_hardened)
itm_mordor_troll_head_a = (itm_troll_head, imod_thick)
itm_mordor_troll_head_b = (itm_troll_head, imod_hardened)
itm_mordor_troll_hands = (itm_ent_hands, imod_bent)
itm_mordor_troll_feet = (itm_ent_feet_boots, imod_bent)

#Handwear and boots variants
itm_leather_gloves_good = 		(itm_leather_gloves, imod_thick)
itm_leather_gloves_bad = 		(itm_leather_gloves, imod_crude)
itm_evil_gauntlets_a_good = 	(itm_evil_gauntlets_a, imod_thick)
itm_evil_gauntlets_a_lordly = 	(itm_evil_gauntlets_a, imod_reinforced)
itm_evil_gauntlets_a_bad = 		(itm_evil_gauntlets_a, imod_crude)
itm_evil_gauntlets_b_good = 	(itm_evil_gauntlets_b, imod_thick)
itm_evil_gauntlets_b_bad = 		(itm_evil_gauntlets_b, imod_crude)
itm_leather_boots_bad = 		(itm_leather_boots, imod_rusty)
itm_leather_boots_dark_bad = 	(itm_leather_boots_dark, imod_rusty)
itm_splinted_greaves_good = 	(itm_splinted_greaves, imod_reinforced)
itm_rohan_shoes_bad = 			(itm_rohan_shoes, imod_rusty)
itm_rohan_shoes_good = 			(itm_rohan_shoes, imod_fine)

#replacing Hoods
itm_dunedain_helm_a = itm_hood_grey
itm_gondor_ranger_hood = itm_hood_green
itm_gondor_ranger_hood_mask = (itm_hood_green, imod_reinforced)
itm_lamedon_hood = itm_hood_grey
itm_pelargir_hood = itm_hood_grey

#hood variants
itm_hood_black_good = (itm_hood_black, imod_thick)
itm_hood_black_bad = (itm_hood_black, imod_rusty)
itm_hood_green_good = (itm_hood_green, imod_thick)
itm_hood_green_bad = (itm_hood_green, imod_rusty)
itm_hood_grey_good = (itm_hood_grey, imod_thick)
itm_hood_grey_bad = (itm_hood_grey, imod_rusty)
itm_hood_leather_good = (itm_hood_leather, imod_thick)
itm_hood_leather_bad = (itm_hood_leather, imod_rusty)

#Dwarf helm variants
itm_dwarf_helm_coif_reinf = (itm_dwarf_helm_coif, imod_reinforced)
itm_dwarf_helm_coif_lordly =  (itm_dwarf_helm_coif, imod_lordly)
itm_dwarf_helm_kettle_lordly =  (itm_dwarf_helm_kettle, imod_lordly)
itm_dwarf_helm_fris_reinf = (itm_dwarf_helm_fris, imod_reinforced)
itm_dwarf_helm_fris_lordly = (itm_dwarf_helm_fris, imod_lordly)
itm_dwarf_nasal_reinf = (itm_dwarf_nasal, imod_reinforced)
itm_dwarf_nasal_lordly =  (itm_dwarf_nasal, imod_lordly)
itm_dwarf_miner_nasal = (itm_dwarf_miner)
itm_dwarf_miner_reinf = (itm_dwarf_miner, imod_reinforced)
itm_dwarf_helm_round_lordly = (itm_dwarf_helm_round, imod_reinforced)
itm_dwarf_helm_sallet_lordly = (itm_dwarf_helm_sallet, imod_reinforced)
itm_dwarf_helm_king_NPC = (itm_witchking_helmet, imod_old)

#Dwarf armour variants
itm_dwarf_armor_a_lordly = (itm_dwarf_armor_a, imod_reinforced)
itm_dwarf_armor_b_lordly = (itm_dwarf_armor_b, imod_reinforced)
itm_dwarf_armor_c_lordly = (itm_dwarf_armor_c, imod_reinforced)
itm_dwarf_vest_lordly = (itm_dwarf_vest, imod_reinforced)
itm_dwarf_vest_b_lordly = (itm_dwarf_vest_b, imod_reinforced)
itm_leather_dwarf_armor_b_lordly = (itm_leather_dwarf_armor_b, imod_reinforced)

#Dwarf weapon variants
itm_dwarf_great_axe_good = (itm_dwarf_great_axe, imod_masterwork)
itm_dwarf_great_mattock_good = (itm_dwarf_great_mattock, imod_balanced)
itm_dwarf_great_pick_good = (itm_dwarf_great_pick, imod_balanced)
itm_dwarf_war_pick_old = (itm_dwarf_great_pick, imod_old)
itm_dwarf_mattock_good = (itm_dwarf_mattock, imod_balanced)
itm_dwarf_sword_a_good = (itm_dwarf_sword_a, imod_fine)

#Dwarf shield variants
itm_dwarf_shield_a_good = (itm_dwarf_shield_a, imod_reinforced)
itm_dwarf_shield_b_good = (itm_dwarf_shield_b, imod_reinforced)
itm_dwarf_shield_c_good = (itm_dwarf_shield_c, imod_reinforced)
itm_dwarf_shield_d_good = (itm_dwarf_shield_d, imod_reinforced)

#Orc helm variants
itm_orc_coif_good = (itm_orc_coif, imod_reinforced)
itm_orc_coif_bad = (itm_orc_coif, imod_cracked)
itm_orc_nosehelm_good = (itm_orc_nosehelm, imod_reinforced)
itm_orc_nosehelm_bad = (itm_orc_nosehelm, imod_cracked)
itm_orc_kettlehelm_good = (itm_orc_kettlehelm, imod_reinforced)
itm_orc_kettlehelm_bad = (itm_orc_kettlehelm, imod_cracked)
itm_orc_buckethelm_good = (itm_orc_buckethelm, imod_reinforced)
itm_orc_buckethelm_bad = (itm_orc_buckethelm, imod_cracked)
itm_orc_morion_good = (itm_orc_morion, imod_reinforced)
itm_orc_morion_bad = (itm_orc_morion, imod_cracked)
itm_orc_beakhelm_good = (itm_orc_beakhelm, imod_reinforced)
itm_orc_beakhelm_bad = (itm_orc_beakhelm, imod_cracked)
itm_orc_beakhelm_lordly = (itm_orc_beakhelm, imod_lordly)
itm_orc_bughelm_good = (itm_orc_bughelm, imod_reinforced)
itm_orc_bughelm_bad = (itm_orc_bughelm, imod_cracked)
itm_orc_bughelm_lordly = (itm_orc_bughelm, imod_lordly)
itm_orc_visorhelm_good = (itm_orc_visorhelm, imod_reinforced)
itm_orc_visorhelm_bad = (itm_orc_visorhelm, imod_cracked)

#Orc weapon variants
itm_uruk_falchion_a_heavy = (itm_uruk_falchion_a, imod_heavy)
itm_uruk_falchion_b_heavy = (itm_uruk_falchion_b, imod_heavy)
itm_uruk_falchion_b_bad = (itm_uruk_falchion_a, imod_crude)
itm_bone_cudgel_heavy = (itm_bone_cudgel, imod_heavy)
itm_orc_club_b_heavy = (itm_orc_club_b, imod_heavy)
itm_orc_club_d_bad = (itm_orc_club_d, imod_crude)
itm_orc_club_d_heavy = (itm_orc_club_d, imod_heavy)
itm_orc_simple_spear_heavy = (itm_orc_simple_spear, imod_heavy)
itm_orc_skull_spear_heavy = (itm_orc_skull_spear, imod_heavy)
itm_orc_bill_bad = (itm_orc_bill, imod_crude)
itm_orc_bill_heavy = (itm_orc_bill, imod_heavy)
itm_orc_slasher_heavy = (itm_orc_slasher, imod_heavy)
itm_orc_falchion_bad = (itm_orc_falchion, imod_crude)
itm_orc_falchion_heavy = (itm_orc_falchion, imod_heavy)
itm_orc_scimitar_bad = (itm_orc_scimitar, imod_crude)
itm_orc_scimitar_heavy = (itm_orc_scimitar, imod_heavy)
itm_orc_sabre_heavy = (itm_orc_sabre, imod_heavy)
itm_orc_sabre_bad = (itm_orc_sabre, imod_crude)
itm_orc_battle_axe_heavy = (itm_orc_battle_axe, imod_heavy)
itm_orc_two_handed_axe_heavy = (itm_orc_two_handed_axe, imod_heavy)

#Mordor Uruk armour variants
itm_m_uruk_light_a_good = (itm_m_uruk_light_a, imod_crude)
itm_m_uruk_light_a_bad = (itm_m_uruk_light_a, imod_reinforced)
itm_m_uruk_light_b_good = (itm_m_uruk_light_b, imod_crude)
itm_m_uruk_light_b_bad = (itm_m_uruk_light_b, imod_reinforced)
itm_m_uruk_light_c_good = (itm_m_uruk_light_c, imod_crude)
itm_m_uruk_light_c_bad = (itm_m_uruk_light_c, imod_reinforced)
itm_m_uruk_med_a_good = (itm_m_uruk_med_a, imod_crude)
itm_m_uruk_med_a_bad = (itm_m_uruk_med_a, imod_reinforced)
itm_m_uruk_med_b_good = (itm_m_uruk_med_b, imod_crude)
itm_m_uruk_med_b_bad = (itm_m_uruk_med_b, imod_reinforced)
itm_m_uruk_med_c_good = (itm_m_uruk_med_c, imod_crude)
itm_m_uruk_med_c_bad = (itm_m_uruk_med_c, imod_reinforced)
itm_m_uruk_heavy_a_good = (itm_m_uruk_heavy_a, imod_crude)
itm_m_uruk_heavy_a_bad = (itm_m_uruk_heavy_a, imod_reinforced)
itm_m_uruk_heavy_b_good = (itm_m_uruk_heavy_b, imod_crude)
itm_m_uruk_heavy_b_bad = (itm_m_uruk_heavy_b, imod_reinforced)
itm_m_uruk_heavy_c_good = (itm_m_uruk_heavy_c, imod_crude)
itm_m_uruk_heavy_c_bad = (itm_m_uruk_heavy_c, imod_reinforced)

#Rohan armour variants
itm_rohan_recruit_bad	 = (itm_rohan_recruit, imod_thick)
itm_rohan_recruit_good = (itm_rohan_recruit, imod_hardened)
itm_rohan_leather_bad = (itm_rohan_leather , imod_crude)
itm_rohan_leather_cloak = (itm_rohan_leather , imod_cloak)
itm_rohan_leather_good = (itm_rohan_leather , imod_thick)
itm_rohan_leather_good_cloak = (itm_rohan_leather , imod_reinforced)
itm_rohan_mail_bad = (itm_rohan_mail , imod_crude)
itm_rohan_mail_cloak = (itm_rohan_mail , imod_cloak)
itm_rohan_mail_good = (itm_rohan_mail , imod_thick)
itm_rohan_mail_good_cloak = (itm_rohan_mail , imod_reinforced)
itm_rohan_rider_bad = (itm_rohan_rider , imod_crude)
itm_rohan_rider_cloak = (itm_rohan_rider , imod_cloak)
itm_rohan_rider_good = (itm_rohan_rider , imod_thick)
itm_rohan_rider_good_cloak = (itm_rohan_rider , imod_reinforced)
itm_rohan_scale_bad = (itm_rohan_scale , imod_crude)
itm_rohan_scale_cloak = (itm_rohan_scale , imod_cloak)
itm_rohan_scale_good = (itm_rohan_scale , imod_thick)
itm_rohan_scale_good_cloak = (itm_rohan_scale , imod_reinforced)
itm_rohan_surcoat_bad = (itm_rohan_surcoat , imod_crude)
itm_rohan_surcoat_cloak = (itm_rohan_surcoat , imod_cloak)
itm_rohan_surcoat_good = (itm_rohan_surcoat , imod_thick)
itm_rohan_surcoat_good_cloak = (itm_rohan_surcoat , imod_reinforced)
itm_rohan_guard_bad = (itm_rohan_guard , imod_crude)
itm_rohan_guard_cloak = (itm_rohan_guard , imod_cloak)
itm_rohan_guard_good = (itm_rohan_guard , imod_reinforced)

#Rohan helms
itm_rohan_light_helmet_a_good = (itm_rohan_light_helmet_a, imod_reinforced)
itm_rohan_light_helmet_a_bad = (itm_rohan_light_helmet_a, imod_rusty)
itm_rohan_light_helmet_b_good = (itm_rohan_light_helmet_b, imod_reinforced)
itm_rohan_light_helmet_b_bad = (itm_rohan_light_helmet_b, imod_rusty)
itm_rohan_inf_helmet_a_good = (itm_rohan_inf_helmet_a, imod_reinforced)
itm_rohan_inf_helmet_a_bad = (itm_rohan_inf_helmet_a, imod_rusty)
itm_rohan_inf_helmet_b_lordly = (itm_rohan_inf_helmet_a, imod_lordly)
itm_rohan_inf_helmet_b_good = (itm_rohan_inf_helmet_b, imod_reinforced)
itm_rohan_inf_helmet_b_bad = (itm_rohan_inf_helmet_b, imod_rusty)
itm_rohan_archer_helmet_a_good = (itm_rohan_archer_helmet_a, imod_reinforced)
itm_rohan_archer_helmet_a_bad = (itm_rohan_archer_helmet_a, imod_rusty)
itm_rohan_archer_helmet_b_good = (itm_rohan_archer_helmet_b, imod_reinforced)
itm_rohan_archer_helmet_b_bad = (itm_rohan_archer_helmet_b, imod_rusty)
itm_rohan_archer_helmet_c_lordly = (itm_rohan_archer_helmet_c, imod_lordly)
itm_rohan_archer_helmet_c_good = (itm_rohan_archer_helmet_c, imod_reinforced)
itm_rohan_archer_helmet_c_bad = (itm_rohan_archer_helmet_c, imod_rusty)

#Rohan Super Warhorse
itm_thengel_warhorse_heavy = (itm_thengel_warhorse, imod_heavy)

#Northmen helms
itm_dale_helmet_a_good = (itm_dale_helmet_a, imod_reinforced)
itm_dale_helmet_b_good = (itm_dale_helmet_b, imod_reinforced)
itm_dale_helmet_c_good = (itm_dale_helmet_c, imod_reinforced)
itm_dale_helmet_d_good = (itm_dale_helmet_d, imod_reinforced)
itm_north_skullcap_bad = (itm_north_skullcap, imod_crude)
itm_north_skullcap_good = (itm_north_skullcap, imod_reinforced)
itm_north_leather_skullcap_good = (itm_north_leather_skullcap, imod_reinforced)
itm_north_leather_skullcap_bad = (itm_north_leather_skullcap, imod_crude)
itm_north_nasal_helm_good = (itm_north_nasal_helm, imod_reinforced)
#Northmen shields
itm_beorn_shield_good = (itm_beorn_shield, imod_thick)
itm_dale_shield_b_good = (itm_dale_shield_b, imod_thick)
itm_dale_shield_c_good = (itm_dale_shield_c, imod_thick)
#Dale armours #Note: Make sure that a version of each armour WITHOUT imod (not even imod_plain!) is used in a Dale troop's inventory. Otherwise, the armours don't show up in shops. (item factionization script doesn't find them?)
itm_north_leather_bad = (itm_north_leather, imod_ragged)
itm_north_leather_ok = (itm_north_leather, imod_plain)
itm_north_leather_good = (itm_north_leather, imod_thick)
itm_dale_light_a_ok = (itm_dale_light_a, imod_plain)
itm_dale_light_a_bad = (itm_dale_light_a, imod_ragged)
itm_dale_light_a_good = (itm_dale_light_a, imod_thick)
itm_dale_light_b_ok = (itm_dale_light_b, imod_plain)
itm_dale_light_b_cloak = (itm_dale_light_b, imod_cloak)
itm_dale_light_b_bad = (itm_dale_light_b, imod_ragged)
itm_dale_light_b_good = (itm_dale_light_b, imod_thick)
itm_dale_light_b_lordly = (itm_dale_light_b, imod_lordly)
itm_dale_med_a_ok = (itm_dale_med_a, imod_plain)
itm_dale_med_a_cloak = (itm_dale_med_a, imod_cloak)
itm_dale_med_a_bad = (itm_dale_med_a, imod_cracked)
itm_dale_med_a_good = (itm_dale_med_a, imod_reinforced)
itm_dale_med_a_lordly = (itm_dale_med_a, imod_lordly)
itm_dale_med_b_ok = (itm_dale_med_b, imod_plain)
itm_dale_med_b_bad = (itm_dale_med_b, imod_cracked)
itm_dale_med_b_good = (itm_dale_med_b, imod_reinforced)	
itm_dale_med_b_lordly = (itm_dale_med_b, imod_lordly)
itm_dale_med_c_ok = (itm_dale_med_c, imod_plain)
itm_dale_med_c_bad = (itm_dale_med_c, imod_cracked)
itm_dale_med_c_good = (itm_dale_med_c, imod_reinforced)	
itm_dale_med_c_cloak = (itm_dale_med_c, imod_lordly)
itm_dale_med_d_ok = (itm_dale_med_d, imod_plain)
itm_dale_med_d_bad = (itm_dale_med_d, imod_cracked)
itm_dale_med_d_good = (itm_dale_med_d, imod_reinforced)	
itm_dale_heavy_a_ok = (itm_dale_heavy_a, imod_plain)	
itm_dale_heavy_a_bad = (itm_dale_heavy_a, imod_cracked)	
itm_dale_heavy_a_good = (itm_dale_heavy_a, imod_thick)
itm_dale_heavy_a_pelt = (itm_dale_heavy_a, imod_lordly)	
itm_dale_heavy_b_ok = (itm_dale_heavy_b, imod_plain)	
itm_dale_heavy_b_bad = (itm_dale_heavy_b, imod_cracked)	
itm_dale_heavy_b_good = (itm_dale_heavy_b, imod_thick)
itm_dale_heavy_b_pelt = (itm_dale_heavy_b, imod_lordly)	
itm_dale_heavy_b_lordly = (itm_dale_heavy_b, imod_reinforced)
itm_dale_heavy_c_ok = (itm_dale_heavy_c, imod_plain)
itm_dale_heavy_c_good = (itm_dale_heavy_c, imod_reinforced)	

#Umbar armours
itm_umb_helm_a_good = (itm_umb_helm_a, imod_thick)
itm_umb_helm_b_good = (itm_umb_helm_b, imod_thick)
itm_umb_helm_c_good = (itm_umb_helm_c, imod_thick)
itm_umb_helm_d_good = (itm_umb_helm_d, imod_thick)
itm_umb_shield_e	= (itm_umb_shield_a, imod_thick)
itm_umb_armor_a_good = (itm_umb_armor_a, imod_reinforced)
itm_umb_armor_b_good = (itm_umb_armor_b, imod_reinforced)
itm_umb_armor_c_good = (itm_umb_armor_c, imod_reinforced)
itm_umb_armor_d_good = (itm_umb_armor_d, imod_reinforced)
itm_umb_armor_e_good = (itm_umb_armor_e, imod_reinforced)
itm_umb_armor_f_good = (itm_umb_armor_f, imod_reinforced)
itm_umb_armor_a_bad = (itm_umb_armor_a, imod_cracked)
itm_umb_armor_b_bad = (itm_umb_armor_b, imod_cracked)
itm_umb_armor_c_bad = (itm_umb_armor_c, imod_cracked)
itm_umb_armor_d_bad = (itm_umb_armor_d, imod_cracked)
itm_umb_armor_e_bad = (itm_umb_armor_e, imod_cracked)
itm_umb_armor_f_bad = (itm_umb_armor_f, imod_cracked)
itm_umb_armor_a_cloak = (itm_umb_armor_a, imod_cloak)
itm_umb_armor_b_cloak = (itm_umb_armor_b, imod_cloak)
itm_umb_armor_c_cloak = (itm_umb_armor_c, imod_cloak)
itm_umb_armor_d_cloak = (itm_umb_armor_d, imod_cloak)
itm_umb_armor_e_cloak = (itm_umb_armor_e, imod_cloak)
itm_umb_armor_f_cloak = (itm_umb_armor_f, imod_cloak)

#Gondor helms
itm_gondorian_light_helm = (itm_gondor_infantry_helm, imod_cracked)
itm_gondor_infantry_helm_bad = (itm_gondor_infantry_helm, imod_cracked)
itm_gondor_infantry_helm_good = (itm_gondor_infantry_helm, imod_thick)
itm_gondor_auxila_helm_bad = (itm_gondor_auxila_helm, imod_cracked)
itm_gondor_auxila_helm_good = (itm_gondor_auxila_helm, imod_thick)
itm_gondorian_light_helm_b = (itm_gondorian_archer_helm, imod_cracked)
itm_gondorian_archer_helm_bad = (itm_gondorian_archer_helm, imod_cracked)
itm_gondorian_archer_helm_good = (itm_gondorian_archer_helm, imod_thick)
itm_gondor_squire_helm = (itm_gondor_knight_helm, imod_cracked)
itm_gondor_knight_helm_bad = (itm_gondor_knight_helm, imod_cracked)
itm_gondor_knight_helm_good = (itm_gondor_knight_helm, imod_thick)
itm_gondor_dolamroth_helm_bad = (itm_gondor_dolamroth_helm, imod_cracked)
itm_gondor_dolamroth_helm_good = (itm_gondor_dolamroth_helm, imod_thick)

#Lorien armours
itm_lorien_archer_cloak = (itm_lorien_archer , imod_cloak)
itm_lorien_archer_good = (itm_lorien_archer , imod_thick)
itm_lorien_archer_good_cloak = (itm_lorien_archer , imod_lordly)
itm_lorien_light = itm_lorien_armor_a
itm_lorien_light_bad = (itm_lorien_armor_a , imod_crude)
itm_lorien_light_cloak = (itm_lorien_armor_a , imod_cloak)
itm_lorien_light_good = (itm_lorien_armor_a , imod_thick)
itm_lorien_light_good_cloak = (itm_lorien_armor_a , imod_lordly)
itm_lorien_med = itm_lorien_armor_b
itm_lorien_med_bad = (itm_lorien_armor_b , imod_crude)
itm_lorien_med_cloak = (itm_lorien_armor_b , imod_cloak)
itm_lorien_med_good = (itm_lorien_armor_b , imod_thick)
itm_lorien_med_good_cloak = (itm_lorien_armor_b , imod_lordly)
itm_lorien_heavy = itm_lorien_armor_c
itm_lorien_heavy_bad = (itm_lorien_armor_c , imod_crude)
itm_lorien_heavy_cloak = (itm_lorien_armor_c , imod_cloak)
itm_lorien_heavy_good = (itm_lorien_armor_c , imod_thick)
itm_lorien_heavy_good_cloak = (itm_lorien_armor_c , imod_lordly)
itm_lorien_helm_a_good = (itm_lorien_helm_a, imod_thick)
itm_lorien_helm_b_good = (itm_lorien_helm_b, imod_thick)


#Khand helms
itm_khand_inf_helm_a_good = (itm_khand_inf_helm_a, imod_reinforced)
itm_khand_inf_helm_a_bad = (itm_khand_inf_helm_a, imod_cracked)
itm_khand_inf_helm_b_good = (itm_khand_inf_helm_b, imod_reinforced)
itm_khand_inf_helm_b_bad = (itm_khand_inf_helm_b, imod_cracked)
itm_khand_inf_helm_c1_good = (itm_khand_inf_helm_c1, imod_reinforced)
itm_khand_inf_helm_c1_bad = (itm_khand_inf_helm_c1, imod_cracked)
itm_khand_inf_helm_c2_good = (itm_khand_inf_helm_c2, imod_reinforced)
itm_khand_inf_helm_c2_bad = (itm_khand_inf_helm_c2, imod_cracked)
itm_khand_inf_helm_d_good = (itm_khand_inf_helm_d, imod_reinforced)
itm_khand_inf_helm_d_bad = (itm_khand_inf_helm_d, imod_cracked)
itm_khand_cav_helm_a_good = (itm_khand_cav_helm_a, imod_reinforced)
itm_khand_cav_helm_a_bad = (itm_khand_cav_helm_a, imod_cracked)
itm_khand_cav_helm_b_good = (itm_khand_cav_helm_b, imod_reinforced)
itm_khand_cav_helm_c_good = (itm_khand_cav_helm_c, imod_reinforced)
itm_khand_helm_mask_good = (itm_khand_helm_mask, imod_reinforced)

#Khand armours
itm_khand_light_good = (itm_khand_light, imod_reinforced)
itm_khand_light_bad = (itm_khand_light, imod_crude)
itm_khand_light_lam_good = (itm_khand_light_lam, imod_reinforced)
itm_khand_light_lam_bad = (itm_khand_light_lam, imod_cracked)
itm_khand_foot_lam_good = (itm_khand_foot_lam, imod_reinforced)
itm_khand_foot_lam_bad = (itm_khand_foot_lam, imod_cracked)
itm_khand_med_lam_good = (itm_khand_med_lam, imod_reinforced)
itm_khand_med_lam_bad = (itm_khand_med_lam, imod_cracked)
itm_khand_heavy_lam_good = (itm_khand_heavy_lam, imod_reinforced)
itm_khand_heavy_lam_bad = (itm_khand_heavy_lam, imod_cracked)
itm_khand_noble_lam = (itm_khand_heavy_lam, imod_lordly)

#Mirkwood Helms
itm_mirkwood_helm_a_bad = (itm_mirkwood_helm_a, imod_cracked)
itm_mirkwood_helm_a_good = (itm_mirkwood_helm_a, imod_reinforced)
itm_mirkwood_helm_b_good = (itm_mirkwood_helm_b, imod_reinforced)
itm_mirkwood_helm_c_good = (itm_mirkwood_helm_c, imod_reinforced)
itm_mirkwood_helm_d_good = (itm_mirkwood_helm_d, imod_reinforced)

#Mirkwood armours
itm_mirkwood_leather_bad = (itm_mirkwood_leather, imod_cracked)
itm_mirkwood_leather_good = (itm_mirkwood_leather, imod_reinforced)
itm_mirkwood_pad_bad = (itm_mirkwood_pad, imod_cracked)
itm_mirkwood_pad_good = (itm_mirkwood_pad, imod_reinforced)
itm_mirkwood_mail_bad = (itm_mirkwood_mail, imod_cracked)
itm_mirkwood_mail_good = (itm_mirkwood_mail, imod_reinforced)
itm_mirkwood_scale_bad = (itm_mirkwood_scale, imod_cracked)
itm_mirkwood_scale_good = (itm_mirkwood_scale, imod_reinforced)
itm_mirkwood_heavy_scale_bad = (itm_mirkwood_heavy_scale, imod_cracked)
itm_mirkwood_heavy_scale_good = (itm_mirkwood_heavy_scale, imod_reinforced)

#Rivendell armours
itm_riv_armor_light = itm_riv_light
itm_riv_armor_light_inf = itm_riv_surcoat
itm_riv_armor_archer = itm_riv_leather
itm_riv_armor_m_archer = itm_riv_foot_mail
itm_riv_armor_med = (itm_riv_surcoat, imod_reinforced)
itm_riv_armor_heavy = itm_mirkwood_leather
itm_riv_armor_h_archer = itm_riv_knight
itm_riv_armor_leader = (itm_riv_knight, imod_lordly)

itm_riv_light_cloak = (itm_riv_light, imod_cloak)
itm_riv_leather_cloak = (itm_riv_leather, imod_cloak)
itm_riv_foot_mail_cloak = (itm_riv_foot_mail, imod_cloak) #28
itm_riv_foot_mail_good = (itm_riv_foot_mail, imod_reinforced) #32
itm_riv_foot_mail_lordly = (itm_riv_foot_mail, imod_lordly) #34
itm_riv_foot_scale_cloak = (itm_riv_foot_scale, imod_cloak) #36
itm_riv_foot_scale_good = (itm_riv_foot_scale, imod_reinforced) #40
itm_riv_foot_scale_lordly = (itm_riv_foot_scale, imod_lordly) #42
itm_riv_surcoat_cloak = (itm_riv_surcoat, imod_cloak) #30
itm_riv_surcoat_good = (itm_riv_surcoat, imod_reinforced) #34
itm_riv_surcoat_lordly = (itm_riv_surcoat, imod_lordly) #36
itm_riv_knight_cloak = (itm_riv_knight, imod_cloak) #38
itm_riv_knight_good = (itm_riv_knight, imod_reinforced) #42
itm_riv_knight_lordly = (itm_riv_knight, imod_lordly) #44

itm_riv_shield_a_good = (itm_riv_shield_a, imod_reinforced)
itm_riv_shield_b_good = (itm_riv_shield_b, imod_reinforced)

#Beorning armour variants
itm_woodman_tunic_bad			= (itm_woodman_tunic, imod_crude)
itm_woodman_tunic_cloak			= (itm_woodman_tunic, imod_cloak)
itm_woodman_tunic_good			= (itm_woodman_tunic, imod_thick)
itm_woodman_tunic_good_cloak	= (itm_woodman_tunic, imod_lordly)
itm_woodman_scout_bad			= (itm_woodman_scout, imod_cracked)
itm_woodman_scout_cloak			= (itm_woodman_scout, imod_cloak)
itm_woodman_scout_good			= (itm_woodman_scout, imod_reinforced)
itm_woodman_scout_good_cloak	= (itm_woodman_scout, imod_lordly)
itm_woodman_padded_bad			= (itm_woodman_padded, imod_cracked)
itm_woodman_padded_cloak		= (itm_woodman_padded, imod_cloak)
itm_woodman_padded_good			= (itm_woodman_padded, imod_reinforced)
itm_woodman_padded_good_cloak	= (itm_woodman_padded, imod_lordly)
itm_woodmen_heavy_bad			= (itm_woodmen_heavy, imod_cracked)
itm_woodmen_heavy_cloak			= (itm_woodmen_heavy, imod_cloak)
itm_woodmen_heavy_good			= (itm_woodmen_heavy, imod_reinforced)
itm_woodmen_heavy_good_cloak	= (itm_woodmen_heavy, imod_lordly)

itm_beorn_tunic_bad				= (itm_beorn_tunic, imod_crude)
itm_beorn_tunic_good			= (itm_beorn_tunic, imod_thick)
itm_beorn_padded_bad			= (itm_beorn_padded, imod_crude)
itm_beorn_padded_good			= (itm_beorn_padded, imod_reinforced)
itm_beorn_heavy_bad				= (itm_beorn_heavy, imod_cracked)
itm_beorn_heavy_good			= (itm_beorn_heavy, imod_reinforced)
itm_beorn_berserk_bad			= (itm_beorn_berserk, imod_cracked)
itm_beorn_berserk_good			= (itm_beorn_berserk, imod_reinforced)
itm_beorn_helmet_light			= (itm_beorn_helmet, imod_cracked)

#Rhun helms
itm_rhun_helm_barbed_good = (itm_rhun_helm_barbed, imod_reinforced)
itm_rhun_helm_barbed_bad = (itm_rhun_helm_barbed, imod_cracked)
itm_rhun_helm_horde_good = (itm_rhun_helm_horde, imod_reinforced)
itm_rhun_helm_horde_bad = (itm_rhun_helm_horde, imod_cracked)
itm_rhun_helm_pot_good = (itm_rhun_helm_pot, imod_reinforced)
itm_rhun_helm_pot_bad = (itm_rhun_helm_pot, imod_cracked)
itm_rhun_helm_round_good = (itm_rhun_helm_round, imod_reinforced)
itm_rhun_helm_round_bad = (itm_rhun_helm_round, imod_cracked)
itm_rhun_helm_leather_good = (itm_rhun_helm_leather, imod_reinforced)
itm_rhun_helm_leather_bad = (itm_rhun_helm_leather, imod_cracked)
itm_rhun_helm_chieftain_good = (itm_rhun_helm_chieftain, imod_reinforced)
itm_rhun_helm_chieftain_bad = (itm_rhun_helm_chieftain, imod_cracked)

#Rhun armour
itm_rhun_armor_g_good = (itm_rhun_armor_g, imod_reinforced)
itm_rhun_armor_g_bad = (itm_rhun_armor_g, imod_cracked)
itm_rhun_armor_h_good = (itm_rhun_armor_h, imod_reinforced)
itm_rhun_armor_h_bad = (itm_rhun_armor_h, imod_cracked)
itm_rhun_armor_p_good = (itm_rhun_armor_p, imod_reinforced)
itm_rhun_armor_p_bad = (itm_rhun_armor_p, imod_cracked)
itm_rhun_armor_k_good = (itm_rhun_armor_k, imod_reinforced)
itm_rhun_armor_k_bad = (itm_rhun_armor_k, imod_cracked)

#Isengard Uruk armours
itm_isen_uruk_light_a_good = (itm_isen_uruk_light_a, imod_reinforced)
itm_isen_uruk_light_a_bad = (itm_isen_uruk_light_a, imod_cracked) #urukhai_isen_light_harness_a
itm_isen_uruk_light_b_good = (itm_isen_uruk_light_b, imod_reinforced)
itm_isen_uruk_light_b_bad = (itm_isen_uruk_light_b, imod_cracked) #urukhai_isen_med_harness_a
itm_isen_uruk_light_c_good = (itm_isen_uruk_light_c, imod_reinforced)
itm_isen_uruk_light_c_bad = (itm_isen_uruk_light_c, imod_cracked) #berserker
itm_isen_uruk_med_a_good = (itm_isen_uruk_med_a, imod_reinforced)
itm_isen_uruk_med_a_bad = (itm_isen_uruk_med_a, imod_cracked) #urukhai_isen_med_pad_a
itm_isen_uruk_med_b_good = (itm_isen_uruk_med_b, imod_reinforced)
itm_isen_uruk_med_b_bad = (itm_isen_uruk_med_b, imod_cracked) #urukhai_isen_med_mail_a
itm_isen_uruk_heavy_a_good = (itm_isen_uruk_heavy_a, imod_reinforced)
itm_isen_uruk_heavy_a_bad = (itm_isen_uruk_heavy_a, imod_cracked) #urukhai_isen_heavy_pad_a
itm_isen_uruk_heavy_b_good = (itm_isen_uruk_heavy_b, imod_reinforced)
itm_isen_uruk_heavy_b_bad = (itm_isen_uruk_heavy_b, imod_cracked) #urukhai_isen_heavy_mail_a
itm_isen_uruk_heavy_c_good = (itm_isen_uruk_heavy_c, imod_reinforced)
itm_isen_uruk_heavy_c_bad = (itm_isen_uruk_heavy_c, imod_cracked) #urukhai_isen_plate_a
itm_isen_uruk_heavy_d_good = (itm_isen_uruk_heavy_d, imod_reinforced)
itm_isen_uruk_heavy_d_bad = (itm_isen_uruk_heavy_d, imod_cracked) #tracker
itm_isen_uruk_heavy_e_good = (itm_isen_uruk_heavy_e, imod_reinforced)
itm_isen_uruk_heavy_e_bad = (itm_isen_uruk_heavy_e, imod_cracked) #tracker

itm_isen_orc_light_a_good = (itm_isen_orc_light_a, imod_reinforced)
itm_isen_orc_light_a_bad = (itm_isen_orc_light_a, imod_cracked)
itm_isen_orc_light_b_good = (itm_isen_orc_light_b, imod_reinforced)
itm_isen_orc_light_b_bad = (itm_isen_orc_light_b, imod_cracked)
itm_isen_orc_pad_a_good = (itm_isen_orc_pad_a, imod_reinforced)
itm_isen_orc_pad_a_bad = (itm_isen_orc_pad_a, imod_cracked)
itm_isen_orc_pad_b_good = (itm_isen_orc_pad_b, imod_reinforced)
itm_isen_orc_pad_b_bad = (itm_isen_orc_pad_b, imod_cracked)
itm_isen_orc_mail_a_good = (itm_isen_orc_mail_a, imod_reinforced)
itm_isen_orc_mail_a_bad = (itm_isen_orc_mail_a, imod_cracked)
itm_isen_orc_mail_b_good = (itm_isen_orc_mail_b, imod_reinforced)
itm_isen_orc_mail_b_bad = (itm_isen_orc_mail_b, imod_cracked)

# helmets
itm_isen_orc_helm_a_good = (itm_isen_orc_helm_a, imod_reinforced)
itm_isen_orc_helm_a_bad = (itm_isen_orc_helm_a, imod_cracked)
itm_isen_uruk_helm_a_good = (itm_isen_uruk_helm_a, imod_reinforced)
itm_isen_uruk_helm_a_bad = (itm_isen_uruk_helm_a, imod_cracked) #tracker
itm_isen_tracker_helm = itm_isen_uruk_helm_e
itm_isen_tracker_helm_good = (itm_isen_uruk_helm_e, imod_reinforced)
itm_isen_tracker_helm_bad = (itm_isen_uruk_helm_e, imod_cracked) #tracker

# harad swords
itm_black_snake_sword_good = (itm_black_snake_sword, imod_balanced)
itm_black_snake_sword_bad = (itm_black_snake_sword, imod_crude)
itm_harad_heavy_sword_good = (itm_harad_heavy_sword, imod_balanced)
itm_harad_heavy_sword_bad = (itm_harad_heavy_sword, imod_crude)
itm_harad_sabre_good = (itm_harad_sabre, imod_balanced)
itm_harad_sabre_bad = (itm_harad_sabre, imod_crude)

# 0x000000018000004136db6db6db6db6db00000000001db6db0000000000000000  default player face
# 0x000000018000000136db6db6db6db6db00000000001db6db0000000000000000  bearded player face
 
troops = [
["player","Player","Player",tf_hero|tf_unmoveable_in_party_window,0,0,fac_player_faction,[],      str_4|agi_4|int_4|cha_4,wp(15),0,0x000000018000004136db6db6db6db6db00000000001db6db0000000000000000],
["temp_troop","Temp_Troop","Temp_Troop",tf_hero,0,0,fac_commoners,[],0,0,knows_common|knows_inventory_management_10,0],
["game","Game","Game",tf_hero,0,0,fac_commoners, [],0,0,0,0],
["unarmed_troop","Unarmed_Troop","Unarmed_Troops",tf_hero,0,0,fac_commoners,[itm_arrows,itm_short_bow],def_attrib|str_14,0,knows_common|knows_power_draw_2,0],
####################################################################################################################
# Troops before this point are hardwired into the game and their order should not be changed!
####################################################################################################################
["temp_troop_2","Temp_Troop_2","Temp_Troop_2",tf_hero,0,0,fac_commoners,   [],      0,0,knows_common|knows_inventory_management_10,0],
["random_town_sequence","Random_Town_Sequence","Random_Town_Sequence",tf_hero,0,0,fac_neutral,[],0,0,0,0],
["tournament_participants","Tournament_Participants","Tournament_Participants",tf_hero,0,0,fac_commoners,[],0,0,0,0],
 
["tutorial_maceman","Maceman","Macemen",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,itm_wood_club,itm_black_tunic],
      attr_tier_1,wp_tier_1,knows_common,mercenary_face_1,mercenary_face_2],
["tutorial_archer","Archer","Archers",tfg_boots| tfg_armor| tfg_ranged,0,0,fac_commoners,
   [itm_leather_boots,itm_short_bow,itm_arrows,itm_black_tunic],
      attr_tier_1,wp_tier_1,knows_common|knows_power_draw_4,mercenary_face_1,mercenary_face_2],
["tutorial_swordsman","Swordsman","Swordsmen",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,itm_black_tunic,itm_practice_sword],
      attr_tier_1,wp_tier_1,knows_common,mercenary_face_1,mercenary_face_2],
["novice_fighter","Novice_Fighter","Novice_Fighters",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,  ],
      attr_tier_1,wp_tier_1,knows_common,mercenary_face_1,mercenary_face_2],
["regular_fighter","Regular_Fighter","Regular_Fighters",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,],
      attr_tier_2,wp_tier_2,knows_common|knows_ironflesh_1|knows_power_strike_1|knows_athletics_1|knows_riding_1|knows_shield_2,mercenary_face_1,mercenary_face_2],
["veteran_fighter","Veteran_Fighter","Veteran_Fighters",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,],
      attr_tier_3,wp_tier_3,knows_common|knows_ironflesh_3|knows_power_strike_2|knows_athletics_2|knows_riding_2|knows_shield_3,mercenary_face_1,mercenary_face_2],
["champion_fighter","Champion_Fighter","Champion_Fighters",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,],
      attr_tier_4,wp_tier_4,knows_common|knows_ironflesh_4|knows_power_strike_3|knows_athletics_3|knows_riding_3|knows_shield_4,mercenary_face_1,mercenary_face_2],
["arena_training_fighter_1","Novice_Fighter","Novice_Fighters",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,mercenary_face_1,mercenary_face_2],
["arena_training_fighter_2","Novice_Fighter","Novice_Fighters",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,mercenary_face_1,mercenary_face_2],
["arena_training_fighter_3","Regular_Fighter","Regular_Fighters",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,],
      attr_tier_3,wp_tier_3,knows_common,mercenary_face_1,mercenary_face_2],
["arena_training_fighter_4","Regular_Fighter","Regular_Fighters",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,],
      attr_tier_3,wp_tier_3,knows_common,mercenary_face_1,mercenary_face_2],
["arena_training_fighter_5","Regular_Fighter","Regular_Fighters",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,],
      attr_tier_3,wp_tier_3,knows_common,mercenary_face_1,mercenary_face_2],
["arena_training_fighter_6","Veteran_Fighter","Veteran_Fighters",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,],
      attr_tier_3,wp_tier_3,knows_common,mercenary_face_1,mercenary_face_2],
["arena_training_fighter_7","Veteran_Fighter","Veteran_Fighters",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,],
      attr_tier_3,wp_tier_3,knows_common,mercenary_face_1,mercenary_face_2],
["arena_training_fighter_8","Veteran_Fighter","Veteran_Fighters",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,],
      attr_tier_3,wp_tier_3,knows_common,mercenary_face_1,mercenary_face_2],
["arena_training_fighter_9","Champion_Fighter","Champion_Fighters",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,],
      attr_tier_3,wp_tier_3,knows_common,mercenary_face_1,mercenary_face_2],
["arena_training_fighter_10","Champion_Fighter","Champion_Fighters",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,],
      attr_tier_3,wp_tier_3,knows_common,mercenary_face_1,mercenary_face_2],
["cattle","Cattle","Cattle",0,0,0,fac_neutral,   [],      0,0,0,0],
#soldiers:
#This troop is the troop marked as soldiers_begin
["farmer","Farmer","Farmers",tfg_armor|tfg_boots,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots, itm_practice_staff],
      attr_tier_1,wp_tier_1,knows_common,man_face_middle_1,man_face_old_2,man_face_older_2],

## Dale Walkers
 ] + (is_a_wb_troop==1 and [
["townsman","Townsman","Townsmen",tfg_boots| tfg_armor,0,0,fac_dale,
   [itm_corsair_boots, itm_leather_boots,itm_leather_boots_dark_bad, itm_rohan_shoes,
   itm_fur_coat_wb, itm_leather_jerkin_wb, itm_black_tunic_wb, itm_lossarnach_shirt, itm_nobleman_outfit_b_new_wb, itm_peasant_man_a_wb, itm_white_tunic_c_wb, itm_red_tunic_wb, itm_sar_robe_b_wb,
   itm_hood_black, itm_hood_grey_bad, itm_fur_hat_a_new_wb, itm_noel_hat_a_wb],
      attr_tier_1,wp_tier_1,knows_common,swadian_face_younger_1,swadian_face_old_2],
["watchman","Townswoman","Townswomen",tf_female| tfg_boots| tfg_armor,0,0,fac_dale,
   [itm_gondor_ranger_hood, itm_wimple_a_wb, itm_wimple_with_veil, itm_fur_hat_a_new_wb, 
   itm_robe_generic_dress_wb, itm_black_dress_wb,itm_rohan_fine_outfit_dale_dress_wb,itm_green_dress_wb,itm_peasant_dress_b_new_wb,
   itm_rohan_shoes_good],
      attr_tier_1,wp_tier_1,knows_common,rohan_woman_face_1,rohan_woman_face_2],      
] or [
["townsman","Townsman","Townsmen",tfg_boots| tfg_armor,0,0,fac_dale,
   [itm_corsair_boots, itm_black_tunic, itm_lossarnach_shirt,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,mercenary_face_1,mercenary_face_2],
["watchman","Townswoman","Townswomen",tf_female| tfg_boots| tfg_armor,0,0,fac_dale,
   [itm_gondor_ranger_hood,itm_black_tunic, itm_rohan_shoes,itm_leather_boots],
      attr_tier_1,wp_tier_1,knows_common,rohan_woman_face_1,rohan_woman_face_2],
]) + [ 

["mercenaries_end","bug","bug",0,0,0,fac_commoners,
   [],
      0,1,0,0],
#soldiers:
#######################################
#@@@@@@@@@@@@%%%%%%%%%%%%%%%%%%

#Woodmen
["i1_woodmen_man","Woodmen_Settler","Woodmen_Settlers",tfg_armor| tfg_boots,0,0,fac_beorn,[itm_gondor_ranger_hood,itm_woodman_tunic_bad, itm_woodman_scout_bad,itm_rohan_shoes,itm_short_bow,itm_arrows,itm_beorn_staff, itm_axe_a,],attr_tier_1,wp_tier_1,knows_common|knows_ironflesh_1|knows_power_strike_1|knows_power_draw_1|knows_athletics_2|knows_looting_1|knows_tracking_1|knows_pathfinding_1|knows_spotting_2|knows_inventory_management_1|knows_wound_treatment_1|knows_persuasion_1,rohan_face_younger_1,rohan_face_middle_2],
["i2_woodmen_forester","Woodmen_Forester","Woodmen_Foresters",tfg_armor| tfg_boots,0,0,fac_beorn,[itm_gondor_ranger_hood,itm_woodman_tunic_good, itm_woodman_scout, itm_woodman_padded_bad,itm_furry_boots,itm_beorn_staff, itm_axe_a,],attr_tier_2,wp_tier_2,knows_common|knows_ironflesh_2|knows_power_strike_2|knows_power_draw_1|knows_athletics_2|knows_looting_1|knows_tracking_1|knows_pathfinding_1|knows_spotting_2|knows_inventory_management_1|knows_wound_treatment_1|knows_persuasion_1 ,rohan_face_young_1,rohan_face_middle_2],
["i3_woodmen_skilled_forester","Woodmen_Skilled_Forester","Woodmen_Skilled_Foresters",tfg_armor| tfg_boots,0,0,fac_beorn,[itm_north_leather_skullcap, itm_north_leather_skullcap_bad,itm_woodman_scout_good, itm_woodman_padded, itm_leather_boots_bad,itm_rohan_shoes,itm_long_bearded_axe,],attr_tier_3,wp_tier_3,knows_common|knows_athletics_3|knows_power_strike_3|knows_ironflesh_3,rohan_face_young_1,rohan_face_middle_2],
["i4_woodmen_axemen","Woodmen_Axeman","Woodmen_Axemen",tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,[itm_north_leather_skullcap, itm_north_leather_skullcap_bad,itm_north_leather_skullcap_good, itm_north_skullcap,itm_woodman_padded_good, itm_woodmen_heavy_bad,itm_evil_gauntlets_a,itm_leather_boots,itm_long_bearded_axe,],attr_tier_4,wp_tier_4,knows_common|knows_athletics_4|knows_power_strike_4|knows_ironflesh_4,rohan_face_young_1,rohan_face_old_2],
["i5_woodmen_night_guard","Night_Guard_of_Mirkwood","Night_Guards_of_Mirkwood",tfg_armor| tfg_helm| tfg_boots| tfg_gloves,0,0,fac_beorn,[itm_north_leather_skullcap_good, itm_north_skullcap, itm_north_nasal_helm_good,itm_woodmen_heavy,itm_leather_boots,itm_leather_boots,itm_2_handed_axe,],attr_tier_5,wp_tier_5,knows_common|knows_athletics_5|knows_power_strike_6|knows_ironflesh_6,rohan_face_middle_1,rohan_face_old_2],
["a2_woodmen_tracker","Woodmen_Tracker","Woodmen_Trackers",tfg_ranged| tfg_armor| tfg_boots,0,0,fac_beorn,[itm_gondor_ranger_hood,itm_woodman_tunic_cloak,itm_leather_boots_bad,itm_rohan_shoes,itm_furry_boots,itm_short_bow,itm_arrows,itm_beorn_staff, itm_axe_a,],attr_tier_2,wp_tier_bow_2,knows_common|knows_ironflesh_1|knows_power_strike_1|knows_power_draw_2|knows_athletics_3|knows_looting_1|knows_tracking_1|knows_pathfinding_1|knows_spotting_2|knows_inventory_management_1|knows_wound_treatment_1|knows_persuasion_1,rohan_face_young_1,rohan_face_old_2],
["a3_woodmen_scout","Woodmen_Scout","Woodmen_Scouts",tfg_ranged| tfg_armor| tfg_boots,0,0,fac_beorn,[itm_gondor_ranger_hood, itm_north_leather_skullcap_bad,itm_woodman_tunic_good_cloak, itm_woodman_scout_cloak,itm_leather_boots_bad,itm_furry_boots,itm_regular_bow,itm_arrows,itm_axe_a, itm_axe_b, itm_beorn_staff,itm_long_bearded_axe,],attr_tier_3,wp_tier_bow_3,knows_common|knows_athletics_3|knows_power_draw_2|knows_power_strike_1|knows_ironflesh_1,rohan_face_young_1,rohan_face_middle_2],
["a4_woodmen_archer","Woodmen_Archer","Woodmen_Archers",tfg_ranged| tfg_armor| tfg_helm|tfg_boots| tfg_gloves,0,0,fac_beorn,[itm_gondor_ranger_hood, itm_north_leather_skullcap_bad, itm_north_leather_skullcap,itm_woodman_scout_good_cloak, itm_woodman_padded_cloak,itm_leather_gloves,itm_evil_gauntlets_a,itm_leather_boots,itm_regular_bow,itm_arrows,itm_axe_b, itm_beorn_staff,itm_long_bearded_axe,],attr_tier_4,wp_tier_bow_5,knows_common|knows_athletics_4|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_2,rohan_face_young_1,rohan_face_old_2],
["a5_woodmen_night_stalker","Night_Stalker_of_Mirkwood","Night_Stalkers_of_Mirkwood",tfg_ranged| tfg_gloves| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,[itm_north_leather_skullcap, itm_north_leather_skullcap_bad,itm_north_leather_skullcap_good, itm_north_skullcap,itm_woodman_padded_good_cloak, itm_leather_boots,itm_leather_boots,itm_elven_bow,itm_arrows,itm_long_bearded_axe,itm_long_bearded_axe,itm_beorn_staff,],attr_tier_5,wp_archery(210)|wp_melee(150),knows_common|knows_athletics_6|knows_power_draw_4|knows_power_strike_3|knows_ironflesh_4,rohan_face_middle_1,rohan_face_old_2],

#Beornings
["i1_beorning_man","Beorning_Man","Beorning_Men",tfg_armor,0,0,fac_beorn,[itm_gondor_ranger_hood,itm_beorn_tunic_bad,itm_furry_boots,itm_beorn_staff,itm_beorn_axe,itm_dwarf_sword_b,],attr_tier_1,wp_tier_1,knows_common|knows_ironflesh_3|knows_power_strike_1|knows_athletics_3|knows_tracking_2|knows_pathfinding_1|knows_spotting_1|knows_surgery_1|knows_persuasion_1|knows_trade_1,beorn_face1,beorn_face2],
["i2_beorning_warrior","Beorning_Warrior","Beorning_Warriors",tfg_armor| tfg_boots,0,0,fac_beorn,[itm_north_skullcap,itm_gondor_ranger_hood,itm_beorn_tunic,itm_beorn_padded_bad,itm_furry_boots,itm_beorn_axe,itm_dwarf_sword_b,itm_beorn_shield,itm_north_round_shield,],attr_tier_2,wp_tier_2,knows_common|knows_ironflesh_3|knows_power_strike_2|knows_athletics_4|knows_tracking_2|knows_pathfinding_1|knows_spotting_1|knows_surgery_1|knows_persuasion_1|knows_trade_1,beorn_face1,beorn_face2],
["i3_beorning_tolltacker","Beorning_Toll-Taker","Beorning_Toll-Takers",tfg_armor| tfg_boots|tfg_shield,0,0,fac_beorn,[itm_north_skullcap,itm_beorn_helmet_light,itm_beorn_padded, itm_beorn_heavy_bad,itm_furry_boots,itm_dwarf_sword_b,itm_beorn_shield,itm_north_round_shield,itm_rohirrim_throwing_axe,],attr_tier_3,wp_tier_3,knows_common|knows_athletics_4|knows_power_strike_3|knows_ironflesh_4|knows_power_throw_2,beorn_face1,beorn_face2],
["i4_beorning_sentinel","Beorning_Sentinel","Beorning_Sentinels",tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,[itm_north_skullcap,itm_beorn_helmet_light,itm_beorn_heavy,itm_leather_boots,itm_dwarf_sword_b,itm_dale_sword,itm_beorn_shield,itm_beorn_shield_good,itm_rohirrim_throwing_axe,],attr_tier_4,wp_tier_4,knows_common|knows_athletics_4|knows_power_strike_3|knows_ironflesh_5|knows_shield_3|knows_power_throw_2,beorn_face1,beorn_face2],
["i5_beorning_warden_of_the_ford","Beorning_Warden_of_the_Ford","Beorning_Wardens_of_the_Ford",tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,[itm_north_skullcap,itm_beorn_helmet, itm_beorn_heavy_good,itm_leather_gloves,itm_leather_boots,itm_dwarf_sword_a,itm_dwarf_sword_b,itm_dale_sword,itm_dale_sword_long,itm_beorn_shield_good,],attr_tier_5,wp_tier_5,knows_common|knows_athletics_5|knows_power_strike_3|knows_ironflesh_6|knows_shield_5|knows_power_throw_3,beorn_face1,beorn_face2],
["i3_beorning_carrock_lookout","Beorning_Carrock_Lookout","Beorning_Carrock_Lookouts",tfg_armor| tfg_boots,0,0,fac_beorn,[itm_north_skullcap,itm_beorn_helmet_light,itm_beorn_tunic_good,itm_beorn_padded_bad,itm_beorn_berserk_bad,itm_furry_boots,itm_beorn_axe,itm_javelin,],attr_tier_3,wp_tier_3,knows_common|knows_athletics_6|knows_power_strike_4|knows_ironflesh_6|knows_power_throw_2,beorn_face1,beorn_face2],
["i4_beorning_carrock_fighter","Beorning_Carrock_Fighter","Beorning_Carrock_Fighters",tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,[itm_beorn_helmet,itm_beorn_helmet_light,itm_beorn_padded, itm_beorn_berserk,itm_furry_boots,itm_beorn_axe,itm_beorn_battle_axe,itm_javelin,itm_javelin,],attr_tier_4,wp_tier_4,knows_common|knows_athletics_7|knows_power_strike_5|knows_ironflesh_7|knows_power_throw_4,beorn_face1,beorn_face2],
["i5_beorning_carrock_berserker","Beorning_Carrock_Berserker","Beorning_Carrock_Berserkers",tfg_gloves| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,[itm_beorn_helmet,itm_beorn_padded_good,itm_beorn_berserk_good,itm_furry_boots,itm_beorn_battle_axe,itm_javelin,itm_javelin,],attr_tier_5,wp_tier_6,knows_common|knows_athletics_8|knows_power_strike_7|knows_ironflesh_9|knows_power_throw_6,beorn_face1,beorn_face2],

["northmen_items","BUG","_",tf_hero,0,0,fac_beorn,
   [itm_leather_gloves,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,itm_sumpter_horse,itm_saddle_horse,],
      0,0,0,0],
#Dale
["i1_dale_militia","Dale_Militiaman","Dale_Militia",tfg_boots| tfg_armor,0,0,fac_dale,[itm_north_leather_skullcap, itm_north_leather_skullcap_bad,itm_hood_grey_bad,itm_north_leather,itm_dale_light_a_bad,itm_rohan_shoes,itm_dale_pike, itm_dale_sword, itm_arrows,itm_short_bow,itm_axe_a,itm_north_round_shield,],attr_tier_1,wp_tier_1,knows_common|knows_ironflesh_1|knows_power_draw_2|knows_shield_1|knows_looting_1|knows_trainer_1|knows_tactics_1|knows_spotting_1|knows_inventory_management_1|knows_wound_treatment_1|knows_prisoner_management_1|knows_trade_2,swadian_face_younger_1,swadian_face_middle_2],
["i2_dale_man_at_arms","Dale_Man-at-Arms","Dale_Men-at-Arms",tfg_shield| tfg_boots| tfg_armor| tfg_helm,0,0,fac_dale,[itm_north_leather_skullcap, itm_north_leather_skullcap_good, itm_north_skullcap, itm_north_skullcap_good, itm_dale_helmet_a,itm_dale_light_a, itm_dale_light_a_good, itm_dale_med_b_bad,itm_dale_med_d_bad, itm_leather_boots_bad,itm_rohan_shoes,itm_dale_sword,itm_dale_pike, itm_axe_a, itm_axe_b, itm_axe_c,itm_north_round_shield, itm_dale_shield_c, itm_dale_shield_a,],attr_tier_2,wp_tier_2,knows_common|knows_ironflesh_1|knows_power_strike_1|knows_power_draw_2|knows_shield_2|knows_looting_1|knows_trainer_1|knows_tactics_1|knows_spotting_1|knows_inventory_management_1|knows_wound_treatment_1|knows_prisoner_management_1|knows_trade_2,swadian_face_young_1,swadian_face_middle_2],
["a2_dale_scout","Dale_Scout","Dale_Scouts",tfg_ranged| tfg_boots| tfg_armor,0,0,fac_dale,[itm_north_leather_skullcap, itm_north_leather_skullcap_good, itm_north_skullcap, itm_dale_light_a, itm_dale_light_a_good,itm_north_leather_ok,itm_north_leather_good,itm_leather_boots_bad,itm_rohan_shoes,itm_arrows,itm_regular_bow,itm_dale_sword, itm_axe_a,],attr_tier_2,wp_tier_bow_2,knows_common|knows_ironflesh_1|knows_power_strike_1|knows_power_draw_2|knows_shield_1|knows_athletics_1|knows_looting_1|knows_trainer_1|knows_tactics_1|knows_spotting_1|knows_inventory_management_1|knows_wound_treatment_1|knows_prisoner_management_1|knows_trade_2,swadian_face_young_1,swadian_face_old_2],
["a3_dale_bowman","Dale_Bowman","Dale_Bowmen",tfg_ranged| tfg_boots| tfg_armor| tfg_helm,0,0,fac_dale,[itm_dale_helmet_b,itm_dale_helmet_b,itm_dale_helmet_b, itm_dale_helmet_b_good,itm_dale_med_b,itm_dale_med_b_bad,itm_dale_med_b_ok,itm_dale_med_b_bad,itm_dale_med_b_good,itm_leather_boots_bad,itm_rohan_shoes,itm_arrows,itm_dale_bow,itm_dale_sword, itm_axe_a, itm_axe_b,],attr_tier_3,wp_tier_bow_3,knows_common|knows_ironflesh_2|knows_power_draw_2|knows_power_strike_1|knows_athletics_2,swadian_face_young_1,swadian_face_older_2],
["a4_dale_archer","Dale_Archer","Dale_Archers",tfg_ranged| tfg_boots| tfg_armor| tfg_helm,0,0,fac_dale,[itm_dale_helmet_d,itm_dale_helmet_c,itm_dale_med_b_lordly,itm_leather_gloves,itm_leather_boots,itm_leather_boots_dark,itm_arrows,itm_dale_bow,itm_dale_sword, itm_axe_b, itm_axe_c,],attr_tier_4,wp_tier_bow_4,knows_common|knows_ironflesh_3|knows_power_draw_3|knows_power_strike_2|knows_athletics_2,swadian_face_young_1,swadian_face_older_2],
["a5_barding_bowman","Barding_Bowman","Barding_Bowmen",tfg_ranged| tfg_boots| tfg_armor| tfg_helm,0,0,fac_dale,[itm_dale_helmet_d_good,itm_dale_helmet_c_good,itm_dale_med_c,itm_dale_med_c_bad,itm_dale_med_c_good,itm_dale_med_c_cloak,itm_leather_gloves_good,itm_leather_boots,itm_leather_boots_dark,itm_arrows,itm_arrows,itm_dale_bow,itm_dale_sword_broad, itm_axe_d,],str_19|agi_18| int_8| cha_8|level(33),wp_archery(260)|wp_melee(180),knows_common|knows_ironflesh_4|knows_power_draw_4|knows_power_strike_2|knows_athletics_3,swadian_face_young_1,swadian_face_older_2],
["i3_dale_swordsman","Dale_Swordsman","Dale_Swordsmen",tfg_shield| tfg_boots| tfg_armor| tfg_helm,0,0,fac_dale,[itm_north_skullcap, itm_north_skullcap_good, itm_north_nasal_helm, itm_dale_helmet_a, itm_dale_helmet_a_good,itm_dale_med_d,itm_leather_boots,itm_leather_boots_dark,itm_dale_sword,itm_dale_shield_a, itm_dale_shield_b,],attr_tier_3,wp_tier_3,knows_common|knows_athletics_1|knows_power_strike_2|knows_ironflesh_3|knows_shield_2,swadian_face_young_1,swadian_face_old_2],
["i4_dale_sergeant","Dale_Sergeant","Dale_Sergeants",tfg_shield| tfg_boots| tfg_armor| tfg_helm,0,0,fac_dale,[itm_dale_helmet_c,itm_dale_med_d_good,itm_dale_heavy_a_bad,itm_leather_gloves,itm_leather_boots_dark, itm_splinted_greaves,itm_dale_sword,itm_dale_sword_broad,itm_axe_d,itm_dale_shield_b,],attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_power_strike_3|knows_ironflesh_4|knows_shield_3,swadian_face_young_1,swadian_face_older_2],
["i5_dale_hearthman","Hearthman_of_Dale","Hearthmen_of_Dale",tfg_shield| tfg_boots| tfg_armor| tfg_helm,0,0,fac_dale,[itm_dale_helmet_c, itm_dale_helmet_c_good, itm_dale_helmet_e,itm_dale_heavy_a_good,itm_evil_gauntlets_a,itm_splinted_greaves,itm_dale_sword_broad, itm_axe_d,itm_dale_shield_b_good,],attr_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_power_strike_4|knows_ironflesh_5|knows_shield_5,swadian_face_middle_1,swadian_face_older_2],
["i3_dale_spearman","Dale_Spearman","Dale_Spearmen",tfg_boots| tfg_armor| tfg_helm,0,0,fac_dale,[itm_north_skullcap, itm_north_skullcap_good, itm_north_nasal_helm, itm_dale_helmet_a, itm_dale_helmet_a_good,itm_dale_med_c,itm_leather_boots_dark, itm_splinted_greaves,itm_dale_pike,],attr_tier_3,wp_tier_3,knows_common|knows_athletics_1|knows_power_strike_1|knows_ironflesh_1,swadian_face_young_1,swadian_face_old_2],
["i4_dale_billman","Dale_Billman","Dale_Billmen",tfg_boots| tfg_armor| tfg_helm,0,0,fac_dale,[itm_dale_helmet_c,itm_dale_med_c_good,itm_leather_gloves,itm_splinted_greaves,itm_dale_billhook,],attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_ironflesh_2|knows_power_strike_2,swadian_face_young_1,swadian_face_older_2],
["i5_dale_bill_master","Dale_Bill_Master","Dale_Bill_Masters",tfg_boots| tfg_armor| tfg_helm,0,0,fac_dale,[itm_dale_helmet_c, itm_dale_helmet_c_good, itm_dale_helmet_f,itm_dale_heavy_b,itm_dale_heavy_b_good, itm_dale_heavy_b_pelt, itm_dale_heavy_b_lordly,itm_evil_gauntlets_b_good,itm_splinted_greaves_good,itm_dale_billhook,],attr_tier_5,wp_tier_5,knows_common|knows_athletics_2|knows_ironflesh_5|knows_power_strike_4,swadian_face_middle_1,swadian_face_older_2],
["c2_rhovanion_retainer","Northmen_Retainer","Northmen_Retainers",tfg_boots| tfg_armor| tfg_shield,0,0,fac_dale,[itm_north_leather_skullcap, itm_north_leather_skullcap_bad,itm_dale_light_b, itm_dale_light_b_good,itm_north_leather_ok,itm_leather_boots_dark_bad,itm_rohan_shoes,itm_dale_pike,itm_dale_sword_long,itm_north_round_shield,itm_beorn_shield,itm_dale_horse,],attr_tier_2,wp_tier_2,knows_common|knows_riding_2|knows_athletics_1|knows_ironflesh_1|knows_shield_3,nord_face_young_1,nord_face_old_2],
["c3_rhovanion_auxilia","Northmen_Auxiliary","Northmen_Auxilia",tf_mounted| tfg_boots| tfg_armor| tfg_helm| tfg_horse| tfg_shield,0,0,fac_dale,[itm_north_leather_skullcap, itm_north_leather_skullcap_bad,itm_north_leather_skullcap_good, itm_north_skullcap,itm_dale_light_b_good, itm_dale_light_b_lordly,itm_north_leather_good,itm_leather_boots_dark,itm_lance,itm_dale_sword_long,itm_north_round_shield,itm_beorn_shield,itm_dale_horse,],attr_tier_3,wp_tier_3,knows_common|knows_riding_4|knows_athletics_1|knows_ironflesh_1|knows_power_strike_1|knows_shield_3,nord_face_young_1,nord_face_old_2],
["c4_rhovanion_rider","Rhovanion_Rider","Rhovanion_Riders",tf_mounted| tfg_boots| tfg_armor| tfg_helm| tfg_horse| tfg_shield,0,0,fac_dale,[itm_north_leather_skullcap_good, itm_north_skullcap, itm_north_nasal_helm, itm_north_skullcap_good,itm_dale_med_a_bad, itm_dale_med_a,itm_leather_boots_dark,itm_lance,itm_dale_sword_long,itm_north_round_shield, itm_dale_shield_c,itm_dale_shield_c_good,itm_dale_horse,itm_dale_warhorse,],attr_tier_4,wp_tier_4,knows_common|knows_riding_5|knows_ironflesh_2|knows_power_strike_2|knows_shield_4,nord_face_young_1,nord_face_older_2],
["ac5_rhovanion_marchwarden","Rhovanion_Marchwarden","Rhovanion_Marchwardens",tf_mounted| tfg_boots| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_shield|tfg_ranged,0,0,fac_dale,[itm_dale_helmet_e, itm_dale_helmet_f,itm_north_skullcap_good,itm_dale_med_a_good,itm_dale_med_a_lordly,itm_leather_gloves,itm_leather_boots_dark,itm_dale_sword_long, itm_javelin, itm_javelin,itm_north_round_shield, itm_dale_shield_c,itm_dale_shield_c_good,itm_dale_warhorse,],attr_tier_5,wp_tier_5,knows_common|knows_riding_8|knows_shield_5|knows_ironflesh_3|knows_power_strike_3|knows_power_throw_6|knows_horse_archery_5,nord_face_middle_1,nord_face_older_2],

["dale_items","BUG","BUG",tf_hero,0,0,fac_dale,
   [itm_leather_boots,itm_leather_gloves,itm_short_bow,itm_arrows,itm_sumpter_horse,itm_saddle_horse,itm_good_mace,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,itm_dale_heavy_a, itm_dale_heavy_c,],
      0,0,0,0],
#Rhun
["i1_rhun_tribesman","Rhun_Tribesman","Rhun_Tribesmen",tf_evil_man| tf_mounted| tfg_armor,0,0,fac_rhun,[itm_rhun_armor_a,itm_rhun_armor_b,itm_furry_boots,itm_rhun_shortsword,itm_arrows,itm_hunting_bow,],attr_evil_tier_1,wp_tier_1,knows_common|knows_power_strike_1|knows_power_draw_1|knows_riding_2|knows_horse_archery_1|knows_looting_1|knows_tracking_1|knows_pathfinding_1|knows_spotting_1|knows_surgery_1|knows_prisoner_management_2|knows_trade_1,rhun_man1,rhun_man2],
["ac2_rhun_horse_scout","Rhun_Horse_Scout","Rhun_Horse_Scouts",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse| tfg_ranged,0,0,fac_rhun,[itm_rhun_armor_a,itm_rhun_armor_b,itm_rhun_armor_d,itm_furry_boots,itm_arrows,itm_nomad_bow,itm_rhun_falchion,itm_rhun_horse_a,itm_rhun_horse_b,],attr_evil_tier_2,wp_tier_2,knows_common|knows_power_strike_1|knows_power_throw_1|knows_power_draw_2|knows_riding_3|knows_horse_archery_2|knows_looting_1|knows_tracking_1|knows_pathfinding_1|knows_spotting_1|knows_surgery_1|knows_prisoner_management_2|knows_trade_1,rhun_man1,rhun_man2],
["ac3_rhun_horse_archer","Rhun_Horse_Archer","Rhun_Horse_Archers",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_ranged| tfg_horse,0,0,fac_rhun,[itm_rhun_helm_leather_bad, itm_rhun_helm_leather,itm_rhun_helm_round_bad,itm_rhun_armor_a,itm_rhun_armor_b,itm_rhun_armor_d,itm_furry_boots,itm_leather_boots_dark_bad,itm_arrows,itm_nomad_bow,itm_rhun_sword,itm_rhun_horse_a,itm_rhun_horse_b,],attr_evil_tier_3,wp_tier_bow_3,knows_common|knows_riding_5|knows_power_draw_3|knows_ironflesh_1|knows_horse_archery_3|knows_power_throw_1,rhun_man1,rhun_man2],
["ac4_rhun_veteran_horse_archer","Rhun_Veteran_Horse_Archer","Rhun_Veteran_Horse_Archers",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_ranged| tfg_horse| tfg_shield|tfg_helm,0,0,fac_rhun,[itm_rhun_helm_leather, itm_rhun_helm_leather_good,itm_rhun_helm_round,itm_rhun_armor_j,itm_rhun_armor_n,itm_rhun_armor_m,itm_furry_boots,itm_leather_boots_dark_bad,itm_arrows,itm_nomad_bow,itm_rhun_sword,itm_rhun_horse_a,itm_rhun_horse_b,],attr_evil_tier_4,wp_tier_bow_4,knows_common|knows_riding_6|knows_power_draw_4|knows_power_strike_1|knows_ironflesh_2|knows_horse_archery_5|knows_power_throw_3,rhun_man1,rhun_man2],
["ac5_rhun_balchoth_horse_archer","Balchoth_Horse_Archer","Balchoth_Horse_Archers",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse| tfg_ranged| tfg_shield|tfg_helm,0,0,fac_rhun,[itm_rhun_helm_round_good, itm_rhun_helm_barbed_good,itm_rhun_armor_o,itm_rhun_armor_n,itm_rhun_armor_m,itm_leather_boots_dark,itm_arrows,itm_rhun_bow,itm_rhun_sword,itm_rhun_bull1_shield,itm_rhun_bull2_shield,itm_rhun_horse_d,itm_rhun_horse_b,],attr_evil_tier_5,wp_tier_bow_5,knows_common|knows_riding_6|knows_power_strike_2|knows_power_draw_5|knows_power_throw_4|knows_ironflesh_2|knows_horse_archery_7,rhun_man1,rhun_man2],
["c3_rhun_swift_horseman","Rhun_Swift_Horseman","Rhun_Swift_Horsemen",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_ranged| tfg_horse,0,0,fac_rhun,[itm_rhun_helm_pot_bad, itm_rhun_helm_horde_bad, itm_rhun_helm_round_bad,itm_rhun_armor_a,itm_rhun_armor_d,itm_furry_boots,itm_leather_boots_dark_bad,itm_rhun_sword,itm_light_lance,itm_rhun_bull1_shield,itm_rhun_horse_a,itm_rhun_horse_b,],attr_evil_tier_3,wp_tier_3,knows_common|knows_riding_5|knows_power_draw_4|knows_ironflesh_1|knows_power_throw_1,rhun_man1,rhun_man2],
["c4_rhun_veteran_swift_horseman","Rhun_Veteran_Swift_Horseman","Rhun_Veteran_Swift_Horsemen",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse| tfg_shield|tfg_helm|tfg_polearm,0,0,fac_rhun,[itm_rhun_helm_pot, itm_rhun_helm_horde, itm_rhun_helm_round,itm_rhun_armor_j,itm_rhun_armor_n,itm_rhun_armor_m,itm_evil_gauntlets_a,itm_furry_boots,itm_leather_boots_dark_bad,itm_rhun_sword,itm_light_lance,itm_rhun_bull1_shield,itm_rhun_shield, itm_rhun_horse_d,itm_rhun_horse_b,],attr_evil_tier_4,wp_tier_4,knows_common|knows_riding_6|knows_power_strike_2|knows_power_draw_2|knows_power_throw_2|knows_ironflesh_2|knows_horse_archery_1,rhun_man1,rhun_man2],
["c5_rhun_falcon_horseman","Falcon_Horseman","Falcon_Horsemen",tf_evil_man| tf_mounted| tfg_boots| tfg_helm|tfg_armor| tfg_horse| tfg_shield|tfg_polearm,0,0,fac_rhun,[itm_rhun_helm_pot_good,itm_rhun_helm_horde_good,itm_rhun_helm_round_good,itm_rhun_armor_g,itm_rhun_armor_h,itm_evil_gauntlets_a_good,itm_leather_boots_dark,itm_rhun_sword,itm_light_lance,itm_rhun_shield,itm_rhun_horse_e,itm_rhun_horse_f,],attr_evil_tier_5,wp_tier_5,knows_common|knows_riding_6|knows_power_strike_3|knows_power_draw_2|knows_power_throw_2|knows_ironflesh_2,rhun_man1,rhun_man2],
["i2_rhun_tribal_warrior","Rhun_Tribal_Footman","Rhun_Tribal_Footmen",tf_evil_man| tfg_boots| tfg_armor| tfg_shield,0,0,fac_rhun,[itm_rhun_armor_a,itm_rhun_armor_b,itm_furry_boots,itm_rhun_falchion,itm_rhun_shortsword,itm_rhun_bull1_shield,],attr_evil_tier_2,wp_tier_2,knows_common|knows_ironflesh_1|knows_power_strike_1|knows_power_draw_1|knows_athletics_2|knows_riding_2|knows_horse_archery_1|knows_looting_1|knows_tracking_1|knows_pathfinding_1|knows_spotting_1|knows_surgery_1|knows_prisoner_management_2|knows_trade_1,rhun_man1,rhun_man2],
["i3_rhun_tribal_infantry","Rhun_Tribal_Warrior","Rhun_Tribal_Warriors",tf_evil_man| tfg_boots| tfg_armor| tfg_shield,0,0,fac_rhun,[itm_rhun_helm_leather_bad,itm_rhun_helm_horde_bad,itm_rhun_armor_a,itm_rhun_armor_b,itm_rhun_armor_d,itm_furry_boots,itm_leather_boots_dark_bad,itm_rhun_glaive,itm_rhun_greatfalchion,itm_rhun_bull1_shield,],attr_evil_tier_3,wp_tier_3,knows_common|knows_athletics_3|knows_ironflesh_1|knows_power_strike_1|knows_shield_2,rhun_man1,rhun_man2],
["i4_rhun_vet_infantry","Rhun_Veteran_Warrior","Rhun_Veteran_Warriors",tf_evil_man| tfg_shield| tfg_boots| tfg_armor| tfg_helm,0,0,fac_rhun,[itm_rhun_helm_barbed, itm_rhun_helm_horde, itm_rhun_helm_round_good,itm_rhun_armor_g,itm_rhun_armor_h,itm_evil_gauntlets_a_good,itm_furry_boots,itm_leather_boots_dark_bad,itm_rhun_falchion,itm_rhun_glaive,itm_rhun_greatfalchion,itm_rhun_battleaxe,itm_rhun_bull1_shield,],attr_evil_tier_4,wp_tier_4,knows_common|knows_athletics_4|knows_ironflesh_2|knows_power_strike_2|knows_shield_2,rhun_man1,rhun_man2],
["i5_rhun_ox_warrior","Warrior_of_the_Ox","Warriors_of_the_Ox",tf_evil_man| tfg_shield| tfg_boots| tfg_armor| tfg_helm,0,0,fac_rhun,[itm_rhun_helm_barbed_good, itm_rhun_helm_pot_good, itm_rhun_helm_horde_good,itm_rhun_armor_g_good,itm_rhun_armor_h_good,itm_rhun_armor_p_bad,itm_rhun_armor_k_bad,itm_evil_gauntlets_b_good,itm_leather_boots_dark_bad, itm_splinted_greaves,itm_rhun_warpick, itm_rhun_mangler, itm_rhun_glaive, itm_rhun_battleaxe,itm_rhun_bull2_shield,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_5|knows_shield_2|knows_ironflesh_3|knows_power_strike_3,rhun_man1,rhun_man2],
["c2_rhun_horseman","Horseman_of_Rhun","Horsemen_of_Rhun",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse,0,0,fac_rhun,[itm_rhun_armor_a,itm_rhun_armor_b,itm_rhun_armor_d,itm_furry_boots,itm_leather_boots_dark_bad,itm_rhun_sword,itm_rhun_bull1_shield,itm_rhun_horse_a,itm_rhun_horse_b,],attr_evil_tier_2,wp_tier_2,knows_common|knows_riding_4|knows_power_draw_3|knows_power_throw_1|knows_horse_archery_3,rhun_man1,rhun_man2],
["c3_rhun_outrider","Outrider_of_Rhun","Outriders_of_Rhun",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse,0,0,fac_rhun,[itm_rhun_helm_horde,itm_rhun_helm_round,itm_rhun_helm_pot_bad,itm_rhun_armor_j,itm_rhun_armor_n,itm_rhun_armor_m,itm_furry_boots,itm_leather_boots_dark_bad,itm_rhun_sword,itm_rhun_bull1_shield,itm_rhun_bull2_shield, itm_rhun_horse_b,itm_rhun_horse_d,],attr_evil_tier_3,wp_tier_3,knows_common|knows_riding_5|knows_power_draw_4|knows_power_strike_1|knows_ironflesh_1|knows_power_throw_1,rhun_man1,rhun_man2],
["c4_rhun_noble_rider","Noble_Rider_of_Rhun","Noble_Riders_of_Rhun",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse| tfg_shield|tfg_helm,0,0,fac_rhun,[itm_rhun_helm_horde_good,itm_rhun_helm_barbed,itm_rhun_helm_pot,itm_rhun_armor_n,itm_rhun_armor_h,itm_rhun_armor_g,itm_furry_boots,itm_leather_boots_dark,itm_rhun_sword,itm_rhun_bull2_shield,itm_rhun_horse_b,itm_rhun_horse_e,itm_rhun_horse_f,],attr_evil_tier_4,wp_tier_4,knows_common|knows_riding_6|knows_power_strike_2|knows_power_draw_2|knows_power_throw_2|knows_ironflesh_2|knows_horse_archery_1,rhun_man1,rhun_man2],
["c5_rhun_warrider","Warrider_of_Rhun","Warriders_of_Rhun",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse| tfg_shield|tfg_helm,0,0,fac_rhun,[itm_rhun_helm_barbed_good,itm_rhun_helm_pot_good,itm_rhun_armor_p,itm_rhun_armor_k,itm_evil_gauntlets_a_good,itm_leather_boots_dark, itm_splinted_greaves,itm_rhun_sword,itm_rhun_greatsword,itm_rhun_bull3_shield,itm_rhun_horse_g,],attr_evil_tier_5,wp_tier_5,knows_common|knows_riding_6|knows_power_strike_3|knows_power_draw_2|knows_power_throw_2|knows_ironflesh_2|knows_horse_archery_1,rhun_man1,rhun_man2],
["c6_rhun_warlord","Warlord_of_Rhun","Warlords_of_Rhun",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse| tfg_shield|tfg_helm,0,0,fac_rhun,[itm_rhun_helm_chieftain,itm_rhun_armor_p_good,itm_rhun_armor_k_good,itm_evil_gauntlets_b_good,itm_splinted_greaves_good,itm_rhun_sword,itm_rhun_greatfalchion,itm_rhun_bull3_shield,itm_rhun_horse_g,],attr_evil_tier_6,wp_tier_6,knows_common|knows_riding_7|knows_power_strike_4|knows_power_draw_2|knows_power_throw_2|knows_ironflesh_2|knows_horse_archery_1,rhun_man1,rhun_man2],

["rhun_items","BUG","BUG",tf_hero,0,0,fac_rhun,
   [itm_saddle_horse,itm_leather_boots,itm_leather_gloves,itm_sumpter_horse,itm_short_bow,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
	  
#Dwarves
["i1_dwarf_apprentice","Apprentice-dwarf","Apprentice-dwarves",tf_dwarf| tfg_armor| tfg_boots,0,0,fac_dwarf,[itm_dwarf_hood, itm_dwarf_miner,itm_dwarf_vest,itm_dwarf_vest_lordly,itm_dwarf_pad_boots,itm_dwarf_mattock, itm_dwarf_mattock_good, itm_dwarf_hand_axe,],attr_dwarf_tier_1,wp_dwarf_tier_1,knows_common|knows_ironflesh_3|knows_power_strike_1|knows_power_throw_1|knows_athletics_1|knows_trainer_1|knows_pathfinding_1|knows_spotting_1|knows_inventory_management_2|knows_wound_treatment_1|knows_trade_2,dwarf_face_2,dwarf_face_3],
["i2_dwarf_warrior","Warrior-dwarf","Warrior-dwarves",tf_dwarf| tfg_armor| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_helm_coif, itm_dwarf_miner, itm_dwarf_miner_nasal,itm_dwarf_nasal_b,itm_dwarf_vest_lordly,itm_dwarf_pad_boots,itm_dwarf_mattock_good, itm_dwarf_hand_axe,itm_dwarf_sword_a, itm_dwarf_spear,itm_dwarf_shield_d, itm_dwarf_shield_d_good,],attr_dwarf_tier_2,wp_dwarf_tier_2,knows_common|knows_ironflesh_3|knows_power_strike_1|knows_power_throw_2|knows_shield_1|knows_athletics_1|knows_trainer_1|knows_pathfinding_1|knows_spotting_1|knows_inventory_management_2|knows_wound_treatment_1|knows_trade_2,dwarf_face_1,dwarf_face_2],
["i3_dwarf_hardened_warrior","Hardened_Warrior-dwarf","Hardened_Warrior-dwarves",tf_dwarf| tfg_armor| tfg_gloves| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_helm_coif, itm_dwarf_helm_kettle, itm_dwarf_helm_round,itm_dwarf_nasal_b,itm_dwarf_armor_a,itm_leather_gloves,itm_dwarf_pad_boots,itm_dwarf_mattock_good, itm_dwarf_hand_axe,itm_dwarf_sword_a, itm_dwarf_spear,itm_dwarf_shield_d, itm_dwarf_shield_d_good,itm_dwarf_shield_a, itm_dwarf_shield_a_good,],attr_dwarf_tier_3,wp_dwarf_tier_3,knows_common_dwarf|knows_athletics_2|knows_power_strike_2|knows_power_throw_2|knows_ironflesh_4|knows_shield_3,dwarf_face_3,dwarf_face_4],
["i4_dwarf_spearman","Spear-dwarf","Spear-dwarves",tf_dwarf| tfg_armor| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_helm_coif_lordly, itm_dwarf_helm_kettle, itm_dwarf_helm_round,itm_dwarf_armor_b,itm_leather_gloves,itm_dwarf_pad_boots,itm_dwarf_spear,itm_dwarf_shield_d, itm_dwarf_shield_d_good,itm_dwarf_shield_a, itm_dwarf_shield_a_good,],attr_dwarf_tier_4,wp_dwarf_tier_4,knows_common_dwarf|knows_athletics_2|knows_power_strike_4|knows_ironflesh_5|knows_shield_3,dwarf_face_1,dwarf_face_2],
["i5_dwarf_pikeman","Pike-dwarf","Pike-dwarves",tf_dwarf| tfg_armor| tfg_gloves| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_helm_sallet,itm_dwarf_armor_b_lordly,itm_mail_mittens,itm_dwarf_chain_boots,itm_dwarf_spear,itm_dwarf_shield_c,],attr_dwarf_tier_5,wp_dwarf_tier_5,knows_common_dwarf|knows_athletics_2|knows_power_strike_5|knows_ironflesh_6|knows_shield_4,dwarf_face_3,dwarf_face_4],
["i6_dwarf_longpikeman","Longpike_Dwarf","Longpike_Dwarves",tf_dwarf| tfg_armor| tfg_shield| tfg_gloves| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_helm_sallet_lordly,itm_dwarf_armor_c,itm_mail_mittens,itm_dwarf_chain_boots,itm_dwarf_scale_boots,itm_dwarf_spear_b,itm_dwarf_shield_c, itm_dwarf_shield_c_good,],attr_dwarf_tier_6,wp_dwarf_tier_6,knows_common_dwarf|knows_athletics_3|knows_power_strike_6|knows_ironflesh_7|knows_shield_5,dwarf_face_7,dwarf_face_7],
["i4_dwarf_axeman","Axedwarf","Axedwarves",tf_dwarf| tfg_armor| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_helm_coif_lordly, itm_dwarf_helm_kettle, itm_dwarf_helm_round,itm_dwarf_armor_a,itm_leather_gloves,itm_dwarf_chain_boots, itm_dwarf_hand_axe,itm_dwarf_throwing_axe,itm_dwarf_throwing_axe,itm_dwarf_shield_d, itm_dwarf_shield_d_good,itm_dwarf_shield_a, itm_dwarf_shield_a_good,],attr_dwarf_tier_4,wp_dwarf_tier_4,knows_common_dwarf|knows_athletics_2|knows_power_throw_2|knows_power_strike_5|knows_ironflesh_5|knows_shield_4,dwarf_face_1,dwarf_face_2],
["i5_dwarf_expert_axeman","Expert_Axedwarf","Expert_Axedwarves",tf_dwarf| tfg_armor| tfg_gloves| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_helm_sallet,itm_dwarf_armor_a_lordly,itm_mail_mittens,itm_dwarf_chain_boots, itm_dwarf_hand_axe, itm_dwarf_battle_axe,itm_dwarf_throwing_axe,itm_dwarf_throwing_axe,itm_dwarf_shield_b,],attr_dwarf_tier_5,wp_dwarf_tier_5,knows_common_dwarf|knows_athletics_3|knows_power_throw_4|knows_power_strike_6|knows_ironflesh_6|knows_shield_5,dwarf_face_3,dwarf_face_4],
["i6_dwarf_longbeard_axeman","Longbeard_Axedwarf","Longbeard_Axedwarves",tf_dwarf| tfg_armor| tfg_gloves| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_helm_sallet_lordly,itm_leather_dwarf_armor,itm_mail_mittens,itm_dwarf_scale_boots,itm_dwarf_battle_axe,itm_dwarf_throwing_axe,itm_dwarf_throwing_axe,itm_dwarf_shield_b_good,],attr_dwarf_tier_6,wp_dwarf_tier_6,knows_common_dwarf|knows_athletics_3|knows_power_throw_5|knows_power_strike_7|knows_ironflesh_7|knows_shield_6,dwarf_face_7,dwarf_face_7],
["a2_dwarf_lookout","Lookout-dwarf","Lookout-dwarves",tf_dwarf| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_hood, itm_dwarf_miner,  itm_dwarf_miner_nasal,itm_dwarf_vest,itm_dwarf_vest_lordly,itm_dwarf_pad_boots,itm_short_bow, itm_arrows,itm_dwarf_hand_axe, itm_dwarf_sword_a,],attr_dwarf_tier_2,wp_dwarf_tier_1,knows_common|knows_ironflesh_3|knows_power_strike_1|knows_power_throw_1|knows_power_draw_1|knows_athletics_2|knows_trainer_1|knows_pathfinding_1|knows_spotting_1|knows_inventory_management_2|knows_wound_treatment_1|knows_trade_2,dwarf_face_1,dwarf_face_2],
["a3_dwarf_scout","Scout-dwarf","Scout-dwarves",tf_dwarf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_hood, itm_dwarf_helm_coif, itm_dwarf_miner,  itm_dwarf_miner_nasal,itm_dwarf_vest_lordly,itm_dwarf_armor_a,itm_leather_gloves,itm_dwarf_pad_boots,itm_dwarf_short_bow, itm_arrows,itm_dwarf_hand_axe, itm_dwarf_sword_a,],attr_dwarf_tier_3,wp_dwarf_tier_2,knows_common_dwarf|knows_athletics_4|knows_power_draw_2|knows_power_strike_2|knows_ironflesh_4,dwarf_face_4,dwarf_face_5],
["a4_dwarf_bowman","Bow-dwarf","Bow-dwarves",tf_dwarf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_helm_kettle, itm_dwarf_helm_round,itm_dwarf_armor_a,itm_leather_gloves,itm_dwarf_pad_boots,itm_dwarf_horn_bow, itm_arrows,itm_dwarf_hand_axe, itm_dwarf_sword_a_good,],attr_dwarf_tier_4,wp_dwarf_tier_3,knows_common_dwarf|knows_athletics_6|knows_power_draw_4|knows_power_strike_4|knows_ironflesh_5,dwarf_face_4,dwarf_face_5],
["i6_dwarf_longaxeman","Longaxe Dwarf","Longaxe Dwarves",tf_dwarf| tfg_armor| tfg_gloves| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_helm_sallet_lordly,itm_dwarf_armor_c,itm_mail_mittens,itm_dwarf_scale_boots,itm_dwarf_spear_c,],attr_dwarf_tier_6,wp_dwarf_tier_6,knows_common_dwarf|knows_athletics_3|knows_power_strike_6|knows_ironflesh_8,dwarf_face_4,dwarf_face_5],
["i3_iron_hills_warrior","Iron_Hills_Warrior","Iron_Hills_Warriors",tf_dwarf| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_miner_reinf, itm_dwarf_helm_fris, itm_dwarf_nasal, itm_dwarf_helm_coif_reinf,itm_leather_dwarf_armor_b, itm_dwarf_vest_b,itm_leather_dwarf_armor_b_lordly,itm_leather_gloves,itm_dwarf_chain_boots,itm_dwarf_mattock, itm_dwarf_mattock_good, itm_dwarf_hand_axe, itm_dwarf_sword_a,itm_dwarf_shield_d, itm_dwarf_shield_d_good,],attr_dwarf_tier_3,wp_dwarf_tier_3,knows_common|knows_ironflesh_2|knows_power_strike_3|knows_power_throw_1|knows_athletics_3|knows_looting_1|knows_trainer_1|knows_tactics_1|knows_pathfinding_1|knows_surgery_1|knows_prisoner_management_1|knows_trade_1,dwarf_face_3,dwarf_face_4],
["i2_iron_hills_miner","Iron_Hills_Miner","Iron_Hills_Miners",tf_dwarf| tfg_armor| tfg_boots,0,0,fac_dwarf,[itm_dwarf_miner, itm_dwarf_miner_reinf,itm_dwarf_vest,itm_dwarf_vest_lordly,itm_leather_dwarf_armor_b,itm_dwarf_pad_boots,itm_dwarf_mattock, itm_dwarf_mattock_good, itm_dwarf_hand_axe, itm_dwarf_sword_a,itm_dwarf_shield_d, itm_dwarf_shield_d_good,],attr_dwarf_tier_2,wp_dwarf_tier_2,knows_common|knows_ironflesh_2|knows_power_strike_2|knows_power_throw_1|knows_athletics_2|knows_looting_1|knows_trainer_1|knows_tactics_1|knows_pathfinding_1|knows_surgery_1|knows_prisoner_management_1|knows_trade_1,dwarf_face_1,dwarf_face_2],
["i4_iron_hills_infantry","Iron_Hills_Infantry","Iron_Hills_Infantry",tf_dwarf| tfg_armor| tfg_gloves| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_miner_reinf, itm_dwarf_helm_fris, itm_dwarf_nasal,itm_dwarf_vest_b, itm_leather_dwarf_armor_b_lordly,itm_leather_gloves,itm_dwarf_chain_boots, itm_dwarf_great_mattock, itm_dwarf_mattock_good, itm_dwarf_sword_a, itm_dwarf_sword_a_good,itm_dwarf_shield_d, itm_dwarf_shield_d_good,],attr_dwarf_tier_4,wp_dwarf_tier_4,knows_common_dwarf|knows_athletics_4|knows_power_strike_3|knows_ironflesh_5|knows_shield_2,dwarf_face_3,dwarf_face_4],
["i5_iron_hills_battle_dwarf","Iron_Hills_Battle-dwarf","Iron_Hills_Battle-dwarves",tf_dwarf| tfg_armor| tfg_gloves| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_nasal_reinf, itm_dwarf_helm_fris_reinf,itm_dwarf_vest_b,itm_dwarf_vest_b_lordly,itm_mail_mittens,itm_dwarf_scale_boots,itm_dwarf_great_pick, itm_dwarf_great_mattock,itm_dwarf_great_axe],attr_dwarf_tier_5,wp_dwarf_tier_5,knows_common_dwarf|knows_athletics_5|knows_power_strike_4|knows_ironflesh_7|knows_shield_3,dwarf_face_1,dwarf_face_2],
["i6_iron_hills_grors_guard","Gror's_Guard","Gror's_Guards",tf_dwarf| tfg_armor| tfg_gloves| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,[itm_dwarf_nasal_lordly, itm_dwarf_helm_fris_lordly,itm_dwarf_armor_d,itm_mail_mittens,itm_dwarf_scale_boots,itm_dwarf_great_pick_good,itm_dwarf_great_mattock_good,itm_dwarf_great_axe,itm_dwarf_great_axe_good,],attr_dwarf_tier_6,wp_dwarf_tier_6,knows_common_dwarf|knows_athletics_6|knows_power_strike_6|knows_ironflesh_9|knows_shield_5,dwarf_face_7,dwarf_face_7],

["dwarf_items","BUG","_",tf_hero,0,0,fac_dwarf,
   [itm_pony, itm_good_mace,itm_dwarf_shield_b,itm_dwarf_sword_c,itm_dwarf_sword_d,itm_dwarf_great_mattock,itm_dwarf_hand_axe,itm_dwarf_throwing_axe,itm_dwarf_spear,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
	  
#Gondor
["i1_gon_levy","Gondor_Levy","Gondor_Levies",tf_gondor| tfg_armor| tfg_boots,0,0,fac_gondor,[itm_gondor_auxila_helm_bad,itm_gon_jerkin,itm_white_tunic_a,itm_gondor_light_greaves,itm_gondor_light_greaves,itm_shortened_spear,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],attr_tier_1,wp_tier_1,knows_common|knows_power_strike_1|knows_power_draw_1|knows_weapon_master_1|knows_shield_1|knows_trainer_1|knows_tactics_1|knows_spotting_1|knows_inventory_management_1|knows_wound_treatment_1|knows_first_aid_1|knows_leadership_2|knows_trade_1,gondor_face1,gondor_face2],
["i2_gon_watchman","Gondor_Watchman","Gondor_Watchmen",tf_gondor| tfg_armor| tfg_shield| tfg_boots| tfg_helm,0,0,fac_gondor,[itm_gondor_auxila_helm,itm_gon_jerkin,itm_gondor_light_greaves,itm_shortened_spear,itm_gondor_short_sword,itm_good_mace,itm_gon_tab_shield_a,],attr_tier_2,wp_tier_2,knows_common|knows_power_strike_1|knows_power_draw_1|knows_weapon_master_1|knows_shield_2|knows_athletics_1|knows_trainer_1|knows_tactics_1|knows_spotting_1|knows_inventory_management_1|knows_wound_treatment_1|knows_first_aid_1|knows_leadership_2|knows_trade_1,gondor_face1,gondor_face2],
["i3_gon_footman","Footman_of_Gondor","Footmen_of_Gondor",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,[itm_gondor_infantry_helm_bad,itm_gon_footman,itm_gondor_med_greaves,itm_gondor_spear,itm_gondor_short_sword,itm_good_mace,itm_gondor_shield_c,],attr_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_shield_2|knows_power_strike_2|knows_ironflesh_1,gondor_face1,gondor_face2],
#Gondor Spearmen
["i4_gon_spearman","Spearman_of_Gondor","Spearmen_of_Gondor",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,[itm_gondor_infantry_helm,itm_gon_regular,itm_leather_gloves,itm_gondor_med_greaves,itm_gondor_spear,itm_gondor_shield_c,],attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,gondor_face1,gondor_face3],
["i5_gon_vet_spearman","Veteran_Spearman_of_Gondor","Veteran_Spearmen_of_Gondor",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,[itm_gondor_infantry_helm_good,itm_gon_regular,itm_mail_mittens,itm_gondor_heavy_greaves,itm_gondor_spear,itm_gondor_shield_c,],attr_tier_5,wp_tier_5,knows_common|knows_athletics_2|knows_shield_4|knows_power_strike_4|knows_ironflesh_2,gondor_face1,gondor_face2],
["i6_gon_tower_spearman","Guard_of_the_Fountain_Court","Guards_of_the_Fountain_Court",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,[itm_tower_guard_helm,itm_gon_tower_guard,itm_mail_mittens,itm_gondor_heavy_greaves,itm_gondor_tower_spear,itm_gondor_shield_a,],attr_tier_6,wp_tier_6,knows_common|knows_athletics_2|knows_shield_6|knows_power_strike_6|knows_ironflesh_4,gondor_face1,gondor_face3],
#Gondor swordsmen
["i4_gon_swordsman","Swordsman_of_Gondor","Swordsmen_of_Gondor",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,[itm_gondor_infantry_helm,itm_gon_regular,itm_leather_gloves,itm_gondor_med_greaves,itm_gondor_sword,itm_gondor_shield_c,],attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,gondor_face1,gondor_face3],
["i5_gon_vet_swordsman","Veteran_Swordsman_of_Gondor","Veteran_Swordsmen_of_Gondor",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,[itm_gondor_infantry_helm_good,itm_gon_regular,itm_mail_mittens,itm_gondor_heavy_greaves,itm_gondor_sword,itm_gondor_shield_c,],attr_tier_5,wp_tier_5,knows_common|knows_athletics_2|knows_shield_4|knows_power_strike_4|knows_ironflesh_2,gondor_face1,gondor_face2],
["i6_gon_tower_swordsman","Swordsman_of_the_Tower_Guard","Swordsmen_of_the_Tower_Guard",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,[itm_tower_guard_helm,itm_gon_tower_guard,itm_mail_mittens,itm_gondor_heavy_greaves,itm_gondor_citadel_sword,itm_gondor_shield_a,],attr_tier_6,wp_tier_6,knows_common|knows_athletics_3|knows_shield_5|knows_power_strike_5|knows_ironflesh_4,gondor_face1,gondor_face3],
#Gondor Noble Line
["c1_gon_nobleman","Gondor_Noble","Gondor_Noble",tf_gondor| tf_mounted| tfg_armor| tfg_boots| tfg_horse,0,0,fac_gondor,[itm_gondor_auxila_helm,itm_gondor_infantry_helm_bad, itm_gon_jerkin,itm_gondor_light_greaves,itm_gondor_sword,itm_saddle_horse,],attr_tier_1,wp_tier_1,knows_common|knows_power_strike_2|knows_weapon_master_1|knows_riding_2|knows_trainer_2|knows_tactics_1|knows_inventory_management_1|knows_wound_treatment_1|knows_leadership_3,gondor_face1,gondor_face2],
["c2_gon_squire","Squire_of_Gondor","Squires_of_Gondor",tf_gondor| tf_mounted| tfg_helm| tfg_armor| tfg_boots| tfg_horse,0,0,fac_gondor,[itm_gondor_auxila_helm_good,itm_gon_noble_cloak,itm_gondor_med_greaves,itm_gondor_cav_sword,itm_gondor_courser,],attr_tier_2,wp_tier_2,knows_common|knows_power_strike_2|knows_weapon_master_2|knows_shield_1|knows_riding_2|knows_trainer_2|knows_tactics_1|knows_inventory_management_1|knows_wound_treatment_1|knows_leadership_3,gondor_face1,gondor_face2],
["c3_gon_vet_squire","Veteran_Squire_of_Gondor","Veteran_Squires_of_Gondor",tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,[itm_gondor_knight_helm_bad,itm_gon_squire,itm_leather_gloves,itm_gondor_med_greaves,itm_gondor_cav_sword,itm_gondor_shield_d,itm_gondor_courser,],attr_tier_3,wp_tier_3,knows_common|knows_riding_2|knows_shield_2|knows_power_strike_2,gondor_face1,gondor_face2],
["c4_gon_knight","Knight_of_Gondor","Knights_of_Gondor",tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,[itm_gondor_knight_helm,itm_gon_knight,itm_mail_mittens,itm_gondor_heavy_greaves,itm_gondor_cav_sword,itm_gondor_lance,itm_gondor_shield_d,itm_gondor_hunter,],attr_tier_4,wp_tier_4,knows_common|knows_riding_3|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,gondor_face1,gondor_face2],
["c5_gon_vet_knight","Veteran_Knight_of_Gondor","Veteran_Knights_of_Gondor",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,[itm_gondor_knight_helm_good,itm_gon_knight,itm_mail_mittens,itm_gondor_heavy_greaves,itm_gondor_cav_sword,itm_gondor_lance,itm_gondor_shield_d,itm_gondor_hunter,],attr_tier_5,wp_tier_5,knows_common|knows_riding_4|knows_shield_3|knows_power_strike_4|knows_ironflesh_4,gondor_face1,gondor_face3],
["c6_gon_tower_knight","Knight_of_the_Citadel","Knights_of_the_Citadel",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,[itm_gondor_citadel_knight_helm,itm_gon_tower_knight,itm_mail_mittens,itm_gondor_heavy_greaves,itm_gondor_lance_banner,itm_gondor_citadel_sword,itm_gondor_shield_b,itm_gondor_warhorse,],attr_tier_6,wp_tier_6,knows_common|knows_riding_6|knows_shield_4|knows_power_strike_6|knows_ironflesh_6,gondor_face1,gondor_face3],
#Gondor Archers
["a3_gon_bowman","Bowman_of_Gondor","Bowmen_of_Gondor",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,[itm_gondorian_archer_helm_bad,itm_gon_bowman,itm_gondor_med_greaves,itm_gondor_arrows,itm_regular_bow,itm_gondor_short_sword,],attr_tier_3,wp_tier_bow_3,knows_common|knows_power_draw_2|knows_ironflesh_1,gondor_face1,gondor_face2],
["a4_gon_archer","Archer_of_Gondor","Archers_of_Gondor",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,[itm_gondorian_archer_helm,itm_gon_archer,itm_gondor_med_greaves,itm_gondor_arrows,itm_gondor_bow,itm_gondor_short_sword,],attr_tier_4,wp_tier_bow_4,knows_common|knows_athletics_2|knows_power_draw_3|knows_ironflesh_1,gondor_face1,gondor_face2],
["a5_gon_vet_archer","Veteran_Archer_of_Gondor","Veteran_Archers_of_Gondor",tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,[itm_gondorian_archer_helm_good,itm_gon_footman,itm_leather_gloves,itm_gondor_med_greaves,itm_gondor_bow,itm_gondor_arrows,itm_gondor_sword,],attr_tier_5,wp_tier_bow_5,knows_common|knows_athletics_2|knows_power_draw_4|knows_power_strike_2|knows_ironflesh_1,gondor_face1,gondor_face2],
["a6_gon_tower_archer","Archer_of_the_Tower_Guard","Archers_of_the_Tower_Guard",tf_gondor| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,[itm_tower_archer_helm,itm_gon_steward_guard,itm_leather_gloves,itm_gondor_heavy_greaves,itm_gondor_bow,itm_gondor_arrows,itm_gondor_arrows,itm_gondor_citadel_sword,],attr_tier_6,wp_tier_bow_6,knows_common|knows_athletics_3|knows_power_draw_6|knows_power_strike_2|knows_ironflesh_2,gondor_face1,gondor_face3],
#Special Denethor Guards (only for scene)
["steward_guard","Steward's_Guard","Steward's_Guards",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,[itm_tower_guard_helm,itm_gon_steward_guard,itm_mail_mittens,itm_gondor_heavy_greaves,itm_gondor_tower_spear,itm_gon_tab_shield_b,],attr_tier_6,wp_tier_6,knows_common|knows_athletics_4|knows_shield_6|knows_power_strike_6|knows_ironflesh_4,gondor_face1,gondor_face3],
#Rangers
["a4_ithilien_ranger","Ranger_of_Ithilien","Rangers_of_Ithilien",tf_gondor| tfg_ranged| tfg_armor| tfg_boots,0,subfac_rangers,fac_gondor,[itm_gondor_ranger_hood,itm_gon_ranger_cloak,itm_leather_gloves,itm_gondor_light_greaves,itm_ithilien_arrows,itm_gondor_bow,itm_gondor_ranger_sword,],attr_tier_4,wp_archery(170)|wp(170),knows_common|knows_pathfinding_1|knows_riding_1|knows_athletics_6|knows_power_draw_3|knows_power_strike_3|knows_ironflesh_3,gondor_face1,gondor_face2],
["a5_ithilien_vet_ranger","Veteran_Ranger_of_Ithilien","Veteran_Rangers_of_Ithilien",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,subfac_rangers,fac_gondor,[itm_gondor_ranger_hood,itm_gon_ranger_cloak,itm_leather_gloves,itm_gondor_light_greaves,itm_ithilien_arrows,itm_gondor_bow,itm_gondor_ranger_sword,],attr_tier_5,wp(220),knows_common|knows_pathfinding_2|knows_riding_1|knows_athletics_7|knows_power_draw_4|knows_power_strike_4|knows_ironflesh_4,gondor_face1,gondor_face2],
["a6_ithilien_master_ranger","Master_Ranger_of_Ithilien","Master_Rangers_of_Ithilien",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,subfac_rangers,fac_gondor,[itm_gondor_ranger_hood_mask,(itm_gon_ranger_skirt, imod_reinforced),itm_leather_gloves,itm_gondor_light_greaves,itm_ithilien_arrows,itm_ithilien_arrows,itm_gondor_bow,itm_gondor_ranger_sword,],attr_tier_6,wp_melee(320)|wp_archery(300),knows_common|knows_pathfinding_3|knows_riding_1|knows_athletics_8|knows_power_draw_6|knows_power_strike_5|knows_ironflesh_6,gondor_face1,gondor_face3],
["a6_ithilien_leader","Captain_of_Ithilien_Rangers","Captains_of_Ithilien_Rangers",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,subfac_rangers,fac_gondor,[itm_gondor_ranger_hood_mask,(itm_gon_ranger_skirt, imod_lordly),itm_leather_gloves,itm_gondor_light_greaves,itm_ithilien_arrows,itm_ithilien_arrows,itm_gondor_bow,itm_gondor_ranger_sword,],attr_tier_7,wp_tier_7,knows_common|knows_pathfinding_4|knows_athletics_9|knows_shield_9|knows_power_draw_9|knows_power_strike_8|knows_ironflesh_10,gondor_face1,gondor_face2],
#Lossarnach
["i1_loss_woodsman","Woodsman_of_Lossarnach","Woodsmen_of_Lossarnach",tf_gondor| tfg_armor| tfg_boots,0,subfac_lossarnach,fac_gondor,[itm_lossarnach_cloth_cap,itm_lossarnach_shirt,itm_gondor_light_greaves,itm_loss_axe,itm_gon_tab_shield_a,itm_loss_throwing_axes,],attr_fief_tier_1,wp_tier_1,knows_common|knows_ironflesh_1|knows_power_strike_1|knows_power_throw_2|knows_weapon_master_1|knows_looting_1|knows_tracking_1|knows_pathfinding_1|knows_wound_treatment_1|knows_surgery_1|knows_first_aid_1|knows_persuasion_1|knows_trade_1,gondor_face1,gondor_face2],
["i2_loss_axeman","Axeman_of_Lossarnach","Axemen_of_Lossarnach",tf_gondor| tfg_armor| tfg_shield| tfg_boots| tfg_helm,0,subfac_lossarnach,fac_gondor,[itm_lossarnach_leather_cap,itm_lossarnach_axeman,itm_gondor_light_greaves,itm_loss_axe,itm_gon_tab_shield_a,itm_loss_throwing_axes,],attr_fief_tier_2,wp_tier_2,knows_common|knows_ironflesh_2|knows_power_strike_1|knows_power_throw_3|knows_weapon_master_1|knows_athletics_1|knows_looting_1|knows_tracking_1|knows_pathfinding_1|knows_wound_treatment_1|knows_surgery_1|knows_first_aid_1|knows_persuasion_1|knows_trade_1,gondor_face1,gondor_face2],
["i3_loss_vet_axeman","Lossarnach_Veteran_Axeman","Lossarnach_Veteran_Axemen",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_lossarnach,fac_gondor,[itm_lossarnach_leather_cap,itm_lossarnach_vet_axeman,itm_gondor_light_greaves,itm_loss_axe,itm_gon_tab_shield_a,itm_loss_throwing_axes,],attr_fief_tier_3,wp_tier_3,knows_common|knows_power_throw_4|knows_athletics_3|knows_power_strike_3|knows_ironflesh_3,gondor_face1,gondor_face2],
["i4_loss_heavy_axeman","Heavy_Lossarnach_Axeman","Heavy_Lossarnach_Axemen",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tfg_gloves,0,subfac_lossarnach,fac_gondor,[itm_lossarnach_scale_cap,itm_lossarnach_warrior,itm_leather_gloves,itm_lossarnach_greaves,itm_loss_axe,itm_gon_tab_shield_a,itm_loss_throwing_axes,],attr_fief_tier_4,wp_tier_4,knows_common|knows_athletics_4|knows_power_strike_5|knows_ironflesh_4|knows_power_throw_5,gondor_face1,gondor_face2],
["i5_loss_axemaster","Axemaster_of_Lossarnach","Axemasters_of_Lossarnach",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_lossarnach,fac_gondor,[itm_lossarnach_scale_cap,itm_lossarnach_vet_warrior,itm_mail_mittens,itm_lossarnach_greaves,itm_loss_war_axe,itm_gon_tab_shield_a,itm_loss_throwing_axes,],attr_tier_5,wp_tier_5,knows_common|knows_athletics_5|knows_power_strike_7|knows_ironflesh_5|knows_power_throw_6,gondor_face1,gondor_face2],
["i6_loss_leader","Captain_of_Lossarnach","Captains_of_Lossarnach",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_lossarnach,fac_gondor,[itm_gondor_leader_helm,itm_lossarnach_leader,itm_mail_mittens,itm_lossarnach_greaves,itm_gondor_cav_sword,itm_loss_axe,itm_gon_tab_shield_a,],attr_tier_6,wp_tier_6,knows_common|knows_riding_8|knows_shield_9|knows_power_strike_8|knows_ironflesh_10,gondor_face1,gondor_face3],
#Pelargir
["i1_pel_watchman","Pelargir_Watchman","Pelargir_Watchmen",tf_gondor| tfg_armor| tfg_helm| tfg_boots,0,subfac_pelargir,fac_gondor,[itm_pel_jerkin,itm_gondor_light_greaves,itm_pelargir_eket,itm_shortened_spear,],attr_fief_tier_1,wp_tier_2,knows_common|knows_ironflesh_1|knows_power_throw_1|knows_weapon_master_1|knows_shield_1|knows_athletics_1|knows_trainer_1|knows_tactics_2|knows_spotting_1|knows_inventory_management_1|knows_leadership_1|knows_trade_2,gondor_face1,gondor_face2],
["a2_pel_marine","Pelargir_Marine","Pelargir_Marines",tf_gondor| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pelargir,fac_gondor,[itm_pelargir_hood,itm_pel_marine,itm_gondor_light_greaves,itm_pelargir_eket,itm_gondor_javelin,itm_gon_tab_shield_a,],attr_tier_2,wp_tier_3,knows_common|knows_ironflesh_1|knows_power_throw_3|knows_weapon_master_1|knows_shield_1|knows_athletics_3|knows_trainer_1|knows_tactics_2|knows_spotting_1|knows_inventory_management_1|knows_leadership_1|knows_trade_2,gondor_face1,gondor_face2],
["a3_pel_vet_marine","Pelargir_Veteran_Marine","Pelargir_Veteran_Marines",tf_gondor| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pelargir,fac_gondor,[itm_pelargir_hood,itm_pel_marine,itm_gondor_light_greaves,itm_pelargir_eket,itm_gondor_javelin,itm_gondor_javelin,itm_gon_tab_shield_a,],attr_tier_5,wp_tier_5,knows_common|knows_athletics_6|knows_power_throw_5|knows_power_strike_2|knows_ironflesh_3,gondor_face1,gondor_face2],
["i2_pel_infantry","Pelargir_Infantryman","Pelargir_Infantrymen",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pelargir,fac_gondor,[itm_pelargir_helmet_light,itm_pel_footman,itm_leather_gloves,itm_gondor_light_greaves,itm_pelargir_sword,itm_gon_tab_shield_b,],attr_tier_2,wp_tier_3,knows_common|knows_ironflesh_1|knows_power_strike_1|knows_power_throw_1|knows_weapon_master_1|knows_shield_4|knows_athletics_1|knows_trainer_1|knows_tactics_2|knows_spotting_1|knows_inventory_management_1|knows_leadership_1|knows_trade_2 ,gondor_face1,gondor_face2],
["i3_pel_vet_infantry","Pelargir_Veteran_Infantryman","Pelargir_Veteran_Infantrymen",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pelargir,fac_gondor,[itm_pelargir_helmet_heavy,itm_pelargir_regular,itm_mail_mittens,itm_pelargir_greaves,itm_pelargir_sword,itm_gon_tab_shield_b,],attr_tier_5,wp_tier_5,knows_common|knows_athletics_2|knows_shield_5|knows_power_strike_5|knows_ironflesh_5,gondor_face1,gondor_face2],
["i6_pel_leader","Captain_of_Pelargir","Captains_of_Pelargir",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pelargir,fac_gondor,[itm_pelargir_helmet_light,itm_pel_leader,itm_mail_mittens,itm_pelargir_greaves,itm_pelargir_sword,itm_gon_tab_shield_c,],attr_tier_6,wp_tier_6,knows_common|knows_athletics_3|knows_shield_9|knows_power_strike_8|knows_ironflesh_10,gondor_face1,gondor_face2],
["a6_pel_marine_leader","Captain_of_Pelargir_Marines","Captains_of_Pelargir_Marine",tf_gondor| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pelargir,fac_gondor,[itm_pelargir_helmet_light,itm_pelargir_marine_leader,itm_pelargir_greaves,itm_pelargir_sword,itm_gon_tab_shield_c,itm_gondor_javelin,],attr_tier_6,wp_tier_6,knows_common|knows_athletics_7|knows_shield_9|knows_power_strike_8|knows_ironflesh_10,gondor_face1,gondor_face2],
#Lamedon
["i1_lam_clansman","Clansman_of_Lamedon","Clansmen_of_Lamedon",tf_gondor| tfg_armor| tfg_boots,0,subfac_ethring,fac_gondor,[itm_lamedon_clansman,itm_gondor_light_greaves,itm_loss_axe,itm_spear,itm_gondor_arrows,itm_gondor_javelin,itm_gondor_javelin,itm_short_bow,],attr_fief_tier_1,wp_tier_1,knows_common|knows_ironflesh_2|knows_power_strike_1|knows_weapon_master_1|knows_athletics_1|knows_looting_1|knows_pathfinding_1|knows_spotting_1|knows_inventory_management_1|knows_surgery_1|knows_first_aid_1|knows_leadership_1|knows_trade_1,gondor_face1,gondor_face2],
["i2_lam_footman","Footman_of_Lamedon","Footmen_of_Lamedon",tf_gondor| tfg_shield| tfg_armor| tfg_boots| tfg_helm,0,subfac_ethring,fac_gondor,[itm_lamedon_hood,itm_lamedon_footman,itm_gondor_light_greaves,itm_gondor_spear,itm_loss_axe,itm_loss_axe,itm_gondor_javelin,itm_gon_tab_shield_a,],attr_fief_tier_2,wp_tier_2,knows_common|knows_ironflesh_2|knows_power_strike_1|knows_power_throw_2|knows_weapon_master_1|knows_athletics_1|knows_looting_1|knows_pathfinding_1|knows_spotting_1|knows_inventory_management_1|knows_surgery_1|knows_first_aid_1|knows_leadership_1|knows_trade_1,gondor_face1,gondor_face2],
["i3_lam_veteran","Veteran_of_Lamedon","Veterans_of_Lamedon",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_ethring,fac_gondor,[itm_gondor_auxila_helm,itm_lamedon_veteran,itm_gondor_light_greaves,itm_loss_axe,itm_gondor_spear,itm_gondor_sword,itm_gon_tab_shield_a,],attr_fief_tier_3,wp_tier_3,knows_common|knows_athletics_4|knows_power_strike_4|knows_ironflesh_5,gondor_face1,gondor_face2],
["i4_lam_warrior","Warrior_of_Lamedon","Warriors_of_Lamedon",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_ethring,fac_gondor,[itm_gondor_auxila_helm,itm_lamedon_warrior,itm_gondor_med_greaves,itm_loss_axe,itm_gondor_sword,itm_gon_tab_shield_d,],attr_fief_tier_4,wp_tier_4,knows_common|knows_athletics_4|knows_power_strike_5|knows_ironflesh_5,gondor_face1,gondor_face2],
["i5_lam_champion","Champion_of_Lamedon","Champions_of_Lamedon",tf_gondor| tfg_gloves| tfg_armor| tfg_helm| tfg_boots,0,subfac_ethring,fac_gondor,[itm_gondor_lamedon_helm,itm_lamedon_vet_warrior,itm_mail_mittens,itm_gondor_heavy_greaves,itm_gondor_2h_sword,itm_gondor_2h_sword,itm_loss_war_axe,],attr_tier_5,wp_tier_5,knows_common|knows_athletics_5|knows_power_strike_5|knows_ironflesh_6,gondor_face1,gondor_face2],
["c5_lam_knight","Knight_of_Lamedon","Knights_of_Lamedon",tf_gondor| tf_mounted | tfg_gloves| tfg_shield| tfg_horse| tfg_armor| tfg_helm| tfg_boots,0,subfac_ethring,fac_gondor,[itm_gondor_lamedon_helm,itm_lamedon_knight,itm_mail_mittens,itm_gondor_heavy_greaves,itm_gondor_cav_sword,itm_gon_tab_shield_c,itm_gondor_lam_horse,],attr_tier_5,wp_tier_5,knows_common|knows_riding_6|knows_power_strike_6|knows_ironflesh_7,gondor_face1,gondor_face2],
["c6_lam_leader","Captain_of_Lamedon","Captains_of_Lamedon",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,subfac_ethring,fac_gondor,[itm_gondor_lamedon_leader_helm,itm_lamedon_leader_surcoat_cloak,itm_mail_mittens,itm_gondor_heavy_greaves,itm_gondor_cav_sword,itm_gon_tab_shield_c,itm_gondor_lam_horse,],attr_tier_6,wp_tier_6,knows_common|knows_riding_8|knows_shield_9|knows_power_strike_8|knows_ironflesh_10,gondor_face1,gondor_face3],
#Pinnath Gelin
["i1_pinnath_plainsman","Plainsman_of_Pinnath_Gelin","Plainsmen_of_Pinnath_Gelin",tf_gondor| tfg_armor| tfg_boots,0,subfac_pinnath_gelin,fac_gondor,[itm_gondor_ranger_hood,itm_pinnath_footman,itm_gondor_light_greaves,itm_shortened_spear,itm_gondor_arrows,itm_short_bow,],attr_fief_tier_1,wp_tier_2,knows_common|knows_ironflesh_2|knows_power_strike_1|knows_power_throw_2|knows_weapon_master_1|knows_athletics_1|knows_looting_1|knows_pathfinding_1|knows_spotting_1|knows_inventory_management_1|knows_surgery_1|knows_first_aid_1|knows_leadership_1|knows_trade_1,gondor_face1,gondor_face2],
["c2_pinnath_rider","Rider_of_Pinnath_Gelin","Riders_of_Pinnath_Gelin",tf_gondor|tf_mounted|tfg_shield| tfg_armor| tfg_helm| tfg_boots|tfg_horse,0,subfac_pinnath_gelin,fac_gondor,[itm_gondor_auxila_helm,itm_pinnath_warrior,itm_leather_gloves,itm_gondor_light_greaves,itm_good_mace,itm_gon_tab_shield_a,itm_gondor_courser,],attr_tier_2,wp_tier_4,knows_common|knows_ironflesh_1|knows_power_strike_2|knows_power_draw_1|knows_athletics_2|knows_riding_3|knows_horse_archery_1|knows_trainer_1|knows_pathfinding_1|knows_spotting_1|knows_inventory_management_1|knows_first_aid_1|knows_persuasion_1|knows_trade_1,gondor_face1,gondor_face2],
["c3_pinnath_knight","Knight_of_Pinnath_Gelin","Knights_of_Pinnath_Gelin",tf_gondor|tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots|tfg_horse,0,subfac_pinnath_gelin,fac_gondor,[itm_gondor_knight_helm_bad,itm_pinnath_leader,itm_leather_gloves,itm_gondor_med_greaves,itm_gondor_heavy_greaves, itm_good_mace,itm_gondor_lance,itm_gon_tab_shield_c,itm_gondor_hunter,],attr_tier_5,wp_tier_5,knows_common|knows_athletics_5|knows_riding_6|knows_power_strike_4|knows_ironflesh_5,gondor_face1,gondor_face2],
["a2_pinnath_bowman","Bowman_of_Pinnath_Gelin","Bowmen_of_Pinnath_Gelin",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,subfac_pinnath_gelin,fac_gondor,[itm_gondor_ranger_hood,itm_pinnath_vet_footman,itm_gondor_light_greaves,itm_gondor_arrows,itm_regular_bow,itm_good_mace,],attr_tier_2,wp_tier_bow_4,knows_common|knows_power_strike_1|knows_power_draw_3|knows_athletics_4|knows_riding_1|knows_horse_archery_1|knows_trainer_1|knows_pathfinding_1|knows_spotting_1|knows_inventory_management_1|knows_first_aid_1|knows_persuasion_1|knows_trade_1,gondor_face1,gondor_face2],
["a3_pinnath_archer","Archer_of_Pinnath_Gelin","Archers_of_Pinnath_Gelin",tf_gondor| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pinnath_gelin,fac_gondor,[itm_gondor_ranger_hood,itm_gondor_auxila_helm,itm_pinnath_archer,itm_gondor_med_greaves,itm_gondor_arrows,itm_regular_bow,itm_good_mace,],attr_fief_tier_4,wp_tier_bow_5,knows_common|knows_athletics_6|knows_power_draw_5|knows_power_strike_5|knows_ironflesh_4,gondor_face1,gondor_face2],
["c6_pinnath_leader","Captain_of_Pinnath_Gelin","Captains_of_Pinnath_Gelin",tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,subfac_pinnath_gelin,fac_gondor,[itm_gondor_leader_helm,itm_pinnath_leader,itm_mail_mittens,itm_gondor_heavy_greaves,itm_gondor_cav_sword,itm_gon_tab_shield_c,itm_gondor_hunter,],attr_tier_6,wp_tier_6,knows_common|knows_riding_8|knows_shield_9|knows_power_strike_8|knows_ironflesh_10,gondor_face1,gondor_face3],
#Blackroot Vale
["a1_blackroot_hunter","Hunter_of_Blackroot_Vale","Hunters_of_Blackroot_Vale",tf_gondor|  tfg_armor|  tfg_boots,0,subfac_blackroot,fac_gondor,[itm_hood_black,itm_blackroot_footman,itm_gondor_light_greaves,itm_short_bow,itm_gondor_arrows,itm_shortened_spear,],attr_fief_tier_1,wp_tier_bow_2,knows_common|knows_ironflesh_1|knows_power_draw_2|knows_athletics_2|knows_looting_1|knows_tracking_2|knows_spotting_2|knows_surgery_1|knows_prisoner_management_1|knows_leadership_1,gondor_face1,gondor_face2],
["a2_blackroot_bowman","Bowman_of_Blackroot_Vale","Bowmen_of_Blackroot_Vale",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,subfac_blackroot,fac_gondor,[itm_hood_black,itm_blackroot_footman,itm_gondor_light_greaves,itm_gondor_arrows,itm_regular_bow,itm_gondor_short_sword,],attr_tier_2,wp_tier_bow_3,knows_common|knows_ironflesh_1|knows_power_draw_3|knows_athletics_3|knows_looting_1|knows_tracking_2|knows_spotting_2|knows_surgery_1|knows_prisoner_management_1|knows_leadership_1,gondor_face1,gondor_face2],
["a3_blackroot_archer","Archer_of_Blackroot_Vale","Archers_of_Blackroot_Vale",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,subfac_blackroot,fac_gondor,[itm_hood_black,itm_blackroot_bowman,itm_gondor_med_greaves,itm_gondor_arrows,itm_gondor_bow,itm_gondor_short_sword,],attr_fief_tier_4,wp_tier_bow_4,knows_common|knows_athletics_5|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_3,gondor_face1,gondor_face2],
["i2_blackroot_footman","Footman_of_Blackroot_Vale","Footmen_of_Blackroot_Vale",tf_gondor| tfg_armor| tfg_helm| tfg_boots,0,subfac_blackroot,fac_gondor,[itm_gondor_auxila_helm_bad,itm_blackroot_footman,itm_gondor_light_greaves,itm_gondor_spear,itm_gon_tab_shield_a,],attr_tier_2,wp_tier_3,knows_common|knows_ironflesh_2|knows_power_strike_2|knows_power_draw_2|knows_athletics_2|knows_looting_1|knows_tracking_2|knows_spotting_2|knows_surgery_1|knows_prisoner_management_1|knows_leadership_1,gondor_face1,gondor_face2],
["i3_blackroot_spearman","Spearman_of_Blackroot_Vale","Spearmen_of_Blackroot_Vale",tf_gondor| tfg_gloves| tfg_armor| tfg_helm| tfg_boots,0,subfac_blackroot,fac_gondor,[itm_gondor_auxila_helm,itm_blackroot_warrior,itm_leather_gloves,itm_gondor_med_greaves,itm_gondor_spear,itm_gon_tab_shield_d,],attr_fief_tier_4,wp_tier_4,knows_common|knows_athletics_5|knows_power_strike_5|knows_ironflesh_5,gondor_face1,gondor_face2],
["a5_blackroot_shadow_hunter","Morthond_Shadow_Hunter","Morthond_Shadow_Hunters",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,subfac_blackroot,fac_gondor,[itm_hood_black,itm_blackroot_leader,itm_leather_gloves_good,itm_gondor_med_greaves,itm_gondor_arrows,itm_gondor_bow,itm_gon_tab_shield_c,itm_gondor_spear,],attr_tier_5,wp_melee(200)|wp_archery(200),knows_common|knows_athletics_7|knows_power_draw_5|knows_power_strike_5|knows_ironflesh_5,gondor_face1,gondor_face3],
#Dol Amroth
["i1_amroth_recruit","Dol_Amroth_Recruit","Dol_Amroth_Recruits",tf_gondor| tfg_armor| tfg_shield| tfg_boots,0,subfac_dol_amroth,fac_gondor,[itm_gondor_auxila_helm,itm_dol_shirt,itm_dol_shoes,itm_gondor_spear,itm_gon_tab_shield_a,],attr_tier_1,wp_tier_1,knows_common|knows_ironflesh_1|knows_power_strike_1|knows_power_draw_1|knows_riding_2|knows_trainer_1|knows_tactics_2|knows_inventory_management_1|knows_wound_treatment_1|knows_prisoner_management_1|knows_leadership_2,gondor_face1,gondor_face2],
["c2_amroth_squire","Squire_of_Dol_Amroth","Squires_of_Dol_Amroth",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,subfac_dol_amroth,fac_gondor,[itm_gondor_auxila_helm_good,itm_dol_padded_coat,itm_leather_gloves,itm_dol_shoes,itm_gondor_lance,itm_amroth_sword_a,itm_gondor_lance,itm_gondor_lance,itm_gon_tab_shield_c,itm_gondor_hunter,],attr_tier_2,wp_tier_2,knows_common|knows_ironflesh_2|knows_power_strike_2|knows_power_draw_1|knows_riding_2|knows_trainer_1|knows_tactics_2|knows_inventory_management_1|knows_wound_treatment_1|knows_prisoner_management_1|knows_leadership_2,gondor_face1,gondor_face3],
["c3_amroth_vet_squire","Veteran_Squire_of_Dol_Amroth","Veteran_Squires_of_Dol_Amroth",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm,0,subfac_dol_amroth,fac_gondor,[itm_gondor_dolamroth_helm_bad,itm_dol_padded_coat,itm_leather_gloves,itm_dol_shoes,itm_gondor_lance,itm_amroth_sword_a,itm_gondor_lance,itm_gon_tab_shield_c,itm_gondor_hunter,],attr_tier_3,wp_tier_3,knows_common|knows_riding_3|knows_shield_3|knows_power_strike_3|knows_ironflesh_3,gondor_face1,gondor_face3],
["c4_amroth_knight","Knight_of_Dol_Amroth","Knights_of_Dol_Amroth",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots|tfg_polearm,0,subfac_dol_amroth,fac_gondor,[itm_gondor_dolamroth_helm,itm_dol_hauberk,itm_mail_mittens,itm_dol_greaves,itm_gondor_lance,itm_gondor_lance,itm_amroth_sword_b,itm_gondor_lance,itm_gondor_lance,itm_gon_tab_shield_c,itm_dol_amroth_warhorse,],attr_tier_4,wp_tier_4,knows_common|knows_riding_4|knows_shield_4|knows_power_strike_4|knows_ironflesh_4,gondor_face1,gondor_face3],
["c5_amroth_vet_knight","Veteran_Knight_of_Dol_Amroth","Veteran_Knights_of_Dol_Amroth",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm,0,subfac_dol_amroth,fac_gondor,[itm_gondor_dolamroth_helm_good,itm_dol_heavy_mail,itm_dol_heavy_mail,itm_mail_mittens,itm_dol_greaves,itm_gondor_lance,itm_gondor_lance,itm_amroth_sword_b,itm_gondor_lance,itm_gondor_lance,itm_gon_tab_shield_c,itm_dol_amroth_warhorse,],attr_tier_5,wp_tier_5,knows_common|knows_riding_5|knows_shield_4|knows_power_strike_5|knows_ironflesh_5,gondor_face1,gondor_face3],
["c6_amroth_swan_knight","Swan_Knight_of_Dol_Amroth","Swan_Knights_of_Dol_Amroth",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm,0,subfac_dol_amroth,fac_gondor,[itm_swan_knight_helm,itm_dol_very_heavy_mail,itm_mail_mittens,itm_dol_greaves,itm_amroth_lance_banner,itm_amroth_sword_b,itm_gon_tab_shield_c,itm_dol_amroth_warhorse2,],attr_tier_6,wp(360),knows_common|knows_riding_8|knows_shield_4|knows_power_strike_8|knows_ironflesh_6,gondor_face1,gondor_face3],
["c6_amroth_leader","Captain_of_Dol_Amroth","Captains_of_Dol_Amroth",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm,0,subfac_dol_amroth,fac_gondor,[itm_gondor_leader_helm,itm_dol_very_heavy_mail,itm_mail_mittens,itm_dol_greaves,itm_amroth_bastard,itm_amroth_lance_banner,itm_gon_tab_shield_c,itm_dol_amroth_warhorse2,],attr_tier_6,wp_tier_6,knows_common|knows_riding_8|knows_shield_9|knows_power_strike_8|knows_ironflesh_10,gondor_face1,gondor_face3],

#Lothlorien #Lorien
["a1_lorien_scout","Lothlorien_Scout","Lothlorien_Scouts",tf_lorien| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_hood_grey,itm_lorien_archer,itm_lorien_boots,itm_short_bow,itm_elven_arrows,itm_lorien_sword_b,],attr_elf_tier_1,wp_elf_tier_1,knows_common|knows_power_strike_1|knows_power_draw_2|knows_weapon_master_1|knows_athletics_2|knows_tactics_1|knows_pathfinding_1|knows_spotting_1|knows_wound_treatment_1|knows_surgery_1|knows_persuasion_2,lorien_elf_face_1,lorien_elf_face_2],
["a2_lorien_warden","Lothlorien_Warden","Lothlorien_Wardens",tf_lorien| tf_mounted| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_lorien_helm_a,itm_hood_grey,itm_lorien_archer_cloak,itm_lorien_boots,itm_regular_bow,itm_elven_arrows,itm_lorien_sword_b,itm_lorien_round_shield,],attr_elf_tier_2,wp_elf_tier_2,knows_common|knows_ironflesh_1|knows_power_strike_2|knows_power_draw_2|knows_weapon_master_1|knows_shield_1|knows_athletics_3|knows_tactics_1|knows_pathfinding_1|knows_spotting_1|knows_wound_treatment_1|knows_surgery_1|knows_persuasion_2,lorien_elf_face_1,lorien_elf_face_2],
["a3_lorien_vet_warden","Lothlorien_Veteran_Warden","Lothlorien_Veteran_Wardens",tf_lorien| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_lorien_helm_a,itm_lorien_archer_good_cloak,itm_lorien_boots,itm_elven_bow,itm_elven_arrows,itm_lorien_sword_b,itm_lorien_round_shield,],attr_elf_tier_3,wp_elf_tier_3,knows_common|knows_athletics_6|knows_shield_3|knows_power_draw_4|knows_power_strike_3|knows_ironflesh_2,lorien_elf_face_1,lorien_elf_face_2],
["a4_lorien_gal_warden","Galadhrim_Warden","Galadhrim_Wardens",tf_lorien| tf_mounted| tfg_ranged| tfg_shield| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_lorien_helm_a_good,itm_lorien_light_cloak,itm_leather_gloves,itm_lorien_boots,itm_elven_bow,itm_elven_arrows,itm_lorien_sword_a,itm_lorien_shield_c,],attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_7|knows_shield_4|knows_power_draw_4|knows_power_strike_3|knows_ironflesh_3,lorien_elf_face_1,lorien_elf_face_2],
["a5_lorien_gal_royal_warden","Galadhrim_Royal_Warden","Galadhrim_Royal_Wardens",tf_lorien| tf_mounted| tfg_ranged| tfg_shield| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_lorien_helm_b,itm_lorien_med_cloak,itm_leather_gloves,itm_lorien_boots,itm_lorien_bow_reward,itm_elven_arrows,itm_lorien_sword_a,itm_lorien_shield_c,],attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_8|knows_shield_5|knows_power_draw_5|knows_power_strike_4|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["a6_lorien_grey_warden","Grey_Warden","Grey_Wardens",tf_lorien| tf_mounted| tfg_ranged| tfg_shield| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_lorien_helm_b_good,itm_lorien_heavy_good_cloak,itm_leather_gloves_good,itm_lorien_boots,(itm_lorien_bow_reward, imod_balanced), itm_elven_arrows,itm_lorien_sword_a,itm_lorien_shield_c,],attr_elf_tier_6,wp_melee(460)|wp_archery(320),knows_common|knows_athletics_9|knows_shield_5|knows_power_draw_6|knows_power_strike_5|knows_ironflesh_5,lorien_elf_face_1,lorien_elf_face_2],
["galadhrim_royal_marksman","Galadhrim_Royal_Marksman","Galadhrim_Royal_Marksmen",tf_lorien| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_lorien_helm_b,itm_lorien_med_cloak,itm_lorien_boots,itm_lorien_bow,itm_elven_arrows,itm_lorien_sword_b,itm_lorien_shield_c,],attr_elf_tier_6,wp_elf_tier_bow_5,knows_common|knows_athletics_7|knows_shield_1|knows_power_draw_6|knows_power_strike_5|knows_ironflesh_6,lorien_elf_face_1,lorien_elf_face_2],
["noldorin_mounted_archer","Noldorin_Mounted_Archer","Noldorin_Mounted_Archers",tf_lorien| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_lorien_helm_b,itm_lorien_med_good_cloak,itm_lorien_boots,itm_lorien_bow_reward,itm_elven_arrows,itm_lorien_sword_a,itm_lorien_round_shield,itm_lorien_warhorse,],attr_elf_tier_6,wp_elf_tier_bow_6,knows_common|knows_horse_archery_7|knows_riding_7|knows_athletics_5|knows_power_draw_5|knows_power_strike_4|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["a2_lorien_archer","Lothlorien_Archer","Lothlorien_Archers",tf_lorien| tfg_ranged| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_lorien_helm_a,itm_lorien_light,itm_leather_gloves,itm_lorien_boots,itm_elven_bow,itm_elven_arrows,itm_lorien_sword_b,],attr_elf_tier_2,wp_elf_tier_bow_2,knows_common|knows_ironflesh_1|knows_power_strike_2|knows_power_draw_3|knows_weapon_master_1|knows_athletics_3|knows_tactics_1|knows_pathfinding_1|knows_spotting_1|knows_wound_treatment_1|knows_surgery_1|knows_persuasion_2,lorien_elf_face_1,lorien_elf_face_2],
["a3_lorien_vet_archer","Lothlorien_Veteran_Archer","Lothlorien_Veteran_Archers",tf_lorien|tfg_ranged| tfg_gloves| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_lorien_helm_a,itm_lorien_med_bad,itm_lorien_boots,itm_elven_bow,itm_elven_arrows,itm_lorien_sword_a,],attr_elf_tier_3,wp_elf_tier_bow_3,knows_common|knows_athletics_5|knows_power_draw_3|knows_power_strike_4|knows_ironflesh_2,lorien_elf_face_1,lorien_elf_face_2],
["a4_lorien_gal_archer","Galadhrim_Archer","Galadhrim_Archers",tf_lorien| tfg_ranged|tfg_gloves| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_lorien_helm_a_good,itm_lorien_med,itm_leather_gloves,itm_lorien_boots,itm_lorien_bow,itm_elven_arrows,itm_lorien_sword_c,],attr_elf_tier_4,wp_elf_tier_bow_4,knows_common|knows_athletics_5|knows_power_draw_3|knows_power_strike_5|knows_ironflesh_3,lorien_elf_face_1,lorien_elf_face_2],
["a5_lorien_gal_royal_archer","Galadhrim_Royal_Marksman","Galadhrim_Royal_Marksmen",tf_lorien|tfg_ranged| tfg_gloves| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_lorien_helm_a_good,itm_lorien_med_good,itm_leather_gloves_good,itm_lorien_boots,itm_lorien_bow,itm_elven_arrows,itm_elven_arrows,itm_lorien_sword_c,],attr_elf_tier_5,wp_elf_tier_bow_5,knows_common|knows_athletics_5|knows_power_draw_6|knows_power_strike_5|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["i3_lorien_inf","Lothlorien_Infantry","Lothlorien_Infantry",tf_lorien| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_lorien_helm_b,itm_lorien_med_good,itm_leather_gloves,itm_lorien_boots,itm_lorien_sword_b,itm_lorien_shield_c,],attr_elf_tier_3,wp_elf_tier_3,knows_common|knows_athletics_3|knows_shield_3|knows_power_draw_5|knows_power_strike_4|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["i4_lorien_gal_inf","Galadhrim_Infantry","Galadhrim_Infantry",tf_lorien| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_lorien_helm_b,itm_lorien_armor_c,itm_mail_mittens,itm_lorien_boots,itm_lorien_sword_a,itm_lorien_shield_b,],attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_4|knows_shield_4|knows_power_draw_5|knows_power_strike_5|knows_ironflesh_5,lorien_elf_face_1,lorien_elf_face_2],
["i5_lorien_gal_royal_inf","Galadhrim_Royal_Guard","Galadhrim_Royal_Guards",tf_lorien|  tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_lorien_helm_b_good,itm_lorien_heavy_good,itm_mail_mittens,itm_lorien_boots,itm_lorien_sword_a,itm_lorien_shield_b,],attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_4|knows_shield_5|knows_power_draw_6|knows_power_strike_6|knows_ironflesh_6,lorien_elf_face_1,lorien_elf_face_2],
["lothlorien_standard_bearer","Lothlorien_Standard_Bearer","Lothlorien_Standard_Bearers",tf_lorien| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,[itm_lorien_helm_b_good,itm_lorien_heavy_good_cloak,itm_mail_mittens,itm_lorien_boots,itm_lorien_banner,],attr_elf_tier_6,wp_elf_tier_6,knows_common|knows_athletics_3|knows_power_draw_3|knows_power_strike_7|knows_ironflesh_10,lorien_elf_face_1,lorien_elf_face_2],

["lorien_items","BUG","_",tf_hero,0,0,fac_lorien,
   [itm_sumpter_horse, itm_saddle_horse,itm_short_bow,itm_regular_bow,itm_arrows,itm_good_mace,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
	  
##MIRKWOOD#####
["a1_greenwood_scout","Greenwood_Scout","Greenwood_Scouts",tf_woodelf| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,[itm_hood_green_bad, itm_mirkwood_leather_bad,itm_rohan_shoes,itm_leather_boots_dark_bad,itm_short_bow,itm_woodelf_arrows,itm_mirkwood_knife,itm_mirkwood_short_spear,],attr_elf_tier_1,wp_elf_tier_bow_1,knows_common|knows_ironflesh_1|knows_power_strike_1|knows_power_draw_2|knows_athletics_4|knows_looting_1|knows_tracking_1|knows_tactics_1|knows_pathfinding_1|knows_spotting_1|knows_persuasion_1,mirkwood_elf_face_1,mirkwood_elf_face_2],
["a2_greenwood_veteran_scout","Greenwood_Veteran_Scout","Greenwood_Veteran_Scouts",tf_woodelf| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,[itm_mirkwood_helm_a_bad,itm_hood_green,itm_mirkwood_leather,itm_mirkwood_pad_bad,itm_leather_boots_bad,itm_leather_boots_dark_bad,itm_rohan_shoes,itm_regular_bow,itm_woodelf_arrows,itm_mirkwood_knife,itm_mirkwood_short_spear,itm_mirkwood_axe,],attr_elf_tier_2,wp_elf_tier_bow_2,knows_common|knows_ironflesh_1|knows_power_strike_2|knows_power_draw_4|knows_athletics_4|knows_looting_1|knows_tracking_1|knows_tactics_1|knows_pathfinding_1|knows_spotting_1|knows_persuasion_1,mirkwood_elf_face_1,mirkwood_elf_face_2],
["a3_greenwood_archer","Greenwood_Archer","Greenwood_Archers",tf_woodelf| tfg_ranged| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,[itm_mirkwood_helm_a_bad,itm_mirkwood_pad,itm_leather_boots, itm_leather_boots_dark,itm_elven_bow,itm_woodelf_arrows,itm_mirkwood_short_spear,],attr_elf_tier_3,wp_elf_tier_bow_3,knows_common|knows_athletics_5|knows_power_draw_5|knows_power_strike_3|knows_ironflesh_3,mirkwood_elf_face_1,mirkwood_elf_face_2],
["a4_greenwood_veteran_archer","Greenwood_Veteran_Archer","Greenwood_Veteran_Archers",tf_woodelf| tfg_ranged| tfg_gloves| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,[itm_mirkwood_helm_a,itm_mirkwood_pad_good,itm_mirkwood_mail_bad,itm_mirkwood_boots,itm_leather_boots,itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_short_spear,],attr_elf_tier_4,wp_elf_tier_bow_4,knows_common|knows_athletics_6|knows_power_draw_6|knows_power_strike_3|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["a5_greenwood_master_archer","Greenwood_Master_Archer","Greenwood_Master_Archers",tf_woodelf| tfg_ranged| tfg_gloves| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,[itm_mirkwood_helm_a_good,itm_mirkwood_mail,itm_leather_gloves,itm_mirkwood_boots,itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_war_spear,],attr_elf_tier_5,wp_elf_tier_bow_5,knows_common|knows_athletics_7|knows_power_draw_6|knows_power_strike_4|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["a6_greenwood_chosen_marksman","Thranduil's_Chosen_Marksman","Thranduil's_Chosen_Marksmen",tf_woodelf| tfg_ranged| tfg_gloves|  tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,[itm_mirkwood_helm_d,itm_mirkwood_mail_good,itm_leather_gloves,itm_mirkwood_boots,itm_mirkwood_bow,itm_woodelf_arrows,itm_woodelf_arrows,itm_mirkwood_great_spear,],attr_elf_tier_6,wp_elf_tier_bow_6,knows_common|knows_athletics_8|knows_power_draw_7|knows_power_strike_5|knows_ironflesh_5,mirkwood_elf_face_1,mirkwood_elf_face_2],
["a3_greenwood_sentinel","Greenwood_Sentinel","Greenwood_Sentinels",tf_woodelf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,[itm_mirkwood_helm_a_bad,itm_hood_green,itm_mirkwood_leather_good,itm_mirkwood_boots,itm_leather_boots,itm_elven_bow,itm_woodelf_arrows,itm_mirkwood_axe,itm_mirkwood_spear_shield_c,],attr_elf_tier_3,wp_elf_tier_3,knows_common|knows_athletics_6|knows_shield_2|knows_power_draw_5|knows_power_strike_4|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["a4_greenwood_vet_sentinel","Greenwood_Veteran_Sentinel","Greenwood_Veteran_Sentinels",tf_woodelf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor|tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,[itm_mirkwood_helm_a,itm_mirkwood_pad_bad,itm_mirkwood_leather_good,itm_mirkwood_boots,itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_axe,itm_mirkwood_sword,itm_mirkwood_spear_shield_c,],attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_8|knows_shield_3|knows_power_draw_6|knows_power_strike_4|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["a5_greenwood_vigilant","Greenwood_Guardian","Greenwood_Guardians",tf_woodelf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,[itm_mirkwood_helm_a_good,itm_mirkwood_mail_bad,itm_leather_gloves,itm_mirkwood_boots,itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_axe,itm_mirkwood_sword,itm_mirkwood_spear_shield_c,],attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_9|knows_shield_5|knows_power_draw_6|knows_power_strike_5|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["i2_greenwood_infantry","Greenwood_Infantry","Greenwood_Infantry",tf_woodelf| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,[itm_mirkwood_helm_a_good,itm_mirkwood_helm_b,itm_hood_green,itm_mirkwood_scale_bad,itm_mirkwood_boots,itm_leather_boots,itm_mirkwood_war_spear,itm_mirkwood_short_spear,itm_mirkwood_axe,itm_mirkwood_knife,itm_mirkwood_spear_shield_a,],attr_elf_tier_2,wp_elf_tier_2,knows_common|knows_ironflesh_2|knows_power_strike_3|knows_weapon_master_1|knows_shield_1|knows_athletics_4|knows_looting_1|knows_tracking_1|knows_tactics_1|knows_pathfinding_1|knows_spotting_1|knows_persuasion_1,mirkwood_elf_face_1,mirkwood_elf_face_2],
["i3_greenwood_vet_infantry","Greenwood_Veteran_Infantry","Greenwood_Veteran_Infantry",tf_woodelf| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots |tfg_polearm| tf_no_capture_alive,0,0,fac_woodelf,[itm_mirkwood_helm_b_good,itm_mirkwood_helm_c,itm_mirkwood_scale,itm_leather_gloves,itm_mirkwood_boots,itm_mirkwood_war_spear,itm_mirkwood_axe,itm_mirkwood_sword,itm_mirkwood_spear_shield_a,],attr_elf_tier_3,wp_elf_tier_3,knows_common|knows_athletics_6|knows_shield_3|knows_power_strike_4|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["i4_greenwood_elite_infantry","Greenwood_Elite_Infantry","Greenwood_Elite_Infantry",tf_woodelf| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots |tfg_polearm| tf_no_capture_alive,0,0,fac_woodelf,[itm_mirkwood_helm_c_good,itm_mirkwood_scale_good,itm_leather_gloves,itm_mirkwood_boots,itm_mirkwood_war_spear,itm_mirkwood_axe,itm_mirkwood_sword,itm_mirkwood_spear_shield_b,],attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_7|knows_shield_4|knows_power_strike_5|knows_ironflesh_5,mirkwood_elf_face_1,mirkwood_elf_face_2],
["i5_greenwood_chosen_shieldmaster","Thranduil's_Chosen_Shield_Master","Thranduil's_Chosen_Shield_Masters",tf_woodelf| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots |tfg_polearm| tf_no_capture_alive,0,0,fac_woodelf,[itm_mirkwood_helm_d_good,itm_mirkwood_scale_good,itm_leather_gloves,itm_mirkwood_boots,itm_mirkwood_war_spear,itm_mirkwood_axe,itm_mirkwood_sword,itm_mirkwood_spear_shield_b,],attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_8|knows_shield_6|knows_power_strike_6|knows_ironflesh_6,mirkwood_elf_face_1,mirkwood_elf_face_2],
["i5_greenwood_chosen_spearmaster","Thranduil's_Chosen_Spear_Master","Thranduil's_Chosen_Spear_Masters",tf_woodelf| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots |tfg_polearm| tf_no_capture_alive,0,0,fac_woodelf,[itm_mirkwood_helm_d_good,itm_mirkwood_heavy_scale,itm_mail_mittens,itm_mirkwood_boots,itm_mirkwood_great_spear,],attr_elf_tier_5,wp_elf_tier_6,knows_common|knows_athletics_8|knows_power_strike_7|knows_ironflesh_7,mirkwood_elf_face_1,mirkwood_elf_face_2],
["i5_greenwood_standard_bearer","Greenwood_Standard_Bearer","Greenwood_Standard_Bearers",tf_woodelf| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,[itm_mirkwood_helm_d_good,itm_mirkwood_mail_good,itm_leather_gloves,itm_mirkwood_boots,itm_woodelf_banner,],attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_4|knows_power_draw_6|knows_power_strike_4|knows_ironflesh_10,mirkwood_elf_face_1,mirkwood_elf_face_2],

["woodelf_items","BUG","_",tf_hero,0,0,fac_woodelf,
   [itm_leather_boots,itm_leather_gloves,itm_short_bow,itm_regular_bow,itm_arrows,itm_sumpter_horse,itm_saddle_horse,itm_good_mace,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
#Rivendell #Imladris
["a1_riv_scout","Rivendell_Scout","Rivendell_Scouts",tf_imladris| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,[itm_hood_grey_bad,itm_riv_light_cloak,itm_rohan_shoes,itm_leather_boots,itm_short_bow,itm_elven_arrows,itm_riv_archer_sword,],attr_elf_tier_1,wp_elf_tier_1,knows_common|knows_power_strike_1|knows_power_draw_1|knows_weapon_master_2|knows_athletics_1|knows_riding_1|knows_horse_archery_1|knows_trainer_1|knows_tactics_1|knows_spotting_1|knows_wound_treatment_1|knows_first_aid_1|knows_leadership_1|knows_trade_1,rivendell_elf_face_1,rivendell_elf_face_2],
["a2_riv_vet_scout","Rivendell_Veteran_Scout","Rivendell_Veteran_Scouts",tf_imladris| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,[itm_hood_grey,itm_riv_leather_cloak,itm_riv_boots,itm_leather_boots,itm_regular_bow,itm_elven_arrows,itm_riv_archer_sword,],attr_elf_tier_2,wp_elf_tier_2,knows_common|knows_ironflesh_1|knows_power_strike_2|knows_power_draw_1|knows_weapon_master_3|knows_athletics_1|knows_riding_1|knows_horse_archery_1|knows_trainer_1|knows_tactics_1|knows_spotting_1|knows_wound_treatment_1|knows_first_aid_1|knows_leadership_1|knows_trade_1,rivendell_elf_face_1,rivendell_elf_face_2],
["a3_riv_archer","Rivendell_Archer","Rivendell_Archers",tf_imladris| tfg_ranged| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,[itm_riv_helm_b,itm_hood_grey,itm_riv_leather_cloak,itm_leather_gloves,itm_riv_boots,itm_leather_boots,itm_elven_bow,itm_elven_arrows,itm_riv_1h_sword,],attr_elf_tier_3,wp_elf_tier_3,knows_common|knows_athletics_4|knows_power_draw_4|knows_power_strike_3|knows_ironflesh_3,rivendell_elf_face_1,rivendell_elf_face_2],
["a4_riv_vet_archer","Rivendell_Veteran_Archer","Rivendell_Veteran_Archers",tf_imladris| tfg_ranged| tfg_gloves| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,[itm_riv_helm_b,itm_riv_foot_mail_cloak,itm_leather_gloves,itm_riv_boots,itm_riv_bow,itm_elven_arrows,itm_riv_1h_sword,],attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_5|knows_power_draw_4|knows_power_strike_3|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["a5_riv_master_archer","Rivendell_Master_Archer","Rivendell_Master_Archers",tf_imladris| tfg_ranged| tfg_gloves| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,[itm_riv_helm_b,itm_riv_foot_mail_cloak,itm_leather_gloves_good,itm_riv_boots,itm_riv_bow,itm_elven_arrows,itm_riv_bas_sword,],attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_5|knows_power_draw_5|knows_power_strike_4|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["a6_riv_guardian","Guardian_of_Imladris","Guardians_of_Imladris",tf_imladris| tfg_ranged| tfg_gloves| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,[itm_riv_helm_b,itm_riv_foot_scale_cloak,itm_leather_gloves_good,itm_riv_boots,itm_riv_bow,itm_elven_arrows,itm_riv_bas_sword,],attr_elf_tier_6,wp_elf_tier_6,knows_common|knows_athletics_5|knows_power_draw_6|knows_power_strike_5|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["i3_riv_swordbearer","Rivendell_Swordbearer","Rivendell_Swordbearers",tf_imladris| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,[itm_riv_helm_b,itm_riv_foot_mail,itm_leather_gloves,itm_riv_boots,itm_riv_1h_sword,itm_riv_archer_sword,itm_riv_shield_a,],attr_elf_tier_3,wp_elf_tier_3,knows_common|knows_athletics_4|knows_shield_3|knows_power_draw_4|knows_power_strike_3|knows_ironflesh_3,rivendell_elf_face_1,rivendell_elf_face_2],
["i4_riv_vet_swordbearer","Rivendell_Veteran_Swordbearer","Rivendell_Veteran_Swordbearers",tf_imladris| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,[itm_riv_helm_b,itm_riv_foot_mail_good, itm_riv_surcoat,itm_leather_gloves,itm_riv_boots,itm_riv_1h_sword,itm_riv_shield_a,],attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_5|knows_shield_4|knows_power_draw_4|knows_power_strike_4|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["i5_riv_swordmaster","Rivendell_Swordmaster","Rivendell_Swordmasters",tf_imladris| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,[itm_riv_helm_c,itm_riv_surcoat_good,itm_riv_foot_scale,itm_leather_gloves_good,itm_riv_boots,itm_riv_1h_sword,itm_riv_shield_a_good,],attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_5|knows_shield_5|knows_power_draw_5|knows_power_strike_5|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["i6_riv_champion","Champion_of_Imladris","Champions_of_Imladris",tf_imladris| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,[itm_riv_helm_c,itm_riv_foot_scale_lordly,itm_riv_knight_good,itm_riv_surcoat_lordly,itm_mail_mittens,itm_riv_boots,itm_riv_1h_sword,itm_riv_bas_sword,itm_riv_shield_a_good,],attr_elf_tier_6,wp_elf_tier_6,knows_common|knows_athletics_5|knows_shield_6|knows_power_strike_7|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["ac5_riv_rider","Rivendell_Rider","Rivendell_Riders",tf_imladris| tfg_ranged| tf_mounted| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,[itm_riv_helm_b,itm_riv_foot_scale, itm_riv_surcoat_good,itm_leather_gloves,itm_riv_boots,(itm_lorien_bow_reward,imod_bent), itm_elven_arrows,itm_riv_shield_b,itm_riv_spear,itm_riv_riding_sword,itm_riv_warhorse,],attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_riding_5|knows_shield_3|knows_athletics_5|knows_horse_archery_6|knows_power_draw_4|knows_power_strike_4|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["ac6_riv_knight","Knight_of_Imladris","Knights_of_Imladris",tf_imladris| tfg_ranged| tf_mounted| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,[itm_riv_helm_c,itm_riv_foot_scale_cloak, itm_riv_knight_cloak,itm_leather_gloves_good,itm_riv_boots,itm_lorien_bow_reward, itm_elven_arrows,itm_riv_bas_sword,itm_riv_shield_b_good,itm_riv_spear,itm_riv_riding_sword,itm_riv_warhorse2,],attr_elf_tier_6,wp_elf_tier_6,knows_common|knows_riding_6|knows_shield_4|knows_horse_archery_9|knows_athletics_5|knows_power_draw_5|knows_power_strike_5|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["i6_rivendell_standard_bearer","Rivendell_Standard_Bearer","Rivendell_Standard_Bearers",tf_imladris| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,[itm_riv_helm_c,itm_riv_foot_scale_good, itm_riv_knight_good, itm_mail_mittens,itm_riv_boots,itm_imladris_banner,],attr_elf_tier_6,wp_elf_tier_6,knows_common|knows_athletics_3|knows_power_draw_6|knows_power_strike_6|knows_ironflesh_10,rivendell_elf_face_1,rivendell_elf_face_2],

#Dunedain #Arnor
["a1_arnor_scout","Dunedain_Scout","Dunedain_Scouts",tf_dunedain| tfg_armor| tfg_boots,0,0,fac_imladris,[itm_hood_grey_bad,itm_arnor_armor_c,itm_leather_gloves,itm_leather_boots_dark_bad,itm_short_bow,itm_arrows,itm_arnor_sword_f,],attr_elf_tier_1,wp_elf_tier_1,knows_common|knows_ironflesh_2|knows_power_strike_1|knows_power_draw_2|knows_athletics_1|knows_tracking_1|knows_tactics_1|knows_pathfinding_1|knows_spotting_1|knows_wound_treatment_1|knows_persuasion_1|knows_leadership_1,arnor_face_middle_1,arnor_face_middle_2],
["a2_arnor_vet_scout","Dunedain_Tracker","Dunedain_Trackers",tf_dunedain| tfg_armor| tfg_boots,0,0,fac_imladris,[itm_hood_grey,itm_arnor_armor_c,itm_leather_gloves,itm_leather_boots,itm_leather_boots_dark_bad,itm_regular_bow,itm_arrows,itm_arnor_sword_f,],attr_elf_tier_2,wp_elf_tier_2,knows_common|knows_ironflesh_2|knows_power_strike_3|knows_power_draw_3|knows_athletics_2|knows_tracking_1|knows_tactics_1|knows_pathfinding_1|knows_spotting_1|knows_wound_treatment_1|knows_persuasion_1|knows_leadership_1,arnor_face_middle_1,arnor_face_middle_2],
["i3_arnor_swordsman","Dunedain_Swordsman","Dunedain_Swordsmen",tf_dunedain| tfg_armor| tfg_helm| tfg_boots,0,0,fac_imladris,[itm_arnor_helm_c,itm_arnor_armor_b,itm_leather_gloves,itm_leather_boots, itm_leather_boots_dark,itm_arnor_sword_f,itm_arnor_sword_a,itm_arnor_shield_a,],attr_elf_tier_3,wp_elf_tier_3,knows_common|knows_athletics_4|knows_shield_3|knows_power_draw_4|knows_power_strike_5|knows_ironflesh_3,arnor_face_middle_1,arnor_face_middle_2],
["i4_arnor_vet_swordsman","Dunedain_Veteran_Swordsman","Dunedain_Veteran_Swordsmen",tf_dunedain| tfg_gloves| tfg_armor| tfg_helm| tfg_boots,0,0,fac_imladris,[itm_arnor_helm_b,itm_arnor_armor_a,itm_leather_gloves,itm_leather_boots, itm_leather_boots_dark,itm_arnor_sword_a,itm_arnor_shield_a,],attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_5|knows_shield_4|knows_power_draw_5|knows_power_strike_6|knows_ironflesh_4,arnor_face_middle_1,arnor_face_middle_2],
["i5_arnor_champion","Champion_of_Arnor","Champions_of_Arnor",tf_dunedain| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_imladris,[itm_dunedain_helm_b,itm_arnor_armor_f,itm_mail_mittens,itm_arnor_greaves,itm_arnor_sword_c,itm_arnor_sword_a,itm_arnor_shield_a,],attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_5|knows_shield_4|knows_power_draw_5|knows_power_strike_7|knows_ironflesh_6,arnor_face_older_1,arnor_face_older_2],
["c4_arnor_horseman","Dunedain_Horseman","Dunedain_Horsemen",tf_dunedain| tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_imladris,[itm_arnor_helm_b,itm_arnor_armor_a,itm_mail_mittens,itm_arnor_greaves,itm_arnor_sword_a,itm_arnor_shield_c,itm_dunedain_warhorse,],attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_riding_4|knows_shield_2|knows_athletics_4|knows_power_strike_6|knows_ironflesh_4,arnor_face_older_1,arnor_face_older_2],
["c5_arnor_knight","Knight_of_Arnor","Knights_of_Arnor",tf_dunedain| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm,0,0,fac_imladris,[itm_dunedain_helm_b,itm_arnor_armor_f,itm_mail_mittens,itm_arnor_greaves,itm_leather_boots_dark,itm_lance,itm_arnor_sword_c,itm_arnor_shield_c,itm_arnor_warhorse,],attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_riding_5|knows_shield_3|knows_athletics_5|knows_power_strike_7|knows_ironflesh_5,arnor_face_older_1,arnor_face_older_2],
["a3_arnor_ranger","Dunedain_Ranger","Dunedain_Rangers",tf_dunedain| tfg_ranged| tfg_gloves| tfg_armor| tfg_boots,0,0,fac_imladris,[itm_hood_grey,itm_arnor_armor_d,itm_leather_gloves,itm_leather_boots,itm_leather_boots_dark_bad,itm_elven_bow,itm_ithilien_arrows,itm_arnor_sword_f,itm_riv_spear,itm_arnor_shield_a,],attr_elf_tier_3,wp_melee(280)|wp_archery(240),knows_common|knows_athletics_6|knows_shield_2|knows_power_draw_4|knows_power_strike_4|knows_ironflesh_4,arnor_face_middle_1,arnor_face_middle_2],
["a4_arnor_vet_ranger","Dunedain_Veteran_Ranger","Dunedain_Veteran_Rangers",tf_dunedain| tfg_ranged| tfg_gloves| tfg_armor| tfg_boots,0,0,fac_imladris,[itm_hood_grey,itm_arnor_helm_a,itm_arnor_armor_d,itm_leather_gloves,itm_leather_boots,itm_leather_boots_dark_bad,itm_elven_bow,itm_ithilien_arrows,itm_arnor_sword_f,itm_riv_spear,itm_arnor_shield_a,],attr_elf_tier_4,wp_melee(310)|wp_archery(270),knows_common|knows_athletics_6|knows_shield_3|knows_power_draw_5|knows_power_strike_4|knows_ironflesh_4,arnor_face_older_1,arnor_face_older_2],
["a5_arnor_master_ranger","Master_Ranger_of_Arnor","Master_Rangers_of_Arnor",tf_dunedain| tfg_ranged| tfg_gloves| tfg_armor| tfg_boots,0,0,fac_imladris,[itm_arnor_helm_c,itm_arnor_armor_d,itm_leather_gloves,itm_leather_boots,itm_leather_boots_dark_bad,itm_elven_bow,itm_ithilien_arrows,itm_arnor_sword_f,itm_arnor_sword_a,itm_riv_spear,itm_arnor_shield_a,],attr_elf_tier_5,wp_melee(360)|wp_archery(300),knows_common|knows_athletics_8|knows_shield_3|knows_power_draw_6|knows_power_strike_5|knows_ironflesh_5,arnor_face_older_1,arnor_face_older_2],

["imladris_items","BUG","BUG",tf_hero,0,0,fac_imladris,
   [itm_leather_boots,itm_leather_gloves,itm_short_bow,itm_regular_bow,itm_arrows,itm_good_mace,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,itm_sumpter_horse, itm_saddle_horse],
      0,0,0,0],
#ROHAN
["i1_rohan_youth","Rohan_Youth","Rohan_Youths",tf_rohan| tfg_armor| tfg_boots,0,0,fac_rohan,[itm_rohan_recruit_bad, itm_rohan_recruit, itm_rohan_recruit_good, itm_rohan_leather_bad,itm_north_leather_bad,itm_north_leather_ok,itm_rohan_tunic_a,itm_rohan_tunic_b,itm_rohan_shoes,itm_rohirrim_short_axe,itm_spear,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,itm_saddle_horse,],attr_tier_1,wp_tier_1,knows_common|knows_power_strike_1|knows_athletics_1|knows_riding_2|knows_horse_archery_1|knows_looting_1|knows_tactics_1|knows_pathfinding_1|knows_spotting_1|knows_inventory_management_1|knows_prisoner_management_1|knows_leadership_1|knows_trade_1,rohan_face_younger_1,rohan_face_middle_2],
["i2_guardsman_of_rohan","Guardsman_of_Rohan","Guardsmen_of_Rohan",tf_rohan| tfg_armor| tfg_boots,0,0,fac_rohan,[itm_rohan_light_helmet_a_bad,itm_rohan_light_helmet_b_bad,itm_rohan_recruit_good, itm_rohan_leather_bad, itm_rohan_leather, itm_rohan_leather_cloak,itm_dale_light_b_bad,itm_north_leather_ok,itm_rohan_shoes,itm_leather_boots_bad,itm_spear,itm_rohan_sword_c,itm_good_mace,itm_rohan_shield_a,itm_rohan_shield_b,itm_rohan_shield_c,],attr_tier_2,wp_tier_2,knows_common|knows_ironflesh_2|knows_power_strike_2|knows_shield_1|knows_athletics_1|knows_riding_1|knows_looting_1|knows_tactics_1|knows_pathfinding_1|knows_spotting_1|knows_inventory_management_1|knows_prisoner_management_1|knows_leadership_1|knows_trade_1,rohan_face_young_1,rohan_face_old_2],
["i3_footman_of_rohan","Footman_of_Rohan","Footmen_of_Rohan",tf_rohan| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,[itm_rohan_light_helmet_b,itm_rohan_light_helmet_a,itm_rohan_leather_good, itm_rohan_leather_cloak,itm_rohan_mail_bad,itm_north_leather_good, itm_rohan_mail,itm_rohan_mail_cloak,itm_dale_light_b_cloak, itm_rohan_light_greaves,itm_leather_boots,itm_rohirrim_short_axe,itm_spear,itm_rohan_sword_c,itm_rohan_shield_a,itm_rohan_shield_b,itm_rohan_shield_c,],attr_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_shield_2|knows_power_strike_2|knows_ironflesh_1,rohan_face_middle_1,rohan_face_old_2],
["i4_veteran_footman_of_rohan","Veteran_Footman_of_Rohan","Veteran_Footmen_of_Rohan",tf_rohan| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,[itm_rohan_inf_helmet_b_bad,itm_rohan_mail,itm_rohan_mail_cloak,itm_rohan_mail_cloak, itm_rohan_rider_bad,itm_dale_light_b_lordly,itm_dale_med_a_bad,itm_rohan_light_greaves,itm_rohirrim_short_axe,itm_rohan_spear,itm_rohan_sword_c,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,],attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_shield_2|knows_power_strike_3|knows_ironflesh_2,rohan_face_middle_1,rohan_face_old_2],
["i5_elite_footman_of_rohan","Elite_Footman_of_Rohan","Elite_Footmen_of_Rohan",tf_rohan| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,[itm_rohan_inf_helmet_b,itm_rohan_scale_bad, itm_rohan_scale_cloak, itm_rohan_scale_good,itm_rohan_rider_good_cloak, itm_rohan_rider_good,itm_dale_med_a_ok, itm_dale_med_a_cloak,itm_rohirrim_war_greaves,itm_rohirrim_long_hafted_axe,itm_rohirrim_short_axe,itm_rohan_spear,itm_rohan_sword_c,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,],attr_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_shield_2|knows_power_strike_3|knows_ironflesh_2,rohan_face_middle_1,rohan_face_old_2],
["i6_footman_guard_of_rohan","Folcwine_Guard_of_Rohan","Folcwine_Guards_of_Rohan",tf_rohan| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,[itm_rohan_inf_helmet_b_good,itm_rohan_surcoat_cloak,itm_rohan_surcoat_good_cloak,itm_leather_gloves,itm_rohirrim_war_greaves,itm_rohirrim_long_hafted_axe,itm_rohirrim_short_axe,itm_rohan_sword_c,itm_heavy_throwing_spear,itm_heavy_throwing_spear,itm_rohirrim_throwing_axe,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,],attr_tier_6,wp_tier_6,knows_common|knows_athletics_3|knows_shield_4|knows_power_throw_4|knows_power_strike_6|knows_ironflesh_4,rohan_face_middle_1,rohan_face_old_2],
["i6_frealaf_raider","Frealaf_Raider","Frealaf_Raiders",tf_rohan| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,[itm_rohan_light_helmet_b,itm_rohan_light_helmet_a,itm_rohan_rider_cloak,itm_rohan_rider_good_cloak,itm_dale_med_b_good,itm_dale_med_b_lordly,itm_rohan_light_greaves,itm_rohirrim_long_hafted_axe,itm_rohirrim_short_axe,itm_heavy_throwing_spear,itm_heavy_throwing_spear,itm_rohirrim_throwing_axe,itm_rohirrim_throwing_axe,itm_rohan_shield_a,itm_rohan_shield_b,itm_rohan_shield_c,],attr_tier_6,wp_tier_6,knows_common|knows_athletics_7|knows_shield_3|knows_power_throw_6|knows_power_strike_6|knows_ironflesh_5,rohan_face_middle_1,rohan_face_old_2],
["i5_raider_of_rohan","Raider_of_Rohan","Raiders_of_Rohan",tf_rohan| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,[itm_rohan_light_helmet_a_bad,itm_rohan_light_helmet_b_bad,itm_rohan_mail, itm_rohan_mail_cloak,itm_rohan_mail_good, itm_rohan_rider_bad,itm_dale_light_b_cloak,itm_dale_light_b_good,itm_leather_boots,itm_rohirrim_long_hafted_axe,itm_rohirrim_short_axe,itm_heavy_throwing_spear,itm_heavy_throwing_spear,itm_rohirrim_throwing_axe,itm_rohirrim_throwing_axe,itm_rohan_shield_a,itm_rohan_shield_b,itm_rohan_shield_c,],attr_tier_5,wp_tier_5,knows_common|knows_athletics_5|knows_shield_2|knows_power_throw_4|knows_power_strike_4|knows_ironflesh_3,rohan_face_middle_1,rohan_face_old_2],
["i6_warden_of_methuseld","Warden_of_Meduseld","Wardens_of_Meduseld",tf_rohan| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,[itm_rohan_archer_helmet_c_good,itm_rohan_archer_helmet_c_bad, itm_rohan_guard_cloak, itm_rohan_guard_good,itm_mail_mittens,itm_rohirrim_war_greaves,itm_rohan_spear,itm_rohan_lance_banner_sun,itm_rohan_lance_banner_horse,itm_rohan_shield_g,],attr_tier_6,wp_tier_6,knows_common|knows_athletics_3|knows_shield_5|knows_power_strike_5|knows_ironflesh_6,rohan_face_old_1,rohan_face_older_2],
["ac3_skirmisher_of_rohan","Skirmisher_of_Rohan","Skirmishers_of_Rohan",tf_rohan| tfg_ranged| tf_mounted| tfg_armor| tfg_horse| tfg_boots,0,0,fac_rohan,[itm_rohan_light_helmet_a,itm_rohan_light_helmet_b,itm_rohan_light_helmet_b_good,itm_rohan_recruit_good, itm_rohan_leather_bad, itm_rohan_leather,itm_dale_light_b_bad,itm_north_leather_good,itm_rohan_shoes,itm_leather_boots_bad,itm_nomad_bow,itm_khergit_arrows,itm_rohan_sword_c,itm_spear,itm_rohirrim_courser,],attr_tier_3,wp_tier_bow_3,knows_common|knows_horse_archery_3|knows_shield_1| knows_riding_3|knows_power_draw_1,rohan_face_young_1,rohan_face_middle_2],
["ac4_veteran_skirmisher_of_rohan","Veteran_Skirmisher_of_Rohan","Veteran_Skirmishers_of_Rohan",tf_rohan| tfg_ranged| tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,[itm_rohan_light_helmet_a,itm_rohan_light_helmet_b_good,itm_rohan_archer_helmet_a_bad,itm_rohan_leather_good,itm_rohan_mail_bad, itm_rohan_mail,itm_dale_light_b,itm_leather_boots,itm_nomad_bow,itm_khergit_arrows,itm_rohirrim_long_hafted_axe,itm_rohan_sword_c,itm_rohirrim_courser,itm_rohirrim_hunter,],attr_tier_4,wp_tier_bow_4,knows_common|knows_horse_archery_5|knows_riding_4|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_1,rohan_face_middle_1,rohan_face_old_2],
["ac5_elite_skirmisher_of_rohan","Elite_Skirmisher_of_Rohan","Elite_Skirmishers_of_Rohan",tf_rohan| tfg_ranged| tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,[itm_rohan_archer_helmet_a,itm_rohan_light_helmet_a,itm_rohan_mail_good, itm_rohan_rider,itm_rohan_rider_bad,itm_dale_light_b_good,itm_leather_gloves,itm_rohan_light_greaves,itm_leather_boots,itm_strong_bow,itm_khergit_arrows,itm_rohan_spear,itm_rohan_sword_c,itm_rohirrim_long_hafted_axe,itm_rohirrim_courser2,],attr_tier_5,wp_tier_bow_5,knows_common|knows_horse_archery_6|knows_riding_6|knows_power_draw_4|knows_power_strike_2|knows_ironflesh_2,rohan_face_middle_1,rohan_face_old_2],
["ac6_skirmisher_guard_of_rohan","Thengel_Guard_of_Rohan","Thengel_Guards_of_Rohan",tf_rohan| tfg_ranged| tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,[itm_rohan_archer_helmet_a_good,itm_rohan_light_helmet_a_good,itm_rohan_surcoat_bad,itm_rohan_surcoat,itm_leather_gloves,itm_rohan_light_greaves,itm_strong_bow,itm_khergit_arrows,itm_rohan_spear,itm_rohirrim_long_hafted_axe,itm_rohan_warhorse,],attr_tier_6,wp_tier_bow_6,knows_common|knows_horse_archery_8|knows_riding_7|knows_power_draw_5|knows_power_strike_3|knows_ironflesh_3,rohan_face_middle_1,rohan_face_old_2],
["c4_lancer_of_rohan","Lancer_of_Rohan","Lancers_of_Rohan",tf_rohan| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm,0,0,fac_rohan,[itm_rohan_archer_helmet_a, itm_rohan_archer_helmet_b,itm_rohan_inf_helmet_a_bad, itm_rohan_inf_helmet_b_bad,itm_rohan_mail_bad, itm_rohan_mail,itm_rohan_mail_cloak,itm_rohan_rider_bad,itm_rohan_rider_cloak,itm_dale_light_b_cloak,itm_dale_med_a_cloak,itm_mail_mittens,itm_rohirrim_war_greaves,itm_rohan_lance,itm_rohan_cav_sword,itm_rohan_shield_a,itm_rohan_shield_b,itm_rohan_shield_c,itm_rohirrim_courser2,],attr_tier_4,wp_tier_4,knows_common|knows_riding_4|knows_shield_1|knows_power_strike_4|knows_ironflesh_2,rohan_face_middle_1,rohan_face_old_2],
["c5_elite_lancer_of_rohan","Elite_Lancer_of_Rohan","Elite_Lancers_of_Rohan",tf_rohan| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm,0,0,fac_rohan,[itm_rohan_archer_helmet_b_good, itm_rohan_inf_helmet_a, itm_rohan_inf_helmet_b,itm_rohan_mail_good_cloak, itm_rohan_rider_bad, itm_rohan_rider,itm_rohan_rider_good,itm_rohan_rider_cloak, itm_rohan_rider_good_cloak,itm_dale_med_a_cloak,itm_dale_med_a_good,itm_mail_mittens,itm_rohirrim_war_greaves,itm_rohan_lance,itm_rohan_lance,itm_rohan_lance_banner_horse,itm_rohan_cav_sword,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,itm_rohan_warhorse],attr_tier_5,wp_tier_5,knows_common|knows_riding_5|knows_shield_2|knows_power_strike_5|knows_ironflesh_3,rohan_face_middle_1,rohan_face_old_2],
["c6_lancer_guard_of_rohan","Brego_Guard_of_Rohan","Brego_Guards_of_Rohan",tf_rohan| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm,0,0,fac_rohan,[itm_rohan_inf_helmet_b_good,itm_rohan_surcoat,itm_rohan_surcoat_cloak,itm_rohan_surcoat_good,itm_rohan_surcoat_good_cloak,itm_mail_mittens,itm_rohirrim_war_greaves,itm_rohan_lance_banner_sun,itm_rohan_lance_banner_horse,itm_rohan_cav_sword,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,itm_thengel_warhorse,],attr_tier_6,wp_tier_6,knows_common|knows_riding_7|knows_shield_3|knows_power_strike_6|knows_ironflesh_6,rohan_face_middle_1,rohan_face_old_2],
["c6_king_s_man_of_rohan","King's_Guard","King's_Guards",tf_rohan| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,[itm_rohan_inf_helmet_b_lordly,itm_rohan_archer_helmet_c_lordly,itm_rohan_guard_good,itm_mail_mittens,itm_rohirrim_war_greaves,itm_rohan_lance_banner_sun,itm_rohan_lance_banner_horse,itm_rohirrim_long_hafted_axe,itm_rohan_sword_c,itm_rohan_shield_g,itm_thengel_warhorse_heavy,],attr_tier_6,wp_tier_6,knows_common|knows_riding_7|knows_shield_3|knows_power_strike_7|knows_ironflesh_6,rohan_face_old_1,rohan_face_older_2],
["c2_squire_of_rohan","Squire_of_Rohan","Squires_of_Rohan",tf_rohan| tf_mounted| tfg_armor| tfg_horse| tfg_boots,0,0,fac_rohan,[itm_rohan_light_helmet_a_bad,itm_rohan_light_helmet_b_bad,itm_rohan_recruit_good, itm_rohan_leather_bad, itm_rohan_leather,itm_north_leather_ok,itm_north_leather_good, itm_rohan_leather_cloak,itm_rohan_leather_cloak,itm_dale_light_b_cloak,itm_leather_gloves,itm_rohan_shoes,itm_leather_boots,itm_spear,itm_rohan_sword_c,itm_short_bow,itm_arrows,itm_rohan_shield_a,itm_rohan_shield_b,itm_rohan_shield_c,itm_saddle_horse,itm_rohirrim_courser,],attr_tier_2,wp_tier_2,knows_common|knows_power_strike_1|knows_athletics_1|knows_riding_3|knows_horse_archery_2|knows_looting_1|knows_tactics_1|knows_pathfinding_1|knows_spotting_1|knows_inventory_management_1|knows_prisoner_management_1|knows_leadership_1|knows_trade_1,rohan_face_young_1,rohan_face_old_2],
["c3_rider_of_rohan","Rider_of_Rohan","Riders_of_Rohan",tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_horse| tfg_boots,0,0,fac_rohan,[itm_rohan_light_helmet_a, itm_rohan_light_helmet_b_good, itm_rohan_archer_helmet_a_bad, itm_rohan_archer_helmet_b_bad,itm_rohan_leather_good,itm_rohan_leather_good_cloak,itm_rohan_mail_bad, itm_rohan_mail,itm_rohan_mail_cloak,itm_rohan_rider_bad,itm_dale_light_b_lordly,itm_leather_gloves,itm_rohan_light_greaves,itm_rohan_spear,itm_rohan_spear,itm_rohan_spear,itm_heavy_throwing_spear,itm_rohan_sword_c,itm_rohirrim_long_hafted_axe,itm_rohan_shield_a,itm_rohan_shield_b,itm_rohan_shield_c,itm_rohirrim_courser,itm_rohirrim_hunter,],attr_tier_3,wp_tier_3,knows_common|knows_horse_archery_1|knows_riding_3|knows_shield_1|knows_power_throw_2|knows_power_strike_2,rohan_face_young_1,rohan_face_old_2],
["c4_veteran_rider_of_rohan","Veteran_Rider_of_Rohan","Veteran_Riders_of_Rohan",tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,[itm_rohan_archer_helmet_a, itm_rohan_archer_helmet_b,itm_rohan_inf_helmet_a_bad, itm_rohan_inf_helmet_b_bad,itm_rohan_mail_good,itm_rohan_mail_good_cloak, itm_rohan_rider_bad, itm_rohan_rider,itm_rohan_rider_cloak,itm_rohan_scale_bad,itm_dale_med_a_cloak,itm_mail_mittens,itm_rohan_light_greaves,itm_rohan_spear,itm_heavy_throwing_spear,itm_heavy_throwing_spear,itm_rohan_cav_sword,itm_rohan_sword_c,itm_rohirrim_long_hafted_axe,itm_rohirrim_long_hafted_axe,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,itm_rohirrim_courser2,itm_rohirrim_hunter,],attr_tier_4,wp_tier_4,knows_common|knows_horse_archery_1|knows_riding_5|knows_shield_2|knows_power_throw_3|knows_power_strike_3|knows_ironflesh_2,rohan_face_middle_1,rohan_face_old_2],
["c5_elite_rider_of_rohan","Elite_Rider_of_Rohan","Elite_Riders_of_Rohan",tf_rohan| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,[itm_rohan_archer_helmet_b_good, itm_rohan_inf_helmet_a, itm_rohan_inf_helmet_b,itm_rohan_rider_good, itm_rohan_rider_good_cloak, itm_rohan_scale,itm_rohan_scale_cloak, itm_rohan_scale_good,itm_rohan_scale_good_cloak,itm_dale_med_a_good,itm_mail_mittens,itm_rohirrim_war_greaves,itm_rohan_spear,itm_heavy_throwing_spear,itm_heavy_throwing_spear,itm_rohan_cav_sword,itm_rohan_sword_c,itm_rohirrim_long_hafted_axe,itm_rohirrim_long_hafted_axe,itm_rohan_sword_c,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,itm_rohan_warhorse],attr_tier_5,wp_tier_5,knows_common|knows_horse_archery_2|knows_riding_6|knows_shield_3|knows_power_throw_4|knows_power_strike_4|knows_ironflesh_3,rohan_face_middle_1,rohan_face_old_2],
["c6_rider_guard_of_rohan","Eorl_Guard_of_Rohan","Eorl_Guards_of_Rohan",tf_rohan| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,[itm_rohan_inf_helmet_b_lordly,itm_rohan_guard_bad, itm_rohan_guard,itm_rohan_guard_cloak, itm_rohan_guard_good,itm_mail_mittens,itm_rohirrim_war_greaves,itm_rohan_spear,itm_heavy_throwing_spear,itm_heavy_throwing_spear,itm_rohan_inf_sword,itm_rohan_inf_sword,itm_rohan_cav_sword,itm_rohirrim_long_hafted_axe,itm_rohirrim_long_hafted_axe,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,itm_rohan_shield_g,itm_thengel_warhorse,],attr_tier_6,wp_tier_6,knows_common|knows_horse_archery_3|knows_riding_8|knows_shield_3|knows_power_throw_5|knows_power_strike_6|knows_ironflesh_6,rohan_face_middle_1,rohan_face_old_2],
["i6_2h_guard_of_rohan","Helm_Guard_of_Rohan","Helm_Guards_of_Rohan",tf_rohan| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,[itm_rohan_inf_helmet_b_lordly,itm_rohan_guard_bad,itm_rohan_guard_cloak,itm_mail_mittens,itm_rohirrim_war_greaves,itm_rohan_2h_sword, itm_rohirrim_long_hafted_axe,],attr_tier_6,wp_tier_6,knows_common|knows_athletics_6|knows_power_strike_7|knows_ironflesh_8,rohan_face_middle_1,rohan_face_old_2],

##Rohan Siege battle dismounted troops
["dismounted_veteran_skirmisher_of_rohan","Veteran_Skirmisher_of_Rohan","Veteran_Skirmishers_of_Rohan",tf_rohan| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,[itm_rohan_light_helmet_a,itm_rohan_light_helmet_b_good,itm_rohan_archer_helmet_a_bad,itm_rohan_mail_bad, itm_rohan_mail,itm_rohan_mail_good,itm_rohan_light_greaves,itm_nomad_bow,itm_khergit_arrows,itm_rohirrim_long_hafted_axe,itm_rohan_sword_c,itm_rohirrim_long_hafted_axe,],attr_tier_4,wp_tier_4,knows_horse_archery_5|knows_riding_6|knows_power_draw_4|knows_power_strike_2|knows_ironflesh_2|knows_power_throw_4,rohan_face_young_1,rohan_face_old_2],
["dismounted_elite_skirmisher_of_rohan","Elite_Skirmisher_of_Rohan","Elite_Skirmishers_of_Rohan",tf_rohan| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,[itm_rohan_archer_helmet_a,itm_rohan_light_helmet_a, itm_rohan_rider_bad, itm_rohan_rider,itm_rohan_rider_good,itm_rohan_light_greaves,itm_strong_bow,itm_khergit_arrows,itm_rohan_sword_c,],attr_tier_5,wp_tier_5,knows_horse_archery_7|knows_riding_7|knows_power_draw_5|knows_power_strike_3|knows_ironflesh_3|knows_power_throw_5,rohan_face_middle_1,rohan_face_old_2],
["dismounted_thengel_guard_of_rohan","Thengel_Guard_of_Rohan","Thengel_Guards_of_Rohan",tf_rohan| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,[itm_rohan_archer_helmet_a_good,itm_rohan_light_helmet_a_good,itm_rohan_surcoat_bad,itm_rohan_surcoat,itm_rohan_surcoat_good,itm_rohirrim_war_greaves,itm_strong_bow,itm_khergit_arrows,itm_rohan_sword_c,],attr_tier_6,wp_tier_6,knows_horse_archery_5|knows_riding_7|knows_power_draw_5|knows_power_throw_5|knows_power_strike_3|knows_ironflesh_3,rohan_face_middle_1,rohan_face_old_2],

#HARAD
["i1_harad_levy","Harad_Levy","Harad_Levies",tf_harad| tfg_armor,0,0,fac_harad,[itm_harad_tunic,itm_desert_boots,itm_harad_javelin,itm_harad_short_spear,],attr_evil_tier_1,wp_tier_1,knows_common|knows_power_strike_1|knows_athletics_2|knows_riding_1|knows_horse_archery_1|knows_looting_1|knows_tactics_1|knows_spotting_1|knows_wound_treatment_1|knows_first_aid_1|knows_leadership_2|knows_trade_1,haradrim_face_1,haradrim_face_2],
["i3_harad_infantry","Harad_Light_Footman","Harad_Light_Footmen",tf_harad| tfg_armor| tfg_boots,0,0,fac_harad,[itm_harad_hauberk,itm_desert_boots,itm_harad_short_spear,itm_harad_dagger,itm_skirmisher_sword,itm_harad_sabre_bad,itm_harad_long_shield_d,itm_harad_long_shield_e,],attr_evil_tier_3,wp_tier_3,knows_common|knows_ironflesh_1|knows_power_strike_1|knows_shield_2|knows_athletics_2|knows_riding_1|knows_horse_archery_1|knows_looting_1|knows_tactics_1|knows_spotting_1|knows_wound_treatment_1|knows_first_aid_1|knows_leadership_2|knows_trade_1,haradrim_face_1,haradrim_face_2],
["i4_harad_spearman","Harad_Spearman","Harad_Spearmen",tf_harad| tfg_shield| tfg_armor| tfg_helm| tfg_boots  |tfg_polearm,0,0,fac_harad,[itm_harad_finhelm,itm_harad_scale,itm_harad_scale_greaves,itm_harad_long_spear,itm_harad_long_shield_d,itm_harad_long_shield_e,],attr_evil_tier_4,wp_tier_4,knows_common|knows_athletics_3|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,haradrim_face_1,haradrim_face_2],
["i5_harad_tiger_guard","Tiger_Guard","Tiger_Guards",tf_harad| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tfg_gloves  |tfg_polearm,0,0,fac_harad,[itm_lion_helm,itm_harad_tiger_scale,itm_leather_gloves,itm_harad_scale_greaves,itm_harad_long_spear,itm_harad_long_shield_b,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_shield_4|knows_power_strike_4|knows_ironflesh_6,haradrim_face_1,haradrim_face_2],
["i4_harad_swordsman","Harad_Swordsman","Harad_Swordsmen",tf_harad| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,[itm_harad_finhelm,itm_harad_scale,itm_harad_scale_greaves,itm_harad_sabre,itm_skirmisher_sword,itm_black_snake_sword_bad,itm_harad_long_shield_d,itm_harad_long_shield_e,],attr_evil_tier_4,wp_tier_4,knows_common|knows_athletics_3|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,haradrim_face_1,haradrim_face_2],
["i5_harad_lion_guard","Lion_Guard","Lion_Guards",tf_harad| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,[itm_lion_helm,itm_harad_lion_scale,itm_leather_gloves,itm_harad_scale_greaves,itm_harad_khopesh,itm_black_snake_sword,itm_harad_long_shield_b,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_6|knows_power_strike_5|knows_ironflesh_4|knows_shield_3,haradrim_face_1,haradrim_face_2],
["a3_harad_hunter","Harad_Hunter","Harad_Hunters",tf_harad| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,[itm_harad_heavy_inf_helm,itm_harad_skirmisher,itm_desert_boots,itm_harad_bow,itm_harad_arrows,itm_harad_short_spear,itm_harad_dagger,],attr_evil_tier_3,wp_tier_bow_3,knows_common|knows_ironflesh_1|knows_power_throw_2|knows_power_draw_2|knows_athletics_3|knows_riding_1|knows_horse_archery_1|knows_looting_1|knows_tactics_1|knows_spotting_1|knows_wound_treatment_1|knows_first_aid_1|knows_leadership_2|knows_trade_1,haradrim_face_1,haradrim_face_2],
["a4_harad_archer","Harad_Archer","Harad_Archers",tf_harad| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,[itm_harad_heavy_inf_helm,itm_harad_archer,itm_harad_leather_greaves,itm_harad_bow,itm_harad_arrows,itm_harad_short_spear,itm_harad_dagger,],attr_evil_tier_4,wp_tier_bow_4,knows_common|knows_athletics_3|knows_power_draw_3|knows_ironflesh_1,haradrim_face_1,haradrim_face_2],
["a5_harad_eagle_guard","Eagle_Guard","Eagle_Guards",tf_harad| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,[itm_harad_eaglehelm,itm_harad_archer,itm_leather_gloves,itm_harad_leather_greaves,itm_lg_bow,itm_harad_arrows,itm_eagle_guard_spear,],attr_evil_tier_5,wp_tier_bow_5,knows_common|knows_athletics_4|knows_power_draw_4|knows_ironflesh_2,haradrim_face_1,haradrim_face_2],
#HARONDOR
["c2_harondor_scout","Harondor_Scout","Harondor_Scouts",tf_harad| tf_mounted| tfg_armor| tfg_horse| tfg_boots,0,0,fac_harad,[itm_harad_cav_helm_a,itm_harad_padded,itm_desert_boots,itm_horandor_a,itm_harad_shield_a,itm_saddle_horse],attr_evil_tier_2,wp_tier_2,knows_common|knows_athletics_2|knows_shield_1|knows_power_strike_1,haradrim_face_1,haradrim_face_2],
["c3_harondor_rider","Harondor_Rider","Harondor_Riders",tf_harad| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,[itm_harad_cav_helm_b,itm_harad_hauberk,itm_harad_leather_greaves,itm_horandor_a,itm_harad_shield_b,itm_harad_shield_c,itm_harad_horse],attr_evil_tier_3,wp_tier_3,knows_common|knows_riding_2|knows_shield_2|knows_power_strike_2,haradrim_face_1,haradrim_face_2],
["c4_harondor_light_cavalry","Harondor_Light_Rider","Harondor_Light_Riders",tf_harad| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,[itm_harad_wavy_helm,itm_harad_lamellar,itm_harad_lamellar_greaves,itm_horandor_a,itm_harad_heavy_sword_bad,itm_harad_shield_b,itm_harad_shield_c,itm_harad_warhorse,],attr_evil_tier_4,wp_tier_4,knows_common|knows_riding_3|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,haradrim_face_1,haradrim_face_2],
["c5_harondor_serpent_knight","Gold_Serpent_Knight","Gold_Serpent_Knights",tf_harad| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots|tfg_polearm,0,0,fac_harad,[itm_harad_dragon_helm,itm_harad_heavy,itm_leather_gloves,itm_harad_lamellar_greaves,itm_harad_long_spear,itm_harad_heavy_sword_good,itm_harad_yellow_shield,itm_harad_warhorse],attr_evil_tier_5,wp_tier_5,knows_common|knows_riding_5|knows_shield_3|knows_power_strike_3|knows_ironflesh_3,haradrim_face_1,haradrim_face_2],
["ac3_harondor_skirmisher","Harondor_Skirmisher","Harondor_Skirmishers",tf_harad| tfg_ranged| tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,[itm_harad_cav_helm_b,itm_harad_skirmisher,itm_desert_boots,itm_harad_bow,itm_harad_arrows,itm_horandor_a,itm_saddle_horse,],attr_evil_tier_3,wp_tier_bow_3,knows_common|knows_horse_archery_3|knows_riding_3|knows_shield_1|knows_power_draw_2|knows_power_strike_2|knows_ironflesh_1,haradrim_face_1,haradrim_face_2],
["ac4_harondor_horse_archer","Harondor_Horse_Archer","Harondor_Horse_Archers",tf_harad| tfg_ranged| tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,[itm_harad_heavy_inf_helm,itm_harad_archer,itm_harad_leather_greaves,itm_nomad_bow,itm_harad_arrows,itm_horandor_a,itm_black_snake_sword,itm_harad_horse,],attr_evil_tier_4,wp_tier_bow_4,knows_common|knows_horse_archery_4|knows_riding_4|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_1,haradrim_face_1,haradrim_face_2],
["ac5_harondor_black_snake","Black_Snake_Horse_Archer","Black_Snake_Horse_Archers",tf_harad| tfg_ranged| tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,[itm_black_snake_helm,itm_black_snake_armor,itm_harad_leather_greaves,itm_nomad_bow,itm_harad_arrows,itm_black_snake_sword_good,itm_harad_heavy_sword,itm_harad_warhorse,],attr_evil_tier_5,wp_tier_bow_5,knows_common|knows_horse_archery_7|knows_riding_5|knows_power_strike_2|knows_ironflesh_3|knows_power_draw_3,haradrim_face_1,haradrim_face_2],
#FAR HARAD
["i2_far_harad_tribesman","Far_Harad_Tribesman","Far_Harad_Tribesmen",tf_harad| tfg_armor| tfg_boots,0,0,fac_harad,[itm_far_harad_2h_mace,itm_harad_short_spear,itm_harad_javelin,],attr_evil_tier_2,wp_tier_2,knows_common|knows_ironflesh_1|knows_power_strike_1|knows_power_throw_1|knows_athletics_4|knows_looting_2|knows_tracking_1|knows_pathfinding_1|knows_wound_treatment_2|knows_surgery_1,far_harad_face1,far_harad_face2],
["i4_far_harad_champion","Far_Harad_Champion","Far_Harad_Champions",tf_harad| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,[itm_harad_champion,itm_far_harad_2h_mace,itm_harad_short_spear,itm_harad_javelin,],attr_evil_tier_4,wp_tier_4,knows_common|knows_ironflesh_1|knows_power_strike_2|knows_power_throw_3|knows_athletics_5|knows_looting_2|knows_tracking_1|knows_pathfinding_1|knows_wound_treatment_2|knows_surgery_1,far_harad_face1,far_harad_face2],
["i5_far_harad_panther_guard","Panther_Guard","Panther_Guards",tf_harad| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,[itm_harad_pantherhelm,itm_panther_guard,itm_harad_mace,itm_harad_javelin,itm_harad_long_shield_a,],attr_evil_tier_5,wp_tier_5,knows_common|knows_power_throw_4|knows_power_strike_4|knows_ironflesh_3|knows_athletics_8,far_harad_face1,far_harad_face2],

["harad_items","BUG","_",tf_hero,0,0,fac_harad,
   [itm_short_bow,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,itm_sumpter_horse, itm_saddle_horse],
      0,0,0,0],
	  
#DUNLAND #Dunnish #Dunlendings
["i1_dun_wildman","Dunnish_Wildman","Dunnish_Wildmen",tf_dunland| tf_randomize_face| tfg_armor| tfg_boots,0,0,fac_dunland,[itm_gundabad_helm_a,itm_dunland_armor_b,itm_dunland_armor_c,itm_dunland_armor_d,itm_dunland_armor_e,itm_dunland_armor_g,itm_dunland_wolfboots,itm_dunnish_axe,itm_dunland_spear,itm_wood_club,itm_dun_shield_a,itm_dun_shield_b,itm_dunland_javelin,],attr_evil_tier_1,wp_tier_1,knows_common|knows_ironflesh_2|knows_power_strike_1|knows_power_throw_1|knows_shield_1|knows_athletics_3|knows_looting_1|knows_tracking_1|knows_pathfinding_2|knows_spotting_1|knows_wound_treatment_1|knows_persuasion_1 ,dunland_face1,dunland_face2],
["i2_dun_warrior","Dunnish_Warrior","Dunnish_Warriors",tf_dunland| tf_randomize_face| tfg_armor| tfg_boots,0,0,fac_dunland,[itm_gundabad_helm_a, itm_gundabad_helm_b,itm_dunland_armor_b,itm_dunland_armor_c,itm_dunland_armor_d,itm_dunland_armor_e,itm_dunland_armor_g,itm_dunland_wolfboots,itm_dunnish_antler_axe,itm_dunnish_axe,itm_wood_club,itm_dunland_spear,itm_dun_shield_a,itm_dun_shield_b,itm_dunland_javelin,itm_dunland_javelin,],attr_evil_tier_2,wp_tier_2,knows_common|knows_ironflesh_2|knows_power_strike_1|knows_power_throw_2|knows_shield_2|knows_athletics_4|knows_looting_1|knows_tracking_1|knows_pathfinding_2|knows_spotting_1|knows_wound_treatment_1|knows_persuasion_1,dunland_face1,dunland_face2],
["i3_dun_pikeman","Dunnish_Pikeman","Dunnish_Pikemen",tf_dunland| tf_randomize_face| tfg_armor| tfg_boots,0,0,fac_dunland,[itm_gundabad_helm_b, itm_dun_helm_b,itm_dunland_armor_b,itm_dunland_armor_c,itm_dunland_armor_d,itm_dunland_armor_e,itm_dunland_armor_g,itm_evil_gauntlets_a,itm_dunland_wolfboots,itm_dunnish_pike,itm_dun_shield_a,itm_dun_shield_b,],attr_evil_tier_3,wp_tier_3,knows_common|knows_athletics_5|knows_shield_2|knows_power_strike_2|knows_ironflesh_4,dunland_face1,dunland_face2],
["i4_dun_vet_pikeman","Dunnish_Veteran_Pikeman","Dunnish_Veteran_Pikemen",tf_dunland| tf_randomize_face| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dunland,[itm_dun_helm_b, itm_dun_helm_e,itm_dunland_armor_i,itm_dunland_armor_j,itm_evil_gauntlets_b,itm_dunland_wolfboots,itm_dunnish_pike,itm_dun_shield_a,],attr_evil_tier_4,wp_tier_4,knows_common|knows_athletics_6|knows_shield_3|knows_power_strike_3|knows_ironflesh_6,dunland_face1,dunland_face2],
["ac4_dun_crebain_rider","Dunnish_Crebain_Rider","Dunnish_Crebain_Riders",tf_dunland| tf_randomize_face| tf_mounted| tfg_armor| tfg_horse| tfg_boots| tfg_ranged,0,0,fac_dunland,[itm_dun_helm_c,itm_dunland_armor_b,itm_dunland_armor_c,itm_dunland_armor_d,itm_dunland_armor_e,itm_dunland_armor_g,itm_dunland_wolfboots,itm_dunnish_antler_axe,itm_dunland_javelin,itm_dunland_javelin,itm_dunland_javelin,itm_dunland_javelin,itm_dun_shield_a,itm_dun_shield_b,itm_saddle_horse],attr_evil_tier_4,wp_tier_3,knows_common|knows_ironflesh_1|knows_power_throw_3|knows_athletics_2|knows_riding_4|knows_horse_archery_3,dunland_face1,dunland_face2],
["i3_dun_vet_warrior","Dunnish_Veteran_Warrior","Dunnish_Veteran_Warriors",tf_dunland| tf_randomize_face| tfg_shield| tfg_armor| tfg_boots,0,0,fac_dunland,[itm_gundabad_helm_a, itm_gundabad_helm_b,itm_dunland_armor_b,itm_dunland_armor_c,itm_dunland_armor_d,itm_dunland_armor_e,itm_dunland_armor_g,itm_evil_gauntlets_a,itm_dunland_wolfboots,itm_dunnish_axe,itm_dunnish_war_axe,itm_dunland_javelin,itm_dunland_javelin,itm_dunland_javelin,itm_dun_shield_a,],attr_evil_tier_3,wp_tier_3,knows_common|knows_athletics_4|knows_shield_2|knows_power_strike_2|knows_ironflesh_1|knows_power_throw_3,dunland_face1,dunland_face2],
["i4_dun_wolf_warrior","Dunnish_Wolf_Warrior","Dunnish_Wolf_Warriors",tf_dunland| tf_randomize_face| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dunland,[itm_dun_helm_a,itm_dunland_armor_i,itm_dunland_armor_j,itm_evil_gauntlets_a,itm_dunland_wolfboots,itm_dunnish_axe,itm_dunnish_war_axe,itm_dunland_javelin,itm_dunland_javelin,itm_dunland_javelin,itm_dun_shield_a,],attr_evil_tier_4,wp_tier_4,knows_common|knows_athletics_5|knows_shield_3|knows_power_strike_3|knows_ironflesh_4|knows_power_throw_4,dunland_face1,dunland_face2],
["i5_dun_wolf_guard","Dunnish_Wolf_Guard","Dunnish_Wolf_Guards",tf_dunland| tf_randomize_face| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dunland,[itm_dun_helm_a,itm_dunland_armor_i,itm_dunland_armor_j,itm_evil_gauntlets_b,itm_dunland_wolfboots,itm_dunnish_war_axe,itm_dun_berserker,itm_dun_shield_a,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_6|knows_shield_5|knows_power_strike_4|knows_ironflesh_6,dunland_face1,dunland_face2],
["ac5_dun_raven_rider","Dunnish_Night_Raven","Dunnish_Night_Ravens",tf_dunland| tf_randomize_face| tf_mounted| tfg_shield| tfg_armor| tfg_horse| tfg_helm| tfg_boots| tfg_ranged,0,0,fac_dunland,[itm_dun_helm_c, itm_dun_helm_d,itm_dunland_armor_i,itm_dunland_armor_j,itm_evil_gauntlets_a,itm_dunland_wolfboots,itm_dunnish_antler_axe,itm_twohand_wood_club,itm_dunland_javelin,itm_dunland_javelin,itm_dunland_javelin,itm_dunland_javelin,itm_dun_shield_a,itm_dun_shield_b,itm_hunter],attr_evil_tier_5,wp_tier_5,knows_common|knows_ironflesh_3|knows_riding_5|knows_shield_2|knows_power_strike_3|knows_power_throw_6|knows_horse_archery_6,dunland_face1,dunland_face2],

["dunland_items","BUG","_",tf_hero,0,0,fac_dunland,
   [itm_sumpter_horse,itm_saddle_horse,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],

#KHAND
["i1_khand_bondsman","Khand_Bondsman","Khand_Bondsmen",tf_evil_man| tfg_armor,0,0,fac_khand,[itm_khand_light_bad,itm_spear,itm_khand_mace1,itm_shortened_spear,itm_khand_pitsword,],attr_evil_tier_1,wp_tier_1,knows_common|knows_power_strike_2|knows_weapon_master_1|knows_athletics_2|knows_trainer_1|knows_tactics_1|knows_spotting_1|knows_inventory_management_1|knows_surgery_1|knows_first_aid_1|knows_prisoner_management_2,khand_man1,khand_man2],
["i2_khand_pit_dog","Khand_Pit_Dog","Khand_Pit_Dogs",tf_evil_man| tfg_armor,0,0,fac_khand,[itm_khand_helm_mask,itm_khand_inf_helm_a_bad,itm_khand_light_bad,itm_leather_boots_dark_bad,itm_khand_voulge,itm_spear,itm_khand_tulwar,itm_khand_pitsword,],attr_evil_tier_2,wp_tier_2,knows_common|knows_power_strike_2|knows_weapon_master_2|knows_shield_1|knows_athletics_2|knows_trainer_1|knows_tactics_1|knows_spotting_1|knows_inventory_management_1|knows_surgery_1|knows_first_aid_1|knows_prisoner_management_2,khand_man1,khand_man2],
["i3_khand_warrior","Khand_Warrior","Khand_Warriors",tf_evil_man| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,[itm_khand_inf_helm_a,itm_khand_inf_helm_b,itm_khand_light_lam,itm_khand_foot_lam_bad,itm_leather_gloves,itm_leather_boots_dark_bad,itm_khand_axe_winged,itm_khand_tulwar,itm_khand_voulge,],attr_evil_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_power_strike_3|knows_ironflesh_2,khand_man1,khand_man2],
["i4_khand_vet_warrior","Khand_Veteran_Warrior","Khand_Veteran_Warriors",tf_evil_man| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,[itm_khand_inf_helm_b_good, itm_khand_inf_helm_c1, itm_khand_inf_helm_c2,itm_khand_foot_lam,itm_mail_mittens,itm_splinted_greaves,itm_khand_axe_winged,itm_khand_tulwar, itm_khand_2h_tulwar,itm_khand_throwing_axe,],attr_evil_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_power_throw_4|knows_power_strike_4|knows_ironflesh_3,khand_man1,khand_man2],
["i5_khand_war_master","Variag_War_Master","Variag_War_Masters",tf_evil_man| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,[itm_khand_inf_helm_c1_good, itm_khand_inf_helm_c2_good,itm_khand_foot_lam_good,itm_mail_mittens,itm_splinted_greaves,itm_khand_axe_great,itm_khand_2h_tulwar,itm_khand_throwing_axe,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_2|knows_power_throw_5|knows_power_strike_5|knows_ironflesh_4,khand_man1,khand_man2],
["c2_khand_pony_rider","Khand_Pony_Rider","Khand_Pony_Riders",tf_evil_man| tf_mounted| tfg_armor| tfg_horse| tfg_boots,0,0,fac_khand,[itm_khand_inf_helm_a_bad, itm_khand_inf_helm_b_bad, itm_khand_cav_helm_a_bad,itm_khand_light,itm_khand_light_lam,itm_leather_boots_dark_bad,itm_khand_tulwar,itm_khand_mace1,itm_steppe_horse,],attr_evil_tier_2,wp_tier_2,knows_common|knows_power_strike_1|knows_power_throw_1|knows_weapon_master_1|knows_shield_1|knows_riding_2|knows_horse_archery_1|knows_trainer_1|knows_tactics_1|knows_spotting_1|knows_inventory_management_1|knows_surgery_1|knows_first_aid_1|knows_prisoner_management_2,khand_man1,khand_man2],
["c3_khand_horseman","Khand_Horseman","Khand_Horsemen",tf_evil_man| tf_mounted|tfg_shield| tfg_armor| tfg_horse| tfg_boots,0,0,fac_khand,[itm_khand_inf_helm_a,itm_khand_inf_helm_a_good, itm_khand_cav_helm_a, itm_khand_med_lam_bad,itm_leather_gloves,itm_leather_boots_dark,itm_khand_tulwar,itm_khand_mace1,itm_easterling_round_horseman,itm_steppe_horse,],attr_evil_tier_3,wp_tier_3,knows_common|knows_riding_3|knows_shield_1|knows_power_strike_2,khand_man1,khand_man2],
["c4_khand_heavy_horseman","Khand_Heavy_Horseman","Khand_Heavy_Horsemen",tf_evil_man| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_khand,[itm_khand_inf_helm_a_good, itm_khand_cav_helm_a, itm_khand_med_lam, itm_mail_mittens,itm_splinted_greaves,itm_khand_tulwar,itm_khand_mace1,itm_khand_mace2,itm_easterling_round_horseman,itm_variag_kataphrakt,],attr_evil_tier_4,wp_tier_4,knows_common|knows_riding_5|knows_shield_3|knows_power_strike_2|knows_ironflesh_2,khand_man1,khand_man2],
["c5_khand_kataphrakt","Variag_Ironclad","Variag_Ironclads",tf_evil_man| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_khand,[itm_khand_inf_helm_a_good, itm_khand_cav_helm_a_good, itm_khand_med_lam_good, itm_mail_mittens,itm_splinted_greaves_good,itm_khand_mace1, itm_khand_mace2,itm_easterling_round_horseman,itm_variag_kataphrakt,],attr_evil_tier_5,wp_tier_5,knows_common|knows_riding_6|knows_shield_3|knows_power_strike_5|knows_ironflesh_3,khand_man1,khand_man2],
["c5_khand_lance_kataphrakt","Variag_Lancer","Variag_Lancers",tf_evil_man| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots  |tfg_polearm,0,0,fac_khand,[itm_khand_cav_helm_c,itm_khand_heavy_lam,itm_mail_mittens,itm_splinted_greaves_good,itm_khand_tulwar,itm_khand_lance,itm_variag_kataphrakt,],attr_evil_tier_5,wp_tier_5,knows_common|knows_riding_6|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,khand_man1,khand_man2],
["i4_khand_halberdier","Khand_Glaiveman","Khand_Glaivemen",tf_evil_man| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,[itm_khand_inf_helm_b, itm_khand_inf_helm_d,itm_khand_foot_lam,itm_mail_mittens,itm_splinted_greaves,itm_khand_voulge,itm_khand_halberd,],attr_evil_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_power_strike_3|knows_ironflesh_2,khand_man1,khand_man2],
["i5_khand_halberd_master","Variag_Halberd_Master","Variag_Halberd_Masters",tf_evil_man| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,[itm_khand_inf_helm_b_good,itm_khand_inf_helm_d_good,itm_khand_foot_lam_good,itm_mail_mittens,itm_splinted_greaves_good,itm_khand_halberd,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_2|knows_power_strike_4|knows_ironflesh_3,khand_man1,khand_man2],
["i3_khand_pitfighter","Khand_Pit_Fighter","Khand_Pit_Fighters",tf_evil_man| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,[itm_khand_helm_mask,itm_khand_light,itm_leather_boots_dark_bad,itm_javelin,itm_khand_tulwar,itm_khand_pitsword,itm_shortened_spear,itm_variag_gladiator_shield,],attr_evil_tier_3,wp_tier_3,knows_common|knows_athletics_4|knows_shield_2|knows_power_throw_2|knows_power_strike_3|knows_ironflesh_3,khand_man1,khand_man2],
["i4_khand_pit_champion","Khand_Pit_Champion","Khand_Pit_Champions",tf_evil_man| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,[itm_khand_helm_mask_good,itm_khand_light,itm_khand_light_good,itm_leather_boots_dark_bad,itm_javelin,itm_khand_tulwar,itm_khand_pitsword,itm_shortened_spear,itm_easterling_hawk_shield,itm_variag_gladiator_shield,],attr_evil_tier_4,wp_tier_4,knows_common|knows_athletics_5|knows_shield_3|knows_power_throw_2|knows_power_strike_4|knows_ironflesh_4,khand_man1,khand_man2],
["i5_khand_pit_master","Variag_Master_of_the_Pits","Variag_Masters_of_the_Pits",tf_evil_man| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,[itm_khand_helm_mask_good,itm_khand_light,itm_khand_light_good,itm_leather_boots_dark_bad,itm_javelin,itm_khand_tulwar,itm_khand_pitsword,itm_khand_trident,itm_easterling_hawk_shield,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_6|knows_shield_4|knows_power_throw_4|knows_power_strike_5|knows_ironflesh_6,khand_man1,khand_man2],
["ac3_khand_skirmisher","Khand_Skirmisher","Khand_Skirmishers",tf_evil_man| tfg_ranged| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_khand,[itm_khand_inf_helm_a_bad, itm_khand_inf_helm_b_bad, itm_khand_cav_helm_a_bad,itm_khand_light,itm_khand_light_lam,itm_leather_boots_dark,itm_javelin,itm_javelin,itm_khand_tulwar,itm_steppe_horse,],attr_evil_tier_3,wp_tier_3,knows_common|knows_horse_archery_4|knows_riding_2|knows_power_throw_2|knows_power_strike_1,khand_man1,khand_man2],
["ac4_khand_vet_skirmisher","Khand_Veteran_Skirmisher","Khand_Veteran_Skirmishers",tf_evil_man| tfg_ranged| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_khand,[itm_khand_inf_helm_a, itm_khand_cav_helm_b,itm_khand_med_lam, itm_leather_gloves,itm_splinted_greaves,itm_leather_boots_dark,itm_javelin,itm_javelin,itm_khand_tulwar,itm_easterling_round_horseman,itm_steppe_horse,],attr_evil_tier_4,wp_tier_4,knows_common|knows_horse_archery_3|knows_riding_5|knows_shield_3|knows_power_throw_3|knows_power_strike_2|knows_ironflesh_2,khand_man1,khand_man2],
["ac5_khand_heavy_skirmisher","Variag_Heavy_Skirmisher","Variag_Heavy_Skirmishers",tf_evil_man| tfg_ranged| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_khand,[itm_khand_cav_helm_b_good,itm_khand_heavy_lam_bad,itm_leather_gloves,itm_splinted_greaves,itm_javelin,itm_javelin,itm_khand_tulwar,itm_easterling_round_horseman,itm_variag_kataphrakt,],attr_evil_tier_5,wp_tier_5,knows_common|knows_horse_archery_4|knows_riding_6|knows_shield_3|knows_power_throw_5|knows_power_strike_3|knows_ironflesh_2,khand_man1,khand_man2],

["khand_items","BUG","_",tf_hero,0,0,fac_khand,
   [itm_leather_boots,itm_leather_gloves,itm_sumpter_horse,itm_saddle_horse,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
#UMBAR #CORSAIRS
["i1_corsair_youth","Umbar_Sailor","Umbar_Sailors",tfg_armor,0,0,fac_umbar,[itm_hood_black,itm_umb_armor_a_bad, itm_umb_armor_a, itm_umb_armor_a_cloak,itm_corsair_boots,itm_shortened_spear,itm_corsair_sword,],attr_evil_tier_1,wp_tier_1,knows_common|knows_power_throw_1|knows_power_draw_1|knows_weapon_master_1|knows_athletics_2|knows_looting_2|knows_tactics_2|knows_spotting_1|knows_inventory_management_1|knows_prisoner_management_1|knows_trade_1,bandit_face1,bandit_face2],
["i2_corsair_warrior","Umbar_Warrior","Umbar_Warriors",tfg_armor,0,0,fac_umbar,[itm_hood_black,itm_umb_helm_d,itm_umb_armor_a, itm_umb_armor_a_cloak,itm_umb_armor_a_good,itm_corsair_boots,itm_shortened_spear,itm_corsair_sword,itm_umbar_rapier,itm_umb_shield_b,],attr_evil_tier_2,wp_tier_2,knows_common|knows_power_strike_1|knows_power_throw_1|knows_power_draw_1|knows_weapon_master_1|knows_shield_1|knows_athletics_3|knows_looting_2|knows_tactics_2|knows_spotting_1|knows_inventory_management_1|knows_prisoner_management_1|knows_trade_1,bandit_face1,bandit_face2],
["i3_corsair_spearman","Spearman_of_Umbar","Spearmen_of_Umbar",tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,[itm_umb_helm_d,itm_umb_helm_c,itm_umb_armor_c_good, itm_umb_armor_c, itm_umb_armor_c_bad,itm_corsair_boots,itm_shortened_spear,itm_umb_shield_a,],attr_evil_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_shield_2|knows_power_strike_2,bandit_face1,bandit_face2],
["i4_corsair_raider","Corsair_Raider","Corsair_Raiders",tfg_armor| tfg_boots,0,0,fac_umbar,[itm_hood_black,itm_umb_armor_b_good,itm_umb_armor_b, itm_umb_armor_b_cloak,itm_corsair_boots,itm_umbar_rapier,itm_corsair_harpoon,itm_corsair_harpoon,itm_umb_shield_b, itm_umb_shield_c,],attr_evil_tier_4,wp_tier_4,knows_common|knows_athletics_6|knows_shield_2|knows_power_throw_3|knows_power_strike_3,bandit_face1,bandit_face2],
["i5_corsair_night_raider","Corsair_Night_Raider","Corsair_Night_Raiders",tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,[itm_hood_black_good,itm_umb_armor_d_bad, itm_umb_armor_d, itm_umb_armor_d_cloak,itm_leather_gloves,itm_corsair_boots,itm_umbar_rapier,itm_corsair_harpoon,itm_corsair_harpoon,itm_umb_shield_c,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_8|knows_shield_4|knows_power_strike_4|knows_ironflesh_3|knows_power_throw_5,bandit_face1,bandit_face2],
["a2_corsair_marine","Umbar_Marine","Umbar_Marines",tfg_ranged| tfg_armor,0,0,fac_umbar,[itm_hood_black,itm_umb_armor_a_bad, itm_umb_armor_a,itm_corsair_boots,itm_short_bow, itm_regular_bow,itm_corsair_arrows,itm_corsair_throwing_dagger,itm_corsair_sword,itm_umb_shield_b,],attr_evil_tier_2,wp_tier_bow_2,knows_common|knows_ironflesh_1|knows_power_throw_1|knows_power_draw_2|knows_weapon_master_1|knows_athletics_3|knows_looting_2|knows_tactics_2|knows_spotting_1|knows_inventory_management_1|knows_prisoner_management_1|knows_trade_1,bandit_face1,bandit_face2],
["a3_corsair_marksman","Marksman_of_Umbar","Marksmen_of_Umbar",tfg_ranged| tfg_armor| tfg_boots,0,0,fac_umbar,[itm_umb_helm_d,itm_umb_helm_c,itm_umb_armor_b_bad, itm_umb_armor_b, itm_umb_armor_b_cloak,itm_corsair_boots,itm_regular_bow,itm_corsair_arrows,itm_corsair_sword,],attr_evil_tier_3,wp_tier_bow_3,knows_common|knows_athletics_3|knows_power_draw_2|knows_ironflesh_1,bandit_face1,bandit_face2],
["a4_corsair_veteran_marksman","Veteran_Marksman_of_Umbar","Veteran_Marksmen_of_Umbar",tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,[itm_umb_helm_d,itm_umb_helm_c,itm_umb_armor_c_bad, itm_umb_armor_c,itm_corsair_boots,itm_corsair_bow,itm_corsair_arrows,itm_umbar_cutlass,],attr_evil_tier_4,wp_tier_bow_4,knows_common|knows_athletics_4|knows_power_draw_4|knows_ironflesh_1,bandit_face1,bandit_face2],
["a5_corsair_master_marksman","Corsair_Master_Marksman","Corsair_Master_Marksmen",tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,[itm_umb_helm_c_good,itm_umb_armor_e_bad, itm_umb_armor_e_cloak, itm_umb_armor_e,itm_leather_gloves,itm_corsair_boots,itm_corsair_bow,itm_corsair_arrows,itm_corsair_arrows,itm_umbar_cutlass,],attr_evil_tier_5,wp_tier_bow_5,knows_common|knows_athletics_6|knows_power_draw_5|knows_ironflesh_2,bandit_face1,bandit_face2],
["i3_corsair_swordsman","Swordsman_of_Umbar","Swordsmen_of_Umbar",tfg_armor| tfg_helm| tfg_boots|tfg_shield,0,0,fac_umbar,[itm_umb_helm_d,itm_umb_helm_c,itm_umb_armor_c_good, itm_umb_armor_c, itm_umb_armor_c_bad,  itm_umb_armor_c_cloak,itm_corsair_boots,itm_umbar_cutlass,itm_umbar_rapier,itm_umb_shield_b, itm_umb_shield_c,],attr_evil_tier_3,wp_tier_3,knows_common|knows_athletics_3|knows_shield_2|knows_power_strike_2,bandit_face1,bandit_face2],
["i4_corsair_veteran_swordsman","Veteran_Swordsman_of_Umbar","Veteran_Swordsmen_of_Umbar",tfg_armor| tfg_helm| tfg_boots|tfg_shield,0,0,fac_umbar,[itm_umb_helm_b,itm_umb_armor_d_good, itm_umb_armor_d_bad, itm_umb_armor_d, itm_umb_armor_d_cloak,itm_leather_gloves,itm_corsair_boots,itm_umbar_cutlass,itm_umb_shield_c,],attr_evil_tier_4,wp_tier_4,knows_common|knows_athletics_4|knows_shield_2|knows_power_throw_1|knows_power_strike_3,bandit_face1,bandit_face2],
["i5_corsair_master_swordsman","Corsair_Swordmaster","Corsair_Swordmasters",tfg_gloves| tfg_armor| tfg_helm| tfg_boots|tfg_shield,0,0,fac_umbar,[itm_umb_helm_b_good,itm_umb_armor_f_bad,itm_umb_armor_f_good, itm_umb_armor_f, itm_umb_armor_f_cloak,itm_leather_gloves,itm_corsair_boots,itm_kraken,itm_umb_shield_d,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_6|knows_shield_2|knows_power_throw_2|knows_power_strike_4|knows_ironflesh_3,bandit_face1,bandit_face2],
["a4_corsair_assassin","Corsair_Assassin","Corsair_Assassins",tfg_ranged| tfg_armor| tfg_boots,0,0,fac_umbar,[itm_hood_black,itm_hood_black_good,itm_leather_gloves,itm_corsair_boots,itm_corsair_bow,itm_corsair_arrows,itm_kraken,itm_umb_shield_b, ],attr_evil_tier_5,wp_archery(150) | wp_melee(200),knows_common|knows_athletics_5|knows_power_draw_3|knows_power_strike_4|knows_ironflesh_4,bandit_face1,bandit_face2],
["a5_corsair_master_assassin","Corsair_Assassin","Corsair_Assassins",tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,[itm_hood_black_good,itm_umb_helm_a,itm_umb_armor_d_cloak, itm_umb_armor_d,itm_leather_gloves,itm_corsair_boots,itm_corsair_bow,itm_corsair_arrows,itm_kraken,itm_umb_shield_b, ],attr_evil_tier_5,wp_archery(150) | wp_melee(200),knows_common|knows_athletics_8|knows_power_draw_5|knows_power_strike_4|knows_ironflesh_4,bandit_face1,bandit_face2],
["i4_corsair_veteran_spearman","Veteran_Spearman_of_Umbar","Veteran_Spearmen_of_Umbar",tfg_armor| tfg_helm| tfg_boots|tfg_shield,0,0,fac_umbar,[itm_umb_helm_b,itm_umb_armor_d_good, itm_umb_armor_d_bad, itm_umb_armor_d,itm_corsair_boots,itm_umbar_spear,itm_umb_shield_a,],attr_evil_tier_4,wp_tier_4,knows_common|knows_athletics_3|knows_shield_2|knows_power_strike_2,bandit_face1,bandit_face2],
["i5_corsair_master_spearman","Spearmaster_of_Umbar","Spearmasters_of_Umbar",tfg_armor| tfg_helm| tfg_boots|tfg_shield,0,0,fac_umbar,[itm_umb_helm_a,itm_umb_armor_e_good, itm_umb_armor_e, itm_umb_armor_e_bad,itm_corsair_boots,itm_umbar_spear,itm_umb_shield_e,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_4|knows_shield_2|knows_power_throw_1|knows_power_strike_3,bandit_face1,bandit_face2],
["i5_corsair_master_pikeman","Pikemaster_of_Umbar","Pikemasters_of_Umbar",tfg_gloves| tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,[itm_umb_helm_b_good,itm_umb_armor_f_good, itm_umb_armor_f, itm_umb_armor_f_cloak,itm_mail_mittens,itm_corsair_boots,itm_umbar_pike,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_4|knows_shield_2|knows_power_throw_2|knows_power_strike_6|knows_ironflesh_3,bandit_face1,bandit_face2],

["umbar_items","BUG","_",tf_hero,0,0,fac_umbar,
   [itm_leather_boots,itm_leather_gloves,itm_short_bow,itm_regular_bow,itm_arrows,itm_sumpter_horse,itm_saddle_horse,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
0,0,0,0],

#Isengard
["i1_isen_orc_snaga","Orc_Snaga_of_Isengard","Orc_Snagas_of_Isengard",tf_orc| tf_no_capture_alive,0,0,fac_isengard,[itm_orc_coif_bad,itm_orc_coif,itm_isen_orc_light_a_bad,itm_isen_orc_light_b_bad,itm_wood_club,itm_orc_simple_spear,itm_orc_slasher,itm_orc_axe,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],attr_orc_tier_1,wp_orc_tier_1,knows_common|knows_ironflesh_1|knows_power_strike_1|knows_shield_1|knows_athletics_1|knows_riding_1|knows_looting_2|knows_tactics_1|knows_pathfinding_1|knows_wound_treatment_1|knows_surgery_1|knows_prisoner_management_1|knows_trade_1,orc_face1,orc_face2],
["i2_isen_orc","Orc_of_Isengard","Orcs_of_Isengard",tf_orc| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_orc_helm_a_bad, itm_isen_orc_helm_a,itm_isen_orc_light_a,itm_isen_orc_light_b,itm_orc_ragwrap,itm_isengard_spear,itm_orc_simple_spear,itm_orc_bill_bad,itm_orc_bill_bad,itm_orc_slasher,itm_orc_slasher_heavy,itm_orc_slasher,itm_orc_axe,itm_isen_orc_shield_a,],attr_orc_tier_2,wp_orc_tier_2,knows_common|knows_ironflesh_1|knows_power_strike_2|knows_power_throw_1|knows_shield_1|knows_athletics_1|knows_riding_1|knows_looting_2|knows_tactics_1|knows_pathfinding_1|knows_wound_treatment_1|knows_surgery_1|knows_prisoner_management_1|knows_trade_1,orc_face2,orc_face3],
["i3_isen_large_orc","Large_Orc_of_Isengard","Large_Orcs_of_Isengard",tf_orc| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_orc_helm_a,itm_isen_orc_pad_a,itm_isen_orc_pad_b,itm_orc_ragwrap,itm_isengard_spear,itm_isengard_spear,itm_orc_simple_spear,itm_orc_bill_bad,itm_orc_slasher_heavy,itm_isengard_sword,itm_orc_axe,itm_isen_orc_shield_a,itm_isen_orc_shield_b,],attr_orc_tier_3,wp_orc_tier_3,knows_common|knows_athletics_2|knows_power_throw_2|knows_power_strike_4,orc_face4,orc_face5],
["i4_isen_fell_orc","Fell_Orc_of_Isengard","Fell_Orcs_of_Isengard",tf_orc| tfg_armor| tfg_helm| tfg_boots| tfg_gloves| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_orc_helm_a_good,itm_isen_orc_pad_b_good, itm_isen_orc_mail_b, itm_orc_greaves,itm_isengard_spear,itm_isengard_spear,itm_isengard_sword,itm_orc_axe,itm_isen_orc_shield_a,itm_isen_orc_shield_b,],attr_orc_tier_4,wp_orc_tier_4,knows_common|knows_athletics_2|knows_power_throw_3|knows_power_strike_4,orc_face6,orc_face7],
["i3_isen_large_orc_despoiler","Large_Orc_Despoiler","Large_Orc_Despoilers",tf_orc|tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_orc_helm_a,itm_isen_orc_mail_a_bad,itm_isen_orc_light_b_good,itm_orc_greaves,itm_orc_sledgehammer,itm_isengard_hammer,itm_twohand_wood_club,],attr_orc_tier_3,wp_orc_tier_3,knows_common|knows_athletics_3|knows_power_strike_4,orc_face8,orc_face9],
["i4_isen_fell_orc_despoiler","Fell_Orc_Despoiler","Fell_Orc_Despoilers",tf_orc| tfg_armor| tfg_helm| tfg_boots| tfg_gloves| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_orc_helm_a_good,itm_isen_orc_mail_a, itm_isen_orc_mail_b_bad, itm_orc_greaves,itm_isengard_mallet,itm_orc_sledgehammer,itm_isengard_hammer,itm_twohand_wood_club,],attr_orc_tier_4,wp_orc_tier_4,knows_common|knows_athletics_4|knows_power_strike_5,orc_face3,orc_face6],
["ac2_isen_wolf_rider","Wolf_Rider_of_Isengard","Wolf_Riders_of_Isengard",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_horse| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_orc_light_a,itm_isen_orc_light_b,itm_orc_throwing_arrow,itm_orc_throwing_arrow,itm_orc_simple_spear,itm_warg_1d,itm_warg_1b,itm_warg_1c,],attr_orc_tier_2,wp_orc_tier_2,knows_common|knows_power_strike_1|knows_power_throw_2|knows_riding_2|knows_horse_archery_2|knows_looting_2|knows_tactics_1|knows_pathfinding_1|knows_wound_treatment_1|knows_surgery_1|knows_prisoner_management_1|knows_trade_1,orc_face7,orc_face4],
["ac3_isen_warg_rider","Warg_Rider_of_Isengard","Warg_Riders_of_Isengard",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_horse| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_orc_helm_a_good,itm_isen_orc_light_a_good, itm_isen_orc_light_b_good, itm_isen_orc_mail_a_bad, itm_orc_ragwrap,itm_orc_throwing_arrow,itm_orc_throwing_arrow,itm_orc_club_b,itm_orc_simple_spear,itm_warg_1d,itm_warg_1b,itm_warg_1c,],attr_orc_tier_3,wp_orc_tier_3,knows_common|knows_riding_3|knows_power_throw_3|knows_power_strike_3|knows_horse_archery_4,orc_face5,orc_face8],
["ac4_isen_white_hand_rider","White_Hand_Rider","White_Hand_Riders",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_uruk_helm_a,itm_isen_orc_mail_a, itm_orc_ragwrap,itm_orc_throwing_arrow,itm_orc_throwing_arrow,itm_isengard_mallet,itm_isengard_spear,itm_wargarmored_1b, itm_wargarmored_1c,],attr_orc_tier_4,wp_orc_tier_4,knows_common|knows_riding_5|knows_power_throw_5|knows_power_strike_4|knows_horse_archery_5,orc_face7,orc_face8],

# "ghost" warg riders:(invisible riders for lone wargs) number and order match warg items
["warg_ghost_1b","Warg","Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm| tf_no_capture_alive ,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_warg_1b],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face7,orc_face2],
["warg_ghost_1c","Warg","Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_warg_1c],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face6,orc_face1],
["warg_ghost_1d","Warg","Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_warg_1d],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face1,orc_face2],
["warg_ghost_a1b","Warg","Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_wargarmored_1b],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face1,orc_face2],
["warg_ghost_a1c","Armored Warg","Armored Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_wargarmored_1c],
     str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face1,orc_face2],
["warg_ghost_a2b","Armored Warg","Armored Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_wargarmored_2b],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face1,orc_face2],
["warg_ghost_a2c","Armored Warg","Armored Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_wargarmored_2c],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face1,orc_face2],
["warg_ghost_a3a","Armored Warg","Armored Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_wargarmored_3a],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face1,orc_face2],
["warg_ghost_h","Huge Warg","Huge Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_warg_reward],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face1,orc_face2],

    
#Isengard 
# first non ghost-warg
["a2_isen_uruk_tracker","Uruk_Hai_Tracker","Uruk_Hai_Trackers",tf_urukhai| tf_mounted| tfg_ranged| tfg_armor| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_uruk_heavy_d_bad,itm_uruk_ragwrap,itm_short_bow,itm_isengard_arrow,itm_isengard_axe,],attr_tier_2,wp_tier_bow_2,knows_common|knows_ironflesh_2|knows_power_strike_1|knows_power_draw_2|knows_weapon_master_1|knows_athletics_3|knows_trainer_1|knows_tactics_1|knows_pathfinding_2|knows_spotting_1|knows_surgery_1|knows_prisoner_management_1|knows_leadership_1,uruk_hai_face1,uruk_hai_face2],
["a3_isen_large_uruk_tracker","Large_Uruk_Hai_Tracker","Large_Uruk_Hai_Trackers",tf_urukhai| tf_mounted| tfg_ranged| tfg_armor| tfg_boots| tfg_helm| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_tracker_helm,itm_isen_uruk_heavy_d,itm_uruk_ragwrap,itm_isengard_large_bow,itm_isengard_arrow,itm_isengard_axe,itm_isengard_sword],attr_evil_tier_3,wp_tier_bow_4,knows_common|knows_athletics_6|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_2,uruk_hai_face1,uruk_hai_face2],
["a4_isen_fighting_uruk_tracker","Fighting_Uruk_Hai_Tracker","Fighting_Uruk_Hai_Trackers",tf_urukhai| tf_mounted| tfg_ranged| tfg_armor| tfg_boots| tfg_helm| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_tracker_helm_good,itm_isen_uruk_heavy_d_good,itm_uruk_ragwrap,itm_isengard_large_bow,itm_isengard_arrow,itm_isengard_sword,itm_isengard_heavy_axe,itm_isengard_heavy_sword,],attr_evil_tier_4,wp_tier_bow_5,knows_common|knows_athletics_7|knows_power_draw_4|knows_power_strike_2|knows_ironflesh_5,uruk_hai_face1,uruk_hai_face2],
["i6_isen_uruk_berserker","Fighting_Uruk_Hai_Berserker","Fighting_Uruk_Hai_Berserkers",tf_urukhai| tf_mounted| tfg_armor| tfg_helm| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_tracker_helm_good,itm_isen_uruk_light_c_bad, itm_isen_uruk_light_c,itm_evil_gauntlets_b,itm_uruk_chain_greaves,itm_uruk_ragwrap, itm_isengard_heavy_axe,itm_isengard_mallet,itm_isengard_heavy_sword,],attr_evil_tier_6,wp_tier_6,knows_common|knows_athletics_7|knows_power_strike_6|knows_ironflesh_10,uruk_hai_face1,uruk_hai_face2],
["i1_isen_uruk_snaga","Uruk_Hai_Newborn","Uruk_Hai_Newborns",tf_urukhai| tf_mounted| tfg_boots| tfg_armor| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_orc_helm_a_bad,itm_isen_uruk_light_a,itm_isen_uruk_light_a_bad,itm_isen_uruk_light_b_bad,itm_uruk_ragwrap,itm_orc_simple_spear,itm_orc_slasher,itm_orc_axe,],attr_evil_tier_1,wp_tier_1,knows_common|knows_ironflesh_2|knows_power_strike_1|knows_weapon_master_1|knows_athletics_1|knows_trainer_1|knows_tactics_1|knows_pathfinding_2|knows_spotting_1|knows_surgery_1|knows_prisoner_management_1|knows_leadership_1,uruk_hai_face1,uruk_hai_face2],
["i2_isen_uruk","Uruk_Hai_of_Isengard","Uruk_Hai_of_Isengard",tf_urukhai| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_orc_helm_a,itm_isen_uruk_light_a_good, itm_isen_uruk_light_b, itm_isen_uruk_med_a_bad, itm_isen_uruk_med_b_bad,itm_uruk_ragwrap,itm_isengard_spear,itm_isengard_axe,itm_isengard_sword, itm_isen_orc_shield_a,itm_isen_orc_shield_b,],attr_evil_tier_2,wp_tier_2,knows_common|knows_ironflesh_2|knows_power_strike_2|knows_weapon_master_1|knows_shield_1|knows_athletics_2|knows_trainer_1|knows_tactics_1|knows_pathfinding_2|knows_spotting_1|knows_surgery_1|knows_prisoner_management_1|knows_leadership_1,uruk_hai_face1,uruk_hai_face2],
["i3_isen_large_uruk","Large_Uruk_Hai_of_Isengard","Large_Uruk_Hai_of_Isengard",tf_urukhai| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_uruk_helm_a_bad,itm_isen_uruk_light_b_good, itm_isen_uruk_med_a, itm_isen_uruk_med_b,itm_evil_gauntlets_a,itm_uruk_ragwrap,itm_uruk_greaves,itm_isengard_axe,itm_isengard_sword, itm_isen_orc_shield_a,itm_isen_orc_shield_b,],attr_evil_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_power_strike_3|knows_ironflesh_4,uruk_hai_face1,uruk_hai_face2],
["i4_isen_fighting_uruk_warrior","Fighting_Uruk_Hai_Warrior","Fighting_Uruk_Hai_Warriors",tf_urukhai|tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_uruk_helm_a,itm_isen_uruk_med_b_good, itm_isen_uruk_heavy_a_bad, itm_isen_uruk_heavy_b, itm_evil_gauntlets_b,itm_uruk_greaves,itm_isengard_sword, itm_isen_uruk_shield_b,],attr_evil_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_power_strike_5|knows_ironflesh_5,uruk_hai_face1,uruk_hai_face2],
["i5_isen_fighting_uruk_champion","Fighting_Uruk_Hai_Champion","Fighting_Uruk_Hai_Champions",tf_urukhai|tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_uruk_helm_a_good,itm_isen_uruk_heavy_b_good, itm_isen_uruk_heavy_c, itm_evil_gauntlets_b,itm_uruk_chain_greaves,itm_isengard_sword, itm_isen_uruk_shield_b,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_power_strike_6|knows_ironflesh_6,uruk_hai_face1,uruk_hai_face2],
["i3_isen_uruk_pikeman","Uruk_Hai_Pikeman","Uruk_Hai_Pikemen",tf_urukhai| tf_mounted|tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_uruk_helm_a,itm_isen_uruk_med_a_good, itm_isen_uruk_heavy_a_bad, itm_isen_uruk_heavy_b_bad, itm_evil_gauntlets_a,itm_uruk_chain_greaves,itm_isengard_pike,],attr_evil_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_power_strike_3|knows_ironflesh_4,uruk_hai_face1,uruk_hai_face2],
["i4_isen_fighting_uruk_pikeman","Fighting_Uruk_Hai_Pikeman","Fighting_Uruk_Hai_Pikemen",tf_urukhai|tf_mounted| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_uruk_helm_a_good,itm_isen_uruk_heavy_c_good, itm_isen_uruk_heavy_b_good,itm_evil_gauntlets_b,itm_uruk_chain_greaves,itm_isengard_pike,itm_isengard_halberd,],attr_evil_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_power_strike_5|knows_ironflesh_5,uruk_hai_face1,uruk_hai_face2],
["i5_isen_uruk_standard_bearer","Uruk_Hai_Standard_Bearer","Uruk_Hai_Standard_Bearers",tf_urukhai|tf_mounted| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_uruk_helm_a_good,itm_isen_uruk_heavy_c_good,itm_evil_gauntlets_b,itm_uruk_chain_greaves,itm_isengard_banner,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_2|knows_power_strike_5|knows_ironflesh_10,uruk_hai_face1,uruk_hai_face2],

#Mordor Uruks
["i1_mordor_uruk_snaga","Uruk_Snaga_of_Mordor","Uruk_Snagas_of_Mordor",tf_uruk| tf_no_capture_alive,0,0,fac_mordor,[itm_m_uruk_light_a,itm_m_uruk_light_a_good, itm_m_uruk_light_a_bad,itm_uruk_ragwrap,itm_orc_axe,itm_orc_falchion,itm_orc_sabre,itm_orc_simple_spear,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],attr_evil_tier_1,wp_tier_1,knows_common|knows_ironflesh_2|knows_power_strike_1|knows_shield_1|knows_athletics_1|knows_looting_1|knows_trainer_2|knows_tactics_1|knows_spotting_1|knows_wound_treatment_1|knows_prisoner_management_1|knows_leadership_1,uruk_hai_face1,uruk_hai_face2],
["i2_mordor_uruk","Uruk_of_Mordor","Uruks_of_Mordor",tf_uruk| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,[itm_uruk_helm_a,itm_uruk_helm_b,itm_orc_coif,itm_m_uruk_light_b, itm_m_uruk_light_b_good, itm_m_uruk_light_b_bad, itm_m_uruk_light_c_good, itm_m_uruk_light_c_bad,itm_uruk_ragwrap,itm_orc_simple_spear_heavy,itm_uruk_falchion_a,itm_uruk_falchion_b,itm_mordor_uruk_shield_a,],attr_evil_tier_2,wp_tier_2,knows_common|knows_ironflesh_3|knows_power_strike_2|knows_shield_1|knows_athletics_1|knows_looting_1|knows_trainer_2|knows_tactics_1|knows_spotting_1|knows_wound_treatment_1|knows_prisoner_management_1|knows_leadership_1,uruk_hai_face1,uruk_hai_face2],
["i3_mordor_large_uruk","Large_Uruk_of_Mordor","Large_Uruks_of_Mordor",tf_uruk| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,[itm_uruk_helm_c,itm_uruk_helm_d,itm_m_uruk_med_a, itm_m_uruk_med_a_good, itm_m_uruk_med_a_bad, itm_m_uruk_med_b, itm_m_uruk_med_b_good, itm_m_uruk_med_b_bad, itm_m_uruk_med_c, itm_m_uruk_med_c_good, itm_m_uruk_med_c_bad, itm_evil_gauntlets_a,itm_uruk_ragwrap,itm_uruk_greaves,itm_uruk_falchion_a,itm_uruk_falchion_b,itm_mordor_uruk_shield_a,itm_mordor_uruk_shield_b,],attr_evil_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_power_strike_3|knows_ironflesh_4,uruk_hai_face1,uruk_hai_face2],
["i4_mordor_fell_uruk","Fell_Uruk_of_Mordor","Fell_Uruks_of_Mordor",tf_uruk| tfg_shield|tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,[itm_uruk_helm_b,itm_uruk_helm_c,itm_uruk_helm_d,itm_m_uruk_heavy_a, itm_m_uruk_heavy_a_good, itm_m_uruk_heavy_a_bad, itm_m_uruk_heavy_b, itm_m_uruk_heavy_b_good, itm_m_uruk_heavy_b_bad,itm_evil_gauntlets_b,itm_uruk_greaves,itm_uruk_chain_greaves,itm_uruk_falchion_a,itm_uruk_falchion_b,itm_mordor_uruk_shield_a,itm_mordor_uruk_shield_b,],attr_evil_tier_4,wp_tier_4,knows_common|knows_athletics_3|knows_power_strike_5|knows_power_throw_3|knows_ironflesh_4|knows_shield_2,uruk_hai_face1,uruk_hai_face2],
["i3_mordor_uruk_slayer","Uruk_Slayer_of_Mordor","Uruk_Slayers_of_Mordor",tf_uruk| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,[itm_uruk_helm_b,itm_uruk_helm_c,itm_uruk_helm_d,itm_m_uruk_med_a, itm_m_uruk_med_a_good, itm_m_uruk_med_a_bad, itm_m_uruk_med_b, itm_m_uruk_med_b_good, itm_m_uruk_med_b_bad, itm_m_uruk_med_c, itm_m_uruk_med_c_good, itm_m_uruk_med_c_bad,itm_uruk_tracker_boots,itm_orc_bill_heavy,itm_orc_skull_spear_heavy,itm_uruk_pike_b,itm_uruk_falchion_a,itm_uruk_falchion_b,],attr_evil_tier_3,wp_tier_4,knows_common|knows_athletics_3|knows_power_strike_5|knows_ironflesh_6,uruk_hai_face1,uruk_hai_face2],
["i4_mordor_fell_uruk_slayer","Fell_Uruk_Slayer_of_Mordor","Fell_Uruk_Slayers_of_Mordor",tf_uruk| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,[itm_uruk_helm_c,itm_uruk_helm_f,itm_m_uruk_heavy_a, itm_m_uruk_heavy_a_good, itm_m_uruk_heavy_a_bad, itm_m_uruk_heavy_b, itm_m_uruk_heavy_b_good, itm_m_uruk_heavy_b_bad,itm_evil_gauntlets_b,itm_uruk_greaves,itm_uruk_chain_greaves,itm_orc_bill_heavy,itm_orc_two_handed_axe_heavy,itm_orc_skull_spear_heavy,itm_uruk_pike_b,itm_uruk_falchion_a,itm_uruk_falchion_b,itm_uruk_bow,itm_orc_hook_arrow,],attr_evil_tier_4,wp_tier_5,knows_common|knows_athletics_5|knows_power_strike_7|knows_power_draw_4|knows_ironflesh_7,uruk_hai_face1,uruk_hai_face2],
["i5_mordor_black_uruk","Black_Uruk_of_Barad_Dur","Black_Uruks_of_Barad_Dur",tf_uruk| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,[itm_uruk_helm_e,itm_m_uruk_heavy_c, itm_m_uruk_heavy_c_good, itm_m_uruk_heavy_c_bad,itm_evil_gauntlets_b,itm_uruk_chain_greaves,itm_orc_two_handed_axe_heavy,itm_uruk_falchion_a,itm_uruk_falchion_b,itm_mordor_uruk_shield_c,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_power_strike_5|knows_ironflesh_9,uruk_hai_face1,uruk_hai_face2],
["i5_mordor_uruk_standard_bearer","Mordor_Standard_Bearer","Mordor_Standard_Bearers",tf_uruk| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,[itm_uruk_helm_b,itm_uruk_helm_c,itm_uruk_helm_d,itm_m_uruk_heavy_c, itm_m_uruk_heavy_c_good, itm_m_uruk_heavy_c_bad,itm_evil_gauntlets_b,itm_uruk_greaves,itm_uruk_chain_greaves,itm_mordor_banner,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_power_strike_5|knows_ironflesh_10,uruk_hai_face1,uruk_hai_face2],

#Trolls  & ents (moved to end of file, keep these a bit for backup reasons)
["troll_of_moria","Cave_Troll","Cave_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_moria,
   [itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_b,itm_tree_trunk_club_b,itm_troll_feet,itm_troll_body,itm_troll_head_a,itm_troll_head_b,itm_troll_head_c,itm_troll_hands],
      str_255| agi_3| int_3| cha_3|level(58),wp(150),knows_power_strike_5|knows_ironflesh_10,troll_face1,troll_face2],
["armoured_troll","Armored_Troll","Armored_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_isengard,
   [itm_giant_mace, itm_giant_mace_b,itm_giant_hammer,itm_isen_olog_feet,itm_isen_olog_body,itm_isen_olog_body_b,itm_isen_olog_head_a,itm_isen_olog_head_b,itm_isen_olog_head_c,itm_isen_olog_hands],
      str_255| agi_3| int_3| cha_3|level(61),wp(175),knows_power_strike_7|knows_ironflesh_13,troll_face1,troll_face2],
["olog_hai","Olog_Hai_of_Mordor","Olog_Hai_of_Mordor",tf_troll|tfg_shield| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_mordor,
   [itm_giant_mace, itm_troll_shield_a,itm_giant_mace_b,itm_giant_hammer,itm_olog_feet,itm_olog_body,itm_olog_body_b,itm_olog_head_a,itm_olog_head_b,itm_olog_head_c,itm_olog_hands],
      str_255| agi_3| int_3| cha_3|level(61),wp(250),knows_power_strike_8|knows_ironflesh_15,troll_face1,troll_face2],
["ent_old","Ent","Ents",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_commoners,
   [itm_tree_trunk_invis,itm_ent_body,itm_ent_hands,itm_ent_feet_boots,itm_ent_head,itm_ent_water,itm_ent_head_2,itm_ent_head_3,],
      str_255| agi_3| int_3| cha_3|level(63),wp(250),knows_power_strike_15|knows_ironflesh_15,troll_face1,troll_face2],

# Dol Guldur Orcs
["i1_guldur_orc_snaga","Orc_Snaga_of_Dol_Guldur","Orc_Snagas_of_Dol_Guldur",tf_orc| tf_no_capture_alive,0,0,fac_guldur,[itm_orc_coif_bad, itm_orc_coif,itm_m_orc_light_a,itm_m_orc_light_b,itm_m_orc_light_c,itm_wood_club,itm_orc_slasher,itm_orc_simple_spear,itm_orc_axe,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],attr_orc_tier_1,wp_orc_tier_1,knows_common|knows_ironflesh_1|knows_power_draw_1|knows_athletics_3|knows_looting_1|knows_tracking_1|knows_tactics_1|knows_pathfinding_2|knows_spotting_1|knows_surgery_1|knows_persuasion_1,orc_face5,orc_face4],
["a2_guldur_orc_tracker","Orc_Tracker_of_Dol_Guldur","Orc_Trackers_of_Dol_Guldur",tf_orc| tfg_ranged| tfg_armor| tf_no_capture_alive,0,0,fac_guldur,[itm_orc_coif, itm_orc_coif_good, itm_orc_nosehelm_bad, itm_orc_nosehelm,itm_m_orc_light_a,itm_m_orc_light_b,itm_m_orc_light_c,itm_orc_ragwrap,itm_orc_bow,itm_orc_hook_arrow,itm_wood_club,itm_orc_simple_spear,itm_orc_axe,],attr_orc_tier_2,wp_orc_tier_2,knows_common|knows_ironflesh_1|knows_power_strike_2|knows_power_draw_1|knows_athletics_4|knows_looting_1|knows_tracking_1|knows_tactics_1|knows_pathfinding_2|knows_spotting_1|knows_surgery_1|knows_persuasion_1,orc_face3,orc_face8],

#MORDOR Orcs
["i1_mordor_orc_snaga","Orc_Snaga_of_Mordor","Orc_Snagas_of_Mordor",tf_orc| tf_no_capture_alive,0,0,fac_mordor,[itm_orc_coif_bad, itm_orc_coif, itm_orc_nosehelm_bad,itm_m_orc_light_a,itm_m_orc_light_b,itm_m_orc_light_c,itm_orc_ragwrap,itm_wood_club,itm_orc_slasher,itm_orc_axe,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],attr_orc_tier_1,wp_orc_tier_1,knows_common|knows_power_strike_1|knows_power_throw_1|knows_shield_1|knows_athletics_1|knows_looting_1|knows_trainer_1|knows_tactics_1|knows_inventory_management_1|knows_wound_treatment_1|knows_prisoner_management_2|knows_leadership_1|knows_trade_1,orc_face1,orc_face2],
["i2_mordor_orc","Orc_of_Mordor","Orcs_of_Mordor",tf_orc| tfg_armor| tf_no_capture_alive,0,0,fac_mordor,[itm_orc_coif_bad, itm_orc_coif, itm_orc_nosehelm, itm_orc_nosehelm_bad, itm_orc_visorhelm_bad,itm_m_orc_light_b,itm_m_orc_light_c,itm_m_orc_light_d,itm_m_orc_light_e,itm_orc_ragwrap,itm_wood_club,itm_orc_falchion_bad,itm_orc_slasher_heavy,itm_orc_slasher,itm_orc_axe,itm_mordor_orc_shield_b,itm_mordor_orc_shield_c,itm_mordor_orc_shield_a,],attr_orc_tier_2,wp_orc_tier_2,knows_common|knows_power_strike_2|knows_power_throw_1|knows_weapon_master_1|knows_shield_1|knows_athletics_1|knows_looting_1|knows_trainer_1|knows_tactics_1|knows_inventory_management_1|knows_wound_treatment_1|knows_prisoner_management_2|knows_leadership_1|knows_trade_1,orc_face7,orc_face8],
["i3_mordor_large_orc","Large_Orc_of_Mordor","Large_Orcs_of_Mordor",tf_orc| tfg_shield| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,[itm_orc_nosehelm_good,itm_orc_kettlehelm_bad, itm_orc_kettlehelm, itm_orc_morion_bad, itm_orc_morion, itm_orc_visorhelm,itm_m_orc_light_d,itm_m_orc_light_e,itm_m_orc_heavy_a,itm_m_orc_heavy_b,itm_orc_greaves,itm_orc_falchion,itm_orc_slasher_heavy,itm_orc_axe,itm_mordor_orc_shield_b,itm_mordor_orc_shield_c,],attr_orc_tier_3,wp_orc_tier_3,knows_common|knows_athletics_2|knows_power_strike_3|knows_power_throw_3,orc_face3,orc_face6],
["i4_mordor_fell_orc","Fell_Orc_of_Mordor","Fell_Orcs_of_Mordor",tf_orc| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,[itm_orc_visorhelm_good, itm_orc_buckethelm_bad, itm_orc_buckethelm, itm_orc_kettlehelm_good,itm_m_orc_heavy_b,itm_m_orc_heavy_c,itm_m_orc_heavy_d,itm_m_orc_heavy_e,itm_evil_gauntlets_a,itm_orc_greaves,itm_orc_club_c,itm_orc_falchion_heavy,itm_orc_two_handed_axe,itm_twohand_wood_club,itm_mordor_orc_shield_b,itm_mordor_orc_shield_c,itm_mordor_orc_shield_e,],attr_orc_tier_4,wp_orc_tier_4,knows_common|knows_athletics_2|knows_power_strike_4|knows_power_throw_4,orc_face7,orc_face4],
["c3_mordor_warg_rider","Warg_Rider_of_Gorgoroth","Warg_Riders_of_Gorgoroth",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_horse| tf_no_capture_alive,0,0,fac_mordor,[itm_orc_coif_bad, itm_orc_coif, itm_orc_nosehelm_bad, itm_orc_nosehelm,itm_orc_visorhelm_bad,itm_m_orc_light_a,itm_m_orc_light_b,itm_m_orc_light_c,itm_orc_throwing_arrow,itm_orc_throwing_arrow,itm_orc_falchion,itm_orc_sabre,itm_warg_1d,itm_warg_1b,itm_warg_1c,],attr_orc_tier_3,wp_orc_tier_3,knows_common|knows_horse_archery_2|knows_riding_4|knows_power_throw_3|knows_power_strike_4,orc_face5,orc_face8],
["c4_mordor_great_warg_rider","Great_Warg_Rider_of_Udun","Great_Warg_Riders_of_Udun",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_horse| tf_no_capture_alive,0,0,fac_mordor,[itm_orc_visorhelm, itm_orc_nosehelm,itm_m_orc_light_b,itm_m_orc_light_c,itm_m_orc_light_d,itm_m_orc_light_e,itm_evil_gauntlets_a,itm_orc_ragwrap,itm_orc_throwing_arrow,itm_orc_throwing_arrow,itm_orc_falchion,itm_orc_sabre,itm_wargarmored_1b, itm_wargarmored_1c,],attr_orc_tier_4,wp_orc_tier_4,knows_common|knows_riding_5|knows_horse_archery_3|knows_power_throw_4|knows_power_strike_4,orc_face7,orc_face8],
["i2_mordor_morgul_orc","Orc_of_Minas_Morgul","Orcs_of_Minas_Morgul",tf_orc| tfg_armor| tfg_boots|tfg_polearm| tf_no_capture_alive,0,0,fac_mordor,[itm_orc_kettlehelm_bad,itm_orc_morion_bad,itm_orc_visorhelm_bad,itm_m_orc_light_b,itm_m_orc_light_c,itm_m_orc_light_d,itm_m_orc_light_e,itm_orc_ragwrap,itm_orc_simple_spear,itm_orc_bill_bad,itm_wood_club,itm_orc_slasher,itm_orc_slasher,itm_mordor_orc_shield_c,itm_mordor_orc_shield_d,],attr_orc_tier_2,wp_orc_tier_2,knows_common|knows_athletics_2|knows_power_strike_3,orc_face5,orc_face4],
["i4_mordor_fell_morgul_orc","Fell_Orc_of_Minas_Morgul","Fell_Orcs_of_Minas_Morgul",tf_orc| tfg_armor| tfg_helm| tfg_boots|tfg_polearm| tf_no_capture_alive,0,0,fac_mordor,[itm_orc_kettlehelm_good, itm_orc_morion_good, itm_orc_buckethelm_good,itm_m_orc_heavy_b,itm_m_orc_heavy_c,itm_m_orc_heavy_d,itm_m_orc_heavy_e,itm_orc_ragwrap,itm_orc_bill_heavy, itm_orc_simple_spear_heavy,itm_orc_slasher,itm_orc_slasher,itm_mordor_uruk_shield_c,],attr_orc_tier_4,wp_orc_tier_4,knows_common|knows_athletics_2|knows_shield_1|knows_power_strike_4,orc_face5,orc_face4],

#Changed these two below to Guldur
["a3_guldur_large_orc_tracker","Large_Orc_Tracker_of_Dol_Guldur","Large_Orc_Trackers_of_Dol_Guldur",tf_orc| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_guldur,[itm_orc_coif, itm_orc_nosehelm_bad,itm_m_orc_light_b,itm_m_orc_light_c,itm_orc_ragwrap,itm_orc_bow,itm_orc_hook_arrow,itm_orc_club_d_bad,],attr_orc_tier_3,wp_orc_tier_3,knows_common|knows_riding_1|knows_athletics_5|knows_power_draw_3|knows_power_strike_2,orc_face9,orc_face4],
["a4_guldur_fell_orc_tracker","Fell_Orc_Tracker_of_Dol_Guldur","Fell_Orc_Trackers_of_Dol_Guldur",tf_orc| tfg_ranged| tfg_helm| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_guldur,[itm_orc_coif, itm_orc_coif_good, itm_orc_nosehelm_bad, itm_orc_nosehelm,itm_m_orc_light_c,itm_m_orc_light_d,itm_m_orc_light_e,itm_m_orc_light_c,itm_evil_gauntlets_a,itm_orc_furboots,itm_uruk_bow,itm_black_arrows_reward,itm_orc_club_d,],str_12| agi_11| int_7| cha_7|level(20),wp_orc_tier_5,knows_common|knows_riding_1|knows_athletics_7|knows_power_draw_4|knows_power_strike_3|knows_ironflesh_2,orc_face1,orc_face4],

["a2_mordor_orc_archer","Orc_Archer_of_Mordor","Orc_Archers_of_Mordor",tf_orc| tfg_ranged| tfg_armor| tf_no_capture_alive,0,0,fac_mordor,[itm_orc_coif_bad, itm_orc_nosehelm_bad,itm_m_orc_light_b,itm_m_orc_light_c,itm_m_orc_light_d,itm_m_orc_light_e,itm_orc_bow,itm_orc_hook_arrow,itm_wood_club,itm_orc_slasher,itm_orc_axe,],attr_orc_tier_2,wp_orc_tier_bow_2,knows_common|knows_power_throw_1|knows_power_draw_2|knows_weapon_master_1|knows_shield_1|knows_athletics_1|knows_looting_1|knows_trainer_1|knows_tactics_1|knows_inventory_management_1|knows_wound_treatment_1|knows_prisoner_management_2|knows_leadership_1|knows_trade_1,orc_face7,orc_face6],
["a3_mordor_large_orc_archer","Large_Orc_Archer_of_Mordor","Large_Orc_Archers_of_Mordor",tf_orc| tfg_ranged| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,[itm_orc_kettlehelm_bad, itm_orc_coif, itm_orc_nosehelm,itm_m_orc_light_b,itm_m_orc_light_c,itm_m_orc_light_d,itm_m_orc_light_e,itm_orc_ragwrap,itm_orc_bow,itm_orc_hook_arrow,itm_orc_slasher_heavy,itm_orc_falchion_bad,itm_orc_axe,],attr_orc_tier_3,wp_orc_tier_bow_3,knows_common|knows_athletics_2|knows_power_draw_3|knows_power_strike_2,orc_face9,orc_face4],
["a4_mordor_fell_orc_archer","Fell_Orc_Archer_of_Mordor","Fell_Orc_Archers_of_Mordor",tf_orc| tfg_ranged| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,[itm_orc_kettlehelm, itm_orc_coif_good, itm_orc_buckethelm_bad,itm_m_orc_light_d,itm_m_orc_light_e,itm_m_orc_heavy_a,itm_m_orc_heavy_b,itm_evil_gauntlets_a,itm_orc_greaves,itm_orc_bow,itm_orc_hook_arrow,itm_orc_slasher_heavy,itm_orc_falchion,],attr_orc_tier_4,wp_orc_tier_bow_4,knows_common|knows_athletics_4|knows_power_draw_4|knows_power_strike_2,orc_face7,orc_face6],

#Moria + tribal orc chief below
["c3_moria_wolf_rider","Wolf_Rider_of_Moria","Wolf_Riders_of_Moria",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_horse| tf_no_capture_alive,0,0,fac_moria,[itm_orc_nosehelm_bad,itm_moria_armor_a,itm_moria_armor_b,itm_orc_sabre,itm_orc_scimitar,itm_orc_falchion,itm_orc_simple_spear,itm_wood_club,itm_orc_throwing_arrow,itm_orc_shield_b,itm_orc_shield_a,itm_warg_1d,itm_warg_1b,itm_warg_1c,],attr_orc_tier_3,wp_orc_tier_2,knows_common|knows_riding_3|knows_power_throw_2|knows_power_strike_2|knows_horse_archery_2,orc_face5,orc_face2],
["c4_moria_warg_rider","Warg_Rider_of_Moria","Warg_Riders_of_Moria",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_horse| tf_no_capture_alive,0,0,fac_moria,[itm_orc_bughelm_bad, itm_orc_nosehelm, itm_orc_beakhelm_bad,itm_moria_armor_a,itm_moria_armor_b,itm_moria_armor_c,itm_orc_ragwrap,itm_orc_sabre,itm_orc_sabre,itm_orc_throwing_arrow,itm_orc_scimitar,itm_orc_simple_spear_heavy,itm_orc_skull_spear,itm_orc_shield_b,itm_orc_shield_a,itm_wargarmored_1b, itm_wargarmored_1c,],attr_orc_tier_4,wp_orc_tier_3,knows_common|knows_riding_3|knows_power_throw_3|knows_power_strike_4|knows_horse_archery_3,orc_face9,orc_face8],
["c5_moria_clan_rider","Bolg_Clan_Rider","Bolg_Clan_Riders",tf_orc| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_moria,[itm_orc_bughelm, itm_orc_bughelm_good, itm_orc_beakhelm,  itm_gundabad_helm_e,itm_moria_armor_c,itm_moria_armor_d,itm_orc_greaves,itm_orc_throwing_arrow,itm_orc_sabre,itm_orc_scimitar,itm_orc_simple_spear,itm_orc_skull_spear_heavy, itm_orc_simple_spear_heavy,itm_moria_orc_shield_c,itm_wargarmored_2b, itm_wargarmored_2c,],attr_orc_tier_5,wp_orc_tier_4,knows_common|knows_riding_4|knows_power_throw_4|knows_power_strike_4|knows_horse_archery_5,orc_face5,orc_face4],
["i1_moria_snaga","Snaga_of_Moria","Snagas_of_Moria",tf_orc| tf_no_capture_alive,0,0,fac_moria,[itm_orc_coif_bad, itm_orc_nosehelm_bad,itm_moria_armor_a,itm_moria_armor_b,itm_orc_falchion_bad,itm_orc_slasher,itm_orc_axe,itm_wood_club,itm_orc_shield_a],attr_orc_tier_1,wp_orc_tier_1,knows_common|knows_ironflesh_2|knows_power_strike_1|knows_athletics_2|knows_looting_2|knows_pathfinding_1|knows_spotting_1|knows_inventory_management_1|knows_surgery_1|knows_prisoner_management_1|knows_trade_1,orc_face4,orc_face9],
["i2_moria_goblin","Goblin_of_Moria","Goblins_of_Moria",tf_orc| tfg_armor| tf_no_capture_alive,0,0,fac_moria,[itm_orc_nosehelm, itm_orc_bughelm_bad, itm_orc_beakhelm_bad,itm_moria_armor_b,itm_moria_armor_c,itm_moria_armor_b,itm_orc_sabre_bad,itm_orc_falchion,itm_orc_scimitar_bad,itm_orc_simple_spear,itm_moria_orc_shield_b,itm_orc_shield_b,itm_orc_shield_a,],attr_orc_tier_2,wp_orc_tier_2,knows_common|knows_ironflesh_2|knows_power_strike_3|knows_athletics_3|knows_looting_2|knows_pathfinding_1|knows_spotting_1|knows_inventory_management_1|knows_surgery_1|knows_prisoner_management_1|knows_trade_1,orc_face9,orc_face2],
["i3_moria_large_goblin","Large_Goblin_of_Moria","Large_Goblins_of_Moria",tf_orc| tfg_shield| tfg_armor| tfg_helm| tf_no_capture_alive,0,0,fac_moria,[itm_orc_bughelm, itm_orc_beakhelm,itm_moria_armor_d,itm_moria_armor_c,itm_moria_armor_d,itm_orc_sabre,itm_orc_scimitar,itm_orc_simple_spear,itm_orc_bill,itm_orc_pick,itm_orc_throwing_axes,itm_moria_orc_shield_c,itm_moria_orc_shield_b,],attr_orc_tier_3,wp_orc_tier_3,knows_common|knows_ironflesh_3|knows_athletics_5|knows_power_throw_2|knows_power_strike_3,orc_face3,orc_face8],
["i4_moria_fell_goblin","Fell_Goblin_of_Moria","Fell_Goblins_of_Moria",tf_orc| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_moria,[itm_orc_bughelm_good, itm_orc_beakhelm_good,itm_moria_armor_e,itm_orc_greaves,itm_orc_sabre_heavy,itm_orc_scimitar_heavy,itm_orc_simple_spear_heavy,itm_orc_bill_heavy,itm_orc_pick,itm_orc_throwing_axes,itm_moria_orc_shield_b,itm_moria_orc_shield_c,],attr_orc_tier_4,wp_orc_tier_4,knows_common|knows_ironflesh_4|knows_athletics_6|knows_power_throw_3|knows_power_strike_4,orc_face1,orc_face6],
["a2_moria_goblin_archer","Goblin_Archer_of_Moria","Goblin_Archers_of_Moria",tf_orc| tfg_ranged| tfg_armor| tf_no_capture_alive,0,0,fac_moria,[itm_orc_bughelm_bad, itm_orc_beakhelm_bad,itm_moria_armor_b, itm_orc_bow,itm_orc_hook_arrow,itm_orc_slasher,itm_orc_falchion_bad,itm_orc_shield_a],attr_orc_tier_2,wp_orc_tier_bow_2,knows_common|knows_ironflesh_2|knows_power_strike_1|knows_power_draw_2|knows_athletics_3|knows_looting_2|knows_pathfinding_1|knows_spotting_1|knows_inventory_management_1|knows_surgery_1|knows_prisoner_management_1|knows_trade_1,orc_face9,orc_face6],
["a3_moria_large_goblin_archer","Large_Goblin_Archer_of_Moria","Large_Goblin_Archers_of_Moria",tf_orc| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_moria,[itm_orc_bughelm_bad, itm_orc_bughelm, itm_orc_beakhelm,itm_moria_armor_c,itm_moria_armor_b,itm_moria_armor_c, itm_evil_gauntlets_a,itm_orc_ragwrap,itm_orc_bow,itm_orc_hook_arrow,itm_orc_slasher_heavy,itm_orc_falchion,itm_moria_orc_shield_b,itm_orc_shield_b,itm_orc_shield_a,],attr_orc_tier_3,wp_orc_tier_bow_3,knows_common|knows_ironflesh_3|knows_athletics_5|knows_power_draw_3|knows_power_strike_2,orc_face5,orc_face6],
["a4_moria_fell_goblin_archer","Fell_Goblin_Archer_of_Moria","Fell_Goblin_Archers_of_Moria",tf_orc| tfg_ranged| tfg_armor| tfg_boots| tfg_helm| tf_no_capture_alive,0,0,fac_moria,[itm_orc_bughelm_good, itm_orc_beakhelm_good,itm_moria_armor_d,itm_moria_armor_c,itm_moria_armor_d, itm_evil_gauntlets_a,itm_orc_ragwrap,itm_uruk_bow,itm_orc_hook_arrow,itm_orc_slasher_heavy,itm_orc_falchion,itm_orc_pick,itm_moria_orc_shield_b,itm_moria_orc_shield_c,],attr_orc_tier_4,wp_orc_tier_bow_4,knows_common|knows_ironflesh_4|knows_athletics_7|knows_power_draw_4|knows_power_strike_3,orc_face5,orc_face6],

["moria_items","BUG","BUG",tf_hero|tf_orc,0,0,fac_moria,
   [itm_warg_1b,itm_warg_1c,itm_warg_1d,itm_gundabad_helm_a,itm_gundabad_helm_b,itm_gundabad_helm_c,itm_gundabad_helm_d,itm_moria_orc_shield_c,itm_orc_scimitar,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
#MT Gundabad #Gundabad
["i1_gunda_goblin","Gundabad_Goblin","Gundabad_Goblins",tf_orc| tf_no_capture_alive,0,0,fac_gundabad,[itm_gundabad_helm_a,itm_gundabad_armor_a,itm_orc_tribal_a,itm_wood_club,itm_orc_slasher,itm_orc_slasher,itm_orc_simple_spear,itm_orc_simple_spear,itm_bone_cudgel,itm_orc_bow,itm_orc_hook_arrow,],attr_orc_tier_1,wp_orc_tier_1,knows_common|knows_power_strike_1|knows_power_throw_1|knows_athletics_4|knows_riding_1|knows_horse_archery_1|knows_looting_2|knows_tracking_1|knows_pathfinding_1|knows_spotting_1|knows_persuasion_1,orc_face1,orc_face2],
["i2_gunda_orc","Gundabad_Orc","Gundabad_Orcs",tf_orc| tfg_armor| tf_no_capture_alive,0,0,fac_gundabad,[itm_gundabad_helm_a,itm_gundabad_helm_b,itm_gundabad_armor_b,itm_gundabad_armor_c,itm_orc_ragwrap,itm_orc_slasher,itm_orc_slasher,itm_wood_club,itm_orc_simple_spear,itm_orc_skull_spear,itm_orc_axe,itm_orc_falchion_bad,itm_orc_bow,itm_orc_hook_arrow,itm_orc_shield_a,itm_orc_shield_b,],attr_orc_tier_2,wp_orc_tier_2,knows_common|knows_power_strike_2|knows_power_throw_2|knows_power_draw_1|knows_athletics_5|knows_riding_1|knows_horse_archery_1|knows_looting_2|knows_tracking_1|knows_pathfinding_1|knows_spotting_1|knows_persuasion_1,orc_face7,orc_face6],
["i3_gunda_orc_fighter","Gundabad_Orc_Fighter","Gundabad_Orc_Fighters",tf_orc| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_gundabad,[itm_gundabad_helm_c,itm_gundabad_helm_b, itm_orc_coif,itm_gundabad_armor_d,itm_gundabad_armor_c, itm_evil_gauntlets_a,itm_orc_furboots,itm_orc_falchion_heavy,itm_orc_scimitar,itm_orc_sabre,itm_orc_axe,itm_orc_skull_spear,itm_orc_throwing_arrow,itm_orc_throwing_axes,itm_orc_throwing_axes,itm_orc_shield_b,itm_orc_shield_a,],attr_orc_tier_3,wp_orc_tier_3,knows_common|knows_athletics_7|knows_power_draw_2|knows_power_throw_2|knows_power_strike_3,orc_face5,orc_face6],
["i4_gunda_orc_warrior","Gundabad_Orc_Warrior","Gundabad_Orc_Warriors",tf_orc| tfg_shield| tfg_armor| tfg_helm|tfg_boots| tf_no_capture_alive,0,0,fac_gundabad,[itm_gundabad_helm_c,itm_gundabad_helm_b, itm_orc_coif,itm_gundabad_armor_d,itm_gundabad_armor_c, itm_evil_gauntlets_a,itm_orc_furboots,itm_orc_falchion_heavy,itm_orc_scimitar_heavy,itm_orc_sabre_heavy,itm_orc_skull_spear_heavy,itm_orc_javelin,itm_orc_throwing_arrow,itm_orc_throwing_axes,itm_orc_shield_b,itm_orc_shield_a,],attr_orc_tier_4,wp_orc_tier_4,knows_common|knows_athletics_8|knows_power_throw_3|knows_power_strike_4|knows_ironflesh_2|knows_shield_2,orc_face3,orc_face8],
["i4_gunda_orc_berserker","Gundabad_Orc_Berserker","Gundabad_Orc_Berserkers",tf_orc| tfg_armor|tfg_boots| tf_no_capture_alive,0,0,fac_gundabad,[itm_gundabad_helm_a,itm_gundabad_helm_b,itm_gundabad_helm_c,itm_gundabad_helm_d,itm_gundabad_armor_d,itm_gundabad_armor_e, itm_evil_gauntlets_a,itm_orc_furboots,itm_orc_two_handed_axe,itm_orc_battle_axe,itm_uruk_falchion_b_bad,itm_uruk_falchion_b_heavy, itm_orc_skull_spear_heavy, itm_orc_club_b,itm_twohand_wood_club,itm_orc_sledgehammer,],attr_orc_tier_5,wp_orc_tier_5,knows_common|knows_athletics_10|knows_power_throw_6|knows_power_strike_7|knows_ironflesh_7,orc_face3,orc_face8],
["ca4_gunda_skirmisher","Gundabad_Skirmisher","Gundabad_Skirmishers",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_boots| tfg_horse| tf_no_capture_alive,0,0,fac_gundabad,[itm_gundabad_helm_a,itm_gundabad_helm_b,itm_gundabad_armor_b,itm_gundabad_armor_c,itm_orc_furboots,itm_orc_ragwrap,itm_uruk_bow,itm_orc_hook_arrow,itm_orc_slasher,itm_orc_scimitar,itm_orc_falchion,itm_warg_1c,itm_warg_1d,itm_warg_1b,itm_warg_1d,],attr_orc_tier_4,wp_orc_tier_bow_4,knows_common|knows_athletics_6|knows_horse_archery_3|knows_riding_4|knows_power_draw_3|knows_power_throw_3|knows_power_strike_1,orc_face1,orc_face6],
["ca5_gunda_clan_skirmisher","Goblin_North_Clan_Skirmisher","Goblin_North_Clan_Skirmishers",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_boots| tfg_horse| tf_no_capture_alive,0,0,fac_gundabad,[itm_gundabad_helm_d,itm_gundabad_helm_e,itm_gundabad_armor_d, itm_evil_gauntlets_a,itm_orc_furboots,itm_uruk_bow,itm_orc_hook_arrow,itm_orc_scimitar,itm_warg_1d,itm_warg_1b,itm_warg_1d,],attr_orc_tier_5,wp_orc_tier_bow_5,knows_common|knows_athletics_7|knows_horse_archery_6|knows_riding_6|knows_power_draw_4|knows_power_throw_4|knows_power_strike_2,orc_face3,orc_face6],
["c3_gunda_goblin_rider","Gundabad_Goblin_Rider","Gundabad_Goblin_Riders",tf_orc| tf_mounted| tfg_armor| tfg_horse| tf_no_capture_alive,0,0,fac_gundabad,[itm_gundabad_helm_a,itm_gundabad_armor_b,itm_orc_ragwrap,itm_uruk_bow,itm_orc_hook_arrow,itm_wood_club,itm_twohand_wood_club,itm_warg_1d,itm_warg_1b,itm_warg_1c,],attr_orc_tier_3,wp_orc_tier_3,knows_common|knows_athletics_5|knows_riding_3|knows_horse_archery_3|knows_power_throw_2|knows_power_draw_2|knows_power_strike_1,orc_face9,orc_face8],
["c4_gunda_warg_rider","Gundabad_Warg_Rider","Gundabad_Warg_Riders",tf_orc| tf_mounted| tfg_armor| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_gundabad,[itm_gundabad_helm_b,itm_gundabad_helm_c,itm_gundabad_armor_b,itm_gundabad_armor_b,itm_orc_furboots,itm_orc_ragwrap,itm_orc_scimitar_heavy,itm_orc_falchion_heavy,itm_orc_sabre,itm_twohand_wood_club,itm_orc_club_b,itm_orc_shield_b,itm_orc_shield_b,itm_wargarmored_2b, itm_wargarmored_2c,],attr_orc_tier_4,wp_orc_tier_4,knows_common|knows_athletics_6|knows_riding_4|knows_power_strike_4|knows_ironflesh_4,orc_face1,orc_face6],
["c5_gunda_clan_rider","Goblin_North_Clan_Rider","Goblin_North_Clan_Riders",tf_orc| tf_mounted| tfg_armor| tfg_shield| tfg_helm| tfg_horse| tfg_boots|tfg_gloves| tf_no_capture_alive,0,0,fac_gundabad,[itm_gundabad_helm_e,itm_gundabad_helm_d,itm_gundabad_armor_d,itm_gundabad_armor_e, itm_evil_gauntlets_a,itm_orc_furboots,itm_orc_sabre_heavy,itm_orc_scimitar_heavy,itm_orc_skull_spear,itm_orc_club_b,itm_orc_club_b_heavy,itm_uruk_falchion_b_bad,itm_orc_shield_b,itm_orc_shield_b,itm_wargarmored_3a,],attr_orc_tier_5,wp_orc_tier_5,knows_common|knows_athletics_7|knows_riding_6|knows_power_strike_5|knows_ironflesh_6,orc_face3,orc_face6],

["gundabad_items","BUG","_",tf_hero|tf_orc| tfg_shield| tfg_armor| tfg_helm|tfg_boots| tf_no_capture_alive,0,0,fac_gundabad,
   [itm_orc_javelin,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,itm_leather_gloves,itm_warg_1b,itm_warg_1c,itm_warg_1d,itm_angmar_shield,itm_orc_bill,itm_orc_scimitar,itm_orc_slasher,itm_orc_axe,itm_orc_two_handed_axe,itm_orc_greaves,],
      attr_orc_tier_5,wp_orc_tier_4,knows_common|knows_athletics_8|knows_power_throw_6|knows_power_strike_5|knows_ironflesh_4|knows_shield_6,orc_face3,orc_face8],

#move this one here before we swap it iwth gundabad_items above eventually. (Savegame compatibility.)	  
["i5_gunda_orc_champion","Gundabad_Orc_Champion","Gundabad_Orc_Champions",tf_orc| tfg_shield| tfg_armor| tfg_helm|tfg_boots| tf_no_capture_alive,0,0,fac_gundabad,[itm_gundabad_helm_c,itm_gundabad_helm_d, itm_gundabad_armor_d,itm_gundabad_armor_e, itm_evil_gauntlets_a,itm_orc_furboots,itm_orc_scimitar_heavy,itm_orc_sabre_heavy,itm_orc_club_c,itm_orc_club_b_heavy,itm_orc_javelin,  itm_orc_throwing_axes,itm_orc_shield_b,itm_orc_shield_c,],attr_orc_tier_5,wp_orc_tier_4,knows_common|knows_athletics_8|knows_power_throw_6|knows_power_strike_5|knows_ironflesh_4|knows_shield_6,orc_face3,orc_face8],

#moved all tribal orcs to end of file, March 2020. Keep these ones a bit for savegame compatibility	  
["mountain_goblin2","Mountain_Goblin","Mountain_Goblins",tf_orc| tf_no_capture_alive,0,0,fac_tribal_orcs,
   [itm_orc_tribal_a,itm_orc_tribal_b,itm_orc_tribal_c,itm_orc_tribal_c,itm_orc_shield_a,itm_orc_shield_b,itm_orc_shield_c,itm_orc_ragwrap,itm_bone_cudgel_heavy,itm_twohand_wood_club,itm_bone_cudgel,itm_wood_club,itm_orc_simple_spear,],
      attr_orc_tier_2,wp_orc_tier_2,knows_athletics_3|knows_power_strike_2,orc_face3,orc_face4],
["tribal_orc2","Tribal_Orc","Tribal_Orcs",tf_orc| tf_no_capture_alive,0,0,fac_tribal_orcs,
   [itm_orc_tribal_a,itm_orc_tribal_b,itm_orc_tribal_c,itm_orc_tribal_c,itm_bone_cudgel_heavy,itm_bone_cudgel,itm_twohand_wood_club,itm_wood_club,itm_orc_simple_spear,itm_wood_club,itm_orc_simple_spear,itm_orc_sledgehammer,],
      attr_orc_tier_1,wp_orc_tier_1,knows_athletics_3,orc_face1,orc_face2],

["i5_gunda_orc_champion2","Gundabad_Orc_Champion","Gundabad_Orc_Champions",tf_orc| tfg_shield| tfg_armor| tfg_helm|tfg_boots| tf_no_capture_alive,0,0,fac_gundabad,[itm_gundabad_helm_c,itm_gundabad_helm_d, itm_gundabad_armor_d,itm_gundabad_armor_e, itm_evil_gauntlets_a,itm_orc_furboots,itm_orc_scimitar,itm_orc_sabre,itm_orc_club_c,itm_orc_javelin,  itm_orc_throwing_axes,itm_orc_shield_b,itm_orc_shield_c,],attr_orc_tier_5,wp_orc_tier_4,knows_common|knows_athletics_8|knows_power_throw_6|knows_power_strike_5|knows_ironflesh_4|knows_shield_6,orc_face3,orc_face8],

#Numenorean
["i2_mordor_num_renegade","Black_Numenorean_Renegade","Black_Numenorean_Renegades",tf_evil_man| tfg_armor| tfg_boots,0,0,fac_mordor,[itm_evil_light_armor, itm_evil_gauntlets_a,itm_uruk_ragwrap,itm_orc_simple_spear_heavy,itm_uruk_falchion_a,itm_orc_sabre,],attr_tier_2,wp_tier_2,knows_common|knows_power_strike_1|knows_power_throw_1|knows_weapon_master_1|knows_athletics_1|knows_riding_1|knows_trainer_2|knows_tactics_1|knows_spotting_1|knows_surgery_1|knows_first_aid_1|knows_leadership_2,mordor_man1,mordor_man2],
["i3_mordor_num_warrior","Black_Numenorean_Warrior","Black_Numenorean_Warriors",tf_evil_man| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,[itm_hood_black,itm_orc_coif,itm_evil_light_armor,itm_m_armor_a, itm_evil_gauntlets_a,itm_uruk_ragwrap,itm_mordor_sword,itm_uruk_pike_b,itm_mordor_orc_shield_b,],attr_tier_3,wp_tier_3,knows_common|knows_ironflesh_2|knows_power_strike_2|knows_power_throw_1|knows_weapon_master_1|knows_athletics_1|knows_riding_2|knows_trainer_2|knows_tactics_1|knows_spotting_1|knows_surgery_1|knows_first_aid_1|knows_leadership_2,mordor_man1,mordor_man2],
["i4_mordor_num_vet_warrior","Black_Numenorean_Veteran_Warrior","Black_Numenorean_Veteran_Warriors",tf_evil_man| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,[itm_mordor_helm,itm_m_armor_a,itm_m_armor_b, itm_evil_gauntlets_a,itm_uruk_greaves,itm_mordor_longsword,itm_mordor_sword,itm_mordor_man_shield_b,],attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_shield_3|knows_power_strike_4|knows_ironflesh_4,mordor_man1,mordor_man2],
["i5_mordor_num_champion","Black_Numenorean_Champion","Black_Numenorean_Champions",tf_evil_man| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,[itm_black_num_helm,itm_black_num_armor, itm_evil_gauntlets_b,itm_uruk_greaves,itm_mordor_man_shield_a,itm_mordor_longsword,itm_orc_club_d],attr_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_shield_4|knows_power_strike_5|knows_ironflesh_5,mordor_man1,mordor_man2],
["i5_mordor_num_assassin","Black_Numenorean_Assassin","Black_Numenorean_Assassins",tf_evil_man| tfg_gloves| tfg_armor| tfg_boots,0,0,fac_mordor,[itm_mordor_helm,itm_hood_black,itm_hood_black,itm_m_armor_a,itm_m_armor_b,itm_black_num_armor, itm_evil_gauntlets_a,itm_uruk_chain_greaves,itm_corsair_throwing_dagger, itm_corsair_throwing_dagger, itm_corsair_throwing_dagger,itm_mordor_sword,itm_mordor_longsword, itm_umb_shield_a,],attr_tier_5,wp_tier_5,knows_common|knows_athletics_7|knows_shield_2|knows_power_strike_6|knows_power_throw_8|knows_ironflesh_7,mordor_man1,mordor_man2],
["c4_mordor_num_horseman","Black_Numenorean_Horseman","Black_Numenorean_Horsemen",tf_evil_man| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_mordor,[itm_mordor_helm,itm_m_armor_a,itm_m_armor_b, itm_evil_gauntlets_a,itm_uruk_chain_greaves,itm_mordor_longsword,itm_orc_simple_spear_heavy,itm_mordor_man_shield_b,itm_mordor_warhorse,],attr_tier_4,wp_tier_4,knows_common|knows_riding_4|knows_athletics_3|knows_shield_3|knows_power_strike_4|knows_ironflesh_4,mordor_man1,mordor_man2],
["c5_mordor_num_knight","Black_Numenorean_Horsemaster","Black_Numenorean_Horsemasters",tf_evil_man| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_mordor,[itm_black_num_helm,itm_black_num_armor, itm_evil_gauntlets_b, itm_uruk_greaves,itm_mordor_longsword,itm_orc_simple_spear_heavy, itm_uruk_pike_b,itm_mordor_man_shield_a,itm_mordor_warhorse,],attr_tier_5,wp_tier_5,knows_common|knows_riding_5|knows_athletics_3|knows_shield_4|knows_power_strike_5|knows_ironflesh_5,mordor_man1,mordor_man2],

#Captains and lieutenants of all factions
["noldorin_commander","Noldorin_Commander","Noldorin_Commanders",tf_lorien| tfg_ranged| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_lorien,
   [itm_lorien_bow,itm_elven_arrows,itm_lorien_armor_c,itm_lorien_helm_b,itm_lorien_shield_b,itm_lorien_boots,itm_lorien_sword_a,itm_lorien_warhorse,],
      attr_elf_tier_6,wp_elf_tier_6,knows_inventory_management_1|knows_power_draw_6|knows_tactics_6|knows_tracking_1|knows_horse_archery_6|knows_riding_5|knows_athletics_6|knows_power_strike_6|knows_ironflesh_6,lorien_elf_face_1,lorien_elf_face_2],
["elf_captain_of_lothlorien","Elf_Captain_of_Lothlorien","Elf_Captains_of_Lothlorien",tf_lorien| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_lorien,
   [itm_lorien_bow,itm_elven_arrows,itm_lorien_armor_c,itm_lorien_helm_b,itm_lorien_shield_b,itm_lorien_boots,itm_lorien_sword_a,itm_lorien_warhorse,],
      attr_elf_tier_6,wp_elf_tier_6,knows_inventory_management_1|knows_power_draw_6|knows_tactics_4|knows_tracking_1|knows_horse_archery_5|knows_riding_5|knows_athletics_5|knows_power_strike_5|knows_ironflesh_5,lorien_elf_face_1,lorien_elf_face_2],
["lothlorien_lieutenant","Lothlorien_Lieutenant","Lothlorien_Lieutenants",tf_lorien| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_lorien,
   [itm_lorien_bow,itm_elven_arrows,itm_lorien_armor_c,itm_lorien_helm_b,itm_lorien_shield_b,itm_lorien_boots,itm_lorien_sword_a,],
      attr_elf_tier_6,wp_elf_tier_6,knows_inventory_management_1|knows_power_draw_6|knows_tactics_3|knows_tracking_1|knows_riding_3|knows_athletics_4|knows_power_strike_4|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["elf_captain_of_mirkwood","Elf_Captain_of_Greenwood","Elf_Captains_of_Greenwood",tf_woodelf| tfg_ranged| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_woodelf,
   [itm_elven_arrows,itm_elven_bow,itm_mirkwood_heavy_scale,itm_mirkwood_helm_b,itm_mirkwood_spear_shield_c,itm_mirkwood_boots,itm_mirkwood_axe],
      attr_elf_tier_6,wp_elf_tier_6,knows_riding_4|knows_athletics_5|knows_power_draw_7|knows_power_strike_5|knows_ironflesh_5,mirkwood_elf_face_1,mirkwood_elf_face_2],
["mirkwood_lieutenant","Greenwood_Lieutenant","Greenwood_Lieutenants",tf_woodelf| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_woodelf,
   [itm_elven_bow,itm_elven_arrows,itm_mirkwood_heavy_scale,itm_mirkwood_helm_b,itm_mirkwood_spear_shield_c,itm_mirkwood_boots,itm_mirkwood_axe,],
      attr_elf_tier_6,wp_elf_tier_6,knows_riding_3|knows_athletics_4|knows_power_draw_6|knows_power_strike_4|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["elf_captain_of_rivendell","Elf_Captain_of_Rivendell","Elf_Captains_of_Rivendell",tf_imladris| tfg_ranged| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_imladris,
   [itm_riv_boots,itm_riv_armor_leader,itm_riv_helm_a,itm_riv_shield_b,itm_riv_warhorse,],
      attr_elf_tier_6,wp_elf_tier_6,knows_riding_5|knows_athletics_5|knows_power_strike_5|knows_power_draw_6|knows_ironflesh_5,rivendell_elf_face_1,rivendell_elf_face_2],
["rivendell_lieutenant","Rivendell_Lieutenant","Rivendell_Lieutenants",tf_imladris| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_imladris,
   [itm_riv_boots,itm_riv_armor_leader,],
      attr_elf_tier_6,wp_elf_tier_6,knows_riding_3|knows_athletics_4|knows_power_draw_5|knows_power_strike_4|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["lieutenant_of_rohan","Lieutenant_of_Rohan","Lieutenants_of_Rohan",tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots |tfg_polearm,0,0,fac_rohan,
   [itm_rohan_surcoat,itm_rohan_inf_helmet_b_lordly,itm_rohan_shield_g,itm_mail_mittens,itm_leather_boots,itm_rohan_inf_sword,itm_rohirrim_courser,itm_rohirrim_hunter,itm_rohan_lance_banner_sun,itm_rohan_lance_banner_horse,],
      attr_tier_6,wp_tier_6,knows_common|knows_tactics_2|knows_riding_3|knows_athletics_2|knows_shield_1|knows_power_strike_4,rohan_face_middle_1,rohan_face_older_2],
["captain_of_rohan","Captain_of_Rohan","Captains_of_Rohan",tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohirrim_long_hafted_axe,itm_rohan_surcoat,itm_rohan_inf_helmet_b_lordly,itm_rohan_shield_g,itm_mail_mittens,itm_rohirrim_war_greaves,itm_rohan_inf_sword,itm_rohan_warhorse,itm_rohan_lance_banner_sun,itm_rohan_lance_banner_horse,],
      attr_tier_6,wp_tier_6,knows_common|knows_tactics_3|knows_riding_5|knows_athletics_3|knows_shield_2|knows_power_strike_5|knows_ironflesh_6,rohan_face_middle_1,rohan_face_older_2],
["high_captain_of_rohan","High_Captain_of_Rohan","High_Captains_of_Rohan",tf_rohan| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohirrim_long_hafted_axe,itm_rohan_surcoat,itm_rohan_inf_helmet_b_lordly,itm_rohan_shield_g,itm_mail_mittens,itm_rohirrim_war_greaves,itm_rohan_inf_sword,itm_rohan_warhorse,itm_rohan_lance_banner_sun,itm_rohan_lance_banner_horse,],
      attr_tier_6,wp_tier_6,knows_common|knows_tactics_4|knows_riding_7|knows_athletics_3|knows_shield_4|knows_power_strike_7|knows_ironflesh_7,rohan_face_middle_1,rohan_face_older_2],
["lieutenant_of_isengard","Lieutenant_of_Isengard","Lieutenants_of_Isengard",tf_urukhai| tfg_gloves| tfg_armor| tfg_helm| tfg_boots,0,0,fac_isengard,
   [itm_isen_uruk_helm_d,itm_isen_uruk_heavy_c,itm_leather_gloves,itm_uruk_greaves,itm_isen_uruk_shield_b,itm_isengard_sword,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_3|knows_power_strike_2,uruk_hai_face1,uruk_hai_face2],
["captain_of_isengard","Captain_of_Isengard","Captains_of_Isengard",tf_urukhai| tfg_gloves| tfg_armor| tfg_helm| tfg_boots,0,0,fac_isengard,
   [itm_isen_uruk_helm_d,itm_isen_uruk_heavy_c,itm_evil_gauntlets_b,itm_uruk_greaves,itm_isen_uruk_shield_b,itm_isengard_sword,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_4|knows_shield_3|knows_power_strike_3|knows_ironflesh_3,uruk_hai_face1,uruk_hai_face2],
["high_captain_of_isengard","High_Captain_of_Isengard","High_Captains_of_Isengard",tf_urukhai| tfg_gloves| tfg_armor| tfg_helm| tfg_boots,0,0,fac_isengard,
   [itm_isen_uruk_helm_d,itm_isen_uruk_heavy_c,itm_evil_gauntlets_a,itm_uruk_greaves,itm_isen_uruk_shield_b,itm_isengard_sword,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_5|knows_shield_4|knows_power_strike_5|knows_ironflesh_3,uruk_hai_face1,uruk_hai_face2],
["lieutenant_of_mordor","Lieutenant_of_Mordor","Lieutenants_of_Mordor",tf_evil_man| tf_mounted| tfg_armor| tfg_horse| tfg_boots,0,0,fac_mordor,
   [itm_mordor_cap_helm,itm_m_cap_armor,itm_leather_gloves,itm_uruk_greaves,itm_mordor_man_shield_a,itm_mordor_longsword,itm_mordor_warhorse2,],
      attr_tier_6,wp_tier_6,knows_common|knows_tactics_1|knows_athletics_2|knows_shield_1|knows_power_strike_4,mordor_man1,mordor_man2],
["captain_of_mordor","Captain_of_Mordor","Captains_of_Mordor",tf_evil_man| tf_mounted| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_mordor,
   [itm_mordor_cap_helm,itm_m_cap_armor,itm_evil_gauntlets_b,itm_uruk_greaves,itm_mordor_man_shield_a,itm_mordor_longsword,itm_mordor_warhorse2,],
      attr_tier_6,wp_tier_6,knows_common|knows_tactics_3|knows_riding_2|knows_athletics_3|knows_shield_3|knows_power_strike_4|knows_ironflesh_1,mordor_man1,mordor_man2],
["high_captain_of_mordor","High_Captain_of_Mordor","High_Captains_of_Mordor",tf_evil_man| tf_mounted| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_mordor,
   [itm_mordor_cap_helm,itm_m_cap_armor,itm_evil_gauntlets_a,itm_uruk_greaves,itm_mordor_man_shield_a,itm_mordor_longsword,itm_mordor_warhorse2,],
      attr_tier_6,wp_tier_6,knows_common|knows_tactics_4|knows_riding_6|knows_athletics_3|knows_shield_3|knows_power_strike_5|knows_ironflesh_7,mordor_man1,mordor_man2],
["easterling_chieftain","Variag_Chieftain","Variag_Chieftains",tf_evil_man| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_khand,
   [itm_khand_noble_lam,itm_splinted_greaves_good,itm_variag_kataphrakt,itm_mail_mittens,itm_khand_tulwar,itm_khand_2h_tulwar,itm_easterling_round_horseman,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_4|knows_athletics_3|knows_shield_2|knows_power_strike_4|knows_ironflesh_5,khand_man1,khand_man2],
["easterling_lieutenant","Variag_War_Priest","Variag_War_Priests",tf_evil_man| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,
   [itm_khand_noble_lam,itm_splinted_greaves_good,itm_mail_mittens,itm_khand_rammace,itm_easterling_round_horseman,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_3|knows_athletics_2|knows_power_strike_3|knows_ironflesh_3,khand_man1,khand_man2],
["harad_chieftain","Harad_Chieftain","Harad_Chieftains",tf_harad| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_horse| tfg_helm| tfg_boots,0,0,fac_harad,
   [itm_harad_leather_greaves,itm_harad_heavy,itm_harad_dragon_helm,itm_harad_khopesh,itm_harad_long_shield_c,itm_harad_warhorse,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_4|knows_athletics_3|knows_shield_3|knows_power_strike_4|knows_ironflesh_4,haradrim_face_1,haradrim_face_2],
["harad_lieutenant","Harad_Lieutenant","Harad_Lieutenants",tf_harad| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_horse| tfg_helm| tfg_boots,0,0,fac_harad,
   [itm_harad_leather_greaves,itm_harad_heavy,itm_harad_dragon_helm,itm_harad_khopesh,itm_harad_long_shield_c,itm_harad_warhorse,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_3|knows_athletics_2|knows_power_strike_3|knows_ironflesh_3,haradrim_face_1,haradrim_face_2],
["black_numenorean_captain","Black_Numenorean_Captain","Black_Numenorean_Captains",tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_umbar,
   [itm_uruk_chain_greaves,itm_m_cap_armor,itm_evil_gauntlets_a,itm_witchking_helmet,itm_mordor_sword,itm_harad_warhorse,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_5|knows_athletics_3|knows_shield_2|knows_power_strike_5|knows_ironflesh_5,bandit_face1,bandit_face2],
["black_numenorean_lieutenant","Black_Numenorean_Lieutenant","Black_Numenorean_Lieutenants",tf_mounted| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_umbar,
   [itm_umb_armor_c,itm_umb_helm_a,itm_evil_gauntlets_a,itm_harad_leather_greaves,itm_umb_shield_c,itm_umb_shield_d,itm_umbar_cutlass,itm_harad_horse,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_5|knows_athletics_2|knows_shield_3|knows_power_strike_4|knows_ironflesh_3,bandit_face1,bandit_face2],
["a5_dun_night_wolf","Dunnish_Night_Wolf","Dunnish_Night_Wolfs",tf_dunland| tf_randomize_face| tfg_shield| tfg_armor| tfg_boots| tfg_ranged,0,0,fac_dunland,[itm_dun_helm_a,itm_dunland_armor_h,itm_evil_gauntlets_b,itm_dunland_wolfboots,itm_dunnish_axe,itm_dunnish_war_axe,itm_dunland_javelin,itm_dunland_javelin,itm_dunland_javelin,itm_dunland_javelin,itm_dunland_javelin,itm_dun_shield_a,],attr_evil_tier_5,wp_tier_5,knows_common|knows_athletics_7|knows_shield_3|knows_power_strike_3|knows_ironflesh_2|knows_power_throw_7,dunland_face1,dunland_face2],
["dunnish_lieutenant","Dunnish_Hetman","Dunnish_Hetmen",tf_dunland| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dunland,
   [itm_dunland_wolfboots,itm_dunland_armor_e,itm_dun_berserker,itm_dun_helm_c,itm_dun_shield_b,itm_evil_gauntlets_a,],
      attr_tier_6,wp_tier_6,knows_common|knows_athletics_2|knows_shield_1|knows_power_strike_3|knows_ironflesh_3,dunland_face1,dunland_face2],
["goblin_chieftain","Goblin_Chieftain","Goblin_Chieftains",tf_orc| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_orc_sabre,itm_moria_orc_shield_a,itm_moria_orc_shield_b,itm_leather_gloves,itm_isen_orc_mail_a,itm_orc_coif,itm_orc_coif,itm_orc_ragwrap,itm_wargarmored_1b,],
      attr_orc_tier_6,wp_orc_tier_6,knows_riding_4|knows_athletics_4|knows_power_draw_1|knows_power_throw_3|knows_power_strike_5|knows_ironflesh_5,orc_face5,orc_face8],
 
["captain_of_gondor","Captain_of_Gondor","Captains_of_Gondor",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gon_leader_surcoat_cloak,itm_gondor_leader_helm,itm_mail_mittens,itm_gondor_heavy_greaves,itm_gondor_shield_e,itm_gondor_citadel_sword,itm_gondor_warhorse,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_1|knows_athletics_4|knows_shield_3|knows_power_strike_5|knows_ironflesh_6,gondor_face1,gondor_face2],
	  
["end_leaders","bug","bug",0,0,0,fac_gondor,   [],      0,0,0,0], #808 range call, not used anymore
#END# Captains and lieutenants of all factions
#Agents begin
["nobleman","Nobleman","Noblemen",tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_2,wp_tier_2,knows_common|knows_riding_5|knows_ironflesh_3,0x110000000003395063803a],
["gondor_agent","Gondor_Agent","Gondor_Agents",tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common|knows_riding_5|knows_ironflesh_3,gondor_face1,gondor_face2],
["rohan_agent","Rohan_Agent","Rohan_Agents",tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common|knows_riding_5|knows_ironflesh_3,rohan_face_middle_1,rohan_face_older_2],
["mordor_agent","Mordor_Agent","Mordor_Agents",tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_mordor,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common|knows_riding_5|knows_ironflesh_3,gondor_face1,gondor_face2],
["isengard_agent","Isengard_Agent","Isengard_Agents",tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_isengard,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common|knows_riding_5|knows_ironflesh_3,evil_man_face1,evil_man_face2],
#Agents end

["looter","Looter","Looters",0,0,0,fac_outlaws,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,bandit_face1,bandit_face2],
["bandit","Bandit","Bandits",tfg_armor,0,0,fac_outlaws,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_2,wp_tier_2,knows_common|knows_power_draw_1,bandit_face1,bandit_face2],
["brigand","Brigand","Brigands",tfg_boots| tfg_armor| tfg_horse,0,0,fac_outlaws,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_2,wp_tier_2,knows_common|knows_power_draw_3,bandit_face1,bandit_face2],
["mountain_bandit","Mountain_Bandit","Mountain_Bandits",tfg_armor| tfg_boots,0,0,fac_outlaws,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_2,wp_tier_2,knows_common|knows_power_draw_2,rhodok_face_young_1,rhodok_face_old_2],
["forest_bandit","Forest_Bandit","Forest_Bandits",tfg_armor| tfg_ranged| tfg_boots,0,0,fac_outlaws,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_2,wp_tier_2,knows_common|knows_power_draw_3,swadian_face_young_1,swadian_face_old_2],
["sea_raider","Sea_Raider","Sea_Raiders",tfg_boots| tfg_armor| tfg_shield,0,0,fac_outlaws,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_2,wp_tier_2,knows_ironflesh_2|knows_power_strike_2|knows_power_draw_3|knows_power_throw_2|knows_riding_1|knows_athletics_2,nord_face_young_1,nord_face_old_2],
["steppe_bandit","Steppe_Bandit","Steppe_Bandits",tfg_boots| tfg_armor| tfg_horse| tfg_ranged| tf_mounted,0,0,fac_outlaws,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_2,wp_tier_2,knows_riding_4|knows_horse_archery_3|knows_power_draw_3,khergit_face_young_1,khergit_face_old_2],
["manhunter","Manhunter","Manhunters",tfg_armor,0,0,fac_manhunters,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_2,wp_tier_2,knows_common,bandit_face1,bandit_face2],
 
["kidnapped_girl","Kidnapped_Girl","Kidnapped_Girls",tf_hero| tf_female| tf_randomize_face| tf_unmoveable_in_party_window,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common|knows_riding_2,woman_face_1,woman_face_2],
["refugee","Refugee","Refugees",tf_female| tfg_armor,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,refugee_face1,refugee_face2],
["peasant_woman","Peasant_Woman","Peasant_Women",tf_female| tf_randomize_face| tfg_armor|tfg_boots,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots, itm_practice_staff],
      attr_tier_1,wp_tier_1,knows_common,refugee_face1,refugee_face2],
["caravan_master","Caravan_Master","Caravan_Masters",tf_mounted| tfg_armor| tfg_horse| tfg_boots,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_2,wp_tier_2,knows_common|knows_riding_4|knows_ironflesh_3,merchant_face_1,merchant_face_2],
["caravan_guard","Caravan_Guard","Caravan_Guards",tf_mounted| tfg_armor| tfg_horse| tfg_boots,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_2,wp_tier_2,knows_common|knows_riding_2|knows_shield_1|knows_power_strike_2|knows_ironflesh_1,bandit_face1,bandit_face2],

# Messengers of different races for quests (non-heroes: can be killed or captured on purpose)
# TODO: Maybe make a messenger for each different faction. (CppCoder)

["messenger_man", "Messenger", "Messengers", tf_randomize_face| tf_unmoveable_in_party_window|tfg_armor|tfg_boots,0,0,fac_commoners,
   [itm_gon_ranger_skirt,itm_gondor_light_greaves,],
      attr_tier_1,wp_tier_1,knows_common|knows_riding_2,man_face_young_1,man_face_old_2],

["messenger_elf", "Messenger", "Messengers", tf_lorien| tf_randomize_face| tf_unmoveable_in_party_window|tfg_armor|tfg_boots,0,0,fac_commoners,
   [itm_lorien_armor_a,itm_lorien_boots,],
      attr_elf_tier_1,wp_elf_tier_1,knows_common|knows_riding_2,lorien_elf_face_1,lorien_elf_face_2],

["messenger_dwarf", "Messenger", "Messengers", tf_dwarf| tf_randomize_face| tf_unmoveable_in_party_window|tfg_armor|tfg_boots,0,0,fac_commoners,
   [itm_dwarf_pad_boots,itm_leather_dwarf_armor,],
      attr_dwarf_tier_1,wp_dwarf_tier_1,knows_common_dwarf|knows_riding_2,dwarf_face_2,dwarf_face_3],

["messenger_orc", "Messenger", "Messengers", tf_orc| tf_randomize_face| tf_unmoveable_in_party_window|tfg_armor|tfg_boots,0,0,fac_commoners,
   [itm_moria_armor_a,],
      attr_orc_tier_1,wp_orc_tier_1,knows_common|knows_riding_2,orc_face3,orc_face8],

# Added to fix evil factions getting gondor messengers.
["messenger_evil_man", "Messenger", "Messengers", tf_evil_man|tf_randomize_face|tf_unmoveable_in_party_window|tfg_armor|tfg_boots,0,0,fac_commoners,
   [itm_khand_foot_lam,itm_splinted_greaves_good,],
      attr_tier_1,wp_tier_1,knows_common|knows_riding_2,khand_man1,khand_man2],

#This troop is the troop marked as soldiers_end
["town_walker_1","Townsman","Townsmen",tf_gondor| tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,man_face_young_1,man_face_old_2],
["town_walker_2","Townswoman","Townswomen",tf_female| tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,woman_face_1,woman_face_2],
["village_walker_1","Villager","Villagers",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,man_face_younger_1,man_face_older_2],
["village_walker_2","Villager","Villagers",tf_female| tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,woman_face_1,woman_face_2],
["spy_walker_1","Townsman","Townsmen",tfg_boots| tfg_armor| tfg_helm,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,man_face_middle_1,man_face_old_2],
["spy_walker_2","Townswoman","Townswomen",tf_female| tfg_boots| tfg_armor| tfg_helm,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,woman_face_1,woman_face_2],
# Ryan END
 
 
 ] + (is_a_wb_troop==1 and [
#TLD walkers - WB
["walker_man_gondor_black","Townsman","_",tf_gondor| tfg_boots| tfg_armor,0,0,fac_gondor,
   [itm_peasant_man_a_wb, itm_white_tunic_c_wb, itm_white_tunic_a_wb, itm_black_tunic_wb, 
   itm_leather_boots_bad, itm_corsair_boots, itm_rohan_shoes_bad],
      attr_tier_1,wp_tier_1,knows_common,man_face_young_1,man_face_old_2],
# Minas Tirith, Pelargir, Dol Amroth
["walker_man_gondor_white","Townsman","_",tf_gondor| tfg_boots| tfg_armor,0,0,fac_gondor,
   [itm_corsair_boots, itm_rohan_shoes_good,
   itm_gondor_fine_outfit_dress, itm_denethor_robe, itm_white_tunic_c_wb, itm_white_tunic_a_wb, itm_black_tunic_wb, itm_nobleman_outfit_b_new_wb, itm_tabard_b_wb, ],
      attr_tier_5,wp_tier_1,knows_common,man_face_young_1,man_face_old_2],
# Dol Amroth, Lossarnach
["walker_man_gondor_blue","Townsman","_",tf_gondor| tfg_boots| tfg_armor,0,0,fac_gondor,
   [itm_hood_black_bad,itm_hood_grey_bad,
   itm_peasant_man_a_wb, itm_white_tunic_c_wb, itm_white_tunic_a_wb, itm_black_tunic_wb, 
   itm_leather_boots_dark_bad, itm_rohan_shoes_bad],
      attr_tier_1,wp_tier_1,knows_common,man_face_young_1,man_face_old_2],
# Linhir, Edhellond, Lossarnach, Tarnost, Erech, Pinnath, Calembel
["walker_man_gondor_green","Townsman","_",tf_gondor| tfg_boots| tfg_armor,0,0,fac_gondor,
   [itm_hood_green_bad, itm_hood_black, itm_hood_grey, itm_lossarnach_cloth_cap, 
   itm_peasant_man_a_wb, itm_black_tunic_wb, itm_white_tunic_c_wb, itm_leather_jerkin_wb, itm_lossarnach_shirt,itm_sar_robe_b_wb,
   itm_leather_boots_bad, itm_corsair_boots, itm_rohan_shoes, ],
      attr_tier_1,wp_tier_1,knows_common,man_face_young_1,man_face_old_2],
["walker_man_rohan_t","Rohan_Townsman","_",tf_rohan| tfg_boots| tfg_armor,0,0,fac_rohan,
   [itm_fur_hat_a_new_wb, 
   itm_tabard_b_wb, itm_peasant_man_a_wb, itm_leather_jerkin_wb, itm_white_tunic_c_wb, itm_rohan_fine_outfit_dale_dress_wb, itm_rohan_tunic_a_wb, itm_rohan_tunic_b_wb, 
   itm_leather_boots,itm_rohan_shoes],
      attr_tier_1,wp_tier_1,knows_common,rohan_face_middle_1,rohan_face_older_2],
["walker_man_rohan_d","Rohan_Townsman","_",tf_rohan| tfg_boots| tfg_armor,0,0,fac_rohan,
   [itm_hood_grey, itm_hood_green,
   itm_tabard_b_wb, itm_peasant_man_a_wb, itm_leather_jerkin_wb, itm_white_tunic_c_wb, itm_rohan_fine_outfit_dale_dress_wb, itm_rohan_tunic_a_wb, itm_rohan_tunic_b_wb, itm_sar_robe_b_wb,
   itm_leather_boots_bad,itm_rohan_shoes_bad],
   attr_tier_1,wp_tier_1,knows_common,rohan_face_middle_1,rohan_face_older_2],
["walker_woman_rohan_t","Rohan_Maiden","_",tf_female| tfg_boots| tfg_armor,0,0,fac_rohan,
   [itm_hood_green_bad,
   itm_robe_generic_dress_wb,itm_green_dress_wb, itm_black_dress_wb,itm_rohan_fine_outfit_dale_dress_wb,
   itm_rohan_shoes_bad,itm_leather_boots_bad],
      attr_tier_1,wp_tier_1,knows_common,rohan_woman_face_1,rohan_woman_face_2],
["walker_woman_rohan_d","Rohan_Maiden","_",tf_female| tfg_boots| tfg_armor,0,0,fac_rohan,
   [itm_hood_grey, itm_hood_green, itm_fur_hat_a_new_wb,
   itm_robe_generic_dress_wb,itm_rohan_fine_outfit_dale_dress_wb, itm_green_dress_wb, itm_black_dress_wb, itm_green_tunic_wb, itm_leather_jerkin_wb, itm_black_tunic_wb,itm_peasant_man_a_wb,
   itm_leather_boots,itm_rohan_shoes],
      attr_tier_1,wp_tier_1,knows_common,rohan_woman_face_1,rohan_woman_face_2],
# all except MT
["walker_woman_gondor_b","Gondor_Woman","_",tf_female| tfg_boots| tfg_armor| tfg_helm,0,0,fac_gondor,
   [itm_hood_black_bad,itm_hood_grey_bad,
   itm_robe_generic_dress,itm_rohan_fine_outfit_dale_dress,itm_black_dress,itm_green_dress_wb, itm_peasant_dress_b_new_wb, 
    itm_rohan_shoes_bad, itm_leather_boots_dark_bad,],
   attr_tier_1,wp_tier_1,knows_common,woman_face_1,woman_face_2],
# all Gondor Cities except Calembel
["walker_woman_gondor_bw","Gondor_Woman","_",tf_female| tfg_boots| tfg_armor| tfg_helm,0,0,fac_gondor,
   [itm_wimple_a_wb, itm_wimple_with_veil_wb, itm_fine_hat_wb, 
   itm_robe_generic_dress,itm_black_dress,itm_black_dress, itm_sarranid_lady_dress_wb,itm_peasant_dress_b_new_wb,  itm_gondor_fine_outfit_dress,itm_blackwhite_dress_wb,
   itm_rohan_shoes_good],
      attr_tier_1,wp_tier_1,knows_common,woman_face_1,woman_face_2],
# Minas Tirith only
["walker_woman_gondor_w","Gondor_Noble","_",tf_male| tfg_boots| tfg_armor,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_fine_outfit_dress, itm_denethor_robe,itm_nobleman_outfit_b_new_wb,
   itm_rohan_shoes_good],
      attr_tier_1,wp_tier_1,knows_common,woman_face_1,woman_face_2],
# end TLD walkers

        ] or [
        #TLD walkers - M&B
        ["walker_man_gondor_black","Townsman","_",tf_gondor| tfg_boots| tfg_armor,0,0,fac_gondor,
           [itm_corsair_boots,itm_pelargir_hood, itm_gondor_fine_outfit_dress, itm_blue_tunic, itm_white_tunic_a, itm_gon_jerkin, itm_white_tunic_a, itm_white_tunic_b, itm_white_tunic_c, itm_black_tunic, itm_leather_boots,],
              attr_tier_1,wp_tier_1,knows_common,man_face_young_1,man_face_old_2],
        ["walker_man_gondor_white","Townsman","_",tf_gondor| tfg_boots| tfg_armor,0,0,fac_gondor,
           [itm_corsair_boots, itm_gondor_fine_outfit_dress, itm_gondor_fine_outfit_dress, itm_white_tunic_a, itm_white_tunic_b, itm_white_tunic_c, itm_blue_tunic, itm_black_tunic, itm_denethor_robe, itm_leather_boots,],
              attr_tier_5,wp_tier_1,knows_common,man_face_young_1,man_face_old_2],
        ["walker_man_gondor_blue","Townsman","_",tf_gondor| tfg_boots| tfg_armor,0,0,fac_gondor,
           [itm_hood_black,itm_pelargir_hood,itm_gondor_fine_outfit_dress, itm_blue_tunic, itm_white_tunic_a, itm_gon_jerkin, itm_leather_jerkin, itm_black_tunic,itm_leather_apron,itm_lossarnach_shirt, itm_leather_boots,],
              attr_tier_1,wp_tier_1,knows_common,man_face_young_1,man_face_old_2],
        ["walker_man_gondor_green","Townsman","_",tf_gondor| tfg_boots| tfg_armor,0,0,fac_gondor,
           [itm_hood_black,itm_blue_tunic, itm_white_tunic_a, itm_leather_jerkin, itm_black_tunic, itm_leather_apron, itm_leather_boots,itm_rohan_shoes],
              attr_tier_1,wp_tier_1,knows_common,man_face_young_1,man_face_old_2],
        ["walker_man_rohan_t","Rohan_Townsman","_",tf_rohan| tfg_boots| tfg_armor,0,0,fac_rohan,
           [itm_rohan_tunic_a,itm_rohan_tunic_b, itm_rohan_fine_outfit_dale_dress, itm_white_tunic_a, itm_leather_jerkin, itm_black_tunic, itm_leather_apron, itm_leather_boots,itm_rohan_shoes],
              attr_tier_1,wp_tier_1,knows_common,rohan_face_middle_1,rohan_face_older_2],
        ["walker_man_rohan_d","Rohan_Townsman","_",tf_rohan| tfg_boots| tfg_armor,0,0,fac_rohan,
           [itm_gondor_ranger_hood,itm_rohan_tunic_a,itm_rohan_tunic_b, itm_rohan_fine_outfit_dale_dress, itm_white_tunic_a, itm_leather_jerkin, itm_black_tunic, itm_leather_apron,  itm_rohan_shoes,],
              attr_tier_1,wp_tier_1,knows_common,rohan_face_middle_1,rohan_face_older_2],
        ["walker_woman_rohan_t","Rohan_Maiden","_",tf_female| tfg_boots| tfg_armor,0,0,fac_rohan,
           [itm_gondor_ranger_hood,itm_robe_generic_dress,itm_green_dress, itm_black_dress,itm_rohan_fine_outfit_dale_dress,itm_rohan_shoes,itm_leather_boots],
              attr_tier_1,wp_tier_1,knows_common,rohan_woman_face_1,rohan_woman_face_2],
        ["walker_woman_rohan_d","Rohan_Maiden","_",tf_female| tfg_boots| tfg_armor,0,0,fac_rohan,
           [itm_robe_generic_dress,itm_rohan_fine_outfit_dale_dress, itm_green_dress, itm_black_dress, itm_green_tunic, itm_white_tunic_a,itm_leather_jerkin, itm_black_tunic, itm_leather_apron,itm_leather_boots,itm_rohan_shoes],
              attr_tier_1,wp_tier_1,knows_common,rohan_woman_face_1,rohan_woman_face_2],
        ["walker_woman_gondor_b","Gondor_Woman","_",tf_female| tfg_boots| tfg_armor| tfg_helm,0,0,fac_gondor,
           [itm_robe_generic_dress,itm_rohan_fine_outfit_dale_dress,itm_black_dress, itm_wimple_a, itm_wimple_with_veil ,itm_leather_boots,],
           attr_tier_1,wp_tier_1,knows_common,woman_face_1,woman_face_2],
        ["walker_woman_gondor_bw","Gondor_Woman","_",tf_female| tfg_boots| tfg_armor| tfg_helm,0,0,fac_gondor,
           [itm_robe_generic_dress,itm_black_dress,itm_black_dress, itm_blackwhite_dress,itm_wimple_a, itm_wimple_with_veil, itm_fine_hat,itm_leather_boots,],
              attr_tier_1,wp_tier_1,knows_common,woman_face_1,woman_face_2],
        ["walker_woman_gondor_w","Gondor_Noble","_",tf_male| tfg_boots| tfg_armor,0,0,fac_gondor,
           [itm_gondor_fine_outfit_dress,itm_gondor_fine_outfit_dress,itm_gondor_fine_outfit_dress,itm_denethor_robe,itm_leather_boots,itm_corsair_boots],
              attr_tier_1,wp_tier_1,knows_common,woman_face_1,woman_face_2],
        # end TLD walkers
        ]) + [ 

# Ryan BEGIN
["ramun_the_slave_trader","Ramun_the_slave_trader","_",tf_hero,0,0,fac_commoners,
   [],
      attr_tier_1,wp_tier_1,knows_common,merchant_face_1,merchant_face_2],
["guide","Quick_Jimmy","_",tf_hero,0,0,fac_commoners,
   [],
      attr_tier_1,wp_tier_1,knows_inventory_management_10,merchant_face_1,merchant_face_2],
# Ryan END

["galeas","Galeas","_",tf_hero,0,0,fac_commoners,
   [],
      attr_tier_1,wp_tier_1,knows_common,merchant_face_1,merchant_face_2],
["farmer_from_bandit_village","Farmer","Farmers",tfg_armor,0,0,fac_commoners,
   [],
      attr_tier_1,wp_tier_1,knows_common,merchant_face_1,merchant_face_2],
["trainer_1","Trainer","_",tf_hero, 0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["trainer_2","Trainer","_",tf_hero, 0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["trainer_3","Trainer","_",tf_hero, 0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["trainer_4","Trainer","_",tf_hero, 0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],

#TRAINERS
["trainer_gondor","Trainer","_",tf_hero| tf_gondor| tfg_armor| tfg_boots, scn_gondor_arena|entry(1),0,fac_commoners,
   [itm_gon_tower_guard,itm_gondor_heavy_greaves,itm_gondor_citadel_sword,itm_mail_mittens],
      0,0,0,gondor_face2],
["trainer_rohan","Trainer","_",tf_hero| tf_rohan| tfg_armor| tfg_boots, scn_rohan_arena|entry(1),0,fac_commoners,
   [itm_rohan_light_greaves,itm_mail_mittens,itm_rohan_leather,itm_rohan_spear,],
      0,0,0,rohan_face_old_2],
["trainer_dale","Trainer","_",tf_hero| tfg_armor| tfg_boots, scn_dale_arena|entry(1),0,fac_commoners,
   [itm_blue_tunic,itm_leather_boots,],
      0,0,0,gondor_face2],
["trainer_elf","Trainer","_",tf_hero| tf_lorien| tfg_armor| tfg_boots, scn_elf_arena|entry(1),0,fac_commoners,
   [itm_whiterobe,itm_leather_boots,],
      attr_tier_5,0,0,lorien_elf_face_2],
["trainer_beorn","Trainer","_",tf_hero| tfg_armor| tfg_boots, scn_beorn_arena|entry(1),0,fac_commoners,
   [itm_beorn_padded,itm_rohan_shoes,],
      0,0,0,beorn_face2],
["trainer_dwarf","Trainer","_",tf_hero| tf_dwarf| tfg_armor| tfg_boots, scn_dwarf_arena|entry(1),0,fac_commoners,
   [itm_leather_dwarf_armor,itm_dwarf_pad_boots,],
      0,0,0,dwarf_face_2],
["trainer_mordor","Trainer","_",tf_hero| tf_orc| tfg_armor| tfg_boots, scn_mordor_arena|entry(1),0,fac_commoners,
   [itm_uruk_ragwrap,itm_orc_tribal_a,],
      0,0,0,orc_face_normal],
["trainer_isengard","Trainer","_",tf_hero| tf_orc| tfg_armor| tfg_boots, scn_isengard_arena|entry(1),0,fac_commoners,
   [itm_uruk_ragwrap,itm_orc_tribal_a,],
      0,0,0,orc_face_normal],
["trainer_khand","Trainer","_",tf_hero| tf_evil_man| tfg_armor| tfg_boots, scn_khand_arena|entry(1),0,fac_commoners,
   [itm_khand_foot_lam,itm_leather_boots,],
      0,0,0,khand_man2],
["trainer_rhun","Trainer","_",tf_hero| tf_evil_man| tfg_armor| tfg_boots, scn_rhun_arena|entry(1),0,fac_commoners,
   [itm_rhun_armor_a,itm_furry_boots,],
      0,0,0,rhun_man2],
["trainer_harad","Trainer","_",tf_hero| tf_harad| tfg_armor| tfg_boots, scn_harad_arena|entry(1),0,fac_commoners,
   [itm_harad_scale,itm_harad_scale_greaves,],
      0,0,0,haradrim_face_2],
["trainer_umbar","Trainer","_",tf_hero| tfg_armor| tfg_boots, scn_umbar_arena|entry(1),0,fac_commoners,
   [itm_umb_armor_d,itm_corsair_boots,],
      0,0,0,bandit_face2],
      
#
# Ransom brokers.
["ransom_broker_1","Ransom_Broker","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["ransom_broker_2","Ransom_Broker","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["ransom_broker_3","Ransom_Broker","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["ransom_broker_4","Ransom_Broker","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["ransom_broker_5","Ransom_Broker","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["ransom_broker_6","Ransom_Broker","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["ransom_broker_7","Ransom_Broker","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["ransom_broker_8","Ransom_Broker","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["ransom_broker_9","Ransom_Broker","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["ransom_broker_10","Ransom_Broker","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
 
# Tavern traveler.
["tavern_traveler_1","Traveller","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["tavern_traveler_2","Traveller","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["tavern_traveler_3","Traveller","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["tavern_traveler_4","Traveller","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["tavern_traveler_5","Traveller","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["tavern_traveler_6","Traveller","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["tavern_traveler_7","Traveller","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["tavern_traveler_8","Traveller","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["tavern_traveler_9","Traveller","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
["tavern_traveler_10","Traveller","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
# Tavern minstrel.
["tavern_minstrel_1","Minstrel","_",tf_hero| tf_randomize_face,0,0,fac_commoners,
   [],
      0,0,0,merchant_face_1,merchant_face_2],
#Companions
["npc1","Mablung","_",tf_hero| tf_gondor| tf_unmoveable_in_party_window,0,0,fac_gondor,
   [itm_gon_ranger_cloak,itm_gondor_light_greaves,itm_gon_tab_shield_a,itm_gondor_ranger_sword,itm_gondor_bow,itm_ithilien_arrows,itm_gondor_ranger_hood,],
      str_15|agi_15|int_12|cha_9|level(20),wp_one_handed(160)|wp_two_handed(140)|wp_polearm(120)|wp_archery(200)|wp_throwing(120),knows_common|knows_ironflesh_3|knows_power_strike_3|knows_power_draw_5|knows_weapon_master_5|knows_shield_2|knows_athletics_5|knows_riding_1|knows_looting_2|knows_trainer_2|knows_tracking_3|knows_tactics_2|knows_pathfinding_4|knows_spotting_3|knows_wound_treatment_2|knows_persuasion_3|knows_leadership_2|knows_trade_2,0x000000086b006144444b6e574146472400000000001ec82c0000000000000000],
["npc2","Cirdil","_",tf_hero| tf_gondor| tf_unmoveable_in_party_window,0,0,fac_gondor,
   [itm_gon_jerkin,itm_leather_boots_bad,itm_gondor_auxila_helm,itm_shortened_spear,itm_gon_tab_shield_a,itm_gondor_short_sword,],
      str_10|agi_8|int_4|cha_6|level(3),wp_one_handed(10)|wp(60),knows_common|knows_ironflesh_1|knows_power_strike_1|knows_power_throw_1|knows_power_draw_1|knows_weapon_master_2|knows_shield_2|knows_athletics_1|knows_trainer_1|knows_tactics_1|knows_spotting_1|knows_inventory_management_1|knows_wound_treatment_1|knows_first_aid_1|knows_leadership_1|knows_trade_1,0x000000002d00418519da91378c8aa8d300000000001eb9110000000000000000],
["npc3","Ulfas","_",tf_rohan| tf_hero| tf_unmoveable_in_party_window,0,0,fac_rohan,
   [itm_rohan_mail_bad,itm_leather_boots_bad,itm_rohan_shield_a,itm_rohan_light_helmet_b_bad,itm_rohan_spear,itm_rohirrim_long_hafted_axe,itm_rohirrim_courser,],
      str_14|agi_10|int_5|cha_9|level(10),wp_one_handed(110)|wp_two_handed(100)|wp_polearm(120)|wp_archery(80)|wp_throwing(100),knows_common|knows_ironflesh_3|knows_power_strike_2|knows_power_throw_1|knows_weapon_master_3|knows_shield_2|knows_athletics_1|knows_riding_3|knows_horse_archery_2|knows_looting_3|knows_trainer_1|knows_tracking_2|knows_pathfinding_1|knows_wound_treatment_1|knows_trade_2,0x0000000886000085395d6db6db6db8db00000000001db6e30000000000000000],
["npc4","Galmyne","_",tf_female| tf_mounted| tfg_ranged| tf_hero| tf_unmoveable_in_party_window,0,0,fac_rohan,
   [itm_rohan_rider,itm_rohan_light_greaves,itm_rohan_shield_d,itm_rohan_archer_helmet_b,itm_rohan_sword_c,itm_strong_bow,itm_khergit_arrows,itm_rohan_warhorse,],
      str_14|agi_18|int_9|cha_12|level(22),wp_one_handed(160)|wp_two_handed(120)|wp_polearm(140)|wp_archery(180)|wp_throwing(160),knows_common|knows_ironflesh_3|knows_power_strike_2|knows_power_throw_4|knows_power_draw_4|knows_weapon_master_6|knows_shield_3|knows_athletics_1|knows_riding_6|knows_horse_archery_5|knows_trainer_1|knows_spotting_1|knows_wound_treatment_4|knows_first_aid_3|knows_trade_1,0x000000000300000114a261248280c73400000000001ca48d0000000000000000],
["npc5","Glorfindel","_",tf_lorien| tf_mounted| tfg_ranged| tf_hero| tf_unmoveable_in_party_window,0,0,fac_lorien,
   [itm_riv_armor_reward,itm_lorien_boots,itm_riv_helm_glorfi,itm_lorien_bow_reward,itm_elven_arrows,itm_elven_arrows,itm_lorien_sword_c,itm_lorien_warhorse,],
      str_30|agi_24|int_18|cha_24|level(55),wp(500),knows_common|knows_ironflesh_6|knows_power_strike_7|knows_power_draw_9|knows_weapon_master_8|knows_athletics_5|knows_riding_7|knows_horse_archery_9|knows_tactics_6|knows_pathfinding_5|knows_spotting_5|knows_first_aid_4|knows_persuasion_3|knows_prisoner_management_3|knows_leadership_9,0x000000018000100a38db6db6db6db6db00000000001db6eb0000000000000000],
["npc6","Luevanna","_",tf_female| tfg_ranged| tf_hero| tf_unmoveable_in_party_window,0,0,fac_woodelf,
   [itm_mirkwood_leather_bad,itm_leather_boots_dark_bad,itm_mirkwood_knife,itm_short_bow,itm_arrows,],
      str_8|agi_13|int_12|cha_6|level(7),wp_one_handed(70)|wp_two_handed(40)|wp_polearm(70)|wp_archery(100)|wp_throwing(60),knows_common|knows_ironflesh_1|knows_power_strike_2|knows_power_throw_1|knows_power_draw_3|knows_weapon_master_2|knows_shield_1|knows_athletics_4|knows_riding_1|knows_horse_archery_1|knows_tracking_3|knows_pathfinding_1|knows_spotting_3|knows_wound_treatment_2|knows_first_aid_2|knows_persuasion_4,0x0000000180004009041d7566cb87608000000000001d24d30000000000000000],
["npc7","Kili_Goldfinger","_",tf_dwarf| tf_hero| tf_unmoveable_in_party_window,0,0,fac_dwarf,
   [itm_leather_dwarf_armor_b,itm_dwarf_pad_boots,itm_dwarf_sword_a,itm_dwarf_throwing_axe,itm_dwarf_mattock,itm_dwarf_shield_a,],
      str_14|agi_8|int_7|cha_6|level(7),wp_one_handed(100)|wp_two_handed(115)|wp_polearm(115)|wp_archery(50)|wp_throwing(115),knows_common|knows_ironflesh_3|knows_power_strike_3|knows_power_throw_3|knows_weapon_master_2|knows_shield_3|knows_athletics_2|knows_riding_10|knows_looting_4|knows_trainer_1|knows_inventory_management_2|knows_prisoner_management_1|knows_trade_3,0x00000001c000110336db6db6db6db6db00000000001db6db0000000000000000],
["npc8","Faniul","_",tf_female| tfg_ranged| tf_hero| tf_unmoveable_in_party_window,0,0,fac_dale,
   [itm_blue_tunic,itm_leather_boots_bad,itm_wimple_with_veil,itm_shortened_spear],
      str_8|agi_6|int_11|cha_5|level(12),wp_one_handed(40)|wp_two_handed(40)|wp_polearm(60)|wp_archery(70)|wp_throwing(40),knows_common|knows_ironflesh_3|knows_power_strike_1|knows_power_draw_2|knows_weapon_master_2|knows_shield_3|knows_athletics_2|knows_riding_2|knows_looting_1|knows_tactics_2|knows_spotting_2|knows_inventory_management_2|knows_wound_treatment_4|knows_surgery_4|knows_first_aid_2|knows_prisoner_management_1|knows_trade_2,0x0000000712003004589dae38ad69a64900000000001ec6cc0000000000000000],
["npc9","Gulm","_",tf_urukhai| tf_hero| tf_unmoveable_in_party_window,0,0,fac_isengard,
   [itm_isen_uruk_light_a,itm_uruk_chain_greaves,itm_isengard_mallet,itm_evil_gauntlets_a,],
      str_24|agi_17|int_8|cha_4|level(20),wp(185),knows_common|knows_ironflesh_10|knows_power_strike_5|knows_power_throw_5|knows_weapon_master_5|knows_shield_3|knows_athletics_7|knows_looting_5|knows_trainer_2,0x00000001b50000c2003d7dc5a4b2195c00000000000000000000000000000000],
["npc10","Durgash","_",tf_orc| tf_mounted| tfg_ranged| tf_hero| tf_unmoveable_in_party_window,0,0,fac_isengard,
   [itm_isen_orc_light_b,itm_wood_club,itm_orc_throwing_arrow,itm_warg_1d,],
      str_12|agi_11|int_11|cha_4|level(10),wp(90),knows_common|knows_ironflesh_3|knows_power_strike_2|knows_power_throw_2|knows_weapon_master_3|knows_riding_4|knows_horse_archery_3|knows_looting_2|knows_trainer_3|knows_tracking_1|knows_tactics_2|knows_pathfinding_4|knows_spotting_2|knows_inventory_management_1|knows_leadership_1,0x00000001a2000007399e8ccc9cae34e500000000001d16ad0000000000000000],
["npc11","Ufthak","_",tf_orc| tf_hero| tf_unmoveable_in_party_window,0,0,fac_mordor,
   [itm_m_orc_light_a,itm_orc_ragwrap,itm_wood_club,itm_orc_simple_spear,],
      str_8|agi_12|int_6|cha_4|level(1),wp(75),knows_common|knows_ironflesh_2|knows_power_strike_1|knows_power_throw_1|knows_power_draw_2|knows_weapon_master_2|knows_athletics_3|knows_looting_2|knows_tracking_2|knows_spotting_1|knows_persuasion_1,orc_face6],
["npc12","Gorbag","_",tf_uruk| tf_hero| tf_unmoveable_in_party_window,0,0,fac_mordor,
   [itm_m_uruk_med_b,itm_uruk_tracker_boots,itm_orc_two_handed_axe,itm_uruk_pike_b,itm_uruk_helm_b,],
      str_19|agi_16|int_9|cha_4|level(20),wp(175),knows_common|knows_ironflesh_6|knows_power_strike_5|knows_power_throw_4|knows_weapon_master_5|knows_shield_5|knows_athletics_2|knows_riding_1|knows_looting_5|knows_trainer_3|knows_tactics_3|knows_spotting_3|knows_leadership_3,uruk_hai_face2],
["npc13","Lykyada","_",tf_harad| tfg_ranged| tf_mounted| tf_hero| tf_unmoveable_in_party_window,0,0,fac_harad,
   [itm_black_snake_armor,itm_harad_leather_greaves,itm_leather_gloves,itm_black_snake_helm,itm_harad_bow,itm_harad_arrows,itm_black_snake_sword,itm_harad_warhorse,],
      str_24|agi_20|int_18|cha_15|level(40),wp(400),knows_common|knows_ironflesh_7|knows_power_strike_6|knows_power_draw_6|knows_weapon_master_4|knows_athletics_3|knows_riding_6|knows_horse_archery_5|knows_trainer_6|knows_tracking_3|knows_tactics_5|knows_pathfinding_5|knows_spotting_5|knows_wound_treatment_4|knows_first_aid_6|knows_leadership_4,0x000000051f00000b372571b8ed79a6ac00000000001db6360000000000000000],
["npc14","Fuldimir","_",tf_hero| tf_unmoveable_in_party_window,0,0,fac_umbar,
   [itm_umb_armor_a,itm_corsair_boots,itm_umb_shield_a,itm_corsair_throwing_dagger,itm_umbar_cutlass,],
      str_10|agi_9|int_7|cha_7|level(4),wp(80),knows_common|knows_power_strike_1|knows_power_throw_2|knows_power_draw_2|knows_weapon_master_3|knows_athletics_2|knows_looting_3|knows_tactics_2|knows_spotting_2|knows_surgery_2|knows_trade_3,0x00000001b70032453add7524dc76d74900000000001d35330000000000000000],
["npc15","Bolzog","_",tf_orc| tf_hero| tf_unmoveable_in_party_window,0,0,fac_moria,
   [itm_moria_armor_a,itm_orc_slasher],
      str_9|agi_10|int_12|cha_4|level(7),wp(80),knows_common|knows_ironflesh_2|knows_power_strike_1|knows_power_throw_2|knows_weapon_master_2|knows_shield_1|knows_athletics_3|knows_riding_1|knows_looting_3|knows_trainer_1|knows_tracking_3|knows_tactics_2|knows_inventory_management_3|knows_wound_treatment_3|knows_surgery_3|knows_first_aid_1,0x00000001ab00200d35627276a42e150c00000000001dca2c0000000000000000],
["npc16","Varfang","_",tf_mounted| tf_hero| tf_unmoveable_in_party_window,0,0,fac_rhun,
   [itm_rhun_armor_a,itm_furry_boots,itm_rhun_sword,itm_light_lance,itm_rhun_helm_pot,itm_rhun_horse_a,],
      str_15|agi_15|int_3|cha_5|level(10),wp(120),knows_common|knows_ironflesh_2|knows_power_strike_4|knows_power_throw_2|knows_weapon_master_3|knows_riding_5|knows_horse_archery_4|knows_looting_4|knows_prisoner_management_1|knows_leadership_1,0x000000018700214944d468dd9bae295b00000000001cb5a40000000000000000],
["npc17","Dimborn","_",tf_hero| tf_unmoveable_in_party_window,0,0,fac_beorn,
   [itm_woodman_tunic,itm_leather_boots_bad,itm_beorn_axe,],
      str_12|agi_10|int_5|cha_3|level(4),wp(95),knows_common|knows_ironflesh_3|knows_power_strike_2|knows_power_draw_2|knows_weapon_master_2|knows_shield_1|knows_athletics_3|knows_riding_1|knows_looting_2|knows_pathfinding_1|knows_wound_treatment_2|knows_persuasion_4,0x00000009f50001c97ac16e65f3ecf7de00000000001cc7080000000000000000],
#NPC system changes end
 
 
# <--- swy: heroes_begin --->
 
## Kham - New Gondor Lord
["knight_6_2","Golasgil","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gondor_lance, itm_pinnath_leader,itm_good_mace,itm_gondor_med_greaves,itm_gondor_hunter,itm_gon_tab_shield_c,itm_mail_mittens,itm_pelargir_helmet_light,],
      attr_tier_5,wp_tier_5,gondor_skills_2|knows_riding_4|knows_trainer_7,0x0000000e800021465e856dd74321355600000000001c58a50000000000000000],

#governors (plural contains how player refers to the guy
["gondor_lord","Steward_Denethor","Steward",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gondor_warhorse,itm_denethor_robe,itm_gondor_light_greaves,itm_mail_mittens,itm_gondor_leader_helm,itm_gondor_citadel_sword,itm_gondor_shield_e],
      attr_tier_7,wp_tier_6,knight_skills_5|knows_riding_4|knows_trainer_5,0x0000000efe00400726c34cb9d447d0cc00000000001cb4580000000000000000],
["rohan_lord","King_Theoden","King",tf_hero| tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_mearas_reward,itm_rohan_armor_th,itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_archer_helmet_c_lordly,itm_eorl_cavalry_sword,itm_rohan_shield_g, itm_rohan_lance],
      attr_tier_7,wp_tier_6,knight_skills_4|knows_riding_4|knows_riding_5|knows_trainer_4,0x0000000fff00130347934c399386b8a300000000001db6d90000000000000000],
["isengard_lord","Saruman","Master",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_isengard,
   [itm_courser,itm_whiterobe_saru,itm_leather_boots,],
      attr_tier_7,wp_tier_6,knight_skills_5|knows_riding_4|knows_trainer_6,0x0000000fff004107121a807fc84b82ff00000000001d1ab00000000000000000],
["mordor_lord","Mouth_of_Sauron","Satrap",tf_hero| tf_evil_man| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_mordor,
   [itm_mordor_warhorse2,itm_m_cap_armor,itm_uruk_chain_greaves,itm_evil_gauntlets_b_good,itm_hood_black,itm_mordor_longsword,],
      attr_tier_7,wp_tier_6,knight_skills_1|knows_riding_4,0x0000000fff00000012078077c00ff1c000000000001cf0680000000000000000],
["harad_lord","Chief_Ul-Ulcari","Chief",tf_hero| tf_harad| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,
   [itm_harad_warhorse,itm_harad_heavy,itm_harad_leather_greaves,itm_evil_gauntlets_a,itm_harad_dragon_helm,itm_harad_khopesh,],
      attr_tier_7,wp_tier_6,knight_skills_4|knows_riding_4|knows_trainer_5,0x00000009ff0020071415a5f9fb60c1b700000000001d663b0000000000000000],
["rhun_lord","Jarl_Helcaroth","Jarl",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_horse_h,itm_rhun_armor_k_good,itm_splinted_greaves_good,itm_evil_gauntlets_b_good,itm_rhun_helm_chieftain_good,itm_rhun_greatsword,],
      attr_tier_7,wp_tier_6,knight_skills_5|knows_riding_4|knows_trainer_5,0x00000004a300640c1a938b5499b6556c00000000001edab90000000000000000],
["khand_lord","Shibh_Krukmahur","Shibh",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_khand,
   [itm_variag_kataphrakt,itm_khand_noble_lam,itm_splinted_greaves_good,itm_evil_gauntlets_b_good,itm_khand_lance,itm_khand_tulwar,itm_variag_gladiator_shield,],
      attr_tier_7,wp_tier_6,knight_skills_5|knows_riding_4|knows_trainer_4,0x0000000f3f00b38712065fd3287f731c00000000001c53780000000000000000],
["umbar_lord","Admiral_Tulmir","Admiral",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_umbar,
   [itm_umb_armor_f_good,itm_corsair_boots,itm_leather_gloves_reward,itm_umb_helm_reward,itm_corsair_bow,itm_corsair_arrows,itm_kraken,itm_umb_shield_e],
      attr_tier_7,wp_tier_6,knight_skills_5|knows_riding_4|knows_trainer_6,0x0000000e3b004244365b6db99b6db7df00000000001dd6eb0000000000000000],
["lorien_lord","Lady_Galadriel","Lady",tf_hero| tf_randomize_face| tf_female| tfg_armor| tfg_helm| tfg_gloves| tfg_boots,0,0,fac_lorien,
   [itm_galadriel,itm_empty_head,itm_empty_legs,itm_empty_hands,],
      attr_tier_7,wp(20),knows_common,0x0000000e3b004000365b6db99b6db7df00000000001dd6eb0000000000000000],
["imladris_lord","Lord_Elrond","Lord",tf_hero| tf_imladris| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_imladris,
   [itm_mearas_reward,itm_riv_armor_reward,itm_riv_boots,itm_leather_gloves_reward,itm_riv_tiara,itm_riv_riding_sword,itm_riv_shield_b,itm_riv_spear],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_4|knows_riding_5|knows_persuasion_5|knows_trainer_5,0x0000000bff002001379b74b75346d08d00000000001d969b0000000000000000],
["woodelf_lord","King_Thranduil","King",tf_hero| tf_woodelf| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_woodelf,
   [itm_mirkwood_heavy_scale,itm_mirkwood_boots,itm_evil_gauntlets_a,itm_riv_tiara,itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_great_spear,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_5|knows_persuasion_7|knows_trainer_5,0x0000000c00003002189d6e454c6465a500000000001c68f20000000000000000],
["moria_lord","Master_Bolg_the_Lesser","Master",tf_hero| tf_uruk| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_moria,
   [itm_warg_reward,itm_m_uruk_heavy_c,itm_uruk_helm_e,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_orc_javelin,itm_uruk_falchion_b,],
      attr_tier_7,wp_tier_6,knight_skills_5|knows_riding_4|knows_trainer_4|knows_persuasion_3|knows_leadership_10|knows_tactics_8,0x00000000260010010038c51051df5f5800000000000000000000000000000000],
["guldur_lord","Master_Fuinur","Master",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_guldur,
   [itm_mordor_warhorse,itm_m_cap_armor,itm_uruk_chain_greaves,itm_evil_gauntlets_b_good,itm_mordor_cap_helm,itm_mordor_man_shield_b,itm_mordor_longsword,],
      attr_tier_7,wp_tier_6,knight_skills_5|knows_riding_4|knows_trainer_6,0x0000000fcd0005c03586a83d4223b2c200000000001c58e00000000000000000],
["gundabad_lord","Master_Burza Krual","Master",tf_hero| tf_uruk| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gundabad,
   [itm_warg_reward,itm_gundabad_armor_e,itm_orc_greaves,itm_evil_gauntlets_a,itm_gundabad_helm_e,itm_orc_throwing_axes,itm_orc_slasher,],
      attr_tier_7,wp_tier_6,knight_skills_4|knows_riding_4|knows_trainer_4|knows_persuasion_3|knows_leadership_10|knows_tactics_8,0x0000000026002085003f006fe95aae4000000000000000000000000000000000],
["dale_lord","King_Brand","King",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_dale,
   [itm_dale_warhorse,itm_dale_armor_reward,itm_leather_boots,itm_evil_gauntlets_b_good,itm_dale_helmet_f,itm_dale_sword_reward,itm_dwarf_shield_c_good,itm_lance,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_riding_4|knows_trainer_5,0x0000000e3f00018436db75b79b6eb6db00000000001db6eb0000000000000000],
["dwarf_lord","King_Dain_II_Ironfoot","King",tf_hero| tf_dwarf| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_armor_c,itm_dwarf_scale_boots,itm_mail_mittens,itm_dwarf_helm_king_NPC,itm_dwarf_throwing_axe,(itm_dwarf_great_axe,imod_rotten)],
      attr_dwarf_tier_6,wp_dwarf_tier_6,knight_skills_5|knows_riding_10|knows_persuasion_3|knows_trainer_4,0x0000000e7f00210133c16e7bb1fffdff00000000001f56f30000000000000000],
["dunland_lord","Chief_Daeglaf_the_Black","Chief",tf_hero| tf_dunland| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_dunland,
   [itm_dunland_armor_k,itm_dunland_wolfboots,itm_evil_gauntlets_a,itm_dun_helm_e,itm_dun_berserker,itm_dun_shield_b,itm_dunland_javelin,],
      attr_tier_7,wp_tier_6,knight_skills_5|knows_persuasion_5|knows_trainer_6,0x000000003f0051c721dc6c71580f36ff00000000001fd2e80000000000000000],
["beorn_lord","Chief_Grimbeorn_the_Old","Chief",tf_hero| tfg_shield| tfg_armor| tfg_helm|tfg_boots,0,0,fac_beorn,
   [itm_beorn_chief,itm_leather_boots,itm_evil_gauntlets_a,itm_beorn_helmet,itm_beorn_battle_axe,itm_dwarf_throwing_axe,itm_beorn_shield_reward,],
      attr_tier_7,wp_tier_6,knight_skills_5|knows_riding_10|knows_persuasion_5|knows_trainer_4,0x0000000d6a00628918d46a72d946e7ae00000000001eeeb90000000000000000],
 

 # marshalls which are not also leaders
["lorien_marshall","Celeborn","_",tf_hero| tf_lorien| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_lorien,
   [itm_mearas_reward,itm_lorien_heavy_good_cloak,itm_lorien_boots,itm_leather_gloves_reward,itm_riv_tiara,itm_lorien_bow,itm_elven_arrows,itm_lorien_sword_a,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_4|knows_riding_4|knows_riding_5|knows_persuasion_7|knows_trainer_4,0x00000008120000024b146a491440e12400000000001cc4ad0000000000000000],

# ["gondor_marshall","Gondor Marshall","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   # [itm_gondor_warhorse,itm_pel_leader,itm_pelargir_greaves,itm_mail_mittens,itm_pelargir_helmet_heavy,itm_pelargir_sword,itm_gondor_bow,itm_gondor_arrows,],
      # attr_tier_6,wp_tier_6,knight_skills_4|knows_riding_4|knows_trainer_1|knows_trainer_3,0x00000006ff003004225b8ac89c62d2f400000000001ec8f90000000000000000],

## hobbits: two versions: for when you didn't meet them, and for when you did meet them (I wish there was a way to RENAME a Troop. str_set_troop_name FTW)  mtarini

["pippin_notmet","halfling","_",tf_hero| tf_mounted| tfg_armor| tfg_helm| tfg_boots,0,0,fac_commoners,
   [itm_empty_head,itm_empty_hands,itm_empty_legs,itm_pippin_outfit],
       attr_tier_7,wp_tier_7,knows_riding_10|knows_athletics_10|knows_power_strike_10|knows_ironflesh_10|knows_pathfinding_10,mercenary_face_2],

["merry_notmet","halfling","_",tf_hero| tf_mounted| tfg_armor| tfg_helm| tfg_boots,0,0,fac_commoners,
   [itm_empty_head,itm_empty_hands,itm_empty_legs,itm_merry_outfit],
       attr_tier_7,wp_tier_7,knows_riding_10|knows_athletics_10|knows_power_strike_10|knows_ironflesh_10|knows_pathfinding_10,mercenary_face_2],

["pippin","Pippin","_",tf_hero| tf_mounted| tfg_armor| tfg_helm| tfg_boots,0,0,fac_commoners,
   [itm_empty_head,itm_empty_hands,itm_empty_legs,itm_pippin_outfit],
       attr_tier_7,wp_tier_7,knows_riding_10|knows_athletics_10|knows_power_strike_10|knows_ironflesh_10|knows_pathfinding_10,mercenary_face_2],

["merry","Merry","_",tf_hero| tf_mounted| tfg_armor| tfg_helm| tfg_boots,0,0,fac_commoners,
   [itm_empty_head,itm_empty_hands,itm_empty_legs,itm_merry_outfit],
       attr_tier_7,wp_tier_7,knows_riding_10|knows_athletics_10|knows_power_strike_10|knows_ironflesh_10|knows_pathfinding_10,mercenary_face_2],

     #Swadian civilian clothes: itm_courtly_outfit itm_gambeson itm_blue_gambeson itm_red_gambeson itm_nobleman_outfit itm_rich_outfit itm_short_tunic itm_tabard
#Gondor Angbor 
["knight_1_1","Angbor_the_Fearless","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gondor_lam_horse,itm_lamedon_leader_surcoat_cloak,itm_gondor_heavy_greaves,itm_mail_mittens,itm_gondor_lamedon_leader_helm,itm_gondor_citadel_sword,itm_gon_tab_shield_a,itm_gondor_javelin,itm_gondor_javelin],
      attr_tier_7,wp_tier_6,gondor_skills_5|knows_riding_4|knows_trainer_4|knows_persuasion_3|knows_horse_archery_5|knows_power_throw_7,0x00000008bf00524435d36db7536db6db00000000001db6dd0000000000000000],
["knight_1_2","Húrin_of_the_Keys","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gon_tower_knight,itm_gondor_heavy_greaves,itm_mail_mittens,itm_gondor_leader_helm,itm_gondor_citadel_sword,itm_gondor_shield_e,itm_gondor_tower_spear],
      attr_tier_7,wp_tier_6,gondor_skills_4|knows_riding_4,0x00000007f700550919da9135148e24e500000000001db9110000000000000000],
["knight_1_3","Prince_Imrahil","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_dol_amroth_warhorse,itm_dol_very_heavy_mail,itm_gondor_heavy_greaves,itm_mail_mittens,itm_swan_knight_helm,itm_amroth_lance_banner,itm_amroth_bastard,itm_gon_tab_shield_c],
      attr_tier_7,wp_tier_6,gondor_skills_5|knows_riding_6|knows_trainer_7,0x0000000e7f00259419da9135148e24e500000000001db9110000000000000000],
["knight_1_4","Orthalion","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_pel_leader,itm_pelargir_greaves,itm_mail_mittens,itm_pelargir_helmet_heavy,itm_pelargir_sword,itm_gon_tab_shield_b,itm_gondor_javelin,itm_gondor_javelin],
      attr_tier_7,wp_tier_6,gondor_skills_3|knows_trainer_7|knows_power_throw_5,0x0000000fff0035d218946ec91266652b00000000001cc6f90000000000000000],
["knight_1_5","Duinhir","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_blackroot_leader,itm_gondor_heavy_greaves,itm_mail_mittens,itm_gondor_leader_helm,itm_gondor_ranger_sword,itm_gondor_tower_spear,itm_gondor_bow,itm_gondor_arrows,],
      attr_tier_7,wp_tier_6,gondor_skills_3|knows_horse_archery_7|knows_power_draw_7,0x000000003f0021544b246a471b65572400000000001cc6ed0000000000000000],
["knight_1_6","Hirluin_the_Fair","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gondor_courser,itm_pinnath_leader,itm_gondor_heavy_greaves,itm_mail_mittens,itm_gondor_leader_helm,itm_gondor_citadel_sword,itm_gon_tab_shield_c,itm_gondor_lance],
      attr_tier_7,wp_tier_6,gondor_skills_4|knows_riding_5,0x000000043a0020944aa46a451261533300000000001ec6af0000000000000000],
["knight_1_7","Faramir","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gondor_warhorse,itm_gon_leader_surcoat_cloak,itm_gondor_heavy_greaves,itm_mail_mittens,itm_gondor_leader_helm,itm_gondor_citadel_sword,itm_gondor_shield_e,itm_gondor_lance],
      attr_tier_7,wp_tier_6,gondor_skills_5|knows_persuasion_7,0x000000043f00200f49248ac99481d72c00000000001d48de0000000000000000],
["knight_1_8","Forlong_the_Fat","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gondor_warhorse,itm_lossarnach_leader,itm_lossarnach_greaves,itm_mail_mittens,itm_mordor_helm,itm_loss_axe,itm_gondor_lance,itm_gon_tab_shield_a],
      attr_tier_7,wp_tier_6,gondor_skills_4|knows_riding_4|knows_power_throw_7,0x00000008b70052935b1b8f4ae9ee793e00000000001f4cad0000000000000000],

#Rohan
["knight_1_9","Grimbold","_",tf_hero| tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_thengel_warhorse,itm_rohan_guard_bad,itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_inf_helmet_b_lordly,itm_rohirrim_long_hafted_axe,itm_strong_bow,itm_khergit_arrows,itm_rohan_shield_g,],
      attr_tier_7,wp_tier_6,knight_skills_4|knows_riding_4,0x0000000e7f0002c313da5e3993abcd3400000000001da6f30000000000000000],
["knight_1_10","Erkenbrand","_",tf_hero| tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_thengel_warhorse,itm_rohan_guard_good,itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_inf_helmet_b_lordly,itm_rohan_cav_sword,itm_rohirrim_throwing_axe,itm_rohan_shield_g],
      attr_tier_7,wp_tier_6,knight_skills_4|knows_riding_4,0x0000000dbf00334521c0723588aacd3700000000001c96db0000000000000000],
["knight_1_11","Elfhelm","_",tf_hero| tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_thengel_warhorse_heavy,itm_rohan_guard_cloak,itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_archer_helmet_c_good,itm_rohan_cav_sword,itm_rohan_lance_banner_sun,itm_rohan_shield_e],
      attr_tier_7,wp_tier_6,knight_skills_4|knows_riding_4|knows_riding_5|knows_persuasion_3,0x0000000d8e002282211a8ce5aafd4eff00000000001cb45b0000000000000000],
["knight_1_12","Hama","_",tf_hero| tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_warhorse,itm_rohan_surcoat_good,itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_inf_helmet_b_lordly,itm_rohirrim_long_hafted_axe,itm_rohan_lance_banner_horse,itm_rohan_shield_f],
      attr_tier_7,wp_tier_6,knight_skills_2|knows_riding_4,0x0000000aa500124421188e67da1fcf3f00000000001cb4730000000000000000],
["knight_1_13","Gamling","_",tf_hero| tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_warhorse,itm_rohan_rider_good_cloak,itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_archer_helmet_c_good,itm_rohirrim_long_hafted_axe,itm_rohirrim_throwing_axe,itm_rohan_shield_f],
      attr_tier_7,wp_tier_6,knight_skills_3|knows_riding_4,0x0000000fff00034220d88d77ea1fc10000000000001cb4730000000000000000],
["knight_1_14","Éomer","_",tf_hero| tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_thengel_warhorse_heavy,itm_rohan_surcoat_good_cloak,itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_archer_helmet_a_good,itm_rohan_cav_sword,itm_heavy_throwing_spear,itm_heavy_throwing_spear,itm_rohan_shield_d],
      attr_tier_7,wp_tier_6,knight_skills_4|knows_riding_4|knows_riding_5,0x0000000033001045055d5db565a9c73500000000001db6f90000000000000000],
#Isengard
["knight_1_15","Ugluk","_",tf_hero| tf_uruk |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_isengard,
   [itm_isen_uruk_heavy_reward,itm_uruk_chain_greaves,itm_evil_gauntlets_b_good,itm_isen_uruk_helm_d,itm_isengard_sword,itm_isen_uruk_shield_b,],
      attr_tier_7,wp_tier_6,knight_skills_5|knows_trainer_3|knows_persuasion_3,0x0000000026000004003da293b938671800000000000000000000000000000000],
["knight_1_16","Mauhur","_",tf_hero| tf_uruk |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_isengard,
   [itm_isen_uruk_heavy_reward,itm_uruk_chain_greaves,itm_evil_gauntlets_b_good,itm_isen_uruk_helm_d,itm_isengard_hammer,itm_isen_uruk_shield_b,],
      attr_tier_7,wp_tier_6,knight_skills_3|knows_persuasion_3,0x0000000026000143003f171a07063a1300000000000000000000000000000000],
["knight_1_17","Mog_the_Seven-fingered","_",tf_hero| tf_urukhai |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_isengard,
   [itm_isen_uruk_heavy_reward,itm_uruk_chain_greaves,itm_evil_gauntlets_b_good,itm_isen_uruk_helm_d,itm_isengard_heavy_sword,itm_isen_uruk_shield_b,],
      attr_tier_7,wp_tier_6,knight_skills_2|knows_persuasion_5,0x0000000740000140003f9f9a3fdad74d00000000000000000000000000000000],
["knight_1_18","Hushnak_Longshanks","_",tf_hero| tf_urukhai |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_isengard,
   [itm_isen_uruk_heavy_reward,itm_uruk_chain_greaves,itm_evil_gauntlets_b_good,itm_isen_uruk_helm_d,itm_isengard_hammer,itm_isen_uruk_shield_b,],
      attr_tier_7,wp_tier_6,knight_skills_3|knows_persuasion_3|knows_trainer_4,0x00000004c400120300384eb95df2446200000000000000000000000000000000],
["knight_1_19","Gridash the Tree-biter","_",tf_hero| tf_urukhai |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_isengard,
   [itm_isen_uruk_heavy_reward,itm_uruk_chain_greaves,itm_evil_gauntlets_b_good,itm_isen_uruk_helm_d,itm_isengard_heavy_axe,itm_isen_uruk_shield_b,],
      attr_tier_7,wp_tier_6,knight_skills_4|knows_persuasion_3|knows_trainer_6,0x00000004fa000046003e72470fba445400000000000000000000000000000000],
["knight_1_20","Gronk the Man-eater","_",tf_hero| tf_urukhai |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_isengard,
   [itm_isen_uruk_heavy_reward,itm_uruk_chain_greaves,itm_evil_gauntlets_b_good,itm_isen_uruk_helm_d,itm_isengard_mallet,itm_isen_uruk_shield_b,],
      attr_tier_7,wp_tier_6,knight_skills_5|knows_persuasion_3|knows_trainer_5,0x00000004f2001185003a4e4b5475450200000000000000000000000000000000],
#Mordor
["knight_2_1","Captain_Mortakh","_",tf_hero| tf_evil_man| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_mordor,
   [itm_mordor_warhorse2,itm_m_cap_armor,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_mordor_cap_helm,itm_mordor_longsword,itm_mordor_man_shield_b,],
      attr_tier_7,wp_tier_6,knight_skills_1|knows_riding_4|knows_trainer_3,0x0000000cff00150f21c38927434e804f00000000001d24be0000000000000000],
["knight_2_2","Berúthiel","_",tf_hero| tf_female| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_mordor,
   [itm_mordor_warhorse2,itm_m_cap_armor,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_mordor_cap_helm,itm_mordor_longsword,itm_mordor_man_shield_b,],
      attr_tier_7,wp_tier_6,knight_skills_2|knows_riding_4|knows_persuasion_5,0x0000000ebf0010060df26111c003815400000000001c5e380000000000000000],
["knight_2_3","Skang","_",tf_hero| tf_uruk |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,
   [itm_m_uruk_heavy_c,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_uruk_helm_f,itm_mordor_longsword,itm_mordor_uruk_shield_c,],
      attr_tier_7,wp_tier_6,knight_skills_3,0x000000003f002580204175274345004f00000000001d24380000000000000000],
["knight_2_4","Pharakhâd_The_Bastard","_",tf_hero| tf_evil_man| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_mordor,
   [itm_mordor_warhorse2,itm_black_num_armor,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_mordor_cap_helm,itm_mordor_longsword,itm_mordor_man_shield_b,],
      attr_tier_7,wp_tier_6,knight_skills_4|knows_riding_4,0x0000000f0d0001143586a83dc22382c600000000001cd8e00000000000000000],
["knight_2_5","Grishnakh","_",tf_hero| tf_uruk |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,
   [itm_m_uruk_heavy_c,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_uruk_helm_f,itm_mordor_longsword,itm_mordor_uruk_shield_c,],
      attr_tier_7,wp_tier_6,knight_skills_5,0x00000000260000870038a005c03c5f7000000000000000000000000000000000],
["knight_2_51","Gothmog","Lieutenant",tf_hero| tf_uruk| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,
   [itm_m_uruk_heavy_c,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_uruk_helm_f,itm_mordor_uruk_shield_c,itm_mordor_longsword,],
      attr_tier_7,wp_tier_6,knight_skills_5|knows_persuasion_5|knows_trainer_4,0x000000002c000104003fb3f407b83d0d00000000000000000000000000000000],
#Harad
["knight_2_6","Chieftain_Karna_the_Lion","_",tf_hero| tf_harad| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,
   [itm_harad_warhorse,itm_harad_lion_scale,itm_harad_leather_greaves,itm_evil_gauntlets_a,itm_harad_dragon_helm,itm_harad_khopesh,itm_harad_long_shield_c,],
      attr_tier_7,wp_tier_6,knight_skills_1|knows_riding_4|knows_persuasion_3|knows_trainer_3,0x00000009ff00300b1415a5f77872f7b700000000001d663b0000000000000000],
["knight_2_7","Chieftain_Na’man","_",tf_hero| tf_harad| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,
   [itm_harad_warhorse,itm_harad_heavy,itm_harad_leather_greaves,itm_evil_gauntlets_a,itm_harad_dragon_helm,itm_harad_khopesh,itm_harad_long_shield_c,],
      attr_tier_7,wp_tier_6,knight_skills_2|knows_riding_4|knows_persuasion_3|knows_trainer_4,0x000000003f00000f20a8b7f9e87ff1b700000000001c3ab80000000000000000],
["knight_2_8","Chieftain_Haarith","_",tf_hero| tf_harad| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,
   [itm_harad_warhorse,itm_harad_tiger_scale,itm_harad_leather_greaves,itm_evil_gauntlets_a,itm_harad_dragon_helm,itm_harad_khopesh,itm_harad_long_shield_c,],
      attr_tier_7,wp_tier_6,knight_skills_2|knows_riding_4|knows_persuasion_3|knows_trainer_4,0x000000003f00100421526ff7708d22f700000000001fea200000000000000000],
# ["knight_2_9","Harad_Chieftain","_",tf_hero,0,reserved,fac_harad,[itm_saddle_horse,itm_rich_outfit,itm_mail_hauberk,itm_leather_boots,itm_mail_boots,itm_mail_mittens,itm_two_handed_axe,itm_shield_heater_c],knight_attrib_4,wp(230),knight_skills_4|knows_riding_4,0x0000000c160451d2136469c4d9b159ad00000000001e28f10000000000000000,vaegir_face_older_2],
# ["knight_2_10","Harad_Lieutenant","_",tf_hero,0,reserved,fac_harad,[itm_warhorse,itm_fur_coat,itm_mail_hauberk,itm_leather_boots,itm_mail_boots,itm_mail_mittens,itm_shield_heater_c],knight_attrib_5,wp(260),knight_skills_5|knows_riding_4|knows_trainer_6,0x0000000f7c00520e66b76edd5cd5eb6e00000000001f691e0000000000000000,vaegir_face_older_2],
#Rhun
["knight_2_11","Kusulak","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_horse_g,itm_rhun_armor_k_good,itm_splinted_greaves_good,itm_evil_gauntlets_b_good,itm_rhun_helm_chieftain_good,itm_rhun_greatsword,itm_light_lance,itm_rhun_bull3_shield,],
      attr_tier_7,wp_tier_6,knight_skills_1|knows_riding_7,0x0000000fff0093c213f746f5e363f35b00000000001de22a0000000000000000],
["knight_2_12","Ulwarth the Balchoth","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_horse_e,itm_rhun_armor_p_good,itm_leather_boots_dark,itm_evil_gauntlets_a,itm_rhun_helm_barbed_good,itm_arrows,itm_rhun_bow,itm_rhun_sword,itm_rhun_bull1_shield,],
      attr_tier_7,wp_tier_6,knight_skills_1|knows_power_draw_5|knows_riding_7|knows_horse_archery_6,0x0000000e8000410b145546b3695b677b00000000001ee6aa0000000000000000],
["knight_2_13","Brodda","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_horse_f,itm_rhun_armor_k_good,itm_splinted_greaves_good,itm_evil_gauntlets_b,itm_rhun_helm_chieftain,itm_rhun_greataxe,itm_rhun_sword,itm_rhun_bull3_shield,],
      attr_tier_7,wp_tier_6,knight_skills_1|knows_riding_6,0x0000000c1b007303201c6fd3a36f3ff300000000001d66e80000000000000000],
#Khand
["knight_2_16","Torask","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_khand,
   [itm_khand_inf_helm_d_good,itm_khand_noble_lam,itm_splinted_greaves_good,itm_evil_gauntlets_a_good,itm_khand_2h_tulwar,itm_khand_trident,itm_javelin, itm_javelin,],
      attr_tier_7,wp_tier_6,knight_skills_1|knows_athletics_4|knows_power_throw_6,0x0000000ac800d5400bf7d3f5fb9179ff00000000001f62fc0000000000000000],
["knight_2_17","Lurmsakun","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_khand,
   [itm_variag_kataphrakt,itm_khand_cav_helm_c,itm_khand_noble_lam,itm_splinted_greaves_good,itm_evil_gauntlets_b_good,itm_khand_lance,itm_khand_rammace,itm_easterling_round_horseman],
      attr_tier_7,wp_tier_6,knight_skills_1|knows_riding_6|knows_horse_archery_3,0x0000000d3f00c40812065fd328ff7bfc00000000001ce6b80000000000000000],
#Umbar
["knight_3_1","Captain_Morbir","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_umbar,
   [itm_umb_armor_f_good,itm_corsair_boots,itm_leather_gloves_good,itm_umb_helm_b_good,itm_corsair_bow,itm_corsair_arrows,itm_kraken,],
      attr_tier_7,wp_tier_6,knight_skills_1|knows_trainer_3|knows_power_draw_4,0x0000000eb10063c8365369b99b6f77df00000000001d5aeb0000000000000000],
["knight_3_2","Captain_Angamaitë","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_umbar,
   [itm_umb_armor_f,itm_splinted_greaves,itm_evil_gauntlets_a,itm_umb_helm_a_good,itm_corsair_harpoon,itm_corsair_harpoon,itm_umbar_cutlass,itm_umb_shield_d,],
      attr_tier_7,wp_tier_6,knight_skills_2|knows_power_throw_7,0x000000093f0035c5300251e9b3e041df00000000001cfaeb0000000000000000],
["knight_3_3","Captain_Sangahyando","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_umbar,
   [itm_umb_armor_e_good,itm_corsair_boots,itm_leather_gloves_reward,itm_umb_helm_a,itm_corsair_bow,itm_corsair_arrows,itm_umbar_pike,],
      attr_tier_7,wp_tier_6,knight_skills_2|knows_power_draw_6,0x000000093f004045300251e9b3e2f7df00000000001dbaab0000000000000000],
#Lothlorien
["knight_3_6","Haldir","_",tf_hero| tf_lorien| tf_mounted| tfg_ranged |tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_lorien,
   [itm_lorien_heavy_good_cloak,itm_riv_tiara,itm_lorien_boots,itm_leather_gloves_reward,itm_lorien_bow,itm_elven_arrows,itm_lorien_sword_c,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_3|knows_persuasion_7|knows_power_draw_4,0x00000006470010023b1d6e351240e36d00000000001cd8ec0000000000000000],
["knight_3_7","Orophin","_",tf_hero| tf_lorien| tf_mounted| tfg_ranged |tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_lorien,
   [itm_lorien_heavy_good_cloak,itm_hood_grey_good,itm_lorien_boots,itm_leather_gloves,itm_lorien_bow,itm_elven_arrows,itm_lorien_sword_a,itm_lorien_round_shield],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_1|knows_power_draw_4|knows_persuasion_7,0x00000006470010023b1d6e351240e36d00000000001cd8ec0000000000000000],
#Imladris
["knight_3_11","Elladan","_",tf_hero| tf_imladris| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_imladris,
   [itm_mearas_reward,itm_riv_tiara,itm_riv_armor_leader,itm_riv_boots,itm_leather_gloves_reward,itm_lorien_bow_reward,itm_elven_arrows,itm_riv_archer_sword,itm_riv_shield_b],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_1|knows_riding_5|knows_persuasion_5|knows_power_draw_4|knows_horse_archery_6,0x000000067f0030021ae66e471560632400000000001c58f20000000000000000],
["knight_3_12","Elrohir","_",tf_hero| tf_imladris| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_imladris,
   [itm_mearas_reward,itm_riv_tiara,itm_riv_armor_leader,itm_riv_boots,itm_leather_gloves_good,itm_lorien_bow_reward,itm_elven_arrows,itm_riv_bas_sword,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_2|knows_riding_5|knows_persuasion_5|knows_power_draw_4|knows_horse_archery_6,0x00000003fa0030063d256e471644555c00000000001ce8720000000000000000],
["knight_3_13","Halbarad","_",tf_hero| tf_dunedain| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_imladris,
   [itm_arnor_greaves,itm_mail_mittens,itm_lance,itm_arnor_armor_f,itm_arnor_sword_c,itm_arnor_shield_c,itm_dunedain_helm_b,itm_arnor_warhorse,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_2|knows_riding_5|knows_persuasion_7|knows_power_draw_4,0x00000008a400224736db6db75b6db6db00000000001db6db0000000000000000],
#Woodelves
["knight_3_16","Miriel","_",tf_hero| tf_female| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_woodelf,
   [itm_riv_tiara,itm_mirkwood_mail_good,itm_mirkwood_boots,itm_evil_gauntlets_a,itm_mirkwood_helm_d,itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_axe,itm_mirkwood_spear_shield_c,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_1|knows_persuasion_7|knows_power_draw_6,0x0000000fc000400c055d7066cb87e08300000000001d44c30000000000000000],
["knight_3_17","Gladvaethor","_",tf_hero| tf_woodelf| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_woodelf,
   [itm_riv_tiara,itm_mirkwood_mail_good,itm_mirkwood_boots,itm_leather_gloves_good,itm_mirkwood_helm_d_good,itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_spear_shield_c,itm_mirkwood_war_spear],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_1|knows_persuasion_7|knows_power_draw_6,0x0000000fc00030023fc36db75b6ab6db00000000001d36db0000000000000000],
#Moria
["knight_4_1","Whip_Snog","_",tf_hero| tf_orc| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_moria,
   [itm_wargarmored_3a,itm_moria_armor_e,itm_orc_beakhelm_lordly,itm_orc_greaves,itm_evil_gauntlets_a,itm_orc_throwing_axes,itm_orc_slasher,],
      attr_tier_7,wp_orc_tier_6,knight_skills_1|knows_riding_4|knows_persuasion_3|knows_leadership_10|knows_tactics_8,0x0000000fff00100936db6db6db6db6db00000000001db6db0000000000000000],
["knight_4_2","Whip_Snotgor","_",tf_hero| tf_orc| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_moria,
   [itm_wargarmored_3a,itm_moria_armor_e,itm_orc_bughelm_lordly,itm_orc_greaves,itm_evil_gauntlets_a,itm_orc_javelin,itm_orc_slasher,],
      attr_tier_7,wp_orc_tier_6,knight_skills_1|knows_riding_4|knows_leadership_10|knows_persuasion_3|knows_tactics_8,0x000000087f00000e36db6db6db6db6db00000000001db6db0000000000000000],
#Dol Guldur
["knight_4_6","General_Tuskim","_",tf_hero| tf_uruk |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_guldur,
   [itm_m_uruk_heavy_c,itm_uruk_chain_greaves,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_uruk_helm_f,itm_mordor_uruk_shield_c,itm_mordor_longsword,],
      attr_tier_7,wp_tier_6,knight_skills_2|knows_trainer_4|knows_leadership_10,0x000000018000210700389ff43fdbff4500000000000000000000000000000000],
["knight_4_7","General_Mugslag","_",tf_hero| tf_uruk |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_guldur,
   [itm_m_uruk_heavy_c,itm_uruk_chain_greaves,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_uruk_helm_f,itm_mordor_uruk_shield_c,itm_mordor_longsword,],
      attr_tier_7,wp_tier_6,knight_skills_2|knows_trainer_4|knows_persuasion_3|knows_leadership_10,0x00000001800011c4003f1c65b8cdb6db00000000000000000000000000000000],
#Northmen
["knight_4_11","Ruel","_",tf_hero| tf_female| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,
   [itm_woodmen_heavy_cloak,itm_hood_leather,itm_leather_boots_reward,itm_evil_gauntlets_a,itm_2_handed_axe,itm_elven_bow,itm_arrows,],
      attr_tier_7,wp_tier_6,knight_skills_1|knows_persuasion_6,0x0000000d3f002001134a4a52a34a474b00000000001db6da0000000000000000],
["knight_4_12","Beranor_Blackfur","_",tf_hero |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,
   [itm_beorn_chief,itm_furry_boots,itm_leather_gloves,itm_beorn_helmet,itm_beorn_shield_reward,itm_rohirrim_throwing_axe,itm_rohirrim_throwing_axe,itm_beorn_axe_reward,],
      attr_tier_7,wp_tier_6,knight_skills_1|knows_persuasion_6,0x0000000bbf0052894dd95757a55accff00000000001d29190000000000000000],
#Mt. Gundabad
["knight_4_16","Whip_Brolgukhsh","_",tf_hero| tf_orc| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gundabad,
   [itm_warg_reward,itm_gundabad_armor_e,itm_orc_greaves,itm_orc_ragwrap,itm_evil_gauntlets_a,itm_gundabad_helm_e,itm_orc_throwing_axes,itm_orc_slasher,],
      attr_tier_7,wp_orc_tier_6,knight_skills_1|knows_riding_4|knows_leadership_10|knows_persuasion_3|knows_tactics_8,0x0000000fc000000536db6db6db6db6db00000000001db6db0000000000000000],
["knight_4_17","Whip_Grumrunt","_",tf_hero| tf_orc| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gundabad,
   [itm_wargarmored_3a,itm_gundabad_armor_e,itm_orc_greaves,itm_orc_ragwrap,itm_evil_gauntlets_a,itm_gundabad_helm_e,itm_orc_throwing_axes,itm_orc_slasher,],
      attr_tier_7,wp_orc_tier_6,knight_skills_1|knows_riding_4|knows_leadership_10|knows_persuasion_3|knows_tactics_8,0x00000009bf00000736db6db6db6db6db00000000001db6db0000000000000000],
["knight_4_18","Whip_Grimsob","_",tf_hero| tf_orc| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gundabad,
   [itm_wargarmored_3a,itm_gundabad_armor_e,itm_orc_greaves,itm_orc_ragwrap,itm_evil_gauntlets_a,itm_gundabad_helm_e,itm_orc_throwing_axes,itm_orc_slasher,],
      attr_tier_7,wp_orc_tier_6,knight_skills_1|knows_riding_4|knows_leadership_10|knows_persuasion_3|knows_tactics_8,0x000000083f00200a36db6db6db6db6db00000000001db6db0000000000000000],
#Dale
["knight_5_1","Lord_Halward","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_dale,
   [itm_dale_warhorse,itm_dale_heavy_c_good,itm_splinted_greaves_good,itm_leather_gloves,itm_north_nasal_helm_good,itm_dale_sword_long,itm_beorn_shield,itm_javelin, itm_javelin],
      attr_tier_7,wp_tier_6,knight_skills_1|knows_riding_4|knows_trainer_3|knows_horse_archery_5|knows_power_throw_6,0x00000005e30024852ad48e24d660d52d00000000001d46ab0000000000000000],
["knight_5_2","Lord_Bard","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_dale,
   [itm_dale_armor_reward,itm_splinted_greaves_good,itm_leather_gloves_reward,itm_dale_helmet_e,itm_dale_sword_long,itm_dale_shield_c,itm_dale_bow,itm_black_arrows_reward],
      attr_tier_7,wp_tier_6,knight_skills_2|knows_power_draw_7|knows_trainer_3,0x000000063f00004336db75b7ab6eb6b400000000001db6eb0000000000000000],
["knight_5_3","Lord_Esgarain","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_dale,
   [itm_dale_heavy_b_pelt,itm_splinted_greaves_good,itm_mail_mittens,itm_dale_helmet_c_good,itm_dale_sword_long,itm_dale_shield_b,],
      attr_tier_7,wp_tier_6,knight_skills_1|knows_trainer_3|knows_shield_7,0x00000008ef00008436db76b7ab6ef6b400000000001d26eb0000000000000000],
#Dwarven
["knight_5_6","Fulgni_Longbeard","_",tf_hero| tf_dwarf| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_armor_b_lordly,itm_dwarf_scale_boots,itm_mail_mittens,itm_dwarf_helm_king_NPC,itm_dwarf_throwing_axe,itm_dwarf_great_axe,],
      attr_dwarf_tier_6,wp_dwarf_tier_6,knows_riding_10|knows_persuasion_3|knight_skills_1|knows_riding_4,0x00000001b000014258e46ec7d780e9fe00000000001ce4710000000000000000],
["knight_5_7","Thorin_Stonehelm","_",tf_hero| tf_dwarf| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_armor_c_lordly,itm_dwarf_scale_boots,itm_mail_mittens,itm_dwarf_helm_king_NPC,itm_dwarf_throwing_axe,itm_dwarf_great_axe,],
      attr_dwarf_tier_6,wp_dwarf_tier_6,knows_riding_10|knows_persuasion_3|knight_skills_1|knows_riding_4,0x00000009bf00510616936b596c56ddfe00000000001ecc780000000000000000],
#Dunland
["knight_5_11","Chief_Fudreim","_",tf_hero| tf_dunland| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_dunland,
   [itm_dunland_armor_k,itm_dunland_wolfboots,itm_dunland_wolfboots,itm_evil_gauntlets_a,itm_dun_helm_e,itm_dun_berserker,itm_dun_shield_b,itm_dunland_javelin,],
      attr_tier_7,wp_tier_6,knight_skills_1,0x0000000cbf00528736db6db71b6db6db00000000001fd6db0000000000000000],
["knight_5_12","Chief_Wulf","_",tf_hero| tf_dunland| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_dunland,
   [itm_dunland_armor_k,itm_dunland_wolfboots,itm_dunland_wolfboots,itm_evil_gauntlets_a,itm_dun_helm_e,itm_dun_berserker,itm_dun_shield_b,itm_dunland_javelin,],
      attr_tier_7,wp_tier_6,knight_skills_1|knows_persuasion_5,0x0000000e3b00324305f858f1606bbfff00000000001f7ce80000000000000000],

## Kham - New Gondor Lord
["knight_6_1","Dervorin","_",tf_hero| tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,
   [itm_lamedon_leader_surcoat_cloak,itm_loss_war_axe,itm_gondor_heavy_greaves,itm_gon_tab_shield_c,itm_mail_mittens,itm_gondor_infantry_helm_bad,itm_loss_throwing_axes],
      attr_tier_5,wp_tier_5,gondor_skills_2|knows_power_throw_5|knows_persuasion_5|knows_shield_9,0x0000000340003004250c85a90f6868f500000000001ed96a0000000000000000],

# <--- swy: heroes_end --->
      
# Kham - move commented out healers to the end

# Weapon merchants
["smith_mtirith","Berethor_the_Smith","Steward's_smiths",tf_hero|  tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x00000007e00065862d1566ab1a40db6d00000000001eeab10000000000000000],
["smith_pelargir","Hallatan_Metalmaster","smithy",tf_hero|  tf_is_merchant| tf_gondor,0,subfac_pelargir,fac_gondor,
   [itm_leather_apron,itm_pelargir_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000b280080ca72a47aeae58d299400000000001d52a80000000000000000],
["smith_linhir","Bor_the_Armorer","smithy",tf_hero|  tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000dd300b180680c4c92da4e492a00000000001e35290000000000000000],
["smith_dolamroth","Haldad_the_Smith","Amroth_smiths",tf_hero|  tf_is_merchant| tf_gondor,0,subfac_dol_amroth,fac_gondor,
   [itm_leather_apron,itm_dol_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x00000009a80015c05e95356d94a75cd500000000001edae90000000000000000],
["smith_edhellond","Ryis_Ironbender","smithy",tf_hero|  tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x000000002a00355304ab85434cc6cdd500000000001e52a80000000000000000],
["smith_lossarnach","Berin_Axemaker","smithy",tf_hero|  tf_is_merchant| tf_gondor,0,subfac_lossarnach,fac_gondor,
   [itm_leather_apron,itm_lossarnach_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x00000006e70062055e94552f1d3f576a00000000001e49300000000000000000],
["smith_tarnost","Harandil_Steelhammer","smithy",tf_hero|  tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x00000002bf00514a125a56da95d9259500000000001d95100000000000000000],
["smith_erech","Lorne_the_Black","smithy",tf_hero|  tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x00000004bf00600855720ed264855b7100000000001d55210000000000000000],
["smith_pinnath","Tarandil_Swordmaker","smithy",tf_hero|  tf_is_merchant| tf_gondor,0,subfac_pinnath_gelin,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x00000007ff0085c7556456942fab291500000000001e45710000000000000000],
["smith_eosgiliath","Bzurg_the_Looter","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_mordor,
   [itm_m_orc_light_e,itm_orc_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,orc_face_normal,orc_face2],
["smith_wosgiliath","Gardil","makeshift_smithy",tf_hero|  tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x00000005a20004cf2a545a466d45d92e00000000001db2f00000000000000000],
["smith_calembel","Agronom","smithy",tf_hero|  tf_is_merchant| tf_gondor,0,subfac_ethring,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x00000005a20014461ca254c85738eaa500000000001ec4a90000000000000000],
["smith_hannun","Fal_the_Ranger_Smith","ranger_gear_stash",tf_hero|  tf_is_merchant,0,subfac_rangers,fac_gondor,
   [itm_gon_ranger_cloak,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x00000007ff002143551359c91985379500000000001e44a90000000000000000],
["smith_candros","Kalimdor","smithy",tf_hero|  tf_is_merchant,0,0,fac_gondor,
   [itm_gon_footman,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_1|knows_power_strike_1|knows_persuasion_1|knows_horse_archery_1|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000c6a003181551359c90885379600000000001ed4a90000000000000000],
["smith_edoras","Eaoden_Steelmaster","King's_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_mail,itm_rohan_shoes,],
      attr_tier_3|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x00000008c80002c219248896a4b96b6300000000001e1af30000000000000000],
["smith_aldburg","Fulm_Ironhoof","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_mail,itm_rohan_shoes,],
      attr_tier_3|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000a22002341375b72ab4c6aba6500000000001f24e20000000000000000],
["smith_hornburg","Aldhelm","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_mail,itm_rohan_shoes,],
      attr_tier_3|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000a35003183479c6e12548f451400000000001f355e0000000000000000],
["smith_eastemnet","Eadfrid","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_mail,itm_rohan_shoes,],
      attr_tier_3|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000a10002282392cc9172d8dbb1b00000000001caa9d0000000000000000],
["smith_westfold","Deor_Helmmaker","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_mail,itm_rohan_shoes,],
      attr_tier_3|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000a100011c4444395aaec92c4c400000000001db6cd0000000000000000],
["smith_westemnet","Armourer","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_leather,itm_rohan_shoes,],
      attr_tier_3|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000a3b000281451d364924d5571400000000001e46a30000000000000000],
["smith_eastfold","Eaderan_Ironcarver","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_leather,itm_rohan_shoes,],
      attr_tier_3|level(2),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000a170000c12b1b8f499892995b00000000001e68e90000000000000000],
["smith_morannon","Hurbag_Gateforger","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_a,itm_uruk_greaves,],
      attr_tier_3|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,orc_face_normal,orc_face2],
["smith_mmorgul","Orgurz_Firebelcher","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_a,itm_uruk_ragwrap,],
      attr_tier_3|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,orc_face_normal,orc_face2],
["town_24_smith","Boz_Ironspoiler","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_mordor,
   [itm_m_uruk_light_b,itm_orc_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,orc_face_normal,orc_face2],
["smith_orc_patrol","Glugz_Ironfinger","camp_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_a,itm_uruk_tracker_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,orc_face_normal,orc_face2],
["smith_oscamp","Kugash_Ironlover","camp_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_a,itm_uruk_tracker_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,orc_face_normal,orc_face2],
["smith_isengard","Burz_Ironbasher","underground_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_light_c,itm_uruk_tracker_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_uoutpost","Gurzuk_Irontooth","outpost_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_light_c,itm_uruk_tracker_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_uhcamp","Rabzug_Rusteater","camp_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_light_c,itm_uruk_tracker_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_urcamp","Glurk","camp_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_light_c,itm_uruk_tracker_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_cgaladhon","Dirufin the Bowyer","elven_weaponmakers",tf_hero| tf_randomize_face| tf_is_merchant| tf_lorien,0,0,fac_lorien,
   [itm_lorien_archer,itm_lorien_boots,],
      def_attrib|level(2),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,lorien_elf_face_1,lorien_elf_face_2],
["smith_cdolen","Dimirian the Fletcher","elven_weaponmakers",tf_hero| tf_randomize_face| tf_is_merchant| tf_lorien,0,0,fac_lorien,
   [itm_lorien_archer,itm_lorien_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,lorien_elf_face_1,lorien_elf_face_2],
["smith_camroth","Getasistan","elven_weaponmakers",tf_hero| tf_randomize_face| tf_is_merchant| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_a,itm_lorien_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,lorien_elf_face_1,lorien_elf_face_2],
["smith_thranduils_halls","Thurinor","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_pad,itm_mirkwood_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,lorien_elf_face_1,lorien_elf_face_2],
["smith_woodelf_camp","Calechir","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_pad,itm_mirkwood_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,lorien_elf_face_1,lorien_elf_face_2],
["smith_beorn","Beornalaf_Axemaker","smithy",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_beorn,
   [itm_beorn_tunic,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_moria","Burgak_Forger","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_moria,
   [itm_moria_armor_b,itm_orc_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_dale","Ardel_Firehand","smithy",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_dale,
   [itm_dale_light_a,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_esgaroth","Kelegarn_The_Bowyer","smithy",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_dale,
   [itm_dale_light_a,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_erebor","Thror_the_Hammerer","praised_Dwarven_smiths",tf_hero| tf_randomize_face| tf_is_merchant| tf_dwarf,0,0,fac_dwarf,
   [itm_leather_dwarf_armor_b,itm_dwarf_pad_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,dwarf_face_3,dwarf_face_4],
["smith_dunland","Dorrowuld_Ironpike","smithy",tf_hero| tf_dunland| tf_is_merchant,0,0,fac_dunland,
   [itm_dunland_armor_h,itm_dunland_wolfboots,],
      def_attrib|level(2),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000cbf00624636db6db71b6db6db00000000001ec2db0000000000000000],
["smith_harad","Har_Steelbender","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_harad,0,0,fac_harad,
   [itm_harad_padded,itm_harad_scale_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_khand","Pushurt_The_Haggler","smithy",tf_hero| tf_is_merchant| tf_evil_man,0,0,fac_khand,
   [itm_khand_light_lam,itm_splinted_greaves_good,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000fff00d45213f7e6f1636172fb00000000001dc22a0000000000000000],
["smith_umbar","Fuinir_the_Forger","smithy",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_umbar,
   [itm_umb_armor_e,itm_corsair_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_imladris","Duifirian","elven_weaponmakers",tf_hero| tf_randomize_face| tf_is_merchant| tf_imladris,0,0,fac_imladris,
   [itm_riv_armor_light,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,rivendell_elf_face_1,rivendell_elf_face_2],
["smith_dolguldur","Shtazg_Dulbash","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_a,itm_uruk_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_north_rhun","Ognjemir_Kladivo","makeshift_smithy",tf_hero| tf_is_merchant| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_armor_j,itm_furry_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x000000098000440b128d9bf9db39725f00000000001d75390000000000000000],
["smith_gundabad","Blurg_Snowseller","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_c,itm_orc_furboots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_ironhill","Ironhill_Smith","Dwarven_camp_smiths",tf_hero| tf_randomize_face| tf_is_merchant| tf_dwarf,0,0,fac_dwarf,
   [itm_dwarf_vest_b,itm_dwarf_chain_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,dwarf_face_3,dwarf_face_4],
["town_50_weaponsmith","Shruklug_Knife_Grinder","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_c,itm_orc_furboots,itm_gundabad_helm_a],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],

["smith_gondor_ac","Bor_the_Armorer","camp_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_rohan_ac","Deor_Helmmaker","camp_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_leather,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_mordor_ac","Hurbag_Gateforger","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_a,itm_uruk_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,orc_face_normal,orc_face2],
["smith_isengard_ac","Burz_Ironbasher","underground_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_light_c,itm_uruk_tracker_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_lorien_ac","Dimirian the Fletcher","elven_weaponmakers",tf_hero| tf_randomize_face| tf_is_merchant| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_c,itm_lorien_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,lorien_elf_face_1,lorien_elf_face_2],
["smith_woodelf_ac","Dhoelath","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_pad,itm_mirkwood_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,lorien_elf_face_1,lorien_elf_face_2],
["smith_dwarf_ac","Ironhill_Smith","Dwarven_camp_smiths",tf_hero| tf_randomize_face| tf_is_merchant| tf_dwarf,0,0,fac_dwarf,
   [itm_dwarf_vest_b,itm_dwarf_chain_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,dwarf_face_3,dwarf_face_4],
["smith_gundabad_ac","Blurg_Snowseller","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_c,itm_orc_furboots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_rhun_ac","Branimir_Bronnik","makeshift_smithy",tf_hero| tf_is_merchant| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_armor_j,itm_furry_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x000000098000440b128d9bf9db39725f00000000001d75390000000000000000],
["smith_guldur_ac","Shtazg_Dulbash","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_a,itm_uruk_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_imladris_ac","Duifirian","elven_weaponmakers",tf_hero| tf_randomize_face| tf_is_merchant| tf_imladris,0,0,fac_imladris,
   [itm_riv_armor_light,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,rivendell_elf_face_1,rivendell_elf_face_2],
["smith_dunland_ac","Dorrowuld_Ironpike","smithy",tf_hero| tf_dunland| tf_is_merchant,0,0,fac_dunland,
   [itm_dunland_armor_h,itm_dunland_wolfboots,],
      def_attrib|level(2),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000cbf00624636db6db71b6db6db00000000001ec2db0000000000000000],
["smith_harad_ac","Har_Steelbender","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_harad,0,0,fac_harad,
   [itm_harad_padded,itm_harad_scale_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_khand_ac","Pushurt_The_Haggler","smithy",tf_hero| tf_is_merchant| tf_evil_man,0,0,fac_khand,
   [itm_khand_light_lam,itm_splinted_greaves_good,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000fff00d45213f7e6f1636172fb00000000001dc22a0000000000000000],
["smith_umbar_ac","Fuinir_the_Forger","smithy",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_umbar,
   [itm_umb_armor_e,itm_corsair_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],

#missing smiths (replacing tavern keepers)
["smith_moria_ac","Burgak_Forger","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_moria,
   [itm_moria_armor_b,itm_orc_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_dale_ac","Ardel_Firehand","smithy",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_dale,
   [itm_dale_light_a,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_beorn_ac","Beornalaf_Axemaker","smithy",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_beorn,
   [itm_beorn_tunic,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],

["smith_woodelf_west_camp","Dhoelath","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_pad,itm_mirkwood_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,lorien_elf_face_1,lorien_elf_face_2],
["smith_woodmen","Beornalaf_Axemaker","smithy",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_beorn,
   [itm_beorn_tunic,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_beorn_v","Beornalaf_Axemaker","smithy",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_beorn,
   [itm_beorn_tunic,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_troll_cave","Burgak_Forger","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_moria,
   [itm_moria_armor_b,itm_orc_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_dg_outpost","Shtazg_Dulbash","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_a,itm_uruk_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_main_rhun","Branimir_Bronnik","makeshift_smithy",tf_hero| tf_is_merchant| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_armor_j,itm_furry_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x000000098000440b128d9bf9db39725f00000000001d75390000000000000000],
["smith_south_rhun","Branimir_Bronnik","makeshift_smithy",tf_hero| tf_is_merchant| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_armor_j,itm_furry_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x000000098000440b128d9bf9db39725f00000000001d75390000000000000000],
["smith_gundabad_ne","Blurg_Snowseller","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_c,itm_orc_furboots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_gundabad_nw","Blurg_Snowseller","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_c,itm_orc_furboots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_gundabad_s","Blurg_Snowseller","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_c,itm_orc_furboots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_gundabad_m","Blurg_Snowseller","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_c,itm_orc_furboots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],

#Tavern keepers   # in TLD, their plular name serves as city "Castle" name. #InVain: Not used anymore

["barman_eastemnet","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face| tf_female,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],
["barman_westfold","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_westemnet","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_eastfold","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_baraddur","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face| tf_uruk,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_morannon","Tavern_Keeper","the_Leader's_Cave",tf_hero| tf_randomize_face| tf_uruk,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_mmorgul","Tavern_Keeper","the_Tower",tf_hero| tf_randomize_face| tf_uruk,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],


#Additional merchants      
["merchant_main_rhun","Supply_Master","camp_stash",tf_hero| tf_is_merchant| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_armor_p,itm_furry_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,0x00000009bf00324113fe9bf7ee397d7f00000000001d75390000000000000000],      
["merchant_dg_outpost","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_guldur,
   [itm_m_uruk_light_c,itm_orc_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,man_face_young_1,man_face_older_2],    
["merchant_woodelf_west_camp","Supply_Master","elven_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_pad,itm_mirkwood_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_1,lorien_elf_face_1,lorien_elf_face_2],
["merchant_gundabad_m","Supply_Master","camp_stash",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_d,itm_orc_furboots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_3,man_face_young_1,man_face_older_2],
["merchant_gundabad_s","Supply_Master","camp_stash",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_d,itm_orc_furboots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_3,man_face_young_1,man_face_older_2],
["merchant_gundabad_nw","Supply_Master","camp_stash",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_d,itm_orc_furboots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_3,man_face_young_1,man_face_older_2],
["merchant_gundabad_ne","Supply_Master","camp_stash",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_d,itm_orc_furboots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_3,man_face_young_1,man_face_older_2],
["merchant_troll_cave","Supply_Master","warg_pit_and_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_moria,
   [itm_moria_armor_c,itm_orc_ragwrap,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,man_face_young_1,man_face_older_2],
["merchant_beorn_v","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_beorn,
   [itm_beorn_tunic,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,man_face_young_1,man_face_older_2],
["merchant_orc_sentry","Supply_Master","camp_stash",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_b,itm_orc_ragwrap,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,man_face_young_1,man_face_older_2],
["merchant_candros","Supply_Master","stable_and_warehouse",tf_hero|  tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_gon_footman,itm_gondor_med_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,0x00000009380085944a9c75a8a43224d400000000001d59160000000000000000],
["merchant_hannun","Supply_Master","ranger_supplies",tf_hero|  tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_gon_footman,itm_gondor_med_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,0x00000009380085944a9c75a8a43224d400000000001d59160000000000000000],

#Goods Merchants
#["town_1_merchant","Merchant","bug",tf_hero|tf_randomize_face|tf_is_merchant,scn_town_store|entry(9),0,fac_commoners,[itm_short_tunic,itm_leather_boots                   ],def_attrib|level(2),wp(20),knows_inventory_management_10,man_face_young_1,man_face_older_2],
#["town_2_merchant","Merchant","bug",tf_hero|tf_randomize_face|tf_is_merchant,scn_town_2_store|entry(9),0,fac_commoners,[itm_leather_apron,itm_leather_boots                   ],def_attrib|level(2),wp(20),knows_inventory_management_10,man_face_young_1,man_face_older_2],
#["salt_mine_merchant","Barezan","Barezan",tf_hero|tf_is_merchant,scn_salt_mine|entry(1),0,fac_commoners,[itm_leather_apron,itm_leather_boots],def_attrib|level(2),wp(20),knows_inventory_management_10,0x00000000000c528601ea69b6e46dbdb6],
# Horse Merchants
["merchant_mtirith","Supply_Master","stable_and_warehouse",tf_hero| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_gon_jerkin,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_inventory_management_10|knows_riding_6,0x0000000fff0015d3350d2f495569451500000000001c92d50000000000000000],
["merchant_pelargir","Supply_Master","stable_and_warehouse",tf_hero|  tf_is_merchant| tf_gondor,0,subfac_pelargir,fac_gondor,
   [itm_pel_jerkin,itm_pelargir_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_3,0x00000004c00004c41c9a29e454440b6400000000001e68d10000000000000000 ],
["merchant_linhir","Supply_Master","stable_and_warehouse",tf_hero| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_lamedon_clansman,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,0x000000073f00154529238a97a03f26d300000000001fb9110000000000000000 ],
["merchant_dolamroth","Supply_Master","stable_and_warehouse",tf_hero|  tf_is_merchant| tf_gondor,0,subfac_dol_amroth,fac_gondor,
   [itm_dol_shirt,itm_dol_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_3,0x0000000a7f002006229d76ba1b66375400000000001dd69e0000000000000000],
["merchant_edhellond","Supply_Master","stable_and_warehouse",tf_hero|  tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_gon_jerkin,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,0x000000016e00114652966a4c4b42334d00000000001cd69a0000000000000000],
["merchant_lossarnach","Supply_Master","stable_and_warehouse",tf_hero|  tf_is_merchant| tf_gondor,0,subfac_lossarnach,fac_gondor,
   [itm_lossarnach_shirt,itm_lossarnach_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,0x0000000bee0022912d146aaaa255db6b00000000001eda790000000000000000],
["merchant_tarnost","Supply_Master","stable_and_warehouse",tf_hero|  tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_gon_jerkin,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_5,0x00000005d00030065a5bba28d989db1100000000001f584d0000000000000000 ],
["merchant_erech","Supply_Master","stable_and_warehouse",tf_hero|  tf_is_merchant| tf_gondor,0,subfac_blackroot,fac_gondor,
   [itm_blackroot_bowman,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,0x00000005d000458354c24364319ba36500000000001cdaa50000000000000000 ],
["merchant_pinnath","Supply_Master","stable_and_warehouse",tf_hero|  tf_is_merchant| tf_gondor,0,subfac_pinnath_gelin,fac_gondor,
   [itm_pinnath_footman,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,0x000000053e0075c239645e2a554c9b1500000000001db6db0000000000000000],
["merchant_eosgiliath","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_mordor,
   [itm_m_orc_heavy_a,itm_orc_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_1,man_face_young_1,man_face_older_2],
["merchant_wosgiliath","Supply_Master","stable_and_warehouse",tf_hero|  tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_gon_footman,itm_gondor_med_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,0x00000009380085944a9c75a8a43224d400000000001d59160000000000000000],
["town_12_horse_merchant","Supply_Master","stable_and_warehouse",tf_hero|  tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_gon_jerkin,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,0x0000000bcd00b14f114a1216ac4cb38c00000000001e670c0000000000000000],
["town_13_horse_merchant","Supply_Master","stable_and_warehouse",tf_hero|  tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_lamedon_clansman,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,0x0000000da100251016638629c951452200000000001da68e0000000000000000],
["merchant_edoras","Supply_Maiden","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_female,0,0,fac_rohan,
   [itm_green_dress,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,woman_face_1,woman_face_2],
["merchant_aldburg","Supply_Master","King's_stable_and_warehouse",tf_hero| tf_rohan| tf_is_merchant,0,0,fac_rohan,
   [itm_green_tunic,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,0x0000000a31000301449bfb13a1ae451d00000000001e2ce30000000000000000],
["merchant_hornburg","Supply_Master","stable_and_warehouse",tf_hero| tf_rohan| tf_is_merchant,0,0,fac_rohan,
   [itm_green_tunic,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,0x0000000a3c00424434944a656429591300000000001d38440000000000000000],
["merchant_eastemnet","Supply_Master","stable_and_warehouse",tf_hero| tf_rohan| tf_is_merchant,0,0,fac_rohan,
   [itm_green_tunic,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,0x0000000a220012456aaca2575d5692ab00000000001e48ec0000000000000000],
["merchant_westfold","Supply_Maiden","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_female,0,0,fac_rohan,
   [itm_green_dress,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,woman_face_1,woman_face_2],
["merchant_westemnet","Supply_Maiden","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_female,0,0,fac_rohan,
   [itm_green_dress,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,woman_face_1,woman_face_2],
["merchant_eastfold","Supply_Maiden","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_female,0,0,fac_rohan,
   [itm_green_dress,itm_rohan_shoes,],
      def_attrib|level(2),wp(20),knows_inventory_management_10|knows_riding_6,woman_face_1,woman_face_2],
["town_21_horse_merchant","Supply_Master","pit_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_b,itm_orc_ragwrap,],
      def_attrib|level(2),wp(20),knows_inventory_management_10,man_face_young_1,man_face_older_2],
["merchant_morannon","Supply_Master","pit_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_a,itm_orc_ragwrap,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,man_face_young_1,man_face_older_2],
["merchant_mmorgul","Supply_Master","pit_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_b,itm_orc_ragwrap,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,man_face_young_1,man_face_older_2],
["town_24_horse_merchant","Supply_Master","pit_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_a,itm_orc_ragwrap,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,man_face_young_1,man_face_older_2],
["merchant_orc_patrol","Supply_Master","camp_stash",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_b,itm_orc_ragwrap,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,man_face_young_1,man_face_older_2],
["merchant_isengard","Supply_Master","camp_stash",tf_hero| tf_randomize_face| tf_is_merchant| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_med_a,itm_uruk_ragwrap,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,man_face_young_1,man_face_older_2],
["town_27_horse_merchant","Supply_Master","warg_pit_and_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,man_face_young_1,man_face_older_2],
["merchant_uoutpost","Supply_Master","warg_pit_and_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_med_a,itm_uruk_ragwrap,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_3,man_face_young_1,man_face_older_2],
["merchant_uhcamp","Supply_Master","warg_pit_and_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_3,man_face_young_1,man_face_older_2],
["merchant_urcamp","Supply_Master","warg_pit_and_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,man_face_young_1,man_face_older_2],
["merchant_cgaladhon","Supply_Master","elven_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_a,itm_lorien_boots,],
      def_attrib|level(2),wp(20),knows_inventory_management_10|knows_riding_3,lorien_elf_face_1,lorien_elf_face_2],
["merchant_cdolen","Supply_Master","elven_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_a,itm_lorien_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_1,lorien_elf_face_1,lorien_elf_face_2],
["merchant_camroth","Supply_Master","elven_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_b,itm_lorien_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,lorien_elf_face_1,lorien_elf_face_2],
["merchant_thranduils_halls","Supply_Master","elven_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_pad,itm_mirkwood_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,lorien_elf_face_1,lorien_elf_face_2],
["merchant_woodelf_camp","Supply_Master","elven_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_pad,itm_mirkwood_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_1,lorien_elf_face_1,lorien_elf_face_2],
["merchant_woodmen","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_beorn,
   [itm_beorn_tunic,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,man_face_young_1,man_face_older_2],
["merchant_beorn","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_beorn,
   [itm_beorn_tunic,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,man_face_young_1,man_face_older_2],
["merchant_moria","Supply_Master","warg_pit_and_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_moria,
   [itm_moria_armor_c,itm_orc_ragwrap,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,man_face_young_1,man_face_older_2],
["merchant_dale","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_dale,
   [itm_fur_coat,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,man_face_young_1,man_face_older_2],
["merchant_esgaroth","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_dale,
   [itm_dale_light_a,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,man_face_young_1,man_face_older_2],
["merchant_erebor","Supply_Master","Dwarven_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_dwarf,0,0,fac_dwarf,
   [itm_dwarf_armor_a,itm_dwarf_pad_boots,],
      attr_dwarf_tier_3|level(5),wp(20),knows_inventory_management_10|knows_riding_1,man_face_young_1,man_face_older_2],
["merchant_dunland","Dun_Stash_Master","camp_stash",tf_hero| tf_dunland| tf_is_merchant,0,0,fac_dunland,
   [itm_dunland_armor_h,itm_dunland_wolfboots,],
      def_attrib|level(2),wp(20),knows_inventory_management_10|knows_riding_2,0x000000003f00520137da6c7bd86f36db00000000001e42f80000000000000000],
["merchant_harad","Harad_Stash_Master","camp_stash",tf_hero| tf_randomize_face| tf_is_merchant| tf_harad,0,0,fac_harad,
   [itm_harad_padded,itm_harad_scale_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_4,man_face_young_1,man_face_older_2],
["merchant_khand","Khand_Stash_Master","camp_stash",tf_hero| tf_is_merchant| tf_evil_man,0,0,fac_khand,
   [itm_khand_foot_lam,itm_splinted_greaves_good,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_3,0x0000000fff0093c213f746f5e363f35b00000000001de22a0000000000000000],
["merchant_umbar","Supply_Master","camp_stash",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_umbar,
   [itm_umb_armor_a,itm_corsair_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_1,man_face_young_1,man_face_older_2],
["merchant_imladris","Supply_Master","camp_supplies",tf_hero| tf_is_merchant,0,0,fac_imladris,
   [itm_arnor_armor_c,itm_arnor_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,0x0000000af700414719da9135148aa8d300000000001db9110000000000000000],
["merchant_dolguldur","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_guldur,
   [itm_m_uruk_light_c,itm_orc_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,man_face_young_1,man_face_older_2],
["merchant_north_rhun","Supply_Master","camp_stash",tf_hero| tf_is_merchant| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_armor_p,itm_furry_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,0x00000009bf00324113fe9bf7ee397d7f00000000001d75390000000000000000],
["merchant_south_rhun","Supply_Master","camp_stash",tf_hero| tf_is_merchant| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_armor_p,itm_furry_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,0x000000092c00528839fe9b55db52f37f00000000001ee73b0000000000000000],
["merchant_gundabad","Supply_Master","camp_stash",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_d,itm_orc_furboots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,man_face_young_1,man_face_older_2],
["merchant_ironhill","Supply_Master","Dwarven_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_dwarf,0,0,fac_dwarf,
   [itm_dwarf_armor_a,itm_dwarf_pad_boots,],
      attr_dwarf_tier_3|level(5),wp(20),knows_inventory_management_10|knows_riding_1,dwarf_face_3,dwarf_face_4],
["town_50_horse_merchant","Gobrip_Yellowtooth","warg_pit_and_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_c,itm_orc_furboots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,man_face_young_1,man_face_older_2],
["merchant_calembel","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,subfac_ethring,fac_gondor,
   [itm_lamedon_clansman,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,man_face_young_1,man_face_older_2],
#
["elder_mtirith","Tirith_Guildmaster","the_White_City",tf_hero| tf_gondor ,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,0x0000000fe4008014251a46da6d04539500000000001d530e0000000000000000],
["elder_pelargir","Sailor_Guildmaster","the_city",tf_hero| tf_gondor ,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_pelargir_greaves,],
      def_attrib|level(2),wp(20),knows_common,0x0000000fff0015d214ea3905525ad6ad00000000001e41090000000000000000],
["elder_linhir","Linhir_Guildmaster","the_city",tf_hero| tf_gondor ,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,0x0000000e6c00258a1cea4a386530c6cb00000000001dc9110000000000000000],
["elder_dolamroth","Dol_Amroth_Guildmaster","the_city",tf_hero| tf_gondor ,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_dol_shoes,],
      def_attrib|level(2),wp(20),knows_common,0x0000000fe800a14612912a2a63252b5600000000001d52d10000000000000000],
["elder_edhellond","Edhellond_Guildmaster","the_city",tf_hero| tf_gondor ,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,0x0000000e1a00018722918a2a63192b5600000000001cd06e0000000000000000],
["elder_lossarnach","Lossarnach_Guildmaster","the_town",tf_hero| tf_gondor ,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,0x0000000d5a00228232986a2b2d15bb5600000000001e30b80000000000000000],
["elder_tarnost","Tarnost_Guildmaster","the_town",tf_hero| tf_gondor ,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,0x0000000fc00032c018284a2b05117b5600000000001ff0fb0000000000000000],
["elder_erech","Erech_Guildmaster","the_town",tf_hero| tf_gondor ,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,0x0000000fc000438006b15622571369aa00000000001ef3280000000000000000],
["elder_pinnath","Pinnath_Tribe_Elder","the_town",tf_hero| tf_gondor ,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,0x0000000e7f0054111b605b4a89b6259000000000001f28e90000000000000000],
["elder_ethring","Calembel_Guildmaster","the_city",tf_hero| tf_gondor ,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,0x0000000c3f0080d01c92591891b70cc900000000001ed52e0000000000000000],
["elder_henneth","Ranger_Guildmaster","the_hideout",tf_hero| tf_gondor ,0,0,fac_gondor,
   [itm_gon_ranger_skirt,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,0x0000000c3f00208812934638aa24db5e00000000001d52ee0000000000000000],
["elder_cairandros","Cair_Andros_Guildmaster","the_island_fortress",tf_hero| tf_gondor ,0,0,fac_gondor,
   [itm_gon_ranger_skirt,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,0x0000000fff00340418594ad88aa7631100000000001d46b60000000000000000],
["elder_edoras","Edoras_Thain","the_city",tf_hero| tf_rohan,0,0,fac_rohan,
   [itm_rohan_fine_outfit_dale_dress,itm_rohan_shoes,],
      def_attrib|level(2),wp(20),knows_common,0x0000000a0e00330226db69d9abb6271300000000001c45130000000000000000],
["elder_aldburg","Aldburg_Thain","the_town",tf_hero| tf_rohan,0,0,fac_rohan,
   [itm_rohan_fine_outfit_dale_dress,itm_rohan_shoes,],
      def_attrib|level(2),wp(20),knows_common,0x0000000a2a0002c326c66a695e8e74f300000000001eeb230000000000000000],
["elder_hornburg","Hornburg_Thain","the_fortress",tf_hero| tf_rohan,0,0,fac_rohan,
   [itm_rohan_fine_outfit_dale_dress,itm_rohan_shoes,],
      def_attrib|level(2),wp(20),knows_common,0x0000000a040021414ce3915792b2ab2200000000001ce7150000000000000000],
["elder_eastemnet","East_Emnet_Thain","the_town",tf_hero| tf_rohan,0,0,fac_rohan,
   [itm_rohan_fine_outfit_dale_dress,itm_rohan_shoes,],
      def_attrib|level(2),wp(20),knows_common,0x0000000a10000341472366aae58ed89400000000001caccb0000000000000000],
["elder_westfold","Westfold_Thain","the_town",tf_hero| tf_rohan,0,0,fac_rohan,
   [itm_rohan_fine_outfit_dale_dress,itm_rohan_shoes,],
      def_attrib|level(2),wp(20),knows_common,0x0000000a3d00410526cbb1c71269cadb00000000001d368a0000000000000000],
["elder_westemnet","West_Emnet_Thain","the_town",tf_hero| tf_rohan,0,0,fac_rohan,
   [itm_rohan_fine_outfit_dale_dress,itm_rohan_shoes,],
      def_attrib|level(2),wp(20),knows_common,0x0000000a1d0021c546cb672932eea69e00000000001eb95b0000000000000000],
["elder_eastfold","Eastfold_Thain","the_town",tf_hero| tf_rohan,0,0,fac_rohan,
   [itm_rohan_fine_outfit_dale_dress,itm_rohan_shoes,],
      def_attrib|level(2),wp(20),knows_common,0x0000000a0d0042c1556a8547648b34e400000000001d56d50000000000000000],
["elder_morannon","Morannon_Chief","the_caves_overlooking_the_Great_Gate",tf_hero| tf_randomize_face| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_mmorgul","Morgul_Chief","the_sinister_city",tf_hero| tf_randomize_face| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_cungol","Camp_Chief","the_camp",tf_hero| tf_randomize_face| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_isengard","Grima_Wormtongue","the_city",tf_hero| tf_evil_man,0,0,fac_isengard,
   [itm_evil_light_armor,itm_leather_boots_dark_bad,],
      def_attrib|level(2),wp(20),knows_common,0x000000003f0000032038a06b587590c500000000001d3a880000000000000000],
["elder_cgaladhon","Lorien Loremaster","the_elven_forest_fortress",tf_hero| tf_randomize_face| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_c,itm_lorien_boots,],
      def_attrib|level(2),wp(20),knows_common,lorien_elf_face_1,lorien_elf_face_2],
["elder_cdolen","Lorien Loremaster","the_encampment",tf_hero| tf_randomize_face| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_c,itm_lorien_boots,],
      def_attrib|level(2),wp(20),knows_common,lorien_elf_face_1,lorien_elf_face_2],
["elder_camroth","Lorien Loremaster","the_encampment",tf_hero| tf_randomize_face| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_c,itm_lorien_boots,],
      def_attrib|level(2),wp(20),knows_common,lorien_elf_face_1,lorien_elf_face_2],
["elder_thalls","Mirkwood_Elder","the_elven_caves",tf_hero| tf_randomize_face| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_leather,itm_mirkwood_boots,],
      def_attrib|level(2),wp(20),knows_common,lorien_elf_face_1,lorien_elf_face_2],
["elder_imladris","Rivendell_Campmaster","the_camp",tf_hero| tf_randomize_face| tf_imladris,0,0,fac_imladris,
   [itm_riv_armor_light,itm_riv_boots,],
      def_attrib|level(2),wp(20),knows_common,lorien_elf_face_1,lorien_elf_face_2],
["elder_wvillage","Pierre_Woodman","the_village",tf_hero,0,0,fac_beorn,
   [itm_beorn_tunic,itm_rohan_shoes,],
      def_attrib|level(2),wp(20),knows_common,0x000000052300000036db6db75eedf6ed00000000001f2adb0000000000000000],
["elder_beorn","Beorn_Elder","the_hamlet",tf_hero| tf_randomize_face,0,0,fac_beorn,
   [itm_beorn_tunic,itm_rohan_shoes,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_harad","Harad_Camp_chief","the_camp",tf_hero| tf_randomize_face| tf_harad,0,0,fac_harad,
   [itm_harad_padded,itm_harad_scale_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_rhun","Rhun_Camp_Chief","the_camp",tf_hero| tf_randomize_face,0,0,fac_rhun,
   [itm_rhun_armor_p,itm_furry_boots,],
      def_attrib|level(2),wp(20),knows_common,rhun_man1,rhun_man2],
["elder_khand","Khand_Camp_Chief","the_camp",tf_hero| tf_randomize_face,0,0,fac_khand,
   [itm_khand_foot_lam,itm_splinted_greaves_good,],
      def_attrib|level(2),wp(20),knows_common,khand_man1,khand_man2],
["elder_dunland","Dun_Camp_Chief","the_camp",tf_hero |tf_dunland,0,0,fac_dunland,
   [itm_dunland_armor_h,itm_dunland_wolfboots,],
      def_attrib|level(2),wp(20),knows_common,0x000000003f0061c720996c7bd86f36db00000000001e42e80000000000000000],
["elder_umbar","Umbar_Quartermaster","the_fortified_camp",tf_hero| tf_randomize_face,0,0,fac_umbar,
   [itm_umb_armor_a,itm_corsair_boots,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_moria","Moria_Chief","the_Mines",tf_hero| tf_randomize_face| tf_orc,0,0,fac_moria,
   [itm_moria_armor_c,itm_orc_ragwrap,],
      def_attrib|level(2),wp(20),knows_common,khand_man1,khand_man2],
["elder_gunda","Master_of_the_Caves","the_caves",tf_hero| tf_randomize_face| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_d,itm_orc_furboots,],
      def_attrib|level(2),wp(20),knows_common,khand_man1,khand_man2],
["elder_dale","Dale_Quartermaster","the_city",tf_hero| tf_randomize_face,0,0,fac_dale,
   [itm_fur_coat,itm_leather_boots,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_esgaroth","Esgaroth_Quartermaster","the_lake_town",tf_hero| tf_randomize_face,0,0,fac_dale,
   [itm_fur_coat,itm_leather_boots,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_erebor","Erebor_Guildmaster","the_Halls",tf_hero| tf_randomize_face| tf_dwarf,0,0,fac_dwarf,
   [itm_dwarf_armor_a,itm_dwarf_pad_boots,],
      attr_dwarf_tier_3|level(2),wp(20),knows_common_dwarf,dwarf_face_3,dwarf_face_4],
["elder_dolguldur","Guldur_Chief","the_black_castle",tf_hero| tf_randomize_face| tf_uruk,0,0,fac_guldur,
   [itm_m_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(2),wp(20),knows_common,mordor_man1,mordor_man2],

["elder_wosgiliath","Campmaster","the_camp",tf_hero| tf_gondor| tf_randomize_face,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_oscamp","Campmaster","the_camp",tf_hero| tf_uruk| tf_randomize_face,0,0,fac_mordor,
   [itm_m_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(2),wp(20),knows_common,0x0000000f00001184574a6934eb6ed2d700000000001eb86e0000000000000000],
["elder_eosgiliath","Campmaster","the_camp",tf_hero| tf_randomize_face| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_uoutpost","Campmaster","the_camp",tf_hero| tf_randomize_face| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_med_b_good,itm_uruk_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_uhcamp","Campmaster","the_camp",tf_hero| tf_randomize_face| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_med_a_good,itm_uruk_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_urcamp","Campmaster","the_camp",tf_hero| tf_randomize_face| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_heavy_a_bad,itm_uruk_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_woodelf_camp","Elder","the_camp",tf_hero| tf_randomize_face| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_leather,itm_mirkwood_boots,],
      def_attrib|level(2),wp(20),knows_common,lorien_elf_face_1,lorien_elf_face_2],
["elder_woodelf_west_camp","Elder","the_camp",tf_hero| tf_randomize_face| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_leather,itm_mirkwood_boots,],
      def_attrib|level(2),wp(20),knows_common,lorien_elf_face_1,lorien_elf_face_2],
["elder_beorn_v","Beorning_Elder","the_village",tf_hero| tf_randomize_face,0,0,fac_beorn,
   [itm_beorn_tunic,itm_rohan_shoes,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_troll_cave","Cave_Chief","the_caves",tf_hero| tf_randomize_face| tf_orc,0,0,fac_moria,
   [itm_moria_armor_c,itm_orc_ragwrap,],
      def_attrib|level(2),wp(20),knows_common,khand_man1,khand_man2],
["elder_dg_outpost","Campmaster","the_camp",tf_hero| tf_randomize_face| tf_orc,0,0,fac_guldur,
   [itm_moria_armor_c,itm_orc_ragwrap,],
      def_attrib|level(2),wp(20),knows_common,rhun_man1,rhun_man2],
["elder_rhun_sc","Rhun_Camp_Chief","the_camp",tf_hero| tf_randomize_face,0,0,fac_rhun,
   [itm_rhun_armor_p,itm_furry_boots,],
      def_attrib|level(2),wp(20),knows_common,rhun_man1,rhun_man2],
["elder_rhun_nc","Rhun_Camp_Chief","the_camp",tf_hero| tf_randomize_face,0,0,fac_rhun,
   [itm_rhun_armor_p,itm_furry_boots,],
      def_attrib|level(2),wp(20),knows_common,rhun_man1,rhun_man2],
["elder_gunda_ne","Orc_Elder","the_camp",tf_hero| tf_randomize_face| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_d,itm_orc_furboots,],
      def_attrib|level(2),wp(20),knows_common,khand_man1,khand_man2],
["elder_gunda_nw","Orc_Elder","the_camp",tf_hero| tf_randomize_face| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_d,itm_orc_furboots,],
      def_attrib|level(2),wp(20),knows_common,khand_man1,khand_man2],
["elder_gunda_s","Orc_Elder","the_camp",tf_hero| tf_randomize_face| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_d,itm_orc_furboots,],
      def_attrib|level(2),wp(20),knows_common,khand_man1,khand_man2],
["elder_gunda_m","Orc_Elder","the_camp",tf_hero| tf_randomize_face| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_d,itm_orc_furboots,],
      def_attrib|level(2),wp(20),knows_common,khand_man1,khand_man2],
["elder_ironhill","Camp_Chief","the_camp",tf_hero| tf_randomize_face| tf_dwarf,0,0,fac_dwarf,
   [itm_dwarf_armor_a,itm_dwarf_pad_boots,],
      attr_dwarf_tier_3|level(2),wp(20),knows_common_dwarf,dwarf_face_3,dwarf_face_4],
    
    
#Village stores
["village_1_elder","Lord_of_the_Lash","the_caves",tf_hero| tf_randomize_face| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_d,itm_orc_furboots,],
      def_attrib|level(2),wp(20),knows_common,khand_man1,khand_man2],
["merchants_end","bug","bug",tf_hero,0,0,fac_commoners,   [],      0,0,0,0],
 
# Chests
#["zendar_chest","Zendar_Chest","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      def_attrib,0,0,0],
["tutorial_chest_1","Melee_Weapons_Chest","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      def_attrib,0,0,0],
["tutorial_chest_2","Ranged_Weapons_Chest","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      def_attrib,0,0,0],
["bonus_chest_1","Bonus_Chest","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      def_attrib,0,0,0],
["bonus_chest_2","Bonus_Chest","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      def_attrib,0,0,0],
["bonus_chest_3","Bonus_Chest","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      def_attrib,0,0,0],
["camp_chest_faction","Faction_Chest","bug",tf_hero|tf_inactive|tf_is_merchant,0,0,fac_neutral,   [],      def_attrib,0,knows_inventory_management_10,0],
["camp_chest_none","Chest_for_nones","bug",tf_hero|tf_inactive|tf_is_merchant,0,0,fac_neutral,   [],      def_attrib,0,0,0],
["player_chest","Your_Chest","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      def_attrib,0,0,0],
# These are used as arrays in the scripts.
["temp_array_a","bug","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      0,0,0,0],
["temp_array_b","bug","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      0,0,0,0],
["temp_array_c","bug","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      0,0,0,0],
["stack_selection_amounts","bug","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      0,0,0,0],
["stack_selection_ids","bug","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      0,0,0,0],
["notification_menu_types","bug","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      0,0,0,0],
["notification_menu_var1","bug","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      0,0,0,0],
["notification_menu_var2","bug","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      0,0,0,0],
["banner_background_color_array","bug","bug",tf_hero|tf_inactive,0,0,fac_neutral,   [],      0,0,0,0],
# Add Extra Quest NPCs below this point  
["local_merchant","Local_Merchant","Local_Merchants",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
      def_attrib|level(5),wp(40),knows_power_strike_1,mercenary_face_1,mercenary_face_2],
["tax_rebel","Peasant_Rebel","Peasant_Rebels",tfg_armor,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
      def_attrib|level(4),wp(60),knows_common,mercenary_face_1,mercenary_face_2],
["trainee_peasant","Peasant","Peasants",tfg_armor,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
      def_attrib|level(4),wp(60),knows_common,mercenary_face_1,mercenary_face_2],
["fugitive_man","Suspicious_Man","Suspicious_Men",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,itm_arnor_sword_f,itm_loss_throwing_axes,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_6|knows_power_throw_6|knows_power_strike_6|knows_ironflesh_9,mercenary_face_1,mercenary_face_2],
["fugitive_elf","Suspicious_Elf","Suspicious_Elves",tf_lorien| tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_lorien_armor_a,itm_lorien_boots,itm_lorien_sword_a,itm_loss_throwing_axes,],
      attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_6|knows_power_throw_6|knows_power_strike_6|knows_ironflesh_9,lorien_elf_face_1,lorien_elf_face_2],
["fugitive_dwarf","Suspicious_Dwarf","Suspicious_Dwarves",tf_dwarf| tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_dwarf_armor,itm_dwarf_pad_boots,itm_dwarf_sword_a,itm_dwarf_throwing_axe,],
      attr_dwarf_tier_4,wp_dwarf_tier_4,knows_common_dwarf|knows_athletics_6|knows_power_throw_6|knows_power_strike_6|knows_ironflesh_9,dwarf_face_2,dwarf_face_3],
["fugitive_orc","Suspicious_Orc","Suspicious_Orcs",tf_orc| tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_moria_armor_a,itm_orc_slasher,itm_orc_throwing_arrow,],
      attr_orc_tier_4,wp_orc_tier_4,knows_common|knows_athletics_6|knows_power_throw_6|knows_power_strike_6|knows_ironflesh_9,mercenary_face_1,mercenary_face_2],
["spy","Shifty-eyed_Corsair","Shifty-eyed_Corsairs",tf_mounted| tfg_boots| tfg_armor| tfg_gloves| tfg_horse,0,0,fac_neutral,
   [itm_umb_armor_d,itm_umb_armor_c,itm_corsair_boots,itm_umb_shield_b,itm_umb_shield_d,itm_umbar_cutlass,itm_umbar_rapier,itm_steppe_horse,],
      attr_tier_4,wp_tier_4,knows_common|knows_riding_3|knows_power_strike_3,bandit_face1,bandit_face2],
["spy_evil","Shifty-eyed_Southerner","Shifty-eyed_Southerners",tf_mounted| tfg_boots| tfg_armor| tfg_gloves| tfg_horse,0,0,fac_neutral,
   [itm_leather_jerkin,itm_leather_gloves,itm_leather_boots,itm_arnor_sword_f,itm_steppe_horse,],
      attr_tier_4,wp_tier_4,knows_common|knows_riding_3|knows_power_strike_3,bandit_face1,bandit_face2],
["spy_partner","Spy_Handler","Spy_Handlers",tf_gondor| tf_mounted| tfg_boots| tfg_armor| tfg_gloves| tfg_horse,0,0,fac_neutral,
   [itm_gon_squire,itm_gondor_med_greaves,itm_gondor_cav_sword,itm_gondor_shield_d,itm_leather_gloves,itm_gondor_knight_helm_bad,itm_gondor_courser,],
      attr_tier_4,wp_tier_4,knows_common|knows_riding_3|knows_athletics_2|knows_power_strike_3|knows_ironflesh_3,gondor_face1,gondor_face2],
["spy_partner_evil","Spy_Handler","Spy_Handlers",tf_mounted| tfg_boots| tfg_armor| tfg_gloves| tfg_horse,0,0,fac_neutral,
   [itm_evil_light_armor,itm_leather_boots,itm_mordor_sword,itm_mordor_man_shield_b,itm_mordor_longsword,itm_mordor_warhorse,],
      attr_tier_4,wp_tier_4,knows_common|knows_riding_3|knows_athletics_2|knows_power_strike_3|knows_ironflesh_3,bandit_face1,bandit_face2],
#MV: Easter Egg Troll in Troll Cave
["easter_egg_troll","The Troll","_",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive| tf_hero,scn_troll_cave_center|entry(8),0,fac_moria,
   [itm_tree_trunk_club_a,itm_troll_feet,itm_troll_head_a,itm_troll_body,itm_troll_hands],
      str_255| agi_3| int_30| cha_18|level(30),wp(200),knows_power_strike_10|knows_ironflesh_10,troll_face1],
["treebeard","Treebeard","_",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive| tf_hero,scn_fangorn|entry(16),0,fac_commoners,
   [itm_tree_trunk_invis,itm_ent_body,itm_ent_hands,itm_ent_feet_boots,itm_ent_head,itm_ent_water,],
      str_255| agi_3| int_30| cha_30|level(30),wp(200),knows_power_strike_10|knows_ironflesh_10,troll_face1,troll_face2],
["ent_1","Bregalad","_",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive| tf_hero,scn_fangorn|entry(17),0,fac_commoners,
   [itm_tree_trunk_invis,itm_ent_body,itm_ent_hands,itm_ent_feet_boots,itm_ent_head_2,itm_ent_water,],
      str_255| agi_3| int_30| cha_30|level(30),wp(200),knows_power_strike_10|knows_ironflesh_10,troll_face1,troll_face2],
["ent_2","Finglas","_",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive| tf_hero,scn_fangorn|entry(18),0,fac_commoners,
   [itm_tree_trunk_invis,itm_ent_body,itm_ent_hands,itm_ent_feet_boots,itm_ent_head_3,itm_ent_water,],
      str_255| agi_3| int_30| cha_30|level(30),wp(200),knows_power_strike_10|knows_ironflesh_10,troll_face1,troll_face2],
["ent_3","Fladrif","_",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive| tf_hero,scn_fangorn|entry(19),0,fac_commoners,
   [itm_tree_trunk_invis,itm_ent_body,itm_ent_hands,itm_ent_feet_boots,itm_ent_head_2,itm_ent_water,],
      str_255| agi_3| int_30| cha_30|level(30),wp(200),knows_power_strike_10|knows_ironflesh_10,troll_face1,troll_face2],

# Gandalf and Nazgul for conversations
["gandalf","Gandalf","Home-grown Gandalves",tf_hero| tf_mounted| tfg_armor| tfg_horse| tfg_boots,0,0,fac_commoners,
   [itm_mearas_reward,itm_whiterobe,itm_leather_boots,],
      attr_tier_7,wp_tier_7,knows_riding_10|knows_athletics_10|knows_power_strike_10|knows_ironflesh_10|knows_pathfinding_10,0x0000000fc000234721419ab9eeafbeff00000000001d89110000000000000000],
["nazgul","Nazgul","Domesticated Nazgul",tf_hero| tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_commoners,
   [itm_uruk_greaves,itm_evil_gauntlets_a,itm_nazgulrobe,itm_empty_head,itm_nazgul_sword,itm_mordor_warhorse2,],
       attr_tier_7,wp_tier_7,knows_riding_10|knows_athletics_10|knows_power_strike_10|knows_ironflesh_10|knows_pathfinding_10,mercenary_face_2],

["quick_battle_6_player","quick_battle_6_player","_",tf_hero,0,0,fac_player_faction,
   [itm_leather_jerkin,itm_leather_boots,itm_corsair_bow,itm_corsair_arrows,],
      knight_attrib_1,wp(130),knight_skills_1|knows_riding_4,0x000000000008010b01f041a9249f65fd],
# GA scene stub NPCs
["barman","Barman","_",tf_hero| tf_randomize_face,0,0,fac_neutral,
   [itm_leather_jerkin,itm_leather_boots,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder","Center_Elder","_",tf_hero| tf_randomize_face,0,0,fac_neutral,
   [itm_leather_jerkin,itm_leather_boots,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["gear_merchant","Gear_Merchant","_",tf_hero| tf_randomize_face,0,0,fac_neutral,
   [itm_leather_jerkin,itm_leather_boots,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["goods_merchant","Goods_Merchant","_",tf_hero| tf_randomize_face,0,0,fac_neutral,
   [itm_leather_jerkin,itm_leather_boots,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["start_quest_caravaneer","Torbal_the_Caravaneer","_",tf_hero| tf_randomize_face,0,0,fac_neutral,
   [itm_leather_jerkin,itm_leather_boots,],
      def_attrib|level(50),wp(400),knows_common|knows_power_strike_10|knows_ironflesh_10,mercenary_face_1,mercenary_face_2],
# ["brigand_arena_master","Tournament_Master","_",tf_hero| tf_randomize_face,scn_zendar_arena|entry(52),0,fac_commoners,
   # [itm_leather_jerkin,itm_leather_boots,],
      # def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
# ["gondor_arena_master","Tournament_Master","_",tf_hero| tf_randomize_face,scn_gondor_arena|entry(52),0,fac_commoners,
   # [itm_leather_jerkin,itm_leather_boots,],
      # def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
# ["rohan_arena_master","Tournament_Master","_",tf_hero| tf_randomize_face,scn_rohan_arena|entry(52),0,fac_commoners,
   # [itm_leather_jerkin,itm_leather_boots,],
      # def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
# ["mordor_arena_master","Pit_Master","_",tf_hero| tf_randomize_face,scn_mordor_arena|entry(52),0,fac_commoners,
   # [itm_leather_jerkin,itm_leather_boots,],
      # def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
# ["elf_arena_master","Tournament_Master","_",tf_hero| tf_randomize_face,scn_elf_arena|entry(52),0,fac_commoners,
   # [itm_leather_jerkin,itm_leather_boots,],
      # def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
#Kolba additions
#["androg","Androg","_",tf_hero,scn_zendar_center|entry(7),0,fac_commoners,
#   [itm_leather_jerkin,itm_leather_boots,],
#      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["dorwinion_bandit","Dorwinion_Bandit","Dorwinion_Bandits",tfg_armor|tfg_shield,0,0,fac_outlaws,
   [itm_rhun_sword,itm_leather_boots,itm_white_tunic_b,itm_white_tunic_c,itm_javelin,itm_shortened_spear,itm_spear,itm_blue_tunic,itm_leather_boots,],
         def_attrib|level(12),wp(100),knows_common,mercenary_face_1,mercenary_face_2],
["dorwinion_raider","Dorwinion_Raider","Dorwinion_Raiders",tfg_armor|tfg_shield|tfg_boots|tfg_helm,0,0,fac_outlaws,
   [itm_rhun_shortsword,itm_rhun_sword,itm_rhun_sword,itm_rhun_helm_pot,itm_rhun_helm_horde,itm_rhun_armor_b,itm_rhun_armor_a,itm_rhun_armor_d,itm_javelin,itm_rhun_shield,itm_leather_boots,],
              def_attrib|level(17),wp(120),knows_common,mercenary_face_1,mercenary_face_2],

# Troops for scripting purpose. Make sure these are the last troops. (by foxyman)
["troops_end","troops_end","troops_end",tf_hero,no_scene,reserved,fac_commoners,[],0,0,0,0,0], #unused
["no_troop","_","the place",tf_hero,0,0,fac_commoners,[],0,0,0,0,0],
["skill2item_type","_","_",tf_hero,0,0,fac_commoners,[],0,0,0,0,0], # array for working with merchant skills as indicator of quantity of items in shop
["traits","_","_",tf_hero,0,0,fac_commoners,[],0,0,0,0,0], # array of traits (0/1)
#Player history array
["log_array_entry_type","_","_",0,0,0,fac_commoners,   [],      0,0,0,0],
["log_array_entry_time","_","_",0,0,0,fac_commoners,   [],      0,0,0,0],
["log_array_actor","_","_",0,0,0,fac_commoners,   [],      0,0,0,0],
["log_array_center_object","_","_",0,0,0,fac_commoners,   [],      0,0,0,0],
["log_array_center_object_lord","_","_",0,0,0,fac_commoners,   [],      0,0,0,0],
["log_array_center_object_faction","_","_",0,0,0,fac_commoners,   [],      0,0,0,0],
["log_array_troop_object","_","_",0,0,0,fac_commoners,   [],      0,0,0,0],
["log_array_troop_object_faction","_","_",0,0,0,fac_commoners,   [],      0,0,0,0],
["log_array_faction_object","_","_",0,0,0,fac_commoners,   [],      0,0,0,0],
##############################
#MV: what are these - future quest troops? not used anywhere
["city_guard","City_Guard","city_guard",tfg_armor| tfg_boots,0,0,fac_gondor,
   [itm_leather_jerkin,itm_leather_boots,itm_gon_tab_shield_a,],
      def_attrib|level(9),wp(90),knows_common|knows_athletics_1|knows_power_strike_1,mercenary_face_1,mercenary_face_2],
["orc_sentry","Orc_Sentry","orc_sentry",tf_orc| tfg_shield| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_mordor_orc_shield_d,itm_orc_coif,itm_orc_ragwrap,itm_orc_slasher,],
      def_attrib|level(12),wp(90),knows_prisoner_management_1|knows_inventory_management_1|knows_pathfinding_1|knows_athletics_3|knows_power_strike_2|knows_ironflesh_2,orc_face1,orc_face2],
["uruk_hai_sentry","Uruk-hai_Sentry","uruk_hai_sentry",tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_isen_uruk_light_a,itm_isen_uruk_light_a,itm_isen_orc_shield_a,itm_isen_orc_light_b,itm_isen_uruk_helm_a,],
      def_attrib|level(12),wp(90),knows_prisoner_management_1|knows_inventory_management_1|knows_pathfinding_1|knows_athletics_2|knows_power_strike_2|knows_ironflesh_3,mercenary_face_1,mercenary_face_2],
["black_numenorean_sorcerer","Black_Numenorean_Sorcerer","Black_numenorean_sorcerer", tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,
   [itm_m_cap_armor,itm_mordor_helm,itm_mordor_sword,itm_leather_boots,],
      def_attrib|level(45),wp(400),knows_common|knows_athletics_10|knows_power_strike_6|knows_ironflesh_10,mercenary_face_1,mercenary_face_2],
["black_numenorean_acolyte","Black_Numenorean_Acolyte","Black_Numenorean_Acolytes",tf_evil_man| tfg_armor| tfg_boots,0,0,fac_mordor,
   [itm_leather_boots,itm_leather_gloves,itm_evil_light_armor,itm_orc_simple_spear_heavy,],
      attr_tier_2,wp_tier_2,knows_common|knows_athletics_1|knows_power_strike_1,mordor_man1,mordor_man2],
["wolf_rider_of_mirkwood","Wolf_Rider_of_Mirkwood","Wolf_Riders_of_Mirkwood",tf_orc| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_orc_bow,itm_arrows,itm_orc_sabre,itm_orc_sabre,itm_isen_uruk_light_a,itm_isen_uruk_light_a,itm_orc_coif,itm_wargarmored_2c,],
      def_attrib|level(15),wp(110),knows_pathfinding_1|knows_horse_archery_2|knows_riding_4|knows_power_throw_2|knows_power_strike_2|knows_ironflesh_2,orc_face3,orc_face6],
["warg_rider_of_mirkwood","Warg_Rider_of_Mirkwood","Warg_Riders_of_Mirkwood",tf_orc| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_orc_bow,itm_arrows,itm_orc_sabre,itm_orc_sabre,itm_isen_uruk_light_a,itm_isen_uruk_light_a,itm_orc_coif,itm_wargarmored_1c,],
      def_attrib|level(22),wp(135),knows_pathfinding_1|knows_horse_archery_3|knows_riding_4|knows_power_throw_3|knows_power_strike_4|knows_ironflesh_4,orc_face3,orc_face8],
["gate_aggravator","Gate_Defence","_", tfg_armor| tfg_boots| tfg_helm|tfg_gloves,0,0,fac_neutral,
   [itm_warg_ghost_armour,itm_empty_hands,itm_empty_legs,itm_empty_head],
      str_255|level(80),wp(5),knows_shield_10|knows_ironflesh_10,0,0],
["orc_pretender","Orc_Pretender","_",tf_orc| tfg_shield| tfg_armor| tfg_helm| tf_no_capture_alive,0,0,fac_neutral,
   [itm_orc_slasher,itm_orc_sabre,itm_moria_orc_shield_b,itm_moria_orc_shield_a,itm_moria_armor_e,itm_orc_greaves,],
      attr_orc_tier_6,wp_tier_6,knows_athletics_5|knows_power_strike_4|knows_ironflesh_10,orc_face5,orc_face8],
["human_prisoner","Human_Prisoner","_",tf_hero| tfg_helm,0,0,fac_neutral,
   [itm_prisoner_coll_chain,],
      attr_orc_tier_4,wp_tier_6,knows_athletics_5|knows_power_strike_4,0x000000063f00004336db75b7ab6eb6b400000000001db6eb0000000000000000],
 
# CC: Ambush troops here...

["spider","Mirkwood Spider","Mirkwood Spiders", tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
[itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_spider],
str_30| agi_7| int_4| cha_4|level(20),0,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face7,orc_face2],

["bear","Bear","Bears", tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_outlaws,
[itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_bear],
str_127|agi_7|int_4|cha_4|level(35),0,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face7,orc_face2], #0x7D = str_127

["wolf","Wolf","Wolves", tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_outlaws,
[itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_wolf],
str_30| agi_7| int_4| cha_4|level(15),0,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face7,orc_face2],

#kham Spears Quest
["dorwinion_sack","Dorwinion_Sack","bug",tf_hero|tfg_helm|tf_inactive|tf_is_merchant,0,0,fac_neutral,   [itm_cram,itm_metal_scraps_good,itm_metal_scraps_good,itm_metal_scraps_good, itm_rhun_helm_horde],      def_attrib,0,knows_inventory_management_10,0],
#end Kham Spears quest

#kham Ring Hunters Start ####

["ring_hunter_captain","Ring_Hunter_Captain","bug",tf_evil_man|tf_hero| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,
   [itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_black_num_armor,itm_black_num_helm,itm_mordor_man_shield_b,itm_mordor_longsword,],
      attr_tier_6,wp_tier_5,knows_common|knows_leadership_10|knows_tactics_1|knows_athletics_8|knows_shield_7|knows_power_strike_7|knows_ironflesh_7,mordor_man1,mordor_man2],

["ring_hunter_lt","Ring_Hunter_Captain","bug",tf_evil_man| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,
   [itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_black_num_armor,itm_black_num_helm,itm_mordor_man_shield_b,itm_mordor_longsword,],
      attr_tier_6,wp_tier_5,knows_common|knows_leadership_10|knows_tactics_1|knows_athletics_8|knows_shield_7|knows_power_strike_7|knows_ironflesh_7,mordor_man1,mordor_man2],


["ring_hunter_one","Ring_Hunter","Ring_Hunters",tf_harad| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,
   [itm_harad_scale_greaves,itm_leather_gloves,itm_harad_lion_scale,itm_lion_helm,itm_harad_heavy_sword,itm_harad_khopesh,itm_harad_long_shield_b,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_6|knows_power_strike_5|knows_ironflesh_6,haradrim_face_1,haradrim_face_2],

["ring_hunter_two","Ring_Hunter","Ring_Hunters",tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_d,itm_umb_helm_d,itm_umb_helm_c,itm_corsair_bow,itm_corsair_arrows,itm_corsair_sword,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_5|knows_power_draw_3|knows_power_strike_4|knows_ironflesh_4,bandit_face1,bandit_face2],

["ring_hunter_three","Ring_Hunter","Ring_Hunters",tf_urukhai|tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_isen_uruk_helm_a_good,itm_isen_uruk_heavy_c,itm_isengard_axe,itm_isen_uruk_shield_b,itm_isengard_hammer,itm_isengard_mallet,itm_isengard_heavy_sword,],
      attr_tier_5,wp_tier_5,knows_athletics_6|knows_power_strike_6|knows_ironflesh_6,uruk_hai_face1,uruk_hai_face2],
["ring_hunter_four","Ring_Hunter","Ring_Hunters",tf_orc| tfg_ranged| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_orc_greaves,itm_evil_gauntlets_b,itm_m_orc_light_d,itm_m_orc_light_e,itm_m_orc_heavy_a,itm_m_orc_heavy_b,itm_orc_bow,itm_orc_hook_arrow,itm_orc_sabre,itm_orc_slasher,itm_orc_slasher,],
      attr_orc_tier_4,wp_orc_tier_4,knows_athletics_4|knows_power_draw_4|knows_power_strike_2,orc_face7,orc_face6],
### Kham Ring Hunters End ###

#Kham Start Quest Troops
["start_quest_uruk","Mordor_Uruk_Captain","bug",tf_uruk| tfg_shield| tfg_ranged|tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_uruk_greaves,itm_uruk_chain_greaves,itm_evil_gauntlets_b,itm_orc_throwing_arrow,itm_uruk_bow,itm_orc_hook_arrow,itm_m_uruk_med_b,itm_m_uruk_med_c,itm_uruk_falchion_a,itm_uruk_falchion_b,itm_orc_skull_spear_heavy,itm_mordor_uruk_shield_a,itm_mordor_uruk_shield_b,itm_uruk_helm_b,itm_uruk_helm_c,itm_uruk_helm_d,],
      attr_tier_4,wp_tier_4,knows_athletics_6|knows_power_strike_5|knows_power_draw_4|knows_power_throw_3|knows_ironflesh_4|knows_shield_2,uruk_hai_face1,uruk_hai_face2],

["start_quest_orc","Mordor_Orc_Lieutenant","Large_Orcs_of_Mordor",tf_orc| tfg_shield| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_orc_greaves,itm_orc_coif, itm_orc_nosehelm, itm_orc_kettlehelm, itm_m_orc_light_d,itm_m_orc_light_e,itm_m_orc_heavy_a,itm_m_orc_heavy_b,itm_orc_sabre,itm_orc_falchion,itm_orc_two_handed_axe,itm_orc_skull_spear,itm_orc_slasher,itm_orc_bill,itm_orc_axe,itm_mordor_orc_shield_b,itm_mordor_orc_shield_c,itm_orc_throwing_axes,itm_mordor_orc_shield_d,],
      attr_orc_tier_3,wp_orc_tier_3,knows_athletics_5|knows_power_strike_3|knows_power_throw_3,orc_face3,orc_face6],

["start_quest_woodelf","Galadhrim_Royal_Marksman","Galadhrim_Royal_Marksmen",tf_lorien| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_lorien_bow,itm_elven_arrows,itm_lorien_helm_b,itm_lorien_armor_c,itm_lorien_boots,itm_lorien_sword_b,itm_lorien_shield_c,],
      attr_elf_tier_6,wp_elf_tier_6,knows_common|knows_athletics_7|knows_shield_1|knows_power_draw_6|knows_power_strike_4|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],

["start_quest_mordor_scout","Mordor_Guide","Mordor_Guides",tf_orc| tfg_ranged| tfg_helm| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_orc_furboots,itm_orc_coif, itm_orc_nosehelm, itm_orc_kettlehelm_bad,itm_leather_gloves,itm_m_orc_light_c,itm_m_orc_light_d,itm_m_orc_light_e,itm_m_orc_light_c,itm_orc_bow,itm_orc_hook_arrow,itm_orc_sabre,itm_orc_slasher,itm_orc_slasher,],
      attr_orc_tier_4,wp_archery(135)| wp(110),knows_riding_1|knows_athletics_6|knows_power_draw_5|knows_power_strike_2,orc_face1,orc_face4],

["start_quest_beorning","Beorning_Carrock_Berserker","Beorning_Carrock_Berserkers",tfg_gloves| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,
   [itm_beorn_berserk,itm_leather_boots,itm_leather_gloves,itm_beorn_helmet,itm_dale_helmet_b,itm_beorn_battle_axe,itm_dale_sword_long,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_6|knows_power_strike_3|knows_ironflesh_6,beorn_face1,beorn_face2],

## Kham Amath Dollen's Troops

["black_shield","Amath_Dollen","-",tf_hero| tf_evil_man| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rhun,
   [itm_corsair_boots,itm_evil_gauntlets_a,itm_m_uruk_heavy_a,itm_rhun_helm_barbed,itm_rhun_sword,itm_mordor_uruk_shield_a,],
      attr_tier_5,wp_tier_6,knows_common|knows_athletics_7|knows_shield_7|knows_power_strike_7|knows_ironflesh_7,0x000000003f00b30d2d2ea72ac902553500000000001d42300000000000000000],

["black_shield_bandit","Amath_Dollen's_Bandit","Amath_Dollen's_Bandits",tf_evil_man| tf_randomize_face| tfg_shield| tfg_armor| tfg_boots,0,0,fac_rhun,
   [itm_furry_boots,itm_leather_gloves,itm_dunland_armor_a,itm_dunland_armor_b,itm_dunland_armor_c,itm_dunland_armor_d,itm_dunland_armor_e,itm_dunland_armor_g,itm_dunland_armor_h,itm_orc_throwing_axes,itm_hood_black,itm_lamedon_hood,itm_orc_shield_a,itm_orc_shield_b,itm_wood_club,itm_orc_axe,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_3|knows_shield_3|knows_power_strike_3|knows_ironflesh_3|knows_power_throw_3,rhun_man1,rhun_man2],

["black_shield_scout","Amath_Dollen's_Scout","Amath_Dollen's_Scouts",tf_evil_man| tf_randomize_face|tfg_helm|tfg_armor| tfg_boots|tfg_ranged,0,0,fac_rhun,
   [itm_furry_boots,itm_leather_gloves,itm_dunland_armor_a,itm_dunland_armor_b,itm_dunland_armor_c,itm_dunland_armor_d,itm_dunland_armor_e,itm_dunland_armor_g,itm_dunland_armor_h,itm_hood_black,itm_hood_black,itm_gondor_ranger_hood_mask,itm_wood_club,itm_arrows,itm_orc_bow,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_3|knows_shield_3|knows_power_strike_3|knows_ironflesh_3|knows_power_draw_5,rhun_man1,rhun_man2],

["black_shield_guard","Amath_Dollen's_Guard","Amath_Dollen's_Guards",tf_evil_man| tf_randomize_face|tfg_helm| tfg_shield| tfg_armor| tfg_boots,0,0,fac_rhun,
   [itm_furry_boots,itm_leather_gloves,itm_dunland_armor_i,itm_dunland_armor_j,itm_corsair_harpoon,itm_rhun_helm_horde,itm_mordor_uruk_shield_a,itm_rhun_falchion,itm_rhun_sword,itm_rhun_shortsword],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_5|knows_shield_5|knows_power_strike_5|knows_ironflesh_5|knows_power_throw_5,rhun_man1,rhun_man2],

["dorwinion_spirit_leader","Spirit","_", tf_urukhai|tfg_armor| tfg_boots| tfg_helm|tfg_gloves,0,0,fac_neutral,
  [(itm_dunland_armor_k,imod_old),(itm_leather_gloves,imod_poor),itm_dunland_wolfboots,(itm_empty_head,imod_old), itm_khand_axe_great],
    attr_tier_6,wp(255),knows_common|knows_athletics_6|knows_power_strike_6|knows_ironflesh_6,0,0],

["dorwinion_spirit","Lesser Spirit","_", tf_uruk|tfg_armor| tfg_boots| tfg_helm|tfg_gloves,0,0,fac_neutral,
  [(itm_dunland_armor_k,imod_poor),(itm_leather_gloves,imod_poor),itm_dunland_wolfboots,(itm_empty_head,imod_poor), itm_dunnish_war_axe, itm_orc_shield_b, itm_orc_shield_c],
    attr_tier_3,wp_tier_4,knows_common|knows_athletics_6|knows_power_strike_6|knows_ironflesh_6,0,0],

#unused
["dummy_troop",  "bug","_", tf_hero, 0, 0, fac_gondor, [], lord_attrib,0,0,0],
["dummy_troop_b","bug","_", tf_hero, 0, 0, fac_gondor, [], lord_attrib,0,0,0],
    
["i6_beorning_bear_warrior","Bear_Warrior","Bear_Warriors",tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,[itm_beorn_helmet,itm_beorn_chief,itm_leather_gloves_good,itm_leather_boots, itm_leather_boots_dark,itm_splinted_greaves,itm_beorn_axe_reward,itm_beorn_shield_reward,itm_rohirrim_throwing_axe,],attr_tier_6,wp_tier_6,knows_common|knows_athletics_5|knows_power_strike_4|knows_ironflesh_8|knows_shield_7|knows_power_throw_4,beorn_face1,beorn_face2],

["test_vet_archer","Test_Vet_Archer","Test_Vet_Archer",tf_woodelf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_mirkwood_pad,itm_mirkwood_boots,itm_mirkwood_helm_d],
      attr_elf_tier_6,wp_elf_tier_6|wp_throwing(300), knows_common|knows_athletics_8|knows_power_draw_7|knows_power_strike_4|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],

## Kham - Volunteers

["volunteers","--- Reserves ---:","_", tfg_armor| tfg_boots| tfg_helm|tfg_gloves,0,0,fac_neutral,
   [itm_warg_ghost_armour,itm_empty_hands,itm_empty_legs,itm_empty_head],
      str_255|level(80),wp(5),knows_shield_10|knows_ironflesh_10,0,0],

## Kham - Dormant Troop

["dormant","Dormant","_", tf_hero|tf_is_merchant,no_scene,reserved,fac_commoners,[],def_attrib,0,knows_common|knows_inventory_management_10,0], #Used for Cheat Item Picker


## Kham - Test AI
["badass_theo","Badass_King_Theo","King",tf_hero| tf_rohan| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_armor_th,itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_inf_helmet_b_lordly,itm_rohirrim_long_hafted_axe, itm_rohan_shield_g],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_riding_4|knows_trainer_4,0x0000000fff00130347934c399386b8a300000000001db6d90000000000000000],

["killer_witcher","Ugly Mogly","Lieutenant",tf_hero| tf_uruk| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,
   [itm_m_uruk_heavy_c,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_uruk_helm_f,itm_mordor_uruk_shield_c,itm_mordor_longsword,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_riding_4|knows_trainer_4,0x000000002c000104003fb3f407b83d0d00000000000000000000000000000000],

## Kham - Healers

["morannon_healer","Okstuk_the_Healer","_",tf_hero|tf_orc,scn_morannon_center|entry(13),0,fac_mordor,[itm_moria_armor_b,itm_orc_greaves,itm_orc_coif],str_30|agi_5|int_4|cha_4|level(2),wp(20),knows_common,orc_face1],
["minas_tirith_healer","Ioreth","_",tf_female|tf_hero,scn_minas_tirith_center|entry(13),0,fac_gondor,[itm_whiterobe,itm_leather_boots],str_30|level(2),wp(20),knows_common,0x0000000fff0030064b3152c34d27231100000000001c986d0000000000000000],
["edoras_healer","Freya_the_Healer","_",tf_female|tf_hero,scn_edoras_center|entry(13),0,fac_rohan,[itm_whiterobe,itm_leather_boots],str_30|level(2),wp(20),knows_common,0x00000005070010045a9569a16d724adc00000000001db95a0000000000000000],
["isengard_healer","Nurgal_the_Patcher","_",tf_hero|tf_urukhai,scn_isengard_center|entry(13),0,fac_isengard,[itm_leather_gloves,itm_isen_uruk_light_a,itm_leather_boots],str_30|agi_5|int_4|cha_4|level(2),wp(20),knows_common,orc_face1],
["guldur_healer","Mornagar_the_Gramaryer","_",tf_hero|tf_evil_man,scn_dol_guldur_center|entry(13),0,fac_guldur,[itm_leather_boots, (itm_rohan_armor_th, imod_old)],str_30|agi_5|int_4|cha_4|level(2),wp(20),knows_common,0x000000047f0024d212014ac90032e05200000000001c84880000000000000000],
["gundabad_healer","Lurgakh_Third_Eye","_",tf_orc|tf_hero,scn_gundabad_camp_center|entry(13),0,fac_gundabad,[itm_gundabad_armor_d,itm_orc_furboots],def_attrib|level(2),wp(20),knows_common,0x0000000fc000200b5ff83e35e4f8ed8900000000001f6d470000000000000000],
["mirkwood_healer","Corwiel_the_Soft-Handed","_",tf_female|tf_hero,scn_thranduils_halls_center|entry(13),0,fac_woodelf,[itm_mirkwood_leather_good,itm_leather_boots],str_30|level(2),wp(20),knows_common,0x00000004bf00400a5b546a3682a4c2cb00000000001d268a0000000000000000],

#Kham Morale Troops

["hungry_uruk","Hungry_Uruk","bug",tf_uruk| tfg_shield| tfg_ranged|tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_uruk_greaves,itm_uruk_chain_greaves,itm_evil_gauntlets_b,itm_orc_throwing_arrow,itm_uruk_bow,itm_orc_hook_arrow,itm_m_uruk_heavy_c,itm_m_uruk_heavy_a,itm_uruk_falchion_a,itm_uruk_falchion_b,itm_orc_skull_spear_heavy,itm_mordor_uruk_shield_a,itm_mordor_uruk_shield_b,itm_uruk_helm_b,itm_uruk_helm_c,itm_uruk_helm_d,],
      attr_tier_4,wp_tier_4,knows_athletics_6|knows_power_strike_5|knows_power_draw_4|knows_power_throw_3|knows_ironflesh_4|knows_shield_2,uruk_hai_face1,uruk_hai_face2],

["hungry_orc","Hungry_Orc","Large_Orcs_of_Mordor",tf_orc| tfg_shield| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_orc_greaves,itm_orc_coif, itm_orc_nosehelm_bad, itm_orc_nosehelm, itm_m_orc_light_d,itm_m_orc_light_e,itm_m_orc_heavy_a,itm_m_orc_heavy_b,itm_orc_sabre,itm_orc_falchion,itm_orc_two_handed_axe,itm_orc_skull_spear,itm_orc_slasher,itm_orc_bill,itm_orc_axe,itm_mordor_orc_shield_b,itm_mordor_orc_shield_c,itm_orc_throwing_axes,itm_mordor_orc_shield_d,],
      attr_orc_tier_3,wp_orc_tier_3,knows_athletics_5|knows_power_strike_3|knows_power_throw_3,orc_face3,orc_face6],

["longing_lorien","Longing_Elf","a1_lorien_scouts",tf_lorien| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_short_bow,itm_elven_arrows,itm_lorien_archer,itm_lorien_boots,itm_lorien_sword_b,],
      attr_elf_tier_1,wp_elf_tier_1,knows_common|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_1,lorien_elf_face_1,lorien_elf_face_2],

["longing_woodelf","Longing_Elf","a1_greenwood_scouts",tf_woodelf| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_short_bow,itm_woodelf_arrows,itm_mirkwood_leather,itm_mirkwood_boots,itm_mirkwood_knife,],
      attr_elf_tier_1,wp_elf_tier_1,knows_common|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_1,mirkwood_elf_face_1,mirkwood_elf_face_2],

["longing_imladris","Longing_Elf","a1_riv_scouts",tf_imladris| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,
   [itm_riv_boots,itm_riv_bow,itm_riv_armor_light,itm_riv_archer_sword,itm_elven_arrows,],
      attr_elf_tier_1,wp_elf_tier_1,knows_common|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_1,rivendell_elf_face_1,rivendell_elf_face_2],

#These troops have been moved out of item factionization range, so their equipment doesn't show up in stores.
["i5_moria_deep_dweller","Deep-Dweller_of_Moria","Deep-Dwellers_of_Moria",tf_orc| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_moria,[itm_orc_bughelm_lordly,itm_orc_bughelm_lordly,itm_uruk_helm_e,itm_uruk_helm_f,itm_moria_armor_e,itm_orc_greaves,itm_orc_club_d_heavy,itm_dwarf_war_pick_old,itm_orc_javelin,itm_orc_javelin,itm_moria_orc_shield_b,itm_moria_orc_shield_c],attr_orc_tier_5,wp_orc_tier_5,knows_common|knows_athletics_7|knows_power_strike_6|knows_power_throw_5|knows_ironflesh_7,orc_face5,orc_face4],
["i5_moria_orc_chieftain","Orc_Chieftain_of_Moria","Orc_Chieftains_of_Moria",tf_orc| tfg_armor| tfg_helm| tfg_boots| tfg_shield| tf_no_capture_alive,0,0,fac_moria,[itm_orc_beakhelm_lordly,itm_uruk_helm_c,itm_uruk_helm_d,itm_uruk_helm_f,(itm_moria_armor_e, imod_sturdy),(itm_moria_armor_e, imod_reinforced),(itm_moria_armor_e, imod_lordly),itm_uruk_greaves, itm_orc_greaves,itm_orc_sabre_heavy,itm_orc_scimitar_heavy,itm_orc_skull_spear,itm_orc_simple_spear_heavy, itm_moria_orc_shield_a, (itm_orc_shield_c, imod_reinforced)],attr_orc_tier_5,wp_orc_tier_5,knows_common|knows_athletics_5|knows_power_strike_4|knows_ironflesh_10|knows_shield_4,orc_face5,orc_face4],
["c5_rhovanion_noble","Rhovanion_Noble","Rhovanion_Noblemen",tf_mounted| tfg_boots| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_shield|tfg_polearm,0,0,fac_dale,[itm_dale_helmet_e, itm_dale_helmet_f, itm_north_nasal_helm_good,itm_dale_heavy_c,itm_dale_heavy_c_good,itm_leather_gloves_good,itm_mail_mittens,itm_leather_boots_dark, itm_splinted_greaves_good,itm_lance,itm_dale_sword_long,itm_dwarf_shield_c, itm_dwarf_shield_c_good,itm_dale_warhorse,],attr_tier_5,wp_tier_5,knows_common|knows_riding_7|knows_shield_6|knows_ironflesh_4|knows_power_strike_3,nord_face_middle_1,nord_face_older_2],

# Malleable Hero Troops for Quests / Triggers

["generic_hero_infantry","generic_hero_infantry","generic_hero_infantry",tf_hero|tf_male| tfg_armor| tfg_helm| tfg_boots| tfg_shield,0,0,fac_commoners,[itm_leather_jerkin, itm_leather_boots],knight_attrib_1,wp_tier_4,knight_skills_2|knows_riding_4,0x000000018000000136db6db6db6db6db00000000001db6db0000000000000000],
["generic_hero_ranged","generic_hero_ranged","generic_hero_ranged",tf_hero|tf_male| tfg_armor| tfg_helm| tfg_boots| tfg_shield,0,0,fac_commoners,[itm_leather_jerkin, itm_leather_boots],knight_attrib_1,wp_tier_4,knight_skills_2|knows_riding_4,orc_face5,orc_face4],
["generic_hero_knight","generic_hero_knight","generic_hero_knight",tf_hero|tf_male| tfg_armor| tfg_helm| tfg_boots| tfg_shield,0,0,fac_commoners,[itm_leather_jerkin, itm_leather_boots],knight_attrib_1,wp_tier_4,knight_skills_2|knows_riding_4,0x000000018000000136db6db6db6db6db00000000001db6db0000000000000000],
["generic_hero_mounted_archer","generic_hero_mounted_archer","generic_hero_mounted_archer",tf_hero|tf_male|tfg_armor| tfg_helm| tfg_boots| tfg_shield,0,0,fac_commoners,[itm_leather_jerkin, itm_leather_boots],knight_attrib_1,wp_tier_4,knight_skills_2|knows_riding_4,0x000000018000000136db6db6db6db6db00000000001db6db0000000000000000],

# New Companions Begin

["npc18","Turmbathu","_",tf_hero| tf_female | tf_unmoveable_in_party_window,0,0,fac_khand,
   [itm_prisoner_coll_chain, itm_feet_chains, itm_khand_light],
      str_16|agi_15|int_4|cha_3|level(9),wp_one_handed(70)|wp_two_handed(80)|wp_polearm(80)|wp_archery(70)|wp_throwing(90),knows_common|knows_ironflesh_4|knows_power_strike_4|knows_power_throw_4|knows_weapon_master_4|knows_shield_1|knows_athletics_5|knows_looting_3,0x00000008ff00200007e68b1850a756c400000000001f34720000000000000000],

["npc19","Heidrek","_",tf_hero| tf_evil_man | tf_unmoveable_in_party_window,0,0,fac_dunland,
   [itm_dunland_armor_g,itm_dunland_wolfboots,itm_dunland_spear,itm_dunland_javelin,],
      str_11|agi_12|int_5|cha_5|level(5),wp_one_handed(60)|wp_two_handed(60)|wp_polearm(60)|wp_archery(60)|wp_throwing(60),knows_common|knows_ironflesh_2|knows_power_strike_1|knows_power_throw_3|knows_weapon_master_2|knows_shield_2|knows_athletics_3|knows_riding_1|knows_looting_2|knows_trainer_1|knows_tracking_2|knows_prisoner_management_1|knows_leadership_1,0x00000006a8001186532b56da62752d6400000000001d5ab20000000000000000],

["npc20","Zigûrphel","_",tf_hero| tf_female | tf_unmoveable_in_party_window,0,0,fac_guldur,
   [itm_evil_light_armor,itm_mordor_longsword,(itm_leather_boots, imod_meek),(itm_leather_gloves, imod_meek),],
      str_9|agi_8|int_15|cha_10|level(15),wp_one_handed(90)|wp_two_handed(90)|wp_polearm(90)|wp_archery(70)|wp_throwing(70),knows_common|knows_ironflesh_1|knows_power_strike_3|knows_power_throw_1|knows_weapon_master_2|knows_athletics_2|knows_riding_3|knows_looting_2|knows_tactics_2|knows_spotting_4|knows_inventory_management_1|knows_wound_treatment_4|knows_surgery_6|knows_first_aid_5|knows_persuasion_2|knows_prisoner_management_2|knows_leadership_2,0x00000005ff001003074372d248664b2700000000001fd6b50000000000000000],

["npc21","Berta","_",tf_hero|tf_troll| tf_unmoveable_in_party_window,0,0,fac_gundabad,
    [itm_gunda_troll_head_a, itm_gunda_troll_body_berta,itm_gunda_troll_hands,itm_gunda_troll_feet,itm_giant_bone_cudgel,],
        str_30| agi_30| int_3| cha_3|level(36),wp(120)|wp_one_handed(120),knows_power_strike_9|knows_ironflesh_13|knows_athletics_8|knows_shield_8,troll_face1],

["npc22","Zigûrphel","_",tf_hero| tf_female | tf_unmoveable_in_party_window,0,0,fac_guldur,
   [itm_evil_light_armor,itm_mordor_longsword,(itm_leather_boots, imod_meek),(itm_leather_gloves, imod_meek),],
      str_11|agi_13|int_21|cha_10|level(20),wp_one_handed(100)|wp_two_handed(100)|wp_polearm(100)|wp_archery(100)|wp_throwing(100),knows_athletics_3|knows_power_strike_2|knows_shield_1|knows_ironflesh_3|knows_weapon_master_2|knows_power_throw_2|knows_riding_4|knows_trainer_6|knows_tactics_2|knows_wound_treatment_7|knows_surgery_7|knows_first_aid_7|knows_persuasion_2|knows_leadership_2|knows_prisoner_management_2,0x00000005ff001003074372d248664b2700000000001fd6b50000000000000000],

["npc23","Zigûrphel","_",tf_hero| tf_female | tf_unmoveable_in_party_window,0,0,fac_guldur,
   [itm_evil_light_armor,itm_mordor_longsword,(itm_leather_boots, imod_meek),(itm_leather_gloves, imod_meek),],
      str_11|agi_13|int_21|cha_10|level(20),wp_one_handed(100)|wp_two_handed(100)|wp_polearm(100)|wp_archery(100)|wp_throwing(100),knows_athletics_3|knows_power_strike_2|knows_shield_1|knows_ironflesh_3|knows_weapon_master_2|knows_power_throw_2|knows_riding_4|knows_trainer_6|knows_tactics_2|knows_wound_treatment_7|knows_surgery_7|knows_first_aid_7|knows_persuasion_2|knows_leadership_2|knows_prisoner_management_2,0x00000005ff001003074372d248664b2700000000001fd6b50000000000000000],

["npc24","Zigûrphel","_",tf_hero| tf_female | tf_unmoveable_in_party_window,0,0,fac_guldur,
   [itm_evil_light_armor,itm_mordor_longsword,(itm_leather_boots, imod_meek),(itm_leather_gloves, imod_meek),],
      str_11|agi_13|int_21|cha_10|level(20),wp_one_handed(100)|wp_two_handed(100)|wp_polearm(100)|wp_archery(100)|wp_throwing(100),knows_athletics_3|knows_power_strike_2|knows_shield_1|knows_ironflesh_3|knows_weapon_master_2|knows_power_throw_2|knows_riding_4|knows_trainer_6|knows_tactics_2|knows_wound_treatment_7|knows_surgery_7|knows_first_aid_7|knows_persuasion_2|knows_leadership_2|knows_prisoner_management_2,0x00000005ff001003074372d248664b2700000000001fd6b50000000000000000],

["npc25","Zigûrphel","_",tf_hero| tf_female | tf_unmoveable_in_party_window,0,0,fac_guldur,
   [itm_evil_light_armor,itm_mordor_longsword,(itm_leather_boots, imod_meek),(itm_leather_gloves, imod_meek),],
      str_11|agi_13|int_21|cha_10|level(20),wp_one_handed(100)|wp_two_handed(100)|wp_polearm(100)|wp_archery(100)|wp_throwing(100),knows_athletics_3|knows_power_strike_2|knows_shield_1|knows_ironflesh_3|knows_weapon_master_2|knows_power_throw_2|knows_riding_4|knows_trainer_6|knows_tactics_2|knows_wound_treatment_7|knows_surgery_7|knows_first_aid_7|knows_persuasion_2|knows_leadership_2|knows_prisoner_management_2,0x00000005ff001003074372d248664b2700000000001fd6b50000000000000000],

["npc26","Zigûrphel","_",tf_hero| tf_female | tf_unmoveable_in_party_window,0,0,fac_guldur,
   [itm_evil_light_armor,itm_mordor_longsword,(itm_leather_boots, imod_meek),(itm_leather_gloves, imod_meek),],
      str_11|agi_13|int_21|cha_10|level(20),wp_one_handed(100)|wp_two_handed(100)|wp_polearm(100)|wp_archery(100)|wp_throwing(100),knows_athletics_3|knows_power_strike_2|knows_shield_1|knows_ironflesh_3|knows_weapon_master_2|knows_power_throw_2|knows_riding_4|knows_trainer_6|knows_tactics_2|knows_wound_treatment_7|knows_surgery_7|knows_first_aid_7|knows_persuasion_2|knows_leadership_2|knows_prisoner_management_2,0x00000005ff001003074372d248664b2700000000001fd6b50000000000000000],

["npc27","Zigûrphel","_",tf_hero| tf_female | tf_unmoveable_in_party_window,0,0,fac_guldur,
   [itm_evil_light_armor,itm_mordor_longsword,(itm_leather_boots, imod_meek),(itm_leather_gloves, imod_meek),],
      str_11|agi_13|int_21|cha_10|level(20),wp_one_handed(100)|wp_two_handed(100)|wp_polearm(100)|wp_archery(100)|wp_throwing(100),knows_athletics_3|knows_power_strike_2|knows_shield_1|knows_ironflesh_3|knows_weapon_master_2|knows_power_throw_2|knows_riding_4|knows_trainer_6|knows_tactics_2|knows_wound_treatment_7|knows_surgery_7|knows_first_aid_7|knows_persuasion_2|knows_leadership_2|knows_prisoner_management_2,0x00000005ff001003074372d248664b2700000000001fd6b50000000000000000],

# New Companions END

# Werewolf

["werewolf","Werewolf","Werewolves", tf_orc|tf_mounted| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive| tf_unmoveable_in_party_window,0,0,fac_outlaws,
  [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_werewolf],
    str_30|agi_7|int_4|cha_4|level(25),0,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face7,orc_face2], #0x7D = str_127

#Trolls  & ents
["moria_troll","Cave_Troll","Cave_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_moria,[itm_troll_head_a,itm_troll_head_b,itm_troll_head_c,itm_troll_body,itm_troll_hands,itm_troll_feet,itm_tree_trunk_club_b,itm_tree_trunk_invis,],str_25| agi_30| int_3| cha_3|level(36),wp(75),knows_power_strike_5|knows_ironflesh_10|knows_athletics_8,troll_face1,troll_face2],
["moria_vet_troll","Trained_Cave_Troll","Trained_Cave_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_moria,[itm_troll_head_a,itm_troll_head_b,itm_troll_head_c,itm_troll_body,itm_troll_hands,itm_troll_feet,itm_giant_club, itm_giant_sledgehammer,],str_25| agi_30| int_3| cha_3|level(38),wp(90),knows_power_strike_6|knows_ironflesh_11|knows_athletics_8,troll_face1,troll_face2],
["moria_armored_troll","Armored_Cave_Troll","Armored_Cave_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_moria,[itm_isen_olog_head_a,itm_troll_body,itm_troll_hands,itm_troll_feet,itm_giant_mace_b,],str_25| agi_30| int_3| cha_3|level(55),wp(100),knows_power_strike_6|knows_ironflesh_12|knows_athletics_8,troll_face1,troll_face2],
["gunda_troll","Mountain_Troll","Mountain_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_gundabad,[itm_gunda_troll_head_a, itm_gunda_troll_head_b, itm_gunda_troll_head_c,itm_gunda_troll_body,itm_gunda_troll_hands,itm_gunda_troll_feet,itm_giant_bone_cudgel,itm_giant_sledgehammer,itm_troll_shield_b,],str_25| agi_30| int_3| cha_3|level(34),wp(90),knows_power_strike_6|knows_ironflesh_8|knows_athletics_8|knows_shield_6,troll_face1,troll_face2],
["gunda_vet_troll","Trained_Mountain_Troll","Trained_Mountain_Trolls",tf_troll| tfg_helm|tfg_shield| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_gundabad,[itm_gunda_troll_head_a, itm_gunda_troll_head_b, itm_gunda_troll_head_c,itm_gunda_troll_body,itm_gunda_troll_hands,itm_gunda_troll_feet,itm_giant_club, itm_giant_sledgehammer,itm_troll_shield_b,],str_25| agi_30| int_3| cha_3|level(36),wp(120)|wp_one_handed(120),knows_power_strike_9|knows_ironflesh_13|knows_athletics_8|knows_shield_8,troll_face1,troll_face2],
["gunda_placeholder","Trained_Mountain_Troll","Trained_Mountain_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_gundabad,[itm_gunda_troll_head_a, itm_gunda_troll_head_b, itm_gunda_troll_head_c,itm_gunda_troll_body,itm_gunda_troll_hands,itm_gunda_troll_feet,itm_troll_shield_b,],str_25| agi_30| int_3| cha_3|level(50),wp(100)|wp_one_handed(120),knows_power_strike_5|knows_ironflesh_10|knows_athletics_8,troll_face1,troll_face2],
["isen_troll","Isengard_Troll","Isengard_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_isengard,[itm_troll_head_a,itm_troll_head_b,itm_troll_head_c,itm_troll_body,itm_troll_hands,itm_troll_feet,itm_tree_trunk_club, itm_tree_trunk_invis,],str_25| agi_30| int_3| cha_3|level(38),wp(75),knows_power_strike_5|knows_ironflesh_8|knows_athletics_8,troll_face1,troll_face2],
["isen_vet_troll","Isengard_Trained_Troll","Isengard_Trained_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_isengard,[itm_troll_head_a,itm_troll_head_b,itm_troll_head_c,itm_troll_body,itm_troll_hands,itm_troll_feet,itm_tree_trunk_club_b, itm_troll_weapon_long, itm_troll_weapon_long,],str_25| agi_30| int_3| cha_3|level(40),wp(85),knows_power_strike_5|knows_ironflesh_10|knows_athletics_8,troll_face1,troll_face2],
["isen_armored_troll","Isengard_Armored_Troll","Isengard_Armored_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_isengard,[itm_isen_olog_head_a,itm_isen_olog_head_b,itm_isen_olog_head_c,itm_isen_olog_body,itm_isen_olog_body_b,itm_isen_olog_hands,itm_isen_olog_feet,itm_giant_spiked_mace, itm_troll_weapon_long, itm_troll_weapon_long,],str_25| agi_30| int_3| cha_3|level(60),wp(100),knows_power_strike_6|knows_ironflesh_12|knows_athletics_8,troll_face1,troll_face2],
["mordor_troll","Mordor_Troll","Mordor_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_mordor,[itm_mordor_troll_head_a, itm_mordor_troll_head_b,itm_mordor_troll_body,itm_mordor_troll_hands,itm_mordor_troll_feet,itm_giant_club,],str_25| agi_30| int_3| cha_3|level(38),wp(90),knows_power_strike_5|knows_ironflesh_10|knows_athletics_8,troll_face1,troll_face2],
["mordor_vet_troll","Mordor_Trained_Troll","Mordor_Trained_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_mordor,[itm_mordor_troll_head_a, itm_mordor_troll_head_b,itm_mordor_troll_body,itm_mordor_troll_hands,itm_mordor_troll_feet,itm_giant_mace_b,itm_troll_shield_a,itm_troll_shield_a,],str_25| agi_30| int_3| cha_3|level(40),wp(100)|wp_one_handed(120),knows_power_strike_6|knows_ironflesh_12|knows_athletics_8|knows_shield_4,troll_face1,troll_face2],
["mordor_olog_hai","Olog_Hai_of_Mordor","Olog_Hai_of_Mordor",tf_troll|tfg_shield| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_mordor,[itm_olog_head_a, itm_olog_head_b, itm_olog_head_c,itm_olog_body,itm_olog_body_b,itm_olog_hands,itm_olog_feet,itm_giant_spiked_mace,itm_giant_hammer,itm_troll_shield_a,],str_25| agi_30| int_3| cha_3|level(65),wp(130)|wp_one_handed(150),knows_power_strike_7|knows_ironflesh_13|knows_athletics_8|knows_shield_6,troll_face1,troll_face2],
["troll_placeholder_1","Cave_Troll","Cave_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_moria,[itm_troll_head_a,itm_troll_head_b,itm_troll_head_c,itm_troll_body,itm_troll_hands,itm_troll_feet,itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_b,itm_tree_trunk_club_b,],str_25| agi_30| int_3| cha_3|level(40),wp(100),knows_power_strike_5|knows_ironflesh_10|knows_athletics_8,troll_face1,troll_face2],
["troll_placeholder_2","Cave_Troll","Cave_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_moria,[itm_troll_head_a,itm_troll_head_b,itm_troll_head_c,itm_troll_body,itm_troll_hands,itm_troll_feet,itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_b,itm_tree_trunk_club_b,],str_25| agi_30| int_3| cha_3|level(40),wp(100),knows_power_strike_5|knows_ironflesh_10|knows_athletics_8,troll_face1,troll_face2],
["troll_placeholder_3","Cave_Troll","Cave_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_moria,[itm_troll_head_a,itm_troll_head_b,itm_troll_head_c,itm_troll_body,itm_troll_hands,itm_troll_feet,itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_b,itm_tree_trunk_club_b,],str_25| agi_30| int_3| cha_3|level(40),wp(100),knows_power_strike_5|knows_ironflesh_10|knows_athletics_8,troll_face1,troll_face2],
["troll_placeholder_4","Cave_Troll","Cave_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_moria,[itm_troll_head_a,itm_troll_head_b,itm_troll_head_c,itm_troll_body,itm_troll_hands,itm_troll_feet,itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_b,itm_tree_trunk_club_b,],str_25| agi_30| int_3| cha_3|level(40),wp(100),knows_power_strike_5|knows_ironflesh_10|knows_athletics_8,troll_face1,troll_face2],
["troll_placeholder_5","Cave_Troll","Cave_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_moria,[itm_troll_head_a,itm_troll_head_b,itm_troll_head_c,itm_troll_body,itm_troll_hands,itm_troll_feet,itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_b,itm_tree_trunk_club_b,],str_25| agi_30| int_3| cha_3|level(40),wp(100),knows_power_strike_5|knows_ironflesh_10|knows_athletics_8,troll_face1,troll_face2],
["troll_placeholder_6","Cave_Troll","Cave_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_moria,[itm_troll_head_a,itm_troll_head_b,itm_troll_head_c,itm_troll_body,itm_troll_hands,itm_troll_feet,itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_b,itm_tree_trunk_club_b,],str_25| agi_30| int_3| cha_3|level(40),wp(100),knows_power_strike_5|knows_ironflesh_10|knows_athletics_8,troll_face1,troll_face2],
["wild_troll","Wild_Cave_Troll","Wild_Cave_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_tribal_orcs,[itm_troll_head_a,itm_troll_head_b,itm_troll_head_c,itm_troll_body,itm_troll_hands,itm_troll_feet,itm_tree_trunk_club_b,itm_tree_trunk_invis,],str_25| agi_30| int_3| cha_3|level(40),wp(100),knows_power_strike_5|knows_ironflesh_10|knows_athletics_8,troll_face1,troll_face2],
["ent","Ent","Ents",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_commoners,[itm_ent_head, itm_ent_head_2, itm_ent_head_3,itm_ent_body,itm_ent_hands,itm_ent_feet_boots,itm_tree_trunk_invis,itm_ent_water,],str_25| agi_30| int_3| cha_3|level(63),wp(250),knows_power_strike_15|knows_ironflesh_15|knows_athletics_8,troll_face1,troll_face2],

["multiplayer_profile_troop_male","multiplayer_profile_troop_male","multiplayer_profile_troop_male", tf_hero, 0, 0,fac_commoners,[itm_leather_jerkin, itm_leather_boots],0,0,0,0x000000018000000136db6db6db6db6db00000000001db6db0000000000000000],
["multiplayer_profile_troop_female","multiplayer_profile_troop_female","multiplayer_profile_troop_female", tf_hero|tf_female, 0, 0,fac_commoners,[itm_leather_jerkin, itm_leather_boots],0,0,0,0x000000018000000136db6db6db6db6db00000000001db6db0000000000000000],

#Tribal orcs moved out of item factionization range, activate around June 2020
["mountain_goblin","Mountain_Goblin","Mountain_Goblins",tf_orc| tf_no_capture_alive,0,0,fac_tribal_orcs,
   [itm_orc_tribal_a,itm_orc_tribal_b,itm_orc_tribal_c,itm_orc_tribal_c,itm_orc_shield_a,itm_orc_shield_b,itm_orc_shield_c,itm_orc_ragwrap,itm_bone_cudgel_heavy,itm_twohand_wood_club,itm_bone_cudgel,itm_wood_club,itm_orc_simple_spear,itm_orc_slasher,itm_metal_scraps_bad],
      attr_orc_tier_1,wp_orc_tier_1,knows_athletics_1|knows_power_strike_1,orc_face3,orc_face4],
["tribal_orc","Tribal_Orc","Tribal_Orcs",tf_orc| tf_no_capture_alive,0,0,fac_tribal_orcs,
   [itm_orc_tribal_a,itm_orc_tribal_b,itm_orc_tribal_c,itm_orc_tribal_c,itm_bone_cudgel_heavy,itm_bone_cudgel,itm_wood_club,itm_orc_simple_spear,itm_orc_slasher,itm_metal_scraps_bad],
      attr_orc_tier_1,wp_orc_tier_1,knows_athletics_1,orc_face1,orc_face2],
["tribal_orc_warrior","Tribal_Orc_Warrior","Tribal_Orc_Warriors",tf_orc| tfg_armor| tf_no_capture_alive,0,0,fac_tribal_orcs,
   [itm_orc_tribal_b,itm_orc_tribal_c,itm_orc_tribal_c,itm_bone_cudgel_heavy,itm_bone_cudgel,itm_wood_club,itm_twohand_wood_club,itm_orc_simple_spear,itm_orc_sledgehammer,itm_wood_club,itm_orc_simple_spear,itm_orc_club_c,itm_orc_slasher,itm_orc_axe,itm_metal_scraps_bad],
      attr_orc_tier_2,wp_orc_tier_2,knows_athletics_2|knows_power_strike_1,orc_face7,orc_face6],	
["tribal_orc_chief","Tribal_Orc_Chief","Tribal_Orc_Chiefs",tf_orc| tfg_armor| tfg_helm| tf_no_capture_alive,0,0,fac_tribal_orcs,
   [itm_orc_coif,itm_orc_tribal_b,itm_orc_tribal_c,itm_orc_tribal_c,itm_bone_cudgel_heavy,itm_bone_cudgel,itm_orc_sabre,itm_orc_simple_spear,itm_orc_ragwrap,itm_orc_slasher,itm_orc_axe,itm_metal_scraps_bad],
attr_orc_tier_3,wp_orc_tier_3,knows_athletics_4|knows_power_strike_3,orc_face1,orc_face2],

["future_troop_6","Mountain_Goblin","Mountain_Goblins",tf_orc| tf_no_capture_alive,0,0,fac_tribal_orcs,
   [itm_orc_tribal_a,itm_orc_tribal_b,itm_orc_tribal_c,itm_orc_tribal_c,itm_orc_shield_a,itm_orc_shield_b,itm_orc_shield_c,itm_orc_ragwrap,itm_bone_cudgel_heavy,itm_twohand_wood_club,itm_bone_cudgel,itm_wood_club,itm_orc_simple_spear,itm_orc_sledgehammer,],
      attr_orc_tier_2,wp_orc_tier_2,knows_athletics_3|knows_power_strike_2,orc_face3,orc_face4],
["future_troop_7","Tribal_Orc","Tribal_Orcs",tf_orc| tf_no_capture_alive,0,0,fac_tribal_orcs,
   [itm_orc_tribal_a,itm_orc_tribal_b,itm_orc_tribal_c,itm_orc_tribal_c,itm_bone_cudgel_heavy,itm_bone_cudgel,itm_twohand_wood_club,itm_wood_club,itm_orc_simple_spear,itm_orc_sledgehammer,itm_wood_club,itm_orc_simple_spear,itm_orc_sledgehammer,],
      attr_orc_tier_1,wp_orc_tier_1,knows_athletics_3,orc_face1,orc_face2],
["future_troop_8","Tribal_Orc_Warrior","Tribal_Orc_Warriors",tf_orc| tfg_armor| tf_no_capture_alive,0,0,fac_tribal_orcs,
   [itm_orc_tribal_b,itm_orc_tribal_c,itm_orc_tribal_c,itm_bone_cudgel_heavy,itm_bone_cudgel,itm_wood_club,itm_twohand_wood_club,itm_orc_simple_spear,itm_orc_sledgehammer,itm_wood_club,itm_orc_simple_spear,itm_orc_sledgehammer,],
      attr_orc_tier_2,wp_orc_tier_2,knows_athletics_4,orc_face7,orc_face6],	
["future_troop_9","Tribal_Orc_Chief","Tribal_Orc_Chiefs",tf_orc| tfg_armor| tfg_helm| tf_no_capture_alive,0,0,fac_tribal_orcs,
   [itm_orc_coif,itm_orc_tribal_b,itm_orc_tribal_c,itm_orc_tribal_c,itm_bone_cudgel_heavy,itm_bone_cudgel,itm_orc_sabre,itm_orc_simple_spear,itm_orc_ragwrap,itm_orc_slasher,],
attr_orc_tier_3,wp_orc_tier_3,knows_athletics_4|knows_power_strike_3,orc_face1,orc_face2],
["future_troop_10","Tribal_Orc_Chief","Tribal_Orc_Chiefs",tf_orc| tfg_armor| tfg_helm| tf_no_capture_alive,0,0,fac_tribal_orcs,
   [itm_orc_coif,itm_orc_tribal_b,itm_orc_tribal_c,itm_orc_tribal_c,itm_bone_cudgel_heavy,itm_bone_cudgel,itm_orc_sabre,itm_orc_simple_spear,itm_orc_ragwrap,itm_orc_slasher,],
attr_orc_tier_3,wp_orc_tier_3,knows_athletics_4|knows_power_strike_3,orc_face1,orc_face2],

#Add new troops here, right before trp_last!

["last","BUG","BUG",0,0,0,fac_commoners,[],0,0,0,0],    #the last troop must stay a stub, so that range calls for all troops include the last but one troop.
# For future troop additions, always make sure to fix trp_last overwrite in script_update_savegame
]
 
#
#WOODMEN
upgrade2(troops,"i1_woodmen_man","i2_woodmen_forester","a2_woodmen_tracker")
upgrade(troops,"i2_woodmen_forester","i3_woodmen_skilled_forester")
upgrade(troops,"i3_woodmen_skilled_forester","i4_woodmen_axemen")
upgrade(troops,"i4_woodmen_axemen","i5_woodmen_night_guard")
upgrade(troops,"a2_woodmen_tracker","a3_woodmen_scout")
upgrade(troops,"a3_woodmen_scout","a4_woodmen_archer")
upgrade(troops,"a4_woodmen_archer","a5_woodmen_night_stalker")
#BEORNINGS
upgrade(troops,"i1_beorning_man","i2_beorning_warrior")
upgrade2(troops,"i2_beorning_warrior","i3_beorning_tolltacker","i3_beorning_carrock_lookout")
upgrade(troops,"i3_beorning_tolltacker","i4_beorning_sentinel")
upgrade(troops,"i4_beorning_sentinel","i5_beorning_warden_of_the_ford")
upgrade(troops,"i5_beorning_warden_of_the_ford","i6_beorning_bear_warrior")
upgrade(troops,"i3_beorning_carrock_lookout","i4_beorning_carrock_fighter")
upgrade(troops,"i4_beorning_carrock_fighter","i5_beorning_carrock_berserker")
##LOSSARNACH
upgrade(troops,"i1_loss_woodsman","i2_loss_axeman")
upgrade(troops,"i2_loss_axeman","i3_loss_vet_axeman")
upgrade(troops,"i3_loss_vet_axeman","i4_loss_heavy_axeman")
upgrade(troops,"i4_loss_heavy_axeman","i5_loss_axemaster")
##LAMEDON
upgrade(troops,"i1_lam_clansman","i2_lam_footman")
upgrade(troops,"i2_lam_footman","i3_lam_veteran")
upgrade(troops,"i3_lam_veteran","i4_lam_warrior")
upgrade2(troops,"i4_lam_warrior","i5_lam_champion","c5_lam_knight")
##PINNATH GELIN
upgrade2(troops,"i1_pinnath_plainsman","c2_pinnath_rider","a2_pinnath_bowman")
upgrade(troops,"c2_pinnath_rider","c3_pinnath_knight")
upgrade(troops,"a2_pinnath_bowman","a3_pinnath_archer")
##BLACK ROOT VALE
upgrade2(troops,"a1_blackroot_hunter","a2_blackroot_bowman","i2_blackroot_footman")
upgrade(troops,"a2_blackroot_bowman","a3_blackroot_archer")
upgrade(troops,"a3_blackroot_archer","a5_blackroot_shadow_hunter")
upgrade(troops,"i2_blackroot_footman","i3_blackroot_spearman")
upgrade(troops,"i3_blackroot_spearman","a5_blackroot_shadow_hunter")
###PELARGIR
upgrade2(troops,"i1_pel_watchman","a2_pel_marine","i2_pel_infantry")
upgrade(troops,"i2_pel_infantry","i3_pel_vet_infantry")
upgrade(troops,"a2_pel_marine","a3_pel_vet_marine")
##DOL AMROTH
upgrade(troops,"i1_amroth_recruit","c2_amroth_squire")
upgrade(troops,"c2_amroth_squire","c3_amroth_vet_squire")
upgrade(troops,"c3_amroth_vet_squire","c4_amroth_knight")
upgrade(troops,"c4_amroth_knight","c5_amroth_vet_knight")
upgrade(troops,"c5_amroth_vet_knight","c6_amroth_swan_knight")
#LORIEN
upgrade2(troops,"a1_lorien_scout","a2_lorien_warden","a2_lorien_archer")
upgrade2(troops,"a2_lorien_warden","a3_lorien_vet_warden","i3_lorien_inf")
upgrade2(troops,"a3_lorien_vet_warden","a4_lorien_gal_warden","a4_lorien_gal_archer")
upgrade2(troops,"a4_lorien_gal_warden","a5_lorien_gal_royal_warden","i5_lorien_gal_royal_inf")
upgrade(troops,"a5_lorien_gal_royal_warden","a6_lorien_grey_warden")
upgrade(troops,"a2_lorien_archer","a3_lorien_vet_archer")
upgrade(troops,"a3_lorien_vet_archer","a4_lorien_gal_archer")
upgrade(troops,"a4_lorien_gal_archer","a5_lorien_gal_royal_archer")
upgrade(troops,"i3_lorien_inf","i4_lorien_gal_inf")
upgrade(troops,"i4_lorien_gal_inf","i5_lorien_gal_royal_inf")
#MIRKWOOD
upgrade2(troops,"a1_greenwood_scout","a2_greenwood_veteran_scout","i2_greenwood_infantry")
upgrade2(troops,"a2_greenwood_veteran_scout","a3_greenwood_archer","a3_greenwood_sentinel")
upgrade(troops,"a3_greenwood_archer","a4_greenwood_veteran_archer")
upgrade(troops,"a4_greenwood_veteran_archer","a5_greenwood_master_archer")
upgrade(troops,"a5_greenwood_master_archer","a6_greenwood_chosen_marksman")
upgrade(troops,"i2_greenwood_infantry","i3_greenwood_vet_infantry")
upgrade(troops,"i3_greenwood_vet_infantry","i4_greenwood_elite_infantry")
upgrade2(troops,"i4_greenwood_elite_infantry","i5_greenwood_chosen_spearmaster","i5_greenwood_chosen_shieldmaster")
upgrade(troops,"a3_greenwood_sentinel","a4_greenwood_vet_sentinel")
upgrade(troops,"a4_greenwood_vet_sentinel","a5_greenwood_vigilant")
#RIVENDELL
upgrade(troops,"a1_riv_scout","a2_riv_vet_scout")
upgrade2(troops,"a2_riv_vet_scout","a3_riv_archer","i3_riv_swordbearer")
upgrade(troops,"a3_riv_archer","a4_riv_vet_archer")
upgrade2(troops,"a4_riv_vet_archer","a5_riv_master_archer","ac5_riv_rider")
upgrade(troops,"a5_riv_master_archer","a6_riv_guardian")
upgrade(troops,"ac5_riv_rider","ac6_riv_knight")
upgrade(troops,"i3_riv_swordbearer","i4_riv_vet_swordbearer")
upgrade2(troops,"i4_riv_vet_swordbearer","i5_riv_swordmaster","ac5_riv_rider")
upgrade2(troops,"i5_riv_swordmaster","i6_riv_champion","a6_riv_guardian")
#DUNEADAIN
upgrade(troops,"a1_arnor_scout","a2_arnor_vet_scout" )
upgrade2(troops,"a2_arnor_vet_scout","i3_arnor_swordsman","a3_arnor_ranger" )
upgrade2(troops,"i3_arnor_swordsman","i4_arnor_vet_swordsman","c4_arnor_horseman" )
upgrade2(troops,"i4_arnor_vet_swordsman","i5_arnor_champion","a5_arnor_master_ranger" )
upgrade(troops,"c4_arnor_horseman","c5_arnor_knight" )
upgrade(troops,"a3_arnor_ranger","a4_arnor_vet_ranger" )
upgrade2(troops,"a4_arnor_vet_ranger","a5_arnor_master_ranger","i5_arnor_champion" )
#Gondor infantry
upgrade(troops,"i1_gon_levy","i2_gon_watchman" )
upgrade2(troops,"i2_gon_watchman","i3_gon_footman","a3_gon_bowman" )
upgrade2(troops,"i3_gon_footman","i4_gon_swordsman","i4_gon_spearman" )
upgrade(troops,"i4_gon_swordsman","i5_gon_vet_swordsman" )
upgrade(troops,"i5_gon_vet_swordsman","i6_gon_tower_swordsman" )
upgrade(troops,"i4_gon_spearman","i5_gon_vet_spearman" )
upgrade(troops,"i5_gon_vet_spearman","i6_gon_tower_spearman" )
#Gondor Noble Line
upgrade(troops,"c1_gon_nobleman","c2_gon_squire" )
upgrade(troops,"c2_gon_squire","c3_gon_vet_squire" )
upgrade(troops,"c3_gon_vet_squire","c4_gon_knight" )
upgrade(troops,"c4_gon_knight","c5_gon_vet_knight" )
upgrade(troops,"c5_gon_vet_knight","c6_gon_tower_knight" )
#Gondor archers
upgrade(troops,"a3_gon_bowman","a4_gon_archer" )
upgrade(troops,"a4_gon_archer","a5_gon_vet_archer" )
upgrade(troops,"a5_gon_vet_archer","a6_gon_tower_archer" )
upgrade(troops,"a4_ithilien_ranger","a5_ithilien_vet_ranger" )
upgrade(troops,"a5_ithilien_vet_ranger","a6_ithilien_master_ranger" )
#ROHAN
upgrade2(troops,"i1_rohan_youth","c2_squire_of_rohan","i2_guardsman_of_rohan")
upgrade(troops,"i2_guardsman_of_rohan","i3_footman_of_rohan")
upgrade(troops,"i3_footman_of_rohan","i4_veteran_footman_of_rohan")
upgrade2(troops,"i4_veteran_footman_of_rohan","i5_elite_footman_of_rohan","i5_raider_of_rohan")
upgrade2(troops,"i5_raider_of_rohan","i6_2h_guard_of_rohan","i6_frealaf_raider")
upgrade2(troops,"i5_elite_footman_of_rohan","i6_warden_of_methuseld","i6_footman_guard_of_rohan")
upgrade(troops,"ac3_skirmisher_of_rohan","ac4_veteran_skirmisher_of_rohan")
upgrade(troops,"ac4_veteran_skirmisher_of_rohan","ac5_elite_skirmisher_of_rohan")
upgrade(troops,"ac5_elite_skirmisher_of_rohan","ac6_skirmisher_guard_of_rohan")
upgrade(troops,"c4_lancer_of_rohan","c5_elite_lancer_of_rohan")
upgrade(troops,"c5_elite_lancer_of_rohan","c6_lancer_guard_of_rohan")
upgrade2(troops,"c2_squire_of_rohan","c3_rider_of_rohan","ac3_skirmisher_of_rohan")
upgrade2(troops,"c3_rider_of_rohan","c4_veteran_rider_of_rohan","c4_lancer_of_rohan")
upgrade(troops,"c4_veteran_rider_of_rohan","c5_elite_rider_of_rohan")
upgrade(troops,"c5_elite_rider_of_rohan","c6_rider_guard_of_rohan")
#HARAD
upgrade2(troops,"i1_harad_levy","i3_harad_infantry","a3_harad_hunter")
upgrade2(troops,"c2_harondor_scout","c3_harondor_rider","ac3_harondor_skirmisher")
upgrade2(troops,"i3_harad_infantry","i4_harad_spearman","i4_harad_swordsman")
upgrade(troops,"i4_harad_swordsman","i5_harad_lion_guard")
upgrade(troops,"i4_harad_spearman","i5_harad_tiger_guard")
upgrade(troops,"c3_harondor_rider","c4_harondor_light_cavalry")
upgrade(troops,"c4_harondor_light_cavalry","c5_harondor_serpent_knight")
upgrade(troops,"a3_harad_hunter","a4_harad_archer")
upgrade(troops,"a4_harad_archer","a5_harad_eagle_guard")
upgrade(troops,"ac3_harondor_skirmisher","ac4_harondor_horse_archer")
upgrade(troops,"ac4_harondor_horse_archer","ac5_harondor_black_snake")
upgrade(troops,"i2_far_harad_tribesman","i4_far_harad_champion")
upgrade(troops,"i4_far_harad_champion","i5_far_harad_panther_guard")
#DUNLAND
upgrade(troops,"i1_dun_wildman","i2_dun_warrior")
upgrade2(troops,"i2_dun_warrior","i3_dun_vet_warrior","i3_dun_pikeman")
upgrade(troops,"i3_dun_pikeman","i4_dun_vet_pikeman")
upgrade(troops,"ac4_dun_crebain_rider","ac5_dun_raven_rider")
upgrade2(troops,"i3_dun_vet_warrior","i4_dun_wolf_warrior","ac4_dun_crebain_rider")
upgrade2(troops,"i4_dun_wolf_warrior","a5_dun_night_wolf","i5_dun_wolf_guard")
#EASTERLINGS
upgrade2(troops,"i1_khand_bondsman","i2_khand_pit_dog","c2_khand_pony_rider")
upgrade2(troops,"i2_khand_pit_dog","i3_khand_warrior","i3_khand_pitfighter")
upgrade2(troops,"i3_khand_warrior","i4_khand_vet_warrior","i4_khand_halberdier")
upgrade(troops,"i4_khand_vet_warrior","i5_khand_war_master")
upgrade2(troops,"c2_khand_pony_rider","c3_khand_horseman","ac3_khand_skirmisher")
upgrade(troops,"c3_khand_horseman","c4_khand_heavy_horseman")
upgrade2(troops,"c4_khand_heavy_horseman","c5_khand_kataphrakt","c5_khand_lance_kataphrakt")
upgrade(troops,"i3_khand_pitfighter","i4_khand_pit_champion")
upgrade(troops,"i4_khand_halberdier","i5_khand_halberd_master")
upgrade(troops,"i4_khand_pit_champion","i5_khand_pit_master")
upgrade(troops,"ac3_khand_skirmisher","ac4_khand_vet_skirmisher")
upgrade(troops,"ac4_khand_vet_skirmisher","ac5_khand_heavy_skirmisher")
#CORSAIRS
upgrade2(troops,"i1_corsair_youth","i2_corsair_warrior","a2_corsair_marine")
upgrade2(troops,"i2_corsair_warrior","i3_corsair_swordsman","i3_corsair_spearman")
upgrade(troops,"i3_corsair_spearman","i4_corsair_veteran_spearman")
upgrade(troops,"i4_corsair_raider","i5_corsair_night_raider")
upgrade(troops,"a2_corsair_marine","a3_corsair_marksman")
upgrade(troops,"a3_corsair_marksman","a4_corsair_veteran_marksman")
upgrade2(troops,"a4_corsair_veteran_marksman","a5_corsair_master_marksman","a5_corsair_master_assassin")
upgrade2(troops,"i3_corsair_swordsman","i4_corsair_veteran_swordsman","i4_corsair_raider")
upgrade(troops,"i4_corsair_veteran_swordsman","i5_corsair_master_swordsman")
#upgrade(troops,"a4_corsair_assassin","a5_corsair_master_assassin")
upgrade2(troops,"i4_corsair_veteran_spearman","i5_corsair_master_spearman","i5_corsair_master_pikeman")
#ISENGARD ORCS
upgrade2(troops,"i1_isen_orc_snaga","i2_isen_orc","ac2_isen_wolf_rider")
upgrade2(troops,"i2_isen_orc","i3_isen_large_orc","i3_isen_large_orc_despoiler")
upgrade(troops,"i3_isen_large_orc","i4_isen_fell_orc")
upgrade(troops,"i3_isen_large_orc_despoiler","i4_isen_fell_orc_despoiler")
upgrade(troops,"ac2_isen_wolf_rider","ac3_isen_warg_rider")
upgrade(troops,"ac3_isen_warg_rider","ac4_isen_white_hand_rider")
#ISENGARD URUK-HAIS
upgrade(troops,"a2_isen_uruk_tracker","a3_isen_large_uruk_tracker")
upgrade(troops,"a3_isen_large_uruk_tracker","a4_isen_fighting_uruk_tracker")
upgrade2(troops,"i1_isen_uruk_snaga","i2_isen_uruk","a2_isen_uruk_tracker")
upgrade2(troops,"i2_isen_uruk","i3_isen_large_uruk","i3_isen_uruk_pikeman")
upgrade(troops,"i3_isen_large_uruk","i4_isen_fighting_uruk_warrior")
upgrade2(troops,"i4_isen_fighting_uruk_warrior","i5_isen_fighting_uruk_champion","i6_isen_uruk_berserker")
upgrade(troops,"i3_isen_uruk_pikeman","i4_isen_fighting_uruk_pikeman")
#upgrade(troops,"i4_isen_fighting_uruk_pikeman","i6_isen_uruk_berserker")
#MORDOR ORCS
upgrade2(troops,"i1_mordor_orc_snaga","i2_mordor_orc","a2_mordor_orc_archer")
upgrade2(troops,"i2_mordor_orc","i3_mordor_large_orc","c3_mordor_warg_rider")
upgrade2(troops,"i3_mordor_large_orc","i4_mordor_fell_orc","i4_mordor_fell_morgul_orc")
upgrade(troops,"a3_guldur_large_orc_tracker","a4_guldur_fell_orc_tracker")
upgrade(troops,"a2_mordor_orc_archer","a3_mordor_large_orc_archer")
upgrade(troops,"a3_mordor_large_orc_archer","a4_mordor_fell_orc_archer")
upgrade(troops,"c3_mordor_warg_rider","c4_mordor_great_warg_rider")
upgrade(troops,"i2_mordor_morgul_orc","i4_mordor_fell_morgul_orc")
#MORDOR URUKS
upgrade(troops,"i1_mordor_uruk_snaga","i2_mordor_uruk")
upgrade2(troops,"i2_mordor_uruk","i3_mordor_large_uruk","i3_mordor_uruk_slayer")
upgrade(troops,"i3_mordor_large_uruk","i4_mordor_fell_uruk")
upgrade(troops,"i3_mordor_uruk_slayer","i4_mordor_fell_uruk_slayer")
#GULDUR ORCS
upgrade2(troops,"i1_guldur_orc_snaga","a2_guldur_orc_tracker","i2_mordor_orc")
upgrade(troops,"a2_guldur_orc_tracker","a3_guldur_large_orc_tracker")
#MORIA ORCS
upgrade(troops,"c3_moria_wolf_rider","c4_moria_warg_rider")
upgrade(troops,"c4_moria_warg_rider","c5_moria_clan_rider")
upgrade2(troops,"i1_moria_snaga","i2_moria_goblin","a2_moria_goblin_archer")
upgrade2(troops,"i2_moria_goblin","i3_moria_large_goblin","c3_moria_wolf_rider")
upgrade(troops,"a2_moria_goblin_archer","a3_moria_large_goblin_archer")
upgrade(troops,"a3_moria_large_goblin_archer","a4_moria_fell_goblin_archer")
upgrade(troops,"i3_moria_large_goblin","i4_moria_fell_goblin")
upgrade2(troops,"i4_moria_fell_goblin","i5_moria_deep_dweller","i5_moria_orc_chieftain")
#GUNDABAD ORCS
upgrade(troops,"i1_gunda_goblin","i2_gunda_orc")
upgrade2(troops,"i2_gunda_orc","i3_gunda_orc_fighter","c3_gunda_goblin_rider")
upgrade(troops,"i3_gunda_orc_fighter","i4_gunda_orc_warrior")
upgrade2(troops,"i4_gunda_orc_warrior","i5_gunda_orc_champion","i4_gunda_orc_berserker")
upgrade2(troops,"c3_gunda_goblin_rider","ca4_gunda_skirmisher","c4_gunda_warg_rider")
upgrade(troops,"ca4_gunda_skirmisher","ca5_gunda_clan_skirmisher")
upgrade(troops,"c4_gunda_warg_rider","c5_gunda_clan_rider")
#BLACK NUMENORIANS
upgrade(troops,"i2_mordor_num_renegade","i3_mordor_num_warrior")
upgrade2(troops,"i3_mordor_num_warrior","i4_mordor_num_vet_warrior","c4_mordor_num_horseman")
upgrade2(troops,"i4_mordor_num_vet_warrior","i5_mordor_num_champion","i5_mordor_num_assassin")
upgrade(troops,"c4_mordor_num_horseman","c5_mordor_num_knight")
#DWARVES
upgrade2(troops,"i1_dwarf_apprentice","i2_dwarf_warrior","a2_dwarf_lookout")
upgrade(troops,"i2_dwarf_warrior","i3_dwarf_hardened_warrior")
upgrade2(troops,"i3_dwarf_hardened_warrior","i4_dwarf_axeman","i4_dwarf_spearman")
upgrade(troops,"i4_dwarf_axeman","i5_dwarf_expert_axeman")
upgrade(troops,"i5_dwarf_expert_axeman","i6_dwarf_longbeard_axeman")
upgrade(troops,"i4_dwarf_spearman","i5_dwarf_pikeman")
upgrade2(troops,"i5_dwarf_pikeman","i6_dwarf_longpikeman","i6_dwarf_longaxeman")
upgrade(troops,"a2_dwarf_lookout","a3_dwarf_scout")
upgrade(troops,"a3_dwarf_scout","a4_dwarf_bowman")
#upgrade(troops,"a4_dwarf_bowman","dwarven_archer")
#upgrade(troops,"dwarven_archer","marksman_of_ravenhill")
upgrade(troops,"i2_iron_hills_miner","i3_iron_hills_warrior")
upgrade(troops,"i3_iron_hills_warrior","i4_iron_hills_infantry")
upgrade(troops,"i4_iron_hills_infantry","i5_iron_hills_battle_dwarf")
upgrade(troops,"i5_iron_hills_battle_dwarf","i6_iron_hills_grors_guard")
#DALE
upgrade2(troops,"i1_dale_militia","i2_dale_man_at_arms","a2_dale_scout")
upgrade2(troops,"i2_dale_man_at_arms","i3_dale_swordsman","i3_dale_spearman")
upgrade(troops,"i3_dale_swordsman","i4_dale_sergeant")
upgrade(troops,"i4_dale_sergeant","i5_dale_hearthman")
upgrade(troops,"i3_dale_spearman","i4_dale_billman")
upgrade(troops,"i4_dale_billman","i5_dale_bill_master")
upgrade(troops,"c2_rhovanion_retainer","c3_rhovanion_auxilia")
upgrade(troops,"c3_rhovanion_auxilia","c4_rhovanion_rider")
upgrade2(troops,"c4_rhovanion_rider","ac5_rhovanion_marchwarden","c5_rhovanion_noble")
upgrade(troops,"a2_dale_scout","a3_dale_bowman")
upgrade(troops,"a3_dale_bowman","a4_dale_archer")
upgrade(troops,"a4_dale_archer","a5_barding_bowman")
#RHUN
upgrade2(troops,"i1_rhun_tribesman","ac2_rhun_horse_scout","i2_rhun_tribal_warrior")
upgrade2(troops,"ac2_rhun_horse_scout","ac3_rhun_horse_archer","c3_rhun_swift_horseman")
upgrade(troops,"ac3_rhun_horse_archer","ac4_rhun_veteran_horse_archer")
upgrade(troops,"ac4_rhun_veteran_horse_archer","ac5_rhun_balchoth_horse_archer")
upgrade(troops,"c3_rhun_swift_horseman","c4_rhun_veteran_swift_horseman")
upgrade(troops,"c4_rhun_veteran_swift_horseman","c5_rhun_falcon_horseman")
upgrade(troops,"i2_rhun_tribal_warrior","i3_rhun_tribal_infantry")
upgrade(troops,"i3_rhun_tribal_infantry","i4_rhun_vet_infantry")
upgrade(troops,"i4_rhun_vet_infantry","i5_rhun_ox_warrior")
upgrade(troops,"c2_rhun_horseman","c3_rhun_outrider")
upgrade(troops,"c3_rhun_outrider","c4_rhun_noble_rider")
upgrade(troops,"c4_rhun_noble_rider","c5_rhun_warrider")
upgrade(troops,"c5_rhun_warrider","c6_rhun_warlord")
#BANDITS
upgrade(troops,"tribal_orc","tribal_orc_warrior")
#upgrade(troops,"tribal_orc_warrior","tribal_orc_chief")
#TROLLS
upgrade(troops,"moria_troll","moria_vet_troll")
upgrade(troops,"gunda_troll","gunda_vet_troll")
upgrade(troops,"isen_troll","isen_vet_troll")
upgrade(troops,"mordor_troll","mordor_vet_troll")



