#OUTPUT troops.py
import random
 
from header_common import *
from header_items import *
from header_troops import *
from header_skills import *
from ID_factions import *
from ID_items import *
from ID_scenes import *
from module_constants import *

 
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
knows_common = knows_riding_1|knows_trade_1|knows_inventory_management_2|knows_prisoner_management_1|knows_leadership_1
knows_common_dwarf = knows_riding_10|knows_horse_archery_10|knows_trade_2|knows_inventory_management_4|knows_prisoner_management_1|knows_leadership_1
def_attrib = str_7| agi_5| int_4| cha_4
 
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
knight_skills_1 = knows_riding_4|knows_ironflesh_2|knows_power_strike_3|knows_athletics_1|knows_tactics_2|knows_prisoner_management_1|knows_leadership_3
knight_skills_2 = knows_riding_4|knows_ironflesh_3|knows_power_strike_4|knows_athletics_2|knows_tactics_3|knows_prisoner_management_2|knows_leadership_5
knight_skills_3 = knows_riding_4|knows_ironflesh_4|knows_power_strike_5|knows_athletics_3|knows_tactics_4|knows_prisoner_management_2|knows_leadership_6
knight_skills_4 = knows_riding_4|knows_ironflesh_5|knows_power_strike_6|knows_athletics_4|knows_tactics_5|knows_prisoner_management_3|knows_leadership_7
knight_skills_5 = knows_riding_4|knows_ironflesh_6|knows_power_strike_7|knows_athletics_5|knows_tactics_6|knows_prisoner_management_3|knows_leadership_9
 
#TLD troop attributes
attr_tier_1 =  str_7| agi_5| int_4| cha_4|level(5)
attr_tier_2 = str_10| agi_7| int_4| cha_4|level(10)
attr_tier_3 = str_13|agi_11| int_4| cha_4|level(15)
attr_tier_4 = str_15|agi_15| int_4| cha_4|level(20)
attr_tier_5 = str_18|agi_18| int_4| cha_4|level(30)
attr_tier_6 = str_20|agi_20|int_20|cha_20|level(40)
attr_tier_7 = str_22|agi_22|int_22|cha_22|level(45)

attr_elf_tier_1 = str_12|agi_12| int_4| cha_4|level(6)
attr_elf_tier_2 = str_14|agi_14| int_4| cha_4|level(12)
attr_elf_tier_3 = str_18|agi_18| int_4| cha_4|level(18)
attr_elf_tier_4 = str_18|agi_24| int_4| cha_4|level(26)
attr_elf_tier_5 = str_24|agi_27| int_4| cha_4|level(38) #GA upped higher levels a bit
attr_elf_tier_6 = str_30|agi_30|int_20|cha_20|level(50)

attr_dwarf_tier_1 =  str_9| agi_6| int_4| cha_4|level(6)
attr_dwarf_tier_2 = str_12| agi_9| int_4| cha_4|level(11)
attr_dwarf_tier_3 = str_15|agi_11| int_4| cha_4|level(16)
attr_dwarf_tier_4 = str_18|agi_13| int_4| cha_4|level(21)
attr_dwarf_tier_5 = str_18|agi_18| int_4| cha_4|level(35) #GA upped 2 highest levels a bit
attr_dwarf_tier_6 = str_24|agi_18| int_4| cha_4|level(48)

attr_orc_tier_1 =  str_5| agi_5| int_4| cha_4|level(4)
attr_orc_tier_2 =  str_7| agi_7| int_4| cha_4|level(9)
attr_orc_tier_3 =  str_9| agi_8| int_4| cha_4|level(14)
attr_orc_tier_4 = str_11| agi_9| int_4| cha_4|level(19)
attr_orc_tier_5 = str_14|agi_10| int_4| cha_4|level(28)
attr_orc_tier_6 = str_17|agi_12| int_4| cha_4|level(37)

#TLD weapon proficiencies
wp_tier_1 = wp(70)
wp_tier_2 = wp(100)
wp_tier_3 = wp(135)
wp_tier_4 = wp(170)
wp_tier_5 = wp(200)
wp_tier_6 = wp(300)
wp_tier_7 = wp(400)

wp_elf_tier_1 = wp(240)
wp_elf_tier_2 = wp(280)
wp_elf_tier_3 = wp(310)
wp_elf_tier_4 = wp(360)
wp_elf_tier_5 = wp(410)
wp_elf_tier_6 = wp(460)

wp_dwarf_tier_1 = wp(100)
wp_dwarf_tier_2 = wp(160)
wp_dwarf_tier_3 = wp(210)
wp_dwarf_tier_4 = wp(240)
wp_dwarf_tier_5 = wp(300)
wp_dwarf_tier_6 = wp(350)

wp_orc_tier_1 = wp(70)
wp_orc_tier_2 = wp(95)
wp_orc_tier_3 = wp(105)
wp_orc_tier_4 = wp(125)
wp_orc_tier_5 = wp(140)
wp_orc_tier_6 = wp(155)

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

#NAMES:
#
itm_warhorse = itm_hunter
itm_charger = itm_hunter
 
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
   [itm_leather_boots,itm_orc_club_a,itm_black_tunic],
      attr_tier_1,wp_tier_1,knows_common,mercenary_face_1,mercenary_face_2],
["tutorial_archer","Archer","Archers",tfg_boots| tfg_armor| tfg_ranged,0,0,fac_commoners,
   [itm_leather_boots,itm_short_bow,itm_arrows,itm_black_tunic],
      attr_tier_1,wp_tier_1,knows_common|knows_power_draw_4,mercenary_face_1,mercenary_face_2],
["tutorial_swordsman","Swordsman","Swordsmen",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,itm_black_tunic,itm_practice_sword],
      attr_tier_1,wp_tier_1,knows_common,mercenary_face_1,mercenary_face_2],
["novice_fighter","Novice_Fighter","Novice_Fighters",tfg_boots| tfg_armor,0,0,fac_commoners,
   [itm_leather_boots,	],
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
["farmer","Farmer","Farmers",tfg_armor,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,man_face_middle_1,man_face_old_2],
["townsman","Townsman","Townsmen",tfg_boots| tfg_armor,0,0,fac_dale,
   [itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,mercenary_face_1,mercenary_face_2],
["watchman","Watchman","Watchmen",tfg_boots| tfg_armor| tfg_shield,0,0,fac_dale,
   [itm_dale_sword,itm_spear,itm_leather_jerkin,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common|knows_shield_1,mercenary_face_1,mercenary_face_2],
["mercenaries_end","bug","bug",0,0,0,fac_commoners,
   [],
      0,1,0,0],
#soldiers:
#######################################
#@@@@@@@@@@@@%%%%%%%%%%%%%%%%%%
#Brigands
# ["brigand_lord","Brigand_Lord","Brigand_Lords",tf_mounted|tfg_gloves|tfg_armor|tfg_helmet|tfg_horse|tfg_boots,0,0,fac_brigands,
# [itm_leather_jerkin,itm_sword_two_handed_a,itm_sword_two_handed_a,itm_two_handed_axe,itm_wooden_shield,itm_hunter,itm_leather_gloves,itm_splinted_greaves],
# def_attrib|level(35),wp(205),knows_common|knows_tactics_2|knows_riding_5|knows_shield_2|knows_power_strike_4|knows_ironflesh_4,bandit_face1,bandit_face2],
# ["brigand_lieutenant","Brigand_Lieutenant","Brigand_Lieutenants",tf_mounted|tfg_gloves|tfg_armor|tfg_helmet|tfg_horse|tfg_boots,0,0,fac_brigands,
# [itm_leather_jerkin,itm_sword_medieval_c,itm_sword_two_handed_a,itm_sword_two_handed_a,itm_two_handed_axe,itm_wooden_shield,itm_fur_covered_shield,itm_hunter,itm_leather_gloves,itm_leather_boots],
# def_attrib|level(25),wp(165),knows_common|knows_tactics_1|knows_riding_5|knows_shield_2|knows_power_strike_3|knows_ironflesh_3,bandit_face1,bandit_face2],
# ["master_brigand","Master_Brigand","Master_Brigands",tf_mounted|tfg_gloves|tfg_armor|tfg_helmet|tfg_horse|tfg_boots,0,0,fac_brigands,
# [itm_leather_jerkin,itm_sword_medieval_c,itm_sword_medieval_c,itm_sword_two_handed_a,itm_two_handed_axe,itm_wooden_shield,itm_hunter,itm_leather_gloves,itm_leather_boots],
# def_attrib|level(23),wp(170),knows_common|knows_riding_4|knows_shield_2|knows_power_strike_3|knows_ironflesh_3,bandit_face1,bandit_face2],
# ["veteran_brigand","Veteran_Brigand","Veteran_Brigands",tf_mounted|tfg_armor|tfg_helmet|tfg_horse|tfg_boots,0,0,fac_brigands,
# [itm_spear,itm_sword_medieval_c,itm_two_handed_axe,itm_sword_medieval_c,itm_fur_covered_shield,itm_leather_jerkin,itm_mail_boots,itm_saddle_horse,itm_hunter,itm_leather_boots],
# def_attrib|level(20),wp(120),knows_common|knows_riding_3|knows_shield_2|knows_power_strike_2|knows_ironflesh_2,bandit_face1,bandit_face2],
# ["brigand","Brigand","Brigands",tfg_armor|tfg_boots,0,0,fac_brigands,
# [itm_arrows,itm_sword_medieval_c,itm_sword_medieval_c,itm_wooden_shield,itm_wooden_shield,itm_short_bow,itm_fur_coat,itm_leather_boots,itm_leather_boots,itm_sumpter_horse],
# def_attrib|level(14),wp(100),knows_common|knows_shield_2|knows_power_strike_2|knows_ironflesh_1,bandit_face1,bandit_face2],
# ["cutthroat","Cutthroat","Cutthroats",tfg_armor|tfg_boots,0,0,fac_brigands,
# [itm_arrows,itm_sword_medieval_c,itm_wooden_shield,itm_wooden_shield,itm_short_bow,itm_fur_coat,itm_leather_boots,itm_sumpter_horse],
# def_attrib|level(9),wp(90),knows_common|knows_shield_2|knows_power_strike_1|knows_ironflesh_1,bandit_face1,bandit_face2],
# ["thug","Thug","looters",tfg_boots,0,0,fac_brigands,
# [itm_one_handed_war_axe_a,itm_linen_tunic, itm_fur_coat,itm_fur_coat,itm_leather_boots,itm_leather_boots],
# def_attrib|level(4),wp(80),knows_common,bandit_face1,pirate_face2],
# ["master_slaver","Master_Slaver","Master_Slavers",tf_mounted|tfg_gloves|tfg_armor|tfg_horse|tfg_boots,0,0,fac_brigands,
# [itm_quarter_staff,itm_fur_covered_shield,itm_leather_jerkin,itm_hunter,itm_courser,itm_leather_gloves,itm_leather_boots],
# def_attrib|level(23),wp(165),knows_common|knows_riding_4|knows_shield_2|knows_power_strike_3|knows_ironflesh_3,bandit_face1,bandit_face2],
# ["brigand_slaver","Brigand_Slaver","Brigand_Slavers",tf_mounted|tfg_armor|tfg_helmet|tfg_boots,0,0,fac_brigands,
# [itm_quarter_staff,itm_fur_covered_shield,itm_leather_jerkin,itm_mail_boots,itm_saddle_horse,itm_hunter],
# def_attrib|level(20),wp(125),knows_common|knows_riding_3|knows_shield_2|knows_power_strike_2|knows_ironflesh_2,bandit_face1,bandit_face2],
#Woodmen
["woodmen_youth","Woodman","Woodmen",tfg_armor| tfg_boots,0,0,fac_beorn,
   [itm_woodman_tunic,itm_leather_boots,itm_beorn_staff,],
      attr_tier_1,wp_tier_1,knows_common|knows_athletics_1|knows_power_strike_1|knows_ironflesh_1,rohan_face_younger_1,rohan_face_middle_2],
# unused - same role as woodmen_tracker
# ["woodmen_hunter","Woodmen_Hunter","Woodmen_Hunters",tfg_armor| tfg_boots,0,0,fac_beorn,
   # [itm_woodman_tunic,itm_leather_boots,itm_short_bow,itm_arrows,itm_beorn_staff,],
      # attr_tier_2,wp_tier_2,knows_common|knows_athletics_2|knows_power_draw_1|knows_ironflesh_1,rohan_face_younger_1,rohan_face_middle_2],
["woodmen_forester","Woodmen_Forester","Woodmen_Foresters",tfg_armor| tfg_boots,0,0,fac_beorn,
   [itm_woodman_tunic,itm_leather_boots,itm_beorn_axe,],
      attr_tier_2,wp_tier_2,knows_common|knows_athletics_2|knows_power_draw_2|knows_power_strike_2|knows_ironflesh_2,rohan_face_young_1,rohan_face_middle_2],
["woodmen_skilled_forester","Woodmen_Skilled_Forester","Woodmen_Skilled_Foresters",tfg_armor| tfg_boots,0,0,fac_beorn,
   [itm_woodman_tunic,itm_leather_boots,itm_beorn_axe,itm_beorn_battle_axe,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_power_draw_2|knows_power_strike_2|knows_ironflesh_2,rohan_face_young_1,rohan_face_middle_2],
["woodmen_axemen","Woodmen_Axeman","Woodmen_Axemen",tfg_armor| tfg_boots,0,0,fac_beorn,
   [itm_woodman_padded,itm_leather_boots,itm_leather_gloves,itm_beorn_helmet,itm_beorn_battle_axe,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_3|knows_power_draw_2|knows_power_strike_3|knows_ironflesh_3,rohan_face_young_1,rohan_face_old_2],
["woodmen_master_axemen","Woodmen_Master_Axeman","Woodmen_Master_Axemen",tfg_armor| tfg_helm| tfg_boots| tfg_gloves,0,0,fac_beorn,
   [itm_woodman_padded,itm_leather_boots,itm_leather_gloves,itm_beorn_helmet,itm_beorn_battle_axe,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_4|knows_power_draw_2|knows_power_strike_4|knows_ironflesh_4,rohan_face_middle_1,rohan_face_old_2],
["woodmen_tracker","Woodmen_Tracker","Woodmen_Trackers",tfg_ranged| tfg_armor| tfg_boots,0,0,fac_beorn,
   [itm_woodman_scout,itm_leather_boots,itm_rohan_shoes,itm_gondor_ranger_hood,itm_short_bow,itm_arrows,itm_beorn_axe,],
      attr_tier_2,wp_tier_2,knows_common|knows_athletics_2|knows_power_draw_1|knows_ironflesh_1,rohan_face_young_1,rohan_face_old_2],
["woodmen_scout","Woodmen_Scout","Woodmen_Scouts",tfg_ranged| tfg_armor| tfg_boots,0,0,fac_beorn,
   [itm_woodman_scout,itm_leather_boots,itm_gondor_ranger_hood,itm_short_bow,itm_arrows,itm_beorn_axe,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_power_draw_2|knows_power_strike_2|knows_ironflesh_2,rohan_face_young_1,rohan_face_middle_2],
["woodmen_archer","Woodmen_Archer","Woodmen_Archers",tfg_ranged| tfg_armor| tfg_helm|tfg_boots| tfg_gloves,0,0,fac_beorn,
   [itm_woodman_scout,itm_leather_boots,itm_leather_gloves,itm_beorn_helmet,itm_gondor_ranger_hood,itm_dale_bow,itm_arrows,itm_beorn_axe,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_3|knows_power_draw_2|knows_power_strike_3|knows_ironflesh_3,rohan_face_young_1,rohan_face_old_2],
["fell_huntsmen_of_mirkwood","Expert_Huntsman_of_Mirkwood","Expert_Huntsmen_of_Mirkwood",tfg_ranged| tfg_gloves| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,
   [itm_woodman_padded,itm_leather_boots,itm_leather_gloves,itm_beorn_helmet,itm_elven_bow,itm_arrows,itm_beorn_battle_axe,itm_beorn_axe,],
      attr_tier_5,wp_archery (200)|wp (170),knows_common|knows_athletics_4|knows_power_draw_3|knows_power_strike_3|knows_ironflesh_4,rohan_face_middle_1,rohan_face_old_2],
#Beornings
["beorning_vale_man","Beorning_Man","Beorning_Men",tfg_armor| tfg_boots,0,0,fac_beorn,
   [itm_beorn_tunic,itm_leather_boots,itm_gondor_ranger_hood,itm_beorn_staff,itm_beorn_axe,],
      attr_tier_1,wp_tier_1,knows_common|knows_athletics_1|knows_power_strike_1|knows_ironflesh_1,beorn_face1,beorn_face2],
["beorning_warrior","Beorning_Warrior","Beorning_Warriors",tfg_armor| tfg_boots,0,0,fac_beorn,
   [itm_beorn_padded,itm_rohan_shoes,itm_beorn_axe,itm_beorn_axe,itm_beorn_battle_axe,],
      attr_tier_2,wp_tier_2,knows_common|knows_athletics_2|knows_power_strike_1|knows_ironflesh_1,beorn_face1,beorn_face2],
["beorning_tolltacker","Beorning_Tolltacker","Beorning_Tolltackers",tfg_armor| tfg_boots,0,0,fac_beorn,
   [itm_beorn_padded,itm_rohan_shoes,itm_leather_gloves,itm_dwarf_sword_a,itm_beorn_shield,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_power_strike_2|knows_ironflesh_2,beorn_face1,beorn_face2],
["beorning_sentinel","Beorning_Sentinel","Beorning_Sentinels",tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,
   [itm_beorn_heavy,itm_leather_boots,itm_leather_gloves,itm_beorn_helmet,itm_beorn_shield,itm_dwarf_sword_a,itm_dale_sword,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_3|knows_power_strike_3|knows_ironflesh_3|knows_shield_2,beorn_face1,beorn_face2],
["beorning_warden_of_the_ford","Beorning_Warden_of_the_Ford","Beorning_Warden_of_the_Ford",tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,
   [itm_beorn_chief,itm_leather_boots,itm_leather_gloves,itm_dale_helmet_b,itm_beorn_shield,itm_dwarf_sword_a,itm_dwarf_sword_b,itm_dale_sword,itm_dale_sword_long,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_4|knows_power_strike_3|knows_ironflesh_4|knows_shield_3,beorn_face1,beorn_face2],
["beorning_carrock_lookout","Beorning_Carrock_Lookout","Beorning_Carrock_Lookouts",tfg_armor| tfg_boots,0,0,fac_beorn,
   [itm_beorn_tunic,itm_rohan_shoes,itm_gondor_ranger_hood,itm_beorn_axe,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_power_strike_2|knows_ironflesh_2,beorn_face1,beorn_face2],
["beorning_carrock_fighter","Beorning_Carrock_Fighter","Beorning_Carrock_Fighters",tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,
   [itm_beorn_heavy,itm_leather_boots,itm_leather_gloves,itm_beorn_helmet,itm_beorn_axe,itm_beorn_battle_axe,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_3|knows_power_strike_3|knows_ironflesh_3,beorn_face1,beorn_face2],
["beorning_carrock_berserker","Beorning_Carrock_Berserker","Beorning_Carrock_Berserkers",tfg_gloves| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,
   [itm_beorn_berserk,itm_leather_boots,itm_leather_gloves,itm_beorn_helmet,itm_dale_helmet_b,itm_beorn_battle_axe,itm_dale_sword_long,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_6|knows_power_strike_3|knows_ironflesh_6,beorn_face1,beorn_face2],
["northmen_items","BUG","_",tf_hero,0,0,fac_beorn,
   [itm_leather_gloves,itm_good_mace,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
#Dale
["dale_militia","Dale_Militiaman","Dale_Militia",tfg_boots| tfg_armor,0,0,fac_dale,
   [itm_dale_armor_a,itm_leather_boots,itm_dale_pike,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,vaegir_face_younger_1,vaegir_face_middle_2],
["dale_man_at_arms","Dale_Man-at-Arms","Dale_Men-at-Arms",tfg_boots| tfg_armor| tfg_shield,0,0,fac_dale,
   [itm_dale_armor_a,itm_dale_sword,itm_leather_boots,itm_dale_shield_a,itm_dale_helmet_b,itm_dale_pike,],
      attr_tier_2,wp_tier_2,knows_common,vaegir_face_young_1,vaegir_face_middle_2],
["laketown_scout","Laketown_Scout","Laketown_Scouts",tfg_ranged| tfg_boots| tfg_armor,0,0,fac_dale,
   [itm_arrows,itm_dale_sword,itm_short_bow,itm_dale_armor_c,itm_dale_armor_d,itm_leather_boots,],
      attr_tier_2,wp_tier_2,knows_ironflesh_1|knows_power_draw_1|knows_power_throw_1,vaegir_face_young_1,vaegir_face_old_2],
["laketown_bowmen","Laketown_Bowman","Laketown_Bowmen",tfg_ranged| tfg_boots| tfg_armor,0,0,fac_dale,
   [itm_arrows,itm_dale_bow,itm_dale_armor_c,itm_dale_armor_d,itm_dale_sword_broad,itm_leather_boots,itm_dale_helmet_d,],
      attr_tier_3,wp_tier_3,knows_ironflesh_1|knows_power_draw_2|knows_athletics_2|knows_power_throw_1,vaegir_face_young_1,vaegir_face_older_2],
["laketown_archer","Laketown_Archer","Laketown_Archers",tfg_ranged| tfg_boots| tfg_armor,0,0,fac_dale,
   [itm_arrows,itm_dale_bow,itm_dale_armor_c,itm_dale_armor_d,itm_dale_sword_broad,itm_leather_boots,itm_dale_helmet_e,itm_dale_helmet_d,itm_dale_helmet_c,],
      attr_tier_4,wp_tier_4,knows_ironflesh_1|knows_power_draw_2|knows_athletics_2|knows_power_throw_1,vaegir_face_young_1,vaegir_face_older_2],
["barding_bowmen_of_esgaroth","Barding_Bowman_of_Esgaroth","Barding_Bowmen_of_Esgaroth",tfg_ranged| tfg_boots| tfg_armor| tfg_helm,0,0,fac_dale,
   [itm_arrows,itm_dale_bow,itm_dale_armor_h,itm_dale_sword,itm_leather_boots,itm_dale_helmet_e,itm_dale_helmet_c,],
      attr_tier_5,wp_archery (240)|wp (200),knows_ironflesh_2|knows_power_draw_4|knows_power_strike_1|knows_athletics_3|knows_power_throw_1,vaegir_face_young_1,vaegir_face_older_2],
["dale_warrior","Dale_Warrior","Dale_Warriors",tfg_boots| tfg_armor| tfg_shield,0,0,fac_dale,
   [itm_dale_pike,itm_dale_sword,itm_dale_armor_b,itm_dale_shield_a,itm_leather_boots,itm_dale_helmet_b,],
      attr_tier_3,wp_tier_3,knows_athletics_1|knows_power_strike_1|knows_ironflesh_1|knows_shield_2,vaegir_face_young_1,vaegir_face_old_2],
["dale_veteran_warrior","Dale_Veteran_Warrior","Dale_Veteran_Warriors",tfg_shield| tfg_boots| tfg_armor| tfg_helm,0,0,fac_dale,
   [itm_dale_pike,itm_dale_shield_a,itm_dale_sword,itm_dale_armor_f,itm_leather_boots,itm_dale_helmet_a,itm_dale_helmet_b,],
      attr_tier_4,wp_tier_4,knows_athletics_2|knows_ironflesh_2|knows_power_strike_2|knows_shield_2,vaegir_face_young_1,vaegir_face_older_2],
["dale_marchwarden","Marchwarden_of_Dale","Marchwardens_of_Dale",tfg_shield| tfg_boots| tfg_armor| tfg_helm,0,0,fac_dale,
   [itm_dale_shield_c,itm_dale_sword_broad,itm_dale_pike,itm_dale_armor_h,itm_dale_armor_i,itm_dale_armor_j,itm_leather_boots,itm_leather_gloves,itm_dale_helmet_a,],
      attr_tier_5,wp_tier_5,knows_athletics_3|knows_shield_2|knows_ironflesh_3|knows_power_strike_3,vaegir_face_middle_1,vaegir_face_older_2],
["dale_pikeman","Dale_Spearman","Dale_Spearmen",tfg_boots| tfg_armor| tfg_shield,0,0,fac_dale,
   [itm_dale_pike,itm_dale_armor_b,itm_leather_boots,itm_dale_helmet_b,itm_dale_helmet_a,],
      attr_tier_3,wp_tier_3,knows_athletics_1|knows_power_strike_1|knows_ironflesh_1|knows_shield_2,vaegir_face_young_1,vaegir_face_old_2],
["dale_billman","Dale_Billman","Dale_Billmen",tfg_shield| tfg_boots| tfg_armor| tfg_helm,0,0,fac_dale,
   [itm_dale_billhook,itm_dale_shield_c,itm_dale_armor_f,itm_leather_boots,itm_dale_helmet_b,itm_dale_helmet_a,],
      attr_tier_4,wp_tier_4,knows_athletics_2|knows_ironflesh_2|knows_power_strike_2|knows_shield_2,vaegir_face_young_1,vaegir_face_older_2],
["dale_bill_master","Dale_Bill_Master","Dale_Bill_Masters",tfg_shield| tfg_boots| tfg_armor| tfg_helm,0,0,fac_dale,
   [itm_dale_billhook,itm_dale_armor_h,itm_dale_armor_i,itm_dale_armor_j,itm_leather_boots,],
      attr_tier_5,wp_tier_5,knows_athletics_3|knows_shield_2|knows_ironflesh_3|knows_power_strike_3,vaegir_face_middle_1,vaegir_face_older_2],
["merchant_squire_or_dale","Merchant_Squire_of_Dale","Merchant_Squires_of_Dale",tfg_boots| tfg_armor| tfg_shield,0,0,fac_dale,
   [itm_dale_pike,itm_dale_sword_long,itm_dale_armor_b,itm_leather_boots,itm_dale_shield_d,itm_dale_helmet_e,],
      attr_tier_2,wp_tier_2,knows_athletics_1|knows_ironflesh_1|knows_shield_2,vaegir_face_young_1,vaegir_face_old_2],
["merchant_guard_of_dale","Merchant_Guard_of_Dale","Merchant_Guards_of_Dale",tf_mounted| tfg_boots| tfg_armor| tfg_helm| tfg_horse| tfg_shield,0,0,fac_dale,
   [itm_lance,itm_dale_shield_d,itm_dale_sword_long,itm_dale_armor_e,itm_dale_armor_f,itm_leather_boots,itm_dale_horse,itm_dale_helmet_e,itm_dale_helmet_f,],
      attr_tier_3,wp_tier_3,knows_athletics_1|knows_ironflesh_1|knows_shield_2,vaegir_face_young_1,vaegir_face_old_2],
["merchant_protector_of_dale","Merchant_Protector_of_Dale","Merchant_Protectors_of_Dale",tf_mounted| tfg_boots| tfg_armor| tfg_helm| tfg_horse| tfg_shield,0,0,fac_dale,
   [itm_lance,itm_dale_shield_d,itm_dale_armor_e,itm_dale_armor_f,itm_leather_boots,itm_dale_horse,itm_dale_helmet_e,itm_dale_helmet_f,],
      attr_tier_4,wp_tier_4,knows_riding_3|knows_ironflesh_2|knows_power_strike_1,vaegir_face_young_1,vaegir_face_older_2],
["girions_guard_of_dale","Girion's_Guard_of_Dale","Girion's_Gaurds_of_Dale",tf_mounted| tfg_boots| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_shield,0,0,fac_dale,
   [itm_lance,itm_dale_shield_d,itm_dale_sword_long,itm_dale_armor_k,itm_dale_armor_l,itm_leather_boots,itm_dale_warhorse,itm_leather_gloves,itm_dale_helmet_f,],
      attr_tier_5,wp_tier_5,knows_riding_4|knows_shield_2|knows_ironflesh_3|knows_power_strike_2,vaegir_face_middle_1,vaegir_face_older_2],
["dale_items","BUG","BUG",tf_hero,0,0,fac_dale,
   [itm_fur_coat,itm_leather_boots,itm_leather_gloves,itm_short_bow,itm_arrows,itm_sumpter_horse,itm_saddle_horse,itm_good_mace,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
#Rhun
["rhun_tribesman","Rhun_Tribesman","Rhun_Tribesmen",tf_evil_man| tf_mounted| tfg_boots| tfg_armor,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_a,itm_rhun_armor_b,itm_rhun_shortsword,itm_arrows,itm_hunting_bow,],
      attr_tier_1,wp_tier_1,knows_common|knows_riding_3|knows_power_draw_2|knows_horse_archery_2,rhun_man1,rhun_man2],
["rhun_horse_scout","Rhun_Horse_Scout","Rhun_Horse_Scouts",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse| tfg_ranged,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_a,itm_rhun_armor_b,itm_rhun_armor_d,itm_rhun_horse_a,itm_rhun_horse_b,itm_rhun_falchion,itm_arrows,itm_nomad_bow,],
      attr_tier_2,wp_tier_2,knows_common|knows_riding_4|knows_power_draw_3|knows_power_throw_1|knows_horse_archery_3,rhun_man1,rhun_man2],
["rhun_horse_archer","Rhun_Horse_Archer","Rhun_Horse_Archers",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_ranged| tfg_horse,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_a,itm_rhun_armor_b,itm_rhun_armor_d,itm_rhun_helm_k,itm_rhun_helm_l,itm_rhun_horse_a,itm_rhun_horse_b,itm_rhun_sword,itm_arrows,itm_nomad_bow,],
      attr_tier_3,wp_tier_3,knows_riding_5|knows_power_draw_3|knows_ironflesh_1|knows_horse_archery_4|knows_power_throw_1,rhun_man1,rhun_man2],
["rhun_veteran_horse_archer","Rhun_Veteran_Horse_Archer","Rhun_Veteran_Horse_Archers",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_ranged| tfg_horse| tfg_shield|tfg_helm,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_j,itm_rhun_armor_n,itm_rhun_armor_m,itm_rhun_helm_k,itm_rhun_helm_l,itm_rhun_helm_m,itm_rhun_horse_a,itm_rhun_horse_b,itm_rhun_sword,itm_arrows,itm_nomad_bow,],
      attr_tier_4,wp_tier_4,knows_riding_6|knows_power_draw_4|knows_power_strike_1|knows_ironflesh_2|knows_horse_archery_5|knows_power_throw_3,rhun_man1,rhun_man2],
["fell_balchoth_horse_archer","Balchoth_Horse_Archer","Balchoth_Horse_Archers",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse| tfg_ranged| tfg_shield|tfg_helm,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_o,itm_rhun_armor_n,itm_rhun_armor_m,itm_rhun_helm_l,itm_rhun_helm_i,itm_rhun_helm_j,itm_rhun_horse_d,itm_rhun_horse_b,itm_rhun_sword,itm_arrows,itm_nomad_bow,itm_rhun_bull1_shield,itm_rhun_bull2_shield,],
      attr_tier_5,wp_tier_5,knows_riding_6|knows_power_strike_2|knows_power_draw_5|knows_power_throw_4|knows_ironflesh_2|knows_horse_archery_6,rhun_man1,rhun_man2],
["rhun_swift_horseman","Rhun_Swift_Horseman","Rhun_Swift_Horsemen",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_ranged| tfg_horse,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_a,itm_rhun_armor_d,itm_rhun_helm_g,itm_rhun_helm_h,itm_rhun_horse_a,itm_rhun_horse_b,itm_rhun_sword,itm_light_lance,],
      attr_tier_3,wp_tier_3,knows_common|knows_riding_5|knows_power_draw_4|knows_ironflesh_1|knows_power_throw_1,rhun_man1,rhun_man2],
["rhun_veteran_swift_horseman","Rhun_Veteran_Swift_Horseman","Rhun_Veteran_Swift_Horsemen",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse| tfg_shield|tfg_helm,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_j,itm_rhun_armor_n,itm_rhun_armor_m,itm_rhun_helm_a,itm_rhun_helm_b,itm_rhun_helm_j,itm_rhun_horse_d,itm_rhun_horse_b,itm_rhun_sword,itm_rhun_bull1_shield,itm_light_lance,],
      attr_tier_4,wp_tier_4,knows_riding_6|knows_power_strike_2|knows_power_draw_2|knows_power_throw_2|knows_ironflesh_2|knows_horse_archery_1,rhun_man1,rhun_man2],
["falcon_horseman","Falcon_Horseman","Falcon_Horsemen",tf_evil_man| tf_mounted| tfg_boots| tfg_helm|tfg_armor| tfg_horse| tfg_shield,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_g,itm_rhun_armor_h,itm_rhun_helm_a,itm_rhun_helm_b,itm_rhun_helm_j,itm_rhun_horse_e,itm_rhun_horse_f,itm_rhun_sword,itm_rhun_bull1_shield,itm_light_lance,],
      attr_tier_5,wp_tier_5,knows_riding_6|knows_power_strike_3|knows_power_draw_2|knows_power_throw_2|knows_ironflesh_2,rhun_man1,rhun_man2],
["rhun_tribal_warrior","Rhun_Tribal_Warrior","Rhun_Tribal_Warriors",tf_evil_man| tfg_boots| tfg_armor| tfg_shield,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_a,itm_rhun_armor_b,itm_rhun_falchion,itm_rhun_shortsword,itm_rhun_shield,],
      attr_tier_2,wp_tier_2,knows_common,rhun_man1,rhun_man2],
["rhun_tribal_infantry","Rhun_Tribal_Infantryman","Rhun_Tribal_Infantry",tf_evil_man| tfg_boots| tfg_armor| tfg_shield,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_a,itm_rhun_armor_b,itm_rhun_armor_d,itm_rhun_helm_k,itm_rhun_helm_l,itm_rhun_helm_m,itm_rhun_glaive,itm_rhun_greatfalchion,itm_rhun_shield,],
      attr_tier_3,wp_tier_3,knows_athletics_1|knows_ironflesh_1|knows_power_strike_1|knows_shield_2,rhun_man1,rhun_man2],
["rhun_vet_infantry","Rhun_Veteran_Infantryman","Rhun_Veteran_Infantry",tf_evil_man| tfg_shield| tfg_boots| tfg_armor| tfg_helm,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_j,itm_rhun_armor_b,itm_rhun_armor_d,itm_rhun_helm_c,itm_rhun_helm_e,itm_rhun_helm_i,itm_rhun_falchion,itm_rhun_glaive,itm_rhun_greatfalchion,itm_rhun_battleaxe,itm_rhun_shield,],
      attr_tier_4,wp_tier_4,knows_athletics_2|knows_ironflesh_2|knows_power_strike_2|knows_shield_2,rhun_man1,rhun_man2],
["infantry_of_the_ox","Infantryman_of_the_Ox","Infantry_of_the_Ox",tf_evil_man| tfg_shield| tfg_boots| tfg_armor| tfg_helm,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_g,itm_rhun_armor_h,itm_rhun_helm_a,itm_rhun_helm_b,itm_rhun_helm_j,itm_rhun_falchion,itm_rhun_greataxe,itm_rhun_battleaxe,itm_rhun_greatsword,itm_rhun_bull2_shield,],
      attr_tier_5,wp_tier_5,knows_athletics_3|knows_shield_2|knows_ironflesh_3|knows_power_strike_3,rhun_man1,rhun_man2],
["rhun_light_horseman","Rhun_Light_Horseman","Rhun_Light_Horsemen",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_a,itm_rhun_armor_b,itm_rhun_armor_d,itm_rhun_horse_a,itm_rhun_horse_b,itm_rhun_sword,],
      attr_tier_2,wp_tier_2,knows_common|knows_riding_4|knows_power_draw_3|knows_power_throw_1|knows_horse_archery_3,rhun_man1,rhun_man2],
["rhun_light_cavalry","Rhun_Light_Cavalryman","Rhun_Light_Cavalry",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_j,itm_rhun_armor_n,itm_rhun_armor_m,itm_rhun_helm_c,itm_rhun_helm_e,itm_rhun_horse_b,itm_rhun_horse_d,itm_rhun_sword,],
      attr_tier_3,wp_tier_3,knows_common|knows_riding_5|knows_power_draw_4|knows_power_strike_1|knows_ironflesh_1|knows_power_throw_1,rhun_man1,rhun_man2],
["rhun_noble_cavalry","Rhun_Noble_Cavalryman","Rhun_Noble_Cavalry",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse| tfg_shield|tfg_helm,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_n,itm_rhun_armor_h,itm_rhun_armor_g,itm_rhun_helm_g,itm_rhun_helm_h,itm_rhun_horse_b,itm_rhun_horse_e,itm_rhun_horse_f,itm_rhun_sword,itm_rhun_bull1_shield,itm_rhun_bull2_shield,],
      attr_tier_4,wp_tier_4,knows_riding_6|knows_power_strike_2|knows_power_draw_2|knows_power_throw_2|knows_ironflesh_2|knows_horse_archery_1,rhun_man1,rhun_man2],
["rhun_heavy_noble_cavalry","Rhun_Heavy_Noble_Cavalry","Rhun_Heavy_Noble_Cavalry",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse| tfg_shield|tfg_helm,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_p,itm_rhun_armor_k,itm_rhun_helm_b,itm_rhun_helm_g,itm_rhun_horse_g,itm_rhun_horse_h,itm_rhun_sword,itm_rhun_greatsword,itm_rhun_bull3_shield,],
      attr_tier_5,wp_tier_5,knows_riding_6|knows_power_strike_3|knows_power_draw_2|knows_power_throw_2|knows_ironflesh_2|knows_horse_archery_1,rhun_man1,rhun_man2],
["dorwinion_noble_of_rhun","Dorwinion_Noble_of_Rhun","Dorwinion_Nobles_of_Rhun",tf_evil_man| tf_mounted| tfg_boots| tfg_armor| tfg_horse| tfg_shield|tfg_helm,0,0,fac_rhun,
   [itm_furry_boots,itm_rhun_armor_p,itm_rhun_armor_k,itm_rhun_helm_n,itm_rhun_helm_o,itm_rhun_horse_g,itm_rhun_horse_h,itm_rhun_sword,itm_rhun_greatfalchion,itm_rhun_bull3_shield,],
      attr_tier_6,wp_tier_6,knows_riding_7|knows_power_strike_4|knows_power_draw_2|knows_power_throw_2|knows_ironflesh_2|knows_horse_archery_1,rhun_man1,rhun_man2],
["rhun_items","BUG","BUG",tf_hero,0,0,fac_rhun,
   [itm_saddle_horse,itm_fur_coat,itm_leather_boots,itm_leather_gloves,itm_sumpter_horse,itm_short_bow,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
########################## DWARVES #############################
["dwarven_apprentice","Apprentice-dwarf","Apprentice-dwarves",tf_dwarf| tfg_armor| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_pad_boots,itm_leather_dwarf_armor_b,itm_lamedon_hood,itm_dwarf_adz,itm_dwarf_mattock,itm_dwarf_sword_a,itm_dwarf_hand_axe,itm_dwarf_shield_a,itm_dwarf_shield_b,],
      attr_dwarf_tier_1,wp_dwarf_tier_1,knows_common_dwarf|knows_ironflesh_1|knows_power_strike_1,dwarf_face_2,dwarf_face_3],
["dwarven_warrior","Warrior-dwarf","Warrior-dwarves",tf_dwarf| tfg_armor| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_pad_boots,itm_leather_dwarf_armor,itm_dwarf_helm_a,itm_dwarf_throwing_axe,itm_dwarf_adz,itm_dwarf_mattock,itm_dwarf_sword_a,itm_dwarf_hand_axe,itm_dwarf_shield_f,itm_dwarf_shield_j,],
      attr_dwarf_tier_2,wp_dwarf_tier_2,knows_common_dwarf|knows_athletics_1|knows_power_strike_1|knows_power_throw_2|knows_ironflesh_1,dwarf_face_1,dwarf_face_2],
["dwarven_hardened_warrior","Hardened_Warrior-dwarf","Hardened_Warrior-dwarves",tf_dwarf| tfg_armor| tfg_gloves| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_chain_boots,itm_dwarf_armor_a,itm_dwarf_helm_c,itm_dwarf_helm_h,itm_dwarf_throwing_axe,itm_dwarf_adz,itm_dwarf_mattock,itm_dwarf_sword_a,itm_dwarf_shield_g,itm_dwarf_shield_k,],
      attr_dwarf_tier_3,wp_dwarf_tier_3,knows_common_dwarf|knows_athletics_2|knows_power_strike_2|knows_power_throw_2|knows_ironflesh_3,dwarf_face_3,dwarf_face_4],
["dwarven_spearman","Spear-dwarf","Spear-dwarves",tf_dwarf| tfg_armor| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_pad_boots,itm_dwarf_armor_a,itm_dwarf_helm_a,itm_dwarf_throwing_axe,itm_dwarf_spear,itm_dwarf_shield_f,itm_dwarf_shield_j,],
      attr_dwarf_tier_4,wp_dwarf_tier_4,knows_common_dwarf|knows_athletics_3|knows_power_strike_4|knows_ironflesh_3,dwarf_face_1,dwarf_face_2],
["dwarven_pikeman","Pike-dwarf","Pike-dwarves",tf_dwarf| tfg_armor| tfg_gloves| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_pad_boots,itm_mail_mittens,itm_dwarf_armor_a,itm_dwarf_helm_c,itm_dwarf_shield_f,itm_dwarf_helm_h,itm_dwarf_spear_b,],
      attr_dwarf_tier_5,wp_dwarf_tier_5,knows_common_dwarf|knows_athletics_4|knows_power_strike_5|knows_ironflesh_4,dwarf_face_3,dwarf_face_4],
["dwarven_halberdier","Longpike_Dwarf","Longpike_Dwarves",tf_dwarf| tfg_armor| tfg_shield| tfg_gloves| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_chain_boots,itm_mail_mittens,itm_dwarf_armor_c,itm_dwarf_helm_p,itm_dwarf_helm_u,itm_dwarf_shield_f,itm_dwarf_helm_x,itm_dwarf_spear_c,],
      attr_dwarf_tier_6,wp_dwarf_tier_6,knows_common_dwarf|knows_athletics_4|knows_power_strike_6|knows_ironflesh_6,dwarf_face_7,dwarf_face_7],
["dwarven_axeman","Axedwarf","Axedwarves",tf_dwarf| tfg_armor| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_pad_boots,itm_dwarf_armor_a,itm_dwarf_helm_a,itm_dwarf_throwing_axe,itm_dwarf_mattock,itm_dwarf_hand_axe,itm_dwarf_shield_f,itm_dwarf_shield_j,],
      attr_dwarf_tier_4,wp_dwarf_tier_4,knows_common_dwarf|knows_athletics_2|knows_power_throw_2|knows_power_strike_5|knows_ironflesh_3,dwarf_face_1,dwarf_face_2],
["dwarven_expert_axeman","Expert_Axedwarf","Expert_Axedwarves",tf_dwarf| tfg_armor| tfg_gloves| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_chain_boots,itm_mail_mittens,itm_leather_dwarf_armor,itm_dwarf_helm_c,itm_dwarf_helm_h,itm_dwarf_throwing_axe,itm_dwarf_adz,itm_dwarf_mattock,itm_dwarf_hand_axe,itm_dwarf_shield_g,itm_dwarf_shield_k,],
      attr_dwarf_tier_5,wp_dwarf_tier_5,knows_common_dwarf|knows_athletics_3|knows_power_throw_4|knows_power_strike_6|knows_ironflesh_4,dwarf_face_3,dwarf_face_4],
["longbeard_axeman","Longbeard_Axedwarf","Longbeard_Axedwarves",tf_dwarf| tfg_armor| tfg_gloves| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_scale_boots,itm_mail_mittens,itm_dwarf_armor_c,itm_dwarf_helm_p,itm_dwarf_helm_u,itm_dwarf_helm_x,itm_dwarf_throwing_axe,itm_dwarf_great_pick,itm_dwarf_war_pick,itm_dwarf_great_mattock,itm_dwarf_great_axe,],
      attr_dwarf_tier_6,wp_dwarf_tier_6,knows_common_dwarf|knows_athletics_4|knows_power_throw_5|knows_power_strike_7|knows_ironflesh_6,dwarf_face_7,dwarf_face_7],
["dwarven_lookout","Lookout-dwarf","Lookout-dwarves",tf_dwarf| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_pad_boots,itm_dwarf_armor_b,itm_lamedon_hood,itm_dwarf_short_bow,itm_arrows,itm_dwarf_sword_a,],
      attr_dwarf_tier_2,wp_dwarf_tier_2,knows_common_dwarf|knows_athletics_1|knows_power_draw_1|knows_power_strike_1|knows_ironflesh_1,dwarf_face_1,dwarf_face_2],
["dwarven_scout","Scout-dwarf","Scout-dwarves",tf_dwarf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_pad_boots,itm_dwarf_armor_b,itm_dwarf_helm_a,itm_dwarf_short_bow,itm_arrows,itm_dwarf_sword_a,],
      attr_dwarf_tier_3,wp_dwarf_tier_3,knows_common_dwarf|knows_athletics_2|knows_power_draw_2|knows_power_strike_2|knows_ironflesh_1,dwarf_face_4,dwarf_face_5],
["dwarven_bowman","Bow-dwarf","Bow-dwarves",tf_dwarf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_pad_boots,itm_dwarf_vest,itm_dwarf_helm_a,itm_dwarf_horn_bow,itm_arrows,itm_dwarf_sword_a,],
      attr_dwarf_tier_4,wp_dwarf_tier_4,knows_common_dwarf|knows_athletics_2|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_2,dwarf_face_4,dwarf_face_5],
["dwarven_archer","Archer-dwarf","Archer-dwarves",tf_dwarf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_chain_boots,itm_dwarf_vest,itm_dwarf_helm_a,itm_dwarf_horn_bow,itm_arrows,itm_dwarf_sword_a,],
      attr_dwarf_tier_5,wp_dwarf_tier_5,knows_common_dwarf|knows_athletics_3|knows_power_draw_4|knows_power_strike_2|knows_ironflesh_2,dwarf_face_4,dwarf_face_5],
["marksman_of_ravenhill","Marks-dwarf_of_Ravenhill","Marks-dwarves_of_Ravenhill",tf_dwarf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_chain_boots,itm_leather_dwarf_armor,itm_dwarf_helm_a,itm_dwarf_horn_bow,itm_arrows,itm_dwarf_sword_a,],
      attr_dwarf_tier_6,wp_dwarf_tier_6,knows_common_dwarf|knows_athletics_4|knows_power_draw_5|knows_power_strike_3|knows_ironflesh_3,dwarf_face_4,dwarf_face_5],

["iron_hills_miner","Iron_Hills_Miner","Iron_Hills_Miners",tf_dwarf| tfg_armor| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_chain_boots,itm_dwarf_vest_b,itm_dwarf_mattock,itm_dwarf_sword_a,itm_dwarf_shield_c,itm_dwarf_shield_d,],
      attr_dwarf_tier_2,wp_dwarf_tier_2,knows_common_dwarf|knows_athletics_1|knows_power_strike_2|knows_ironflesh_1,dwarf_face_1,dwarf_face_2],
["iron_hills_infantry","Iron_Hills_Infantry","Iron_Hills_Infantry",tf_dwarf| tfg_armor| tfg_gloves| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_chain_boots,itm_dwarf_armor_a,itm_dwarf_helm_c,itm_dwarf_helm_h,itm_dwarf_adz,itm_dwarf_mattock,itm_dwarf_sword_a,itm_dwarf_shield_g,itm_dwarf_shield_k,],
      attr_dwarf_tier_4,wp_dwarf_tier_4,knows_common_dwarf|knows_athletics_2|knows_power_strike_3|knows_ironflesh_2,dwarf_face_3,dwarf_face_4],
["iron_hills_battle_infantry","Iron_Hills_Battle-dwarf","Iron_Hills_Battle-dwarves",tf_dwarf| tfg_armor| tfg_gloves| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_chain_boots,itm_mail_mittens,itm_dwarf_armor_a,itm_dwarf_helm_p,itm_dwarf_helm_u,itm_dwarf_helm_x,itm_dwarf_great_pick,itm_dwarf_war_pick,itm_dwarf_great_mattock,],
      attr_dwarf_tier_5,wp_dwarf_tier_5,knows_common_dwarf|knows_athletics_3|knows_power_strike_4|knows_ironflesh_3,dwarf_face_1,dwarf_face_2],
["grors_guard","Gror's_Guard","Gror's_Guards",tf_dwarf| tfg_armor| tfg_gloves| tfg_shield| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_scale_boots,itm_mail_mittens,itm_dwarf_armor_c,itm_dwarf_helm_p,itm_dwarf_helm_u,itm_dwarf_helm_x,itm_dwarf_great_pick,itm_dwarf_war_pick,itm_dwarf_great_mattock,],
      attr_dwarf_tier_6,wp_dwarf_tier_6,knows_common_dwarf|knows_athletics_4|knows_power_strike_6|knows_ironflesh_5,dwarf_face_7,dwarf_face_7],
["dwarf_items","BUG","_",tf_hero,0,0,fac_dwarf,
   [itm_pony, itm_good_mace,itm_dwarf_helm_b,itm_dwarf_shield_a,itm_dwarf_shield_b,itm_dwarf_shield_f,itm_dwarf_shield_g,itm_dwarf_shield_i,itm_dwarf_shield_j,itm_dwarf_shield_k,itm_dwarf_shield_l,itm_dwarf_sword_b,itm_dwarf_sword_c,itm_dwarf_sword_d,itm_dwarf_great_mattock,itm_dwarf_hand_axe,itm_dwarf_throwing_axe,itm_dwarf_spear,itm_dwarf_helm_i,itm_dwarf_helm_j,itm_dwarf_helm_l,itm_dwarf_helm_m,itm_dwarf_helm_o,itm_dwarf_helm_q,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
#GONDOR
["gondor_commoner","Gondor_Levy","Gondor_Levies",tf_gondor| tfg_armor| tfg_boots,0,0,fac_gondor,
   [itm_gon_jerkin,itm_gondor_light_greaves,itm_gondor_arrows,itm_hunting_bow,itm_shortened_spear,itm_tld_tunic,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      attr_tier_1,wp_tier_1,knows_common,gondor_face1,gondor_face2],
["gondor_militiamen","Gondor_Watchman","Gondor_Watchmen",tf_gondor| tfg_armor| tfg_shield| tfg_boots| tfg_helm,0,0,fac_gondor,
   [itm_gon_jerkin,itm_gondor_light_greaves,itm_shortened_spear,itm_gondor_auxila_helm,itm_short_bow,itm_gondor_arrows,itm_gon_tab_shield_a,itm_gondor_short_sword,itm_good_mace,],
      attr_tier_2,wp_tier_2,knows_common|knows_athletics_1|knows_power_strike_1,gondor_face1,gondor_face2],
["footmen_of_gondor","Footman_of_Gondor","Footmen_of_Gondor",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,
   [itm_gon_footman,itm_gondor_spear,itm_gondor_shield_c,itm_gondorian_light_helm,itm_gondor_med_greaves,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_shield_2|knows_power_strike_2|knows_ironflesh_1,gondor_face1,gondor_face2],
#Gondor spearmen
["gondor_spearmen","Spearman_of_Gondor","Spearmen_of_Gondor",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,
   [itm_gon_regular,itm_gondor_infantry_helm,itm_gon_regular,itm_gondor_shield_c,itm_gondor_med_greaves,itm_gondor_spear,itm_leather_gloves,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,gondor_face1,gondor_face3],
["gondor_veteran_spearmen","Veteran_Spearman_of_Gondor","Veteran_Spearmen_of_Gondor",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,
   [itm_gon_regular,itm_gondor_infantry_helm,itm_gon_regular,itm_gondor_shield_c,itm_gondor_heavy_greaves,itm_gondor_spear,itm_mail_mittens,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_shield_4|knows_power_strike_4|knows_ironflesh_2,gondor_face1,gondor_face2],
["guard_of_the_fountain_court","Guard_of_the_Fountain_Court","Guards_of_the_Fountain_Court",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,
   [itm_gon_tower_guard,itm_gondor_heavy_greaves,itm_gondor_tower_spear,itm_mail_mittens,itm_gondor_shield_a,itm_tower_guard_helm,],
      attr_tier_6,wp_tier_6,knows_common|knows_athletics_4|knows_shield_6|knows_power_strike_6|knows_ironflesh_4,gondor_face1,gondor_face3],
#Gondor swordsmen
["gondor_swordsmen","Swordsman_of_Gondor","Swordsmen_of_Gondor",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,
   [itm_gon_regular,itm_gondor_infantry_helm,itm_gon_regular,itm_gondor_shield_c,itm_gondor_med_greaves,itm_gondor_sword,itm_leather_gloves,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,gondor_face1,gondor_face3],
["gondor_veteran_swordsmen","Veteran_Swordsman_of_Gondor","Veteran_Swordsmen_of_Gondor",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,
   [itm_gon_regular,itm_gondor_infantry_helm,itm_gon_regular,itm_gondor_shield_c,itm_gondor_heavy_greaves,itm_gondor_sword,itm_mail_mittens,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_shield_4|knows_power_strike_4|knows_ironflesh_2,gondor_face1,gondor_face2],
["swordsmen_of_the_tower_guard","Swordsman_of_the_Tower_Guard","Swordsmen_of_the_Tower_Guard",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,
   [itm_gon_tower_guard,itm_gondor_heavy_greaves,itm_gondor_citadel_sword,itm_mail_mittens,itm_gondor_shield_a,itm_tower_guard_helm,],
      attr_tier_6,wp_tier_6,knows_common|knows_athletics_4|knows_shield_5|knows_power_strike_5|knows_ironflesh_4,gondor_face1,gondor_face3],
#Gondor Noble Line
["gondor_noblemen","Gondor_Nobleman","Gondor_Noblemen",tf_gondor| tfg_armor| tfg_boots,0,0,fac_gondor,
   [itm_gon_noble_cloak,itm_gondor_light_greaves,itm_gondor_cav_sword,],
      attr_tier_1,wp_tier_1,knows_common,gondor_face1,gondor_face2],
["squire_of_gondor","Squire_of_Gondor","Squires_of_Gondor",tf_gondor| tf_mounted| tfg_helm| tfg_armor| tfg_boots| tfg_horse,0,0,fac_gondor,
   [itm_gon_squire,itm_gondor_cav_sword,itm_gondor_med_greaves,itm_gondor_courser,itm_gondor_squire_helm,],
      attr_tier_2,wp_tier_2,knows_common|knows_power_strike_1|knows_riding_2,gondor_face1,gondor_face2],
["veteran_squire_of_gondor","Veteran_Squire_of_Gondor","Veteran_Squires_of_Gondor",tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gon_squire,itm_gondor_cav_sword,itm_gondor_med_greaves,itm_gondor_courser,itm_gondor_shield_d,itm_leather_gloves,itm_gondor_squire_helm,],
      attr_tier_3,wp_tier_3,knows_common|knows_riding_2|knows_shield_2|knows_power_strike_2,gondor_face1,gondor_face2],
["knight_of_gondor","Knight_of_Gondor","Knights_of_Gondor",tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gon_knight,itm_gondor_cav_sword,itm_gondor_lance,itm_gondor_heavy_greaves,itm_gondor_hunter,itm_gondor_shield_d,itm_mail_mittens,itm_gondor_knight_helm,],
      attr_tier_4,wp_tier_4,knows_common|knows_riding_3|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,gondor_face1,gondor_face2],
["veteran_knight_of_gondor","Veteran_Knight_of_Gondor","Veteran_Knights_of_Gondor",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gon_knight,itm_gondor_cav_sword,itm_gondor_heavy_greaves,itm_gondor_hunter,itm_gondor_shield_d,itm_gondor_lance,itm_mail_mittens,itm_gondor_knight_helm,],
      attr_tier_5,wp_tier_5,knows_common|knows_riding_4|knows_shield_3|knows_power_strike_4|knows_ironflesh_4,gondor_face1,gondor_face3],
["knight_of_the_citadel","Knight_of_the_Citadel","Knights_of_the_Citadel",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gondor_lance_banner,itm_gon_tower_knight,itm_gondor_heavy_greaves,itm_gondor_warhorse,itm_gondor_shield_b,itm_gondor_citadel_sword,itm_mail_mittens,itm_gondor_citadel_knight_helm,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_6|knows_shield_4|knows_power_strike_6|knows_ironflesh_6,gondor_face1,gondor_face3],
#Gondor Archers
["bowmen_of_gondor","Bowman_of_Gondor","Bowmen_of_Gondor",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,
   [itm_gon_bowman,itm_gondor_arrows,itm_regular_bow,itm_gondor_med_greaves,itm_gondorian_light_helm_b,itm_gondor_short_sword,],
      attr_tier_3,wp_tier_3,knows_common|knows_power_draw_2|knows_ironflesh_1,gondor_face1,gondor_face2],
["archer_of_gondor","Archer_of_Gondor","Archers_of_Gondor",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,
   [itm_gon_archer,itm_gondor_arrows,itm_gondor_sword,itm_gondor_bow,itm_gondor_med_greaves,itm_gondorian_archer_helm,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_power_draw_4|knows_ironflesh_1,gondor_face1,gondor_face2],
["veteran_archer_of_gondor","Veteran_Archer_of_Gondor","Veteran_Archers_of_Gondor",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,
   [itm_gon_archer,itm_gondor_bow,itm_gondor_sword,itm_gondor_arrows,itm_gondor_med_greaves,itm_gondorian_archer_helm,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_4|knows_power_draw_4|knows_power_strike_5|knows_ironflesh_3,gondor_face1,gondor_face2],
["archer_of_the_tower_guard","Archer_of_the_Tower_Guard","Archers_of_the_Tower_Guard",tf_gondor| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,
   [itm_gon_steward_guard,itm_gondor_bow,itm_gondor_citadel_sword,itm_gondor_arrows,itm_gondor_heavy_greaves,itm_tower_archer_helm,],
      attr_tier_6,wp_tier_6,knows_common|knows_athletics_5|knows_power_draw_6|knows_power_strike_4|knows_ironflesh_4,gondor_face1,gondor_face3],
# Special Denetor guars (only for scene)
["steward_guard","Steward's_Guard","Steward's_Guards",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_gondor,
   [itm_gon_steward_guard,itm_gondor_heavy_greaves,itm_gondor_tower_spear,itm_mail_mittens,itm_gon_tab_shield_b,itm_tower_guard_helm,],
      attr_tier_6,wp_tier_6,knows_common|knows_athletics_4|knows_shield_6|knows_power_strike_6|knows_ironflesh_4,gondor_face1,gondor_face3],
#RANGERS
["ranger_of_ithilien","Ranger_of_Ithilien","Rangers_of_Ithilien",tf_gondor| tfg_ranged| tfg_armor| tfg_boots,0,subfac_rangers,fac_gondor,
   [itm_gondor_ranger_sword,itm_ithilien_arrows,itm_gondor_bow,itm_gon_ranger_cloak,itm_gondor_ranger_hood,itm_gondor_light_greaves,],
      attr_tier_4,wp_archery (200)|wp (170),knows_common|knows_pathfinding_1|knows_riding_1|knows_athletics_6|knows_power_draw_3|knows_power_strike_3|knows_ironflesh_2,gondor_face1,gondor_face2],
["veteran_ranger_of_ithilien","Veteran_Ranger_of_Ithilien","Veteran_Rangers_of_Ithilien",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,subfac_rangers,fac_gondor,
   [itm_gondor_ranger_sword,itm_ithilien_arrows,itm_gondor_bow,itm_gon_ranger_cloak,itm_gondor_ranger_hood,itm_gondor_light_greaves,],
      attr_tier_5,wp (250),knows_common|knows_pathfinding_2|knows_riding_1|knows_athletics_7|knows_power_draw_3|knows_power_strike_4|knows_ironflesh_4,gondor_face1,gondor_face2],
["master_ranger_of_ithilien","Master_Ranger_of_Ithilien","Master_Rangers_of_Ithilien",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,subfac_rangers,fac_gondor,
   [itm_gondor_ranger_sword,itm_ithilien_arrows,itm_gondor_bow,itm_gon_ranger_skirt,itm_gondor_ranger_hood_mask,itm_gondor_light_greaves,],
      attr_tier_6,wp_melee (320)|wp_throwing (300)|wp_archery (380),knows_common|knows_pathfinding_3|knows_riding_1|knows_athletics_8|knows_power_draw_5|knows_power_strike_5|knows_ironflesh_4,gondor_face1,gondor_face3],
["ithilien_leader","Captain_of_Ithilien_Rangers","Captains_of_Ithilien_Rangers",tf_gondor| tfg_ranged| tfg_shield| tfg_armor| tfg_boots,0,subfac_rangers,fac_gondor,
   [itm_gondor_ranger_sword,itm_ithilien_arrows,itm_gondor_bow,itm_gon_ranger_skirt,itm_gondor_light_greaves,],
      attr_tier_7,wp_tier_7,knows_common|knows_pathfinding_4|knows_athletics_9|knows_shield_9|knows_power_draw_9|knows_power_strike_8|knows_ironflesh_10,gondor_face1,gondor_face2],
#Lossarnach#######
["woodsman_of_lossarnach","Woodsman_of_Lossarnach","Woodsmen_of_Lossarnach",tf_gondor| tfg_armor| tfg_boots,0,subfac_lossarnach,fac_gondor,
   [itm_lossarnach_shirt,itm_gondor_light_greaves,itm_loss_axe,itm_lossarnach_cloth_cap,itm_gon_tab_shield_a,itm_loss_throwing_axes,],
      str_7| agi_5| int_4| cha_4|level(4),wp_tier_1,knows_common|knows_power_throw_2,gondor_face1,gondor_face2],
["axeman_of_lossarnach","Axeman_of_Lossarnach","Axemen_of_Lossarnach",tf_gondor| tfg_armor| tfg_shield| tfg_boots| tfg_helm,0,subfac_lossarnach,fac_gondor,
   [itm_lossarnach_axeman,itm_gondor_light_greaves,itm_loss_axe,itm_lossarnach_leather_cap,itm_gon_tab_shield_a,itm_loss_throwing_axes,],
      str_10| agi_7| int_4| cha_4|level(8),wp_tier_2,knows_common|knows_power_throw_3|knows_athletics_1|knows_power_strike_1,gondor_face1,gondor_face2],
["vet_axeman_of_lossarnach","Lossarnach_Veteran_Axeman","Lossarnach_Veteran_Axemen",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_lossarnach,fac_gondor,
   [itm_lossarnach_vet_axeman,itm_loss_axe,itm_gon_tab_shield_a,itm_gondor_light_greaves,itm_lossarnach_leather_cap,itm_loss_throwing_axes,],
      str_13|agi_11| int_4| cha_4|level(12),wp_tier_3,knows_common|knows_power_throw_4|knows_athletics_3|knows_power_strike_3|knows_ironflesh_3,gondor_face1,gondor_face2],
["heavy_lossarnach_axeman","Heavy_Lossarnach_Axeman","Heavy_Lossarnach_Axemen",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tfg_gloves,0,subfac_lossarnach,fac_gondor,
   [itm_lossarnach_warrior,itm_lossarnach_scale_cap,itm_loss_axe,itm_gon_tab_shield_a,itm_loss_throwing_axes,itm_lossarnach_greaves,itm_leather_gloves,],
      str_15|agi_15| int_4| cha_4|level(16),wp_tier_4,knows_common|knows_athletics_4|knows_power_strike_5|knows_ironflesh_4|knows_power_throw_5,gondor_face1,gondor_face2],
["axemaster_of_lossarnach","Axemaster_of_Lossarnach","Axemasters_of_Lossarnach",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_lossarnach,fac_gondor,
   [itm_lossarnach_scale_cap,itm_lossarnach_vet_warrior,itm_loss_war_axe,itm_lossarnach_greaves,itm_gon_tab_shield_a,itm_loss_throwing_axes,itm_mail_mittens,],
      str_18|agi_18| int_4| cha_4|level(25),wp_two_handed (320)|wp (200),knows_common|knows_athletics_5|knows_power_strike_7|knows_ironflesh_5|knows_power_throw_6,gondor_face1,gondor_face2],
["lossarnach_leader","Captain_of_Lossarnach","Captains_of_Lossarnach",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,subfac_lossarnach,fac_gondor,
   [itm_lossarnach_leader,itm_gondor_cav_sword,itm_loss_axe,itm_lossarnach_greaves,itm_gondor_hunter,itm_gon_tab_shield_a,itm_mail_mittens,itm_gondor_leader_helm,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_8|knows_shield_9|knows_power_strike_8|knows_ironflesh_10,gondor_face1,gondor_face3],
####PELARGIR
["pelargir_watchman","Pelargir_Watchman","Pelargir_Watchmen",tf_gondor| tfg_armor| tfg_helm| tfg_boots,0,subfac_pelargir,fac_gondor,
   [itm_pel_jerkin,itm_gondor_auxila_arrows,itm_short_bow,itm_gondor_light_greaves,itm_shortened_spear,itm_gondor_javelin,],
      str_7| agi_5| int_4| cha_4|level(4),wp_tier_2,knows_common|knows_power_draw_2|knows_power_throw_2|knows_ironflesh_1,gondor_face1,gondor_face2],
["pelargir_marine","Pelargir_Marine","Pelargir_Marines",tf_gondor| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pelargir,fac_gondor,
   [itm_pel_marine,itm_gondor_javelin,itm_gondor_light_greaves,itm_pelargir_eket,itm_gon_tab_shield_a,itm_pelargir_hood,],
      str_15|agi_15| int_4| cha_4|level(16),wp_tier_4,knows_common|knows_athletics_2|knows_power_throw_5|knows_power_draw_5|knows_ironflesh_1,gondor_face1,gondor_face2,],
["pelargir_vet_marine","Pelargir_Veteran_Marine","Pelargir_Veteran_Marine",tf_gondor| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pelargir,fac_gondor,
   [itm_pel_marine,itm_gondor_auxila_arrows,itm_short_bow,itm_regular_bow,itm_gondor_light_greaves,itm_pelargir_hood,itm_pelargir_eket,itm_gon_tab_shield_a,],
      str_18|agi_18| int_4| cha_4|level(25),wp_tier_5,knows_common|knows_athletics_4|knows_power_draw_5|knows_power_strike_2|knows_ironflesh_3,gondor_face1,gondor_face2,],
["pelargir_infantry","Pelargir_Infantryman","Pelargir_Infantrymen",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pelargir,fac_gondor,
   [itm_pel_footman,itm_leather_gloves,itm_pelargir_helmet_light,itm_pelargir_sword,itm_gon_tab_shield_b,itm_pelargir_greaves,],
      str_15|agi_15| int_4| cha_4|level(16),wp_tier_4,knows_common|knows_athletics_4|knows_power_throw_2|knows_power_strike_4|knows_ironflesh_4,gondor_face1,gondor_face2,],
["pelargir_vet_infantry","Pelargir_Veteran_Infantryman","Pelargir_Veteran_Infantrymen",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pelargir,fac_gondor,
   [itm_pelargir_regular,itm_pelargir_helmet_heavy,itm_mail_mittens,itm_gon_tab_shield_b,itm_pelargir_greaves,itm_pelargir_sword,],
      str_18|agi_18| int_4| cha_4|level(25),wp_tier_5,knows_common|knows_athletics_5|knows_power_throw_3|knows_power_strike_5|knows_ironflesh_5,gondor_face1,gondor_face2,],
["pelargir_leader","Captain_of_Pelargir","Captains_of_Pelargir",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pelargir,fac_gondor,
   [itm_pel_leader,itm_pelargir_helmet_light,itm_mail_mittens,itm_gon_tab_shield_c,itm_pelargir_greaves,itm_pelargir_sword,],
      attr_tier_6,wp_tier_6,knows_common|knows_athletics_7|knows_shield_9|knows_power_strike_8|knows_ironflesh_10,gondor_face1,gondor_face2,],
["pelargir_marine_leader","Captain_of_Pelargir_Marines","Captains_of_Pelargir_Marine",tf_gondor| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pelargir,fac_gondor,
   [itm_pelargir_marine_leader,itm_pelargir_helmet_light,itm_gon_tab_shield_c,itm_pelargir_greaves,itm_pelargir_sword,],
      attr_tier_6,wp_tier_6,knows_common|knows_athletics_7|knows_shield_9|knows_power_strike_8|knows_ironflesh_10,gondor_face1,gondor_face2,],
#Lamedon#######
["clansman_of_lamedon","Clansman_of_Lamedon","Clansmen_of_Lamedon",tf_gondor| tfg_armor| tfg_boots,0,subfac_ethring,fac_gondor,
   [itm_gondor_auxila_arrows,itm_lamedon_clansman,itm_gondor_javelin,itm_loss_axe,itm_gondor_light_greaves,itm_spear,itm_gondor_javelin,itm_short_bow,],
      str_7| agi_5| int_4| cha_4|level(4),wp_tier_1,knows_common|knows_power_throw_1,gondor_face1,gondor_face2,],
["footman_of_lamedon","Footman_of_Lamedon","Footmen_of_Lamedon",tf_gondor| tfg_shield| tfg_armor| tfg_boots| tfg_helm,0,subfac_ethring,fac_gondor,
   [itm_lamedon_footman,itm_gondor_light_greaves,itm_gondor_spear,itm_lamedon_hood,itm_gondor_javelin,itm_loss_axe,itm_loss_axe,itm_gon_tab_shield_a,],
      str_10| agi_7| int_4| cha_4|level(8),wp_tier_2,knows_common|knows_athletics_1|knows_power_strike_1|knows_power_throw_2,gondor_face1,gondor_face2,],
["veteran_of_lamedon","Veteran_of_Lamedon","Veterans_of_Lamedon",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_ethring,fac_gondor,
   [itm_lamedon_veteran,itm_gondor_auxila_helm,itm_gon_tab_shield_a,itm_loss_axe,itm_gondor_spear,itm_gondor_sword,itm_gondor_light_greaves,],
      str_13|agi_11| int_4| cha_4|level(12),wp_tier_3,knows_common|knows_athletics_4|knows_power_strike_4|knows_ironflesh_5,gondor_face1,gondor_face2,],
["warrior_of_lamedon","Warrior_of_Lamedon","Warriors_of_Lamedon",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_ethring,fac_gondor,
   [itm_lamedon_warrior,itm_gondor_auxila_helm,itm_loss_axe,itm_gon_tab_shield_d,itm_gondor_sword,itm_gondor_med_greaves,],
      str_15|agi_15| int_4| cha_4|level(16),wp_tier_4,knows_common|knows_athletics_4|knows_power_strike_5|knows_ironflesh_5,gondor_face1,gondor_face2,],
["champion_of_lamedon","Champion_of_Lamedon","Champions_of_Lamedon",tf_gondor| tfg_gloves| tfg_armor| tfg_helm| tfg_boots,0,subfac_ethring,fac_gondor,
   [itm_lamedon_vet_warrior,itm_gondor_lamedon_helm,itm_gondor_bastard,itm_gondor_bastard,itm_gondor_heavy_greaves,itm_mail_mittens,itm_loss_war_axe,],
      str_18|agi_18| int_4| cha_4|level(25),wp_tier_5,knows_common|knows_athletics_5|knows_power_strike_5|knows_ironflesh_6,gondor_face1,gondor_face2,],
["knight_of_lamedon","Knight_of_Lamedon","Knights_of_Lamedon",tf_gondor| tf_mounted | tfg_gloves| tfg_shield| tfg_horse| tfg_armor| tfg_helm| tfg_boots,0,subfac_ethring,fac_gondor,
   [itm_lamedon_knight,itm_gon_tab_shield_c,itm_gondor_lamedon_helm,itm_gondor_cav_sword,itm_gondor_heavy_greaves,itm_mail_mittens,itm_gondor_lam_horse,],
      str_18|agi_18| int_4| cha_4|level(25),wp_tier_5,knows_common|knows_riding_6|knows_power_strike_6|knows_ironflesh_7,gondor_face1,gondor_face2,],
["lamedon_leader","Captain_of_Lamedon","Captains_of_Lamedon",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,subfac_ethring,fac_gondor,
   [itm_lamedon_leader_surcoat_cloak,itm_gondor_cav_sword,itm_gondor_heavy_greaves,itm_gondor_lam_horse,itm_gon_tab_shield_c,itm_mail_mittens,itm_gondor_lamedon_leader_helm,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_8|knows_shield_9|knows_power_strike_8|knows_ironflesh_10,gondor_face1,gondor_face3,],
#Pinnath Gelin####
["pinnath_gelin_plainsman","Plainsman_of_Pinnath_Gelin","Plainsmen_of_Pinnath_Gelin",tf_gondor| tfg_armor| tfg_boots,0,subfac_pinnath_gelin,fac_gondor,
   [itm_pinnath_footman,itm_gondor_ranger_hood,itm_shortened_spear,itm_gondor_light_greaves,itm_gondor_auxila_arrows,itm_short_bow,],
      str_10| agi_7| int_4| cha_4|level(8),wp_tier_2,knows_common|knows_athletics_3|knows_power_throw_1|knows_power_strike_3|knows_ironflesh_3,gondor_face1,gondor_face2,],
["pinnath_gelin_spearman","Spearman_of_Pinnath_Gelin","Spearmen_of_Pinnath_Gelin",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pinnath_gelin,fac_gondor,
   [itm_pinnath_footman,itm_gondor_auxila_helm,itm_spear,itm_gon_tab_shield_a,itm_gondor_light_greaves,itm_leather_gloves,],
      str_15|agi_15| int_4| cha_4|level(16),wp_tier_5,knows_common|knows_athletics_4|knows_power_throw_2|knows_power_strike_4|knows_ironflesh_4,gondor_face1,gondor_face2,],
["warrior_of_pinnath_gelin","Warrior_of_Pinnath_Gelin","Warriors_of_Pinnath_Gelin",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pinnath_gelin,fac_gondor,
   [itm_pinnath_warrior,itm_gondor_auxila_helm,itm_gon_tab_shield_d,itm_gondor_spear,itm_gondor_sword,itm_gondor_med_greaves,itm_leather_gloves,],
      str_18|agi_18| int_4| cha_4|level(25),wp_one_handed (200)|wp_two_handed (200)|wp_polearm (320),knows_common|knows_athletics_5|knows_power_throw_3|knows_power_strike_6|knows_ironflesh_5,gondor_face1,gondor_face2,],
["pinnath_gelin_bowman","Bowman_of_Pinnath_Gelin","Bowmen_of_Pinnath_Gelin",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,subfac_pinnath_gelin,fac_gondor,
   [itm_pinnath_vet_footman,itm_gondor_auxila_arrows,itm_regular_bow,itm_gondor_light_greaves,itm_gondor_sword,itm_gondor_ranger_hood,itm_gondor_short_sword,],
      str_15|agi_15| int_4| cha_4|level(16),wp_tier_4,knows_common|knows_athletics_2|knows_power_draw_4|knows_ironflesh_1,gondor_face1,gondor_face2,],
["pinnath_gelin_archer","Archer_of_Pinnath_Gelin","Archers_of_Pinnath_Gelin",tf_gondor| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_pinnath_gelin,fac_gondor,
   [itm_pinnath_archer,itm_gondor_auxila_arrows,itm_regular_bow,itm_gondor_med_greaves,itm_gondor_ranger_hood,itm_gondor_sword,],
      str_18|agi_18| int_4| cha_4|level(25),wp_tier_5,knows_common|knows_athletics_4|knows_power_draw_5|knows_power_strike_2|knows_ironflesh_3,gondor_face1,gondor_face2,],
["pinnath_leader","Captain_of_Pinnath_Gelin","Captains_of_Pinnath_Gelin",tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,subfac_pinnath_gelin,fac_gondor,
   [itm_pinnath_leader,itm_gondor_cav_sword,itm_gondor_med_greaves,itm_gondor_hunter,itm_gon_tab_shield_c,itm_mail_mittens,itm_gondor_leader_helm,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_8|knows_shield_9|knows_power_strike_8|knows_ironflesh_10,gondor_face1,gondor_face3,],
#####Black Root Vale#####
["blackroot_vale_archer","Hunter_of_Blackroot_Vale","Hunter_of_Blackroot_Vale",tf_gondor|  tfg_armor|  tfg_boots,0,subfac_blackroot,fac_gondor,
   [itm_blackroot_footman,itm_spear,itm_short_bow,itm_gondor_auxila_arrows,itm_gondor_light_greaves,],
      str_10| agi_7| int_4| cha_4|level(8),wp_tier_2,knows_common|knows_power_draw_3|knows_ironflesh_1,gondor_face1,gondor_face2,],
["veteran_blackroot_vale_archer","Bowman_of_Blackroot_Vale","Bowmen_of_Blackroot_Vale",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,subfac_blackroot,fac_gondor,
   [itm_blackroot_bowman,itm_gondor_auxila_arrows,itm_regular_bow,itm_gondor_sword,itm_gondor_light_greaves,itm_blackroot_hood,],
      str_15|agi_15| int_4| cha_4|level(16),wp_tier_4,knows_common|knows_athletics_2|knows_power_draw_4|knows_ironflesh_1,gondor_face1,gondor_face2,],
["master_blackroot_vale_archer","Archer_of_Blackroot_Vale","Archers_of_Blackroot_Vale",tf_gondor| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,subfac_blackroot,fac_gondor,
   [itm_gondor_auxila_arrows,itm_gondor_bow,itm_blackroot_archer,itm_gondor_short_sword,itm_gondor_med_greaves,itm_blackroot_hood,],
      str_18|agi_18| int_4| cha_4|level(25),wp_tier_5,knows_common|knows_athletics_4|knows_power_draw_5|knows_power_strike_2|knows_ironflesh_3,gondor_face1,gondor_face2,],
["footman_of_blackroot_vale","Footman_of_Blackroot_Vale","Footmen_of_Blackroot_Vale",tf_gondor| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_blackroot,fac_gondor,
   [itm_blackroot_footman,itm_gondor_auxila_helm,itm_gondor_spear,itm_gon_tab_shield_a,itm_gondor_light_greaves,],
      str_15|agi_15| int_4| cha_4|level(16),wp_tier_4,knows_common|knows_athletics_4|knows_power_throw_2|knows_power_strike_4|knows_ironflesh_4,gondor_face1,gondor_face2,],
["spearman_of_blackroot_vale","Spearman_of_Blackroot_Vale","Spearmen_of_Blackroot_Vale",tf_gondor| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,subfac_blackroot,fac_gondor,
   [itm_blackroot_warrior,itm_gondor_auxila_helm,itm_gon_tab_shield_d,itm_gondor_spear,itm_gondor_med_greaves,itm_leather_gloves,],
      str_18|agi_18| int_4| cha_4|level(25),wp_tier_5,knows_common|knows_athletics_5|knows_power_throw_3|knows_power_strike_5|knows_ironflesh_5,gondor_face1,gondor_face2,],
["blackroot_leader","Captain_of_Blackroot_Vale","Captains_of_Blackroot_Vale",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,subfac_blackroot,fac_gondor,
   [itm_blackroot_leader,itm_gondor_cav_sword,itm_gondor_med_greaves,itm_gondor_hunter,itm_gon_tab_shield_c,itm_mail_mittens,itm_gondor_leader_helm,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_8|knows_shield_9|knows_power_strike_8|knows_ironflesh_10,gondor_face1,gondor_face3,],
###Dol Amroth#####
["dol_amroth_youth","Dol_Amroth_Recruit","Dol_Amroth_Recruits",tf_gondor| tfg_armor| tfg_shield| tfg_boots,0,subfac_dol_amroth,fac_gondor,
   [itm_dol_shirt,itm_dol_shoes,itm_gondor_spear,itm_gon_tab_shield_a,],
      attr_tier_1,wp_tier_1,knows_common,gondor_face1,gondor_face2,],
["squire_of_dol_amroth","Squire_of_Dol_Amroth","Squires_of_Dol_Amroth",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,subfac_dol_amroth,fac_gondor,
   [itm_dol_padded_coat,itm_gondor_lance,itm_amroth_sword_a,itm_gondor_lance,itm_gondor_lance,itm_gon_tab_shield_c,itm_dol_shoes,itm_leather_gloves,itm_gondor_hunter,itm_gondor_dolamroth_helm,],
      attr_tier_2,wp_tier_2,knows_common|knows_riding_2|knows_shield_2|knows_power_strike_2|knows_ironflesh_2,gondor_face1,gondor_face3,],
["veteran_squire_of_dol_amroth","Veteran_Squire_of_Dol_Amroth","Veteran_Squires_of_Dol_Amroth",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,subfac_dol_amroth,fac_gondor,
   [itm_dol_padded_coat,itm_gon_tab_shield_c,itm_gondor_lance,itm_amroth_sword_a,itm_gondor_lance,itm_dol_shoes,itm_leather_gloves,itm_gondor_hunter,itm_gondor_dolamroth_helm,],
      attr_tier_3,wp_tier_3,knows_common|knows_riding_3|knows_shield_3|knows_power_strike_3|knows_ironflesh_3,gondor_face1,gondor_face3,],
["knight_of_dol_amroth","Knight_of_Dol_Amroth","Knights_of_Dol_Amroth",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,subfac_dol_amroth,fac_gondor,
   [itm_dol_hauberk,itm_gondor_lance,itm_gondor_lance,itm_amroth_sword_b,itm_gondor_lance,itm_gon_tab_shield_c,itm_dol_greaves,itm_swan_knight_helm,itm_gondor_lance,itm_mail_mittens,itm_dol_amroth_warhorse,],
      attr_tier_4,wp_tier_4,knows_common|knows_riding_4|knows_shield_4|knows_power_strike_4|knows_ironflesh_4,gondor_face1,gondor_face3,],
["veteran_knight_of_dol_amroth","Veteran_Knight_of_Dol_Amroth","Veteran_Knights_of_Dol_Amroth",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,subfac_dol_amroth,fac_gondor,
   [itm_dol_heavy_mail,itm_gondor_lance,itm_gondor_lance,itm_amroth_sword_b,itm_gondor_lance,itm_dol_heavy_mail,itm_gon_tab_shield_c,itm_gondor_lance,itm_dol_greaves,itm_swan_knight_helm,itm_mail_mittens,itm_dol_amroth_warhorse,],
      attr_tier_5,wp_tier_5,knows_common|knows_riding_5|knows_shield_4|knows_power_strike_5|knows_ironflesh_5,gondor_face1,gondor_face3,],
["swan_knight_of_dol_amroth","Swan_Knight_of_Dol_Amroth","Swan_Knights_of_Dol_Amroth",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,subfac_dol_amroth,fac_gondor,
   [itm_amroth_lance_banner,itm_dol_very_heavy_mail,itm_amroth_sword_b,itm_gon_tab_shield_c,itm_dol_greaves,itm_swan_knight_helm,itm_mail_mittens,itm_dol_amroth_warhorse2,],
      attr_tier_6,wp (360),knows_common|knows_riding_8|knows_shield_4|knows_power_strike_8|knows_ironflesh_6,gondor_face1,gondor_face3,],
["dol_amroth_leader","Captain_of_Dol_Amroth","Captains_of_Dol_Amroth",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,subfac_dol_amroth,fac_gondor,
   [itm_dol_very_heavy_mail,itm_amroth_bastard,itm_dol_greaves,itm_dol_amroth_warhorse2,itm_gon_tab_shield_c,itm_mail_mittens,itm_gondor_leader_helm,itm_amroth_lance_banner,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_8|knows_shield_9|knows_power_strike_8|knows_ironflesh_10,gondor_face1,gondor_face3,],
#Lothlorien
["lothlorien_scout","Lothlorien_Scout","Lothlorien_Scouts",tf_lorien| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_short_bow,itm_elven_arrows,itm_lorien_archer,itm_lorien_boots,itm_lorien_sword_b,],
      attr_elf_tier_1,wp_elf_tier_1,knows_common|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_1,lorien_elf_face_1,lorien_elf_face_2],
["lothlorien_veteran_scout","Lothlorien_Veteran_Scout","Lothlorien_Veteran_Scouts",tf_lorien| tfg_ranged| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_elven_bow,itm_elven_arrows,itm_lorien_helm_a,itm_lorien_archer,itm_lorien_boots,itm_lorien_sword_b,],
      attr_elf_tier_2,wp_elf_tier_2,knows_common|knows_athletics_4|knows_power_draw_4|knows_power_draw_4|knows_ironflesh_1,lorien_elf_face_1,lorien_elf_face_2],
["lothlorien_archer","Lothlorien_Archer","Lothlorien_Archers",tf_lorien| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_elven_bow,itm_elven_arrows,itm_lorien_helm_a,itm_lorien_armor_a,itm_lorien_boots,itm_lorien_sword_b,],
      attr_elf_tier_3,wp_elf_tier_3,knows_common|knows_athletics_5|knows_power_draw_4|knows_power_strike_3|knows_ironflesh_3,lorien_elf_face_1,lorien_elf_face_2],
["lothlorien_veteran_archer","Lothlorien_Veteran_Archer","Lothlorien_Veteran_Archers",tf_lorien| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_lorien_bow,itm_elven_arrows,itm_lorien_helm_a,itm_lorien_armor_e,itm_lorien_boots,itm_lorien_sword_b,],
      attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_6|knows_power_draw_5|knows_power_strike_3|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["lothlorien_master_archer","Lothlorien_Master_Archer","Lothlorien_Master_Archers",tf_lorien| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_lorien_bow,itm_elven_arrows,itm_lorien_helm_b,itm_lorien_armor_e,itm_lorien_boots,itm_lorien_sword_b,itm_lorien_round_shield,],
      attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_7|knows_power_draw_6|knows_power_strike_4|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["galadhrim_royal_archer","Galadhrim_Royal_Archer","Galadhrim_Royal_Archers",tf_lorien| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_lorien_bow,itm_elven_arrows,itm_lorien_helm_b,itm_lorien_armor_c,itm_lorien_boots,itm_lorien_sword_b,itm_lorien_round_shield,],
      attr_elf_tier_6,wp_elf_tier_6,knows_common|knows_athletics_8|knows_power_draw_7|knows_power_strike_4|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["galadhrim_royal_marksman","Galadhrim_Royal_Marksman","Galadhrim_Royal_Marksmen",tf_lorien| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_lorien_bow,itm_elven_arrows,itm_lorien_helm_b,itm_lorien_armor_f,itm_lorien_boots,itm_lorien_sword_b,itm_lorien_shield_c,],
      attr_elf_tier_6,wp_elf_tier_6,knows_common|knows_athletics_7|knows_shield_1|knows_power_draw_6|knows_power_strike_4|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["noldorin_mounted_archer","Noldorin_Mounted_Archer","Noldorin_Mounted_Archers",tf_lorien| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_glorfi_bow,itm_elven_arrows,itm_lorien_helm_b,itm_lorien_armor_c,itm_lorien_boots,itm_lorien_warhorse,itm_lorien_sword_a,itm_lorien_round_shield,],
      attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_horse_archery_7|knows_riding_7|knows_athletics_5|knows_power_draw_9|knows_power_strike_6|knows_ironflesh_6,lorien_elf_face_1,lorien_elf_face_2],
["lothlorien_infantry","Lothlorien_Infantry","Lothlorien_Infantry",tf_lorien| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_lorien_helm_c,itm_lorien_armor_a,itm_lorien_boots,itm_leather_gloves,itm_lorien_shield_c,itm_lorien_sword_a],
      attr_elf_tier_1,wp_elf_tier_1,knows_common|knows_athletics_4|knows_power_draw_4|knows_power_strike_2|knows_ironflesh_3,lorien_elf_face_1,lorien_elf_face_2],
["lothlorien_veteran_infantry","Lothlorien_Veteran_Infantry","Lothlorien_Veteran_Infantry",tf_lorien| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_lorien_helm_c,itm_lorien_armor_a,itm_lorien_boots,itm_mail_mittens,itm_lorien_sword_a,itm_lorien_shield_c,],
      attr_elf_tier_2,wp_elf_tier_2,knows_common|knows_athletics_5|knows_power_draw_3|knows_power_strike_3|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["lothlorien_elite_infantry","Lothlorien_Elite_Infantry","Lothlorien_Elite_Infantry",tf_lorien| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_lorien_helm_c,itm_lorien_armor_b,itm_lorien_boots,itm_mail_mittens,itm_lorien_sword_a,itm_lorien_shield_b,],
      attr_elf_tier_4,wp_elf_tier_5,knows_common|knows_athletics_5|knows_power_draw_3|knows_power_strike_5|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["galadhrim_royal_swordsman","Galadhrim_Royal_Swordsman","Galadhrim_Royal_Swordsmen",tf_lorien| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_lorien_helm_c,itm_lorien_armor_d,itm_lorien_boots,itm_mail_mittens,itm_lorien_sword_a,itm_lorien_shield_b,],
      attr_elf_tier_5,wp_melee(500),knows_common|knows_athletics_5|knows_power_draw_6|knows_power_strike_8|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["lothlorien_warden","Lothlorien_Warden","Lothlorien_Wardens",tf_lorien| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_elven_bow,itm_elven_arrows,itm_lorien_helm_b,itm_lorien_armor_e,itm_lorien_boots,itm_lorien_sword_c,],
      attr_elf_tier_2,wp_elf_tier_2,knows_common|knows_athletics_6|knows_power_draw_5|knows_power_strike_4|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["lothlorien_veteran_warden","Lothlorien_Veteran_Warden","Lothlorien_Veteran_Wardens",tf_lorien| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_elven_bow,itm_elven_arrows,itm_lorien_helm_b,itm_lorien_armor_e,itm_lorien_boots,itm_lorien_sword_c,],
      attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_7|knows_power_draw_5|knows_power_strike_4|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["galadhrim_royal_warden","Galadhrim_Royal_Warden","Galadhrim_Royal_Wardens",tf_lorien| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_lorien_bow,itm_elven_arrows,itm_lorien_helm_b,itm_lorien_armor_d,itm_lorien_boots,itm_lorien_sword_c,itm_lorien_shield_c,],
      attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_8|knows_power_draw_6|knows_power_strike_4|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["lothlorien_standard_bearer","Lothlorien_Standard_Bearer","Lothlorien_Standard_Bearers",tf_lorien| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_lorien,
   [itm_lorien_helm_c,itm_lorien_armor_f,itm_lorien_boots,itm_mail_mittens,itm_lorien_banner,],
      attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_3|knows_power_draw_3|knows_power_strike_7|knows_ironflesh_10,lorien_elf_face_1,lorien_elf_face_2],
["lorien_items","BUG","_",tf_hero,0,0,fac_lorien,
   [itm_saddle_horse,itm_short_bow,itm_good_mace,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
##MIRKWOOD#####
["greenwood_scout","Greenwood_Scout","Greenwood_Scouts",tf_woodelf| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_short_bow,itm_woodelf_arrows,itm_mirkwood_armor_a,itm_mirkwood_boots,itm_mirkwood_knife,],
      attr_elf_tier_1,wp_elf_tier_1,knows_common|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_1,mirkwood_elf_face_1,mirkwood_elf_face_2],
["greenwood_veteran_scout","Greenwood_Veteran_Scout","Greenwood_Veteran_Scouts",tf_woodelf| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_short_bow,itm_woodelf_arrows,itm_mirkwood_armor_a,itm_mirkwood_boots,itm_mirkwood_knife,],
      attr_elf_tier_2,wp_elf_tier_2,knows_common|knows_athletics_4|knows_power_draw_4|knows_power_strike_2|knows_ironflesh_1,mirkwood_elf_face_1,mirkwood_elf_face_2],
["greenwood_archer","Greenwood_Bowman","Greenwood_Bowmen",tf_woodelf| tfg_ranged| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_armor_a,itm_mirkwood_boots,itm_mirkwood_knife,],
      attr_elf_tier_3,wp_elf_tier_3,knows_common|knows_athletics_5|knows_power_draw_5|knows_power_strike_3|knows_ironflesh_3,mirkwood_elf_face_1,mirkwood_elf_face_2],
["greenwood_veteran_archer","Greenwood_Archer","Greenwood_Archers",tf_woodelf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_armor_d,itm_mirkwood_boots,itm_mirkwood_knife,itm_mirkwood_helm_a,],
      attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_6|knows_power_draw_5|knows_power_strike_3|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["greenwood_master_archer","Greenwood_Veteran_Archer","Greenwood_Veteran_Archers",tf_woodelf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_armor_d,itm_mirkwood_leather_greaves,itm_mirkwood_knife,itm_mirkwood_helm_a,],
      attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_7|knows_power_draw_6|knows_power_strike_4|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["thranduils_royal_marksman","Thranduil's_Royal_Marksman","Thranduil's_Royal_Marksmen",tf_woodelf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_armor_e,itm_mirkwood_leather_greaves,itm_mirkwood_knife,itm_mirkwood_helm_d,],
      attr_elf_tier_6,wp_elf_tier_6,knows_common|knows_athletics_8|knows_power_draw_7|knows_power_strike_4|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["greenwood_sentinel","Greenwood_Sentinel","Greenwood_Sentinels",tf_woodelf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_armor_a,itm_mirkwood_boots,itm_mirkwood_sword,itm_mirkwood_spear_shield_b,],
      attr_elf_tier_3,wp_elf_tier_3,knows_common|knows_athletics_6|knows_power_draw_5|knows_power_strike_4|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["greenwood_vet_sentinel","Greenwood_Veteran_Sentinel","Greenwood_Veteran_Sentinels",tf_woodelf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_armor_a,itm_mirkwood_boots,itm_mirkwood_sword,itm_mirkwood_helm_a,itm_mirkwood_spear_shield_b,],
      attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_7|knows_power_draw_6|knows_power_strike_4|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["mirkwood_guardsman","Greenwood_Guardsman","Greenwood_Guardsmen",tf_woodelf| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_armor_a,itm_mirkwood_boots,itm_mirkwood_sword,itm_mirkwood_helm_d,itm_mirkwood_spear_shield_c,],
      attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_8|knows_power_draw_7|knows_power_strike_4|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["greenwood_spearman","Greenwood_Infantry","Greenwood_Infantry",tf_woodelf| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_mirkwood_war_spear,itm_mirkwood_spear_shield_a,itm_leather_gloves,itm_mirkwood_armor_a,itm_mirkwood_boots,itm_mirkwood_short_spear,itm_mirkwood_helm_b,itm_mirkwood_sword,],
      attr_elf_tier_2,wp_elf_tier_2,knows_common|knows_athletics_5|knows_power_draw_3|knows_power_strike_3|knows_ironflesh_3,mirkwood_elf_face_1,mirkwood_elf_face_2],
["greenwood_veteran_spearman","Greenwood_Veteran_Infantry","Greenwood_Veteran_Infantry",tf_woodelf| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_mirkwood_war_spear,itm_mirkwood_spear_shield_a,itm_leather_gloves,itm_mirkwood_light_scale,itm_mirkwood_leather_greaves,itm_mirkwood_helm_b,itm_mirkwood_sword,],
      attr_elf_tier_3,wp_elf_tier_3,knows_common|knows_athletics_6|knows_power_draw_3|knows_power_strike_4|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["greenwood_royal_spearman","Greenwood_Elite_Infantry","Greenwood_Elite_Infantry",tf_woodelf| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_mirkwood_war_spear,itm_mirkwood_spear_shield_b,itm_leather_gloves,itm_mirkwood_armor_d,itm_mirkwood_leather_greaves,itm_mirkwood_helm_b,],
      attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_7|knows_power_draw_3|knows_power_strike_5|knows_ironflesh_5,mirkwood_elf_face_1,mirkwood_elf_face_2],
["thranduils_royal_swordsman","Thranduil's_Royal_Swordsman","Thranduil's_Royal_Swordsmen",tf_woodelf| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_mirkwood_spear_shield_c,itm_leather_gloves,itm_mirkwood_armor_e,itm_mirkwood_leather_greaves,itm_mirkwood_helm_b,itm_mirkwood_sword,],
      attr_elf_tier_5,wp_elf_tier_6,knows_common|knows_athletics_8|knows_power_draw_7|knows_power_strike_7|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["thranduils_spearman","Thranduil's_Royal_Spearman","Thranduil's_Royal_Spearmen",tf_woodelf| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_mirkwood_great_spear,itm_leather_gloves,itm_mirkwood_armor_c,itm_mirkwood_leather_greaves,itm_mirkwood_helm_c,],
      attr_elf_tier_5,wp_melee (500),knows_common|knows_athletics_8|knows_power_draw_7|knows_power_strike_7|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["greenwood_standard_bearer","Greenwood_Standard_Bearer","Greenwood_Standard_Bearers",tf_woodelf| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_woodelf,
   [itm_mirkwood_armor_c,itm_mirkwood_leather_greaves,itm_mirkwood_helm_a,itm_woodelf_banner,],
      attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_4|knows_power_draw_6|knows_power_strike_4|knows_ironflesh_10,mirkwood_elf_face_1,mirkwood_elf_face_2],
["woodelf_items","BUG","_",tf_hero,0,0,fac_woodelf,
   [itm_leather_boots,itm_leather_gloves,itm_short_bow,itm_arrows,itm_sumpter_horse,itm_saddle_horse,itm_good_mace,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
#Rivendell
["rivendell_scout","Rivendell_Scout","Rivendell_Scouts",tf_imladris| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,
   [itm_riv_boots,itm_riv_bow,itm_riv_armor_light,itm_riv_archer_sword,itm_elven_arrows,],
      attr_elf_tier_1,wp_elf_tier_1,knows_common|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_1,rivendell_elf_face_1,rivendell_elf_face_2],
["rivendell_veteran_scout","Rivendell_Veteran_Scout","Rivendell_Veteran_Scouts",tf_imladris| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,
   [itm_riv_boots,itm_riv_bow,itm_riv_armor_light,itm_riv_archer_sword,itm_elven_arrows,],
      attr_elf_tier_2,wp_elf_tier_2,knows_common|knows_athletics_2|knows_power_strike_2|knows_power_draw_3|knows_power_strike_4|knows_ironflesh_1,rivendell_elf_face_1,rivendell_elf_face_2],
["rivendell_sentinel","Rivendell_Sentinel","Rivendell_Sentinels",tf_imladris| tfg_ranged| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,
   [itm_riv_boots,itm_riv_bow,itm_riv_armor_archer,itm_riv_archer_sword,itm_elven_arrows,itm_riv_helm_a,],
      attr_elf_tier_3,wp_elf_tier_3,knows_common|knows_athletics_4|knows_power_draw_4|knows_power_strike_3|knows_ironflesh_3,rivendell_elf_face_1,rivendell_elf_face_2],
["rivendell_veteran_sentinel","Rivendell_Veteran_Sentinel","Rivendell_Veteran_Sentinels",tf_imladris| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,
   [itm_riv_boots,itm_riv_bow,itm_riv_armor_archer,itm_riv_archer_sword,itm_elven_arrows,itm_riv_helm_a,],
      attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_5|knows_power_draw_4|knows_power_strike_3|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["rivendell_elite_sentinel","Rivendell_Elite_Sentinel","Rivendell_Elite_Sentinels",tf_imladris| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,
   [itm_riv_boots,itm_riv_bow,itm_riv_armor_m_archer,itm_riv_1h_sword,itm_elven_arrows,itm_riv_helm_b,itm_riv_shield_a,],
      attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_5|knows_power_draw_5|knows_power_strike_4|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["rivendell_guardian","Rivendell_Guardian","Rivendell_Guardians",tf_imladris| tfg_ranged| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,
   [itm_riv_boots,itm_leather_gloves,itm_riv_bow,itm_riv_armor_m_archer,itm_riv_1h_sword,itm_elven_arrows,itm_riv_helm_b,itm_riv_shield_a,],
      attr_elf_tier_6,wp_elf_tier_6,knows_common|knows_horse_archery_6|knows_athletics_5|knows_power_draw_6|knows_power_strike_4|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["rivendell_infantry","Rivendell_Infantry","Rivendell_Infantry",tf_imladris| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,
   [itm_riv_boots,itm_leather_gloves,itm_riv_spear,itm_riv_armor_light,itm_riv_1h_sword,itm_riv_helm_a,itm_riv_shield_a,],
      attr_elf_tier_2,wp_elf_tier_2,knows_common|knows_athletics_4|knows_power_draw_4|knows_power_strike_3|knows_ironflesh_3,rivendell_elf_face_1,rivendell_elf_face_2],
["rivendell_veteran_infantry","Rivendell_Veteran_Infantry","Rivendell_Veteran_Infantry",tf_imladris| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,
   [itm_riv_boots,itm_leather_gloves,itm_riv_spear,itm_riv_armor_light_inf,itm_riv_1h_sword,itm_riv_helm_b,itm_riv_shield_a,],
      attr_elf_tier_3,wp_elf_tier_3,knows_common|knows_athletics_5|knows_power_draw_4|knows_power_strike_4|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["rivendell_elite_infantry","Rivendell_Elite_Infantry","Rivendell_Elite_Infantry",tf_imladris| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,
   [itm_riv_boots,itm_leather_gloves,itm_riv_spear,itm_riv_armor_med,itm_riv_1h_sword,itm_riv_helm_c,itm_riv_shield_a,],
      attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_5|knows_power_draw_5|knows_power_strike_5|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["rivendell_royal_infantry","Rivendell_Royal_Infantry","Rivendell_Royal_Infantry",tf_imladris| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,
   [itm_riv_boots,itm_mail_mittens,itm_riv_spear,itm_riv_armor_heavy,itm_riv_1h_sword,itm_riv_bas_sword,itm_riv_helm_c,itm_riv_shield_a,],
      attr_elf_tier_5,wp_elf_tier_6,knows_common|knows_horse_archery_6|knows_athletics_5|knows_power_draw_6|knows_power_strike_7|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["rivendell_cavalry","Rivendell_Cavalry","Rivendell_Cavalry",tf_imladris| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,
   [itm_riv_boots,itm_leather_gloves,itm_riv_spear,itm_riv_armor_h_archer,itm_riv_1h_sword,itm_riv_riding_sword,itm_riv_bas_sword,itm_riv_helm_c,itm_riv_warhorse,itm_riv_shield_b,],
      attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_5|knows_power_draw_5|knows_power_strike_6|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["knight_of_rivendell","Knight_of_Rivendell","Knights_of_Rivendell",tf_imladris| tfg_ranged| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,
   [itm_riv_boots,itm_strong_bow,itm_riv_armor_h_archer,itm_riv_1h_sword,itm_elven_arrows,itm_riv_bas_sword,itm_riv_helm_c,itm_riv_warhorse2,itm_riv_shield_b,itm_riv_spear,itm_riv_riding_sword,],
      attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_horse_archery_6|knows_athletics_5|knows_power_draw_6|knows_power_strike_6|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["rivendell_standard_bearer","Rivendell_Standard_Bearer","Rivendell_Standard_Bearers",tf_imladris| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_imladris,
   [itm_riv_boots,itm_mail_mittens,itm_riv_armor_heavy,itm_riv_helm_c,itm_imladris_banner,],
      attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_3|knows_power_draw_6|knows_power_strike_6|knows_ironflesh_10,rivendell_elf_face_1,rivendell_elf_face_2],
#Dunedain
["dunedain_scout","Dunedain_Scout","Dunedain_Scouts",tf_dunedain| tfg_armor| tfg_boots,0,0,fac_imladris,
   [itm_arnor_splinted,itm_leather_gloves,itm_short_bow,itm_arnor_armor_c,itm_arnor_sword_f,itm_arrows,],
      attr_elf_tier_1,wp_elf_tier_1,knows_common|knows_power_draw_3|knows_power_strike_1|knows_ironflesh_1,arnor_face_middle_1,arnor_face_middle_2],
["dunedain_trained_scout","Dunedain_Tracker","Dunedain_Trackers",tf_dunedain| tfg_armor| tfg_boots,0,0,fac_imladris,
   [itm_arnor_splinted,itm_leather_gloves,itm_short_bow,itm_arnor_armor_c,itm_arnor_sword_f,itm_arrows,],
      attr_elf_tier_2,wp_elf_tier_2,knows_common|knows_athletics_2|knows_power_draw_3|knows_power_strike_4|knows_ironflesh_1,arnor_face_middle_1,arnor_face_middle_2],
["arnor_man_at_arms","Arnor_Man_at_Arms","Arnor_Men_at_Arms",tf_dunedain| tfg_armor| tfg_helm| tfg_boots,0,0,fac_imladris,
   [itm_arnor_greaves,itm_leather_gloves,itm_arnor_armor_b,itm_arnor_sword_f,itm_arnor_shield_a,itm_arnor_helm_c,],
      attr_elf_tier_3,wp_elf_tier_3,knows_common|knows_athletics_4|knows_power_draw_4|knows_power_strike_5|knows_ironflesh_3,arnor_face_middle_1,arnor_face_middle_2],
["arnor_master_at_arms","Arnor_Master_at_Arms","Arnor_Masters_at_Arms",tf_dunedain| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_imladris,
   [itm_arnor_greaves,itm_leather_gloves,itm_arnor_armor_a,itm_arnor_sword_a,itm_arnor_shield_a,itm_arnor_helm_b,],
      attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_5|knows_power_draw_5|knows_power_strike_6|knows_ironflesh_4,arnor_face_middle_1,arnor_face_middle_2],
["high_swordsman_of_arnor","High_Swordsman_of_Arnor","High_Swordsmen_of_Arnor",tf_dunedain| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_imladris,
   [itm_arnor_greaves,itm_mail_mittens,itm_arnor_armor_f,itm_arnor_sword_c,itm_arnor_shield_a,itm_dunedain_helm_b,],
      attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_5|knows_power_draw_5|knows_power_strike_7|knows_ironflesh_6,arnor_face_older_1,arnor_face_older_2],
["arnor_horsemen","Arnor_Horseman","Arnor_Horsemen",tf_dunedain| tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_imladris,
   [itm_arnor_greaves,itm_mail_mittens,itm_arnor_armor_a,itm_arnor_sword_a,itm_arnor_shield_c,itm_arnor_helm_b,itm_dunedain_warhorse,],
      attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_riding_4|knows_athletics_4|knows_power_draw_3|knows_power_strike_6|knows_ironflesh_4,arnor_face_older_1,arnor_face_older_2],
["knight_of_arnor","Knight_of_Arnor","Knights_of_Arnor",tf_dunedain| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_imladris,
   [itm_arnor_greaves,itm_mail_mittens,itm_lance,itm_arnor_armor_f,itm_arnor_sword_c,itm_arnor_shield_c,itm_dunedain_helm_b,itm_arnor_warhorse,],
      attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_riding_5|knows_athletics_5|knows_power_strike_7|knows_ironflesh_5|knows_power_draw_6,arnor_face_older_1,arnor_face_older_2],
["dunedain_ranger","Dunedain_Ranger","Dunedain_Rangers",tf_dunedain| tfg_ranged| tfg_gloves| tfg_armor| tfg_boots,0,0,fac_imladris,
   [itm_arnor_splinted,itm_elven_bow,itm_arnor_armor_d,itm_arnor_sword_f,itm_ithilien_arrows,itm_dunedain_helm_a,],
      attr_elf_tier_3,wp_elf_tier_3,knows_common|knows_athletics_6|knows_power_draw_4|knows_power_strike_4|knows_ironflesh_4,arnor_face_middle_1,arnor_face_middle_2],
["dunedain_veteran_ranger","Dunedain_Veteran_Ranger","Dunedain_Veteran_Rangers",tf_dunedain| tfg_ranged| tfg_gloves| tfg_armor| tfg_boots,0,0,fac_imladris,
   [itm_arnor_splinted,itm_elven_bow,itm_arnor_armor_d,itm_arnor_sword_f,itm_ithilien_arrows,itm_dunedain_helm_a,],
      attr_elf_tier_4,wp_elf_tier_4,knows_common|knows_athletics_6|knows_power_draw_5|knows_power_strike_4|knows_ironflesh_4,arnor_face_older_1,arnor_face_older_2],
["dunedain_master_ranger","Dunedain_Master_Ranger","Dunedain_Master_Rangers",tf_dunedain| tfg_ranged| tfg_gloves| tfg_armor| tfg_boots,0,0,fac_imladris,
   [itm_arnor_greaves,itm_elven_bow,itm_arnor_armor_d,itm_arnor_sword_f,itm_ithilien_arrows,itm_dunedain_helm_a,],
      attr_elf_tier_5,wp_elf_tier_5,knows_common|knows_athletics_7|knows_power_draw_6|knows_power_strike_4|knows_ironflesh_4,arnor_face_older_1,arnor_face_older_2],
["imladris_items","BUG","BUG",tf_hero,0,0,fac_imladris,
   [itm_leather_boots,itm_leather_gloves,itm_short_bow,itm_good_mace,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
#ROHAN
["rohan_youth","Rohan_Youth","Rohan_Youths",tf_rohan| tfg_armor| tfg_boots,0,0,fac_rohan,
   [itm_rohan_shoes,itm_rohan_armor_a,itm_rohan_armor_b,itm_rohirrim_short_axe,itm_spear,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      attr_tier_1,wp_tier_1,knows_common,rohan_face_younger_1,rohan_face_middle_2],
["guardsman_of_rohan","Guardsman_of_Rohan","Guardsmen_of_Rohan",tf_rohan| tfg_armor| tfg_boots,0,0,fac_rohan,
   [itm_rohan_shoes,itm_rohan_armor_g,itm_rohan_armor_h,itm_rohan_armor_i,itm_rohan_light_helmet_a,itm_rohan_light_helmet_b,itm_spear,itm_rohan_sword_c,itm_rohan_shield_a,itm_rohan_shield_b,itm_rohan_shield_c,itm_good_mace,],
      attr_tier_2,wp_tier_2,knows_common|knows_athletics_1|knows_power_strike_1,rohan_face_young_1,rohan_face_old_2],
["footman_of_rohan","Footman_of_Rohan","Footmen_of_Rohan",tf_rohan| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,
   [itm_rohan_light_greaves,itm_rohan_armor_d,itm_rohan_armor_e,itm_rohan_armor_f,itm_rohan_light_helmet_b,itm_rohan_inf_helmet_a,itm_rohirrim_short_axe,itm_spear,itm_rohan_sword_c,itm_rohan_shield_a,itm_rohan_shield_b,itm_rohan_shield_c,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_shield_2|knows_power_strike_2|knows_ironflesh_1,rohan_face_middle_1,rohan_face_old_2],
["veteran_footman_of_rohan","Veteran_Footman_of_Rohan","Veteran_Footmen_of_Rohan",tf_rohan| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,
   [itm_rohan_light_greaves,itm_rohan_armor_j,itm_rohan_armor_k,itm_rohan_armor_l,itm_rohan_inf_helmet_b,itm_rohirrim_short_axe,itm_heavy_throwing_spear,itm_rohan_spear,itm_rohan_sword_c,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_shield_2|knows_power_strike_3|knows_ironflesh_2,rohan_face_middle_1,rohan_face_old_2],
["elite_footman_of_rohan","Elite_Footman_of_Rohan","Elite_Footmen_of_Rohan",tf_rohan| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,
   [itm_rohirrim_war_greaves,itm_rohan_armor_m,itm_rohan_armor_n,itm_rohan_armor_o,itm_rohan_inf_helmet_b,itm_rohirrim_long_hafted_axe,itm_rohirrim_short_axe,itm_heavy_throwing_spear,itm_rohan_spear,itm_rohan_sword_c,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_shield_2|knows_power_throw_4|knows_power_strike_4|knows_ironflesh_2,rohan_face_middle_1,rohan_face_old_2],
["folcwine_guard_of_rohan","Folcwine_Guard_of_Rohan","Folcwine_Guards_of_Rohan",tf_rohan| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,
   [itm_rohirrim_war_greaves,itm_rohan_armor_s,itm_rohan_inf_helmet_b,itm_rohirrim_long_hafted_axe,itm_rohirrim_short_axe,itm_heavy_throwing_spear,itm_rohirrim_throwing_axe,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,],
      attr_tier_6,wp_tier_6,knows_common|knows_athletics_4|knows_shield_2|knows_power_throw_6|knows_power_strike_6|knows_ironflesh_5,rohan_face_middle_1,rohan_face_old_2],
["raider_of_rohan","Frealaf_Raider","Frealaf_Raiders",tf_rohan| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,
   [itm_rohan_light_greaves,itm_rohan_armor_o,itm_rohan_armor_n,itm_rohan_armor_m,itm_rohirrim_long_hafted_axe,itm_rohirrim_short_axe,itm_rohirrim_throwing_axe,itm_rohan_shield_a,itm_rohan_shield_b,itm_rohan_shield_c,],
      attr_tier_6,wp_tier_6,knows_common|knows_athletics_7|knows_shield_3|knows_power_throw_2|knows_power_strike_6|knows_ironflesh_5,rohan_face_middle_1,rohan_face_old_2],
["heavy_swordsman_of_rohan","Heavy_Swordsman_of_Rohan","Heavy_Swordsmen_of_Rohan",tf_rohan| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,
   [itm_rohan_light_greaves,itm_rohan_armor_m,itm_rohan_armor_n,itm_rohan_armor_o,itm_rohan_inf_helmet_b,itm_rohan_2h_sword,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_shield_2|knows_power_strike_4|knows_ironflesh_2,rohan_face_middle_1,rohan_face_old_2],
["warden_of_methuseld","Warden_of_Methuseld","Wardens_of_Methuseld",tf_rohan| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,
   [itm_rohirrim_war_greaves,itm_rohan_armor_p,itm_rohan_armor_q,itm_rohan_armor_r,itm_rohan_inf_helmet_b,itm_rohan_sword_c,itm_rohan_shield_g,],
      attr_tier_6,wp_tier_6,knows_common|knows_athletics_5|knows_shield_2|knows_power_strike_6|knows_ironflesh_6,rohan_face_old_1,rohan_face_older_2],
["skirmisher_of_rohan","Skirmisher_of_Rohan","Skirmishers_of_Rohan",tf_rohan| tfg_ranged| tf_mounted| tfg_armor| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_light_greaves,itm_rohan_armor_g,itm_rohan_armor_h,itm_rohan_armor_i,itm_rohan_light_helmet_a,itm_rohan_light_helmet_b,itm_nomad_bow,itm_khergit_arrows,itm_heavy_throwing_spear,itm_rohan_sword_c,itm_rohan_shield_a,itm_rohan_shield_b,itm_rohan_shield_c,itm_rohirrim_courser,itm_rohirrim_courser2,],
      attr_tier_3,wp_tier_3,knows_horse_archery_2|knows_riding_3|knows_power_draw_2|knows_power_throw_2,rohan_face_young_1,rohan_face_middle_2],
["veteran_skirmisher_of_rohan","Veteran_Skirmisher_of_Rohan","Veteran_Skirmishers_of_Rohan",tf_rohan| tfg_ranged| tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_light_greaves,itm_rohan_armor_j,itm_rohan_armor_k,itm_rohan_armor_l,itm_rohan_archer_helmet_a,itm_rohan_archer_helmet_b,itm_nomad_bow,itm_khergit_arrows,itm_rohirrim_long_hafted_axe,itm_rohan_sword_c,itm_rohirrim_long_hafted_axe,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,itm_rohirrim_courser,itm_rohirrim_courser2,],
      attr_tier_4,wp_tier_4,knows_horse_archery_3|knows_riding_4|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_1|knows_power_throw_3,rohan_face_middle_1,rohan_face_old_2],
["elite_skirmisher_of_rohan","Elite_Skirmisher_of_Rohan","Elite_Skirmishers_of_Rohan",tf_rohan| tfg_ranged| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_light_greaves,itm_rohan_armor_m,itm_rohan_armor_o,itm_rohan_archer_helmet_b,itm_rohan_archer_helmet_c,itm_strong_bow,itm_khergit_arrows,itm_rohan_sword_c,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,itm_rohan_warhorse,],
      attr_tier_5,wp_tier_5,knows_horse_archery_5|knows_riding_6|knows_power_draw_4|knows_power_strike_2|knows_ironflesh_2|knows_power_throw_4,rohan_face_middle_1,rohan_face_old_2],
["thengel_guard_of_rohan","Thengel_Guard_of_Rohan","Thengel_Guards_of_Rohan",tf_rohan| tfg_ranged| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_shoes,itm_rohan_armor_s,itm_rohan_archer_helmet_c,itm_strong_bow,itm_khergit_arrows,itm_rohan_sword_c,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,itm_thengel_warhorse,],
      attr_tier_6,wp_tier_6,knows_horse_archery_7|knows_riding_7|knows_power_draw_5|knows_power_strike_3|knows_ironflesh_3|knows_power_throw_5,rohan_face_middle_1,rohan_face_old_2],
["lancer_of_rohan","Lancer_of_Rohan","Lancers_of_Rohan",tf_rohan| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_armor_j,itm_rohan_armor_k,itm_rohan_armor_l,itm_rohan_cav_helmet_b,itm_rohan_spear,itm_rohan_lance,itm_rohan_cav_sword,itm_rohan_shield_a,itm_rohan_shield_b,itm_rohan_shield_c,itm_rohirrim_courser,itm_rohirrim_courser2,itm_rohirrim_hunter,],
      attr_tier_4,wp_tier_4,knows_common|knows_riding_4|knows_shield_1|knows_power_strike_4|knows_ironflesh_2,rohan_face_middle_1,rohan_face_old_2],
["elite_lancer_of_rohan","Elite_Lancer_of_Rohan","Elite_Lancers_of_Rohan",tf_rohan| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_armor_m,itm_rohan_armor_n,itm_rohan_armor_o,itm_rohan_cav_helmet_b,itm_rohan_cav_helmet_c,itm_rohan_lance,itm_rohan_lance,itm_rohan_lance_banner_horse,itm_rohan_cav_sword,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,itm_rohan_warhorse,],
      attr_tier_5,wp_tier_5,knows_common|knows_riding_5|knows_shield_2|knows_power_strike_5|knows_ironflesh_3,rohan_face_middle_1,rohan_face_old_2],
["brego_guard_of_rohan","Brego_Guard_of_Rohan","Brego_Guards_of_Rohan",tf_rohan| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_armor_s,itm_rohan_cav_helmet_c,itm_rohan_lance_banner_sun,itm_rohan_lance_banner_horse,itm_rohan_cav_sword,itm_rohan_warhorse,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_7|knows_shield_3|knows_power_strike_6|knows_ironflesh_6,rohan_face_middle_1,rohan_face_old_2],
["king_s_man_of_rohan","King's_Guard","King's_Guards",tf_rohan| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_armor_p,itm_rohan_armor_q,itm_rohan_armor_r,itm_rohan_cav_helmet_c,itm_rohan_spear,itm_rohan_inf_sword,itm_rohan_cav_sword,itm_rohirrim_long_hafted_axe,itm_rohan_sword_c,itm_rohan_shield_g,itm_rohan_warhorse,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_7|knows_shield_3|knows_power_strike_7|knows_ironflesh_6,rohan_face_old_1,rohan_face_older_2],
["squire_of_rohan","Squire_of_Rohan","Squires_of_Rohan",tf_rohan| tf_mounted| tfg_armor| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_shoes,itm_leather_gloves,itm_rohan_armor_g,itm_rohan_armor_h,itm_rohan_armor_i,itm_rohan_light_helmet_a,itm_spear,itm_rohan_sword_c,itm_rohan_shield_a,itm_rohan_shield_b,itm_rohan_shield_c,itm_saddle_horse,],
      attr_tier_2,wp_tier_2,knows_common|knows_shield_1| knows_riding_1|knows_power_strike_1,rohan_face_young_1,rohan_face_old_2],
["rider_of_rohan","Rider_of_Rohan","Riders_of_Rohan",tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_light_greaves,itm_leather_gloves,itm_rohan_armor_d,itm_rohan_armor_e,itm_rohan_armor_f,itm_rohan_light_helmet_a,itm_rohan_light_helmet_b,itm_rohan_spear,itm_rohan_spear,itm_rohan_sword_c,itm_rohirrim_long_hafted_axe,itm_spear,itm_rohan_lance,itm_rohan_shield_a,itm_rohan_shield_b,itm_rohan_shield_c,itm_rohirrim_courser,itm_rohirrim_courser2,],
      attr_tier_3,wp_tier_3,knows_common|knows_riding_3|knows_shield_1|knows_power_strike_2,rohan_face_young_1,rohan_face_old_2],
["veteran_rider_of_rohan","Veteran_Rider_of_Rohan","Veteran_Riders_of_Rohan",tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_light_greaves,itm_mail_mittens,itm_rohan_armor_j,itm_rohan_armor_k,itm_rohan_armor_l,itm_rohan_cav_helmet_a,itm_rohan_cav_helmet_b,itm_rohan_spear,itm_rohan_cav_sword,itm_rohan_sword_c,itm_rohirrim_long_hafted_axe,itm_rohirrim_long_hafted_axe,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,itm_rohirrim_courser,itm_rohirrim_courser2,itm_rohirrim_hunter,],
      attr_tier_4,wp_tier_4,knows_common|knows_riding_5|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,rohan_face_middle_1,rohan_face_old_2],
["elite_rider_of_rohan","Elite_Rider_of_Rohan","Elite_Riders_of_Rohan",tf_rohan| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_armor_m,itm_rohan_armor_n,itm_rohan_armor_o,itm_rohan_cav_helmet_b,itm_rohan_cav_helmet_c,itm_rohan_spear,itm_rohan_cav_sword,itm_rohan_sword_c,itm_rohirrim_long_hafted_axe,itm_rohirrim_long_hafted_axe,itm_rohan_sword_c,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,itm_rohirrim_courser2,itm_rohirrim_hunter,],
      attr_tier_5,wp_tier_5,knows_common|knows_riding_6|knows_shield_3|knows_power_strike_2|knows_ironflesh_3,rohan_face_middle_1,rohan_face_old_2],
["eorl_guard_of_rohan","Eorl_Guard_of_Rohan","Eorl_Guards_of_Rohan",tf_rohan| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_armor_s,itm_rohan_captain_helmet,itm_rohan_lance_banner_sun,itm_rohan_lance_banner_horse,itm_rohan_inf_sword,itm_rohan_inf_sword,itm_rohan_cav_sword,itm_rohirrim_long_hafted_axe,itm_rohirrim_long_hafted_axe,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,itm_rohan_warhorse,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_8|knows_shield_3|knows_power_strike_6|knows_ironflesh_6,rohan_face_middle_1,rohan_face_old_2],
#Rohan Siege battle dismounted troops
["dismounted_skirmisher_of_rohan","Skirmisher_of_Rohan","Skirmishers_of_Rohan",tf_rohan| tfg_ranged| tfg_armor| tfg_boots,0,0,fac_rohan,
   [itm_rohan_light_greaves,itm_rohan_armor_g,itm_rohan_armor_h,itm_rohan_armor_i,itm_rohan_light_helmet_a,itm_rohan_light_helmet_b,itm_nomad_bow,itm_khergit_arrows,itm_heavy_throwing_spear,itm_rohan_sword_c,itm_rohan_shield_a,itm_rohan_shield_b,itm_rohan_shield_c,],
      attr_tier_3,wp_tier_3,knows_horse_archery_3|knows_riding_4|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_1|knows_power_throw_3,rohan_face_young_1,rohan_face_middle_2],
["dismounted_veteran_skirmisher_of_rohan","Veteran_Skirmisher_of_Rohan","Veteran_Skirmishers_of_Rohan",tf_rohan| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,
   [itm_rohan_light_greaves,itm_rohan_armor_j,itm_rohan_armor_k,itm_rohan_armor_l,itm_rohan_archer_helmet_a,itm_rohan_archer_helmet_b,itm_nomad_bow,itm_khergit_arrows,itm_rohirrim_long_hafted_axe,itm_rohan_sword_c,itm_rohirrim_long_hafted_axe,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,],
      attr_tier_4,wp_tier_4,knows_horse_archery_5|knows_riding_6|knows_power_draw_4|knows_power_strike_2|knows_ironflesh_2|knows_power_throw_4,rohan_face_young_1,rohan_face_old_2],
["dismounted_elite_skirmisher_of_rohan","Elite_Skirmisher_of_Rohan","Elite_Skirmishers_of_Rohan",tf_rohan| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,
   [itm_rohan_light_greaves,itm_rohan_armor_m,itm_rohan_armor_o,itm_rohan_archer_helmet_b,itm_rohan_archer_helmet_c,itm_strong_bow,itm_khergit_arrows,itm_rohan_sword_c,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,],
      attr_tier_5,wp_tier_5,knows_horse_archery_7|knows_riding_7|knows_power_draw_5|knows_power_strike_3|knows_ironflesh_3|knows_power_throw_5,rohan_face_middle_1,rohan_face_old_2],
["dismounted_thengel_guard_of_rohan","Thengel_Guard_of_Rohan","Thengel_Guards_of_Rohan",tf_rohan| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_rohan,
   [itm_rohirrim_war_greaves,itm_rohan_armor_s,itm_rohan_archer_helmet_c,itm_strong_bow,itm_khergit_arrows,itm_rohan_sword_c,itm_rohan_shield_d,itm_rohan_shield_e,itm_rohan_shield_f,],
      attr_tier_6,wp_tier_6,knows_horse_archery_5|knows_riding_7|knows_power_draw_5|knows_power_throw_5|knows_power_strike_3|knows_ironflesh_3,rohan_face_middle_1,rohan_face_old_2],
#HARAD
["harad_desert_warrior","Harad_Levy","Harad_Levies",tf_harad| tfg_armor,0,0,fac_harad,
   [itm_desert_boots,itm_harad_tunic,itm_harad_javelin,itm_harad_short_spear,],
      attr_tier_1,wp_tier_1,knows_common|knows_athletics_2|knows_shield_1|knows_power_strike_1,haradrim_face_1,haradrim_face_2],
["harad_infantry","Harad_Light_Infantry","Harad_Light_Infantry",tf_harad| tfg_armor| tfg_boots,0,0,fac_harad,
   [itm_desert_boots,itm_harad_hauberk,itm_harad_sabre,itm_harad_short_spear,itm_harad_dagger,itm_harad_long_shield_d,itm_harad_long_shield_e,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_3|knows_shield_2|knows_power_strike_2|knows_ironflesh_2,haradrim_face_1,haradrim_face_2],
["harad_veteran_infantry","Harad_Spearman","Harad_Spearmen",tf_harad| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,
   [itm_harad_scale_greaves,itm_harad_scale,itm_harad_finhelm,itm_harad_long_spear,itm_harad_long_shield_d,itm_harad_long_shield_e,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_3|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,haradrim_face_1,haradrim_face_2],
["harad_tiger_guard","Tiger_Guard","Tiger_Guards",tf_harad| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tfg_gloves,0,0,fac_harad,
   [itm_harad_scale_greaves,itm_leather_gloves,itm_harad_tiger_scale,itm_lion_helm,itm_harad_long_spear,itm_harad_long_shield_b,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_shield_4|knows_power_strike_4|knows_ironflesh_3,haradrim_face_1,haradrim_face_2],
["harad_swordsman","Harad_Swordsman","Harad_Swordsmen",tf_harad| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,
   [itm_harad_scale_greaves,itm_harad_scale,itm_harad_finhelm,itm_harad_heavy_sword,itm_harad_khopesh,itm_harad_long_shield_d,itm_harad_long_shield_e,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_3|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,haradrim_face_1,haradrim_face_2],
["harad_lion_guard","Lion_Guard","Lion_Guards",tf_harad| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,
   [itm_harad_scale_greaves,itm_leather_gloves,itm_harad_lion_scale,itm_lion_helm,itm_harad_heavy_sword,itm_harad_khopesh,itm_harad_long_shield_b,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_6|knows_power_strike_5|knows_ironflesh_6,haradrim_face_1,haradrim_face_2],
["harad_skirmisher","Harad_Skirmisher","Harad_Skirmishers",tf_harad| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,
   [itm_desert_boots,itm_harad_skirmisher,itm_harad_heavy_inf_helm,itm_harad_bow,itm_harad_arrows,itm_harad_dagger,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_1|knows_power_draw_2|knows_ironflesh_1|knows_power_throw_2,haradrim_face_1,haradrim_face_2],
["harad_archer","Harad_Archer","Harad_Archers",tf_harad| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,
   [itm_harad_leather_greaves,itm_harad_archer,itm_harad_heavy_inf_helm,itm_harad_bow,itm_harad_arrows,itm_skirmisher_sword,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_power_draw_3|knows_ironflesh_1,haradrim_face_1,haradrim_face_2],
["harad_eagle_guard","Eagle_Guard","Eagle_Guards",tf_harad| tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,
   [itm_harad_leather_greaves,itm_leather_gloves,itm_black_snake_armor,itm_harad_eaglehelm,itm_lg_bow,itm_harad_arrows,itm_eagle_guard_spear,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_2|knows_power_draw_4|knows_ironflesh_2,haradrim_face_1,haradrim_face_2],
###HARONDOR#####
["harondor_scout","Harondor_Scout","Harondor_Scouts",tf_harad| tf_mounted| tfg_armor| tfg_horse| tfg_boots,0,0,fac_harad,
   [itm_desert_boots,itm_harad_padded,itm_horandor_a,itm_harad_shield_a,itm_saddle_horse,],
      attr_tier_2,wp_tier_2,knows_common|knows_athletics_2|knows_shield_1|knows_power_strike_1,haradrim_face_1,haradrim_face_2],
["harondor_rider","Harondor_Rider","Harondor_Riders",tf_harad| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,
   [itm_harad_leather_greaves,itm_harad_hauberk,itm_harad_cav_helm_b,itm_horandor_a,itm_harad_shield_b,itm_harad_horse,itm_harad_shield_c,],
      attr_tier_3,wp_tier_3,knows_common|knows_riding_2|knows_shield_2|knows_power_strike_2,haradrim_face_1,haradrim_face_2],
["harondor_light_cavalry","Harondor_Light_Cavalry","Harondor_Light_Cavalry",tf_harad| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,
   [itm_harad_lamellar_greaves,itm_harad_lamellar,itm_harad_wavy_helm,itm_horandor_a,itm_harad_shield_b,itm_harad_warhorse,itm_harad_shield_c,],
      attr_tier_4,wp_tier_4,knows_common|knows_riding_3|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,haradrim_face_1,haradrim_face_2],
["fang_heavy_cavalry","Fang_Heavy_Cavalry","Fang_Heavy_Cavalry",tf_harad| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,
   [itm_harad_lamellar_greaves,itm_leather_gloves,itm_harad_heavy,itm_harad_dragon_helm,itm_harad_long_spear,itm_harad_yellow_shield,itm_harad_warhorse,],
      attr_tier_5,wp_tier_5,knows_common|knows_riding_5|knows_shield_3|knows_power_strike_3|knows_ironflesh_3,haradrim_face_1,haradrim_face_2],
["harad_horse_archer","Harad_Horse_Archer","Harad_Horse_Archers",tf_harad| tfg_ranged| tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,
   [itm_desert_boots,itm_harad_skirmisher,itm_harad_cav_helm_a,itm_harad_bow,itm_harad_arrows,itm_harad_sabre,itm_saddle_horse,],
      attr_tier_3,wp_tier_3,knows_common|knows_horse_archery_2|knows_riding_3|knows_shield_1|knows_power_draw_2|knows_power_strike_2|knows_ironflesh_1,haradrim_face_1,haradrim_face_2],
["black_snake_horse_archer","Black_Snake_Horse_Archer","Black_Snake_Horse_Archers",tf_harad| tfg_ranged| tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,
   [itm_harad_leather_greaves,itm_harad_archer,itm_harad_heavy_inf_helm,itm_harad_bow,itm_harad_arrows,itm_harad_sabre,itm_harad_horse,],
      attr_tier_4,wp_tier_4,knows_common|knows_horse_archery_3|knows_riding_4|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_1,haradrim_face_1,haradrim_face_2],
["gold_serpent_horse_archer","Gold_Serpent_Horse_Archer","Gold_Serpent_Horse_Archers",tf_harad| tfg_ranged| tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,
   [itm_harad_leather_greaves,itm_black_snake_armor,itm_black_snake_helm,itm_harad_bow,itm_harad_arrows,itm_black_snake_sword,itm_harad_warhorse,],
      attr_tier_5,wp_tier_5,knows_common|knows_horse_archery_5|knows_riding_5|knows_power_strike_2|knows_ironflesh_3|knows_power_draw_3,haradrim_face_1,haradrim_face_2],
#FAR HARAD
["far_harad_tribesman","Far_Harad_Tribesman","Far_Harad_Tribesmen",tf_harad| tfg_armor| tfg_boots,0,0,fac_harad,
   [itm_far_harad_2h_mace,itm_harad_javelin,itm_harad_short_spear,],
      attr_tier_2,wp_tier_2,knows_common|knows_athletics_1,far_harad_face1,far_harad_face2],
["far_harad_champion","Far_Harad_Champion","Far_Harad_Champions",tf_harad| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,
   [itm_harad_champion,itm_far_harad_2h_mace,itm_harad_javelin,itm_harad_short_spear,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_power_throw_3|knows_ironflesh_1|knows_power_strike_2,far_harad_face1,far_harad_face2],
["far_harad_panther_guard","Panther_Guard","Panther_Guards",tf_harad| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_harad,
   [itm_panther_guard,itm_harad_pantherhelm,itm_harad_mace,itm_harad_javelin,itm_harad_long_shield_a,],
      attr_tier_5,wp_tier_5,knows_common|knows_power_throw_4|knows_power_strike_4|knows_ironflesh_3|knows_athletics_3,far_harad_face1,far_harad_face2],
["harad_items","BUG","_",tf_hero,0,0,fac_harad,
   [itm_short_bow,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
#Dunnish
["dunnish_wildman","Dunnish_Wildman","Dunnish_Wildmen",tf_dunland| tf_randomize_face| tfg_armor| tfg_boots,0,0,fac_dunland,
   [itm_dunland_wolfboots,itm_dunland_armor_a,itm_dunland_armor_b,itm_dunland_armor_c,itm_dunland_armor_d,itm_dunland_armor_e,itm_dunland_armor_g,itm_dunland_armor_h,itm_dunnish_axe,itm_dunland_spear,itm_wood_club,itm_dunland_javelin,],
      attr_tier_1,wp_tier_1,knows_common|knows_athletics_1|knows_power_throw_1,dunland_face1,dunland_face2],
["dunnish_warrior","Dunnish_Warrior","Dunnish_Warriors",tf_dunland| tf_randomize_face| tfg_armor| tfg_boots,0,0,fac_dunland,
   [itm_dunland_wolfboots,itm_dunland_armor_a,itm_dunland_armor_b,itm_dunland_armor_c,itm_dunland_armor_d,itm_dunland_armor_e,itm_dunland_armor_g,itm_dunland_armor_h,itm_dunnish_antler_axe,itm_dunnish_axe,itm_wood_club,itm_dunland_javelin,itm_dunland_javelin,],
      attr_tier_2,wp_tier_2,knows_common|knows_athletics_2|knows_shield_1|knows_power_strike_1|knows_power_throw_2,dunland_face1,dunland_face2],
["dunnish_pikeman","Dunnish_Pikeman","Dunnish_Pikemen",tf_dunland| tf_randomize_face| tfg_shield| tfg_armor| tfg_boots,0,0,fac_dunland,
   [itm_dunland_wolfboots,itm_leather_gloves,itm_dunland_armor_a,itm_dunland_armor_b,itm_dunland_armor_c,itm_dunland_armor_d,itm_dunland_armor_e,itm_dunland_armor_g,itm_dunland_armor_h,itm_gundabad_helm_a,itm_dun_helm_c,itm_dun_helm_e,itm_dunnish_pike,],
      attr_tier_3,wp_tier_4,knows_common|knows_athletics_2|knows_shield_2|knows_power_strike_2|knows_ironflesh_1,dunland_face1,dunland_face2],
["dunnish_veteran_pikeman","Dunnish_Veteran_Pikeman","Dunnish_Veteran_Pikemen",tf_dunland| tf_randomize_face| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dunland,
   [itm_dunland_wolfboots,itm_evil_gauntlets_b,itm_dunland_armor_i,itm_dunland_armor_j,itm_gundabad_helm_b,itm_dun_helm_c,itm_dun_helm_e,itm_dunnish_pike,],
      attr_tier_4,wp_tier_5,knows_common|knows_shield_3|knows_power_strike_3|knows_ironflesh_2|knows_athletics_3,dunland_face1,dunland_face2],
["dunnish_raven_rider","Dunnish_Raven_Rider","Dunnish_Raven_Riders",tf_dunland| tf_randomize_face| tf_mounted| tfg_armor| tfg_horse| tfg_boots| tfg_ranged,0,0,fac_dunland,
   [itm_dunland_wolfboots,itm_dunland_armor_a,itm_dunland_armor_b,itm_dunland_armor_c,itm_dunland_armor_d,itm_dunland_armor_e,itm_dunland_armor_g,itm_dunland_armor_h,itm_dunnish_antler_axe,itm_dunland_javelin,itm_dunland_javelin,itm_dun_shield_a,itm_dun_shield_b,itm_saddle_horse,],
      attr_tier_2,wp_tier_2,knows_common|knows_riding_2|knows_shield_1|knows_power_strike_1|knows_power_throw_2,dunland_face1,dunland_face2],
["dunnish_vet_warrior","Dunnish_Veteran_Warrior","Dunnish_Veteran_Warriors",tf_dunland| tf_randomize_face| tfg_shield| tfg_armor| tfg_boots,0,0,fac_dunland,
   [itm_dunland_wolfboots,itm_leather_gloves,itm_dunland_armor_a,itm_dunland_armor_b,itm_dunland_armor_c,itm_dunland_armor_d,itm_dunland_armor_e,itm_dunland_armor_g,itm_dunland_armor_h,itm_dunland_javelin,itm_dun_helm_b,itm_dunnish_axe,itm_dunnish_war_axe,itm_gundabad_helm_a,itm_dun_shield_a,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_shield_2|knows_power_strike_2|knows_ironflesh_1|knows_power_throw_2,dunland_face1,dunland_face2],
["dunnish_wolf_warrior","Dunnish_Wolf_Warrior","Dunnish_Wolf_Warriors",tf_dunland| tf_randomize_face| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dunland,
   [itm_dunland_wolfboots,itm_evil_gauntlets_b,itm_dunland_armor_i,itm_dunland_armor_j,itm_dunnish_axe,itm_dunnish_war_axe,itm_dunland_javelin,itm_dun_shield_a,itm_dun_helm_a,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_shield_3|knows_power_strike_3|knows_ironflesh_2|knows_power_throw_3,dunland_face1,dunland_face2],
["dunnish_wolf_guard","Dunnish_Wolf_Guard","Dunnish_Wolf_Guards",tf_dunland| tf_randomize_face| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dunland,
   [itm_dunland_wolfboots,itm_evil_gauntlets_b,itm_dunland_armor_i,itm_dunland_armor_j,itm_dun_helm_a,itm_dun_helm_b,itm_dun_shield_a,itm_dunnish_axe,itm_dunnish_war_axe,itm_dunland_javelin,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_shield_4|knows_power_strike_4|knows_ironflesh_3|knows_power_throw_5,dunland_face1,dunland_face2],
#unused
["dunnish_chieftan","Dunnish_Chieftain","Dunnish_Chieftains",tf_dunland| tf_randomize_face| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dunland,
   [itm_dunland_wolfboots,itm_evil_gauntlets_a,itm_dunland_armor_k,itm_dun_helm_d,itm_dun_berserker,itm_dun_shield_a,itm_dun_shield_b,],
      attr_tier_5,wp_tier_5,knows_athletics_5|knows_power_strike_4|knows_ironflesh_5,dunland_face1,dunland_face2],
["dunland_items","BUG","_",tf_hero,0,0,fac_dunland,
   [itm_sumpter_horse,itm_saddle_horse,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],

#Easterlings 
["easterling_youth","Variag_Bondsman","Variag_Bondsmen",tf_evil_man| tfg_armor| tfg_boots,0,0,fac_khand,
   [itm_khand_light,itm_leather_boots,itm_spear,itm_khand_mace1,],
      attr_tier_1,wp_tier_1,knows_common|knows_athletics_1,khand_man1,khand_man2],
["easterling_warrior","Warrior_of_Khand","Warriors_of_Khand",tf_evil_man| tfg_armor| tfg_boots,0,0,fac_khand,
   [itm_khand_light,itm_leather_boots,itm_khand_helmet_a2,itm_khand_voulge,itm_spear,itm_khand_tulwar,itm_khand_mace1,itm_tab_shield_small_round_b,],
      attr_tier_2,wp_tier_2,knows_common|knows_athletics_1|knows_shield_1|knows_power_strike_2,khand_man1,khand_man2],
["easterling_axeman","Variag_Axeman","Variag_Axemen",tf_evil_man| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,
   [itm_khand_foot_lam_c,itm_leather_boots,itm_khand_helmet_a2,itm_khand_axe_winged,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_shield_1|knows_power_strike_3|knows_ironflesh_1,khand_man1,khand_man2],
["easterling_veteran_axeman","Variag_Veteran_Axeman","Variag_Veteran_Axemen",tf_evil_man| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,
   [itm_khand_foot_lam_b,itm_variag_greaves,itm_khand_helmet_c3,itm_khand_helmet_c4,itm_khand_axe_winged,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_shield_2|knows_power_strike_4|knows_ironflesh_2,khand_man1,khand_man2],
["easterling_axe_master","Variag_Axe_Master","Variag_Axe_Masters",tf_evil_man| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,
   [itm_khand_foot_lam_a,itm_variag_greaves,itm_khand_helmet_c3,itm_khand_helmet_c4,itm_khand_axe_great,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_shield_2|knows_power_strike_5|knows_ironflesh_3,khand_man1,khand_man2],
["easterling_rider","Variag_Pony_Rider","Variag_Pony_Riders",tf_evil_man| tf_mounted| tfg_armor| tfg_horse| tfg_boots,0,0,fac_khand,
   [itm_khand_light_lam,itm_leather_boots,itm_variag_pony,itm_khand_tulwar,itm_khand_mace1,],
      attr_tier_2,wp_tier_2,knows_common|knows_riding_2|knows_shield_1|knows_power_strike_1,khand_man1,khand_man2],
["easterling_horseman","Variag_Horseman","Variag_Horsemen",tf_evil_man| tf_mounted| tfg_armor| tfg_horse| tfg_boots,0,0,fac_khand,
   [itm_khand_med_lam_b,itm_leather_boots,itm_variag_pony,itm_khand_helmet_a2,itm_khand_helmet_a3,itm_khand_helmet_b3,itm_khand_tulwar,itm_khand_mace1,itm_leather_gloves,itm_easterling_round_horseman,],
      attr_tier_3,wp_tier_3,knows_common|knows_riding_2|knows_shield_1|knows_power_strike_2,khand_man1,khand_man2],
["easterling_veteran_horseman","Variag_Heavy_Horseman","Variag_Heavy_Horsemen",tf_evil_man| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_khand,
   [itm_khand_med_lam_c,itm_variag_greaves,itm_variag_pony,itm_khand_helmet_a2,itm_khand_helmet_a3,itm_khand_helmet_b3,itm_khand_tulwar,itm_khand_mace1,itm_khand_mace2,itm_mail_mittens,itm_easterling_round_horseman,],
      attr_tier_4,wp_tier_4,knows_common|knows_riding_5|knows_shield_3|knows_power_strike_2|knows_ironflesh_2,khand_man1,khand_man2],
["easterling_horsemaster","Variag_Kataphrakt","Variag_Kataphrakts",tf_evil_man| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_khand,
   [itm_khand_med_lam_d,itm_variag_greaves,itm_variag_kataphrakt,itm_khand_helmet_a1,itm_khand_helmet_b4,itm_khand_helmet_d2,itm_khand_tulwar,itm_khand_lance,itm_mail_mittens,itm_easterling_round_horseman,],
      attr_tier_5,wp_tier_5,knows_common|knows_riding_5|knows_shield_3|knows_power_strike_4|knows_ironflesh_2,khand_man1,khand_man2],
["easterling_lance_kataphract","Variag_Lance_Kataphrakt","Variag_Lance_Kataphrakts",tf_evil_man| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_khand,
   [itm_khand_heavy_lam,itm_variag_greaves,itm_variag_kataphrakt,itm_khand_helmet_b2,itm_khand_helmet_d1,itm_khand_helmet_d3,itm_khand_lance,itm_mail_mittens,],
      attr_tier_5,wp_tier_5,knows_common|knows_riding_5|knows_shield_3|knows_power_strike_4|knows_ironflesh_2,khand_man1,khand_man2],
#Khand Variags
["khand_glaive_whirler","Khand_Blade_Whirler","Khand_Blade_Whirlers",tf_evil_man| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,
   [itm_khand_foot_lam_c,itm_leather_boots,itm_khand_helmet_e1,itm_khand_helmet_e4,itm_khand_helmet_e3,itm_khand_voulge,itm_leather_gloves,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_1|knows_power_strike_2|knows_ironflesh_1,khand_man1,khand_man2],
["variag_veteran_glaive_whirler","Khand_Veteran_Blade_Whirler","Khand_Veteran_Blade_Whirlers",tf_evil_man| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,
   [itm_khand_foot_lam_b,itm_leather_boots,itm_khand_helmet_e2,itm_khand_helmet_e3,itm_khand_voulge,itm_khand_halberd,itm_mail_mittens,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_power_strike_3|knows_ironflesh_1,khand_man1,khand_man2],
["khand_glaive_master","Khand_Halberd_Master","Khand_Halberd_Masters",tf_evil_man| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,
   [itm_khand_foot_lam_a,itm_variag_greaves,itm_khand_helmet_e2,itm_khand_halberd,itm_mail_mittens,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_power_throw_4|knows_power_strike_4|knows_ironflesh_2,khand_man1,khand_man2],
["variag_pitfighter","Variag_Pitfighter","Variag_Pitfighters",tf_evil_man| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,
   [itm_khand_light,itm_javelin,itm_leather_boots,itm_khand_helmet_mask1,itm_khand_helmet_mask2,itm_khand_tulwar,itm_khand_pitsword,itm_easterling_hawk_shield,itm_variag_gladiator_shield,itm_tab_shield_small_round_b,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_5|knows_power_throw_2|knows_power_strike_4|knows_ironflesh_4,khand_man1,khand_man2],
["variag_gladiator","Variag_Berserker","Variag_Berserkers",tf_evil_man| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,
   [itm_khand_light,itm_javelin,itm_leather_boots,itm_khand_helmet_mask1,itm_khand_helmet_mask2,itm_khand_2h_tulwar,itm_khand_tulwar,itm_khand_pitsword,itm_khand_mace_spiked,itm_khand_2h_tulwar,itm_easterling_hawk_shield,itm_tab_shield_small_round_b,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_6|knows_power_throw_3|knows_power_strike_5|knows_ironflesh_6,khand_man1,khand_man2],
["easterling_skirmisher","Variag_Skirmisher","Variag_Skirmishers",tf_evil_man| tfg_ranged| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_khand,
   [itm_khand_light_lam,itm_javelin,itm_leather_boots,itm_variag_pony,itm_khand_helmet_a2,itm_khand_tulwar,itm_khand_mace1,itm_khand_mace2,],
      attr_tier_3,wp_tier_3,knows_common|knows_horse_archery_2|knows_riding_2|knows_power_throw_2|knows_power_strike_1,khand_man1,khand_man2],
["easterling_veteran_skirmisher","Variag_Veteran_Skirmisher","Variag_Veteran_Skirmishers",tf_evil_man| tfg_ranged| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_khand,
   [itm_khand_med_lam_b,itm_javelin,itm_variag_greaves,itm_variag_pony,itm_khand_helmet_a2,itm_leather_gloves,itm_khand_tulwar,itm_khand_mace1,itm_khand_mace2,itm_easterling_round_horseman,],
      attr_tier_4,wp_tier_4,knows_common|knows_horse_archery_3|knows_riding_4|knows_shield_3|knows_power_throw_3|knows_power_strike_2|knows_ironflesh_2,khand_man1,khand_man2],
["easterling_elite_skirmisher","Variag_Heavy_Skirmisher","Variag_Heavy_Skirmishers",tf_evil_man| tfg_ranged| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_khand,
   [itm_khand_med_lam_c,itm_javelin,itm_variag_greaves,itm_variag_kataphrakt,itm_khand_helmet_a1,itm_leather_gloves,itm_khand_tulwar,itm_khand_mace1,itm_khand_mace2,itm_easterling_round_horseman,],
      attr_tier_5,wp_tier_5,knows_common|knows_horse_archery_4|knows_riding_5|knows_shield_2|knows_power_throw_4|knows_power_strike_3|knows_ironflesh_2,khand_man1,khand_man2],
["khand_items","BUG","_",tf_hero,0,0,fac_khand,
   [itm_leather_boots,itm_leather_gloves,itm_sumpter_horse,itm_saddle_horse,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
#Corsair
["corsair_youth","Umbar_Sailor","Umbar_Sailors",tfg_armor| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_a,itm_umb_armor_a1,itm_umb_shield_a,itm_umb_shield_b,itm_shortened_spear,itm_corsair_sword,itm_corsair_throwing_dagger,itm_umbar_rapier,],
      attr_tier_1,wp_tier_1,knows_common|knows_athletics_1|knows_power_throw_2,bandit_face1,bandit_face2],
["corsair_warrior","Umbar_Warrior","Umbar_Warriors",tfg_armor| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_b,itm_umb_hood,itm_umb_shield_b,itm_umb_shield_d,itm_shortened_spear,itm_corsair_sword,itm_corsair_harpoon,itm_umbar_rapier,],
      attr_tier_2,wp_tier_2,knows_common|knows_athletics_1|knows_shield_1|knows_power_strike_1,bandit_face1,bandit_face2],
["corsair_pikeman","Pikeman_of_Umbar","Pikemen_of_Umbar",tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_f,itm_umb_armor_h,itm_umb_helm_e,itm_umb_helm_f,itm_corsair_sword,itm_umbar_pike,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_shield_2|knows_power_strike_2|knows_ironflesh_1,bandit_face1,bandit_face2],
["corsair_veteran_raider","Corsair_Veteran_Raider","Corsair_Veteran_Raiders",tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_f,itm_umb_armor_h,itm_umb_helm_e,itm_umb_helm_f,itm_corsair_sword,itm_umbar_pike,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,bandit_face1,bandit_face2],
["corsair_night_raider","Corsair_Night_Raider","Corsair_Night_Raiders",tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_g,itm_umb_helm_a,itm_umb_helm_b,itm_kraken,itm_umbar_pike,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_shield_4|knows_power_strike_4|knows_ironflesh_3,bandit_face1,bandit_face2],
["militia_of_umbar","Umbar_Militiaman","Umbar_Militia",tfg_ranged| tfg_armor| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_b,itm_umb_hood,itm_umb_shield_a,itm_umb_shield_e,itm_corsair_bow,itm_corsair_arrows,itm_umbar_cutlass,itm_corsair_throwing_dagger,],
      attr_tier_2,wp_tier_2,knows_common|knows_power_draw_1|knows_ironflesh_1,bandit_face1,bandit_face2],
["marksman_of_umbar","Skirmisher_of_Umbar","Skirmishers_of_Umbar",tfg_ranged| tfg_armor| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_c,itm_umb_armor_e,itm_umb_helm_c,itm_umb_helm_d,itm_corsair_bow,itm_corsair_arrows,itm_umbar_cutlass,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_1|knows_power_draw_2|knows_ironflesh_1,bandit_face1,bandit_face2],
["veteran_marksman_of_umbar","Veteran_Skirmisher_of_Umbar","Veteran_Skirmishers_of_Umbar",tfg_ranged| tfg_armor| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_c,itm_umb_armor_e,itm_umb_helm_c,itm_umb_helm_d,itm_corsair_bow,itm_corsair_arrows,itm_umbar_cutlass,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_power_draw_3|knows_ironflesh_1,bandit_face1,bandit_face2],
["master_marksman_of_umbar","Corsair_Master_Skirmisher","Corsair_Master_Skirmishers",tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_d,itm_umb_helm_c,itm_umb_helm_d,itm_umb_shield_a,itm_corsair_bow,itm_corsair_arrows,itm_umbar_cutlass,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_power_draw_4|knows_ironflesh_2,bandit_face1,bandit_face2],
["corsair_marauder","Swordsman_of_Umbar","Swordsmen_of_Umbar",tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_f,itm_umb_armor_h,itm_umb_helm_e,itm_umb_helm_f,itm_umb_shield_b,itm_umb_shield_d,itm_umbar_cutlass,itm_umbar_rapier,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_1|knows_shield_2|knows_power_strike_2,bandit_face1,bandit_face2],
["corsair_veteran_marauder","Veteran_Swordsman_of_Umbar","Veteran_Swordsmen_of_Umbar",tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_f,itm_umb_armor_h,itm_umb_helm_e,itm_umb_helm_f,itm_umb_shield_b,itm_umb_shield_d,itm_umbar_cutlass,itm_umbar_rapier,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_2|knows_shield_2|knows_power_throw_1|knows_power_strike_3,bandit_face1,bandit_face2],
["corsair_elite_marauder","Corsair_Swordmaster","Corsair_Swordmasters",tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_g,itm_umb_helm_a,itm_umb_helm_b,itm_umb_shield_c,itm_kraken,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_shield_2|knows_power_throw_2|knows_power_strike_6|knows_ironflesh_3,bandit_face1,bandit_face2],
["assassin_of_umbar","Assassin_of_Umbar","Assassins_of_Umbar",tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_f,itm_umb_armor_d,itm_umb_helm_b,itm_umb_shield_b,itm_corsair_bow,itm_corsair_arrows,itm_umbar_cutlass,itm_kraken,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_4|knows_power_throw_2|knows_power_draw_2|knows_power_strike_3|knows_ironflesh_3,bandit_face1,bandit_face2],
["master_assassin_of_umbar","Corsair_Assassin","Corsair_Assassins",tfg_ranged| tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_d,itm_umb_helm_d,itm_umb_helm_c,itm_corsair_bow,itm_corsair_arrows,itm_corsair_sword,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_5|knows_power_draw_3|knows_power_strike_4|knows_ironflesh_4,bandit_face1,bandit_face2],
["pikeman_of_umbar","Pikeman_of_Umbar","Pikemen_of_Umbar",tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_b,itm_umb_armor_c,itm_umb_helm_c,itm_umbar_pike,itm_umb_shield_a,itm_umb_shield_b,itm_umb_shield_d,],
      attr_tier_3,wp_tier_3,knows_common|knows_athletics_2|knows_shield_2|knows_power_strike_3|knows_ironflesh_2,bandit_face1,bandit_face2],
["veteran_pikeman_of_umbar","Veteran_Pikeman_of_Umbar","Veteran_Pikemen_of_Umbar",tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_c,itm_umb_armor_d,itm_umb_helm_a,itm_umbar_pike,itm_umb_shield_a,itm_umb_shield_b,],
      attr_tier_4,wp_tier_4,knows_common|knows_athletics_3|knows_shield_3|knows_power_strike_3|knows_ironflesh_2,bandit_face1,bandit_face2],
["pike_master_of_umbar","Corsair_Pike_Master","Corsair_Pike_Masters",tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_umbar,
   [itm_corsair_boots,itm_umb_armor_f,itm_umb_armor_g,itm_umb_helm_a,itm_umbar_pike,itm_umb_shield_a,itm_umb_shield_b,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_3|knows_shield_4|knows_power_strike_4|knows_ironflesh_3,bandit_face1,bandit_face2],
["umbar_items","BUG","_",tf_hero,0,0,fac_umbar,
   [itm_leather_boots,itm_leather_gloves,itm_short_bow,itm_sumpter_horse,itm_saddle_horse,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
#Isengard
["orc_snaga_of_isengard","Orc_Snaga_of_Isengard","Orc_Snagas_of_Isengard",tf_orc| tf_no_capture_alive,0,0,fac_isengard,
   [itm_isen_orc_armor_a,itm_isen_orc_armor_b,itm_isengard_hammer,itm_isengard_spear,itm_isengard_spear,itm_orc_club_a,itm_orc_club_b,itm_orc_club_c,itm_orc_club_d,itm_orc_simple_spear,itm_orc_axe,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      attr_orc_tier_1,wp_orc_tier_1,knows_athletics_3|knows_power_throw_1|knows_power_strike_1,orc_face1,orc_face2],
["orc_of_isengard","Orc_of_Isengard","Orcs_of_Isengard",tf_orc| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_orc_ragwrap,itm_isen_orc_armor_c,itm_isen_orc_armor_d,itm_isen_orc_helm_a,itm_isen_orc_helm_b,itm_isen_orc_shield_a,itm_orc_slasher,itm_orc_falchion,itm_orc_scimitar,itm_orc_sabre,itm_orc_machete,itm_isengard_sword,itm_isengard_hammer,itm_isengard_spear,itm_isengard_spear,itm_orc_club_a,itm_orc_club_b,itm_orc_club_c,itm_orc_club_d,itm_orc_simple_spear,itm_orc_bill,itm_orc_bill,itm_orc_axe,],
      attr_orc_tier_2,wp_orc_tier_2,knows_athletics_4|knows_power_throw_2|knows_power_strike_3,orc_face2,orc_face3],
["large_orc_of_isengard","Large_Orc_of_Isengard","Large_Orcs_of_Isengard",tf_orc| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_orc_ragwrap,itm_evil_gauntlets_b,itm_isen_orc_armor_e,itm_isen_orc_armor_f,itm_isen_orc_helm_b,itm_leather_gloves,itm_isen_orc_shield_a,itm_isen_orc_shield_b,itm_orc_slasher,itm_orc_falchion,itm_orc_scimitar,itm_orc_sabre,itm_orc_machete,itm_isengard_sword,itm_isengard_hammer,itm_isengard_spear,itm_isengard_spear,itm_orc_club_a,itm_orc_club_b,itm_orc_simple_spear,itm_orc_club_d,itm_orc_bill,itm_orc_axe,],
      attr_orc_tier_3,wp_orc_tier_3,knows_athletics_5|knows_power_throw_2|knows_power_strike_4,orc_face4,orc_face5],
["fell_orc_of_isengard","Fell_Orc_of_Isengard","Fell_Orcs_of_Isengard",tf_orc| tfg_armor| tfg_helm| tfg_boots| tfg_gloves| tf_no_capture_alive,0,0,fac_isengard,
   [itm_orc_greaves,itm_evil_gauntlets_b,itm_isen_orc_armor_g,itm_isen_orc_helm_c,itm_isen_orc_shield_a,itm_isen_orc_shield_b,itm_orc_slasher,itm_orc_falchion,itm_orc_scimitar,itm_orc_sabre,itm_orc_machete,itm_isengard_sword,itm_isengard_hammer,itm_isengard_spear,itm_isengard_spear,itm_orc_club_a,itm_orc_club_b,itm_orc_club_c,itm_orc_club_d,itm_orc_simple_spear,itm_orc_bill,itm_orc_bill,itm_orc_axe,],
      attr_orc_tier_4,wp_orc_tier_4,knows_athletics_6|knows_power_throw_3|knows_power_strike_4,orc_face6,orc_face7],
["large_orc_despoiler","Large_Orc_Despoiler","Large_Orc_Despoilers",tf_orc| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_orc_greaves,itm_evil_gauntlets_b,itm_isen_orc_armor_e,itm_isen_orc_armor_f,itm_isen_orc_helm_b,itm_isengard_mallet,itm_orc_sledgehammer,itm_isengard_hammer,itm_orc_club_a,itm_orc_club_b,itm_orc_club_c,itm_orc_club_d,],
      attr_orc_tier_3,wp_orc_tier_3,knows_athletics_6|knows_power_strike_4,orc_face8,orc_face9],
["fell_orc_despoiler","Fell_Orc_Despoiler","Fell_Orc_Despoilers",tf_orc| tfg_armor| tfg_helm| tfg_boots| tfg_gloves| tf_no_capture_alive,0,0,fac_isengard,
   [itm_orc_greaves,itm_evil_gauntlets_b,itm_isen_orc_armor_g,itm_isen_orc_helm_c,itm_isengard_mallet,itm_orc_sledgehammer,itm_isengard_hammer,itm_orc_club_a,itm_orc_club_b,itm_orc_club_c,itm_orc_club_d,],
      attr_orc_tier_4,wp_orc_tier_4,knows_athletics_7|knows_power_strike_5,orc_face3,orc_face6],
["wolf_rider_of_isengard","Wolf_Rider_of_Isengard","Wolf_Riders_of_Isengard",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_horse| tf_no_capture_alive,0,0,fac_isengard,
   [itm_orc_throwing_arrow,itm_isen_orc_armor_a,itm_isen_orc_armor_b,itm_warg_1d,itm_warg_1b,itm_warg_1c,itm_orc_club_a,itm_orc_club_b,itm_orc_club_c,itm_orc_club_d,itm_orc_axe,],
      attr_orc_tier_2,wp_orc_tier_2,knows_riding_3|knows_power_throw_2|knows_power_strike_2|knows_horse_archery_2,orc_face7,orc_face4],
["warg_rider_of_isengard","Warg_Rider_of_Isengard","Warg_Riders_of_Isengard",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_horse| tf_no_capture_alive,0,0,fac_isengard,
   [itm_uruk_ragwrap,itm_orc_throwing_arrow,itm_isen_orc_armor_a,itm_isen_orc_armor_b,itm_wargarmored_1b,itm_warg_1c,itm_warg_1b,itm_wargarmored_2c,itm_orc_scimitar,itm_orc_machete,],
      attr_orc_tier_3,wp_orc_tier_3,knows_riding_3|knows_power_throw_3|knows_power_strike_3|knows_horse_archery_4,orc_face5,orc_face8],
["white_hand_rider","White_Hand_Rider","White_Hand_Riders",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_uruk_ragwrap,itm_orc_throwing_arrow,itm_isen_orc_armor_a,itm_isen_orc_armor_b,itm_wargarmored_1b,itm_wargarmored_1c,itm_wargarmored_2b,itm_wargarmored_2c,itm_orc_scimitar,itm_orc_falchion,itm_orc_sabre,],
      attr_orc_tier_4,wp_orc_tier_4,knows_riding_5|knows_power_throw_5|knows_power_strike_4|knows_horse_archery_5,orc_face7,orc_face8],

# "ghost" warg riders: (invisible riders for lone wargs) number and order match warg items
["warg_ghost_1b","Warg","Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_warg_1b],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face7,orc_face2],
["warg_ghost_1c","Warg","Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_warg_1c],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face6,orc_face1],
["warg_ghost_1d","Warg","Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_warg_1d],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face1,orc_face2],
["warg_ghost_a1b","Warg","Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_wargarmored_1b],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face1,orc_face2],
["warg_ghost_a1c","Armored Warg","Armored Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_wargarmored_1c],
     str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face1,orc_face2],
["warg_ghost_a2b","Armored Warg","Armored Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_wargarmored_2b],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face1,orc_face2],
["warg_ghost_a2c","Armored Warg","Armored Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_wargarmored_2c],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face1,orc_face2],
["warg_ghost_a3a","Armored Warg","Armored Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_wargarmored_3a],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face1,orc_face2],
["warg_ghost_h","Huge Warg","Huge Wargs",tf_orc| tfg_gloves| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_warg_ghost_lance,itm_warg_ghost_armour,itm_empty_legs,itm_empty_hands,itm_empty_head,itm_warg_reward],
      str_30| agi_7| int_4| cha_4|level(9),wp_orc_tier_2,knows_riding_10|knows_ironflesh_10|knows_power_strike_2,orc_face1,orc_face2],

	  
#Isengard
# first non ghost-warg
["uruk_hai_tracker","Uruk_Hai_Tracker","Uruk_Hai_Trackers",tf_urukhai| tf_mounted| tfg_ranged| tfg_armor| tf_no_capture_alive,0,0,fac_isengard,
   [itm_uruk_ragwrap,itm_isen_uruk_heavy_d,itm_isengard_large_bow,itm_isengard_arrow,itm_isengard_axe,],
      attr_tier_2,wp_tier_2,knows_athletics_3|knows_power_draw_2|knows_power_strike_1,uruk_hai_face1,uruk_hai_face2],
["large_uruk_hai_tracker","Large_Uruk_Hai_Tracker","Large_Uruk_Hai_Trackers",tf_urukhai| tf_mounted| tfg_ranged| tfg_armor| tfg_boots| tfg_helm| tf_no_capture_alive,0,0,fac_isengard,
   [itm_uruk_tracker_boots,itm_isen_uruk_helm_e,itm_isen_uruk_heavy_d,itm_isen_uruk_heavy_e,itm_isengard_large_bow,itm_isengard_arrow,itm_isengard_axe,],
      attr_tier_3,wp_tier_3,knows_athletics_4|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_2,uruk_hai_face1,uruk_hai_face2],
["fighting_uruk_hai_tracker","Fighting_Uruk_Hai_Tracker","Fighting_Uruk_Hai_Trackers",tf_urukhai| tf_mounted| tfg_ranged| tfg_armor| tfg_boots| tfg_helm| tf_no_capture_alive,0,0,fac_isengard,
   [itm_uruk_tracker_boots,itm_isen_uruk_helm_f,itm_isen_uruk_heavy_e,itm_isengard_large_bow,itm_isengard_arrow,itm_isengard_sword,],
      attr_tier_4,wp_tier_4,knows_athletics_4|knows_power_draw_4|knows_power_strike_2|knows_ironflesh_5,uruk_hai_face1,uruk_hai_face2],
["fighting_uruk_hai_berserker","Fighting_Uruk_Hai_Berserker","Fighting_Uruk_Hai_Berserkers",tf_urukhai| tf_mounted| tfg_helm| tf_no_capture_alive,0,0,fac_isengard,
   [itm_uruk_chain_greaves,itm_isen_uruk_helm_f,itm_isen_uruk_helm_e,itm_evil_gauntlets_a,itm_isen_uruk_light_a,itm_isen_uruk_light_b,itm_isengard_heavy_axe,itm_isengard_mallet,itm_isengard_sword,itm_isengard_halberd,itm_isengard_heavy_sword,],
      attr_tier_6,wp_tier_6,knows_athletics_7|knows_power_strike_6|knows_ironflesh_10,uruk_hai_face1,uruk_hai_face2],
["uruk_snaga_of_isengard","Uruk_Hai_Newborn","Uruk_Hai_Newborns",tf_urukhai| tf_mounted| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_uruk_ragwrap,itm_isen_uruk_light_a,itm_isengard_axe,itm_isengard_sword,],
      attr_tier_1,wp_tier_1,knows_athletics_1|knows_power_strike_1|knows_ironflesh_2,uruk_hai_face1,uruk_hai_face2],
["uruk_hai_of_isengard","Uruk_Hai_of_Isengard","Uruk_Hai_of_Isengard",tf_urukhai| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_uruk_ragwrap,itm_isen_uruk_helm_a,itm_isen_uruk_light_a,itm_isengard_axe,itm_isengard_spear,itm_isengard_sword,],
      attr_tier_2,wp_tier_2,knows_athletics_2|knows_power_strike_2|knows_ironflesh_3,uruk_hai_face1,uruk_hai_face2],
["large_uruk_hai_of_isengard","Large_Uruk_Hai_of_Isengard","Large_Uruk_Hai_of_Isengard",tf_urukhai| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_uruk_chain_greaves,itm_evil_gauntlets_b,itm_isen_uruk_helm_b,itm_isen_uruk_heavy_a,itm_isengard_spear,itm_isengard_heavy_axe,itm_isengard_sword,],
      attr_tier_3,wp_tier_3,knows_athletics_3|knows_power_strike_3|knows_ironflesh_4,uruk_hai_face1,uruk_hai_face2],
["fighting_uruk_hai_warrior","Fighting_Uruk_Hai_Warrior","Fighting_Uruk_Hai_Warriors",tf_urukhai|tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_isen_uruk_helm_c,itm_isen_uruk_heavy_c,itm_isengard_heavy_axe,itm_isengard_heavy_sword,itm_isen_uruk_shield_b,],
      attr_tier_4,wp_tier_4,knows_athletics_5|knows_power_strike_5|knows_ironflesh_5,uruk_hai_face1,uruk_hai_face2],
["fighting_uruk_hai_champion","Fighting_Uruk_Hai_Champion","Fighting_Uruk_Hai_Champions",tf_urukhai|tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_isen_uruk_helm_c,itm_isen_uruk_heavy_c,itm_isengard_axe,itm_isen_uruk_shield_b,itm_isengard_hammer,itm_isengard_mallet,itm_isengard_heavy_sword,],
      attr_tier_5,wp_tier_5,knows_athletics_6|knows_power_strike_6|knows_ironflesh_6,uruk_hai_face1,uruk_hai_face2],
["uruk_hai_pikeman","Uruk_Hai_Pikeman","Uruk_Hai_Pikemen",tf_urukhai| tf_mounted|tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_uruk_chain_greaves,itm_evil_gauntlets_b,itm_isen_uruk_helm_b,itm_isen_uruk_light_a,itm_isen_uruk_heavy_a,itm_isengard_pike,],
      attr_tier_3,wp_tier_3,knows_athletics_3|knows_power_strike_3|knows_ironflesh_4,uruk_hai_face1,uruk_hai_face2],
["fighting_uruk_hai_pikeman","Fighting_Uruk_Hai_Pikeman","Fighting_Uruk_Hai_Pikemen",tf_urukhai|tf_mounted| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_isen_uruk_helm_c,itm_isen_uruk_light_d,itm_isengard_pike,itm_isengard_halberd,],
      attr_tier_4,wp_tier_4,knows_athletics_5|knows_power_strike_5|knows_ironflesh_5,uruk_hai_face1,uruk_hai_face2],
["urukhai_standard_bearer","Uruk_Hai_Standard_Bearer","Uruk_Hai_Standard_Bearers",tf_urukhai|tf_mounted| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_isen_uruk_helm_c,itm_isen_uruk_heavy_c,itm_isengard_banner,],
      attr_tier_5,wp_tier_5,knows_athletics_2|knows_power_strike_5|knows_ironflesh_10,uruk_hai_face1,uruk_hai_face2],
#Mordor Uruks
["uruk_snaga_of_mordor","Uruk_Snaga_of_Mordor","Uruk_Snagas_of_Mordor",tf_uruk| tf_no_capture_alive,0,0,fac_mordor,
   [itm_uruk_ragwrap,itm_m_uruk_light_a,itm_m_uruk_light_b,itm_orc_axe,itm_orc_falchion,itm_orc_sabre,itm_orc_simple_spear,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      attr_tier_1,wp_tier_1,knows_athletics_3|knows_power_strike_1|knows_ironflesh_2,uruk_hai_face1,uruk_hai_face2],
["uruk_of_mordor","Uruk_of_Mordor","Uruks_of_Mordor",tf_uruk| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_uruk_ragwrap,itm_m_uruk_heavy_c,itm_m_uruk_heavy_d,itm_uruk_falchion_a,itm_uruk_falchion_b,itm_uruk_spear,itm_mordor_uruk_shield_a,itm_uruk_helm_a,itm_uruk_helm_b,itm_orc_coif,],
      attr_tier_2,wp_tier_2,knows_athletics_4|knows_power_strike_2|knows_ironflesh_3,uruk_hai_face1,uruk_hai_face2],
["large_uruk_of_mordor","Large_Uruk_of_Mordor","Large_Uruks_of_Mordor",tf_uruk| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_uruk_ragwrap,itm_uruk_greaves,itm_leather_gloves,itm_m_uruk_heavy_e,itm_m_uruk_heavy_f,itm_m_uruk_heavy_g,itm_uruk_falchion_a,itm_uruk_falchion_b,itm_uruk_skull_spear,itm_mordor_uruk_shield_a,itm_mordor_uruk_shield_b,itm_uruk_helm_c,itm_uruk_helm_d,],
      attr_tier_3,wp_tier_3,knows_athletics_4|knows_power_strike_3|knows_ironflesh_4,uruk_hai_face1,uruk_hai_face2],
["fell_uruk_of_mordor","Fell_Uruk_of_Mordor","Fell_Uruks_of_Mordor",tf_uruk| tfg_shield| tfg_ranged|tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_uruk_greaves,itm_uruk_chain_greaves,itm_evil_gauntlets_b,itm_orc_throwing_arrow,itm_uruk_bow,itm_orc_hook_arrow,itm_m_uruk_heavy_h,itm_m_uruk_heavy_i,itm_uruk_falchion_a,itm_uruk_falchion_b,itm_uruk_skull_spear,itm_mordor_uruk_shield_a,itm_mordor_uruk_shield_b,itm_uruk_helm_b,itm_uruk_helm_c,itm_uruk_helm_d,],
      attr_tier_4,wp_tier_4,knows_athletics_6|knows_power_strike_5|knows_power_draw_4|knows_power_throw_3|knows_ironflesh_4|knows_shield_2,uruk_hai_face1,uruk_hai_face2],
["uruk_slayer_of_mordor","Uruk_Slayer_of_Mordor","Uruk_Slayers_of_Mordor",tf_uruk| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_uruk_tracker_boots,itm_m_uruk_heavy_e,itm_m_uruk_heavy_f,itm_m_uruk_heavy_g,itm_uruk_falchion_a,itm_uruk_falchion_b,itm_uruk_voulge,itm_uruk_helm_b,itm_uruk_helm_c,itm_uruk_helm_d,],
      attr_tier_3,wp_tier_3,knows_riding_1|knows_athletics_6|knows_power_strike_5|knows_ironflesh_6,uruk_hai_face1,uruk_hai_face2],
["fell_uruk_slayer_of_mordor","Fell_Uruk_Slayer_of_Mordor","Fell_Uruk_Slayers_of_Mordor",tf_uruk| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_uruk_greaves,itm_uruk_chain_greaves,itm_evil_gauntlets_b,itm_m_uruk_heavy_h,itm_m_uruk_heavy_i,itm_uruk_falchion_a,itm_uruk_falchion_b,itm_uruk_voulge,itm_uruk_helm_c,itm_uruk_helm_f,],
      attr_tier_4,wp_tier_4,knows_riding_1|knows_athletics_7|knows_power_strike_7|knows_ironflesh_7,uruk_hai_face1,uruk_hai_face2],
["black_uruk_of_barad_dur","Black_Uruk_of_Barad_Dur","Black_Uruks_of_Barad_Dur",tf_uruk| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_m_uruk_heavy_j,itm_m_uruk_heavy_k,itm_uruk_heavy_axe,itm_uruk_falchion_a,itm_uruk_falchion_b,itm_mordor_uruk_shield_c,itm_uruk_helm_e,],
      attr_tier_5,wp_tier_5,knows_athletics_6|knows_power_strike_5|knows_ironflesh_5,uruk_hai_face1,uruk_hai_face2],
["uruk_mordor_standard_bearer","Mordor_Standard_Bearer","Mordor_Standard_Bearers",tf_uruk| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_uruk_greaves,itm_uruk_chain_greaves,itm_evil_gauntlets_b,itm_m_uruk_heavy_h,itm_m_uruk_heavy_i,itm_mordor_banner,itm_uruk_helm_b,itm_uruk_helm_c,itm_uruk_helm_d,],
      attr_tier_5,wp_tier_5,knows_athletics_6|knows_power_strike_5|knows_ironflesh_10,uruk_hai_face1,uruk_hai_face2],
#Trolls  & ents
["troll_of_moria","Troll_of_Moria","Trolls_of_Moria",tf_troll| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_moria,
   [itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_a,itm_tree_trunk_club_b,itm_tree_trunk_club_b,itm_troll_feet_boots,itm_troll_head_helm,itm_troll_head_helm_b,itm_troll_head_helm_c,],
      str_255| agi_3| int_3| cha_3|level(58),wp(75),knows_power_strike_10|knows_ironflesh_10,troll_face1,troll_face2],
["armoured_troll","Armored_Troll","Armored_Trolls",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_isengard,
   [itm_giant_mace,itm_giant_mace_b,itm_giant_hammer,itm_olog_feet_boots,itm_olog_body,itm_olog_body_b,itm_olog_head_helm,itm_olog_head_helm_b,itm_olog_head_helm_c,itm_olog_hands,],
      str_255| agi_3| int_3| cha_3|level(61),wp(100),knows_power_strike_10|knows_ironflesh_10,troll_face1,troll_face2],
["olog_hai","Olog_Hai_of_Mordor","Olog_Hai_of_Mordor",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_mordor,
   [itm_giant_mace,itm_giant_mace_b,itm_giant_hammer,itm_olog_feet_boots,itm_olog_body,itm_olog_body_b,itm_olog_head_helm,itm_olog_head_helm_b,itm_olog_head_helm_c,itm_olog_hands,],
      str_255| agi_3| int_3| cha_3|level(61),wp(100),knows_power_strike_10|knows_ironflesh_10,troll_face1,troll_face2],
["ent","Ent","Ents",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive,0,0,fac_commoners,
   [itm_tree_trunk_invis,itm_ent_body,itm_ent_hands,itm_ent_feet_boots,itm_ent_head_helm,itm_ent_water,itm_ent_head_helm2,itm_ent_head_helm3,],
      str_255| agi_3| int_3| cha_3|level(63),wp(200),knows_power_strike_10|knows_ironflesh_10,troll_face1,troll_face2],
# Dol Guldur Orcs (duplicates of Mordor orcs!)
["orc_snaga_of_guldur","Orc_Snaga_of_Guldur","Orc_Snagas_of_Guldur",tf_orc| tf_no_capture_alive,0,0,fac_guldur,
   [itm_m_orc_light_a,itm_m_orc_light_b,itm_m_orc_light_c,itm_orc_club_a,itm_orc_club_b,itm_orc_club_c,itm_orc_club_d,itm_orc_machete,itm_orc_simple_spear,itm_orc_axe,itm_orc_helm_a,itm_orc_helm_b,itm_orc_helm_c,itm_orc_helm_d,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      attr_orc_tier_1,wp_orc_tier_1,knows_athletics_3|knows_power_strike_1,orc_face5,orc_face4],
["orc_of_guldur","Orc_of_Guldur","Orcs_of_Guldur",tf_orc| tfg_armor| tf_no_capture_alive,0,0,fac_guldur,
   [itm_orc_ragwrap,itm_m_orc_light_b,itm_m_orc_light_c,itm_m_orc_light_d,itm_m_orc_light_e,itm_orc_club_a,itm_orc_falchion,itm_orc_club_c,itm_orc_sabre,itm_orc_slasher,itm_orc_bill,itm_orc_axe,itm_mordor_orc_shield_b,itm_mordor_orc_shield_c,itm_mordor_orc_shield_d,itm_mordor_orc_shield_a,itm_orc_helm_b,itm_orc_helm_c,itm_orc_helm_d,itm_orc_helm_e,],
      attr_orc_tier_2,wp_orc_tier_2,knows_athletics_4|knows_power_strike_2,orc_face3,orc_face8],
#Mordor Orcs
["orc_snaga_of_mordor","Orc_Snaga_of_Mordor","Orc_Snagas_of_Mordor",tf_orc| tf_no_capture_alive,0,0,fac_mordor,
   [itm_orc_ragwrap,itm_m_orc_light_a,itm_m_orc_light_b,itm_m_orc_light_c,itm_orc_club_a,itm_orc_club_b,itm_orc_club_c,itm_orc_club_d,itm_orc_machete,itm_orc_simple_spear,itm_orc_axe,itm_orc_helm_a,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      attr_orc_tier_1,wp_orc_tier_1,knows_athletics_3|knows_power_strike_1,orc_face1,orc_face2],
["orc_of_mordor","Orc_of_Mordor","Orcs_of_Mordor",tf_orc| tfg_armor| tf_no_capture_alive,0,0,fac_mordor,
   [itm_orc_ragwrap,itm_m_orc_light_b,itm_m_orc_light_c,itm_m_orc_light_d,itm_m_orc_light_e,itm_orc_club_a,itm_orc_falchion,itm_orc_skull_spear,itm_orc_sabre,itm_orc_slasher,itm_orc_bill,itm_orc_axe,itm_mordor_orc_shield_b,itm_mordor_orc_shield_c,itm_mordor_orc_shield_d,itm_mordor_orc_shield_a,itm_orc_helm_b,itm_orc_helm_c,itm_orc_helm_d,itm_orc_helm_e,],
      attr_orc_tier_2,wp_orc_tier_2,knows_athletics_4|knows_power_strike_2,orc_face7,orc_face8],
["large_orc_of_mordor","Large_Orc_of_Mordor","Large_Orcs_of_Mordor",tf_orc| tfg_shield| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_orc_greaves,itm_m_orc_light_d,itm_m_orc_light_e,itm_m_orc_heavy_a,itm_m_orc_heavy_b,itm_orc_sabre,itm_orc_falchion,itm_orc_two_handed_axe,itm_orc_skull_spear,itm_orc_slasher,itm_orc_bill,itm_orc_axe,itm_mordor_orc_shield_b,itm_mordor_orc_shield_c,itm_orc_throwing_axes,itm_mordor_orc_shield_d,itm_orc_helm_d,itm_orc_helm_e,itm_orc_helm_f,itm_orc_helm_g,itm_orc_helm_i,],
      attr_orc_tier_3,wp_orc_tier_3,knows_athletics_5|knows_power_strike_3|knows_power_throw_3,orc_face3,orc_face6],
["fell_orc_of_mordor","Fell_Orc_of_Mordor","Fell_Orcs_of_Mordor",tf_orc| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_orc_greaves,itm_evil_gauntlets_a,itm_orc_throwing_axes,itm_m_orc_heavy_b,itm_m_orc_heavy_c,itm_m_orc_heavy_d,itm_m_orc_heavy_e,itm_orc_sabre,itm_orc_falchion,itm_orc_two_handed_axe,itm_orc_scimitar,itm_orc_slasher,itm_orc_bill,itm_mordor_orc_shield_b,itm_mordor_orc_shield_c,itm_mordor_orc_shield_d,itm_mordor_orc_shield_e,itm_orc_helm_h,itm_orc_helm_i,itm_orc_helm_j,itm_orc_helm_k,],
      attr_orc_tier_4,wp_orc_tier_4,knows_athletics_6|knows_power_strike_4|knows_power_throw_4,orc_face7,orc_face4],
["warg_rider_of_gorgoroth","Warg_Rider_of_Gorgoroth","Warg_Riders_of_Gorgoroth",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_horse| tf_no_capture_alive,0,0,fac_mordor,
   [itm_m_orc_light_a,itm_m_orc_light_b,itm_m_orc_light_c,itm_orc_throwing_arrow,itm_orc_falchion,itm_orc_sabre,itm_orc_machete,itm_orc_machete,itm_wargarmored_1b,itm_warg_1b,itm_warg_1d,itm_warg_1c,],
      attr_orc_tier_3,wp_orc_tier_3,knows_horse_archery_3|knows_riding_4|knows_power_throw_3|knows_power_strike_4,orc_face5,orc_face8],
["great_warg_rider_of_mordor","Great_Warg_Rider_of_Udun","Great_Warg_Riders_of_Udun",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_horse| tf_no_capture_alive,0,0,fac_mordor,
   [itm_orc_ragwrap,itm_leather_gloves,itm_m_orc_light_b,itm_m_orc_light_c,itm_m_orc_light_d,itm_m_orc_light_e,itm_orc_throwing_arrow,itm_orc_falchion,itm_orc_sabre,itm_orc_machete,itm_orc_slasher,itm_wargarmored_2b,itm_wargarmored_2c,itm_wargarmored_3a,itm_wargarmored_2b,],
      attr_orc_tier_4,wp_orc_tier_4,knows_riding_5|knows_horse_archery_4|knows_power_throw_4|knows_power_strike_4,orc_face7,orc_face8],
["morgul_orc","Morgul_Orc","Morgul_Orcs",tf_orc| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_orc_ragwrap,itm_m_orc_light_b,itm_m_orc_light_c,itm_m_orc_light_d,itm_m_orc_light_e,itm_orc_club_a,itm_orc_falchion,itm_orc_club_c,itm_orc_sabre,itm_orc_slasher,itm_orc_bill,itm_orc_axe,itm_mordor_orc_shield_b,itm_mordor_orc_shield_c,itm_mordor_orc_shield_d,itm_orc_helm_b,itm_orc_helm_c,itm_orc_helm_d,itm_orc_helm_e,],
      attr_orc_tier_2,wp_orc_tier_2,knows_athletics_5|knows_power_strike_3,orc_face5,orc_face4],
["fell_morgul_orc","Fell_Morgul_Orc","Fell_Morgul_Orcs",tf_orc| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_orc_ragwrap,itm_leather_gloves,itm_orc_throwing_axes,itm_m_orc_heavy_b,itm_m_orc_heavy_c,itm_m_orc_heavy_d,itm_m_orc_heavy_e,itm_orc_sabre,itm_orc_falchion,itm_orc_two_handed_axe,itm_orc_scimitar,itm_orc_slasher,itm_orc_bill,itm_mordor_orc_shield_b,itm_mordor_orc_shield_c,itm_mordor_orc_shield_d,itm_mordor_orc_shield_e,itm_orc_helm_g,itm_orc_helm_h,itm_orc_helm_i,itm_orc_helm_j,itm_orc_helm_k,],
      attr_orc_tier_4,wp_orc_tier_4,knows_athletics_6|knows_shield_1|knows_power_strike_4,orc_face5,orc_face4],
["orc_tracker_of_mordor","Orc_Tracker_of_Mordor","Orc_Trackers_of_Mordor",tf_orc| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_orc_ragwrap,itm_leather_gloves,itm_m_orc_light_b,itm_m_orc_light_c,itm_orc_bow,itm_orc_hook_arrow,itm_orc_sabre,itm_orc_falchion,itm_orc_helm_b,itm_orc_helm_c,itm_orc_helm_d,itm_orc_helm_e,],
      attr_orc_tier_3,wp_archery (110)|wp (100),knows_riding_1|knows_athletics_5|knows_power_draw_4|knows_power_strike_2,orc_face9,orc_face4],
["fell_orc_tracker_of_mordor","Fell_Orc_Tracker_of_Mordor","Fell_Orc_Trackers_of_Mordor",tf_orc| tfg_ranged| tfg_helm| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_orc_furboots,itm_leather_gloves,itm_m_orc_light_c,itm_m_orc_light_d,itm_m_orc_light_e,itm_m_orc_light_c,itm_orc_bow,itm_orc_hook_arrow,itm_orc_sabre,itm_orc_slasher,itm_orc_slasher,itm_orc_helm_d,itm_orc_helm_e,itm_orc_helm_f,itm_orc_helm_g,],
      attr_orc_tier_4,wp_archery (135)| wp (110),knows_riding_1|knows_athletics_6|knows_power_draw_5|knows_power_strike_2,orc_face1,orc_face4],
["orc_archer_of_mordor","Orc_Archer_of_Mordor","Orc_Archers_of_Mordor",tf_orc| tfg_ranged| tfg_armor| tf_no_capture_alive,0,0,fac_mordor,
   [itm_m_orc_light_b,itm_m_orc_light_c,itm_m_orc_light_d,itm_m_orc_light_e,itm_orc_bow,itm_orc_hook_arrow,itm_orc_club_a,itm_orc_club_b,itm_orc_club_c,itm_orc_club_d,itm_orc_helm_a,itm_orc_helm_b,itm_orc_helm_c,],
      attr_orc_tier_2,wp_orc_tier_2,knows_athletics_3|knows_power_draw_2|knows_power_strike_1,orc_face7,orc_face6],
["large_orc_archer_of_mordor","Large_Orc_Archer_of_Mordor","Large_Orc_Archers_of_Mordor",tf_orc| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_orc_ragwrap,itm_leather_gloves,itm_m_orc_light_b,itm_m_orc_light_c,itm_m_orc_light_d,itm_m_orc_light_e,itm_orc_bow,itm_orc_hook_arrow,itm_orc_sabre,itm_orc_falchion,itm_orc_helm_b,itm_orc_helm_c,itm_orc_helm_d,itm_orc_helm_e,],
      attr_orc_tier_3,wp_orc_tier_3,knows_athletics_3|knows_power_draw_3|knows_power_strike_2,orc_face9,orc_face4],
["fell_orc_archer_of_mordor","Fell_Orc_Archer_of_Mordor","Fell_Orc_Archers_of_Mordor",tf_orc| tfg_ranged| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_mordor,
   [itm_orc_greaves,itm_evil_gauntlets_b,itm_m_orc_light_d,itm_m_orc_light_e,itm_m_orc_heavy_a,itm_m_orc_heavy_b,itm_orc_bow,itm_orc_hook_arrow,itm_orc_sabre,itm_orc_slasher,itm_orc_slasher,itm_orc_helm_d,itm_orc_helm_e,itm_orc_helm_f,itm_orc_helm_g,],
      attr_orc_tier_4,wp_orc_tier_4,knows_athletics_4|knows_power_draw_4|knows_power_strike_2,orc_face7,orc_face6],
#Moria
["wolf_rider_of_moria","Wolf_Rider_of_Moria","Wolf_Riders_of_Moria",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_horse| tf_no_capture_alive,0,0,fac_moria,
   [itm_orc_sabre,itm_orc_throwing_arrow,itm_orc_falchion,itm_orc_scimitar,itm_warg_1d,itm_warg_1b,itm_warg_1c,],
      str_7| agi_7| int_4| cha_4|level(7),wp_orc_tier_2,knows_riding_3|knows_power_throw_2|knows_power_strike_2|knows_horse_archery_2,orc_face5,orc_face2],
["warg_rider_of_moria","Warg_Rider_of_Moria","Warg_Riders_of_Moria",tf_orc| tf_mounted| tfg_ranged| tfg_armor| tfg_horse| tf_no_capture_alive,0,0,fac_moria,
   [itm_orc_sabre,itm_orc_sabre,itm_orc_throwing_arrow,itm_orc_sabre,itm_moria_armor_a,itm_warg_1d,itm_warg_1d,itm_warg_1b,itm_warg_1c,itm_orc_ragwrap,],
      str_9| agi_8| int_4| cha_4|level(12),wp_orc_tier_3,knows_riding_3|knows_power_throw_3|knows_power_strike_4|knows_horse_archery_3,orc_face9,orc_face8],
["bolg_clan_rider","Bolg_Clan_Rider","Bolg_Clan_Riders",tf_orc| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_moria,
   [itm_orc_sabre,itm_orc_scimitar,itm_orc_throwing_arrow,itm_orc_ragwrap,itm_wargarmored_2b,itm_wargarmored_2c,itm_wargarmored_3a,itm_moria_armor_a,itm_moria_armor_b,itm_gundabad_helm_e,itm_moria_orc_shield_c,],
      str_11| agi_9| int_4| cha_4|level(17),wp_orc_tier_4,knows_riding_4|knows_power_throw_4|knows_power_strike_4|knows_horse_archery_5,orc_face5,orc_face4],
["snaga_of_moria","Snaga_of_Moria","Snagas_of_Moria",tf_orc| tf_no_capture_alive,0,0,fac_moria,
   [itm_orc_helm_b,itm_orc_helm_c,itm_orc_helm_d,itm_orc_sabre,itm_moria_armor_a,itm_moria_armor_b,itm_orc_falchion,itm_orc_scimitar,itm_orc_machete,itm_orc_axe,],
      attr_orc_tier_1,wp_orc_tier_1,knows_athletics_3|knows_power_throw_1|knows_power_strike_1,orc_face4,orc_face9],
["goblin_of_moria","Goblin_of_Moria","Goblins_of_Moria",tf_orc| tfg_armor| tf_no_capture_alive,0,0,fac_moria,
   [itm_orc_sabre,itm_orc_falchion,itm_orc_scimitar,itm_moria_armor_b,itm_moria_armor_c,itm_moria_armor_b,itm_orc_simple_spear,itm_moria_orc_shield_a,itm_orc_helm_b,itm_orc_helm_c,itm_orc_helm_d,itm_orc_helm_e,],
      attr_orc_tier_2,wp_orc_tier_2,knows_athletics_4|knows_power_draw_1|knows_power_throw_2|knows_power_strike_3,orc_face9,orc_face2],
["large_goblin_of_moria","Large_Goblin_of_Moria","Large_Goblins_of_Moria",tf_orc| tfg_shield| tfg_armor| tfg_helm| tf_no_capture_alive,0,0,fac_moria,
   [itm_orc_throwing_axes,itm_orc_sabre,itm_moria_armor_d,itm_moria_armor_c,itm_orc_simple_spear,itm_moria_orc_shield_a,itm_moria_orc_shield_b,itm_moria_armor_d,itm_orc_helm_g,itm_orc_helm_h,itm_orc_helm_j,itm_orc_helm_k,itm_orc_bill,],
      attr_orc_tier_3,wp_orc_tier_3,knows_athletics_5|knows_power_draw_2|knows_power_throw_2|knows_power_strike_4,orc_face3,orc_face8],
["fell_goblin_of_moria","Fell_Goblin_of_Moria","Fell_Goblins_of_Moria",tf_orc| tfg_shield| tfg_armor| tfg_helm| tf_no_capture_alive,0,0,fac_moria,
   [itm_isengard_axe,itm_orc_slasher,itm_orc_throwing_axes,itm_moria_orc_shield_b,itm_moria_orc_shield_a,itm_moria_armor_e,itm_orc_helm_g,itm_orc_helm_h,itm_orc_helm_j,itm_orc_helm_k,itm_orc_greaves,itm_moria_orc_shield_c,],
      attr_orc_tier_4,wp_orc_tier_4,knows_athletics_6|knows_power_draw_2|knows_power_throw_3|knows_power_strike_4,orc_face1,orc_face6],
["archer_snaga_of_moria","Archer_Snaga_of_Moria","Archer_Snagas_of_Moria",tf_orc| tfg_ranged| tfg_armor| tf_no_capture_alive,0,0,fac_moria,
   [itm_orc_slasher,itm_orc_falchion,itm_orc_bow,itm_orc_hook_arrow,itm_moria_armor_b,itm_orc_helm_b,],
      attr_orc_tier_2,wp_orc_tier_2,knows_athletics_3|knows_power_draw_2|knows_power_strike_1,orc_face9,orc_face6],
["large_goblin_archer_of_moria","Large_Goblin_Archer_of_Moria","Large_Goblin_Archers_of_Moria",tf_orc| tfg_ranged| tfg_boots| tf_no_capture_alive,0,0,fac_moria,
   [itm_orc_slasher,itm_orc_falchion,itm_orc_bow,itm_orc_hook_arrow,itm_leather_gloves,itm_moria_armor_c,itm_moria_armor_b,itm_moria_armor_c,itm_orc_helm_b,itm_orc_ragwrap,itm_orc_helm_c,itm_orc_helm_e,],
      attr_orc_tier_3,wp_orc_tier_3,knows_athletics_3|knows_power_draw_3|knows_power_strike_2,orc_face5,orc_face6],
["fell_goblin_archer_of_moria","Fell_Goblin_Archer_of_Moria","Fell_Goblin_Archers_of_Moria",tf_orc| tfg_ranged| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_moria,
   [itm_orc_slasher,itm_orc_falchion,itm_orc_bow,itm_orc_hook_arrow,itm_moria_armor_d,itm_moria_armor_e,itm_moria_armor_d,itm_orc_greaves,itm_orc_helm_g,itm_orc_helm_h,itm_orc_helm_j,itm_orc_helm_k,],
      attr_orc_tier_4,wp_orc_tier_4,knows_athletics_4|knows_power_draw_4|knows_power_strike_2,orc_face5,orc_face4],
["moria_items","BUG","BUG",tf_hero,0,0,fac_moria,
   [itm_warg_1b,itm_warg_1c,itm_warg_1d,itm_gundabad_armor_a,itm_gundabad_armor_b,itm_gundabad_armor_c,itm_gundabad_armor_d,itm_gundabad_armor_e,itm_gundabad_helm_a,itm_gundabad_helm_b,itm_gundabad_helm_c,itm_gundabad_helm_d,itm_gundabad_helm_e,itm_moria_orc_shield_c,itm_orc_scimitar,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,],
      0,0,0,0],
#MT Gundabad
["goblin_gundabad","Gundabad_Goblin","Gundabad_Goblins",tf_orc| tf_no_capture_alive,0,0,fac_gundabad,
   [itm_gundabad_helm_a,itm_gundabad_armor_a,itm_orc_tribal_a,itm_orc_club_a,itm_orc_machete,itm_orc_club_b,itm_orc_simple_spear,itm_orc_simple_spear,],
      attr_orc_tier_1,wp_orc_tier_1,knows_athletics_3|knows_power_throw_1|knows_power_strike_1,orc_face1,orc_face2],
["orc_gundabad","Gundabad_Orc","Gundabad_Orcs",tf_orc| tfg_armor| tf_no_capture_alive,0,0,fac_gundabad,
   [itm_gundabad_helm_a,itm_gundabad_helm_b,itm_gundabad_armor_b,itm_orc_machete,itm_orc_club_c,itm_orc_club_d,itm_orc_simple_spear,itm_gundabad_armor_c,itm_orc_axe,itm_orc_shield_a,itm_orc_shield_b,],
      attr_orc_tier_2,wp_orc_tier_2,knows_athletics_4|knows_power_draw_1|knows_power_throw_2|knows_power_strike_3,orc_face7,orc_face6],
["orc_fighter_gundabad","Gundabad_Orc_Fighter","Gundabad_Orc_Fighters",tf_orc| tfg_shield| tfg_armor| tfg_helm| tfg_boots| tf_no_capture_alive,0,0,fac_gundabad,
   [itm_gundabad_helm_c,itm_gundabad_helm_b,itm_gundabad_armor_d,itm_gundabad_armor_c,itm_orc_throwing_axes,itm_orc_sabre,itm_orc_machete,itm_leather_gloves,itm_orc_coif,itm_orc_furboots,itm_orc_shield_b,itm_orc_shield_a,],
      attr_orc_tier_3,wp_orc_tier_3,knows_athletics_5|knows_power_draw_1|knows_power_throw_2|knows_power_strike_4,orc_face5,orc_face6],
["fell_orc_warrior_gundabad","Gundabad_Fell_Orc_Warrior","Gundabad_Fell_Orc_Warriors",tf_orc| tfg_shield| tfg_armor| tfg_helm| tf_no_capture_alive,0,0,fac_gundabad,
   [itm_gundabad_helm_c,itm_gundabad_helm_d,itm_gundabad_armor_d,itm_gundabad_armor_e,itm_orc_two_handed_axe,itm_orc_sabre,itm_orc_throwing_axes,itm_orc_sabre,itm_leather_gloves,itm_orc_furboots,itm_orc_shield_b,itm_orc_shield_a,],
      attr_orc_tier_4,wp_orc_tier_4,knows_athletics_6|knows_power_draw_2|knows_power_throw_3|knows_power_strike_5,orc_face3,orc_face8],
["goblin_bowmen_gundabad","Goblin_Shooter_of_the_North","Goblin_Shooters_of_the_North",tf_orc| tfg_ranged| tfg_armor| tf_no_capture_alive,0,0,fac_gundabad,
   [itm_gundabad_helm_a,itm_gundabad_armor_a,itm_orc_tribal_a,itm_orc_club_a,itm_orc_club_c,itm_orc_bow,itm_orc_hook_arrow,itm_orc_ragwrap,],
      attr_orc_tier_2,wp_orc_tier_2,knows_athletics_3|knows_power_draw_2|knows_power_strike_1,orc_face1,orc_face2],
["keen_eyed_goblin_archer_gundabad","Keen-Eyed_Goblin_Archer_of_the_North","Keen-Eyed_Goblin_Archers_of_the_North",tf_orc| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_gundabad,
   [itm_gundabad_helm_a,itm_gundabad_helm_b,itm_gundabad_armor_c,itm_gundabad_armor_b,itm_orc_axe,itm_orc_club_d,itm_orc_bow,itm_orc_hook_arrow,itm_leather_gloves,itm_orc_ragwrap,itm_orc_furboots,],
      attr_orc_tier_3,wp_orc_tier_3,knows_athletics_3|knows_power_draw_3|knows_power_strike_2,orc_face5,orc_face8],
["fell_goblin_archer_gundabad","Fell_Goblin_Archer_of_the_North","Fell_Goblin_Archers_of_the_North",tf_orc| tfg_ranged| tfg_armor| tfg_boots| tf_no_capture_alive,0,0,fac_gundabad,
   [itm_gundabad_helm_c,itm_gundabad_armor_e,itm_gundabad_armor_d,itm_orc_axe,itm_orc_machete,itm_orc_bow,itm_orc_hook_arrow,itm_orc_furboots,],
      attr_orc_tier_4,wp_orc_tier_4,knows_athletics_4|knows_power_draw_4|knows_power_strike_2,orc_face3,orc_face6],
["goblin_rider_gundabad","Gundabad_Goblin_Rider","Gundabad_Goblin_Riders",tf_orc| tf_mounted| tfg_armor| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_gundabad,
   [itm_gundabad_armor_b,itm_orc_club_a,itm_orc_club_b,itm_orc_club_c,itm_orc_throwing_arrow,itm_warg_1d,itm_warg_1b,itm_warg_1c,],
      attr_orc_tier_2,wp_orc_tier_3,knows_riding_3|knows_horse_archery_2|knows_power_throw_2|knows_power_strike_2,orc_face9,orc_face8],
["warg_rider_gundabad","Gundabad_Warg_Rider","Gundabad_Warg_Riders",tf_orc| tf_mounted| tfg_armor| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_gundabad,
   [itm_gundabad_armor_b,itm_gundabad_armor_b,itm_orc_machete,itm_orc_club_c,itm_orc_throwing_arrow,itm_orc_club_d,itm_orc_furboots,itm_orc_ragwrap,itm_warg_1c,itm_warg_1d,itm_warg_1b,itm_warg_1d,itm_orc_shield_b,],
      attr_orc_tier_3,wp_orc_tier_4,knows_horse_archery_3|knows_riding_3|knows_power_throw_3|knows_power_strike_4,orc_face1,orc_face6],
["goblin_north_clan_rider","Goblin_North_Clan_Rider","Goblin_North_Clan_Riders",tf_orc| tf_mounted| tfg_armor| tfg_shield| tfg_helm| tfg_horse| tfg_boots|tfg_gloves| tf_no_capture_alive,0,0,fac_gundabad,
   [itm_gundabad_helm_e,itm_gundabad_armor_b,itm_gundabad_armor_e,itm_orc_throwing_arrow,itm_orc_sabre,itm_orc_scimitar,itm_leather_gloves,itm_orc_furboots,itm_wargarmored_3a,itm_orc_shield_b,itm_orc_shield_a,],
      str_11| agi_9| int_4| cha_4|level(20),wp_orc_tier_5,knows_horse_archery_4|knows_riding_5|knows_power_throw_4|knows_power_strike_4,orc_face3,orc_face6],
["gundabad_items","BUG","_",tf_hero,0,0,fac_gundabad,
   [itm_leather_boots,itm_metal_scraps_bad,itm_metal_scraps_medium,itm_metal_scraps_good,itm_leather_gloves,itm_warg_1b,itm_warg_1c,itm_warg_1d,itm_angmar_shield,itm_orc_bill,itm_orc_scimitar,itm_orc_machete,itm_orc_axe,itm_orc_two_handed_axe,itm_orc_greaves,],
      0,0,0,0],
["mountain_goblin","Mountain_Goblin","Mountain_Goblins",tf_orc| tf_no_capture_alive,0,0,fac_tribal_orcs,
   [itm_orc_tribal_a,itm_orc_tribal_b,itm_orc_tribal_c,itm_orc_tribal_c,itm_orc_shield_a,itm_orc_shield_b,itm_orc_shield_c,itm_orc_ragwrap,itm_skull_club,itm_twohand_wood_club,itm_bone_cudgel,itm_wood_club,itm_orc_simple_spear,itm_orc_sledgehammer,],
      attr_orc_tier_2,wp_orc_tier_2,knows_athletics_3|knows_power_strike_2,orc_face3,orc_face4],
["tribal_orc","Tribal_Orc","Tribal_Orcs",tf_orc| tf_no_capture_alive,0,0,fac_tribal_orcs,
   [itm_orc_tribal_a,itm_orc_tribal_b,itm_orc_tribal_c,itm_orc_tribal_c,itm_skull_club,itm_bone_cudgel,itm_twohand_wood_club,itm_wood_club,itm_orc_simple_spear,itm_orc_sledgehammer,itm_wood_club,itm_orc_simple_spear,itm_orc_sledgehammer,],
      attr_orc_tier_1,wp_orc_tier_1,knows_athletics_3,orc_face1,orc_face2],
["tribal_orc_warrior","Tribal_Orc_Warrior","Tribal_Orc_Warriors",tf_orc| tfg_armor| tf_no_capture_alive,0,0,fac_tribal_orcs,
   [itm_orc_tribal_b,itm_orc_tribal_c,itm_orc_tribal_c,itm_skull_club,itm_bone_cudgel,itm_wood_club,itm_twohand_wood_club,itm_orc_simple_spear,itm_orc_sledgehammer,itm_wood_club,itm_orc_simple_spear,itm_orc_sledgehammer,],
      attr_orc_tier_2,wp_orc_tier_2,knows_athletics_4,orc_face7,orc_face6],
["tribal_orc_chief","Tribal_Orc_Chief","Tribal_Orc_Chiefs",tf_orc| tfg_armor| tfg_helm| tf_no_capture_alive,0,0,fac_tribal_orcs,
   [itm_orc_coif,itm_orc_tribal_b,itm_orc_tribal_c,itm_orc_tribal_c,itm_skull_club,itm_bone_cudgel,itm_orc_sabre,itm_orc_simple_spear,itm_orc_ragwrap,itm_orc_machete,],
      attr_orc_tier_3,wp_orc_tier_3,knows_athletics_4|knows_power_strike_3,orc_face1,orc_face2],
#Numenorean
["black_numenorean_renegade","Black_Numenorean_Renegade","Black_Numenorean_Renegades",tf_evil_man| tfg_armor| tfg_boots,0,0,fac_mordor,
   [itm_leather_boots,itm_leather_gloves,itm_evil_light_armor,itm_uruk_spear,],
      attr_tier_2,wp_tier_2,knows_common|knows_riding_1|knows_athletics_1|knows_power_strike_1,mordor_man1,mordor_man2],
["black_numenorean_warrior","Black_Numenorean_Warrior","Black_Numenorean_Warriors",tf_evil_man| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,
   [itm_leather_boots,itm_leather_gloves,itm_evil_light_armor,itm_m_armor_b,itm_mordor_man_shield_b,itm_mordor_sword,],
      attr_tier_3,wp_tier_3,knows_common|knows_riding_2|knows_athletics_2|knows_shield_2|knows_power_strike_3|knows_ironflesh_3,mordor_man1,mordor_man2],
["black_numenorean_veteran_warrior","Black_Numenorean_Veteran_Warrior","Black_Numenorean_Veteran_Warriors",tf_evil_man| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,
   [itm_uruk_greaves,itm_evil_gauntlets_b,itm_m_armor_a,itm_mordor_helm,itm_mordor_man_shield_b,itm_mordor_longsword,itm_mordor_sword,],
      attr_tier_4,wp_tier_4,knows_common|knows_tactics_1|knows_athletics_4|knows_shield_3|knows_power_strike_4|knows_ironflesh_4,mordor_man1,mordor_man2],
["black_numenorean_champion","Black_Numenorean_Champion","Black_Numenorean_Champions",tf_evil_man| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,
   [itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_black_num_armor,itm_black_num_helm,itm_mordor_man_shield_b,itm_mordor_longsword,],
      attr_tier_5,wp_tier_5,knows_common|knows_tactics_1|knows_athletics_5|knows_shield_4|knows_power_strike_5|knows_ironflesh_5,mordor_man1,mordor_man2],
["black_numenorean_assassin","Black_Numenorean_Assassin","Black_Numenorean_Assassins",tf_evil_man| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,
   [itm_uruk_greaves,itm_leather_gloves,itm_m_armor_a,itm_mordor_helm,itm_mordor_man_shield_b,itm_mordor_longsword,],
      attr_tier_5,wp_tier_5,knows_common|knows_athletics_6|knows_shield_2|knows_power_strike_5|knows_ironflesh_6,mordor_man1,mordor_man2],
["black_numenorean_veteran_horseman","Black_Numenorean_Horseman","Black_Numenorean_Horsemen",tf_evil_man| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_mordor,
   [itm_leather_boots,itm_evil_gauntlets_b,itm_m_armor_a,itm_mordor_helm,itm_mordor_man_shield_b,itm_mordor_warhorse,itm_mordor_longsword,],
      attr_tier_4,wp_tier_4,knows_common|knows_tactics_1|knows_riding_4|knows_athletics_3|knows_shield_3|knows_power_strike_4|knows_ironflesh_4,mordor_man1,mordor_man2],
["black_numenorean_horsemaster","Black_Numenorean_Horsemaster","Black_Numenorean_Horsemasters",tf_evil_man| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_mordor,
   [itm_uruk_greaves,itm_evil_gauntlets_a,itm_black_num_armor,itm_black_num_helm,itm_mordor_man_shield_a,itm_mordor_warhorse,itm_mordor_longsword,],
      attr_tier_5,wp_tier_5,knows_common|knows_tactics_1|knows_riding_5|knows_athletics_3|knows_shield_4|knows_power_strike_5|knows_ironflesh_5,mordor_man1,mordor_man2],

#Captains and lieutenants of all factions
["noldorin_commander","Noldorin_Commander","Noldorin_Commanders",tf_lorien| tfg_ranged| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_lorien,
   [itm_lorien_bow,itm_elven_arrows,itm_lorien_armor_c,itm_lorien_helm_b,itm_lorien_shield_b,itm_lorien_boots,itm_lorien_sword_a,itm_lorien_warhorse,],
      attr_elf_tier_6,wp_elf_tier_6,knows_inventory_management_1|knows_power_draw_6|knows_tactics_6|knows_tracking_1|knows_horse_archery_6|knows_riding_5|knows_athletics_6|knows_power_strike_6|knows_ironflesh_6,lorien_elf_face_1,lorien_elf_face_2],
["elf_captain_of_lothlorien","Elf_Captain_of_Lothlorien","Elf_Captains_of_Lothlorien",tf_lorien| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_lorien,
   [itm_lorien_bow,itm_elven_arrows,itm_lorien_armor_c,itm_lorien_helm_b,itm_lorien_shield_b,itm_lorien_boots,itm_lorien_sword_a,itm_lorien_warhorse,],
      attr_elf_tier_6,wp_elf_tier_6,knows_inventory_management_1|knows_power_draw_6|knows_tactics_4|knows_tracking_1|knows_horse_archery_5|knows_riding_5|knows_athletics_5|knows_power_strike_5|knows_ironflesh_5,lorien_elf_face_1,lorien_elf_face_2],
["lothlorien_lieutenant","Lothlorien_Lieutenant","Lothlorien_Lieutenants",tf_lorien| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_lorien,
   [itm_lorien_bow,itm_elven_arrows,itm_lorien_armor_e,itm_lorien_helm_b,itm_lorien_shield_b,itm_lorien_boots,itm_lorien_sword_a,],
      attr_elf_tier_6,wp_elf_tier_6,knows_inventory_management_1|knows_power_draw_6|knows_tactics_3|knows_tracking_1|knows_riding_3|knows_athletics_4|knows_power_strike_4|knows_ironflesh_4,lorien_elf_face_1,lorien_elf_face_2],
["elf_captain_of_mirkwood","Elf_Captain_of_Greenwood","Elf_Captains_of_Greenwood",tf_woodelf| tfg_ranged| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_woodelf,
   [itm_lorien_bow,itm_elven_arrows,itm_mirkwood_armor_e,itm_mirkwood_helm_b,itm_mirkwood_spear_shield_c,itm_mirkwood_leather_greaves,itm_lorien_sword_a,],
      attr_elf_tier_6,wp_elf_tier_6,knows_riding_4|knows_athletics_5|knows_power_draw_7|knows_power_strike_5|knows_ironflesh_5,mirkwood_elf_face_1,mirkwood_elf_face_2],
["mirkwood_lieutenant","Greenwood_Lieutenant","Greenwood_Lieutenants",tf_woodelf| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_woodelf,
   [itm_elven_bow,itm_elven_arrows,itm_mirkwood_armor_c,itm_mirkwood_helm_b,itm_mirkwood_spear_shield_c,itm_mirkwood_leather_greaves,itm_lorien_sword_a,],
      attr_elf_tier_6,wp_elf_tier_6,knows_riding_3|knows_athletics_4|knows_power_draw_6|knows_power_strike_4|knows_ironflesh_4,mirkwood_elf_face_1,mirkwood_elf_face_2],
["elf_captain_of_rivendell","Elf_Captain_of_Rivendell","Elf_Captains_of_Rivendell",tf_imladris| tfg_ranged| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_imladris,
   [itm_riv_boots,itm_lorien_bow,itm_riv_armor_leader,itm_riv_helm_a,itm_riv_shield_b,itm_elven_arrows,itm_lorien_sword_a,itm_riv_warhorse,],
      attr_elf_tier_6,wp_elf_tier_6,knows_riding_5|knows_athletics_5|knows_power_strike_5|knows_power_draw_6|knows_ironflesh_5,rivendell_elf_face_1,rivendell_elf_face_2],
["rivendell_lieutenant","Rivendell_Lieutenant","Rivendell_Lieutenants",tf_imladris| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_imladris,
   [itm_riv_boots,itm_lorien_bow,itm_riv_armor_leader,itm_elven_arrows,itm_lorien_sword_a,],
      attr_elf_tier_6,wp_elf_tier_6,knows_riding_3|knows_athletics_4|knows_power_draw_5|knows_power_strike_4|knows_ironflesh_4,rivendell_elf_face_1,rivendell_elf_face_2],
["lieutenant_of_rohan","Lieutenant_of_Rohan","Lieutenants_of_Rohan",tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_armor_l,itm_rohan_captain_helmet,itm_rohan_shield_g,itm_mail_mittens,itm_leather_boots,itm_rohan_inf_sword,itm_rohirrim_courser,itm_rohirrim_hunter,itm_rohan_lance_banner_sun,itm_rohan_lance_banner_horse,],
      attr_tier_6,wp_tier_6,knows_common|knows_tactics_2|knows_riding_3|knows_athletics_2|knows_shield_1|knows_power_strike_4,rohan_face_middle_1,rohan_face_older_2],
["captain_of_rohan","Captain_of_Rohan","Captains_of_Rohan",tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohirrim_long_hafted_axe,itm_rohan_armor_l,itm_rohan_captain_helmet,itm_rohan_shield_g,itm_mail_mittens,itm_rohirrim_war_greaves,itm_rohan_inf_sword,itm_rohan_warhorse,itm_rohan_lance_banner_sun,itm_rohan_lance_banner_horse,],
      attr_tier_6,wp_tier_6,knows_common|knows_tactics_3|knows_riding_5|knows_athletics_3|knows_shield_2|knows_power_strike_5|knows_ironflesh_6,rohan_face_middle_1,rohan_face_older_2],
["high_captain_of_rohan","High_Captain_of_Rohan","High_Captains_of_Rohan",tf_rohan| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohirrim_long_hafted_axe,itm_rohan_armor_l,itm_rohan_captain_helmet,itm_rohan_shield_g,itm_mail_mittens,itm_rohirrim_war_greaves,itm_rohan_inf_sword,itm_rohan_warhorse,itm_rohan_lance_banner_sun,itm_rohan_lance_banner_horse,],
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
   [itm_khand_noble_lam,itm_variag_greaves,itm_variag_kataphrakt,itm_khand_helmet_b1,itm_mail_mittens,itm_khand_tulwar,itm_khand_2h_tulwar,itm_easterling_round_horseman,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_4|knows_athletics_3|knows_shield_2|knows_power_strike_4|knows_ironflesh_5,khand_man1,khand_man2],
["easterling_lieutenant","Variag_War_Priest","Variag_War_Priests",tf_evil_man| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_khand,
   [itm_khand_noble_lam,itm_variag_greaves,itm_khand_helmet_b1,itm_mail_mittens,itm_khand_rammace,itm_easterling_round_horseman,],
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
["dunnish_chieftain","Dunnish_Chieftain","Dunnish_Chieftains",tf_dunland| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_dunland,
   [itm_dunland_wolfboots,itm_dunland_armor_e,itm_dun_berserker,itm_dun_shield_b,itm_dun_berserker,itm_hunter,itm_leather_boots,itm_evil_gauntlets_a,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_4|knows_athletics_3|knows_shield_3|knows_power_strike_5|knows_ironflesh_5,dunland_face1,dunland_face2],
["dunnish_lieutenant","Dunnish_Hetman","Dunnish_Hetmen",tf_dunland| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dunland,
   [itm_dunland_wolfboots,itm_dunland_armor_e,itm_dun_berserker,itm_dun_helm_c,itm_dun_shield_b,itm_evil_gauntlets_a,],
      attr_tier_6,wp_tier_6,knows_common|knows_athletics_2|knows_shield_1|knows_power_strike_3|knows_ironflesh_3,dunland_face1,dunland_face2],
["goblin_chieftain","Goblin_Chieftain","Goblin_Chieftains",tf_orc| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_orc_sabre,itm_moria_orc_shield_a,itm_moria_orc_shield_b,itm_leather_gloves,itm_isen_orc_armor_e,itm_orc_coif,itm_orc_coif,itm_orc_ragwrap,itm_wargarmored_1b,],
      attr_orc_tier_6,wp_orc_tier_6,knows_riding_4|knows_athletics_4|knows_power_draw_1|knows_power_throw_3|knows_power_strike_5|knows_ironflesh_5,orc_face5,orc_face8],
 
["captain_of_gondor","Captain_of_Gondor","Captains_of_Gondor",tf_gondor| tf_mounted| tfg_gloves| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gon_leader_surcoat_cloak,itm_gondor_leader_helm,itm_mail_mittens,itm_gondor_heavy_greaves,itm_gondor_shield_e,itm_gondor_bastard,itm_gondor_warhorse,],
      attr_tier_6,wp_tier_6,knows_common|knows_riding_1|knows_athletics_4|knows_shield_3|knows_power_strike_5|knows_ironflesh_6,gondor_face1,gondor_face2],
#["high_captain_of_gondor","High_Captain_of_Gondor","High_Captains_of_Gondor",tf_mounted|tfg_gloves|tfg_shield|tfg_armor|tfg_helmet|tfg_horse|tfg_boots,0,0,fac_gondor,
#[itm_gon_tower_knight,itm_gondor_leader_helm,itm_mail_mittens,itm_mail_mittens,itm_mail_boots,itm_gondor_shield_a,itm_sword_medieval_c,itm_sword_viking_1,itm_gondor_warhorse],
#def_attrib|level(40),wp(255),knows_common|knows_riding_2|knows_athletics_6|knows_shield_4|knows_power_strike_6|knows_ironflesh_6,gondor_face1,gondor_face2],
["end_leaders","bug","bug",0,0,0,fac_gondor,   [],      0,0,0,0],
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
["peasant_woman","Peasant_Woman","Peasant_Women",tf_female| tfg_armor,0,0,fac_commoners,
   [itm_leather_jerkin,itm_leather_boots,],
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
   [itm_khand_foot_lam_c,itm_variag_greaves,],
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
 
#TLD walkers
["walker_man_gondor_black","Townsman","_",tf_gondor| tfg_boots| tfg_armor,0,0,fac_gondor,
   [itm_tld_tunic,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,man_face_young_1,man_face_old_2],
["walker_man_gondor_white","Townsman","_",tf_gondor| tfg_boots| tfg_armor,0,0,fac_gondor,
   [itm_tld_tunic,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,man_face_young_1,man_face_old_2],
["walker_man_gondor_blue","Townsman","_",tf_gondor| tfg_boots| tfg_armor,0,0,fac_gondor,
   [itm_tld_tunic,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,man_face_young_1,man_face_old_2],
["walker_man_gondor_green","Townsman","_",tf_gondor| tfg_boots| tfg_armor,0,0,fac_gondor,
   [itm_tld_tunic,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,man_face_young_1,man_face_old_2],
["walker_man_rohan_t","Rohan_Townsman","_",tf_rohan| tfg_boots| tfg_armor,0,0,fac_rohan,
   [itm_tld_tunic,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,rohan_face_middle_1,rohan_face_older_2],
["walker_man_rohan_d","Rohan_Townsman","_",tf_rohan| tfg_boots| tfg_armor,0,0,fac_rohan,
   [itm_rohan_fine_outfit_dale_dress,itm_rohan_shoes,],
      attr_tier_1,wp_tier_1,knows_common,rohan_face_middle_1,rohan_face_older_2],
["walker_woman_rohan_t","Rohan_Maiden","_",tf_female| tfg_boots| tfg_armor,0,0,fac_rohan,
   [itm_tld_tunic,itm_rohan_shoes,],
      attr_tier_1,wp_tier_1,knows_common,rohan_woman_face_1,rohan_woman_face_2],
["walker_woman_rohan_d","Rohan_Maiden","_",tf_female| tfg_boots| tfg_armor,0,0,fac_rohan,
   [itm_green_dress,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,rohan_woman_face_1,rohan_woman_face_2],
["walker_woman_gondor_b","Gondor_Woman","_",tf_female| tfg_boots| tfg_armor| tfg_helm,0,0,fac_gondor,
   [itm_black_dress,itm_wimple_a,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,woman_face_1,woman_face_2],
["walker_woman_gondor_bw","Gondor_Woman","_",tf_female| tfg_boots| tfg_armor| tfg_helm,0,0,fac_gondor,
   [itm_blackwhite_dress,itm_wimple_with_veil,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,woman_face_1,woman_face_2],
["walker_woman_gondor_w","Gondor_Noble","_",tf_male| tfg_boots| tfg_armor,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_leather_boots,],
      attr_tier_1,wp_tier_1,knows_common,woman_face_1,woman_face_2],
# end TLD walkers

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
   [itm_rohan_light_greaves,itm_mail_mittens,itm_rohan_armor_j,itm_rohan_spear,],
      0,0,0,rohan_face_old_2],
["trainer_dale","Trainer","_",tf_hero| tfg_armor| tfg_boots, scn_dale_arena|entry(1),0,fac_commoners,
   [itm_blue_tunic,itm_leather_boots,],
      0,0,0,gondor_face2],
["trainer_elf","Trainer","_",tf_hero| tf_lorien| tfg_armor| tfg_boots, scn_elf_arena|entry(1),0,fac_commoners,
   [itm_whiterobe,itm_leather_boots,],
      0,0,0,lorien_elf_face_2],
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
   [itm_khand_foot_lam_c,itm_leather_boots,],
      0,0,0,khand_man2],
["trainer_rhun","Trainer","_",tf_hero| tf_evil_man| tfg_armor| tfg_boots, scn_rhun_arena|entry(1),0,fac_commoners,
   [itm_rhun_armor_a,itm_furry_boots,],
      0,0,0,rhun_man2],
["trainer_harad","Trainer","_",tf_hero| tf_harad| tfg_armor| tfg_boots, scn_harad_arena|entry(1),0,fac_commoners,
   [itm_harad_scale,itm_harad_scale_greaves,],
      0,0,0,haradrim_face_2],
["trainer_umbar","Trainer","_",tf_hero| tfg_armor| tfg_boots, scn_umbar_arena|entry(1),0,fac_commoners,
   [itm_umb_armor_g,itm_corsair_boots,],
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
      str_15|agi_15|int_12|cha_9|level(20),wp_one_handed(160)|wp_two_handed(140)|wp_polearm(120)|wp_archery(140)|wp_throwing(120),knows_trade_2|knows_riding_1|knows_athletics_5|knows_power_draw_3|knows_power_strike_4|knows_shield_3|knows_ironflesh_4|knows_weapon_master_4|knows_spotting_3|knows_pathfinding_4|knows_tracking_3|knows_trainer_3|knows_tactics_2|knows_wound_treatment_2,0x000000086b006144444b6e574146472400000000001ec82c0000000000000000],
["npc2","Cirdil","_",tf_hero| tf_gondor| tf_unmoveable_in_party_window,0,0,fac_gondor,
   [itm_gon_jerkin,itm_gondor_light_greaves,itm_gondor_auxila_helm,itm_shortened_spear,itm_short_bow,itm_gondor_arrows,itm_gon_tab_shield_a,itm_gondor_short_sword,],
      str_10|agi_7|int_4|cha_4|level(1),wp(60),knows_athletics_1|knows_power_strike_1|knows_first_aid_1,0x000000002d00418519da91378c8aa8d300000000001eb9110000000000000000],
["npc3","Ulfas","_",tf_rohan| tf_hero| tf_unmoveable_in_party_window,0,0,fac_rohan,
   [itm_rohan_armor_d,itm_rohan_light_greaves,itm_rohan_shield_a,itm_leather_gloves,itm_rohan_cav_helmet_a,itm_rohan_spear,itm_rohirrim_long_hafted_axe,itm_rohirrim_courser,],
      str_14|agi_10|int_5|cha_9|level(10),wp(100),knows_riding_3|knows_shield_1|knows_power_strike_2|knows_power_throw_1|knows_ironflesh_3|knows_weapon_master_2|knows_athletics_1|knows_wound_treatment_1|knows_first_aid_2|knows_trade_2|knows_looting_2,0x0000000886000085395d6db6db6db8db00000000001db6e30000000000000000],
["npc4","Galmyne","_",tf_female| tf_mounted| tfg_ranged| tf_hero| tf_unmoveable_in_party_window,0,0,fac_rohan,
   [itm_rohan_armor_m,itm_rohan_light_greaves,itm_rohan_shield_d,itm_rohan_archer_helmet_b,itm_rohan_sword_c,itm_strong_bow,itm_khergit_arrows,itm_rohan_warhorse,],
      str_14|agi_18|int_9|cha_12|level(24),wp_one_handed(160)|wp_two_handed(120)|wp_polearm(140)|wp_archery(180)|wp_throwing(160),knows_horse_archery_5|knows_riding_6|knows_power_draw_4|knows_power_strike_2|knows_power_throw_4|knows_ironflesh_3|knows_weapon_master_4|knows_shield_3|knows_athletics_1|knows_wound_treatment_4|knows_first_aid_3|knows_trade_3,0x000000000300000114a261248280c73400000000001ca48d0000000000000000],
["npc5","Glorfindel","_",tf_lorien| tf_mounted| tfg_ranged| tf_hero| tf_unmoveable_in_party_window,0,0,fac_lorien,
   [itm_riv_armor_reward,itm_lorien_boots,itm_riv_helm_glorfi,itm_glorfi_bow,itm_elven_arrows,itm_lorien_sword_c,itm_lorien_warhorse,],
      str_30|agi_24|int_18|cha_24|level(55),wp(500),knows_riding_7|knows_ironflesh_6|knows_power_strike_7|knows_athletics_5|knows_tactics_6|knows_prisoner_management_3|knows_leadership_9|knows_power_draw_9|knows_horse_archery_9|knows_weapon_master_8|knows_trainer_6,0x000000018000100a38db6db6db6db6db00000000001db6eb0000000000000000],
["npc6","Luevanna","_",tf_female| tfg_ranged| tf_hero| tf_unmoveable_in_party_window,0,0,fac_woodelf,
   [itm_mirkwood_armor_a,itm_mirkwood_boots,itm_mirkwood_knife,itm_short_bow,itm_woodelf_arrows,],
      str_8|agi_13|int_12|cha_6|level(1),wp_one_handed(70)|wp_two_handed(40)|wp_polearm(40)|wp_archery(100)|wp_throwing(60),knows_power_draw_2|knows_ironflesh_1|knows_athletics_1|knows_spotting_1|knows_pathfinding_3|knows_tracking_1|knows_wound_treatment_2,0x0000000180004009041d7566cb87608000000000001d24d30000000000000000],
["npc7","Kili_Goldfinger","_",tf_dwarf| tf_hero| tf_unmoveable_in_party_window,0,0,fac_dwarf,
   [itm_leather_dwarf_armor,itm_dwarf_pad_boots,itm_dwarf_helm_a,itm_dwarf_sword_a,itm_dwarf_throwing_axe,itm_dwarf_adz,itm_dwarf_shield_f,],
      str_14|agi_8|int_7|cha_6|level(7),wp_one_handed(100)|wp_two_handed(115)|wp_polearm(70)|wp_archery(50)|wp_throwing(115),knows_riding_10|knows_athletics_2|knows_power_strike_3|knows_power_throw_3|knows_ironflesh_3|knows_weapon_master_2|knows_trainer_1|knows_engineer_4|knows_looting_4|knows_trade_3,0x00000001c000110336db6db6db6db6db00000000001db6db0000000000000000],
["npc8","Faniul","_",tf_female| tfg_ranged| tf_hero| tf_unmoveable_in_party_window,0,0,fac_dale,
   [itm_blue_tunic,itm_leather_boots,itm_wimple_with_veil,],
      str_7|agi_6|int_11|cha_5|level(1),wp(40),knows_ironflesh_1|knows_wound_treatment_2|knows_first_aid_3|knows_surgery_2|knows_trade_1,0x0000000712003004589dae38ad69a64900000000001ec6cc0000000000000000],
["npc9","Gulm","_",tf_urukhai| tf_hero| tf_unmoveable_in_party_window,0,0,fac_isengard,
   [itm_isen_uruk_light_a,itm_uruk_chain_greaves,itm_isengard_mallet,itm_evil_gauntlets_a,],
      str_24|agi_17|int_8|cha_4|level(25),wp(185),knows_athletics_7|knows_power_strike_5|knows_ironflesh_10|knows_weapon_master_5|knows_trainer_2,0x00000001b50000c2003d7dc5a4b2195c00000000000000000000000000000000],
["npc10","Durgash","_",tf_orc| tf_mounted| tfg_ranged| tf_hero| tf_unmoveable_in_party_window,0,0,fac_isengard,
   [itm_isen_orc_armor_a,itm_orc_club_a,itm_orc_throwing_arrow,itm_warg_1d,],
      str_12|agi_11|int_11|cha_4|level(10),wp(90),knows_riding_3|knows_power_throw_2|knows_power_strike_2|knows_ironflesh_3|knows_weapon_master_3|knows_spotting_2|knows_pathfinding_4|knows_tracking_1,0x00000001a2000007399e8ccc9cae34e500000000001d16ad0000000000000000],
["npc11","Ufthak","_",tf_orc| tf_hero| tf_unmoveable_in_party_window,0,0,fac_mordor,
   [itm_m_orc_light_a,itm_orc_ragwrap,itm_orc_club_a,itm_orc_simple_spear,itm_orc_helm_a,],
      str_13|agi_8|int_4|cha_4|level(1),wp(75),knows_athletics_2|knows_power_strike_1|knows_ironflesh_1,orc_face6],
["npc12","Gorbag","_",tf_uruk| tf_hero| tf_unmoveable_in_party_window,0,0,fac_mordor,
   [itm_m_uruk_heavy_e,itm_uruk_tracker_boots,itm_orc_two_handed_axe,itm_uruk_pike_a,itm_uruk_helm_b,],
      str_21|agi_16|int_7|cha_4|level(20),wp(175),knows_riding_1|knows_athletics_5|knows_power_strike_5|knows_ironflesh_6|knows_weapon_master_5,uruk_hai_face2],
["npc13","Lykyada","_",tf_harad| tfg_ranged| tf_mounted| tf_hero| tf_unmoveable_in_party_window,0,0,fac_harad,
   [itm_black_snake_armor,itm_harad_leather_greaves,itm_leather_gloves,itm_black_snake_helm,itm_harad_bow,itm_harad_arrows,itm_black_snake_sword,itm_harad_warhorse,],
      str_24|agi_20|int_18|cha_15|level(40),wp(400),knows_horse_archery_5|knows_riding_6|knows_power_strike_5|knows_power_draw_5|knows_ironflesh_7|knows_athletics_3|knows_weapon_master_6|knows_tactics_5|knows_trainer_6,0x000000051f00000b372571b8ed79a6ac00000000001db6360000000000000000],
["npc14","Fuldimir","_",tf_hero| tf_unmoveable_in_party_window,0,0,fac_umbar,
   [itm_umb_armor_a,itm_corsair_boots,itm_umb_shield_a,itm_corsair_throwing_dagger,itm_umbar_rapier,],
      str_10|agi_9|int_7|cha_7|level(5),wp(80),knows_athletics_1|knows_power_throw_2|knows_power_strike_1|knows_trade_2|knows_looting_2,0x00000001b70032453add7524dc76d74900000000001d35330000000000000000],
["npc15","Bolzog","_",tf_orc| tf_hero| tf_unmoveable_in_party_window,0,0,fac_moria,
   [itm_moria_armor_a,itm_orc_helm_b,itm_orc_machete,orc_face_normal],
      str_9|agi_10|int_12|cha_4|level(7),wp(80),knows_athletics_2|knows_power_throw_1|knows_power_strike_1|knows_ironflesh_1|knows_wound_treatment_2|knows_first_aid_2|knows_surgery_1,0x00000001ab00200d35627276a42e150c00000000001dca2c0000000000000000],
["npc16","Varfang","_",tf_mounted| tf_hero| tf_unmoveable_in_party_window,0,0,fac_rhun,
   [itm_rhun_armor_a,itm_furry_boots,itm_rhun_sword,itm_light_lance,itm_rhun_helm_g,itm_tab_shield_small_round_b,itm_rhun_horse_a,],
      str_15|agi_15|int_3|cha_5|level(10),wp(120),knows_riding_5|knows_power_strike_4|knows_ironflesh_1|knows_power_throw_1|knows_weapon_master_3,0x000000018700214944d468dd9bae295b00000000001cb5a40000000000000000],
["npc17","Dimborn","_",tf_hero| tf_unmoveable_in_party_window,0,0,fac_beorn,
   [itm_woodman_tunic,itm_leather_boots,itm_beorn_axe,],
      str_17|agi_13|int_3|cha_3|level(8),wp(95),knows_riding_1|knows_athletics_3|knows_power_draw_2|knows_power_strike_2|knows_ironflesh_3|knows_pathfinding_2,0x00000009f50001c97ac16e65f3ecf7de00000000001cc7080000000000000000],
#NPC system changes end
 
["kingdom_heroes_including_player_begin","bug","_",tf_hero,0,0,fac_gondor,
   [],
      lord_attrib,0,0,0],
#governors (plural contains how player refers to the guy
["gondor_lord","Steward_Denethor","Steward",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gondor_warhorse,itm_denethor_robe,itm_gondor_light_greaves,itm_mail_mittens,itm_gondor_leader_helm,itm_gondor_citadel_sword,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_trainer_5,0x0000000efe00400726c34cb9d447d0cc00000000001cb4580000000000000000],
["rohan_lord","King_Theoden","King",tf_hero| tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_mearas_reward,itm_rohan_armor_th,itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_captain_helmet,itm_rohirrim_long_hafted_axe,itm_rohirrim_throwing_axe,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_trainer_4,0x0000000fff00130347934c399386b8a300000000001db6d90000000000000000],
["isengard_lord","Saruman","Master",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_isengard,
   [itm_courser,itm_whiterobe,itm_leather_boots,itm_sarustaff,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_trainer_6,0x0000000fff004107121a807fc84b82ff00000000001d1ab00000000000000000],
["mordor_lord","Mouth_of_Sauron","Satrap",tf_hero| tf_evil_man| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_mordor,
   [itm_mordor_warhorse2,itm_m_cap_armor,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_blackroot_hood,itm_mordor_longsword,],
      attr_tier_6,wp_tier_6,knight_skills_1,0x0000000fff00000012078077c00ff1c000000000001cf0680000000000000000],
["harad_lord","Chief_Ul-Ulcari","Chief",tf_hero| tf_harad| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,
   [itm_harad_warhorse,itm_harad_heavy,itm_harad_leather_greaves,itm_evil_gauntlets_a,itm_harad_dragon_helm,itm_harad_khopesh,],
      attr_tier_6,wp_tier_6,knight_skills_4|knows_trainer_5,0x00000009ff0020071415a5f9fb60c1b700000000001d663b0000000000000000],
["rhun_lord","Jarl_Helcaroth","Jarl",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_horse_e,itm_rhun_armor_k,itm_furry_boots,itm_evil_gauntlets_a,itm_rhun_helm_o,itm_rhun_greatsword,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_trainer_5,0x00000004a300640c1a938b5499b6556c00000000001edab90000000000000000],
["khand_lord","Shibh_Krukmahur","Shibh",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_khand,
   [itm_variag_kataphrakt,itm_khand_noble_lam,itm_variag_greaves,itm_evil_gauntlets_a,itm_khand_lance,itm_khand_tulwar,itm_variag_gladiator_shield,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_trainer_4,0x0000000f3f00b38712065fd3287f731c00000000001c53780000000000000000],
["umbar_lord","Admiral_Tulmir","Admiral",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_umbar,
   [itm_umb_armor_h,itm_corsair_boots,itm_leather_gloves,itm_umb_helm_f,itm_corsair_bow,itm_corsair_arrows,itm_umbar_rapier,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_trainer_6,0x0000000e3b004244365b6db99b6db7df00000000001dd6eb0000000000000000],
["lorien_lord","Lady_Galadriel","Lady",tf_hero| tf_randomize_face| tf_female,0,0,fac_lorien,
   [itm_galadriel,itm_empty_head,itm_empty_legs,itm_empty_hands,],
      def_attrib|level(2),wp(20),knows_common,0x0000000e3b004000365b6db99b6db7df00000000001dd6eb0000000000000000],
["imladris_lord","Lord_Elrond","Lord",tf_hero| tf_imladris| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_imladris,
   [itm_mearas_reward,itm_riv_armor_leader,itm_riv_boots,itm_leather_gloves,itm_riv_tiara,itm_riv_bow,itm_elven_arrows,itm_riv_bas_sword,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_4|knows_trainer_5,0x0000000bff002001379b74b75346d08d00000000001d969b0000000000000000],
["woodelf_lord","King_Thranduil","King",tf_hero| tf_woodelf| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_woodelf,
   [itm_mirkwood_armor_f,itm_mirkwood_leather_greaves,itm_leather_gloves,itm_riv_tiara,itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_sword,itm_mirkwood_spear_shield_c,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_5|knows_trainer_5,0x0000000c00003002189d6e454c6465a500000000001c68f20000000000000000],
["moria_lord","Master_Bolg_the_Lesser","Master",tf_hero| tf_uruk| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_moria,
   [itm_wargarmored_3a,itm_moria_armor_e,itm_leather_boots,itm_evil_gauntlets_a,itm_orc_helm_c,itm_orc_throwing_axes,itm_orc_slasher,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_trainer_4|knows_leadership_10,0x00000000260010010038c51051df5f5800000000000000000000000000000000],
["guldur_lord","Master_Fuinur","Master",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_guldur,
   [itm_mordor_warhorse,itm_m_cap_armor,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_mordor_cap_helm,itm_mordor_man_shield_b,itm_mordor_longsword,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_trainer_6,0x0000000fcd0005c03586a83d4223b2c200000000001c58e00000000000000000],
["gundabad_lord","Master_Burza Krual","Master",tf_hero| tf_uruk| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gundabad,
   [itm_wargarmored_3a,itm_gundabad_armor_e,itm_orc_greaves,itm_evil_gauntlets_a,itm_gundabad_helm_e,itm_orc_throwing_axes,itm_orc_slasher,],
      attr_tier_6,wp_tier_6,knight_skills_4|knows_trainer_5|knows_leadership_10,0x0000000026002085003f006fe95aae4000000000000000000000000000000000],
["dale_lord","King_Brand","King",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_dale,
   [itm_dale_warhorse,itm_dale_armor_l,itm_leather_boots,itm_leather_gloves,itm_dale_helmet_f,itm_dale_sword_long,itm_dale_shield_d,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_trainer_5,0x0000000e3f00018436db75b79b6eb6db00000000001db6eb0000000000000000],
["dwarf_lord","King_Dain_II_Ironfoot","King",tf_hero| tf_dwarf| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_armor_c,itm_dwarf_scale_boots,itm_mail_mittens,itm_dwarf_helm_p,itm_dwarf_throwing_axe,itm_dwarf_great_axe,],
      attr_dwarf_tier_6,wp_dwarf_tier_6,knight_skills_5|knows_riding_10|knows_trainer_4,0x0000000e7f00210133c16e7bb1fffdff00000000001f56f30000000000000000],
["dunland_lord","Chief_Daeglaf_the_Black","Chief",tf_hero| tf_dunland| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_dunland,
   [itm_saddle_horse,itm_dunland_armor_k,itm_dunland_wolfboots,itm_evil_gauntlets_a,itm_dun_helm_e,itm_dun_berserker,itm_dun_shield_b,itm_dunland_javelin,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_trainer_6,0x000000003f0051c721dc6c71580f36ff00000000001fd2e80000000000000000],
["beorn_lord","Chief_Grimbeorn_the_Old","Chief",tf_hero| tfg_shield| tfg_armor| tfg_helm|tfg_boots,0,0,fac_beorn,
   [itm_beorn_chief,itm_leather_boots,itm_mail_mittens,itm_beorn_helmet,itm_beorn_axe,itm_dwarf_throwing_axe,itm_beorn_shield,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_trainer_4,0x0000000d6a00628918d46a72d946e7ae00000000001eeeb90000000000000000],
 

 # marshalls which are not also leaders
["lorien_marshall","Celeborn","_",tf_hero| tf_lorien| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_lorien,
   [itm_mearas_reward,itm_lorien_royal_armor,itm_lorien_boots,itm_leather_gloves,itm_riv_tiara,itm_lorien_bow,itm_elven_arrows,itm_lorien_sword_a,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_5|knows_trainer_4,0x00000008120000024b146a491440e12400000000001cc4ad0000000000000000],

# ["gondor_marshall","Gondor Marshall","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   # [itm_gondor_warhorse,itm_pel_leader,itm_pelargir_greaves,itm_mail_mittens,itm_pelargir_helmet_heavy,itm_pelargir_sword,itm_gondor_bow,itm_gondor_arrows,],
      # attr_tier_6,wp_tier_6,knight_skills_4|knows_trainer_1|knows_trainer_3,0x00000006ff003004225b8ac89c62d2f400000000001ec8f90000000000000000],

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
["knight_1_1","Angbor","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gondor_lam_horse,itm_lamedon_leader_surcoat_cloak,itm_gondor_heavy_greaves,itm_mail_mittens,itm_gondor_lamedon_leader_helm,itm_gondor_citadel_sword,],
      attr_tier_6,wp_tier_6,knight_skills_4|knows_trainer_1|knows_trainer_3,0x00000008bf00524435d36db7536db6db00000000001db6dd0000000000000000],
["knight_1_2","Baranor","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gondor_lam_horse,itm_gon_leader_surcoat_cloak,itm_gondor_heavy_greaves,itm_mail_mittens,itm_gondor_leader_helm,itm_gondor_citadel_sword,],
      attr_tier_6,wp_tier_6,knight_skills_5,0x00000007f700550919da9135148e24e500000000001db9110000000000000000],
["knight_1_3","Prince_Imrahil","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_dol_amroth_warhorse,itm_dol_very_heavy_mail,itm_gondor_heavy_greaves,itm_mail_mittens,itm_swan_knight_helm,itm_gondor_citadel_sword,],
      attr_tier_6,wp_tier_6,knight_skills_5,0x0000000e7f00259419da9135148e24e500000000001db9110000000000000000],
["knight_1_4","Orthalion","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gondor_warhorse,itm_pel_leader,itm_pelargir_greaves,itm_mail_mittens,itm_pelargir_helmet_heavy,itm_pelargir_sword],
      attr_tier_6,wp_tier_6,knight_skills_4,0x0000000fff0035d218946ec91266652b00000000001cc6f90000000000000000],
["knight_1_5","Duinhir","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gondor_warhorse,itm_blackroot_leader,itm_gondor_heavy_greaves,itm_mail_mittens,itm_gondor_leader_helm,itm_gondor_citadel_sword,itm_gondor_bow,itm_gondor_arrows,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_horse_archery_7|knows_power_draw_7,0x000000003f0021544b246a471b65572400000000001cc6ed0000000000000000],
["knight_1_6","Hirluin_the_Fair","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gondor_warhorse,itm_pinnath_leader,itm_gondor_heavy_greaves,itm_mail_mittens,itm_gondor_leader_helm,itm_gondor_citadel_sword,],
      attr_tier_6,wp_tier_6,knight_skills_3,0x000000043a0020944aa46a451261533300000000001ec6af0000000000000000],
["knight_1_7","Faramir","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gondor_courser,itm_gon_leader_surcoat_cloak,itm_gondor_heavy_greaves,itm_mail_mittens,itm_gondor_leader_helm,itm_gondor_citadel_sword,itm_gondor_bow,itm_ithilien_arrows,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_horse_archery_7|knows_power_draw_7,0x000000043f00200f49248ac99481d72c00000000001d48de0000000000000000],
["knight_1_8","Forlong_the_Fat","_",tf_hero| tf_gondor| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gondor,
   [itm_gondor_warhorse,itm_lossarnach_leader,itm_lossarnach_greaves,itm_mail_mittens,itm_mordor_helm,itm_gondor_citadel_sword,itm_loss_axe,itm_loss_throwing_axes,],
      attr_tier_6,wp_tier_6,knight_skills_3|knows_power_throw_7,0x00000008b70052935b1b8f4ae9ee793e00000000001f4cad0000000000000000],
#Rohan
["knight_1_9","Grimbold","_",tf_hero| tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_warhorse,itm_rohan_armor_s,itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_captain_helmet,itm_rohirrim_long_hafted_axe,itm_strong_bow,itm_khergit_arrows,itm_rohan_shield_g,],
      attr_tier_6,wp_tier_6,knight_skills_4,0x0000000e7f0002c313da5e3993abcd3400000000001da6f30000000000000000],
["knight_1_10","Erkenbrand","_",tf_hero| tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_warhorse,itm_rohan_armor_s,itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_captain_helmet,itm_rohirrim_long_hafted_axe,itm_rohirrim_throwing_axe,itm_rohan_shield_g],
      attr_tier_6,wp_tier_6,knight_skills_5,0x0000000dbf00334521c0723588aacd3700000000001c96db0000000000000000],
["knight_1_11","Elfhelm","_",tf_hero| tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_warhorse,itm_rohan_armor_s,itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_captain_helmet,itm_rohirrim_long_hafted_axe,itm_rohirrim_throwing_axe,],
      attr_tier_6,wp_tier_6,knight_skills_1,0x0000000d8e002282211a8ce5aafd4eff00000000001cb45b0000000000000000],
["knight_1_12","Hama","_",tf_hero| tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_warhorse,itm_rohan_armor_s,itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_captain_helmet,itm_rohirrim_long_hafted_axe,itm_rohirrim_throwing_axe,],
      attr_tier_6,wp_tier_6,knight_skills_2,0x0000000aa500124421188e67da1fcf3f00000000001cb4730000000000000000],
["knight_1_13","Gamling","_",tf_hero| tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_warhorse,itm_rohan_armor_s,itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_captain_helmet,itm_rohirrim_long_hafted_axe,itm_rohirrim_throwing_axe,],
      attr_tier_6,wp_tier_6,knight_skills_3,0x0000000fff00034220d88d77ea1fc10000000000001cb4730000000000000000],
["knight_1_14","Éomer","_",tf_hero| tf_rohan| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_rohan,
   [itm_rohan_warhorse,itm_rohan_armor_s,itm_rohirrim_war_greaves,itm_mail_mittens,itm_rohan_captain_helmet,itm_rohirrim_long_hafted_axe,itm_rohirrim_throwing_axe,],
      attr_tier_6,wp_tier_6,knight_skills_4,0x0000000033001045055d5db565a9c73500000000001db6f90000000000000000],
#Isengard
["knight_1_15","Ugluk","_",tf_hero| tf_uruk |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_isengard,
   [itm_isen_uruk_heavy_c,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_isen_uruk_helm_d,itm_isengard_hammer,itm_isen_uruk_shield_b,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_trainer_3,0x0000000026000004003da293b938671800000000000000000000000000000000],
["knight_1_16","Mauhur","_",tf_hero| tf_uruk |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_isengard,
   [itm_isen_uruk_heavy_c,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_isen_uruk_helm_d,itm_isengard_hammer,itm_isen_uruk_shield_b,],
      attr_tier_6,wp_tier_6,knight_skills_3,0x0000000026000143003f171a07063a1300000000000000000000000000000000],
["knight_1_17","Mog_the_Seven-fingered","_",tf_hero| tf_urukhai |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_isengard,
   [itm_isen_uruk_heavy_c,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_isen_uruk_helm_d,itm_isengard_hammer,itm_isen_uruk_shield_b,],
      attr_tier_6,wp_tier_6,knight_skills_2,0x0000000740000140003f9f9a3fdad74d00000000000000000000000000000000],
["knight_1_18","Hushnak_Longshanks","_",tf_hero| tf_urukhai |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_isengard,
   [itm_isen_uruk_heavy_c,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_isen_uruk_helm_d,itm_isengard_hammer,itm_isen_uruk_shield_b,],
      attr_tier_6,wp_tier_6,knight_skills_3|knows_trainer_4,0x00000004c400120300384eb95df2446200000000000000000000000000000000],
["knight_1_19","Gridash the Tree-biter","_",tf_hero| tf_urukhai |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_isengard,
   [itm_isen_uruk_heavy_c,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_isen_uruk_helm_d,itm_isengard_hammer,itm_isen_uruk_shield_b,],
      attr_tier_6,wp_tier_6,knight_skills_4|knows_trainer_6,0x00000004fa000046003e72470fba445400000000000000000000000000000000],
["knight_1_20","Gronk the Man-eater","_",tf_hero| tf_urukhai |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_isengard,
   [itm_isen_uruk_heavy_c,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_isen_uruk_helm_d,itm_isengard_hammer,itm_isen_uruk_shield_b,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_trainer_5,0x00000004f2001185003a4e4b5475450200000000000000000000000000000000],
#Mordor
["knight_2_1","Captain_Mortakh","_",tf_hero| tf_evil_man| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_mordor,
   [itm_mordor_warhorse2,itm_m_cap_armor,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_mordor_cap_helm,itm_mordor_longsword,itm_mordor_man_shield_b,],
      attr_tier_6,wp_tier_6,knight_skills_1|knows_trainer_3,0x0000000cff00150f21c38927434e804f00000000001d24be0000000000000000],
["knight_2_2","Berúthiel","_",tf_hero| tf_female| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_mordor,
   [itm_mordor_warhorse2,itm_m_cap_armor,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_mordor_cap_helm,itm_mordor_longsword,itm_mordor_man_shield_b,],
      attr_tier_6,wp_tier_6,knight_skills_2,0x0000000ebf0010060df26111c003815400000000001c5e380000000000000000],
["knight_2_3","Skang","_",tf_hero| tf_uruk |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,
   [itm_m_uruk_heavy_k,itm_m_uruk_heavy_k,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_uruk_helm_f,itm_mordor_longsword,itm_mordor_uruk_shield_c,],
      attr_tier_6,wp_tier_6,knight_skills_3,0x000000003f002580204175274345004f00000000001d24380000000000000000],
["knight_2_4","Pharakhâd_The_Bastard","_",tf_hero| tf_evil_man| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_mordor,
   [itm_mordor_warhorse2,itm_m_cap_armor,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_mordor_cap_helm,itm_mordor_longsword,itm_mordor_man_shield_b,],
      attr_tier_6,wp_tier_6,knight_skills_4,0x0000000f0d0001143586a83dc22382c600000000001cd8e00000000000000000],
["knight_2_5","Grishnakh","_",tf_hero| tf_uruk |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,
   [itm_m_uruk_heavy_k,itm_m_uruk_heavy_k,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_uruk_helm_f,itm_mordor_longsword,itm_mordor_uruk_shield_c,],
      attr_tier_6,wp_tier_6,knight_skills_5,0x00000000260000870038a005c03c5f7000000000000000000000000000000000],
["knight_2_51","Gothmog","Lieutenant",tf_hero| tf_uruk| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,
   [itm_m_uruk_heavy_k,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_uruk_helm_f,itm_mordor_uruk_shield_c,itm_mordor_longsword,],
      attr_tier_6,wp_tier_6,knight_skills_5|knows_trainer_4,0x000000002c000104003fb3f407b83d0d00000000000000000000000000000000],
#Harad
["knight_2_6","Chieftain_Karna_the_Lion","_",tf_hero| tf_harad| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,
   [itm_harad_warhorse,itm_harad_lion_scale,itm_harad_leather_greaves,itm_evil_gauntlets_a,itm_harad_dragon_helm,itm_harad_khopesh,itm_harad_long_shield_c,],
      attr_tier_6,wp_tier_6,knight_skills_1|knows_trainer_3,0x00000009ff00300b1415a5f77872f7b700000000001d663b0000000000000000],
["knight_2_7","Chieftain_Na’man","_",tf_hero| tf_harad| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,
   [itm_harad_warhorse,itm_harad_heavy,itm_harad_leather_greaves,itm_evil_gauntlets_a,itm_harad_dragon_helm,itm_harad_khopesh,itm_harad_long_shield_c,],
      attr_tier_6,wp_tier_6,knight_skills_2|knows_trainer_4,0x000000003f00000f20a8b7f9e87ff1b700000000001c3ab80000000000000000],
["knight_2_8","Chieftain_Haarith","_",tf_hero| tf_harad| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_harad,
   [itm_harad_warhorse,itm_harad_tiger_scale,itm_harad_leather_greaves,itm_evil_gauntlets_a,itm_harad_dragon_helm,itm_harad_khopesh,itm_harad_long_shield_c,],
      attr_tier_6,wp_tier_6,knight_skills_2|knows_trainer_4,0x000000003f00100421526ff7708d22f700000000001fea200000000000000000],
# ["knight_2_9","Harad_Chieftain","_",tf_hero,0,reserved,fac_harad,[itm_saddle_horse,itm_rich_outfit,itm_mail_hauberk,itm_leather_boots,itm_mail_boots,itm_mail_mittens,itm_two_handed_axe,itm_shield_heater_c],knight_attrib_4,wp(230),knight_skills_4,0x0000000c160451d2136469c4d9b159ad00000000001e28f10000000000000000,vaegir_face_older_2],
# ["knight_2_10","Harad_Lieutenant","_",tf_hero,0,reserved,fac_harad,[itm_warhorse,itm_fur_coat,itm_mail_hauberk,itm_leather_boots,itm_mail_boots,itm_mail_mittens,itm_shield_heater_c],knight_attrib_5,wp(260),knight_skills_5|knows_trainer_6,0x0000000f7c00520e66b76edd5cd5eb6e00000000001f691e0000000000000000,vaegir_face_older_2],
#Rhun
["knight_2_11","Kusulak","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_horse_g,itm_rhun_armor_k,itm_furry_boots,itm_evil_gauntlets_a,itm_rhun_helm_o,itm_rhun_greatsword,itm_rhun_bull3_shield,],
      attr_tier_6,wp_tier_6,knight_skills_1,0x0000000fff0093c213f746f5e363f35b00000000001de22a0000000000000000],
["knight_2_12","Ulwarth the Balchoth","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_horse_g,itm_rhun_armor_k,itm_furry_boots,itm_evil_gauntlets_a,itm_rhun_helm_o,itm_rhun_greatsword,itm_rhun_bull3_shield,],
      attr_tier_6,wp_tier_6,knight_skills_1,0x0000000e8000410b145546b3695b677b00000000001ee6aa0000000000000000],
["knight_2_13","Brodda","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_horse_g,itm_rhun_armor_k,itm_furry_boots,itm_evil_gauntlets_a,itm_rhun_helm_o,itm_rhun_greatsword,itm_rhun_bull3_shield,],
      attr_tier_6,wp_tier_6,knight_skills_1,0x0000000c1b007303201c6fd3a36f3ff300000000001d66e80000000000000000],
#Khand
["knight_2_16","Torask","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_khand,
   [itm_variag_kataphrakt,itm_khand_noble_lam,itm_variag_greaves,itm_evil_gauntlets_a,itm_khand_tulwar,itm_easterling_round_horseman,],
      attr_tier_6,wp_tier_6,knight_skills_1,0x0000000ac800d5400bf7d3f5fb9179ff00000000001f62fc0000000000000000],
["knight_2_17","Lurmsakun","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_evil_man,0,0,fac_khand,
   [itm_variag_kataphrakt,itm_khand_noble_lam,itm_variag_greaves,itm_evil_gauntlets_a,itm_khand_tulwar,itm_easterling_round_horseman,],
      attr_tier_6,wp_tier_6,knight_skills_1,0x0000000d3f00c40812065fd328ff7bfc00000000001ce6b80000000000000000],
#Umbar
["knight_3_1","Captain_Morbir","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_umbar,
   [itm_umb_armor_h,itm_umb_armor_h,itm_corsair_boots,itm_corsair_boots,itm_leather_gloves,itm_umb_helm_f,itm_corsair_bow,itm_corsair_arrows,itm_umbar_rapier,],
      attr_tier_6,wp_tier_6,knight_skills_1|knows_trainer_3|knows_power_draw_4,0x0000000eb10063c8365369b99b6f77df00000000001d5aeb0000000000000000],
["knight_3_2","Captain_Angamaitë","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_umbar,
   [itm_umb_armor_h,itm_umb_armor_h,itm_corsair_boots,itm_corsair_boots,itm_leather_gloves,itm_umb_helm_f,itm_corsair_bow,itm_corsair_arrows,itm_umbar_rapier,],
      attr_tier_6,wp_tier_6,knight_skills_2|knows_power_draw_4,0x000000093f0035c5300251e9b3e041df00000000001cfaeb0000000000000000],
["knight_3_3","Captain_Sangahyando","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_umbar,
   [itm_umb_armor_h,itm_umb_armor_h,itm_corsair_boots,itm_corsair_boots,itm_leather_gloves,itm_umb_helm_f,itm_corsair_bow,itm_corsair_arrows,itm_umbar_rapier,],
      attr_tier_6,wp_tier_6,knight_skills_2|knows_power_draw_4,0x000000093f004045300251e9b3e2f7df00000000001dbaab0000000000000000],
#Lothlorien
["knight_3_6","Haldir","_",tf_hero| tf_lorien| tf_mounted| tfg_ranged |tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_lorien,
   [itm_lorien_warhorse,itm_lorien_royal_armor,itm_riv_tiara,itm_lorien_boots,itm_leather_gloves,itm_lorien_bow,itm_elven_arrows,itm_lorien_sword_a,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_1|knows_power_draw_4,0x00000006470010023b1d6e351240e36d00000000001cd8ec0000000000000000],
["knight_3_7","Orophin","_",tf_hero| tf_lorien| tf_mounted| tfg_ranged |tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_lorien,
   [itm_lorien_warhorse,itm_lorien_royal_armor,itm_riv_tiara,itm_lorien_boots,itm_leather_gloves,itm_lorien_bow,itm_elven_arrows,itm_lorien_sword_a,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_1|knows_power_draw_4,0x00000006470010023b1d6e351240e36d00000000001cd8ec0000000000000000],
#Imladris
["knight_3_11","Elladan","_",tf_hero| tf_imladris| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_imladris,
   [itm_mearas_reward,itm_riv_tiara,itm_riv_armor_leader,itm_riv_boots,itm_leather_gloves,itm_riv_bow,itm_elven_arrows,itm_riv_bas_sword,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_1|knows_power_draw_4,0x000000067f0030021ae66e471560632400000000001c58f20000000000000000],
["knight_3_12","Elrohir","_",tf_hero| tf_imladris| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_imladris,
   [itm_mearas_reward,itm_riv_tiara,itm_riv_armor_leader,itm_riv_boots,itm_leather_gloves,itm_riv_bow,itm_elven_arrows,itm_riv_bas_sword,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_2|knows_power_draw_4,0x00000003fa0030063d256e471644555c00000000001ce8720000000000000000],
["knight_3_13","Halbarad","_",tf_hero| tf_dunedain| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_imladris,
   [itm_arnor_greaves,itm_mail_mittens,itm_lance,itm_arnor_armor_f,itm_arnor_sword_c,itm_arnor_shield_c,itm_dunedain_helm_b,itm_arnor_warhorse,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_2|knows_power_draw_4,0x00000008a400224736db6db75b6db6db00000000001db6db0000000000000000],
#Woodelves
["knight_3_16","Miriel","_",tf_hero| tf_female| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_woodelf,
   [itm_riv_tiara,itm_mirkwood_armor_f,itm_mirkwood_leather_greaves,itm_leather_gloves,itm_mirkwood_helm_d,itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_sword,itm_mirkwood_spear_shield_c,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_1|knows_power_draw_4,0x0000000fc000400c055d7066cb87e08300000000001d44c30000000000000000],
["knight_3_17","Gladvaethor","_",tf_hero| tf_woodelf| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_woodelf,
   [itm_riv_tiara,itm_mirkwood_armor_f,itm_mirkwood_leather_greaves,itm_leather_gloves,itm_mirkwood_helm_d,itm_mirkwood_bow,itm_woodelf_arrows,itm_mirkwood_sword,itm_mirkwood_spear_shield_c,],
      attr_elf_tier_6,wp_elf_tier_6,knight_skills_1|knows_power_draw_4,0x0000000fc00030023fc36db75b6ab6db00000000001d36db0000000000000000],
#Moria
["knight_4_1","Whip_Snog","_",tf_hero| tf_orc| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_moria,
   [itm_wargarmored_3a,itm_moria_armor_e,itm_moria_armor_e,itm_evil_gauntlets_a,itm_orc_helm_c,itm_orc_throwing_axes,itm_orc_slasher,],
      attr_orc_tier_6,wp_orc_tier_6,knight_skills_1|knows_leadership_10,0x0000000fff00100936db6db6db6db6db00000000001db6db0000000000000000],
["knight_4_2","Whip_Snotgor","_",tf_hero| tf_orc| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_moria,
   [itm_wargarmored_3a,itm_moria_armor_e,itm_moria_armor_e,itm_evil_gauntlets_a,itm_orc_helm_c,itm_orc_throwing_axes,itm_orc_slasher,],
      attr_orc_tier_6,wp_orc_tier_6,knight_skills_1|knows_leadership_10,0x000000087f00000e36db6db6db6db6db00000000001db6db0000000000000000],
#Dol Guldur
["knight_4_6","General_Tuskim","_",tf_hero| tf_uruk |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_guldur,
   [itm_m_uruk_heavy_k,itm_m_uruk_heavy_k,itm_uruk_chain_greaves,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_uruk_helm_f,itm_mordor_uruk_shield_c,itm_mordor_longsword,],
      attr_tier_6,wp_tier_6,knight_skills_2|knows_trainer_4|knows_leadership_10,0x000000018000210700389ff43fdbff4500000000000000000000000000000000],
["knight_4_7","General_Mugslag","_",tf_hero| tf_uruk |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_guldur,
   [itm_m_uruk_heavy_k,itm_m_uruk_heavy_k,itm_uruk_chain_greaves,itm_uruk_chain_greaves,itm_evil_gauntlets_a,itm_uruk_helm_f,itm_mordor_uruk_shield_c,itm_mordor_longsword,],
      attr_tier_6,wp_tier_6,knight_skills_2|knows_trainer_4|knows_leadership_10,0x00000001800011c4003f1c65b8cdb6db00000000000000000000000000000000],
#Northmen
["knight_4_11","Beranhelm","_",tf_hero |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,
   [itm_beorn_chief,itm_beorn_chief,itm_leather_boots,itm_leather_gloves,itm_beorn_helmet,itm_beorn_axe,itm_dwarf_throwing_axe,itm_beorn_shield,],
      attr_tier_6,wp_tier_6,knight_skills_1,0x0000000b260022493f596db9df7b7e7f00000000001f47530000000000000000],
["knight_4_12","Beranor_Blackfur","_",tf_hero |tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_beorn,
   [itm_beorn_chief,itm_beorn_chief,itm_leather_boots,itm_leather_gloves,itm_beorn_helmet,itm_beorn_axe,itm_dwarf_throwing_axe,itm_beorn_shield,],
      attr_tier_6,wp_tier_6,knight_skills_1,0x0000000bbf0052894dd95757a55accff00000000001d29190000000000000000],
#Mt. Gundabad
["knight_4_16","Whip_Brolgukhsh","_",tf_hero| tf_orc| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gundabad,
   [itm_wargarmored_3a,itm_gundabad_armor_e,itm_orc_greaves,itm_orc_greaves,itm_orc_ragwrap,itm_evil_gauntlets_a,itm_gundabad_helm_e,itm_orc_throwing_axes,itm_orc_slasher,],
      attr_orc_tier_6,wp_orc_tier_6,knight_skills_1|knows_leadership_10,0x0000000fc000000536db6db6db6db6db00000000001db6db0000000000000000],
["knight_4_17","Whip_Grumrunt","_",tf_hero| tf_orc| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gundabad,
   [itm_wargarmored_3a,itm_gundabad_armor_e,itm_orc_greaves,itm_orc_greaves,itm_orc_ragwrap,itm_evil_gauntlets_a,itm_gundabad_helm_e,itm_orc_throwing_axes,itm_orc_slasher,],
      attr_orc_tier_6,wp_orc_tier_6,knight_skills_1|knows_leadership_10,0x00000009bf00000736db6db6db6db6db00000000001db6db0000000000000000],
["knight_4_18","Whip_Grimsob","_",tf_hero| tf_orc| tf_mounted| tfg_ranged| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_gundabad,
   [itm_wargarmored_3a,itm_gundabad_armor_e,itm_orc_greaves,itm_orc_greaves,itm_orc_ragwrap,itm_evil_gauntlets_a,itm_gundabad_helm_e,itm_orc_throwing_axes,itm_orc_slasher,],
      attr_orc_tier_6,wp_orc_tier_6,knight_skills_1|knows_leadership_10,0x000000083f00200a36db6db6db6db6db00000000001db6db0000000000000000],
#Dale
["knight_5_1","Lord_Halward","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_dale,
   [itm_dale_warhorse,itm_dale_armor_l,itm_dale_armor_l,itm_leather_boots,itm_leather_boots,itm_leather_gloves,itm_dale_helmet_f,itm_dale_sword_long,itm_dale_shield_d,],
      attr_tier_6,wp_tier_6,knight_skills_1|knows_trainer_3,0x00000005e30024852ad48e24d660d52d00000000001d46ab0000000000000000],
["knight_5_2","Lord_Bard","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_dale,
   [itm_dale_warhorse,itm_dale_armor_l,itm_dale_armor_l,itm_leather_boots,itm_leather_boots,itm_leather_gloves,itm_dale_helmet_f,itm_dale_sword_long,itm_dale_shield_d,],
      attr_tier_6,wp_tier_6,knight_skills_1|knows_trainer_3,0x000000063f00004336db75b7ab6eb6b400000000001db6eb0000000000000000],
["knight_5_3","Lord_Esgarain","_",tf_hero| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_dale,
   [itm_dale_warhorse,itm_dale_armor_l,itm_dale_armor_l,itm_leather_boots,itm_leather_boots,itm_leather_gloves,itm_dale_helmet_f,itm_dale_sword_long,itm_dale_shield_d,],
      attr_tier_6,wp_tier_6,knight_skills_1|knows_trainer_3,0x00000008ef00008436db76b7ab6ef6b400000000001d26eb0000000000000000],
#Dwarven
["knight_5_6","Fulgni_Longbeard","_",tf_hero| tf_dwarf| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_armor_c,itm_dwarf_armor_c,itm_dwarf_scale_boots,itm_dwarf_scale_boots,itm_mail_mittens,itm_dwarf_helm_p,itm_dwarf_throwing_axe,itm_dwarf_great_axe,],
      attr_dwarf_tier_6,wp_dwarf_tier_6,knows_riding_10|knight_skills_1,0x00000001b000014258e46ec7d780e9fe00000000001ce4710000000000000000],
["knight_5_7","Thorin_Stonehelm","_",tf_hero| tf_dwarf| tfg_shield| tfg_armor| tfg_helm| tfg_boots,0,0,fac_dwarf,
   [itm_dwarf_armor_c,itm_dwarf_armor_c,itm_dwarf_scale_boots,itm_dwarf_scale_boots,itm_mail_mittens,itm_dwarf_helm_p,itm_dwarf_throwing_axe,itm_dwarf_great_axe,],
      attr_dwarf_tier_6,wp_dwarf_tier_6,knows_riding_10|knight_skills_1,0x00000009bf00510616936b596c56ddfe00000000001ecc780000000000000000],
#Dunland
["knight_5_11","Chief_Fudreim","_",tf_hero| tf_dunland| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_dunland,
   [itm_saddle_horse,itm_dunland_armor_k,itm_dunland_armor_k,itm_dunland_wolfboots,itm_dunland_wolfboots,itm_evil_gauntlets_a,itm_dun_helm_e,itm_dun_berserker,itm_dun_shield_b,itm_dunland_javelin,],
      attr_tier_6,wp_tier_6,knight_skills_1,0x0000000cbf00528736db6db71b6db6db00000000001fd6db0000000000000000],
["knight_5_12","Chief_Wulf","_",tf_hero| tf_dunland| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_dunland,
   [itm_saddle_horse,itm_dunland_armor_k,itm_dunland_armor_k,itm_dunland_wolfboots,itm_dunland_wolfboots,itm_evil_gauntlets_a,itm_dun_helm_e,itm_dun_berserker,itm_dun_shield_b,itm_dunland_javelin,],
      attr_tier_6,wp_tier_6,knight_skills_1,0x0000000e3b00324305f858f1606bbfff00000000001f7ce80000000000000000],

["heroes_end","bug","_",tf_hero,0,0,fac_neutral,
   [],
      0,0,0,0x000000000008318101f390c515555594],
#Healers
#["morannon_healer","Okstuk_the_healer","_",tf_hero,scn_tld_morannon_castle|entry(5),0,fac_isengard,[itm_leather_gloves,itm_isen_uruk_light_a,itm_leather_boots],str_15|agi_5|int_4|cha_4|level(2),wp(20),knows_common,orc_face1],
#["minas_tirith_healer","Ioreth","_",tf_female|tf_hero,scn_town_1_castle|entry(5),0,fac_gondor,[itm_white_robe,itm_leather_boots],def_attrib|level(2),wp(20),knows_common,0x10500501d14886db69d699],
#["edoras_healer","Freya_the_healer","_",tf_female|tf_hero,scn_town_11_castle|entry(5),0,fac_gondor,[itm_white_robe,itm_leather_boots],def_attrib|level(2),wp(20),knows_common,0x10500501d14886db69d699],
#["isengard_healer","Nurgal_the_patcher","_",tf_hero,scn_tld_isengard_castle|entry(5),0,fac_mordor,[itm_leather_gloves,itm_isen_uruk_light_a,itm_leather_boots],str_15|agi_5|int_4|cha_4|level(2),wp(20),knows_common,orc_face1],

# Weapon merchants
["smith_mtirith","Berethor_the_Smith","Steward's_smiths",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_pelargir","Hallatan_Metalmaster","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,subfac_pelargir,fac_gondor,
   [itm_leather_apron,itm_pelargir_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_linhir","Bor_the_Armorer","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_dolamroth","Haldad_the_Smith","Amroth_smiths",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,subfac_dol_amroth,fac_gondor,
   [itm_leather_apron,itm_dol_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_edhellond","Ryis_Ironbender","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_lossarnach","Berin_Axemaker","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,subfac_lossarnach,fac_gondor,
   [itm_leather_apron,itm_lossarnach_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_tarnost","Harandil_Steelhammer","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_erech","Lorne_the_Black","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_pinnath","Tarandil_Swordmaker","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,subfac_blackroot,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_eosgiliath","Bzurg_the_Looter","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_mordor,
   [itm_m_orc_light_e,itm_orc_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,orc_face_normal,orc_face2],
["smith_wosgiliath","Gardil","makeshift_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_calembel","Agronom","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,subfac_ethring,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_hannun","Fal_the_Ranger_Smith","ranger_gear_stash",tf_hero| tf_randomize_face| tf_is_merchant,0,subfac_rangers,fac_gondor,
   [itm_gon_ranger_cloak,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_candros","Kalimdor","smithy",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_gondor,
   [itm_gon_footman,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_1|knows_power_strike_1|knows_persuasion_1|knows_horse_archery_1|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_edoras","Eaoden_Steelmaster","King's_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_armor_c,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x00000008c80002c219248896a4b96b6300000000001e1af30000000000000000],
["smith_aldburg","Fulm_Ironhoof","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_armor_c,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000a22002341375b72ab4c6aba6500000000001f24e20000000000000000],
["smith_hornburg","Aldhelm","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_armor_c,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000a35003183479c6e12548f451400000000001f355e0000000000000000],
["smith_eastemnet","Eadfrid","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_armor_c,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000a10002282392cc9172d8dbb1b00000000001caa9d0000000000000000],
["smith_westfold","Deor_Helmmaker","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_armor_c,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000a100011c4444395aaec92c4c400000000001db6cd0000000000000000],
["smith_westemnet","Armourer","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_armor_c,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000a3b000281451d364924d5571400000000001e46a30000000000000000],
["smith_eastfold","Eaderan_Ironcarver","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_armor_c,itm_rohan_shoes,],
      def_attrib|level(2),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000a170000c12b1b8f499892995b00000000001e68e90000000000000000],
["smith_morannon","Hurbag_Gateforger","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_a,itm_uruk_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,orc_face_normal,orc_face2],
["smith_mmorgul","Orgurz_Firebelcher","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_a,itm_uruk_ragwrap,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,orc_face_normal,orc_face2],
["town_24_smith","Boz_Ironspoiler","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_mordor,
   [itm_m_uruk_light_b,itm_orc_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,orc_face_normal,orc_face2],
["smith_orc_patrol","Glugz_Ironfinger","camp_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_a,itm_uruk_tracker_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,orc_face_normal,orc_face2],
["smith_oscamp","Kugash_Ironlover","camp_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_isen_uruk_light_c,itm_uruk_tracker_boots,],
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
   [itm_lorien_armor_e,itm_lorien_boots,],
      def_attrib|level(2),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,lorien_elf_face_1,lorien_elf_face_2],
["smith_cdolen","Dimirian the Fletcher","elven_weaponmakers",tf_hero| tf_randomize_face| tf_is_merchant| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_e,itm_lorien_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,lorien_elf_face_1,lorien_elf_face_2],
["smith_camroth","Getasistan","elven_weaponmakers",tf_hero| tf_randomize_face| tf_is_merchant| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_e,itm_lorien_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,lorien_elf_face_1,lorien_elf_face_2],
["smith_thranduils_halls","Thurinor","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_armor_a,itm_mirkwood_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,lorien_elf_face_1,lorien_elf_face_2],
["smith_woodelf_camp","Calechir","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_armor_a,itm_mirkwood_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,lorien_elf_face_1,lorien_elf_face_2],
["smith_beorn","Beornalaf_Axemaker","smithy",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_beorn,
   [itm_beorn_tunic,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_moria","Burgak_Forger","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_moria,
   [itm_moria_armor_b,itm_orc_greaves,itm_orc_helm_c,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_dale","Ardel_Firehand","smithy",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_dale,
   [itm_dale_armor_l,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_esgaroth","Kelegarn_The_Bowyer","smithy",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_dale,
   [itm_dale_armor_l,itm_leather_boots,],
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
   [itm_khand_light_lam,itm_variag_greaves,],
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
["town_50_weaponsmith","Armourer","smithy",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_commoners,
   [itm_leather_apron,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,mercenary_face_1,mercenary_face_2],

["smith_gondor_ac","Bor_the_Armorer","camp_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_leather_apron,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_rohan_ac","Deor_Helmmaker","camp_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_rohan,0,0,fac_rohan,
   [itm_rohan_armor_c,itm_rohan_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_mordor_ac","Hurbag_Gateforger","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_a,itm_uruk_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,orc_face_normal,orc_face2],
["smith_isengard_ac","Burz_Ironbasher","underground_smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_light_c,itm_uruk_tracker_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],
["smith_lorien_ac","Dimirian the Fletcher","elven_weaponmakers",tf_hero| tf_randomize_face| tf_is_merchant| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_e,itm_lorien_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,lorien_elf_face_1,lorien_elf_face_2],
["smith_woodelf_ac","Dhoelath","smithy",tf_hero| tf_randomize_face| tf_is_merchant| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_armor_a,itm_mirkwood_boots,],
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
   [itm_khand_light_lam,itm_variag_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,0x0000000fff00d45213f7e6f1636172fb00000000001dc22a0000000000000000],
["smith_umbar_ac","Fuinir_the_Forger","smithy",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_umbar,
   [itm_umb_armor_e,itm_corsair_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_leadership_2|knows_power_strike_2|knows_persuasion_2|knows_horse_archery_2|knows_shield_4|knows_power_draw_2|knows_power_throw_2|knows_trade_4|knows_tactics_4|knows_ironflesh_4|knows_athletics_2|knows_looting_1,mercenary_face_1,mercenary_face_2],

#Tavern keepers   # in TLD, their plular name serves as city "Castle" name.
["barman_mtirith","Tavern_Keeper","the_Citadel",tf_hero| tf_randomize_face,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_pelargir","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_linhir","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face| tf_female,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],
["barman_dolamroth","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_edhellond","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face,0,0,fac_commoners, [],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_lossarnach","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face| tf_female,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],
["barman_tarnost","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face| tf_female,0,0,fac_commoners,   [],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],
["barman_erech","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face,0,0,fac_commoners,   [],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_pinnath","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face| tf_female,0,0,fac_commoners,   [],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],
["barman_hannun","Tavern_Keeper","the_Secret_Cave",tf_hero| tf_randomize_face| tf_female,0,0,fac_commoners,   [],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],
["barman_calembel","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face| tf_female,0,0,fac_commoners, [],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],
["barman_edoras","Tavern_Keeper","Meduseld,_the_Golden_Hall",tf_hero| tf_randomize_face,0,0,fac_commoners, [],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_aldburg","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face| tf_female,0,0,fac_commoners, [],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],
["barman_hornburg","Tavern_Keeper","the_Lord_Halls",tf_hero| tf_randomize_face,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
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
["barman_cungol","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face| tf_uruk,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_isengard","Tavern_Keeper","the_tower_of_Orthanc",tf_hero| tf_randomize_face| tf_urukhai,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],
["barman_cgaladhon","Tavern_Keeper","the_Tree_castle",tf_hero| tf_randomize_face| tf_lorien,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_cdolen","Tavern_Keeper","the_Tree_castle",tf_hero| tf_randomize_face| tf_lorien,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_camroth","Tavern_Keeper","the_Tree_castle",tf_hero| tf_randomize_face| tf_lorien,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],
["barman_thalls","Tavern_Keeper","the_Throne_Room",tf_hero| tf_randomize_face| tf_woodelf,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_beorn","Tavern_Keeper","Beorn_House",tf_hero| tf_randomize_face| tf_female,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],
["barman_moria","Tavern_Keeper","the_Chief's_Chamber",tf_hero| tf_randomize_face| tf_orc,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],
["barman_dale","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["barman_esgaroth","Tavern_Keeper","the_Hall",tf_hero| tf_randomize_face| tf_female,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],
["barman_erebor","Tavern_Keeper","the_Lord's_Chamber",tf_hero| tf_randomize_face| tf_dwarf,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],
["barman_dolguldur","Tavern_Keeper","the_Castle",tf_hero| tf_randomize_face| tf_uruk,0,0,fac_commoners,[],
      def_attrib|level(2),wp(20),knows_common,woman_face_1,woman_face_2],
#Goods Merchants
#["town_1_merchant","Merchant","bug",tf_hero|tf_randomize_face|tf_is_merchant,scn_town_store|entry(9),0,fac_commoners,[itm_short_tunic,itm_leather_boots                   ],def_attrib|level(2),wp(20),knows_inventory_management_10,man_face_young_1,man_face_older_2],
#["town_2_merchant","Merchant","bug",tf_hero|tf_randomize_face|tf_is_merchant,scn_town_2_store|entry(9),0,fac_commoners,[itm_leather_apron,itm_leather_boots                   ],def_attrib|level(2),wp(20),knows_inventory_management_10,man_face_young_1,man_face_older_2],
#["salt_mine_merchant","Barezan","Barezan",tf_hero|tf_is_merchant,scn_salt_mine|entry(1),0,fac_commoners,[itm_leather_apron,itm_leather_boots],def_attrib|level(2),wp(20),knows_inventory_management_10,0x00000000000c528601ea69b6e46dbdb6],
# Horse Merchants
["merchant_mtirith","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_gon_jerkin,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_inventory_management_10|knows_riding_6,woman_face_1,woman_face_2],
["merchant_pelargir","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,subfac_pelargir,fac_gondor,
   [itm_pel_jerkin,itm_pelargir_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_3,man_face_young_1,man_face_older_2],
["merchant_linhir","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_lamedon_clansman,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,man_face_young_1,man_face_older_2],
["merchant_dolamroth","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,subfac_dol_amroth,fac_gondor,
   [itm_dol_shirt,itm_dol_shoes,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_3,man_face_young_1,man_face_older_2],
["merchant_edhellond","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_gon_jerkin,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,man_face_young_1,man_face_older_2],
["merchant_lossarnach","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,subfac_lossarnach,fac_gondor,
   [itm_lossarnach_shirt,itm_lossarnach_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,man_face_young_1,man_face_older_2],
["merchant_tarnost","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_gon_jerkin,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_5,man_face_young_1,man_face_older_2],
["merchant_erech","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,subfac_blackroot,fac_gondor,
   [itm_blackroot_bowman,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,man_face_young_1,man_face_older_2],
["merchant_pinnath","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,subfac_pinnath_gelin,fac_gondor,
   [itm_pinnath_footman,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,0x0000000c2900555235d36db7536db6db00000000001db6dd0000000000000000],
["merchant_eosgiliath","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_mordor,
   [itm_m_orc_heavy_a,itm_orc_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_1,man_face_young_1,man_face_older_2],
["merchant_wosgiliath","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_gon_footman,itm_gondor_med_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,man_face_young_1,man_face_older_2],
["town_12_horse_merchant","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_gon_jerkin,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,man_face_young_1,man_face_older_2],
["town_13_horse_merchant","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,0,fac_gondor,
   [itm_lamedon_clansman,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,man_face_young_1,man_face_older_2],
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
["merchant_isengard","Supply_Master","camp_stash",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_a,itm_orc_ragwrap,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,man_face_young_1,man_face_older_2],
["town_27_horse_merchant","Supply_Master","warg_pit_and_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,man_face_young_1,man_face_older_2],
["merchant_uoutpost","Supply_Master","warg_pit_and_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_3,man_face_young_1,man_face_older_2],
["merchant_uhcamp","Supply_Master","warg_pit_and_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_3,man_face_young_1,man_face_older_2],
["merchant_urcamp","Supply_Master","warg_pit_and_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,man_face_young_1,man_face_older_2],
["merchant_cgaladhon","Supply_Master","elven_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_e,itm_lorien_boots,],
      def_attrib|level(2),wp(20),knows_inventory_management_10|knows_riding_3,lorien_elf_face_1,lorien_elf_face_2],
["merchant_cdolen","Supply_Master","elven_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_e,itm_lorien_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_1,lorien_elf_face_1,lorien_elf_face_2],
["merchant_camroth","Supply_Master","elven_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_e,itm_lorien_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,lorien_elf_face_1,lorien_elf_face_2],
["merchant_thranduils_halls","Supply_Master","elven_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_armor_d,itm_mirkwood_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,lorien_elf_face_1,lorien_elf_face_2],
["merchant_woodelf_camp","Supply_Master","elven_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_armor_d,itm_mirkwood_boots,],
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
   [itm_dale_armor_l,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,man_face_young_1,man_face_older_2],
["merchant_erebor","Supply_Master","Dwarven_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_dwarf,0,0,fac_dwarf,
   [itm_dwarf_armor_a,itm_dwarf_pad_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_1,man_face_young_1,man_face_older_2],
["merchant_dunland","Dun_Stash_Master","camp_stash",tf_hero| tf_dunland| tf_is_merchant,0,0,fac_dunland,
   [itm_dunland_armor_h,itm_dunland_wolfboots,],
      def_attrib|level(2),wp(20),knows_inventory_management_10|knows_riding_2,0x000000003f00520137da6c7bd86f36db00000000001e42f80000000000000000],
["merchant_harad","Harad_Stash_Master","camp_stash",tf_hero| tf_randomize_face| tf_is_merchant| tf_harad,0,0,fac_harad,
   [itm_harad_padded,itm_harad_scale_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_4,man_face_young_1,man_face_older_2],
["merchant_khand","Khand_Stash_Master","camp_stash",tf_hero| tf_is_merchant| tf_evil_man,0,0,fac_khand,
   [itm_khand_foot_lam_c,itm_variag_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_3,0x0000000fff0093c213f746f5e363f35b00000000001de22a0000000000000000],
["merchant_umbar","Supply_Master","camp_stash",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_umbar,
   [itm_umb_armor_a,itm_corsair_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_1,man_face_young_1,man_face_older_2],
["merchant_imladris","Supply_Master","camp_supplies",tf_hero| tf_is_merchant,0,0,fac_imladris,
   [itm_arnor_armor_c,itm_arnor_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,0x0000000af700414719da9135148aa8d300000000001db9110000000000000000],
["merchant_dolguldur","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_uruk,0,0,fac_guldur,
   [itm_m_uruk_heavy_c,itm_orc_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_2,man_face_young_1,man_face_older_2],
["merchant_north_rhun","Supply_Master","camp_stash",tf_hero| tf_is_merchant| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_armor_p,itm_furry_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,0x00000009bf00324113fe9bf7ee397d7f00000000001d75390000000000000000],
["merchant_south_rhun","Supply_Master","camp_stash",tf_hero| tf_is_merchant| tf_evil_man,0,0,fac_rhun,
   [itm_rhun_armor_p,itm_furry_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,0x000000092c00528839fe9b55db52f37f00000000001ee73b0000000000000000],
["merchant_gundabad","Supply_Master","camp_stash",tf_hero| tf_randomize_face| tf_is_merchant| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_d,itm_orc_furboot_tall,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,man_face_young_1,man_face_older_2],
["merchant_ironhill","Supply_Master","Dwarven_supplies",tf_hero| tf_randomize_face| tf_is_merchant| tf_dwarf,0,0,fac_dwarf,
   [itm_dwarf_armor_a,itm_dwarf_pad_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_1,dwarf_face_3,dwarf_face_4],
["town_50_horse_merchant","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_female,0,0,fac_gondor,
   [itm_leather_jerkin,itm_leather_boots,],
      def_attrib|level(5),wp(20),knows_inventory_management_10,woman_face_1,woman_face_2],
["merchant_calembel","Supply_Master","stable_and_warehouse",tf_hero| tf_randomize_face| tf_is_merchant| tf_gondor,0,subfac_ethring,fac_gondor,
   [itm_lamedon_clansman,itm_gondor_light_greaves,],
      def_attrib|level(5),wp(20),knows_inventory_management_10|knows_riding_6,man_face_young_1,man_face_older_2],
#
["elder_mtirith","Tirith_Guildmaster","the_White_City",tf_hero| tf_gondor| tf_randomize_face,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_pelargir","Sailor_Guildmaster","the_city",tf_hero| tf_gondor| tf_randomize_face,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_pelargir_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_linhir","Linhir_Guildmaster","the_city",tf_hero| tf_gondor| tf_randomize_face,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_dolamroth","Dol_Amroth_Guildmaster","the_city",tf_hero| tf_gondor| tf_randomize_face,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_dol_shoes,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_edhellond","Edhellond_Guildmaster","the_city",tf_hero| tf_gondor| tf_randomize_face,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_lossarnach","Lossarnach_Guildmaster","the_town",tf_hero| tf_gondor| tf_randomize_face,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_tarnost","Tarnost_Guildmaster","the_town",tf_hero| tf_gondor| tf_randomize_face,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_erech","Erech_Guildmaster","the_town",tf_hero| tf_gondor| tf_randomize_face,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_pinnath","Pinnath_Tribe_Elder","the_town",tf_hero| tf_gondor| tf_randomize_face,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_ethring","Calembel_Guildmaster","the_city",tf_hero| tf_gondor| tf_randomize_face,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_henneth","Ranger_Guildmaster","the_hideout",tf_hero| tf_gondor| tf_randomize_face,0,0,fac_gondor,
   [itm_gon_ranger_skirt,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_cairandros","Cair_Andros_Guildmaster","the_island_fortress",tf_hero| tf_gondor| tf_randomize_face,0,0,fac_gondor,
   [itm_gon_ranger_skirt,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
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
   [itm_evil_light_armor,itm_leather_boots,],
      def_attrib|level(2),wp(20),knows_common,0x000000003f0000032038a06b587590c500000000001d3a880000000000000000],
["elder_cgaladhon","Lorien Loremaster","the_elven_forest_fortress",tf_hero| tf_randomize_face| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_e,itm_lorien_boots,],
      def_attrib|level(2),wp(20),knows_common,lorien_elf_face_1,lorien_elf_face_2],
["elder_cdolen","Lorien Loremaster","the_encampment",tf_hero| tf_randomize_face| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_e,itm_lorien_boots,],
      def_attrib|level(2),wp(20),knows_common,lorien_elf_face_1,lorien_elf_face_2],
["elder_camroth","Lorien Loremaster","the_encampment",tf_hero| tf_randomize_face| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_e,itm_lorien_boots,],
      def_attrib|level(2),wp(20),knows_common,lorien_elf_face_1,lorien_elf_face_2],
["elder_thalls","Mirkwood_Elder","the_elven_caves",tf_hero| tf_randomize_face| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_armor_d,itm_mirkwood_boots,],
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
   [itm_khand_foot_lam_c,itm_variag_greaves,],
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
["elder_gunda","Mater_of_the_Caves","the_caves",tf_hero| tf_randomize_face| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_d,itm_orc_furboot_tall,],
      def_attrib|level(2),wp(20),knows_common,khand_man1,khand_man2],
["elder_dale","Dale_Quartermaster","the_city",tf_hero| tf_randomize_face,0,0,fac_dale,
   [itm_fur_coat,itm_leather_boots,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_esgaroth","Esgaroth_Quartermaster","the_lake_town",tf_hero| tf_randomize_face,0,0,fac_dale,
   [itm_fur_coat,itm_leather_boots,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_erebor","Erebor_Guildmaster","the_Halls",tf_hero| tf_randomize_face| tf_dwarf,0,0,fac_dwarf,
   [itm_dwarf_armor_a,itm_dwarf_pad_boots,],
      def_attrib|level(2),wp(20),knows_common_dwarf,dwarf_face_3,dwarf_face_4],
["elder_dolguldur","Guldur_Chief","the_black_castle",tf_hero| tf_randomize_face| tf_uruk,0,0,fac_guldur,
   [itm_m_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(2),wp(20),knows_common,mordor_man1,mordor_man2],

["elder_gondor_ac","Campmaster","the_camp",tf_hero| tf_gondor| tf_randomize_face,0,0,fac_gondor,
   [itm_gondor_fine_outfit_dress,itm_gondor_light_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_rohan_ac","Campmaster","the_camp",tf_hero| tf_rohan| tf_randomize_face,0,0,fac_rohan,
   [itm_rohan_fine_outfit_dale_dress,itm_rohan_shoes,],
      def_attrib|level(2),wp(20),knows_common,0x0000000f00001184574a6934eb6ed2d700000000001eb86e0000000000000000],
["elder_mordor_ac","Campmaster","the_camp",tf_hero| tf_randomize_face| tf_uruk,0,0,fac_mordor,
   [itm_m_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_isengard_ac","Campmaster","the_camp",tf_hero| tf_randomize_face| tf_urukhai,0,0,fac_isengard,
   [itm_isen_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_lorien_ac","Campmaster","the_camp",tf_hero| tf_randomize_face| tf_lorien,0,0,fac_lorien,
   [itm_lorien_armor_e,itm_lorien_boots,],
      def_attrib|level(2),wp(20),knows_common,lorien_elf_face_1,lorien_elf_face_2],
["elder_woodelf_ac","Campmaster","the_camp",tf_hero| tf_randomize_face| tf_woodelf,0,0,fac_woodelf,
   [itm_mirkwood_armor_d,itm_mirkwood_boots,],
      def_attrib|level(2),wp(20),knows_common,lorien_elf_face_1,lorien_elf_face_2],
["elder_imladris_ac","Campmaster","the_camp",tf_hero| tf_randomize_face| tf_imladris,0,0,fac_imladris,
   [itm_riv_armor_light,itm_riv_boots,],
      def_attrib|level(2),wp(20),knows_common,lorien_elf_face_1,lorien_elf_face_2],
["elder_beorn_ac","Campmaster","the_camp",tf_hero| tf_randomize_face,0,0,fac_beorn,
   [itm_beorn_tunic,itm_rohan_shoes,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_harad_ac","Harad_Camp_Chief","the_camp",tf_hero| tf_randomize_face| tf_harad,0,0,fac_harad,
   [itm_harad_padded,itm_harad_scale_greaves,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_rhun_ac","Rhun_Camp_Chief","the_camp",tf_hero| tf_randomize_face,0,0,fac_rhun,
   [itm_rhun_armor_p,itm_furry_boots,],
      def_attrib|level(2),wp(20),knows_common,rhun_man1,rhun_man2],
["elder_khand_ac","Khand_Camp_Chief","the_camp",tf_hero| tf_randomize_face,0,0,fac_khand,
   [itm_khand_foot_lam_c,itm_variag_greaves,],
      def_attrib|level(2),wp(20),knows_common,khand_man1,khand_man2],
["elder_dunland_ac","Dun_Camp_Chief","the_camp",tf_hero |tf_dunland,0,0,fac_dunland,
   [itm_dunland_armor_h,itm_dunland_wolfboots,],
      def_attrib|level(2),wp(20),knows_common,0x000000003f0061c720996c7bd86f36db00000000001e42e80000000000000000],
["elder_umbar_ac","Umbar_Quartermaster","the_camp",tf_hero| tf_randomize_face,0,0,fac_umbar,
   [itm_umb_armor_a,itm_corsair_boots,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_moria_ac","Moria_Camp_Chief","the_camp",tf_hero| tf_randomize_face| tf_orc,0,0,fac_moria,
   [itm_moria_armor_c,itm_orc_ragwrap,],
      def_attrib|level(2),wp(20),knows_common,khand_man1,khand_man2],
["elder_gunda_ac","Gundabad_Camp_Chief","the_camp",tf_hero| tf_randomize_face| tf_orc,0,0,fac_gundabad,
   [itm_gundabad_armor_d,itm_orc_furboot_tall,],
      def_attrib|level(2),wp(20),knows_common,khand_man1,khand_man2],
["elder_dale_ac","Dale_Quartermaster","the_camp",tf_hero| tf_randomize_face,0,0,fac_dale,
   [itm_fur_coat,itm_leather_boots,],
      def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["elder_guldur_ac","Guldur_Camp_Chief","the_camp",tf_hero| tf_randomize_face| tf_uruk,0,0,fac_guldur,
   [itm_m_uruk_light_b,itm_uruk_greaves,],
      def_attrib|level(2),wp(20),knows_common,mordor_man1,mordor_man2],	  
["elder_dwarf_ac","Dwarven_Campmaster","the_camp",tf_hero| tf_randomize_face| tf_dwarf,0,0,fac_dwarf,
   [itm_dwarf_armor_a,itm_dwarf_pad_boots,],
      def_attrib|level(2),wp(20),knows_common_dwarf,dwarf_face_3,dwarf_face_4],
	  
	  
#Village stores
["village_1_elder","Village_Elder","_",tf_hero| tf_randomize_face| tf_is_merchant,0,0,fac_commoners,
   [],
      0,0,0,0],
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
   [itm_umb_armor_f,itm_umb_armor_h,itm_corsair_boots,itm_umb_shield_b,itm_umb_shield_d,itm_umbar_cutlass,itm_umbar_rapier,itm_steppe_horse,],
      attr_tier_4,wp_tier_4,knows_common|knows_riding_3|knows_power_strike_3,bandit_face1,bandit_face2],
["spy_evil","Shifty-eyed_Southerner","Shifty-eyed_Southerners",tf_mounted| tfg_boots| tfg_armor| tfg_gloves| tfg_horse,0,0,fac_neutral,
   [itm_leather_jerkin,itm_leather_gloves,itm_leather_boots,itm_arnor_sword_f,itm_steppe_horse,],
      attr_tier_4,wp_tier_4,knows_common|knows_riding_3|knows_power_strike_3,bandit_face1,bandit_face2],
["spy_partner","Spy_Handler","Spy_Handlers",tf_gondor| tf_mounted| tfg_boots| tfg_armor| tfg_gloves| tfg_horse,0,0,fac_neutral,
   [itm_gon_squire,itm_gondor_med_greaves,itm_gondor_cav_sword,itm_gondor_shield_d,itm_leather_gloves,itm_gondor_squire_helm,itm_gondor_courser,],
      attr_tier_4,wp_tier_4,knows_common|knows_riding_3|knows_athletics_2|knows_power_strike_3|knows_ironflesh_3,gondor_face1,gondor_face2],
["spy_partner_evil","Spy_Handler","Spy_Handlers",tf_mounted| tfg_boots| tfg_armor| tfg_gloves| tfg_horse,0,0,fac_neutral,
   [itm_evil_light_armor,itm_leather_boots,itm_mordor_sword,itm_mordor_man_shield_b,itm_mordor_longsword,itm_mordor_warhorse,],
      attr_tier_4,wp_tier_4,knows_common|knows_riding_3|knows_athletics_2|knows_power_strike_3|knows_ironflesh_3,bandit_face1,bandit_face2],
#MV: Easter Egg Troll in Troll Cave
["easter_egg_troll","The Troll","_",tf_troll| tfg_helm| tfg_boots| tf_no_capture_alive| tf_hero,scn_troll_cave_center|entry(8),0,fac_moria,
   [itm_tree_trunk_club_a,itm_troll_feet_boots,itm_troll_head_helm,],
      str_255| agi_3| int_30| cha_18|level(30),wp(200),knows_power_strike_10|knows_ironflesh_10,troll_face1],
["treebeard","Treebeard","_",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive| tf_hero,scn_fangorn|entry(16),0,fac_commoners,
   [itm_tree_trunk_invis,itm_ent_body,itm_ent_hands,itm_ent_feet_boots,itm_ent_head_helm,itm_ent_water,],
      str_255| agi_3| int_30| cha_30|level(30),wp(200),knows_power_strike_10|knows_ironflesh_10,troll_face1,troll_face2],
["ent_1","Bregalad","_",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive| tf_hero,scn_fangorn|entry(17),0,fac_commoners,
   [itm_tree_trunk_invis,itm_ent_body,itm_ent_hands,itm_ent_feet_boots,itm_ent_head_helm2,itm_ent_water,],
      str_255| agi_3| int_30| cha_30|level(30),wp(200),knows_power_strike_10|knows_ironflesh_10,troll_face1,troll_face2],
["ent_2","Finglas","_",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive| tf_hero,scn_fangorn|entry(18),0,fac_commoners,
   [itm_tree_trunk_invis,itm_ent_body,itm_ent_hands,itm_ent_feet_boots,itm_ent_head_helm3,itm_ent_water,],
      str_255| agi_3| int_30| cha_30|level(30),wp(200),knows_power_strike_10|knows_ironflesh_10,troll_face1,troll_face2],
["ent_3","Fladrif","_",tf_troll| tfg_helm| tfg_boots| tfg_armor| tfg_gloves| tf_no_capture_alive| tf_hero,scn_fangorn|entry(19),0,fac_commoners,
   [itm_tree_trunk_invis,itm_ent_body,itm_ent_hands,itm_ent_feet_boots,itm_ent_head_helm2,itm_ent_water,],
      str_255| agi_3| int_30| cha_30|level(30),wp(200),knows_power_strike_10|knows_ironflesh_10,troll_face1,troll_face2],

# Gandalf and Nazgul for conversations
["gandalf","Gandalf","Home-grown Gandalves",tf_hero| tf_mounted| tfg_armor| tfg_horse| tfg_boots,0,0,fac_commoners,
   [itm_mearas_reward,itm_whiterobe,itm_leather_boots,itm_gandstaff,itm_sword_of_arathorn,],
      attr_tier_7,wp_tier_7,knows_riding_10|knows_athletics_10|knows_power_strike_10|knows_ironflesh_10|knows_pathfinding_10,0x0000000fc000234721419ab9eeafbeff00000000001d89110000000000000000],
["nazgul","Nazgul","Domesticated Nazgul",tf_hero| tf_mounted| tfg_armor| tfg_helm| tfg_horse| tfg_boots,0,0,fac_commoners,
   [itm_uruk_greaves,itm_evil_gauntlets_a,itm_nazgulrobe,itm_empty_head,itm_nazgul_sword,itm_mordor_warhorse2,],
       attr_tier_7,wp_tier_7,knows_riding_10|knows_athletics_10|knows_power_strike_10|knows_ironflesh_10|knows_pathfinding_10,mercenary_face_2],

["quick_battle_6_player","quick_battle_6_player","_",tf_hero,0,0,fac_player_faction,
   [itm_leather_jerkin,itm_leather_boots,itm_corsair_bow,itm_corsair_arrows,],
      knight_attrib_1,wp(130),knight_skills_1,0x000000000008010b01f041a9249f65fd],
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
   [itm_rhun_shortsword,itm_rhun_sword,itm_rhun_sword,itm_rhun_helm_g,itm_rhun_helm_h,itm_rhun_armor_b,itm_rhun_armor_a,itm_rhun_armor_d,itm_javelin,itm_rhun_shield,itm_leather_boots,],
              def_attrib|level(17),wp(120),knows_common,mercenary_face_1,mercenary_face_2],

# Troops for scripting purpose. Make sure these are the last troops. (by foxyman)
["troops_end","troops_end","troops_end",tf_hero,no_scene,reserved,fac_commoners,[],0,0,0,0,0],
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
   [itm_isen_uruk_light_a,itm_isen_uruk_light_a,itm_isen_orc_shield_a,itm_isen_orc_armor_b,itm_isen_uruk_helm_a,],
      def_attrib|level(12),wp(90),knows_prisoner_management_1|knows_inventory_management_1|knows_pathfinding_1|knows_athletics_2|knows_power_strike_2|knows_ironflesh_3,mercenary_face_1,mercenary_face_2],
["black_numenorean_sorcerer","Black_Numenorean_Sorcerer","Black_numenorean_sorcerer", tfg_armor| tfg_helm| tfg_boots,0,0,fac_mordor,
   [itm_m_cap_armor,itm_mordor_helm,itm_mordor_sword,itm_leather_boots,],
      def_attrib|level(45),wp(255),knows_common|knows_athletics_6|knows_power_strike_6|knows_ironflesh_6,mercenary_face_1,mercenary_face_2],
["black_numenorean_acolyte","Black_Numenorean_Acolyte","Black_Numenorean_Acolytes",tf_evil_man| tfg_armor| tfg_boots,0,0,fac_mordor,
   [itm_leather_boots,itm_leather_gloves,itm_evil_light_armor,itm_uruk_spear,],
      attr_tier_2,wp_tier_2,knows_common|knows_athletics_1|knows_power_strike_1,mordor_man1,mordor_man2],
["wolf_rider_of_mirkwood","Wolf_Rider_of_Mirkwood","Wolf_Riders_of_Mirkwood",tf_orc| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_orc_bow,itm_arrows,itm_orc_sabre,itm_orc_sabre,itm_isen_uruk_light_a,itm_isen_uruk_light_a,itm_orc_coif,itm_wargarmored_2c,],
      def_attrib|level(15),wp(110),knows_pathfinding_1|knows_horse_archery_2|knows_riding_4|knows_power_throw_2|knows_power_strike_2|knows_ironflesh_2,orc_face3,orc_face6],
["warg_rider_of_mirkwood","Warg_Rider_of_Mirkwood","Warg_Riders_of_Mirkwood",tf_orc| tf_mounted| tfg_shield| tfg_armor| tfg_helm| tfg_horse| tfg_boots| tf_no_capture_alive,0,0,fac_isengard,
   [itm_orc_bow,itm_arrows,itm_orc_sabre,itm_orc_sabre,itm_isen_uruk_light_a,itm_isen_uruk_light_a,itm_orc_coif,itm_wargarmored_1c,],
      def_attrib|level(22),wp(135),knows_pathfinding_1|knows_horse_archery_3|knows_riding_4|knows_power_throw_3|knows_power_strike_4|knows_ironflesh_4,orc_face3,orc_face8],
["gate_aggravator","Gate_is_holding","_", tfg_armor| tfg_boots| tfg_helm|tfg_gloves,0,0,fac_neutral,
   [itm_warg_ghost_armour,itm_empty_hands,itm_empty_legs,itm_empty_head],
      str_255|level(80),wp(5),knows_shield_10|knows_ironflesh_10,0,0],
["orc_pretender","Orc_Pretender","_",tf_orc| tfg_shield| tfg_armor| tfg_helm| tf_no_capture_alive,0,0,fac_neutral,
   [itm_orc_slasher,itm_orc_sabre,itm_moria_orc_shield_b,itm_moria_orc_shield_a,itm_moria_armor_e,itm_orc_helm_g,itm_orc_helm_j,itm_orc_helm_k,itm_orc_greaves,],
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

["last","BUG","BUG",tf_hero,0,0,fac_commoners,[],0,0,0,0],

["multiplayer_profile_troop_male","multiplayer_profile_troop_male","multiplayer_profile_troop_male", tf_hero, 0, 0,fac_commoners,[itm_leather_jerkin, itm_leather_boots],0,0,0,0x000000018000000136db6db6db6db6db00000000001db6db0000000000000000],
["multiplayer_profile_troop_female","multiplayer_profile_troop_female","multiplayer_profile_troop_female", tf_hero|tf_female, 0, 0,fac_commoners,[itm_leather_jerkin, itm_leather_boots],0,0,0,0x000000018000000136db6db6db6db6db00000000001db6db0000000000000000],

["future_troop_6","Compartibility","_", tf_randomize_face,0,0,fac_neutral,[], def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["future_troop_7","Compartibility","_", tf_randomize_face,0,0,fac_neutral,[], def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["future_troop_8","Compartibility","_", tf_randomize_face,0,0,fac_neutral,[], def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["future_troop_9","Compartibility","_", tf_randomize_face,0,0,fac_neutral,[], def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
["future_troop_10","Compartibility","_", tf_randomize_face,0,0,fac_neutral,[], def_attrib|level(2),wp(20),knows_common,mercenary_face_1,mercenary_face_2],
	  
]
 
#
#upgrade(troops,"veteran_brigand","master_brigand")
#upgrade2(troops,"brigand","veteran_brigand","brigand_slaver")
#upgrade(troops,"cutthroat","brigand")
#upgrade(troops,"thug","cutthroat")
#upgrade(troops,"brigand_slaver","master_slaver")
#WOODMEN
upgrade2(troops,"woodmen_youth","woodmen_forester","woodmen_tracker")
upgrade(troops,"woodmen_forester","woodmen_skilled_forester")
upgrade(troops,"woodmen_skilled_forester","woodmen_axemen")
upgrade(troops,"woodmen_axemen","woodmen_master_axemen")
upgrade(troops,"woodmen_tracker","woodmen_scout")
upgrade(troops,"woodmen_scout","woodmen_archer")
upgrade(troops,"woodmen_archer","fell_huntsmen_of_mirkwood")
#BEORNINGS
upgrade(troops,"beorning_vale_man","beorning_warrior")
upgrade2(troops,"beorning_warrior","beorning_tolltacker","beorning_carrock_lookout")
upgrade(troops,"beorning_tolltacker","beorning_sentinel")
upgrade(troops,"beorning_sentinel","beorning_warden_of_the_ford")
upgrade(troops,"beorning_carrock_lookout","beorning_carrock_fighter")
upgrade(troops,"beorning_carrock_fighter","beorning_carrock_berserker")
##LOSSARNACH
upgrade(troops,"woodsman_of_lossarnach","axeman_of_lossarnach")
upgrade(troops,"axeman_of_lossarnach","vet_axeman_of_lossarnach")
upgrade(troops,"vet_axeman_of_lossarnach","heavy_lossarnach_axeman")
upgrade(troops,"heavy_lossarnach_axeman","axemaster_of_lossarnach")
##LAMEDON
upgrade(troops,"clansman_of_lamedon","footman_of_lamedon")
upgrade(troops,"footman_of_lamedon","veteran_of_lamedon")
upgrade(troops,"veteran_of_lamedon","warrior_of_lamedon")
upgrade2(troops,"warrior_of_lamedon","champion_of_lamedon","knight_of_lamedon")
##PINNATH GELIN
upgrade2(troops,"pinnath_gelin_plainsman","pinnath_gelin_spearman","pinnath_gelin_bowman")
upgrade(troops,"pinnath_gelin_spearman","warrior_of_pinnath_gelin")
upgrade(troops,"pinnath_gelin_bowman","pinnath_gelin_archer")
##BLACK ROOT VALE
upgrade2(troops,"blackroot_vale_archer","veteran_blackroot_vale_archer","footman_of_blackroot_vale")
upgrade(troops,"veteran_blackroot_vale_archer","master_blackroot_vale_archer")
upgrade(troops,"footman_of_blackroot_vale","spearman_of_blackroot_vale")
###PELARGIR
upgrade2(troops,"pelargir_watchman","pelargir_marine","pelargir_infantry")
upgrade(troops,"pelargir_infantry","pelargir_vet_infantry")
upgrade(troops,"pelargir_marine","pelargir_vet_marine")
##DOL AMROTH
upgrade(troops,"dol_amroth_youth","squire_of_dol_amroth")
upgrade(troops,"squire_of_dol_amroth","veteran_squire_of_dol_amroth")
upgrade(troops,"veteran_squire_of_dol_amroth","knight_of_dol_amroth")
upgrade(troops,"knight_of_dol_amroth","veteran_knight_of_dol_amroth")
upgrade(troops,"veteran_knight_of_dol_amroth","swan_knight_of_dol_amroth")
#LORIEN
upgrade(troops,"lothlorien_scout","lothlorien_veteran_scout")
upgrade(troops,"lothlorien_veteran_scout","lothlorien_archer")
upgrade(troops,"lothlorien_archer","lothlorien_veteran_archer")
upgrade2(troops,"lothlorien_veteran_archer","lothlorien_master_archer","noldorin_mounted_archer")
upgrade2(troops,"lothlorien_master_archer","galadhrim_royal_archer","galadhrim_royal_marksman")
upgrade2(troops,"lothlorien_infantry","lothlorien_veteran_infantry","lothlorien_warden")
upgrade(troops,"lothlorien_veteran_infantry","lothlorien_elite_infantry")
upgrade(troops,"lothlorien_elite_infantry","galadhrim_royal_swordsman")
upgrade(troops,"lothlorien_warden","lothlorien_veteran_warden")
upgrade(troops,"lothlorien_veteran_warden","galadhrim_royal_warden")
#MIRKWOOD
upgrade2(troops,"greenwood_scout","greenwood_veteran_scout","greenwood_spearman")
upgrade2(troops,"greenwood_veteran_scout","greenwood_archer","greenwood_sentinel")
upgrade(troops,"greenwood_archer","greenwood_veteran_archer")
upgrade(troops,"greenwood_veteran_archer","greenwood_master_archer")
upgrade(troops,"greenwood_master_archer","thranduils_royal_marksman")
upgrade(troops,"greenwood_spearman","greenwood_veteran_spearman")
upgrade(troops,"greenwood_veteran_spearman","greenwood_royal_spearman")
upgrade2(troops,"greenwood_royal_spearman","thranduils_spearman","thranduils_royal_swordsman")
upgrade(troops,"greenwood_sentinel","greenwood_vet_sentinel")
upgrade(troops,"greenwood_vet_sentinel","mirkwood_guardsman")
#RIVENDELL
upgrade2(troops,"rivendell_scout","rivendell_veteran_scout","rivendell_infantry")
upgrade(troops,"rivendell_veteran_scout","rivendell_sentinel")
upgrade2(troops,"rivendell_sentinel","rivendell_veteran_sentinel","rivendell_cavalry")
upgrade(troops,"rivendell_veteran_sentinel","rivendell_elite_sentinel")
upgrade(troops,"rivendell_elite_sentinel","rivendell_guardian")
upgrade(troops,"rivendell_cavalry","knight_of_rivendell")
upgrade(troops,"rivendell_infantry","rivendell_veteran_infantry")
upgrade(troops,"rivendell_veteran_infantry","rivendell_elite_infantry")
upgrade(troops,"rivendell_elite_infantry","rivendell_royal_infantry")
#DUNEADAIN
upgrade(troops,"dunedain_scout","dunedain_trained_scout" )
upgrade2(troops,"dunedain_trained_scout","arnor_man_at_arms","dunedain_ranger" )
upgrade2(troops,"arnor_man_at_arms","arnor_master_at_arms","arnor_horsemen" )
upgrade(troops,"arnor_master_at_arms","high_swordsman_of_arnor" )
upgrade(troops,"arnor_horsemen","knight_of_arnor" )
upgrade(troops,"dunedain_ranger","dunedain_veteran_ranger" )
upgrade(troops,"dunedain_veteran_ranger","dunedain_master_ranger" )
#Gondor infantry
upgrade(troops,"gondor_commoner","gondor_militiamen" )
upgrade2(troops,"gondor_militiamen","footmen_of_gondor","bowmen_of_gondor" )
upgrade2(troops,"footmen_of_gondor","gondor_swordsmen","gondor_spearmen" )
upgrade(troops,"gondor_swordsmen","gondor_veteran_swordsmen" )
upgrade(troops,"gondor_veteran_swordsmen","swordsmen_of_the_tower_guard" )
upgrade(troops,"gondor_spearmen","gondor_veteran_spearmen" )
upgrade(troops,"gondor_veteran_spearmen","guard_of_the_fountain_court" )
#Gondor Noble Line
upgrade(troops,"gondor_noblemen","squire_of_gondor" )
upgrade(troops,"squire_of_gondor","veteran_squire_of_gondor" )
upgrade(troops,"veteran_squire_of_gondor","knight_of_gondor" )
upgrade(troops,"knight_of_gondor","veteran_knight_of_gondor" )
upgrade(troops,"veteran_knight_of_gondor","knight_of_the_citadel" )
#Gondor archers
upgrade2(troops,"bowmen_of_gondor","archer_of_gondor","ranger_of_ithilien" )
upgrade(troops,"archer_of_gondor","veteran_archer_of_gondor" )
upgrade(troops,"veteran_archer_of_gondor","archer_of_the_tower_guard" )
upgrade(troops,"ranger_of_ithilien","veteran_ranger_of_ithilien" )
upgrade(troops,"veteran_ranger_of_ithilien","master_ranger_of_ithilien" )
#ROHAN
upgrade2(troops,"rohan_youth","squire_of_rohan","guardsman_of_rohan")
upgrade(troops,"guardsman_of_rohan","footman_of_rohan")
upgrade(troops,"footman_of_rohan","veteran_footman_of_rohan")
upgrade2(troops,"veteran_footman_of_rohan","elite_footman_of_rohan","heavy_swordsman_of_rohan")
upgrade2(troops,"elite_footman_of_rohan","folcwine_guard_of_rohan","raider_of_rohan")
upgrade(troops,"heavy_swordsman_of_rohan","warden_of_methuseld")
upgrade(troops,"skirmisher_of_rohan","veteran_skirmisher_of_rohan")
upgrade(troops,"veteran_skirmisher_of_rohan","elite_skirmisher_of_rohan")
upgrade(troops,"elite_skirmisher_of_rohan","thengel_guard_of_rohan")
upgrade(troops,"lancer_of_rohan","elite_lancer_of_rohan")
upgrade(troops,"elite_lancer_of_rohan","brego_guard_of_rohan")
upgrade2(troops,"squire_of_rohan","rider_of_rohan","skirmisher_of_rohan")
upgrade2(troops,"rider_of_rohan","veteran_rider_of_rohan","lancer_of_rohan")
upgrade(troops,"veteran_rider_of_rohan","elite_rider_of_rohan")
upgrade(troops,"elite_rider_of_rohan","eorl_guard_of_rohan")
#HARAD
upgrade2(troops,"harad_desert_warrior","harad_infantry","harad_skirmisher")
upgrade2(troops,"harondor_scout","harondor_rider","harad_horse_archer")
upgrade2(troops,"harad_infantry","harad_veteran_infantry","harad_swordsman")
upgrade(troops,"harad_swordsman","harad_lion_guard")
upgrade(troops,"harad_veteran_infantry","harad_tiger_guard")
upgrade(troops,"harondor_rider","harondor_light_cavalry")
upgrade(troops,"harondor_light_cavalry","fang_heavy_cavalry")
upgrade(troops,"harad_skirmisher","harad_archer")
upgrade(troops,"harad_archer","harad_eagle_guard")
upgrade(troops,"harad_horse_archer","black_snake_horse_archer")
upgrade(troops,"black_snake_horse_archer","gold_serpent_horse_archer")
upgrade(troops,"far_harad_tribesman","far_harad_champion")
upgrade(troops,"far_harad_champion","far_harad_panther_guard")
#DUNLAND
upgrade2(troops,"dunnish_wildman","dunnish_warrior","dunnish_raven_rider")
upgrade2(troops,"dunnish_warrior","dunnish_vet_warrior","dunnish_pikeman")
upgrade(troops,"dunnish_pikeman","dunnish_veteran_pikeman")
#upgrade(troops,"dunnish_veteran_spearman","dunnish_spear_master")
#upgrade(troops,"dunnish_long_spearman","dunnish_pike_master")
#upgrade(troops,"dunnish_horseman","dunnish_wolf_guard")
upgrade(troops,"dunnish_vet_warrior","dunnish_wolf_warrior")
upgrade(troops,"dunnish_wolf_warrior","dunnish_wolf_guard")
#upgrade2(troops,"dunnish_axeman","dunnish_veteran_axeman","dunnish_wolf_warrior")
#upgrade(troops,"dunnish_veteran_axeman","dunnish_axe_master")
#upgrade2(troops,"dunnish_wolf_warrior","dunnish_berserker","dunnish_crebain_raider")
#EASTERLINGS
upgrade2(troops,"easterling_youth","easterling_warrior","easterling_rider")
upgrade2(troops,"easterling_warrior","easterling_axeman","khand_glaive_whirler")
upgrade2(troops,"easterling_axeman","easterling_veteran_axeman","variag_pitfighter")
upgrade(troops,"easterling_veteran_axeman","easterling_axe_master")
upgrade2(troops,"easterling_rider","easterling_horseman","easterling_skirmisher")
upgrade(troops,"easterling_horseman","easterling_veteran_horseman")
upgrade2(troops,"easterling_veteran_horseman","easterling_horsemaster","easterling_lance_kataphract")
upgrade2(troops,"khand_glaive_whirler","variag_veteran_glaive_whirler","variag_pitfighter")
upgrade(troops,"variag_veteran_glaive_whirler","khand_glaive_master")
upgrade(troops,"variag_pitfighter","variag_gladiator")
upgrade(troops,"easterling_skirmisher","easterling_veteran_skirmisher")
upgrade(troops,"easterling_veteran_skirmisher","easterling_elite_skirmisher")
#CORSAIRS
upgrade2(troops,"corsair_youth","corsair_warrior","militia_of_umbar")
upgrade2(troops,"corsair_warrior","corsair_pikeman","corsair_marauder")
upgrade(troops,"corsair_pikeman","corsair_veteran_raider")
upgrade(troops,"corsair_veteran_raider","corsair_night_raider")
upgrade(troops,"militia_of_umbar","marksman_of_umbar")
upgrade(troops,"marksman_of_umbar","veteran_marksman_of_umbar")
upgrade2(troops,"veteran_marksman_of_umbar","master_marksman_of_umbar","master_assassin_of_umbar")
upgrade(troops,"corsair_marauder","corsair_veteran_marauder")
upgrade(troops,"corsair_veteran_marauder","corsair_elite_marauder")
#upgrade(troops,"assassin_of_umbar","master_assassin_of_umbar")
#upgrade(troops,"pikeman_of_umbar","veteran_pikeman_of_umbar")
#upgrade(troops,"veteran_pikeman_of_umbar","pike_master_of_umbar")
#ISENGARD ORCS
upgrade2(troops,"orc_snaga_of_isengard","orc_of_isengard","wolf_rider_of_isengard")
upgrade2(troops,"orc_of_isengard","large_orc_of_isengard","large_orc_despoiler")
upgrade(troops,"large_orc_of_isengard","fell_orc_of_isengard")
upgrade(troops,"large_orc_despoiler","fell_orc_despoiler")
upgrade(troops,"wolf_rider_of_isengard","warg_rider_of_isengard")
upgrade(troops,"warg_rider_of_isengard","white_hand_rider")
#ISENGARD URUK-HAIS
upgrade(troops,"uruk_hai_tracker","large_uruk_hai_tracker")
upgrade(troops,"large_uruk_hai_tracker","fighting_uruk_hai_tracker")
upgrade2(troops,"uruk_snaga_of_isengard","uruk_hai_of_isengard","uruk_hai_tracker")
upgrade2(troops,"uruk_hai_of_isengard","large_uruk_hai_of_isengard","uruk_hai_pikeman")
upgrade(troops,"large_uruk_hai_of_isengard","fighting_uruk_hai_warrior")
upgrade(troops,"fighting_uruk_hai_warrior","fighting_uruk_hai_champion")
upgrade(troops,"uruk_hai_pikeman","fighting_uruk_hai_pikeman")
upgrade(troops,"fighting_uruk_hai_pikeman","fighting_uruk_hai_berserker")
#MORDOR ORCS
upgrade2(troops,"orc_snaga_of_mordor","orc_of_mordor","orc_archer_of_mordor")
upgrade2(troops,"orc_of_mordor","large_orc_of_mordor","warg_rider_of_gorgoroth")
upgrade2(troops,"large_orc_of_mordor","fell_orc_of_mordor","fell_morgul_orc")
upgrade(troops,"orc_tracker_of_mordor","fell_orc_tracker_of_mordor")
upgrade2(troops,"orc_archer_of_mordor","large_orc_archer_of_mordor","orc_tracker_of_mordor")
upgrade(troops,"large_orc_archer_of_mordor","fell_orc_archer_of_mordor")
upgrade(troops,"warg_rider_of_gorgoroth","great_warg_rider_of_mordor")
upgrade(troops,"morgul_orc","fell_morgul_orc")
#MORDOR URUKS
upgrade(troops,"uruk_snaga_of_mordor","uruk_of_mordor")
upgrade2(troops,"uruk_of_mordor","large_uruk_of_mordor","uruk_slayer_of_mordor")
upgrade(troops,"large_uruk_of_mordor","fell_uruk_of_mordor")
upgrade(troops,"uruk_slayer_of_mordor","fell_uruk_slayer_of_mordor")
#GULDUR ORCS
upgrade2(troops,"orc_snaga_of_guldur","orc_of_guldur","orc_archer_of_mordor")
upgrade2(troops,"orc_of_guldur","large_orc_of_mordor","warg_rider_of_gorgoroth")
#MORIA ORCS
upgrade(troops,"wolf_rider_of_moria","warg_rider_of_moria")
upgrade(troops,"warg_rider_of_moria","bolg_clan_rider")
upgrade2(troops,"snaga_of_moria","goblin_of_moria","archer_snaga_of_moria")
upgrade2(troops,"goblin_of_moria","large_goblin_of_moria","wolf_rider_of_moria")
upgrade(troops,"archer_snaga_of_moria","large_goblin_archer_of_moria")
upgrade(troops,"large_goblin_archer_of_moria","fell_goblin_archer_of_moria")
upgrade(troops,"large_goblin_of_moria","fell_goblin_of_moria")
#GUNDABAD ORCS
upgrade2(troops,"goblin_gundabad","orc_gundabad","goblin_bowmen_gundabad")
upgrade2(troops,"orc_gundabad","orc_fighter_gundabad","goblin_rider_gundabad")
upgrade(troops,"orc_fighter_gundabad","fell_orc_warrior_gundabad")
upgrade(troops,"goblin_bowmen_gundabad","keen_eyed_goblin_archer_gundabad")
upgrade(troops,"keen_eyed_goblin_archer_gundabad","fell_goblin_archer_gundabad")
upgrade(troops,"goblin_rider_gundabad","warg_rider_gundabad")
upgrade(troops,"warg_rider_gundabad","goblin_north_clan_rider")
#BLACK NUMENORIANS
upgrade(troops,"black_numenorean_renegade","black_numenorean_warrior")
upgrade2(troops,"black_numenorean_warrior","black_numenorean_veteran_warrior","black_numenorean_veteran_horseman")
upgrade2(troops,"black_numenorean_veteran_warrior","black_numenorean_champion","black_numenorean_assassin")
upgrade(troops,"black_numenorean_veteran_horseman","black_numenorean_horsemaster")
#DWARVES
upgrade2(troops,"dwarven_apprentice","dwarven_warrior","dwarven_lookout")
upgrade(troops,"dwarven_warrior","dwarven_hardened_warrior")
upgrade2(troops,"dwarven_hardened_warrior","dwarven_axeman","dwarven_spearman")
upgrade(troops,"dwarven_axeman","dwarven_expert_axeman")
upgrade(troops,"dwarven_expert_axeman","longbeard_axeman")
upgrade(troops,"dwarven_spearman","dwarven_pikeman")
upgrade(troops,"dwarven_pikeman","dwarven_halberdier")
upgrade(troops,"dwarven_lookout","dwarven_scout")
upgrade(troops,"dwarven_scout","dwarven_bowman")
upgrade(troops,"dwarven_bowman","dwarven_archer")
upgrade(troops,"dwarven_archer","marksman_of_ravenhill")
upgrade(troops,"iron_hills_miner","iron_hills_infantry")
upgrade(troops,"iron_hills_infantry","iron_hills_battle_infantry")
upgrade(troops,"iron_hills_battle_infantry","grors_guard")
#DALE
upgrade2(troops,"dale_militia","dale_man_at_arms","laketown_scout")
upgrade2(troops,"dale_man_at_arms","dale_warrior","dale_pikeman")
upgrade(troops,"dale_warrior","dale_veteran_warrior")
upgrade(troops,"dale_veteran_warrior","dale_marchwarden")
upgrade(troops,"dale_pikeman","dale_billman")
upgrade(troops,"dale_billman","dale_bill_master")
upgrade(troops,"merchant_squire_or_dale","merchant_guard_of_dale")
upgrade(troops,"merchant_guard_of_dale","merchant_protector_of_dale")
upgrade(troops,"merchant_protector_of_dale","girions_guard_of_dale")
upgrade(troops,"laketown_scout","laketown_bowmen")
upgrade(troops,"laketown_bowmen","laketown_archer")
upgrade(troops,"laketown_archer","barding_bowmen_of_esgaroth")
#RHUN
upgrade2(troops,"rhun_tribesman","rhun_horse_scout","rhun_tribal_warrior")
upgrade2(troops,"rhun_horse_scout","rhun_horse_archer","rhun_swift_horseman")
upgrade(troops,"rhun_horse_archer","rhun_veteran_horse_archer")
upgrade(troops,"rhun_veteran_horse_archer","fell_balchoth_horse_archer")
upgrade(troops,"rhun_swift_horseman","rhun_veteran_swift_horseman")
upgrade(troops,"rhun_veteran_swift_horseman","falcon_horseman")
upgrade(troops,"rhun_tribal_warrior","rhun_tribal_infantry")
upgrade(troops,"rhun_tribal_infantry","rhun_vet_infantry")
upgrade(troops,"rhun_vet_infantry","infantry_of_the_ox")
upgrade(troops,"rhun_light_horseman","rhun_light_cavalry")
upgrade(troops,"rhun_light_cavalry","rhun_noble_cavalry")
upgrade(troops,"rhun_noble_cavalry","rhun_heavy_noble_cavalry")
upgrade(troops,"rhun_heavy_noble_cavalry","dorwinion_noble_of_rhun")
#BANDITS
upgrade(troops,"tribal_orc","tribal_orc_warrior")
upgrade(troops,"tribal_orc_warrior","tribal_orc_chief")


