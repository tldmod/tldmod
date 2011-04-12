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
 ("escort_lady", "Escort the messenger to {s14}", qf_random_quest,
  "None"
  ),
## ("rescue_lady_under_siege", "Rescue {s3} from {s4}", qf_random_quest,
##  "{s1} asked you to rescue his {s7} {s3} from {s4} and return her back to him."
##  ),
## ("deliver_message_to_lover", "Deliver Message to {s3}", qf_random_quest,
##  "{s1} asked you to take a message to his lover {s3} at {s4}."
##  ),
## ("bring_prisoners_to_enemy", "Bring Prisoners to {s4}", qf_random_quest,
##  "{s1} asked you to bring {reg1} {s3} as prisoners to the guards at {s4}."
##  ),
## ("bring_reinforcements_to_siege", "Bring Reinforcements to the Siege of {s5}", qf_random_quest,
##  "{s1} asked you to bring {reg1} {s3} to {s4} at the siege of {s5}."
##  ),
## ("deliver_supply_to_center_under_siege", "Deliver Supplies to {s5}", qf_random_quest,
##  "TODO: Take {reg1} cartloads of supplies from constable {s3} and deliver them to constable {s4} at {s5}."
##  ),

 # ("deal_with_bandits_at_lords_village", "Save the Village of {s15} from Marauding Bandits", qf_random_quest,
  # "{s13} asked you to deal with the bandits who took refuge in his village of {s15} and then report back to him."
  # ),
 # ("collect_taxes", "Collect taxes from {s3}", qf_random_quest,
  # "{s9} asked you to collect taxes from {s3}. He offered to leave you one-fifth of all the money you collect there."
  # ),
 ("hunt_down_fugitive", "Hunt down {s4}", qf_random_quest,
  "{s9} asked you to hunt down the fugitive named {s4}. He is currently believed to be at {s3}."
  ),
  
## ("capture_messenger", "Capture {s3}", qf_random_quest,
##  "{s1} asked you to capture a {s3} and bring him back."
##  ),
## ("bring_back_deserters", "Bring {reg1} {s3}", qf_random_quest,
##  "{s1} asked you to bring {reg1} {s3}."
##  ),

 # ("kill_local_merchant", "Assassinate Local Merchant at {s3}", qf_random_quest,
  # "{s9} asked you to assassinate a local merchant at {s3}."
  # ),
 ("bring_back_runaway_serfs", "Bring Back Runaway Serfs", qf_random_quest,
  "{s9} asked you to bring back the three groups of runaway serfs back to {s2}. He said all three groups must be running away in the direction of {s3}."
  ),
 ("follow_spy", "Follow the Spy to Meeting", qf_random_quest,
  "{s11} asked you to follow the spy that will leave {s12}. You must be careful not to be seen by the spy during his travel, or else he may get suspicious and turn back. Once the spy meets with his accomplice, you are to ambush and capture them and bring them both back to {s11}."
  ),
 ("capture_enemy_hero", "Capture a Lord from {s13}", qf_random_quest,
  "TODO: {s11} asked you to capture a lord from {s13}."
  ),
 ("lend_companion", "Lend Your Companion {s3} to {s9}", qf_random_quest,
  "{s9} asked you to lend your companion {s3} to him for a week."
  ),
 # ("collect_debt", "Collect the debt {s3} owes to {s9}", qf_random_quest,
  # "{s9} asked you to collect the debt of {reg4} denars {s3} owes to him."
  # ),
## ("capture_conspirators", "Capture Conspirators", qf_random_quest,
##  "TODO: {s1} asked you to capture all troops in {reg1} conspirator parties that plan to rebel against him and join {s3}."
##  ),
## ("defend_nobles_against_peasants", "Defend Nobles Against Peasants", qf_random_quest,
##  "TODO: {s1} asked you to defend {reg1} noble parties against peasants."
##  ),
 # ("incriminate_loyal_commander", "Incriminate the Loyal Commander of {s13}, {s16}", qf_random_quest,
  # "None"
  # ),
 # ("raid_caravan_to_start_war", "Raid {reg13} Caravans of {s13}", qf_random_quest,
  # "None"
  # ),
 # ("meet_spy_in_enemy_town", "Meet Spy in {s13}", qf_random_quest,
  # "None"
  # ),
 ("capture_prisoners", "Bring {reg1} {s3} Prisoners", qf_random_quest,
  "{s9} wanted you to bring him {reg1} {s3} as prisoners."
  ),
  
# TLD BEGIN   lord's quests  (mtarini)
 
 ("investigate_fangorn", "Investigate Fangorn", qf_random_quest,
  "{s9} asked you to find out what is going on in the Fangorn forest, and to report back."),

 ("capture_troll", "Capture a Troll", qf_random_quest,
  "{s9} asked you to bring back a savage troll for use in his army."),

 ("find_lost_spears", "Find the lost spears of king Bladorthin", qf_random_quest,
  "{s9} asked you to find the lost spears dwarves once made for king Bladorthin. You have to ask the dwarves permission to search for the spears in the depths of the Lonely Mountain."),

# TLD END lord's quests 

#TLD lord missions begin  
 ("rescue_prisoners", "Rescue {reg1} Prisoners", qf_random_quest,
  "{s9} wanted you to rescue {reg1} prisoners."
  ),
#TLD lord missions end  

## ("hunt_down_raiders", "Hunt Down Raiders",qf_random_quest,
##  "{s1} asked you to hunt down and punish the raiders that attacked a village near {s3} before they reach the safety of their base at {s4}."
##  ),

##################
# Enemy Kingdom Lord quests
##################
# Note : This is defined as the first enemy lord quest in module_constants.py:
 # ("lend_surgeon", "Lend Your Surgeon {s3} to {s1}", qf_random_quest,
  # "Lend your experienced surgeon {s3} to {s1}."
  # ),

##################
# Kingdom Army quests
##################
# Note : This is defined as lord quests end in module_constants.py:
 ("follow_army", "Follow {s9}'s Army", qf_random_quest,
  "None"
  ),
 ("report_to_army", "Report to {s13}, the Marshall", qf_random_quest,
  "None"
  ),
# Note : This is defined as the first army quest in module_constants.py:
 ("deliver_cattle_to_army", "Deliver {reg3} Heads of Cattle to {s13}", qf_random_quest,
  "None"
  ),
 ("join_siege_with_army", "Join the Siege of {s14}", qf_random_quest,
  "None"
  ),
 ("scout_waypoints", "Scout {s13}, {s14} and {s15}", qf_random_quest,
  "None"
  ),


##################
# Kingdom Lady quests
##################
# Note : This is defined as the first kingdom lady quest in module_constants.py:
 # ("rescue_lord_by_replace", "Rescue {s13} from {s14}", qf_random_quest,
  # "None"
  # ),
 # ("deliver_message_to_prisoner_lord", "Deliver Message to {s13} at {s14}", qf_random_quest,
  # "None"
  # ),
  # ("duel_for_lady", "Challenge {s13} to a Trial of Arms", qf_random_quest,
  # "None"
  # ),

##################
# Mayor quests
##################
# Note : This is defined as the first mayor quest in module_constants.py: 
 ("move_cattle_herd", "Move Cattle Herd to {s13}", qf_random_quest,
  "Guildmaster of {s10} asked you to move a cattle herd to {s13}."
  ),
 ("escort_merchant_caravan", "Escort Supply Caravan to {s8}", qf_random_quest,
  "Escort the supply caravan to the town of {s8}."
  ),
 ("deliver_wine", "Deliver {reg5} Units of {s6} to {s4}", qf_random_quest,
  "{s9} of {s3} asked you to deliver {reg5} units of {s6} to the tavern in {s4} in 7 days."
  ),
 ("troublesome_bandits", "Hunt Down Troublesome Bandits", qf_random_quest,
  "{s9} of {s4} asked you to hunt down the troublesome bandits in the vicinity of the town."
  ),
 # ("kidnapped_girl", "Ransom Girl from Bandits", qf_random_quest,
  # "Guildmaster of {s4} gave you {reg12} denars to pay the ransom of a girl kidnapped by bandits.\
 # You are to meet the bandits near {s3} and pay them the ransom fee.\
 # After that you are to bring the girl back to {s4}."
  # ),
 # ("persuade_lords_to_make_peace", "Make Sure Two Lords Do Not Object to Peace", qf_random_quest,
  # "Guildmaster of {s4} promised you {reg12} denars if you can make sure that\
 # {s12} and {s13} no longer pose a threat to a peace settlement between {s15} and {s14}.\
 # In order to do that, you must either convince them or make sure they fall captive and remain so until a peace agreement is made."
  # ),
 ("deal_with_looters", "Deal with Looters", qf_random_quest,
  "The Guildmaster of {s4} has asked you to deal with several bands of looters around {s4}, and bring back any goods you recover."
  ),
 ("deal_with_night_bandits", "Deal with Night Bandits", qf_random_quest,
  "TODO: The Guildmaster of {s14} has asked you to deal with night bandits at {s14}."
  ),

############
# Village Elder quests
############
# Note : This is defined as the first village elder quest in module_constants.py:
 # ("deliver_grain", "Bring wheat to {s3}", qf_random_quest,
  # "The elder of the village of {s3} asked you to bring them {reg5} packs of wheat.."
  # ), 
 # ("deliver_cattle", "Deliver {reg5} Heads of Cattle to {s3}", qf_random_quest,
  # "The elder of the village of {s3} asked you to bring {reg5} heads of cattle."
  # ), 
 # ("train_peasants_against_bandits", "Train the Peasants of {s13} Against Bandits.", qf_random_quest,
  # "None"
  # ), 
# Deliver horses, Deliver food, Escort_Caravan, Hunt bandits, Ransom Merchant.
## ("capture_nobleman", "Capture Nobleman",qf_random_quest,
##  "{s1} wanted you to capture an enemy nobleman on his way from {s3} to {s4}. He said the nobleman would leave {s3} in {reg1} days."
##  ),

# Bandit quests: Capture rich merchant, capture banker, kill manhunters?..

# Note : This is defined as the last village elder quest in module_constants.py:
 # ("eliminate_bandits_infesting_village", "Save the Village of {s7} from Marauding Bandits", qf_random_quest,
  # "A villager from {s7} begged you to save their village from the bandits that took refuge there."
  # ),


 # Tutorial quest
## ("destroy_dummies", "Destroy Dummies", qf_show_progression,
##  "Trainer ordered you to destroy 10 dummies in the training camp."
##     ),

 # Join Kingdom quest - TLD: not used, but could be reworked
 ("join_faction", "Give Oath of Homage to {s1}", qf_random_quest,
  "Find {s1} and give him your oath of homage."
  ),

 # Rebel against Kingdom quest
 # ("rebel_against_kingdom", "Help {s13} Claim the Throne of {s14}", qf_random_quest,
  # "None"
  # ),

### TLD quests
  ("tld_introduction","Deliver message about Mordor orcs to the command",qf_random_quest,
  "None",
  ),

 ("quests_end", "Quests End", 0, "."),
]

