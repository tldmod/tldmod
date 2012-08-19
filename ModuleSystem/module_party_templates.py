from header_common import *
from header_parties import *
from ID_troops import *
from ID_factions import *
from ID_map_icons import *
from ID_menus import *

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
("none","none",icon_generic_knight,0,fac_commoners,merchant_personality,[]),
("rescued_prisoners","Rescued Prisoners",icon_generic_knight,0,fac_commoners,merchant_personality,[]),
("enemy","Enemy",icon_generic_knight,0,fac_commoners,merchant_personality,[]),
("hero_party","Hero Party",icon_generic_knight,0,fac_commoners,merchant_personality,[]),
####################################################################################################################
# Party templates before this point are hard-wired into the game and should not be changed. 
####################################################################################################################
#  ("village_defenders","Village Defenders",icon_peasant,0,fac_commoners,merchant_personality,[(trp_farmer,10,20),(trp_peasant_woman,0,4)]),

("cattle_herd","Cattle Herd",icon_generic_knight|carries_goods(10),0,fac_neutral,merchant_personality,[(trp_cattle,80,120)]), #icon_cattle
("ruins","Ruins",icon_ancient_ruins,0,fac_commoners,merchant_personality,[(trp_farmer,1,1)]),
("legendary_place","Legendary Place",icon_camp,0,fac_commoners,merchant_personality,[(trp_farmer,1,1)]),
("mound","Hero_Mound",icon_burial_mound|pf_hide_defenders|pf_is_static|pf_always_visible, 0,fac_commoners,merchant_personality,[(trp_farmer,1,1)]),
("pyre","Hero_Pyre",icon_burial_mound|pf_hide_defenders|pf_is_static|pf_always_visible, 0,fac_commoners,merchant_personality,[(trp_farmer,1,1)]),

# ("manhunters","Manhunters",icon_generic_knight,0,fac_manhunters,soldier_personality,[(trp_manhunter,9,40)]),
##  ("peasant","Peasant",icon_peasant,0,fac_commoners,merchant_personality,[(trp_farmer,1,6),(trp_peasant_woman,0,7)]),

("wild_troll"      ,"Wild Troll"     ,icon_wild_troll|pf_quest_party,0,fac_commoners,bandit_personality,[(trp_troll_of_moria,1,2),]),
("raging_trolls"   ,"Raging Trolls"  ,icon_wild_troll|pf_quest_party,0,fac_outlaws,bandit_personality,[(trp_troll_of_moria,1,3),]),
("looters"         ,"Tribal Orcs"    ,icon_orc_tribal|carries_goods(4),0,fac_outlaws,bandit_personality,[(trp_tribal_orc_warrior,0,1),(trp_tribal_orc,2,25)]),
("forest_bandits"  ,"Orc Stragglers" ,icon_orc_tribal|carries_goods(4),0,fac_outlaws,bandit_personality,[(trp_tribal_orc_chief,0,1),(trp_tribal_orc_warrior,0,8),(trp_tribal_orc,3,40),(trp_mountain_goblin,1,30)]),
("mountain_bandits","Wild Goblins"   ,icon_orc_tribal|carries_goods(4),0,fac_outlaws,bandit_personality,[(trp_mountain_goblin,2,40)]),
("steppe_bandits"  ,"Dunland Outcasts",icon_dunlander|carries_goods(4),0,fac_outlaws,bandit_personality,[(trp_dunnish_warrior,3,10), (trp_dunnish_wildman,5,35)]),
("sea_raiders"     ,"Corsair Renegades",icon_umbar_corsair|carries_goods(4),0,fac_outlaws,bandit_personality,[(trp_corsair_warrior,3,30),(trp_marksman_of_umbar,3,20)]),

("deserters","Deserters",icon_axeman|carries_goods(3),0,fac_deserters,bandit_personality,[]),

("merchant_caravan","Merchant Caravan",icon_mule|carries_goods(20)|pf_auto_remove_in_town|pf_quest_party,0,fac_commoners,escorted_merchant_personality,[(trp_caravan_master,1,1),(trp_caravan_guard,5,25)]),
("troublesome_bandits","Troublesome Goblins",icon_orc_tribal|carries_goods(9)|pf_quest_party,0,fac_outlaws,bandit_personality,[(trp_mountain_goblin,14,55)]),
("fangorn_orcs","Tree-chopping Orcs",icon_orc_x4|carries_goods(9)|pf_quest_party,0,fac_neutral,bandit_personality,[(trp_fighting_uruk_hai_champion,1,1),(trp_large_uruk_hai_of_isengard,3,8),(trp_large_uruk_hai_tracker,8,13),(trp_uruk_snaga_of_isengard,12,24)]),
# ("bandits_awaiting_ransom","Bandits Awaiting Ransom",icon_axeman|carries_goods(9)|pf_auto_remove_in_town|pf_quest_party,0,fac_neutral,bandit_personality,[(trp_brigand,24,58),(trp_kidnapped_girl,1,1,pmf_is_prisoner)]),
# ("kidnapped_girl","Kidnapped Girl",icon_woman|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_kidnapped_girl,1,1)]),

("village_farmers","Village Farmers",icon_peasant,0,fac_innocents,merchant_personality,[(trp_farmer,5,10),(trp_peasant_woman,3,8)]),

("spy_partners", "Suspicious Travellers", icon_generic_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy_partner,1,1),(trp_squire_of_dol_amroth,5,11)]),
("spy_partners_evil", "Suspicious Travellers", icon_generic_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy_partner_evil,1,1),(trp_dunnish_raven_rider,5,11)]),
("runaway_serfs","Runaway Slaves",icon_peasant|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_farmer,6,7), (trp_peasant_woman,3,3)]),
("spy", "Lone Rider", icon_generic_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy,1,1)]),
("spy_evil", "Lone Rider", icon_generic_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy_evil,1,1)]),
("sacrificed_messenger", "Sacrificed Messenger", icon_generic_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[]),
("gandalf", "Lone Rider",icon_gandalf|pf_default_behavior|pf_quest_party|pf_hide_defenders,0,fac_neutral,merchant_personality,[(trp_gandalf,1,1)]),
("nazgul" , "Lone Rider", icon_nazgul|pf_default_behavior|pf_quest_party|pf_hide_defenders,0,fac_neutral,merchant_personality,[(trp_nazgul,1,1)]),

#TLD Scouts
#MV: in general, average strength should be 30-60 (except Beornings who have scouts only)
("gondor_scouts"      ,"Gondorian Scouts",icon_footman_gondor|carries_goods(1)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_squire_of_gondor,1,1),(trp_bowmen_of_gondor,3,7),(trp_gondor_militiamen,3,7)]), #34-74
("blackroot_auxila" ,"Blackroot Auxilia",icon_ithilien_ranger|carries_goods(1)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_master_blackroot_vale_archer,1,1),(trp_veteran_blackroot_vale_archer,0,3),(trp_blackroot_vale_archer,4,7)]), #32-71
("lamedon_auxila"  ,"Lamedon Auxilia"   ,icon_footman_lamedon|carries_goods(1)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_warrior_of_lamedon,1,1),(trp_veteran_of_lamedon,1,5),(trp_footman_of_lamedon,4,8)]), #31-71
("lossarnach_auxila","Lossarnach Auxilia",icon_lossarnach_axeman_icon|carries_goods(1)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_heavy_lossarnach_axeman,1,1),(trp_vet_axeman_of_lossarnach,0,3),(trp_axeman_of_lossarnach,2,6),(trp_woodsman_of_lossarnach,4,10)]), #25-71
("pinnath_gelin_auxila","Pinnath Gelin Auxilia",icon_footman_pinnath|carries_goods(1)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_pinnath_gelin_bowman,1,3),(trp_pinnath_gelin_spearman,1,2),(trp_pinnath_gelin_plainsman,3,6)]), #30-69
("ranger_scouts"       ,"Ranger Scouts" ,icon_ithilien_ranger|carries_goods(0)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_veteran_ranger_of_ithilien,1,3),(trp_ranger_of_ithilien,3,6)]), #43-102 more punch for rangers, elites operating in enemy territory

("rohan_scouts"    ,"Rohirrim Scouts"      ,icon_knight_rohan |carries_goods(1)|pf_show_faction,0,fac_rohan   ,scout_personality,[(trp_elite_skirmisher_of_rohan,1,1),(trp_veteran_skirmisher_of_rohan,1,4),(trp_skirmisher_of_rohan,3,5)]), #43-82 rohan good at scouting
("lorien_scouts"   ,"Lothlorien Scouts"    ,icon_lorien_elf_a |carries_goods(1)|pf_show_faction,0,fac_lorien  ,scout_personality,[(trp_lothlorien_veteran_warden,1,2),(trp_lothlorien_veteran_scout,3,6),(trp_lothlorien_scout,3,6)]), #31-62
("woodelf_scouts"  ,"Mirkwood Elven Scouts",icon_mirkwood_elf |carries_goods(1)|pf_show_faction,0,fac_woodelf ,scout_personality,[(trp_greenwood_master_archer,1,1),(trp_greenwood_veteran_scout,2,6),(trp_greenwood_scout,4,8)]), #37-65
("imladris_scouts","Rivendell Elven Scouts",icon_rivendell_elf|carries_goods(1)|pf_show_faction,0,fac_imladris,scout_personality,[(trp_rivendell_elite_sentinel,1,1),(trp_rivendell_veteran_scout,2,6),(trp_rivendell_scout,4,8)]), #37-65
("dale_scouts"     ,"Dale Scouts"          ,icon_generic_knight  |carries_goods(2)|pf_show_faction,0,fac_dale    ,scout_personality,[(trp_dale_veteran_warrior,1,1),(trp_dale_man_at_arms,2,6),(trp_dale_militia,4,8)]), #25-49 weak
("esgaroth_scouts" ,"Esgaroth Scouts"    ,icon_ithilien_ranger|carries_goods(2)|pf_show_faction,0,fac_dale    ,scout_personality,[(trp_barding_bowmen_of_esgaroth,1,1),(trp_laketown_archer,1,3),(trp_laketown_scout,4,6)]), #41-67 stronger than dale
("dwarf_scouts"    ,"Dwarven Lookouts"     ,icon_dwarf        |carries_goods(2)|pf_show_faction,0,fac_dwarf   ,scout_personality,[(trp_dwarven_archer,1,1),(trp_dwarven_hardened_warrior,1,3),(trp_dwarven_lookout,4,6)]), #41-63
("beorn_scouts"    ,"Beorning Scouts"      ,icon_axeman       |carries_goods(1)|pf_show_faction,0,fac_beorn   ,scout_personality,[(trp_beorning_carrock_berserker,1,1),(trp_beorning_sentinel,3,5),(trp_beorning_warrior,3,8)]), #55-93 stronger, no raiders/patrols
("woodmen_scouts"  ,"Woodmen Scouts"       ,icon_axeman       |carries_goods(1)|pf_show_faction,0,fac_beorn   ,scout_personality,[(trp_fell_huntsmen_of_mirkwood,1,1),(trp_woodmen_scout,2,3),(trp_woodmen_skilled_forester,3,6)]), #46-70

("mordor_scouts"    ,"Mordor Scouts"       ,icon_orc             |carries_goods(1)|pf_show_faction,0,fac_mordor  ,scout_personality,[(trp_fell_orc_tracker_of_mordor,1,1),(trp_large_orc_of_mordor,1,3),(trp_orc_tracker_of_mordor,2,5),(trp_orc_of_mordor,2,6)]), #29-66
("morgul_scouts"    ,"Morgul Scouts"       ,icon_orc             |carries_goods(1)|pf_show_faction,0,fac_mordor  ,scout_personality,[(trp_fell_orc_tracker_of_mordor,1,1),(trp_fell_morgul_orc,1,2),(trp_orc_tracker_of_mordor,2,5),(trp_morgul_orc,3,5)]), #29-66
("isengard_scouts"  ,"Isengard Scouts"     ,icon_orc_isengard    |carries_goods(1)|pf_show_faction,0,fac_isengard,scout_personality,[(trp_fighting_uruk_hai_tracker,1,1),(trp_large_uruk_hai_tracker,2,6),(trp_uruk_hai_tracker,3,7)]), #33-73
("isengard_scouts_warg","Isengard Warg Riders",icon_wargrider_run|carries_goods(1)|pf_show_faction,0,fac_isengard,scout_personality,[(trp_white_hand_rider,1,1),(trp_warg_rider_of_isengard,3,6),(trp_wolf_rider_of_isengard,3,6)]), #32-56 fast but weaker
("harad_scouts"     ,"Haradrim Scouts"     ,icon_harad_horseman  |carries_goods(1)|pf_show_faction,0,fac_harad   ,scout_personality,[(trp_black_snake_horse_archer,1,1),(trp_harad_horse_archer,1,4),(trp_harondor_scout,4,8)]), #31-65
("dunland_scouts"   ,"Dunlending Scouts"   ,icon_dunlander       |carries_goods(1)|pf_show_faction,0,fac_dunland ,scout_personality,[(trp_dunnish_raven_rider,5,10)]), #20-40 fast weaklings
("umbar_scouts"     ,"Corsair Scouts"      ,icon_umbar_corsair   |carries_goods(1)|pf_show_faction,0,fac_umbar   ,scout_personality,[(trp_corsair_veteran_raider,1,1),(trp_marksman_of_umbar,2,4),(trp_militia_of_umbar,3,7)]), #33-61
("khand_scouts"     ,"Easterling Scouts"   ,icon_cataphract      |carries_goods(1)|pf_show_faction,0,fac_umbar   ,scout_personality,[(trp_easterling_veteran_skirmisher,1,1),(trp_easterling_horseman,2,4),(trp_easterling_rider,3,6)]), #33-57 fast and capable
("moria_scouts"     ,"Moria Scouts"        ,icon_orc             |carries_goods(1)|pf_show_faction,0,fac_moria   ,scout_personality,[(trp_bolg_clan_rider,1,1),(trp_warg_rider_of_moria,2,5),(trp_wolf_rider_of_moria,3,6)]), #27-51 fast
("guldur_scouts"    ,"Dol Guldur Scouts"   ,icon_orc             |carries_goods(1)|pf_show_faction,0,fac_guldur  ,scout_personality,[(trp_orc_of_guldur,3,4),(trp_orc_snaga_of_guldur,8,12)]), #32-61
("gundabad_scouts","Gundabad Scouts",icon_wargrider_run|carries_goods(1)|pf_show_faction,0,fac_gundabad,scout_personality,[(trp_goblin_north_clan_rider,1,2),(trp_warg_rider_gundabad,3,6),(trp_goblin_rider_gundabad,6,10)]), #41-76, was 30-54 fast
("rhun_scouts"      ,"Rhun Scouts"      ,icon_easterling_horseman|carries_goods(1)|pf_show_faction,0,fac_rhun    ,scout_personality,[(trp_rhun_horse_archer,1,3),(trp_rhun_swift_horseman,3,6),(trp_rhun_horse_scout,5,8)]), #44-86 fast and very capable
 
####TLD Raiders
#MV: in general, average strength should be 80-160, good sides weaker, evil stronger (foraging vs. raiding)
("gondor_raiders"  ,"Gondor Foragers"    ,icon_knight_gondor|carries_goods(1)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_veteran_squire_of_gondor,1,1),(trp_footmen_of_gondor,6,12),(trp_bowmen_of_gondor,6,12)]), #78-150
("rohan_raiders"   ,"Rohirrim Foragers"  ,icon_knight_rohan |carries_goods(1)|pf_show_faction,0,fac_rohan   ,soldier_personality,[(trp_elite_rider_of_rohan,1,1),(trp_rider_of_rohan,3,8),(trp_skirmisher_of_rohan,3,8),(trp_squire_of_rohan,5,10)]), #72-152
("imladris_raiders","Rivendell Foragers" ,icon_rivendell_elf|carries_goods(2)|pf_show_faction,0,fac_imladris,soldier_personality,[(trp_rivendell_royal_infantry,1,1),(trp_rivendell_sentinel,6,12),(trp_rivendell_infantry,6,12)]), #91-163
("lorien_raiders"  ,"Lothlorien Foragers",icon_lorien_elf_a |carries_goods(2)|pf_show_faction,0,fac_lorien  ,soldier_personality,[(trp_lothlorien_veteran_warden,1,1),(trp_lothlorien_archer,7,16),(trp_lothlorien_infantry,6,15)]), #71-152
("woodelf_raiders" ,"Mirkwood Foragers"  ,icon_mirkwood_elf |carries_goods(2)|pf_show_faction,0,fac_woodelf ,soldier_personality,[(trp_greenwood_royal_spearman,1,1),(trp_greenwood_veteran_spearman,4,10),(trp_greenwood_archer,5,10)]), #73-150
("dale_raiders"    ,"Dale Foragers"      ,icon_generic_knight  |carries_goods(2)|pf_show_faction,0,fac_dale    ,soldier_personality,[(trp_girions_guard_of_dale,1,1),(trp_merchant_squire_or_dale,4,10),(trp_dale_man_at_arms,4,10),(trp_laketown_scout,4,12)]), #64-144
("dwarf_raiders"   ,"Dwarven Foragers"   ,icon_dwarf        |carries_goods(2)|pf_show_faction,0,fac_dwarf   ,soldier_personality,[(trp_dwarven_expert_axeman,1,1),(trp_dwarven_hardened_warrior,4,12),(trp_dwarven_lookout,5,15)]), #66-162
("ranger_raiders"  ,"Ranger Raiders"   ,icon_ithilien_ranger|carries_goods(1)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_master_ranger_of_ithilien,1,1),(trp_veteran_ranger_of_ithilien,3,6),(trp_ranger_of_ithilien,5,10)]), #118-211 real raiders have more punch
#("beorning_raiders","Beorning Foragers" ,icon_axeman  |carries_goods(1),0,fac_beorn   ,soldier_personality,[(trp_blank,10,15),(trp_blank,10,15),(trp_blank,1,1)]),

("morgul_raiders"  ,"Morgul Raiders"    ,icon_orc           |carries_goods(1)|pf_show_faction,0,fac_mordor  ,soldier_personality,[(trp_fell_morgul_orc,1,1),(trp_morgul_orc,15,30),(trp_orc_archer_of_mordor,15,30)]), #98-188 better raiders
("mordor_raiders"  ,"Mordor Raiders"    ,icon_orc           |carries_goods(1)|pf_show_faction,0,fac_mordor  ,soldier_personality,[(trp_fell_orc_of_mordor,1,1),(trp_orc_of_mordor,13,26),(trp_orc_archer_of_mordor,13,26)]), #86-164
("isengard_raiders","Isengard Raiders"  ,icon_uruk_isengard |carries_goods(1)|pf_show_faction,0,fac_isengard,soldier_personality,[(trp_fighting_uruk_hai_champion,1,1),(trp_large_uruk_hai_of_isengard,3,8),(trp_large_uruk_hai_tracker,8,13),(trp_uruk_snaga_of_isengard,8,13)]), #98-168
("dunland_raiders","Dunlending Raiders",icon_dunland_captain|carries_goods(2)|pf_show_faction,0,fac_dunland ,soldier_personality,[(trp_dunnish_wolf_guard,1,1),(trp_dunnish_wolf_warrior,2,4),(trp_dunnish_vet_warrior,4,8),(trp_dunnish_warrior,8,16)]), #90-164
("harad_raiders"   ,"Haradrim Raiders"  ,icon_harad_horseman|carries_goods(2)|pf_show_faction,0,fac_harad   ,soldier_personality,[(trp_harad_tiger_guard,1,1),(trp_harad_skirmisher,10,20),(trp_harad_desert_warrior,11,20)]), #98-176
("khand_raiders"   ,"Khand Raiders"     ,icon_cataphract    |carries_goods(2)|pf_show_faction,0,fac_khand   ,soldier_personality,[(trp_easterling_horsemaster,1,1),(trp_easterling_rider,5,10),(trp_easterling_veteran_horseman,5,15)]), #81-191
("umbar_raiders"   ,"Umbar Raiders"     ,icon_umbar_corsair |carries_goods(2)|pf_show_faction,0,fac_umbar   ,soldier_personality,[(trp_corsair_night_raider,1,1),(trp_corsair_veteran_raider,4,8),(trp_corsair_pikeman,4,8),(trp_corsair_warrior,6,15)]), #100-196 good at it
("moria_raiders"   ,"Moria Raiders"     ,icon_orc           |carries_goods(2)|pf_show_faction,0,fac_moria   ,soldier_personality,[(trp_fell_goblin_archer_of_moria,1,1),(trp_large_goblin_archer_of_moria,3,9),(trp_large_goblin_of_moria,5,15),(trp_archer_snaga_of_moria,8,16)]), #72-176
("guldur_raiders"  ,"Dol Guldur Raiders",icon_orc_tribal    |carries_goods(2)|pf_show_faction,0,fac_guldur  ,soldier_personality,[(trp_fell_orc_tracker_of_mordor,1,1),(trp_large_orc_of_mordor,4,10),(trp_orc_of_guldur,8,16),(trp_orc_archer_of_mordor,8,16),(trp_orc_snaga_of_guldur,15,30)]), #91-184
("gundabad_raiders","Gundabad Raiders"  ,icon_orc_tribal    |carries_goods(2)|pf_show_faction,0,fac_gundabad,soldier_personality,[(trp_goblin_north_clan_rider,1,3),(trp_keen_eyed_goblin_archer_gundabad,6,12),(trp_goblin_bowmen_gundabad,12,18),(trp_orc_gundabad,18,32),(trp_troll_of_moria,0,1)]), #128-234 was 93-163
("rhun_raiders"    ,"Rhun Raiders"      ,icon_easterling_horseman|carries_goods(1)|pf_show_faction,0,fac_rhun    ,soldier_personality,[(trp_rhun_heavy_noble_cavalry,1,3),(trp_rhun_horse_archer,8,16),(trp_rhun_light_cavalry,10,20)]), #124-264, was 100-184


####TLD Patrols
#MV: in general, average strength should be 300-600, Mordor and Isengard about 20% better than Gondor and Rohan
("gondor_patrol"  ,"Gondor Patrol"    ,icon_footman_gondor |carries_goods(2)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_veteran_knight_of_gondor,1,1),(trp_veteran_archer_of_gondor,3,6),(trp_gondor_veteran_swordsmen,3,6),(trp_archer_of_gondor,8,20),(trp_gondor_swordsmen,8,20)]), #256-568
("rohan_patrol"   ,"Rohirrim Patrol"  ,icon_knight_rohan   |carries_goods(2)|pf_show_faction,0,fac_rohan   ,soldier_personality,[(trp_thengel_guard_of_rohan,1,1),(trp_elite_skirmisher_of_rohan,3,6),(trp_lancer_of_rohan,3,6),(trp_veteran_skirmisher_of_rohan,6,14),(trp_skirmisher_of_rohan,6,14),(trp_rider_of_rohan,8,20)]), #238-505 fast!
("imladris_patrol","Dunedain Patrol"  ,icon_rivendell_elf  |carries_goods(0)|pf_show_faction,0,fac_imladris,soldier_personality,[(trp_knight_of_arnor,1,1),(trp_arnor_horsemen,4,10),(trp_high_swordsman_of_arnor,3,5),(trp_arnor_master_at_arms,8,20),(trp_arnor_man_at_arms,8,20)]), #252-554
("lorien_patrol"  ,"Lothlorien Patrol",icon_lorien_elf_b   |carries_goods(2)|pf_show_faction,0,fac_lorien  ,soldier_personality,[(trp_galadhrim_royal_archer,1,1),(trp_lothlorien_master_archer,3,6),(trp_lothlorien_veteran_archer,4,10),(trp_lothlorien_elite_infantry,8,16),(trp_lothlorien_archer,8,16),(trp_lothlorien_veteran_infantry,10,20)]), #312-615
("woodelf_patrol" ,"Mirkwood Patrol"  ,icon_mirkwood_elf   |carries_goods(2)|pf_show_faction,0,fac_woodelf ,soldier_personality,[(trp_thranduils_royal_marksman,1,1),(trp_greenwood_master_archer,3,6),(trp_greenwood_veteran_archer,4,10),(trp_greenwood_royal_spearman,4,10),(trp_greenwood_veteran_spearman,4,10),(trp_greenwood_archer,8,16)]), #250-525
("dale_patrol"    ,"Dale Patrol"      ,icon_generic_knight    |carries_goods(2)|pf_show_faction,0,fac_dale    ,soldier_personality,[(trp_girions_guard_of_dale,1,1),(trp_dale_marchwarden,4,8),(trp_dale_bill_master,3,8),(trp_dale_billman,4,10),(trp_laketown_archer,6,12),(trp_dale_man_at_arms,6,12)]), #242-518
("esgaroth_patrol","Esgaroth Patrol"  ,icon_ithilien_ranger|carries_goods(2)|pf_show_faction,0,fac_dale    ,soldier_personality,[(trp_girions_guard_of_dale,1,1),(trp_barding_bowmen_of_esgaroth,6,10),(trp_dale_billman,4,10),(trp_laketown_archer,10,15),(trp_laketown_scout,6,12)]), #242-518
("dwarf_patrol"   ,"Dwarven Patrol"   ,icon_dwarf          |carries_goods(2)|pf_show_faction,0,fac_dwarf   ,soldier_personality,[(trp_longbeard_axeman,1,1),(trp_dwarven_bowman,8,16),(trp_dwarven_spearman,5,10),(trp_dwarven_axeman,8,20),(trp_dwarven_lookout,10,25)]), #257-542

("ranger_patrol"  ,"Ranger Patrol"    ,icon_ithilien_ranger|carries_goods(0)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_ithilien_leader,1,1),(trp_master_ranger_of_ithilien,4,8),(trp_veteran_ranger_of_ithilien,6,12),(trp_ranger_of_ithilien,8,20)]), #299-603
("amroth_patrol" ,"Dol Amroth Patrol",icon_knight_dolamroth|carries_goods(2)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_dol_amroth_leader,1,1),(trp_swan_knight_of_dol_amroth,2,6),(trp_knight_of_dol_amroth,6,14),(trp_veteran_squire_of_dol_amroth,8,20),(trp_squire_of_dol_amroth,16,30)]), #241-541
("pelargir_patrol","Pelargir Patrol"  ,icon_footman_gondor |carries_goods(2)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_pelargir_leader,1,1),(trp_pelargir_vet_marine,3,8),(trp_pelargir_vet_infantry,3,8),(trp_pelargir_marine,6,14),(trp_pelargir_infantry,6,14)]), #229-533
("lossarnach_patrol","Lossarnach Patrol",icon_lossarnach_axeman_icon|carries_goods(2)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_lossarnach_leader,1,1),(trp_axemaster_of_lossarnach,3,8),(trp_heavy_lossarnach_axeman,4,10),(trp_archer_of_gondor,8,20),(trp_axeman_of_lossarnach,8,20)]), #213-503
("brv_patrol"     ,"Blackroot Patrol" ,icon_ithilien_ranger|carries_goods(2)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_blackroot_leader,1,1),(trp_master_blackroot_vale_archer,4,8),(trp_veteran_blackroot_vale_archer,6,12),(trp_footman_of_blackroot_vale,8,16),(trp_blackroot_vale_archer,10,20)]), #255-485
("pinnath_patrol" ,"Pinnath Patrol"   ,icon_footman_pinnath|carries_goods(2)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_pinnath_leader,1,1),(trp_pinnath_gelin_archer,3,6),(trp_warrior_of_pinnath_gelin,3,6),(trp_pinnath_gelin_bowman,6,16),(trp_pinnath_gelin_spearman,8,20)]), #247-541
("lamedon_patrol" ,"Lamedon Patrol"  ,icon_lamedon_horseman|carries_goods(2)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_lamedon_leader,1,1),(trp_knight_of_lamedon,3,6),(trp_champion_of_lamedon,3,6),(trp_warrior_of_lamedon,8,20),(trp_veteran_of_lamedon,10,24)]), #253-541

# Used as patrols, except Dale 
("mordor_war_party"  ,"Mordor_War_Party"  ,icon_uruk_x4          |carries_goods(3)|pf_show_faction,0,fac_mordor  ,soldier_personality,[(trp_uruk_mordor_standard_bearer,1,2),(trp_large_uruk_of_mordor,10,22),(trp_uruk_of_mordor,16,36),(trp_orc_of_mordor,20,40),(trp_orc_archer_of_mordor,40,60),(trp_olog_hai,0,3)]), #310-658
("isengard_war_party","Isengard_War_Party",icon_wargrider_walk_x4|carries_goods(3)|pf_show_faction,0,fac_isengard,soldier_personality,[(trp_urukhai_standard_bearer,1,2),(trp_fighting_uruk_hai_berserker,3,6),(trp_fighting_uruk_hai_champion,3,6),(trp_fighting_uruk_hai_tracker,15,25),(trp_wolf_rider_of_isengard,5,10),(trp_armoured_troll,0,3)]), #275-550
("harad_war_party"   ,"Harad_War_Party"   ,icon_cataphract_x3    |carries_goods(3)|pf_show_faction,0,fac_harad   ,soldier_personality,[(trp_harad_tiger_guard,2,4),(trp_fang_heavy_cavalry,2,4),(trp_gold_serpent_horse_archer,2,4),(trp_harad_archer,8,16),(trp_harondor_rider,10,20),(trp_harad_desert_warrior,20,40)]), #268-536
("dunland_war_party" ,"Dunlending_Warband",icon_dunlander_x3     |carries_goods(3)|pf_show_faction,0,fac_dunland ,soldier_personality,[(trp_dunnish_wolf_guard,2,4),(trp_dunnish_veteran_pikeman,6,12),(trp_dunnish_warrior,12,24),(trp_dunnish_raven_rider,10,20),(trp_dunnish_wildman,20,50)]), #214-448 weak
("khand_war_party"   ,"Variag_War_Party"   ,icon_cataphract_x3   |carries_goods(3)|pf_show_faction,0,fac_khand   ,soldier_personality,[(trp_easterling_axe_master,2,4),(trp_easterling_horsemaster,2,4),(trp_easterling_veteran_axeman,5,10),(trp_easterling_axeman,8,16),(trp_easterling_rider,10,20),(trp_easterling_warrior,20,40)]), #277-554
#("corsair_war_party" ,"Corsair_War_Party" ,icon_umbar_corsair_x3 |carries_goods(3),0,fac_umbar   ,soldier_personality,[(trp_pike_master_of_umbar   ,20,50),(trp_corsair_veteran_raider,15,30),(trp_veteran_pikeman_of_umbar,13,36),(trp_master_marksman_of_umbar,5,30),(trp_corsair_veteran_marauder,5,40),(trp_master_assassin_of_umbar,5,20)]),
("moria_war_party"   ,"Moria_War_Party"   ,icon_orc_tribal_x4    |carries_goods(3)|pf_show_faction,0,fac_moria   ,soldier_personality,[(trp_fell_goblin_of_moria,5,10),(trp_large_goblin_archer_of_moria,10,20),(trp_large_goblin_of_moria,12,24),(trp_goblin_of_moria,15,30),(trp_snaga_of_moria,20,50),(trp_troll_of_moria,1,2)]), #262-534
#Northern war
("dale_war_party"  ,"Dale_War_Party"   ,icon_generic_knight       |carries_goods(3)|pf_show_faction,0,fac_dale   ,soldier_personality,[(trp_dale_man_at_arms,8,13),(trp_dale_veteran_warrior,8,20),(trp_barding_bowmen_of_esgaroth,8,16),(trp_laketown_archer,5,20),(trp_dale_billman,10,25),(trp_merchant_squire_or_dale,4,15)]), # NOT USED and unbalanced 383-953
#("dwarf_war_party" ,"Dwarven_War_Party",icon_dwarf_x3              |carries_goods(3),0,fac_dwarf  ,soldier_personality,[(trp_dwarven_apprentice      ,8,13),(trp_grors_guard,8,20),(trp_dwarven_warrior,8,16),(trp_dwarven_expert_axeman,5,20),(trp_dwarven_lookout,4,15),(trp_dwarven_archer,4,15)]),
("rhun_war_party"  ,"Rhun_War_Party"   ,icon_easterling_horseman_x3|carries_goods(3)|pf_show_faction,0,fac_rhun   ,soldier_personality,[(trp_dorwinion_noble_of_rhun,2,4),(trp_rhun_heavy_noble_cavalry,5,10),(trp_rhun_veteran_swift_horseman,8,16),(trp_rhun_veteran_horse_archer,8,16),(trp_rhun_tribal_warrior,12,24),(trp_rhun_tribesman,18,36)]), #358-716 was 260-552

####TLD Companies (only Gondorian used, as a MT patrol)
("gondor_company" ,"Minas Tirith Patrol",icon_knight_gondor |carries_goods(4)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_captain_of_gondor,1,1),(trp_veteran_knight_of_gondor,2,4),(trp_knight_of_gondor,4,8),(trp_gondor_veteran_swordsmen,10,20),(trp_veteran_archer_of_gondor,10,20),(trp_gondor_veteran_spearmen,10,20)]), #573-1121 elite, rare, overpowered
("rohan_company"   ,"Rohan Company"     ,icon_knight_rohan        ,0,fac_rohan   ,soldier_personality,[(trp_elite_rider_of_rohan,25,25),(trp_elite_skirmisher_of_rohan,25,25),(trp_elite_footman_of_rohan,25,25),(trp_eorl_guard_of_rohan,12,12),(trp_thengel_guard_of_rohan,12,12),(trp_captain_of_rohan,1,1)]),
("imladris_company","Rivendell Company" ,icon_rivendell_elf       ,0,fac_imladris,soldier_personality,[(trp_rivendell_infantry,20,33),(trp_rivendell_veteran_infantry,20,33),(trp_rivendell_elite_infantry,20,33),(trp_rivendell_royal_infantry,3,6),(trp_elf_captain_of_rivendell,1,1)]),
("lorien_company"  ,"Lothlorien Company",icon_lorien_elf_b        ,0,fac_lorien  ,soldier_personality,[(trp_lothlorien_veteran_infantry,30,30),(trp_lothlorien_elite_infantry,30,30),(trp_lothlorien_veteran_warden,30,30),(trp_galadhrim_royal_warden,5,5),(trp_galadhrim_royal_swordsman,5,5),(trp_elf_captain_of_lothlorien,1,1)]),
("woodelf_company" ,"Mirkwood Company"  ,icon_mirkwood_elf        ,0,fac_woodelf ,soldier_personality,[(trp_greenwood_veteran_spearman,21,22),(trp_greenwood_veteran_spearman,21,22),(trp_greenwood_veteran_archer,21,22),(trp_greenwood_master_archer,21,22),(trp_thranduils_royal_marksman,8,12)]),
("dale_company"    ,"Dale Company"      ,icon_generic_knight         ,0,fac_dale    ,soldier_personality,[(trp_laketown_archer,20,20),(trp_barding_bowmen_of_esgaroth,20,20),(trp_dale_veteran_warrior,20,20),(trp_dale_bill_master,20,20),(trp_girions_guard_of_dale,20,20)]),
("dwarf_company"   ,"Dwarven Company"   ,icon_dwarf               ,0,fac_dwarf   ,soldier_personality,[(trp_dwarven_hardened_warrior,25,25),(trp_dwarven_lookout,25,25),(trp_dwarven_warrior,20,20),(trp_dwarven_expert_axeman,20,20),(trp_dwarven_archer,10,10)]),

####TLD Elite Companies (not used)
("gondor_elite_company"  ,"Gondor Elite Company"    ,icon_knight_gondo_trot_x3,0,fac_gondor  ,soldier_personality,[(trp_guard_of_the_fountain_court,15,30),(trp_knight_of_the_citadel,15,30),(trp_archer_of_the_tower_guard,15,30),(trp_swordsmen_of_the_tower_guard,15,30),(trp_captain_of_gondor,1,1)]),
("rohan_elite_company"   ,"Rohan Elite Company"     ,icon_knight_rohan_x3     ,0,fac_rohan   ,soldier_personality,[(trp_eorl_guard_of_rohan        ,10,20),(trp_thengel_guard_of_rohan,10,20),(trp_folcwine_guard_of_rohan,10,20),(trp_warden_of_methuseld,10,20),(trp_raider_of_rohan,10,20),(trp_captain_of_rohan,1,1)]),
("imladris_elite_company","Rivendell Elite Company" ,icon_knight_rivendell    ,0,fac_imladris,soldier_personality,[(trp_rivendell_royal_infantry   ,25,50),(trp_knight_of_rivendell,25,50),(trp_elf_captain_of_rivendell,1,1)]),
("lorien_elite_company"  ,"Lothlorien Elite Company",icon_lorien_elf_b_x3     ,0,fac_lorien  ,soldier_personality,[(trp_galadhrim_royal_marksman   ,13,25),(trp_galadhrim_royal_swordsman,13,25),(trp_galadhrim_royal_archer,13,25),(trp_galadhrim_royal_warden,13,25),(trp_noldorin_commander,1,1)]),
("woodelf_elite_company" ,"Mirkwood Elite Company"  ,icon_mirkwood_elf_x3     ,0,fac_woodelf ,soldier_personality,[(trp_greenwood_royal_spearman   ,20,40),(trp_thranduils_royal_marksman,20,40),(trp_elf_captain_of_mirkwood,0,0)]),
("dale_elite_company"    ,"Dale Elite Company"      ,icon_generic_knight         ,0,fac_dale    ,soldier_personality,[(trp_dale_bill_master           ,13,25),(trp_dale_marchwarden,13,25),(trp_girions_guard_of_dale,13,25),(trp_barding_bowmen_of_esgaroth,13,25),(trp_knight_5_1,13,25)]),
("dwarf_elite_company"   ,"Dwarven Elite Company"   ,icon_dwarf_x3            ,0,fac_dwarf   ,soldier_personality,[(trp_dwarven_warrior            ,18,34),(trp_dwarven_expert_axeman,18,34),(trp_dwarven_archer,18,34),(trp_knight_5_6,1,1)]),

####TLD Legions
#("gondor_legion","Gondor Legion",icon_|carries_goods(2),0,fac_,soldier_personality,[(trp_,0,0)]),
#("rohan_legion","Rohan Legion",icon_|carries_goods(2),0,fac_,soldier_personality,[(trp_,0,0)]),
#("rivendell_legion","Rivendell Legion",icon_|carries_goods(2),0,fac_,soldier_personality,[(trp_,0,0)]),
#("lorien_legion","Lothlorien Legion",icon_|carries_goods(2),0,fac_,soldier_personality,[(trp_,0,0)]),
#("mirkwood_legion","Mirkwood Legion",icon_|carries_goods(2),0,fac_,soldier_personality,[(trp_,0,0)]),
#("dale_legion","Dale Legion",icon_|carries_goods(2),0,fac_,soldier_personality,[(trp_,0,0)]),
#("dwarven_legion","Dwarven Legion",icon_|carries_goods(2),0,fac_,soldier_personality,[(trp_,0,0)]),

####TLD Caravans
# MV guidelines:
# - make good caravans stronger than evil (allegedly good guys care more about supplies)
# - favor guard and militia units, no elite troops should be tied down to escort duty (tiers 2-4)
# - in general, caravans are stronger than raiders, but weaker than patrols
# - aim for strength 250-500
("gondor_caravan"  ,"Gondor Caravan"    ,icon_supply_gondor|carries_goods(10)|pf_show_faction,0,fac_gondor  ,prisoner_train_personality,[(trp_knight_of_gondor,1,4),(trp_squire_of_gondor,4,10),(trp_gondor_swordsmen,4,10),(trp_gondor_spearmen,4,10),(trp_archer_of_gondor,7,14),(trp_gondor_militiamen,30,50)]), # strength 280-582
("rohan_caravan"   ,"Rohan Caravan"     ,icon_supply_rohan |carries_goods(10)|pf_show_faction,0,fac_rohan   ,prisoner_train_personality,[(trp_veteran_rider_of_rohan,1,4),(trp_squire_of_rohan,4,10),(trp_veteran_skirmisher_of_rohan,7,14),(trp_veteran_footman_of_rohan,6,14),(trp_guardsman_of_rohan,26,42)]), # strength 246-496
("imladris_caravan","Rivendell Caravan" ,icon_mule         |carries_goods(10)|pf_show_faction,0,fac_imladris,prisoner_train_personality,[(trp_rivendell_cavalry,1,4),(trp_rivendell_veteran_sentinel,4,10),(trp_rivendell_sentinel,12,24),(trp_rivendell_veteran_scout,10,16),(trp_rivendell_infantry,14,24)]), # strength 254-508
("lorien_caravan"  ,"Lothlorien Caravan",icon_mule         |carries_goods(10)|pf_show_faction,0,fac_lorien  ,prisoner_train_personality,[(trp_lothlorien_veteran_warden,2,6),(trp_lothlorien_elite_infantry,4,10),(trp_lothlorien_archer,14,30),(trp_lothlorien_warden,12,18),(trp_lothlorien_veteran_infantry,16,28)]), # strength 298-600
("woodelf_caravan" ,"Mirkwood Caravan"  ,icon_mule         |carries_goods(10)|pf_show_faction,0,fac_woodelf ,prisoner_train_personality,[(trp_greenwood_vet_sentinel,1,4),(trp_greenwood_royal_spearman,4,10),(trp_greenwood_sentinel,12,24),(trp_greenwood_veteran_scout,10,16),(trp_greenwood_spearman,14,24)]), # strength 254-508
("dale_caravan"    ,"Dale Caravan"      ,icon_mule         |carries_goods(10)|pf_show_faction,0,fac_dale    ,prisoner_train_personality,[(trp_merchant_protector_of_dale,1,5),(trp_laketown_archer,5,10),(trp_merchant_guard_of_dale,4,8),(trp_dale_warrior,8,16),(trp_laketown_scout,18,30)]), # strength 198-399
("dwarf_caravan"   ,"Dwarven Caravan"   ,icon_mule         |carries_goods(10)|pf_show_faction,0,fac_dwarf   ,prisoner_train_personality,[(trp_dwarven_axeman,2,6),(trp_dwarven_bowman,2,4),(trp_dwarven_hardened_warrior,12,24),(trp_dwarven_lookout,16,24),(trp_dwarven_warrior,20,40)]), # strength 264-514

("mordor_caravan"  ,"Mordor Supply Train"  ,icon_supply_mordor  |carries_goods(10)|pf_show_faction,0,fac_mordor  ,prisoner_train_personality, [(trp_large_uruk_of_mordor, 4, 12), (trp_large_orc_archer_of_mordor, 8, 18), (trp_large_orc_of_mordor, 8, 18), (trp_orc_archer_of_mordor, 14, 22), (trp_orc_of_mordor, 18, 30)]), # strength 200-408
("isengard_caravan","Isengard Supply Train",icon_supply_isengard|carries_goods(10)|pf_show_faction,0,fac_isengard,prisoner_train_personality, [(trp_warg_rider_of_isengard, 3, 8), (trp_large_uruk_hai_of_isengard, 6, 16), (trp_uruk_hai_of_isengard, 6, 10), (trp_uruk_hai_tracker, 6, 10), (trp_orc_of_isengard, 20, 40)]), # strength 159-336
("gunda_caravan"   ,"Gundabad Supply Train",icon_supply_isengard|carries_goods(10)|pf_show_faction,0,fac_gundabad,prisoner_train_personality, [(trp_goblin_north_clan_rider, 1, 2), (trp_keen_eyed_goblin_archer_gundabad, 6, 16), (trp_goblin_bowmen_gundabad, 6, 10), (trp_orc_gundabad, 20, 30)]),

####TLD Prisoner Trains
# MV guidelines:
# - make evil prisoner trains stronger than good (allegedly evil guys care more about guarding slaves/prisoners)
# - as for caravans: favor guard and militia units, no elite troops should be tied down to escort duty (tiers 1-3)
# - prisoner trains should be about half the size of caravans, but slow and interceptable, so give them more slow tier 1 troops and no/less cavalry
# - aim for strength 150-250
("gondor_p_train"  ,"Gondor Prisoner Train"    ,icon_supply_gondor|pf_show_faction,0,fac_gondor  ,prisoner_train_personality,[(trp_footmen_of_gondor,1,2), (trp_bowmen_of_gondor,4,6), (trp_gondor_militiamen,15,25), (trp_gondor_commoner,30,45)]), # strength 150-238
("rohan_p_train"   ,"Rohan Prisoner Train"     ,icon_supply_rohan |pf_show_faction,0,fac_rohan   ,prisoner_train_personality,[(trp_footman_of_rohan,2,4), (trp_dismounted_skirmisher_of_rohan,4,6), (trp_squire_of_rohan,4,6), (trp_guardsman_of_rohan,8,12), (trp_rohan_youth,24,30)]), # strength 132-192
("imladris_p_train","Rivendell Prisoner Train" ,icon_mule         |pf_show_faction,0,fac_imladris,prisoner_train_personality,[(trp_rivendell_veteran_infantry,2,4), (trp_rivendell_sentinel,2,4), (trp_rivendell_infantry,6,10), (trp_rivendell_veteran_scout,6,8), (trp_rivendell_scout,25,35)]), # strength 138-216
("lorien_p_train"  ,"Lothlorien Prisoner Train",icon_mule         |pf_show_faction,0,fac_lorien  ,prisoner_train_personality,[(trp_lothlorien_archer,6,10), (trp_lothlorien_veteran_infantry,6,10), (trp_lothlorien_warden,6,10), (trp_lothlorien_infantry,25,35)]), # strength 152-240
("woodelf_p_train" ,"Mirkwood Prisoner Train"  ,icon_mule         |pf_show_faction,0,fac_woodelf ,prisoner_train_personality,[(trp_greenwood_sentinel,2,4), (trp_greenwood_veteran_spearman,2,4), (trp_greenwood_spearman,6,10), (trp_greenwood_veteran_scout,6,8), (trp_greenwood_scout,25,35)]), # strength 138-216
("dale_p_train"    ,"Dale Prisoner Train"      ,icon_mule         |pf_show_faction,0,fac_dale    ,prisoner_train_personality,[(trp_merchant_guard_of_dale,1,2), (trp_dale_warrior,1,2), (trp_laketown_bowmen,1,2), (trp_dale_man_at_arms,4,6), (trp_laketown_scout,6,10), (trp_dale_militia,21,25)]), # strength 100-150
("dwarf_p_train"   ,"Dwarven Prisoner Train"   ,icon_mule         |pf_show_faction,0,fac_dwarf   ,prisoner_train_personality,[(trp_dwarven_hardened_warrior,2,4), (trp_dwarven_scout,4,6), (trp_dwarven_warrior,4,6), (trp_dwarven_lookout,8,14), (trp_dwarven_apprentice,25,35)]), # strength 140-220

("mordor_p_train"  ,"Mordor Prisoner Train"    ,icon_slaver_mordor  |carries_goods(2)|pf_show_faction,0,fac_mordor  , prisoner_train_personality, [(trp_large_orc_of_mordor,6,8), (trp_orc_tracker_of_mordor,6,10), (trp_orc_of_mordor,16,24), (trp_orc_archer_of_mordor,16,24), (trp_orc_snaga_of_mordor,40,60)]), # strength 196-294
("isengard_p_train","Isengard Prisoner Train"  ,icon_slaver_isengard|carries_goods(2)|pf_show_faction,0,fac_isengard, prisoner_train_personality, [(trp_warg_rider_of_isengard,4,6), (trp_large_orc_of_isengard,10,14), (trp_orc_of_isengard,24,36), (trp_orc_snaga_of_isengard,40,60)]), # strength 182-268

("kingdom_hero_party","War Party",icon_player_horseman|pf_show_faction|pf_default_behavior,0,fac_commoners,soldier_personality,[]),

# Reinforcements

#MV: Guidelines:
# A: base tier 1 and 2 troops (7-14 total)
# B: tier 3 archers mixed with other tier 3 troops and tier 2 archers, troops more useful in sieges (5-10 total)
# C: tier 4 troop mix, mostly cavalry, troops more useful in field battles (4-8 total)
# Notes:
# - with reinforcements quantity counts more than quality, compared to normal non-upgradable party templates
# - balance between (sub)trees to get a desired mix of inv, arch, cav
# - towns get 60% A, 35% B, 5% C (more low level troops and archers); heroes get 50% A, 30% B, 20% C (more cavalry) - see script_cf_reinforce_party
# - sort order: higher tier and mounted troops first

("gondor_reinf_d"    ,"_",0,0,fac_commoners,0,[(trp_knight_of_the_citadel,1,2), (trp_archer_of_the_tower_guard,2,4), (trp_swordsmen_of_the_tower_guard,1,2), (trp_guard_of_the_fountain_court,1,2),]), #MT garrison only

("gondor_reinf_a"    ,"_",0,0,fac_commoners,0,[(trp_gondor_militiamen,3,6),(trp_gondor_commoner,4,8)]),
("gondor_reinf_b"    ,"_",0,0,fac_commoners,0,[(trp_bowmen_of_gondor,3,5),(trp_footmen_of_gondor,1,2),(trp_gondor_militiamen,1,2),(trp_gondor_noblemen,0,1),]), #T1 cav because it has a separate tree
("gondor_reinf_c"    ,"_",0,0,fac_commoners,0,[(trp_archer_of_gondor,1,2),(trp_gondor_spearmen,2,3),(trp_gondor_swordsmen,0,1),(trp_veteran_squire_of_gondor,1,2),]),
("pelargir_reinf_a"  ,"_",0,0,fac_commoners,0,[(trp_pelargir_watchman,6,12),]), #no T1
("pelargir_reinf_b"  ,"_",0,0,fac_commoners,0,[(trp_pelargir_marine,1,2),(trp_pelargir_infantry,1,2),(trp_pelargir_watchman,3,6),]), #no T3
("pelargir_reinf_c"  ,"_",0,0,fac_commoners,0,[(trp_pelargir_marine,2,5),(trp_pelargir_infantry,2,3),]),
("dol_amroth_reinf_a","_",0,0,fac_commoners,0,[(trp_squire_of_dol_amroth,2,4),(trp_dol_amroth_youth,5,10),]),
("dol_amroth_reinf_b","_",0,0,fac_commoners,0,[(trp_veteran_squire_of_dol_amroth,3,6),(trp_squire_of_dol_amroth,2,4),]),
("dol_amroth_reinf_c","_",0,0,fac_commoners,0,[(trp_knight_of_dol_amroth,4,8),]),
("lamedon_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_footman_of_lamedon,2,4),(trp_clansman_of_lamedon,5,10),]),
("lamedon_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_veteran_of_lamedon,4,8),(trp_footman_of_lamedon,1,2),]),
("lamedon_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_warrior_of_lamedon,4,8),]),
("lossarnach_reinf_a","_",0,0,fac_commoners,0,[(trp_axeman_of_lossarnach,2,4),(trp_woodsman_of_lossarnach,5,10),]),
("lossarnach_reinf_b","_",0,0,fac_commoners,0,[(trp_vet_axeman_of_lossarnach,4,8),(trp_axeman_of_lossarnach,1,2),]),
("lossarnach_reinf_c","_",0,0,fac_commoners,0,[(trp_heavy_lossarnach_axeman,4,8),]),
("pinnath_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_pinnath_gelin_plainsman,6,12),]), #no T1
("pinnath_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_pinnath_gelin_bowman,1,2),(trp_pinnath_gelin_spearman,1,2),(trp_pinnath_gelin_plainsman,3,6)]), #no T3
("pinnath_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_pinnath_gelin_spearman,2,4),(trp_pinnath_gelin_bowman,2,4)]),
("ithilien_reinf_a"  ,"_",0,0,fac_commoners,0,[(trp_ranger_of_ithilien,4,7),]), #since they begin at T4, halve them
("ithilien_reinf_b"  ,"_",0,0,fac_commoners,0,[(trp_veteran_ranger_of_ithilien,3,5),]),
("ithilien_reinf_c"  ,"_",0,0,fac_commoners,0,[(trp_master_ranger_of_ithilien,2,4),]),
("blackroot_reinf_a" ,"_",0,0,fac_commoners,0,[(trp_blackroot_vale_archer,6,12)]), #no T1
("blackroot_reinf_b" ,"_",0,0,fac_commoners,0,[(trp_footman_of_blackroot_vale,1,2),(trp_veteran_blackroot_vale_archer,1,2),(trp_blackroot_vale_archer,3,6),]), #no T3
("blackroot_reinf_c" ,"_",0,0,fac_commoners,0,[(trp_veteran_blackroot_vale_archer,2,4),(trp_footman_of_blackroot_vale,2,4),]),
#rohan	
("rohan_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_squire_of_rohan,1,2),(trp_guardsman_of_rohan,2,4),(trp_rohan_youth,4,8),]),
("rohan_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_rider_of_rohan,1,2),(trp_skirmisher_of_rohan,3,5),(trp_footman_of_rohan,1,2),(trp_squire_of_rohan,0,1),]),
("rohan_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_veteran_rider_of_rohan,1,2),(trp_lancer_of_rohan,1,2),(trp_veteran_skirmisher_of_rohan,1,2),(trp_veteran_footman_of_rohan,1,2),]),
#Isengard - two short trees (up to T4/T5), easier to upgrade, so lower tier reinforcements; also extra orcs (8-16, 7-13, 5-10)
("isengard_reinf_a","_",0,0,fac_commoners,0,[(trp_uruk_snaga_of_isengard,3,6),(trp_orc_snaga_of_isengard,5,10),]), #two T1
("isengard_reinf_b","_",0,0,fac_commoners,0,[(trp_wolf_rider_of_isengard,2,3),(trp_uruk_hai_tracker,2,4),(trp_uruk_hai_of_isengard,1,2),(trp_orc_of_isengard,2,4),]), #more T2 troops
("isengard_reinf_c","_",0,0,fac_commoners,0,[(trp_warg_rider_of_isengard,1,2),(trp_large_uruk_hai_of_isengard,1,2),(trp_uruk_hai_pikeman,1,2),(trp_large_orc_of_isengard,1,2),(trp_large_orc_despoiler,1,2),]), #more T3 troops
#Mordor - same as Isengard + Numenorean cavalry (8-16, 7-13, 5-10)
("mordor_reinf_a"  ,"_",0,0,fac_commoners,0,[(trp_uruk_snaga_of_mordor,3,6),(trp_orc_snaga_of_mordor,5,10),]),
("mordor_reinf_b"  ,"_",0,0,fac_commoners,0,[(trp_orc_archer_of_mordor,2,4),(trp_large_orc_archer_of_mordor,2,4),(trp_uruk_of_mordor,2,3),(trp_orc_of_mordor,2,4),]),
("mordor_reinf_c"  ,"_",0,0,fac_commoners,0,[(trp_warg_rider_of_gorgoroth,1,2),(trp_large_uruk_of_mordor,1,1),(trp_uruk_slayer_of_mordor,0,1),(trp_large_orc_archer_of_mordor,1,2),(trp_large_orc_of_mordor,1,2),(trp_olog_hai,0,1),]),
#Harad (7-14, 5-10, 4-8)
("harad_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_harondor_scout,1,2),(trp_far_harad_tribesman,1,2),(trp_harad_desert_warrior,5,10),]),
("harad_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_harad_horse_archer,1,2),(trp_harad_skirmisher,2,4),(trp_harad_infantry,1,2),(trp_far_harad_tribesman,1,2),]),
("harad_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_black_snake_horse_archer,1,2),(trp_harondor_light_cavalry,1,2),(trp_far_harad_champion,1,2),(trp_harad_swordsman,1,1),(trp_harad_veteran_infantry,0,1),]),
#Rhun
("rhun_reinf_a"    ,"_",0,0,fac_commoners,0,[(trp_rhun_light_horseman,1,2),(trp_rhun_horse_scout,2,3),(trp_rhun_tribesman,5,10),]),
("rhun_reinf_b"    ,"_",0,0,fac_commoners,0,[(trp_rhun_horse_archer,3,5),(trp_rhun_light_cavalry,1,2),(trp_rhun_tribal_infantry,2,4),]),
("rhun_reinf_c"    ,"_",0,0,fac_commoners,0,[(trp_rhun_noble_cavalry,2,4),(trp_rhun_veteran_swift_horseman,1,2),(trp_rhun_veteran_horse_archer,2,4),]),
#Khand
("khand_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_easterling_rider,1,2),(trp_easterling_warrior,2,4),(trp_easterling_youth,4,8),]),
("khand_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_easterling_skirmisher,2,4),(trp_easterling_horseman,0,1),(trp_easterling_axeman,2,3),(trp_khand_glaive_whirler,1,2),]),
("khand_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_easterling_veteran_horseman,2,4),(trp_easterling_veteran_skirmisher,1,2),(trp_variag_pitfighter,1,2)]),
#Umbar (7-14, 5-10, 4-8)
("umbar_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_militia_of_umbar,1,2),(trp_corsair_warrior,2,4),(trp_corsair_youth,4,8),]),
("umbar_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_black_numenorean_renegade,1,2),(trp_corsair_marauder,1,2),(trp_marksman_of_umbar,2,4),(trp_corsair_pikeman,1,2)]),
("umbar_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_black_numenorean_warrior,1,2),(trp_corsair_veteran_raider,1,2),(trp_corsair_veteran_marauder,1,2),(trp_veteran_marksman_of_umbar,1,2),]),
#Lothlorien - Elves get slightly less troops (6-12, 4-8, 4-8)
("lorien_reinf_a"  ,"_",0,0,fac_commoners,0,[(trp_lothlorien_veteran_infantry,1,2),(trp_lothlorien_veteran_scout,1,2),(trp_lothlorien_scout,2,4),(trp_lothlorien_infantry,2,4),]),
("lorien_reinf_b"  ,"_",0,0,fac_commoners,0,[(trp_lothlorien_archer,2,4),(trp_lothlorien_veteran_infantry,1,2),(trp_lothlorien_warden,1,2),]),
("lorien_reinf_c"  ,"_",0,0,fac_commoners,0,[(trp_lothlorien_veteran_archer,2,4),(trp_lothlorien_elite_infantry,1,2),(trp_lothlorien_veteran_warden,1,2),]),
#Imladris - two trees, Rivendell favored over Dunedain (6-12, 4-8, 4-8)
("imladris_reinf_a","_",0,0,fac_commoners,0,[(trp_rivendell_veteran_scout,1,2),(trp_rivendell_infantry,1,1),(trp_dunedain_trained_scout,0,1),(trp_rivendell_scout,2,4),(trp_dunedain_scout,2,4)]),
("imladris_reinf_b","_",0,0,fac_commoners,0,[(trp_rivendell_sentinel,2,4),(trp_dunedain_ranger,1,1),(trp_rivendell_veteran_infantry,1,2),(trp_arnor_man_at_arms,0,1),]),
("imladris_reinf_c","_",0,0,fac_commoners,0,[(trp_rivendell_cavalry,2,4),(trp_arnor_horsemen,1,1),(trp_rivendell_elite_infantry,1,2),(trp_dunedain_veteran_ranger,0,1),]),
#Woodelves (6-12, 4-8, 4-8)
("woodelf_reinf_a" ,"_",0,0,fac_commoners,0,[(trp_greenwood_veteran_scout,1,3),(trp_greenwood_spearman,1,2),(trp_greenwood_scout,4,7),]),
("woodelf_reinf_b" ,"_",0,0,fac_commoners,0,[(trp_greenwood_archer,2,4),(trp_greenwood_sentinel,1,2),(trp_greenwood_veteran_spearman,1,2),]),
("woodelf_reinf_c" ,"_",0,0,fac_commoners,0,[(trp_greenwood_veteran_archer,1,2),(trp_greenwood_vet_sentinel,1,2),(trp_greenwood_royal_spearman,2,4),]),
#Moria (8-16, 7-13, 5-10)
("moria_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_snaga_of_moria,8,16),]),
("moria_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_archer_snaga_of_moria,4,7),(trp_goblin_of_moria,3,6),]),
("moria_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_wolf_rider_of_moria,3,6),(trp_large_goblin_of_moria,1,2),(trp_large_goblin_archer_of_moria,1,2),(trp_troll_of_moria,1,1),]),
#Dol Guldur - same as Mordor without uruks and Numenoreans (8-16, 7-13, 5-10)
("guldur_reinf_a"  ,"_",0,0,fac_commoners,0,[(trp_orc_snaga_of_guldur,8,16),]),
("guldur_reinf_b"  ,"_",0,0,fac_commoners,0,[(trp_orc_archer_of_mordor,4,7),(trp_orc_of_guldur,3,6),]),
("guldur_reinf_c"  ,"_",0,0,fac_commoners,0,[(trp_warg_rider_of_gorgoroth,1,2),(trp_large_orc_archer_of_mordor,1,2),(trp_orc_tracker_of_mordor,1,2),(trp_large_orc_of_mordor,1,2),(trp_olog_hai,0,1),]),
#Beornings - two trees, Beornings favored over Woodmen (7-14, 5-10, 4-8)
("beorn_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_beorning_warrior,2,4),(trp_beorning_vale_man,2,4),(trp_woodmen_youth,3,6)]),
("beorn_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_woodmen_scout,2,4),(trp_woodmen_skilled_forester,1,2),(trp_beorning_tolltacker,1,2),(trp_beorning_carrock_lookout,1,2)]),
("beorn_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_beorning_sentinel,1,3),(trp_beorning_carrock_fighter,2,3),(trp_woodmen_axemen,1,2),]),
#Mt. Gundabad - see Moria (8-16, 7-13, 5-10)
("gundabad_reinf_a","_",0,0,fac_commoners,0,[(trp_goblin_gundabad,8,16)]),
("gundabad_reinf_b","_",0,0,fac_commoners,0,[(trp_goblin_bowmen_gundabad,4,7),(trp_orc_gundabad,4,7),]),
("gundabad_reinf_c","_",0,0,fac_commoners,0,[(trp_goblin_rider_gundabad,2,5),(trp_orc_fighter_gundabad,2,3),(trp_keen_eyed_goblin_archer_gundabad,1,3),(trp_troll_of_moria,1,1),]),
#Dale (7-14, 5-10, 4-8)
("dale_reinf_a"    ,"_",0,0,fac_commoners,0,[(trp_dale_man_at_arms,1,2),(trp_laketown_scout,1,2),(trp_dale_militia,5,10),]),
("dale_reinf_b"    ,"_",0,0,fac_commoners,0,[(trp_merchant_squire_or_dale,0,1),(trp_laketown_bowmen,3,5),(trp_dale_pikeman,1,2),(trp_dale_warrior,1,2),]),
("dale_reinf_c"    ,"_",0,0,fac_commoners,0,[(trp_merchant_protector_of_dale,2,4),(trp_dale_billman,1,2),(trp_dale_veteran_warrior,1,2),]),
#Erebor (7-14, 5-10, 4-8)
("dwarf_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_dwarven_warrior,1,2),(trp_dwarven_lookout,1,2),(trp_iron_hills_miner,1,2),(trp_dwarven_apprentice,4,8),]),
("dwarf_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_dwarven_scout,1,3),(trp_dwarven_hardened_warrior,4,6),(trp_iron_hills_miner,0,1),]),
("dwarf_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_dwarven_bowman,1,2),(trp_dwarven_axeman,1,2),(trp_dwarven_spearman,1,2),(trp_iron_hills_infantry,1,2),]),
#Dunlenders (7-14, 5-10, 4-8)
("dunland_reinf_a" ,"_",0,0,fac_commoners,0,[(trp_dunnish_warrior,3,6),(trp_dunnish_wildman,4,8),]),
("dunland_reinf_b" ,"_",0,0,fac_commoners,0,[(trp_dunnish_vet_warrior,3,6),(trp_dunnish_pikeman,2,4),]),
("dunland_reinf_c" ,"_",0,0,fac_commoners,0,[(trp_dunnish_raven_rider,1,2),(trp_dunnish_wolf_warrior,2,4),(trp_dunnish_veteran_pikeman,1,2),]),

#Volunteer templates
#MV guidelines:
#  - A mix of T1 (tier 1) troops, size 2-5 (if there are no T1, use fewer T2)
#  - Ideally the starting troops from each faction subtree

("gondor_cap_recruits","_",0,0,fac_commoners,0,[(trp_gondor_commoner,2,5),(trp_gondor_noblemen,1,1)]),
("gondor_recruits"    ,"_",0,0,fac_commoners,0,[(trp_gondor_commoner,1,4),(trp_gondor_noblemen,0,1)]),
("pelargir_recruits"  ,"_",0,0,fac_commoners,0,[(trp_pelargir_watchman,1,4)]), #T2
("dol_amroth_recruits","_",0,0,fac_commoners,0,[(trp_dol_amroth_youth,2,4)]), #Cavalry line nerf
("lamedon_recruits"   ,"_",0,0,fac_commoners,0,[(trp_clansman_of_lamedon,2,5)]),
("lossarnach_recruits","_",0,0,fac_commoners,0,[(trp_woodsman_of_lossarnach,2,5)]),
("pinnath_recruits"   ,"_",0,0,fac_commoners,0,[(trp_pinnath_gelin_plainsman,1,4)]), #T2
("ithilien_recruits"  ,"_",0,0,fac_commoners,0,[(trp_ranger_of_ithilien,1,2)]), #T4! nerf
("blackroot_recruits" ,"_",0,0,fac_commoners,0,[(trp_blackroot_vale_archer,1,4)]), #T2

("rohan_recruits"     ,"_",0,0,fac_commoners,0,[(trp_rohan_youth,2,4)]),
("rohan_cap_recruits" ,"_",0,0,fac_commoners,0,[(trp_rohan_youth,2,6)]),
("isengard_recruits"  ,"_",0,0,fac_commoners,0,[(trp_uruk_snaga_of_isengard,1,2),(trp_orc_snaga_of_isengard,1,3)]), #two T1
("morannon_recruits"  ,"_",0,0,fac_commoners,0,[(trp_uruk_snaga_of_mordor,0,2),(trp_orc_snaga_of_mordor,3,5),(trp_black_numenorean_renegade,1,1),]), #two T1 & prize
("mordor_recruits"    ,"_",0,0,fac_commoners,0,[(trp_uruk_snaga_of_mordor,0,2),(trp_orc_snaga_of_mordor,3,5)]), #two T1
("morgul_recruits"    ,"_",0,0,fac_commoners,0,[(trp_uruk_snaga_of_mordor,1,2),(trp_morgul_orc,1,2)]), #T1 T2
("harad_recruits"     ,"_",0,0,fac_commoners,0,[(trp_harad_desert_warrior,1,3),(trp_harondor_scout,0,2),(trp_far_harad_tribesman,1,2)]), #three T1
("rhun_recruits"      ,"_",0,0,fac_commoners,0,[(trp_rhun_tribesman,1,4),(trp_rhun_light_horseman,1,1)]), #T1 and T2
("khand_recruits"     ,"_",0,0,fac_commoners,0,[(trp_easterling_youth,2,5)]),
("umbar_recruits"     ,"_",0,0,fac_commoners,0,[(trp_corsair_youth,3,6)]),
("lorien_recruits"    ,"_",0,0,fac_commoners,0,[(trp_lothlorien_scout,1,3),(trp_lothlorien_infantry,1,1)]), #two T1
("imladris_recruits"  ,"_",0,0,fac_commoners,0,[(trp_rivendell_scout,1,2),(trp_dunedain_scout,1,2)]), #two T1
("woodelf_recruits"   ,"_",0,0,fac_commoners,0,[(trp_greenwood_scout,1,4)]),
("moria_recruits"     ,"_",0,0,fac_commoners,0,[(trp_snaga_of_moria,5,10)]),
("guldur_recruits"    ,"_",0,0,fac_commoners,0,[(trp_orc_snaga_of_guldur,5,10)]),
("beorn_recruits"     ,"_",0,0,fac_commoners,0,[(trp_beorning_vale_man,2,5)]),
("woodman_recruits"   ,"_",0,0,fac_commoners,0,[(trp_woodmen_youth,2,5)]),
("gundabad_recruits"  ,"_",0,0,fac_commoners,0,[(trp_goblin_gundabad,3,6)]),
("gundabad_cap_recruits","_",0,0,fac_commoners,0,[(trp_goblin_gundabad,3,7)]),
("dale_recruits"      ,"_",0,0,fac_commoners,0,[(trp_dale_militia,1,4),(trp_merchant_squire_or_dale,1,1)]), #T1 and T2
("dwarf_recruits"     ,"_",0,0,fac_commoners,0,[(trp_dwarven_apprentice,2,4)]), #T1 and T2
("dwarf_iron_recruits","_",0,0,fac_commoners,0,[(trp_iron_hills_miner,1,3)]), #T1 and T2
("dunland_recruits"   ,"_",0,0,fac_commoners,0,[(trp_dunnish_wildman,3,7)]),

("caravan_survivors","Caravan Survivors",icon_generic_knight|carries_goods(2),0,fac_neutral,merchant_personality,[(trp_sea_raider,5,5)]),

# Morale parties

("routed_allies","Routed Allies",icon_axeman|carries_goods(3),0,fac_outlaws,merchant_personality,[]),
("routed_enemies","Routed Enemies",icon_axeman|carries_goods(3),0,fac_outlaws,merchant_personality,[]),

# Mordor Legions

("legion_minas_morgul","Legion_of_Minas_Morgul",icon_uruk_x4|carries_goods(3), 0, fac_mordor, soldier_personality,[(trp_high_captain_of_mordor,1,1),(trp_black_numenorean_horsemaster,10,30),(trp_fell_uruk_of_mordor,30,60),(trp_uruk_of_mordor,45,105)]),
("legion_udun","Legion_of_Udun",icon_uruk_x4|carries_goods(3), 0, fac_mordor, soldier_personality,[(trp_high_captain_of_mordor,1,1),(trp_easterling_elite_skirmisher,10,30),(trp_fell_orc_archer_of_mordor,30,45),(trp_fell_uruk_slayer_of_mordor, 30, 45),(trp_orc_of_mordor,30,90)]),
("legion_gorgoroth","Legion_of_Gorgoroth",icon_uruk_x4|carries_goods(3), 0, fac_mordor, soldier_personality,[(trp_high_captain_of_mordor,1,1),(trp_captain_of_mordor,3,3),(trp_olog_hai,10,10),(trp_warg_rider_of_gorgoroth,50,80),(trp_uruk_of_mordor,50,110)]),
("legion_barad_dur","Legion_of_Barad-Dur",icon_uruk_x4|carries_goods(3), 0, fac_mordor, soldier_personality,[(trp_high_captain_of_mordor,1,1),(trp_captain_of_mordor,5,5),(trp_black_uruk_of_barad_dur,60,60),(trp_uruk_of_mordor,30,90),(trp_great_warg_rider_of_mordor,60,60),(trp_olog_hai,20,20)]),

]
