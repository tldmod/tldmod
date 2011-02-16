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

default_kingdom_relations = [("outlaws",-0.05),("deserters", -0.05),("mountain_bandits", -0.02),("forest_bandits", -0.02)]
factions = [
  ("no_faction","No Faction",0, 0.9, [], []),
  ("commoners","Commoners",0, 0.1,[("player_faction",0.1)], []),
  ("outlaws","Outlaws", max_player_rating(-30), 0.5,[("commoners",-0.6),("player_faction",-0.15)], [], 0x888888),
# Factions before this point are hardwired into the game end their order should not be changed.
#########################
#TLD UNCOMMENTED
##########################
##TLD FACTIONS BEGIN##########
  ("gondor",     "Gondor",     0,0.5,[                ("rohan", 0.2),("lorien", 0.5 ),("imladris", 0.5 ),("woodelf", 0.5 ),("mordor",-0.5),("harad",-0.5 ),("rhun",-0.5 ),("khand",-0.5 ),("dunland",-0.5 ),("umbar",-0.5 ),("isengard",-0.5 ),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),("dale", 0.2),("dwarf", 0.2),("beorn", 0.2),("tribal_orcs",-0.5),("outlaws",-0.15),("player_faction",0.2  )], [], 0xEEF7ED),
  ("dwarf",      "Erebor",     0,0.5,[("gondor", 0.2),("rohan", 0.2),("lorien", 0.0 ),("imladris", 0.0 ),("woodelf", 0.1 ),("mordor",-0.2),("harad",-0.05),("rhun",-0.05),("khand",-0.05),("dunland",-0.05),("umbar",-0.05),("isengard",-0.05),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),("dale", 0.5),               ("beorn", 0.2),("tribal_orcs",-0.5),("outlaws",-0.05)], [], 0xEBF0DD),
  ("rohan",      "Rohan",      0,0.5,[("gondor", 0.2),               ("lorien", 0.0 ),("imladris", 0.0 ),("woodelf", 0.0 ),("mordor",-0.5),("harad",-0.5 ),("rhun",-0.5 ),("khand",-0.5 ),("dunland",-0.5 ),("umbar",-0.5 ),("isengard",-0.5 ),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),("dale", 0.5),("dwarf", 0.2),("beorn", 0.2),("tribal_orcs",-0.5),("outlaws",-0.15),("player_faction",0.2  )], [], 0x0DFF00),
  ("mordor",     "Mordor",     0,0.5,[("gondor",-0.5),("rohan",-0.2),("lorien",-0.2 ),("imladris",-0.2 ),("woodelf",-0.2 ),                ("harad", 0.5 ),("rhun", 0.2 ),("khand", 0.2 ),("dunland", 0.2 ),("umbar", 0.5 ),("isengard", 0.2 ),("moria", 0.5),("guldur", 0.5),("gundabad", 0.5),("dale",-0.2),("dwarf",-0.2),("beorn",-0.2),("tribal_orcs",-0.5),("player_faction",-0.15)], [], 0xFF0000),
  ("isengard",   "Isengard",   0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.05),("imladris",-0.05),("woodelf",-0.05),("mordor", 0.2),("harad", 0.05),("rhun", 0.5 ),("khand", 0.5 ),("dunland", 0.5 ),("umbar", 0.5 ),                   ("moria", 0.5),("guldur", 0.5),("gundabad", 0.5),("dale",-0.2),("dwarf",-0.2),("beorn",-0.2),("tribal_orcs",-0.5),("player_faction",-0.15)], [], 0xFFEE00),
  ("lorien",     "Lothlorien", 0,0.5,[("gondor", 0.5),("rohan", 0.2),                 ("imladris", 0.5 ),("woodelf", 0.5 ),("mordor",-0.2),("harad",-0.05),("rhun",-0.5 ),("khand",-0.05),("dunland",-0.05),("umbar",-0.05),("isengard",-0.05),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),("dale", 0.2),("dwarf", 0.0),("beorn", 0.2),("tribal_orcs",-0.5)], [], 0x00FFC8),
  ("imladris",   "Imladris",   0,0.5,[("gondor", 0.5),("rohan", 0.2),("lorien", 0.5 ),                   ("woodelf", 0.5 ),("mordor",-0.2),("harad",-0.05),("rhun",-0.05),("khand",-0.05),("dunland",-0.05),("umbar",-0.05),("isengard",-0.05),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),("dale", 0.2),("dwarf", 0.0),("beorn", 0.2),("tribal_orcs",-0.5),("outlaws",-0.05)], [], 0x160ae5),
  ("woodelf",    "The Mirkwood Elves",  0,0.5,[("gondor", 0.5),("rohan", 0.2),("lorien", 0.5 ),("imladris", 0.5 ),                  ("mordor",-0.2),("harad",-0.05),("rhun",-0.05),("khand",-0.05),("dunland",-0.05),("umbar",-0.05),("isengard",-0.05),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),("dale", 0.0),("dwarf", 0.0),("beorn", 0.2),("tribal_orcs",-0.5),("outlaws",-0.05)], [], 0x5EFFA9),
  ("dale",       "Dale",       0,0.5,[("gondor", 0.2),("rohan", 0.5),("lorien", 0.5 ),("imladris", 0.5 ),("woodelf", 0.5 ),("mordor",-0.5),("harad",-0.5 ),("rhun",-0.5 ),("khand",-0.5 ),("dunland",-0.5 ),("umbar",-0.5 ),("isengard",-0.5 ),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),              ("dwarf", 0.5),("beorn", 0.2),("tribal_orcs",-0.5),("outlaws",-0.05)], [], 0xFFFEB8),
  ("harad",      "Harad",   0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.05),("imladris",-0.05),("woodelf",-0.05),("mordor", 0.5),                ("rhun", 0.5 ),("khand", 0.5 ),("dunland", 0.5 ),("umbar", 0.5 ),("isengard", 0.5 ),("moria", 0.5),("guldur", 0.5),("gundabad", 0.5),("dale",-0.2),("dwarf",-0.2),("beorn",-0.2),("tribal_orcs",-0.5)], [], 0xFF5E79),
  ("rhun",       "Rhun",       0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.05),("imladris",-0.05),("woodelf",-0.05),("mordor", 0.2),("harad", 0.05),               ("khand", 0.5 ),("dunland", 0.05),("umbar", 0.5 ),("isengard", 0.5 ),("moria", 0.5),("guldur", 0.5),("gundabad", 0.5),("dale",-0.5),("dwarf",-0.5),("beorn",-0.5),("tribal_orcs",-0.5)], [], 0xF081C2),
  ("khand",      "Khand",      0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.05),("imladris",-0.05),("woodelf",-0.05),("mordor", 0.2),("harad", 0.05),("rhun", 0.5 ),                ("dunland", 0.05),("umbar", 0.5 ),("isengard", 0.5 ),("moria", 0.5),("guldur", 0.5),("gundabad", 0.5),("dale",-0.5),("dwarf",-0.5),("beorn",-0.5),("tribal_orcs",-0.5)], [], 0xEA96FF),
  ("umbar",      "Umbar",      0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.5 ),("imladris",-0.5 ),("woodelf",-0.5 ),("mordor", 0.5),("harad", 0.5 ),("rhun", 0.5 ),("khand", 0.5 ),("dunland", 0.5 ),                ("isengard", 0.5 ),("moria", 0.5),("guldur", 0.5),("gundabad", 0.5),("dale",-0.2),("dwarf",-0.2),("beorn",-0.2),("tribal_orcs",-0.5)], [], 0xFF9421),
  ("moria",      "Moria",      0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.5 ),("imladris",-0.5 ),("woodelf",-0.5 ),("mordor", 0.5),("harad", 0.5 ),("rhun", 0.5 ),("khand", 0.5 ),("dunland", 0.5 ),("umbar", 0.5 ),("isengard", 0.5 ),               ("guldur", 0.5),("gundabad", 0.5),("dale",-0.2),("dwarf",-0.2),("beorn",-0.2),("tribal_orcs",-0.5)], [], 0xFF9421),
  ("guldur",     "Dol Guldur", 0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.5 ),("imladris",-0.5 ),("woodelf",-0.5 ),("mordor", 0.5),("harad", 0.5 ),("rhun", 0.5 ),("khand", 0.5 ),("dunland", 0.5 ),("umbar", 0.5 ),("isengard", 0.5 ),("moria", 0.5),                ("gundabad", 0.5),("dale",-0.5),("dwarf",-0.5),("beorn",-0.5),("tribal_orcs",-0.5)], [], 0xFF0000),
  ("gundabad",   "Mt.Gundabad",0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.5 ),("imladris",-0.5 ),("woodelf",-0.5 ),("mordor", 0.5),("harad", 0.5 ),("rhun", 0.5 ),("khand", 0.5 ),("dunland", 0.5 ),("umbar", 0.5 ),("isengard", 0.5 ),("moria", 0.5),("guldur", 0.5),                  ("dale",-0.5),("dwarf",-0.5),("beorn",-0.5),("tribal_orcs",-0.5)], [], 0xFF9421),
  ("dunland",    "Dunland", 0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.05),("imladris",-0.05),("woodelf",-0.05),("mordor", 0.5),("harad", 0.5 ),("rhun", 0.5 ),("khand", 0.5 ),                  ("umbar", 0.5 ),("isengard", 0.5 ),("moria", 0.5),("guldur", 0.5),("gundabad", 0.5),("dale",-0.2),("dwarf",-0.2),("beorn",-0.2),("tribal_orcs",-0.5)], [], 0xFF4800),
#  ("northmen",   "Northmen",   0,0.5,[("gondor", 0.2),("rohan", 0.2),("lorien", 0.5 ),("imladris", 0.5 ),("woodelf", 0.5 ),                   ("mordor",-0.2),("harad",-0.5 ),("rhun",-0.5 ),("khand",-0.5 ),("dunland",-0.5 ),("umbar",-0.5 ),("isengard",-0.5 ),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),("dale", 0.5),("dwarf", 0.5),("beorn", 0.2),("tribal_orcs",-0.5),("outlaws",-0.05)], [], 0xA5F29B),
  ("beorn",      "The Beornings",  0,0.5,[("gondor", 0.2),("rohan", 0.2),("lorien", 0.5 ),("imladris", 0.5 ),("woodelf", 0.5 ),("mordor",-0.2),("harad",-0.5 ),("rhun",-0.5 ),("khand",-0.5 ),("dunland",-0.5 ),("umbar",-0.5 ),("isengard",-0.5 ),("moria",-0.5),("guldur",-0.5),("gundabad",-0.5),("dale", 0.5),("dwarf", 0.5),               ("tribal_orcs",-0.5),("outlaws",-0.05)], [], 0xA5F29B),
  
 
  ("player_supporters_faction","Player Faction",0, 0.9, [("player_faction",1.00),("outlaws",-0.05),("deserters", -0.02),("mountain_bandits", -0.05),("forest_bandits", -0.05)], []),
  ("kingdoms_end","kingdoms_end",0,0,[],[]),
  ("player_faction","Player Faction",0, 0.9, [("mordor",-0.6),("gondor",0.1)], []),
  ("brigands",   "Brigands",   0,0.5,[("gondor", 0  ),("rohan", 0  ),("lorien", 0   ),("imladris", 0   ),                  ("mordor", 0  ),("harad", 0   ),("rhun", 0   ),("khand", 0   ),("dunland", 0   ),("umbar", 0   ),("isengard", 0   ),("moria", 0  ),("guldur", 0  ),("gundabad", 0  ),("dale", 0  ),               ("tribal_orcs",-0.5)], [], 0xCFCFCF),
  ("tribal_orcs","Tribal Orcs",0,0.5,[("gondor",-0.5),("rohan",-0.5),("lorien",-0.5 ),("imladris",-0.5 ),("woodelf",-0.5 ),("mordor", -0.5),("harad", -0.5 ),("rhun",-0.5 ),("khand",-0.5 ),("dunland",-0.5 ),("umbar",-0.5 ),("isengard",-0.5 ),("moria",-0.5),("guldur",-0.5)                                                                    ], [], 0x414141),
##TLD FACTIONS END##########

  ("neutral","Neutral",0, 0.1,[("player_faction",0.0)], [],0xFFFFFF),
  ("innocents","Innocents", ff_always_hide_label, 0.5,[("outlaws",-0.05)], []),
  ("merchants","Merchants", ff_always_hide_label, 0.5,[("outlaws",-0.5),], []),

  ("dark_knights","Dark Knights", 0, 0.5,[("innocents",-0.9),("player_faction",-0.4)], []),

  ("culture_1",  "culture_1", 0, 0.9, [], []),
  ("culture_2",  "culture_2", 0, 0.9, [], []),
  ("culture_3",  "culture_3", 0, 0.9, [], []),
  ("culture_4",  "culture_4", 0, 0.9, [], []),
  ("culture_5",  "culture_5", 0, 0.9, [], []),
  ("culture_6",  "culture_6", 0, 0.9, [], []),
  ("culture_7",  "culture_7", 0, 0.9, [], []),
  ("culture_8",  "culture_8", 0, 0.9, [], []),
  ("culture_9",  "culture_9", 0, 0.9, [], []),
  ("culture_10",  "culture_10", 0, 0.9, [], []),
  ("culture_11",  "culture_11", 0, 0.9, [], []),
  ("culture_12",  "culture_12", 0, 0.9, [], []),
  ("culture_13",  "culture_13", 0, 0.9, [], []),
  ("culture_14",  "culture_14", 0, 0.9, [], []),
  ("culture_15",  "culture_15", 0, 0.9, [], []),
  ("culture_16",  "culture_16", 0, 0.9, [], []),
  ("culture_17",  "culture_17", 0, 0.9, [], []),
  ("culture_18",  "culture_18", 0, 0.9, [], []),
  ("culture_19",  "culture_19", 0, 0.9, [], []),
#########################
#TLD UNCOMMENTED
##########################
# ("swadian_caravans","Swadian Caravans", 0, 0.5,[("outlaws",-0.8), ("dark_knights",-0.2)], []),
# ("vaegir_caravans","Vaegir Caravans", 0, 0.5,[("outlaws",-0.8), ("dark_knights",-0.2)], []),

#  ("robber_knights",  "robber_knights", 0, 0.1, [], []),
  ("black_khergits","Black Khergits", 0, 0.5,[("player_faction",-0.3),("gondor",-0.02),("rohan",-0.02)], []),
##  ("rebel_peasants","Rebel Peasants", 0, 0.5,[("vaegirs",-0.5),("player_faction",0.0)], []),
  ("manhunters","Manhunters", 0, 0.5,[("outlaws",-0.6),("player_faction",0.1)], []),
  ("deserters","Deserters", 0, 0.5,[("manhunters",-0.6),("merchants",-0.5),("player_faction",-0.1)], [], 0x888888),
  ("mountain_bandits","Mountain Bandits", 0, 0.5,[("commoners",-0.2),("merchants",-0.5),("manhunters",-0.6),("player_faction",-0.15)], [], 0x888888),
  ("forest_bandits","Forest Bandits", 0, 0.5,[("commoners",-0.2),("merchants",-0.5),("manhunters",-0.6),("player_faction",-0.15)], [], 0x888888),

#  ("undeads","Undeads", max_player_rating(-30), 0.5,[("commoners",-0.7),("player_faction",-0.5)], []),
#  ("slavers","Slavers", 0, 0.1, [], []),
#  ("peasant_rebels","Peasant Rebels", 0, 1.0,[("noble_refugees",-1.0),("player_faction",-0.4)], []),
  ("noble_refugees","Noble Refugees", 0, 0.5,[], []),
]
