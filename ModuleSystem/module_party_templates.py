from header_common import *
from header_parties import *
from ID_troops import *
from ID_factions import *
from ID_map_icons import *
from ID_menus import *
from module_scripts_common_warp import common_warp_templates

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

("wild_troll",       "Wild Troll",          icon_wild_troll   |pf_quest_party,  0,fac_neutral,	bandit_personality,[(trp_wild_troll,1,2),]),
("raging_trolls",    "Raging Trolls",       icon_wild_troll   |pf_quest_party,  0,fac_neutral,	bandit_personality,[(trp_wild_troll,1,3),]),
("looters",          "Tribal Orcs",         icon_orc_tribal   |carries_goods(4),0,fac_outlaws,  bandit_personality,[(trp_tribal_orc_warrior,0,1),(trp_tribal_orc,2,25)]),
("forest_bandits",   "Orc Stragglers",      icon_orc_tribal   |carries_goods(4),0,fac_outlaws,  bandit_personality,[(trp_tribal_orc_warrior,0,8),(trp_tribal_orc,3,40),(trp_mountain_goblin,1,30)]),
("mountain_bandits", "Wild Goblins",        icon_orc_tribal   |carries_goods(4),0,fac_outlaws,  bandit_personality,[(trp_mountain_goblin,2,40)]),
("steppe_bandits",   "Dunland Outcasts",    icon_dunlander    |carries_goods(4),0,fac_outlaws,  bandit_personality,[(trp_i2_dun_warrior,3,10), (trp_i1_dun_wildman,5,35)]),
("sea_raiders",      "Corsair Renegades",   icon_umbar_corsair|carries_goods(4),0,fac_outlaws,  bandit_personality,[(trp_i4_corsair_raider,1,5),(trp_i2_corsair_warrior,3,20),(trp_a2_corsair_marine,3,15)]),

("deserters","Deserters",icon_axeman|carries_goods(3),0,fac_deserters,bandit_personality,[]),

("merchant_caravan","Merchant Caravan",icon_mule|carries_goods(20)|pf_auto_remove_in_town|pf_quest_party,0,fac_commoners,escorted_merchant_personality,[(trp_caravan_master,1,1),(trp_caravan_guard,5,25)]),
("troublesome_bandits","Troublesome Goblins",icon_orc_tribal|carries_goods(9)|pf_quest_party,0,fac_deserters,bandit_personality,[(trp_tribal_orc,14,55)]),
("fangorn_orcs","Tree-chopping Orcs",icon_orc_x4|carries_goods(9)|pf_quest_party,0,fac_neutral,bandit_personality,[(trp_i5_isen_fighting_uruk_champion,1,1),(trp_i3_isen_large_uruk,3,8),(trp_a3_isen_large_uruk_tracker,8,13),(trp_i1_isen_uruk_snaga,12,24)]),
# ("bandits_awaiting_ransom","Bandits Awaiting Ransom",icon_axeman|carries_goods(9)|pf_auto_remove_in_town|pf_quest_party,0,fac_neutral,bandit_personality,[(trp_brigand,24,58),(trp_kidnapped_girl,1,1,pmf_is_prisoner)]),
# ("kidnapped_girl","Kidnapped Girl",icon_woman|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_kidnapped_girl,1,1)]),

("village_farmers","Village Farmers",icon_peasant,0,fac_innocents,merchant_personality,[(trp_farmer,5,10),(trp_peasant_woman,3,8)]),

("spy_partners", "Suspicious Travellers", icon_generic_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy_partner,1,1),(trp_c2_amroth_squire,5,11)]),
("spy_partners_evil", "Suspicious Travellers", icon_generic_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy_partner_evil,1,1),(trp_ac4_dun_crebain_rider,5,11)]),
("runaway_serfs","Runaway Slaves",icon_peasant|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_farmer,6,7), (trp_peasant_woman,3,3)]),
("spy", "Lone Rider", icon_generic_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy,1,1)]),
("spy_evil", "Lone Rider", icon_generic_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy_evil,1,1)]),
("ents", "Ents",icon_ent|pf_default_behavior|pf_hide_defenders,0,fac_neutral,soldier_personality,[(trp_ent,5,8)]),
("gandalf", "Lone Rider",icon_gandalf|pf_default_behavior|pf_quest_party|pf_hide_defenders,0,fac_neutral,merchant_personality,[(trp_gandalf,1,1)]),
("nazgul" , "Lone Rider", icon_nazgul|pf_default_behavior|pf_quest_party|pf_hide_defenders,0,fac_neutral,merchant_personality,[(trp_nazgul,1,1)]),

#TLD Scouts
#MV: in general, average strength should be 30-60 (except Beornings who have scouts only)
("gondor_scouts"      ,"Gondorian Scouts",icon_footman_gondor|carries_goods(1)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_c2_gon_squire,1,2),(trp_a3_gon_bowman,2,5),(trp_i3_gon_footman,1,3),(trp_i2_gon_watchman,2,5)]), #11-25 weak scouts (Gondor spawns a lot of them)
("blackroot_auxila" ,"Blackroot Auxilia",icon_ithilien_ranger|carries_goods(1)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_a3_blackroot_archer,1,1),(trp_i2_blackroot_footman,2,4),(trp_a2_blackroot_bowman,2,4),(trp_a1_blackroot_hunter,3,6)]), #32-71
("lamedon_auxila"  ,"Lamedon Auxilia"   ,icon_footman_lamedon|carries_goods(1)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_i4_lam_warrior,1,1),(trp_i3_lam_veteran,3,6),(trp_i2_lam_footman,4,8)]), #31-71
("lossarnach_auxila","Lossarnach Auxilia",icon_lossarnach_axeman_icon|carries_goods(1)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_i4_loss_heavy_axeman,1,1),(trp_i3_loss_vet_axeman,1,3),(trp_i2_loss_axeman,2,4),(trp_i1_loss_woodsman,4,8)]), #25-71
("pinnath_gelin_auxila","Pinnath Gelin Auxilia",icon_footman_pinnath|carries_goods(1)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_c2_pinnath_rider,2,4),(trp_a2_pinnath_bowman,2,4),(trp_i1_pinnath_plainsman,3,6)]), #30-69
("ranger_scouts"       ,"Ranger Scouts" ,icon_ithilien_ranger|carries_goods(0)|pf_show_faction,0,fac_gondor,scout_personality,[(trp_a5_ithilien_vet_ranger,1,2),(trp_a4_ithilien_ranger,2,4)]), #43-102 more punch for rangers, elites operating in enemy territory

("rohan_scouts"    ,"Rohirrim Scouts"      ,icon_knight_rohan |carries_goods(1)|pf_show_faction,0,fac_rohan   ,scout_personality,[(trp_c3_rider_of_rohan,2,3),(trp_ac3_skirmisher_of_rohan,3,5),(trp_c2_squire_of_rohan,1,3)]), #36-64 rohan good at scouting
("lorien_scouts"   ,"Lothlorien Scouts"    ,icon_lorien_elf_a |carries_goods(1)|pf_show_faction,0,fac_lorien  ,scout_personality,[(trp_i4_lorien_gal_inf,1,2),(trp_a2_lorien_warden,3,4),(trp_a1_lorien_scout,3,4)]), #31-62
("woodelf_scouts"  ,"Mirkwood Elven Scouts",icon_mirkwood_elf |carries_goods(1)|pf_show_faction,0,fac_woodelf ,scout_personality,[(trp_a5_greenwood_master_archer,1,1),(trp_a2_greenwood_veteran_scout,1,5),(trp_a1_greenwood_scout,2,5)]), #37-65
("imladris_scouts","Dunedain Scouts",icon_ithilien_ranger|carries_goods(1)|pf_show_faction,0,fac_imladris,scout_personality,[(trp_a5_arnor_master_ranger,1,1),(trp_a2_arnor_vet_scout,1,3),(trp_a1_arnor_scout,2,5)]), #37-65
("dale_scouts"     ,"Dale Scouts"          ,icon_generic_knight  |carries_goods(2)|pf_show_faction,0,fac_dale    ,scout_personality,[(trp_i4_dale_sergeant,1,1),(trp_i2_dale_man_at_arms,2,6),(trp_i1_dale_militia,4,8)]), #25-49 weak
("esgaroth_scouts" ,"Esgaroth Scouts"    ,icon_ithilien_ranger|carries_goods(2)|pf_show_faction,0,fac_dale    ,scout_personality,[(trp_a5_barding_bowman,1,1),(trp_a4_dale_archer,1,3),(trp_a2_dale_scout,4,6)]), #41-67 stronger than dale
("dwarf_scouts"    ,"Dwarven Lookouts"     ,icon_dwarf        |carries_goods(2)|pf_show_faction,0,fac_dwarf   ,scout_personality,[(trp_a4_dwarf_bowman,1,1),(trp_i3_dwarf_hardened_warrior,1,3),(trp_a2_dwarf_lookout,4,6)]), #41-63
("beorn_scouts"    ,"Beorning Scouts"      ,icon_axeman       |carries_goods(1)|pf_show_faction,0,fac_beorn   ,scout_personality,[(trp_i4_beorning_carrock_fighter,1,1),(trp_i3_beorning_carrock_lookout,3,5),(trp_i2_beorning_warrior,2,4)]), #48-73 stronger, no raiders/patrols
("woodmen_scouts"  ,"Woodmen Scouts"       ,icon_axeman       |carries_goods(1)|pf_show_faction,0,fac_beorn   ,scout_personality,[(trp_a5_woodmen_night_stalker,1,1),(trp_a3_woodmen_scout,2,4),(trp_i3_woodmen_skilled_forester,2,4)]), #46-65

("mordor_scouts"    ,"Mordor Scouts"       ,icon_orc             |carries_goods(1)|pf_show_faction,0,fac_mordor  ,scout_personality,[(trp_a4_mordor_fell_orc_archer,1,1),(trp_i3_mordor_large_orc,1,3),(trp_a2_mordor_orc_archer,2,5),(trp_i2_mordor_orc,2,6)]), #29-66
("morgul_scouts"    ,"Morgul Scouts"       ,icon_orc             |carries_goods(1)|pf_show_faction,0,fac_mordor  ,scout_personality,[(trp_a4_mordor_fell_orc_archer,1,1),(trp_i4_mordor_fell_morgul_orc,1,2),(trp_a2_mordor_orc_archer,2,5),(trp_i2_mordor_morgul_orc,3,5)]), #29-66
("isengard_scouts"  ,"Isengard Scouts"     ,icon_orc_isengard    |carries_goods(1)|pf_show_faction,0,fac_isengard,scout_personality,[(trp_a4_isen_fighting_uruk_tracker,1,1),(trp_a3_isen_large_uruk_tracker,2,6),(trp_a2_isen_uruk_tracker,3,7)]), #33-73
("isengard_scouts_warg","Isengard Warg Riders",icon_wargrider_run|carries_goods(1)|pf_show_faction,0,fac_isengard,scout_personality,[(trp_ac4_isen_white_hand_rider,1,1),(trp_ac3_isen_warg_rider,3,6),(trp_ac2_isen_wolf_rider,3,6)]), #32-56 fast but weaker
("harad_scouts"     ,"Haradrim Scouts"     ,icon_harad_horseman  |carries_goods(1)|pf_show_faction,0,fac_harad   ,scout_personality,[(trp_ac4_harondor_horse_archer,1,1),(trp_ac3_harondor_skirmisher,1,3),(trp_a3_harad_hunter,0,4),(trp_c2_harondor_scout,4,8)]), #32-66
("dunland_scouts"   ,"Dunlending Scouts"   ,icon_dunlander       |carries_goods(1)|pf_show_faction,0,fac_dunland ,scout_personality,[(trp_ac4_dun_crebain_rider,4,8)]), #20-40 fast weaklings
("umbar_scouts"     ,"Corsair Scouts"      ,icon_umbar_corsair   |carries_goods(1)|pf_show_faction,0,fac_umbar   ,scout_personality,[(trp_i4_corsair_raider,1,2),(trp_a3_corsair_marksman,1,3),(trp_i2_corsair_warrior,2,4),(trp_a2_corsair_marine,3,8)]), #26-63
("khand_scouts"     ,"Easterling Scouts"   ,icon_cataphract      |carries_goods(1)|pf_show_faction,0,fac_khand   ,scout_personality,[(trp_ac4_khand_vet_skirmisher,1,3),(trp_ac3_khand_skirmisher,2,4),(trp_c3_khand_horseman,2,4),(trp_c2_khand_pony_rider,3,6)]), #33-74 fast and capable
("moria_scouts"     ,"Moria Scouts"        ,icon_orc             |carries_goods(1)|pf_show_faction,0,fac_moria   ,scout_personality,[(trp_c5_moria_clan_rider,1,1),(trp_c4_moria_warg_rider,2,5),(trp_c3_moria_wolf_rider,3,6),(trp_a3_moria_large_goblin_archer,0,4),(trp_a2_moria_goblin_archer,0,5)]), #35-85 can be strong, but archers slow them down (and they fight against elves)
("guldur_scouts"    ,"Dol Guldur Scouts"   ,icon_orc             |carries_goods(1)|pf_show_faction,0,fac_guldur  ,scout_personality,[(trp_a4_guldur_fell_orc_tracker,2,5),(trp_a3_guldur_large_orc_tracker,5,8),(trp_a2_guldur_orc_tracker,5,7)]), #39-73 numerous and strong for orcs
("gundabad_scouts","Gundabad Scouts"	,icon_wargrider_run		 |carries_goods(1)|pf_show_faction,0,fac_gundabad,scout_personality,[(trp_c5_gunda_clan_rider,1,1),(trp_ca4_gunda_skirmisher,2,4),(trp_c3_gunda_goblin_rider,4,8)]), #31-54 fast
("rhun_scouts"      ,"Rhun Scouts"      ,icon_easterling_horseman|carries_goods(1)|pf_show_faction,0,fac_rhun    ,scout_personality,[(trp_c3_rhun_outrider,2,3),(trp_ac3_rhun_horse_archer,1,3),(trp_c3_rhun_swift_horseman,3,6),(trp_ac2_rhun_horse_scout,5,8)]), #41-76 fast and very capable
 
####TLD Raiders
#MV: in general, average strength should be 80-160, good sides weaker, evil stronger (foraging vs. raiding)
("gondor_raiders"  ,"Gondor Foragers"    ,icon_knight_gondor|carries_goods(1)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_c3_gon_vet_squire,1,1),(trp_i3_gon_footman,6,12),(trp_a3_gon_bowman,6,12)]), #78-150
("rohan_raiders"   ,"Rohirrim Foragers"  ,icon_knight_rohan |carries_goods(1)|pf_show_faction,0,fac_rohan   ,soldier_personality,[(trp_c5_elite_rider_of_rohan,1,1),(trp_c3_rider_of_rohan,3,8),(trp_ac3_skirmisher_of_rohan,3,8),(trp_c2_squire_of_rohan,5,10)]), #72-152
("imladris_raiders","Rivendell Foragers" ,icon_knight_rivendell|carries_goods(2)|pf_show_faction,0,fac_imladris,soldier_personality,[(trp_ac6_riv_knight,1,1),(trp_ac5_riv_rider,2,5),(trp_i3_riv_swordbearer,6,12)]), #97-194 # less but stronger troops, cavalry
("lorien_raiders"  ,"Lothlorien Foragers",icon_lorien_elf_a |carries_goods(2)|pf_show_faction,0,fac_lorien  ,soldier_personality,[(trp_i4_lorien_gal_inf,1,1),(trp_a3_lorien_vet_warden,7,15),(trp_a2_lorien_archer,6,12)]), #71-152
("woodelf_raiders" ,"Mirkwood Foragers"  ,icon_mirkwood_elf |carries_goods(2)|pf_show_faction,0,fac_woodelf ,soldier_personality,[(trp_i4_greenwood_elite_infantry,1,1),(trp_i3_greenwood_vet_infantry,4,10),(trp_a3_greenwood_archer,5,10)]), #73-150
("dale_raiders"    ,"Dale Foragers"      ,icon_generic_knight  |carries_goods(2)|pf_show_faction,0,fac_dale    ,soldier_personality,[(trp_ac5_rhovanion_marchwarden,1,1),(trp_c2_rhovanion_retainer,4,10),(trp_i2_dale_man_at_arms,4,10),(trp_a2_dale_scout,4,12)]), #64-144
("dwarf_raiders"   ,"Dwarven Foragers"   ,icon_dwarf        |carries_goods(2)|pf_show_faction,0,fac_dwarf   ,soldier_personality,[(trp_i5_dwarf_expert_axeman,1,1),(trp_i3_dwarf_hardened_warrior,4,12),(trp_a2_dwarf_lookout,5,15)]), #66-162
("ranger_raiders"  ,"Ranger Raiders"   ,icon_ithilien_ranger|carries_goods(1)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_a6_ithilien_master_ranger,1,3),(trp_a5_ithilien_vet_ranger,5,8),(trp_a4_ithilien_ranger,5,10)]), #118-211 real raiders have more punch #InVain: 180-350 can attack Mordor supply trains
#("beorning_raiders","Beorning Foragers" ,icon_axeman  |carries_goods(1),0,fac_beorn   ,soldier_personality,[(trp_blank,10,15),(trp_blank,10,15),(trp_blank,1,1)]),

("morgul_raiders"  ,"Morgul Raiders"    ,icon_orc           |carries_goods(1)|pf_show_faction,0,fac_mordor  ,soldier_personality,[(trp_i4_mordor_fell_morgul_orc,1,1),(trp_i2_mordor_morgul_orc,15,30),(trp_a2_mordor_orc_archer,15,30)]), #98-188 better raiders
("mordor_raiders"  ,"Mordor Raiders"    ,icon_orc           |carries_goods(1)|pf_show_faction,0,fac_mordor  ,soldier_personality,[(trp_i4_mordor_fell_orc,1,1),(trp_i2_mordor_orc,13,26),(trp_a2_mordor_orc_archer,13,26)]), #86-164
("isengard_raiders","Isengard Raiders"  ,icon_uruk_isengard |carries_goods(1)|pf_show_faction,0,fac_isengard,soldier_personality,[(trp_i5_isen_fighting_uruk_champion,1,1),(trp_i3_isen_large_uruk,3,8),(trp_a3_isen_large_uruk_tracker,8,13),(trp_i1_isen_uruk_snaga,8,13)]), #98-168
("dunland_raiders","Dunlending Raiders",icon_dunland_captain|carries_goods(2)|pf_show_faction,0,fac_dunland ,soldier_personality,[(trp_i5_dun_wolf_guard,1,1),(trp_i4_dun_wolf_warrior,2,4),(trp_i3_dun_vet_warrior,4,8),(trp_i2_dun_warrior,8,16)]), #90-164
("harad_raiders"   ,"Haradrim Raiders"  ,icon_harad_horseman|carries_goods(2)|pf_show_faction,0,fac_harad   ,soldier_personality,[(trp_i5_harad_tiger_guard,1,1),(trp_a3_harad_hunter,10,20),(trp_i1_harad_levy,11,20)]), #98-176
("khand_raiders"   ,"Khand Raiders"     ,icon_cataphract    |carries_goods(2)|pf_show_faction,0,fac_khand   ,soldier_personality,[(trp_c5_khand_kataphrakt,1,1),(trp_c2_khand_pony_rider,5,10),(trp_c4_khand_heavy_horseman,5,15)]), #81-191
("umbar_raiders"   ,"Umbar Raiders"     ,icon_umbar_corsair |carries_goods(2)|pf_show_faction,0,fac_umbar   ,soldier_personality,[(trp_i5_corsair_night_raider,1,4),(trp_i4_corsair_raider,3,6),(trp_i3_corsair_swordsman,3,6),(trp_i4_corsair_veteran_swordsman,3,6),(trp_i3_corsair_spearman,3,6),(trp_i2_corsair_warrior,6,15)]), #100-196 good at it
("moria_raiders"   ,"Moria Raiders"     ,icon_orc           |carries_goods(2)|pf_show_faction,0,fac_moria   ,soldier_personality,[(trp_i5_moria_orc_chieftain,1,3),(trp_a3_moria_large_goblin_archer,3,9),(trp_i3_moria_large_goblin,5,15),(trp_a2_moria_goblin_archer,8,16)]), #72-176
("guldur_raiders"  ,"Dol Guldur Raiders",icon_orc_tribal    |carries_goods(2)|pf_show_faction,0,fac_guldur  ,soldier_personality,[(trp_a4_guldur_fell_orc_tracker,1,1),(trp_i3_mordor_large_orc,4,10),(trp_i2_mordor_orc,8,16),(trp_a2_guldur_orc_tracker,8,16),(trp_i1_guldur_orc_snaga,15,30)]), #91-184
("gundabad_raiders","Gundabad Raiders"  ,icon_orc_tribal    |carries_goods(2)|pf_show_faction,0,fac_gundabad,soldier_personality,[(trp_c5_gunda_clan_rider,1,3),(trp_ca4_gunda_skirmisher,6,12),(trp_c4_gunda_warg_rider,6,12),(trp_i2_gunda_orc,18,32),(trp_gunda_troll,1,2)]), #128-234 was 93-163
("rhun_raiders"    ,"Rhun Raiders"      ,icon_easterling_horseman|carries_goods(1)|pf_show_faction,0,fac_rhun    ,soldier_personality,[(trp_c5_rhun_warrider,1,3),(trp_ac3_rhun_horse_archer,8,16),(trp_c3_rhun_outrider,10,20)]), #124-264, was 100-184


####TLD Patrols
#MV: in general, average strength should be 300-600, Mordor and Isengard about 20% better than Gondor and Rohan
("gondor_patrol"  ,"Gondor Patrol"    ,icon_footman_gondor |carries_goods(2)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_c5_gon_vet_knight,1,1),(trp_a5_gon_vet_archer,3,6),(trp_i5_gon_vet_swordsman,3,6),(trp_a4_gon_archer,8,20),(trp_i4_gon_swordsman,8,20)]), #256-568
("rohan_patrol"   ,"Rohirrim Patrol"  ,icon_knight_rohan   |carries_goods(2)|pf_show_faction,0,fac_rohan   ,soldier_personality,[(trp_ac6_skirmisher_guard_of_rohan,1,1),(trp_ac5_elite_skirmisher_of_rohan,3,6),(trp_c4_lancer_of_rohan,3,6),(trp_ac4_veteran_skirmisher_of_rohan,6,14),(trp_ac3_skirmisher_of_rohan,6,14),(trp_c3_rider_of_rohan,8,20)]), #238-505 fast!
("imladris_patrol","Dunedain Patrol"  ,icon_knight_rivendell  |carries_goods(0)|pf_show_faction,0,fac_imladris,soldier_personality,[(trp_c5_arnor_knight,1,1),(trp_c4_arnor_horseman,4,10),(trp_i5_arnor_champion,3,5),(trp_i4_arnor_vet_swordsman,8,20),(trp_i3_arnor_swordsman,8,20)]), #252-554
("lorien_patrol"  ,"Lothlorien Patrol",icon_lorien_elf_b   |carries_goods(2)|pf_show_faction,0,fac_lorien  ,soldier_personality,[(trp_a6_lorien_grey_warden,1,1),(trp_a5_lorien_gal_royal_warden,3,6),(trp_a4_lorien_gal_warden,4,10),(trp_a4_lorien_gal_archer,8,16),(trp_a3_lorien_vet_warden,8,16),(trp_a3_lorien_vet_archer,10,20)]), #312-615
("woodelf_patrol" ,"Mirkwood Patrol"  ,icon_mirkwood_elf   |carries_goods(2)|pf_show_faction,0,fac_woodelf ,soldier_personality,[(trp_a6_greenwood_chosen_marksman,1,1),(trp_a5_greenwood_master_archer,3,6),(trp_a4_greenwood_veteran_archer,4,10),(trp_i4_greenwood_elite_infantry,4,10),(trp_i3_greenwood_vet_infantry,4,10),(trp_a3_greenwood_archer,8,16)]), #250-525
("dale_patrol"    ,"Dale Patrol"      ,icon_generic_knight    |carries_goods(2)|pf_show_faction,0,fac_dale    ,soldier_personality,[(trp_ac5_rhovanion_marchwarden,1,1),(trp_i5_dale_hearthman,4,8),(trp_i5_dale_bill_master,3,8),(trp_i4_dale_billman,4,10),(trp_a4_dale_archer,6,12),(trp_i2_dale_man_at_arms,6,12)]), #242-518
("esgaroth_patrol","Esgaroth Patrol"  ,icon_ithilien_ranger|carries_goods(2)|pf_show_faction,0,fac_dale    ,soldier_personality,[(trp_ac5_rhovanion_marchwarden,1,1),(trp_a5_barding_bowman,6,10),(trp_i4_dale_billman,4,10),(trp_a4_dale_archer,10,15),(trp_a2_dale_scout,6,12)]), #242-518
("dwarf_patrol"   ,"Dwarven Patrol"   ,icon_dwarf          |carries_goods(2)|pf_show_faction,0,fac_dwarf   ,soldier_personality,[(trp_i6_dwarf_longbeard_axeman,1,1),(trp_a4_dwarf_bowman,8,16),(trp_i4_dwarf_spearman,5,10),(trp_i4_dwarf_axeman,8,20),(trp_a2_dwarf_lookout,10,25)]), #257-542

("ranger_patrol"  ,"Ranger Patrol"    ,icon_ithilien_ranger|carries_goods(0)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_a6_ithilien_leader,1,1),(trp_a6_ithilien_master_ranger,5,9),(trp_a5_ithilien_vet_ranger,8,14),(trp_a4_ithilien_ranger,8,25)]), #299-603 #InVain 410-820 can attack lone hosts
("amroth_patrol" ,"Dol Amroth Patrol",icon_knight_dolamroth|carries_goods(2)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_c6_amroth_leader,1,1),(trp_c6_amroth_swan_knight,2,6),(trp_c4_amroth_knight,6,14),(trp_c3_amroth_vet_squire,8,20),(trp_c2_amroth_squire,16,30)]), #241-541
("pelargir_patrol","Pelargir Patrol"  ,icon_footman_gondor |carries_goods(2)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_i6_pel_leader,1,1),(trp_a3_pel_vet_marine,3,8),(trp_i3_pel_vet_infantry,3,8),(trp_a2_pel_marine,6,14),(trp_i2_pel_infantry,6,14)]), #229-533
("lossarnach_patrol","Lossarnach Patrol",icon_lossarnach_axeman_icon|carries_goods(2)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_i6_loss_leader,1,1),(trp_i5_loss_axemaster,3,8),(trp_i4_loss_heavy_axeman,4,10),(trp_a4_gon_archer,8,20),(trp_i2_loss_axeman,8,20)]), #213-503
("brv_patrol"     ,"Blackroot Patrol" ,icon_ithilien_ranger|carries_goods(2)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_a5_blackroot_shadow_hunter,1,1),(trp_a3_blackroot_archer,4,8),(trp_a2_blackroot_bowman,6,12),(trp_i2_blackroot_footman,8,16),(trp_a1_blackroot_hunter,10,20)]), #255-485
("pinnath_patrol" ,"Pinnath Patrol"   ,icon_footman_pinnath|carries_goods(2)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_c6_pinnath_leader,1,1),(trp_a3_pinnath_archer,3,6),(trp_c3_pinnath_knight,3,6),(trp_a2_pinnath_bowman,6,16),(trp_c2_pinnath_rider,8,20)]), #247-541
("lamedon_patrol" ,"Lamedon Patrol"  ,icon_lamedon_horseman|carries_goods(2)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_c6_lam_leader,1,1),(trp_c5_lam_knight,6,14),(trp_i5_lam_champion,3,6),(trp_i4_lam_warrior,8,20),(trp_i3_lam_veteran,10,24)]), #253-541 #InVain 270-600, added more cavalry

# Used as patrols, except Dale 
("mordor_war_party"  ,"Mordor_War_Party"  ,icon_uruk_x4          |carries_goods(3)|pf_show_faction,0,fac_mordor  ,soldier_personality,[(trp_i5_mordor_uruk_standard_bearer,1,2),(trp_i3_mordor_large_uruk,10,22),(trp_i2_mordor_uruk,16,36),(trp_i2_mordor_orc,60,80),(trp_a2_mordor_orc_archer,40,60),(trp_mordor_olog_hai,0,3)]), #310-658 #InVain 356-812 (new formula) added more fodder orcs to make fight more epic, but not so much harder.
("isengard_war_party","Isengard_War_Party",icon_wargrider_walk_x4|carries_goods(3)|pf_show_faction,0,fac_isengard,soldier_personality,[(trp_i5_isen_uruk_standard_bearer,1,2),(trp_i6_isen_uruk_berserker,3,6),(trp_i5_isen_fighting_uruk_champion,3,6),(trp_a4_isen_fighting_uruk_tracker,15,25),(trp_ac2_isen_wolf_rider,5,10),(trp_isen_armored_troll,0,3)]), #275-550
("harad_war_party"   ,"Harad_War_Party"   ,icon_harad_horseman_x3|carries_goods(3)|pf_show_faction,0,fac_harad   ,soldier_personality,[(trp_i5_harad_tiger_guard,2,4),(trp_c5_harondor_serpent_knight,2,4),(trp_ac5_harondor_black_snake,2,4),(trp_a4_harad_archer,8,16),(trp_c3_harondor_rider,10,20),(trp_i1_harad_levy,20,40)]), #268-536
("dunland_war_party" ,"Dunlending_Warband",icon_dunlander_x3     |carries_goods(3)|pf_show_faction,0,fac_dunland ,soldier_personality,[(trp_i5_dun_wolf_guard,2,4),(trp_i4_dun_vet_pikeman,6,12),(trp_i2_dun_warrior,12,24),(trp_ac4_dun_crebain_rider,10,20),(trp_i1_dun_wildman,20,50)]), #214-448 weak
("khand_war_party"   ,"Variag_War_Party"   ,icon_cataphract_x3   |carries_goods(3)|pf_show_faction,0,fac_khand   ,soldier_personality,[(trp_i5_khand_war_master,2,4),(trp_c5_khand_kataphrakt,2,4),(trp_i4_khand_vet_warrior,5,10),(trp_i3_khand_warrior,8,16),(trp_c2_khand_pony_rider,10,20),(trp_i2_khand_pit_dog,20,40)]), #277-554
#("corsair_war_party" ,"Corsair_War_Party" ,icon_umbar_corsair_x3 |carries_goods(3),0,fac_umbar   ,soldier_personality,[(trp_i5_corsair_master_pikeman   ,20,50),(trp_i4_corsair_veteran_swordsman,15,30),(trp_i5_corsair_master_spearman,13,36),(trp_a5_corsair_master_marksman,5,30),(trp_i4_corsair_veteran_swordsman,5,40),(trp_a5_corsair_master_assassin,5,20)]),
("moria_war_party"   ,"Moria_War_Party"   ,icon_orc_tribal_x4    |carries_goods(3)|pf_show_faction,0,fac_moria   ,soldier_personality,[(trp_i4_moria_fell_goblin,5,10),(trp_a3_moria_large_goblin_archer,10,20),(trp_i3_moria_large_goblin,12,24),(trp_i2_moria_goblin,15,30),(trp_i1_moria_snaga,20,50),(trp_moria_troll,1,2)]), #262-534
#Northern war
("guldur_war_party"  ,"Dol_Guldur_War_Party"  ,icon_uruk_x4          |carries_goods(3)|pf_show_faction,0,fac_mordor  ,soldier_personality,[(trp_i5_mordor_uruk_standard_bearer,1,2),(trp_i3_mordor_large_uruk,10,22),(trp_i2_mordor_uruk,16,36),(trp_i2_mordor_orc,60,80),(trp_a2_guldur_orc_tracker,40,60),(trp_mordor_olog_hai,0,3)]), #310-658 #InVain 356-812 (new formula) added more fodder orcs to make fight more epic, but not so much harder.
#("dwarf_war_party" ,"Dwarven_War_Party",icon_dwarf_x3              |carries_goods(3),0,fac_dwarf  ,soldier_personality,[(trp_i1_dwarf_apprentice      ,8,13),(trp_i6_iron_hills_grors_guard,8,20),(trp_i2_dwarf_warrior,8,16),(trp_i5_dwarf_expert_axeman,5,20),(trp_a2_dwarf_lookout,4,15),(trp_a4_dwarf_bowman,4,15)]),
("rhun_war_party"  ,"Rhun_War_Party"   ,icon_easterling_horseman_x3|carries_goods(3)|pf_show_faction,0,fac_rhun   ,soldier_personality,[(trp_c6_rhun_warlord,2,4),(trp_c5_rhun_warrider,5,10),(trp_c4_rhun_veteran_swift_horseman,8,16),(trp_ac4_rhun_veteran_horse_archer,8,16),(trp_i2_rhun_tribal_warrior,12,24),(trp_i1_rhun_tribesman,18,36)]), #358-716 was 260-552

####TLD Companies (only Gondorian used, as a MT patrol)
("gondor_company" ,"Minas Tirith Patrol",icon_knight_gondor |carries_goods(4)|pf_show_faction,0,fac_gondor  ,soldier_personality,[(trp_captain_of_gondor,1,1),(trp_c5_gon_vet_knight,2,4),(trp_c4_gon_knight,8,16),(trp_i5_gon_vet_swordsman,10,20),(trp_a5_gon_vet_archer,10,20),(trp_i5_gon_vet_spearman,10,20)]), #573-1121 elite, rare, overpowered #InVain 754-1474 (new formula) added a few more knights
("rohan_company"   ,"Rohan Company"     ,icon_knight_rohan        ,0,fac_rohan   ,soldier_personality,[(trp_c5_elite_rider_of_rohan,25,25),(trp_ac5_elite_skirmisher_of_rohan,25,25),(trp_i5_elite_footman_of_rohan,25,25),(trp_c6_rider_guard_of_rohan,12,12),(trp_ac6_skirmisher_guard_of_rohan,12,12),(trp_captain_of_rohan,1,1)]),
("imladris_company","Rivendell Company" ,icon_rivendell_elf       ,0,fac_imladris,soldier_personality,[(trp_i3_riv_swordbearer,20,33),(trp_i4_riv_vet_swordbearer,20,33),(trp_i5_riv_swordmaster,20,33),(trp_i6_riv_champion,3,6),(trp_elf_captain_of_rivendell,1,1)]),
("lorien_company"  ,"Lothlorien Company",icon_lorien_elf_b        ,0,fac_lorien  ,soldier_personality,[(trp_a3_lorien_vet_archer,30,30),(trp_a4_lorien_gal_archer,30,30),(trp_i4_lorien_gal_inf,30,30),(trp_i5_lorien_gal_royal_inf,5,5),(trp_a5_lorien_gal_royal_archer,5,5),(trp_elf_captain_of_lothlorien,1,1)]),
("woodelf_company" ,"Mirkwood Company"  ,icon_mirkwood_elf        ,0,fac_woodelf ,soldier_personality,[(trp_i3_greenwood_vet_infantry,21,22),(trp_i3_greenwood_vet_infantry,21,22),(trp_a4_greenwood_veteran_archer,21,22),(trp_a5_greenwood_master_archer,21,22),(trp_a6_greenwood_chosen_marksman,8,12)]),
("dale_company"    ,"Dale Company"      ,icon_generic_knight         ,0,fac_dale    ,soldier_personality,[(trp_a4_dale_archer,20,20),(trp_a5_barding_bowman,20,20),(trp_i4_dale_sergeant,20,20),(trp_i5_dale_bill_master,20,20),(trp_ac5_rhovanion_marchwarden,20,20)]),
("dwarf_company"   ,"Dwarven Company"   ,icon_dwarf               ,0,fac_dwarf   ,soldier_personality,[(trp_i3_dwarf_hardened_warrior,25,25),(trp_a2_dwarf_lookout,25,25),(trp_i2_dwarf_warrior,20,20),(trp_i5_dwarf_expert_axeman,20,20),(trp_a4_dwarf_bowman,10,10)]),

####TLD Elite Companies (not used)
("gondor_elite_company"  ,"Gondor Elite Company"    ,icon_knight_gondo_trot_x3,0,fac_gondor  ,soldier_personality,[(trp_i6_gon_tower_spearman,15,30),(trp_c6_gon_tower_knight,15,30),(trp_a6_gon_tower_archer,15,30),(trp_i6_gon_tower_swordsman,15,30),(trp_captain_of_gondor,1,1)]),
("rohan_elite_company"   ,"Rohan Elite Company"     ,icon_knight_rohan_x3     ,0,fac_rohan   ,soldier_personality,[(trp_c6_rider_guard_of_rohan        ,10,20),(trp_ac6_skirmisher_guard_of_rohan,10,20),(trp_i6_footman_guard_of_rohan,10,20),(trp_i6_warden_of_methuseld,10,20),(trp_i6_frealaf_raider,10,20),(trp_captain_of_rohan,1,1)]),
("imladris_elite_company","Rivendell Elite Company" ,icon_knight_rivendell    ,0,fac_imladris,soldier_personality,[(trp_i6_riv_champion   ,25,50),(trp_ac6_riv_knight,25,50),(trp_elf_captain_of_rivendell,1,1)]),
("lorien_elite_company"  ,"Lothlorien Elite Company",icon_lorien_elf_b_x3     ,0,fac_lorien  ,soldier_personality,[(trp_galadhrim_royal_marksman   ,13,25),(trp_a5_lorien_gal_royal_archer,13,25),(trp_a6_lorien_grey_warden,13,25),(trp_i5_lorien_gal_royal_inf,13,25),(trp_noldorin_commander,1,1)]),
("woodelf_elite_company" ,"Mirkwood Elite Company"  ,icon_mirkwood_elf_x3     ,0,fac_woodelf ,soldier_personality,[(trp_i4_greenwood_elite_infantry   ,20,40),(trp_a6_greenwood_chosen_marksman,20,40),(trp_elf_captain_of_mirkwood,0,0)]),
("dale_elite_company"    ,"Dale Elite Company"      ,icon_generic_knight         ,0,fac_dale    ,soldier_personality,[(trp_i5_dale_bill_master           ,13,25),(trp_i5_dale_hearthman,13,25),(trp_ac5_rhovanion_marchwarden,13,25),(trp_a5_barding_bowman,13,25),(trp_knight_5_1,13,25)]),
("dwarf_elite_company"   ,"Dwarven Elite Company"   ,icon_dwarf_x3            ,0,fac_dwarf   ,soldier_personality,[(trp_i2_dwarf_warrior            ,18,34),(trp_i5_dwarf_expert_axeman,18,34),(trp_a4_dwarf_bowman,18,34),(trp_knight_5_6,1,1)]),

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
("gondor_caravan"  ,"Gondor Caravan"    ,icon_supply_gondor|carries_goods(10)|pf_show_faction,0,fac_gondor  ,prisoner_train_personality,[(trp_c4_gon_knight,1,4),(trp_c2_gon_squire,4,10),(trp_i4_gon_swordsman,4,10),(trp_i4_gon_spearman,4,10),(trp_a4_gon_archer,7,14),(trp_i2_gon_watchman,30,50)]), # strength 280-582
("rohan_caravan"   ,"Rohan Caravan"     ,icon_supply_rohan |carries_goods(10)|pf_show_faction,0,fac_rohan   ,prisoner_train_personality,[(trp_c4_veteran_rider_of_rohan,1,4),(trp_c2_squire_of_rohan,4,10),(trp_ac4_veteran_skirmisher_of_rohan,7,14),(trp_i4_veteran_footman_of_rohan,6,14),(trp_i2_guardsman_of_rohan,26,42)]), # strength 246-496
("imladris_caravan","Rivendell Caravan" ,icon_mule         |carries_goods(10)|pf_show_faction,0,fac_imladris,prisoner_train_personality,[(trp_ac5_riv_rider,1,4),(trp_a4_riv_vet_archer,4,10),(trp_a3_riv_archer,12,24),(trp_a2_riv_vet_scout,10,16),(trp_i3_riv_swordbearer,14,24)]), # strength 254-508
("lorien_caravan"  ,"Lothlorien Caravan",icon_mule         |carries_goods(10)|pf_show_faction,0,fac_lorien  ,prisoner_train_personality,[(trp_i4_lorien_gal_inf,2,6),(trp_a4_lorien_gal_archer,4,10),(trp_a3_lorien_vet_warden,14,30),(trp_i3_lorien_inf,12,18),(trp_a3_lorien_vet_archer,16,28)]), # strength 298-600
("woodelf_caravan" ,"Mirkwood Caravan"  ,icon_mule         |carries_goods(10)|pf_show_faction,0,fac_woodelf ,prisoner_train_personality,[(trp_a4_greenwood_vet_sentinel,1,4),(trp_i4_greenwood_elite_infantry,4,10),(trp_a3_greenwood_sentinel,12,24),(trp_a2_greenwood_veteran_scout,10,16),(trp_i2_greenwood_infantry,14,24)]), # strength 254-508
("dale_caravan"    ,"Dale Caravan"      ,icon_mule         |carries_goods(10)|pf_show_faction,0,fac_dale    ,prisoner_train_personality,[(trp_c4_rhovanion_rider,1,5),(trp_a4_dale_archer,5,10),(trp_c3_rhovanion_auxilia,4,8),(trp_i3_dale_swordsman,8,16),(trp_a2_dale_scout,18,30)]), # strength 198-399
("dwarf_caravan"   ,"Dwarven Caravan"   ,icon_mule         |carries_goods(10)|pf_show_faction,0,fac_dwarf   ,prisoner_train_personality,[(trp_i4_dwarf_axeman,2,6),(trp_a4_dwarf_bowman,2,4),(trp_i3_dwarf_hardened_warrior,12,24),(trp_a2_dwarf_lookout,16,24),(trp_i2_dwarf_warrior,20,40)]), # strength 264-514

("mordor_caravan"  ,"Mordor Supply Train"  ,icon_supply_mordor  |carries_goods(10)|pf_show_faction,0,fac_mordor  ,prisoner_train_personality, [(trp_i3_mordor_large_uruk, 4, 12), (trp_a3_mordor_large_orc_archer, 8, 18), (trp_i3_mordor_large_orc, 8, 18), (trp_a2_mordor_orc_archer, 14, 22), (trp_i2_mordor_orc, 18, 30)]), # strength 200-408
("isengard_caravan","Isengard Supply Train",icon_supply_isengard|carries_goods(10)|pf_show_faction,0,fac_isengard,prisoner_train_personality, [(trp_ac3_isen_warg_rider, 3, 8), (trp_i3_isen_large_uruk, 6, 16), (trp_i2_isen_uruk, 6, 10), (trp_a2_isen_uruk_tracker, 6, 10), (trp_i2_isen_orc, 20, 40)]), # strength 159-336
("gunda_caravan"   ,"Gundabad Supply Train",icon_supply_isengard|carries_goods(10)|pf_show_faction,0,fac_gundabad,prisoner_train_personality, [(trp_c5_gunda_clan_rider, 1, 2), (trp_ca4_gunda_skirmisher, 6, 16), (trp_i4_gunda_orc_berserker, 6, 10), (trp_i2_gunda_orc, 20, 30)]),

####TLD Prisoner Trains
# MV guidelines:
# - make evil prisoner trains stronger than good (allegedly evil guys care more about guarding slaves/prisoners)
# - as for caravans: favor guard and militia units, no elite troops should be tied down to escort duty (tiers 1-3)
# - prisoner trains should be about half the size of caravans, but slow and interceptable, so give them more slow tier 1 troops and no/less cavalry
# - aim for strength 150-250
("gondor_p_train"  ,"Gondor Prisoner Train"    ,icon_supply_gondor|pf_show_faction,0,fac_gondor  ,prisoner_train_personality,[(trp_i3_gon_footman,1,2), (trp_a3_gon_bowman,4,6), (trp_i2_gon_watchman,15,25), (trp_i1_gon_levy,30,45)]), # strength 150-238
("rohan_p_train"   ,"Rohan Prisoner Train"     ,icon_supply_rohan |pf_show_faction,0,fac_rohan   ,prisoner_train_personality,[(trp_i3_footman_of_rohan,2,4), (trp_ac3_skirmisher_of_rohan,4,6), (trp_c2_squire_of_rohan,4,6), (trp_i2_guardsman_of_rohan,8,12), (trp_i1_rohan_youth,24,30)]), # strength 132-192
("imladris_p_train","Rivendell Prisoner Train" ,icon_mule         |pf_show_faction,0,fac_imladris,prisoner_train_personality,[(trp_i4_riv_vet_swordbearer,2,4), (trp_a3_riv_archer,2,4), (trp_i3_riv_swordbearer,6,10), (trp_a2_riv_vet_scout,6,8), (trp_a1_riv_scout,25,35)]), # strength 138-216
("lorien_p_train"  ,"Lothlorien Prisoner Train",icon_mule         |pf_show_faction,0,fac_lorien  ,prisoner_train_personality,[(trp_a3_lorien_vet_warden,6,10), (trp_a3_lorien_vet_archer,6,10), (trp_i3_lorien_inf,6,10), (trp_a2_lorien_archer,25,35)]), # strength 152-240
("woodelf_p_train" ,"Mirkwood Prisoner Train"  ,icon_mule         |pf_show_faction,0,fac_woodelf ,prisoner_train_personality,[(trp_a3_greenwood_sentinel,2,4), (trp_i3_greenwood_vet_infantry,2,4), (trp_i2_greenwood_infantry,6,10), (trp_a2_greenwood_veteran_scout,6,8), (trp_a1_greenwood_scout,25,35)]), # strength 138-216
("dale_p_train"    ,"Dale Prisoner Train"      ,icon_mule         |pf_show_faction,0,fac_dale    ,prisoner_train_personality,[(trp_c3_rhovanion_auxilia,1,2), (trp_i3_dale_swordsman,1,2), (trp_a3_dale_bowman,1,2), (trp_i2_dale_man_at_arms,4,6), (trp_a2_dale_scout,6,10), (trp_i1_dale_militia,21,25)]), # strength 100-150
("dwarf_p_train"   ,"Dwarven Prisoner Train"   ,icon_mule         |pf_show_faction,0,fac_dwarf   ,prisoner_train_personality,[(trp_i3_dwarf_hardened_warrior,2,4), (trp_a3_dwarf_scout,4,6), (trp_i2_dwarf_warrior,4,6), (trp_a2_dwarf_lookout,8,14), (trp_i1_dwarf_apprentice,25,35)]), # strength 140-220

("mordor_p_train"  ,"Mordor Prisoner Train"    ,icon_slaver_mordor  |carries_goods(2)|pf_show_faction,0,fac_mordor  , prisoner_train_personality, [(trp_i3_mordor_large_orc,6,8), (trp_a2_mordor_orc_archer,6,10), (trp_i2_mordor_orc,16,24), (trp_a2_mordor_orc_archer,16,24), (trp_i1_mordor_orc_snaga,40,60)]), # strength 196-294
("isengard_p_train","Isengard Prisoner Train"  ,icon_slaver_isengard|carries_goods(2)|pf_show_faction,0,fac_isengard, prisoner_train_personality, [(trp_ac3_isen_warg_rider,4,6), (trp_i3_isen_large_orc,10,14), (trp_i2_isen_orc,24,36), (trp_i1_isen_orc_snaga,40,60)]), # strength 182-268

("kingdom_hero_party","War Party",icon_player_horseman|pf_show_faction|pf_default_behavior,0,fac_commoners,soldier_personality,[]),

# Reinforcements

#MV: Guidelines:
# A: base tier 1 and 2 troops (7-14 total)
# B: tier 3 archers mixed with other tier 3 troops and tier 2 archers, troops more useful in sieges (5-10 total)
# C: tier 4 troop mix, mostly cavalry, troops more useful in field battles (4-8 total)
# Notes:
# - with reinforcements quantity counts more than quality, compared to normal non-upgradable party templates
# - balance between (sub)trees to get a desired mix of inv, arch, cav
# - towns get 60% A, 35% B, 5% C (more low level troops and archers); heroes get 50% A, 30% B, 20% C (more cavalry) - see script_cf_reinforce_party InVain: Garrisons now get 30/60/10
# - sort order: higher tier and mounted troops first

("gondor_reinf_d"    ,"_",0,0,fac_commoners,0,[(trp_c6_gon_tower_knight,1,2), (trp_a6_gon_tower_archer,2,4), (trp_i6_gon_tower_swordsman,1,2), (trp_i6_gon_tower_spearman,1,2),]), #MT garrison only

("gondor_reinf_a"    ,"_",0,0,fac_commoners,0,[(trp_i2_gon_watchman,3,6),(trp_i1_gon_levy,1,3),(trp_i3_gon_footman,1,2)]), #InVain: less commoners, less archers
("gondor_reinf_b"    ,"_",0,0,fac_commoners,0,[(trp_a3_gon_bowman,3,5),(trp_i3_gon_footman,2,4),(trp_i2_gon_watchman,2,4),(trp_c1_gon_nobleman,1,2),(trp_a4_gon_archer, 1,2)]), #T1 cav because it has a separate tree, InVain: More archers+ t4 archers (due to changed garrison reinforcements)
("gondor_reinf_c"    ,"_",0,0,fac_commoners,0,[(trp_i4_gon_spearman,2,3),(trp_i4_gon_swordsman,2,3),(trp_c3_gon_vet_squire,1,2),]), #InVain: Removed archers, hosts are more infantry-heavy
("pelargir_reinf_a"  ,"_",0,0,fac_commoners,0,[(trp_i1_pel_watchman,6,12),]), #no T1
("pelargir_reinf_b"  ,"_",0,0,fac_commoners,0,[(trp_a2_pel_marine,1,2),(trp_i2_pel_infantry,1,2),(trp_i1_pel_watchman,3,6),]), #no T3
("pelargir_reinf_c"  ,"_",0,0,fac_commoners,0,[(trp_a2_pel_marine,2,5),(trp_i2_pel_infantry,2,3),]),
("dol_amroth_reinf_a","_",0,0,fac_commoners,0,[(trp_c2_amroth_squire,2,4),(trp_i1_amroth_recruit,5,10),]),
("dol_amroth_reinf_b","_",0,0,fac_commoners,0,[(trp_c3_amroth_vet_squire,3,6),(trp_c2_amroth_squire,2,4),]),
("dol_amroth_reinf_c","_",0,0,fac_commoners,0,[(trp_c4_amroth_knight,4,8),]),
("lamedon_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_i2_lam_footman,2,4),(trp_i1_lam_clansman,5,10),]),
("lamedon_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_i3_lam_veteran,4,8),(trp_i2_lam_footman,1,2),]),
("lamedon_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_i4_lam_warrior,4,8),]),
("lossarnach_reinf_a","_",0,0,fac_commoners,0,[(trp_i2_loss_axeman,2,4),(trp_i1_loss_woodsman,5,10),]),
("lossarnach_reinf_b","_",0,0,fac_commoners,0,[(trp_i3_loss_vet_axeman,4,8),(trp_i2_loss_axeman,1,2),]),
("lossarnach_reinf_c","_",0,0,fac_commoners,0,[(trp_i4_loss_heavy_axeman,4,8),]),
("pinnath_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_i1_pinnath_plainsman,6,12),]), #no T1
("pinnath_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_a2_pinnath_bowman,1,2),(trp_c2_pinnath_rider,1,2),(trp_i1_pinnath_plainsman,3,6)]), #no T3
("pinnath_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_c2_pinnath_rider,2,4),(trp_a2_pinnath_bowman,2,4)]),
("ithilien_reinf_a"  ,"_",0,0,fac_commoners,0,[(trp_a4_ithilien_ranger,4,7),]), #since they begin at T4, halve them
("ithilien_reinf_b"  ,"_",0,0,fac_commoners,0,[(trp_a5_ithilien_vet_ranger,3,5),]),
("ithilien_reinf_c"  ,"_",0,0,fac_commoners,0,[(trp_a6_ithilien_master_ranger,2,4),]),
("blackroot_reinf_a" ,"_",0,0,fac_commoners,0,[(trp_a1_blackroot_hunter,6,12)]), #no T1
("blackroot_reinf_b" ,"_",0,0,fac_commoners,0,[(trp_i2_blackroot_footman,1,2),(trp_a2_blackroot_bowman,1,2),(trp_a1_blackroot_hunter,3,6),]), #no T3
("blackroot_reinf_c" ,"_",0,0,fac_commoners,0,[(trp_a2_blackroot_bowman,2,4),(trp_i2_blackroot_footman,2,4),]),
#rohan	
("rohan_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_c2_squire_of_rohan,2,4),(trp_i2_guardsman_of_rohan,1,2),(trp_i1_rohan_youth,3,6),]),
("rohan_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_c3_rider_of_rohan,2,4),(trp_ac3_skirmisher_of_rohan,1,2),(trp_i3_footman_of_rohan,3,5),(trp_ac4_veteran_skirmisher_of_rohan,1,2),]),
("rohan_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_c4_veteran_rider_of_rohan,2,3),(trp_c4_lancer_of_rohan,1,2),(trp_i4_veteran_footman_of_rohan,1,2),]),
#Isengard - two short trees (up to T4/T5), easier to upgrade, so lower tier reinforcements; also extra orcs (8-16, 7-13, 5-10)
("isengard_reinf_a","_",0,0,fac_commoners,0,[(trp_i1_isen_uruk_snaga,1,2),(trp_i1_isen_orc_snaga,2,5),(trp_a2_isen_uruk_tracker,1,2),(trp_i2_isen_uruk,1,2),(trp_i2_isen_orc,2,4),]), #two T1 #InVain: mixed a bit, see Mordor
("isengard_reinf_b","_",0,0,fac_commoners,0,[(trp_ac2_isen_wolf_rider,2,3),(trp_a2_isen_uruk_tracker,1,2),(trp_i2_isen_uruk,2,4),(trp_i2_isen_orc,2,4),(trp_a3_isen_large_uruk_tracker,1,3),(trp_i3_isen_large_orc,1,2),]), #more T2 troops #InVain: More archers, t3 archers+orcs
("isengard_reinf_c","_",0,0,fac_commoners,0,[(trp_ac3_isen_warg_rider,1,2),(trp_i3_isen_large_uruk,1,2),(trp_i3_isen_uruk_pikeman,1,2),(trp_i3_isen_large_orc,1,2),(trp_i3_isen_large_orc_despoiler,1,2),]), #more T3 troops
#Mordor - same as Isengard + Numenorean cavalry (8-16, 7-13, 5-10)
("mordor_reinf_a"  ,"_",0,0,fac_commoners,0,[(trp_i1_mordor_uruk_snaga,1,3),(trp_i1_mordor_orc_snaga,2,5),(trp_i2_mordor_uruk,1,2),(trp_i2_mordor_orc,2,4),]), #InVain: less t1, a few t2 = less orc archers for field armies
("mordor_reinf_b"  ,"_",0,0,fac_commoners,0,[(trp_a2_mordor_orc_archer,2,4),(trp_a3_mordor_large_orc_archer,2,4),(trp_i2_mordor_uruk,2,3),(trp_i2_mordor_orc,3,6),(trp_i3_mordor_large_orc,1,2),(trp_a4_mordor_fell_orc_archer,1,2)]), #InVain: More archers, t3+t4 archers, t3 orcs
("mordor_reinf_c"  ,"_",0,0,fac_commoners,0,[(trp_c3_mordor_warg_rider,1,2),(trp_i3_mordor_large_uruk,1,1),(trp_i3_mordor_uruk_slayer,0,1),(trp_i4_mordor_fell_orc,1,2),(trp_i4_mordor_fell_morgul_orc,1,2),]), #InVain: Removed t3 archers, add t4 Mordor + Morgul orcs
#Harad (7-14, 5-10, 4-8)
("harad_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_c2_harondor_scout,1,2),(trp_i2_far_harad_tribesman,1,2),(trp_i1_harad_levy,5,10),]),
("harad_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_ac3_harondor_skirmisher,1,2),(trp_a3_harad_hunter,2,4),(trp_i3_harad_infantry,1,2),(trp_i2_far_harad_tribesman,1,2),]),
("harad_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_ac4_harondor_horse_archer,1,2),(trp_c4_harondor_light_cavalry,1,2),(trp_i4_far_harad_champion,1,2),(trp_i4_harad_swordsman,1,1),(trp_i4_harad_spearman,0,2),(trp_ac5_camel_rider,1,2)]),
#Rhun
("rhun_reinf_a"    ,"_",0,0,fac_commoners,0,[(trp_c2_rhun_horseman,1,2),(trp_ac2_rhun_horse_scout,2,3),(trp_i1_rhun_tribesman,5,10),]),
("rhun_reinf_b"    ,"_",0,0,fac_commoners,0,[(trp_ac3_rhun_horse_archer,2,4),(trp_c3_rhun_outrider,1,2),(trp_i3_rhun_tribal_infantry,3,5),]),
("rhun_reinf_c"    ,"_",0,0,fac_commoners,0,[(trp_c4_rhun_noble_rider,2,4),(trp_c4_rhun_veteran_swift_horseman,2,3),(trp_ac4_rhun_veteran_horse_archer,1,3),]),
#Khand
("khand_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_c2_khand_pony_rider,1,2),(trp_i2_khand_pit_dog,2,4),(trp_i1_khand_bondsman,4,8),]),
("khand_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_ac3_khand_skirmisher,2,4),(trp_c3_khand_horseman,0,1),(trp_i3_khand_warrior,2,3),(trp_i3_khand_pitfighter,1,2),]),
("khand_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_c4_khand_heavy_horseman,2,4),(trp_ac4_khand_vet_skirmisher,1,2),(trp_i4_khand_pit_champion,1,2)]),
#Umbar (7-14, 5-10, 4-8)
("umbar_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_a2_corsair_marine,1,2),(trp_i2_corsair_warrior,2,4),(trp_i1_corsair_youth,4,8),]),
("umbar_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_i2_mordor_num_renegade,1,2),(trp_i3_corsair_swordsman,1,2),(trp_i3_corsair_spearman,1,2),(trp_a3_corsair_marksman,2,4)]),
("umbar_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_i3_mordor_num_warrior,1,2),(trp_i4_corsair_veteran_swordsman,1,2),(trp_i4_corsair_veteran_spearman,1,2),(trp_a4_corsair_veteran_marksman,1,2),]),
#Lothlorien - Elves get slightly less troops (6-12, 4-8, 4-8)
("lorien_reinf_a"  ,"_",0,0,fac_commoners,0,[(trp_i3_lorien_inf,2,4),(trp_a2_lorien_warden,2,4),(trp_a1_lorien_scout,2,4),(trp_a2_lorien_archer,1,2),]),
("lorien_reinf_b"  ,"_",0,0,fac_commoners,0,[(trp_a3_lorien_vet_warden,1,2),(trp_a3_lorien_vet_archer,1,2),(trp_i3_lorien_inf,2,4),]),
("lorien_reinf_c"  ,"_",0,0,fac_commoners,0,[(trp_a4_lorien_gal_warden,1,2),(trp_a4_lorien_gal_archer,1,2),(trp_i4_lorien_gal_inf,3,6),]),
#Imladris - two trees, Rivendell favored over Dunedain (6-12, 4-8, 4-8)
("imladris_reinf_a","_",0,0,fac_commoners,0,[(trp_i3_riv_swordbearer,1,3),(trp_a2_arnor_vet_scout,0,1),(trp_a1_riv_scout,1,2),(trp_a1_arnor_scout,2,4)]), #InVain: Fewer archers, more inf
("imladris_reinf_b","_",0,0,fac_commoners,0,[(trp_a3_riv_archer,2,4),(trp_a3_arnor_ranger,1,2),(trp_i4_riv_vet_swordbearer,1,2),(trp_i3_arnor_swordsman,0,1),]),
("imladris_reinf_c","_",0,0,fac_commoners,0,[(trp_ac5_riv_rider,2,4),(trp_c4_arnor_horseman,1,1),(trp_i5_riv_swordmaster,1,2),(trp_a4_arnor_vet_ranger,0,1),]),
#Woodelves (6-12, 4-8, 4-8)
("woodelf_reinf_a" ,"_",0,0,fac_commoners,0,[(trp_a2_greenwood_veteran_scout,1,2),(trp_i2_greenwood_infantry,1,3),(trp_a1_greenwood_scout,4,7),]),
("woodelf_reinf_b" ,"_",0,0,fac_commoners,0,[(trp_a3_greenwood_archer,1,2),(trp_a3_greenwood_sentinel,1,2),(trp_i3_greenwood_vet_infantry,2,4),]),
("woodelf_reinf_c" ,"_",0,0,fac_commoners,0,[(trp_a4_greenwood_veteran_archer,1,2),(trp_a4_greenwood_vet_sentinel,1,2),(trp_i4_greenwood_elite_infantry,2,4),]),
#Moria (8-16, 7-13, 5-10)
("moria_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_i1_moria_snaga,4,8),(trp_i2_moria_goblin,2,4),]), #InVain: traded some t1 for t2 = more infantry for hosts
("moria_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_a3_moria_large_goblin_archer,4,7),(trp_i2_moria_goblin,1,2),(trp_i3_moria_large_goblin,2,4),(trp_i4_moria_fell_goblin,1,2)]), #InVain: t3 archers, t3 inf, some t4 inf
("moria_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_c3_moria_wolf_rider,2,4),(trp_i3_moria_large_goblin,1,2),]), #InVain: removed archers, because B has so many, less cav, fewer t3
#Dol Guldur - same as Mordor without uruks and Numenoreans (8-16, 7-13, 5-10)
("guldur_reinf_a"  ,"_",0,0,fac_commoners,0,[(trp_i1_guldur_orc_snaga,4,10),(trp_i2_mordor_orc,3,5)]),
("guldur_reinf_b"  ,"_",0,0,fac_commoners,0,[(trp_a3_guldur_large_orc_tracker,2,5),(trp_i2_mordor_orc,1,2),(trp_i3_mordor_large_orc,3,5),]), #InVain: t3 archers, t3 inf
("guldur_reinf_c"  ,"_",0,0,fac_commoners,0,[(trp_c3_mordor_warg_rider,1,2),(trp_a4_guldur_fell_orc_tracker,1,2),(trp_i4_mordor_fell_orc,2,4),]),
#Beornings - two trees, Beornings favored over Woodmen (7-14, 5-10, 4-8)
("beorn_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_i2_beorning_warrior,2,4),(trp_i1_beorning_man,2,4),(trp_i1_woodmen_man,3,6)]),
("beorn_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_a3_woodmen_scout,2,4),(trp_i3_woodmen_skilled_forester,1,2),(trp_i3_beorning_tolltacker,1,2),(trp_i3_beorning_carrock_lookout,1,2)]),
("beorn_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_i4_beorning_sentinel,1,3),(trp_i4_beorning_carrock_fighter,2,3),(trp_i4_woodmen_axemen,1,2),]),
#Mt. Gundabad - see Moria (8-16, 7-13, 5-10)
("gundabad_reinf_a","_",0,0,fac_commoners,0,[(trp_i1_gunda_goblin,6,12),(trp_i2_gunda_orc,5,8)]), #InVain: traded some t1 for t2 /#InVain: increased number of infantry by 50%, so lords have less space left for warg riders (hope this works)
("gundabad_reinf_b","_",0,0,fac_commoners,0,[(trp_ca4_gunda_skirmisher,1,3),(trp_i2_gunda_orc,3,5),(trp_i3_gunda_orc_fighter,2,3),]), #InVain t3 orcs, less t2 orcs
("gundabad_reinf_c","_",0,0,fac_commoners,0,[(trp_c3_gunda_goblin_rider,1,2),(trp_i3_gunda_orc_fighter,2,3),]), 
#Dale (7-14, 5-10, 4-8)
("dale_reinf_a"    ,"_",0,0,fac_commoners,0,[(trp_c2_rhovanion_retainer,2,4),(trp_i2_dale_man_at_arms,1,2),(trp_a2_dale_scout,1,2),(trp_i1_dale_militia,5,10),]),
("dale_reinf_b"    ,"_",0,0,fac_commoners,0,[(trp_c2_rhovanion_retainer,0,2),(trp_a3_dale_bowman,3,5),(trp_i3_dale_spearman,1,2),(trp_i3_dale_swordsman,1,2),]),
("dale_reinf_c"    ,"_",0,0,fac_commoners,0,[(trp_c4_rhovanion_rider,3,6),(trp_i4_dale_billman,1,2),(trp_i4_dale_sergeant,1,2),]), #InVain: More Cav
#Erebor (7-14, 5-10, 4-8)
("dwarf_reinf_a"   ,"_",0,0,fac_commoners,0,[(trp_i2_dwarf_warrior,2,3),(trp_i2_iron_hills_miner,1,2),(trp_i1_dwarf_apprentice,4,8),]), #InVain: no archers
("dwarf_reinf_b"   ,"_",0,0,fac_commoners,0,[(trp_a3_dwarf_scout,2,4),(trp_a4_dwarf_bowman,1,2),(trp_i3_dwarf_hardened_warrior,2,4),(trp_i2_iron_hills_miner,0,1),]), #InVain: More archers, less infantry
("dwarf_reinf_c"   ,"_",0,0,fac_commoners,0,[(trp_i4_dwarf_axeman,2,4),(trp_i4_dwarf_spearman,2,4),(trp_i4_iron_hills_infantry,1,2),]), #InVain: No archers, more Erebor infantry
#Dunlenders (7-14, 5-10, 4-8)
("dunland_reinf_a" ,"_",0,0,fac_commoners,0,[(trp_i2_dun_warrior,3,6),(trp_i1_dun_wildman,4,8),]),
("dunland_reinf_b" ,"_",0,0,fac_commoners,0,[(trp_i3_dun_vet_warrior,3,6),(trp_i3_dun_pikeman,2,4),]),
("dunland_reinf_c" ,"_",0,0,fac_commoners,0,[(trp_ac4_dun_crebain_rider,1,3),(trp_i4_dun_wolf_warrior,2,4),(trp_i4_dun_vet_pikeman,1,3),]),

#Volunteer templates
#MV guidelines:
#  - A mix of T1 (tier 1) troops, size 2-5 (if there are no T1, use fewer T2)
#  - Ideally the starting troops from each faction subtree

("gondor_cap_recruits","_",0,0,fac_commoners,0,[(trp_i1_gon_levy,2,5),(trp_c1_gon_nobleman,1,1)]),
("gondor_recruits"    ,"_",0,0,fac_commoners,0,[(trp_i1_gon_levy,1,4),(trp_c1_gon_nobleman,0,1)]),
("pelargir_recruits"  ,"_",0,0,fac_commoners,0,[(trp_i1_pel_watchman,1,4)]), #T2
("dol_amroth_recruits","_",0,0,fac_commoners,0,[(trp_i1_amroth_recruit,2,4)]), #Cavalry line nerf
("lamedon_recruits"   ,"_",0,0,fac_commoners,0,[(trp_i1_lam_clansman,2,5)]),
("lossarnach_recruits","_",0,0,fac_commoners,0,[(trp_i1_loss_woodsman,2,5)]),
("pinnath_recruits"   ,"_",0,0,fac_commoners,0,[(trp_i1_pinnath_plainsman,1,4)]), #T2
("ithilien_recruits"  ,"_",0,0,fac_commoners,0,[(trp_a4_ithilien_ranger,1,2)]), #T4! nerf
("blackroot_recruits" ,"_",0,0,fac_commoners,0,[(trp_a1_blackroot_hunter,1,4)]), #T2

("rohan_recruits"     ,"_",0,0,fac_commoners,0,[(trp_i1_rohan_youth,2,4)]),
("rohan_cap_recruits" ,"_",0,0,fac_commoners,0,[(trp_i1_rohan_youth,2,6)]),
("isengard_recruits"  ,"_",0,0,fac_commoners,0,[(trp_i1_isen_uruk_snaga,2,3),(trp_i1_isen_orc_snaga,2,4)]), #two T1
("morannon_recruits"  ,"_",0,0,fac_commoners,0,[(trp_i1_mordor_uruk_snaga,1,2),(trp_i1_mordor_orc_snaga,3,5),(trp_i2_mordor_num_renegade,1,1),]), #two T1 & prize
("mordor_recruits"    ,"_",0,0,fac_commoners,0,[(trp_i1_mordor_uruk_snaga,1,2),(trp_i1_mordor_orc_snaga,3,5)]), #two T1
("morgul_recruits"    ,"_",0,0,fac_commoners,0,[(trp_i1_mordor_uruk_snaga,2,3),(trp_i2_mordor_morgul_orc,1,2)]), #T1 T2
("harad_recruits"     ,"_",0,0,fac_commoners,0,[(trp_i1_harad_levy,1,3),(trp_c2_harondor_scout,0,2),(trp_i2_far_harad_tribesman,1,2)]), #three T1
("rhun_recruits"      ,"_",0,0,fac_commoners,0,[(trp_i1_rhun_tribesman,1,4),(trp_c2_rhun_horseman,1,1)]), #T1 and T2
("khand_recruits"     ,"_",0,0,fac_commoners,0,[(trp_i1_khand_bondsman,2,5)]),
("umbar_recruits"     ,"_",0,0,fac_commoners,0,[(trp_i1_corsair_youth,3,6)]),
("lorien_recruits"    ,"_",0,0,fac_commoners,0,[(trp_a1_lorien_scout,1,3),(trp_a2_lorien_archer,1,1)]), #two T1
("imladris_recruits"  ,"_",0,0,fac_commoners,0,[(trp_a1_riv_scout,0,2),(trp_a1_arnor_scout,2,3)]), #two T1
("woodelf_recruits"   ,"_",0,0,fac_commoners,0,[(trp_a1_greenwood_scout,1,4)]),
("moria_recruits"     ,"_",0,0,fac_commoners,0,[(trp_i1_moria_snaga,5,10)]),
("guldur_recruits"    ,"_",0,0,fac_commoners,0,[(trp_i1_guldur_orc_snaga,5,10)]),
("beorn_recruits"     ,"_",0,0,fac_commoners,0,[(trp_i1_beorning_man,2,3),(trp_i1_woodmen_man,1,2)]),
("woodman_recruits"   ,"_",0,0,fac_commoners,0,[(trp_i1_woodmen_man,2,3),(trp_i1_beorning_man,1,2)]),
("gundabad_recruits"  ,"_",0,0,fac_commoners,0,[(trp_i1_gunda_goblin,3,6)]),
("gundabad_cap_recruits","_",0,0,fac_commoners,0,[(trp_i1_gunda_goblin,3,7)]),
("dale_recruits"      ,"_",0,0,fac_commoners,0,[(trp_i1_dale_militia,1,4),(trp_c2_rhovanion_retainer,1,2)]), #T1 and T2
("dwarf_recruits"     ,"_",0,0,fac_commoners,0,[(trp_i1_dwarf_apprentice,2,3),(trp_i2_iron_hills_miner,0,2)]), #T1 and T2
("dwarf_iron_recruits","_",0,0,fac_commoners,0,[(trp_i2_iron_hills_miner,1,2),(trp_i1_dwarf_apprentice,1,2)]), #T1 and T2
("dunland_recruits"   ,"_",0,0,fac_commoners,0,[(trp_i1_dun_wildman,3,7)]),

("caravan_survivors","Caravan Survivors",icon_generic_knight|carries_goods(2),0,fac_neutral,merchant_personality,[(trp_sea_raider,5,5)]),

# Morale parties

("routed_allies","Routed Allies",icon_axeman|carries_goods(3),0,fac_outlaws,merchant_personality,[]),
("routed_enemies","Routed Enemies",icon_axeman|carries_goods(3),0,fac_outlaws,merchant_personality,[]),

# Mordor Legions

("legion_minas_morgul","Legion_of_Minas_Morgul",icon_uruk_x4|carries_goods(3), 0, fac_mordor, soldier_personality,[(trp_high_captain_of_mordor,1,1),(trp_mordor_olog_hai,10,10),(trp_i4_mordor_fell_uruk,30,60),(trp_i4_mordor_fell_morgul_orc,25,55),(trp_i2_mordor_morgul_orc, 25, 50),(trp_a3_mordor_large_orc_archer, 25, 50)]),
("legion_udun","Legion_of_Udun",icon_uruk_x4|carries_goods(3), 0, fac_mordor, soldier_personality,[(trp_high_captain_of_mordor,1,1),(trp_c4_mordor_great_warg_rider,20,30),(trp_a4_mordor_fell_orc_archer,30,45),(trp_i4_mordor_fell_uruk_slayer, 30, 45),(trp_i3_mordor_large_orc,30,90),(trp_mordor_olog_hai,10,10)]),
("legion_gorgoroth","Legion_of_Gorgoroth",icon_uruk_x4|carries_goods(3), 0, fac_mordor, soldier_personality,[(trp_high_captain_of_mordor,1,1),(trp_c5_mordor_num_knight,30,30),(trp_mordor_olog_hai,10,10),(trp_c3_mordor_warg_rider,30,50),(trp_i3_mordor_large_orc,40,90),(trp_a3_mordor_large_orc_archer,20,40)]),
("legion_barad_dur","Legion_of_Barad-Dur",icon_uruk_x4|carries_goods(3), 0, fac_mordor, soldier_personality,[(trp_high_captain_of_mordor,1,1),(trp_captain_of_mordor,5,5),(trp_i5_mordor_black_uruk,60,60),(trp_i4_mordor_fell_orc,90,90),(trp_a4_mordor_fell_orc_archer,60,60),(trp_mordor_olog_hai,15,15)]),

##Kham Quests ####
##Kham  Ring Hunters Start ####
("beorn_messenger"    ,"Beorning Messenger"      ,icon_axeman       |carries_goods(1)|pf_show_faction,0,fac_beorn   ,scout_personality,[(trp_i5_beorning_carrock_berserker,1,1)]), 
("village","Village",icon_village_a| pf_quest_party| pf_hide_defenders|pf_is_static|pf_always_visible,0,fac_commoners,merchant_personality,[(trp_farmer,1,1)]),
("ring_hunters","Ring_Hunters",icon_harad_horseman|carries_goods(2)| pf_quest_party | ai_bhvr_hold  ,0,fac_commoners  ,bandit_personality,[(trp_ring_hunter_captain,1,1),(trp_ring_hunter_one,10,15),(trp_c5_khand_kataphrakt,10,15),(trp_ring_hunter_three,12,20),(trp_ring_hunter_four,20,35),(trp_ring_hunter_two,15,30)]),
## Kham Ring Hunters End ####

##Kham Destroy Scout Camp Start
("scout_camp_small","Scout Camp",icon_nomadcamp_b| pf_quest_party| pf_hide_defenders|pf_is_static|pf_always_visible,0,fac_commoners,merchant_personality,[(trp_farmer,1,1)]),
("scout_camp_large","Fortified Scout Camp",icon_orctower| pf_quest_party| pf_hide_defenders|pf_is_static|pf_always_visible,0,fac_commoners,merchant_personality,[(trp_farmer,1,1)]),

##Kham Beorning Caravans Start
("beorn_caravan"    ,"Woodsmen Caravan"      ,icon_mule         |carries_goods(10)|pf_show_faction,0,fac_beorn    ,prisoner_train_personality,[(trp_i4_beorning_sentinel,1,5),(trp_a4_woodmen_archer,5,10),(trp_i4_woodmen_axemen,4,8),(trp_a3_woodmen_scout,8,16),(trp_i3_woodmen_skilled_forester,18,30)]), # strength 198-399

##Kham Orc Horde
("orc_horde"   ,"Orc Horde"     ,icon_orc_x4           |carries_goods(6)|pf_show_faction,0,fac_moria   ,soldier_personality,[(trp_i3_moria_large_goblin,40,50),(trp_i1_moria_snaga,50,80)]), 

("vet_archer"  ,"Vet Archer",icon_mirkwood_elf |carries_goods(1)|pf_show_faction,0,fac_lorien ,scout_personality,[(trp_killer_witcher,1,1)]),

##Kham - Replacement Volunteer party template
("volunteers","Reserves",icon_generic_knight|pf_is_static,0,fac_commoners,merchant_personality,[]),

##Kham - Refugee Quests
("refugees","Refugees",icon_mule|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_innocents,merchant_personality,[(trp_farmer,6,7), (trp_peasant_woman,3,3)]),


## Kham - Retreat Troops
("retreat_troops","Cover Troops",icon_axeman|carries_goods(3),0,fac_outlaws,merchant_personality,[(trp_farmer,1,1)]),

("radagast", "Lone Rider",icon_generic_knight|pf_default_behavior|pf_quest_party|pf_hide_defenders,0,fac_neutral,merchant_personality,[(trp_radagast,1,1)]),
] + common_warp_templates
