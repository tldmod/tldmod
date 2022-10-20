from ID_factions import *
from ID_items import *
from ID_map_icons import *
from ID_meshes import *
from ID_parties import *
from ID_party_templates import *
from ID_quests import *
from ID_scenes import *
from ID_scene_props import *
from ID_sounds import *
from ID_strings import *
from ID_tableau_materials import *
from ID_troops import *

from header_item_modifiers import *
from header_common import *
from header_music import *
from header_troops import *
from module_info import wb_compile_switch as is_a_wb_constant
##############################################################
# These constants are used in various files.
# If you need to define a value that will be used in those files,
# just define it here rather than copying it across each file, so
# that it will be easy to change it if you need to.
##############################################################

########################################################
##  ITEM SLOTS             #############################
########################################################

race_names = (
 "@man","@woman","@gondor","@rohan","@dunlander","@orc","@urukhai", "@uruk","@haradrim","@dwarf","@troll","@dunedain","@lothlorien","@rivendell","@mirkwood","@evil_man",
)

not_enough_rp = "^^[not enough Resource Points]"
earned_reg14_rp_of_s14 = "^^[earned {reg14} Resource Points of {s14}]"
earned_reg14_times_reg15_rp_of_s14 = "^^[earned {reg14}x{reg15} Resource Points of {s14}]"
promise_reg14_rp_of_s14 = "^^[you will earn {reg14} Resource Points of {s14}]"
spend_reg14_inf_on_reg15 = " [costs {reg14}/{reg15} Influence]"
costs_reg14_inf_with_s14 = " [costs {reg14} Influence with {s14}]"
## SUBFACTIONS INDICES
############

subfac_regular = 0  # the capital (Gondor or Rohan)

# of Gondor
subfac_pelargir = 1
subfac_dol_amroth = 2
subfac_ethring = 3
subfac_lossarnach = 4
subfac_pinnath_gelin = 5
subfac_blackroot = 6
subfac_rangers = 7

# of Rohan (used only for regions)
subfac_east_emnet = 1
subfac_west_emnet = 2
subfac_eastfold = 3
subfac_westfold = 4
subfac_hornburg = 5


## REGIONS INDICES -- just geographical regions...
##############

# six regions of Gondor, each linked to a fiefdom (same order as subfactions)
region_pelennor = 0   # subfac_regular, i.e. minas thirit region,
region_lebennin = 1 #subfac_pelargir = 1
region_befalas = 2  #subfac_dol_amroth = 2
region_ringlo = 3    #subfac_ethring = 3
region_lossarnach = 4 # subfac_lossarnach = 4
region_green_hills = 5  #subfac_pinnath_gelin = 5
region_lamedon = 6  #subfac_blackroot = 6

region_n_ithilien = 7   # subfac_rangers = 7
region_c_ithilien = 8 
region_s_ithilien = 9
region_druadan_forest = 10
region_firien_wood = 11
region_anorien = 12

# four Rohan regions, one for each "subfaction"
region_harrowdale = 13   # subfac_regular, edoras region
region_east_emnet = 14  # subfac_east_emnet
region_west_emnet = 15  # subfac_west_emnet
region_eastfold = 16 # subfac_estfold
region_westfold = 17 # subfac_westfold
region_hornburg = 18 # subfac_hornburg

region_the_wold = 19
region_gap_of_rohan = 20
region_entwash = 21
region_wetwang = 22
region_dead_marshes = 23
region_isengard = 24
region_fangorn = 25
region_brown_lands = 26
region_dagorlad = 27
region_n_undeep = 28
region_s_undeep = 29
region_emyn_muil = 30 
region_misty_mountains = 31
region_lorien = 32
region_anduin_banks = 33
region_n_mirkwood = 34
region_s_mirkwood = 35
region_c_mirkwood = 36 #replaces previously unused region
region_grey_mountains = 37
region_mordor = 38
region_dimrill = 39 #InVain
region_s_erebor = 40 #InVain
region_rhun = 41
region_erebor = 42
region_celebrant = 43
region_gladden_fields = 44
region_w_emyn_muil = 45
region_s_misty_mountains = 46
region_n_anduin_vale = 47
region_s_anduin_vale = 48
region_cair_andros = 49

slot_item_is_checked              = 0
slot_item_food_bonus              = 1
slot_item_book_reading_progress   = 2
slot_item_book_read               = 3
slot_item_intelligence_requirement= 4
slot_item_faction                 = 5 # additional item slot for culture-specific shop inventories
slot_item_text                    = 6 # for future use, links to text string
slot_item_subfaction              = 7 # parties and troops and items can have one subfaction -- gondor fiefdoms(mtarini)

slot_item_given_as_reward         = 8 # 0 or 1, used to check if item was already given as a reward

slot_item_strength_bonus          = 9 # 0 or 1, used to check if strength bonus was already applied by this item
slot_item_agility_bonus           = 10 # 0 or 1, used to check if agility bonus was already applied by this item
slot_item_intelligence_bonus      = 11 # 0 or 1, used to check if intelligence bonus was already applied by this item
slot_item_charisma_bonus          = 12 # 0 or 1, used to check if charisma bonus was already applied by this item

slot_item_is_active               = 13 # 0 or 1
slot_item_deactivation_hour       = 14 # Hour when the item will be deactivated (and possibly destroyed)

# CC: For octo's defiled armor.
slot_item_tableau_0		  = 0
slot_item_tableau_1		  = 1
slot_item_tableau_2		  = 2
slot_item_tableau_3		  = 3
slot_item_tableau_4		  = 4
slot_item_tableau_5		  = 5
slot_item_tableau_6		  = 6
slot_item_tableau_7		  = 7

#Kham - Item Slots for Weapon check

slot_item_needs_two_hands	= 41
slot_item_length	        = 42
slot_item_speed	            = 43
slot_item_thrust_damage	= 44
slot_item_swing_damage	= 45
slot_item_couchable     = 46
slot_item_pike          = 47

slot_item_head_armor	= slot_item_needs_two_hands
slot_item_body_armor	= slot_item_thrust_damage
slot_item_leg_armor	    = slot_item_swing_damage

slot_item_horse_speed	= slot_item_needs_two_hands
slot_item_horse_armor	= slot_item_thrust_damage
slot_item_horse_charge	= slot_item_swing_damage

########################################################
##  AGENT SLOTS            #############################
########################################################

slot_agent_target_entry_point     = 0 #for town walkers and siege archer reinforcements
slot_agent_target_x_pos           = 1
slot_agent_target_y_pos           = 2
slot_agent_is_alive_before_retreat= 3
slot_agent_is_in_scripted_mode    = 4
slot_agent_is_not_reinforcement   = 5
slot_agent_tournament_point       = 6
slot_agent_knocked_down			  = slot_agent_tournament_point # Use for tracking Knockbacks - Kham
slot_agent_arena_team_set         = 7
slot_agent_map_overlay_id         = 10
# slot_agent_target_entry_point     = 11 #duplicate
slot_agent_walker_type            = 12 # 1= civilians; 2=patrols; 3=messengers
slot_agent_last_knockdown_time    = slot_agent_walker_type #Use for tracking Knockbacks    

# TLD

slot_agent_troll_swing_status     	= 13
slot_agent_troll_swing_move       	= 14
slot_agent_last_hp		        = 15
slot_agent_mount_side		       	= 16 # a mount has the side as its rider
slot_agent_mount_dead			= 17
slot_agent_time_counter			= 18
slot_agent_routed			= 19
slot_agent_mount			= 20 
slot_agent_rallied			= 21 # Commanders use this slot to remember they've rallied their troops.
slot_agent_alive			= 22 
slot_agent_wounded			= 23 
#swy-- keep a reference in the mount of its original rider for the lone_wargs mechanic
#   -- so that we can check if the rider is unmounted but alive
#   -- (the player can order it and it bugs out the mechanic due to an unhadled case)
slot_agent_mount_orig_rider = 24

# why not use duplicate slots for an agent that will never use it? -CC

slot_agent_warg_pouncing		= 13
slot_agent_warg_pounce_time		= 14

# Kham 
slot_agent_is_running_away		= 25

#InVain
slot_agent_base_accuracy		= 26 #used for resetting accuracy after unquipping shields

########################################################
##  FACTION SLOTS          #############################
########################################################

slot_faction_mask                   = 3 #bitmask
slot_faction_ai_state               = 4
slot_faction_ai_object              = 5
slot_faction_ai_last_offensive_time = 6
slot_faction_marshall               = 7
slot_faction_ai_offensive_max_followers = 8

slot_faction_culture              = 9
slot_faction_leader               = 10
##slot_faction_vassal_of            = 11

slot_faction_number_of_parties    = 20
slot_faction_state                = 21
slot_faction_scripted_until      = 22 #scripted AI mode blocks regular calculations, slot stores campaign hours

slot_faction_player_alarm         = 30
slot_faction_last_mercenary_offer_time = 31

slot_faction_tier_1_troop         = 41
slot_faction_tier_2_troop         = 42
slot_faction_tier_3_troop         = 43
slot_faction_tier_4_troop         = 44
slot_faction_tier_5_troop         = 45
slot_faction_deserter_troop       = 48
slot_faction_guard_troop          = 49
slot_faction_rider_troop            = 50
slot_faction_archer_troop         = 51
slot_faction_castle_guard_troop   = 52
slot_faction_ranged_troop 		  = 53 #Kham Addition for quests
slot_faction_troll_troop		  = 54 #Kham Addition for Hireable Trolls

slot_faction_has_rebellion_chance = 60

# TLD Player Reward system
# Player's stat per faction
slot_faction_influence = 70
slot_faction_rank = 71
slot_faction_respoint = 72


#slot_faction_deserter_party_template       = 62

slot_faction_reinforcements_a        = 77
slot_faction_reinforcements_b        = 78
slot_faction_reinforcements_c        = 79

slot_faction_num_armies              = 80
slot_faction_num_castles             = 81
slot_faction_num_towns               = 82


##################################
# TLD War System faction (foxyman)
#

#MV: these two used for tracking strength gain/loss for balancing purposes, not needed for release
slot_faction_debug_str_gain         = 148
slot_faction_debug_str_loss         = 149

slot_faction_strength               = 150 # strength 0-8000, was 9995
slot_faction_party_map_banner		= 151
slot_faction_hosts                  = 152 # number of alive hosts
slot_faction_strength_tmp           = 153 # strength changes from killed parties enter here first, then processed through onmap trigger each hour (to make messages work ok)
slot_faction_capital                = 154 # capital city of faction, king resides and heros would respawn here
slot_faction_prisoner_train         = 155
#
# TLD War System end (foxyman)
slot_faction_rumors_begin           = 156
slot_faction_rumors_end             = 157

# TLD War System begin(matrini)
slot_faction_side          = 158  # side_good, side_eye, or side_hand
slot_faction_home_theater  = 159  # theater_SW, theater_SE, theater_C, theater_N
slot_faction_active_theater= 160  # theater_SW, theater_SE, theater_C, theater_N #MV
slot_faction_advance_camp  = 161  # MV: advance camp party
slot_faction_advcamp_timer = 162  # MV: used to time establishing an advance camp (3+ days)
# TLD War System end (matrini)
slot_faction_ambient_sound_day    = 170
slot_faction_ambient_sound_always = 171
slot_faction_occasional_sound1_day = 173
slot_faction_occasional_sound2_day = 174
slot_faction_occasional_sound3_day = 175
slot_faction_occasional_sound1_night = 176
slot_faction_occasional_sound2_night = 177
slot_faction_occasional_sound3_night = 178

slot_faction_temp_value = 179 # temp values used for various scripts
slot_faction_guardian_party = 180 # keeps the party ID of the guardian party, spawned when the faction is dying

# slots for stealth missions companion tracking
slot_fcomp_troopid = 1
slot_fcomp_agentid = 2
slot_fcomp_hp      = 3
slot_fcomp_kia     = 4

##################################


########################################################
##  PARTY SLOTS            #############################
########################################################
slot_party_type                = 0  #spt_caravan, spt_town, spt_castle
slot_party_victory_value       = 1  #TLD, subtract from faction strength when defeated
slot_party_retreat_flag        = 2
slot_party_ignore_player_until = 3
slot_party_ai_state            = 4
slot_mound_state               = 4  #TLD
slot_camp_place_occupied       = 4  #TLD
slot_party_ai_object           = 5
slot_mound_killer_faction      = 5  #TLD

slot_town_belongs_to_kingdom   = 6
slot_town_lord                 = 7
slot_party_ai_substate         = 8
slot_town_claimed_by_player    = 9

slot_cattle_driven_by_player = slot_town_lord #hack

slot_town_center        = 10
slot_town_castle        = 11
slot_town_prison        = 12
slot_town_tavern        = 13
slot_town_store         = 14
slot_town_arena         = 16
slot_town_alley         = 17
slot_town_walls         = 18
#slot_center_culture     = 19
slot_center_visited     = 19 #TLD entry spawn conditions
slot_town_captain       = 20
slot_town_weaponsmith   = 21
#slot_town_armorer       = 22 #TLD all gear in smiths
slot_town_merchant      = 23
#slot_town_horse_merchant= 24 #TLD all goods & horses in merchants
slot_town_elder         = 25
slot_center_player_relation = 26

slot_center_siege_with_belfry = 27 #unused in TLD
#slot_barracks_visited    = 27
slot_center_last_taken_by_troop = 28

# party will follow this party if set:
slot_party_commander_party = 30 #default -1
slot_party_following_player    = 31
slot_party_follow_player_until_time = 32
slot_party_dont_follow_player_until_time = 33

slot_weaponsmith_visited = 34 # TLD center visiting flags, overlap with unused village ones
slot_merchant_visited    = 35
slot_elder_visited       = 36
slot_castle_visited      = 37
slot_barracks_visited    = 38

slot_village_raided_by        = 34 #unused in TLD
slot_village_state            = 35 #unused in TLD, svs_normal, svs_being_raided, svs_looted, svs_recovering, svs_deserted
slot_village_raid_progress    = 36 #unused in TLD
slot_village_recover_progress = 37 #unused in TLD
slot_village_smoke_added      = 38 # used for ruins smoking after destruction
slot_village_infested_by_bandits   = 39 #TLD: not used

slot_town_menu_background     = 40 #TLD menu background picture

slot_center_last_player_alarm_hour = 42

slot_village_land_quality          = 44
slot_village_number_of_cattle      = 45
slot_village_player_can_not_steal_cattle = 46

slot_center_accumulated_rents      = 47
slot_center_accumulated_tariffs    = 48
slot_town_wealth        = 49
slot_town_prosperity    = 50
slot_town_player_odds   = 51


slot_party_last_toll_paid_hours = 52
slot_party_food_store           = 53 #used for sieges
slot_center_is_besieged_by      = 54 #used for sieges
slot_center_last_spotted_enemy  = 55

slot_party_cached_strength      = 56
slot_party_nearby_friend_strength = 57
slot_party_nearby_enemy_strength = 58
slot_party_follower_strength = 59

slot_town_recruits_pt             = 60
slot_center_original_faction      = 61
slot_center_ex_faction            = 62

slot_party_follow_me              = 63
slot_center_siege_begin_hours     = 64 #used for sieges
slot_center_siege_hardness        = 65

slot_town_volunteer_pt            = 66 # mtarini: each town has one volunteer party
slot_party_subfaction             = 67 # parties and troops and items can have one subfaction -- gondor fiefdoms(mtarini)


slot_castle_exterior    = slot_town_center

#slot_town_rebellion_contact   = 76
#trs_not_yet_approached  = 0
#trs_approached_before   = 1
#trs_approached_recently = 2

argument_none    = 0
argument_claim   = 1
argument_ruler   = 2
argument_benefit = 3
argument_victory = 4

slot_town_rebellion_readiness = 77
#(readiness can be a negative number if the rebellion has been defeated)

slot_town_arena_melee_mission_tpl = 78
slot_town_arena_torny_mission_tpl = 79
slot_town_arena_melee_1_num_teams = 80
slot_town_arena_melee_1_team_size = 81
slot_town_arena_melee_2_num_teams = 82
slot_town_arena_melee_2_team_size = 83
slot_town_arena_melee_3_num_teams = 84
slot_town_arena_melee_3_team_size = 85
slot_town_arena_melee_cur_tier    = 86
##slot_town_arena_template	  = 87

slot_center_npc_volunteer_troop_type   = 90
slot_center_npc_volunteer_troop_amount = 91
slot_center_mercenary_troop_type  = 90
slot_center_mercenary_troop_amount= 91
slot_center_volunteer_troop_type  = 92
slot_center_volunteer_troop_amount= 93

#slot_center_companion_candidate   = 94
slot_center_ransom_broker         = 95
slot_center_tavern_traveler       = 96
slot_center_traveler_info_faction = 97
slot_center_tavern_bookseller     = 98
slot_center_tavern_minstrel       = 99

num_party_loot_slots    = 5
slot_party_next_looted_item_slot  = 109
slot_party_looted_item_1          = 110
slot_party_looted_item_2          = 111
slot_party_looted_item_3          = 112
slot_party_looted_item_4          = 113
slot_party_looted_item_5          = 114
slot_party_looted_item_1_modifier = 115
slot_party_looted_item_2_modifier = 116
slot_party_looted_item_3_modifier = 117
slot_party_looted_item_4_modifier = 118
slot_party_looted_item_5_modifier = 119

slot_village_bound_center         = 120
slot_village_market_town          = 121
slot_village_farmer_party         = 122
slot_party_home_center            = 123

slot_center_current_improvement   = 124
slot_center_improvement_end_hour  = 125

slot_center_has_manor            = 130 #village
slot_center_has_fish_pond        = 131 #village
slot_center_has_watch_tower      = 132 #village
slot_center_has_school           = 133 #village
slot_center_has_messenger_post   = 134 #town, castle, village
slot_center_has_prisoner_tower   = 135 #town, castle

village_improvements_begin = slot_center_has_manor
village_improvements_end          = 135

walled_center_improvements_begin = slot_center_has_messenger_post
walled_center_improvements_end               = 136

slot_center_has_bandits                      = 149
slot_town_has_tournament                     = 150
slot_town_tournament_max_teams               = 151
slot_town_tournament_max_team_size           = 152

slot_center_faction_when_oath_renounced      = 155

slot_center_walker_0_troop                   = 160
slot_center_walker_1_troop                   = 161
slot_center_walker_2_troop                   = 162
slot_center_walker_3_troop                   = 163
slot_center_walker_4_troop                   = 164
slot_center_walker_5_troop                   = 165
slot_center_walker_6_troop                   = 166
slot_center_walker_7_troop                   = 167
slot_center_walker_8_troop                   = 168
slot_center_walker_9_troop                   = 169

slot_center_walker_0_dna                     = 170
slot_center_walker_1_dna                     = 171
slot_center_walker_2_dna                     = 172
slot_center_walker_3_dna                     = 173
slot_center_walker_4_dna                     = 174
slot_center_walker_5_dna                     = 175
slot_center_walker_6_dna                     = 176
slot_center_walker_7_dna                     = 177
slot_center_walker_8_dna                     = 178
slot_center_walker_9_dna                     = 179

slot_center_walker_0_type                    = 180
slot_center_walker_1_type                    = 181
slot_center_walker_2_type                    = 182
slot_center_walker_3_type                    = 183
slot_center_walker_4_type                    = 184
slot_center_walker_5_type                    = 185
slot_center_walker_6_type                    = 186
slot_center_walker_7_type                    = 187
slot_center_walker_8_type                    = 188
slot_center_walker_9_type                    = 189

slot_town_trade_route_1           = 190
slot_town_trade_route_2           = 191
slot_town_trade_route_3           = 192
slot_town_trade_route_4           = 193
slot_town_trade_route_5           = 194
slot_town_trade_route_6           = 195
slot_town_trade_route_7           = 196
slot_town_trade_route_8           = 197
slot_town_trade_route_9           = 198
slot_town_trade_route_10          = 199
slot_town_trade_route_11          = 200
slot_town_trade_route_12          = 201
slot_town_trade_route_13          = 202
slot_town_trade_route_14          = 203
slot_town_trade_route_15          = 204
slot_town_trade_routes_begin = slot_town_trade_route_1
slot_town_trade_routes_end = slot_town_trade_route_15 + 1


num_trade_goods = itm_siege_supply - itm_smoked_fish
slot_town_trade_good_productions_begin       = 205
slot_town_trade_good_prices_begin            = slot_town_trade_good_productions_begin + num_trade_goods + 1

slot_center_rumor_check_begin = 200 # TLD [slot+32, slot+45] used for checking walkers already told you rumors this day

### TLD center specific guards
slot_town_guard_troop          = 250
slot_town_archer_troop   = 251
slot_town_castle_guard_troop   = 252
###

slot_town_reinforcements_a        = 253
slot_town_reinforcements_b        = 254
slot_town_reinforcements_c        = 255

#MV for TLD, next three initialized from center_list
slot_center_strength_income       = 256 # regular faction strength gain from center
slot_center_garrison_limit        = 257 # max number of troops in garrison, used to check if garrison needs reinforcements
slot_center_destroy_on_capture    = 258 # 0 - leave it alone as in Native; 1 - disable it (leave vanilla ruins ); 2 - disable it (leave debris) 3 - RAZE IT!)
slot_center_theater               = 259 # theater_SW, theater_SE, theater_C, theater_N - initialized on start from faction theater
slot_center_destroyed             = 260 # 0 - normal, 1 - destroyed, skip it in iterations
slot_center_siegability           = 261 # see tld_siegable_X values

#for holding ws_party_spawns_list values
slot_center_spawn_scouts          = 265
slot_center_spawn_raiders         = 266
slot_center_spawn_patrol          = 267
slot_center_spawn_caravan         = 268

#for sounds
slot_center_ambient_sound_day    = 270
slot_center_ambient_sound_always = 271
slot_center_occasional_sound1_day = 273
slot_center_occasional_sound2_day = 274
slot_center_occasional_sound3_day = 275
slot_center_occasional_sound1_night = 276
slot_center_occasional_sound2_night = 277
slot_center_occasional_sound3_night = 278

#slot_party_type values
#spt_ruined_center      = 1 # TLD
spt_castle             = 2
spt_town               = 3
spt_village            = 4
spt_forager            = 5
spt_war_party          = 6
spt_patrol             = 7
spt_messenger          = 8
spt_raider             = 9
spt_scout              = 10
spt_kingdom_caravan    = 11
spt_prisoner_train     = 12
spt_kingdom_hero_party = 13 # TLD hosts
spt_kingdom_hero_alone = 14 # TLD heros w/o hosts atm
spt_guardian           = 15
spt_ship               = 16
spt_cattle_herd        = 17
spt_bandit             = 18 #WTH, native doesn't have a spt for bandits?! (TLD foxyman)
#spt_deserter           = 20

kingdom_party_types_begin = spt_patrol
kingdom_party_types_end = spt_guardian + 1

#slot_faction_state values
sfs_active                     = 0
sfs_defeated                   = 1
sfs_inactive                   = 2
sfs_inactive_rebellion         = 3
sfs_beginning_rebellion        = 4


#slot_faction_ai_state values
sfai_default                   = 0
sfai_gathering_army            = 1
sfai_attacking_center          = 2
sfai_raiding_village           = 3
sfai_attacking_enemy_army      = 4
sfai_attacking_enemies_around_center = 5
#Rebellion system changes begin
sfai_nascent_rebellion          = 6
#Rebellion system changes end

#slot_party_ai_state values
spai_undefined                  = -1
spai_besieging_center           = 1
spai_patrolling_around_center   = 4
spai_raiding_around_center      = 5 #MV: disabled for TLD
##spai_raiding_village            = 6
spai_holding_center             = 7
##spai_helping_town_against_siege = 9
spai_engaging_army              = 10
spai_accompanying_army          = 11
spai_trading_with_town          = 13
spai_retreating_to_center       = 14
##spai_trading_within_kingdom     = 15
spai_recruiting_troops          = 16 #MV: disabled for TLD

#slot_village_state values
svs_normal                      = 0
svs_being_raided                = 1
svs_looted                      = 2
svs_recovering                  = 3
svs_deserted                    = 4
svs_under_siege                 = 5

#$g_player_icon_state values
pis_normal                      = 0
pis_camping                     = 1
pis_ship                        = 2


########################################################
##  SCENE SLOTS            #############################
########################################################
slot_scene_visited              = 0
slot_scene_belfry_props_begin   = 10

########################################################
##  SCENE PROP SLOTS            #############################
########################################################
scene_prop_open_or_close_slot             = 0 #0= closed, 1=open, 2=destroyed
slot_gate_aggravator                      = 1 #stores agent_no of assigned gate aggravator

########################################################
##  TROOP SLOTS            #############################
########################################################

slot_troop_wound_mask          = 1 # TLD heroes wounds and death system
wound_arm   = 0x001
wound_leg   = 0x002
wound_head  = 0x004
wound_chest = 0x008
wound_death = 0x010

slot_troop_occupation          = 2  # 0 = free, 1 = merchant
### Troop occupations slot_troop_occupation
slto_kingdom_hero      = 2
slto_player_companion  = 3
#slto_kingdom_lady      = 4
slto_kingdom_seneschal = 5
slto_robber_knight     = 6
slto_retirement        = 11
stl_unassigned          = -1
stl_reserved_for_player = -2
stl_rejected_by_player  = -3



slot_troop_state               = 3  
slot_troop_last_talk_time      = 4
slot_troop_met                 = 5
slot_troop_party_template      = 6
slot_troop_renown              = 7
slot_troop_prisoner_of_party   = 8  # important for heroes only
slot_troop_wounded             = 9  # TLD, for tracking wounded in current battle 
slot_troop_leaded_party        = 10 # important for kingdom heroes only
slot_troop_wealth              = 11 # important for kingdom heroes only (in TLD, only used for Zigurphel)
slot_troop_respawn_timer       = 11 # TLD, for tracking hero respawn
slot_troop_cur_center          = 12 # important for royal family members only (non-kingdom heroes)

slot_troop_banner_scene_prop   = 13 # important for kingdom heroes and player only

slot_troop_original_faction    = 14 # for pretenders

slot_troop_loyalty              = 15
slot_troop_player_order_state   = 16
slot_troop_player_order_object  = 17
slot_troop_rumor_check          = 18 # TLD if 1: troop already told player a rumor this day
slot_troop_present_at_event    = 19
slot_troop_does_not_give_quest = 20
#@ slot_troop_player_debt         = 21   # NOT USED in TLD
slot_troop_player_relation     = 22
slot_companion_agent_id        = 23 #TLD, tracks companion agent in battle 
slot_troop_last_quest          = 24
slot_troop_last_quest_betrayed = 25
slot_troop_last_persuasion_time= 26
slot_troop_last_comment_time   = 27
slot_troop_spawned_before      = 28
slot_troop_last_comment_slot   = 29

slot_troop_trainer_met                       = 30
slot_troop_trainer_waiting_for_result        = 31 #used in TLD
slot_troop_trainer_training_result           = 32 #used in TLD
slot_troop_trainer_training_mode             = 33 #used in TLD
slot_troop_trainer_num_opponents_to_beat     = 34 #used in TLD
slot_troop_trainer_opponent_troop            = 35
slot_troop_trainer_training_difficulty       = 36

slot_lord_reputation_type     = 37
slot_troop_change_to_faction          = 38
slot_troop_readiness_to_join_army     = 39
slot_troop_readiness_to_follow_orders = 40

## TLD Penalties system slot(foxyman)
slot_troop_prof_night_penalties_begin = 41
slot_troop_prof_night_penalties_end   = slot_troop_prof_night_penalties_begin+6 # = 47

# TLD Player Reward system
slot_troop_upkeep_not_paid = 48 # if 1: player didn't pay upkeep for troops of this type in his party: (mtarini)
slot_troop_subfaction      = 49 # parties and troops and items can have one subfaction -- gondor fiefdoms(mtarini)
slot_troop_player_reserve_party = 50

#TLD equipment tracking
slot_troop_armor_type = 51
slot_troop_boots_type = 52
slot_troop_horse_type = 53
#TLD number of items in a shop:food,goods
slot_troop_shop_gold   = 56
slot_troop_shop_food   = 57

# NPC-related constants
slot_troop_first_encountered          = 58
slot_troop_home                       = 59

slot_troop_morality_state       = 60



tms_no_problem         = 0
tms_acknowledged       = 1
tms_dismissed          = 2

slot_troop_morality_type = 61
tmt_aristocratic = 1
tmt_egalitarian = 2
tmt_humanitarian = 3
tmt_honest = 4
tmt_pious = 5
slot_troop_morality_value = 62
slot_troop_2ary_morality_type  = 63
slot_troop_2ary_morality_state = 64
slot_troop_2ary_morality_value = 65
slot_troop_morality_penalties =  66 ### accumulated grievances from morality conflicts

slot_troop_personalityclash_object     = 67
#(0 - they have no problem, 1 - they have a problem)
slot_troop_personalityclash_state    = 68 #1 = pclash_penalty_to_self, 2 = pclash_penalty_to_other, 3 = pclash_penalty_to_other,
pclash_penalty_to_self  = 1
pclash_penalty_to_other = 2
pclash_penalty_to_both  = 3
#(a string)
slot_troop_personalityclash2_object   = 69
slot_troop_personalityclash2_state    = 70

slot_troop_personalitymatch_object   =  71
slot_troop_personalitymatch_state   =  72

slot_troop_personalityclash_penalties = 73 ### accumulated grievances from personality clash

slot_troop_home_speech_delivered = 74

slot_troop_last_complaint_hours = 75 #TLD: last time complained about his faction being demolished

#NPC history slots
slot_troop_met_previously      = 80
slot_troop_turned_down_twice   = 81

slot_troop_playerparty_history = 82
pp_history_scattered         = 1
pp_history_dismissed         = 2
pp_history_quit              = 3
pp_history_indeterminate     = 4

slot_troop_playerparty_history_string   = 83
slot_troop_return_renown        = 84

slot_troop_custom_banner_bg_color_1      = 85
slot_troop_custom_banner_bg_color_2      = 86
slot_troop_custom_banner_charge_color_1  = 87
slot_troop_custom_banner_charge_color_2  = 88
slot_troop_custom_banner_charge_color_3  = 89
slot_troop_custom_banner_charge_color_4  = 90
slot_troop_custom_banner_bg_type         = 91
slot_troop_custom_banner_charge_type_1   = 92
slot_troop_custom_banner_charge_type_2   = 93
slot_troop_custom_banner_charge_type_3   = 94
slot_troop_custom_banner_charge_type_4   = 95
slot_troop_custom_banner_flag_type       = 96
slot_troop_custom_banner_num_charges     = 97
slot_troop_custom_banner_positioning     = 98
slot_troop_custom_banner_map_flag_type   = 99

#conversation strings -- must be in this order!
slot_troop_intro = 101

slot_troop_intro_response_1 = 102
slot_troop_intro_response_2 = 103

slot_troop_backstory_a = 104
slot_troop_backstory_b = 105
slot_troop_backstory_c = 106

slot_troop_backstory_delayed = 107

slot_troop_backstory_response_1 = 108
slot_troop_backstory_response_2 = 109

slot_troop_signup   = 110
slot_troop_signup_2 = 111

slot_troop_signup_response_1 = 112
slot_troop_signup_response_2 = 113

slot_troop_mentions_payment = 114
#slot_troop_payment_response = 115
slot_troop_morality_speech   = 116
slot_troop_2ary_morality_speech = 117
slot_troop_personalityclash_speech = 118
slot_troop_personalityclash_speech_b = 119
slot_troop_personalityclash2_speech = 120
slot_troop_personalityclash2_speech_b = 121
slot_troop_personalitymatch_speech = 122
slot_troop_personalitymatch_speech_b = 123
slot_troop_retirement_speech = 124 #Not actually used
slot_troop_rehire_speech = 125
slot_troop_home_intro           = 126
slot_troop_home_description    = 127
slot_troop_home_description_2 = 128
slot_troop_home_recap         = 129
slot_troop_honorific   = 130
slot_troop_strings_end = 131
slot_troop_payment_request = 132
slot_troop_rank_request = 133 #TLD: faction rank needed to hire a NPC companion

slot_troop_flags       = 134 # the original flags defined for troops, including item guarantees (mtarini)

slot_troop_routed_us 		= 135
slot_troop_routed_allies 	= 136
slot_troop_routed_enemies 	= 137

# WEAPON MERCHANT ITP AVAILABILITY SLOTS -- warband only (=troop slots)

#swy-- we use the slot range from [138 + 0x2 = 140] to [138 + 0x0f = 153] of the dummy 'trp_skill2item_type' troop
#      for storing the number of available items of each type for the weapon merchant refresh trigger, in WB.
slot_troop_shop_aval_itp_counter_base = 138

from header_items import *

slot_troop_shop_aval_itp_itp_type_one_handed_wpn = slot_troop_shop_aval_itp_counter_base + itp_type_one_handed_wpn # 140
slot_troop_shop_aval_itp_itp_type_two_handed_wpn = slot_troop_shop_aval_itp_counter_base + itp_type_two_handed_wpn # 141
slot_troop_shop_aval_itp_itp_type_polearm        = slot_troop_shop_aval_itp_counter_base + itp_type_polearm        # 142
slot_troop_shop_aval_itp_itp_type_arrows         = slot_troop_shop_aval_itp_counter_base + itp_type_arrows         # 143
slot_troop_shop_aval_itp_itp_type_bolts          = slot_troop_shop_aval_itp_counter_base + itp_type_bolts          # 144
slot_troop_shop_aval_itp_itp_type_shield         = slot_troop_shop_aval_itp_counter_base + itp_type_shield         # 145
slot_troop_shop_aval_itp_itp_type_bow            = slot_troop_shop_aval_itp_counter_base + itp_type_bow            # 146
slot_troop_shop_aval_itp_itp_type_crossbow       = slot_troop_shop_aval_itp_counter_base + itp_type_crossbow       # 147
slot_troop_shop_aval_itp_itp_type_thrown         = slot_troop_shop_aval_itp_counter_base + itp_type_thrown         # 148
slot_troop_shop_aval_itp_itp_type_goods          = slot_troop_shop_aval_itp_counter_base + itp_type_goods          # 149
slot_troop_shop_aval_itp_itp_type_head_armor     = slot_troop_shop_aval_itp_counter_base + itp_type_head_armor     # 150
slot_troop_shop_aval_itp_itp_type_body_armor     = slot_troop_shop_aval_itp_counter_base + itp_type_body_armor     # 151
slot_troop_shop_aval_itp_itp_type_foot_armor     = slot_troop_shop_aval_itp_counter_base + itp_type_foot_armor     # 152
slot_troop_shop_aval_itp_itp_type_hand_armor     = slot_troop_shop_aval_itp_counter_base + itp_type_hand_armor     # 153

#swy-- used exclusively for the player, should be a global var,
#      but the game doesn't update them/read them well inside
#      hardcoded callback scripts such as <game_get_upgrade_cost>
slot_troop_forbid_companion_upgrade_mode = 139

# TRAIT SLOTS (=troop slots)
tld_first_trait_string = "str_trait_title_elf_friend"

slot_trait_elf_friend        = 1
slot_trait_gondor_friend     = 2
slot_trait_rohan_friend      = 3
slot_trait_brigand_friend    = 4
slot_trait_blessed           = 5
slot_trait_reverent          = 6
slot_trait_merciful          = 7
slot_trait_bravery           = 8
slot_trait_oathkeeper        = 9
slot_trait_oathbreaker       = 10
slot_trait_orc_pit_champion  = 11
slot_trait_despoiler         = 12
slot_trait_accursed          = 13
slot_trait_stealthy          = 14
slot_trait_berserker         = 15
slot_trait_infantry_captain  = 16
slot_trait_archer_captain    = 17
slot_trait_cavalry_captain   = 18
slot_trait_command_voice     = 19
slot_trait_foe_hammer        = 20
slot_trait_battle_scarred    = 21
slot_trait_fell_beast        = 22
slot_trait_butcher			 = 23 #Kham
slot_trait_well_travelled	 = 24 #kham
slot_trait_bear_shape        = 25 # Arsakes
slot_trait_first             = slot_trait_elf_friend
slot_trait_last              = slot_trait_bear_shape


########################################################
##  QUEST SLOTS            #############################
########################################################

slot_quest_target_center            = 1
slot_quest_target_troop             = 2
slot_quest_target_faction           = 3
slot_quest_object_troop             = 4
##slot_quest_target_troop_is_prisoner = 5
slot_quest_giver_troop              = 6
slot_quest_object_center            = 7
slot_quest_target_party             = 8
slot_quest_target_party_template    = 9
slot_quest_target_amount            = 10
slot_quest_current_state            = 11
slot_quest_giver_center             = 12
slot_quest_target_dna               = 13
slot_quest_target_item              = 14
slot_quest_object_faction           = 15

slot_quest_convince_value           = 19
slot_quest_importance               = 20
slot_quest_xp_reward                = 21
slot_quest_gold_reward              = 22
slot_quest_expiration_days          = 23
slot_quest_dont_give_again_period   = 24
slot_quest_dont_give_again_remaining_days = 25
slot_quest_rank_reward              = 26
slot_quest_giver_fac_str_effect     = 27
slot_quest_target_fac_str_effect   = 28


########################################################
##  PARTY TEMPLATE SLOTS   #############################
########################################################

# Ryan BEGIN
slot_party_template_num_killed   = 1
# Ryan END

########################################################
rel_enemy   = 0
rel_neutral = 1
rel_ally    = 2


#Talk contexts
tc_town_talk                  = 0
tc_court_talk   	          = 1
tc_party_encounter            = 2
tc_castle_gate                = 3
tc_siege_commander            = 4
tc_join_battle_ally           = 5
tc_join_battle_enemy          = 6
tc_castle_commander           = 7
tc_hero_freed                 = 8
tc_hero_defeated              = 9
tc_entering_center_quest_talk = 10
tc_back_alley                 = 11
tc_siege_won_seneschal        = 12
tc_ally_thanks                = 13
tc_tavern_talk                = 14
tc_rebel_thanks               = 15
tc_hire_troops                = 16
tc_starting_quest             = 17 #TLD
tc_make_enemy_join_player     = 18 #TLD
###tc_prisoner_talk              = 19 #TLD not used anymore
tc_troop_review_talk          = 20 #TLD
tc_improve_equipment	      = 21

tld_max_quest_distance = 100 #TLD

#Troop Commentaries begin
#Log entry types
#civilian
logent_village_raided            = 1
logent_village_extorted          = 2
logent_caravan_accosted          = 3
logent_helped_peasants           = 4 

logent_castle_captured_by_player              = 10
logent_lord_defeated_by_player                = 11
logent_lord_captured_by_player                = 12
logent_lord_defeated_but_let_go_by_player     = 13
logent_player_defeated_by_lord                = 14
logent_player_retreated_from_lord             = 15
logent_player_retreated_from_lord_cowardly    = 16
logent_lord_helped_by_player                  = 17
logent_player_participated_in_siege           = 18
logent_player_participated_in_major_battle    = 19

logent_pledged_allegiance        = 21
logent_fief_granted_village      = 22
logent_renounced_allegiance      = 23 

logent_game_start                           = 31 
logent_poem_composed                        = 32 ##Not added
logent_tournament_distinguished             = 33 ##Not added
logent_tournament_won                       = 34 ##Not added


#lord reputation type, for commentaries
#"Martial" will be twice as common as the other types
lrep_none          = 0 
lrep_martial       = 1 #chivalrous but not terribly empathetic or introspective, - eg Richard Lionheart, your average 14th century French baron
lrep_quarrelsome   = 2 #spiteful, cynical, a bit paranoid, possibly hotheaded - eg Robert Graves' Tiberius, Shakespeare's Richard III
lrep_selfrighteous = 3 #coldblooded, moralizing, often cruel - eg William the Conqueror, Timur, Octavian, Aurangzeb (although he borders on upstanding)
lrep_cunning       = 4 #coldblooded, pragmatic, amoral - eg Louis XI, Guiscard, Akbar Khan, Abd al-Aziz Ibn Saud
lrep_debauched     = 5 #spiteful, amoral, sadistic, - eg Caligula, Tuchman's Charles of Navarre
lrep_goodnatured   = 6 #chivalrous, benevolent, perhaps a little too decent to be a good warlord - eg Hussein, poss Ranjit Singh (although roguish), Humayun
lrep_upstanding    = 7 #moralizing, benevolent, pragmatic, - eg Bernard Cornwell's Alfred, Charlemagne, Sher Shah Suri

#Troop Commentaries end

#Walker types:
walkert_default            = 0
walkert_needs_money        = 1
walkert_needs_money_helped = 2
walkert_spy                = 3
num_town_walkers           = 8
town_walker_entries_start  = 32

reinforcement_cost            = 400

merchant_toll_duration        = 72 #Tolls are valid for 72 hours

hero_escape_after_defeat_chance = 100 #MV: was 80

raid_distance = 4

surnames_begin = str_surname_1
surnames_nickname_begin = str_surname_21
surnames_end = str_surnames_end
names_begin = str_name_1
names_elf_begin = str_name_elf_1
names_dwarf_begin = str_name_dwarf_1
names_orc_begin = str_name_orc_1
names_end = names_elf_begin
names_elf_end = names_dwarf_begin
names_dwarf_end = names_orc_begin
names_orc_end = surnames_begin

#countersigns_begin = "str_countersign_1"
#countersigns_end = names_begin
#secret_signs_begin = "str_secret_sign_1"
#secret_signs_end = countersigns_begin

kingdoms_begin   = fac_gondor
kingdoms_begin_i = fac_gondor
kingdoms_end     = fac_kingdoms_end
kingdoms_end_i   = fac_kingdoms_end

kingdom_heroes_begin = trp_knight_6_2       # was: trp_gondor_lord
kingdom_heroes_end   = trp_knight_6_1 + 1   # was: trp_heroes_end

heroes_begin = kingdom_heroes_begin
heroes_end   = kingdom_heroes_end

companions_begin = trp_npc1
companions_end   = trp_npc17 + 1

new_companions_begin = trp_npc18
new_companions_end = trp_npc27 + 1

soldiers_begin = trp_farmer
soldiers_end = trp_town_walker_1

tavern_minstrels_begin = trp_tavern_minstrel_1
tavern_minstrels_end   = companions_begin

tavern_travelers_begin = trp_tavern_traveler_1
tavern_travelers_end   = tavern_minstrels_begin

lord_quests_begin = "qst_deliver_message"
lord_quests_end   = "qst_follow_army"

lord_quests_begin_2 = "qst_blank_quest_01"
lord_quests_end_2	= "qst_blank_quest_06"

enemy_lord_quests_begin = lord_quests_end #no enemy lord quests at present in TLD, was "qst_lend_surgeon"
enemy_lord_quests_end   = lord_quests_end

mayor_quests_begin  = "qst_move_cattle_herd"
mayor_quests_end    = "qst_tld_introduction"

mayor_quests_begin_2 = "qst_blank_quest_16" 
mayor_quests_end_2 = "qst_blank_quest_18"

army_quests_begin = "qst_deliver_cattle_to_army"
army_quests_end   = mayor_quests_begin

all_quests_begin = 0
all_quests_end = "qst_quests_end"

centers_begin = p_town_minas_tirith
centers_end = p_centers_end

# LANDMARKS (mtarini)

# Rationale: landmarks are small places  on the map determining the battlefield . 
# In a give moment, the player is inside  a "region", and he  *can* be near a landmark (or, none). 
# Both things affect battlefield.
# Both things are described in the Action Menu

# special landmark ID(unlike all ather landmarks ID, they are not ID of parties  on the map)
landmark_great_east_road = 1001;
landmark_old_forest_road  = 1002;  # where it crosses mirkwook

# fords are landmarks
fords_begin = p_ford_cair_andros1 
fords_big_begin = p_ford_cair_andros1 
fords_big_end = p_ford_cerin_dolen
fords_small_begin = p_ford_cerin_dolen
fords_small_end = p_test_scene
fords_end = p_test_scene

# many landmarks are parties (e.g. the hand sign and minas titith outside)
landmark_begin = centers_begin
landmark_end = fords_end

# end of landmark


advcamps_begin = p_advcamp_gondor
advcamps_end   = centers_end

scenes_begin = scn_minas_tirith_center
scenes_end = scn_castle_1_exterior

regular_troops_begin       = trp_novice_fighter
regular_troops_end         = trp_ramun_the_slave_trader

training_ground_trainers_begin    = trp_trainer_gondor
training_ground_trainers_end      = trp_ransom_broker_1

spy_walkers_begin = trp_spy_walker_1
spy_walkers_end = trp_walker_man_gondor_black

weapon_merchants_begin = trp_smith_mtirith
weapon_merchants_end   = trp_barman_eastemnet

tavernkeepers_begin    = trp_barman_eastemnet
tavernkeepers_end      = trp_merchant_mtirith

horse_merchants_begin  = trp_merchant_main_rhun
horse_merchants_end    = trp_elder_mtirith

mayors_begin           = trp_elder_mtirith
mayors_end             = trp_merchants_end

average_price_factor = 1000
minimum_price_factor = 100
maximum_price_factor = 10000

scrap_bad_value = 50
scrap_medium_value = 300 
scrap_good_value = 1000

item_horse_begin = itm_sumpter_horse
item_horse_end = itm_warg_1b

item_warg_begin = itm_warg_1b
item_warg_end = itm_warg_reward+1

warg_ghost_begin = trp_warg_ghost_1b
warg_ghost_end = trp_a2_isen_uruk_tracker

trade_goods_begin = itm_human_meat #MV: was itm_smoked_fish
trade_goods_end = itm_siege_supply
food_begin = itm_human_meat
normal_food_begin = itm_smoked_fish
food_end = itm_grain

scraps_begin = itm_metal_scraps_bad
scraps_end = itm_oliphant #itm_metal_scraps_good+1

# Banner constants
banner_meshes_begin = mesh_banner_gondor
banner_meshes_end_minus_one = mesh_banner_f20

arms_meshes_begin = mesh_arms_a01
arms_meshes_end_minus_one = mesh_arms_f21

custom_banner_charges_begin = mesh_custom_banner_charge_01
custom_banner_charges_end = mesh_tableau_mesh_custom_banner

custom_banner_backgrounds_begin = mesh_custom_banner_bg
custom_banner_backgrounds_end = custom_banner_charges_begin

custom_banner_flag_types_begin = mesh_custom_banner_01
custom_banner_flag_types_end = custom_banner_backgrounds_begin

custom_banner_flag_map_types_begin = mesh_custom_map_banner_01
custom_banner_flag_map_types_end = custom_banner_flag_types_begin

custom_banner_flag_scene_props_begin = spr_custom_banner_01
custom_banner_flag_scene_props_end = spr_banner_a

custom_banner_map_icons_begin = icon_custom_banner_01
custom_banner_map_icons_end = icon_banner_126

banner_map_icons_begin = icon_mfp_gondor
banner_map_icons_end_minus_one = icon_banner_126

banner_scene_props_begin = spr_banner_a
banner_scene_props_end_minus_one = spr_banner_f20

# Some constants for merchant invenotries
merchant_inventory_space = 30
num_merchandise_goods = 3 #MV: was 40

num_forest_bandit_spawn_points = 5
num_mountain_bandit_spawn_points = 5
num_steppe_bandit_spawn_points = 2
#num_black_khergit_spawn_points = 1
num_sea_raider_spawn_points = 2

#peak_prisoner_trains = 4
#peak_kingdom_caravans = 12
#peak_kingdom_messengers = 3

# Note positions
note_troop_location = 3

#battle tactics
btactic_hold = 1
btactic_follow_leader = 2
btactic_charge = 3
btactic_stand_ground = 4

#default right mouse menu orders
cmenu_move = -7
cmenu_follow = -6

# Town center modes
tcm_default = 0
tcm_disguised = 1

# Arena battle modes
#abm_fight = 0
abm_training = 1
abm_visit = 2
abm_tournament = 3
abm_team = 4
abm_gauntlet = 5
abm_mass_melee = 6

# Camp training modes
ctm_melee    = 1
ctm_ranged   = 2
ctm_mounted  = 3
ctm_training = 4

# Village bandits attack modes
vba_normal          = 1
vba_after_training  = 2

arena_tier1_opponents_to_beat = 3
arena_tier1_prize = 5
arena_tier2_opponents_to_beat = 6
arena_tier2_prize = 10
arena_tier3_opponents_to_beat = 10
arena_tier3_prize = 25
arena_tier4_opponents_to_beat = 20
arena_tier4_prize = 60
arena_grand_prize = 250

#####################################
# TLD constants begin (foxyman)
#
debug_point_0 = (1106, "@DEBUG: Routine 0", 0xffff00ff)
debug_point_1 = (1106, "@DEBUG: Routine 1", 0xffff00ff)
debug_point_2 = (1106, "@DEBUG: Routine 2", 0xffff00ff)
debug_point_3 = (1106, "@DEBUG: Routine 3", 0xffff00ff)
debug_point_4 = (1106, "@DEBUG: Routine 4", 0xffff00ff)

debug_color = 0xff00ff

# color-coded item descriptions
color_item_text_normal  = 0xFFEEDD
color_item_text_morale  = 0x4444FF
color_item_text_bonus   = 0xE066FF
color_item_text_special = 0xEEEE00

# color-coded messages
color_good_news    = 0x50FF50
color_bad_news     = 0xFF5050
color_neutral_news = 0xFFAA00

def concatenate_scripts(block_list):
    result = []
    for block in block_list:
        result += block
    return result

tld_troops_begin = trp_player
#tld_troops_end = trp_troops_end
tld_troops_end = trp_last #This range is only called for day/night penalties. Extended to affect all troops (also heroes)
tld_player_level_to_begin_war = 8
tld_player_level_to_own_chest = 10

# TLD: influence costs for orders to lords
tld_command_cost_follow = 20
tld_command_cost_goto   = 5
tld_command_cost_patrol = 10
tld_command_cost_engage = 25
tld_command_cost_siege =  35 #marshalls only #kham - reduced from 50


####################################################
# TLD War System (foxyman and mtarini and MV) ######
####################################################

# three factions sides
faction_side_good = 0  
faction_side_eye = 1 
faction_side_hand = 2
faction_side_noside = 3 # outlaws etc

# four theaters
theater_SE = 1<<0  
theater_SW = 1<<1  
theater_C =  1<<2  
theater_N =  1<<3

evil_party_str_handicap = 50 # if the player is evil, evil parties and garrisons have this % of regular party strength (used in AI battles)

# MV: some constants for faction strength as used in the faction AI
fac_str_dying = 500 # less than this, go for the kill by sieging the capital
fac_str_very_weak = 1000 # less than this, faction capital can be sieged and faction can be destroyed by capturing the capital
fac_str_weak = 3000 # lesser or equal to this can only defend (state "weakened" or worse); faction centers can be sieged and captured
fac_str_ok = 3500 # lesser or equal can attack around enemy centers, higher can siege #Kham - Changed from 4000
fac_str_max = 8000

fac_str_guardian = 1300 # was: 1000 # less than this, spawn the guardian party

# faction ,	initial strength,culture,			faction lord,  	faction marshall,  [5 tiers of troops],			T2							t3								t4									t5									archer								troll				[reinforcement templates, prisoner trains],                                       main banner,  map party banner, [slot_faction: deserter_troop, guard_troop,				rider_troop, 					    archer_troop, 				        castle_guard_troop]					faction capital         side              home theater, advance camp
faction_init = [
(fac_gondor  ,4400,mtf_culture_gondor       ,[trp_gondor_lord  ,trp_knight_1_3    ],[trp_i1_gon_levy,     		trp_i2_gon_watchman,		trp_i3_gon_footman,       		trp_i4_gon_swordsman,          		trp_c5_gon_vet_knight, 				trp_a4_gon_archer, 								 -1],	[pt_gondor_reinf_a,  pt_gondor_reinf_b,  pt_gondor_reinf_c,  pt_gondor_p_train],  spr_banner_a, icon_mfp_gondor,  [-1,                      trp_i2_gon_watchman,        	trp_c2_gon_squire,       		    trp_a3_gon_bowman,  				trp_i6_gon_tower_swordsman],		p_town_minas_tirith,    faction_side_good,theater_SE,p_advcamp_gondor),
(fac_rohan   ,4000,mtf_culture_rohan_goodmen,[trp_rohan_lord   ,trp_rohan_lord    ],[trp_i1_rohan_youth,      	trp_c2_squire_of_rohan, 	trp_c3_rider_of_rohan,      	trp_c4_veteran_rider_of_rohan,    	trp_c6_rider_guard_of_rohan,		trp_ac3_skirmisher_of_rohan, 		 			 -1],	[pt_rohan_reinf_a,   pt_rohan_reinf_b,   pt_rohan_reinf_c,   pt_rohan_p_train],   spr_banner_b, icon_mfp_rohan,   [-1,                      trp_i2_guardsman_of_rohan,		trp_c2_squire_of_rohan,	            trp_ac3_skirmisher_of_rohan,	trp_c6_king_s_man_of_rohan],p_town_edoras,          faction_side_good,theater_SW,p_advcamp_rohan),
(fac_isengard,4500,mtf_culture_orcs         ,[trp_isengard_lord,trp_knight_1_17   ],[trp_i1_isen_orc_snaga,		trp_i2_isen_uruk, 	 		trp_i3_isen_large_uruk,			trp_i4_isen_fighting_uruk_warrior, 	trp_ac4_isen_white_hand_rider,		trp_a2_isen_uruk_tracker, 			trp_isen_troll,],	[pt_isengard_reinf_a,pt_isengard_reinf_b,pt_isengard_reinf_c,pt_isengard_p_train],spr_banner_s, icon_mfp_isengard,[trp_i2_isen_orc,     	trp_i2_isen_uruk,     	        trp_ac2_isen_wolf_rider,			trp_a2_isen_uruk_tracker,	        trp_i5_isen_fighting_uruk_champion], p_town_isengard,        faction_side_hand,theater_SW,p_advcamp_isengard),
(fac_mordor  ,4500,mtf_culture_orcs         ,[trp_mordor_lord  ,trp_knight_2_51   ],[trp_i1_mordor_orc_snaga, 	trp_i2_mordor_orc,      	trp_i3_mordor_large_orc,    	trp_i4_mordor_fell_morgul_orc,		trp_c4_mordor_great_warg_rider,		trp_a2_mordor_orc_archer, 		  trp_mordor_troll,],	[pt_mordor_reinf_a,  pt_mordor_reinf_b,  pt_mordor_reinf_c,  pt_mordor_p_train],  spr_banner_c, icon_mfp_mordor,  [trp_i1_mordor_orc_snaga, trp_i2_mordor_orc,	            trp_c3_mordor_warg_rider,			trp_a2_mordor_orc_archer,			trp_i3_mordor_uruk_slayer],			p_town_morannon,        faction_side_eye ,theater_SE,p_advcamp_mordor),
(fac_harad   ,2700,mtf_culture_harad        ,[trp_harad_lord   ,trp_harad_lord    ],[trp_i1_harad_levy,			trp_i3_harad_infantry,  	trp_c3_harondor_rider,      	trp_ac4_harondor_horse_archer,  	trp_c5_harondor_serpent_knight,		trp_a4_harad_archer, 							 -1],	[pt_harad_reinf_a,   pt_harad_reinf_b,   pt_harad_reinf_c,   -1],                 spr_banner_d, icon_mfp_harad,   [trp_i1_harad_levy,		trp_i3_harad_infantry,	        trp_c2_harondor_scout,		        trp_a3_harad_hunter,			    trp_i4_harad_spearman],				p_town_harad_camp,      faction_side_eye ,theater_SE,p_advcamp_harad),
(fac_rhun    ,3500,mtf_culture_evilmen      ,[trp_rhun_lord    ,trp_rhun_lord     ],[trp_i1_rhun_tribesman,     trp_ac2_rhun_horse_scout,	trp_c3_rhun_swift_horseman, 	trp_ac4_rhun_veteran_horse_archer, 	trp_c6_rhun_warlord, 				trp_ac3_rhun_horse_archer,						 -1],	[pt_rhun_reinf_a,    pt_rhun_reinf_b,    pt_rhun_reinf_c,    -1],                 spr_banner_f, icon_mfp_rhun,    [trp_i1_rhun_tribesman,	trp_i2_rhun_tribal_warrior,     trp_c2_rhun_horseman,			    trp_i2_rhun_tribal_warrior,			trp_c6_rhun_warlord],				p_town_rhun_main_camp, 	faction_side_eye ,theater_N ,p_advcamp_rhun),
(fac_khand   ,2100,mtf_culture_evilmen      ,[trp_khand_lord   ,trp_khand_lord    ],[trp_i1_khand_bondsman,    	trp_i2_khand_pit_dog,    	trp_i3_khand_warrior,       	trp_i4_khand_pit_champion,         	trp_c5_khand_kataphrakt,			trp_ac3_khand_skirmisher, 						 -1],	[pt_khand_reinf_a,   pt_khand_reinf_b,   pt_khand_reinf_c,   -1],                 spr_banner_e, icon_mfp_khand,   [trp_i2_khand_pit_dog,  	trp_i2_khand_pit_dog,     	    trp_c2_khand_pony_rider,			trp_i3_khand_warrior,			    trp_c3_khand_horseman],       	  	p_town_khand_camp,      faction_side_eye ,theater_SE,p_advcamp_khand),
(fac_umbar   ,2300,mtf_culture_evilmen      ,[trp_umbar_lord   ,trp_umbar_lord    ],[trp_i1_corsair_youth,    	trp_i2_corsair_warrior,  	trp_i3_corsair_swordsman,   	trp_i4_corsair_veteran_swordsman,  	trp_i5_corsair_master_swordsman,	trp_a3_corsair_marksman, 						 -1],	[pt_umbar_reinf_a,   pt_umbar_reinf_b,   pt_umbar_reinf_c,   -1],                 spr_banner_g, icon_mfp_umbar,   [trp_i2_corsair_warrior,	trp_i2_corsair_warrior,	        trp_i3_corsair_spearman,			trp_a2_corsair_marine,	            trp_i5_corsair_master_swordsman],	p_town_umbar_camp,      faction_side_eye ,theater_SE,p_advcamp_umbar),
(fac_lorien  ,4500,mtf_culture_elves        ,[trp_lorien_lord ,trp_lorien_marshall],[trp_a1_lorien_scout,    	trp_a2_lorien_warden,  		trp_a3_lorien_vet_warden,		trp_a4_lorien_gal_warden, 			trp_a5_lorien_gal_royal_warden,		trp_a1_lorien_scout, 							 -1],	[pt_lorien_reinf_a,  pt_lorien_reinf_b,  pt_lorien_reinf_c,  pt_lorien_p_train],  spr_banner_h, icon_mfp_lorien,  [-1,                      trp_i3_lorien_inf,			    trp_a2_lorien_warden,				trp_a2_lorien_archer,			    trp_a5_lorien_gal_royal_archer],	p_town_caras_galadhon,  faction_side_good,theater_C ,p_advcamp_lorien),
(fac_imladris,3300,mtf_culture_elves        ,[trp_imladris_lord,trp_imladris_lord ],[trp_a1_riv_scout,    		trp_a2_riv_vet_scout, 		trp_a3_riv_archer,				trp_a4_riv_vet_archer,				trp_ac6_riv_knight,					trp_a1_riv_scout,								 -1],	[pt_imladris_reinf_a,pt_imladris_reinf_b,pt_imladris_reinf_c,pt_imladris_p_train],spr_banner_i, icon_mfp_imladris,[-1,                      trp_i3_riv_swordbearer,			trp_ac5_riv_rider,					trp_a2_riv_vet_scout,				trp_ac6_riv_knight],         		p_town_imladris_camp,   faction_side_good,theater_C ,p_advcamp_imladris),
(fac_woodelf ,3300,mtf_culture_elves        ,[trp_woodelf_lord ,trp_woodelf_lord  ],[trp_a1_greenwood_scout,    trp_a2_greenwood_veteran_scout, trp_a3_greenwood_archer,	trp_a4_greenwood_veteran_archer,  	trp_i5_greenwood_chosen_shieldmaster,trp_a2_greenwood_veteran_scout,				 -1],	[pt_woodelf_reinf_a, pt_woodelf_reinf_b, pt_woodelf_reinf_c, pt_woodelf_p_train], spr_banner_j, icon_mfp_woodelf, [-1,                      trp_i2_greenwood_infantry,		trp_a3_greenwood_sentinel,		    trp_a2_greenwood_veteran_scout,		trp_i4_greenwood_elite_infantry],	p_town_thranduils_halls,faction_side_good,theater_N ,p_advcamp_woodelf),
(fac_moria   ,4000,mtf_culture_orcs         ,[trp_moria_lord   ,trp_moria_lord    ],[trp_i1_moria_snaga,   		trp_i2_moria_goblin,      	trp_i3_moria_large_goblin,  	trp_i4_moria_fell_goblin,   		trp_c5_moria_clan_rider,			trp_a3_moria_large_goblin_archer,  trp_moria_troll,],	[pt_moria_reinf_a,   pt_moria_reinf_b,   pt_moria_reinf_c,   -1],                 spr_banner_k, icon_mfp_moria,   [trp_i1_moria_snaga,   	trp_i2_moria_goblin,			trp_c3_moria_wolf_rider,			trp_a2_moria_goblin_archer,			trp_i4_moria_fell_goblin],			p_town_moria,           faction_side_hand,theater_C ,p_advcamp_moria),
(fac_guldur  ,3500,mtf_culture_orcs         ,[trp_guldur_lord  ,trp_guldur_lord   ],[trp_i1_guldur_orc_snaga, 	trp_a2_guldur_orc_tracker,  trp_a3_guldur_large_orc_tracker,trp_a4_guldur_fell_orc_tracker,		trp_c4_mordor_great_warg_rider,		trp_a2_guldur_orc_tracker, 		  trp_mordor_troll],	[pt_guldur_reinf_a,  pt_guldur_reinf_b,  pt_guldur_reinf_c,  -1],                 spr_banner_l, icon_mfp_guldur,  [trp_i1_guldur_orc_snaga, trp_i2_mordor_orc,		        trp_c3_mordor_warg_rider,			trp_a2_guldur_orc_tracker,	        trp_a4_guldur_fell_orc_tracker],	p_town_dol_guldur,      faction_side_eye ,theater_C ,p_advcamp_guldur),
(fac_gundabad,3500,mtf_culture_orcs         ,[trp_gundabad_lord,trp_gundabad_lord ],[trp_i1_gunda_goblin,  		trp_i2_gunda_orc,         	trp_i3_gunda_orc_fighter,   	trp_ca5_gunda_clan_skirmisher,		trp_c5_gunda_clan_rider,			trp_i4_gunda_orc_berserker, 	    trp_gunda_troll],	[pt_gundabad_reinf_a,pt_gundabad_reinf_b,pt_gundabad_reinf_c,-1],                 spr_banner_n, icon_mfp_gundabad,[trp_i1_gunda_goblin,     trp_i2_gunda_orc,				trp_c3_gunda_goblin_rider,			trp_i2_gunda_orc,			        trp_c4_gunda_warg_rider],			p_town_gundabad,        faction_side_hand,theater_N ,p_advcamp_gundabad),
(fac_dale    ,2900,mtf_culture_rohan_goodmen,[trp_dale_lord    ,trp_dale_lord     ],[trp_i1_dale_militia,       trp_a2_dale_scout,          trp_a3_dale_bowman,         	trp_a4_dale_archer,           		trp_ac5_rhovanion_marchwarden,		trp_a2_dale_scout,								 -1],	[pt_dale_reinf_a,    pt_dale_reinf_b,    pt_dale_reinf_c,    pt_dale_p_train],    spr_banner_o, icon_mfp_dale,    [-1,                      trp_i2_dale_man_at_arms,		trp_c2_rhovanion_retainer,			trp_a2_dale_scout,				    trp_i5_dale_hearthman],				p_town_dale,            faction_side_good,theater_N ,p_advcamp_dale),
(fac_dwarf   ,4000,mtf_culture_rohan_goodmen,[trp_dwarf_lord   ,trp_dwarf_lord    ],[trp_i1_dwarf_apprentice,	trp_i2_dwarf_warrior,      	trp_i3_dwarf_hardened_warrior,	trp_i4_dwarf_axeman,        		trp_i6_iron_hills_grors_guard,		trp_a4_dwarf_bowman,							 -1],	[pt_dwarf_reinf_a,   pt_dwarf_reinf_b,   pt_dwarf_reinf_c,   pt_dwarf_p_train],   spr_banner_p, icon_mfp_dwarf,   [-1,                      trp_i2_dwarf_warrior,			trp_i3_iron_hills_warrior,			trp_a3_dwarf_scout,			        trp_i6_dwarf_longbeard_axeman],		p_town_erebor,          faction_side_good,theater_N ,p_advcamp_dwarf),
(fac_dunland ,2500,mtf_culture_evilmen      ,[trp_dunland_lord ,trp_dunland_lord  ],[trp_i1_dun_wildman,     	trp_i2_dun_warrior,         trp_i3_dun_vet_warrior,     	trp_i4_dun_wolf_warrior,      		trp_i5_dun_wolf_guard,				trp_i3_dun_pikeman,								 -1],	[pt_dunland_reinf_a, pt_dunland_reinf_b, pt_dunland_reinf_c, -1],                 spr_banner_r, icon_mfp_dunland, [trp_i2_dun_warrior,    	trp_i3_dun_pikeman,				trp_ac4_dun_crebain_rider,			trp_i2_dun_warrior,					trp_i3_dun_pikeman],				p_town_dunland_camp,    faction_side_hand,theater_SW,p_advcamp_dunland),
(fac_beorn   ,3000,mtf_culture_rohan_goodmen,[trp_beorn_lord   ,trp_beorn_lord    ],[trp_i1_woodmen_man,  	 	trp_i2_woodmen_forester,    trp_i3_beorning_carrock_lookout,trp_i4_beorning_carrock_fighter,  	trp_i5_beorning_carrock_berserker,	trp_a4_woodmen_archer,							 -1],	[pt_beorn_reinf_a,   pt_beorn_reinf_b,   pt_beorn_reinf_c,   -1],                 spr_banner_m, icon_mfp_northmen,[-1,                      trp_i2_beorning_warrior,		trp_i3_beorning_carrock_lookout,	trp_a2_woodmen_tracker,				trp_i6_beorning_bear_warrior],		p_town_beorn_house,     faction_side_good,theater_N ,p_advcamp_beorn),
]

# feudal troops guarding some Gondor centers
# 0) subfaction index,1) city, 2) substring_present_in_all_troop_names, 3)[guard_troop,archer_troop,castle_guard_troop],  				5)[ reinforcements for garrisons],  								6) [leaders...]
subfaction_data= [      
 (subfac_pelargir     ,p_town_pelargir     ,"Pelargir"  ,[trp_i1_pel_watchman,		trp_a2_pel_marine,		    trp_i3_pel_vet_infantry],		[pt_pelargir_reinf_a  ,pt_pelargir_reinf_b  ,pt_pelargir_reinf_c  ],[trp_i6_pel_leader, trp_a6_pel_marine_leader,]),
 (subfac_dol_amroth   ,p_town_dol_amroth   ,"Amroth"    ,[trp_c2_amroth_squire,		trp_i2_gon_watchman,    	trp_c6_amroth_swan_knight],		[pt_dol_amroth_reinf_a,pt_dol_amroth_reinf_b,pt_dol_amroth_reinf_c],[trp_c6_amroth_leader]),
 (subfac_ethring      ,p_town_calembel     ,"Lamedon"   ,[trp_i1_lam_clansman,		trp_i2_gon_watchman,		trp_c5_lam_knight],			    [pt_lamedon_reinf_a   ,pt_lamedon_reinf_b   ,pt_lamedon_reinf_c   ],[trp_c6_lam_leader]),
 (subfac_lossarnach   ,p_town_lossarnach   ,"Lossarnach",[trp_i1_loss_woodsman,		trp_i2_gon_watchman,		trp_i5_loss_axemaster],			[pt_lossarnach_reinf_a,pt_lossarnach_reinf_b,pt_lossarnach_reinf_c],[trp_i6_loss_leader]),
 (subfac_pinnath_gelin,p_town_pinnath_gelin,"Pinnath"   ,[trp_i1_pinnath_plainsman,	trp_a2_pinnath_bowman,		trp_c3_pinnath_knight],			[pt_pinnath_reinf_a   ,pt_pinnath_reinf_b   ,pt_pinnath_reinf_c   ],[trp_c6_pinnath_leader]),
 (subfac_blackroot    ,p_town_erech        ,"Blackroot" ,[trp_a1_blackroot_hunter,	trp_a2_blackroot_bowman,	trp_a5_blackroot_shadow_hunter],[pt_blackroot_reinf_a ,pt_blackroot_reinf_b ,pt_blackroot_reinf_c ],[trp_a5_blackroot_shadow_hunter]),
 (subfac_rangers      ,p_town_henneth_annun,"Ithilien"  ,[trp_a4_ithilien_ranger,	trp_a4_ithilien_ranger,	    trp_a6_ithilien_master_ranger],	[pt_ithilien_reinf_a  ,pt_ithilien_reinf_b  ,pt_ithilien_reinf_c  ],[trp_a6_ithilien_leader]),
]


# Specify patrol/scout/raider party templates here
# Format:
# (town_id/castle_id/village_id, scout_id, raider_id, patrol_id, cavaran_id),
# Use -1 to indicate a center should not spawn such kind of party
#
ws_party_spawns_list = [
#   ("p_town_name"            ,"pt_faction_scouts",       "pt_faction_raiders",    "pt_faction_patrol",   "pt_faction_caravan"),
#Gondor    
(p_town_minas_tirith    ,pt_gondor_scouts,		pt_gondor_raiders,	pt_gondor_company,	pt_gondor_caravan),
(p_town_pinnath_gelin	,pt_pinnath_gelin_auxila,-1,				pt_pinnath_patrol,	pt_gondor_caravan),
(p_town_pelargir        ,pt_gondor_scouts,		pt_gondor_raiders,	pt_pelargir_patrol,	pt_gondor_caravan),
(p_town_linhir          ,pt_lamedon_auxila,		pt_gondor_raiders,	pt_lamedon_patrol,	pt_gondor_caravan),
(p_town_calembel        ,pt_lamedon_auxila,		pt_gondor_raiders,	pt_lamedon_patrol,	pt_gondor_caravan),
(p_town_dol_amroth      ,-1,					pt_gondor_raiders,	pt_amroth_patrol,	pt_gondor_caravan),
(p_town_edhellond       ,-1,					-1,					pt_gondor_patrol,	pt_gondor_caravan),
(p_town_lossarnach      ,pt_lossarnach_auxila,	pt_gondor_raiders,	pt_lossarnach_patrol,pt_gondor_caravan),
(p_town_tarnost         ,pt_gondor_scouts,		pt_gondor_raiders,	pt_gondor_patrol,	pt_gondor_caravan),
(p_town_erech           ,pt_blackroot_auxila,	pt_gondor_raiders,	pt_brv_patrol,		pt_gondor_caravan),
(p_town_west_osgiliath  ,pt_ranger_scouts,		pt_gondor_raiders,	-1,    				-1),
(p_town_henneth_annun   ,pt_ranger_scouts,		pt_ranger_raiders,	pt_ranger_patrol,	-1), #kham - added
(p_town_cair_andros     ,pt_gondor_scouts,		-1			   , 	-1,					pt_gondor_caravan),
#Rohan    
(p_town_edoras          ,pt_rohan_scouts,		pt_rohan_raiders,	pt_rohan_patrol,     pt_rohan_caravan),
(p_town_aldburg         ,pt_rohan_scouts,		pt_rohan_raiders,	pt_rohan_patrol,     pt_rohan_caravan),
(p_town_hornburg        ,pt_rohan_scouts,		pt_rohan_raiders,	pt_rohan_patrol,     pt_rohan_caravan),
(p_town_east_emnet      ,pt_rohan_scouts,		pt_rohan_raiders,	pt_rohan_patrol,     pt_rohan_caravan),
(p_town_westfold        ,pt_rohan_scouts,		-1,					pt_rohan_patrol,     pt_rohan_caravan),
(p_town_west_emnet      ,pt_rohan_scouts,		pt_rohan_raiders,	pt_rohan_patrol,     pt_rohan_caravan),
(p_town_eastfold        ,pt_rohan_scouts,		pt_rohan_raiders,	pt_rohan_patrol,     pt_rohan_caravan),
#Mordor   
(p_town_minas_morgul    ,pt_morgul_scouts,		pt_morgul_raiders, pt_mordor_war_party, pt_mordor_caravan),
(p_town_morannon        ,pt_mordor_scouts,		pt_mordor_raiders, pt_mordor_war_party, pt_mordor_caravan),
(p_town_east_osgiliath  ,pt_mordor_scouts,		pt_mordor_raiders, -1,                    -1),
(p_town_orc_sentry_camp ,pt_mordor_scouts,		pt_mordor_raiders, -1,                    -1),
(p_town_cirith_ungol    ,pt_mordor_scouts,		pt_mordor_raiders, -1,                    -1), #kham- added
#Isengard
(p_town_isengard        ,pt_isengard_scouts,      pt_isengard_raiders,   pt_isengard_war_party,	pt_isengard_caravan),
(p_town_urukhai_outpost ,pt_isengard_scouts_warg, pt_isengard_raiders,   pt_isengard_war_party,	pt_isengard_caravan),
(p_town_urukhai_h_camp  ,pt_isengard_scouts, 	  pt_isengard_raiders,   -1,					pt_isengard_caravan),
(p_town_urukhai_r_camp  ,pt_isengard_scouts_warg, pt_isengard_raiders,   -1,					pt_isengard_caravan),
#Others good
(p_town_caras_galadhon  ,pt_lorien_scouts,        pt_lorien_raiders,     pt_lorien_patrol,    pt_lorien_caravan),
(p_town_cerin_dolen     ,-1,        			  -1,                    pt_lorien_patrol,    pt_lorien_caravan),
(p_town_cerin_amroth    ,pt_lorien_scouts,        -1,                    pt_lorien_patrol,    -1),
(p_town_imladris_camp   ,pt_imladris_scouts,      pt_imladris_raiders,   pt_imladris_patrol,  pt_imladris_caravan),

(p_town_thranduils_halls,pt_woodelf_scouts,       pt_woodelf_raiders,    pt_woodelf_patrol,   pt_woodelf_caravan),
(p_town_woodelf_camp    ,pt_woodelf_scouts,       pt_woodelf_raiders,    pt_woodelf_patrol,   pt_woodelf_caravan),
(p_town_woodelf_west_camp,pt_woodelf_scouts,      pt_woodelf_raiders,    pt_woodelf_patrol,   pt_woodelf_caravan),

(p_town_woodsmen_village,pt_woodmen_scouts,       -1,                      -1,                    pt_beorn_caravan),
(p_town_beorning_village,pt_beorn_scouts,         -1,                      -1,                    pt_beorn_caravan),
(p_town_beorn_house     ,pt_beorn_scouts,         -1,                      -1,                    pt_beorn_caravan),

(p_town_dale            ,pt_dale_scouts,          pt_dale_raiders,    pt_dale_patrol,      pt_dale_caravan),
(p_town_esgaroth        ,pt_esgaroth_scouts,      pt_dale_raiders,    pt_esgaroth_patrol,  pt_dale_caravan),
(p_town_erebor          ,pt_dwarf_scouts,         -1,				    pt_dwarf_patrol,     pt_dwarf_caravan),
(p_town_ironhill_camp   ,pt_dwarf_scouts,         -1,				    pt_dwarf_patrol,     pt_dwarf_caravan),
#Others evil
(p_town_moria           ,pt_moria_scouts,         pt_moria_raiders,   pt_moria_war_party,  -1),
(p_town_troll_cave      ,pt_moria_scouts,         pt_moria_raiders,   pt_moria_war_party,  -1),

(p_town_dol_guldur      ,pt_guldur_scouts,        pt_guldur_raiders,  pt_guldur_war_party, -1),
(p_town_dol_guldur_north_outpost,pt_guldur_scouts,pt_guldur_raiders,  pt_guldur_war_party, -1),

(p_town_dunland_camp    ,pt_dunland_scouts,       pt_dunland_raiders, pt_dunland_war_party,-1),
(p_town_harad_camp      ,pt_harad_scouts,         pt_harad_raiders,   pt_harad_war_party,  -1),
(p_town_khand_camp      ,pt_khand_scouts,         pt_khand_raiders,   pt_khand_war_party,  -1),

(p_town_rhun_main_camp ,pt_rhun_scouts,          pt_rhun_raiders,    pt_rhun_war_party,   -1),
(p_town_rhun_south_camp ,pt_rhun_scouts,          pt_rhun_raiders,    pt_rhun_war_party,   -1),
(p_town_rhun_north_camp ,pt_rhun_scouts,          pt_rhun_raiders,    pt_rhun_war_party,   -1),

(p_town_umbar_camp      ,pt_umbar_scouts,         pt_umbar_raiders,   -1,                    -1),

(p_town_gundabad                 ,pt_gundabad_scouts,pt_gundabad_raiders,-1,                    pt_gunda_caravan),
(p_town_gundabad_ne_outpost      ,pt_gundabad_scouts,pt_gundabad_raiders,-1,                    pt_gunda_caravan),
(p_town_gundabad_nw_outpost      ,pt_gundabad_scouts,pt_gundabad_raiders,-1,                    pt_gunda_caravan),
(p_town_goblin_north_outpost     ,pt_gundabad_scouts,pt_gundabad_raiders,-1,                    pt_gunda_caravan),
(p_town_goblin_south_outpost     ,pt_gundabad_scouts,pt_gundabad_raiders,-1,                    -1),
(p_town_gundabad_m_outpost       ,pt_gundabad_scouts,pt_gundabad_raiders,-1,                    -1),
#Advance camps   
(p_advcamp_gondor       ,pt_gondor_scouts,        pt_gondor_raiders,     pt_gondor_patrol,    pt_gondor_caravan),
(p_advcamp_rohan        ,pt_rohan_scouts,         pt_rohan_raiders,      pt_rohan_patrol,     pt_rohan_caravan),
(p_advcamp_isengard     ,pt_isengard_scouts,      pt_isengard_raiders,   pt_isengard_war_party,pt_isengard_caravan),
(p_advcamp_mordor       ,pt_mordor_scouts,        pt_mordor_raiders,     pt_mordor_war_party, pt_mordor_caravan),
(p_advcamp_harad        ,pt_harad_scouts,         pt_harad_raiders,      pt_harad_war_party,  -1),
(p_advcamp_rhun         ,pt_rhun_scouts,          pt_rhun_raiders,       pt_rhun_war_party,   -1),
(p_advcamp_khand        ,pt_khand_scouts,         pt_khand_raiders,      pt_khand_war_party,  -1),
(p_advcamp_umbar        ,pt_umbar_scouts,         pt_umbar_raiders,      -1,                    -1),
(p_advcamp_lorien       ,pt_lorien_scouts,        pt_lorien_raiders,     pt_lorien_patrol,    pt_lorien_caravan),
(p_advcamp_imladris     ,pt_imladris_scouts,      pt_imladris_raiders,   pt_imladris_patrol,  pt_imladris_caravan),
(p_advcamp_woodelf      ,pt_woodelf_scouts,       pt_woodelf_raiders,    pt_woodelf_patrol,   pt_woodelf_caravan),
(p_advcamp_moria        ,pt_moria_scouts,         pt_moria_raiders,      pt_moria_war_party,  -1),
(p_advcamp_guldur       ,pt_guldur_scouts,        pt_guldur_raiders,     pt_mordor_war_party, -1),
(p_advcamp_gundabad     ,pt_gundabad_scouts,      pt_gundabad_raiders,   -1,                    pt_gunda_caravan),
(p_advcamp_dale         ,pt_dale_scouts,          pt_dale_raiders,       pt_dale_patrol,      pt_dale_caravan),
(p_advcamp_dwarf        ,pt_dwarf_scouts,         -1,				       pt_dwarf_patrol,     pt_dwarf_caravan),
(p_advcamp_dunland      ,pt_dunland_scouts,       pt_dunland_raiders,    pt_dunland_war_party,-1),
(p_advcamp_beorn        ,pt_beorn_scouts,         -1,                      -1,                    -1),
	
]

# TLD Party base probability to spawn daily per center (0-100), for average faction strength (3500); modified by strength/100-35
# Kham - Increased by 10 (March 2017)
ws_scout_chance = 50
ws_raider_chance = 40 # no chance below str. 500
ws_patrol_chance = 30 # no chance below str. 1500
ws_caravan_chance = 25 # no chance below str. 2000
#ws_host_chance = 35

# TLD Party limit multiplier. Maximum number of parties for faction strength 3500 (double that for 7000). (Namely strength*multiplier/3500 is the party number limit)
# Kham - Increased by varied amount (March 2017) # InVain - reduced number of scouts again so early game is not as cluttered
ws_scout_limit_multiplier = 17 #+11 increase #-8 decrease
ws_raider_limit_multiplier = 15 #+6 increase
ws_patrol_limit_multiplier = 12 #+6 increase
ws_caravan_limit_multiplier = 10 #+5 increase
#ws_host_limit_multiplier = 4

# TLD Party victory points. Faction strength decreased by these when party is killed, winner gets half of it. (slot_party_victory_value)
ws_scout_vp   = 10  # strength 30-60
ws_raider_vp  = 20  # strength 80-160
ws_patrol_vp  = 50  # strength 300-600
ws_caravan_vp = 50  # strength 250-500; valued more because they represent logistics
ws_alone_vp   = 20  # for hero-led parties (bodyguards only).
ws_host_vp    = 80  # for hero-led parties (hosts). strength about 1000
ws_p_train_vp = 30  # strength 150-250
ws_center_vp  = 100 # loss of center
ws_guard_vp   = 1850 # guardian party, spawned when str<1300, so it can be used to defeat a faction

# Center strength daily incomes (slot_center_strength_income), for easy mass tweaking
str_income_none = 0
str_income_low  = 5
str_income_med  = 10
str_income_high = 20
str_income_very_high = 30

# Center garrison limits (slot_center_garrison_limit), for easy mass tweaking
garrison_limit_low  = 250 # for Elves and Dwarves
garrison_limit_med  = 300
garrison_limit_high = 450 #capitals
# Evil factions have 20% larger garrisons (quantity vs quality) #InVain: garrison sizes are now adjusted via script (so they affect capturable settlements)
garrison_limit_evil_low  = garrison_limit_low*120/100 #not used
garrison_limit_evil_med  = garrison_limit_med #*120/100
garrison_limit_evil_high = garrison_limit_high #*150/100

# Siegability flag values
tld_siegable_always  = 1  # siege if attstr>fac_str_ok
tld_siegable_normal  = 2  # siege if attstr>fac_str_ok and defstr<fac_str_weak
tld_siegable_capital = 3  # capital, siege if attstr>fac_str_ok and defstr<fac_str_very_weak; may be redundant, but gives some flexibility
tld_siegable_never   = 4  # never siege


str_fullname_region_begin = str_fullname_region_pelennor
str_shortname_region_begin = str_shortname_region_pelennor
str_fullname_region_begin_new = str_fullname_region_rhun
str_shortname_region_begin_new = str_shortname_region_rhun

###########################################################################################
# center scenes list, to assign subscenes and npcs to centers
# instead of ordering scenes and npcs in module_troops, which is cumbersome
center_list = [
    # (party_center,  [scenes: center, castle, prison, tavern, arena, siege, menu mesh], 
	#     [npcs: captain, smith, merchant, elder, lord, 4 walkers], 
	#     [map banner],[arena:team#,size 123], strength income, garrison limit, destroy-on-capture flag, siegability flag) 
    # -1 if no such subscene, "trp_no_troop" if no such npc
	
	#("p_zendar", ["scn_zendar_center", -1, -1,"scn_the_happy_boar","scn_zendar_arena",-1,"mesh_ui_default_menu_window" ],
	#    ["trp_barman_mtirith", "trp_smith_mtirith", "trp_merchant_mtirith", "trp_elder", "pt_gondor_recruits", "trp_gondor_lord", "trp_walker_woman_gondor_bw","trp_walker_man_gondor_black","trp_walker_man_gondor_white","trp_walker_woman_gondor_w"],
	#	[0],[900],[2,1,4,1,4,1], str_income_med, garrison_limit_med, 0, tld_siegable_never),
(p_town_minas_tirith, [scn_minas_tirith_center, scn_minas_tirith_castle, scn_gondor_prison,scn_gondor_tavern,scn_gondor_arena,scn_minas_tirith_siege,mesh_town_minas_tirith],
	[trp_captain_of_gondor, trp_smith_mtirith, trp_merchant_mtirith, trp_elder_mtirith, pt_gondor_cap_recruits, trp_gondor_lord, trp_walker_woman_gondor_bw,trp_walker_man_gondor_black,trp_walker_man_gondor_white,trp_walker_woman_gondor_w], 
	[icon_mfc_gondor],[700],[2,1,4,1,4,1], str_income_high, garrison_limit_evil_med, 1, tld_siegable_capital),
(p_town_pelargir, [scn_pelargir_center, scn_gondor_castle_a, scn_gondor_prison,scn_gondor_tavern,scn_gondor_arena,scn_pelargir_siege,mesh_town_pelargir],
	[trp_i6_pel_leader, trp_smith_pelargir, trp_merchant_pelargir, trp_elder_pelargir, pt_pelargir_recruits, trp_knight_1_4, trp_walker_woman_gondor_bw,trp_walker_man_gondor_black,trp_walker_man_gondor_white,trp_walker_woman_gondor_b], 
	[icon_mfc_pelargir],[500],[4,4,4,6,4,8], str_income_med, garrison_limit_med, 0, tld_siegable_always),
(p_town_linhir, [scn_linhir_center, scn_gondor_castle_b, scn_gondor_prison,scn_gondor_tavern,scn_gondor_arena,scn_linhir_siege, mesh_ui_default_menu_window],
	[trp_captain_of_gondor, trp_smith_linhir, trp_merchant_linhir, trp_elder_linhir, pt_gondor_recruits, trp_gondor_lord, trp_walker_woman_gondor_bw,trp_walker_man_gondor_black,trp_walker_man_gondor_green,trp_walker_woman_gondor_b], 
	[icon_mfc_gondor],[500],[2,8,2,8,2,8], str_income_low, garrison_limit_med, 1, tld_siegable_always),
(p_town_dol_amroth, [scn_dol_amroth_center, scn_dol_amroth_castle, scn_gondor_prison,scn_gondor_tavern,scn_gondor_arena,scn_dol_amroth_siege,mesh_town_dol_amroth],
	[trp_c6_amroth_leader, trp_smith_dolamroth, trp_merchant_dolamroth, trp_elder_dolamroth, pt_dol_amroth_recruits, trp_knight_1_3, trp_walker_woman_gondor_bw,trp_walker_man_gondor_white,trp_walker_man_gondor_blue,trp_walker_woman_gondor_b], 
	[icon_mfc_dol_amroth],[500],[2,8,3,8,2,5], str_income_med, garrison_limit_high, 1, tld_siegable_normal),
(p_town_edhellond, [scn_edhellond_center, scn_gondor_castle, scn_gondor_prison,scn_gondor_tavern,scn_gondor_arena,scn_edhellond_siege, mesh_town_edhellond],
	[trp_captain_of_gondor, trp_smith_edhellond, trp_merchant_edhellond, trp_elder_edhellond, pt_gondor_recruits, trp_gondor_lord, trp_walker_woman_gondor_bw,trp_walker_man_gondor_black,trp_walker_man_gondor_green,trp_walker_woman_gondor_b], 
	[icon_mfc_gondor],[500],[2,3,2,5,2,8], str_income_low, garrison_limit_low, 1, tld_siegable_normal),
(p_town_lossarnach, [scn_lossarnach_center, scn_gondor_castle, scn_gondor_prison,scn_gondor_tavern,scn_gondor_arena,scn_lossarnach_siege, mesh_town_lossarnach],
	[trp_i6_loss_leader, trp_smith_lossarnach, trp_merchant_lossarnach, trp_elder_lossarnach, pt_lossarnach_recruits, trp_knight_1_8, trp_walker_woman_gondor_bw,trp_walker_man_gondor_blue,trp_walker_man_gondor_green,trp_walker_woman_gondor_b], 
	[icon_mfc_lossarnach],[500],[2,4,3,4,3,6], str_income_low, garrison_limit_med, 1, tld_siegable_normal),
(p_town_tarnost, [scn_tarnost_center, scn_gondor_castle_c, scn_gondor_prison,scn_gondor_tavern,scn_gondor_arena,scn_tarnost_siege, mesh_ui_default_menu_window],
	[trp_captain_of_gondor, trp_smith_tarnost, trp_merchant_tarnost, trp_elder_tarnost, pt_gondor_recruits, trp_gondor_lord, trp_walker_woman_gondor_bw,trp_walker_man_gondor_black,trp_walker_man_gondor_green,trp_walker_woman_gondor_b], 
	[icon_mfc_gondor],[500],[4,4,4,6,4,8], str_income_low, garrison_limit_med, 1, tld_siegable_always),
(p_town_erech, [scn_erech_center, scn_gondor_castle, scn_gondor_prison,scn_gondor_tavern,scn_gondor_arena,scn_erech_siege, mesh_town_erech],
	[trp_a5_blackroot_shadow_hunter, trp_smith_erech, trp_merchant_erech, trp_elder_erech, pt_blackroot_recruits, trp_knight_1_5, trp_walker_woman_gondor_bw,trp_walker_man_gondor_black,trp_walker_man_gondor_green,trp_walker_woman_gondor_b], 
	[icon_mfc_erech],[500],[3,1,3,3,3,7], str_income_low, garrison_limit_low, 1, tld_siegable_normal),
(p_town_pinnath_gelin, [scn_pinnath_gelin_center, scn_gondor_castle, scn_gondor_prison,scn_gondor_tavern,scn_gondor_arena,scn_pinnath_gelin_siege, mesh_ui_default_menu_window],
	[trp_c6_pinnath_leader, trp_smith_pinnath, trp_merchant_pinnath, trp_elder_pinnath, pt_pinnath_recruits, trp_knight_1_6, trp_walker_woman_gondor_bw,trp_walker_man_gondor_black,trp_walker_man_gondor_green,trp_walker_woman_gondor_b], 
	[icon_mfc_pinnath],[500],[2,2,2,5,2,8], str_income_low, garrison_limit_low, 1, tld_siegable_normal),
(p_town_west_osgiliath, [scn_west_osgiliath_center, scn_west_osgiliath_castle, -1, -1, -1, scn_west_osgiliath_siege,mesh_town_osgilliath],
	[trp_captain_of_gondor, trp_smith_wosgiliath, trp_merchant_wosgiliath,trp_elder_wosgiliath , pt_gondor_recruits, trp_gondor_lord, trp_i1_gon_levy,trp_i2_gon_watchman,trp_a4_ithilien_ranger,trp_i4_gon_swordsman], 
	[icon_mfc_gondor],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_med, 0, tld_siegable_always),
(p_town_henneth_annun, [scn_henneth_annun_center, scn_henneth_annun_castle, -1, -1, -1, -1, mesh_town_henneth_annun],
	[trp_a6_ithilien_leader, trp_smith_hannun, trp_merchant_hannun, trp_elder_henneth, pt_ithilien_recruits, trp_gondor_lord, trp_a4_ithilien_ranger,trp_a4_ithilien_ranger,trp_a5_ithilien_vet_ranger,trp_a6_ithilien_master_ranger], 
	[icon_mfc_gondor],[500],[2,1,4,1,4,1], str_income_none, garrison_limit_low, 1, tld_siegable_never),
(p_town_cair_andros, [scn_cair_andros_center, scn_cair_andros_castle, -1, -1, -1, scn_cair_andros_siege, mesh_town_cair_andros],
	[trp_a6_ithilien_leader, trp_smith_candros, trp_merchant_candros, trp_elder_cairandros, pt_gondor_recruits, trp_gondor_lord, trp_i1_gon_levy,trp_i2_gon_watchman,trp_a4_ithilien_ranger,trp_i4_gon_swordsman], 
	[icon_mfc_gondor],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_med, 0, tld_siegable_always),
(p_town_calembel, [scn_ethring_center, scn_gondor_castle, scn_gondor_prison,scn_gondor_tavern,scn_gondor_arena, scn_ethring_siege, mesh_town_calembel],
	[trp_c6_lam_leader, trp_smith_calembel, trp_merchant_calembel, trp_elder_ethring, pt_lamedon_recruits, trp_knight_1_1, trp_i1_gon_levy,trp_walker_man_gondor_black,trp_walker_man_gondor_green,trp_walker_woman_gondor_b], 
	[icon_mfc_ethring],[500],[2,2,2,5,2,8], str_income_low, garrison_limit_low, 1, tld_siegable_normal),
# Rohan centers
(p_town_edoras, [scn_edoras_center, scn_edoras_castle, scn_rohan_prison,scn_rohan_tavern,scn_rohan_arena, scn_edoras_siege,mesh_town_edoras],
	[trp_captain_of_rohan, trp_smith_edoras, trp_merchant_edoras, trp_elder_edoras, pt_rohan_cap_recruits, trp_rohan_lord, trp_walker_woman_rohan_d, trp_walker_man_rohan_t, trp_walker_man_rohan_d, trp_walker_woman_rohan_t], 
	[icon_mfc_rohan],[900],[2,8,3,4,3,6], str_income_high, garrison_limit_high, 1, tld_siegable_capital),
(p_town_aldburg, [scn_aldburg_center, scn_rohan_castle, scn_rohan_prison,scn_rohan_tavern,scn_rohan_arena, scn_aldburg_siege, mesh_ui_default_menu_window],
	[trp_captain_of_rohan, trp_smith_aldburg, trp_merchant_aldburg, trp_elder_aldburg, pt_rohan_recruits, trp_knight_1_11, trp_walker_woman_rohan_d, trp_walker_man_rohan_t, trp_walker_man_rohan_d, trp_walker_woman_rohan_t], 
	[icon_mfc_rohan],[500],[2,3,2,5,2,8], str_income_med, garrison_limit_med, 1, tld_siegable_normal),
(p_town_hornburg, [scn_hornburg_center, scn_hornburg_castle, scn_rohan_prison,scn_rohan_tavern, -1, scn_hornburg_siege,mesh_town_hornburg],
	[trp_captain_of_rohan, trp_smith_hornburg, trp_merchant_hornburg, trp_elder_hornburg, pt_rohan_recruits, trp_rohan_lord, trp_i1_rohan_youth, trp_walker_man_rohan_t, trp_i2_guardsman_of_rohan, trp_i3_footman_of_rohan], 
	[icon_mfc_rohan],[500],[3,8,4,6,4,5], str_income_high, garrison_limit_high, 1, tld_siegable_capital),
(p_town_east_emnet, [scn_east_emnet_center, scn_rohan_castle_a, scn_rohan_prison,scn_rohan_tavern,scn_rohan_arena, scn_east_emnet_siege, mesh_ui_default_menu_window],
	[trp_captain_of_rohan, trp_smith_eastemnet, trp_merchant_eastemnet, trp_elder_eastemnet, pt_rohan_recruits, trp_knight_1_14, trp_walker_woman_rohan_d, trp_walker_man_rohan_t, trp_walker_man_rohan_d, trp_walker_woman_rohan_t], 
	[icon_mfc_rohan],[500],[2,8,4,5,4,7], str_income_med, garrison_limit_med, 1, tld_siegable_always),
(p_town_westfold, [scn_westfold_center, scn_rohan_castle_b, scn_rohan_prison,scn_rohan_tavern,scn_rohan_arena, scn_westfold_siege, mesh_ui_default_menu_window],
	[trp_captain_of_rohan, trp_smith_westfold, trp_merchant_westfold, trp_elder_westfold, pt_rohan_recruits, trp_knight_1_9, trp_walker_woman_rohan_d, trp_walker_man_rohan_t, trp_walker_man_rohan_d, trp_walker_woman_rohan_t], 
	[icon_mfc_rohan],[500],[2,4,2,5,2,6], str_income_med, garrison_limit_med, 1, tld_siegable_always),
(p_town_west_emnet, [scn_west_emnet_center, scn_rohan_castle_a, scn_rohan_prison,scn_rohan_tavern,scn_rohan_arena, scn_west_emnet_siege, mesh_town_west_emnet],
	[trp_captain_of_rohan, trp_smith_westemnet, trp_merchant_westemnet, trp_elder_westemnet, pt_rohan_recruits, trp_knight_1_10, trp_walker_woman_rohan_d, trp_walker_man_rohan_t, trp_walker_man_rohan_d, trp_walker_woman_rohan_t], 
	[icon_mfc_rohan],[500],[2,8,3,4,3,6], str_income_med, garrison_limit_med, 1, tld_siegable_always),
(p_town_eastfold, [scn_eastfold_center, scn_rohan_castle_b, scn_rohan_prison,scn_rohan_tavern,scn_rohan_arena, scn_eastfold_siege, mesh_ui_default_menu_window],
	[trp_captain_of_rohan, trp_smith_eastfold, trp_merchant_eastfold, trp_elder_eastfold, pt_rohan_recruits, trp_knight_1_13, trp_walker_woman_rohan_d, trp_walker_man_rohan_t, trp_walker_man_rohan_d, trp_walker_woman_rohan_t], 
	[icon_mfc_rohan],[500],[3,8,4,6,4,5], str_income_med, garrison_limit_med, 1, tld_siegable_normal),
# Mordor centers
(p_town_morannon, [scn_morannon_center, scn_morannon_castle, scn_mordor_prison,scn_mordor_tavern,scn_mordor_arena, scn_morannon_siege,mesh_town_morannon],
	[trp_i5_mordor_black_uruk, trp_smith_morannon, trp_merchant_morannon, trp_elder_morannon, pt_morannon_recruits, trp_mordor_lord, trp_i2_mordor_uruk, trp_i2_mordor_orc, trp_i3_mordor_large_orc, trp_a3_guldur_large_orc_tracker], 
	[icon_mfc_mordor],[900],[2,8,4,5,4,7], str_income_high, garrison_limit_evil_high*2, 1, tld_siegable_capital),
(p_town_minas_morgul, [scn_minas_morgul_center, scn_mordor_castle_b, scn_mordor_prison,scn_mordor_tavern,scn_mordor_arena, scn_minas_morgul_siege, mesh_ui_default_menu_window],
	[trp_i5_mordor_black_uruk, trp_smith_mmorgul, trp_merchant_mmorgul, trp_elder_mmorgul, pt_morgul_recruits, trp_mordor_lord, trp_i2_mordor_uruk, trp_i2_mordor_orc, trp_i3_mordor_large_orc, trp_a3_guldur_large_orc_tracker], 
	[icon_mfc_mordor],[500],[2,4,2,5,2,6], str_income_med, garrison_limit_evil_med*2, 1, tld_siegable_capital),
(p_town_cirith_ungol, [scn_cirith_ungol_center, -1, scn_mordor_prison,scn_mordor_tavern, -1, scn_cirith_ungol_siege, mesh_town_evilcamp],
	[trp_i5_mordor_black_uruk, trp_smith_orc_patrol, trp_merchant_orc_patrol, trp_elder_cungol, pt_mordor_recruits, trp_mordor_lord, trp_i2_mordor_uruk, trp_i2_mordor_orc, trp_i3_mordor_large_orc, trp_a3_guldur_large_orc_tracker], 
	[icon_mfc_mordor],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_evil_high, 2, tld_siegable_normal),
(p_town_orc_sentry_camp, [scn_orc_sentry_camp_center, -1, -1, -1, -1, scn_orc_sentry_camp_center_siege, mesh_town_evilcamp],
	[trp_i5_mordor_black_uruk, trp_smith_oscamp, trp_merchant_orc_sentry, trp_elder_oscamp, pt_mordor_recruits, trp_mordor_lord, trp_i2_mordor_uruk, trp_i2_mordor_orc, trp_i3_mordor_large_orc, trp_a3_guldur_large_orc_tracker], 
	[icon_mfc_mordor],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_evil_high, 2, tld_siegable_normal),
(p_town_east_osgiliath, [scn_east_osgiliath_center, scn_east_osgiliath_castle, -1, -1, -1, scn_east_osgiliath_siege, mesh_town_osgilliath],
	[trp_i5_mordor_black_uruk, trp_smith_eosgiliath, trp_merchant_eosgiliath, trp_elder_eosgiliath, pt_mordor_recruits, trp_mordor_lord, trp_i2_mordor_uruk, trp_i2_mordor_orc, trp_i3_mordor_large_orc, trp_a3_guldur_large_orc_tracker], 
	[icon_mfc_mordor],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_med, 0, tld_siegable_always),
# Isengard centers
(p_town_isengard, [scn_isengard_center, scn_isengard_castle, scn_mordor_prison,scn_mordor_tavern, scn_isengard_arena, scn_isengard_siege,mesh_town_isengard],
	[trp_captain_of_isengard, trp_smith_isengard, trp_merchant_isengard, trp_elder_isengard, pt_isengard_recruits,  trp_isengard_lord,trp_i2_isen_orc,trp_i3_isen_large_orc,trp_a2_isen_uruk_tracker,trp_i2_isen_uruk], 
	[icon_mfc_isengard],[900],[2,1,4,1,4,1], str_income_high, garrison_limit_evil_high, 1, tld_siegable_never),
(p_town_urukhai_outpost, [scn_uruk_hai_outpost_center, -1, -1, -1, scn_isengard_arena, scn_uruk_hai_outpost_center_siege, mesh_town_evilcamp],
	[trp_captain_of_isengard, trp_smith_uoutpost, trp_merchant_uoutpost, trp_elder_uoutpost, pt_isengard_recruits,  trp_isengard_lord,trp_i2_isen_orc,trp_i3_isen_large_orc,trp_a2_isen_uruk_tracker,trp_i2_isen_uruk], 
	[icon_mfc_isengard],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_evil_med, 2, tld_siegable_always),
(p_town_urukhai_h_camp, [scn_uruk_hai_h_camp_center, -1, -1, -1, scn_isengard_arena, scn_uruk_hai_h_camp_center_siege, mesh_town_evilcamp],
	[trp_captain_of_isengard, trp_smith_uhcamp, trp_merchant_uhcamp,trp_elder_uhcamp, pt_isengard_recruits,  trp_isengard_lord,trp_i2_isen_orc,trp_i3_isen_large_orc,trp_a2_isen_uruk_tracker,trp_i2_isen_uruk], 
	[icon_mfc_isengard],[500],[2,1,4,1,4,1], str_income_med, garrison_limit_evil_high, 2, tld_siegable_normal),
(p_town_urukhai_r_camp, [scn_uruk_hai_r_camp_center, -1, -1, -1, scn_isengard_arena, scn_uruk_hai_r_camp_center_siege, mesh_town_evilcamp],
	[trp_captain_of_isengard, trp_smith_urcamp, trp_merchant_urcamp, trp_elder_urcamp, pt_isengard_recruits,  trp_isengard_lord,trp_i2_isen_orc,trp_i3_isen_large_orc,trp_a2_isen_uruk_tracker,trp_i2_isen_uruk], 
	[icon_mfc_isengard],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_evil_med, 2, tld_siegable_always),
# Elf centers
(p_town_caras_galadhon, [scn_caras_galadhon_center, -1, scn_elf_prison,scn_elf_tavern,scn_elf_arena,scn_caras_galadhon_siege,mesh_town_caras_galadhon],
	[-1, trp_smith_cgaladhon, trp_merchant_cgaladhon, trp_elder_cgaladhon, pt_lorien_recruits, trp_lorien_lord, trp_a1_lorien_scout, trp_a3_lorien_vet_warden, trp_a2_lorien_archer, trp_i3_lorien_inf], 
	[icon_mfc_lorien],[900],[2,1,4,1,4,1], str_income_high, garrison_limit_med, 1, tld_siegable_capital),
(p_town_cerin_dolen, [scn_cerin_dolen_center, -1, -1, -1, -1, scn_cerin_dolen_siege, mesh_ui_default_menu_window],
	[-1, trp_smith_cdolen, trp_merchant_cdolen, trp_elder_cdolen, pt_lorien_recruits,  trp_lorien_lord, trp_a1_lorien_scout, trp_a3_lorien_vet_warden, trp_a2_lorien_archer, trp_i3_lorien_inf], 
	[icon_mfc_lorien],[500],[2,1,4,1,4,1], str_income_med, garrison_limit_low, 2, tld_siegable_always),
(p_town_cerin_amroth, [scn_cerin_amroth_center, -1, -1, -1, -1, scn_cerin_amroth_siege, mesh_ui_default_menu_window],
	[-1, trp_smith_camroth, trp_merchant_camroth, trp_elder_camroth, pt_lorien_recruits,  trp_lorien_lord, trp_a1_lorien_scout, trp_a3_lorien_vet_warden, trp_a2_lorien_archer, trp_i3_lorien_inf], 
	[icon_mfc_lorien],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_low, 2, tld_siegable_normal),

(p_town_thranduils_halls, [scn_thranduils_halls_center, scn_thranduil_hall_room, scn_elf_prison,scn_elf_tavern,scn_elf_arena,scn_thranduils_halls_siege,mesh_town_thranduils],
	[-1, trp_smith_thranduils_halls, trp_merchant_thranduils_halls, trp_elder_thalls, pt_woodelf_recruits, trp_woodelf_lord, trp_a3_greenwood_archer, trp_a1_greenwood_scout, trp_a3_greenwood_archer, trp_i2_greenwood_infantry], 
	[icon_mfc_woodelf],[900],[2,1,4,1,4,1], str_income_med, garrison_limit_high, 1, tld_siegable_capital),
(p_town_woodelf_camp, [scn_woodelf_camp_center, -1, -1,-1,-1,scn_woodelf_camp_siege, mesh_town_goodcamp],
	[-1, trp_smith_woodelf_camp, trp_merchant_woodelf_camp, trp_elder_woodelf_camp, pt_woodelf_recruits, trp_woodelf_lord, trp_a3_greenwood_archer, trp_a1_greenwood_scout, trp_a3_greenwood_archer, trp_i2_greenwood_infantry], 
	[icon_mfc_woodelf],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_med, 2, tld_siegable_always),
(p_town_woodelf_west_camp, [scn_woodelf_west_camp_center, -1, -1,-1,-1,scn_woodelf_west_camp_siege, mesh_town_goodcamp],
	[-1, trp_smith_woodelf_west_camp, trp_merchant_woodelf_west_camp, trp_elder_woodelf_west_camp, pt_woodelf_recruits, trp_woodelf_lord, trp_a3_greenwood_archer, trp_a1_greenwood_scout, trp_a3_greenwood_archer, trp_i2_greenwood_infantry], 
	[icon_mfc_woodelf],[500],[2,1,4,1,4,1], str_income_med, garrison_limit_med, 2, tld_siegable_normal),
(p_town_imladris_camp, [scn_rivendell_camp_center, -1, -1,-1,-1,scn_rivendell_camp_siege,mesh_town_rivendell_camp],
	[-1, trp_smith_imladris, trp_merchant_imladris, trp_elder_imladris, pt_imladris_recruits, trp_imladris_lord, trp_a1_riv_scout,trp_i3_riv_swordbearer, trp_a3_riv_archer,trp_a1_arnor_scout], 
	[icon_mfc_imladris],[900],[2,1,4,1,4,1], str_income_high, garrison_limit_med, 2, tld_siegable_capital),

(p_town_woodsmen_village, [scn_woodsmen_village2_center, -1, -1,-1,-1,scn_woodsmen_village2_siege, mesh_ui_default_menu_window],
	[-1, trp_smith_woodmen, trp_merchant_woodmen, trp_elder_wvillage, pt_woodman_recruits, trp_beorn_lord, trp_i1_woodmen_man, trp_a2_woodmen_tracker, trp_i2_woodmen_forester, trp_i4_woodmen_axemen], 
	[icon_mfc_northmen],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_med, 1, tld_siegable_always),
(p_town_beorning_village, [scn_beorning_village_center, -1, -1,-1,-1,scn_beorning_village_siege, mesh_ui_default_menu_window],
	[-1, trp_smith_beorn_v, trp_merchant_beorn_v, trp_elder_beorn_v, pt_beorn_recruits, trp_beorn_lord, trp_i1_beorning_man, trp_i4_beorning_sentinel, trp_i1_woodmen_man, trp_i3_beorning_tolltacker], 
	[icon_mfc_northmen],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_med, 1, tld_siegable_always),
(p_town_beorn_house, [scn_woodsmen_village_center, scn_beorn_castle, -1,-1, scn_beorn_arena,scn_woodsmen_village_siege,mesh_town_beorns_house],
	[-1, trp_smith_beorn, trp_merchant_beorn, trp_elder_beorn, pt_beorn_recruits, trp_beorn_lord, trp_i1_beorning_man, trp_i4_beorning_carrock_fighter, trp_i2_beorning_warrior, trp_i1_woodmen_man], 
	[icon_mfc_northmen],[900],[2,1,4,1,4,1], str_income_low, garrison_limit_high, 1, tld_siegable_capital),

(p_town_moria, [scn_moria_center, -1, scn_mordor_prison,scn_mordor_tavern,scn_mordor_arena,scn_moria_siege,mesh_town_moria],
	[-1, trp_smith_moria, trp_merchant_moria, trp_elder_moria, pt_moria_recruits, trp_moria_lord,trp_i1_moria_snaga,trp_i2_moria_goblin,trp_c3_moria_wolf_rider,trp_i3_moria_large_goblin], 
	[icon_mfc_moria],[900],[2,1,4,1,4,1], str_income_high, garrison_limit_high, 1, tld_siegable_capital),
(p_town_troll_cave, [scn_troll_cave_center, -1, -1,-1,-1,scn_troll_cave_siege, mesh_ui_default_menu_window],
	[-1, trp_smith_troll_cave, trp_merchant_troll_cave, trp_elder_troll_cave, pt_moria_recruits, trp_moria_lord,trp_i1_moria_snaga,trp_i2_moria_goblin,trp_c3_moria_wolf_rider,trp_i3_moria_large_goblin], 
	[icon_mfc_moria],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_med, 1, tld_siegable_normal),

(p_town_dale, [scn_dale_center, scn_dale_castle, scn_rohan_prison,scn_rohan_tavern,scn_dale_arena, scn_dale_siege, mesh_ui_default_menu_window],
	[-1, trp_smith_dale, trp_merchant_dale, trp_elder_dale, pt_dale_recruits, trp_dale_lord,trp_townsman,trp_watchman,trp_i1_dale_militia,trp_townsman], 
	[icon_mfc_dale],[900],[2,1,4,1,4,1], str_income_med, garrison_limit_high, 0, tld_siegable_capital),
(p_town_esgaroth, [scn_esgaroth_center, scn_esgaroth_castle, scn_rohan_prison,scn_rohan_tavern,scn_dale_arena,scn_esgaroth_siege,mesh_town_esgaroth],
	[-1, trp_smith_esgaroth, trp_merchant_esgaroth, trp_elder_esgaroth, pt_dale_recruits, trp_dale_lord,trp_townsman,trp_watchman,trp_i1_dale_militia,trp_townsman], 
	[icon_mfc_dale],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_med, 1, tld_siegable_normal),

(p_town_dunland_camp, [scn_dunland_camp_center, -1, -1,-1,-1,scn_dunland_camp_siege, mesh_town_evilcamp],
	[-1, trp_smith_dunland, trp_merchant_dunland, trp_elder_dunland, pt_dunland_recruits, trp_dunland_lord, trp_i1_dun_wildman,trp_i2_dun_warrior, trp_i3_dun_pikeman, trp_i5_dun_wolf_guard], 
	[icon_mfc_dunland],[900],[2,1,4,1,4,1], str_income_med, garrison_limit_evil_high, 2, tld_siegable_capital),
(p_town_harad_camp, [scn_harad_camp_center, -1, -1,-1, scn_harad_arena,scn_harad_camp_siege, mesh_town_harad],
	[-1, trp_smith_harad, trp_merchant_harad, trp_elder_harad, pt_harad_recruits, trp_harad_lord,trp_i1_harad_levy,trp_i1_harad_levy,trp_i3_harad_infantry,trp_c3_harondor_rider], 
	[icon_mfc_harad],[900],[2,1,4,1,4,1], str_income_high, garrison_limit_evil_high, 2, tld_siegable_capital),
(p_town_khand_camp, [scn_khand_camp_center, -1, -1,-1, scn_khand_arena, scn_khand_camp_siege, mesh_town_khand],
	[-1, trp_smith_khand, trp_merchant_khand, trp_elder_khand, pt_khand_recruits, trp_khand_lord, trp_i1_khand_bondsman, trp_i3_khand_warrior,trp_i3_khand_pitfighter,trp_i4_khand_pit_champion], 
	[icon_mfc_khand],[900],[2,1,4,1,4,1], str_income_high, garrison_limit_evil_high, 2, tld_siegable_capital),
(p_town_umbar_camp, [scn_umbar_camp_center, -1, -1,-1, scn_umbar_arena,scn_umbar_camp_siege, mesh_town_evilcamp],
	[-1, trp_smith_umbar, trp_merchant_umbar, trp_elder_umbar, pt_umbar_recruits, trp_umbar_lord, trp_i1_corsair_youth, trp_i2_corsair_warrior, trp_a4_corsair_veteran_marksman,trp_a2_corsair_marine], 
	[icon_mfc_umbar],[900],[2,1,4,1,4,1], str_income_high, garrison_limit_evil_high, 1, tld_siegable_capital),
	
(p_town_dol_guldur, [scn_dol_guldur_center, scn_mordor_castle, scn_mordor_prison,scn_mordor_tavern,scn_mordor_arena,scn_dol_guldur_siege,mesh_town_dol_guldur],
	[-1, trp_smith_dolguldur, trp_merchant_dolguldur, trp_elder_dolguldur, pt_guldur_recruits, trp_guldur_lord, trp_i2_mordor_uruk, trp_i2_mordor_orc, trp_i3_mordor_large_orc, trp_a3_guldur_large_orc_tracker], 
	[icon_mfc_guldur],[900],[2,1,4,1,4,1], str_income_med, 550, 1, tld_siegable_capital),
(p_town_dol_guldur_north_outpost, [scn_dol_guldur_north_outpost_center, -1, -1,-1,-1,scn_dol_guldur_north_outpost_center_siege, mesh_town_evilcamp],
	[-1, trp_smith_dg_outpost, trp_merchant_dg_outpost, trp_elder_dg_outpost, pt_guldur_recruits, trp_guldur_lord, trp_i2_mordor_uruk, trp_i2_mordor_orc, trp_i3_mordor_large_orc, trp_a3_guldur_large_orc_tracker], 
	[icon_mfc_guldur],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_evil_high, 2, tld_siegable_normal),

(p_town_rhun_main_camp, [scn_north_rhun_camp_center, -1, -1,-1, scn_rhun_arena,scn_north_rhun_camp_siege, mesh_town_rhun_north],
	[-1, trp_smith_main_rhun, trp_merchant_main_rhun, trp_elder_rhun, pt_rhun_recruits,  trp_rhun_lord, trp_c4_rhun_noble_rider, trp_i4_rhun_vet_infantry, trp_i1_rhun_tribesman, trp_i2_rhun_tribal_warrior, ], 
	[icon_mfc_rhun],[900],[2,1,4,1,4,1], str_income_high, garrison_limit_evil_high, 2, tld_siegable_capital),
(p_town_rhun_south_camp, [scn_rhun_south_camp_center, -1, -1,-1,-1,scn_rhun_south_camp_siege, mesh_town_rhun],
	[-1, trp_smith_north_rhun, trp_merchant_south_rhun, trp_elder_rhun_sc, pt_rhun_recruits,  trp_rhun_lord, trp_c4_rhun_noble_rider, trp_i4_rhun_vet_infantry, trp_i1_rhun_tribesman, trp_i2_rhun_tribal_warrior, ], 
	[icon_mfc_rhun],[500],[2,1,4,1,4,1], str_income_med, garrison_limit_evil_med, 2, tld_siegable_normal),
(p_town_rhun_north_camp, [scn_rhun_north_camp_center, -1, -1,-1,-1,scn_rhun_north_camp_siege, mesh_town_rhun],
	[-1, trp_smith_south_rhun, trp_merchant_north_rhun, trp_elder_rhun_nc, pt_rhun_recruits,  trp_rhun_lord, trp_c4_rhun_noble_rider, trp_i4_rhun_vet_infantry, trp_i1_rhun_tribesman, trp_i2_rhun_tribal_warrior, ], 
	[icon_mfc_rhun],[500],[2,1,4,1,4,1], str_income_med, garrison_limit_evil_med, 2, tld_siegable_normal),
# Gundabad camp
(p_town_gundabad,     [scn_gundabad_camp_center, -1, -1,-1, scn_mordor_arena,scn_gundabad_siege, mesh_town_gundabad],
	[-1, trp_smith_gundabad, trp_merchant_gundabad, trp_elder_gunda, pt_gundabad_cap_recruits, trp_gundabad_lord,trp_i1_gunda_goblin,trp_i2_gunda_orc,trp_i3_gunda_orc_fighter,trp_c4_gunda_warg_rider], 
	[icon_mfc_gundabad],[900],[2,1,4,1,4,1], str_income_low, 600, 2, tld_siegable_capital),
(p_town_gundabad_ne_outpost, [scn_gundabad_ne_outpost_center, -1, -1,-1,-1,scn_gundabad_ne_outpost_center_siege, mesh_town_evilcamp],
	[-1, trp_smith_gundabad_ne, trp_merchant_gundabad_ne, trp_elder_gunda_ne, pt_gundabad_recruits, trp_gundabad_lord,trp_i1_gunda_goblin,trp_i2_gunda_orc,trp_i3_gunda_orc_fighter,trp_c4_gunda_warg_rider], 
	[icon_mfc_gundabad],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_evil_high, 0, tld_siegable_always),
(p_town_gundabad_nw_outpost, [scn_gundabad_nw_outpost_center, -1, -1,-1,-1,scn_gundabad_nw_outpost_center_siege, mesh_town_evilcamp],
	[-1, trp_smith_gundabad_nw, trp_merchant_gundabad_nw, trp_elder_gunda_nw, pt_gundabad_recruits, trp_gundabad_lord,trp_i1_gunda_goblin,trp_i2_gunda_orc,trp_i3_gunda_orc_fighter,trp_c4_gunda_warg_rider], 
	[icon_mfc_gundabad],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_evil_med, 2, tld_siegable_normal),
(p_town_goblin_north_outpost, [scn_goblin_north_outpost_center, -1, -1,-1,-1,scn_goblin_north_outpost_center_siege, mesh_town_evilcamp],
	[-1, trp_town_50_weaponsmith, trp_town_50_horse_merchant, trp_village_1_elder, pt_gundabad_recruits, trp_gundabad_lord,trp_i1_gunda_goblin,trp_i2_gunda_orc,trp_i3_gunda_orc_fighter,trp_c4_gunda_warg_rider], 
	[icon_mfc_gundabad],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_evil_high, 2, tld_siegable_normal),
(p_town_goblin_south_outpost, [scn_goblin_south_outpost_center, -1, -1,-1,-1,scn_goblin_south_outpost_center_siege, mesh_town_evilcamp],
	[-1, trp_smith_gundabad_s, trp_merchant_gundabad_s, trp_elder_gunda_s, pt_gundabad_recruits, trp_gundabad_lord,trp_i1_gunda_goblin,trp_i2_gunda_orc,trp_i3_gunda_orc_fighter,trp_c4_gunda_warg_rider], 
	[icon_mfc_gundabad],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_evil_high, 2, tld_siegable_always),
(p_town_gundabad_m_outpost, [scn_gundabad_mirkwood_outpost, -1, -1,-1,-1,scn_gundabad_mirkwood_outpost_siege, mesh_town_evilcamp],
	[-1, trp_smith_gundabad_m, trp_merchant_gundabad_m, trp_elder_gunda_m, pt_gundabad_recruits, trp_gundabad_lord,trp_i1_gunda_goblin,trp_i2_gunda_orc,trp_i3_gunda_orc_fighter,trp_c4_gunda_warg_rider], 
	[icon_mfc_gundabad],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_evil_med, 2, tld_siegable_normal),
(p_town_erebor, [scn_erebor_center, scn_erebor_castle, scn_rohan_prison,-1,scn_dwarf_arena,scn_erebor_siege, mesh_town_erebor],
	[-1, trp_smith_erebor, trp_merchant_erebor, trp_elder_erebor, pt_dwarf_recruits, trp_dwarf_lord, trp_i1_dwarf_apprentice, trp_a2_dwarf_lookout, trp_a4_dwarf_bowman, trp_i2_iron_hills_miner], 
	[icon_mfc_dwarf],[900],[2,1,4,1,4,1], str_income_high, garrison_limit_high, 1, tld_siegable_capital),
(p_town_ironhill_camp, [scn_ironhill_camp_center, -1, -1,-1,-1,scn_ironhill_camp_siege, mesh_town_goodcamp],
	[-1, trp_smith_ironhill, trp_merchant_ironhill, trp_elder_ironhill, pt_dwarf_iron_recruits, trp_dwarf_lord,trp_a2_dwarf_lookout, trp_a4_dwarf_bowman, trp_i4_iron_hills_infantry, trp_i2_iron_hills_miner], 
	[icon_mfc_dwarf],[500],[2,1,4,1,4,1], str_income_low, garrison_limit_low, 0, tld_siegable_always),
	
	
# Advance camps
# Note that scenes are borrowed from other camps where possible, or from Ironhill Camp
# NPCs are borrowed from other faction locations - this should be changed
# There is no income, and the garrison strength should be respectable, so they are not easily destroyed
(p_advcamp_gondor, [scn_advcamp_gondor, -1, -1, -1, -1, scn_advcamp_gondor_siege, mesh_town_goodcamp],
	[-1, trp_smith_wosgiliath, trp_merchant_wosgiliath, trp_no_troop, pt_gondor_recruits, trp_gondor_lord, trp_a4_ithilien_ranger,trp_i2_gon_watchman,trp_i4_gon_spearman,trp_i4_gon_swordsman], 
	[icon_mfc_gondor],[900],[2,1,4,1,4,1], 0, garrison_limit_low, 3, tld_siegable_always),
(p_advcamp_rohan, [scn_advcamp_rohan, -1, -1, -1, -1, scn_advcamp_rohan_siege, mesh_town_goodcamp],
	[-1, trp_smith_eastfold, trp_merchant_eastfold, trp_no_troop, pt_rohan_recruits, trp_rohan_lord, trp_ac3_skirmisher_of_rohan, trp_c4_lancer_of_rohan, trp_i2_guardsman_of_rohan, trp_i3_footman_of_rohan], 
	[icon_mfc_rohan],[900],[3,8,4,6,4,5], 0, garrison_limit_low, 3, tld_siegable_always),
(p_advcamp_isengard, [scn_advcamp_isengard, -1, -1, -1, -1, scn_advcamp_isengard_siege, mesh_town_evilcamp],
	[-1, trp_smith_urcamp, trp_merchant_urcamp, trp_no_troop, pt_isengard_recruits, trp_isengard_lord, trp_i2_isen_orc,trp_i3_isen_large_orc, trp_a2_isen_uruk_tracker, trp_i2_isen_uruk], 
	[icon_mfc_isengard],[900],[2,1,4,1,4,1], 0, garrison_limit_evil_low, 3, tld_siegable_always),
(p_advcamp_mordor, [scn_advcamp_mordor, -1, -1, -1, -1, scn_advcamp_mordor_siege, mesh_town_evilcamp],
	[-1, trp_smith_oscamp, trp_merchant_isengard, trp_no_troop, pt_mordor_recruits, trp_mordor_lord, trp_i2_mordor_uruk, trp_i2_mordor_orc, trp_i3_mordor_large_orc, trp_a3_guldur_large_orc_tracker], 
	[icon_mfc_mordor],[900],[2,1,4,1,4,1], 0, garrison_limit_evil_low, 3, tld_siegable_always),
(p_advcamp_harad, [scn_advcamp_harad, -1, -1,-1,-1, scn_advcamp_harad_siege, mesh_town_harad],
	[-1, trp_smith_harad, trp_merchant_harad, trp_no_troop, pt_harad_recruits, trp_harad_lord,trp_i1_harad_levy,trp_i1_harad_levy,trp_i3_harad_infantry,trp_c3_harondor_rider], 
	[icon_mfc_harad],[900],[2,1,4,1,4,1], 0, garrison_limit_evil_low, 3, tld_siegable_always),
(p_advcamp_rhun, [scn_advcamp_rhun, -1, -1,-1,-1, scn_advcamp_rhun_siege, mesh_town_rhun_north],
	[-1, trp_smith_north_rhun, trp_merchant_north_rhun, trp_no_troop, pt_rhun_recruits,  trp_rhun_lord, trp_c4_rhun_noble_rider, trp_i4_rhun_vet_infantry, trp_i1_rhun_tribesman, trp_i2_rhun_tribal_warrior, ], 
	[icon_mfc_rhun],[900],[2,1,4,1,4,1], 0, garrison_limit_evil_low, 3, tld_siegable_always),
(p_advcamp_khand, [scn_advcamp_khand, -1, -1,-1,-1, scn_advcamp_khand_siege, mesh_town_evilcamp],
	[-1, trp_smith_khand, trp_merchant_khand, trp_no_troop, pt_khand_recruits, trp_khand_lord, trp_i1_khand_bondsman, trp_i3_khand_warrior,trp_i3_khand_pitfighter,trp_i4_khand_pit_champion], 
	[icon_mfc_khand],[900],[2,1,4,1,4,1], 0, garrison_limit_evil_low, 3, tld_siegable_always),
(p_advcamp_umbar, [scn_advcamp_umbar, -1, -1,-1,-1, scn_advcamp_umbar_siege, mesh_town_evilcamp],
	[-1, trp_smith_umbar, trp_merchant_umbar, trp_no_troop, pt_umbar_recruits, trp_umbar_lord, trp_i1_corsair_youth, trp_i2_corsair_warrior, trp_a4_corsair_veteran_marksman,trp_a2_corsair_marine], 
	[icon_mfc_umbar],[900],[2,1,4,1,4,1], 0, garrison_limit_evil_low, 3, tld_siegable_always),
(p_advcamp_lorien, [scn_advcamp_lorien, -1, -1, -1, -1, scn_advcamp_lorien_siege, mesh_town_goodcamp],
	[-1, trp_smith_camroth, trp_merchant_camroth, trp_no_troop, pt_lorien_recruits,  trp_lorien_lord, trp_a1_lorien_scout, trp_a3_lorien_vet_warden, trp_a2_lorien_archer, trp_i3_lorien_inf], 
	[icon_mfc_lorien],[900],[2,1,4,1,4,1], 0, garrison_limit_low, 3, tld_siegable_always),
(p_advcamp_imladris, [scn_advcamp_imladris, -1, -1,-1,-1, scn_advcamp_imladris_siege, mesh_town_goodcamp],
	[-1, trp_smith_imladris, trp_merchant_imladris, trp_no_troop, pt_imladris_recruits, trp_imladris_lord, trp_a1_riv_scout,trp_i3_riv_swordbearer, trp_a3_riv_archer,trp_a1_arnor_scout], 
	[icon_mfc_imladris],[900],[2,1,4,1,4,1], 0, garrison_limit_low, 3, tld_siegable_always),
(p_advcamp_woodelf, [scn_advcamp_mirkwood, -1, -1,-1,-1, scn_advcamp_mirkwood_siege, mesh_town_goodcamp],
	[-1, trp_smith_woodelf_camp, trp_merchant_woodelf_camp, trp_no_troop, pt_woodelf_recruits, trp_woodelf_lord, trp_a3_greenwood_archer, trp_a1_greenwood_scout, trp_a3_greenwood_archer, trp_i2_greenwood_infantry], 
	[icon_mfc_woodelf],[900],[2,1,4,1,4,1], 0, garrison_limit_low, 3, tld_siegable_always),
(p_advcamp_moria, [scn_advcamp_moria, -1, -1,-1,-1, scn_advcamp_moria_siege, mesh_town_evilcamp],
	[-1, trp_smith_moria_ac, trp_merchant_moria, trp_no_troop, pt_moria_recruits, trp_moria_lord,trp_i1_moria_snaga,trp_i2_moria_goblin,trp_c3_moria_wolf_rider,trp_i3_moria_large_goblin], 
	[icon_mfc_moria],[900],[2,1,4,1,4,1], 0, garrison_limit_evil_low, 3, tld_siegable_always),
(p_advcamp_guldur, [scn_advcamp_guldur, -1, -1,-1,-1, scn_advcamp_guldur_siege, mesh_town_evilcamp],
	[-1, trp_smith_dolguldur, trp_merchant_dolguldur, trp_no_troop, pt_guldur_recruits, trp_guldur_lord, trp_i2_mordor_uruk, trp_i2_mordor_orc, trp_i3_mordor_large_orc, trp_a3_guldur_large_orc_tracker], 
	[icon_mfc_guldur],[900],[2,1,4,1,4,1], 0, garrison_limit_evil_low, 3, tld_siegable_always),
(p_advcamp_gundabad, [scn_advcamp_gundabad, -1, -1,-1,-1, scn_advcamp_gundabad_siege, mesh_town_evilcamp],
	[-1, trp_smith_gundabad, trp_merchant_gundabad, trp_no_troop, pt_gundabad_recruits, trp_gundabad_lord,trp_i1_gunda_goblin,trp_i2_gunda_orc,trp_i3_gunda_orc_fighter,trp_c4_gunda_warg_rider], 
	[icon_mfc_gundabad],[900],[2,1,4,1,4,1], 0, garrison_limit_evil_low, 3, tld_siegable_always),
(p_advcamp_dale, [scn_advcamp_dale, -1, -1, -1, -1, scn_advcamp_dale_siege, mesh_town_goodcamp],
	[-1, trp_smith_dale_ac, trp_merchant_esgaroth, trp_no_troop, pt_dale_recruits, trp_dale_lord,trp_i3_dale_swordsman,trp_i4_dale_billman,trp_i5_dale_hearthman,trp_a4_dale_archer], 
	[icon_mfc_dale],[900],[2,1,4,1,4,1], 0, garrison_limit_low, 3, tld_siegable_always),
(p_advcamp_dwarf, [scn_advcamp_erebor, -1, -1,-1,-1, scn_advcamp_erebor_siege, mesh_town_goodcamp],
	[-1, trp_smith_ironhill, trp_merchant_ironhill, trp_no_troop, pt_dwarf_recruits, trp_dwarf_lord,trp_a2_dwarf_lookout, trp_a4_dwarf_bowman, trp_i4_iron_hills_infantry, trp_i2_iron_hills_miner], 
	[icon_mfc_dwarf],[900],[2,1,4,1,4,1], 0, garrison_limit_low, 3, tld_siegable_always),
(p_advcamp_dunland, [scn_advcamp_dunland, -1, -1,-1,-1, scn_advcamp_dunland_siege, mesh_town_evilcamp],
	[-1, trp_smith_dunland, trp_merchant_dunland, trp_no_troop, pt_dunland_recruits, trp_dunland_lord, trp_i1_dun_wildman,trp_i2_dun_warrior, trp_i3_dun_pikeman, trp_i5_dun_wolf_guard], 
	[icon_mfc_dunland],[900],[2,1,4,1,4,1], 0, garrison_limit_evil_low, 3, tld_siegable_always),
(p_advcamp_beorn, [scn_advcamp_beorn, -1, -1,-1,-1, scn_advcamp_beorn_siege, mesh_town_goodcamp],
	[-1, trp_smith_beorn_ac, trp_merchant_woodmen, trp_no_troop, pt_beorn_recruits, trp_beorn_lord, trp_i5_beorning_carrock_berserker, trp_i4_beorning_sentinel, trp_i2_beorning_warrior, trp_i3_beorning_tolltacker], 
	[icon_mfc_northmen],[900],[2,1,4,1,4,1], 0, garrison_limit_low, 3, tld_siegable_always),
]

# evil camps that will appear only when War starts
centers_disabled_at_start =	[
  p_town_orc_sentry_camp, p_town_urukhai_outpost, p_town_urukhai_r_camp,#p_town_dunland_camp,
  p_town_dol_guldur_north_outpost, p_town_rhun_south_camp, p_town_rhun_north_camp, p_town_gundabad_ne_outpost, 
  p_town_gundabad_nw_outpost, p_town_goblin_south_outpost, p_town_gundabad_m_outpost #, p_town_goblin_north_outpost
]		 
#### end of center descriptions

# forest tree seeding. 1-scene prop to use, 2-number of times to repeat, 3-displacement vector, 4-vector rotation angle, then repeat with other scene prop 
#forest_list = [
# rohan steppe
# ("spr_tree1","spr_tree2","spr_tree3","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4",
# "spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4"),
# broadleaf forest
# ("spr_tree1","spr_tree2","spr_tree3","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4",
# "spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4"),
# pine forest
# ("spr_tree1","spr_tree2","spr_tree3","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4",
# "spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4","spr_tree4"),
#]
# landmark seeding. 1-sceneprop, 2-xcoord, 3-ycoord, (optional things) 4-zcoord,5-xpitch,6-zpitch, separated from next prop by -1
# 1-3th placeholders standard size, 4th placeholder double size, 5th placeholder 1/2 size
#landmark_list = [
# ("spr_ruin1",0,0,-1,"spr_bush1",10,10,-1,"spr_tree1",-10,10,-1,"spr_tree1",-10,-10,-1,"spr_tree1",10,-10,-1),
#]

# trade routes structure. 1st town in line connected with all others in line. Repeat for each line. 
routes_list = [ 
 (p_town_minas_tirith,     p_town_pelargir, p_town_dol_amroth, p_town_erech, p_town_pinnath_gelin, p_town_edoras, p_town_hornburg, p_town_east_emnet, p_town_west_emnet, p_town_eastfold, p_advcamp_gondor),
 (p_town_pelargir,         p_town_dol_amroth, p_town_lossarnach, p_town_erech, p_town_hornburg, p_town_east_emnet, p_town_west_emnet, p_town_eastfold),
 (p_town_linhir,           p_town_dol_amroth, p_town_edhellond, p_town_lossarnach, p_town_tarnost, p_town_westfold, p_town_west_emnet, p_town_minas_morgul),
 (p_town_dol_amroth,       p_town_lossarnach, p_town_hornburg, p_town_east_emnet, p_town_west_emnet, p_town_eastfold),
 (p_town_edhellond,        p_town_lossarnach, p_town_tarnost, p_town_westfold, p_town_west_emnet),
 (p_town_lossarnach,       p_town_tarnost, p_town_edoras, p_town_east_emnet, p_town_west_emnet, p_town_eastfold, p_town_morannon),
 (p_town_tarnost,          p_town_aldburg, p_town_edoras, p_town_east_emnet, p_town_westfold, p_town_west_emnet, p_town_eastfold),
 (p_town_erech,            p_town_pinnath_gelin, p_town_edoras, p_town_hornburg, p_town_east_emnet, p_town_eastfold),
 (p_town_pinnath_gelin,    p_town_edoras, p_town_hornburg, p_town_east_emnet, p_town_eastfold),
 (p_town_aldburg,          p_town_edoras, p_town_westfold),
 (p_town_edoras,           p_town_hornburg, p_town_east_emnet, p_town_westfold, p_town_eastfold, p_advcamp_rohan),
 (p_town_hornburg,         p_town_east_emnet, p_town_eastfold),
 (p_town_eastfold,         p_town_east_emnet, p_town_west_emnet),
 (p_town_morannon,         p_town_minas_morgul, p_town_cirith_ungol,p_town_east_osgiliath, p_advcamp_mordor),
 (p_town_erebor,           p_town_dale,p_town_esgaroth, p_town_ironhill_camp, p_advcamp_dwarf),
 (p_town_dale,             p_advcamp_dale),
 (p_town_isengard,         p_town_urukhai_outpost,p_town_urukhai_h_camp,p_town_urukhai_r_camp, p_advcamp_isengard),
 (p_town_gundabad,         p_town_gundabad_ne_outpost,p_town_gundabad_nw_outpost,p_town_goblin_north_outpost,p_town_goblin_south_outpost,p_town_gundabad_m_outpost, p_advcamp_gundabad),
 (p_town_dol_guldur,       p_town_dol_guldur_north_outpost, p_advcamp_guldur),
 (p_town_caras_galadhon,   p_town_thranduils_halls, p_town_imladris_camp, p_town_cerin_dolen, p_town_cerin_amroth, p_advcamp_lorien),
 (p_town_thranduils_halls, p_town_imladris_camp, p_town_woodelf_camp, p_town_woodelf_west_camp, p_advcamp_woodelf),
 (p_town_imladris_camp,    p_advcamp_imladris),
 (p_town_beorn_house,	   p_town_woodsmen_village, p_town_beorning_village),
]

lords_spawn = [ (trp_knight_1_1, p_town_calembel),
				(trp_knight_1_2, p_town_minas_tirith),
                (trp_knight_1_3, p_town_dol_amroth),
                (trp_knight_1_4, p_town_pelargir),
                (trp_knight_1_5, p_town_erech),
                (trp_knight_1_6, p_town_pinnath_gelin),
                (trp_knight_1_7, p_town_west_osgiliath),
                (trp_knight_1_8, p_town_lossarnach),
                (trp_knight_2_51,p_town_minas_morgul),
                (trp_knight_5_3, p_town_esgaroth),
                (trp_knight_5_1, p_town_dale),
                (trp_knight_5_2, p_town_dale),
                (trp_knight_6_1, p_town_calembel),
                (trp_knight_6_2, p_town_pinnath_gelin),
				(trp_knight_4_11, p_town_woodsmen_village)
]

#### banner colors #0-130
color_list = [ 0xFF8f4531, 0xFF315458, 0xFF373736, 0xFFa48b28, 0xFF497735, 0xFF82362d, 0xFF793329, 0xFF262521, 0xFFd9dad1, 0xFF524563, 
               0xFF91312c, 0xFFafa231, 0xFF706d3c, 0xFFd6d3ce, 0xFF912929, 0xFF394584, 0xFF42662e, 0xFFdfded6, 0xFF292724, 0xFF58611b, 
               0xFF313a67, 0xFFb5a231, 0xFFbdb629, 0xFF6e7929, 0xFFd6d3ce, 0xFF94a642, 0xFF944131, 0xFF893b34, 0xFF425510, 0xFF94452e, 
               0xFF475a94, 0xFFd1b231, 0xFFe1e2df, 0xFF4a4942, 0xFFc6b74d, 0xFF7b5184, 0xFF212421, 0xFF3c5d9a, 0xFF4d7136, 0xFFdfdfd6,
               0xFF527539, 0xFF9c3c39, 0xFF42518c, 0xFFa46a2c, 0xFF843829, 0xFF2c6189, 0xFF556421, 0xFF9d621e, 0xFFdeded6, 0xFF6e4891,
               0xFF865a29, 0xFFdedfd9, 0xFF524273, 0xFF8c3821, 0xFF948403, 0xFF313031, 0xFF47620d, 0xFFdfded6, 0xFFd6d7d6, 0xFF2e2f2c,
               0xFF604283, 0xFF395584, 0xFF313031, 0xFF7e3f2e, 0xFF343434, 0xFF3c496b, 0xFFd9d8d1, 0xFF99823c, 0xFF9f822e, 0xFF393839,
               0xFFa54931, 0xFFdfdcd6, 0xFF9f4a36, 0xFF8c7521, 0xFF9f4631, 0xFF793324, 0xFF395076, 0xFF2c2b2c, 0xFF657121, 0xFF7e3121,
               0xFF76512e, 0xFFe7e3de, 0xFF947921, 0xFF4d7b7c, 0xFF343331, 0xFFa74d36, 0xFFe7e3de, 0xFFd6d8ce, 0xFF3e4d67, 0xFF913331,
               0xFF4d6994, 0xFF4a6118, 0xFFd9d8d3, 0xFF394479, 0xFF343331, 0xFF3f4d5d, 0xFF4a6489, 0xFF313031, 0xFFd6d7ce, 0xFFc69e00,
               0xFF638e52, 0xFFdcdbd3, 0xFFdbdcd3, 0xFF843831, 0xFFcecfc6, 0xFF8f4431, 0xFF602926, 0xFFd3d4cb, 0xFFdcdbd3, 0xFF556024,
               0xFF602d2c, 0xFF315184, 0xFF313031, 0xFFe7e7e7, 0xFF526d47, 0xFFdedbd6, 0xFFb2a631, 0xFF76713f, 0xFFdedbd6, 0xFFe9eae7,
               0xFF6b5131, 0xFF31557b, 0xFF703324, 0xFFe7e3de, 0xFFd6d7ce, 0xFF3f6e39, 
               # default banners			   
               0xFF212221, 0xFF212221, 0xFF2E3B10, 0xFF425D7B, 0xFF394608 ]
            
# foxyman (swy: this option controls most of the TLD developer options and menus)
cheat_switch = 1
# TLD faction ranks end

faction_strings =[#shop rumors begin	shop rumors end          loop_ambient_day      loop_ambient_always		occasional_ambient(later to be divided into occasional nature and occasional faction)
 (fac_gondor  ,str_gondor_rumor_begin  ,str_dwarf_rumor_begin   ,snd_gondor_ambiance ,snd_wind_ambiance      ,snd_gondor_occasional),
 (fac_rohan   ,str_rohan_rumor_begin   ,str_gondor_rumor_begin  ,snd_rohan_ambiance  ,snd_wind_ambiance      ,snd_rohan_occasional),
 (fac_isengard,str_isengard_rumor_begin,str_rhun_rumor_begin    ,snd_orcs_ambiance   ,snd_wind_ambiance      ,snd_urukhai_occasional),
 (fac_mordor  ,str_mordor_rumor_begin  ,str_isengard_rumor_begin,0                   ,snd_wind_ambiance      ,snd_orc_occasional),
 (fac_harad   ,str_harad_rumor_begin   ,str_gunda_rumor_begin   ,snd_harad_ambiance  ,snd_wind_ambiance      ,snd_harad_occasional),
 (fac_rhun    ,str_rhun_rumor_begin    ,str_dunland_rumor_begin ,snd_evilmen_ambiance,snd_wind_ambiance      ,snd_rhun_occasional),
 (fac_khand   ,str_khand_rumor_begin   ,str_good_rumor_begin    ,snd_evilmen_ambiance,snd_wind_ambiance      ,snd_rhun_occasional),
 (fac_umbar   ,str_umbar_rumor_begin   ,str_khand_rumor_begin   ,snd_evilmen_ambiance,snd_water_waves_ambiance,snd_umbar_occasional),
 (fac_lorien  ,str_lorien_rumor_begin  ,str_imladris_rumor_begin,0                   ,snd_goodforest_ambiance,snd_lorien_occasional),
 (fac_imladris,str_imladris_rumor_begin,str_woodelf_rumor_begin ,0                   ,snd_goodforest_ambiance,snd_elves_occasional),
 (fac_woodelf ,str_woodelf_rumor_begin ,str_dale_rumor_begin    ,0                   ,snd_goodforest_ambiance,snd_elves_occasional),
 (fac_moria   ,str_moria_rumor_begin   ,str_umbar_rumor_begin   ,0                   ,snd_moria_ambiance     ,snd_moria_occasional),
 (fac_guldur  ,str_mordor_rumor_begin  ,str_isengard_rumor_begin,snd_orcs_ambiance   ,snd_evilforest_ambiance,snd_orc_occasional),
 (fac_gundabad,str_gunda_rumor_begin   ,str_moria_rumor_begin   ,snd_orcs_ambiance   ,snd_wind_ambiance      ,snd_orc_occasional),
 (fac_dale    ,str_dale_rumor_begin    ,str_harad_rumor_begin   ,snd_rohan_ambiance  ,snd_wind_ambiance      ,snd_dale_occasional),
 (fac_dwarf   ,str_dwarf_rumor_begin   ,str_mordor_rumor_begin  ,snd_dwarf_ambiance  ,snd_wind_ambiance      ,snd_dwarf_occasional),
 (fac_dunland ,str_dunland_rumor_begin ,str_beorn_rumor_begin   ,snd_evilmen_ambiance,snd_wind_ambiance      ,snd_dunland_occasional),
 (fac_beorn   ,str_beorn_rumor_begin   ,str_lorien_rumor_begin  ,snd_rohan_ambiance  ,snd_neutralforest_ambiance,snd_beorn_occasional),
]
# specific ambient sounds for selected centers  ]+concatenate_scripts([[     ] for ct in range(cheat_switch)])+[
center_sounds=[#center      specific day ambiance , specific always ambiance      , occasional sounds (later to be divided into occasional nature and occasional faction)
    (p_town_dol_amroth   ,snd_gondor_ambiance ,snd_water_waves_ambiance     ,snd_seaside_occasional),
    (p_town_pelargir     ,snd_gondor_ambiance ,snd_water_wavesplash_ambiance,snd_seaside_occasional),
    (p_town_edhellond    ,snd_gondor_ambiance ,snd_water_waves_ambiance     ,snd_seaside_occasional),
    (p_town_cair_andros  ,0                   ,snd_water_splash_ambiance    ,snd_elves_occasional),
    (p_town_henneth_annun,0                   ,snd_henneth_ambiance         ,snd_elves_occasional),
    (p_town_isengard     ,snd_orcs_ambiance   ,snd_isengard_ambiance        ,snd_isengard_occasional),
    (p_town_west_osgiliath,0                  ,0         					,snd_wosgi_occasional),
    (p_town_east_osgiliath,0                  ,0 		           			,snd_eosgi_occasional),
    (p_town_esgaroth     ,snd_town_ambiance   ,snd_water_splash_ambiance    ,snd_beorn_occasional),
    (p_town_lossarnach   ,snd_gondor_ambiance ,snd_goodforest_ambiance      ,snd_elves_occasional),
    (p_town_pinnath_gelin,snd_gondor_ambiance ,snd_goodforest_ambiance      ,snd_elves_occasional),
    (p_town_erebor       ,snd_town_ambiance   ,snd_moria_ambiance           ,snd_dwarf_occasional),
    (p_town_minas_morgul ,0                   ,snd_morgul_ambiance          ,snd_morgul_occasional),
    (p_town_gundabad_m_outpost,snd_orcs_ambiance,snd_evilforest_ambiance	,snd_orc_occasional),
    (p_town_troll_cave   ,0                   ,snd_evilforest_ambiance      ,snd_orc_occasional),
    (p_town_morannon     ,0                   ,snd_wind_ambiance            ,0),
	(p_town_goblin_north_outpost     ,0       ,snd_moria_ambiance           ,0),
	(p_town_beorn_house,snd_bees_people_ambiance,snd_neutralforest_ambiance      ,snd_beorn_occasional),
	(p_town_woodsmen_village     ,0     	  ,snd_evilforest_ambiance      ,snd_beorn_occasional),
] 

## tableau meshes list for factions
fac_tableau_list = [
[(tableau_tld_tunic, [mesh_tableau_mesh_gondor_tunic_a, mesh_tableau_mesh_gondor_tunic_b]),],#fac_gondor = 3
[],#fac_dwarf = 4
[(tableau_tld_tunic, [mesh_tableau_mesh_rohan_tunic]),],#fac_rohan = 5
[],#fac_mordor = 6
[],#fac_isengard = 7
[],#fac_lorien = 8
[],#fac_imladris = 9
[],#fac_woodelf = 10
[(tableau_tld_tunic, [mesh_tableau_mesh_dale_tunic]),],#fac_dale = 11
[],#fac_harad = 12
[],#fac_rhun = 13
[],#fac_khand = 14
[],#fac_umbar = 15
[],#fac_moria = 16
[],#fac_guldur = 17
[],#fac_gundabad = 18
[],#fac_dunland = 19
[(tableau_tld_tunic, [mesh_tableau_mesh_woodman_tunic]),],#fac_beorn = 20
]

## Reward items (rank number 0-9, item id, item modifier); rank rewards; faction rewards
## TODO: fill out the list, these are test values
fac_reward_items_list = [

] + (is_a_wb_constant and [

#fac_gondor
[(2,itm_cooking_cauldron,0),(3,itm_herbarium_reward,0),(4,itm_gondor_shield_e, 0), (5, itm_silmarillion_reward, 0), (6, itm_gon_tower_guard, 0), (7, itm_tower_guard_helm, 0), (8, itm_westernesse1h_reward, 0), (9, itm_horn_gondor_reward, 0)],
#fac_dwarf
[(2,itm_cooking_cauldron,0),(3,itm_hammer_reward ,0),(4,itm_dwarf_throwing_axe_reward, 0), (5, itm_dwarf_shield_reward, 0), (6, itm_gauntlets_reward, imod_lordly), (7, itm_dwarf_armor_c, imod_lordly), (8, itm_dwarf_great_axe_reward, 0), (9, itm_dwarf_helm_p, imod_lordly)],
#fac_rohan
[(2,itm_cooking_cauldron,0),(3,itm_map           ,0),(4,itm_rohirrim_courser2, imod_heavy), (5, itm_rohan_lance_banner_horse, imod_balanced), (6, itm_rohan_armor_th, 0), (7, itm_rohan_saddle, imodbit_lordly), (8, itm_eorl_cavalry_sword, 0), (9, itm_mearas_reward, 0)],
#fac_mordor
[(2,itm_cooking_cauldron,0),(3,itm_orc_brew      ,0),(4,itm_orc_hammer, imod_balanced), (5, itm_warg_reward, 0), (6, itm_angmar_whip_reward, 0), (7, itm_m_cap_armor, imod_reinforced), (8, itm_mordor_warhorse2, imod_heavy), (9, itm_nazgul_sword, 0)],
#fac_isengard
[(2,itm_cooking_cauldron,0),(3,itm_orc_brew      ,0),(4,itm_gauntlets_reward, imod_hardened), (5, itm_warg_reward, 0), (6, itm_torque_reward, 0), (7, itm_silmarillion_reward, 0), (8, itm_isen_uruk_heavy_reward, imod_lordly), (9, itm_tome_of_knowledge, 0)],
#fac_lorien
[(2,itm_lembas          ,0),(3,itm_athelas_reward,0),(4,itm_elven_amulet_reward, 0), (5, itm_elven_cloak , 0), (6, itm_silmarillion_reward, 0), (7, itm_tiara_reward, 0), (8, itm_lorien_bow_reward, imod_balanced), (9, itm_phial_reward, 0)],
#fac_imladris
[(2,itm_lembas          ,0),(3,itm_athelas_reward,0),(4,itm_scroll_reward, 0), (5, itm_miruvor_reward, 0), (6, itm_riv_warhorse2, 0), (7, itm_westernesse2h_reward, 0), (8, itm_shield_of_tuor, 0), (9, itm_riv_armor_reward, 0)],
#fac_woodelf
[(2,itm_lembas          ,0),(3,itm_athelas_reward,0),(4,itm_elven_amulet_reward, 0), (5, itm_mirkwood_bow, imod_balanced), (6, itm_mirkwood_great_spear, imod_masterwork), (7, itm_ring_b_reward, 0), (8, itm_woodelf_arrows, imod_masterwork), (9, itm_mirkwood_sword_reward, 0)],
#fac_dale
[(2,itm_cooking_cauldron,0),(3,itm_map ,0),			(4,itm_leather_gloves_reward, 0), (5, itm_thrush_reward, 0), (6, itm_dale_armor_reward, 0), (7, itm_dale_sword_reward, imod_masterwork), (8, itm_black_arrows_reward, imod_masterwork), (9, itm_dale_bow_reward, 0)],
#fac_harad
[(2,itm_cooking_cauldron,0),(3,itm_map           ,0),(4,itm_lg_bow, imod_balanced), (5, itm_rohan_saddle, imod_masterwork), (6, itm_herbarium_reward, 0), (7, itm_eagle_guard_spear, imod_masterwork), (8, itm_black_snake_armor, imod_lordly), (9, itm_harad_totem_reward, 0)],
#fac_rhun
[(2,itm_cooking_cauldron,0),(3,itm_rhun_horse_d, imod_heavy),(4,itm_rohan_saddle, imod_heavy), (5, itm_rhun_greataxe, imod_balanced), (6, itm_ring_a_reward, 0), (7, itm_rhun_horse_h, 0), (8, itm_rhun_bow, imod_balanced), (9, itm_khamul_helm, 0)],
#fac_khand
[(2,itm_cooking_cauldron,0),(3,itm_hammer_reward ,0),(4,itm_khand_lance, imod_balanced), (5, itm_torque_reward, 0), (6, itm_ring_a_reward, 0), (7, itm_variag_kataphrakt, imod_champion), (8, itm_khand_rammace, imod_masterwork),  (9, itm_khand_knife_reward, 0)],
#fac_umbar
[(2,itm_cooking_cauldron,0),(3,itm_map           ,0),(4,itm_corsair_throwing_dagger_reward, 0), (5, itm_leather_gloves_reward, 0), (6, itm_ring_b_reward, 0), (7, itm_corsair_bow, imod_balanced), (8,itm_corsair_trident , 0), (9, itm_umb_helm_reward, 0)],
#fac_moria
[(2,itm_cooking_cauldron,0),(3,itm_orc_brew      ,0),(4,itm_moria_orc_shield_c, imod_reinforced), (5, itm_wargarmored_3a, imod_reinforced), (6, itm_ring_b_reward, 0), (7, itm_dwarf_great_pick, imod_strong), (8, itm_moria_armor_e, imod_lordly), (9, itm_drums_of_the_deep, 0)],
#fac_guldur
[(2,itm_cooking_cauldron,0),(3,itm_orc_brew      ,0),(4,itm_orc_club_d, imod_balanced), (5, itm_leather_gloves_reward, imod_crude), (6, itm_herbarium_reward, 0), (7, itm_spider, 0), (8, itm_black_arrows_reward, 0), (9, itm_witchking_helmet, 0)],
#fac_gundabad
[(2,itm_cooking_cauldron,0),(3,itm_orc_brew      ,0),(4, itm_orc_throwing_axes_reward, 0), (5, itm_uruk_falchion_b, imod_balanced), (6, itm_warg_reward, 0), (7, itm_gundabad_helm_e, imod_lordly), (8, itm_gundabad_armor_e, imod_lordly), (9, itm_orc_idol_reward, 0)],
#fac_dunland
[(2,itm_cooking_cauldron,0),(3,itm_garlic_reward ,0),(4, itm_crebain_reward, 0), (5, itm_wilderness_cowl, 0), (6, itm_fur_gloves_reward, 0), (7, itm_leather_boots_reward, 0), (8, itm_dunland_armor_k, imod_lordly), (9, itm_dun_berserker, imod_masterwork)],
#fac_beorn
[(2,itm_cooking_cauldron,0),(3, itm_fur_gloves_reward, 0),(4, itm_leather_boots_reward, 0), (5, itm_wilderness_cowl, 0), (6, itm_herbarium_reward, 0), (7, itm_beorn_axe_reward, imod_masterwork), (8, itm_beorn_chief, imod_lordly), (9, itm_beorn_shield_reward, imod_reinforced)],

] or [
#fac_gondor
[(2,itm_cooking_cauldron,0),(3,itm_herbarium_reward,0),(4,itm_gondor_shield_e, 0), (5, itm_silmarillion_reward, 0), (6, itm_gon_tower_guard, 0), (7, itm_tower_guard_helm, 0), (8, itm_westernesse1h_reward, 0), (9, itm_horn_gondor_reward, 0)],
#fac_dwarf
[(2,itm_cooking_cauldron,0),(3,itm_hammer_reward ,0),(4,itm_dwarf_throwing_axe_reward, 0), (5, itm_dwarf_shield_reward, 0), (6, itm_gauntlets_reward, imod_lordly), (7, itm_dwarf_armor_c, imod_lordly), (8, itm_dwarf_great_axe_reward, 0), (9, itm_dwarf_helm_p, imod_lordly)],
#fac_rohan
[(2,itm_cooking_cauldron,0),(3,itm_map           ,0),(4,itm_rohirrim_courser2, imod_heavy), (5, itm_rohan_lance_banner_horse, imod_balanced), (6, itm_rohan_armor_th, 0), (7, itm_rohan_saddle, imodbit_lordly), (8, itm_eorl_cavalry_sword, 0), (9, itm_mearas_reward, 0)],
#fac_mordor
[(2,itm_cooking_cauldron,0),(3,itm_orc_brew      ,0),(4,itm_orc_hammer, imod_balanced), (5, itm_warg_reward, 0), (6, itm_angmar_whip_reward, 0), (7, itm_m_cap_armor, imod_reinforced), (8, itm_mordor_warhorse2, imod_heavy), (9, itm_nazgul_sword, 0)],
#fac_isengard
[(2,itm_cooking_cauldron,0),(3,itm_orc_brew      ,0),(4,itm_gauntlets_reward, imod_hardened), (5, itm_warg_reward, 0), (6, itm_torque_reward, 0), (7, itm_silmarillion_reward, 0), (8, itm_isen_uruk_heavy_reward, imod_lordly), (9, itm_tome_of_knowledge, 0)],
#fac_lorien
[(2,itm_lembas          ,0),(3,itm_athelas_reward,0),(4,itm_elven_amulet_reward, 0), (5, itm_elven_cloak , 0), (6, itm_silmarillion_reward, 0), (7, itm_tiara_reward, 0), (8, itm_lorien_bow_reward, imod_balanced), (9, itm_phial_reward, 0)],
#fac_imladris
[(2,itm_lembas          ,0),(3,itm_athelas_reward,0),(4,itm_scroll_reward, 0), (5, itm_miruvor_reward, 0), (6, itm_riv_warhorse2, 0), (7, itm_westernesse2h_reward, 0), (8, itm_shield_of_tuor, 0), (9, itm_riv_armor_reward, 0)],
#fac_woodelf
[(2,itm_lembas          ,0),(3,itm_athelas_reward,0),(4,itm_elven_amulet_reward, 0), (5, itm_mirkwood_bow, imod_balanced), (6, itm_mirkwood_great_spear, imod_masterwork), (7, itm_ring_b_reward, 0), (8, itm_woodelf_arrows, imod_masterwork), (9, itm_mirkwood_sword_reward, 0)],
#fac_dale
[(2,itm_cooking_cauldron,0),(3,itm_map ,0),			(4,itm_leather_gloves_reward, 0), (5, itm_thrush_reward, 0), (6, itm_dale_armor_reward, 0), (7, itm_dale_sword_reward, imod_masterwork), (8, itm_black_arrows_reward, imod_masterwork), (9, itm_dale_bow_reward, 0)],
#fac_harad
[(2,itm_cooking_cauldron,0),(3,itm_map           ,0),(4,itm_lg_bow, imod_balanced), (5, itm_rohan_saddle, imod_masterwork), (6, itm_herbarium_reward, 0), (7, itm_eagle_guard_spear, imod_masterwork), (8, itm_black_snake_armor, imod_lordly), (9, itm_harad_totem_reward, 0)],
#fac_rhun
[(2,itm_cooking_cauldron,0),(3,itm_rhun_horse_d, imod_heavy),(4,itm_rohan_saddle, imod_heavy), (5, itm_rhun_greataxe, imod_balanced), (6, itm_ring_a_reward, 0), (7, itm_rhun_horse_h, 0), (8, itm_rhun_bow, imod_balanced), (9, itm_khamul_helm, 0)],
#fac_khand
[(2,itm_cooking_cauldron,0),(3,itm_hammer_reward ,0),(4,itm_khand_lance, imod_balanced), (5, itm_torque_reward, 0), (6, itm_ring_a_reward, 0), (7, itm_variag_kataphrakt, imod_champion), (8, itm_khand_rammace, imod_masterwork),  (9, itm_khand_knife_reward, 0)],
#fac_umbar
[(2,itm_cooking_cauldron,0),(3,itm_map           ,0),(4,itm_corsair_throwing_dagger_reward, 0), (5, itm_leather_gloves_reward, 0), (6, itm_ring_b_reward, 0), (7, itm_corsair_bow, imod_balanced), (8,itm_corsair_trident , 0), (9, itm_umb_helm_reward, 0)],
#fac_moria
[(2,itm_cooking_cauldron,0),(3,itm_orc_brew      ,0),(4,itm_moria_orc_shield_c, imod_reinforced), (5, itm_wargarmored_3a, imod_reinforced), (6, itm_ring_b_reward, 0), (7, itm_dwarf_great_pick, imod_strong), (8, itm_moria_armor_e, imod_lordly), (9, itm_drums_of_the_deep, 0)],
#fac_guldur
[(2,itm_cooking_cauldron,0),(3,itm_orc_brew      ,0),(4,itm_orc_club_d, imod_balanced), (5, itm_leather_gloves_reward, imod_crude), (6, itm_herbarium_reward, 0), (7, itm_spider, 0), (8, itm_black_arrows_reward, 0), (9, itm_witchking_helmet, 0)],
#fac_gundabad
[(2,itm_cooking_cauldron,0),(3,itm_orc_brew      ,0),(4, itm_orc_throwing_axes_reward, 0), (5, itm_uruk_falchion_b, imod_balanced), (6, itm_warg_reward, 0), (7, itm_gundabad_helm_e, imod_lordly), (8, itm_gundabad_armor_e, imod_lordly), (9, itm_orc_idol_reward, 0)],
#fac_dunland
[(2,itm_cooking_cauldron,0),(3,itm_garlic_reward ,0),(4, itm_crebain_reward, 0), (5, itm_wilderness_cowl, 0), (6, itm_fur_gloves_reward, 0), (7, itm_leather_boots_reward, 0), (8, itm_dunland_armor_k, imod_lordly), (9, itm_dun_berserker, imod_masterwork)],
#fac_beorn
[(2,itm_cooking_cauldron,0),(3, itm_fur_gloves_reward, 0),(4, itm_leather_boots_reward, 0), (5, itm_wilderness_cowl, 0), (6, itm_herbarium_reward, 0), (7, itm_beorn_axe_reward, imod_masterwork), (8, itm_beorn_chief, imod_lordly), (9, itm_beorn_shield_reward, imod_reinforced)],
]) + [ 

]

#Formations and AI by Motomataru with adjustments by Treebeard (JL) and MadVader (MV)

#Formation modes
formation_none		= 0
formation_default	= 1
formation_ranks		= 2
formation_shield	= 3
formation_wedge		= 4
formation_square	= 5

#Formation tweaks
formation_minimum_spacing_horse_length	= 300
formation_minimum_spacing_horse_width	= 200
formation_minimum_spacing	= 67
formation_start_spread_out	= 2
formation_min_foot_troops	= 12
formation_min_cavalry_troops	= 5
formation_autorotate_at_player	= 1
#formation_native_ai_use_formation = 1 #replaced by $tld_option_formations in TLD
formation_delay_for_spawn	= .4
formation_stagger_archers	= 0

from header_triggers import *
key_for_ranks	= key_j
key_for_shield	= key_k
key_for_wedge	= key_l
key_for_square	= key_semicolon
key_for_undo	= key_u
key_for_skirmish = key_comma #Kham - Skirmish Key Toggle
key_for_skirmish_end = key_period

#Kham - Formations Additions START
slot_team_d0_type                       = 185 

#Presentations Constants Moto chief
Screen_Border_Width = 24
Screen_Width = 1024-Screen_Border_Width
Screen_Height = 768-Screen_Border_Width
Screen_Text_Height = 35
Screen_Checkbox_Height_Adj = 4
Screen_Numberbox_Width = 64
Screen_Title_Height = Screen_Height-Screen_Border_Width-Screen_Text_Height
Screen_Check_Box_Dimension = 20
Screen_Undistort_Width_Num = 7  #distortion midway between 1024x768 and 1366x768 -- things will appear a little narrow on thin screens and vice versa
Screen_Undistort_Width_Den = 8

#Kham - Formations Additions END

###FormAI_constants:
#AI variables
AI_long_range	= 15000	#do not put over 130m if you want archers to always fire
AI_firing_distance	= AI_long_range / 2
AI_charge_distance	= 2000
AI_Self_Defence_Distance = 1500 #range for preparing for self defense, JL
AI_for_kingdoms_only	= 1
Weapon_Length_Proxy	= 100
Far_Away	= 1000000
Percentage_Cav_For_New_Dest	= 40
Hold_Point	= 100	#archer hold if outnumbered
Advance_More_Point	= 100 - Hold_Point * 100 / (Hold_Point + 100)	#advance 'cause expect other side is holding
AI_Delay_For_Spawn	= formation_delay_for_spawn + .1	#fire AFTER formations init

#Battle Phases
BP_Setup	= 1
BP_Jockey	= 2
BP_Fight	= 3
#BP_Charge   = 4 #JL not used now, but could be useful in the future
#BP_InfCharge = 5 #JL not used now, but could be useful in the future

#positions used in a script, named for convenience
Nearest_Enemy_Troop_Pos	= 46	#pos46
Nearest_Non_Cav_Enemy_Troop_Pos	= 47	#pos47
Nearest_Threat_Pos	= 48	#pos48
Nearest_Target_Pos	= 49	#pos49
Infantry_Pos	= 50	#pos50
Archers_Pos	= 51	#pos51
Cavalry_Pos	= 55	#pos55 - MV: changed from 52, overwritten in script_find_high_ground_around_pos1
Enemy_Team_Pos	= 53	#pos53
Nearest_Enemy_Battlegroup_Pos	= 54	#pos54

#positions used through AI trigger
Player_Battle_Group3_Pos	= 24	#pos24
Player_Battle_Group4_Pos	= 25	#pos25
Player_Battle_Group5_Pos	= 26	#pos26
Player_Battle_Group6_Pos	= 27	#pos27
Player_Battle_Group7_Pos	= 28	#pos28
Player_Battle_Group8_Pos	= 29	#pos29

Team0_Infantry_Pos	= 30	#pos30
Team0_Archers_Pos	= 31	#pos31
Team0_Cavalry_Pos	= 32	#pos32
Team0_Average_Pos	= 33	#pos33
Team1_Infantry_Pos	= 34	#pos34
Team1_Archers_Pos	= 35	#pos35
Team1_Cavalry_Pos	= 36	#pos36
Team1_Average_Pos	= 37	#pos37
Team2_Infantry_Pos	= 38	#pos38
Team2_Archers_Pos	= 39	#pos39
Team2_Cavalry_Pos	= 40	#pos40
Team2_Average_Pos	= 41	#pos41
Team3_Infantry_Pos	= 42	#pos42
Team3_Archers_Pos	= 43	#pos43
Team3_Cavalry_Pos	= 44	#pos44
Team3_Average_Pos	= 45	#pos45

#positions used through battle
Team0_Cavalry_Destination	= 56	#pos56
Team1_Cavalry_Destination	= 57	#pos57
Team2_Cavalry_Destination	= 58	#pos58
Team3_Cavalry_Destination	= 59	#pos59
Team0_Starting_Point	= 12	#pos12
Team1_Starting_Point	= 13	#pos13
Team2_Starting_Point	= 14	#pos14
Team3_Starting_Point	= 16	#pos16
### End of formAI_constants

### orc bonus for party headcount (each tf_orc in main party adds nom/denom to max party size)
orc_bonus_nominator   = 2
orc_bonus_denominator = 3

# party player icons (mtarini)
# for each faction: icon-mounted, icon-on-foot (melee), icon-on-foot (ranged)
faction_player_icons = [
    (fac_gondor  ,icon_knight_gondor			,icon_footman_gondor,icon_ithilien_ranger),
    (fac_rohan   ,icon_knight_rohan				,icon_player		,icon_player),
    (fac_isengard,icon_wargrider_run			,icon_uruk_isengard	,icon_uruk_isengard), # assuming uruk orc (not uruk or evil man). Evil men will be deatl separately
    (fac_mordor  ,icon_wargrider_run         	,icon_uruk			,icon_uruk),         # same thing
    (fac_harad   ,icon_harad_horseman			,icon_player		,icon_player),       
    (fac_rhun    ,icon_easterling_horseman		,icon_player		,icon_player),
    (fac_khand   ,icon_easterling_horseman		,icon_player		,icon_player),
    (fac_umbar   ,icon_umbar_captain			,icon_umbar_corsair	,icon_umbar_corsair),
    (fac_lorien  ,icon_knight_rivendell			,icon_lorien_elf_b	,icon_lorien_elf_a),
    (fac_imladris,icon_lamedon_horseman			,icon_mirkwood_elf	,icon_mirkwood_elf),
    (fac_woodelf ,icon_player_horseman			,icon_mirkwood_elf	,icon_mirkwood_elf),
    (fac_moria   ,icon_wargrider_run		    ,icon_orc			,icon_orc),
    (fac_guldur  ,icon_wargrider_run		    ,icon_orc			,icon_orc),
    (fac_gundabad,icon_wargrider_run		    ,icon_orc			,icon_orc),
    (fac_dale    ,icon_player_horseman			,icon_player		,icon_player),
    (fac_dwarf   ,icon_player_horseman			,icon_dwarf			,icon_dwarf),
    (fac_dunland ,icon_dunland_captain			,icon_dunlander		,icon_dunlander),
    (fac_beorn   ,icon_player_horseman			,icon_axeman		,icon_axeman),
]
subfac_regular = 0  # the capital (Gondor or Rohan)


subfaction_gondor_player_icons = [
    (subfac_regular  ,		icon_knight_gondor	,icon_footman_gondor	,icon_ithilien_ranger),
    (subfac_pelargir  ,		icon_knight_gondor	,icon_footman_gondor	,icon_ithilien_ranger),
    (subfac_dol_amroth,		icon_knight_dolamroth,icon_footman_gondor	,icon_ithilien_ranger),
    (subfac_ethring ,		icon_lamedon_horseman,icon_footman_lamedon	,icon_ithilien_ranger),
    (subfac_lossarnach ,	icon_knight_gondor	,icon_lossarnach_axeman_icon,icon_ithilien_ranger),
    (subfac_pinnath_gelin ,	icon_knight_gondor	,icon_footman_pinnath	,icon_ithilien_ranger),
    (subfac_blackroot  ,	icon_knight_gondor	,icon_footman_gondor	,icon_ithilien_ranger),
    (subfac_rangers  ,		icon_knight_gondor	,icon_footman_gondor	,icon_ithilien_ranger),
]

# Daytime/Nighttime penalties system (foxyman), increased and also affecting melee wp (InVain)
Penalties_sys = [
    (tf_male,    [        ], [(wpt_archery, 40),(wpt_throwing, 30),(wpt_one_handed_weapon, 30),(wpt_two_handed_weapon, 30),(wpt_polearm, 30)]),
    (tf_female,  [        ], [(wpt_archery, 40),(wpt_throwing, 30),(wpt_one_handed_weapon, 30),(wpt_two_handed_weapon, 30),(wpt_polearm, 30)]),
    (tf_gondor,  [        ], [(wpt_archery, 40),(wpt_throwing, 30),(wpt_one_handed_weapon, 30),(wpt_two_handed_weapon, 30),(wpt_polearm, 30)]),
    (tf_rohan,   [        ], [(wpt_archery, 40),(wpt_throwing, 30),(wpt_one_handed_weapon, 30),(wpt_two_handed_weapon, 30),(wpt_polearm, 30)]),
    (tf_dunland, [        ], [(wpt_archery, 40),(wpt_throwing, 30),(wpt_one_handed_weapon, 30),(wpt_two_handed_weapon, 30),(wpt_polearm, 30)]),
    (tf_orc,     [("skl_athletics", -3),("skl_spotting", -1),("skl_pathfinding", -1)], [(wpt_one_handed_weapon, -20),(wpt_two_handed_weapon, -20),(wpt_polearm, -20),(wpt_archery, -50),(wpt_throwing, -20)]),
    (tf_uruk,    [("skl_athletics", -3),("skl_spotting", -1),("skl_pathfinding", -1)], [(wpt_one_handed_weapon, -20),(wpt_two_handed_weapon, -20),(wpt_polearm, -20),(wpt_archery, -50),(wpt_throwing, -20)]),
    (tf_urukhai, [        ], [        ]),
    (tf_harad,   [        ], [(wpt_archery, 40),(wpt_throwing, 30),(wpt_one_handed_weapon, 30),(wpt_two_handed_weapon, 30),(wpt_polearm, 30)]),
    (tf_dwarf,   [        ], [(wpt_archery, 40),(wpt_throwing, 30),(wpt_one_handed_weapon, 30),(wpt_two_handed_weapon, 30),(wpt_polearm, 30)]),
    (tf_troll,   [          ], [(wpt_one_handed_weapon, -20),(wpt_two_handed_weapon, -20),(wpt_polearm, -20)]),
    (tf_dunedain,[        ], [(wpt_archery, 40),(wpt_throwing, 30),(wpt_one_handed_weapon, 30),(wpt_two_handed_weapon, 30),(wpt_polearm, 30)]),
    (tf_lorien,  [        ], [(wpt_archery, 25),(wpt_throwing, 25),(wpt_one_handed_weapon, 20),(wpt_two_handed_weapon, 20),(wpt_polearm, 20)]),
    (tf_imladris,[        ], [(wpt_archery, 25),(wpt_throwing, 25),(wpt_one_handed_weapon, 20),(wpt_two_handed_weapon, 20),(wpt_polearm, 20)]),
    (tf_woodelf, [        ], [(wpt_archery, 25),(wpt_throwing, 25),(wpt_one_handed_weapon, 20),(wpt_two_handed_weapon, 20),(wpt_polearm, 20)]),
    (tf_evil_man,[        ], [(wpt_archery, 40),(wpt_throwing, 30),(wpt_one_handed_weapon, 20),(wpt_two_handed_weapon, 20),(wpt_polearm, 20)]),
]	

skill2item_list = [0,"skl_riding","skl_leadership","skl_power_strike","skl_persuasion","skl_horse_archery","skl_first_aid","skl_shield","skl_power_draw","skl_surgery","skl_power_throw","skl_trade","skl_tactics","skl_ironflesh","skl_athletics","skl_looting"]

#conversation cutscenes codes; also mission codes for the travelling Gandalf/Nazgul ($g_tld_gandalf_state, $g_tld_nazgul_state)
# special values 0=travelling for flavor; -1=inactive
tld_cc_gandalf_advice     = 1
tld_cc_gandalf_ally_down  = 2
tld_cc_gandalf_enemy_down = 3
tld_cc_gandalf_victory    = 4
tld_cc_nazgul_baggins     = 5
tld_cc_nazgul_evil_war    = 6
tld_cc_nazgul_victory     = 7

#conversation bit masks for $g_tld_conversations_done
tld_conv_bit_gandalf_advice     = 0x01
tld_conv_bit_gandalf_ally_down  = 0x02
tld_conv_bit_gandalf_enemy_down = 0x04
tld_conv_bit_gandalf_victory    = 0x08
tld_conv_bit_nazgul_baggins     = 0x10
tld_conv_bit_nazgul_evil_war    = 0x20
tld_conv_bit_nazgul_victory     = 0x40

# Constants added by CppCoder below

# TLD morale codes -x% chance they will flee

tld_morale_very_good		= 40
tld_morale_good			= 20
tld_morale_average		= 10
tld_morale_poor			= 5

tld_morale_formation_bonus	= 25 # Gondor and Dunland

tld_morale_leader_important	= 35 # Black numenoreans / evil men
tld_morale_leader_bonus		= 25 # Gondor and Dunland
tld_morale_leader_average	= 15 # Default morale bonus
tld_morale_leader_avenge	= 35 # Dwarfs,   when leader falls
tld_morale_leader_urukhai	= 25 # Uruk hai, when leader falls

# These are extra bonuses to simply boost the courage
tld_morale_bonus_easterlings	= 20
tld_morale_bonus_elves		= 35

tld_morale_rout			= 60

tld_morale_rout_allies		= -tld_morale_rout
tld_morale_rout_enemies		= tld_morale_rout

tld_rout_party_spawn_ratio_numerator	= 75
tld_rout_party_spawn_ratio_denominator	= 100

# Party count option in tweaks menu

tld_party_count_option_increment	= 10
tld_party_count_option_max		= 2500
tld_party_count_option_min		= 600
tld_party_count_option_high_crash	= 1501
tld_party_count_option_med_crash	= 950

# Hero parties smaller than this will not siege...

tld_siege_min_party_size		= 100

# Constants for defiled item meshes...

defiled_items_begin 			= "itm_defiled_armor_gondor"
defiled_items_end			= "itm_save_compartibility_item10"

# Max values for resources and influence

tld_rp_cap				= 200000
tld_if_cap				= 5000
tld_influence_trait_bonus		= 2

# These are used for the gift giving system.
gift_strings_begin			= "str_gondor_gift0"
tld_gifts_per_faction			= 5

# These are for the Warband command cursor to work with formations
tld_cursor_undefined			= -1
tld_cursor_arrow_mode			= -2
tld_cursor_time				= 10


##### Kham Constant Additions ######

## More Town Walkers Additions
isengard_mordor_centers_begin = p_town_morannon
isengard_mordor_centers_end = p_town_urukhai_r_camp + 1

moria_centers_begin = p_town_moria
moria_centers_end = p_town_troll_cave + 1

gundabad_centers_begin = p_town_gundabad
gundabad_centers_end = p_town_gundabad_m_outpost + 1
## More Town Walkers Additions End ##

##Troop Presentation Constants ##
kingdoms_begin = "fac_gondor"
kingdoms_end = "fac_kingdoms_end"

npc_kingdoms_begin = kingdoms_begin
npc_kingdoms_end = kingdoms_end

## Troop Presentation constants End ##

## Kham Oath of Vengeance Constant
tld_oath_kills = 120

## Kham Player Initiated Sieges Constants
tld_player_siege_resp_cost = 100000

## Kham PBOD Additions
## Prebattle Orders & Deployment Begin
#PBOD General
##Settings
skirmish_min_distance = 1500 #Min distance you wish maintained, in cm. Where agent will retreat
skirmish_max_distance = 2500 #Max distance to maintain, in cm. Where agent will stop retreating
#pbod_debug            = 0    #On/Off for debug messages

slot_party_skirmish_d0 = slot_town_arena_melee_mission_tpl
slot_party_skirmish_d1 = slot_town_arena_torny_mission_tpl
slot_party_skirmish_d2 = slot_town_arena_melee_1_num_teams
slot_party_skirmish_d3 = slot_town_arena_melee_1_team_size
slot_party_skirmish_d4 = slot_town_arena_melee_2_num_teams
slot_party_skirmish_d5 = slot_town_arena_melee_2_team_size
slot_party_skirmish_d6 = slot_town_arena_melee_3_num_teams
slot_party_skirmish_d7 = slot_town_arena_melee_3_team_size
slot_party_skirmish_d8 = slot_town_arena_melee_cur_tier
slot_agent_is_skirmisher = 32

#PBOD Preference Slots (used for p_main_party; available 72 - 108)
slot_party_pref_div_dehorse  = 400        
slot_party_pref_div_no_ammo  = 401     
slot_party_pref_wu_lance     = 402 
slot_party_pref_wu_harcher   = 403 
slot_party_pref_wu_spear     = 404 
slot_party_pref_dmg_tweaks   = 405 


#Agent Slots
slot_agent_lance         = 33
slot_agent_horsebow      = 34
slot_agent_spear         = 35
slot_agent_horse         = 36
slot_agent_volley_fire   = 37
slot_agent_alt_div_check = 40
slot_agent_new_division  = 41

#Order Constants
no_order  = -1
clear     = 0
onehand   = 1
twohands  = 2
polearm   = 3
ranged    = 4
free      = 5 #shield
shield    = 6
noshield  = 7
begin     = 1
end       = 0

##Kham PBOD Additions END

#Legendary Places Slots (party slot)
slot_legendary_visited = 300
slot_legendary_explored = 301

#Aiming slots (agent slot)
agent_aim_overridden = 302

#Track Mount and Rider Slots (agent slot)
slot_agent_horse_agent = 303
slot_agent_rider_agent = 304

#Rank Trigger Slots (faction slot)
slot_faction_war_council = 305
slot_faction_siege_reports = 306

#New Party Creation/Removal system (party slot)
slot_party_dormant = 306

#AI Slots (agent slot)
agent_is_free_of_pathing = 307

#Healer Slots (troop slot)
slot_troop_needs_healing = 308

#Adv Camp Reserve Party (troop slot)
slot_troop_player_reserve_adv_camp = 309

#Morale Penalties / bonuses
low_party_morale = 30
high_party_morale = 70

#Exploration Points Party Slots
slot_exploration_point_1 = 302
slot_exploration_point_2 = 303
slot_exploration_point_3 = 304
slot_exploration_point_4 = 305


# VC Presentantion Constants
font_title = 2400
font_small = 800
font_normal = 1200

# shows mouse coordinates on presentations (set 0 for production)
debug_show_presentation_coordinates = 0

#VC Troop Tree Presentation
Troop_Tree_Num_Levels = 6
Troop_Tree_Max_Per_Level = 5  #2^(Troop_Tree_Num_Levels-1) opt for counting most upgrade2 over all factions
Troop_Tree_Area_Height = Screen_Title_Height-4*Screen_Text_Height
Troop_Tree_Area_Width = Screen_Width-2*Screen_Border_Width
Troop_Tree_Line_Color = 0x000000
Troop_Tree_Tableau_Height = 800
Troop_Tree_Tableau_Width = Troop_Tree_Tableau_Height*Screen_Undistort_Width_Num/Screen_Undistort_Width_Den

def sq(distance):
  return distance * distance / 100 # get_sq_distance_between_positions always uses fixed point multiplier 100
 
#Labels
max_distance_to_see_labels = 1500

#Adv Camps Revamp

slot_faction_theater_retreated_from = 181


# Armour Customization Constants
armor_cloth                   = 0
armor_armor                   = 1
armor_plate                   = 2

custom_armor_maximum_submaterial = 7 #armor_plate + 4, thanks platemail
slot_item_materials_begin = 81
slot_item_materials_end = 82
slot_item_num_components = 83
slot_item_init_script = 84
#mandatory + optional | color
slot_item_player_slots_begin = 85
slot_item_player_slots_end = slot_item_player_slots_begin + custom_armor_maximum_submaterial
slot_item_player_color = slot_item_player_slots_end

custom_item_color_mask = 0xf
custom_item_color_bits = 4

message_positive = 0x33FF33
message_negative = 0xFF3333
message_neutral = 0xFFFF33

#Order Weapon Switch
slot_team_shield_order = 1000

key_for_onehand   = key_p
key_for_twohands =  key_open_braces
key_for_polearms =  key_close_braces
key_for_ranged    = key_back_slash
key_for_shield_up   = key_apostrophe
key_for_noshield =  key_slash

#Modified Vyrn HP Shield - kham
slot_troop_hp_shield = 154
slot_agent_hp_shield_active = 43
slot_agent_hp_shield = 44

## Health Restore on Kill begin
#  Rates listed below are per kill, not based on duration.  They are also % of health, not exact values.
wp_hr_player_rate                  = 5
wp_hr_strength_factor              = 4   # This is the value STR is divided by.  So 4 = .25% per point of Strength.
wp_hr_leadership_factor            = 2   # This is the value Leadership is divided by.  Only non-heroes gain this. (Unused)
wp_hr_lord_rate                    = 15
wp_hr_berserker_rate               = 10
wp_hr_king_rate                    = 20	 # Currently unused.
wp_hr_common_rate                  = 5	 # Currently unused.
wp_hr_elite_rate                   = 15  # Currently unused.
wp_hr_factor_difficulty            = 0   # This turns ON (1) or OFF (0) any code changes based on difficulty.
wp_hr_diff_enemy_bonus             = 4   # Amount the health regeneration of enemies is boosted by per difficulty rank.
wp_hr_diff_ally_penalty            = -3  # Amount the health regeneration of allies is reduced by per difficulty rank.
wp_hr_debug                        = 0   # This turns ON (1) or OFF (0) all of the debug messages.
## Health Restore on Kill end

slot_nazgul_timer = 46

#Intro strings

intro_strings_begin = str_gondor_faction_intro
intro_strings_end = str_intro_faction_intro_strings_end

#Regular Parties Follow Player
slot_party_number_following_player = 307
slot_faction_allowed_follow = 182

#Batching
slot_agent_tick_check_time = 1000
slot_agent_period_reset_time = 1001


########################
########################
#####FORM V5 Additions #
########################

# Formations AI v5 by Motomataru
# rel. 02/12/2016

AI_Max_Reinforcements	= 8	#maximum number of reinforcement stages in a battle
AI_Replace_Dead_Player	= 1 #Replaced with Global so we can toggle
AI_Poor_Troop_Level	= 12	#average level of troops under which a division may lose discipline

#positions used in a script, named for convenience
Nearest_Enemy_Troop_Pos_MOTO	= 48	#pos48	used only by infantry AI
Nearest_Enemy_Battlegroup_Pos_MOTO	= 50	#pos50	used only by ranged AI
Nearest_Threat_Pos_MOTO	= Nearest_Enemy_Troop_Pos_MOTO	#used only by cavalry AI
Nearest_Target_Pos_MOTO	= Nearest_Enemy_Battlegroup_Pos_MOTO	#used only by cavalry AI
Infantry_Pos_MOTO	= 51	#pos51
Archers_Pos_MOTO	= 53	#pos53
Cavalry_Pos_MOTO	= 54	#pos54
Team_Starting_Point	= 55	#pos55

#positions used through battle
Team0_Cavalry_Destination	= 56	#pos56
Team1_Cavalry_Destination	= 57	#pos57
Team2_Cavalry_Destination	= 58	#pos58
Team3_Cavalry_Destination	= 59	#pos59

# Formations AI v5 by Motomataru
# rel. 02/12/2016

#Team Data
slot_team_faction                       = 1
slot_team_starting_x                    = 2
slot_team_starting_y                    = 3
slot_team_reinforcement_stage           = 4

#Reset with every call of Store_Battlegroup_Data
slot_team_size                          = 5
slot_team_adj_size                      = 6 #cavalry double counted for AI considerations
slot_team_num_infantry                  = 7	#class counts
slot_team_num_archers                   = 8
slot_team_num_cavalry                   = 9
slot_team_level                         = 10
slot_team_avg_zrot                      = 11
slot_team_avg_x                         = 12
slot_team_avg_y                         = 13

#Battlegroup slots (1 for each of 9 divisions). A "battlegroup" is uniquely defined by team and division
slot_team_d0_size                       = 14
slot_team_d0_percent_ranged             = 23
slot_team_d0_percent_throwers           = 32
slot_team_d0_low_ammo                   = 41
slot_team_d0_level                      = 50
slot_team_d0_armor                      = 59
slot_team_d0_weapon_length              = 68
slot_team_d0_swung_weapon_length        = 77
slot_team_d0_front_weapon_length        = 86
slot_team_d0_front_agents               = 95	#for calculating slot_team_d0_front_weapon_length
slot_team_d0_is_fighting                = 104
slot_team_d0_enemy_supporting_melee     = 113
slot_team_d0_closest_enemy              = 122
slot_team_d0_closest_enemy_dist         = 131	#for calculating slot_team_d0_closest_enemy
slot_team_d0_closest_enemy_special      = 140	#tracks non-cavalry for AI infantry division, infantry for AI archer division
slot_team_d0_closest_enemy_special_dist = 149	#for calculating slot_team_d0_closest_enemy_special
slot_team_d0_avg_x                      = 158
slot_team_d0_avg_y                      = 167
slot_team_d0_avg_zrot                   = 176
#End Reset Group

sdt_infantry   = 0
sdt_archer     = 1
sdt_cavalry    = 2
sdt_polearm    = 3
sdt_skirmisher = 4
sdt_harcher    = 5
sdt_support    = 6
sdt_bodyguard  = 7
sdt_unknown    = -1

slot_team_d0_formation                  = 194

#Native formation modes
#Constants actually correspond to number of "Stand Closer" commands required by WB to create formation
#Extended to 5 line for WFaS
formation_1_row    = 0
formation_2_row    = -1
formation_3_row    = -2
formation_4_row    = -3
formation_5_row    = -4

slot_team_d0_formation_space            = 203	#number of extra 50cm spaces currently in use
slot_team_d0_move_order                 = 212	#now used only for player divisions
slot_team_d0_fclock                     = 221	#now used only for player divisions
slot_team_d0_first_member               = 230	#-1 if division not in formation
slot_team_d0_prev_first_member          = 239
slot_team_d0_speed_limit                = 248
slot_team_d0_percent_in_place           = 257
slot_team_d0_destination_x              = 266
slot_team_d0_destination_y              = 275
slot_team_d0_destination_zrot           = 284
slot_team_d0_target_team                = 293	#targeted battlegroup (team ID)
slot_team_d0_target_division            = 302	#targeted battlegroup (division ID)
slot_team_d0_formation_num_ranks        = 311
slot_team_d0_exists                     = 320
#NEXT                                   = 329
#Battlegroup slots end

reset_team_stats_begin = slot_team_size  
reset_team_stats_end   = slot_team_d0_type

minimum_ranged_ammo = 3	#below this not considered ranged type troop

#Formation tweaks
formation_reequip	= 1	#allow troops in formations to switch weapons
formation_reform_interval	= 2 #seconds
formation_rethink_for_formations_only	= 0

#Other constants (not tweaks)
Third_Max_Weapon_Length = 227 / 3
Km_Per_Hour_To_Cm = formation_reform_interval * 100000 / 3600
Reform_Trigger_Modulus = formation_reform_interval * 2	#trigger is half-second
Top_Speed	= 13

#positions used through formations and AI triggers
Current_Pos     = 34	#pos34
Speed_Pos       = 36	#pos36
Target_Pos      = 37	#pos37
Enemy_Team_Pos_MOTO  = 38	#pos38
Temp_Pos        = 39	#pos39

#Hold Over There Command Tracking
HOT_no_order           = 0
HOT_F1_pressed         = 1
HOT_F1_held            = 2

#Team Slots SEE SECTION

scratch_team = 7	#Should be used just for above slots. If you use it, check for conflicts.

WB_Implementation   = 0
WFaS_Implementation = 1
Native_Formations_Implementation = WB_Implementation

#Other slots
#use faction slots to remember information between battles
slot_faction_d0_mem_formation           = 200
slot_faction_d0_mem_formation_space     = 209
slot_faction_d0_mem_relative_x_flag     = 218
slot_faction_d0_mem_relative_y          = 227
#NEXT                                   = 236

#the following applied only to infantry in formation
slot_agent_formation_rank      = 27
slot_agent_inside_formation    = 28
slot_agent_nearest_enemy_agent = 29
slot_agent_new_division        = 30
slot_agent_positioned          = 31

slot_item_alternate            = 46	#table between swing/noswing versions of same weapon

#Battle Phases
BP_Ready  = 0
BP_Init   = 1
BP_Deploy = 2
BP_Setup_MOTO  = 3
BP_Jockey_MOTO = 4
BP_Duel   = 5
BP_Fight_MOTO  = 6

first_time_hold_F1         = 0x200
first_time_formations      = 0x400

Outfit_Thorax_Length = 60  #length dark ages human thorax
Outfit_Fast_Weapon_Speed = 100

mission_tpl_are_all_agents_spawned     = 1943   # (mission_tpl_are_all_agents_spawned), #agents >300 may keep spawning after ti_after_mission_start (still fires .1 second too early)

#### END Moto's FormV5 ##########


fac_str_reinforcement_boost = 1000 #Kham

slot_faction_last_stand = 307
slot_faction_guardian_party_spawned = 308

slot_item_light_armor = 86

slot_troop_player_clone = 155
slot_troop_has_custom_armour = 156

slot_party_battle_encounter_effect = 308

NO_EFFECT_PRESENT = 0
LORIEN_MIST = 1
GIANT_BOULDERS = 2
EAGLES_ABOVE = 3
SAURON_DARKNESS = 4
SARUMAN_STORM = 5
GULDUR_FOG = 6
END_EFFECTS = 7

RANGED_ACCURACY_DEBUFF = 85
RANGED_ACCURACY_BUFF = 115
RANGED_DAMAGE_DEBUFF = 90
RANGED_DAMAGE_BUFF = 110
RANGED_RELOAD_SPEED_DEBUFF = 85
RANGED_RELOAD_SPEED_BUFF = 115
WEAPON_DAMAGE_DEBUFF = 90
WEAPON_DAMAGE_BUFF = 110
SPEED_DEBUFF = 90
SPEED_BUFF = 110
MAX_HEALTH_BUFF = 110
MAX_HEALTH_DEBUFF = 90
ENCOUNTER_EFFECT_MORALE_BUFF = 10
ENCOUNTER_EFFECT_MORALE_DEBUFF = 10

slot_party_scripted_ai = 309


slot_troll_agent_charging = 50
slot_troll_agent_last_charge = 51

OLOG_ENT_HP_SHIELD = 320
MORIA_TROLL_HP_SHIELD = 500

slot_troop_has_combat_ai = 157

# Guildmaster Companion Strings Start
slot_troop_gm_companion_ask = 158
slot_troop_gm_companion_none = 159
slot_troop_gm_companion_player_none = 160
slot_troop_gm_companion_player_found = 161
slot_troop_gm_companion_1 = 162
slot_troop_gm_companion_2 = 163

slot_party_has_companion = 310

# Control allies
player_control_allies_inf = 3

# Troll Hiring Constants
slot_troop_troll_armoured_variant = 164 #Gets the armoured variant of a troll troop.

#Retainers Begin

slot_troop_retainer_troop = 165 #What type of troop (if any) a lord uses as their personal retainers
slot_troop_friendship_reward = 166 #Lord wants to give the player a gift (may store *type* of gift in the future)
slot_troop_friendship_roll = 167 #Stores a friendship roll ahead of time so it can't be cheesed by saving before quest turn in
slot_troop_friendship_reward_hours = 168 #Last time a lord gave a friendship reward, used to limit reward frequency

friendship_reward_none = 0
friendship_reward_troops = 1
friendship_reward_gear = 2
friendship_reward_end = 3

#Retainers End
