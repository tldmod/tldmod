from header_music import *
####################################################################################################################
#  Each track record contains the following fields:
#  1) Track id: used for referencing tracks.
#  2) Track file: filename of the track
#  3) Track flags. See header_music.py for a list of available flags
#  4) Continue Track flags: Shows in which situations or cultures the track can continue playing. See header_music.py for a list of available flags
####################################################################################################################

# WARNING: You MUST add mtf_module_track flag to the flags of the tracks located under module directory

tracks = [
("bogus", "cant_find_this.ogg", 0, 0),
("mount_and_blade_title_screen", "TLD_A_Tale_Untold.mp3", mtf_module_track|mtf_sit_main_title|mtf_start_immediately, mtf_sit_fight),

# ("ambushed_by_neutral", "TLD_Rohan_Ambush.mp3", mtf_module_track|mtf_sit_ambushed|mtf_sit_siege, mtf_sit_fight),
# ("ambushed_by_khergit", "TLD_Orc_Ambush.mp3", mtf_module_track|mtf_sit_ambushed|mtf_sit_siege, mtf_sit_fight),

("arena_1", "arena_1.ogg", mtf_sit_arena, 0),
#MV: next two commented out only because they are Native
#("armorer", "armorer.ogg", mtf_sit_travel, 0), 
#("bandit_fight", "bandit_fight.ogg", mtf_sit_fight|mtf_sit_ambushed, 0),

#("calm_night_1", "TLD_NightMusic.mp3", mtf_module_track|mtf_sit_night, mtf_sit_tavern|mtf_sit_travel),
("captured", "capture.ogg", mtf_persist_until_finished, 0),

("defeated_by_neutral","TLD_Killed.mp3",mtf_module_track|                 mtf_persist_until_finished|mtf_sit_killed, 0),
("defeated_by_neutral_2", "defeated_by_neutral_2.ogg",                            mtf_persist_until_finished|mtf_sit_killed, 0),
("defeated_by_neutral_3", "defeated_by_neutral_3.ogg",                            mtf_persist_until_finished|mtf_sit_killed, 0),
("killed_by_swadian", "killed_by_swadian.ogg" ,                  mtf_culture_good|mtf_persist_until_finished|mtf_sit_killed, 0),
("killed_by_khergit", "TLD_Killed.mp3", mtf_module_track|mtf_culture_evil|mtf_persist_until_finished|mtf_sit_killed, 0),
  

#TLD battle music
("TLD_Battle_Barding",   "Battle\TLD_Battle_Barding.mp3",   mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Beorn",     "Battle\TLD_Battle_Beorn.mp3",     mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Corsair",   "Battle\TLD_Battle_Corsair.mp3",   mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Dunland",   "Battle\TLD_Battle_Dunland.mp3",   mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Dwarves",   "Battle\TLD_Battle_Dwarves.mp3",   mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Elves",     "Battle\TLD_Battle_Elves.mp3",     mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Wood_Elves","Battle\TLD_Battle_WoodElves.mp3", mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Imladris",  "Battle\TLD_Battle_Rivendell.mp3", mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Far_Harad", "Battle\TLD_Battle_Far_Harad.mp3", mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Khand",     "Battle\TLD_Battle_Khand.mp3",     mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Gondor",    "Battle\TLD_Battle_Gondor.mp3",    mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Gondor_2",  "Battle\TLD_Battle_Gondor_2.mp3",  mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Gundabad",  "Battle\TLD_Battle_Gundabad.mp3",  mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Isengard",  "Battle\TLD_Battle_Isengard.mp3",  mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Mordor",    "Battle\TLD_Battle_Mordor.mp3",    mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Orcs",      "Battle\TLD_Battle_Orcs.mp3",      mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Rohan",     "Battle\TLD_Battle_Rohan.mp3",     mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Battle_Rhun",      "Battle\TLD_Battle_Rhun.mp3",      mtf_module_track, mtf_sit_fight|mtf_sit_ambushed),

#TLD siege music (played by the MB music system)
("TLD_Bad_Siege",  "Battle\TLD_Bad_Siege.mp3",  mtf_module_track|mtf_sit_siege|mtf_culture_evil, mtf_sit_fight|mtf_sit_ambushed),
("TLD_Good_Siege", "Battle\TLD_Good_Siege.mp3", mtf_module_track|mtf_sit_siege|mtf_culture_good, mtf_sit_fight|mtf_sit_ambushed),


#old battle music - all Native tracks
# ("fight_1"              , "fight_1.ogg"              ,               mtf_sit_fight|mtf_sit_ambushed, 0),
# ("fight_2"              , "fight_2.ogg"              ,               mtf_sit_fight|mtf_sit_ambushed, 0),
# ("fight_3"              , "fight_3.ogg"              ,               mtf_sit_fight|mtf_sit_ambushed, 0),
# ("fight_as_vaegir"      , "fight_as_vaegir.ogg"      , mtf_culture_2|mtf_sit_fight|mtf_sit_ambushed, mtf_culture_all),
# ("fight_as_khergit"     , "fight_as_khergit.ogg"     , mtf_culture_3|mtf_sit_fight|mtf_sit_ambushed, mtf_culture_all),
# ("fight_as_nord"        , "fight_as_nord.ogg"        , mtf_culture_4|mtf_sit_fight|mtf_sit_ambushed, mtf_culture_all),
# ("fight_as_rhodok"      , "fight_as_rhodok.ogg"      , mtf_culture_5|mtf_sit_fight|mtf_sit_ambushed, mtf_culture_all),
# ("fight_while_mounted_1", "fight_while_mounted_1.ogg",               mtf_sit_fight|mtf_sit_ambushed, 0),
# ("fight_while_mounted_2", "fight_while_mounted_2.ogg",               mtf_sit_fight|mtf_sit_ambushed, 0),
  
("infiltration_evil", "TLD_Infiltration_Evil.mp3", mtf_module_track|mtf_culture_evil|mtf_sit_town_infiltrate, mtf_culture_all),
("infiltration_good", "TLD_Infiltrate_Good.mp3"  , mtf_module_track|mtf_culture_good|mtf_sit_town_infiltrate, mtf_culture_all),

# ("lords_hall_swadian", "lords_hall_swadian.ogg"    ,                 mtf_culture_1|mtf_sit_travel, mtf_sit_night|mtf_sit_tavern),
# ("lords_hall_goodmen", "TLD_Rohan_LordHall.mp3"    ,mtf_module_track|mtf_culture_2|mtf_sit_travel, mtf_sit_night|mtf_sit_tavern),
# ("lords_hall_orcs"   , "lords_hall_khergit.ogg"    ,                 mtf_culture_3|mtf_sit_travel, mtf_sit_night|mtf_sit_tavern|mtf_culture_all),
# ("lords_hall_nord"   , "lords_hall_nord.ogg"       ,                               mtf_sit_travel, mtf_sit_night|mtf_sit_tavern),
# ("lords_hall_rhodok" , "lords_hall_rhodok.ogg"     ,                               mtf_sit_travel, mtf_sit_night|mtf_sit_tavern),
# ("lords_hall_khand","TLD_Easterlings_LordsHall.mp3",mtf_module_track|mtf_culture_5|mtf_sit_travel, mtf_sit_night|mtf_sit_tavern|mtf_culture_all),

# ("mounted_snow_terrain_calm", "mounted_snow_terrain_calm.ogg", mtf_sit_travel, mtf_sit_night|mtf_sit_tavern),
("neutral_infiltration", "neutral_infiltration.ogg", mtf_sit_town_infiltrate, 0),
# ("outdoor_beautiful_land", "outdoor_beautiful_land.ogg", mtf_sit_travel, mtf_sit_night|mtf_sit_tavern),
("retreat", "retreat.ogg", mtf_persist_until_finished|mtf_sit_killed, 0),

#("seige_neutral", "TLD_Siege.mp3", mtf_module_track|mtf_sit_siege, mtf_sit_fight|mtf_sit_ambushed),

#no taverns in TLD
# ("tavern_1", "tavern_1.ogg", mtf_sit_tavern, 0),
# ("tavern_2", "tavern_2.ogg", mtf_sit_tavern, 0),

#old town music
# ("town_neutral", "TLD_Town_Neutral.mp3" ,mtf_module_track|              mtf_sit_town|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night),
# ("town_khergit", "TLD_Isengard_Town.mp3",mtf_module_track|mtf_culture_3|mtf_sit_town|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
# ("town_nord"   , "town_nord.ogg"        ,                 mtf_culture_4|mtf_sit_town|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
# ("town_rhodok" , "TLD_Harad_Town.mp3"   ,mtf_module_track|mtf_culture_5|mtf_sit_town|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
# ("town_swadian", "TLD_Town_Gondor.mp3"  ,mtf_module_track|mtf_culture_1|mtf_sit_town|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
# ("town_vaegir" , "TLD_Rohan_Town.mp3"   ,mtf_module_track|mtf_culture_2|mtf_sit_town|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),

#TLD town tracks
("TLD_Alliance_Towns",   "TLD_Alliance_Towns.mp3",   mtf_module_track, mtf_sit_town),

("TLD_Minas_Tirith",     "TLD_Minas_Tirith.mp3",     mtf_module_track, mtf_sit_town),
("TLD_Black_Root",   	 "TLD_Black_Root.mp3",       mtf_module_track, mtf_sit_town),
("TLD_Dol_Amroth",   	 "TLD_Dol_Amroth.mp3",       mtf_module_track, mtf_sit_town),
("TLD_Henneth_Annun",	 "TLD_Henneth_Annun.mp3",    mtf_module_track, mtf_sit_town),
("TLD_Pinnath_Gelin",	 "TLD_Pinnath_Gelin.mp3",    mtf_module_track, mtf_sit_town),
#("TLD_Lamedon",    	 "TLD_Lossarnach.mp3",       mtf_module_track, mtf_sit_town),
("TLD_Lossarnach",    	 "TLD_Lossarnach.mp3",       mtf_module_track, mtf_sit_town),
("TLD_Osgiliath",    	 "TLD_Osgiliath.mp3",        mtf_module_track, mtf_sit_town),
#("TLD_Pelagir",    	 "TLD_Pelagir.mp3",          mtf_module_track, mtf_sit_town),

("TLD_Gondor_Cities",    "TLD_Gondor_Cities.mp3",    mtf_module_track, mtf_sit_town),
("TLD_Edoras",           "TLD_Edoras.mp3",           mtf_module_track, mtf_sit_town),
("TLD_Helms_Deep",       "TLD_Helms_Deep.mp3",       mtf_module_track, mtf_sit_town),
("TLD_Rohan_Village",    "TLD_Rohan_Village.mp3",    mtf_module_track, mtf_sit_town),
("TLD_Erebor",           "TLD_Erebor.mp3",           mtf_module_track, mtf_sit_town),
("TLD_Iron_Hill_Mine",   "TLD_Iron_Hill_Mine.mp3",   mtf_module_track, mtf_sit_town),
("TLD_Minas_Morgul",     "TLD_Minas_Morgul.mp3",     mtf_module_track, mtf_sit_town),
("TLD_Orc_Camp",         "TLD_Orc_Camp.mp3",         mtf_module_track, mtf_sit_town),
("TLD_Isengard_Town",    "TLD_Isengard_Town.mp3",    mtf_module_track, mtf_sit_town),
("TLD_Uruk_Camp",        "TLD_Uruk_Camp.mp3",        mtf_module_track, mtf_sit_town),
("TLD_Lothlorien",       "TLD_Lothlorien.mp3",       mtf_module_track, mtf_sit_town),
("TLD_Rivendell_Camp",   "TLD_Rivendell_Camp.mp3",   mtf_module_track, mtf_sit_town),
("TLD_Mirkwood_Camp",    "TLD_Mirkwood_Camp.mp3",    mtf_module_track, mtf_sit_town),
("TLD_Esgaroth",         "TLD_Esgaroth.mp3",         mtf_module_track, mtf_sit_town),
("TLD_Dale",             "TLD_Dale.mp3",             mtf_module_track, mtf_sit_town),
("TLD_Harad_Camp",       "TLD_Harad_Camp.mp3",       mtf_module_track, mtf_sit_town),
("TLD_Rhun_Encampment",  "TLD_Rhun_Encampment.mp3",  mtf_module_track, mtf_sit_town),
("TLD_Khand_Encampment", "TLD_Khand_Encampment.mp3", mtf_module_track, mtf_sit_town),
("TLD_Corsair_Camp",     "TLD_Corsair_Camp.mp3",     mtf_module_track, mtf_sit_town),
("TLD_Gundabad_Camp",    "TLD_Gundabad_Camp.mp3",    mtf_module_track, mtf_sit_town),
("TLD_Dunland_Camp",     "TLD_Dunland_Camp.mp3",     mtf_module_track, mtf_sit_town),
("TLD_Beorning_Town",    "TLD_Beorning_Town.mp3",    mtf_module_track, mtf_sit_town),

#old travel tracks
# ("travel_khergit", "travel_khergit.ogg",                 mtf_culture_3|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
# ("travel_neutral", "travel_neutral.ogg",                               mtf_sit_travel, mtf_sit_tavern|mtf_sit_night                ),
# ("travel_nord",    "travel_nord.ogg"   ,                 mtf_culture_4|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
# ("travel_rhodok",  "travel_rhodok.ogg" ,                 mtf_culture_5|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
# ("travel_swadian", "TLD_Gondor_Map.mp3",mtf_module_track|mtf_culture_1|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
# ("travel_vaegir",  "travel_vaegir.ogg" ,                 mtf_culture_2|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
# ("travel_khand",  "travel_neutral.ogg" ,                 mtf_culture_5|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
# ("travel_umbar", "TLD_Corsair_Map.mp3" ,mtf_module_track|mtf_culture_5|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
# ("uncertain_homestead", "uncertain_homestead.ogg", mtf_sit_travel, mtf_sit_night|mtf_sit_tavern),

#TLD travel tracks
#Common travel and night tracks
#If the number of the Day tracks change, update script_music_set_situation_with_culture
("TLD_Map_Day_A", "Day-Night-Map\TLD_Map_Day_A.mp3", mtf_module_track, mtf_sit_travel),
("TLD_Map_Day_B", "Day-Night-Map\TLD_Map_Day_B.mp3", mtf_module_track, mtf_sit_travel),
("TLD_Map_Day_C", "Day-Night-Map\TLD_Map_Day_C.mp3", mtf_module_track, mtf_sit_travel),
("TLD_Map_Day_D", "Day-Night-Map\TLD_Map_Day_D.mp3", mtf_module_track, mtf_sit_travel),
("TLD_Map_Day_E", "Day-Night-Map\TLD_Map_Day_E.mp3", mtf_module_track, mtf_sit_travel),
("TLD_Map_Day_F", "Day-Night-Map\TLD_Map_Day_F.mp3", mtf_module_track, mtf_sit_travel),
("TLD_Map_Day_G", "Day-Night-Map\TLD_Map_Day_G.mp3", mtf_module_track, mtf_sit_travel),
("TLD_Map_Day_H", "Day-Night-Map\TLD_Map_Day_H.mp3", mtf_module_track, mtf_sit_travel),
("TLD_Map_Day_I", "Day-Night-Map\TLD_Map_Day_I.mp3", mtf_module_track, mtf_sit_travel),
("TLD_Map_Day_J", "Day-Night-Map\TLD_Map_Day_J.mp3", mtf_module_track, mtf_sit_travel),
("TLD_Map_Day_M", "Day-Night-Map\TLD_Map_Day_Misty_Mountains.mp3", mtf_module_track, mtf_sit_travel),
#Night tracks are played by the MB jukebox, plus night travel scripting
("TLD_Map_Night_A", "Day-Night-Map\TLD_Map_Night_A.mp3", mtf_module_track|mtf_sit_night, mtf_sit_travel),
("TLD_Map_Night_B", "Day-Night-Map\TLD_Map_Night_B.mp3", mtf_module_track|mtf_sit_night, mtf_sit_travel),
("TLD_Map_Night_C", "Day-Night-Map\TLD_Map_Night_C.mp3", mtf_module_track|mtf_sit_night, mtf_sit_travel),
("TLD_Map_Night_D", "Day-Night-Map\TLD_Map_Night_D.mp3", mtf_module_track|mtf_sit_night, mtf_sit_travel),
("TLD_Map_Night_E", "Day-Night-Map\TLD_Map_Night_E.mp3", mtf_module_track|mtf_sit_night, mtf_sit_travel),
("TLD_Map_Night_F", "Day-Night-Map\TLD_Map_Night_F.mp3", mtf_module_track|mtf_sit_night, mtf_sit_travel),
("TLD_Map_Night_N", "Day-Night-Map\TLD_Map_Night_Nightfall_On_The_Anduin.mp3", mtf_module_track|mtf_sit_night, mtf_sit_travel),
#Faction territory tracks - faction tracks need to be kept together
#If any of these tracks change, you need to update script_music_set_situation_with_culture
("TLD_Map_Dunland_A", "Day-Night-Map\TLD_Map_Dunland_A.mp3", mtf_module_track|mtf_culture_evilmen, mtf_sit_travel),
("TLD_Map_Dunland_B", "Day-Night-Map\TLD_Map_Dunland_B.mp3", mtf_module_track|mtf_culture_evilmen, mtf_sit_travel),
("TLD_Map_Dwarves_A", "Day-Night-Map\TLD_Map_Dwarves_A.mp3", mtf_module_track|mtf_culture_rohan_goodmen, mtf_sit_travel),
("TLD_Map_Dwarves_B", "Day-Night-Map\TLD_Map_Dwarves_B.mp3", mtf_module_track|mtf_culture_rohan_goodmen, mtf_sit_travel),
("TLD_Map_Dwarves_C", "Day-Night-Map\TLD_Map_Dwarves_C.mp3", mtf_module_track|mtf_culture_rohan_goodmen, mtf_sit_travel),
("TLD_Map_Elven_A", "Day-Night-Map\TLD_Map_Elven_A.mp3", mtf_module_track|mtf_culture_elves, mtf_sit_travel),
("TLD_Map_Elven_B", "Day-Night-Map\TLD_Map_Elven_B.mp3", mtf_module_track|mtf_culture_elves, mtf_sit_travel),
("TLD_Map_Elven_C", "Day-Night-Map\TLD_Map_Elven_C.mp3", mtf_module_track|mtf_culture_elves, mtf_sit_travel),
("TLD_Map_Elven_D", "Day-Night-Map\TLD_Map_Elven_D.mp3", mtf_module_track|mtf_culture_elves, mtf_sit_travel),
("TLD_Map_Elven_E", "Day-Night-Map\TLD_Map_Elven_E.mp3", mtf_module_track|mtf_culture_elves, mtf_sit_travel),
("TLD_Map_Gondor_A", "Day-Night-Map\TLD_Map_Gondor_A.mp3", mtf_module_track|mtf_culture_gondor, mtf_sit_travel),
("TLD_Map_Gondor_B", "Day-Night-Map\TLD_Map_Gondor_B.mp3", mtf_module_track|mtf_culture_gondor, mtf_sit_travel),
("TLD_Map_Gondor_C", "Day-Night-Map\TLD_Map_Gondor_C.mp3", mtf_module_track|mtf_culture_gondor, mtf_sit_travel),
("TLD_Map_Gondor_D", "Day-Night-Map\TLD_Map_Gondor_D.mp3", mtf_module_track|mtf_culture_gondor, mtf_sit_travel),
("TLD_Map_Gondor_E", "Day-Night-Map\TLD_Map_Gondor_E.mp3", mtf_module_track|mtf_culture_gondor, mtf_sit_travel),
("TLD_Map_Harad_A", "Day-Night-Map\TLD_Map_Harad_A.mp3", mtf_module_track|mtf_culture_harad, mtf_sit_travel),
("TLD_Map_Harad_B", "Day-Night-Map\TLD_Map_Harad_B.mp3", mtf_module_track|mtf_culture_harad, mtf_sit_travel),
("TLD_Map_Harad_C", "Day-Night-Map\TLD_Map_Harad_C.mp3", mtf_module_track|mtf_culture_harad, mtf_sit_travel),
("TLD_Map_Harad_D", "Day-Night-Map\TLD_Map_Harad_D.mp3", mtf_module_track|mtf_culture_harad, mtf_sit_travel),
("TLD_Map_Khand_A", "Day-Night-Map\TLD_Map_Khand_A.mp3", mtf_module_track|mtf_culture_evilmen, mtf_sit_travel),
("TLD_Map_Khand_B", "Day-Night-Map\TLD_Map_Khand_B.mp3", mtf_module_track|mtf_culture_evilmen, mtf_sit_travel),
("TLD_Map_Khand_C", "Day-Night-Map\TLD_Map_Khand_C.mp3", mtf_module_track|mtf_culture_evilmen, mtf_sit_travel),
("TLD_Map_Orcs_A", "Day-Night-Map\TLD_Map_Orcs_A.mp3", mtf_module_track|mtf_culture_orcs, mtf_sit_travel),
("TLD_Map_Orcs_B", "Day-Night-Map\TLD_Map_Orcs_B.mp3", mtf_module_track|mtf_culture_orcs, mtf_sit_travel),
("TLD_Map_Orcs_C", "Day-Night-Map\TLD_Map_Orcs_C.mp3", mtf_module_track|mtf_culture_orcs, mtf_sit_travel),
("TLD_Map_Orcs_D", "Day-Night-Map\TLD_Map_Orcs_D.mp3", mtf_module_track|mtf_culture_orcs, mtf_sit_travel),
("TLD_Map_Rohan_A", "Day-Night-Map\TLD_Map_Rohan_A.mp3", mtf_module_track|mtf_culture_rohan_goodmen, mtf_sit_travel),
("TLD_Map_Rohan_B", "Day-Night-Map\TLD_Map_Rohan_B.mp3", mtf_module_track|mtf_culture_rohan_goodmen, mtf_sit_travel),
("TLD_Map_Rohan_C", "Day-Night-Map\TLD_Map_Rohan_C.mp3", mtf_module_track|mtf_culture_rohan_goodmen, mtf_sit_travel),
("TLD_Map_Rohan_D", "Day-Night-Map\TLD_Map_Rohan_D.mp3", mtf_module_track|mtf_culture_rohan_goodmen, mtf_sit_travel),


# victory tracks, never called directly
("victorious_good1", "Battle\TLD_Victory_Good_1.mp3", mtf_module_track|mtf_culture_good|mtf_persist_until_finished|mtf_sit_victorious, 0),
("victorious_good2", "Battle\TLD_Victory_Good_2.mp3", mtf_module_track|mtf_culture_good|mtf_persist_until_finished|mtf_sit_victorious, 0),
("victorious_good3", "Battle\TLD_Victory_Good_3.mp3", mtf_module_track|mtf_culture_good|mtf_persist_until_finished|mtf_sit_victorious, 0),
("victorious_evil1", "Battle\TLD_Victory_Evil_1.mp3", mtf_module_track|mtf_culture_evil|mtf_persist_until_finished|mtf_sit_victorious, 0),
("victorious_evil2", "Battle\TLD_Victory_Evil_2.mp3", mtf_module_track|mtf_culture_evil|mtf_persist_until_finished|mtf_sit_victorious, 0),
("victorious_evil3", "Battle\TLD_Victory_Evil_3.mp3", mtf_module_track|mtf_culture_evil|mtf_persist_until_finished|mtf_sit_victorious, 0),

]
