from header_common import *
from header_parties import *
from ID_troops import *
from ID_factions import *
from ID_party_templates import *
from ID_map_icons import *
from module_constants import *
from ID_menus import *

from module_parties_mapscribbler import *
#parties_scribbler = []

####################################################################################################################
#  Each party record contains the following fields:
#  1) Party id: used for referencing parties in other files.
#     The prefix p_ is automatically added before each party id.
#  2) Party name.
#  3) Party flags. See header_parties.py for a list of available flags
#  4) Menu. ID of the menu to use when this party is met. The value 0 uses the default party encounter system.
#  5) Party-template. ID of the party template this party belongs to. Use pt_none as the default value.
#  6) Faction.
#  7) Personality. See header_parties.py for an explanation of personality flags.
#  8) Ai-behavior
#  9) Ai-target party
# 10) Initial coordinates.
# 11) List of stacks. Each stack record is a triple that contains the following fields:
#   11.1) Troop-id. 
#   11.2) Number of troops in this stack. 
#   11.3) Member flags. Use pmf_is_prisoner to note that this member is a prisoner.
# 12) Party direction in degrees [optional]
####################################################################################################################
no_menu = 0
pf_tld_down  = pf_is_static|pf_always_visible|pf_show_faction|pf_label_large

parties = [
  ("main_party","Main_Party",icon_player|pf_limit_members, no_menu, pt_none,fac_player_faction,0,ai_bhvr_hold,0,(13.6,54.6),[(trp_player,1,0)]),
  ("temp_party","temp_party",pf_disabled, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0,0),[]),
  ("camp_bandits","camp_bandits",pf_disabled, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(1,1),[(trp_unarmed_troop,3,0)]),
#parties before this point are hardwired. Their order should not be changed.

  ("temp_party_2","temp_party_2"   ,pf_disabled, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0,0),[]),
#Used for calculating casulties.
  ("temp_casualties","casualties"  ,pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("temp_casualties_2","casualties",pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("temp_casualties_3","casualties",pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("temp_wounded","enemies_wounded",pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("temp_killed","enemies_killed"  ,pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("main_party_backup","_"         ,pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("encountered_party_backup","_"  ,pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("collective_friends_backup","_" ,pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("player_casualties","_"         ,pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("enemy_casualties","_"          ,pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("ally_casualties","_"           ,pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),

  ("collective_enemy"  ,"collective_enemy",pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("collective_ally"   ,"collective_ally" ,pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("collective_friends","collective_ally" ,pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  
  #("zendar","Brigand Fort", icon_castle_c|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-29.9,-28.3),[]),

#TLD TOWNS
    # Gondor towns
    ("town_minas_tirith"    ,"Minas_Tirith",icon_minas_tirith       |pf_tld_down, no_menu, pt_none, fac_gondor,0,ai_bhvr_hold,0,(-47.47, 24.28),[],205),
    ("town_pelargir"        ,"Pelargir",    icon_gondortown         |pf_tld_down, no_menu, pt_none, fac_gondor,0,ai_bhvr_hold,0,(-41.31, 61.0 ),[],240),
    ("town_linhir"          ,"Linhir",      icon_gondortown         |pf_tld_down, no_menu, pt_none, fac_gondor,0,ai_bhvr_hold,0,( -0.83, 59.13),[],170),
    ("town_dol_amroth"      ,"Dol_Amroth",  icon_dolamroth          |pf_tld_down, no_menu, pt_none, fac_gondor,0,ai_bhvr_hold,0,(  46.6, 64.6 ),[],280),
    ("town_edhellond"       ,"Edhellond",   icon_gondortown         |pf_tld_down, no_menu, pt_none, fac_gondor,0,ai_bhvr_hold,0,( 37.66, 46.14),[],170),
    ("town_lossarnach"      ,"Lossarnach",  icon_castle_gondor_small|pf_tld_down, no_menu, pt_none, fac_gondor,0,ai_bhvr_hold,0,(-39.85, 37.0 ),[],170),
    ("town_tarnost"         ,"Tarnost",     icon_castle_gondor_small|pf_tld_down, no_menu, pt_none, fac_gondor,0,ai_bhvr_hold,0,( 15.31, 63.94),[],170),
    ("town_erech"           ,"Erech",       icon_castle_gondor_small|pf_tld_down, no_menu, pt_none, fac_gondor,0,ai_bhvr_hold,0,( 28.17,  9.34),[],170),
    ("town_pinnath_gelin"  ,"Pinnath_Gelin",icon_gondortown         |pf_tld_down, no_menu, pt_none, fac_gondor,0,ai_bhvr_hold,0,( 50.82, 30.82),[],170),
    ("town_west_osgiliath","West_Osgiliath",icon_west_osgilliath    |pf_tld_down, no_menu, pt_none, fac_gondor,0,ai_bhvr_hold,0,(-58.19, 20.5 ),[],0),
    ("town_henneth_annun"  ,"Henneth_Annun",icon_henneth_annun|pf_is_static|pf_show_faction, no_menu, pt_none, fac_gondor,0,ai_bhvr_hold,0,(-63.81,-14.05),[],170),
    ("town_cair_andros"     ,"Cair_Andros", icon_cairandros         |pf_tld_down, no_menu, pt_none, fac_gondor,0,ai_bhvr_hold,0,(-56.48,  3.55),[],170),
    ("town_calembel"        ,"Calembel",    icon_gondortown         |pf_tld_down, no_menu, pt_none, fac_gondor,0,ai_bhvr_hold,0,( -2.16, 30.86),[],50),
# Rohan towns
    ("town_edoras","Edoras",         icon_edoras     |pf_tld_down, no_menu, pt_none, fac_rohan,0,ai_bhvr_hold,0,( 22.8,-14.7),[],215),
    ("town_aldburg","Aldburg",       icon_rohantown1 |pf_tld_down, no_menu, pt_none, fac_rohan,0,ai_bhvr_hold,0,(  7.9, -8.3),[],170),
    ("town_hornburg","Hornburg",     icon_helms_deep |pf_tld_down, no_menu, pt_none, fac_rohan,0,ai_bhvr_hold,0,( 40.2,-11.9),[],190),
    ("town_east_emnet","East_Emnet", icon_rohantown1 |pf_tld_down, no_menu, pt_none, fac_rohan,0,ai_bhvr_hold,0,(-2.9,-27.6),[],170),
    ("town_westfold","Westfold",     icon_rohantown1 |pf_tld_down, no_menu, pt_none, fac_rohan,0,ai_bhvr_hold,0,( 41.5,-29.3),[],260),
    ("town_west_emnet","West_Emnet", icon_rohantown1 |pf_tld_down, no_menu, pt_none, fac_rohan,0,ai_bhvr_hold,0,( 22.1,-40.1),[],250),
    ("town_eastfold","Eastfold",     icon_rohantown1 |pf_tld_down, no_menu, pt_none, fac_rohan,0,ai_bhvr_hold,0,(-19.2,-0.52),[],170),
# Mordor towns
    ("town_morannon","Morannon",              icon_morannon   |pf_tld_down,  no_menu, pt_none, fac_mordor,0,ai_bhvr_hold,0,(-78.9,-34.2),[],170),
    ("town_minas_morgul","Minas_Morgul",      icon_minasmorgul|pf_tld_down,  no_menu, pt_none, fac_mordor,0,ai_bhvr_hold,0,(-72.3,23.8),[],170),
    ("town_cirith_ungol","Orc_Patrol_Camp",   icon_orctower   |pf_tld_down,  no_menu, pt_none, fac_mordor,0,ai_bhvr_hold,0,(-50.1,-45.3),[],170),
    ("town_east_osgiliath","East_Osgiliath",icon_east_osgilliath|pf_tld_down,no_menu, pt_none, fac_mordor,0,ai_bhvr_hold,0,(-62.2,20.6),[],0),
    ("town_orc_sentry_camp","Orc_Sentry_Camp",icon_orctower   |pf_tld_down,  no_menu, pt_none, fac_mordor,0,ai_bhvr_hold,0,(-56.4,30.4),[],170),
# Isengard towns
    ("town_isengard","Isengard",                   icon_isengard|pf_tld_down, no_menu, pt_none, fac_isengard,0,ai_bhvr_hold,0,(52.8,-57.7),[],170),
    ("town_urukhai_outpost","Uruk_Hai_Outpost",    icon_orctower|pf_tld_down, no_menu, pt_none, fac_isengard,0,ai_bhvr_hold,0,(23.7,-52.4),[],170),
    ("town_urukhai_h_camp","Uruk_Hai_Hunting_camp",icon_orctower|pf_tld_down, no_menu, pt_none, fac_isengard,0,ai_bhvr_hold,0,(16.8,-78.7),[],170),
    ("town_urukhai_r_camp","Uruk_Hai_River_camp",  icon_orctower|pf_tld_down, no_menu, pt_none, fac_isengard,0,ai_bhvr_hold,0,(5.9,-54.9),[],170),
# Lothlorien towns
    ("town_caras_galadhon","Caras_Galadhon",icon_grove |pf_tld_down, no_menu, pt_none, fac_lorien,0,ai_bhvr_hold,0,( -5.7,-131.3),[],350),
    ("town_cerin_dolen"   ,"Cerin_Dolen",   icon_tree  |pf_tld_down, no_menu, pt_none, fac_lorien,0,ai_bhvr_hold,0,( 20.2,-135.7),[],170),
    ("town_cerin_amroth"  ,"Cerin_Amroth",  icon_tree  |pf_tld_down, no_menu, pt_none, fac_lorien,0,ai_bhvr_hold,0,(  5.7,-134.3),[],170),
# Woodelves towns
    ("town_thranduils_halls","Thranduil's_Halls",icon_thranduil|pf_tld_down, no_menu, pt_none, fac_woodelf,0,ai_bhvr_hold,0,(-30.8,-223.0),[],170),
    ("town_woodelf_camp"     ,"Woodelf_Camp",        icon_tree |pf_tld_down, no_menu, pt_none, fac_woodelf,0,ai_bhvr_hold,0,(-42.3,-155.1),[],170),
    ("town_woodelf_west_camp","Woodelf_West_Camp",   icon_tree |pf_tld_down, no_menu, pt_none, fac_woodelf,0,ai_bhvr_hold,0,( -6.2,-215.4),[],170),
# Woodmen and Beorning towns   
    ("town_woodsmen_village","Woodsmen_Village", icon_village_a    |pf_tld_down, no_menu, pt_none, fac_beorn,0,ai_bhvr_hold,0,(-35.4,-175.1),[],170),
    ("town_beorning_village","Beorning_Village", icon_smallvillage |pf_tld_down, no_menu, pt_none, fac_beorn,0,ai_bhvr_hold,0,(-4.4,-184.7),[],170),
    ("town_beorn_house"     ,"Beorn's House",    icon_smallvillage |pf_tld_down, no_menu, pt_none, fac_beorn,0,ai_bhvr_hold,0,(-19.7,-194.0),[],170),
# Moria towns
    ("town_moria","Gates_of_Moria",           icon_moria      |pf_tld_down, no_menu, pt_none, fac_moria,0,ai_bhvr_hold,0,(55.33,-150.7),[],200),
    ("town_troll_cave","Troll_Cave", icon_orctower   |pf_tld_down, no_menu, pt_none, fac_moria,0,ai_bhvr_hold,0,(49.6,-120),[],170),
# Dale towns
    ("town_dale","Dale",             icon_town     |pf_tld_down, no_menu, pt_none, fac_dale,0,ai_bhvr_hold,0,(-61.1,-223.9),[],170),
    ("town_esgaroth","Esgaroth",     icon_esgaroth |pf_tld_down, no_menu, pt_none, fac_dale,0,ai_bhvr_hold,0,(-61.89,-216.83),[],150),
# Dunlanders towns
    ("town_dunland_camp","Dunlander_Camp", icon_nomadcamp_b|pf_tld_down, no_menu, pt_none, fac_dunland,0,ai_bhvr_hold,0,(49.9,-48.5),[],350),# pos changes to (45.9,-43.5) after war starts
# Haradrim towns
    ("town_harad_camp","Haradrim_Camp",    icon_haradcamp  |pf_tld_down, no_menu, pt_none, fac_harad,0,ai_bhvr_hold,0,(-55.9,67.7),[],170),
# Khand towns
    ("town_khand_camp","Khand_Camp",       icon_nomadcamp  |pf_tld_down, no_menu, pt_none, fac_khand,0,ai_bhvr_hold,0,(-74.2,-44.9),[],170),
# Umbar towns
    ("town_umbar_camp","Corsair_Camp",     icon_corsaircamp|pf_tld_down, no_menu, pt_none, fac_umbar,0,ai_bhvr_hold,0,(-4.03,70.33),[],129), # 129 V di 30
# Imladris towns
    ("town_imladris_camp","Rivendell_Camp",icon_camp       |pf_tld_down, no_menu, pt_none, fac_imladris,0,ai_bhvr_hold,0,(21.5,-145.1),[],170),
# Dol Guldur towns
    ("town_dol_guldur","Dol_Guldur",       icon_dolguldur  |pf_tld_down,   no_menu, pt_none, fac_guldur,0,ai_bhvr_hold,0,(-41.3,-131.1),[],170),
    ("town_dol_guldur_north_outpost","Dol_Guldur North Outpost",  icon_orctower  |pf_tld_down,   no_menu, pt_none, fac_guldur,0,ai_bhvr_hold,0,(-46.6,-188.0),[],170),
# Rhun towns
    ("town_rhun_main_camp","Main_Rhun_Camp",     icon_nomadcamp  |pf_tld_down, no_menu, pt_none, fac_rhun,0,ai_bhvr_hold,0,(-71.2,-223.1),[],170),
    ("town_rhun_south_camp","Rhun_Southern Outpost",  icon_nomadcamp  |pf_tld_down, no_menu, pt_none, fac_rhun,0,ai_bhvr_hold,0,(-73.02,-189.9),[],170),
    ("town_rhun_north_camp","Rhun_Northern Outpost",  icon_nomadcamp  |pf_tld_down, no_menu, pt_none, fac_rhun,0,ai_bhvr_hold,0,(-68.63,-236.87),[],170),
# Gundabad towns
    ("town_gundabad"            ,"Gundabad",                 icon_moria   |pf_tld_down, no_menu, pt_none, fac_gundabad,0,ai_bhvr_hold,0,(35.7,-241.5),[],165),
    ("town_gundabad_ne_outpost" ,"Gundabad_NE_Outpost",      icon_orctower|pf_tld_down, no_menu, pt_none, fac_gundabad,0,ai_bhvr_hold,0,(-25.1,-246.1),[],120),
    ("town_gundabad_nw_outpost" ,"Gundabad_NW_Outpost",      icon_orctower|pf_tld_down, no_menu, pt_none, fac_gundabad,0,ai_bhvr_hold,0,(-4.2,-243.6),[],270),
    ("town_goblin_north_outpost","Goblin_Northern_Outpost",  icon_orctower|pf_tld_down, no_menu, pt_none, fac_gundabad,0,ai_bhvr_hold,0,(22.1,-211.2),[],10),
    ("town_goblin_south_outpost","Goblin_Southern_Outpost",  icon_orctower|pf_tld_down, no_menu, pt_none, fac_gundabad,0,ai_bhvr_hold,0,(18.9,-194.8),[],140),
    ("town_gundabad_m_outpost"  ,"Gundabad_Mirkwood_Outpost",icon_orctower|pf_tld_down, no_menu, pt_none, fac_gundabad,0,ai_bhvr_hold,0,(-13.9,-224.0),[],170),
# Dwarves towns
    ("town_erebor"       ,"Erebor",          icon_moria |pf_tld_down, no_menu, pt_none, fac_dwarf,0,ai_bhvr_hold,0,(-59.6,-226.4),[],130),
    ("town_ironhill_camp","Iron_Hills_Quarry",icon_camp  |pf_tld_down, no_menu, pt_none, fac_dwarf,0,ai_bhvr_hold,0,(-49.6,-239.9),[],170),

####DONE TLD TOWNS

# Advance camps for other theaters 
 ("advcamp_gondor"  ,"Gondor Advance Camp"  ,icon_camp     |pf_tld_down|pf_disabled,no_menu,pt_none,fac_gondor  ,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_rohan"   ,"Rohan Advance Camp"   ,icon_camp     |pf_tld_down|pf_disabled,no_menu,pt_none,fac_rohan   ,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_isengard","Isengard Advance Camp",icon_orctower |pf_tld_down|pf_disabled,no_menu,pt_none,fac_isengard,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_mordor"  ,"Mordor Advance Camp"  ,icon_orctower |pf_tld_down|pf_disabled,no_menu,pt_none,fac_mordor  ,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_harad"   ,"Harad Advance Camp"   ,icon_haradcamp|pf_tld_down|pf_disabled,no_menu,pt_none,fac_harad   ,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_rhun"    ,"Rhun Advance Camp"    ,icon_nomadcamp|pf_tld_down|pf_disabled,no_menu,pt_none,fac_rhun    ,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_khand"   ,"Khand Advance Camp"   ,icon_nomadcamp|pf_tld_down|pf_disabled,no_menu,pt_none,fac_khand   ,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_umbar"   ,"Umbar Advance Camp"   ,icon_camp     |pf_tld_down|pf_disabled,no_menu,pt_none,fac_umbar   ,0, ai_bhvr_hold,0,(0,0),[],175),
 ("advcamp_lorien"  ,"Lorien Advance Camp"  ,icon_camp     |pf_tld_down|pf_disabled,no_menu,pt_none,fac_lorien  ,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_imladris","Imladris Advance Camp",icon_camp     |pf_tld_down|pf_disabled,no_menu,pt_none,fac_imladris,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_woodelf" ,"Mirkwood Advance Camp",icon_camp     |pf_tld_down|pf_disabled,no_menu,pt_none,fac_woodelf ,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_moria"   ,"Moria Advance Camp"   ,icon_orctower |pf_tld_down|pf_disabled,no_menu,pt_none,fac_moria   ,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_guldur" ,"Dol Guldur Advance Camp",icon_orctower|pf_tld_down|pf_disabled,no_menu,pt_none,fac_guldur  ,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_gundabad","Gundabad Advance Camp",icon_orctower |pf_tld_down|pf_disabled,no_menu,pt_none,fac_gundabad,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_dale"    ,"Dale Advance Camp"    ,icon_camp     |pf_tld_down|pf_disabled,no_menu,pt_none,fac_dale    ,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_dwarf"   ,"Erebor Advance Camp"  ,icon_camp     |pf_tld_down|pf_disabled,no_menu,pt_none,fac_dwarf   ,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_dunland" ,"Dunland Advance Camp" ,icon_nomadcamp|pf_tld_down|pf_disabled,no_menu,pt_none,fac_dunland ,0, ai_bhvr_hold,0,(0,0),[],170),
 ("advcamp_beorn"   ,"Beorning Advance Camp",icon_camp     |pf_tld_down|pf_disabled,no_menu,pt_none,fac_beorn   ,0, ai_bhvr_hold,0,(0,0),[],170),


("centers_end","_",pf_disabled, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0,0),[]),
# stuff from native
# ("castle_1","Ethring",icon_castle_gondor_small|pf_tld_down|pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-2.2,30.9),[],50),

### TLD map icons
   ("Argonath","Argonath",icon_argonath|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-34.883472,-51.047958),[],180),
   ("Argonath2","Argonath",icon_argonath|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-36.795536,-51.047958),[],180),
   #("Hand1","hand_isen",icon_hand_isen|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(64.8,-59.1),[],75),
   #("Hand2","hand_isen",icon_hand_isen|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(65.4,-57.3),[],75),
   #("Hand3","hand_isen",icon_hand_isen|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(68.5,-64.5),[],5),
   #("Hand4","hand_isen",icon_hand_isen|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(70.4,-64.5),[],5),
   ("hand_isen" ,"Handsign_of_Isengard" ,icon_hand_isen|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(51.886200,-52.610794),[],185),
   ("mount_doom","Mount_Doom",icon_orodruin |pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-109.411041,1.567230),[],170),
   ("town_barad_dur","Barad_Dur",icon_baraddur|pf_is_static|pf_always_visible          , no_menu, pt_none, fac_mordor ,0,ai_bhvr_hold,0,(-100.048325,-3.573029),[],170),

   #fords _big BEGIN
  ("ford_cair_andros1"  ,"Anduin",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-56.69,   1.67),[], 90),
  ("ford_cair_andros2"  ,"Anduin",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-55.36,   5.32),[],170),
  ("ford_caras_galadhon","Anduin",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-11.26,-129.55),[],220),
  ("ford_brown_lands"   ,"Anduin",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,( -18.7,-109.76),[], 30),
  ("ford_rauros"        ,"Anduin",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-35.27, -32.95),[],145),
  ("ford_pelargir"      ,"Anduin",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-41.91,  64.37),[],145),
  ("ford_edhellond"     ,"Anduin",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,( 36.59,  48.24),[],145),
#fords_small  BEGIN
  ("ford_cerin_dolen"   ,"Silverlode",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(21.46,-130.72),[],220),
  ("old_ford"           ,"_Old_Ford_",icon_ford_rocks|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,( 0.46,-189.36),[],145),
  ("ford_erech"         ,"Ringlo",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,( 0.74,  31.75),[],145),
  ("ford_isen1"         ,"Isen",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(49.35, -43.6),[],145),
  ("ford_isen2"         ,"Isen",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(47.73, -47.21),[],145),
  ("ford_rohan"         ,"Entwash",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,( 7.70, -53.44),[],145),
  ("ford_rohan2"        ,"Entwash",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-6.66, -12.31),[],145),
  ("ford_fangorn"       ,"Entwash",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(27.89, -66.35),[],145),
  ("ford_fangorn2"      ,"Limlight",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,( 19.6, -96.0),[],145),
  ("ford_moria"         ,"Silverlode",icon_ford_rocks|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,( 37.5,-142.13),[],145),
#fords_small END

  #("salt_mine","Salt_Mine",icon_village_a|pf_disabled|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(6.004257,-11.482468),[]),
  #("four_ways_inn","Four_Ways_Inn",icon_village_a|pf_disabled|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-24.064327,1.070496),[]),
  ("test_scene","test_scene",icon_village_a|pf_disabled|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(4.077255,-12.735809),[]),
  ("battlefields","battlefields",pf_disabled|icon_village_a|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(4.255280,-10.009171),[]),

# Legendary Places
  ("legend_amonhen","Amon Hen",icon_ancient_ruins|pf_disabled|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_legendary_place, fac_neutral,0,ai_bhvr_hold,0,(-31.80,-47.71),[],180),
  ("legend_deadmarshes","Dead Marshes",icon_burial_mound|pf_disabled|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_legendary_place, fac_neutral,0,ai_bhvr_hold,0,(-58.10,-36.43),[],180),
  ("legend_mirkwood","Mirkwood Forest",icon_tree_low|pf_disabled|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_legendary_place, fac_neutral,0,ai_bhvr_hold,0,(-40.04,-144.54),[],180),
  ("legend_fangorn","Fangorn Entmoot",icon_tree_low|pf_disabled|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_legendary_place, fac_neutral,0,ai_bhvr_hold,0,(35.24,-84.19),[],180),
  
# central positions in theaters used to calculate advance camp positions
  ("theater_SE_center", "SE Theater center", pf_disabled|icon_village_a|pf_hide_defenders|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-53,21),[]), # West of West Osgiliath
  ("theater_SW_center", "SW Theater center", pf_disabled|icon_village_a|pf_hide_defenders|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-2,-43),[]), # Nortwest of East Emnet
  ("theater_C_center", "C Theater center", pf_disabled|icon_village_a|pf_hide_defenders|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,( 5.7,-134.3),[]), # Cerin Amroth
  ("theater_N_center", "N Theater center", pf_disabled|icon_village_a|pf_hide_defenders|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-19,-181),[]), # Beorn's House

# Fangorn central position used to check if player is in Fangorn
  ("fangorn_center", "Fangorn Center", pf_disabled|icon_village_a|pf_hide_defenders|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(35.24,-84.19),[]),

#  ("training_ground"  ,"Training_Ground", pf_disabled|icon_village_a|pf_hide_defenders|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(2.189980,-6.471909),[]),
#  ("training_ground_1","Training_Field",  pf_disabled|icon_village_a|pf_hide_defenders|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(39.999908,62.778122),[],100),
#  ("training_ground_2","Training_Field",  pf_disabled|icon_village_a|pf_hide_defenders|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-31.935398,57.532211),[],100),
#  ("training_ground_3","Training_Field",  pf_disabled|icon_village_a|pf_hide_defenders|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(53.349197,18.407715),[],100),
#  ("training_ground_4","Training_Field",  pf_disabled|icon_village_a|pf_hide_defenders|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-2.176975,-68.801270),[],100),
#  ("training_ground_5","Training_Field",  pf_disabled|icon_village_a|pf_hide_defenders|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-16.855721,-30.506454),[],100),

#  bridge_a
  ("looter_spawn_point"   ,"looter_sp",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(29.273674,79.890099),[(trp_looter,15,0)]),
  ("steppe_bandit_spawn_point"  ,"steppe_bandit_sp",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(27.303375,-60.205627),[(trp_looter,15,0)]),
  ("steppe_bandit_spawn_point_2"  ,"steppe_bandit_sp_2",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(28.19,-30.90),[(trp_looter,15,0)]),
##  ("black_khergit_spawn_point"  ,"black_khergit_sp",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(47.1, -73.3),[(trp_looter,15,0)]),
  ("forest_bandit_spawn_point"  ,"forest_bandit_sp",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-37.252506,6.916382),[(trp_looter,15,0)]),
  ("forest_bandit_spawn_point_2"  ,"forest_bandit_sp_2",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-65.33,43.30),[(trp_looter,15,0)]),
  ("forest_bandit_spawn_point_3"  ,"forest_bandit_sp_3",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-52.10,-28.62),[(trp_looter,15,0)]),
  ("forest_bandit_spawn_point_4"  ,"forest_bandit_sp_4",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-25.94,-117.04),[(trp_looter,15,0)]),
  ("forest_bandit_spawn_point_5"  ,"forest_bandit_sp_5",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-59.65,-173.31),[(trp_looter,15,0)]),
  ("mountain_bandit_spawn_point","mountain_bandit_sp",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(39.789207,26.066040),[(trp_looter,15,0)]),
  ("mountain_bandit_spawn_point_2","mountain_bandit_sp_2",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-21.54,34.50),[(trp_looter,15,0)]),
  ("mountain_bandit_spawn_point_3","mountain_bandit_sp_3",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(40.43,-130.92),[(trp_looter,15,0)]),
  ("mountain_bandit_spawn_point_4","mountain_bandit_sp_4",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(17.53,-175.76),[(trp_looter,15,0)]),
  ("mountain_bandit_spawn_point_5","mountain_bandit_sp_5",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-15.06,-237.27),[(trp_looter,15,0)]),
  ("sea_raider_spawn_point_1"   ,"sea_raider_sp",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-3,66.7),[(trp_looter,15,0)]),
  ("sea_raider_spawn_point_2"   ,"sea_raider_sp",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(48.6,48.6),[(trp_looter,15,0)]),
 
 #####TLD PARTIES BEGIN##########
  ("gondor_test"    ,"gondor_test_sp"    ,pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-7.509827,-5.265762),[(trp_looter,15,0)]),
  ("mordor_test"    ,"mordor_test_sp"    ,pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-7.312775,-4.991470),[(trp_looter,15,0)]),
  ("gondor_allies_test","gondor_allies_test_sp",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-7.500393,-5.082901),[(trp_looter,15,0)]),
  ("isengard_test"  ,"isengard_test_sp"  ,pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-7.317505,-5.082901),[(trp_looter,15,0)]),
  ("isen_rohan"     ,"isen_rohan_sp"     ,pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(34.842987,-27.865891),[(trp_looter,15,0)]),
  ("mordor_gondor"  ,"mordor_gondor_sp"  ,pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(30.825653,-23.388062),[(trp_looter,15,0)]),
  ("harad_gondor"   ,"harad_gondor_sp"   ,pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(37.227943,-30.542084),[(trp_looter,15,0)]),
  ("corsair_gondor" ,"corsair_gondor_sp" ,pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-7.312775,-4.991470),[(trp_looter,15,0)]),
  ("rhun_gondor"    ,"rhun_gondor_sp"    ,pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-7.312775,-4.991470),[(trp_looter,15,0)]),
  ("khand_gondor"   ,"khand_gondor_sp"   ,pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-7.312775,-4.991470),[(trp_looter,15,0)]),
  ("lorien_moria"   ,"lorien_moria_sp"   ,pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-7.312775,-4.991470),[(trp_looter,15,0)]),
  ("gunda_woodelves","gunda_woodelves_sp",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-7.312775,-4.991470),[(trp_looter,15,0)]),
  ("gunda_dwarves"  ,"gunda_dwarves_sp"  ,pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-7.312775,-4.991470),[(trp_looter,15,0)]),
 
 # add extra towns before this point 
  ("spawn_points_end","last_spawn_point",pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(-7.746731,1.880096),[(trp_looter,15,0)]),
 # pointers for scripting purposes
  ("pointer_player"           ,"_",pf_disabled|pf_no_label|pf_hide_defenders, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(0.314220,-10.163879),[]),
  ("pointer_z_0_begin"        ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-214.3,122.4),[]), # rt_water = 0
  ("pointer_z_0_mountain"     ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-214.3,122.4),[]), # rt_mountain = 1
  ("pointer_z_0_steppe"       ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-214.3,122.4),[]), # rt_steppe = 2
  ("pointer_z_0_plain"        ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-214.3,103.3),[]), # rt_plain = 3
  ("pointer_z_0_snow"         ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-214.3, 89.5),[]), # rt_swamp = rt_snow = 4  
  ("pointer_z_0_desert"       ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-214.3, 74.1),[]), # rt_desert = 5
  #("pointer_z_0_river"        ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-214.3, 74.1),[]), # rt_river  = 8
  ("pointer_z_0_steppe_forest","_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-219.5,112.4),[]), # rt_steppe_forest = 10
  ("pointer_z_0_plain_forest" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-219.5, 96.4),[]), # rt_forest = 10
  ("pointer_z_0_snow_forest"  ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-219.5, 81.1),[]), # rt_snow_forest = 12
  ("pointer_z_0_desert_forest","_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-219.5, 64.9),[]), # rt_desert_forest = 13


  # advanced camps placements (if not enough, spawn around camplace1)
  # south-from-beorn places
  ("camplace_N1" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-19.8,-170),[]),
  ("camplace_N2" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-24,-176),[]),
  ("camplace_N3" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-18,-165),[]),
  ("camplace_N4" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-7.7,-166),[]),
  ("camplace_N5" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,( -8,-171),[]),
  # east-from-fangorn places
  ("camplace_M1" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(5.2,-76.1),[]),
  ("camplace_M2" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(6.1,-95),[]),
  ("camplace_M3" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-1.7,-72),[]),
  ("camplace_M4" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-6.1,-60),[]),
  ("camplace_M5" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(13.6,-93),[]),
  # anorien places
  ("camplace_S1" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-44.6,6.5),[]),
  ("camplace_S2" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-36.56,0.75),[]),
  ("camplace_S3" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-44.41,0.88),[]),
  ("camplace_S4" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-42.7,9.2),[]),
  ("camplace_S5" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-29.84,3.32),[]),
  ("ancient_ruins","Ancient_Ruins",icon_ancient_ruins|pf_hide_defenders|pf_is_static|pf_always_visible|pf_label_small|pf_disabled, no_menu, pt_none,fac_guldur,0,ai_bhvr_hold,0,(-35, -125),[],170),
# mirkwood forest adornments 
  ("shrubbery1" ,"_" ,icon_shrubbery|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-40,-175),[],185),
  ("shrubbery2" ,"_" ,icon_shrubbery|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-51.5,-132.5),[],185),
  ("shrubbery3" ,"_" ,icon_shrubbery|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-55.6,-128.1),[],185),
  ("shrubbery4" ,"_" ,icon_shrubbery|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-47.54,-136.2),[],185),
  ("shrubbery5" ,"_" ,icon_shrubbery|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-45.75,-141.8),[],185),
  ("shrubbery6" ,"_" ,icon_shrubbery|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-48.4,-149.05),[],135),
  ("shrubbery7" ,"_" ,icon_shrubbery|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-52.14,-154.45),[],195),
  ("shrubbery8" ,"_" ,icon_shrubbery|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-55.52,-159.83),[],195),
  
# these are parties for storing routed troops
  ("routed_troops" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(0,0),[]),
  ("routed_allies" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(0,0),[]),
  ("routed_enemies" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(0,0),[]),

# These are for tracking which troops to remove from the casualty parties
  ("save4" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(0,0),[]),
  ("save5" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(0,0),[]),
  ("save6" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(0,0),[]),
  ("save7" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(0,0),[]),
  ("save8" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(0,0),[]),
  ("save9" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(0,0),[]),
  ("save10" ,"_",pf_disabled|pf_no_label|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(0,0),[]),
  
] + parties_scribbler 
