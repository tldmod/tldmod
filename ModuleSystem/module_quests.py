from header_quests import *

####################################################################################################################
#  Each quest record contains the following fields:
#  1) Quest id: used for referencing quests in other files. The prefix qst_ is automatically added before each quest-id.
#  2) Quest Name: Name displayed in the quest screen.
#  3) Quest flags. See header_quests.py for a list of available flags
#  4) Quest Description: Description displayed in the quest screen.
#
# Note that you may call the opcode setup_quest_text for setting up the name and description
####################################################################################################################

quests = [
# Note : This is defined as the first governer quest in module_constants.py: 
("deliver_message", "Deliver Message to {s13}", qf_random_quest,
  "{s9} asked you to take a message to {s13}. {s13} was at {s4} when you were given this quest."
  ),
("deliver_message_to_enemy_lord", "Deliver Message to {s13}", qf_random_quest,
  "{s9} asked you to take a message to {s13} of {s15}. {s13} was at {s4} when you were given this quest."
  ),
("raise_troops", "Raise {reg1} {s14}", qf_random_quest,
  "{s9} asked you to raise {reg1} {s14} and bring them to him."
  ),
("escort_messenger", "Escort the messenger to {s14}", qf_random_quest,
  "None"
  ),
#( "rescue_lady_under_siege", "Rescue {s3} from {s4}", qf_random_quest,
#  "{s1} asked you to rescue his {s7} {s3} from {s4} and return her back to him."
#  ),
#( "deliver_message_to_lover", "Deliver Message to {s3}", qf_random_quest,
#  "{s1} asked you to take a message to his lover {s3} at {s4}."
#  ),
#( "bring_prisoners_to_enemy", "Bring Prisoners to {s4}", qf_random_quest,
#  "{s1} asked you to bring {reg1} {s3} as prisoners to the guards at {s4}."
#  ),
#( "bring_reinforcements_to_siege", "Bring Reinforcements to the Siege of {s5}", qf_random_quest,
#  "{s1} asked you to bring {reg1} {s3} to {s4} at the siege of {s5}."
#  ),
#( "deliver_supply_to_center_under_siege", "Deliver Supplies to {s5}", qf_random_quest,
#  "TODO: Take {reg1} cartloads of supplies from constable {s3} and deliver them to constable {s4} at {s5}."
#  ),
#( "deal_with_bandits_at_lords_village", "Save the Village of {s15} from Marauding Bandits", qf_random_quest,
#  "{s13} asked you to deal with the bandits who took refuge in his village of {s15} and then report back to him."
#  ),
#( "collect_taxes", "Collect taxes from {s3}", qf_random_quest,
#  "{s9} asked you to collect taxes from {s3}. He offered to leave you one-fifth of all the money you collect there."
#  ),
("hunt_down_fugitive", "Hunt down {s4}", qf_random_quest,
  "{s9} asked you to hunt down the fugitive named {s4}. He is currently believed to be at {s3}."
  ),
#( "capture_messenger", "Capture {s3}", qf_random_quest,
#  "{s1} asked you to capture a {s3} and bring him back."
#  ),
#( "bring_back_deserters", "Bring {reg1} {s3}", qf_random_quest,
#  "{s1} asked you to bring {reg1} {s3}."
#  ),

#( "kill_local_merchant", "Assassinate Local Merchant at {s3}", qf_random_quest,
#  "{s9} asked you to assassinate a local merchant at {s3}."
#  ),
( "bring_back_runaway_serfs", "Bring Back Runaway Slaves", qf_random_quest,
  "{s9} asked you to bring back the three groups of runaway slaves back to {s2}. He said all three groups must be running away in the direction of {s3}."
  ),
("follow_spy", "Follow the Spy to Meeting", qf_random_quest,
  "{s11} asked you to follow the spy that will leave {s12}. You must be careful not to be seen by the spy during his travel, or else he may get suspicious and turn back. Once the spy meets with his accomplice, you are to ambush and capture them and bring them both back to {s11}."
  ),
("capture_enemy_hero", "Capture an enemy commander", qf_random_quest,
  "{s11} asked you to capture an enemy commander."
  ),
("lend_companion", "Lend Your Companion {s3} to {s9}", qf_random_quest,
  "{s9} asked you to lend your companion {s3} to him for a week."
  ),
#( "collect_debt", "Collect the debt {s3} owes to {s9}", qf_random_quest,
#  "{s9} asked you to collect the debt of {reg4} denars {s3} owes to him."
#  ),
#( "capture_conspirators", "Capture Conspirators", qf_random_quest,
#  "TODO: {s1} asked you to capture all troops in {reg1} conspirator parties that plan to rebel against him and join {s3}."
#  ),
#( "defend_nobles_against_peasants", "Defend Nobles Against Peasants", qf_random_quest,
#  "TODO: {s1} asked you to defend {reg1} noble parties against peasants."
#  ),
#( "incriminate_loyal_commander", "Incriminate the Loyal Commander of {s13}, {s16}", qf_random_quest,
#  "None"
#  ),
#( "raid_caravan_to_start_war", "Raid {reg13} Caravans of {s13}", qf_random_quest,
#  "None"
#  ),
#( "meet_spy_in_enemy_town", "Meet Spy in {s13}", qf_random_quest,
#  "None"
#  ),
("capture_prisoners", "Bring {reg1} enemy prisoners", qf_random_quest,
  "{s9} wanted you to bring him {reg1} enemy prisoners."
  ),
  
# TLD BEGIN   lord's quests  (mtarini)
("investigate_fangorn", "Investigate Fangorn", qf_random_quest,
  "{s9} asked you to find out what is going on in the Fangorn forest, and to report back."
  ),
("capture_troll", "Capture a Troll", qf_random_quest,
   "{s9} asked you to bring back a savage troll for use in his army."
  ),
("kill_troll", "Dispatch raging Troll", qf_random_quest,
   "{s9} asked you to free {s13} from the menace of a Troll raging in its outskirts."
  ),
("mirkwood_sorcerer", "Slay a sorcerer in Mirkwood", qf_random_quest,
  "Galadriel's power to defend Lothlorien has been undermined by the foul rituals of a sorcerer of Dol Guldur.  Though he is a mortal, he represents a great threat to the Elves. Search for him in Mirkwood forest, not far from Dol Guldur itself. Use stealth to prevent the alarm from being raised as there will be only one opportunity to defeat him."
  ),
("find_lost_spears", "Find the lost spears of king Bladorthin", qf_random_quest,
  "{s9} asked you to find the lost spears dwarves once made for king Bladorthin. You have to ask the dwarves permission to search for the spears in the depths of the Lonely Mountain."
  ),

#TLD lord missions begin (MV)
( "rescue_prisoners", "Rescue {reg1} Prisoners", qf_random_quest,
  "{s9} wanted you to rescue {reg1} prisoners."
  ),
( "scout_enemy_town", "Scout Enemy Town", qf_random_quest,
  "{s9} asked you to scout around {s13}."
  ),
( "dispatch_scouts", "Dispatch a Scout Party", qf_random_quest,
  "{s9} asked you to dispatch a scout party near {s13}."
  ),
( "eliminate_patrols", "Eliminate {reg1} Enemy Parties", qf_random_quest,
  "{s9} asked you to eliminate {reg1} {s13} enemy parties."
  ),
( "lend_surgeon", "Lend Your Surgeon {s3} to {s1}", qf_random_quest,
  "Lend your experienced surgeon {s3} to {s1}."
  ),
#TLD lord missions end  

#( "hunt_down_raiders", "Hunt Down Raiders",qf_random_quest,
#  "{s1} asked you to hunt down and punish the raiders that attacked a village near {s3} before they reach the safety of their base at {s4}."
#  ),

##################
# Kingdom Army quests
##################
# Note : This is defined as lord quests end in module_constants.py:
( "follow_army", "Follow {s9}'s Army", qf_random_quest,
  "None"
  ),
( "report_to_army", "Report to {s13}", qf_random_quest,
  "None"
  ),
# Note : This is defined as the first army quest in module_constants.py:
( "deliver_cattle_to_army", "Deliver {reg3} units of food to {s13}", qf_random_quest,
  "None"
  ),
( "join_siege_with_army", "Join the Siege of {s14}", qf_random_quest,
  "None"
  ),
( "scout_waypoints", "Scout {s13}, {s14} and {s15}", qf_random_quest,
  "None"
  ),
##################
# Mayor quests
##################
# Note : This is defined as the first mayor quest in module_constants.py: 
( "move_cattle_herd", "Move {s12} to {s13}", qf_random_quest,
  "The Elder of {s10} asked you to move some {s12} to {s13}."
  ),
( "escort_merchant_caravan", "Escort Supply Train to {s8}", qf_random_quest,
  "Escort the supply train to {s8}."
  ),
( "deliver_wine", "Deliver {reg5} Units of {s6} to {s4}", qf_random_quest,
  "The {s9} of {s3} asked you to deliver {reg5} units of {s6} to {s4} in 7 days."
  ),
( "troublesome_bandits", "Hunt Down Troublesome Goblins", qf_random_quest,
  "The {s9} of {s4} asked you to hunt down the troublesome goblins in the vicinity of the town."
  ),
#( "kidnapped_girl", "Ransom Girl from Bandits", qf_random_quest,
#  "Guildmaster of {s4} gave you {reg12} denars to pay the ransom of a girl kidnapped by bandits.\
#  You are to meet the bandits near {s3} and pay them the ransom fee.\
#  After that you are to bring the girl back to {s4}."
#  ),
#( "persuade_lords_to_make_peace", "Make Sure Two Lords Do Not Object to Peace", qf_random_quest,
#  "Guildmaster of {s4} promised you {reg12} denars if you can make sure that\
#  {s12} and {s13} no longer pose a threat to a peace settlement between {s15} and {s14}.\
#  In order to do that, you must either convince them or make sure they fall captive and remain so until a peace agreement is made."
#  ),
( "deal_with_looters", "Deal with Tribal Orcs", qf_random_quest,
  "The Elder of {s4} has asked you to deal with several bands of tribal orcs around {s4}."
  ),
( "deal_with_night_bandits", "Deal with Rogue Goblins", qf_random_quest,
  "The Elder of {s14} has asked you to deal with night goblins at {s14}."
  ),
( "deliver_food", "Supply {s3} with {reg5} Units of food", qf_random_quest,
  "The {s9} of {s3} asked you to bring him {reg5} units of food in 10 days."
  ), 
( "deliver_iron", "Supply {s3} with {reg5} Units of {s6}", qf_random_quest,
  "The {s9} of {s3} asked you to bring him {reg5} units of {s6}."
  ), 
############
# Village Elder quests
############
#Note : This is defined as the first village elder quest in module_constants.py:
#( "deliver_grain", "Bring wheat to {s3}", qf_random_quest,
#  "The elder of the village of {s3} asked you to bring them {reg5} packs of wheat.."
# ), 
#( "deliver_cattle", "Deliver {reg5} Heads of Cattle to {s3}", qf_random_quest,
#  "The elder of the village of {s3} asked you to bring {reg5} heads of cattle."
#  ), 
#( "train_peasants_against_bandits", "Train the Peasants of {s13} Against Bandits.", qf_random_quest,
#  "None"
#  ), 
#Deliver horses, Deliver food, Escort_Caravan, Hunt bandits, Ransom Merchant.
#( "capture_nobleman", "Capture Nobleman",qf_random_quest,
#  "{s1} wanted you to capture an enemy nobleman on his way from {s3} to {s4}. He said the nobleman would leave {s3} in {reg1} days."
#  ),

#Note : This is defined as the last village elder quest in module_constants.py:
#( "eliminate_bandits_infesting_village", "Save the Village of {s7} from Marauding Bandits", qf_random_quest,
#  "A villager from {s7} begged you to save their village from the bandits that took refuge there."
#  ),
#Tutorial quest
#( "destroy_dummies", "Destroy Dummies", qf_show_progression,
#  "Trainer ordered you to destroy 10 dummies in the training camp."
#  ),
# Join Kingdom quest - TLD: not used, but could be reworked
#("join_faction", "Give Oath of Homage to {s1}", qf_random_quest,
#  "Find {s1} and give him your oath of homage."
#  ),
#Rebel against Kingdom quest
#("rebel_against_kingdom", "Help {s13} Claim the Throne of {s14}", qf_random_quest,
# "None"
# ),

### TLD quests
( "tld_introduction", "Deliver message about Mordor orcs to the command", qf_random_quest,
  "None",
  ),
( "treebeard_kill_orcs", "Defeat the tree-chopping orc party", qf_random_quest,
  "Treebeard wants you find and defeat the orcs cutting down trees in Fangorn.",
  ),
( "oath_of_vengeance", "Oath of Vengeance", qf_random_quest,
  "Enraged by the death of {s1}, you have sworn an oath of vengeance upon the forces of {s2}. You must now destroy as many of the armies of {s2} as possible in the coming days. You are keenly aware that your followers have witnessed this oath and you do not wish to become known as an oathbreaker. An orgy of bloodletting must now begin!"
  ),
  ("deliver_gift", "Deliver a {s4} of {s1} from {s2} to {s3}", qf_random_quest,
  "You have requested to deliver a {s4} of {s1} to {s3} from {s2}."
  ),
 # ### TLD traits
# ( "trait_elf_friend", "*TRAIT*_-Elf_Friend", 0, 
  # "You_have_become_highly_esteemed_by_the_Elves_and_they_now_regard_you_as_a_trusted_ally._The_influence_cost_to_recruit_elves_has_been_reduced_and_you_may_now_attempt_to_give_orders_to_elven_armies."
  # ),
# ( "trait_gondor_friend", "*TRAIT*_-Steward's_Blessing", 0, 
  # "You_have_become_highly_esteemed_by_the_Steward_Denethor_and_your_status_has_risen_among_the_men_of_Gondor_as_a_result._The_influence_cost_to_recruit_experienced_Gondorians_has_been_reduced_and_you_may_now_attempt_to_give_orders_to_Gondorian_armies."
  # ),
# ( "trait_rohan_friend", "*TRAIT*_-King's_Man", 0, 
  # "You_have_become_highly_esteemed_by_King_Theoden_of_Rohan_and_your_status_has_risen_among_the_men_of_Rohan_as_a_result._The_influence_cost_to_recruit_experienced_Rohirrim_men_has_been_reduced_and_you_may_now_attempt_to_give_orders_to_the_armies_of_the_Riddermark."
  # ),
# ( "trait_brigand_friend", "*TRAIT*_-Brigand_Champion", 0, 
  # "You_have_become_highly_esteemed_by_the_brigands_of_the_Entwash_as_a_result_of_your_impressive_displays_in_their_arena._You_may_now_recruit_experienced_brigand_men_from_Balan_at_the_brigand_fort."
  # ),
# ( "trait_blessed", "*TRAIT*_-Blessed", 0, 
  # "You_sense_that_you_have_been_blessed_by_powers_from_beyond_the_sea,_and_perhaps_further_away_still._You_do_not_know_why_this_has_happened_or_what_it_may_mean_but_you_are_certain_that_it_is_so."
  # ),
# ( "trait_reverent", "*TRAIT*_-Reverent", 0, 
  # "You_have_aquired_a_reputation_for_reverence_and_wisdom._Men_and_Elves_are_more_likely_to_listen_to_your_counsel."
  # ),
# ( "trait_merciful", "*TRAIT*_-Merciful", 0, 
  # "You_have_aquired_a_reputation_for_merciful_treatment_towards_the_evil_men_who_serve_the_Enemy._Many_of_the_hardened_men_who_serve_you_are_conflicted_by_your_behavior_and_suffer_a_morale_penalty._Among_the_wise,_however,_your_mercy_is_seen_as_evidence_of_high_character_and_you_recieve_an_influence_bonus."
  # ),
# ( "trait_bravery", "*TRAIT*_-Bravery", 0, 
  # "You_have_aquired_a_reputation_for_bravery_in_the_face_of_great_danger._Your_courage_is_spoken_of_in_both_quiet_taverns_and_the_halls_of_the_wise._Your_deeds_inspire_your_men_and_they_recieve_a_weekly_morale_bonus."
  # ),
# ( "trait_oathkeeper", "*TRAIT*_-Oathkeeper", 0, 
  # "You_have_sworn_grim_oaths_and_lived_to_see_them_fulfilled._Subsequently_you_have_aquired_a_reputation_as_a_man_of_his_word._You_receive_a_weekly_influence_bonus."
  # ), 
# ( "trait_oathbreaker", "*TRAIT*_-Oathbreaker", 0, 
  # "You_have_sworn_grim_oaths_and_failed_to_see_them_through_to_their_conclusion._Subsequently_you_have_aquired_a_reputation_as_a_man_whose_passion_outstrips_his_prowess._You_receive_a_weekly_influence_penalty."
  # ),
# ( "trait_orc_pit_champion", "*TRAIT*_-Orc_Pit_Champion", 0, 
  # "You_have_become_renowned_as_a_brutal_warrior_who_was_able_to_survive_the_cruelest_of_the_orcish_fighting_contests._Such_strength_is_both_respected_and_feared_by_your_black_hearted_followers_and_they_now_receive_a_weekly_morale_bonus."
  # ),
# ( "trait_despoiler", "*TRAIT*_-Despoiler", 0, 
  # "You_have_aquired_a_reputation_for_leaving_behind_wanton_destruction_wherever_you_travel._Such_behavior_is_valued_by_the_dark_powers_you_serve_and_your_receive_a_weekly_influence_bonus."
  # ),
# ( "trait_accursed", "*TRAIT*_-Accursed", 0, 
  # "You_sense_that_you_have_drawn_the_ire_of_powers_beyond_the_sea._Your_followers_sense_this_doom_as_well_and_fear_being_around_you._They_receive_a_weekly_morale_penalty."
  # ),
# ( "trait_stealthy", "*TRAIT*_-Stealthy", 0, 
  # "You_have_developed_uncanny_skill_in_the_art_of_stealthy_infiltration._You_receive_a_bonus_to_your_stealth_rating_when_undertaking_such_missions."
  # ),
# ( "trait_berserker", "*TRAIT*_-Berserker", 0, 
  # "After_many_battles_where_you_eschewed_the_use_of_armor_your_ferocious_will_has_become_like_iron._In_battles_where_you_are_gravely_wounded_you_will_receive_an_occasional_health_bonus._This_will_not_restore_you_to_full_strength_but_may_keep_you_going_long_after_others_would_have_succumbed_to_their_wounds."
  # ),
# ( "trait_infantry_captain", "*TRAIT*_-Infantry_Captain", 0, 
  # "You_have_developed_uncanny_skill_in_the_command_of_infantry_troops._Due_to_rigorous_and_specialized_training_such_troops_will_receive_a_small_health_boost,_once_per_battle,_upon_being_wounded._You_will_also_receive_a_small_bonus_during_the_melee_phase_of_abstracted_battles."
  # ),
# ( "trait_archer_captain", "*TRAIT*_-Archery_Captain", 0, 
  # "You_have_developed_uncanny_skill_in_the_command_of_missile_troops._Due_to_rigorous_and_specialized_training_such_troops_will_receive_a_small_health_boost,_once_per_battle,_upon_being_wounded._You_will_also_receive_a_small_bonus_during_the_missile_phase_of_abstracted_battles."
  # ),
# ( "trait_cavalry_captain", "*TRAIT*_-Cavalry_Captain", 0, 
  # "You_have_developed_uncanny_skill_in_the_command_of_mounted_troops._Due_to_rigorous_and_specialized_training_such_troops_will_receive_a_small_health_boost,_once_per_battle,_upon_being_wounded._You_will_also_receive_a_small_bonus_during_the_shock_phase_of_abstracted_battles."
  # ),
# ( "trait_command_voice", "*TRAIT*_-Command_Voice", 0, 
  # "Your_experience_with_commanding_men_in_the_field_has_lent_you_an_air_of_authority._The_cost_to_give_orders_to_armies_in_the_field_has_been_reduced."
  # ),
# ( "trait_foe_hammer", "*TRAIT*_-Foe_Hammer", 0, 
  # "Having_slain_many_of_the_great_captains_of_the_enemy_you_find_that_you_have_earned_a_reputation_as_a_fearsome_warrior._Troops_under_your_command_now_receive_a_weekly_morale_bonus._Your_experiences_have_also_honed_your_skill_in_battle."
  # ),
# ( "trait_battle_scarred", "*TRAIT*_-Battle_Scars", 0, 
  # "You_have_suffered_horrific_wounds_during_your_many_campaigns_yet_you_still_live_to_tell_the_tale._Your_scarred_and_knotted_flesh_now_conspires_with_hard_experience_to_increase_your_resistance_to_injury._While_others_may_find_your_appearance_somewhat_shocking_your_followers_consider_it_an_affirmation_of_your_battle_experience._They_subsequently_receive_a_weekly_morale_bonus."
  # ),
# ( "trait_fell_beast", "*TRAIT*_-Fell_Beast", 0, 
  # "Your_hide_is_riven_with_the_knotted_scars_of_countless_battles_and_your_evil_will_is_likewise_hard_and_unyielding._Even_by_the_standards_of_orc,_uruk_and_troll-kind_you_are_judged_a_fell_and_dangerous_beast._Those_who_serve_you_cry_your_name_in_joy_when_you_take_to_the_field._You_are_an_avatar_of_war_itself_and_there_is_little_you_fear."
  # ),
# ### TLD end traits

  ("quests_end", "Quests End", 0, "."),
]

