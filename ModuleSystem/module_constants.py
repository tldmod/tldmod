from ID_items import *
from ID_quests import *
from ID_factions import *
#from ID_strings import *
from header_item_modifiers import *
from header_common import *
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

slot_item_is_checked              = 0
slot_item_food_bonus              = 1
slot_item_book_reading_progress   = 2
slot_item_book_read               = 3
slot_item_intelligence_requirement= 4
slot_item_faction                 = 5 # additional item slot for culture-specific shop inventories
slot_item_text                    = 6 # for future use, links to text string
slot_item_subfaction              = 7 # parties and troops and items can have one subfaction -- gondor fiefdoms(mtarini)


########################################################
##  AGENT SLOTS            #############################
########################################################

slot_agent_target_entry_point     = 0
slot_agent_target_x_pos           = 1
slot_agent_target_y_pos           = 2
slot_agent_is_alive_before_retreat= 3
slot_agent_is_in_scripted_mode    = 4
slot_agent_is_not_reinforcement   = 5
slot_agent_tournament_point       = 6
slot_agent_arena_team_set         = 7
slot_agent_map_overlay_id         = 10
slot_agent_target_entry_point     = 11
slot_agent_walker_type            = 12    
# TLD
slot_agent_troll_swing_status     = 13
slot_agent_troll_swing_move       = 14
slot_agent_last_hp		          = 15

########################################################
##  FACTION SLOTS          #############################
########################################################
slot_faction_ai_state                 = 4
slot_faction_ai_object                = 5
slot_faction_ai_last_offensive_time   = 6
slot_faction_marshall                 = 7
slot_faction_ai_offensive_max_followers = 8

slot_faction_culture              = 9
slot_faction_leader               = 10
##slot_faction_vassal_of            = 11

slot_faction_number_of_parties    = 20
slot_faction_state                = 21

slot_faction_player_alarm         = 30
slot_faction_last_mercenary_offer_time = 31

slot_faction_tier_1_troop         = 41
slot_faction_tier_2_troop         = 42
slot_faction_tier_3_troop         = 43
slot_faction_tier_4_troop         = 44
slot_faction_tier_5_troop         = 45
slot_faction_deserter_troop       = 48
slot_faction_guard_troop          = 49
slot_faction_messenger_troop      = 50
slot_faction_prison_guard_troop   = 51
slot_faction_castle_guard_troop   = 52

slot_faction_has_rebellion_chance = 60

# TLD Player Reward system
# Player's stat per faction
slot_faction_influence = 70
slot_faction_rank = 71
slot_faction_respoint = 72

#Rebellion changes
#slot_faction_rebellion_target                     = 65
#slot_faction_inactive_leader_location         = 66
#slot_faction_support_base                     = 67
#Rebellion changes



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
slot_faction_strength               = 150 # strength 0-7000
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
slot_faction_home_theater  = 159  # theater_SW  theater_SE theater_C,  theater_N
# TLD War System end (matrini)

_= "itm_warg_1b"
item_warg_end = "itm_troll_feet_boots"

##################################


########################################################
##  PARTY SLOTS            #############################
########################################################
slot_party_type                = 0  #spt_caravan, spt_town, spt_castle
slot_party_victory_value       = 1  #TLD, subtract from faction strength when defeated
slot_party_retreat_flag        = 2
slot_party_ignore_player_until = 3
slot_party_ai_state            = 4
slot_party_ai_object           = 5

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
slot_center_culture     = 19

slot_town_barman  = 20
slot_town_weaponsmith   = 21
slot_town_armorer       = 22
slot_town_merchant      = 23
slot_town_horse_merchant= 24
slot_town_elder         = 25
slot_center_player_relation = 26

slot_center_siege_with_belfry = 27
slot_center_last_taken_by_troop = 28

# party will follow this party if set:
slot_party_commander_party = 30 #default -1
slot_party_following_player    = 31
slot_party_follow_player_until_time = 32
slot_party_dont_follow_player_until_time = 33

slot_village_raided_by        = 34
slot_village_state            = 35 #svs_normal, svs_being_raided, svs_looted, svs_recovering, svs_deserted
slot_village_raid_progress    = 36
slot_village_recover_progress = 37
slot_village_smoke_added      = 38
slot_village_infested_by_bandits   = 39

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

slot_town_reinf_pt                = 60
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

### TLD center specific guards
slot_town_guard_troop          = 250
slot_town_prison_guard_troop   = 251
slot_town_castle_guard_troop   = 252
###

slot_town_reinforcements_a        = 253
slot_town_reinforcements_b        = 254
slot_town_reinforcements_c        = 255

#slot_party_type values
##spt_caravan            = 1
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
spt_village_farmer     = 15
spt_ship               = 16
spt_cattle_herd        = 17
spt_bandit              = 18 #WTH, native doesn't have a spt for bandits?! (TLD foxyman)
#spt_deserter           = 20

kingdom_party_types_begin = spt_patrol
kingdom_party_types_end = spt_kingdom_hero_alone + 1

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
spai_raiding_around_center      = 5
##spai_raiding_village            = 6
spai_holding_center             = 7
##spai_helping_town_against_siege = 9
spai_engaging_army              = 10
spai_accompanying_army          = 11
spai_trading_with_town          = 13
spai_retreating_to_center       = 14
##spai_trading_within_kingdom     = 15
spai_recruiting_troops          = 16

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
##  TROOP SLOTS            #############################
########################################################
#slot_troop_role         = 0  # 10=Kingdom Lord
#slot_troop_player_start_char   = 1  #TLD starting char


slot_troop_occupation          = 2  # 0 = free, 1 = merchant
#slot_troop_duty               = 3  # Kingdom duty, 0 = free
slot_troop_state               = 3  
slot_troop_last_talk_time      = 4
slot_troop_met                 = 5
slot_troop_party_template      = 6
#slot_troop_kingdom_rank        = 7

slot_troop_renown              = 7

##slot_troop_is_prisoner         = 8  # important for heroes only
slot_troop_prisoner_of_party   = 8  # important for heroes only
#slot_troop_is_player_companion = 9  # important for heroes only:::USE  slot_troop_occupation = slto_player_companion



slot_troop_leaded_party        = 10 # important for kingdom heroes only
slot_troop_wealth              = 11 # important for kingdom heroes only
slot_troop_cur_center          = 12 # important for royal family members only (non-kingdom heroes)

slot_troop_banner_scene_prop   = 13 # important for kingdom heroes and player only

slot_troop_original_faction    = 14 # for pretenders
slot_troop_loyalty              = 15
slot_troop_player_order_state   = 16
slot_troop_player_order_object  = 17

#slot_troop_present_at_event    = 19 #defined below

slot_troop_does_not_give_quest = 20
slot_troop_player_debt         = 21
slot_troop_player_relation     = 22
#slot_troop_player_favor        = 23
slot_troop_last_quest          = 24
slot_troop_last_quest_betrayed = 25
slot_troop_last_persuasion_time= 26
slot_troop_last_comment_time   = 27
slot_troop_spawned_before      = 28

#Post 0907 changes begin
slot_troop_last_comment_slot   = 29
slot_troop_present_at_event    = 19
#Post 0907 changes end

slot_troop_spouse              = 30
slot_troop_father              = 31
slot_troop_mother              = 32
slot_troop_daughter            = 33
slot_troop_son                 = 34
slot_troop_sibling             = 35
slot_troop_lover               = 36

slot_troop_trainer_met                       = 30
slot_troop_trainer_waiting_for_result        = 31
slot_troop_trainer_training_fight_won        = 32
slot_troop_trainer_num_opponents_to_beat     = 33
slot_troop_trainer_training_system_explained = 34
slot_troop_trainer_opponent_troop            = 35
slot_troop_trainer_training_difficulty       = 36
slot_troop_trainer_training_fight_won        = 37


slot_troop_family_begin        = 30
slot_troop_family_end          = 36

slot_troop_enemy_1             = 40
slot_troop_enemy_2             = 41
slot_troop_enemy_3             = 42
slot_troop_enemy_4             = 43
slot_troop_enemy_5             = 44

slot_troop_enemies_begin       = 40
slot_troop_enemies_end         = 45

slot_troop_honorable          = 50
#slot_troop_merciful          = 51
slot_lord_reputation_type     = 52

slot_troop_change_to_faction          = 55
slot_troop_readiness_to_join_army     = 57
slot_troop_readiness_to_follow_orders = 58

# NPC-related constants

#NPC companion changes begin
slot_troop_first_encountered          = 59
slot_troop_home                       = 60

slot_troop_morality_state       = 61
tms_no_problem         = 0
tms_acknowledged       = 1
tms_dismissed          = 2

slot_troop_morality_type = 62
tmt_aristocratic = 1
tmt_egalitarian = 2
tmt_humanitarian = 3
tmt_honest = 4
tmt_pious = 5

slot_troop_morality_value = 63

slot_troop_2ary_morality_type  = 64
slot_troop_2ary_morality_state = 65
slot_troop_2ary_morality_value = 66

slot_troop_morality_penalties =  69 ### accumulated grievances from morality conflicts


slot_troop_personalityclash_object     = 71
#(0 - they have no problem, 1 - they have a problem)
slot_troop_personalityclash_state    = 72 #1 = pclash_penalty_to_self, 2 = pclash_penalty_to_other, 3 = pclash_penalty_to_other,
pclash_penalty_to_self  = 1
pclash_penalty_to_other = 2
pclash_penalty_to_both  = 3
#(a string)
slot_troop_personalityclash2_object   = 73
slot_troop_personalityclash2_state    = 74

slot_troop_personalitymatch_object   =  75
slot_troop_personalitymatch_state   =  76

slot_troop_personalityclash_penalties = 77 ### accumulated grievances from personality clash

slot_troop_home_speech_delivered = 78

#NPC history slots

slot_troop_met_previously        = 80
slot_troop_turned_down_twice     = 81
slot_troop_playerparty_history   = 82

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

slot_troop_mentions_payment = 114 #Not actually used
slot_troop_payment_response = 115 #Not actually used
slot_troop_morality_speech   = 116
slot_troop_2ary_morality_speech = 117
slot_troop_personalityclash_speech = 118
slot_troop_personalityclash_speech_b = 119
slot_troop_personalityclash2_speech = 120
slot_troop_personalityclash2_speech_b = 121
slot_troop_personalitymatch_speech = 122
slot_troop_personalitymatch_speech_b = 123
slot_troop_retirement_speech = 124
slot_troop_rehire_speech = 125
slot_troop_home_intro           = 126
slot_troop_home_description    = 127
slot_troop_home_description_2 = 128
slot_troop_home_recap         = 129
slot_troop_honorific   = 130
slot_troop_strings_end = 131
slot_troop_payment_request = 132

#Rebellion changes begin
slot_troop_discussed_rebellion = 140
slot_troop_support_base = 141

## TLD Penalties system slot(foxyman)
slot_troop_prof_night_penalties_begin = 142
slot_troop_prof_night_penalties_end   = slot_troop_prof_night_penalties_begin+6

#TLD number of items in a shop: body,head,foot,hand,gold,1h,2h,pole,shield,bow,thrown,arrows,horses,food,goods
# same order as itp_type flags!! 
slot_troop_shop_horses = 150
slot_troop_shop_1h     = 151
slot_troop_shop_2h     = 152
slot_troop_shop_pole   = 153
slot_troop_shop_arrows = 154
slot_troop_shop_bolts       = 155
slot_troop_shop_shield = 156
slot_troop_shop_bow    = 157
slot_troop_shop_crossbow    = 158
slot_troop_shop_thrown = 159
slot_troop_shop_goods  = 160
slot_troop_shop_head   = 161
slot_troop_shop_body   = 162
slot_troop_shop_foot   = 163
slot_troop_shop_hand   = 164
slot_troop_shop_gold   = 165
slot_troop_shop_food   = 166


# TLD faction ranks
slot_troop_faction_rank = 167
stfr_position_mask      =        0x7
stfr_position_unit      =        0x1
stfr_rank_mask          =       0xF8
stfr_rank_unit          =       0x08
stfr_equipments_permit  =     0xF800
stfr_equipment_unit     =     0x0800
stfr_soldiers_permit    =    0x10000
stfr_supplies_permit   =     0x20000
stfr_garrison_permit    =    0x40000
stfr_grand_general      =    0x80000
stfr_in_command         =   0x100000
stfr_reinforcement      =   0x200000
stfr_name_string        = 0xff000000
stfr_name_string_unit   = 0x01000000

slot_troop_faction_status = 168

# TLD Player Reward system
slot_troop_upkeep_not_paid = 169   # if 1: player didn't pay upkeep for troops of this type in his party: (mtarini)
slot_troop_subfaction      = 170 # parties and troops and items can have one subfaction -- gondor fiefdoms(mtarini)

#######################

#Rebellion changes end
# character backgrounds
cb_noble = 1
cb_merchant = 2
cb_guard = 3
cb_forester = 4
cb_nomad = 5
cb_thief = 6
cb_priest = 7

cb2_page = 0
cb2_apprentice = 1
cb2_urchin  = 2
cb2_steppe_child = 3
cb2_merchants_helper = 4

cb3_poacher = 3
cb3_craftsman = 4
cb3_peddler = 5
cb3_troubadour = 7
cb3_squire = 8
cb3_lady_in_waiting = 9
cb3_student = 10

cb4_revenge = 1
cb4_loss    = 2
cb4_wanderlust =  3
cb4_disown  = 5
cb4_greed  = 6

#NPC system changes end
#Encounter types
enctype_fighting_against_village_raid = 1
enctype_catched_during_village_raid   = 2


### Troop occupations slot_troop_occupation
##slto_merchant           = 1
slto_kingdom_hero       = 2
slto_player_companion   = 3
slto_kingdom_lady       = 4
slto_kingdom_seneschal  = 5
slto_robber_knight      = 6

stl_unassigned          = -1
stl_reserved_for_player = -2
stl_rejected_by_player  = -3

#NPC changes begin
slto_retirement      = 11
#slto_retirement_medium    = 12
#slto_retirement_short     = 13
#NPC changes end

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
tc_court_talk   	      = 1
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

hero_escape_after_defeat_chance = 80


raid_distance = 4

surnames_begin = "str_surname_1"
surnames_end = "str_surnames_end"
names_begin = "str_name_1"
names_end = surnames_begin
countersigns_begin = "str_countersign_1"
countersigns_end = names_begin
secret_signs_begin = "str_secret_sign_1"
secret_signs_end = countersigns_begin

kingdoms_begin = "fac_gondor"
kingdoms_begin_i = fac_gondor
kingdoms_end = "fac_kingdoms_end"
kingdoms_end_i = fac_kingdoms_end

kingdom_ladies_begin = "trp_knight_1_1_wife"
kingdom_ladies_end = "trp_heroes_end"

kings_begin = "trp_gondor_lord"
kings_end = "trp_knight_1_1"

kingdom_heroes_begin = "trp_gondor_lord"
kingdom_heroes_end = kingdom_ladies_begin

heroes_begin = kingdom_heroes_begin
heroes_end = kingdom_ladies_end


companions_begin = "trp_npc1"
companions_end = "trp_kingdom_heroes_including_player_begin"

soldiers_begin = "trp_farmer"
soldiers_end = "trp_town_walker_1"

#Rebellion changes

##rebel_factions_begin = "fac_kingdom_1_rebels"
##rebel_factions_end =   "fac_kingdoms_end"

pretenders_begin = "trp_kingdom_1_pretender"
pretenders_end = kingdom_heroes_end
#Rebellion changes

tavern_minstrels_begin = "trp_tavern_minstrel_1"
tavern_minstrels_end   = companions_begin


tavern_travelers_begin = "trp_tavern_traveler_1"
tavern_travelers_end   = tavern_minstrels_begin

ransom_brokers_begin = "trp_ransom_broker_1"
ransom_brokers_end   = tavern_travelers_begin

mercenary_troops_begin = "trp_watchman"
mercenary_troops_end = "trp_mercenaries_end"

lord_quests_begin = "qst_deliver_message"
lord_quests_end   = "qst_follow_army"

enemy_lord_quests_begin = "qst_lend_surgeon"
enemy_lord_quests_end   = lord_quests_end

village_elder_quests_begin = "qst_deliver_grain"
village_elder_quests_end = "qst_eliminate_bandits_infesting_village"

mayor_quests_begin  = "qst_move_cattle_herd"
mayor_quests_end    = village_elder_quests_begin

lady_quests_begin = "qst_rescue_lord_by_replace"
lady_quests_end   = mayor_quests_begin

army_quests_begin = "qst_deliver_cattle_to_army"
army_quests_end   = lady_quests_begin


all_quests_begin = 0
all_quests_end = "qst_quests_end"

towns_begin = "p_town_minas_tirith"
castles_begin = "p_castle_1"
villages_begin = "p_castle_1" # changed from p_village_1

towns_end = castles_begin
castles_end = villages_begin
villages_end   = "p_salt_mine"

walled_centers_begin = towns_begin
walled_centers_end   = towns_end    #edited from castles_end

centers_begin = towns_begin
centers_end   = towns_end           #edited from villages_end

scenes_begin = "scn_minas_tirith_center"
scenes_end = "scn_castle_1_exterior"

spawn_points_begin = "p_zendar"
spawn_points_end = "p_spawn_points_end"

regular_troops_begin       = "trp_novice_fighter"
regular_troops_end         = "trp_tournament_master"

swadian_merc_parties_begin = "p_town_1_mercs"
swadian_merc_parties_end   = "p_town_8_mercs"

vaegir_merc_parties_begin  = "p_town_8_mercs"
vaegir_merc_parties_end    = "p_zendar"

##########################################################
# Test : Tavern Recruitment Begin ########################
##########################################################
slot_town_mercs = 66
merc_parties_begin = "p_town_merc_1"
merc_parties_end = "p_zendar"
#########################################################
# Test : Tavern Recruitment End #########################
#########################################################
arena_masters_begin    = "trp_brigand_arena_master"
arena_masters_end      = "trp_troops_end"

training_gound_trainers_begin    = "trp_trainer_1"
training_gound_trainers_end      = "trp_ransom_broker_1"

# town_walkers_begin = "trp_town_walker_1"
# town_walkers_end = "trp_village_walker_1"

# village_walkers_begin = "trp_village_walker_1"
# village_walkers_end   = "trp_spy_walker_1"

spy_walkers_begin = "trp_spy_walker_1"
spy_walkers_end = "trp_tournament_master"

# walkers_begin = town_walkers_begin
# walkers_end   = spy_walkers_end

armor_merchants_begin  = "trp_smith_mtirith"
armor_merchants_end    = "trp_barman_mtirith"

weapon_merchants_begin = "trp_smith_mtirith"
weapon_merchants_end   = "trp_barman_mtirith"

tavernkeepers_begin    = "trp_barman_mtirith"
tavernkeepers_end      = "trp_town_1_horse_merchant"

goods_merchants_begin  = "trp_town_1_horse_merchant"
goods_merchants_end    = "trp_village_1_elder"

horse_merchants_begin  = "trp_town_1_horse_merchant"
horse_merchants_end    = "trp_village_1_elder"

mayors_begin           = "trp_elder"
mayors_end             = "trp_gear_merchant"

village_elders_begin   = "trp_village_1_elder"
village_elders_end     = "trp_merchants_end"


average_price_factor = 1000
minimum_price_factor = 100
maximum_price_factor = 10000

village_prod_min = -5
village_prod_max = 18

item_warg_begin = "itm_warg_1b"
item_warg_end = "itm_troll_feet_boots"

trade_goods_begin = "itm_smoked_fish"
trade_goods_end = "itm_siege_supply"
food_begin = "itm_human_meat"
normal_food_begin = "itm_smoked_fish"
food_end = "itm_grain"

#reference_books_begin = "itm_book_wound_treatment_reference"
#reference_books_end   = trade_goods_begin
#readable_books_begin = "itm_book_tactics"
#readable_books_end   = reference_books_begin
#books_begin = readable_books_begin
#books_end = reference_books_end
horses_begin = "itm_sumpter_horse"
horses_end = "itm_arrows"
weapons_begin = "itm_wooden_stick"
weapons_end = "itm_wooden_shield"
ranged_weapons_begin = "itm_javelin"
ranged_weapons_end = "itm_corsair_bow"
armors_begin = "itm_leather_gloves"
armors_end = "itm_wooden_stick"
shields_begin = "itm_wooden_shield"
shields_end = "itm_javelin"

# Banner constants

banner_meshes_begin = "mesh_banner_a01"
banner_meshes_end_minus_one = "mesh_banner_f21"

arms_meshes_begin = "mesh_arms_a01"
arms_meshes_end_minus_one = "mesh_arms_f21"

custom_banner_charges_begin = "mesh_custom_banner_charge_01"
custom_banner_charges_end = "mesh_tableau_mesh_custom_banner"

custom_banner_backgrounds_begin = "mesh_custom_banner_bg"
custom_banner_backgrounds_end = custom_banner_charges_begin

custom_banner_flag_types_begin = "mesh_custom_banner_01"
custom_banner_flag_types_end = custom_banner_backgrounds_begin

custom_banner_flag_map_types_begin = "mesh_custom_map_banner_01"
custom_banner_flag_map_types_end = custom_banner_flag_types_begin

custom_banner_flag_scene_props_begin = "spr_custom_banner_01"
custom_banner_flag_scene_props_end = "spr_banner_a"

custom_banner_map_icons_begin = "icon_custom_banner_01"
custom_banner_map_icons_end = "icon_banner_01"

banner_map_icons_begin = "icon_mfp_gondor"
banner_map_icons_end_minus_one = "icon_banner_126"

banner_scene_props_begin = "spr_banner_a"
banner_scene_props_end_minus_one = "spr_banner_f21"

khergit_banners_begin_offset = 63
khergit_banners_end_offset = 84

# Some constants for merchant invenotries
merchant_inventory_space = 30
num_merchandise_goods = 40

num_max_river_pirates = 25
num_max_zendar_peasants = 25
num_max_zendar_manhunters = 10

num_max_dp_bandits = 10
num_max_refugees = 10
num_max_deserters = 10

num_max_militia_bands = 15
num_max_armed_bands = 12

num_max_vaegir_punishing_parties = 20
num_max_rebel_peasants = 25

num_max_frightened_farmers = 50
num_max_undead_messengers  = 20

num_forest_bandit_spawn_points = 1
num_mountain_bandit_spawn_points = 1
num_steppe_bandit_spawn_points = 1
num_black_khergit_spawn_points = 1
num_sea_raider_spawn_points = 2

peak_prisoner_trains = 4
peak_kingdom_caravans = 12
peak_kingdom_messengers = 3


# Note positions
note_troop_location = 3

#battle tactics
btactic_hold = 1
btactic_follow_leader = 2
btactic_charge = 3
btactic_stand_ground = 4

#default right mouse menu orders
cmenu_move = -7

# Town center modes
tcm_default = 0
tcm_disguised = 1

# Arena battle modes
#abm_fight = 0
abm_training = 1
abm_visit = 2
abm_tournament = 3

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

def concatenate_scripts(block_list):
    result = []
    for block in block_list:
        result += block
    return result

tld_troops_begin = "trp_player"
tld_troops_end = "trp_troops_end"
tld_player_level_to_begin_war = 2
####################################################
# TLD War System (foxyman and mtarini) #########################
####################################################

# three factions sides
faction_side_good = 0  
faction_side_eye = 1 
faction_side_hand = 2     

# four theaters
theatre_SE = 1<<0  
theatre_SW = 1<<1  
theatre_C =  1<<2  
theatre_N =  1<<3

# faction ,initial strength, culture,      faction lord,       [5 tiers of troops],                                                                                                                                 [reinforcement templates, prisoner trains],                                                    main banner,    map party banner   [slot_faction: deserter_troop, guard_troop, messenger_troop, prison_guard_troop, castle_guard_troop]                                                   faction capital           side                 initial theater
faction_init = [
    ("fac_gondor"  ,4500,"fac_culture_1" , "trp_gondor_lord"  ,["trp_gondor_commoner",      "trp_gondor_militiamen",      "trp_footmen_of_gondor",       "trp_gondor_swordsmen",   "trp_veteran_knight_of_gondor"], ["pt_gondor_reinf_a",   "pt_gondor_reinf_b",  "pt_gondor_reinf_c",  "pt_gondor_p_train"   ], "spr_banner_a", "icon_mfp_gondor"  ,[-1                    ,"trp_gondor_militiamen"     ,"trp_ranger_of_ithilien"        ,"trp_gondor_swordsmen"       ,"trp_swordsmen_of_the_tower_guard"],"p_town_minas_tirith"    ,faction_side_good  , theatre_SE),
    ("fac_rohan"   ,4500,"fac_culture_2" , "trp_rohan_lord"   ,["trp_guardsman_of_rohan",   "trp_esquire_of_rohan",      "trp_rider_of_rohan",    "trp_veteran_rider_of_rohan",       "trp_eorl_guard_of_rohan"  ], ["pt_rohan_reinf_a",    "pt_rohan_reinf_b",    "pt_rohan_reinf_c",  "pt_rohan_p_train"    ], "spr_banner_b", "icon_mfp_rohan"   ,[-1                    ,"trp_footman_of_rohan"      ,"trp_thengel_guard_of_rohan"    ,"trp_veteran_footman_of_rohan" ,"trp_king_s_man_of_rohan"       ],"p_town_edoras"          ,faction_side_good  , theatre_SW),
    ("fac_isengard",5500,"fac_culture_3" , "trp_isengard_lord",["trp_orc_snaga_of_isengard", "trp_uruk_hai_scout",    "trp_uruk_hai_of_isengard", "trp_fighting_uruk_hai_warrior",     "trp_white_hand_rider"    ], ["pt_isengard_reinf_a","pt_isengard_reinf_b","pt_isengard_reinf_c", "pt_isengard_p_train" ], "spr_banner_s", "icon_mfp_isengard",["trp_orc_of_isengard" ,"trp_uruk_hai_of_isengard"  ,"trp_uruk_hai_scout"            ,"trp_fighting_uruk_hai_champion","trp_fighting_uruk_hai_pikeman"],"p_town_isengard"        ,faction_side_hand  , theatre_SW),
    ("fac_mordor"  ,7900,"fac_culture_4" , "trp_mordor_lord"  ,["trp_orc_snaga_of_mordor","trp_large_orc_of_mordor","trp_orc_tracker_of_mordor","trp_large_orc_archer_of_mordor","trp_great_warg_rider_of_mordor"], ["pt_mordor_reinf_a",  "pt_mordor_reinf_b",   "pt_mordor_reinf_c",  "pt_mordor_p_train"   ], "spr_banner_c", "icon_mfp_mordor"  ,["trp_orc_snaga_of_mordor","trp_large_orc_archer_of_mordor","trp_warg_rider_of_gorgoroth","trp_black_uruk_of_barad_dur","trp_uruk_slayer_of_mordor"   ],"p_town_minas_morgul"    ,faction_side_eye   , theatre_SW),
    ("fac_harad"   ,3500,"fac_culture_5" , "trp_harad_lord"   ,["trp_harad_youth",        "trp_harad_desert_warrior",       "trp_harad_cavalry",      "trp_black_serpent_cavalry", "trp_harad_veteran_archer"    ], ["pt_harad_reinf_a",    "pt_harad_reinf_b",   "pt_harad_reinf_c",   -1                    ], "spr_banner_d", "icon_mfp_harad"   ,["trp_harad_desert_warrior","trp_black_serpent_cavalry", "trp_black_serpent_cavalry" ,"trp_harad_black_serpent_infantry","trp_harad_veteran_infantry" ],"p_town_harad_camp"      ,faction_side_eye   , theatre_SE),
    ("fac_rhun"    ,3500,"fac_culture_6" , "trp_rhun_lord"    ,["trp_rhun_tribesman",      "trp_rhun_veteran_horse_archer", "trp_rhun_light_horseman",  "trp_rhun_vet_infantry",  "trp_dorwinion_noble_of_rhun"  ], ["pt_rhun_reinf_a",     "pt_rhun_reinf_b",      "pt_rhun_reinf_c",  -1                    ], "spr_banner_e", "icon_mfp_rhun"    ,["trp_rhun_tribesman","trp_rhun_veteran_horse_archer", "trp_rhun_light_horseman"     ,"trp_rhun_vet_infantry"        ,"trp_dorwinion_noble_of_rhun"   ],"p_town_rhun_south_camp" ,faction_side_eye   , theatre_SE),
    ("fac_khand"   ,3500,"fac_culture_7" , "trp_khand_lord"   ,["trp_easterling_youth",      "trp_easterling_warrior",     "trp_easterling_axeman",      "trp_easterling_rider",      "trp_easterling_horseman"  ], ["pt_khand_reinf_a",     "pt_khand_reinf_b",  "pt_khand_reinf_c",   -1                    ], "spr_banner_f", "icon_mfp_khand"   ,["trp_easterling_warrior","trp_easterling_axe_master","trp_easterling_rider"         ,"trp_easterling_rider"         ,"trp_easterling_horseman"       ],"p_town_khand_camp"      ,faction_side_eye   , theatre_SE),
    ("fac_umbar"   ,3500,"fac_culture_8" , "trp_umbar_lord"   ,["trp_corsair_youth",      "trp_corsair_warrior",     "trp_militia_of_umbar",    "trp_veteran_marksman_of_umbar",   "trp_veteran_pikeman_of_umbar"], ["pt_umbar_reinf_a",    "pt_umbar_reinf_b",    "pt_umbar_reinf_c",  -1                    ], "spr_banner_g", "icon_mfp_umbar"   ,["trp_corsair_warrior" ,"trp_corsair_night_raider"  ,"trp_marksman_of_umbar"         ,"trp_veteran_marksman_of_umbar","trp_corsair_elite_marauder"    ],"p_town_umbar_camp"      ,faction_side_eye   , theatre_SE),
    ("fac_lorien"  ,4500,"fac_culture_9" , "trp_lorien_lord"  ,["trp_lothlorien_scout","trp_lothlorien_veteran_scout","trp_lothlorien_infantry","trp_lothlorien_elite_infantry","trp_lothlorien_veteran_warden"  ], ["pt_lorien_reinf_a",   "pt_lorien_reinf_b",  "pt_lorien_reinf_c",  "pt_lorien_p_train"   ], "spr_banner_h", "icon_mfp_lorien"  ,[-1                    ,"trp_lothlorien_infantry"   ,"trp_lothlorien_veteran_scout","trp_lothlorien_veteran_infantry","trp_galadhrim_royal_swordsman" ],"p_town_caras_galadhon"  ,faction_side_good  , theatre_N),
    ("fac_imladris",3500,"fac_culture_10", "trp_imladris_lord",["trp_rivendell_scout",   "trp_rivendell_sentinel", "trp_rivendell_veteran_sentinel", "trp_rivendell_elite_sentinel", "trp_knight_of_rivendell"   ], ["pt_imladris_reinf_a","pt_imladris_reinf_b","pt_imladris_reinf_c", "pt_rivendell_p_train"], "spr_banner_i", "icon_mfp_imladris",[-1                    ,"trp_rivendell_infantry"    ,"trp_rivendell_scout"           ,"trp_rivendell_sentinel"       ,"trp_knight_of_rivendell"       ],"p_town_imladris_camp"   ,faction_side_good  , theatre_C),
    ("fac_woodelf" ,3500,"fac_culture_11", "trp_woodelf_lord" ,["trp_greenwood_scout",  "trp_greenwood_veteran_scout", "trp_greenwood_archer", "trp_greenwood_master_archer", "trp_greenwood_royal_spearman"     ], ["pt_woodelf_reinf_a",  "pt_woodelf_reinf_b","pt_woodelf_reinf_c",  "pt_mirkwood_p_train" ], "spr_banner_j", "icon_mfp_woodelf" ,[-1                    ,"trp_greenwood_sentinel"    ,"trp_greenwood_scout"           ,"trp_greenwood_veteran_spearman","trp_greenwood_royal_spearman" ],"p_town_thranduils_halls",faction_side_good  , theatre_C),
    ("fac_moria"   ,2500,"fac_culture_12", "trp_moria_lord"   ,["trp_snaga_of_moria",         "trp_goblin_of_moria",     "trp_fell_goblin_of_moria",     "trp_large_goblin_of_moria",   "trp_mountain_goblin"    ], ["pt_moria_reinf_a",     "pt_moria_reinf_b", "pt_moria_reinf_c",    -1                    ], "spr_banner_k", "icon_mfp_moria"   ,["trp_snaga_of_moria"  ,"trp_goblin_of_moria"       ,"trp_large_goblin_of_moria"     ,"trp_fell_goblin_of_moria"     ,"trp_fell_goblin_of_moria"      ],"p_town_moria"           ,faction_side_hand  , theatre_C),
    ("fac_guldur"  ,4500,"fac_culture_13", "trp_guldur_lord"  ,["trp_orc_snaga_of_mordor","trp_large_orc_of_mordor","trp_orc_tracker_of_mordor","trp_large_orc_archer_of_mordor","trp_great_warg_rider_of_mordor"], ["pt_guldur_reinf_a",   "pt_guldur_reinf_b",  "pt_guldur_reinf_c",  -1                    ], "spr_banner_l", "icon_mfp_guldur"  ,["trp_snaga_of_moria"  ,"trp_goblin_of_moria"       ,"trp_large_goblin_of_moria"     ,"trp_fell_goblin_of_moria"     ,"trp_fell_goblin_of_moria"      ],"p_town_dol_guldur"      ,faction_side_eye   , theatre_C),
#    ("fac_northmen",2500,"fac_culture_14", "trp_northmen_lord",["trp_beorning_vale_man",      "trp_beorning_warrior",   "trp_beorning_carrock_fighter",   "trp_woodmen_scout",       "trp_woodmen_master_axemen" ], ["pt_northmen_reinf_a","pt_northmen_reinf_b","pt_northmen_reinf_c", -1                    ], "spr_banner_m", "icon_mfp_northmen",[-1                    ,"trp_beorning_warrior"      ,"trp_beorning_carrock_fighter"  ,"trp_woodmen_scout"            ,"trp_woodmen_master_axemen"     ],"p_town_woodsmen_village",faction_side_good  , theatre_N), 
    ("fac_gundabad",3500,"fac_culture_15", "trp_gundabad_lord",["trp_goblin_gundabad",     "trp_orc_gundabad",      "trp_fell_orc_warrior_gundabad", "trp_goblin_bowmen_gundabad", "trp_goblin_rider_gundabad"   ], ["pt_gundabad_reinf_a","pt_gundabad_reinf_b","pt_gundabad_reinf_c", -1                    ], "spr_banner_n", "icon_mfp_gundabad",["trp_goblin_gundabad" ,"trp_orc_gundabad"          ,"trp_fell_orc_warrior_gundabad" ,"trp_goblin_bowmen_gundabad"   ,"trp_goblin_rider_gundabad"     ],"p_town_gundabad_camp"   ,faction_side_eye   , theatre_SE),
    ("fac_dale"    ,3500,"fac_culture_16", "trp_dale_lord"    ,["trp_dale_militia",              "trp_dale_man_at_arms",       "trp_laketown_archer",      "trp_dale_warrior",    "trp_merchant_squire_or_dale"  ], ["pt_dale_reinf_a",    "pt_dale_reinf_b",    "pt_dale_reinf_c",     "pt_dale_p_train"     ], "spr_banner_f21","icon_mfp_dale"   ,[-1                    ,"trp_dale_man_at_arms"      ,"trp_laketown_archer"           ,"trp_dale_warrior"             ,"trp_dale_marchwarden"          ],"p_town_dale"            ,faction_side_eye   , theatre_SE),
    ("fac_dwarf"   ,3500,"fac_culture_17", "trp_dwarf_lord"   ,["trp_dwarven_apprentice",         "trp_dwarven_warrior",         "trp_dwarven_spearman",       "trp_dwarven_lookout",      "trp_dwarven_bowman"  ], ["pt_dwarf_reinf_a",    "pt_dwarf_reinf_b",   "pt_dwarf_reinf_c",   "pt_dwarven_p_train"  ], "spr_banner_p", "icon_mfp_dwarf"   ,[-1                    ,"trp_dwarven_warrior"       ,"trp_dwarven_spearman"          ,"trp_dwarven_lookout"          ,"trp_dwarven_bowman"            ],"p_town_erebor"          ,faction_side_good  , theatre_N),
    ("fac_dunland" ,3500,"fac_culture_18", "trp_dunland_lord" ,["trp_dunnish_warrior",    "trp_dunnish_veteran_pikeman",    "trp_dunnish_raven_rider",    "trp_dunnish_wolf_guard",   "trp_dunnish_wolf_warrior" ], ["pt_dunland_reinf_a", "pt_dunland_reinf_b", "pt_dunland_reinf_c",  -1                    ], "spr_banner_q", "icon_mfp_dunland" ,["trp_dunnish_warrior" ,"trp_dunnish_pikeman"       ,"trp_dunnish_pikeman"           ,"trp_dunnish_pikeman"          ,"trp_dunnish_pikeman"           ],"p_town_dunland_camp"    ,faction_side_hand  , theatre_SE),
    ("fac_beorn"   ,2500,"fac_culture_14", "trp_beorn_lord"   ,["trp_beorning_vale_man",      "trp_beorning_warrior",   "trp_beorning_carrock_fighter",   "trp_woodmen_scout",       "trp_woodmen_master_axemen" ], ["pt_northmen_reinf_a","pt_northmen_reinf_b","pt_northmen_reinf_c", -1                    ], "spr_banner_q", "icon_mfp_northmen",[-1                    ,"trp_beorning_warrior"      ,"trp_beorning_carrock_fighter"  ,"trp_woodmen_scout"            ,"trp_woodmen_master_axemen"     ],"p_town_beorn_house"     ,faction_side_good  , theatre_N),
]

  
# feudal troops guarding some Gondor centers
# 0) subfaction index,     
# 1) city,    
# 2) substring_present_in_all_troop_names ,     
# 3)  [guard_troop,                prison_guard_troop,                   castle_guard_troop  ], 
# 4)  [ reinforcements for garrisons], 
# 5) [leaders...]
subfaction_data= [ # center          guard_troop,                prison_guard_troop,                   castle_guard_troop  
 (subfac_pelargir,     "p_town_pelargir"     ,"Pelargir"  ,[  "trp_gondor_militiamen",       "trp_gondor_swordsmen",                "trp_veteran_knight_of_gondor"  ],["pt_pelargir_reinf_a",   "pt_pelargir_reinf_b",  "pt_pelargir_reinf_c"],  ["trp_pelargir_leader", "trp_pelargir_marine_leader",]),
 (subfac_dol_amroth,   "p_town_dol_amroth"   ,"Amroth"    ,[  "trp_squire_of_dol_amroth",    "trp_veteran_squire_of_dol_amroth",    "trp_swan_knight_of_dol_amroth" ],["pt_dol_amroth_reinf_a", "pt_dol_amroth_reinf_b","pt_dol_amroth_reinf_c"],["trp_dol_amroth_leader"]),
 (subfac_ethring,      "p_town_ethring"      ,"Lamedon"   ,[  "trp_clansman_of_lamedon",     "trp_footman_of_lamedon",     			"trp_veteran_of_lamedon"  ],     ["pt_ethring_reinf_a",   "pt_ethring_reinf_b",   "pt_ethring_reinf_c"],     ["trp_lamedon_leader"]),
 (subfac_lossarnach,   "p_town_lossarnach"   ,"Lossarnach",[  "trp_woodsman_of_lossarnach",  "trp_axeman_of_lossarnach",            "trp_axemaster_of_lossarnach"   ],["pt_lossarnach_reinf_a", "pt_lossarnach_reinf_b","pt_lossarnach_reinf_c"],["trp_lossarnach_leader"]),
 (subfac_pinnath_gelin,"p_town_pinnath_gelin","Pinnath"   ,[  "trp_warrior_of_pinnath_gelin","trp_veteran_warrior_of_pinnath_gelin","trp_champion_of_pinnath_gelin"],["pt_pinnath_reinf_a",    "pt_pinnath_reinf_b",   "pt_pinnath_reinf_c"],    ["trp_pinnath_leader"]),
 (subfac_rangers,      "p_town_henneth_annun","Ithilien"  ,[  "trp_warrior_of_pinnath_gelin","trp_veteran_warrior_of_pinnath_gelin","trp_champion_of_pinnath_gelin"],["pt_ithilien_reinf_a",   "pt_ithilien_reinf_b",  "pt_ithilien_reinf_c"],   ["trp_ithilien_leader"]),
 (subfac_blackroot,    "p_town_erech"        ,"Blackroot" ,[  "trp_blackroot_vale_archer",   "trp_footman_of_blackroot_vale", 	    "trp_master_blackroot_vale_archer"],["pt_blackroot_reinf_a","pt_blackroot_reinf_b",  "pt_blackroot_reinf_c"],["trp_blackroot_leader"]),
 
]


# Specify patrol/scout/raider party templates here
# Format:
# (town_id/castle_id/village_id, scout_id, raider_id, patrol_id, cavaran_id),
# Use -1 to indicate a center should not spawn such kind of party
#
ws_party_spawns_list = [
#   ("p_town_name"            , "pt_faction_scouts",           "pt_faction_raiders",     "pt_faction_patrol",    "pt_faction_caravan"),
#Gondor    
	("p_town_minas_tirith"    , "pt_gondor_scouts",            "pt_gondor_raiders",      "pt_gondor_company",    "pt_gondor_caravan"),
    ("p_town_pinnath_gelin"   , "pt_pinnath_gelin_auxila",      -1,                      "pt_gondor_patrol",     "pt_gondor_caravan"),
    ("p_town_pelargir"        , "pt_gondor_scouts",            "pt_gondor_raiders",      "pt_gondor_patrol",     "pt_gondor_caravan"),
    ("p_town_linhir"          , "pt_gondor_scouts",            "pt_gondor_raiders",      "pt_gondor_patrol",     "pt_gondor_caravan"),
    ("p_town_dol_amroth"      , "pt_gondor_scouts",            "pt_gondor_raiders",      "pt_gondor_patrol",     "pt_gondor_caravan"),
    ("p_town_edhellond"       , "pt_lemedon_auxila",           "pt_gondor_raiders",      "pt_gondor_patrol",     "pt_gondor_caravan"),
    ("p_town_lossarnach"      , "pt_gondor_scouts",            "pt_gondor_raiders",      "pt_gondor_patrol",     "pt_gondor_caravan"),
    ("p_town_tarnost"         , "pt_gondor_scouts",            "pt_gondor_raiders",      "pt_gondor_patrol",     "pt_gondor_caravan"),
    ("p_town_erech"           , "pt_blackroot_auxila",         "pt_gondor_raiders",      "pt_gondor_patrol",     "pt_gondor_caravan"),
    ("p_town_west_osgiliath"  , "pt_gondor_scouts",            "pt_gondor_raiders",      "pt_gondor_patrol",     -1),
    ("p_town_henneth_annun"   , "pt_gondor_scouts",            "pt_gondor_raiders",      -1,                     -1),
#Rohan    
	("p_town_edoras"          , "pt_rohan_scouts",             "pt_rohan_raiders",       "pt_rohan_patrol",      "pt_rohan_caravan"),
 	("p_town_aldburg"         , "pt_rohan_scouts",             "pt_rohan_raiders",       "pt_rohan_patrol",      "pt_rohan_caravan"),
	("p_town_hornburg"        , "pt_rohan_scouts",             "pt_rohan_raiders",       "pt_rohan_patrol",      "pt_rohan_caravan"),
	("p_town_east_emnet"      , "pt_rohan_scouts",             "pt_rohan_raiders",       "pt_rohan_patrol",      "pt_rohan_caravan"),
	("p_town_westfold"        , "pt_rohan_scouts",             "pt_rohan_raiders",       "pt_rohan_patrol",      "pt_rohan_caravan"),
	("p_town_west_emnet"      , "pt_rohan_scouts",             "pt_rohan_raiders",       "pt_rohan_patrol",      "pt_rohan_caravan"),
	("p_town_eastfold"        , "pt_rohan_scouts",             "pt_rohan_raiders",       "pt_rohan_patrol",      "pt_rohan_caravan"),
#Mordor   
	("p_town_minas_morgul"    , "pt_mordor_scouts",            "pt_mordor_war_party",     -1,                    "pt_mordor_caravan"),
	("p_town_morannon"        , "pt_mordor_scouts",            "pt_mordor_war_party",     -1,                    "pt_mordor_caravan"),
	("p_town_east_osgiliath"  , "pt_mordor_scouts",            -1,                        -1,                    -1),
	("p_town_orc_sentry_camp" , "pt_mordor_scouts",            -1,                        -1,                    -1),
#Isengard
	("p_town_isengard"        , "pt_isengard_scouts",          "pt_isengard_scouts_b",    -1,                    "pt_isengard_caravan"),
	("p_town_urukhai_outpost" , "pt_isengard_scouts",          "pt_isengard_scouts_b",    -1,                    "pt_isengard_caravan"),
	("p_town_urukhai_h_camp"  , "pt_isengard_scouts",          "pt_isengard_scouts_b",    -1,                    "pt_isengard_caravan"),
	("p_town_urukhai_r_camp"  , "pt_isengard_scouts",          "pt_isengard_scouts_b",    -1,                    "pt_isengard_caravan"),
#Others
	("p_town_caras_galadhon"  , "pt_lorien_scouts",            "pt_lorien_raiders",      "pt_lorien_patrol",     "pt_lorien_caravan"),
	("p_town_thranduils_halls", "pt_woodelves_scouts",         "pt_mirkwood_raiders",    "pt_mirkwood_patrol",   "pt_mirkwood_caravan"),
	("p_town_dale"            , "pt_dale_scouts",              "pt_dale_raiders",        "pt_dale_patrol",       "pt_dale_caravan"),
	("p_town_imladris_camp"   , "pt_rivendell_scouts",         "pt_rivendell_raiders",   "pt_rivendell_patrol",  "pt_rivendell_caravan"),
	("p_town_erebor"          , "pt_dwarven_scouts",           "pt_dwarven_raiders",     "pt_dwarven_patrol",    "pt_dwarven_caravan"),
]

# TLD Spawn frequency multiplier. How frequent a party can spawn
ws_scout_freq_multiplier = 3.5
ws_patrol_freq_multiplier = 1.5
ws_raider_freq_multiplier = 2.5
ws_caravan_freq_multiplier = 2.5
ws_host_freq_multiplier = 1

# TLD Party limit multiplier. Maximum number of parties depending on the faction strength. (Namely strength*multiplier is the party number limit)
ws_scout_limit_multiplier = 10
ws_patrol_limit_multiplier = 4.5
ws_raider_limit_multiplier = 7
ws_caravan_limit_multiplier = 5.5
ws_host_limit_multiplier = 4

# TLD Party victory points. Faction strength got diminished by these when party is killed.
ws_scout_vp   = 20
ws_patrol_vp  = 100
ws_raider_vp  = 50
ws_caravan_vp = 200
ws_host_vp    = 500  # for hero-led parties (hosts). Only those killed can flip faction strength to lower level
ws_alone_vp   = 100  # for hero-led parties (alone).
ws_p_train_vp = 50

# TLD faction restoration speed (added each 2 hours to faction strength)
ws_faction_restoration = 1

###########################################################################################
# center scenes list, to assign subscenes and npcs to centers
# instead of ordering scenes and npcs in module_troops, which is cumbersome
center_list = [
    # (party_center,  [scenes: center, castle, prison, tavern, arena], 
	#     [npcs: barman, smith, merchant, elder, lord, 4 walkers], 
	#     [map banner], [shop: horses,1h,2h,pole,arrows,bolts,shield,bow,crossbow,thrown,goods,head,body,foot,hand],[arena:team#,size 123] )
    # -1 if no such subscene or npc
	("p_zendar", ["scn_zendar_center", -1, -1,"scn_the_happy_boar","scn_zendar_arena"],
	    ["trp_barman_mtirith", "trp_smith_mtirith", "trp_town_1_horse_merchant", "trp_elder", "pt_gondor_reinf_a", "trp_gondor_lord", "trp_walker_woman_gondor_bw","trp_walker_man_gondor_black","trp_walker_man_gondor_white","trp_walker_woman_gondor_w"],
		[0],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1],[2,1,4,1,4,1]),
	("p_town_minas_tirith", ["scn_minas_tirith_center", "scn_minas_tirith_castle", "scn_gondor_prison","scn_gondor_tavern","scn_gondor_arena"],
	    ["trp_barman_mtirith", "trp_smith_mtirith", "trp_town_1_horse_merchant", "trp_elder", "pt_gondor_reinf_a", "trp_gondor_lord", "trp_walker_woman_gondor_bw","trp_walker_man_gondor_black","trp_walker_man_gondor_white","trp_walker_woman_gondor_w"], 
		["icon_mfc_gondor"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,2000],[2,1,4,1,4,1]),
	("p_town_pelargir", ["scn_pelargir_center", "scn_gondor_castle_a", "scn_gondor_prison","scn_gondor_tavern","scn_gondor_arena"],
	    ["trp_barman_pelargir", "trp_smith_pelargir", "trp_town_2_horse_merchant", "trp_elder", "pt_gondor_reinf_a", "trp_gondor_lord", "trp_walker_woman_gondor_bw","trp_walker_man_gondor_black","trp_walker_man_gondor_white","trp_walker_woman_gondor_b"], 
		["icon_mfc_gondor"],[3,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[4,4,4,6,4,8]),
	("p_town_linhir", ["scn_linhir_center", "scn_gondor_castle_b", "scn_gondor_prison","scn_gondor_tavern","scn_gondor_arena"],
	    ["trp_barman_linhir", "trp_smith_linhir", "trp_town_3_horse_merchant", "trp_elder", "pt_gondor_reinf_a", "trp_gondor_lord", "trp_walker_woman_gondor_bw","trp_walker_man_gondor_black","trp_walker_man_gondor_green","trp_walker_woman_gondor_b"], 
		["icon_mfc_gondor"],[2,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,8,2,8,2,8]),
	("p_town_dol_amroth", ["scn_dol_amroth_center", "scn_dol_amroth_castle", "scn_gondor_prison","scn_gondor_tavern","scn_gondor_arena"],
	    ["trp_barman_dolamroth", "trp_smith_dolamroth", "trp_town_4_horse_merchant", "trp_elder", "pt_gondor_reinf_a", "trp_gondor_lord", "trp_walker_woman_gondor_bw","trp_walker_man_gondor_white","trp_walker_man_gondor_blue","trp_walker_woman_gondor_b"], 
		["icon_mfc_gondor"],[3,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,8,3,8,2,5]),
	("p_town_edhellond", ["scn_edhellond_center", "scn_gondor_castle", "scn_gondor_prison","scn_gondor_tavern","scn_gondor_arena"],
	    ["trp_barman_edhellond", "trp_smith_edhellond", "trp_town_5_horse_merchant", "trp_elder", "pt_gondor_reinf_a", "trp_gondor_lord", "trp_walker_woman_gondor_bw","trp_walker_man_gondor_black","trp_walker_man_gondor_green","trp_walker_woman_gondor_b"], 
		["icon_mfc_gondor"],[2,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,3,2,5,2,8]),
	("p_town_lossarnach", ["scn_lossarnach_center", "scn_gondor_castle", "scn_gondor_prison","scn_gondor_tavern","scn_gondor_arena"],
	    ["trp_barman_lossarnach", "trp_smith_lossarnach", "trp_town_6_horse_merchant", "trp_elder", "pt_gondor_reinf_a", "trp_gondor_lord", "trp_walker_woman_gondor_bw","trp_walker_man_gondor_blue","trp_walker_man_gondor_green","trp_walker_woman_gondor_b"], 
		["icon_mfc_gondor"],[2,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,4,3,4,3,6]),
	("p_town_tarnost", ["scn_tarnost_center", "scn_gondor_castle_c", "scn_gondor_prison","scn_gondor_tavern","scn_gondor_arena"],
	    ["trp_barman_tarnost", "trp_smith_tarnost", "trp_town_7_horse_merchant", "trp_elder", "pt_gondor_reinf_a", "trp_gondor_lord", "trp_walker_woman_gondor_bw","trp_walker_man_gondor_black","trp_walker_man_gondor_green","trp_walker_woman_gondor_b"], 
		["icon_mfc_gondor"],[5,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[4,4,4,6,4,8]),
	("p_town_erech", ["scn_erech_center", "scn_gondor_castle", "scn_gondor_prison","scn_gondor_tavern","scn_gondor_arena"],
	    ["trp_barman_erech", "trp_smith_erech", "trp_town_8_horse_merchant", "trp_elder", "pt_gondor_reinf_a", "trp_gondor_lord", "trp_walker_woman_gondor_bw","trp_walker_man_gondor_black","trp_walker_man_gondor_green","trp_walker_woman_gondor_b"], 
		["icon_mfc_gondor"],[8,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[3,1,3,3,3,7]),
	("p_town_pinnath_gelin", ["scn_pinnath_gelin_center", "scn_gondor_castle", "scn_gondor_prison","scn_gondor_tavern","scn_gondor_arena"],
	    ["trp_barman_pinnath", "trp_smith_pinnath", "trp_town_9_horse_merchant", "trp_elder", "pt_gondor_reinf_a", "trp_gondor_lord", "trp_walker_woman_gondor_bw","trp_walker_man_gondor_black","trp_walker_man_gondor_green","trp_walker_woman_gondor_b"], 
		["icon_mfc_gondor"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,2,2,5,2,8]),
	("p_town_west_osgiliath", ["scn_west_osgiliath_center", "scn_west_osgiliath_castle", -1, -1, -1],
	    [-1, "trp_smith_wosgiliath", "trp_town_11_horse_merchant", -1 , "pt_gondor_reinf_a", "trp_gondor_lord", "trp_gondor_commoner","trp_gondor_militiamen","trp_gondor_spearmen","trp_gondor_swordsmen"], 
		["icon_mfc_gondor"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_henneth_annun", ["scn_henneth_annun_center", "scn_henneth_annun_castle", -1, -1, -1],
	    [-1, "trp_smith_hannun", "trp_no_troop", -1, "pt_gondor_reinf_a", "trp_gondor_lord", "trp_gondor_commoner","trp_gondor_militiamen","trp_gondor_spearmen","trp_gondor_swordsmen"], 
		["icon_mfc_gondor"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_cair_andros", ["scn_cair_andros_center", "scn_cair_andros_castle", -1, -1, -1],
	    [-1, "trp_smith_candros", "trp_no_troop", -1, "pt_gondor_reinf_a", "trp_gondor_lord", "trp_gondor_commoner","trp_gondor_militiamen","trp_gondor_spearmen","trp_gondor_swordsmen"], 
		["icon_mfc_gondor"],[6,1,1,1,1,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_ethring", ["scn_ethring_center", "scn_gondor_castle", "scn_gondor_prison","scn_gondor_tavern","scn_gondor_arena"],
	    ["trp_barman_ethring", "trp_smith_ethring", "trp_no_troop", "trp_elder", "pt_gondor_reinf_a", "trp_gondor_lord", "trp_gondor_commoner","trp_walker_man_gondor_black","trp_walker_man_gondor_green","trp_walker_woman_gondor_b"], 
		["icon_mfc_gondor"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,2,2,5,2,8]),
# Rohan centers
	("p_town_edoras", ["scn_edoras_center", "scn_edoras_castle", "scn_rohan_prison","scn_rohan_tavern","scn_rohan_arena"],
	    ["trp_barman_edoras", "trp_smith_edoras", "trp_town_14_horse_merchant", "trp_elder", "pt_rohan_reinf_a", "trp_rohan_lord", "trp_walker_woman_rohan_d", "trp_walker_man_rohan_t", "trp_walker_man_rohan_d", "trp_walker_woman_rohan_t"], 
		["icon_mfc_rohan"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,8,3,4,3,6]),
	("p_town_aldburg", ["scn_aldburg_center", "scn_rohan_castle", "scn_rohan_prison","scn_rohan_tavern","scn_rohan_arena"],
	    ["trp_barman_aldburg", "trp_smith_aldburg", "trp_town_15_horse_merchant", "trp_elder", "pt_rohan_reinf_a", "trp_rohan_lord", "trp_walker_woman_rohan_d", "trp_walker_man_rohan_t", "trp_walker_man_rohan_d", "trp_walker_woman_rohan_t"], 
		["icon_mfc_rohan"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,3,2,5,2,8]),
	("p_town_hornburg", ["scn_hornburg_center", -1, "scn_rohan_prison","scn_rohan_tavern", -1],
	    ["trp_barman_hornburg", "trp_smith_hornburg", "trp_town_16_horse_merchant", "trp_elder", "pt_rohan_reinf_a", "trp_rohan_lord", "trp_rohan_youth", "trp_walker_man_rohan_t", "trp_guardsman_of_rohan", "trp_footman_of_rohan"], 
		["icon_mfc_rohan"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[3,8,4,6,4,5]),
	("p_town_east_emnet", ["scn_east_emnet_center", "scn_rohan_castle_a", "scn_rohan_prison","scn_rohan_tavern","scn_rohan_arena"],
	    ["trp_barman_eastemnet", "trp_smith_eastemnet", "trp_town_17_horse_merchant", "trp_elder", "pt_rohan_reinf_a", "trp_rohan_lord", "trp_walker_woman_rohan_d", "trp_walker_man_rohan_t", "trp_walker_man_rohan_d", "trp_walker_woman_rohan_t"], 
		["icon_mfc_rohan"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,8,4,5,4,7]),
	("p_town_westfold", ["scn_westfold_center", "scn_rohan_castle_b", "scn_rohan_prison","scn_rohan_tavern","scn_rohan_arena"],
	    ["trp_barman_westfold", "trp_smith_westfold", "trp_town_18_horse_merchant", "trp_elder", "pt_rohan_reinf_a", "trp_rohan_lord", "trp_walker_woman_rohan_d", "trp_walker_man_rohan_t", "trp_walker_man_rohan_d", "trp_walker_woman_rohan_t"], 
		["icon_mfc_rohan"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,4,2,5,2,6]),
	("p_town_west_emnet", ["scn_west_emnet_center", "scn_rohan_castle_a", "scn_rohan_prison","scn_rohan_tavern","scn_rohan_arena"],
	    ["trp_barman_westemnet", "trp_smith_westemnet", "trp_town_19_horse_merchant", "trp_elder", "pt_rohan_reinf_a", "trp_rohan_lord", "trp_walker_woman_rohan_d", "trp_walker_man_rohan_t", "trp_walker_man_rohan_d", "trp_walker_woman_rohan_t"], 
		["icon_mfc_rohan"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,8,3,4,3,6]),
	("p_town_eastfold", ["scn_eastfold_center", "scn_rohan_castle_b", "scn_rohan_prison","scn_rohan_tavern","scn_rohan_arena"],
	    ["trp_barman_eastfold", "trp_smith_eastfold", "trp_town_20_horse_merchant", "trp_elder", "pt_rohan_reinf_a", "trp_rohan_lord", "trp_walker_woman_rohan_d", "trp_walker_man_rohan_t", "trp_walker_man_rohan_d", "trp_walker_woman_rohan_t"], 
		["icon_mfc_rohan"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[3,8,4,6,4,5]),
# Mordor centers
#	("p_town_barad_dur", ["scn_barad_dur_center", "scn_mordor_castle", "scn_mordor_prison","scn_mordor_tavern","scn_mordor_arena"],
#	    ["trp_barman_baraddur", "trp_smith_baraddur", "trp_town_21_horse_merchant", "trp_elder", "pt_mordor_reinf_a", "trp_mordor_lord", "trp_uruk_of_mordor", "trp_orc_of_mordor", "trp_large_orc_of_mordor", "trp_orc_tracker_of_mordor"], 
#		["icon_mfc_mordor"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_morannon", ["scn_morannon_center", "scn_mordor_castle_a", "scn_mordor_prison","scn_mordor_tavern","scn_mordor_arena"],
	    ["trp_barman_morannon", "trp_smith_morannon", "trp_town_22_horse_merchant", "trp_elder", "pt_mordor_reinf_a", "trp_mordor_lord", "trp_uruk_of_mordor", "trp_orc_of_mordor", "trp_large_orc_of_mordor", "trp_orc_tracker_of_mordor"], 
		["icon_mfc_mordor"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,8,4,5,4,7]),
	("p_town_minas_morgul", ["scn_minas_morgul_center", "scn_mordor_castle_b", "scn_mordor_prison","scn_mordor_tavern","scn_mordor_arena"],
	    ["trp_barman_mmorgul", "trp_smith_mmorgul", "trp_town_23_horse_merchant", "trp_elder", "pt_mordor_reinf_a", "trp_mordor_lord", "trp_uruk_of_mordor", "trp_orc_of_mordor", "trp_large_orc_of_mordor", "trp_orc_tracker_of_mordor"], 
		["icon_mfc_mordor"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,4,2,5,2,6]),
#	("p_town_mount_doom", ["scn_mount_doom_center", -1, -1, -1, -1],
#	    [-1, -1, -1, "trp_elder", "pt_mordor_reinf_a", "trp_mordor_lord", "trp_uruk_of_mordor", "trp_orc_of_mordor", "trp_large_orc_of_mordor", "trp_orc_tracker_of_mordor"], 
#		["icon_mfc_mordor"],[1,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_cirith_ungol", ["scn_cirith_ungol_center", "scn_mordor_castle", "scn_mordor_prison","scn_mordor_tavern","scn_mordor_arena"],
	    ["trp_barman_cungol", "trp_smith_cungol", "trp_town_25_horse_merchant", "trp_elder", "pt_mordor_reinf_a", "trp_mordor_lord", "trp_uruk_of_mordor", "trp_orc_of_mordor", "trp_large_orc_of_mordor", "trp_orc_tracker_of_mordor"], 
		["icon_mfc_mordor"],[2,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_orc_sentry_camp", ["scn_orc_sentry_camp_center", -1, -1, -1, -1],
	    [-1, "trp_smith_oscamp", "trp_town_26_horse_merchant", "trp_elder", "pt_mordor_reinf_a", "trp_mordor_lord", "trp_uruk_of_mordor", "trp_orc_of_mordor", "trp_large_orc_of_mordor", "trp_orc_tracker_of_mordor"], 
		["icon_mfc_mordor"],[2,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_east_osgiliath", ["scn_east_osgiliath_center", -1, -1, -1, -1],
	    [-1, "trp_smith_eosgiliath", "trp_town_10_horse_merchant", "trp_elder", "pt_mordor_reinf_a", "trp_mordor_lord", "trp_uruk_of_mordor", "trp_orc_of_mordor", "trp_large_orc_of_mordor", "trp_orc_tracker_of_mordor"], 
		["icon_mfc_mordor"],[1,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_isengard", ["scn_isengard_center", "scn_isengard_castle", "scn_mordor_prison","scn_mordor_tavern","scn_mordor_arena"],
	    ["trp_barman_isengard", "trp_smith_isengard", "trp_town_26_horse_merchant", "trp_elder", "pt_isengard_reinf_a",  "trp_isengard_lord","trp_orc_of_isengard","trp_large_orc_of_isengard","trp_uruk_hai_scout","trp_uruk_hai_of_isengard"], 
		["icon_mfc_isengard"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_urukhai_outpost", ["scn_uruk_hai_outpost_center", -1, -1, -1, -1],
	    [-1, "trp_smith_uoutpost", "trp_town_28_horse_merchant", "trp_elder", "pt_isengard_reinf_a",  "trp_isengard_lord","trp_orc_of_isengard","trp_large_orc_of_isengard","trp_uruk_hai_scout","trp_uruk_hai_of_isengard"], 
		["icon_mfc_isengard"],[3,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_urukhai_h_camp", ["scn_uruk_hai_h_camp_center", -1, -1, -1, -1],
	    [-1, "trp_smith_uhcamp", "trp_town_29_horse_merchant", "trp_elder", "pt_isengard_reinf_a",  "trp_isengard_lord","trp_orc_of_isengard","trp_large_orc_of_isengard","trp_uruk_hai_scout","trp_uruk_hai_of_isengard"], 
		["icon_mfc_isengard"],[3,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_urukhai_r_camp", ["scn_uruk_hai_r_camp_center", -1, -1, -1, -1],
	    [-1, "trp_smith_urcamp", "trp_town_30_horse_merchant", "trp_elder", "pt_isengard_reinf_a",  "trp_isengard_lord","trp_orc_of_isengard","trp_large_orc_of_isengard","trp_uruk_hai_scout","trp_uruk_hai_of_isengard"], 
		["icon_mfc_isengard"],[2,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),

	("p_town_caras_galadhon", ["scn_caras_galadhon_center", "scn_elf_castle", "scn_elf_prison","scn_elf_tavern","scn_elf_arena"],
	    ["trp_barman_cgaladhon", "trp_smith_cgaladhon", "trp_town_31_horse_merchant", "trp_elder", "pt_lorien_reinf_a", "trp_lorien_lord", "trp_lothlorien_scout", "trp_lothlorien_archer", "trp_lothlorien_infantry", "trp_lothlorien_warden"], 
		["icon_mfc_lorien"],[3,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_cerin_dolen", ["scn_cerin_dolen_center", -1, -1, -1, -1],
	    [-1, "trp_smith_cdolen", "trp_town_32_horse_merchant", "trp_elder", "pt_lorien_reinf_a",  "trp_lorien_lord", "trp_lothlorien_scout", "trp_lothlorien_archer", "trp_lothlorien_infantry", "trp_lothlorien_warden"], 
		["icon_mfc_lorien"],[1,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_cerin_amroth", ["scn_cerin_amroth_center", -1, -1, -1, -1],
	    [-1, "trp_smith_camroth", "trp_town_33_horse_merchant", "trp_elder", "pt_lorien_reinf_a",  "trp_lorien_lord", "trp_lothlorien_scout", "trp_lothlorien_archer", "trp_lothlorien_infantry", "trp_lothlorien_warden"], 
		["icon_mfc_lorien"],[2,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_thranduils_halls", ["scn_thranduils_halls_center", "scn_rohan_castle", "scn_elf_prison","scn_elf_tavern","scn_elf_arena"],
	    ["trp_barman_thalls", "trp_town_34_weaponsmith", "trp_town_34_horse_merchant", "trp_elder", "pt_woodelf_reinf_a", "trp_woodelf_lord", "trp_greenwood_archer", "trp_greenwood_scout", "trp_greenwood_archer", "trp_greenwood_spearman"], 
		["icon_mfc_woodelf"],[0,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_woodelf_camp", ["scn_woodelf_camp_center", -1, -1,-1,-1],
	    [-1, "trp_town_35_weaponsmith", "trp_town_35_horse_merchant", "trp_elder", "pt_woodelf_reinf_a", "trp_woodelf_lord", "trp_greenwood_archer", "trp_greenwood_scout", "trp_greenwood_archer", "trp_greenwood_spearman"], 
		["icon_mfc_woodelf"],[1,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_woodelf_west_camp", ["scn_woodelf_west_camp_center", -1, -1,-1,-1],
	    [-1, "trp_town_35_weaponsmith", "trp_town_35_horse_merchant", "trp_elder", "pt_woodelf_reinf_a", "trp_woodelf_lord", "trp_greenwood_archer", "trp_greenwood_scout", "trp_greenwood_archer", "trp_greenwood_spearman"], 
		["icon_mfc_woodelf"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
#	("p_town_woodelf_north_camp", ["scn_woodelf_camp_center", -1, -1,-1,-1],
#	    [-1, "trp_town_35_weaponsmith", "trp_town_35_horse_merchant", "trp_elder", "pt_woodelf_reinf_a", "trp_woodelf_lord", "trp_greenwood_archer", "trp_greenwood_scout", "trp_greenwood_archer", "trp_greenwood_spearman"], 
#		["icon_mfc_woodelf"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_woodsmen_village", ["scn_woodsmen_village_center", -1, -1,-1,-1],
	    [-1, "trp_town_36_weaponsmith", "trp_town_36_horse_merchant", "trp_elder", "pt_rohan_reinf_a", "trp_beorn_lord", "trp_beorning_vale_man", "trp_beorning_carrock_berserker", "trp_beorning_warrior", "trp_beorning_carrock_fighter"], 
		["icon_mfc_northmen"],[0,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_beorning_village", ["scn_woodsmen_village_center", -1, -1,-1,-1],
	    [-1, "trp_town_36_weaponsmith", "trp_town_36_horse_merchant", "trp_elder", "pt_rohan_reinf_a", "trp_beorn_lord", "trp_beorning_vale_man", "trp_beorning_carrock_berserker", "trp_beorning_warrior", "trp_beorning_carrock_fighter"], 
		["icon_mfc_northmen"],[0,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_beorn_house", ["scn_woodsmen_village_center", -1, -1,-1,-1],
	    [-1, "trp_town_36_weaponsmith", "trp_town_36_horse_merchant", "trp_elder", "pt_rohan_reinf_a", "trp_beorn_lord", "trp_beorning_vale_man", "trp_beorning_carrock_berserker", "trp_beorning_warrior", "trp_beorning_carrock_fighter"], 
		["icon_mfc_northmen"],[1,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),

	("p_town_moria", ["scn_moria_center", "scn_mordor_castle", "scn_mordor_prison","scn_mordor_tavern","scn_mordor_arena"],
	    ["trp_barman_moria", "trp_town_37_weaponsmith", "trp_town_37_horse_merchant", "trp_elder", "pt_moria_reinf_a", "trp_moria_lord","trp_snaga_of_moria","trp_goblin_of_moria","trp_wolf_rider_of_moria","trp_large_goblin_of_moria"], 
		["icon_mfc_moria"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_troll_cave", ["scn_troll_cave_center", -1, -1,-1,-1],
	    [-1, "trp_no_troop", "trp_no_troop", "trp_elder", "pt_moria_reinf_a", "trp_moria_lord","trp_snaga_of_moria","trp_goblin_of_moria","trp_wolf_rider_of_moria","trp_large_goblin_of_moria"], 
		["icon_mfc_moria"],[0,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),

	("p_town_dale", ["scn_dale_center", "scn_rohan_castle", "scn_rohan_prison","scn_rohan_tavern","scn_rohan_arena"],
	    ["trp_barman_dale", "trp_town_38_weaponsmith", "trp_town_38_horse_merchant", "trp_elder", "pt_dale_reinf_a", "trp_dale_lord","trp_townsman","trp_watchman","trp_dale_militia","trp_laketown_bowmen"], 
		["icon_mfc_dale"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_esgaroth", ["scn_esgaroth_center", "scn_rohan_castle", "scn_rohan_prison","scn_rohan_tavern","scn_rohan_arena"],
	    ["trp_barman_esgaroth", "trp_town_39_weaponsmith", "trp_town_39_horse_merchant", "trp_elder", "pt_dale_reinf_a", "trp_dale_lord","trp_townsman","trp_watchman","trp_dale_militia","trp_laketown_archer"], 
		["icon_mfc_dale"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),

	("p_town_dunland_camp", ["scn_dunland_camp_center", -1, -1,-1,-1],
	    [-1, "trp_town_41_weaponsmith", "trp_town_41_horse_merchant", "trp_elder", "pt_dunland_reinf_a", "trp_dunland_lord", "trp_dunnish_wildman","trp_dunnish_warrior", "trp_dunnish_pikeman", "trp_dunnish_wolf_guard"], 
		["icon_mfc_dunland"],[2,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_harad_camp", ["scn_harad_camp_center", -1, -1,-1,-1],
	    [-1, "trp_town_42_weaponsmith", "trp_town_42_horse_merchant", "trp_elder", "pt_harad_reinf_a", "trp_harad_lord","trp_harad_youth","trp_harad_desert_warrior","trp_harad_infantry","trp_harad_cavalry"], 
		["icon_mfc_harad"],[4,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_khand_camp", ["scn_khand_camp_center", -1, -1,-1,-1],
	    [-1, "trp_town_43_weaponsmith", "trp_town_43_horse_merchant", "trp_elder", "pt_khand_reinf_a", "trp_khand_lord", "trp_easterling_youth", "trp_easterling_axeman","trp_khand_glaive_whirler","trp_variag_pitfighter"], 
		["icon_mfc_khand"],[3,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_umbar_camp", ["scn_umbar_camp_center", -1, -1,-1,-1],
	    [-1, "trp_town_44_weaponsmith", "trp_town_44_horse_merchant", "trp_elder", "pt_umbar_reinf_a", "trp_umbar_lord", "trp_corsair_youth", "trp_corsair_warrior", "trp_assassin_of_umbar","trp_militia_of_umbar"], 
		["icon_mfc_umbar"],[1,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_imladris_camp", ["scn_rivendell_camp_center", -1, -1,-1,-1],
	    [-1, "trp_town_45_weaponsmith", "trp_town_45_horse_merchant", "trp_elder", "pt_imladris_reinf_a", "trp_imladris_lord", "trp_rivendell_scout","trp_rivendell_infantry", "trp_rivendell_sentinel","trp_dunedain_scout"], 
		["icon_mfc_imladris"],[2,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_dol_guldur", ["scn_dol_guldur_center", "scn_mordor_castle", "scn_mordor_prison","scn_mordor_tavern","scn_mordor_arena"],
	    ["trp_barman_dolguldur", "trp_town_46_weaponsmith", "trp_town_46_horse_merchant", "trp_elder", "pt_rohan_reinf_a", "trp_guldur_lord", "trp_uruk_of_mordor", "trp_orc_of_mordor", "trp_large_orc_of_mordor", "trp_orc_tracker_of_mordor"], 
		["icon_mfc_guldur"],[2,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_dol_guldur_north_outpost", ["scn_dol_guldur_north_outpost_center", -1, -1,-1,-1],
	    [-1, "trp_town_46_weaponsmith", "trp_town_46_horse_merchant", "trp_elder", "pt_rohan_reinf_a", "trp_guldur_lord", "trp_uruk_of_mordor", "trp_orc_of_mordor", "trp_large_orc_of_mordor", "trp_orc_tracker_of_mordor"], 
		["icon_mfc_guldur"],[1,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_north_rhun_camp", ["scn_north_rhun_camp_center", -1, -1,-1,-1],
	    [-1, "trp_town_47_weaponsmith", "trp_town_47_horse_merchant", "trp_elder", "pt_gundabad_reinf_a",  "trp_rhun_lord", "trp_rhun_noble_cavalry", "trp_rhun_vet_infantry", "trp_rhun_tribesman", "trp_rhun_tribal_warrior", ], 
		["icon_mfc_rhun"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_rhun_south_camp", ["scn_rhun_south_camp_center", -1, -1,-1,-1],
	    [-1, "trp_town_47_weaponsmith", "trp_no_troop", "trp_elder", "pt_gundabad_reinf_a",  "trp_rhun_lord", "trp_rhun_noble_cavalry", "trp_rhun_vet_infantry", "trp_rhun_tribesman", "trp_rhun_tribal_warrior", ], 
		["icon_mfc_rhun"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_rhun_north_camp", ["scn_rhun_north_camp_center", -1, -1,-1,-1],
	    [-1, "trp_no_troop", "trp_town_47_horse_merchant", "trp_elder", "pt_gundabad_reinf_a",  "trp_rhun_lord", "trp_rhun_noble_cavalry", "trp_rhun_vet_infantry", "trp_rhun_tribesman", "trp_rhun_tribal_warrior", ], 
		["icon_mfc_rhun"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_gundabad_camp", ["scn_gundabad_camp_center", -1, -1,-1,-1],
	    [-1, "trp_town_48_weaponsmith", "trp_town_48_horse_merchant", "trp_elder", "pt_gundabad_reinf_a", "trp_gundabad_lord","trp_goblin_gundabad","trp_orc_gundabad","trp_orc_fighter_gundabad","trp_goblin_rider_gundabad"], 
		["icon_mfc_gundabad"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_gundabad_ne_outpost", ["scn_gundabad_ne_outpost_center", -1, -1,-1,-1],
	    [-1, "trp_no_troop", "trp_town_48_horse_merchant", "trp_elder", "pt_gundabad_reinf_a", "trp_gundabad_lord","trp_goblin_gundabad","trp_orc_gundabad","trp_orc_fighter_gundabad","trp_goblin_rider_gundabad"], 
		["icon_mfc_gundabad"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_gundabad_nw_outpost", ["scn_gundabad_nw_outpost_center", -1, -1,-1,-1],
	    [-1, "trp_town_48_weaponsmith", "trp_no_troop", "trp_elder", "pt_gundabad_reinf_a", "trp_gundabad_lord","trp_goblin_gundabad","trp_orc_gundabad","trp_orc_fighter_gundabad","trp_goblin_rider_gundabad"], 
		["icon_mfc_gundabad"],[6,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_goblin_north_outpost", ["scn_gundabad_camp_center", -1, -1,-1,-1],
	    [-1, "trp_town_48_weaponsmith", "trp_town_48_horse_merchant", "trp_elder", "pt_gundabad_reinf_a", "trp_gundabad_lord","trp_goblin_gundabad","trp_orc_gundabad","trp_orc_fighter_gundabad","trp_goblin_rider_gundabad"], 
		["icon_mfc_gundabad"],[2,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_goblin_south_outpost", ["scn_gundabad_camp_center", -1, -1,-1,-1],
	    [-1, "trp_town_48_weaponsmith", "trp_town_48_horse_merchant", "trp_elder", "pt_gundabad_reinf_a", "trp_gundabad_lord","trp_goblin_gundabad","trp_orc_gundabad","trp_orc_fighter_gundabad","trp_goblin_rider_gundabad"], 
		["icon_mfc_gundabad"],[2,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_gundabad_mirkwood_outpost", ["scn_gundabad_mirkwood_outpost", -1, -1,-1,-1],
	    [-1, "trp_town_48_weaponsmith", "trp_town_48_horse_merchant", "trp_elder", "pt_gundabad_reinf_a", "trp_gundabad_lord","trp_goblin_gundabad","trp_orc_gundabad","trp_orc_fighter_gundabad","trp_goblin_rider_gundabad"], 
		["icon_mfc_gundabad"],[2,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_erebor", ["scn_erebor_center", "scn_rohan_castle", "scn_rohan_prison","scn_rohan_tavern","scn_rohan_arena"],
	    ["trp_barman_erebor", "trp_town_40_weaponsmith", "trp_town_40_horse_merchant", "trp_elder", "pt_dwarf_reinf_a", "trp_dwarf_lord", "trp_dwarven_apprentice", "trp_dwarven_lookout", "trp_dwarven_bowman", "trp_iron_hills_miner"], 
		["icon_mfc_dwarf"],[0,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
	("p_town_ironhill_camp", ["scn_ironhill_camp_center", -1, -1,-1,-1],
	    [-1, "trp_town_49_weaponsmith", "trp_town_49_horse_merchant", "trp_elder", "pt_dwarf_reinf_a", "trp_dwarf_lord","trp_dwarven_lookout", "trp_dwarven_bowman", "trp_iron_hills_infantry", "trp_iron_hills_miner"], 
		["icon_mfc_dwarf"],[0,2,2,2,2,0,4,2,0,2,4,4,4,2,1,900],[2,1,4,1,4,1]),
]
# evil camps that will appear only when War starts
centers_disabled_at_start =	["p_town_orc_sentry_camp","p_town_urukhai_outpost","p_town_urukhai_r_camp","p_town_dunland_camp","p_town_dol_guldur_north_outpost","p_town_rhun_south_camp","p_town_rhun_north_camp","p_town_gundabad_camp","p_town_gundabad_ne_outpost", "p_town_gundabad_nw_outpost","p_town_goblin_north_outpost","p_town_goblin_south_outpost","p_town_gundabad_mirkwood_outpost"]		 
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
 ("p_town_minas_tirith" , "p_town_pelargir", "p_town_dol_amroth", "p_town_erech", "p_town_pinnath_gelin", "p_town_edoras", "p_town_hornburg", "p_town_east_emnet", "p_town_west_emnet", "p_town_eastfold"),
 ("p_town_pelargir"     , "p_town_dol_amroth", "p_town_lossarnach", "p_town_erech", "p_town_hornburg", "p_town_east_emnet", "p_town_west_emnet", "p_town_eastfold"),
 ("p_town_linhir"       , "p_town_dol_amroth", "p_town_edhellond", "p_town_lossarnach", "p_town_tarnost", "p_town_westfold", "p_town_west_emnet", "p_town_minas_morgul"),
 ("p_town_dol_amroth"   , "p_town_lossarnach", "p_town_hornburg", "p_town_east_emnet", "p_town_west_emnet", "p_town_eastfold"),
 ("p_town_edhellond"    , "p_town_lossarnach", "p_town_tarnost", "p_town_westfold", "p_town_west_emnet"),
 ("p_town_lossarnach"   , "p_town_tarnost", "p_town_edoras", "p_town_east_emnet", "p_town_west_emnet", "p_town_eastfold", "p_town_morannon"),
 ("p_town_tarnost"      , "p_town_aldburg", "p_town_edoras", "p_town_east_emnet", "p_town_westfold", "p_town_west_emnet", "p_town_eastfold"),
 ("p_town_erech"        , "p_town_pinnath_gelin", "p_town_edoras", "p_town_hornburg", "p_town_east_emnet", "p_town_eastfold"),
 ("p_town_pinnath_gelin", "p_town_edoras", "p_town_hornburg", "p_town_east_emnet", "p_town_eastfold"),
 ("p_town_aldburg"      , "p_town_edoras", "p_town_westfold"),
 ("p_town_edoras"       , "p_town_hornburg", "p_town_east_emnet", "p_town_westfold", "p_town_eastfold"),
 ("p_town_hornburg"     , "p_town_east_emnet", "p_town_eastfold"),
 ("p_town_eastfold"     , "p_town_east_emnet", "p_town_west_emnet"),
 ("p_town_morannon"     , "p_town_minas_morgul"),
]

lords_spawn = [ ("trp_gondor_lord","p_town_minas_tirith"),
                ("trp_rohan_lord","p_town_edoras"),
				("trp_isengard_lord","p_town_isengard"),
				("trp_mordor_lord","p_town_minas_morgul"),
				("trp_lorien_lord","p_town_caras_galadhon"),
]
			 # TLD constants end
#####################################
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
            
# foxyman
cheat_switch = 1

# titles for one's own starting faction

#########################################################
# TLD faction ranks
#
# Each faction with a list (enclosed in []) of ranks, each rank with (status points for rank, salary, list of positions in [])
# Each position with (position name, list of troops[], list of items[], list of supplies[], condition script, renew troops cost, position description)
# sort them in descend order of renown/influence value

tld_faction_ranks = [
#fac_gondor = 3
[],
#fac_dwarf = 4
[],
#fac_rohan = 5
[
    (1450, 3000, [
        ("Captain of the Eorl Guard", 
            [("trp_eorl_guard_of_rohan", 10), ("trp_elite_rider_of_rohan", 30)], 
            [("itm_rohan_warhorse", 1), ("itm_rohan_armor_r", 1), ("itm_rohan_helmet_h", 1), ("itm_rohan_shield_g", 1), ("itm_rohirrim_war_greaves", 1), ("itm_rohan_cav_sword", 1), ("itm_rohirrim_short_axe", 1)],
            [("itm_smoked_fish", 5), ("itm_dried_meat", 5)],
            "script_cf_can_be_captain_of_the_eorl_guard", 300, "str_captain_of_the_eorl_guard_dscpt"
        ),
        ("Captain of the Brego Guard",
            [("trp_brego_guard_of_rohan", 10), ("trp_elite_lancer_of_rohan", 30)], 
            [("itm_rohan_warhorse", 1), ("itm_rohan_armor_r", 1), ("itm_rohan_helmet_h", 1), ("itm_rohan_shield_g", 1), ("itm_rohirrim_war_greaves", 1), ("itm_rohan_cav_sword", 1), ("itm_rohan_spear", 1), ("itm_heavy_throwing_spear", 1)],
            [("itm_smoked_fish", 5), ("itm_dried_meat", 5)],
            "script_cf_can_be_captain_of_the_brego_guard", 300, "str_captain_of_the_brego_guard_dscpt"            
        ),
    ]),
    (1100, 1500, [
        ("Captain of Edoras",
            [("trp_dismounted_thengel_guard_of_rohan", 10), ("trp_dismounted_elite_skirmisher_of_rohan", 20), ("trp_dismounted_veteran_skirmisher_of_rohan", 20)],
            [],
            [],
            -1, 250, "str_captain_of_edoras_dscpt"
        ),
    ]),
],
#fac_mordor = 6
[],
#fac_isengard = 7
[],
#fac_lorien = 8
[],
#fac_imladris = 9
[],
#fac_woodelf = 10
[],
#fac_dale = 11
[],
#fac_harad = 12
[],
#fac_rhun = 13
[],
#fac_khand = 14
[],
#fac_umbar = 15
[],
#fac_moria = 16
[],
#fac_guldur = 17
[],
#fac_gundabad = 18
[],
#fac_dunland = 19
[],
#fac_northmen = 20
[],
#fac_beorn = 21
[],
]
tfr_name_pos    = 0
tfr_soldiers_pos = 1
tfr_equipments_pos = 2
tfr_supplies_pos = 3
tfr_condition_pos = 4
tfr_con_sol_ex_pos  = 5
tfr_text_pos    = 6

tfr_name_strings_begin = "str_tfr_name_strings_begin"

#
# TLD faction ranks end
###############################################
faction_strings =[    #shop rumors begin          shop rumors end
    ("fac_gondor"  ,"str_gondor_rumor_begin", "str_other_rumor_begin"),
    ("fac_rohan"   ,"str_rohan_rumor_begin" , "str_gondor_rumor_begin"),
    ("fac_isengard","str_default_rumor", "str_rohan_rumor_begin"),
    ("fac_mordor"  ,"str_default_rumor", "str_rohan_rumor_begin"),
    ("fac_harad"   ,"str_default_rumor", "str_rohan_rumor_begin"),
    ("fac_rhun"    ,"str_default_rumor", "str_rohan_rumor_begin"),
    ("fac_khand"   ,"str_default_rumor", "str_rohan_rumor_begin"),
    ("fac_umbar"   ,"str_default_rumor", "str_rohan_rumor_begin"),
    ("fac_lorien"  ,"str_default_rumor", "str_rohan_rumor_begin"),
    ("fac_imladris","str_default_rumor", "str_rohan_rumor_begin"),
    ("fac_woodelf" ,"str_default_rumor", "str_rohan_rumor_begin"),
    ("fac_moria"   ,"str_default_rumor", "str_rohan_rumor_begin"),
    ("fac_guldur"  ,"str_default_rumor", "str_rohan_rumor_begin"),
#    ("fac_northmen","str_default_rumor", "str_rohan_rumor_begin"),
    ("fac_gundabad","str_default_rumor", "str_rohan_rumor_begin"),
    ("fac_dale"    ,"str_default_rumor", "str_rohan_rumor_begin"),
    ("fac_dwarf"   ,"str_default_rumor", "str_rohan_rumor_begin"),
    ("fac_dunland" ,"str_default_rumor", "str_rohan_rumor_begin"),
    ("fac_beorn"   ,"str_default_rumor", "str_rohan_rumor_begin"),
]

## tableau meshes list for factions
fac_tableau_list = [
#fac_gondor = 3
[ ("tableau_tld_tunic", ["mesh_tableau_mesh_gondor_tunic_a", "mesh_tableau_mesh_gondor_tunic_b"]),
],
#fac_dwarf = 4
[],
#fac_rohan = 5
[ ("tableau_tld_tunic", ["mesh_tableau_mesh_rohan_tunic"]),
],
#fac_mordor = 6
[],
#fac_isengard = 7
[],
#fac_lorien = 8
[],
#fac_imladris = 9
[],
#fac_woodelf = 10
[],
#fac_dale = 11
[ ("tableau_tld_tunic", ["mesh_tableau_mesh_dale_tunic"]),
],
#fac_harad = 12
[],
#fac_rhun = 13
[],
#fac_khand = 14
[],
#fac_umbar = 15
[],
#fac_moria = 16
[],
#fac_guldur = 17
[],
#fac_gundabad = 18
[],
#fac_dunland = 19
[],
#fac_northmen = 20
[# ("tableau_tld_tunic", ["mesh_tableau_mesh_woodman_tunic"]),
],
#fac_beorn = 21
[ ("tableau_tld_tunic", ["mesh_tableau_mesh_woodman_tunic"]),
],

]
