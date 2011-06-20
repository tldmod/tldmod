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
("mount_and_blade_title_screen", "TLD_A_Tale_Untold.mp3", mtf_module_track|mtf_sit_main_title|mtf_start_immediately, 0),

("ambushed_by_neutral", "TLD_Rohan_Ambush.mp3", mtf_module_track|mtf_sit_ambushed|mtf_sit_siege, mtf_sit_fight),
("ambushed_by_khergit", "TLD_Orc_Ambush.mp3", mtf_module_track|mtf_culture_all|mtf_sit_ambushed|mtf_sit_siege, mtf_sit_fight|mtf_culture_all),

("arena_1", "arena_1.ogg", mtf_sit_arena, 0),
("armorer", "armorer.ogg", mtf_sit_travel, 0),
("bandit_fight", "bandit_fight.ogg", mtf_sit_fight|mtf_sit_ambushed, 0),

("calm_night_1", "TLD_NightMusic.mp3", mtf_module_track|mtf_sit_night, mtf_sit_town|mtf_sit_tavern|mtf_sit_travel),
("captured", "capture.ogg", mtf_persist_until_finished, 0),

("defeated_by_neutral","TLD_Killed_By_Evil.mp3",mtf_module_track|                 mtf_persist_until_finished|mtf_sit_killed, 0),
("defeated_by_neutral_2", "defeated_by_neutral_2.ogg",                            mtf_persist_until_finished|mtf_sit_killed, 0),
("defeated_by_neutral_3", "defeated_by_neutral_3.ogg",                            mtf_persist_until_finished|mtf_sit_killed, 0),
("killed_by_swadian", "killed_by_swadian.ogg" ,                  mtf_culture_good|mtf_persist_until_finished|mtf_sit_killed, 0),
("killed_by_khergit", "TLD_Killed_By_Evil.mp3", mtf_module_track|mtf_culture_evil|mtf_persist_until_finished|mtf_sit_killed, 0),
  

("empty_village", "empty_village.ogg", mtf_persist_until_finished, 0),
("encounter_hostile_nords", "encounter_hostile_nords.ogg", mtf_persist_until_finished|mtf_sit_encounter_hostile, 0),
("escape", "escape.ogg", mtf_persist_until_finished, 0),

("fight_1"              , "fight_1.ogg"              ,               mtf_sit_fight|mtf_sit_ambushed, 0),
("fight_2"              , "fight_2.ogg"              ,               mtf_sit_fight|mtf_sit_ambushed, 0),
("fight_3"              , "fight_3.ogg"              ,               mtf_sit_fight|mtf_sit_ambushed, 0),
("fight_as_vaegir"      , "fight_as_vaegir.ogg"      , mtf_culture_2|mtf_sit_fight|mtf_sit_ambushed, mtf_culture_all),
("fight_as_khergit"     , "fight_as_khergit.ogg"     , mtf_culture_3|mtf_sit_fight|mtf_sit_ambushed, mtf_culture_all),
("fight_as_nord"        , "fight_as_nord.ogg"        , mtf_culture_4|mtf_sit_fight|mtf_sit_ambushed, mtf_culture_all),
("fight_as_rhodok"      , "fight_as_rhodok.ogg"      , mtf_culture_5|mtf_sit_fight|mtf_sit_ambushed, mtf_culture_all),
("fight_while_mounted_1", "fight_while_mounted_1.ogg",               mtf_sit_fight|mtf_sit_ambushed, 0),
("fight_while_mounted_2", "fight_while_mounted_2.ogg",               mtf_sit_fight|mtf_sit_ambushed, 0),
  
("infiltration_evil", "TLD_Infiltration_Evil.mp3", mtf_module_track|mtf_culture_evil|mtf_sit_town_infiltrate, mtf_culture_all),
("infiltration_good", "TLD_Infiltrate_Good.mp3"  , mtf_module_track|mtf_culture_good|mtf_sit_town_infiltrate, mtf_culture_all),

("lords_hall_swadian", "lords_hall_swadian.ogg"    ,                 mtf_culture_1|mtf_sit_travel, mtf_sit_town|mtf_sit_night|mtf_sit_tavern),
("lords_hall_goodmen", "TLD_Rohan_LordHall.mp3"    ,mtf_module_track|mtf_culture_2|mtf_sit_travel, mtf_sit_town|mtf_sit_night|mtf_sit_tavern),
("lords_hall_orcs"   , "lords_hall_khergit.ogg"    ,                 mtf_culture_3|mtf_sit_travel, mtf_sit_town|mtf_sit_night|mtf_sit_tavern|mtf_culture_all),
("lords_hall_nord"   , "lords_hall_nord.ogg"       ,                               mtf_sit_travel, mtf_sit_town|mtf_sit_night|mtf_sit_tavern),
("lords_hall_rhodok" , "lords_hall_rhodok.ogg"     ,                               mtf_sit_travel, mtf_sit_town|mtf_sit_night|mtf_sit_tavern),
("lords_hall_khand","TLD_Easterlings_LordsHall.mp3",mtf_module_track|mtf_culture_5|mtf_sit_travel, mtf_sit_town|mtf_sit_night|mtf_sit_tavern|mtf_culture_all),

("mounted_snow_terrain_calm", "mounted_snow_terrain_calm.ogg", mtf_sit_travel, mtf_sit_town|mtf_sit_night|mtf_sit_night|mtf_sit_tavern),
("neutral_infiltration", "neutral_infiltration.ogg", mtf_sit_town_infiltrate, 0),
("outdoor_beautiful_land", "outdoor_beautiful_land.ogg", mtf_sit_travel, mtf_sit_town|mtf_sit_night|mtf_sit_night|mtf_sit_tavern),
("retreat", "retreat.ogg", mtf_persist_until_finished|mtf_sit_killed, 0),

("seige_neutral", "TLD_Siege.mp3", mtf_module_track|mtf_sit_siege, mtf_sit_fight|mtf_sit_ambushed),

("tavern_1", "tavern_1.ogg", mtf_sit_tavern, 0),
("tavern_2", "tavern_2.ogg", mtf_sit_tavern, 0),

("town_neutral", "TLD_Town_Neutral.mp3" ,mtf_module_track|              mtf_sit_town|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night),
("town_khergit", "TLD_Isengard_Town.mp3",mtf_module_track|mtf_culture_3|mtf_sit_town|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
("town_nord"   , "town_nord.ogg"        ,                 mtf_culture_4|mtf_sit_town|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
("town_rhodok" , "TLD_Harad_Town.mp3"   ,mtf_module_track|mtf_culture_5|mtf_sit_town|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
("town_swadian", "TLD_Town_Gondor.mp3"  ,mtf_module_track|mtf_culture_1|mtf_sit_town|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
("town_vaegir" , "TLD_Rohan_Town.mp3"   ,mtf_module_track|mtf_culture_2|mtf_sit_town|mtf_sit_travel, mtf_sit_tavern|mtf_sit_night|mtf_culture_all),

("travel_khergit", "travel_khergit.ogg",                 mtf_culture_3|mtf_sit_travel, mtf_sit_town|mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
("travel_neutral", "travel_neutral.ogg",                               mtf_sit_travel, mtf_sit_town|mtf_sit_tavern|mtf_sit_night                ),
("travel_nord",    "travel_nord.ogg"   ,                 mtf_culture_4|mtf_sit_travel, mtf_sit_town|mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
("travel_rhodok",  "travel_rhodok.ogg" ,                 mtf_culture_5|mtf_sit_travel, mtf_sit_town|mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
("travel_swadian", "TLD_Gondor_Map.mp3",mtf_module_track|mtf_culture_1|mtf_sit_travel, mtf_sit_town|mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
("travel_vaegir",  "travel_vaegir.ogg" ,                 mtf_culture_2|mtf_sit_travel, mtf_sit_town|mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
("travel_khand",  "travel_neutral.ogg" ,                 mtf_culture_5|mtf_sit_travel, mtf_sit_town|mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
("travel_umbar", "TLD_Corsair_Map.mp3" ,mtf_module_track|mtf_culture_5|mtf_sit_travel, mtf_sit_town|mtf_sit_tavern|mtf_sit_night|mtf_culture_all),
  
("uncertain_homestead", "uncertain_homestead.ogg", mtf_sit_travel, mtf_sit_town|mtf_sit_night|mtf_sit_tavern),

# victory tracks, never called directly
("victorious_good1", "TLD_Victory_Good_1.mp3", mtf_module_track|mtf_culture_good|mtf_persist_until_finished|mtf_sit_victorious, 0),
("victorious_good2", "TLD_Victory_Good_2.mp3", mtf_module_track|mtf_culture_good|mtf_persist_until_finished|mtf_sit_victorious, 0),
("victorious_good3", "TLD_Victory_Good_3.mp3", mtf_module_track|mtf_culture_good|mtf_persist_until_finished|mtf_sit_victorious, 0),
("victorious_evil1", "TLD_Victory_Evil_1.mp3", mtf_module_track|mtf_culture_evil|mtf_persist_until_finished|mtf_sit_victorious, 0),
("victorious_evil2", "TLD_Victory_Evil_2.mp3", mtf_module_track|mtf_culture_evil|mtf_persist_until_finished|mtf_sit_victorious, 0),
("victorious_evil3", "TLD_Victory_Evil_3.mp3", mtf_module_track|mtf_culture_evil|mtf_persist_until_finished|mtf_sit_victorious, 0),
#  ("victorious_neutral_1", "victorious_neutral_1.ogg", mtf_persist_until_finished|mtf_sit_victorious, 0),
#  ("victorious_neutral_2", "victorious_neutral_2.ogg", mtf_persist_until_finished|mtf_sit_victorious, 0),
#  ("victorious_neutral_3", "victorious_neutral_3.ogg", mtf_persist_until_finished|mtf_sit_victorious, 0),
]
