from header_common import *
from header_parties import *
from ID_troops import *
from ID_factions import *
from ID_map_icons import *

pmf_is_prisoner = 0x0001


####################################################################################################################
#  Each party template record contains the following fields:
#  1) Party-template id: used for referencing party-templates in other files.
#     The prefix pt_ is automatically added before each party-template id.
#  2) Party-template name.
#  3) Party flags. See header_parties.py for a list of available flags
#  4) Menu. ID of the menu to use when this party is met. The value 0 uses the default party encounter system.
#  5) Faction
#  6) Personality. See header_parties.py for an explanation of personality flags.
#  7) List of stacks. Each stack record is a tuple that contains the following fields:
#    7.1) Troop-id. 
#    7.2) Minimum number of troops in the stack. 
#    7.3) Maximum number of troops in the stack. 
#    7.4) Member flags(optional). Use pmf_is_prisoner to note that this member is a prisoner.
#     Note: There can be at most 6 stacks.
####################################################################################################################


party_templates = [
  ("none","none",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
  ("rescued_prisoners","Rescued Prisoners",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
  ("enemy","Enemy",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
  ("hero_party","Hero Party",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
####################################################################################################################
# Party templates before this point are hard-wired into the game and should not be changed. 
####################################################################################################################
##  ("old_garrison","Old Garrison",icon_eorl_guard_of_rohan,0,fac_neutral,merchant_personality,[]),
  ("village_defenders","Village Defenders",icon_peasant,0,fac_commoners,merchant_personality,[(trp_farmer,10,20),(trp_peasant_woman,0,4)]),

  ("cattle_herd","Cattle Herd",icon_cattle|carries_goods(10),0,fac_neutral,merchant_personality,[(trp_cattle,80,120)]),
  ("ruins","Ruins",icon_ancient_ruins,0,fac_commoners,merchant_personality,[(trp_farmer,1,1)]),
  ("legendary_place","Legendary Place",icon_camp,0,fac_commoners,merchant_personality,[(trp_farmer,1,1)]),
  
##  ("vaegir_nobleman","Vaegir Nobleman",icon_eorl_guard_of_rohan|carries_goods(10)|pf_quest_party,0,fac_commoners,merchant_personality,[(trp_nobleman,1,1),(trp_eorl_guard_of_rohan,2,6),(trp_brego_guard_of_rohan,4,12)]),
##  ("swadian_nobleman","Swadian Nobleman",icon_gray_knight|carries_goods(10)|pf_quest_party,0,fac_commoners,merchant_personality,[(trp_nobleman,1,1),(trp_veteran_knight_of_gondor,2,6),(trp_knight_of_the_citadel,4,12)]),

 ("manhunters","Manhunters",icon_gray_knight,0,fac_manhunters,soldier_personality,[(trp_manhunter,9,40)]),
##  ("peasant","Peasant",icon_peasant,0,fac_commoners,merchant_personality,[(trp_farmer,1,6),(trp_peasant_woman,0,7)]),

  ("wild_troll"      ,"Wild Troll"        ,icon_wild_troll|carries_goods(0),0,fac_outlaws,bandit_personality,[(trp_troll_of_moria,1,2),]),
  ("raging_trolls"   ,"Raging Trolls"        ,icon_wild_troll|carries_goods(0),0,fac_outlaws,bandit_personality,[(trp_troll_of_moria,1,3),]),

  ("looters"         ,"Tribal Orcs"       ,icon_orc_tribal|carries_goods(8),0,fac_outlaws,bandit_personality,[(trp_tribal_orc_warrior,0,1),(trp_tribal_orc,2,25)]),
  
  ("forest_bandits"  ,"Orc Stragglers"       ,icon_orc_tribal|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_tribal_orc_chief,0,1),(trp_tribal_orc_warrior,0,8),(trp_tribal_orc,3,40),(trp_mountain_goblin,1,30)]),
  ("mountain_bandits","Wild Goblins"    ,icon_orc_tribal|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_mountain_goblin,2,40)]),
  ("steppe_bandits"  ,"Dunlending Raiders",icon_khergit   |carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_dunnish_raven_rider,3,48)]),
  ("sea_raiders"     ,"Corsair Raiders"   ,icon_axeman    |carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_corsair_marauder,3,50)]),

  ("deserters","Deserters",icon_vaegir_knight|carries_goods(3),0,fac_deserters,bandit_personality,[]),

  ("merchant_caravan","Merchant Caravan",icon_gray_knight|carries_goods(20)|pf_auto_remove_in_town|pf_quest_party,0,fac_commoners,escorted_merchant_personality,[(trp_caravan_master,1,1),(trp_caravan_guard,5,25)]),
  ("troublesome_bandits","Troublesome Goblins",icon_axeman|carries_goods(9)|pf_quest_party,0,fac_outlaws,bandit_personality,[(trp_mountain_goblin,14,55)]),
  ("fangorn_orcs","Tree-chopping Orcs",icon_axeman|carries_goods(9)|pf_quest_party,0,fac_neutral,bandit_personality,[(trp_fighting_uruk_hai_champion,1,1),(trp_large_uruk_hai_of_isengard,3,8),(trp_large_uruk_hai_scout,8,13),(trp_uruk_snaga_of_isengard,12,24)]),
  # ("bandits_awaiting_ransom","Bandits Awaiting Ransom",icon_axeman|carries_goods(9)|pf_auto_remove_in_town|pf_quest_party,0,fac_neutral,bandit_personality,[(trp_brigand,24,58),(trp_kidnapped_girl,1,1,pmf_is_prisoner)]),
  # ("kidnapped_girl","Kidnapped Girl",icon_woman|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_kidnapped_girl,1,1)]),

##  ("farmers","Farmers",icon_peasant,0,fac_innocents,merchant_personality,[(trp_farmer,11,22),(trp_peasant_woman,16,44)]),
  ("village_farmers","Village Farmers",icon_peasant,0,fac_innocents,merchant_personality,[(trp_farmer,5,10),(trp_peasant_woman,3,8)]),
##  ("refugees","Refugees",icon_woman_b,0,fac_innocents,merchant_personality,[(trp_refugee,19,48)]),
##  ("dark_hunters","Dark Hunters",icon_gray_knight,0,fac_dark_knights,soldier_personality,[(trp_dark_knight,4,42),(trp_dark_hunter,13,25)]),

  ("spy_partners", "Suspicious Travellers", icon_gray_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy_partner,1,1),(trp_squire_of_dol_amroth,5,11)]),
  ("spy_partners_evil", "Suspicious Travellers", icon_gray_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy_partner_evil,1,1),(trp_dunnish_raven_rider,5,11)]),
  ("runaway_serfs","Runaway Slaves",icon_peasant|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_farmer,6,7), (trp_peasant_woman,3,3)]),
  ("spy", "Lone Rider", icon_gray_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy,1,1)]),
  ("spy_evil", "Lone Rider", icon_gray_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy_evil,1,1)]),
  ("sacrificed_messenger", "Sacrificed Messenger", icon_gray_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[]),
##  ("conspirator", "Conspirators", icon_gray_knight|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_conspirator,3,4)]),
##  ("conspirator_leader", "Conspirator Leader", icon_gray_knight|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_conspirator_leader,1,1)]),
##  ("peasant_rebels", "Peasant Rebels", icon_peasant,0,fac_peasant_rebels,bandit_personality,[(trp_peasant_rebel,33,97)]),
##  ("noble_refugees", "Noble Refugees", icon_gray_knight|carries_goods(12)|pf_quest_party,0,fac_noble_refugees,merchant_personality,[(trp_noble_refugee,3,5),(trp_noble_refugee_woman,5,7)]),

  ("forager_party","Foraging Party",icon_gray_knight|carries_goods(5)|pf_show_faction,0,fac_commoners,merchant_personality,[]),
  ("scout_party","Scouts",icon_gray_knight|carries_goods(1)|pf_show_faction,0,fac_commoners,bandit_personality,[]),
  ("patrol_party","Patrol",icon_gray_knight|carries_goods(2)|pf_show_faction,0,fac_commoners,soldier_personality,[]),
  ("war_party", "War Party",icon_gray_knight|carries_goods(3),0,fac_commoners,soldier_personality,[]),
  ("messenger_party","Messenger",icon_gray_knight|pf_show_faction,0,fac_commoners,merchant_personality,[]),
  ("raider_party","Raiders",icon_gray_knight|carries_goods(16)|pf_quest_party,0,fac_commoners,bandit_personality,[]),
  ("raider_captives","Raider Captives",0,0,fac_commoners,0,[(trp_peasant_woman,6,30,pmf_is_prisoner)]),
  ("kingdom_caravan_party","Caravan",icon_mule|carries_goods(25)|pf_show_faction,0,fac_commoners,merchant_personality,[(trp_caravan_master,1,1),(trp_caravan_guard,12,40)]),
  ("prisoner_train_party","Prisoner Train",icon_gray_knight|carries_goods(5)|pf_show_faction,0,fac_commoners,merchant_personality,[]),
  ("default_prisoners","Default Prisoners",0,0,fac_commoners,0,[(trp_brigand,5,10,pmf_is_prisoner)]),


# Caravans
#################
#   ("swadian_caravan","Swadian Caravan",icon_mule|carries_goods(25),0,fac_gondor,merchant_personality,[(trp_caravan_master,1,1),(trp_swordsmen_of_the_tower_guard,8,16),(trp_master_ranger_of_ithilien,5,20)]),
#   ("vaegir_caravan","Vaegir Caravan",icon_mule|carries_goods(25),0,fac_rohan,merchant_personality,[(trp_caravan_master,1,1),(trp_swordsmen_of_the_tower_guard,8,16),(trp_master_ranger_of_ithilien,5,20)]),

#Prisoner trains
#   ("swadian_prisoner_train","Gondor Prisoner Train",icon_gray_knight|carries_goods(5)|pf_show_faction,0,fac_gondor,merchant_personality,[(trp_swordsmen_of_the_tower_guard,8,16),(trp_master_ranger_of_ithilien,5,20),
#                                                       (trp_swordsmen_of_the_tower_guard,1,12,pmf_is_prisoner),(trp_swordsmen_of_the_tower_guard,6,10,pmf_is_prisoner),(trp_bandit,0,5,pmf_is_prisoner)]),
#   ("vaegir_prisoner_train","Rohan Prisoner Train",icon_vaegir_knight|carries_goods(5)|pf_show_faction,0,fac_rohan,merchant_personality,[(trp_swordsmen_of_the_tower_guard,8,16),(trp_master_ranger_of_ithilien,5,20),
#                                                       (trp_swordsmen_of_the_tower_guard,1,12,pmf_is_prisoner),(trp_swordsmen_of_the_tower_guard,6,10,pmf_is_prisoner),(trp_bandit,0,5,pmf_is_prisoner)]),
# ("swadian_foragers","Swadian Foragers",icon_gray_knight|carries_goods(5)|pf_show_faction,0,fac_gondor,soldier_personality,[(trp_swordsmen_of_the_tower_guard,8,16),(trp_master_ranger_of_ithilien,5,20)]),
# ("vaegir_foragers","Vaegir Foragers",icon_vaegir_knight|carries_goods(5)|pf_show_faction,0,fac_rohan,merchant_personality,[(trp_swordsmen_of_the_tower_guard,8,16),(trp_master_ranger_of_ithilien,5,20)]),

#TLD Scouts

("gondor_scouts"       ,"Gondorian Scouts" ,icon_ithilien_ranger|carries_goods(1)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_ranger_of_ithilien,1,1),(trp_gondor_militiamen,3,5),(trp_gondor_commoner,3,5)]),
("blackroot_auxila"    ,"Blackroot_Vale Auxilia",icon_gray_knight|carries_goods(1)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_blackroot_leader,1,1),(trp_veteran_blackroot_vale_archer,2,25),(trp_blackroot_vale_archer,6,30)]),
("lamedon_auxila"      ,"Lamedon Auxilia"   ,icon_axeman         |carries_goods(1)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_lamedon_leader,1,1),(trp_footman_of_lamedon,2,25),(trp_clansman_of_lamedon,6,30)]),
("pinnath_gelin_auxila","Pinnath_Gelin Auxilia",icon_axeman      |carries_goods(1)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_pinnath_leader,1,1),(trp_veteran_warrior_of_pinnath_gelin,2,25),(trp_warrior_of_pinnath_gelin,6,30)]),

("rohan_scouts"    ,"Rohirrim Scouts"      ,icon_knight_rohan |carries_goods(1)|pf_show_faction,0,fac_rohan   ,scout_personality,[(trp_elite_skirmisher_of_rohan,1,1),(trp_guardsman_of_rohan,3,5),(trp_rohan_youth,3,5)]),
("lorien_scouts"   ,"Lothlorien Scouts"    ,icon_lorien_elf_a |carries_goods(1)|pf_show_faction,0,fac_lorien  ,scout_personality,[(trp_lothlorien_veteran_warden,1,1),(trp_lothlorien_veteran_scout,3,5),(trp_lothlorien_scout,3,5)]),
("woodelf_scouts"  ,"Mirkwood Elven Scouts",icon_mirkwood_elf |carries_goods(1)|pf_show_faction,0,fac_woodelf ,scout_personality,[(trp_greenwood_veteran_archer,1,1),(trp_greenwood_archer,2,4),(trp_greenwood_spearman,2,4),(trp_greenwood_veteran_scout,2,4)]),
("imladris_scouts" ,"Rivendell Scouts"     ,icon_rivendell_elf|carries_goods(1)|pf_show_faction,0,fac_imladris,scout_personality,[(trp_arnor_man_at_arms,1,1),(trp_rivendell_veteran_scout,3,5),(trp_rivendell_scout,3,5)]),
("dale_scouts"     ,"Dale Scouts"          ,icon_gray_knight  |carries_goods(2)|pf_show_faction,0,fac_dale    ,scout_personality,[(trp_dale_marchwarden,1,1),(trp_dale_warrior,3,5),(trp_laketown_scout,3,5)]),
("dwarf_scouts"    ,"Dwarven Lookouts"     ,icon_axeman       |carries_goods(2)|pf_show_faction,0,fac_dwarf   ,scout_personality,[(trp_dwarven_archer,1,1),(trp_dwarven_hardened_warrior,3,5),(trp_dwarven_lookout,3,5)]),
("beorn_scouts"    ,"Beorning Scouts"      ,icon_axeman       |carries_goods(1)|pf_show_faction,0,fac_beorn   ,scout_personality,[(trp_beorning_carrock_berserker,1,1),(trp_beorning_sentinel,3,5),(trp_beorning_warrior,3,6)]),
("woodmen_scouts"  ,"Woodmen Scouts"       ,icon_axeman       |carries_goods(1)|pf_show_faction,0,fac_beorn   ,scout_personality,[(trp_fell_huntsmen_of_mirkwood,1,1),(trp_woodmen_scout,3,5),(trp_woodmen_skilled_forester,3,6)]),

("mordor_scouts"    ,"Mordor Scouts"       ,icon_orc                |carries_goods(1)|pf_show_faction,0,fac_mordor  ,scout_personality,[(trp_fell_orc_tracker_of_mordor,3,6),(trp_uruk_snaga_of_mordor,3,6)]),
("isengard_scouts"  ,"Isengard Scouts"     ,icon_orc_isengard       |carries_goods(1)|pf_show_faction,0,fac_isengard,scout_personality,[(trp_large_uruk_hai_scout,3,6),(trp_uruk_snaga_of_isengard,3,6)]),
("isengard_scouts_b","Isengard Warg Riders",icon_wargrider_run      |carries_goods(1)|pf_show_faction,0,fac_isengard,scout_personality,[(trp_white_hand_rider,1,1),(trp_warg_rider_of_isengard,3,6),(trp_wolf_rider_of_isengard,3,6)]),
("harad_scouts"     ,"Haradrim Scouts"     ,icon_harad_horseman     |carries_goods(1)|pf_show_faction,0,fac_harad   ,scout_personality,[(trp_harad_archer,3,6),(trp_harad_desert_warrior,3,6)]),
("dunland_scouts"   ,"Dunlending Scouts"   ,icon_dunlander          |carries_goods(1)|pf_show_faction,0,fac_dunland ,scout_personality,[(trp_dunnish_raven_rider,3,6),(trp_dunnish_pikeman,3,6)]),
("umbar_scouts"     ,"Corsair Scouts"      ,icon_umbar_corsair      |carries_goods(1)|pf_show_faction,0,fac_umbar   ,scout_personality,[(trp_corsair_veteran_marauder,3,6),(trp_corsair_veteran_raider,3,6)]),
("khand_scouts"     ,"Easterling Scouts"   ,icon_easterling_horseman|carries_goods(1)|pf_show_faction,0,fac_umbar   ,scout_personality,[(trp_easterling_elite_skirmisher,3,6),(trp_easterling_horseman,3,6)]),
("moria_scouts"     ,"Moria Scouts"        ,icon_orc                |carries_goods(1)|pf_show_faction,0,fac_moria   ,scout_personality,[(trp_fell_goblin_archer_of_moria,1,1),(trp_warg_rider_of_moria,3,6),(trp_goblin_of_moria,3,5)]),
("guldur_scouts"    ,"Dol Guldur Scouts"   ,icon_orc_tribal         |carries_goods(1)|pf_show_faction,0,fac_guldur  ,scout_personality,[(trp_fell_morgul_orc,1,1),(trp_orc_archer_of_mordor,3,6),(trp_goblin_of_moria,3,5)]),
("gundabad_scouts"  ,"Gundabad Scouts"     ,icon_orc_tribal         |carries_goods(1)|pf_show_faction,0,fac_gundabad,scout_personality,[(trp_goblin_north_clan_rider,1,1),(trp_keen_eyed_goblin_archer_gundabad,3,5),(trp_orc_gundabad,3,6)]),
("rhun_scouts"      ,"Rhun Scouts"         ,icon_vaegir_knight      |carries_goods(1)|pf_show_faction,0,fac_rhun    ,scout_personality,[(trp_rhun_horse_archer,1,1),(trp_rhun_swift_horseman,3,6),(trp_rhun_house_scout,3,5)]),
 
####TLD Raiders
("gondor_raiders"  ,"Gondor Foragers"    ,icon_knight_gondor|carries_goods(1),0,fac_gondor  ,soldier_personality,[(trp_footmen_of_gondor,10,15),(trp_bowmen_of_gondor,10,15),(trp_squire_of_gondor,1,1)]),
("rohan_raiders"   ,"Rohan Foragers"     ,icon_knight_rohan |carries_goods(1),0,fac_rohan   ,soldier_personality,[(trp_esquire_of_rohan,5,10),(trp_rider_of_rohan,3,8),(trp_skirmisher_of_rohan,3,8),(trp_elite_rider_of_rohan,1,1)]),
("imladris_raiders","Rivendell Foragers" ,icon_rivendell_elf|carries_goods(2),0,fac_imladris,soldier_personality,[(trp_rivendell_infantry,10,15),(trp_rivendell_sentinel,10,15),(trp_rivendell_royal_infantry,1,1)]),
("lorien_raiders"  ,"Lothlorien Foragers",icon_lorien_elf_a |carries_goods(2),0,fac_lorien  ,soldier_personality,[(trp_lothlorien_infantry,6,15),(trp_lothlorien_archer,6,15),(trp_galadhrim_royal_warden,1,1)]),
("woodelf_raiders" ,"Mirkwood Foragers"  ,icon_mirkwood_elf |carries_goods(2),0,fac_woodelf ,soldier_personality,[(trp_greenwood_veteran_spearman,5,15),(trp_greenwood_veteran_archer,5,15),(trp_greenwood_royal_spearman,1,1)]),
("dale_raiders"    ,"Dale Foragers"      ,icon_gray_knight  |carries_goods(2),0,fac_dale    ,soldier_personality,[(trp_merchant_squire_or_dale,4,10),(trp_dale_man_at_arms,4,10),(trp_laketown_scout,4,10),(trp_girions_guard_of_dale,1,1)]),
("dwarf_raiders"   ,"Dwarven Foragers"   ,icon_dwarf        |carries_goods(2),0,fac_dwarf   ,soldier_personality,[(trp_dwarven_hardened_warrior,5,15),(trp_dwarven_lookout,5,15),(trp_dwarven_expert_axeman,1,1)]),
#("beorning_raiders","Beorning Foragers" ,icon_gray_knight  |carries_goods(1),0,fac_beorn   ,soldier_personality,[(trp_blank,10,15),(trp_blank,10,15),(trp_blank,1,1)]),

("mordor_raiders"  ,"Mordor Raiders"    ,icon_uruk          |carries_goods(1),0,fac_mordor  ,soldier_personality,[(trp_orc_snaga_of_mordor,15,20),(trp_orc_archer_of_mordor,15,20),(trp_fell_morgul_orc,1,1)]),
("isengard_raiders","Isengard Raiders"  ,icon_uruk_isengard |carries_goods(1),0,fac_isengard,soldier_personality,[(trp_uruk_snaga_of_isengard,8,13),(trp_large_uruk_hai_scout,8,13),(trp_large_uruk_hai_of_isengard,3,8),(trp_fighting_uruk_hai_champion,1,1)]),
("dunland_raiders" ,"Dunlending Raiders",icon_dunlander     |carries_goods(2),0,fac_dunland ,soldier_personality,[(trp_dunnish_wildman,15,20),(trp_dunnish_raven_rider,15,20),(trp_dunnish_wolf_guard,1,1)]),
("harad_raiders"   ,"Haradrim Raiders"  ,icon_harad_horseman|carries_goods(2),0,fac_harad   ,soldier_personality,[(trp_harad_desert_warrior,11,20),(trp_harad_archer,10,20),(trp_harad_black_serpent_infantry,1,1)]),
("khand_raiders"   ,"Khand Raiders"     ,icon_cataphract    |carries_goods(2),0,fac_khand   ,soldier_personality,[(trp_easterling_veteran_horseman,5,15),(trp_easterling_rider,5,15),(trp_easterling_horsemaster,1,1)]),
("umbar_raiders"   ,"Umbar Raiders"     ,icon_umbar_corsair |carries_goods(2),0,fac_umbar   ,soldier_personality,[(trp_corsair_warrior,4,10),(trp_corsair_raider,4,10),(trp_corsair_veteran_raider,4,10),(trp_corsair_night_raider,1,1)]),
("moria_raiders"   ,"Moria Raiders"     ,icon_orc           |carries_goods(2),0,fac_moria   ,soldier_personality,[(trp_warg_rider_of_moria,5,15),(trp_goblin_of_moria,5,15),(trp_fell_goblin_archer_of_moria,1,1)]),
("guldur_raiders"  ,"Dol Guldur Raiders",icon_orc_tribal    |carries_goods(2),0,fac_guldur  ,soldier_personality,[(trp_orc_of_guldur,4,10),(trp_large_orc_of_mordor,4,10),(trp_fell_orc_of_mordor,4,10),(trp_fell_orc_tracker_of_mordor,1,1)]),
("gundabad_raiders","Gundabad Raiders"  ,icon_orc_tribal    |carries_goods(2),0,fac_gundabad,soldier_personality,[(trp_orc_gundabad,5,15),(trp_keen_eyed_goblin_archer_gundabad,5,15),(trp_goblin_north_clan_rider,1,1)]),
("rhun_raiders"    ,"Rhun Raiders"      ,icon_gray_knight   |carries_goods(1),0,fac_rhun    ,soldier_personality,[(trp_rhun_horse_archer,10,15),(trp_rhun_tribal_infantry,10,15),(trp_infantry_of_the_ox,1,1)]),

####TLD Patrols
("gondor_patrol"  ,"Gondor Patrol"    ,icon_ithilien_ranger|carries_goods(2),0,fac_gondor  ,soldier_personality,[(trp_ranger_of_ithilien,8,20),(trp_veteran_ranger_of_ithilien,8,20),(trp_master_ranger_of_ithilien,4,10),(trp_ithilien_leader,1,1)]),
("rohan_patrol"   ,"Rohan Patrol"     ,icon_knight_rohan   |carries_goods(2),0,fac_rohan   ,soldier_personality,[(trp_skirmisher_of_rohan,3,5),(trp_veteran_skirmisher_of_rohan,3,5),(trp_elite_skirmisher_of_rohan,3,5),(trp_thengel_guard_of_rohan,1,1)]),
("imladris_patrol","Rivendell Patrol" ,icon_rivendell_elf  |carries_goods(2),0,fac_imladris,soldier_personality,[(trp_rivendell_sentinel,8,20),(trp_rivendell_veteran_sentinel,8,20),(trp_rivendell_elite_sentinel,4,10),(trp_rivendell_guardian,1,1)]),
("lorien_patrol"  ,"Lothlorien Patrol",icon_lorien_elf_b   |carries_goods(2),0,fac_lorien  ,soldier_personality,[(trp_lothlorien_archer,4,15),(trp_lothlorien_veteran_archer,4,15),(trp_lothlorien_master_archer,3,5),(trp_galadhrim_royal_archer,1,1)]),
("woodelf_patrol" ,"Mirkwood Patrol"  ,icon_mirkwood_elf   |carries_goods(2),0,fac_woodelf ,soldier_personality,[(trp_greenwood_archer,7,17),(trp_greenwood_veteran_archer,7,17),(trp_greenwood_master_archer,7,17),(trp_thranduils_royal_marksman,1,1)]),
("dale_patrol"    ,"Dale Patrol"      ,icon_gray_knight    |carries_goods(2),0,fac_dale    ,soldier_personality,[(trp_laketown_archer,4,10),(trp_barding_bowmen_of_esgaroth,4,10),(trp_laketown_scout,4,10),(trp_dale_billman,4,10),(trp_dale_marchwarden,4,10),(trp_girions_guard_of_dale,1,1)]),
("dwarf_patrol"   ,"Dwarven Patrol"   ,icon_dwarf          |carries_goods(2),0,fac_dwarf   ,soldier_personality,[(trp_dwarven_lookout,10,25),(trp_dwarven_archer,10,25),(trp_dwarven_warrior,1,1)]),

("rhun_patrol"    ,"Rhun Patrol"      ,icon_gray_knight    |carries_goods(1),0,fac_rhun    ,soldier_personality,[(trp_rhun_vet_infantry,8,20),(trp_rhun_veteran_horse_archer,8,20),(trp_rhun_heavy_noble_cavalry,8,20),(trp_dorwinion_noble_of_rhun,1,1)]),

####TLD Companies
("gondor_company"  ,"Gondor Company"    ,icon_knight_gondo_trot_x3,0,fac_gondor  ,soldier_personality,[(trp_gondor_veteran_swordsmen   ,10,30),(trp_gondor_veteran_spearmen   ,10,30),(trp_veteran_archer_of_gondor ,10,20),(trp_knight_of_gondor,7,10),(trp_veteran_knight_of_gondor,7,10),(trp_captain_of_gondor,1,1)]),
("rohan_company"   ,"Rohan Company"     ,icon_knight_rohan        ,0,fac_rohan   ,soldier_personality,[(trp_elite_rider_of_rohan       ,25,25),(trp_elite_skirmisher_of_rohan ,25,25),(trp_elite_footman_of_rohan   ,25,25),(trp_eorl_guard_of_rohan,12,12),(trp_thengel_guard_of_rohan,12,12),(trp_captain_of_rohan,1,1)]),
("imladris_company","Rivendell Company" ,icon_rivendell_elf       ,0,fac_imladris,soldier_personality,[(trp_rivendell_infantry         ,20,33),(trp_rivendell_veteran_infantry,20,33),(trp_rivendell_elite_infantry ,20,33),(trp_rivendell_royal_infantry,3,6),(trp_elf_captain_of_rivendell,1,1)]),
("lorien_company"  ,"Lothlorien Company",icon_lorien_elf_b        ,0,fac_lorien  ,soldier_personality,[(trp_lothlorien_veteran_infantry,30,30),(trp_lothlorien_elite_infantry ,30,30),(trp_lothlorien_veteran_warden,30,30),(trp_galadhrim_royal_warden,5,5),(trp_galadhrim_royal_swordsman,5,5),(trp_elf_captain_of_lothlorien,1,1)]),
("woodelf_company" ,"Mirkwood Company"  ,icon_mirkwood_elf        ,0,fac_woodelf ,soldier_personality,[(trp_greenwood_veteran_spearman ,21,22),(trp_greenwood_veteran_spearman,21,22),(trp_greenwood_veteran_archer ,21,22),(trp_greenwood_master_archer,21,22),(trp_thranduils_royal_marksman,8,12)]),
("dale_company"    ,"Dale Company"      ,icon_gray_knight         ,0,fac_dale    ,soldier_personality,[(trp_laketown_archer            ,20,20),(trp_barding_bowmen_of_esgaroth,20,20),(trp_dale_veteran_warrior     ,20,20),(trp_dale_bill_master,20,20),(trp_girions_guard_of_dale,20,20),(trp_knight_5_1,1,1)]),
("dwarf_company"   ,"Dwarven Company"   ,icon_dwarf               ,0,fac_dwarf   ,soldier_personality,[(trp_dwarven_hardened_warrior   ,25,25),(trp_dwarven_lookout           ,25,25),(trp_dwarven_warrior          ,20,20),(trp_dwarven_expert_axeman,20,20),(trp_dwarven_archer,10,10),(trp_knight_5_6,1,1)]),

#("blank_patrol","Blank Patrol",icon_gray_knight|carries_goods(1)|pf_show_faction,0,fac_blank,soldier_personality,[(trp_blank,8,20),(trp_blank,8,20),(trp_blank,8,20),(trp_blank,1,1)]),

####TLD Elite Companies
("gondor_elite_company"  ,"Gondor Elite Company"    ,icon_knight_gondo_trot_x3,0,fac_gondor  ,soldier_personality,[(trp_guard_of_the_fountain_court,15,30),(trp_knight_of_the_citadel,15,30),(trp_archer_of_the_tower_guard,15,30),(trp_swordsmen_of_the_tower_guard,15,30),(trp_captain_of_gondor,1,1)]),
("rohan_elite_company"   ,"Rohan Elite Company"     ,icon_knight_rohan_x3     ,0,fac_rohan   ,soldier_personality,[(trp_eorl_guard_of_rohan        ,10,20),(trp_thengel_guard_of_rohan,10,20),(trp_folcwine_guard_of_rohan,10,20),(trp_warden_of_methuseld,10,20),(trp_raider_of_rohan,10,20),(trp_captain_of_rohan,1,1)]),
("imladris_elite_company","Rivendell Elite Company" ,icon_knight_rivendell    ,0,fac_imladris,soldier_personality,[(trp_rivendell_royal_infantry   ,25,50),(trp_knight_of_rivendell,25,50),(trp_elf_captain_of_rivendell,1,1)]),
("lorien_elite_company"  ,"Lothlorien Elite Company",icon_lorien_elf_b_x3     ,0,fac_lorien  ,soldier_personality,[(trp_galadhrim_royal_marksman   ,13,25),(trp_galadhrim_royal_swordsman,13,25),(trp_galadhrim_royal_archer,13,25),(trp_galadhrim_royal_warden,13,25),(trp_noldorin_commander,1,1)]),
("woodelf_elite_company" ,"Mirkwood Elite Company"  ,icon_mirkwood_elf_x3     ,0,fac_woodelf ,soldier_personality,[(trp_greenwood_royal_spearman   ,20,40),(trp_thranduils_royal_marksman,20,40),(trp_elf_captain_of_mirkwood,0,0)]),
("dale_elite_company"    ,"Dale Elite Company"      ,icon_gray_knight         ,0,fac_dale    ,soldier_personality,[(trp_dale_bill_master           ,13,25),(trp_dale_marchwarden,13,25),(trp_girions_guard_of_dale,13,25),(trp_barding_bowmen_of_esgaroth,13,25),(trp_knight_5_1,13,25)]),
("dwarf_elite_company"   ,"Dwarven Elite Company"   ,icon_dwarf               ,0,fac_dwarf   ,soldier_personality,[(trp_dwarven_warrior            ,18,34),(trp_dwarven_expert_axeman,18,34),(trp_dwarven_archer,18,34),(trp_knight_5_6,1,1)]),

####TLD Legions
#("gondor_legion","Gondor Legion",icon_|carries_goods(2),0,fac_,soldier_personality,[(trp_,0,0)]),
#("rohan_legion","Rohan Legion",icon_|carries_goods(2),0,fac_,soldier_personality,[(trp_,0,0)]),
#("rivendell_legion","Rivendell Legion",icon_|carries_goods(2),0,fac_,soldier_personality,[(trp_,0,0)]),
#("lorien_legion","Lothlorien Legion",icon_|carries_goods(2),0,fac_,soldier_personality,[(trp_,0,0)]),
#("mirkwood_legion","Mirkwood Legion",icon_|carries_goods(2),0,fac_,soldier_personality,[(trp_,0,0)]),
#("dale_legion","Dale Legion",icon_|carries_goods(2),0,fac_,soldier_personality,[(trp_,0,0)]),
#("dwarven_legion","Dwarven Legion",icon_|carries_goods(2),0,fac_,soldier_personality,[(trp_,0,0)]),

####TLD Caravans
("gondor_caravan"  ,"Gondor Caravan"    ,icon_supply_gondor|carries_goods(2),0,fac_gondor  ,prisoner_train_personality,[(trp_gondor_swordsmen,15,15),(trp_gondor_spearmen,15,15),(trp_archer_of_gondor,15,15),(trp_knight_of_gondor,10,10),(trp_caravan_master,1,1)]),
("rohan_caravan"   ,"Rohan Caravan"     ,icon_supply_rohan |carries_goods(2),0,fac_rohan   ,prisoner_train_personality,[(trp_veteran_rider_of_rohan,15,15),(trp_veteran_skirmisher_of_rohan,15,15),(trp_veteran_footman_of_rohan,15,15),(trp_caravan_master,1,1)]),
("imladris_caravan","Rivendell Caravan" ,icon_mule         |carries_goods(2),0,fac_imladris,prisoner_train_personality,[(trp_rivendell_veteran_infantry,20,20),(trp_rivendell_veteran_sentinel,20,20),(trp_knight_of_rivendell,10,10),(trp_caravan_master,1,1)]),
("lorien_caravan"  ,"Lothlorien Caravan",icon_mule         |carries_goods(2),0,fac_lorien  ,prisoner_train_personality,[(trp_lothlorien_warden,20,20),(trp_lothlorien_veteran_infantry,20,20),(trp_galadhrim_royal_swordsman,10,10),(trp_caravan_master,1,1)]),
("woodelf_caravan" ,"Mirkwood Caravan"  ,icon_mule         |carries_goods(2),0,fac_woodelf ,prisoner_train_personality,[(trp_greenwood_veteran_archer,20,20),(trp_greenwood_veteran_spearman,20,20),(trp_greenwood_master_archer,10,10)],(trp_caravan_master,1,1)),
("dale_caravan"    ,"Dale Caravan"      ,icon_mule         |carries_goods(2),0,fac_dale    ,prisoner_train_personality,[(trp_dale_veteran_warrior,20,20),(trp_merchant_squire_or_dale,10,10),(trp_laketown_archer,20,20),(trp_caravan_master,1,1)]),
("dwarf_caravan"   ,"Dwarven Caravan"   ,icon_mule         |carries_goods(2),0,fac_dwarf   ,prisoner_train_personality,[(trp_dwarven_lookout,20,20),(trp_dwarven_hardened_warrior,20,20),(trp_dwarven_expert_axeman,10,10),(trp_caravan_master,1,1)]),

("mordor_caravan"  ,"Mordor Supply Train"  ,icon_supply_mordor  |carries_goods(2),0,fac_mordor  ,prisoner_train_personality, [(trp_large_orc_archer_of_mordor, 10, 15), (trp_large_orc_of_mordor, 10, 15), (trp_large_uruk_of_mordor, 10, 15), (trp_olog_hai, 0, 2)]),
("isengard_caravan","Isengard Supply Train",icon_supply_isengard|carries_goods(2),0,fac_isengard,prisoner_train_personality, [(trp_uruk_hai_scout, 10, 15), (trp_large_uruk_hai_of_isengard, 10, 15), (trp_large_orc_despoiler, 10, 15), (trp_warg_rider_of_isengard, 3, 8)]),


####TLD Prisoner Trains
("gondor_p_train"  ,"Gondor Prisoner Train"    ,icon_supply_gondor,0,fac_gondor  ,prisoner_train_personality,[(trp_gondor_swordsmen          ,10,15),(trp_gondor_spearmen,10,15),(trp_archer_of_gondor,10,15),(trp_knight_of_gondor,5,10)]),
("rohan_p_train"   ,"Rohan Prisoner Train"     ,icon_supply_rohan ,0,fac_rohan   ,prisoner_train_personality,[(trp_veteran_rider_of_rohan    ,10,15),(trp_veteran_skirmisher_of_rohan,10,15),(trp_veteran_footman_of_rohan,10,15)]),
("imladris_p_train","Rivendell Prisoner Train" ,icon_mule         ,0,fac_imladris,prisoner_train_personality,[(trp_rivendell_veteran_infantry,15,20),(trp_rivendell_veteran_sentinel,15,20),(trp_knight_of_rivendell,5,10)]),
("lorien_p_train"  ,"Lothlorien Prisoner Train",icon_mule         ,0,fac_lorien  ,prisoner_train_personality,[(trp_lothlorien_warden         ,15,20),(trp_lothlorien_veteran_infantry,15,20),(trp_galadhrim_royal_swordsman,5,10)]),
("woodelf_p_train" ,"Mirkwood Prisoner Train"  ,icon_mule         ,0,fac_woodelf ,prisoner_train_personality,[(trp_greenwood_veteran_archer  ,15,20),(trp_greenwood_veteran_spearman,15,20),(trp_greenwood_master_archer,5,10)]),
("dale_p_train"    ,"Dale Prisoner Train"      ,icon_mule         ,0,fac_dale    ,prisoner_train_personality,[(trp_dale_veteran_warrior      ,15,20),(trp_merchant_squire_or_dale,5,10),(trp_laketown_archer,15,20)]),
("dwarf_p_train"   ,"Dwarven Prisoner Train"   ,icon_mule         ,0,fac_dwarf   ,prisoner_train_personality,[(trp_dwarven_lookout           ,15,20),(trp_dwarven_hardened_warrior,15,20),(trp_dwarven_expert_axeman,5,10)]),

("mordor_p_train"  ,"Mordor Prisoner Train"    ,icon_slaver_mordor  |carries_goods(2),0,fac_mordor  , prisoner_train_personality, [(trp_large_orc_archer_of_mordor, 10, 15), (trp_large_orc_of_mordor, 10, 15), (trp_large_uruk_of_mordor, 10, 15), (trp_olog_hai, 0, 2)]),
("isengard_p_train","Isengard Prisoner Train"  ,icon_slaver_isengard|carries_goods(2),0,fac_isengard, prisoner_train_personality, [(trp_uruk_hai_scout, 10, 15), (trp_large_uruk_hai_of_isengard, 10, 15), (trp_large_orc_despoiler, 10, 15), (trp_warg_rider_of_isengard, 3, 8)]),


#Patrols
("swadian_patrol","Swadian Patrol",icon_gray_knight|carries_goods(3)|pf_show_faction,0,fac_gondor,soldier_personality,[(trp_bowmen_of_gondor,8,13),(trp_footmen_of_gondor,8,20),(trp_swordsmen_of_the_tower_guard,8,16),(trp_master_ranger_of_ithilien,5,20),(trp_knight_of_gondor,4,15),(trp_knight_of_the_citadel,4,15)]),
("vaegir_patrol","Vaegir Patrol",icon_vaegir_knight|carries_goods(2)|pf_show_faction,0,fac_rohan,soldier_personality,[(trp_bowmen_of_gondor,8,13),(trp_footmen_of_gondor,8,20),(trp_swordsmen_of_the_tower_guard,8,16),(trp_master_ranger_of_ithilien,5,20),(trp_knight_of_gondor,4,15),(trp_knight_of_the_citadel,4,15)]),
#War Parties
("swadian_war_party","Swadian War Party",icon_gray_knight|carries_goods(5)|pf_show_faction,0,fac_gondor,soldier_personality,[(trp_bowmen_of_gondor,8,13),(trp_footmen_of_gondor,8,20),(trp_swordsmen_of_the_tower_guard,8,16),(trp_master_ranger_of_ithilien,5,20),(trp_knight_of_gondor,4,15),(trp_knight_of_the_citadel,4,15)]),
("vaegir_war_party","Vaegir War Party",icon_vaegir_knight|carries_goods(5)|pf_show_faction,0,fac_rohan,soldier_personality,[(trp_bowmen_of_gondor,8,13),(trp_footmen_of_gondor,8,20),(trp_swordsmen_of_the_tower_guard,8,16),(trp_master_ranger_of_ithilien,5,20),(trp_knight_of_gondor,4,15),(trp_knight_of_the_citadel,4,15)]),

#Raiders
# ("swadian_raiders","Swadian Raiders",icon_gray_knight|carries_goods(16)|pf_quest_party,0,fac_gondor,soldier_personality,[(trp_swordsmen_of_the_tower_guard,8,16),(trp_master_ranger_of_ithilien,5,20),(trp_peasant_woman,6,30,pmf_is_prisoner)]),
# ("vaegir_raiders","Vaegir Raiders",icon_vaegir_knight|carries_goods(16)|pf_quest_party,0,fac_rohan,soldier_personality,[(trp_swordsmen_of_the_tower_guard,8,16),(trp_master_ranger_of_ithilien,5,20),(trp_peasant_woman,6,30,pmf_is_prisoner)]),
##########################
("center_reinforcements","Reinforcements",icon_axeman|carries_goods(16),0,fac_commoners,soldier_personality,[(trp_beorning_vale_man,5,30),(trp_watchman,4,20)]),
("kingdom_hero_party","War Party",icon_flagbearer_a|pf_show_faction|pf_default_behavior,0,fac_commoners,soldier_personality,[]),
  
("gondor_war_party"   ,"Gondor_War_Party"   ,icon_knight_gondo_trot_x3|carries_goods(3),0,fac_gondor,soldier_personality,[(trp_guard_of_the_fountain_court,8,36),(trp_master_ranger_of_ithilien,15,20),(trp_knight_of_gondor,15,35),(trp_veteran_archer_of_gondor,8,13),(trp_gondor_veteran_swordsmen,8,20),(trp_veteran_knight_of_gondor,5,35)]),
("gondor_allies_war_party","Gondor_Allies_War_Party",icon_mirkwood_elf_x3|carries_goods(3),0,fac_gondor,soldier_personality,[(trp_swan_knight_of_dol_amroth,8,13),(trp_veteran_knight_of_dol_amroth,8,20),(trp_knight_of_dol_amroth,8,16),(trp_champion_of_pinnath_gelin,5,20),(trp_squire_of_dol_amroth,4,15),(trp_master_blackroot_vale_archer,4,15)]),
("rohan_war_party"    ,"Rohan_War_Party"    ,icon_knight_rohan_x3 |carries_goods(3),0,fac_rohan   ,soldier_personality,[(trp_elite_lancer_of_rohan  ,8,13),(trp_brego_guard_of_rohan,8,20),(trp_elite_skirmisher_of_rohan,4,16),(trp_lancer_of_rohan,10,20),(trp_rider_of_rohan,14,35),(trp_eorl_guard_of_rohan,14,45)]),
("lorien_war_party"   ,"Lothlorien_War_Party",icon_lorien_elf_b_x3|carries_goods(3),0,fac_lorien  ,soldier_personality,[(trp_lothlorien_archer,8,20),(trp_galadhrim_royal_marksman,8,16),(trp_lothlorien_veteran_infantry,5,20),(trp_galadhrim_royal_swordsman,4,15),(trp_lothlorien_warden,4,15),(trp_lothlorien_standard_bearer,2,4)]),
("woodelf_war_party"  ,"Woodelf_War_Party"  ,icon_mirkwood_elf_x3 |carries_goods(3),0,fac_woodelf ,soldier_personality,[(trp_greenwood_royal_spearman,8,20),(trp_greenwood_master_archer,8,16),(trp_greenwood_spearman,5,20),(trp_greenwood_veteran_spearman,4,15),(trp_greenwood_royal_spearman,4,15),(trp_greenwood_standard_bearer,2,4)]),
("imladris_war_party" ,"Rivendell_War_Party",icon_rivendell_elf_x3|carries_goods(3),0,fac_imladris,soldier_personality,[(trp_rivendell_sentinel,8,20),(trp_rivendell_veteran_sentinel,8,16),(trp_knight_of_rivendell,5,20),(trp_rivendell_elite_sentinel,4,15),(trp_rivendell_veteran_scout,4,15),(trp_rivendell_standard_bearer,2,4)]),
("dunedain_war_party" ,"Dunedain_War_Party" ,icon_dunlander_x3    |carries_goods(3),0,fac_imladris,soldier_personality,[(trp_dunedain_veteran_ranger,8,13),(trp_arnor_horsemen,8,20),(trp_high_swordsman_of_arnor,8,16),(trp_knight_of_arnor,5,20),(trp_dunedain_ranger,4,15),(trp_dunedain_master_ranger,4,15)]),
  
("mordor_war_party"   ,"Mordor_War_Party"  ,icon_uruk_x6          |carries_goods(3),0,fac_mordor  ,soldier_personality,[(trp_large_orc_of_mordor    ,20,50),(trp_orc_archer_of_mordor,13,36),(trp_black_numenorean_warrior,15,30),(trp_black_numenorean_veteran_warrior,5,40),(trp_olog_hai,1,2),(trp_uruk_mordor_standard_bearer,2,3)]),#(trp_uruk_snaga_of_mordor,5,20), ,(trp_black_numenorean_captain,1,1)
("isengard_war_party" ,"Isengard_War_Party",icon_wargrider_walk_x4|carries_goods(3),0,fac_isengard,soldier_personality,[(trp_fighting_uruk_hai_champion,10,30),(trp_large_uruk_hai_of_isengard,13,36),(trp_wolf_rider_of_isengard,5,30),(trp_fighting_uruk_hai_berserker,10,40),(trp_troll_of_moria,1,2),(trp_urukhai_standard_bearer,1,2)]),#(trp_fighting_uruk_hai_pikeman,5,20),
("harad_war_party"    ,"Harad_War_Party"   ,icon_harad_horseman_x3|carries_goods(3),0,fac_harad   ,soldier_personality,[(trp_harad_desert_warrior   ,20,50),(trp_harad_veteran_archer,15,30),(trp_harad_black_serpent_infantry,13,36),(trp_harad_cavalry,5,30),(trp_black_serpent_cavalry,5,40),(trp_black_serpent_horse_archer,5,20)]),
("dunland_war_party"  ,"Dunlending_Warband",icon_dunlander_x3     |carries_goods(3),0,fac_dunland ,soldier_personality,[(trp_dunnish_wildman        ,20,50),(trp_dunnish_veteran_pikeman,15,30),(trp_dunnish_warrior,13,36),(trp_dunnish_raven_rider,5,30)]),
("khand_war_party"    ,"Khand_War_Party"   ,icon_cataphract_x3    |carries_goods(3),0,fac_khand   ,soldier_personality,[(trp_easterling_warrior     ,20,50),(trp_easterling_axe_master,15,30),(trp_easterling_rider,13,36),(trp_khand_glaive_master,5,30),(trp_easterling_horsemaster,5,40),(trp_easterling_lance_kataphract,5,20)]),
("corsair_war_party"  ,"Corsair_War_Party" ,icon_umbar_corsair_x3 |carries_goods(3),0,fac_umbar   ,soldier_personality,[(trp_pike_master_of_umbar   ,20,50),(trp_corsair_veteran_raider,15,30),(trp_veteran_pikeman_of_umbar,13,36),(trp_master_marksman_of_umbar,5,30),(trp_corsair_veteran_marauder,5,40),(trp_master_assassin_of_umbar,5,20)]),
("moria_war_party"    ,"Moria_War_Party"   ,icon_orc_tribal_x4    |carries_goods(3),0,fac_moria   ,soldier_personality,[(trp_snaga_of_moria         ,20,50),(trp_goblin_of_moria,15,30),(trp_large_goblin_of_moria,13,36),(trp_fell_goblin_of_moria,15,30),(trp_large_goblin_archer_of_moria,5,40),(trp_troll_of_moria,1,2)]), #(trp_tribal_orc,5,20),
#Northern war
("dale_war_party"  ,"Dale_War_Party"   ,icon_mirkwood_elf_x3       |carries_goods(3),0,fac_dale   ,soldier_personality,[(trp_dale_man_at_arms        ,8,13),(trp_dale_veteran_warrior,8,20),(trp_barding_bowmen_of_esgaroth,8,16),(trp_laketown_archer,5,20),(trp_beorning_sentinel,4,15),(trp_merchant_squire_or_dale,4,15)]),
("dwarf_war_party" ,"Dwarven_War_Party",icon_dwarf_x3              |carries_goods(3),0,fac_dwarf  ,soldier_personality,[(trp_dwarven_apprentice      ,8,13),(trp_grors_guard,8,20),(trp_dwarven_warrior,8,16),(trp_dwarven_expert_axeman,5,20),(trp_dwarven_lookout,4,15),(trp_dwarven_archer,4,15)]),
("rhun_war_party"  ,"Rhun_War_Party"   ,icon_easterling_horseman_x3|carries_goods(3),0,fac_rhun   ,soldier_personality,[(trp_rhun_heavy_noble_cavalry,20,50),(trp_dorwinion_noble_of_rhun,15,30),(trp_rhun_tribal_warrior,13,36),(trp_rhun_veteran_swift_horseman,5,30),(trp_rhun_veteran_horse_archer,5,40),(trp_rhun_tribesman,5,20)]),

# Reinforcements
("gondor_reinf_d"    ,"_",0,0,fac_commoners,0,[(trp_knight_of_the_citadel,2,4), (trp_archer_of_the_tower_guard,2,4),(trp_swordsmen_of_the_tower_guard,2,4),(trp_guard_of_the_fountain_court,2,4),]),

("gondor_reinf_a"    ,"_",0,0,fac_commoners,0,[(trp_bowmen_of_gondor,4,6), (trp_gondor_militiamen,3,4), (trp_gondor_commoner,5,8),(trp_gondor_noblemen,1,2)]),
("gondor_reinf_b"    ,"_",0,0,fac_commoners,0,[(trp_archer_of_gondor,4,6), (trp_footmen_of_gondor,3,4), (trp_gondor_spearmen,1,3),(trp_gondor_swordsmen,0,2),(trp_squire_of_gondor,0,2)]),
("gondor_reinf_c"    ,"_",0,0,fac_commoners,0,[(trp_veteran_archer_of_gondor,4,6), (trp_gondor_veteran_spearmen,3,4),(trp_gondor_veteran_swordsmen,0,2),(trp_veteran_squire_of_gondor,0,2) ]),
("pelargir_reinf_a"  ,"_",0,0,fac_commoners,0,[(trp_pelargir_watchman,6,16), (trp_pelargir_infantry,6,16),]),
("pelargir_reinf_b"  ,"_",0,0,fac_commoners,0,[(trp_pelargir_infantry,6,16), (trp_pelargir_vet_infantry,6,16),]),
("pelargir_reinf_c"  ,"_",0,0,fac_commoners,0,[(trp_pelargir_marine,6,9),]),
("dol_amroth_reinf_a","_",0,0,fac_commoners,0,[(trp_dol_amroth_youth,2,6), (trp_squire_of_dol_amroth,4,10),]),
("dol_amroth_reinf_b","_",0,0,fac_commoners,0,[(trp_knight_of_dol_amroth,2,6), (trp_squire_of_dol_amroth,4,7)]),
("dol_amroth_reinf_c","_",0,0,fac_commoners,0,[(trp_veteran_knight_of_dol_amroth,3,6), (trp_swan_knight_of_dol_amroth,1,4)]),
("lamedon_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_clansman_of_lamedon,4,8), (trp_footman_of_lamedon,4,8),]),
("lamedon_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_veteran_of_lamedon,2,6), (trp_warrior_of_lamedon,2,6)]),
("lamedon_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_knight_of_lamedon,2,5), (trp_champion_of_lamedon,2,5)]),
("lossarnach_reinf_a","_",0,0,fac_commoners,0,[(trp_woodsman_of_lossarnach,2,6),(trp_axeman_of_lossarnach,4,5),]),
("lossarnach_reinf_b","_",0,0,fac_commoners,0,[(trp_vet_axeman_of_lossarnach,2,6),(trp_heavy_lossarnach_axeman,3,6)]),
("lossarnach_reinf_c","_",0,0,fac_commoners,0,[(trp_axemaster_of_lossarnach,3,6),(trp_vet_axeman_of_lossarnach,2,4)]),
("pinnath_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_warrior_of_pinnath_gelin,3,8),(trp_pinnath_gelin_bowman,3,8),]),
("pinnath_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_veteran_warrior_of_pinnath_gelin,2,6),(trp_pinnath_gelin_archer,4,7)]),
("pinnath_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_champion_of_pinnath_gelin,3,6),(trp_pinnath_gelin_archer,4,7)]),
("ithilien_reinf_a"  ,"_",0,0,fac_commoners,0,[(trp_ranger_of_ithilien,4,8),           ]),
("ithilien_reinf_b"  ,"_",0,0,fac_commoners,0,[(trp_veteran_ranger_of_ithilien,4,8),   ]),
("ithilien_reinf_c"  ,"_",0,0,fac_commoners,0,[(trp_master_ranger_of_ithilien,2,6),    ]),
("blackroot_reinf_a" ,"_",0,0,fac_commoners,0,[(trp_blackroot_vale_archer,2,6),(trp_footman_of_blackroot_vale,4,10),]),
("blackroot_reinf_b" ,"_",0,0,fac_commoners,0,[(trp_veteran_blackroot_vale_archer,2,6),(trp_spearman_of_blackroot_vale,4,7),]),
("blackroot_reinf_c" ,"_",0,0,fac_commoners,0,[(trp_master_blackroot_vale_archer,3,6),(trp_spearman_of_blackroot_vale,1,6)]),
#rohan	
("rohan_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_esquire_of_rohan,2,6),(trp_guardsman_of_rohan,4,7)]),
("rohan_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_guardsman_of_rohan,2,6),(trp_elite_footman_of_rohan,3,5),(trp_esquire_of_rohan,1,3)]),
("rohan_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_brego_guard_of_rohan,3,6)]),
#Isengard
("isengard_reinf_a","_",0,0,fac_commoners,0,[(trp_uruk_hai_scout,2,6),(trp_orc_snaga_of_isengard,4,7)]),
("isengard_reinf_b","_",0,0,fac_commoners,0,[(trp_fighting_uruk_hai_warrior,2,6),(trp_uruk_hai_scout,4,7)]),
("isengard_reinf_c","_",0,0,fac_commoners,0,[(trp_fighting_uruk_hai_champion,3,6)]),
#Mordor
("mordor_reinf_a"  ,"_",0,0,fac_commoners,0,[(trp_large_orc_of_mordor,4,8),(trp_orc_snaga_of_mordor,2,4)]),
("mordor_reinf_b"  ,"_",0,0,fac_commoners,0,[(trp_orc_archer_of_mordor,1,3),(trp_uruk_of_mordor,3,5),(trp_large_orc_of_mordor,2,5)]),
("mordor_reinf_c"  ,"_",0,0,fac_commoners,0,[(trp_large_orc_archer_of_mordor,3,6)]),
#Harad
("harad_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_harad_desert_warrior,2,5),(trp_far_harad_tribesman,2,4),(trp_harad_desert_skirmisher,2,4)]),
("harad_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_harad_black_serpent_infantry,2,6),(trp_black_serpent_cavalry,4,7)]),
("harad_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_harad_veteran_archer,3,6)]),
#Rhun
("rhun_reinf_a"    ,"_",0,0,fac_commoners,0,[(trp_rhun_tribesman,2,6),(trp_rhun_light_horseman,4,7)]),
("rhun_reinf_b"    ,"_",0,0,fac_commoners,0,[(trp_rhun_horse_archer,2,6),(trp_rhun_veteran_horse_archer,4,7),(trp_rhun_swift_horseman,4,7)]),
("rhun_reinf_c"    ,"_",0,0,fac_commoners,0,[(trp_rhun_light_cavalry,3,6),(trp_rhun_noble_cavalry,3,6),(trp_rhun_heavy_noble_cavalry,3,6)]),
#Khand
("khand_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_easterling_youth,2,6),(trp_easterling_warrior,4,7)]),
("khand_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_easterling_axeman,2,6),(trp_easterling_rider,3,5),(trp_variag_veteran_glaive_whirler,1,3)]),
("khand_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_easterling_elite_skirmisher,3,6)]),
#Umbar
("umbar_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_corsair_youth,2,6),(trp_corsair_warrior,4,7)]),
("umbar_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_corsair_veteran_marauder,2,6),(trp_marksman_of_umbar,4,7),(trp_black_numenorean_warrior,3,6)]),
("umbar_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_pike_master_of_umbar,3,6),(trp_black_numenorean_champion,1,5)]),
#Lothlorien
("lorien_reinf_a"  ,"_",0,0,fac_commoners,0,[(trp_lothlorien_scout,2,4),(trp_lothlorien_veteran_scout,2,4)]),
("lorien_reinf_b"  ,"_",0,0,fac_commoners,0,[(trp_lothlorien_master_archer,1,3),(trp_lothlorien_infantry,1,3),(trp_lothlorien_elite_infantry,2,5)]),
("lorien_reinf_c"  ,"_",0,0,fac_commoners,0,[(trp_lothlorien_veteran_warden,3,6)]),
#Imladris
("imladris_reinf_a","_",0,0,fac_commoners,0,[(trp_rivendell_scout,3,7),(trp_dunedain_scout,3,6)]),
("imladris_reinf_b","_",0,0,fac_commoners,0,[(trp_arnor_man_at_arms,2,6),(trp_rivendell_veteran_sentinel,4,7)]),
("imladris_reinf_c","_",0,0,fac_commoners,0,[(trp_knight_of_rivendell,1,6),(trp_dunedain_veteran_ranger,3,6)]),
#Woodelves  
("woodelf_reinf_a" ,"_",0,0,fac_commoners,0,[(trp_greenwood_scout,3,7),(trp_greenwood_veteran_scout,3,6)]),
("woodelf_reinf_b" ,"_",0,0,fac_commoners,0,[(trp_greenwood_master_archer,2,6),(trp_greenwood_spearman,4,7)]),
("woodelf_reinf_c" ,"_",0,0,fac_commoners,0,[(trp_greenwood_royal_spearman,3,6)]),
#Moria
("moria_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_snaga_of_moria,4,10),(trp_goblin_of_moria,6,10)]),
("moria_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_large_goblin_of_moria,2,10),(trp_goblin_of_moria,3,13),(trp_archer_snaga_of_moria,3,10)]),
("moria_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_fell_goblin_of_moria,5,16)]),
#Dol Guldur
("guldur_reinf_a"  ,"_",0,0,fac_commoners,0,[(trp_large_orc_of_mordor,4,8),(trp_orc_snaga_of_mordor,2,4)]),
("guldur_reinf_b"  ,"_",0,0,fac_commoners,0,[(trp_orc_archer_of_mordor,1,3),(trp_uruk_of_mordor,3,5),(trp_large_orc_of_mordor,2,5)]),
("guldur_reinf_c"  ,"_",0,0,fac_commoners,0,[(trp_warg_rider_of_gorgoroth,3,6)]),
#Beornings
("beorn_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_beorning_vale_man,4,8),(trp_beorning_vale_man,2,4)]),
("beorn_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_beorning_vale_man,1,3),(trp_beorning_warrior,3,5),(trp_beorning_vale_man,2,5)]),
("beorn_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_beorning_vale_man,3,6)]),
#Mt. Gundabad
("gundabad_reinf_a","_",0,0,fac_commoners,0,[(trp_goblin_gundabad,4,10),(trp_orc_fighter_gundabad,6,10)]),
("gundabad_reinf_b","_",0,0,fac_commoners,0,[(trp_goblin_bowmen_gundabad,2,10),(trp_keen_eyed_goblin_archer_gundabad,3,13),(trp_goblin_rider_gundabad,3,10)]),
("gundabad_reinf_c","_",0,0,fac_commoners,0,[(trp_fell_orc_warrior_gundabad,5,16)]),
#Dale
("dale_reinf_a"    ,"_",0,0,fac_commoners,0,[(trp_dale_militia,4,8),(trp_dale_man_at_arms,2,4)]),
("dale_reinf_b"    ,"_",0,0,fac_commoners,0,[(trp_dale_militia,1,3),(trp_dale_warrior,3,5),(trp_dale_veteran_warrior,2,5)]),
("dale_reinf_c"    ,"_",0,0,fac_commoners,0,[(trp_dale_marchwarden,3,6)]),
#Erebor
("dwarf_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_dwarven_apprentice,2,6),(trp_dwarven_lookout,4,7)]),
("dwarf_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_dwarven_hardened_warrior,2,6),(trp_dwarven_warrior,3,5),(trp_dwarven_expert_axeman,1,3)]),
("dwarf_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_dwarven_archer,3,6),(trp_iron_hills_infantry,3,6)]),
#Dunlenders
("dunland_reinf_a" ,"_",0,0,fac_commoners,0,[(trp_dunnish_wildman,2,6),(trp_dunnish_pikeman,4,7)]),
("dunland_reinf_b" ,"_",0,0,fac_commoners,0,[(trp_dunnish_veteran_pikeman,2,6),(trp_dunnish_wolf_warrior,4,7)]),
("dunland_reinf_c" ,"_",0,0,fac_commoners,0,[(trp_dunnish_wolf_warrior,3,6)]),

("caravan_survivors","Caravan Survivors",icon_gray_knight|carries_goods(2),0,fac_neutral,merchant_personality,[(trp_sea_raider,5,5)]),
]
