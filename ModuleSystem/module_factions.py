from header_factions import *

####################################################################################################################
#  Each faction record contains the following fields:
#  1) Faction id: used for referencing factions in other files.
#     The prefix fac_ is automatically added before each faction id.
#  2) Faction name.
#  3) Faction flags. See header_factions.py for a list of available flags
#  4) Faction coherence. Relation between members of this faction.
#  5) Relations. This is a list of relation records.
#     Each relation record is a tuple that contains the following fields:
#    5.1) Faction. Which other faction this relation is referring to
#    5.2) Value: Relation value between the two factions.
#         Values range between -1 and 1.
#  6) Ranks
#  7) Faction color (default is gray)
####################################################################################################################

default_kingdom_relations = [("outlaws",-0.1),("deserters", -0.1),("mountain_bandits", -0.02),("forest_bandits", -0.02)]
factions = [
  ("no_faction","No Faction",0, 0.9, [], []),
  ("commoners","Commoners",0, 0.1,[("player_faction",0.1)], []),
  ("outlaws","Savages and Bandits", max_player_rating(-30), 0.5,[("commoners",-0.6),("player_faction",-0.15)], [], 0x888888),
# Factions before this point are hardwired into the game end their order should not be changed.
#
##TLD FACTIONS BEGIN##########
  ("gondor",    "Gondor",     0,0.5,[                ("rohan", 0.2),("lorien", 0.5),("imladris", 0.5),("woodelf", 0.5),("mordor",-0.5),("harad",-0.5),("rhun",-0.5),("khand",-0.5),("dunland",-0.5),("umbar",-0.5),("isengard",-0.5),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),("dale", 0.2),("dwarf", 0.2),("beorn", 0.2),("tribal_orcs",-0.5),("outlaws",-0.15),("player_faction",0.2  )], [], 0xEEF7ED),
  ("dwarf",     "Erebor",     0,0.5,[("gondor", 0.2),("rohan", 0.2),("lorien", 0.1),("imladris", 0.1),("woodelf", 0.1),("mordor",-0.2),("harad",-0.1),("rhun",-0.1),("khand",-0.1),("dunland",-0.1),("umbar",-0.1),("isengard",-0.1),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),("dale", 0.5),               ("beorn", 0.2),("tribal_orcs",-0.5),("outlaws",-0.05)], [], 0xEBF0DD),
  ("rohan",     "Rohan",      0,0.5,[("gondor", 0.2),               ("lorien", 0.1),("imladris", 0.1),("woodelf", 0.1),("mordor",-0.5),("harad",-0.5),("rhun",-0.5),("khand",-0.5),("dunland",-0.5),("umbar",-0.5),("isengard",-0.5),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),("dale", 0.5),("dwarf", 0.2),("beorn", 0.2),("tribal_orcs",-0.5),("outlaws",-0.15),("player_faction",0.2  )], [], 0x0DFF00),
  ("mordor",    "Mordor",     0,0.5,[("gondor",-0.5),("rohan",-0.2),("lorien",-0.2),("imladris",-0.2),("woodelf",-0.2),                ("harad", 0.5),("rhun", 0.2),("khand", 0.2),("dunland", 0.2),("umbar", 0.5),("isengard", 0.2),("moria", 0.5),("guldur", 0.5),("gundabad", 0.5),("dale",-0.2),("dwarf",-0.2),("beorn",-0.2),("tribal_orcs",-0.5),("player_faction",-0.15)], [], 0xFF0000),
  ("isengard",  "Isengard",   0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.1),("imladris",-0.1),("woodelf",-0.1),("mordor", 0.2),("harad", 0.1),("rhun", 0.5),("khand", 0.5),("dunland", 0.5),("umbar", 0.5),                  ("moria", 0.5),("guldur", 0.5),("gundabad", 0.5),("dale",-0.2),("dwarf",-0.2),("beorn",-0.2),("tribal_orcs",-0.5),("player_faction",-0.15)], [], 0xFFEE00),
  ("lorien",    "Lothlorien", 0,0.5,[("gondor", 0.5),("rohan", 0.2),                ("imladris", 0.5),("woodelf", 0.5),("mordor",-0.2),("harad",-0.1),("rhun",-0.5),("khand",-0.1),("dunland",-0.1),("umbar",-0.1),("isengard",-0.1),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),("dale", 0.2),("dwarf", 0.1),("beorn", 0.2),("tribal_orcs",-0.5)], [], 0x00FFC8),
  ("imladris",  "Imladris",   0,0.5,[("gondor", 0.5),("rohan", 0.2),("lorien", 0.5),                  ("woodelf", 0.5),("mordor",-0.2),("harad",-0.1),("rhun",-0.1),("khand",-0.1),("dunland",-0.1),("umbar",-0.1),("isengard",-0.1),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),("dale", 0.2),("dwarf", 0.1),("beorn", 0.2),("tribal_orcs",-0.5),("outlaws",-0.05)], [], 0x160ae5),
  ("woodelf","Mirkwood Elves",0,0.5,[("gondor", 0.5),("rohan", 0.2),("lorien", 0.5),("imladris", 0.5),                 ("mordor",-0.2),("harad",-0.1),("rhun",-0.1),("khand",-0.1),("dunland",-0.1),("umbar",-0.1),("isengard",-0.1),("moria",-0.5),("guldur",-0.9),("gundabad",-0.5),("dale", 0.1),("dwarf", 0.1),("beorn", 0.2),("tribal_orcs",-0.5),("outlaws",-0.05)], [], 0x5EFFA9),
  ("dale",      "Dale",       0,0.5,[("gondor", 0.2),("rohan", 0.5),("lorien", 0.5),("imladris", 0.5),("woodelf", 0.5),("mordor",-0.5),("harad",-0.5),("rhun",-0.5),("khand",-0.5),("dunland",-0.5),("umbar",-0.5),("isengard",-0.5),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),              ("dwarf", 0.5),("beorn", 0.2),("tribal_orcs",-0.5),("outlaws",-0.05)], [], 0xFFFEB8),
  ("harad",     "Harad",      0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.1),("imladris",-0.1),("woodelf",-0.1),("mordor", 0.5),               ("rhun", 0.5),("khand", 0.5),("dunland", 0.5),("umbar", 0.5),("isengard", 0.5),("moria", 0.5),("guldur", 0.5),("gundabad", 0.5),("dale",-0.2),("dwarf",-0.2),("beorn",-0.2),("tribal_orcs",-0.5)], [], 0xFF5E79),
  ("rhun",      "Rhun",       0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.1),("imladris",-0.1),("woodelf",-0.1),("mordor", 0.2),("harad", 0.1),              ("khand", 0.5),("dunland", 0.1),("umbar", 0.5),("isengard", 0.5),("moria", 0.5),("guldur", 0.5),("gundabad", 0.5),("dale",-0.7),("dwarf",-0.7),("beorn",-0.2),("tribal_orcs",-0.5)], [], 0xF081C2),
  ("khand",     "Khand",      0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.1),("imladris",-0.1),("woodelf",-0.1),("mordor", 0.2),("harad", 0.1),("rhun", 0.5),               ("dunland", 0.1),("umbar", 0.5),("isengard", 0.5),("moria", 0.5),("guldur", 0.5),("gundabad", 0.5),("dale",-0.5),("dwarf",-0.5),("beorn",-0.5),("tribal_orcs",-0.5)], [], 0xEA96FF),
  ("umbar",     "Umbar",      0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.5),("imladris",-0.5),("woodelf",-0.5),("mordor", 0.5),("harad", 0.5),("rhun", 0.5),("khand", 0.5),("dunland", 0.5),               ("isengard", 0.5),("moria", 0.5),("guldur", 0.5),("gundabad", 0.5),("dale",-0.2),("dwarf",-0.2),("beorn",-0.2),("tribal_orcs",-0.5)], [], 0xFF9421),
  ("moria",     "Moria",      0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.5),("imladris",-0.5),("woodelf",-0.5),("mordor", 0.5),("harad", 0.5),("rhun", 0.5),("khand", 0.5),("dunland", 0.5),("umbar", 0.5),("isengard", 0.5),               ("guldur", 0.5),("gundabad", 0.5),("dale",-0.2),("dwarf",-0.2),("beorn",-0.2),("tribal_orcs",-0.5)], [], 0xFF9421),
  ("guldur",    "Dol Guldur", 0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.5),("imladris",-0.5),("woodelf",-0.5),("mordor", 0.5),("harad", 0.5),("rhun", 0.5),("khand", 0.5),("dunland", 0.5),("umbar", 0.5),("isengard", 0.5),("moria", 0.5),                ("gundabad", 0.5),("dale",-0.5),("dwarf",-0.5),("beorn",-0.5),("tribal_orcs",-0.5)], [], 0xFF0000),
  ("gundabad",  "Mt.Gundabad",0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.5),("imladris",-0.5),("woodelf",-0.5),("mordor", 0.5),("harad", 0.5),("rhun", 0.5),("khand", 0.5),("dunland", 0.5),("umbar", 0.5),("isengard", 0.5),("moria", 0.5),("guldur", 0.5),                  ("dale",-0.5),("dwarf",-0.5),("beorn",-0.5),("tribal_orcs",-0.5)], [], 0xFF9421),
  ("dunland",   "Dunlendings",0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.1),("imladris",-0.1),("woodelf",-0.1),("mordor", 0.5),("harad", 0.5),("rhun", 0.5),("khand", 0.5),                 ("umbar", 0.5),("isengard", 0.5),("moria", 0.5),("guldur", 0.5),("gundabad", 0.5),("dale",-0.2),("dwarf",-0.2),("beorn",-0.2),("tribal_orcs",-0.5)], [], 0xFF4800),
  ("beorn",     "Beornings",  0,0.5,[("gondor", 0.2),("rohan", 0.2),("lorien", 0.5),("imladris", 0.5),("woodelf", 0.5),("mordor",-0.2),("harad",-0.5),("rhun",-0.5),("khand",-0.5),("dunland",-0.5),("umbar",-0.5),("isengard",-0.5),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),("dale", 0.5),("dwarf", 0.5),               ("tribal_orcs",-0.5),("outlaws",-0.05)], [], 0xA5F29B),
  
  ("kingdoms_end","kingdoms_end",0,0,[],[]),
  ("player_supporters_faction","Player Faction",0, 0.9, [("player_faction",1.00),("outlaws",-0.1),("deserters", -0.02),("mountain_bandits", -0.1),("forest_bandits", -0.05)], []),
  ("player_faction","Player Faction",0, 0.9, [("mordor",-0.6),("gondor",0.1)], []),
  ("brigands",   "Brigands",   0,0.5,[("gondor", 0  ),("rohan", 0  ),("lorien", 0  ),("imladris", 0  ),                 ("mordor", 0  ),("harad", 0  ),("rhun", 0  ),("khand", 0  ),("dunland", 0   ),("umbar", 0 ),("isengard", 0  ),("moria", 0  ),("guldur", 0  ),("gundabad", 0),("dale", 0  ),("tribal_orcs",-0.5)], [], 0xCFCFCF),
  ("tribal_orcs","Tribal Orcs",0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.5),("imladris",-0.5),("woodelf",-0.5),("mordor",-0.5),("harad",-0.5),("rhun",-0.5),("khand",-0.5),("dunland",-0.5),("umbar",-0.5),("isengard",-0.5),("moria",-0.5),("guldur",-0.5),                ("dale",-0.5),], [], 0x414141),
##TLD FACTIONS END##########

  ("neutral","ruins",ff_always_hide_label, 0.1,[("player_faction",0.0)], [],0x888888),
  ("innocents","Innocents", ff_always_hide_label, 0.5,[("outlaws",-0.05)], []),
  ("merchants","Merchants", ff_always_hide_label, 0.5,[("outlaws",-0.5),], []),
#########################
#TLD UNCOMMENTED
##########################
  ("manhunters","Manhunters", 0, 0.5,[("outlaws",-0.6),("player_faction",0.1)], []),
  ("deserters","Deserters", 0, 0.5,[("manhunters",-0.6),("merchants",-0.5),("player_faction",-0.1)], [], 0x888888),
  ("mountain_bandits","Mountain Bandits", 0, 0.5,[("commoners",-0.2),("merchants",-0.5),("manhunters",-0.6),("player_faction",-0.15)], [], 0x888888),
  ("forest_bandits","Forest Bandits", 0, 0.5,[("commoners",-0.2),("merchants",-0.5),("manhunters",-0.6),("player_faction",-0.15)], [], 0x888888),

#  ("noble_refugees","Noble Refugees", 0, 0.5,[], []),

  ("mission_companion_1" ,"_", 0, 0.5,[], []), # mission companion arrays
  ("mission_companion_2" ,"_", 0, 0.5,[], []),
  ("mission_companion_3" ,"_", 0, 0.5,[], []),
  ("mission_companion_4" ,"_", 0, 0.5,[], []),
  ("mission_companion_5" ,"_", 0, 0.5,[], []),
  ("mission_companion_6" ,"_", 0, 0.5,[], []),
  ("mission_companion_7" ,"_", 0, 0.5,[], []),
  ("mission_companion_8" ,"_", 0, 0.5,[], []),
  ("mission_companion_9" ,"_", 0, 0.5,[], []),
  ("mission_companion_10","_", 0, 0.5,[], []),
  ("mission_companion_11","_", 0, 0.5,[], []),
]
