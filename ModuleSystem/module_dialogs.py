from header_common import *
from header_dialogs import *
from header_operations import *
from header_parties import *
from header_item_modifiers import *
from header_skills import *
from header_triggers import *
from ID_troops import *
from ID_party_templates import *

from module_constants import *


####################################################################################################################
# During a dialog, the dialog lines are scanned from top to bottom.
# If the dialog-line is spoken by the player, all the matching lines are displayed for the player to pick from.
# If the dialog-line is spoken by another, the first (top-most) matching line is selected.
#
#  Each dialog line contains the following fields:
# 1) Dialogue partner: This should match the person player is talking to.
#    Usually this is a troop-id.
#    You can also use a party-template-id by appending '|party_tpl' to this field.
#    Use the constant 'anyone' if you'd like the line to match anybody.
#    Appending '|plyr' to this field means that the actual line is spoken by the player
#    Appending '|other(troop_id)' means that this line is spoken by a third person on the scene.
#       (You must make sure that this third person is present on the scene)
#
# 2) Starting dialog-state:
#    During a dialog there's always an active Dialog-state.
#    A dialog-line's starting dialog state must be the same as the active dialog state, for the line to be a possible candidate.
#    If the dialog is started by meeting a party on the map, initially, the active dialog state is "start"
#    If the dialog is started by speaking to an NPC in a town, initially, the active dialog state is "start"
#    If the dialog is started by helping a party defeat another party, initially, the active dialog state is "party_relieved"
#    If the dialog is started by liberating a prisoner, initially, the active dialog state is "prisoner_liberated"
#    If the dialog is started by defeating a party led by a hero, initially, the active dialog state is "enemy_defeated"
#    If the dialog is started by a trigger, initially, the active dialog state is "event_triggered"
# 3) Conditions block (list): This must be a valid operation block. See header_operations.py for reference.  
# 4) Dialog Text (string):
# 5) Ending dialog-state:
#    If a dialog line is picked, the active dialog-state will become the picked line's ending dialog-state.
# 6) Consequences block (list): This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

dialogs = [



 

  [anyone ,"start", [(store_conversation_troop, "$g_talk_troop"),
                     (store_conversation_agent, "$g_talk_agent"),
                     (store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),
#                     (troop_get_slot, "$g_talk_troop_relation", "$g_talk_troop", slot_troop_player_relation),
                     (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
                     (assign, "$g_talk_troop_relation", reg0),

                     (try_begin),
                       (this_or_next|is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
                       (is_between, "$g_talk_troop", mayors_begin, mayors_end),
                       (party_get_slot, "$g_talk_troop_relation", "$current_town", slot_center_player_relation),
                     (try_end),
                     (store_relation, "$g_talk_troop_faction_relation", "$g_talk_troop_faction", "fac_player_faction"),
                     
                     (assign, "$g_talk_troop_party", "$g_encountered_party"),
                     (try_begin),
                       (troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1),
                       (troop_get_slot, "$g_talk_troop_party", "$g_talk_troop", slot_troop_leaded_party),
                     (try_end),
                     
#                     (assign, "$g_talk_troop_kingdom_relation", 0),
#                     (try_begin),
#                       (gt, "$players_kingdom", 0),
#                       (store_relation, "$g_talk_troop_kingdom_relation", "$g_talk_troop_faction", "$players_kingdom"),
#                     (try_end),
                     
                     (store_current_hours, "$g_current_hours"),
                     (troop_get_slot, "$g_talk_troop_last_talk_time", "$g_talk_troop", slot_troop_last_talk_time),
                     (troop_set_slot, "$g_talk_troop", slot_troop_last_talk_time, "$g_current_hours"),
                     (store_sub, "$g_time_since_last_talk","$g_current_hours","$g_talk_troop_last_talk_time"),
                     (troop_get_slot, "$g_talk_troop_met", "$g_talk_troop", slot_troop_met),
                     (troop_set_slot, "$g_talk_troop", slot_troop_met, 1),

                     (try_begin),
#                       (this_or_next|eq, "$talk_context", tc_party_encounter),
#                       (this_or_next|eq, "$talk_context", tc_castle_commander),
                       (call_script, "script_party_calculate_strength", "p_collective_enemy",0),
                       (assign, "$g_enemy_strength", reg0),
                       (call_script, "script_party_calculate_strength", "p_main_party",0),
                       (assign, "$g_ally_strength", reg0),
                       (store_mul, "$g_strength_ratio", "$g_ally_strength", 100),
                       (val_div, "$g_strength_ratio", "$g_enemy_strength"),
                     (try_end),

                     (assign, "$g_comment_found", 0),
                     
                     (try_begin),
                       (troop_is_hero, "$g_talk_troop"),
                       (talk_info_show, 1),
                       (call_script, "script_setup_talk_info"),
                     (try_end),

                     (try_begin),
                       (is_between, "$g_talk_troop", kingdom_heroes_begin, kingdom_heroes_end),
                       (call_script, "script_get_relevant_comment_to_s42"),
                       (assign, "$g_comment_found", reg0),
                     (try_end),

                     (troop_get_type, reg65, "$g_talk_troop"),
                     (try_begin),
                       (faction_slot_eq,"$g_talk_troop_faction",slot_faction_leader,"$g_talk_troop"),
                       (str_store_string,s64,"@{reg65?my Lady:my Lord}"), #bug fix
                       (str_store_string,s65,"@{reg65?my Lady:my Lord}"),
                       (str_store_string,s66,"@{reg65?My Lady:My Lord}"),
                       (str_store_string,s67,"@{reg65?My Lady:My Lord}"), #bug fix
                     (else_try),
                       (str_store_string,s64,"@{reg65?madame:sir}"), #bug fix
                       (str_store_string,s65,"@{reg65?madame:sir}"),
                       (str_store_string,s66,"@{reg65?Madame:Sir}"),
                       (str_store_string,s67,"@{reg65?Madame:Sir}"), #bug fix
                     (try_end),

                     (eq, 1, 0)],
   "Warning: This line is never displayed. It is just for storing conversation variables.", "close_window", []],

  [anyone ,"member_chat", [(store_conversation_troop, "$g_talk_troop"),
                           (try_begin),
                               (is_between, "$g_talk_troop", companions_begin, companions_end),
                               (talk_info_show, 1),
                               (call_script, "script_setup_talk_info_companions"),
                           (try_end),
                           (troop_get_type, reg65, "$g_talk_troop"),
                           
                     (troop_get_type, reg65, "$g_talk_troop"),
                     (try_begin),
                       (faction_slot_eq,"$g_talk_troop_faction",slot_faction_leader,"$g_talk_troop"),
                       (str_store_string,s64,"@{reg65?my Lady:my Lord}"), #bug fix
                       (str_store_string,s65,"@{reg65?my Lady:my Lord}"),
                       (str_store_string,s66,"@{reg65?My Lady:My Lord}"),
                     (else_try),
                       (str_store_string,s64,"@{reg65?madame:sir}"), #bug fix
                       (str_store_string,s65,"@{reg65?madame:sir}"),
                       (str_store_string,s66,"@{reg65?Madame:Sir}"),
                     (try_end),

                     (eq, 1, 0)],  
   "Warning: This line is never displayed. It is just for storing conversation variables.", "close_window", []],

  [anyone ,"event_triggered", [(store_conversation_troop, "$g_talk_troop"),
                           (try_begin),
                               (is_between, "$g_talk_troop", companions_begin, companions_end),
                               (talk_info_show, 1),
                               (call_script, "script_setup_talk_info_companions"),
                           (try_end),
                               
                     (troop_get_type, reg65, "$g_talk_troop"),
                     (try_begin),
                       (faction_slot_eq,"$g_talk_troop_faction",slot_faction_leader,"$g_talk_troop"),
                       (str_store_string,s64,"@{reg65?my Lady:my Lord}"), #bug fix
                       (str_store_string,s65,"@{reg65?my Lady:my Lord}"),
                       (str_store_string,s66,"@{reg65?My Lady:My Lord}"),
                     (else_try),
                       (str_store_string,s64,"@{reg65?madame:sir}"), #bug fix
                       (str_store_string,s65,"@{reg65?madame:sir}"),
                       (str_store_string,s66,"@{reg65?Madame:Sir}"),
                     (try_end),


                     (eq, 1, 0)],  
   "Warning: This line is never displayed. It is just for storing conversation variables.", "close_window", []],

   
   #[trp_antler, "start", [], "Hello. Can you find the mythical Salt Mine?", "antler1",[]],
   #[trp_antler|trp_player, "antler1",[],"HOPEFULLY!.", "close_window",[
    #  (enable_party, "p_salt_mine")]],
   #mtarini: commented abovr
   [trp_ramun_the_slave_trader, "start", [], "Hello. Can you find the mythical Salt Mine?", "antler1",[]],
   [trp_ramun_the_slave_trader|trp_player, "antler1",[],"HOPEFULLY!.", "close_window",[
      (enable_party, "p_salt_mine")]],
   

  [trp_ramun_the_slave_trader, "start", [
   (troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),
   ], "Good day to you, {young man/lassie}.", "ramun_introduce_1",[]],
  [trp_ramun_the_slave_trader|plyr, "ramun_introduce_1", [], "Forgive me, you look like a trader, but I see none of your merchandise.", "ramun_introduce_2",[
   (troop_set_slot, "$g_talk_troop", slot_troop_met_previously, 1),
  ]],
  [trp_ramun_the_slave_trader|plyr, "ramun_introduce_1", [], "Never mind.", "close_window",[]],
  [trp_ramun_the_slave_trader, "ramun_introduce_2", [], "A trader? Oh, aye, I certainly am that.\
 My merchandise is a bit different from most, however. It has to be fed and watered twice a day and tries to run away if I turn my back.", "ramun_introduce_3",[]],
  [trp_ramun_the_slave_trader|plyr, "ramun_introduce_3", [], "Livestock?", "ramun_introduce_4",[]],
  [trp_ramun_the_slave_trader, "ramun_introduce_4", [], "Close enough. I like to call myself the man who keeps every boat on this ocean moving.\
 Boats are driven by oars, you see, and oars need men to pull them or they stop. That's where I come in.", "ramun_introduce_5",[]],
  [trp_ramun_the_slave_trader|plyr, "ramun_introduce_5", [], "Galley slaves.", "ramun_introduce_6",[]],
  [trp_ramun_the_slave_trader, "ramun_introduce_6", [], "Now you're catching on! A trading port like this couldn't survive without them.\
 The ships lose a few hands on every voyage, so there's always a high demand. The captains come to me and they pay well.", "ramun_introduce_7",[]],
  [trp_ramun_the_slave_trader|plyr, "ramun_introduce_7", [], "Where do the slaves come from?", "ramun_introduce_8",[]],
  [trp_ramun_the_slave_trader, "ramun_introduce_8", [], "Mostly I deal in convicted criminals bought from the authorities.\
 Others are prisoners of war from various nations, brought to me because I offer the best prices.\
 However, on occasion I'll buy from privateers and other . . . 'individuals'. You can't be picky about your suppliers in this line of work.\
 You wouldn't happen to have any prisoners with you, would you?", "ramun_introduce_9",[]],
  [trp_ramun_the_slave_trader|plyr, "ramun_introduce_9", [], "Me? ", "ramun_introduce_10",[]],
  [trp_ramun_the_slave_trader, "ramun_introduce_10", [], "Why not? If you intend to set foot outside this town,\
 you're going to cross swords with someone sooner or later. And, God willing, you'll come out on top.\
 Why not make some extra money off the whole thing? Take them alive, bring them back to me, and I'll pay you fifty denars for each head.\
 Don't much care who they are or where they come from.", "ramun_introduce_11",[]],
  [trp_ramun_the_slave_trader|plyr, "ramun_introduce_11", [], "Hmm. I'll think about it.", "ramun_introduce_12",[]],
  [trp_ramun_the_slave_trader, "ramun_introduce_12", [], "Do think about it!\
 There's a lot of silver to be made, no mistake. More than enough for the both of us.", "close_window",[]],

  [trp_ramun_the_slave_trader,"start", [], "Hello, {playername}.", "ramun_talk",[]],
  [trp_ramun_the_slave_trader,"ramun_pre_talk", [], "Anything else?", "ramun_talk",[]],

  [trp_ramun_the_slave_trader|plyr,"ramun_talk",
   [[store_num_regular_prisoners,reg(0)],[ge,reg(0),1]],
   "I've brought you some prisoners, Ramun. Would you like a look?", "ramun_sell_prisoners",[]],
  [trp_ramun_the_slave_trader,"ramun_sell_prisoners", [],
  "Let me see what you have...", "ramun_sell_prisoners_2",
   [[change_screen_trade_prisoners]]],
  [trp_ramun_the_slave_trader, "ramun_sell_prisoners_2", [], "A pleasure doing business with you.", "close_window",[]],

  [trp_ramun_the_slave_trader|plyr,"ramun_talk", [(neg|troop_slot_ge,"$g_talk_troop",slot_troop_met_previously,1)], "How do I take somebody as prisoner?", "ramun_ask_about_capturing",[]],
  [trp_ramun_the_slave_trader|plyr,"ramun_talk", [(troop_slot_ge,"$g_talk_troop", slot_troop_met_previously, 1)], "Can you tell me again about capturing prisoners?", "ramun_ask_about_capturing",[(troop_set_slot,"$g_talk_troop", slot_troop_met_previously, 2)]],

  [trp_ramun_the_slave_trader,"ramun_ask_about_capturing", [(neg|troop_slot_ge,"$g_talk_troop",slot_troop_met_previously,1)],
 "You're new to this, aren't you? Let me explain it in simple terms.\
 The basic rule of taking someone prisoner is knocking him down with a blunt weapon, like a mace or a club,\
 rather than cutting him open with a sword. That way he goes to sleep for a little while rather than bleeding to death, you see?\
 I'm assuming you have a blunt weapon with you . . .", "ramun_have_blunt_weapon",[]],
  [trp_ramun_the_slave_trader|plyr,"ramun_have_blunt_weapon", [],
 "Of course.", "ramun_have_blunt_weapon_yes",[]],
  [trp_ramun_the_slave_trader|plyr,"ramun_have_blunt_weapon", [],
 "As a matter of fact, I don't.", "ramun_have_blunt_weapon_no",[]],
  [trp_ramun_the_slave_trader,"ramun_have_blunt_weapon_yes", [],
 "Good. Then all you need to do is beat the bugger down with your weapon, and when the fighting's over you clap him in irons.\
 It's a bit different for nobles and such, they tend to be protected enough that it won't matter what kind of weapon you use,\
 but your average rabble-rouser will bleed like a stuck pig if you get him with something sharp. I don't have many requirements in my merchandise,\
 but I do insist they be breathing when I buy them.", "ramun_ask_about_capturing_2",[]],
  [trp_ramun_the_slave_trader,"ramun_have_blunt_weapon_no", [],
 "No? Heh, well, this must be your lucky day. I've got an old club lying around that I was going to throw away.\
 It a bit battered, but still good enough bash someone until he stops moving.\
 Here, have it.","ramun_have_blunt_weapon_no_2",[(troop_add_item, "trp_player","itm_wood_club",imod_cracked)]],
  [trp_ramun_the_slave_trader|plyr,"ramun_have_blunt_weapon_no_2", [],
 "Thanks, Ramun. Perhaps I may try my hand at it.", "ramun_have_blunt_weapon_yes",[]],
  [trp_ramun_the_slave_trader,"ramun_ask_about_capturing", [],
 "Alright, I'll try and expain it again in simple terms. The basic rule of taking someone prisoner is knocking him down with a blunt weapon, like a mace or a club,\
 rather than cutting him open with a sword. That way he goes to sleep for a little while rather than bleeding to death, you see?\
 It's a bit different for nobles and such, they tend to be protected enough that it won't matter what kind of weapon you use,\
 but your average rabble-rouser will bleed like a stuck pig if you get him with something sharp.", "ramun_ask_about_capturing_2",[]],
  [trp_ramun_the_slave_trader|plyr,"ramun_ask_about_capturing_2", [], "Alright, I think I understand. Anything else?", "ramun_ask_about_capturing_3",[]],
  [trp_ramun_the_slave_trader,"ramun_ask_about_capturing_3", [],
 "Well, it's not as simple as all that. Blunt weapons don't do as much damage as sharp ones, so they won't bring your enemies down as quickly.\
 And trust me, given the chance, most of the scum you run across would just as soon kill you as look at you, so don't expect any courtesy when you pull out a club instead of a sword.\
 Moreover, having to drag prisoners to and fro will slow down your party, which is why some people simply set their prisoners free after the fighting's done.\
 It's madness. How could anyone turn down all that silver, eh?", "ramun_ask_about_capturing_4",[]],
  [trp_ramun_the_slave_trader|plyr,"ramun_ask_about_capturing_4", [],
 "Is that everything?", "ramun_ask_about_capturing_5",[]],
  [trp_ramun_the_slave_trader,"ramun_ask_about_capturing_5", [],
 "Just one final thing. Managing prisoners safely is not an easy thing to do, you could call it a skill in itself.\
 If you want to capture a lot of prisoners, you should try and learn the tricks of it yourself,\
 or you won't be able to hang on to a single man you catch.", "ramun_ask_about_capturing_7",[]],
  [trp_ramun_the_slave_trader|plyr,"ramun_ask_about_capturing_7", [],
 "Thanks, I'll keep it in mind.", "ramun_pre_talk",[]],

  [trp_ramun_the_slave_trader|plyr,"ramun_talk", [], "I'd better be going.", "ramun_leave",[]],
  [trp_ramun_the_slave_trader,"ramun_leave", [], "Remember, any prisoners you've got, bring them to me. I'll pay you good silver for every one.", "close_window",[]],


##  [trp_tutorial_trainer,"start", [(eq, "$tutorial_quest_award_taken", 1),], "I think you have trained enough. Perhaps you should go to Zendar for the next step of your adventure.", "close_window",[]],
##  [trp_tutorial_trainer,"start", [(store_character_level, ":player_level", "trp_player"),(gt, ":player_level", 1)], "I think you have trained enough. Perhaps you should go to Zendar for the next step of your adventure.", "close_window",[]],
##  [trp_tutorial_trainer,"start", [(eq, "$tutorial_quest_taken", 0),], "Greetings stranger. What's your name?", "tutorial1_1",[]],
##  [trp_tutorial_trainer|plyr, "tutorial1_1", [], "Greetings sir, it's {playername}.", "tutorial1_2", []],
##  [trp_tutorial_trainer, "tutorial1_2", [], "Well {playername}, this place you see is the training ground. Locals come here to practice their combat skills. Since you are here you may have a go as well.", "tutorial1_3", []],
##  [trp_tutorial_trainer|plyr, "tutorial1_3", [], "I'd like that very much sir. Thank you.", "tutorial1_4", []],
##  [trp_tutorial_trainer, "tutorial1_4", [], "You will learn the basics of weapons and riding a horse here.\
##  First you'll begin with melee weapons. Then you'll enter an archery range to test your skills. And finally you'll see a horse waiting for you.\
##  I advise you to train in all these 3 areas. But you can skip some of them, it's up to you.", "tutorial1_6", []],
##  [trp_tutorial_trainer, "tutorial1_6", [], "Tell you what, if you destroy at least 10 dummies while training, I will give you my old knife as a reward. It's a little rusty but it's a good blade.", "tutorial1_7", []],
##  [trp_tutorial_trainer|plyr, "tutorial1_7", [], "Sounds nice, I'm ready for training.", "tutorial1_9", []],
##  [trp_tutorial_trainer, "tutorial1_9", [], "Good. Return to me when you have earned your reward.", "close_window", [(eq, "$tutorial_quest_taken", 0),
##                                                                                                                     (str_store_troop_name, 1, "trp_tutorial_trainer"),
##                                                                                                                     (str_store_party_name, 2, "p_training_ground"),
##                                                                                                                     (setup_quest_giver, "qst_destroy_dummies", "str_given_by_s1_at_s2"),
##                                                                                                                     (str_store_string, s2, "@Trainer ordered you to destroy 10 dummies in the training camp."),
##                                                                                                                     (call_script, "script_start_quest", "qst_destroy_dummies", "$g_talk_troop"),
##                                                                                                                     (assign, "$tutorial_quest_taken", 1)]],
##
##  [trp_tutorial_trainer,"start", [(eq, "$tutorial_quest_taken", 1),
##                                  (eq, "$tutorial_quest_succeeded", 1),], "Well done {playername}. Now you earned this knife. There you go.", "tutorial2_1",[]],
##  [trp_tutorial_trainer|plyr, "tutorial2_1", [], "Thank you master.", "close_window", [(call_script, "script_end_quest", "qst_destroy_dummies"),(assign, "$tutorial_quest_award_taken", 1),(add_xp_to_troop, 100, "trp_player"),(troop_add_item, "trp_player","itm_knife",imod_chipped),]],
##
##  [trp_tutorial_trainer,"start", [(eq, "$tutorial_quest_taken", 1),
##                                  (eq, "$tutorial_quest_succeeded", 1),], "Greetings {playername}. Feel free to train with the targets.", "tutorial2_1",[]],
##
##  [trp_tutorial_trainer,"start", [(eq, "$tutorial_quest_taken", 1),
##                                  (eq, "$tutorial_quest_succeeded", 0),], "I don't see 10 dummies on the floor from here. You haven't earned your reward yet.", "tutorial3_1",[]],
##  [trp_tutorial_trainer|plyr, "tutorial3_1", [], "Alright alright, I was just tired and wanted to talk to you while resting.", "tutorial3_2", []],
##  [trp_tutorial_trainer, "tutorial3_2", [], "Less talk, more work.", "close_window", []],


##  [party_tpl|pt_peasant,"start", [(eq,"$talk_context",tc_party_encounter)], "Greetings traveller.", "peasant_talk_1",[(play_sound,"snd_encounter_farmers")]],
##  [party_tpl|pt_peasant|plyr,"peasant_talk_1", [[eq,"$quest_accepted_zendar_looters"]], "Greetings to you too.", "close_window",[(assign, "$g_leave_encounter",1)]],
##  [party_tpl|pt_peasant|plyr,"peasant_talk_1", [[neq,"$quest_accepted_zendar_looters"],[eq,"$peasant_misunderstanding_said"]], "I have been charged with hunting down outlaws in this area...", "peasant_talk_2",[[assign,"$peasant_misunderstanding_said",1]]],
##  [party_tpl|pt_peasant|plyr,"peasant_talk_1", [[neq,"$quest_accepted_zendar_looters"],[neq,"$peasant_misunderstanding_said"]], "Greetings. I am hunting outlaws. Have you seen any around here?", "peasant_talk_2b",[]],
##  [party_tpl|pt_peasant,"peasant_talk_2", [], "I swear to God {sir/madam}. I am not an outlaw... I am just a simple peasant. I am taking my goods to the market, see.", "peasant_talk_3",[]],
##  [party_tpl|pt_peasant|plyr,"peasant_talk_3", [], "I was just going to ask if you saw any outlaws around here.", "peasant_talk_4",[]],
##  [party_tpl|pt_peasant,"peasant_talk_4", [], "Oh... phew... yes, outlaws are everywhere. They are making life miserable for us.\
## I pray to God you will kill them all.", "close_window",[(assign, "$g_leave_encounter",1)]],
##  [party_tpl|pt_peasant,"peasant_talk_2b", [], "Outlaws? They are everywhere. They are making life miserable for us.\
## I pray to God you will kill them all.", "close_window",[(assign, "$g_leave_encounter",1)]],

  [party_tpl|pt_manhunters,"start", [(eq,"$talk_context",tc_party_encounter)], "Hey, you there! You seen any outlaws around here?", "manhunter_talk_b",[]],
  [party_tpl|pt_manhunters|plyr,"manhunter_talk_b", [], "Yes, they went this way about an hour ago.", "manhunter_talk_b1",[]],
  [party_tpl|pt_manhunters,"manhunter_talk_b1", [], "I knew it! Come on, lads, lets go get these bastards! Thanks a lot, friend.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [party_tpl|pt_manhunters|plyr,"manhunter_talk_b", [], "No, haven't seen any outlaws lately.", "manhunter_talk_b2",[]],
  [party_tpl|pt_manhunters,"manhunter_talk_b2", [], "Bah. They're holed up in this country like rats, but we'll smoke them out yet. Sooner or later.", "close_window",[(assign, "$g_leave_encounter",1)]],

  [party_tpl|pt_looters|auto_proceed,"start", [(eq,"$talk_context",tc_party_encounter)], "Warning: This line should never be displayed.", "looters_1",[
	(str_store_string, s11, "@Hrrr! Frresh meat and shiny things."),
	(str_store_string, s12, "@Gharr! Hand over all yerr stuff, and we might spare yourr life."),
	(str_store_string, s13, "@Death to men!"),
	(store_random_in_range, ":random", 11, 14),
	(str_store_string_reg, s4, ":random"),
	(play_sound, "snd_encounter_looters")
  ]],
  [party_tpl|pt_looters,"looters_1", [], "{s4}", "looters_2",[]],
  [party_tpl|pt_looters|plyr,"looters_2", [[store_character_level,reg(1),"trp_player"],[lt,reg(1),4]], "I'm not afraid of you lot. Fight me if you dare!", "close_window",
   [[encounter_attack]]],
  [party_tpl|pt_looters|plyr,"looters_2", [[store_character_level,reg(1),"trp_player"],[ge,reg(1),4]], "You'll have nothing of mine but cold steel, scum.", "close_window",
   [[encounter_attack]]],
#####################################################################
#TLD STUFFF
#########################################################
    ##Kingdom Patrols, Scouts, and Unique Parties - Melissa

   # [party_tpl|pt_swadian_scouts,"start", [(eq,"$talk_context",tc_party_encounter),
                    # (encountered_party_is_attacker),],
   # "Halt! I have heard your name, {playername}! Your audacity is at an end! Surrender or die!", "scouts_talk", []
                    # ],
   
   # [party_tpl|pt_swadian_scouts,"start", [(eq,"$talk_context",tc_party_encounter)], "Yes, what do you wish, my {Lord/Lady}?", "scout_talk_a",[]],
   # [party_tpl|pt_swadian_scouts|plyr,"scout_talk_a", [], "Nothing. I was merely passing by.", "close_window",[(assign,"$g_leave_encounter",1)]],
   # [party_tpl|pt_swadian_scouts|plyr,"scout_talk_a", [(neq,"$g_encountered_party_faction","$players_kingdom"),], "Drop your weapons and come with me. You're trespassing on my land.", "scout_talk_b1",[]],
   # [party_tpl|pt_swadian_scouts,"scout_talk_b1", [], "What madness is this? You'll have to fight us to take us, {fool/chit}!", "close_window",[(call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),[encounter_attack]]],
   
  # [anyone|plyr,"scouts_talk", [
                    # ],
   # "You bloody fool! I'll have your head on a pike!.", "close_window", [[encounter_attack]]],
  
  # [anyone|plyr,"scouts_talk", [
                    # ],
   # "Don't kill us, we surrender!.", "close_window", [(assign,"$g_player_surrenders",1)]],

   # [party_tpl|pt_vaegir_scouts,"start", [(eq,"$talk_context",tc_party_encounter),
                    # (encountered_party_is_attacker),],
   # "Halt! I have heard your name, {playername}! Your audacity is at an end! Surrender or die!", "scouts_talk", []
                    # ],

   # [party_tpl|pt_vaegir_scouts,"start", [(eq,"$talk_context",tc_party_encounter)], "Yes, what do you wish, my {Lord/Lady}?", "scout_talk_a",[]],
   # [party_tpl|pt_vaegir_scouts|plyr,"scout_talk_a", [], "Nothing. I was merely passing by.", "close_window",[(assign,"$g_leave_encounter",1)]],
   # [party_tpl|pt_vaegir_scouts|plyr,"scout_talk_a", [(neq,"$g_encountered_party_faction","$players_kingdom"),], "Drop your weapons and come with me. You're trespassing on my land.", "scout_talk_b1",[]],
   # [party_tpl|pt_vaegir_scouts,"scout_talk_b1", [], "What madness is this? You'll have to fight us to take us, {fool/chit}!", "close_window",[(call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),[encounter_attack]]],
   
   # [party_tpl|pt_khergit_scouts,"start", [(eq,"$talk_context",tc_party_encounter),
                    # (encountered_party_is_attacker),],
   # "Halt! I have heard your name, {playername}! Your audacity is at an end! Surrender or die!", "scouts_talk", []
                    # ],

   # [party_tpl|pt_khergit_scouts,"start", [(eq,"$talk_context",tc_party_encounter)], "Yes, what do you wish, my {Lord/Lady}?", "scout_talk_a",[]],
   # [party_tpl|pt_khergit_scouts|plyr,"scout_talk_a", [], "Nothing. I was merely passing by.", "close_window",[(assign,"$g_leave_encounter",1)]],
   # [party_tpl|pt_khergit_scouts|plyr,"scout_talk_a", [(neq,"$g_encountered_party_faction","$players_kingdom"),], "Drop your weapons and come with me. You're trespassing on my land.", "scout_talk_b1",[]],
   # [party_tpl|pt_khergit_scouts,"scout_talk_b1", [], "What madness is this? You'll have to fight us to take us, {fool/chit}!", "close_window",[(call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),[encounter_attack]]],
   
   # [party_tpl|pt_nord_scouts,"start", [(eq,"$talk_context",tc_party_encounter),
                    # (encountered_party_is_attacker),],
   # "Halt! I have heard your name, {playername}! Your audacity is at an end! Surrender or die!", "scouts_talk", []
                    # ],

   # [party_tpl|pt_nord_scouts,"start", [(eq,"$talk_context",tc_party_encounter)], "Yes, what do you wish, my {Lord/Lady}?", "scout_talk_a",[]],
   # [party_tpl|pt_nord_scouts|plyr,"scout_talk_a", [], "Nothing. I was merely passing by.", "close_window",[(assign,"$g_leave_encounter",1)]],
   # [party_tpl|pt_nord_scouts|plyr,"scout_talk_a", [(neq,"$g_encountered_party_faction","$players_kingdom"),], "Drop your weapons and come with me. You're trespassing on my land.", "scout_talk_b1",[]],
   # [party_tpl|pt_nord_scouts,"scout_talk_b1", [], "What madness is this? You'll have to fight us to take us, {fool/chit}!", "close_window",[(call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),[encounter_attack]]],
   
   # [party_tpl|pt_rhodok_scouts,"start", [(eq,"$talk_context",tc_party_encounter),
                    # (encountered_party_is_attacker),],
   # "Halt! I have heard your name, {playername}! Your audacity is at an end! Surrender or die!", "scouts_talk", []
                    # ],

   # [party_tpl|pt_rhodok_scouts,"start", [(eq,"$talk_context",tc_party_encounter)], "Yes, what do you wish, my {Lord/Lady}?", "scout_talk_a",[]],
   # [party_tpl|pt_rhodok_scouts|plyr,"scout_talk_a", [], "Nothing. I was merely passing by.", "close_window",[(assign,"$g_leave_encounter",1)]],
   # [party_tpl|pt_rhodok_scouts|plyr,"scout_talk_a", [(neq,"$g_encountered_party_faction","$players_kingdom"),], "Drop your weapons and come with me. You're trespassing on my land.", "scout_talk_b1",[]],
   # [party_tpl|pt_rhodok_scouts,"scout_talk_b1", [], "What madness is this? You'll have to fight us to take us, {fool/chit}!", "close_window",[(call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),[encounter_attack]]],
   
   # [party_tpl|pt_swadian_patrol,"start", [(eq,"$talk_context",tc_party_encounter),
                    # (encountered_party_is_attacker),],
   # "Halt, foes of the Queen and our Holy Empire! Surrender yourselves or meet death!", "patrol_charge", []
                    # ],

   # [party_tpl|pt_swadian_patrol,"start", [(eq,"$talk_context",tc_party_encounter)], "Yes, {sir/ma'am}?", "patrol_talk_a",[]],
   # [party_tpl|pt_swadian_patrol|plyr,"patrol_talk_a", [], "Nothing. Farewell.", "close_window",[(assign,"$g_leave_encounter",1)]],
   # [party_tpl|pt_swadian_patrol|plyr,"patrol_talk_a", [(neq,"$g_encountered_party_faction","$players_kingdom"),],
      # "You all die here!", "patrol_talk_b1",[]],
   # [party_tpl|pt_swadian_patrol,"patrol_talk_b1", [], "What, {sir/ma'am}?", "patrol_talk_b2",[]],
   # [party_tpl|pt_swadian_patrol|plyr,"patrol_talk_b2", [], "Apologies. I mistook you for someone else. Farewell.", "close_window",[(assign,"$g_leave_encounter",1)]],
   # [party_tpl|pt_swadian_patrol|plyr,"patrol_talk_b2", [], "You're going to die. Here.", "patrol_attack",[]],
   # [party_tpl|pt_swadian_patrol,"patrol_attack", [], "Damn you! At {his/her} throat, Brothers!", "close_window",[(call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),[encounter_attack]]],
   
  # [anyone|plyr,"patrol_charge", [
                    # ],
   # "Die, scum!", "close_window", [[encounter_attack]]],
  
  # [anyone|plyr,"patrol_charge", [
                    # ],
   # "Don't kill us, we surrender!.", "close_window", [(assign,"$g_player_surrenders",1)]],

   # [party_tpl|pt_vaegir_patrol,"start", [(eq,"$talk_context",tc_party_encounter),
                    # (encountered_party_is_attacker),],
   # "Surrender to the justice of the Principality, or die!", "patrol_charge", []
                    # ],

   # [party_tpl|pt_vaegir_patrol,"start", [(eq,"$talk_context",tc_party_encounter)], "Yes, {sir/ma'am}?", "patrol_talk_a",[]],
   # [party_tpl|pt_vaegir_patrol|plyr,"patrol_talk_a", [], "Nothing. Farewell.", "close_window",[(assign,"$g_leave_encounter",1)]],
   # [party_tpl|pt_vaegir_patrol|plyr,"patrol_talk_a", [(neq,"$g_encountered_party_faction","$players_kingdom"),],
       # "You all die here!", "patrol_talk_b1",[]],
   # [party_tpl|pt_vaegir_patrol,"patrol_talk_b1", [], "What, {sir/ma'am}?", "patrol_talk_b2",[]],
   # [party_tpl|pt_vaegir_patrol|plyr,"patrol_talk_b2", [], "Apologies. I mistook you for someone else. Farewell.", "close_window",[(assign,"$g_leave_encounter",1)]],
   # [party_tpl|pt_vaegir_patrol|plyr,"patrol_talk_b2", [], "You're going to die. Here.", "patrol_attack",[]],
   # [party_tpl|pt_vaegir_patrol,"patrol_attack", [], "Damn you! At {his/her} throat, clansmen!", "close_window",[(call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),[encounter_attack]]],
   
   # [party_tpl|pt_khergit_patrol,"start", [(eq,"$talk_context",tc_party_encounter),
                    # (encountered_party_is_attacker),],
   # "Surrender or be crushed beneath our hooves!", "patrol_charge", []
                    # ],

   # [party_tpl|pt_khergit_patrol,"start", [(eq,"$talk_context",tc_party_encounter)], "Yes, {sir/ma'am}?", "patrol_talk_a",[]],
   # [party_tpl|pt_khergit_patrol|plyr,"patrol_talk_a", [], "Nothing. Farewell.", "close_window",[(assign,"$g_leave_encounter",1)]],
   # [party_tpl|pt_khergit_patrol|plyr,"patrol_talk_a", [(neq,"$g_encountered_party_faction","$players_kingdom"),],
       # "You all die here!", "patrol_talk_b1",[]],
   # [party_tpl|pt_khergit_patrol,"patrol_talk_b1", [], "What, {sir/ma'am}?", "patrol_talk_b2",[]],
   # [party_tpl|pt_khergit_patrol|plyr,"patrol_talk_b2", [], "Apologies. I mistook you for someone else. Farewell.", "close_window",[(assign,"$g_leave_encounter",1)]],
   # [party_tpl|pt_khergit_patrol|plyr,"patrol_talk_b2", [], "You're going to die. Here.", "patrol_attack",[]],
   # [party_tpl|pt_khergit_patrol,"patrol_attack", [], "You will have to get past our arrows first!", "close_window",[(call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),[encounter_attack]]],
   
   # [party_tpl|pt_nord_patrol,"start", [(eq,"$talk_context",tc_party_encounter),
                    # (encountered_party_is_attacker),],
   # "Either die here on our swords, or surrender and live to see another day, Calradian.", "patrol_charge", []
                    # ],

   # [party_tpl|pt_nord_patrol,"start", [(eq,"$talk_context",tc_party_encounter)], "Yes, {sir/ma'am}?", "patrol_talk_a",[]],
   # [party_tpl|pt_nord_patrol|plyr,"patrol_talk_a", [], "Nothing. Farewell.", "close_window",[(assign,"$g_leave_encounter",1)]],
   # [party_tpl|pt_nord_patrol|plyr,"patrol_talk_a", [(neq,"$g_encountered_party_faction","$players_kingdom"),],
       # "You all die here!", "patrol_talk_b1",[]],
   # [party_tpl|pt_nord_patrol,"patrol_talk_b1", [], "What, {sir/ma'am}?", "patrol_talk_b2",[]],
   # [party_tpl|pt_nord_patrol|plyr,"patrol_talk_b2", [], "Apologies. I mistook you for someone else. Farewell.", "close_window",[(assign,"$g_leave_encounter",1)]],
   # [party_tpl|pt_nord_patrol|plyr,"patrol_talk_b2", [], "You're going to die. Here.", "patrol_attack",[]],
   # [party_tpl|pt_nord_patrol,"patrol_attack", [], "DEATH AND GLORY! ATTACK, NORTHMEN!", "close_window",[(call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),[encounter_attack]]],
   
   # [party_tpl|pt_rhodok_patrol,"start", [(eq,"$talk_context",tc_party_encounter),
                    # (encountered_party_is_attacker),],
   # "In the name of the Confederacy of Rhodokius, surrender your troops and weapons.", "patrol_charge", []
                    # ],					

   # [party_tpl|pt_rhodok_patrol,"start", [(eq,"$talk_context",tc_party_encounter)], "Yes, {sir/ma'am}?", "patrol_talk_a",[]],
   # [party_tpl|pt_rhodok_patrol|plyr,"patrol_talk_a", [], "Nothing. Farewell.", "close_window",[(assign,"$g_leave_encounter",1)]],
   # [party_tpl|pt_rhodok_patrol|plyr,"patrol_talk_a", [(neq,"$g_encountered_party_faction","$players_kingdom"),],
         # "You all die here!", "patrol_talk_b1",[]],
   # [party_tpl|pt_rhodok_patrol,"patrol_talk_b1", [], "What, {sir/ma'am}?", "patrol_talk_b2",[]],
   # [party_tpl|pt_rhodok_patrol|plyr,"patrol_talk_b2", [], "Apologies. I mistook you for someone else. Farewell.", "close_window",[(assign,"$g_leave_encounter",1)]],
   # [party_tpl|pt_rhodok_patrol|plyr,"patrol_talk_b2", [], "You're going to die. Here.", "patrol_attack",[]],
   # [party_tpl|pt_rhodok_patrol,"patrol_attack", [], "Damn you! Charge, Rhodoks!", "close_window",[(call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),[encounter_attack]]],
   
   # [party_tpl|pt_crusaders,"start", [(eq,"$talk_context",tc_party_encounter),
                    # (encountered_party_is_attacker),],
   # "For the Holy Light and our Empire!", "special_charge", []
                    # ],  
   
   
   #########################################################
   #TLD TLD LTDL
 #########################################################  
   
   
   
   
   
  [party_tpl|pt_village_farmers,"start", [(eq,"$talk_context",tc_party_encounter),
                                          (agent_play_sound, "$g_talk_agent", "snd_encounter_farmers"),
  ],
   " My {lord/lady}, we're only poor farmers from the village of {s11}. {reg1?We are taking our products to the market at {s12}.:We are returning from the market at {s12} back to our village.}", "village_farmer_talk",
   [(party_get_slot, ":target_center", "$g_encountered_party", slot_party_ai_object),
    (party_get_slot, ":home_center", "$g_encountered_party", slot_party_home_center),
    (party_get_slot, ":market_town", ":home_center", slot_village_market_town),
    (str_store_party_name, s11, ":home_center"),
    (str_store_party_name, s12, ":market_town"),
    (assign, reg1, 1),
    (try_begin),
      (party_slot_eq, ":target_center", slot_party_type, spt_village),
      (assign, reg1, 0),
    (try_end),
    ]],

  [anyone|plyr,"village_farmer_talk", [], "We'll see how poor you are after I take what you've got!", "close_window",
   [(party_get_slot, ":home_center", "$g_encountered_party", slot_party_home_center),
    (party_get_slot, ":market_town", ":home_center", slot_village_market_town),
    (party_get_slot, ":village_owner", ":home_center", slot_town_lord),
    (call_script, "script_change_player_relation_with_center", ":home_center", -4),
    (call_script, "script_change_player_relation_with_center", ":market_town", -2),
    (call_script, "script_change_player_relation_with_troop", ":village_owner", -2),
    (store_relation,":rel", "$g_encountered_party_faction","fac_player_supporters_faction"),
    (try_begin),
      (gt, ":rel", 0),
      (val_sub, ":rel", 5),
    (try_end),
    (val_sub, ":rel", 3),
    (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":rel"),
    ]],
  [anyone|plyr,"village_farmer_talk", [], "Carry on, then. Farewell.", "close_window",[(assign, "$g_leave_encounter",1)]],


### COMPANIONS
  [anyone,"start", [(troop_slot_eq,"$g_talk_troop", slot_troop_occupation, slto_player_companion),
                    (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
                    (party_get_num_companion_stacks, ":num_stacks", "$g_encountered_party"),
                    (ge, ":num_stacks", 1),
                    (party_stack_get_troop_id, ":castle_leader", "$g_encountered_party", 0),
                    (eq, ":castle_leader", "$g_talk_troop"),
                    (eq, "$talk_context", 0)],
   "Yes, {playername}? What can I do for you?", "member_castellan_talk",[]],
  
  [anyone,"member_castellan_pretalk", [], "Anything else?", "member_castellan_talk",[]],
  
  [anyone|plyr,"member_castellan_talk", [],
   "I want to review the castle garrison.", "member_review_castle_garrison",[]],
  [anyone,"member_review_castle_garrison", [], "Of course. Here are our lists, let me know of any changes you require...", "member_castellan_pretalk",[(change_screen_exchange_members,0)]],
  [anyone|plyr,"member_castellan_talk", [],
   "Let me see your equipment.", "member_review_castellan_equipment",[]],
  [anyone,"member_review_castellan_equipment", [], "Very well, it's all here...", "member_castellan_pretalk",[(change_screen_equip_other)]],
  [anyone|plyr,"member_castellan_talk", [],
   "I want you to abandon the castle and join my party.", "member_castellan_join",[]],
  [anyone,"member_castellan_join", [(party_can_join_party,"$g_encountered_party","p_main_party")],
   "I've grown quite fond of the place... But if it is your wish, {playername}, I'll come with you.", "close_window", [
       (assign, "$g_move_heroes", 1),
       (call_script, "script_party_add_party", "p_main_party", "$g_encountered_party"),
       (party_clear, "$g_encountered_party"),
       ]],
  [anyone,"member_castellan_join", [],
   "And where would we sleep? You're dragging a whole army with you, {playername}, there's no more room for all of us.", "member_castellan_pretalk",[]],
  
  [anyone|plyr,"member_castellan_talk", [], "[Leave]", "close_window",[]],


  [anyone,"start", [(troop_slot_eq,"$g_talk_troop", slot_troop_occupation, slto_player_companion),
                    (neg|main_party_has_troop,"$g_talk_troop"),
                    (eq, "$talk_context", tc_party_encounter)],
   "Do you want me to rejoin you?", "member_wilderness_talk",[]],
  [anyone,"start", [(neg|main_party_has_troop,"$g_talk_troop"),(eq, "$g_encountered_party", "p_four_ways_inn")], "Do you want me to rejoin you?", "member_inn_talk",[]],
#  [anyone,"member_separate_inn", [], "I don't know what you will do without me, but you are the boss. I'll wait for you at the Four Ways inn.", "close_window",
#  [anyone,"member_separate_inn", [], "All right then. I'll meet you at the four ways inn. Good luck.", "close_window",
#   [(remove_member_from_party,"$g_talk_troop", "p_main_party"),(add_troop_to_site, "$g_talk_troop", "scn_four_ways_inn", borcha_inn_entry)]],

#Quest heroes member chats

  [trp_kidnapped_girl,"member_chat", [], "Are we home yet?", "kidnapped_girl_chat_1",[]],
  [trp_kidnapped_girl|plyr,"kidnapped_girl_chat_1", [], "Not yet.", "kidnapped_girl_chat_2",[]],
  [trp_kidnapped_girl,"kidnapped_girl_chat_2", [], "I can't wait to get back. I've missed my family so much, I'd give anything to see them again.", "close_window",[]],

  [anyone,"member_chat",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
    ], "{playername}, when do you think we can reach our destination?", "member_lady_1",[]],
  [anyone|plyr, "member_lady_1", [],  "We still have a long way ahead of us.", "member_lady_2a", []],
  [anyone|plyr, "member_lady_1", [],  "Very soon. We're almost there.", "member_lady_2b", []],

  [anyone ,"member_lady_2a", [],  "Ah, I am going to enjoy the road for a while longer then. I won't complain.\
 I find riding out in the open so much more pleasant than sitting in the castle all day.\
 You know, I envy you. You can live like this all the time.", "close_window", []],
  [anyone ,"member_lady_2b", [],  "That's good news. Not that I don't like your company, but I did miss my little luxuries.\
 Still I am sorry that I'll leave you soon. You must promise me, you'll come visit me when you can.", "close_window", []],

  [anyone ,"member_chat", [(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),],
   "Greetings, {playername}, my first and foremost vassal. I await your counsel.", "supported_pretender_talk", []],
  [anyone ,"supported_pretender_pretalk", [],
   "Anything else?", "supported_pretender_talk", []],

  [anyone|plyr,"supported_pretender_talk", [],
   "What do you think about our progress so far?", "pretender_progress",[]],

  [anyone,"pretender_progress", [
       (assign, reg11, 0),(assign, reg13, 0),(assign, reg14, 0),(assign, reg15, 0),
       (assign, reg21, 0),(assign, reg23, 0),(assign, reg24, 0),(assign, reg25, 0),
       
       (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
         (store_troop_faction, ":troop_faction", ":troop_no"),
         (try_begin),
           (eq, ":troop_faction", "fac_player_supporters_faction"),
           (neq, ":troop_no", "trp_player"),
           (neq, ":troop_no", "$supported_pretender"),
           (val_add, reg11, 1),
         (else_try),
           (eq, ":troop_faction", "$supported_pretender_old_faction"),
           (neg|faction_slot_eq, "$supported_pretender_old_faction", slot_faction_leader, ":troop_no"),
           (val_add, reg21, 1),
         (try_end),
       (try_end),
       (try_for_range, ":center_no", centers_begin, centers_end),
         (store_faction_of_party, ":center_faction", ":center_no"),
         (try_begin),
           (eq, ":center_faction", "fac_player_supporters_faction"),
           (try_begin),
             (party_slot_eq, ":center_no", slot_party_type, spt_town),
             (val_add, reg13, 1),
           (else_try),
             (party_slot_eq, ":center_no", slot_party_type, spt_castle),
             (val_add, reg14, 1),
           (else_try),
             (party_slot_eq, ":center_no", slot_party_type, spt_village),
             (val_add, reg15, 1),
           (try_end),
         (else_try),
           (eq, ":center_faction", "$supported_pretender_old_faction"),
           (try_begin),
             (party_slot_eq, ":center_no", slot_party_type, spt_town),
             (val_add, reg23, 1),
           (else_try),
             (party_slot_eq, ":center_no", slot_party_type, spt_castle),
             (val_add, reg24, 1),
           (else_try),
             (party_slot_eq, ":center_no", slot_party_type, spt_village),
             (val_add, reg25, 1),
           (try_end),
         (try_end),
       (try_end),
       (store_add, reg19, reg13, reg14),
       (val_add, reg19, reg15),
       (store_add, reg29, reg23, reg24),
       (val_add, reg29, reg25),
       (store_add, ":our_score", reg13, reg14),
       (val_add, ":our_score", reg11),
       (store_add, ":their_score", reg23, reg24),
       (val_add, ":their_score", reg21),
       (store_add, ":total_score", ":our_score", ":their_score"),
       (val_mul, ":our_score", 100),
       (store_div, ":our_ratio", ":our_score", ":total_score"),
       (try_begin),
         (lt, ":our_ratio", 10),
         (str_store_string, s30, "@we have made very little progress so far"),
       (else_try),
         (lt, ":our_ratio", 30),
         (str_store_string, s30, "@we have suceeded in gaining some ground, but we still have a long way to go"),
       (else_try),
         (lt, ":our_ratio", 50),
         (str_store_string, s30, "@we have become a significant force, and we have an even chance of victory"),
       (else_try),
         (lt, ":our_ratio", 75),
         (str_store_string, s30, "@we are winning the war, but our enemies are still holding on."),
       (else_try),
         (str_store_string, s30, "@we are on the verge of victory. The remaining enemies pose no threat, but we still need to hunt them down."),
       (try_end),
       (faction_get_slot, ":enemy_king", "$supported_pretender_old_faction", slot_faction_leader),
       (str_store_troop_name, s9, ":enemy_king"),
      ],
   "{reg11?We have {reg11} lords on our side:We have no lord with us yet},\
 whereas {reg21?{s9} still has {reg21} lords supporting him:{s9} has no loyal lords left}.\
 {reg19?We control {reg13?{reg13} towns:} {reg14?{reg14} castles:} {reg15?and {reg15} villages:}:We don't control any settlements},\
 while {reg29?they have {reg23?{reg23} towns:} {reg24?{reg24} castles:} {reg25?and {reg25} villages:}:they have no remaining settlements}.\
 Overall, {s30}.", "pretender_progress_2",[]],

  [anyone|plyr,"pretender_progress_2", [],
   "Then, we must keep fighting and rally our supporters!", "supported_pretender_pretalk",[]],

  [anyone|plyr,"pretender_progress_2", [],
   "It seems this rebellion is not going anywhere. We must give up.", "pretender_quit_rebel_confirm",[]],
  
  [anyone,"pretender_quit_rebel_confirm", [],
   "{playername}, you can't abandon me now. Are you serious?", "pretender_quit_rebel_confirm_2",[]],
  
  [anyone|plyr,"pretender_quit_rebel_confirm_2", [],
   "Indeed, I am. I can't support you any longer.", "pretender_quit_rebel_confirm_3",[]],
  
  [anyone|plyr,"pretender_quit_rebel_confirm_2", [],
   "I was jesting. I will fight for you until we succeed.", "supported_pretender_pretalk",[]],
 
   [anyone,"pretender_quit_rebel_confirm_3", [],
   "Are you absolutely sure? I will never forgive you if you abandon my cause.", "pretender_quit_rebel_confirm_4",[]],
  
  [anyone|plyr,"pretender_quit_rebel_confirm_4", [],
   "I am sure.", "pretender_quit_rebel",[]],
  
  [anyone|plyr,"pretender_quit_rebel_confirm_4", [],
   "Let me think about this some more.", "supported_pretender_pretalk",[]],
 
  [anyone,"pretender_quit_rebel", [],
   "So be it. Then my cause is lost. There is only one thing to do for me now. I will go from Calradia and never come back.", "close_window",
   [
     (troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
     (try_for_range, ":cur_troop", kingdom_heroes_begin, kingdom_heroes_end),
       (neq, "$supported_pretender", ":cur_troop"),
       (store_troop_faction, ":cur_faction", ":cur_troop"),
       (eq, ":cur_faction", "fac_player_supporters_faction"),
       (call_script, "script_change_troop_faction", ":cur_troop", ":original_faction"),
     (try_end),
     (troop_set_faction, "$g_talk_troop", "fac_neutral"),
     (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
     (assign, ":has_center", 0),
     (try_for_range, ":cur_center", centers_begin, centers_end),
       (store_faction_of_party, ":cur_faction", ":cur_center"),
       (eq, ":cur_faction", "fac_player_supporters_faction"),
       (assign, ":has_center", 1),
       (neg|party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
       (call_script, "script_give_center_to_lord", ":cur_center", "trp_player", 0),
     (try_end),
     (party_remove_members, "p_main_party", "$supported_pretender", 1),
     (faction_set_slot, ":original_faction", slot_faction_has_rebellion_chance, 0),
     (assign, "$supported_pretender", 0),
     (try_begin),
       (eq, ":has_center", 1),
       (faction_set_color, "fac_player_supporters_faction", 0xAAAAAA),
     (else_try),
       (call_script, "script_activate_deactivate_player_faction", -1),
     (try_end),
     (call_script, "script_change_player_honor", -20),
     (call_script, "script_fail_quest", "qst_rebel_against_kingdom"),
     (call_script, "script_end_quest", "qst_rebel_against_kingdom"),
    ]],


  [anyone|plyr,"supported_pretender_talk", [],
   "{reg65?My lady:My lord}, would you allow me to check out your equipment?", "supported_pretender_equip",[]],
  [anyone,"supported_pretender_equip", [], "Very well, it's all here...", "supported_pretender_pretalk",[
      (change_screen_equip_other),
      ]],

  [anyone|plyr,"supported_pretender_talk", [], "If it would please you, can you tell me about your skills?", "pretneder_view_char_requested",[]],
  [anyone,"pretneder_view_char_requested", [], "Well, all right.", "supported_pretender_pretalk",[(change_screen_view_character)]],


  [anyone|plyr,"supported_pretender_talk", [],
   "Let us keep going, {reg65?my lady:sir}.", "close_window",[]],


  [anyone,"do_member_trade", [], "Anything else?", "member_talk",[]],


  [anyone,"member_chat", [(store_conversation_troop,"$g_talk_troop"),
                          (troop_is_hero,"$g_talk_troop"),
                          (troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
                          (str_store_string, s5, ":honorific"),
                          ], "Yes, {s5}?", "member_talk",[]],

  [anyone|plyr,"member_talk", [],

   "Let me see your equipment.", "member_trade",[]],
  [anyone,"member_trade", [], "Very well, it's all here...", "do_member_trade",[
#      (change_screen_trade)
      (change_screen_equip_other),
      ]],

  [anyone,"do_member_trade", [], "Anything else?", "member_talk",[]],

  [anyone|plyr,"member_talk", [], "What can you tell me about your skills?", "view_member_char_requested",[]],
  [anyone,"view_member_char_requested", [], "All right, let me tell you...", "do_member_view_char",[(change_screen_view_character)]],

  [anyone|plyr,"member_talk", [], "We need to separate for a while.", "member_separate",[
            # (call_script, "script_npc_morale", "$g_talk_troop"),
            # (assign, "$npc_quit_morale", reg0),
      ]],

  [anyone,"member_separate", [
#            (gt, "$npc_quit_morale", 30),
      ], "Oh really? Well, I'm not just going to wait around here. I'm going to go to my home town to look for other work. Is that what you want?", "member_separate_confirm",
   []],

#  [anyone,"member_separate", [
#      ], "Well, actually, there was something I needed to tell you.", "companion_quitting",
#   [ ]],


  [anyone|plyr,"member_separate_confirm", [], "That's right. We need to part ways.", "member_separate_yes",[]],
  [anyone|plyr,"member_separate_confirm", [], "No, I'd rather have you at my side.", "do_member_trade",[]],

  [anyone,"member_separate_yes", [
      ], "Well. I'll be off, then. Look me up if you need me.", "close_window",
   [
            (troop_set_slot, "$g_talk_troop", slot_troop_occupation, 0),
            (troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_dismissed),
            (remove_member_from_party, "$g_talk_troop"),
       ]],


  [anyone|plyr,"member_talk", [], "I'd like to ask you something.", "member_question",[]],

  [anyone|plyr,"member_talk", [], "Never mind.", "close_window",[]],

  [anyone,"member_question", [], "Very well. What did you want to ask?", "member_question_2",[]],

  [anyone|plyr,"member_question_2", [], "How do you feel about the way things are going in this company?", "member_morale",[]],
  [anyone|plyr,"member_question_2", [], "Tell me your story again.", "member_background_recap",[]],

  [anyone,"member_morale", [
        (call_script, "script_npc_morale", "$g_talk_troop"),
      ], "{s21}", "do_member_trade",[]],

  [anyone,"member_background_recap", [
          (troop_get_slot, ":first_met", "$g_talk_troop", slot_troop_first_encountered),
          (str_store_party_name, 20, ":first_met"),
          (troop_get_slot, ":home", "$g_talk_troop", slot_troop_home),
          (str_store_party_name, 21, ":home"),
          (troop_get_slot, ":recap", "$g_talk_troop", slot_troop_home_recap),
          (str_store_string, 5, ":recap"),
      ], "{s5}", "member_background_recap_2",[]],

  [anyone,"member_background_recap_2", [
          (str_clear, 19),
          (troop_get_slot, ":background", "$g_talk_troop", slot_troop_backstory_b),
          (str_store_string, 5, ":background"),
      ], "{s5}", "member_background_recap_3",[]],

  [anyone,"member_background_recap_3", [
      ], "Then shortly after, I joined up with you.", "do_member_trade",[]],

  [anyone,"do_member_view_char", [], "Anything else?", "member_talk",[]],



  [anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (this_or_next|eq, "$talk_context", tc_court_talk), #TLD
                     (this_or_next|eq, "$talk_context", tc_town_talk), #TLD
                     (eq, "$talk_context", tc_tavern_talk),
                     (main_party_has_troop, "$g_talk_troop")],
   "Let's leave whenever you are ready.", "close_window", []],

  [anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_turned_down_twice, 1),
   ],
   "Please do not waste any more of my time today, {sir/madame}. Perhaps we shall meet again in our travels.", "close_window", [
       ]],


  [anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (eq, "$g_talk_troop_met", 0),
                     (troop_get_slot, ":intro", "$g_talk_troop", slot_troop_intro),
                     (str_store_string, 5, ":intro"),
                     (str_store_party_name, 20, "$g_encountered_party"),
   ],
   "{s5}", "companion_recruit_intro_response", [
                    (troop_set_slot, "$g_talk_troop", slot_troop_first_encountered, "$g_encountered_party"),
       ]],


  [anyone|plyr, "companion_recruit_intro_response", [
                     (troop_get_slot, ":intro_response", "$g_talk_troop", slot_troop_intro_response_1),
                     (str_store_string, 6, ":intro_response")
      ], "{s6}", "companion_recruit_backstory_a", []],

  [anyone|plyr, "companion_recruit_intro_response", [
                     (troop_get_slot, ":intro_response", "$g_talk_troop", slot_troop_intro_response_2),
                     (str_store_string, 7, ":intro_response")
      ],  "{s7}", "close_window", [
          ]],

  [anyone, "companion_recruit_backstory_a", [(troop_get_slot, ":backstory_a", "$g_talk_troop", slot_troop_backstory_a),
                     (str_store_string, 5, ":backstory_a"),
                     (str_store_string, 19, "str_here_plus_space"),
                     (str_store_party_name, 20, "$g_encountered_party"),
   ],
   "{s5}", "companion_recruit_backstory_b", []],

  [anyone, "companion_recruit_backstory_b", [(troop_get_slot, ":backstory_b", "$g_talk_troop", slot_troop_backstory_b),
                     (str_store_string, 5, ":backstory_b"),
                     (str_store_party_name, 20, "$g_encountered_party"),
   ],
   "{s5}", "companion_recruit_backstory_c", []],

  [anyone, "companion_recruit_backstory_c", [(troop_get_slot, ":backstory_c", "$g_talk_troop", slot_troop_backstory_c),
                     (str_store_string, 5, ":backstory_c"),
   ],
   "{s5}", "companion_recruit_backstory_response", []],

  [anyone|plyr, "companion_recruit_backstory_response", [
                     (troop_get_slot, ":backstory_response", "$g_talk_troop", slot_troop_backstory_response_1),
                     (str_store_string, 6, ":backstory_response")
      ], "{s6}", "companion_recruit_signup", []],

  [anyone|plyr, "companion_recruit_backstory_response", [
                     (troop_get_slot, ":backstory_response", "$g_talk_troop", slot_troop_backstory_response_2),
                     (str_store_string, 7, ":backstory_response")
      ],  "{s7}", "close_window", [
          ]],

  [anyone, "companion_recruit_signup", [(troop_get_slot, ":signup", "$g_talk_troop", slot_troop_signup),
                     (str_store_string, 5, ":signup"),
                     (str_store_party_name, 20, "$g_encountered_party"),

   ],
   "{s5}", "companion_recruit_signup_b", []],

  [anyone, "companion_recruit_signup_b", [
      (troop_get_slot, ":signup", "$g_talk_troop", slot_troop_signup_2),
      (troop_get_slot, reg3, "$g_talk_troop", slot_troop_payment_request),#

      (str_store_string, 5, ":signup"),
      (str_store_party_name, 20, "$g_encountered_party"),

   ],
   "{s5}", "companion_recruit_signup_response", []],

  [anyone|plyr, "companion_recruit_signup_response", [(neg|hero_can_join, "p_main_party"),], "Unfortunately, I can't take on any more hands in my party right now.", "close_window", [
     ]],

  [anyone|plyr, "companion_recruit_signup_response", [
                    (hero_can_join, "p_main_party"),
                    (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_1),
                    (str_store_string, 6, ":signup_response")
      ], "{s6}", "companion_recruit_payment", []],

  [anyone|plyr, "companion_recruit_signup_response", [
                    (hero_can_join, "p_main_party"),
                     (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_2),
                     (str_store_string, 7, ":signup_response")
      ],  "{s7}", "close_window", [
          ]],

  [anyone|auto_proceed, "companion_recruit_payment", [
      (troop_slot_eq, "$g_talk_troop", slot_troop_payment_request, 0),
   ],
   ".", "companion_recruit_signup_confirm", []],
  
  [anyone, "companion_recruit_payment", [
      (store_sub, ":npc_offset", "$g_talk_troop", "trp_npc1"),
      (store_add, ":dialog_line", "str_npc1_payment", ":npc_offset"),
      (str_store_string, s5, ":dialog_line"),
      (troop_get_slot, reg3, "$g_talk_troop", slot_troop_payment_request),
      (str_store_party_name, s20, "$g_encountered_party"),
   ],
   "{s5}", "companion_recruit_payment_response", []],

  [anyone|plyr, "companion_recruit_payment_response", [
                    (hero_can_join, "p_main_party"),
                    (troop_get_slot, ":amount_requested", "$g_talk_troop", slot_troop_payment_request),#
                    (store_troop_gold, ":gold", "trp_player"),#
                    (ge, ":gold", ":amount_requested"),#
                    (assign, reg3, ":amount_requested"),
                    (store_sub, ":npc_offset", "$g_talk_troop", "trp_npc1"),
                    (store_add, ":dialog_line", "str_npc1_payment_response", ":npc_offset"),
                    (str_store_string, s6, ":dialog_line"),
      ], "{s6}", "companion_recruit_signup_confirm", [
                    (troop_get_slot, ":amount_requested", "$g_talk_troop", slot_troop_payment_request),#
                    (gt, ":amount_requested", 0),#
                    (troop_remove_gold, "trp_player", ":amount_requested"),  #                  
                    (troop_set_slot, "$g_talk_troop", slot_troop_payment_request, 0),#
          ]],

  [anyone|plyr, "companion_recruit_payment_response", [
                     (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_2),
                     (str_store_string, s7, ":signup_response")
      ],  "Sorry. I can't afford that at the moment.", "close_window", [
          ]],

  [anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 1),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, 0),

    ],
   "We meet again.", "companion_recruit_meet_again", [
                     (troop_set_slot, "$g_talk_troop", slot_troop_turned_down_twice, 1),
       ]],

  [anyone|plyr, "companion_recruit_meet_again", [
      ], "So... What have you been doing since our last encounter?", "companion_recruit_backstory_delayed", []],

  [anyone|plyr, "companion_recruit_meet_again", [
      ],  "Good day to you.", "close_window", [
          ]],


  [anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, 0),
   ],
   "Yes?", "companion_recruit_secondchance", [
                     (troop_set_slot, "$g_talk_troop", slot_troop_turned_down_twice, 1),
       ]],


  [anyone|plyr, "companion_recruit_secondchance", [
      ], "My apologies if I was rude, earlier. What was your story again?", "companion_recruit_backstory_b", []],

  [anyone|plyr, "companion_recruit_secondchance", [
      ],  "Never mind.", "close_window", [
          ]],

  [anyone, "companion_recruit_backstory_delayed",
   [(troop_get_slot, ":backstory_delayed", "$g_talk_troop", slot_troop_backstory_delayed),
     (str_store_string, 5, ":backstory_delayed")
   ],
   "{s5}", "companion_recruit_backstory_delayed_response", []],

  [anyone|plyr, "companion_recruit_backstory_delayed_response", [
      ], "I might be able to use you in my company.", "companion_recruit_signup_b", [
          ]],

  [anyone|plyr, "companion_recruit_backstory_delayed_response", [
      ],  "I'll let you know if I hear of anything.", "close_window", [
          ]],

  [anyone, "companion_recruit_signup_confirm", [], "Good! Give me a few moments to prepare and I'll be ready to move.", "close_window",
   [(call_script, "script_recruit_troop_as_companion", "$g_talk_troop")]],



### Rehire dialogues
  [anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate),
   ],
   "My offer to rejoin you still stands, if you'll have me.", "companion_rehire", []],

### If the companion and the player were separated in battle
  [anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_scattered),
                     (assign, ":battle_fate", "str_battle_fate_1"),
                     (store_random_in_range, ":fate_roll", 0, 5),
                     (val_add, ":battle_fate", ":fate_roll"),
                     (str_store_string, 6, ":battle_fate"),
                     (troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
                     (str_store_string, 5, ":honorific"),
   ],
   "It is good to see you alive, {s5}! {s6}, and I did not know whether you had been captured, or slain, or got away. I've been roaming around since then, looking for you. Shall I get my gear together and rejoin your company?",
   "companion_rehire", [
                     (troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate),
      ]],


### If the player and the companion parted on bad terms
  [anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_turned_down_twice, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_quit),
                     (troop_get_slot, ":speech", "$g_talk_troop", slot_troop_rehire_speech),
                     (str_store_string, 5, ":speech"),
   ],
   "{s5}", "companion_rehire", [
                     (troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate),
      ]],


###If the player and the companion parted on good terms
  [anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_dismissed),
                     (troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
                     (str_store_string, 21, ":honorific"),
                     (troop_get_slot, ":speech", "$g_talk_troop", slot_troop_backstory_delayed),
                     (str_store_string, 5, ":speech"),
   ],
   "It is good to see you, {s21}! To tell you the truth, I had hoped to run into you.",
   "companion_was_dismissed", [
                     (troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate),
      ]],

  [anyone, "companion_was_dismissed", [
                      (troop_get_slot, ":speech", "$g_talk_troop", slot_troop_backstory_delayed),
                     (str_store_string, 5, ":speech"),
   ],
   "{s5}. Would you want me to rejoin your company?", "companion_rehire", [
      ]],


  [anyone|plyr, "companion_rehire", [
                    (hero_can_join, "p_main_party")
      ], "Welcome back, my friend!", "companion_recruit_signup_confirm", []],

  [anyone|plyr, "companion_rehire", [
      ],  "Sorry, I can't take on anyone else right now now.", "companion_rehire_refused", [
          ]],

  [anyone, "companion_rehire_refused", [], "Well... Look me up if you change your mind, eh?", "close_window",
   []],

  [anyone, "event_triggered",
   [
     (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "$g_talk_troop"),
     (ge, "$g_center_taken_by_player_faction", 0),
     (str_store_party_name, s1, "$g_center_taken_by_player_faction"),
     ],
   "{s1} is not being managed by anyone. Whom shall I put in charge?", "center_captured_lord_advice",
   []],

  [anyone|plyr|repeat_for_troops, "center_captured_lord_advice",
   [
     (store_repeat_object, ":troop_no"),
     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
     (neq, "$g_talk_troop", ":troop_no"),
     (neq, "trp_player", ":troop_no"),
     (store_troop_faction, ":faction_no", ":troop_no"),
     (eq, ":faction_no", "fac_player_supporters_faction"),
     (str_store_troop_name, s11, ":troop_no"),
     (call_script, "script_print_troop_owned_centers_in_numbers_to_s0", ":troop_no"),
     (try_begin),
       (eq, reg0, 0),
       (str_store_string, s1, "@(no fiefs)"),
     (else_try),
       (str_store_string, s1, "@(fiefs: {s0})"),
     (try_end),
     ],
   "{s11}. {s1}", "center_captured_lord_advice_2",
   [
     (store_repeat_object, "$temp"),
     ]],

  [anyone|plyr, "center_captured_lord_advice",
   [
     (call_script, "script_print_troop_owned_centers_in_numbers_to_s0", "trp_player"),
     (str_store_party_name, s1, "$g_center_taken_by_player_faction"),
    ],
   "Please {s65}, I want to have {s1} for myself. (fiefs: {s0})", "center_captured_lord_advice_2",
   [
     (assign, "$temp", "trp_player"),
     ]],

  [anyone|plyr, "center_captured_lord_advice",
   [
     (call_script, "script_print_troop_owned_centers_in_numbers_to_s0", "$g_talk_troop"),
     (str_store_party_name, s1, "$g_center_taken_by_player_faction"),
     ],
   "{s66}, you should have {s1} for yourself. (fiefs: {s0})", "center_captured_lord_advice_2",
   [
     (assign, "$temp", "$g_talk_troop"),
     ]],

  [anyone, "center_captured_lord_advice_2",
   [
#     (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "$g_talk_troop"),
#     (ge, "$g_center_taken_by_player_faction", 0),
     ],
   "Hmmm. All right, {playername}. I value your counsel highly. {reg6?I:{reg7?You:{s11}}} will be the new {reg3?lady:lord} of {s1}.", "close_window",
   [
     (assign, ":new_owner", "$temp"),
     (call_script, "script_calculate_troop_score_for_center", ":new_owner", "$g_center_taken_by_player_faction"),
     (assign, ":new_owner_score", reg0),
     (assign, ":total_negative_effect"),
     (try_for_range, ":cur_troop", kingdom_heroes_begin, kingdom_heroes_end),
       (store_troop_faction, ":cur_faction", ":cur_troop"),
       (eq, ":cur_faction", "fac_player_supporters_faction"),
       (neq, ":cur_troop", ":new_owner"),
       (call_script, "script_calculate_troop_score_for_center", ":cur_troop", "$g_center_taken_by_player_faction"),
       (assign, ":cur_troop_score", reg0),
       (gt, ":cur_troop_score", ":new_owner_score"),
       (store_sub, ":difference", ":cur_troop_score", ":new_owner_score"),
       (store_random_in_range, ":random_dif", 0, ":difference"),
       (val_div, ":random_dif", 1000),
       (gt, ":random_dif", 0),
       (val_add, ":total_negative_effect", ":random_dif"),
       (val_mul, ":random_dif", -1),
       (call_script, "script_change_player_relation_with_troop", ":cur_troop", ":random_dif"),
     (try_end),
     (val_mul, ":total_negative_effect", 2),
     (val_div, ":total_negative_effect", 3),
     (val_add, ":total_negative_effect", 5),
     (try_begin),
       (neq, ":new_owner", "trp_player"),
       (val_min, ":total_negative_effect", 30),
       (call_script, "script_change_player_relation_with_troop", ":new_owner", ":total_negative_effect"),
     (try_end),
     (call_script, "script_give_center_to_lord", "$g_center_taken_by_player_faction", ":new_owner", 0),
     (try_begin),
       (neq, ":new_owner", "trp_player"),
       (call_script, "script_cf_reinforce_party", "$g_center_taken_by_player_faction"),
       (call_script, "script_cf_reinforce_party", "$g_center_taken_by_player_faction"),
     (try_end),

     (assign, reg6, 0),
     (assign, reg7, 0),
     (try_begin),
       (eq, "$temp", "$g_talk_troop"),
       (assign, reg6, 1),
     (else_try),
       (eq, "$temp", "trp_player"),
       (assign, reg7, 1),
     (else_try),
       (str_store_troop_name, s11, "$temp"),
     (try_end),
     (str_store_party_name, s1, "$g_center_taken_by_player_faction"),
     (troop_get_type, reg3, "$temp"),
     (assign, "$g_center_taken_by_player_faction", -1),
     ]],


  [anyone, "event_triggered", [
                     (eq, "$npc_map_talk_context", slot_troop_home), 
                     (store_conversation_troop, "$map_talk_troop"),
                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_home_intro),
                     (str_store_string, s5, ":speech"),
                     ],
   "{s5}", "companion_home_description", [
                    (troop_set_slot, "$map_talk_troop", slot_troop_home_speech_delivered, 1),
       ]],

  [anyone|plyr, "companion_home_description", [
      ],  "Tell me more.", "companion_home_description_2", [
          ]],

  [anyone|plyr, "companion_home_description", [
      ],  "We don't have time to chat just now.", "close_window", [
          ]],

  [anyone|plyr, "companion_home_description", [
      ],  "I prefer my companions not to bother me with such trivialities.", "close_window", [
                    (assign, "$disable_local_histories", 1),
          ]],


  [anyone, "companion_home_description_2", [
                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_home_description),
                     (str_store_string, 5, ":speech"),
      ],  "{s5}", "companion_home_description_3", [
          ]],

  [anyone, "companion_home_description_3", [
                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_home_description_2),
                     (str_store_string, 5, ":speech"),
      ],  "{s5}", "close_window", [
          ]],


# TLD recruiting in city -- mtarini
#

[anyone,"start", 
   [
		(eq, "$talk_context", tc_hire_troops), 
		# prepare strings useful in the folowing dialog
		(store_faction_of_party, ":fac", "$g_encountered_party"),
		(assign, ":p_fac", "$players_kingdom" ),
		(str_store_party_name, s21, "$g_encountered_party"), # s21: CITY NAME
		(str_store_faction_name, s22, ":fac"), # s22: City faction name
		(str_store_troop_name, s23, "$g_player_troop"), # s23: Player name
		(faction_get_slot, ":p_rank", ":fac", slot_faction_rank),
		(call_script, "script_get_rank_title", ":p_fac" ),(str_store_string_reg, 29, 24), # s29: player TITLE  (among own faction)
		(call_script, "script_get_rank_title", ":fac" ), # s24: player TITLE  (among city faction)
		(str_store_faction_name, s25, ":p_fac"), # s25: Player's faction name
		(assign, reg26, 0),(try_begin),(eq,":p_fac",":fac"),(assign,reg26,1),(try_end), # reg26: 1 if city of player faction
		(party_get_num_companions, reg27, "p_main_party"), # reg27: initial party size

		# prepare greeting string
		(store_div, reg10,":p_rank", 100),
		(try_begin),
			(eq, reg26, 1), (str_store_string, s33, "@Greetings, {s23}, {s24}."), # same faction (military salut?)
		(else_try),
			(ge, reg10, 4), (str_store_string, s33, "@Greetings, {s23}, {s24}."),  # player not same faction, but thrusted
		(else_try),
			(ge, reg10, 1), (str_store_string, s33, "@Greetings, {s23}."), # player not much thrusted
		(else_try),
			(str_store_string, s33, "@So, you are {s23}. I hear you fight for {s25}, so I guess I should consider you an ally."), # player unknown
		(try_end),

		# just to see if someone can be given away: backup party, then see if troops which can be given away 
		(call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
		(call_script, "script_party_split_by_faction", "p_main_party_backup", "p_temp_party",":fac"),
		
   ],
   "{s33}^^I am currently in charge of the forces garrisoned here at {s21}. Did you want to see me?", "player_hire_troop", 
   [
   ]
 ],

[anyone|plyr,"player_hire_troop", 
	[(party_get_free_companions_capacity,reg10,"p_main_party"), (gt,reg10,0)], 
	"I need volunteers willing to follow me in dangerous missions in the open.", "player_hire_troop_take", [
		# prepare party to recruit  from
		(party_get_slot, "$hiring_from", "$current_town", slot_town_volunteer_pt ),
		(assign, "$num_hirable", 0),
		(try_begin),
			(ge, "$hiring_from", 0),
			(party_is_active, "$hiring_from"),
			(store_party_size, "$num_hirable" , "$hiring_from"),
			(set_mercenary_source_party,"$hiring_from"),
			(call_script, "script_get_party_min_join_cost", "$hiring_from"),
			(assign, "$cheapest_join", reg0),
		(try_end),
	]
],

[anyone|plyr,"player_hire_troop", 
	[(party_get_num_companions,reg11,"p_main_party_backup"), (gt,reg11,1)], # player has someone to give away 
	"Some of my soldiers in my group would be more useful here, to defend {s21}.", "player_hire_troop_give", [
		(store_faction_of_party, ":fac", "$g_encountered_party"),
		(call_script, "script_party_split_by_faction", "p_main_party", "p_temp_party",":fac"),
		
		(party_get_num_companions, reg28, "p_main_party"), # reg28: initial party size (after removing troops unfit to be given)
		(call_script, "script_get_party_disband_cost", "p_main_party",1),(assign,reg29,reg0), # reg29: initial party total value (after removing troops ...)

	]
	
],

[anyone|plyr,"player_hire_troop", [], "Farewell.", "close_window", [] ],

[anyone,"player_hire_troop_take", 
  [(eq,"$num_hirable" ,0)], # no one wants to join
  "I am sorry, no-one else is ready to go.^They will serve {s22} by holding the defences here.", 
  "player_hire_troop_nextcycle", []
],

[anyone,"player_hire_troop_take", 
  [(store_troop_gold, ":cur_gold", "$g_player_troop"), (gt,"$cheapest_join",":cur_gold"),(eq, reg26, 1)], # these who want to join cost too much -- player same faction
  "There would be brave soldiers willing to risk their life, but in those dark times I cannot afford to let them leave the defence here, or to lose one more man.^^Not even to let them fight under your command. Sorry.", 
  "player_hire_troop_nextcycle", []
],

[anyone,"player_hire_troop_take", 
  [(store_troop_gold, ":cur_gold", "$g_player_troop"), (gt,"$cheapest_join",":cur_gold"),(eq, reg26, 0)], # these who want to join cost too much -- player other faction
  "There are brave soldiers here willing to risk their life, but not fighting under your command, I'm afraid...^^We are men of {s22}, not of {s25}.", 
  "player_hire_troop_nextcycle", []
],

[anyone,"player_hire_troop_take", 
	[(gt,"$num_hirable" ,0),   # there's someone to hire...
	 (store_troop_gold, ":cur_gold", "$g_player_troop"), (le,"$cheapest_join",":cur_gold"),], # and player can afford it
	"There are brave soldiers here volunteering for these missions.^^I think can let a few of them go with you for a while.", 
	"player_hire_troop_pre_pre_nextcycle", [[change_screen_buy_mercenaries]]
],

 [anyone,"player_hire_troop_give", 
	 [],
	 "Strenghten defences in {s21}? This is surely welcome. ", 
	 "player_hire_troop_reunite", [[change_screen_give_members]]
 ],

 [anyone,"player_hire_troop_pre_pre_nextcycle", [ ], 
    ". . .", 
    "player_hire_troop_pre_nextcycle", []
 ],

 [anyone,"player_hire_troop_pre_nextcycle", 
	 [ (party_get_num_companions, reg10, "p_main_party"), (eq, reg10, reg27), ], # party didn't change size 
    "So you changed your mind...^I see.", 
    "player_hire_troop_nextcycle", []
 ],

 [anyone,"player_hire_troop_pre_nextcycle", 
	 [ (party_get_num_companions, reg10, "p_main_party"), (gt, reg10, reg27),], # party increased size 
    "Make them return in one piece. I personally know the valor of each one of them. And here we need every soul.", 
    "player_hire_troop_nextcycle", []
 ],

 [anyone,"player_hire_troop_reunite", [ ], 
    ". . .", 
    "player_hire_troop_reunite_1", [
	]
 ],

 [anyone,"player_hire_troop_reunite_1", 
	 [ 
	   (party_get_num_companions, reg0, "p_main_party"), 
	   (eq, reg28, reg0), # player didn't give anyone (party size unchanged)
	 ], # party decreased size 
    "So you changed your mind...^I see.", 
    "player_hire_troop_nextcycle", []
 ],

 [anyone,"player_hire_troop_reunite_1", 
	 [ 
		(party_get_num_companions, reg0, "p_main_party"), (store_sub, reg10, reg28, reg0), 
		(gt, reg10, 0), # player did give someone 
		(store_sub, reg9, reg10, 1),
		(call_script, "script_get_party_disband_cost", "p_main_party", 1), (store_sub, reg11, reg29, reg0), 
		(str_clear,  s31),(str_clear,  s32),
		(try_begin),(eq, reg26, 1), #player is in own faction
			(str_store_string, s31, "@Thank you, officer.^"),
		(else_try),
			(str_store_string, s32, "@^{s22} is grateful to you, {s23}, {s29}^"),
		(try_end),
		

	 ], # party decreased size 
    "{s31}{reg9?Those:That} brave {reg9?soldiers:soldier} will surely help us defend {s21}.{s32}^^^[earned {reg11} Res.Points of {s22}]", 
    "player_hire_troop_reunite_2", [(troop_add_gold, "$g_player_troop", reg11),]
 ],

 [anyone|plyr,"player_hire_troop_reunite_2", 
	 [ (try_begin),(eq, reg26, 1), #player is ih own faction
			(str_store_string, s31, "@My duty."),
		(else_try),
			(str_store_string, s31, "@Our enemy is ultimately the same,^our war is one."),
		(try_end), 
	],
    "{s31}", 
    "player_hire_troop_nextcycle", [
	(call_script, "script_party_add_party", "p_main_party", "p_temp_party"),
	]
 ],

 [anyone,"player_hire_troop_nextcycle", 
	 [  ], # party didn't change size 
    "Anything else?", 
    "player_hire_troop", [
		(party_get_num_companions, reg27, "p_main_party"),
		# prepare troops which can be given away (others are in moved in temp party)
		(store_faction_of_party, ":fac", "$current_town"),
		(call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
		(call_script, "script_party_split_by_faction", "p_main_party_backup", "p_temp_party",":fac"),
	]
 ],

		




# Kingdom Lords:
  [anyone,"start", [(eq, "$talk_context", tc_castle_commander)],
   "What do you want?", "player_siege_castle_commander_1", []],
  [anyone|plyr,"player_siege_castle_commander_1", [],
   "Surrender! Your situation is hopeless!", "player_siege_ask_surrender", []],
  [anyone|plyr,"player_siege_castle_commander_1", [], "Nothing. I'll leave you now.", "close_window", []],

  
  [anyone,"player_siege_ask_surrender", [(lt, "$g_enemy_strength", 100), (store_mul,":required_str","$g_enemy_strength",5),(ge, "$g_ally_strength", ":required_str")],
   "Perhaps... Do you give your word of honour that we'll be treated well?", "player_siege_ask_surrender_treatment", []],
  [anyone,"player_siege_ask_surrender", [(lt, "$g_enemy_strength", 200), (store_mul,":required_str","$g_enemy_strength",3),(ge, "$g_ally_strength", ":required_str")],
   "We are ready to leave this castle to you and march away if you give me your word of honour that you'll let us leave unmolested.", "player_siege_ask_leave_unmolested", []],
  [anyone,"player_siege_ask_surrender", [],
   "Surrender? Hah! We can hold these walls until we all die of old age.", "close_window", []],

  
  [anyone|plyr,"player_siege_ask_surrender_treatment", [],
   "I give you nothing. Surrender now or prepare to die!", "player_siege_ask_surrender_treatment_reject", []],
  [anyone,"player_siege_ask_surrender_treatment_reject", [],
   "Bastard. We will fight you to the last man!", "close_window", []],
  [anyone|plyr,"player_siege_ask_surrender_treatment", [],
   "You will be ransomed and your soldiers will live. I give you my word.", "player_siege_ask_surrender_treatment_accept", []],
  [anyone,"player_siege_ask_surrender_treatment_accept", [],
   "Very well then. Under those terms, I offer you my surrender.", "close_window", [(assign,"$g_enemy_surrenders",1)]],

  [anyone|plyr,"player_siege_ask_leave_unmolested", [],
   "You have my word. You will not come under attack if you leave the castle.", "player_siege_ask_leave_unmolested_accept", []],
  [anyone,"player_siege_ask_leave_unmolested_accept", [],
   "Very well. Then we leave this castle to you. You have won this day. But we'll meet again.", "close_window", [(assign,"$g_castle_left_to_player",1)]],
  [anyone|plyr,"player_siege_ask_leave_unmolested", [],
   "Unacceptable. I want prisoners.", "player_siege_ask_leave_unmolested_reject", []],
  [anyone,"player_siege_ask_leave_unmolested_reject", [],
   "Then we will defend this castle to the death, and this parley is done. Farewell.", "close_window", []],

  
#After battle texts
  
 
#Troop commentary changes begin
  [anyone,"start", [(eq,"$talk_context",tc_hero_defeated),
                    (troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero)],
   "{s43}", "defeat_lord_answer",
   [(troop_set_slot, "$g_talk_troop", slot_troop_leaded_party, -1),
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_surrender_offer_default"),
    ]],

  [anyone|plyr,"defeat_lord_answer", [],
   "You are my prisoner now.", "defeat_lord_answer_1",
   [
     #(troop_set_slot, "$g_talk_troop", slot_troop_is_prisoner, 1),
     (troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, "p_main_party"),
     (party_force_add_prisoners, "p_main_party", "$g_talk_troop", 1),#take prisoner
     (call_script, "script_add_log_entry", logent_lord_captured_by_player, "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction"),
     ]],

  [anyone,"defeat_lord_answer_1", [],
   "I am at your mercy.", "close_window", []],

  [anyone|plyr,"defeat_lord_answer", [],
   "You have fought well. You are free to go.", "defeat_lord_answer_2",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 5),
    (call_script, "script_change_player_honor", 3),
    (call_script, "script_add_log_entry", logent_lord_defeated_but_let_go_by_player, "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction")]],

  [anyone,"defeat_lord_answer_2", [],
   "{s43}", "close_window", [
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_prisoner_released_default"),
       ]],
#Troop commentary changes end

#Troop commentaries changes begin
  [anyone,"start", [(eq,"$talk_context",tc_party_encounter),
                    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
                    (lt,"$g_encountered_party_relation",0),
                    (encountered_party_is_attacker),
                    (eq, "$g_talk_troop_met", 1),                    ],
   "{playername}!", "party_encounter_lord_hostile_attacker", [
                    ]],

  [anyone,"start", [(eq,"$talk_context",tc_party_encounter),
                    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
                    (lt,"$g_encountered_party_relation",0),
                    (encountered_party_is_attacker),                ],
   "Halt!", "party_encounter_lord_hostile_attacker", [
                    ]],

  [anyone,"party_encounter_lord_hostile_attacker", [
      (gt, "$g_comment_found", 0),
                    ],
   "{s42}", "party_encounter_lord_hostile_attacker", [
                         (try_begin),
                           (neq, "$log_comment_relation_change", 0),
                           (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", "$log_comment_relation_change"),
                         (try_end),
                         (assign, "$g_comment_found", 0),
                    ]],

#Troop commentaries changes end
  [anyone,"party_encounter_lord_hostile_attacker", [
                    ],
   "{s43}", "party_encounter_lord_hostile_attacker_2",
   [
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_surrender_demand_default"),
       ]],

  [anyone|plyr,"party_encounter_lord_hostile_attacker_2", [
                    ],
   "Is there no way to avoid this battle? I don't want to fight with you.", "party_encounter_offer_dont_fight", []],
  
  [anyone|plyr,"party_encounter_lord_hostile_attacker_2", [
                    ],
   "Don't attack! We surrender.", "close_window", [(assign,"$g_player_surrenders",1)]],

  [anyone|plyr,"party_encounter_lord_hostile_attacker_2", [
                    ],
   "We will fight you to the end!", "close_window", []],

  [anyone, "party_encounter_offer_dont_fight", [(gt, "$g_talk_troop_relation", 30),
#TODO: Add adition conditions, lord personalities, battle advantage, etc...                                                
                    ],
   "I owe you a favor, don't I. Well... all right then. I will let you go just this once.", "close_window", [
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop", -7),
    (store_current_hours,":protected_until"),
    (val_add, ":protected_until", 72),
    (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,":protected_until"),
    (party_ignore_player, "$g_encountered_party", 72),
    (assign, "$g_leave_encounter",1)
       ]],
  
  [anyone, "party_encounter_offer_dont_fight", [
                    ],
   "Ha-ha. But I want to fight with you.", "close_window", []],
  
##  [anyone,"start", [(eq,"$talk_context",tc_party_encounter),
##                    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
##                    (lt,"$g_encountered_party_relation",0),
##                    (neg|encountered_party_is_attacker),
##                    ],
##   "What do you want?", "party_encounter_lord_hostile_defender",
##   []],


#  [anyone|plyr,"party_encounter_lord_hostile_defender", [],
#   "Nothing. We'll leave you in peace.", "close_window", [(assign, "$g_leave_encounter",1)]],



 
#Betrayal texts should go here


##  [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
##                     (troop_slot_eq,"$g_talk_troop",slot_troop_last_quest_betrayed, 1),
##                     (troop_slot_eq,"$g_talk_troop",slot_troop_last_quest, "qst_deliver_message_to_lover"),
##                     (le,"$talk_context",tc_siege_commander),
##                     ],
##   "I had trusted that letter to you, thinking you were a {man/lady} of honor, and you handed it directly to the girl's father.\
## I should have known you were not to be trusted. Anyway, I have learned my lesson and I won't make that mistake again.", "close_window",
##   [(call_script, "script_clear_last_quest", "$g_talk_troop")]],






#Rebellion changes begin


  [anyone ,"start",
   [
     (is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
     (faction_slot_eq, "$g_talk_troop_faction", slot_faction_state, 2),
     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
     ],
   "[Our first task is to seize a fortress. Then other lords will join us.]", "pretender_start", [
     ]],

  [anyone ,"start",
   [
     (is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
     (eq, "$g_talk_troop", "$supported_pretender"),
     ],
   "I await your counsel, {playername}.", "supported_pretender_talk", [
     ]],

  [anyone ,"start",
   [
     (is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
     (assign, "$pretender_told_story", 0),
     (eq, "$g_talk_troop_met", 0),
     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
     ],
   "Do I know you?.", "pretender_intro_1", []],
  [anyone|plyr ,"pretender_intro_1", [], "My name is {playername}. At your sevice.", "pretender_intro_2", []],
  [anyone|plyr ,"pretender_intro_1", [], "I am {playername}. Perhaps you have heard of my exploits.", "pretender_intro_2", []],

  [anyone ,"pretender_intro_2", [(troop_get_slot, ":rebellion_string", "$g_talk_troop", slot_troop_original_faction),
                                 (val_sub, ":rebellion_string", "fac_gondor"),
                                 (val_add, ":rebellion_string", "str_swadian_rebellion_pretender_intro"),
                                 (str_store_string, 48, ":rebellion_string"),],
   "{s48}", "pretender_intro_3", []],

  [anyone|plyr ,"pretender_intro_3", [(troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                      (str_store_faction_name, s12, ":original_faction"),
                                      (faction_get_slot, ":original_ruler", ":original_faction", slot_faction_leader),
                                      (str_store_troop_name, s11, ":original_ruler"),],
   "I thought {s12} was ruled by {s11}?", "pretender_rebellion_cause_1", [(troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1),]],

  [anyone ,"start",
   [
     (is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
     ],
   "Greetings, {playername}", "pretender_start", [(assign, "$pretender_told_story", 0)]],

  [anyone|plyr ,"pretender_start",
   [
     (troop_slot_eq, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
     (eq, "$pretender_told_story", 0)
     ],
   "What was your story again, {reg65?my lady:sir}?", "pretender_rebellion_cause_prelim", [
     ]],

  [anyone,"pretender_rebellion_cause_prelim", [],
   "I shall tell you.", "pretender_rebellion_cause_1", [
                     ]],


  [anyone,"pretender_rebellion_cause_1", [],
   "{s48}", "pretender_rebellion_cause_2", [
                     (assign, "$pretender_told_story", 1),
                     (troop_get_slot, ":rebellion_string", "$g_talk_troop", slot_troop_original_faction),
                     (val_sub, ":rebellion_string", "fac_gondor"),                                
                     (val_add, ":rebellion_string", "str_swadian_rebellion_pretender_story_1"),
                     (str_store_string, 48, ":rebellion_string"),
                     ]],

  [anyone,"pretender_rebellion_cause_2", [],
   "{s48}", "pretender_rebellion_cause_3", [
                     (troop_get_slot, ":rebellion_string", "$g_talk_troop", slot_troop_original_faction),
                     (val_sub, ":rebellion_string", "fac_gondor"),                                
                     (val_add, ":rebellion_string", "str_swadian_rebellion_pretender_story_2"),
                     (str_store_string, 48, ":rebellion_string"),
                     ]],

  [anyone,"pretender_rebellion_cause_3", [],
   "{s48}", "pretender_start", [
                     (troop_get_slot, ":rebellion_string", "$g_talk_troop", slot_troop_original_faction),
                     (val_sub, ":rebellion_string", "fac_gondor"),                                
                     (val_add, ":rebellion_string", "str_swadian_rebellion_pretender_story_3"),
                     (str_store_string, 48, ":rebellion_string"),
                     ]],

  [anyone|plyr ,"pretender_start", [
                    (troop_slot_eq, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
                     ],
   "I want to take up your cause and help you reclaim your throne!", "pretender_discuss_rebellion_1", [
     ]],

  [anyone|plyr ,"pretender_start", [
                     ],
   "I must leave now.", "pretender_end", [
     ]],

  [anyone ,"pretender_discuss_rebellion_1", [(troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                             (faction_get_slot, ":original_ruler", ":original_faction", slot_faction_leader),
                                             (str_store_troop_name, s11, ":original_ruler")],
   "Are you sure you will be up to the task, {playername}? Reclaiming my throne will be no simple matter.\
 The lords of our realm have all sworn oaths of homage to {s11}.\
 Such oaths to a usurper are of course invalid, and we can expect some of the lords to side with us, but it will be a very tough and challenging struggle ahead.", "pretender_discuss_rebellion_2", []],

  [anyone|plyr ,"pretender_discuss_rebellion_2", [],  "I am ready for this struggle.", "pretender_discuss_rebellion_3", []],
  [anyone|plyr ,"pretender_discuss_rebellion_2", [],  "You are right. Perhaps, I should think about this some more.", "pretender_end", []],

  [anyone ,"pretender_discuss_rebellion_3", [(neg|troop_slot_ge, "trp_player",slot_troop_renown, 200),
                                             (troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                             (faction_get_slot, ":original_ruler", ":original_faction", slot_faction_leader),
                                             (str_store_troop_name, s11, ":original_ruler")],
   "I have no doubt that your support for my cause is heartfelt, {playername}, and I am grateful to you for it.\
 But I don't think we have much of a chance of success.\
 If you can gain renown in the battlefield and make a name for yourself as a great commander, then our friends would not hesitate to join our cause,\
 and our enemies would be wary to take up arms against us. When that time comes, I will come with you gladly.\
 But until that time, it will be wiser not to openly challange the usurper, {s11}.", "close_window", []],

  [anyone ,"pretender_discuss_rebellion_3", [(gt, "$supported_pretender", 0),
                                             (str_store_troop_name, s17, "$supported_pretender")],
   "Haven't you already taken up the cause of {s17}?\
 You must have a very strong sense of justice, indeed.\
 But no, thanks. I will not be part of your game.", "close_window", []],

  [anyone ,"pretender_discuss_rebellion_3", [(gt, "$players_kingdom", 0),
                                             (neq, "$players_kingdom", "fac_player_supporters_faction"),
                                             (neq, "$players_kingdom", "fac_player_faction"),
                                             (troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                             (neq, "$players_kingdom", ":original_faction"),
                                             (gt, "$player_has_homage", 0),
                                             (str_store_faction_name, s16, "$players_kingdom"),
                                             (faction_get_slot, ":player_ruler", "$players_kingdom", slot_faction_leader),
                                             (str_store_troop_name, s15, ":player_ruler"),
                                             (str_store_faction_name, s17, ":original_faction"),
                                             ],
   "{playername}, you are already oath-bound to serve {s15}.\
 As such, I cannot allow you to take up my cause, and let my enemies claim that I am but a mere puppet of {s16}.\
 No, if I am to have the throne of {s17}, I must do it due to the righteousness of my cause and the support of my subjects alone.\
 If you want to help me, you must first free yourself of your oath to {s15}.", "close_window", []],

  [anyone ,"pretender_discuss_rebellion_3", [(troop_get_slot, ":original_faction", "$g_talk_troop", slot_troop_original_faction),
                                             (str_store_faction_name, s12, ":original_faction"),
                                             (faction_get_slot, ":original_ruler", ":original_faction", slot_faction_leader),
                                             (str_store_troop_name, s11, ":original_ruler")],
   "You are a capable warrior, {playername}, and I am sure with your renown as a commander, and my righteous cause, the nobles and the good people of {s12} will flock to our support.\
 The time is ripe for us to act! I will come with you, and together, we will topple the usurper {s11} and take the throne from his bloodied hands.\
 But first, you must give me your oath of homage and accept me as your liege {reg65?lady:lord}.", "pretender_rebellion_ready", []],


  [anyone ,"pretender_discuss_rebellion", [(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
                     (assign, "$town_to_rebel",    0),
                     (assign, "$town_to_approach", 0),
                     (troop_get_slot, ":rebellion_target_faction", "$g_talk_troop", slot_troop_original_faction),
                     (try_for_range, ":town", towns_begin, towns_end),
                        (store_faction_of_party, ":town_faction", ":town"),
                        (eq, ":town_faction", ":rebellion_target_faction"),
                        (party_get_slot, ":siege_state", ":town", slot_village_state),
                        (neq, ":siege_state", svs_under_siege),
                        (try_begin),
                            (party_slot_ge, ":town", slot_town_rebellion_readiness, 30),
                            (assign, "$town_to_rebel", ":town"),
                        (else_try),
#                            (party_get_slot, ":contact", ":town", slot_town_rebellion_contact), 
#                            (lt, ":contact", 2),
                            (assign, "$town_to_approach", ":town"),
                            (assign, ":support_base_is_available", 1),
                            (try_begin),
#Check to see if support base is captured or under siege
                            (try_end),
                        (try_end),
                     (try_end),
                     (eq, "$town_to_rebel", 0),
                     (gt, "$town_to_approach", 0),
                     (gt, ":support_base_is_available", 0),
                     ],
   "[Before we rebel, I want you to raise support for my cause. I have always had strong backing from the town of {s4}, but you may have good ties in other places. Are you up for that?]", "pretender_town_quest", [
                     (troop_get_slot, ":support_base", "$g_talk_troop", slot_troop_support_base),
                     (str_store_party_name, s4, ":support_base"),
     ]],

  [anyone ,"pretender_discuss_rebellion", [(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
                     (eq, "$town_to_rebel", 0),
                     (gt, "$town_to_approach", 0),
                     ],
   "[Before we rebel, I want you to raise support for my cause. If you have good ties with any towns, you should try there. Are you up for that?]", "pretender_town_quest", [
     ]],


  [anyone ,"pretender_discuss_rebellion", [(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
                     (eq, "$town_to_approach", 0),

                     ],
   "[Circumstances aren't really right for a rebellion right now. Let us lay low for a while]", "pretender_start", [
     ]],


  [anyone ,"pretender_discuss_rebellion", [(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
                     (gt, "$town_to_rebel", 0),
                     (gt, "$players_kingdom", 0),
                     ],
   "[You have laid the groundwork for a rebellion, but you are affiliated with another liege]", "pretender_start", [
     ]],

  [anyone ,"pretender_discuss_rebellion", [(is_between, "$g_talk_troop", pretenders_begin, pretenders_end),
                     (gt, "$town_to_rebel", 0),
                     ],   "You have done good work. {s4} and possibly other towns are ready to rebel. Whenever you are ready, let us ride forth to war.", "pretender_rebellion_ready", [
                     (str_store_party_name, 4, "$town_to_rebel"),
     ]],


  [anyone|plyr ,"pretender_rebellion_ready", [
                     (troop_get_type, reg3, "$g_talk_troop"),
                     ],
   "I am ready to pledge myself to your cause, {reg3?my lady:sir}.", "lord_give_oath_2", [
     ]],

  [anyone|plyr ,"pretender_rebellion_ready", [
                     ],
   "Let us bide our time a little longer.", "pretender_end", [
     ]],


  [anyone|plyr ,"pretender_town_quest", [
                                 ],
   "[Abracadabra - the town is ready]", "pretender_discuss_rebellion", [
                     (troop_get_slot, ":support_base", "$g_talk_troop", slot_troop_support_base),

                     (party_set_slot, ":support_base", slot_town_rebellion_readiness, 40),
     ]],

  [anyone|plyr ,"pretender_town_quest", [                    
                     ],
   "[Not interested, thanks]", "pretender_end", [
     ]],


  [anyone ,"pretender_end", [
                     ],
   "Farewell for now, then.", "close_window", [
     ]],



# Events....
# Choose friend.  
#Post 0907 changes begin
  [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     (neq, "$g_talk_troop_met", 0),
                     (gt, "$g_time_since_last_talk", 24),
                     (gt, "$g_talk_troop_relation", -10),
                     (store_random_in_range, ":random_num", 0, 100),
                     (lt, ":random_num", 30),
                     (eq,"$talk_context",tc_town_talk),
                     (call_script, "script_cf_troop_get_random_enemy_troop_with_occupation", "$g_talk_troop", slto_kingdom_hero),
                     (assign, ":other_lord",reg0),
                     (troop_get_slot, ":other_lord_relation", ":other_lord", slot_troop_player_relation),
                     (ge, ":other_lord_relation", 20),
                     (str_store_troop_name, s6, ":other_lord"),
                     (assign, "$temp", ":other_lord"),
                     ],
   "I heard that you have befriended that {s43} called {s6}.\
 Believe me, you can't trust that man.\
 You should end your dealings with him.", "lord_event_choose_friend", [
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_insult_default"),

     ]],

  [anyone|plyr ,"lord_event_choose_friend", [],  "I assure you, {s65}, I am no friend of {s6}.", "lord_event_choose_friend_renounce", [
      (call_script, "script_change_player_relation_with_troop","$g_talk_troop",5),
      (call_script, "script_change_player_relation_with_troop","$temp",-10),
      ]],

  [anyone ,"lord_event_choose_friend_renounce", [],  "Glad news, {playername}. I would fear for your safety otherwise.\
 If you do encounter {s6}, be on your guard and don't believe a word.", "lord_pretalk", []],
  
  [anyone|plyr ,"lord_event_choose_friend", [],  "{s6} is an honourable man, you've no right to speak of him thus.", "lord_event_choose_friend_defend", [
      (call_script, "script_change_player_relation_with_troop","$g_talk_troop",-10),
      (call_script, "script_change_player_relation_with_troop","$temp",5),
      ]],
  [anyone ,"lord_event_choose_friend_defend", [],  "As you like, {playername}.\
 A fool you might be, but a loyal fool at the least. {s6}'s loyalty may not be so steadfast, however...", "lord_pretalk", []],
#Post 0907 changes end
  
  [anyone|plyr ,"lord_event_choose_friend", [],  "I don't want to be involved in your quarrel with {s6}.", "lord_event_choose_friend_neutral", [
      (call_script, "script_change_player_relation_with_troop","$g_talk_troop",-2),
      (call_script, "script_change_player_relation_with_troop","$temp",-3),
      ]],

  [anyone ,"lord_event_choose_friend_neutral", [],  "Hmph. As you wish, {playername}.\
 Just remember that a {man/woman} needs friends in this world, and you'll never make any if you never stand with anyone.", "lord_pretalk", []],

#Meeting.

  [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     (check_quest_active, "qst_join_faction"),
                     (eq, "$g_invite_faction_lord", "$g_talk_troop"),
                     (try_begin),
                       (gt, "$g_invite_offered_center", 0),
                       (store_faction_of_party, ":offered_center_faction", "$g_invite_offered_center"),
                       (neq, ":offered_center_faction", "$g_talk_troop_faction"),
                       (call_script, "script_get_poorest_village_of_faction", "$g_talk_troop_faction"),
                       (assign, "$g_invite_offered_center", reg0),
                     (try_end),
                     ],
   #TODO: change conversations according to relation.
   "{playername}, I've been expecting you. Word has reached my ears of your exploits.\
 Why, I keep hearing such tales of prowess and bravery that my mind was quickly made up.\
 I knew that I had found someone worthy of becoming my vassal.", "lord_invite_1",
   []],


  [anyone|plyr ,"lord_invite_1", [],  "Thank you, {s65}, you honour me with your offer.", "lord_invite_2",  []],
  [anyone|plyr ,"lord_invite_1", [],  "It is good to have my true value recognised.", "lord_invite_2",  []],
   
  [anyone ,"lord_invite_2", [],  "Aye. Let us dispense with the formalities, {playername}; are you ready to swear homage to me?", "lord_invite_3",  []],
    
  [anyone|plyr ,"lord_invite_3", [],  "Yes, {s65}.", "lord_give_oath_2",  []],
  [anyone|plyr ,"lord_invite_3", [],  "No, {s65}. I cannot serve you right now.", "lord_enter_service_reject",  []],

  [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     (neq, "$g_talk_troop_met", 0),
                     (gt, "$g_time_since_last_talk", 24),
                     (gt, "$g_talk_troop_relation", 50),
                     (gt, "$g_talk_troop_faction_relation", 10),
                     (le,"$talk_context",tc_siege_commander),
                     ],
   "If it isn't my brave champion, {playername}...", "lord_start",  []],
  
  [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     (neq, "$g_talk_troop_met", 0),
                     (gt, "$g_time_since_last_talk", 24),
                     (gt, "$g_talk_troop_relation", 10),
                     (le,"$talk_context",tc_siege_commander),
                     ],
   "Good to see you again {playername}...", "lord_start", []],

  [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     (neq, "$g_talk_troop_met", 0),
                     (gt, "$g_time_since_last_talk", 24),
#                     (lt, "$g_talk_troop_faction_relation", 0),
                     (le,"$talk_context",tc_siege_commander),
                     ],
   "We meet again, {playername}...", "lord_start", []],

  [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     (eq, "$g_talk_troop_met", 0),
                     (ge, "$g_talk_troop_faction_relation", 0),
                     (le,"$talk_context",tc_siege_commander),
                     ],
   "Do I know you?", "lord_meet_neutral", []],
  [anyone|plyr ,"lord_meet_neutral", [],  "I am {playername}.", "lord_intro", []],
  [anyone|plyr ,"lord_meet_neutral", [],  "My name is {playername}. At your service sir.", "lord_intro", []],

  [anyone ,"lord_intro", [],
   "{s11}", "lord_start", [(faction_get_slot, ":faction_leader", "$g_talk_troop_faction", slot_faction_leader),
                          (str_store_faction_name, s6, "$g_talk_troop_faction"),
                          (assign, reg4, 0),
                          (str_store_troop_name, s4, "$g_talk_troop"),
                          (try_begin),
                            (eq, ":faction_leader", "$g_talk_troop"),
                            (str_store_string, s9, "@I am {s4}, the ruler of {s6}", 0),
                          (else_try),
                            (str_store_string, s9, "@I am {s4}, a vassal of {s6}", 0),
                          (try_end),
                          (assign, ":num_centers", 0),
                          (str_clear, s8),
                          (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
                            (party_slot_eq, ":cur_center", slot_town_lord, "$g_talk_troop"),
                            (try_begin),
                              (eq, ":num_centers", 0),
                              (str_store_party_name, s8, ":cur_center"),
                            (else_try),
                              (eq, ":num_centers", 1),
                              (str_store_party_name, s7, ":cur_center"),
                              (str_store_string, s8, "@{s7} and {s8}"),
                            (else_try),
                              (str_store_party_name, s7, ":cur_center"),
                              (str_store_string, s8, "@{s7}, {s8}"),
                            (try_end),
                            (val_add, ":num_centers", 1),
                          (try_end),
                          (assign, reg5, ":num_centers"),
                          (str_store_string, s11, "@{s9}{reg5? and the lord of {s8}.:.", 0),
                          ]],

#  [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
#                     (eq, "$g_talk_troop_met", 0),
#                     (ge, "$g_talk_troop_faction_relation", 0),
#                     (le,"$talk_context",tc_siege_commander),
#                     ],
#   "Who is this then?", "lord_meet_ally", []],
#  [anyone|plyr ,"lord_meet_ally", [],  "I am {playername} sir. A warrior of {s4}.", "lord_start", []],
#  [anyone|plyr ,"lord_meet_ally", [],  "I am but a soldier of {s4} sir. My name is {playername}.", "lord_start", []],

  [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     (eq, "$g_talk_troop_met", 0),
                     (lt, "$g_talk_troop_faction_relation", 0),
#                     (str_store_faction_name, s4,  "$players_kingdom"),
                     (le,"$talk_context",tc_siege_commander),
                     ],
   "{s43}", "lord_meet_enemy", [
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_enemy_meet_default"),
       ]],
  [anyone|plyr ,"lord_meet_enemy", [],  "I am {playername}, {s65}.", "lord_intro", []],  #A warrior of {s4}.
  [anyone|plyr ,"lord_meet_enemy", [],  "They know me as {playername}. Mark it down, you shall be hearing of me a lot.", "lord_intro", []],
#  [anyone, "lord_meet_enemy_2", [],  "{playername} eh? Never heard of you. What do want?", "lord_talk", []],

  [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     (le,"$talk_context",tc_siege_commander),
                     ],
   "Well, {playername}...", "lord_start",
   []],


  [anyone,"lord_start", [(gt, "$g_comment_found", 0), #changed to s32 from s62 because overlaps with setup_talk_info strings
                        ],  "{s42}", "lord_start", [
#                         (store_current_hours, ":cur_time"),
#                         (troop_set_slot, "$g_talk_troop", slot_troop_last_comment_time, ":cur_time"),
                         (try_begin),
                           (neq, "$log_comment_relation_change", 0),
                           (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", "$log_comment_relation_change"),
                         (try_end),
                         (assign, "$g_comment_found", 0),
                         ]],  


  
  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_lend_surgeon"),
                         (quest_slot_eq, "qst_lend_surgeon", slot_quest_giver_troop, "$g_talk_troop")],
   "Your surgeon managed to convince my friend and made the operation.  The matter is in God's hands now,, and all we can do is pray for his recovery.\
 Anyway, I thank you for lending your surgeon to me {sir/madam}. You have a noble spirit. I will not forget it.", "lord_generic_mission_completed",
   [
     (call_script, "script_finish_quest", "qst_lend_surgeon", 100),
     (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
     ]],
##### TODO: QUESTS COMMENT OUT BEGIN

##
##  [anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_bring_prisoners_to_enemy"),
##                         (quest_slot_eq, "qst_bring_prisoners_to_enemy", slot_quest_current_state, 0),
##                         (check_quest_succeeded, "qst_bring_prisoners_to_enemy"),
##                         (quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                         (assign, reg1, ":quest_target_amount")],
##   "TODO: You have brought the prisoners and received {reg1} denars. Give me the money now.", "lord_bring_prisoners_complete_2",[]],
##
##  [anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_bring_prisoners_to_enemy"),
##                         (quest_slot_eq, "qst_bring_prisoners_to_enemy", slot_quest_current_state, 1),#Some of them were brought only
##                         (check_quest_succeeded, "qst_bring_prisoners_to_enemy"),
##                         (quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                         (assign, reg1, ":quest_target_amount")],
##   "TODO: You have brought the prisoners but some of them died during your expedition. Give me the full money of {reg1} denars.", "lord_bring_prisoners_complete_2",[]],
##
##
##  [anyone|plyr,"lord_bring_prisoners_complete_2", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                                   (quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                                                   (ge, ":cur_gold", ":quest_target_amount")],
##   "TODO: Here it is.", "lord_generic_mission_thank", [(quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                                                  (troop_remove_gold, "trp_player", ":quest_target_amount"),
##                                                  (call_script, "script_finish_quest", "qst_bring_prisoners_to_enemy", 100)]],
##  
##  [anyone|plyr,"lord_bring_prisoners_complete_2", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                                   (quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                                                   (lt, ":cur_gold", ":quest_target_amount")],
##   "TODO: I'm afraid I spent some of it, I don't have that much money with me.", "lord_bring_prisoners_no_money", [(quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                                                                                                                   (call_script, "script_change_debt_to_troop", "$g_talk_troop", ":quest_target_amount"),#Adding the taken money as a debt
##                                                                                                                   (call_script, "script_finish_quest", "qst_bring_prisoners_to_enemy", 100)]],
##
##  [anyone,"lord_bring_prisoners_no_money", [],
##   "TODO: You owe me that money!", "lord_pretalk", []],
##
##
  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_incriminate_loyal_commander"),
                         (check_quest_succeeded, "qst_incriminate_loyal_commander"),
                         (quest_get_slot, ":quest_target_troop", "qst_incriminate_loyal_commander", slot_quest_target_troop),
                         (str_store_troop_name, s3, ":quest_target_troop"),
                         (quest_get_slot, reg5, "qst_incriminate_loyal_commander", slot_quest_gold_reward),
                         ],
   "Hah! Our little plot against {s3} worked perfectly, {playername}.\
 The fool has lost one of his most valuable retainers, and we are one step closer to bringing him to his knees.\
 Here, this purse contains {reg5} denars, and I wish you to have it. You deserve every copper.\
 And, need I remind you, there could be much more to come if you've a mind to earn it...", "lord_generic_mission_completed",[
     (call_script, "script_end_quest", "qst_incriminate_loyal_commander"),
     (call_script, "script_change_player_relation_with_troop","$g_talk_troop",5),
     (call_script, "script_change_player_honor", -10),
     ]],

  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_incriminate_loyal_commander"),
                         (check_quest_failed, "qst_incriminate_loyal_commander")],
   "You werent't able to complete a simple task. I had set up everything.\
 The only thing you needed to do was sacrifice a messenger, and we would be celebrating now.\
 But no, you were too damned honorable, weren't you?", "close_window",[
     (call_script, "script_end_quest", "qst_incriminate_loyal_commander"),
     (call_script, "script_change_player_relation_with_troop","$g_talk_troop",-5),
     (call_script, "script_change_player_honor", 3),
 ]],
  #TODO: NO GENERIC MISSION FAILED ANYMORE!!!!

  #TLD quests fail/success BEGIN:

    [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_investigate_fangorn"),
                         (check_quest_succeeded, "qst_investigate_fangorn"),
                         ],
   "So, {playername}, you return from Fangorn. What did you find out?", "lord_investigate_fangorn_completed0",[
     ]],
	 
	[anyone|plyr, "lord_investigate_fangorn_completed0",[],
	"The trees are alive! They assault our troops!","lord_investigate_fangorn_completed1",[] ],
	
	[anyone, "lord_investigate_fangorn_completed1",[],
	"ktnxbye","close_window",[
	(call_script, "script_end_quest", "qst_investigate_fangorn"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",5)] ],

  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_investigate_fangorn"),
                         (check_quest_failed, "qst_investigate_fangorn")],
   "My patience is over. \
   I was expecting you to tell me something about Fangorn by now, but you know nothing.", "close_window",[
   (call_script, "script_end_quest", "qst_investigate_fangorn"),
   (call_script, "script_change_player_relation_with_troop","$g_talk_troop",-5) 
   ]],
  
  #TLD quests fail/success END:
 
	 

  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_meet_spy_in_enemy_town"),
                         (check_quest_succeeded, "qst_meet_spy_in_enemy_town"),
                         ],
   "Have you brought me any news about that task I gave you? You know the one I mean...", "quest_meet_spy_in_enemy_town_completed",
   []],

  [anyone|plyr, "quest_meet_spy_in_enemy_town_completed", [],
   "I have the reports you wanted right here.", "quest_meet_spy_in_enemy_town_completed_2",[]],

  [anyone, "quest_meet_spy_in_enemy_town_completed_2", [],
   "Ahh, well done. It's good to have competent {men/people} on my side. Here is the payment I promised you.", "lord_pretalk",
   [
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
     (add_xp_as_reward, 500),
     (quest_get_slot, ":gold", "qst_meet_spy_in_enemy_town", slot_quest_gold_reward),
     (call_script, "script_troop_add_gold", "trp_player", ":gold"),
     (call_script, "script_end_quest", "qst_meet_spy_in_enemy_town"),
     ]],

  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_raid_caravan_to_start_war"),
                         (check_quest_succeeded, "qst_raid_caravan_to_start_war"),
                         (quest_get_slot, ":quest_target_faction", "qst_raid_caravan_to_start_war", slot_quest_target_faction),
                         (str_store_faction_name, s13, ":quest_target_faction"),
                         ],
   "Brilliant work, {playername}! Your caravan raids really got their attention, I must say.\
 I've just received word that {s13} has declared war!\
 Now the time has come for us to reap the benefits of our hard work, {playername}.\
 And by that I of course mean taking and plundering {s13} land!\
 This war is going to make us rich {men/souls}, mark my words!", "lord_pretalk",
   [
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 10),
    (try_for_range, ":vassal", kingdom_heroes_begin, kingdom_heroes_end),
      (store_troop_faction, ":vassal_fac", ":vassal"),
      (eq, ":vassal_fac", "$players_kingdom"),
      (neq,  ":vassal", "$g_talk_troop"),
      (store_random_in_range, ":rel_change", -5, 4),
      (call_script, "script_change_player_relation_with_troop", ":vassal", ":rel_change"),
    (try_end),
    #TODO: Add gold reward notification before the quest is given. 500 gold is not mentioned anywhere.
    (call_script, "script_troop_add_gold", "trp_player", 500),
    (add_xp_as_reward, 2000),
    (call_script, "script_change_player_honor", -5),
    (call_script, "script_end_quest", "qst_raid_caravan_to_start_war")
    ]],

  [anyone,"lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_raid_caravan_to_start_war"),
                         (check_quest_failed, "qst_raid_caravan_to_start_war"),
                         ],
   "You incompetent buffoon!\
 What in Hell made you think that getting yourself captured while trying to start a war was a good idea?\
 These plans took months to prepare, and now everything's been ruined! I will not forget this, {playername}.\
 Oh, be assured that I will not.", "lord_pretalk",
   [
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -10),
    (call_script, "script_end_quest", "qst_raid_caravan_to_start_war")
    ]],

  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_collect_debt"),
                         (quest_slot_eq, "qst_collect_debt", slot_quest_current_state, 1),
                         (quest_get_slot, ":target_troop", "qst_collect_debt", slot_quest_target_troop),
                         (str_store_troop_name, s7, ":target_troop"),
                         (quest_get_slot, ":total_collected","qst_collect_debt",slot_quest_target_amount),
                         (store_div, reg3, ":total_collected", 5),
                         (store_sub, reg4, ":total_collected", reg3)],
   "I'm told that you've collected the money owed me from {s7}. Good, it's past time I had it back.\
 I believe I promised to give you one-fifth of it all, eh?\
 Well, that makes {reg3} denars, so if you give me my share -- that's {reg4} denars -- you can keep the rest.", "lord_collect_debt_completed", []],

  
  [anyone|plyr,"lord_collect_debt_completed", [(store_troop_gold, ":gold", "trp_player"),
                                               (ge, ":gold", reg4)],
   "Of course, {s65}. {reg4} denars, all here.", "lord_collect_debt_pay",[]],

  [anyone,"lord_collect_debt_pay", [],
   "I must admit I'm impressed, {playername}. I had lost hope of ever getting this money back.\
 Please accept my sincere thanks.", "lord_pretalk",[
     (troop_remove_gold, "trp_player", reg4),
     (call_script, "script_change_player_relation_with_troop","$g_talk_troop",3),
     (add_xp_as_reward, 100),
     (call_script, "script_end_quest", "qst_collect_debt")
     ]],
  
  [anyone|plyr,"lord_collect_debt_completed", [], "I am afraid I don't have the money with me sir.", "lord_collect_debt_no_pay",[]],
  [anyone,"lord_collect_debt_no_pay", [], "Is this a joke?\
 I know full well that {s7} gave you the money, and I want every denar owed to me, {sir/madam}.\
 As far as I'm concerned, I hold you personally in my debt until I see that silver.", "close_window",[
     (call_script, "script_change_debt_to_troop", "$g_talk_troop", reg4),
     (call_script, "script_end_quest", "qst_collect_debt"),

     (call_script, "script_objectionable_action", tmt_honest, "str_squander_money"),
     ]],

  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_kill_local_merchant"),
                         (check_quest_succeeded, "qst_kill_local_merchant"),
                         (quest_slot_eq, "qst_kill_local_merchant", slot_quest_current_state, 1)],
   "I heard you got rid of that poxy merchant that was causing me so much grief.\
 I can see you're not afraid to get your hands dirty, eh? I like that in a {man/woman}.\
 Here's your reward. Remember, {playername}, stick with me and we'll go a long, long way together.", "close_window",
   [ (call_script, "script_troop_add_gold", "trp_player", 600),
     (call_script, "script_change_player_relation_with_troop","$g_talk_troop",4),
     (add_xp_as_reward, 300),
     (call_script, "script_end_quest", "qst_kill_local_merchant"),

     (call_script, "script_objectionable_action", tmt_humanitarian, "str_murder_merchant"), 
     
     (assign, "$g_leave_encounter", 1)]],

  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_kill_local_merchant"),
                         (check_quest_failed, "qst_kill_local_merchant")],
   "Oh, it's you. Enlighten me, how exactly does one lose a simple fight to some poxy, lowborn merchant?\
 Truly, if I ever need my guardsmen to take a lesson in how to lay down and die, I'll be sure to come to you.\
 Just leave me be, {playername}, I have things to do.", "close_window",
   [(call_script, "script_end_quest", "qst_kill_local_merchant"),
    (assign, "$g_leave_encounter", 1)]],

  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_kill_local_merchant"),
                         (check_quest_succeeded, "qst_kill_local_merchant"),
                         (quest_slot_eq, "qst_kill_local_merchant", slot_quest_current_state, 2)],
   "You! Do you have sawdust between your ears? Did you think that when I said to kill the merchant,\
 I meant you to have a nice chat with him and then let him go?! What possessed you?", "lord_kill_local_merchant_let_go",[]],

  [anyone|plyr,"lord_kill_local_merchant_let_go", [],
   "Sir, I made sure he will not act against you.", "lord_kill_local_merchant_let_go_2",[]],

  [anyone,"lord_kill_local_merchant_let_go_2", [],
   "Piffle. You were supposed to remove him, not give him a sermon and send him on his way.\
 He had better do as you say, or you'll both regret it.\
 Here, this is half the money I promised you. Don't say a word, {playername}, you're lucky to get even that.\
 I have little use for {men/people} who cannot follow orders.", "lord_pretalk",
   [(call_script, "script_troop_add_gold", "trp_player", 300),
     (call_script, "script_change_player_relation_with_troop","$g_talk_troop",2),
     (add_xp_as_reward, 500),
     (call_script, "script_end_quest", "qst_kill_local_merchant"),
     (assign, "$g_leave_encounter", 1)
    ]],

##  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_hunt_down_raiders"),
##                         (check_quest_failed, "qst_hunt_down_raiders")],
##   "I heard that those raiders you were after have got away. Do you have an explanation?", "quest_hunt_down_raiders_failed",[]],
##  [anyone|plyr,"quest_hunt_down_raiders_failed", [],  "They were too quick for us my lord. But next time we'll get them", "quest_hunt_down_raiders_failed_2",[]],
##  [anyone|plyr,"quest_hunt_down_raiders_failed", [],  "They were too strong and well armed my lord. But we'll be ready for them next time.", "quest_hunt_down_raiders_failed_2",[]],
##  
##  [anyone|plyr,"quest_hunt_down_raiders_failed", [],  "Well, it was a long call anyway. Next time do make sure that you are better prepared.",
##   "lord_pretalk",[(call_script, "script_end_quest", "qst_hunt_down_raiders")]],
##
##
##
##  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_hunt_down_raiders"),
##                         (check_quest_succeeded, "qst_hunt_down_raiders")],
##   "I heard that you have given those raiders the punishment they deserved. Well done {playername}.\
## ", "lord_generic_mission_completed",[(call_script, "script_finish_quest", "qst_hunt_down_raiders", 100),
##                                      (call_script, "script_change_player_relation_with_troop","$g_talk_troop",3)]],
##


##  [anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_defend_nobles_against_peasants"),
##                         (this_or_next|check_quest_succeeded, "qst_defend_nobles_against_peasants"),
##                         (check_quest_failed, "qst_defend_nobles_against_peasants"),
##                         (assign, ":num_saved", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##                         (party_count_companions_of_type, ":num_nobles", "p_main_party", "trp_noble_refugee"),
##                         (val_add, ":num_saved", ":num_nobles"),
##                         (party_count_companions_of_type, ":num_nobles", "p_main_party", "trp_noble_refugee_woman"),
##                         (val_add, ":num_saved", ":num_nobles"),
##                         (assign, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_saved"),
##                         (eq, ":num_saved", "$qst_defend_nobles_against_peasants_num_nobles_to_save")],
##   "TODO: You have saved all of them. Good boy.", "lord_generic_mission_completed",
##   [(party_remove_members, "p_main_party", "trp_noble_refugee", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##    (party_remove_members, "p_main_party", "trp_noble_refugee_woman", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##    (call_script, "script_finish_quest", "qst_defend_nobles_against_peasants", 100)]],
##
##  [anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_defend_nobles_against_peasants"),
##                         (this_or_next|check_quest_succeeded, "qst_defend_nobles_against_peasants"),
##                         (check_quest_failed, "qst_defend_nobles_against_peasants"),
##                         (assign, ":num_saved", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##                         (party_count_companions_of_type, ":num_nobles", "p_main_party", "trp_noble_refugee"),
##                         (val_add, ":num_saved", ":num_nobles"),
##                         (party_count_companions_of_type, ":num_nobles", "p_main_party", "trp_noble_refugee_woman"),
##                         (val_add, ":num_saved", ":num_nobles"),
##                         (assign, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_saved"),
##                         (lt, ":num_saved", "$qst_defend_nobles_against_peasants_num_nobles_to_save"),
##                         (gt, "$qst_defend_nobles_against_peasants_num_nobles_saved", 0)],
##   "TODO: You have saved some of them. Half good boy.", "lord_capture_conspirators_half_completed",
##   [(party_remove_members, "p_main_party", "trp_noble_refugee", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##    (party_remove_members, "p_main_party", "trp_noble_refugee_woman", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##    (assign, ":ratio", 100),
##    (val_mul, ":ratio", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##    (val_div, ":ratio", "$qst_defend_nobles_against_peasants_num_nobles_to_save"),
##    (call_script, "script_finish_quest", "qst_defend_nobles_against_peasants", ":ratio")]],
##
##  [anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_defend_nobles_against_peasants"),
##                         (this_or_next|check_quest_succeeded, "qst_defend_nobles_against_peasants"),
##                         (check_quest_failed, "qst_defend_nobles_against_peasants"),
##                         (assign, ":num_saved", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##                         (party_count_companions_of_type, ":num_nobles", "p_main_party", "trp_noble_refugee"),
##                         (val_add, ":num_saved", ":num_nobles"),
##                         (party_count_companions_of_type, ":num_nobles", "p_main_party", "trp_noble_refugee_woman"),
##                         (val_add, ":num_saved", ":num_nobles"),
##                         (eq, ":num_saved", 0)],
##   "TODO: You have saved none of them. Bad boy.", "lord_generic_mission_failed", []],
##
##
##  [anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_capture_conspirators"),
##                         (this_or_next|check_quest_succeeded, "qst_capture_conspirators"),
##                         (check_quest_failed, "qst_capture_conspirators"),
##                         (party_count_prisoners_of_type, ":num_conspirators", "p_main_party", "trp_conspirator"),
##                         (party_count_prisoners_of_type, ":num_conspirator_leaders", "p_main_party", "trp_conspirator_leader"),
##                         (store_add, ":sum_captured", ":num_conspirators", ":num_conspirator_leaders"),
##                         (ge, ":sum_captured", "$qst_capture_conspirators_num_troops_to_capture")],
##   "TODO: You have captured all of them. Good boy.", "lord_generic_mission_completed",
##   [(party_remove_prisoners, "p_main_party", "trp_conspirator_leader", "$qst_capture_conspirators_num_troops_to_capture"),
##    (party_remove_prisoners, "p_main_party", "trp_spy_partner", "$qst_capture_conspirators_num_troops_to_capture"),
##    (call_script, "script_finish_quest", "qst_capture_conspirators", 100)]],
##
##  [anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_capture_conspirators"),
##                         (this_or_next|check_quest_succeeded, "qst_capture_conspirators"),
##                         (check_quest_failed, "qst_capture_conspirators"),
##                         (party_count_prisoners_of_type, ":num_conspirators", "p_main_party", "trp_conspirator"),
##                         (party_count_prisoners_of_type, ":num_conspirator_leaders", "p_main_party", "trp_conspirator_leader"),
##                         (store_add, ":sum_captured", ":num_conspirators", ":num_conspirator_leaders"),
##                         (lt, ":sum_captured", "$qst_capture_conspirators_num_troops_to_capture"),
##                         (gt, ":sum_captured", 0)],
##   "TODO: You have captured some of them. Half good boy.", "lord_capture_conspirators_half_completed",
##   [(assign, ":sum_removed", 0),
##    (party_remove_prisoners, "p_main_party", "trp_conspirator_leader", "$qst_capture_conspirators_num_troops_to_capture"),
##    (val_add, ":sum_removed", reg0),
##    (party_remove_prisoners, "p_main_party", "trp_conspirator", "$qst_capture_conspirators_num_troops_to_capture"),
##    (val_add, ":sum_removed", reg0),
##    (val_mul, ":sum_removed", 100),
##    (val_div, ":sum_removed", "$qst_capture_conspirators_num_troops_to_capture"),
##    (call_script, "script_finish_quest", "qst_capture_conspirators", ":sum_removed")]],
##
##  [anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_capture_conspirators"),
##                         (this_or_next|check_quest_succeeded, "qst_capture_conspirators"),
##                         (check_quest_failed, "qst_capture_conspirators"),
##                         (party_count_prisoners_of_type, ":num_conspirators", "p_main_party", "trp_conspirator"),
##                         (party_count_prisoners_of_type, ":num_conspirator_leaders", "p_main_party", "trp_conspirator_leader"),
##                         (store_add, ":sum_captured", ":num_conspirators", ":num_conspirator_leaders"),
##                         (eq, ":sum_captured", 0)],
##   "TODO: You have captured none of them. Bad boy.", "lord_generic_mission_failed", []],
##
##  [anyone|plyr,"lord_capture_conspirators_half_completed", [],
##   "TODO: That's all I can do.", "lord_pretalk", []],


  [anyone,"lord_start", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
						 (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                         (store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_follow_spy"),
                         (eq, "$qst_follow_spy_no_active_parties", 1),
                         (party_count_prisoners_of_type, ":num_spies", "p_main_party", "trp_spy"),
                         (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", "trp_spy_partner"),
                         (gt, ":num_spies", 0),
                         (gt, ":num_spy_partners", 0)],
   "Beautiful work, {playername}! You captured both the spy and his handler, just as I'd hoped,\
 and the pair are now safely ensconced in my dungeon, waiting to be questioned.\
 My torturer shall be busy tonight! Anyway, I'm very pleased with your success, {playername}, and I give you\
 this purse as a token of my appreciation.", "lord_follow_spy_completed",
   [(party_remove_prisoners, "p_main_party", "trp_spy", 1),
    (party_remove_prisoners, "p_main_party", "trp_spy_partner", 1),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",4),
    (call_script, "script_troop_add_gold", "trp_player", 2000),
    (add_xp_as_reward, 4000),
    (call_script, "script_end_quest", "qst_follow_spy")]],

  [anyone,"lord_start", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
						 (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                         (store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_follow_spy"),
                         (eq, "$qst_follow_spy_no_active_parties", 1),
                         (party_count_prisoners_of_type, ":num_spies", "p_main_party", "trp_spy"),
                         (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", "trp_spy_partner"),
                         (gt, ":num_spies", 0),
                         (eq, ":num_spy_partners", 0),],
   "Blast and damn you! I wanted TWO prisoners, {playername} -- what you've brought me is one step short of\
 useless! I already know everything the spy knows, it was the handler I was after.\
 Here, half a job gets you half a reward. Take it and begone.", "lord_follow_spy_half_completed",
   [(party_remove_prisoners, "p_main_party", "trp_spy", 1),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",-1),
    (call_script, "script_troop_add_gold", "trp_player", 1000),
    (add_xp_as_reward, 400),
    (call_script, "script_end_quest", "qst_follow_spy")]],

  [anyone,"lord_start", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
					     (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                         (store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_follow_spy"),
                         (eq, "$qst_follow_spy_no_active_parties", 1),
                         (party_count_prisoners_of_type, ":num_spies", "p_main_party", "trp_spy"),
                         (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", "trp_spy_partner"),
                         (eq, ":num_spies", 0),
                         (gt, ":num_spy_partners", 0),
                         ],
   "I asked you for two prisoners, {playername}, not one. Two. Still, I suppose you did capture the spy's handler,\
 the more important one of the pair. The spy will not dare return here and will prove quite useless to\
 whatever master he served. 'Tis better than nothing.\
 However, you'll understand if I pay you half the promised reward for what is but half a success.", "lord_follow_spy_half_completed",
   [(party_remove_prisoners, "p_main_party", "trp_spy_partner", 1),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
    (call_script, "script_troop_add_gold", "trp_player", 1000),
    (add_xp_as_reward, 400),
    (call_script, "script_end_quest", "qst_follow_spy")]],

  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_follow_spy"),
                         (eq, "$qst_follow_spy_no_active_parties", 1),
                         (party_count_prisoners_of_type, ":num_spies", "p_main_party", "trp_spy"),
                         (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", "trp_spy_partner"),
                         (eq, ":num_spies", 0),
                         (eq, ":num_spy_partners", 0),
                         ],
   "Truly, {playername}, you are nothing short of totally incompetent.\
 Failing to capture both the spy AND his handler plumbs astonishing new depths of failure.\
 Forget any reward I offered you. You've done nothing to earn it.", "lord_follow_spy_failed",
   [
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",-2),
    (call_script, "script_end_quest", "qst_follow_spy"),
    ]],

  [anyone|plyr,"lord_follow_spy_half_completed", [],
   "I did my best, {s65}.", "lord_pretalk", []],

  [anyone|plyr,"lord_follow_spy_completed", [],
   "Thank you, {s65}.", "lord_pretalk", []],

  [anyone|plyr,"lord_follow_spy_failed", [],
   "Hrm. As you like, {s65}.", "lord_pretalk", []],


  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_bring_back_runaway_serfs"),
                         (check_quest_succeeded, "qst_bring_back_runaway_serfs")],
   "Damn me, but you've done it, {playername}. All the serfs are back and they're busy preparing for the harvest.\
 You certainly earned your reward. Here, take it, with my compliments.", "lord_generic_mission_completed",
   [(call_script, "script_change_player_relation_with_troop","$g_talk_troop",4),
    (call_script, "script_troop_add_gold", "trp_player", 300),
    (add_xp_as_reward, 300),
    (call_script, "script_end_quest", "qst_bring_back_runaway_serfs"),
    (call_script, "script_objectionable_action", tmt_humanitarian, "str_round_up_serfs"),
    ]],

  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_bring_back_runaway_serfs"),
                         (check_quest_failed, "qst_bring_back_runaway_serfs"),],
   "{playername}. I have been waiting patiently for my serfs, yet none have returned. Have you an explanation?\
 Were you outwitted by simple fieldhands, or are you merely incompetent?\
 Or perhaps you are plotting with my enemies, intending to ruin me...", "lord_bring_back_runaway_serfs_failed", []],
  [anyone|plyr,"lord_bring_back_runaway_serfs_failed", [],
   "Forgive me, {s65}, those serfs were slippery as eels.", "lord_bring_back_runaway_serfs_failed_1a", []],
  [anyone|plyr,"lord_bring_back_runaway_serfs_failed", [],
   "Perhaps if you had treated them better...", "lord_bring_back_runaway_serfs_failed_1b", []],
  [anyone,"lord_bring_back_runaway_serfs_failed_1a", [],
   "Hmph, that is hardly an excuse for failure, {playername}.\
 Now if you will excuse me, I need to recruit new men to work these fields before we all starve.", "lord_pretalk",
   [(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-1),
    (call_script, "script_end_quest", "qst_bring_back_runaway_serfs")]],
  [anyone,"lord_bring_back_runaway_serfs_failed_1b", [],
   "Hah, now you reveal your true colours, traitor! Your words match your actions all too well. I should never have trusted you.", "close_window",
   [(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-10),
    (quest_get_slot, ":home_village", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center",":home_village",6),
    (call_script, "script_end_quest", "qst_bring_back_runaway_serfs"),
    (assign, "$g_leave_encounter", 1),
    ]],

  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_bring_back_runaway_serfs"),
                         (check_quest_concluded, "qst_bring_back_runaway_serfs"),
                         (assign, reg17, "$qst_bring_back_runaway_serfs_num_parties_returned")],
   "You disappoint me, {playername}. There were 3 groups of serfs that I charged you to return. 3. Not {reg17}.\
 I suppose the ones who did come back shall have to work twice as hard to make up for those that got away.\
 As for your reward, {playername}, I'll only pay you for the serfs you returned, not the ones you let fly.\
 Here. Take it, and let this business be done.", "lord_runaway_serf_half_completed",
   [(store_mul, ":reward", "$qst_bring_back_runaway_serfs_num_parties_returned", 100),
    (val_div, ":reward", 2),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop","$qst_bring_back_runaway_serfs_num_parties_returned"),
    (call_script, "script_troop_add_gold", "trp_player", ":reward"),
    (add_xp_as_reward, ":reward"),


    (call_script, "script_objectionable_action", tmt_humanitarian, "str_round_up_serfs"),
    
    (call_script, "script_end_quest", "qst_bring_back_runaway_serfs"),
    ]],

  [anyone|plyr,"lord_runaway_serf_half_completed", [],
   "Thank you, {s65}. You are indeed generous.", "lord_pretalk", []],
  [anyone|plyr,"lord_runaway_serf_half_completed", [],
   "Bah, this proved to be a waste of my time.", "lord_pretalk", []],

  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_deal_with_bandits_at_lords_village"),
                         (check_quest_succeeded, "qst_deal_with_bandits_at_lords_village")],
   "{playername}, I was told that you have crushed the bandits at my village of {s5}. Please know that I am most grateful to you for that.\
 Please, let me pay the expenses of your campaign. Here, I hope these {reg14} denars will be adequate.", "lord_deal_with_bandits_completed",
   [
       (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
       (store_character_level, ":level", "trp_player"),
       (store_mul, ":reward", ":level", 20),
       (val_add, ":reward", 300),
       (call_script, "script_troop_add_gold", "trp_player", ":reward"),
       (add_xp_as_reward, 350),
       (call_script, "script_end_quest", "qst_deal_with_bandits_at_lords_village"),
       (assign, reg14, ":reward"),
       (quest_get_slot, ":village", "qst_deal_with_bandits_at_lords_village", slot_quest_target_center),
       (str_store_party_name, s5, ":village"),
       ]],

  [anyone|plyr, "lord_deal_with_bandits_completed", [],
   "Not a problem, {s65}.", "lord_pretalk",[]],
  [anyone|plyr, "lord_deal_with_bandits_completed", [],
   "Glad to be of service.", "lord_pretalk",[]],
  [anyone|plyr, "lord_deal_with_bandits_completed", [],
   "It was mere child's play.", "lord_pretalk",[]],

  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_deal_with_bandits_at_lords_village"),
                         (check_quest_concluded, "qst_deal_with_bandits_at_lords_village")],
   "Damn it, {playername}. I heard that you were unable to drive off the bandits from my village of {s5}, and thanks to you, my village now lies in ruins.\
 Everyone said that you were a capable warrior, but appearently, they were wrong.", "lord_pretalk",
   [
       (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -5),
       (call_script, "script_end_quest", "qst_deal_with_bandits_at_lords_village"),
       (quest_get_slot, ":village", "qst_deal_with_bandits_at_lords_village", slot_quest_target_center),
       (str_store_party_name, s5, ":village"),
       ]],


  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq, ":lords_quest", "qst_deliver_cattle_to_army"),
                         (check_quest_succeeded, "qst_deliver_cattle_to_army"),
                         (quest_get_slot, reg13, "qst_deliver_cattle_to_army", slot_quest_target_amount),
                         ],
   "Ah, {playername}. My quartermaster has informed me of your delivery, {reg13} heads of cattle, as I requested. I'm impressed.", "lord_deliver_cattle_to_army_thank",
   [
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
     (quest_get_slot, ":quest_target_amount", "qst_deliver_cattle_to_army", slot_quest_target_amount),
     #TODO: Change reward
     (store_mul, ":reward", ":quest_target_amount", 100),
     (call_script, "script_troop_add_gold", "trp_player", ":reward"),
     (val_div, ":reward", 5),
     (add_xp_as_reward, ":reward"),
     (call_script, "script_end_quest", "qst_deliver_cattle_to_army"),
     #Reactivating follow army quest
     (str_store_troop_name_link, s9, "$g_talk_troop"),
     (setup_quest_text, "qst_follow_army"),
     (str_store_string, s2, "@Your mission is complete, {s9} wants you to resume following his army until further notice."),
     (call_script, "script_start_quest", "qst_follow_army", "$g_talk_troop"),
     #(assign, "$g_player_follow_army_warnings", 0),
     ]],

  [anyone|plyr, "lord_deliver_cattle_to_army_thank", [],
   "Not a problem, {s65}.", "lord_pretalk",[]],
  [anyone|plyr, "lord_deliver_cattle_to_army_thank", [],
   "Glad to be of service.", "lord_pretalk",[]],
  [anyone|plyr, "lord_deliver_cattle_to_army_thank", [],
   "Mere child's play.", "lord_pretalk",[]],

  [anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq, ":lords_quest", "qst_scout_waypoints"),
                         (check_quest_succeeded, "qst_scout_waypoints"),
                         (str_store_party_name, s13, "$qst_scout_waypoints_wp_1"),
                         (str_store_party_name, s14, "$qst_scout_waypoints_wp_2"),
                         (str_store_party_name, s15, "$qst_scout_waypoints_wp_3"),
                         ],
   "You make a good scout, {playername}. My runner just brought me your reports of the mission to {s13}, {s14} and {s15}. Well done.", "lord_scout_waypoints_thank",
   [
     #TODO: Change reward
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
#     (call_script, "script_troop_add_gold", "trp_player", 100),
     (add_xp_as_reward, 100),
     (call_script, "script_end_quest", "qst_scout_waypoints"),
     #Reactivating follow army quest
     (str_store_troop_name_link, s9, "$g_talk_troop"),
     (setup_quest_text, "qst_follow_army"),
     (str_store_string, s2, "@Your mission is complete, {s9} wants you to resume following his army until further notice."),
     (call_script, "script_start_quest", "qst_follow_army", "$g_talk_troop"),
     #(assign, "$g_player_follow_army_warnings", 0),
     ]],

  [anyone|plyr, "lord_scout_waypoints_thank", [],
   "A simple task, {s65}.", "lord_pretalk",[]],
  [anyone|plyr, "lord_scout_waypoints_thank", [],
   "Nothing I couldn't handle.", "lord_pretalk",[]],
  [anyone|plyr, "lord_scout_waypoints_thank", [],
   "My pleasure, sir.", "lord_pretalk",[]],
  


  [anyone, "lord_start",
   [
     (check_quest_active, "qst_follow_army"),
     (faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"),
     (eq, "$g_random_army_quest", "qst_deliver_cattle_to_army"),
     (quest_get_slot, ":quest_target_amount", "$g_random_army_quest", slot_quest_target_amount),
     (assign, reg3, ":quest_target_amount"),
     ],
   "The army's supplies are dwindling too quickly, {playername}. I need you to bring me {reg3} heads of cattle so I can keep the troops fed. I care very little about where you get them, just bring them to me as soon as you can.", "lord_mission_told_deliver_cattle_to_army",
   [
   ]
   ],

  [anyone|plyr,"lord_mission_told_deliver_cattle_to_army", [], "Very well, I can find you some cattle.", "lord_mission_told_deliver_cattle_to_army_accepted",[]],
  [anyone|plyr,"lord_mission_told_deliver_cattle_to_army", [], "Sorry, sir, I have other plans.", "lord_mission_told_deliver_cattle_to_army_rejected",[]],

  [anyone,"lord_mission_told_deliver_cattle_to_army_accepted", [], "Excellent! You know what to do, {playername}, now get to it. I need that cattle sooner rather than later.", "close_window",
   [
     (call_script, "script_end_quest", "qst_follow_army"),
     (quest_get_slot, ":quest_target_amount", "$g_random_army_quest", slot_quest_target_amount),
     (str_store_troop_name_link, s13, "$g_talk_troop"),
     (assign, reg3, ":quest_target_amount"),
     (setup_quest_text, "$g_random_army_quest"),
     (str_store_string, s2, "@{s13} asked you to gather {reg3} heads of cattle and deliver them back to him."),
     (call_script, "script_start_quest", "$g_random_army_quest", "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter",1),
    ]],

  [anyone, "lord_mission_told_deliver_cattle_to_army_rejected", [], "That . . . is unfortunate, {playername}. I shall have to find someone else who's up to the task. Please go now, I've work to do.", "close_window",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    (assign, "$g_leave_encounter",1),]],
  


  [anyone,"lord_start",[(check_quest_active,"qst_report_to_army"),
                        (quest_slot_eq, "qst_report_to_army", slot_quest_target_troop, "$g_talk_troop"),
                        ],
   "Ah, you have arrived at last, {playername}. We've been expecting you. I hope you have brought with you troops of sufficient number and experience.", "lord_report_to_army_asked",
   []],

  [anyone|plyr,"lord_report_to_army_asked", [(quest_get_slot, ":quest_target_amount", "qst_report_to_army", slot_quest_target_amount),
                                             (call_script, "script_party_count_fit_for_battle", "p_main_party"),
                                             (gt, reg0, ":quest_target_amount"), # +1 for player
                                             ],
   "I have a company of good, hardened soldiers with me. We are ready to join you.", "lord_report_to_army_completed",
   []],

  [anyone|plyr,"lord_report_to_army_asked", [],
   "I don't have the sufficient number of troops yet. I will need some more time.", "lord_report_to_army_continue",
   []],

  [anyone,"lord_report_to_army_completed", [], "Excellent. I will send the word when I have a task for you. For the moment, just follow us and stay close. We'll be moving soon.", "close_window",[
     (call_script, "script_end_quest", "qst_report_to_army"),
     (quest_set_slot, "qst_report_to_army", slot_quest_giver_troop, "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
     #Activating follow army quest
     (str_store_troop_name_link, s9, "$g_talk_troop"),
     (setup_quest_text, "qst_follow_army"),
     (str_store_string, s2, "@{s9} wants you to follow his army until further notice."),
     (call_script, "script_start_quest", "qst_follow_army", "$g_talk_troop"),
     #(assign, "$g_player_follow_army_warnings", 0),
     (assign, "$g_leave_encounter", 1),
   ]],

  [anyone,"lord_report_to_army_continue", [], "Then you'd better hurry. We'll be moving out soon against the enemy and I need every able hand we can muster.", "close_window",
   [(assign, "$g_leave_encounter",1),
    #Must be closed because of not letting player to terminate this quest on the general conversation
    ]],


  [anyone, "lord_start",
   [
     (check_quest_active, "qst_follow_army"),
     (faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"),
     (eq, "$g_random_army_quest", "qst_scout_waypoints"),
     (str_store_party_name, s13, "$qst_scout_waypoints_wp_1"),
     (str_store_party_name, s14, "$qst_scout_waypoints_wp_2"),
     (str_store_party_name, s15, "$qst_scout_waypoints_wp_3"),
     ],
   "{playername}, I need a volunteer to scout the area. We're sorely lacking on information,\
 and I simply must have a better picture of the situation before we can proceed.\
 I want you to go to {s13}, {s14} and {s15} and report back whatever you find.", "lord_mission_told_scout_waypoints",
   [
   ]],

  [anyone|plyr, "lord_mission_told_scout_waypoints", [], "You've found your volunteer, sir.", "lord_mission_told_scout_waypoints_accepted",[]],
  [anyone|plyr, "lord_mission_told_scout_waypoints", [], "I fear I must decline.", "lord_mission_told_scout_waypoints_rejected",[]],

  [anyone,"lord_mission_told_scout_waypoints_accepted", [], "Good {man/lass}! Simply pass near {s13}, {s14} and {s15} and check out what's there. Make a note of anything you find and return to me as soon as possible.", "close_window",
   [
     (call_script, "script_end_quest", "qst_follow_army"),
     (str_store_troop_name_link, s9, "$g_talk_troop"),
     (str_store_party_name_link, s13, "$qst_scout_waypoints_wp_1"),
     (str_store_party_name_link, s14, "$qst_scout_waypoints_wp_2"),
     (str_store_party_name_link, s15, "$qst_scout_waypoints_wp_3"),
     (setup_quest_text, "$g_random_army_quest"),
     (str_store_string, s2, "@{s9} asked you to scout {s13}, {s14} and {s15}, then report back."),
     (call_script, "script_start_quest", "$g_random_army_quest", "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter",1),
    ]],

  [anyone,"lord_mission_told_scout_waypoints_rejected", [], "Hm. I'm disappointed, {playername}. Very disappointed. We'll talk later, I need to go and find somebody to scout for us.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],


  

##
##  [anyone,"lord_start",[(check_quest_active,"qst_rescue_lady_under_siege"),
##                        (quest_slot_eq, "qst_rescue_lady_under_siege", slot_quest_target_troop, "$g_talk_troop"),
##                        (quest_slot_eq, "qst_rescue_lady_under_siege", slot_quest_current_state, 1)],
##   "I heard that you have rescued my {s7} from the siege of {s5} and brought her to safety.\
## I am in your debt for this {playername}. Thank you.", "lord_generic_mission_completed",
##   [(quest_get_slot, ":quest_object_troop", "qst_rescue_lady_under_siege", slot_quest_object_troop),
##    (try_begin),
##      (troop_slot_eq, "$g_talk_troop", slot_troop_daughter, ":quest_object_troop"),
##      (str_store_string, s7, "str_daughter"),
##    (else_try),
##      (str_store_string, s7, "str_wife"),
##    (try_end),
##    (remove_member_from_party, ":quest_object_troop"),
##    (try_begin),
##      (is_between, "$g_encountered_party", centers_begin, centers_end),#Lord might be in wilderness
##      (troop_set_slot, ":quest_object_troop", slot_troop_cur_center, "$g_encountered_party"),
##    (try_end),
##    (call_script, "script_finish_quest", "qst_rescue_lady_under_siege", 100),
##    (call_script, "script_change_player_relation_with_troop","$g_talk_troop", 4),    
##    ]],
##
##### TODO: QUESTS COMMENT OUT END
  [anyone,"lord_generic_mission_thank", [],
   "You have been most helpful, {playername}. My thanks.", "lord_generic_mission_completed",[]],

  [anyone|plyr,"lord_generic_mission_completed", [],
   "It was an honour to serve.", "lord_pretalk",[]],

##  [anyone|plyr,"lord_generic_mission_failed", [],
##   "I'm sorry I failed you sir. It won't happen again.", "lord_pretalk",
##   [(store_partner_quest,":lords_quest"),
##    (call_script, "script_finish_quest", ":lords_quest"),
##    ]],
  
  [anyone,"lord_start", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                         (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                         (troop_get_slot, ":cur_debt", "$g_talk_troop", slot_troop_player_debt),
                         (gt, ":cur_debt", 0),
                         (assign, reg1, ":cur_debt")],
   "I think you owe me {reg1} denars, {playername}. Do you intend to pay your debt anytime soon?", "lord_pay_debt_2",[]],

  [anyone|plyr, "lord_pay_debt_2", [(troop_get_slot, ":cur_debt", "$g_talk_troop", slot_troop_player_debt),
                                    (store_troop_gold, ":cur_gold", "trp_player"),
                                    (le, ":cur_debt", ":cur_gold")],
   "That is why I came, {s65}. Here it is, every denar I owe you.", "lord_pay_debt_3_1", [(troop_get_slot, ":cur_debt", "$g_talk_troop", slot_troop_player_debt),
                                                   (troop_remove_gold, "trp_player", ":cur_debt"),
                                                   (troop_set_slot, "$g_talk_troop", slot_troop_player_debt, 0)]],

  [anyone|plyr, "lord_pay_debt_2", [],
   "Alas, I don't have sufficient funds, {s65}. But I'll pay you soon enough.", "lord_pay_debt_3_2", []],

  [anyone, "lord_pay_debt_3_1", [],
   "Ah, excellent. You are a {man/woman} of honour, {playername}. I am satisfied, yopur debt to me has been paid in full.", "lord_pretalk", []],

  [anyone, "lord_pay_debt_3_2", [],
   "Well, don't keep me waiting much longer.", "lord_pretalk", []],
   
  [anyone,"lord_start", [(party_slot_eq, "$g_encountered_party",slot_town_lord, "$g_talk_troop"),#we are talking to Town's Lord.
                         (ge,"$g_talk_troop_faction_relation",0),
                         (neq, "$g_ransom_offer_rejected", 1),
                         (lt, "$g_encountered_party_2", 0), #town is not under siege
                         (hero_can_join_as_prisoner, "$g_encountered_party"),
                         (store_random_in_range, ":random_no", 0, 100),
                         (lt, ":random_no", 10),#start this conversation with a 10% chance
                         (party_get_num_prisoner_stacks,":num_prisoner_stacks","p_main_party"),
                         (assign, "$prisoner_lord_to_buy", -1),
                         (try_for_range,":i_pris_stack",0,":num_prisoner_stacks"),
                           (party_prisoner_stack_get_troop_id, ":t_id", "p_main_party", ":i_pris_stack"),
                           (troop_slot_eq, ":t_id", slot_troop_occupation, slto_kingdom_hero),
                           (store_troop_faction, ":fac", ":t_id"),
                           (store_relation, ":rel", ":fac", "$g_talk_troop_faction"),
                           (lt,  ":rel", 0),
                           (assign, "$prisoner_lord_to_buy", ":t_id"),
                         (try_end),
                         (gt, "$prisoner_lord_to_buy", 0), #we have a prisoner lord.
                         (assign, ":continue", 1),
                         (try_begin),
                           (check_quest_active, "qst_capture_enemy_hero"),
                           (store_troop_faction, ":prisoner_faction", "$prisoner_lord_to_buy"),
                           (quest_slot_eq, "qst_capture_enemy_hero", slot_quest_target_faction, ":prisoner_faction"),
                           (assign, ":continue", 0),
                         (try_end),
                         (eq, ":continue", 1),
                         (str_store_troop_name, s3, "$prisoner_lord_to_buy"),
                         (assign, reg5, "$prisoner_lord_to_buy"),
                         (call_script, "script_calculate_ransom_amount_for_troop", "$prisoner_lord_to_buy"),
                         (assign, reg6, reg0),
                         (val_div, reg6, 2),
                         (assign, "$temp", reg6),
                         ],
   "I heard that you have captured our enemy {s3} and he is with you at the moment.\
 I can pay you {reg6} denars for him if you want to get rid of him.\
 You can wait for his family to pay his ransom of course, but there is no telling how long that will take, eh?\
", "lord_buy_prisoner", []],

  [anyone|plyr,"lord_buy_prisoner", [],
   "I accept your offer. I'll leave {s3} to you for {reg6} denars.", "lord_buy_prisoner_accept", []],
  [anyone|plyr,"lord_buy_prisoner", [],
   "I fear I can't accept your offer.", "lord_buy_prisoner_deny", [(assign, "$g_ransom_offer_rejected", 1),]],

  [anyone,"lord_buy_prisoner_accept", [],
   "Excellent! Here's your {reg6} denars.\
 I'll send some men to take him to our prison with due haste.", "lord_pretalk", [
     (remove_troops_from_prisoners,  "$prisoner_lord_to_buy", 1),
     (call_script, "script_troop_add_gold", "trp_player", "$temp"),
     (party_add_prisoners, "$g_encountered_party", "$prisoner_lord_to_buy", 1),
     #(troop_set_slot, "$prisoner_lord_to_buy", slot_troop_is_prisoner, 1),
     (troop_set_slot, "$prisoner_lord_to_buy", slot_troop_prisoner_of_party, "$g_encountered_party"),
     ]],

  [anyone,"lord_buy_prisoner_deny", [],
   "Mmm. As you wish, {playername}, but you'll not get a better offer. Take it from me.", "lord_pretalk", []],

  [anyone,"lord_start", [],
   "What is it?", "lord_talk",[]],

#  [anyone,"lord_start_2", [],
#   "Yes?", "lord_talk",[]],

  [anyone,"lord_pretalk", [],
   "Anything else?", "lord_talk",[]],
  
  [anyone,"hero_pretalk", [],
   "Anything else?", "lord_talk",[]],

##### TODO: QUESTS COMMENT OUT BEGIN

  [anyone|plyr,"lord_talk",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                            (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                            (check_quest_active,"qst_lend_companion"),
                            (quest_slot_eq, "qst_lend_companion", slot_quest_giver_troop, "$g_talk_troop"),
                            (store_current_day, ":cur_day"),
                            (quest_get_slot, ":quest_target_amount", "qst_lend_companion", slot_quest_target_amount),
                            (ge, ":cur_day", ":quest_target_amount"),
                            (quest_get_slot, ":quest_target_troop", "qst_lend_companion", slot_quest_target_troop),
                            (str_store_troop_name,s14,":quest_target_troop"),
                            (troop_get_type, reg3, ":quest_target_troop"),
                            ],
   "I should like {s14} returned to me, {s65}, if you no longer require {reg3?her:his} services.", "lord_lend_companion_end",
   []],

  [anyone,"lord_lend_companion_end",[(neg|hero_can_join, "p_main_party")],
   "You've too many men in your company already, {playername}. You could not lead any more at the moment.", "lord_pretalk",
   []],

  [anyone,"lord_lend_companion_end",[],
   "Certainly, {playername}. {reg3?She:He} is a bright {reg3?girl:fellow}, you're a lucky {man/woman} to have such worthy companions.", "lord_pretalk",
   [(quest_get_slot, ":quest_target_troop", "qst_lend_companion", slot_quest_target_troop),
    (party_add_members, "p_main_party", ":quest_target_troop", 1),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
    (add_xp_as_reward, 100),
    (call_script, "script_end_quest", "qst_lend_companion"),
    (str_store_troop_name,s14,":quest_target_troop"),
    (troop_get_type, reg3, ":quest_target_troop"),
    ]],
   
  [anyone|plyr,"lord_talk",[(check_quest_active,"qst_collect_debt"),
                            (quest_slot_eq,  "qst_collect_debt", slot_quest_current_state, 0),
                            (quest_get_slot, ":quest_target_troop", "qst_collect_debt", slot_quest_target_troop),
                            (eq,"$g_talk_troop",":quest_target_troop"),
                            (quest_get_slot, ":quest_giver_troop", "qst_collect_debt", slot_quest_giver_troop),
                            (str_store_troop_name,1,":quest_giver_troop")],
   "I've come to collect the debt you owe to {s1}.", "lord_ask_to_collect_debt",
   [(assign, "$g_convince_quest", "qst_collect_debt")]],

  [anyone,"lord_ask_to_collect_debt", [],  "Oh. Well, {s1} did lend me some silver a ways back,\
 but I've done him many favours in the past and I consider that money as my due payment.", "lord_ask_to_collect_debt_2",[]],
  [anyone|plyr,"lord_ask_to_collect_debt_2", [],  "{s1} considers it a debt. He asked me to speak to you on his behalf.", "convince_begin",[]],
  [anyone|plyr,"lord_ask_to_collect_debt_2", [],  "Then I will not press the matter any further.", "lord_pretalk",[]],


  [anyone,"convince_accept",[(check_quest_active, "qst_collect_debt"),
                             (quest_slot_eq, "qst_collect_debt", slot_quest_target_troop, "$g_talk_troop"),
                             (quest_get_slot, ":quest_giver_troop", "qst_collect_debt", slot_quest_giver_troop),
                             (str_store_troop_name,s8,":quest_giver_troop"),
                             (quest_get_slot, reg10, "qst_collect_debt", slot_quest_target_amount)],
   "My debt to {s8} has long been overdue and was a source of great discomfort to me.\
 Thank you for accepting to take the money to him.\
 Please give him these {reg10} denars and thank him on my behalf.", "close_window",
   [(call_script, "script_troop_add_gold", "trp_player", reg10),
    (quest_set_slot,  "qst_collect_debt", slot_quest_current_state, 1),
    (call_script, "script_succeed_quest", "qst_collect_debt"),
    (assign, "$g_leave_encounter", 1),
    ]],


  [anyone|plyr,"lord_talk",[(check_quest_active,"qst_persuade_lords_to_make_peace"),
                            (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
                            (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
                            (this_or_next|eq, ":quest_target_troop", "$g_talk_troop"),
                            (eq, ":quest_object_troop", "$g_talk_troop"),
                            (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
                            (quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
                            (str_store_faction_name, s12, ":quest_target_faction"),
                            (str_store_faction_name, s13, ":quest_object_faction"),
                            ],
   "Please, {s64}, it's time to end this war between {s12} and {s13}.", "lord_ask_to_make_peace",
   [(assign, "$g_convince_quest", "qst_persuade_lords_to_make_peace")]],

  [anyone,"lord_ask_to_make_peace", [], "Eh? I'm not sure I heard you right, {playername}.\
 War is not easily forgotten by either side of the conflict, and I have a very long memory.\
 Why should I take any interest in brokering peace with those dogs?", "lord_ask_to_make_peace_2",[]],

  [anyone|plyr,"lord_ask_to_make_peace_2", [],  "Perhaps I can talk you into it...", "convince_begin",[]],
  [anyone|plyr,"lord_ask_to_make_peace_2", [],  "Never mind, peace can wait for now.", "lord_pretalk",[]],

  [anyone,"convince_accept",[(check_quest_active, "qst_persuade_lords_to_make_peace"),
                             (this_or_next|quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, "$g_talk_troop"),
                             (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, "$g_talk_troop"),
                             (quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
                             (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
                             (str_store_faction_name, s12, ":quest_object_faction"),
                             (str_store_faction_name, s13, ":quest_target_faction"),
                             (try_begin), # store name of other faction
                               (eq,":quest_object_faction","$g_talk_troop_faction"),
                               (str_store_faction_name, s14, ":quest_target_faction"),
                               (else_try),
                               (str_store_faction_name, s14, ":quest_object_faction"),
                             (try_end),
                             ],
   "You... have convinced me, {playername}. Very well then, you've my blessing to bring a peace offer to {s14}. I cannot guarantee they will accept it, but on the off-chance they do, I will stand by it.", "close_window",
   [(store_mul, ":new_value", "$g_talk_troop", -1),
    (try_begin),
      (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, "$g_talk_troop"),
      (quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":new_value"),
    (else_try),
      (quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":new_value"),
    (try_end),
    (quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_convince_value, 1500),#reseting convince value for the second persuasion
    (assign, "$g_leave_encounter", 1),
    (neg|quest_slot_ge, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, 0),
    (neg|quest_slot_ge, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, 0),
    (call_script, "script_succeed_quest", "qst_persuade_lords_to_make_peace"),
    ]],


##
##
##  [anyone|plyr,"lord_talk",[(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                            (check_quest_active,"qst_bring_reinforcements_to_siege"),
##                             (quest_get_slot, ":quest_target_troop", "qst_bring_reinforcements_to_siege", slot_quest_target_troop),
##                             (eq,"$g_talk_troop",":quest_target_troop"),
##                             (quest_get_slot, ":quest_giver_troop", "qst_bring_reinforcements_to_siege", slot_quest_giver_troop),
##                             (quest_get_slot, ":quest_target_amount", "qst_bring_reinforcements_to_siege", slot_quest_target_amount),
##                             (quest_get_slot, ":quest_object_troop", "qst_bring_reinforcements_to_siege", slot_quest_object_troop),
##                             (party_count_companions_of_type, ":num_companions", "p_main_party", ":quest_object_troop"),
##                             (ge, ":num_companions", ":quest_target_amount"),
##                             (str_store_troop_name,1,":quest_giver_troop"),
##                             (assign, reg1, ":quest_target_amount"),
##                             (str_store_troop_name,2,":quest_object_troop")],
##   "Sir, {s1} ordered me to bring {reg1} {s2} to reinforce your siege.", "lord_reinforcement_brought",
##   [(quest_get_slot, ":quest_target_amount", "qst_bring_reinforcements_to_siege", slot_quest_target_amount),
##    (quest_get_slot, ":quest_target_party", "qst_bring_reinforcements_to_siege", slot_quest_target_party),
##    (quest_get_slot, ":quest_object_troop", "qst_bring_reinforcements_to_siege", slot_quest_object_troop),
##    (party_remove_members, "p_main_party", ":quest_object_troop", ":quest_target_amount"),
##    (party_add_members, ":quest_target_party", ":quest_object_troop", ":quest_target_amount"),
##    (call_script, "script_finish_quest", "qst_bring_reinforcements_to_siege", 100),
##    ]],
##
##  [anyone|plyr,"lord_talk",[(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                            (check_quest_active,"qst_bring_reinforcements_to_siege"),
##                             (quest_get_slot, ":quest_target_troop", "qst_bring_reinforcements_to_siege", slot_quest_target_troop),
##                             (eq,"$g_talk_troop",":quest_target_troop"),
##                             (quest_get_slot, ":quest_giver_troop", "qst_bring_reinforcements_to_siege", slot_quest_giver_troop),
##                             (quest_get_slot, ":quest_target_amount", "qst_bring_reinforcements_to_siege", slot_quest_target_amount),
##                             (quest_get_slot, ":quest_object_troop", "qst_bring_reinforcements_to_siege", slot_quest_object_troop),
##                             (party_count_companions_of_type, ":num_companions", "p_main_party", ":quest_object_troop"),
##                             (lt, ":num_companions", ":quest_target_amount"),
##                             (gt, ":num_companions", 0),
##                             (str_store_troop_name,1,":quest_giver_troop"),
##                             (assign, reg1, ":quest_target_amount"),
##                             (str_store_troop_name,2,":quest_object_troop")],
##   "Sir, {s1} ordered me to bring {reg1} {s2} as a reinforcement to your siege, but unfortunately I lost some of them during my expedition.", "lord_reinforcement_brought_some",
##   [(quest_get_slot, ":quest_target_amount", "qst_bring_reinforcements_to_siege", slot_quest_target_amount),
##    (quest_get_slot, ":quest_target_party", "qst_bring_reinforcements_to_siege", slot_quest_target_party),
##    (quest_get_slot, ":quest_object_troop", "qst_bring_reinforcements_to_siege", slot_quest_object_troop),
##    (party_count_companions_of_type, ":num_companions", "p_main_party", ":quest_object_troop"),
##    (party_remove_members, "p_main_party", ":quest_object_troop", ":num_companions"),
##    (party_add_members, ":quest_target_party", ":quest_object_troop", ":num_companions"),
##    (assign, ":percentage_completed", 100),
##    (val_mul, ":percentage_completed", ":num_companions"),
##    (val_div, ":percentage_completed", ":quest_target_amount"),
##    (call_script, "script_finish_quest", "qst_bring_reinforcements_to_siege", ":percentage_completed"),
##     ]],
##
##  [anyone,"lord_reinforcement_brought", [], "Well done {playername}. These men will no doubt be very useful. I will speak to {s1} of your help.", "lord_pretalk",[]],
##  [anyone,"lord_reinforcement_brought_some", [], "That's not quite good enough {playername}. But I suppose it is better than no reinforcements at all. Whatever, I'll tell {s1} you tried your best.", "lord_pretalk",[]],
##

  [anyone|plyr,"lord_talk",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                            (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                            (check_quest_active,"qst_duel_for_lady"),
                            (neg|check_quest_concluded,"qst_duel_for_lady"),
                            (quest_slot_eq, "qst_duel_for_lady", slot_quest_target_troop, "$g_talk_troop"),
                            (quest_get_slot, ":quest_giver_troop", "qst_duel_for_lady", slot_quest_giver_troop),
                            (str_store_troop_name,1,":quest_giver_troop")],
   "I want you to take back your accusations against {s1}.", "lord_challenge_duel_for_lady", []],
  [anyone,"lord_challenge_duel_for_lady", [], "What accusations?\
 Everyone knows that she beds her stable boys and anyone else she can lay hands on while her husband is away.\
 I merely repeat the words of many.", "lord_challenge_duel_for_lady_2",[]],
  [anyone|plyr,"lord_challenge_duel_for_lady_2", [], "You will recant these lies, sirrah, or prove them against my sword!", "lord_challenge_duel_for_lady_3",[]],
  [anyone|plyr,"lord_challenge_duel_for_lady_2", [], "If you say so...", "lord_pretalk",[]],
  [anyone,"lord_challenge_duel_for_lady_3", [], "You are challenging me to a duel? How droll!\
 As you wish, {playername}, it will be good sport to bash your head in.", "close_window",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -20),
    (assign, "$g_leave_encounter", 1),
    (try_begin),
      (is_between, "$g_encountered_party", towns_begin, towns_end),
      (party_get_slot, ":arena_scene", "$g_encountered_party", slot_town_arena),
    (else_try),
      (assign, ":closest_dist", 100000),
      (assign, ":closest_town", -1),
      (try_for_range, ":cur_town", towns_begin, towns_end),
        (store_distance_to_party_from_party, ":dist", ":cur_town", "p_main_party"),
        (lt, ":dist", ":closest_dist"),
        (assign, ":closest_dist", ":dist"),
        (assign, ":closest_town", ":cur_town"),
      (try_end),
      (party_get_slot, ":arena_scene", ":closest_town", slot_town_arena),
    (try_end),
    (modify_visitors_at_site, ":arena_scene"),
    (reset_visitors),
    (set_visitor, 0, "trp_player"),
    (set_visitor, 1, "$g_talk_troop"),
    (set_jump_mission, "mt_arena_challenge_fight"),
    (jump_to_scene, ":arena_scene"),
    (try_begin),
      (neq, "$talk_context", tc_court_talk),
      (jump_to_menu, "mnu_arena_duel_fight"),
    (try_end),
    ]],

  
  [anyone|plyr,"lord_talk",[(check_quest_active,"qst_deliver_message"),
                             (quest_get_slot, ":quest_target_troop", "qst_deliver_message", slot_quest_target_troop),
                             (eq,"$g_talk_troop",":quest_target_troop"),
                             (quest_get_slot, ":quest_giver_troop", "qst_deliver_message", slot_quest_giver_troop),
                             (str_store_troop_name,s9,":quest_giver_troop")],
   "I bring a message from {s9}.", "lord_message_delivered",
   []],

  [anyone,"lord_message_delivered", [], "Oh? Let me see that...\
 Well well well! It was good of you to bring me this, {playername}. Take my seal as proof that I've received it,\
 and give my regards to {s9} when you see him again.", "lord_pretalk",[
     (call_script, "script_end_quest", "qst_deliver_message"),
     (quest_get_slot, ":quest_giver", "qst_deliver_message", slot_quest_giver_troop),
     (str_store_troop_name,s9,":quest_giver"),
     (call_script, "script_change_player_relation_with_troop", ":quest_giver", 1),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
   ]],

  [anyone|plyr,"lord_talk",[(check_quest_active,"qst_deliver_message_to_enemy_lord"),
                            (quest_get_slot, ":quest_target_troop", "qst_deliver_message_to_enemy_lord", slot_quest_target_troop),
                            (eq,"$g_talk_troop",":quest_target_troop"),
                            (quest_get_slot, ":quest_giver_troop", "qst_deliver_message_to_enemy_lord", slot_quest_giver_troop),
                            (str_store_troop_name,s9,":quest_giver_troop")],
   "I bring a message from {s9}.", "lord_message_delivered_enemy",
   []],


  [anyone,"lord_message_delivered_enemy", [], "Oh? Let me see that...\
 Hmmm. It was good of you to bring me this, {playername}. Take my seal as proof that I've received it,\
 with my thanks.", "close_window",[
     (call_script, "script_end_quest", "qst_deliver_message_to_enemy_lord"),
     (quest_get_slot, ":quest_giver", "qst_deliver_message_to_enemy_lord", slot_quest_giver_troop),
     (call_script, "script_change_player_relation_with_troop", ":quest_giver", 3),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter", 1),
     ]],



  [anyone|plyr,"lord_talk", [(check_quest_active,"qst_deliver_message_to_prisoner_lord"),
                             (quest_slot_eq, "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop, "$g_talk_troop"),
                             (quest_get_slot, ":quest_giver_troop", "qst_deliver_message_to_prisoner_lord", slot_quest_giver_troop),
                             (str_store_troop_name, s11, ":quest_giver_troop")],
   "I bring a message from {s11}.", "lord_deliver_message_prisoner",
   [
     #TODO: Add reward
     (call_script, "script_end_quest", "qst_deliver_message_to_prisoner_lord"),
     ]],

  [anyone,"lord_deliver_message_prisoner", [], "Can it be true?\
 Oh, thank you kindly, {playername}! You have brought hope and some small ray of light to these bleak walls.\
 Perhaps one day I will be able to repay you.", "lord_deliver_message_prisoner_2",[]],
  [anyone|plyr,"lord_deliver_message_prisoner_2", [], " 'Twas the least I could do, {s65}.", "lord_deliver_message_prisoner_2a",[]],
  [anyone,"lord_deliver_message_prisoner_2a", [], "You've no idea how grateful I am, {playername}. A thousand thanks and more.", "close_window",[]],
  [anyone|plyr,"lord_deliver_message_prisoner_2", [], "Worry not, {s65}. You'll have ample opportunity once you are free again.", "lord_deliver_message_prisoner_2b",[]],
  [anyone,"lord_deliver_message_prisoner_2b", [], "Hah, of course, {playername}. My eternal thanks go with you.", "close_window",[]],

  [anyone|plyr,"lord_talk", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 1),
                             (troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             (check_quest_active,"qst_rescue_lord_by_replace"),
                             (quest_slot_eq, "qst_rescue_lord_by_replace", slot_quest_target_troop, "$g_talk_troop"),
                             (neg|check_quest_succeeded, "qst_rescue_lord_by_replace")],
   "Fear not, I am here to rescue you.", "lord_rescue_by_replace_offer",[]],
  [anyone,"lord_rescue_by_replace_offer", [],
   "By God, are you serious? What is your plan?", "lord_rescue_by_replace_offer_2",[]],
  [anyone|plyr,"lord_rescue_by_replace_offer_2", [],
   "A simple ruse, {s65}. If we exchange garments, I shall take your place here in prison,\
 while you make your escape disguised as myself.\
 I paid the guards a handsome bribe, with which I am sure they have already purchased half the wine stocks of the nearest tavern.\
 With some luck they'll soon get so drunk they'd have trouble\
 recognising their own mothers, let alone telling one of us from the other.\
 At least not until you are safely away.", "lord_rescue_by_replace_offer_3",[]],
  [anyone,"lord_rescue_by_replace_offer_3", [],
   "Hmm, it might just work... But what of you, my {friend/lady}? The guards won't take kindly to this trickery.\
 You may end up spending some time in this cell yourself.", "lord_rescue_by_replace_offer_4",[]],
  [anyone|plyr,"lord_rescue_by_replace_offer_4", [],
   "Not to worry, {s65}. The place is already starting to grow on me.", "lord_rescue_by_replace_offer_5a",[]],
  [anyone|plyr,"lord_rescue_by_replace_offer_4", [],
   "I shall be fine as long there is an ample reward waiting at the end.", "lord_rescue_by_replace_offer_5b",[]],
  [anyone,"lord_rescue_by_replace_offer_5a",[],
   "You are a brave soul indeed. I won't forget this.", "lord_rescue_by_replace_offer_6",[]],
  [anyone,"lord_rescue_by_replace_offer_5b",[],
   "Of course, my {friend/lady}, of course! Come to me when you have regained your freedom,\
 and perhaps I shall be able to repay the debt I owe you.", "lord_rescue_by_replace_offer_6",[]],
  [anyone|plyr,"lord_rescue_by_replace_offer_6",[],
   "Quickly, {s65}, let us change garments. It is past time you were away from here.", "close_window",
   [(call_script, "script_succeed_quest", "qst_rescue_lord_by_replace"),
    (quest_get_slot, ":quest_target_troop", "qst_rescue_lord_by_replace", slot_quest_target_troop),
    (quest_get_slot, ":quest_target_center", "qst_rescue_lord_by_replace", slot_quest_target_center),
    (party_remove_prisoners, ":quest_target_center", ":quest_target_troop", 1),
    #(troop_set_slot, ":quest_target_troop", slot_troop_is_prisoner, 0),
    (troop_set_slot, ":quest_target_troop", slot_troop_prisoner_of_party, -1),
    (assign, "$auto_menu", -1),
    (assign, "$capturer_party", "$g_encountered_party"),
    (jump_to_menu, "mnu_captivity_rescue_lord_taken_prisoner"),
    (finish_mission),
    ]],

##  
##  [anyone|plyr,"lord_talk", [(check_quest_active, "qst_deliver_message_to_lover"),
##                             (troop_get_slot, ":cur_daughter", "$g_talk_troop", slot_troop_daughter),
##                             (quest_slot_eq, "qst_deliver_message_to_lover", slot_quest_target_troop, ":cur_daughter"),
##                             (quest_get_slot, ":troop_no", "qst_deliver_message_to_lover", slot_quest_giver_troop),
##                             (str_store_troop_name, 3, ":troop_no"),
##                             (str_store_troop_name, 4, ":cur_daughter")],
##   "My lord, {s3} asked me to give this letter to your daughter, but I think you should read it first.", "lord_deliver_message_to_lover_tell_father",[]],
##
##  [anyone,"lord_deliver_message_to_lover_tell_father", [],
##   "That swine called {s3} is trying to approach my daughter eh? You have made the right decision by bringing this letter to me. I'll have a long talk with {s4} about it.", "lord_pretalk",
##   [(add_xp_as_reward, 200),
##    (call_script, "script_troop_add_gold", "trp_player", 1000),
##    (quest_get_slot, ":quest_giver", "qst_deliver_message_to_lover", slot_quest_giver_troop),
##    (quest_get_slot, ":target_troop", "qst_deliver_message_to_lover", slot_quest_target_troop),
##    (call_script, "script_change_player_relation_with_troop", ":quest_giver", -20),
##    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 10),
##    (call_script, "script_change_player_relation_with_troop", ":target_troop", -10),
##    (call_script, "script_end_quest", "qst_deliver_message_to_lover"),
##    #Adding betrayal to the quest giver
##    (troop_set_slot, ":quest_giver", slot_troop_last_quest, "qst_deliver_message_to_lover"),
##    (troop_set_slot, ":quest_giver", slot_troop_last_quest_betrayed, 1)]],
##
##
##### TODO: QUESTS COMMENT OUT END


  [anyone|plyr,"lord_talk", [(store_partner_quest,":lords_quest"),
                             (ge,":lords_quest",0),
                             ],
   "About the task you gave me...", "lord_active_mission_1",[]],


  [anyone|plyr,"lord_talk", [(faction_slot_eq,"$g_talk_troop_faction",slot_faction_leader, "$g_talk_troop"),
                             (eq, "$players_kingdom", "$g_talk_troop_faction"),
                             (eq, "$player_has_homage", 0),
                             (gt, "$mercenary_service_accumulated_pay", 0),
                             ],
   "{s67}, I humbly request the weekly payment for my service.", "lord_pay_mercenary",[]],

  [anyone,"lord_pay_mercenary", [(assign, reg8, "$mercenary_service_accumulated_pay")],
   "Hmm, let me see... According to my ledgers, we owe you {reg8} denars for your work. Here you are.", "lord_pay_mercenary_2",
   [(troop_add_gold, "trp_player", "$mercenary_service_accumulated_pay"),
    (assign, "$mercenary_service_accumulated_pay", 0)]],

  [anyone|plyr,"lord_pay_mercenary_2", [], "Thank you, sir.", "lord_pretalk", []],

  [anyone|plyr,"lord_talk", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             (ge, "$g_talk_troop_faction_relation", 0),
                             (store_partner_quest,":lords_quest"),
                             (lt,":lords_quest",0),
#                             (eq,"$g_talk_troop_faction","$players_kingdom")
                             ],
   "Do you have any tasks for me?", "lord_request_mission_ask",[]],

  #TLD Dain II Ironfoot dialogue (Kolba)

  [anyone|plyr,"lord_talk",[
                          (eq,"$g_talk_troop","trp_dwarf_lord"),
                          (check_quest_active,"qst_find_lost_spears"),
                          ],
   "Let me come into the dungeons","find_lost_spears_permission",[]],

  [anyone,"find_lost_spears_permission",[(ge, "$g_talk_troop_faction_relation", 0)],
   "Alright, go. Your relations with my faction are ok.","find_lost_spears_permission_yes",[]],

  [anyone,"find_lost_spears_permission",[],
   "Ye shall not go there. Your relations with my faction are bad.","find_lost_spears_permission_no",[]],

  [anyone,"find_lost_spears_permission_yes",[],
   "I thank you, my lord.","lord_pretalk",[(assign,"$dungeon_access",1)]],
                            


   #TLD - those oath options disabled for now, as no consequence menu is freezing game (Kolba)
                                                                                                                                                                                    
##  [anyone|plyr,"lord_talk", [(le,"$talk_context", tc_party_encounter),
##                             (ge, "$g_talk_troop_faction_relation", 0),
##                             #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
##                             (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
##                             (neq, "$players_kingdom", "$g_talk_troop_faction"),
##                             (store_partner_quest, ":lords_quest"),
##                             (neq, ":lords_quest", "qst_join_faction"),
##                            ],
##   "{s66}, I have come to offer you my sword in vassalage!", "lord_ask_enter_service",[]],
##
##
##  [anyone|plyr,"lord_talk", [(le,"$talk_context", tc_party_encounter),
##                             (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
##                             (eq, "$players_kingdom", "$g_talk_troop_faction"),
##                             (eq, "$player_has_homage", 0),
##                             (store_partner_quest, ":lords_quest"),
##                             (neq, ":lords_quest", "qst_join_faction"),
##                            ],
##   "{s66}, I wish to become your sworn {man/woman} and fight for your honour.", "lord_ask_enter_service",[]],
##
##  [anyone|plyr,"lord_talk", [(le,"$talk_context", tc_party_encounter),
##                             (ge, "$g_talk_troop_faction_relation", 0),
##                             #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
##                             (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
##                             (eq, "$players_kingdom", "$g_talk_troop_faction"),
##                             (eq, "$player_has_homage", 1),
##                            ],
##   "{s66}, I wish to be released from my oath to you.", "lord_ask_leave_service",[]],

    #TLD - oath options end (Kolba)
  

##  [anyone|plyr,"lord_talk", [(le,"$talk_context", tc_party_encounter),
##                             (ge, "$g_talk_troop_faction_relation", 0),
##                             (troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                             (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
##                             (eq, "$players_kingdom", 0),
##                             (eq,1,0)],
##   "TODO2:I want to fight alongside you against your enemies.", "close_window",[]],



  [anyone|plyr,"lord_talk", [(eq, 1, 0),(le,"$talk_context", tc_party_encounter),(ge, "$g_talk_troop_faction_relation", 0)],
   "I have an offer for you.", "lord_talk_preoffer",[]],

  
  [anyone|plyr,"lord_talk", [(eq, "$g_talk_troop_faction", "fac_player_supporters_faction"),
                             #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             ],
   "I want to give some troops to you.", "lord_give_troops",[]],

  [anyone,"lord_give_troops", [],
   "Well, I could use some good soldiers. Thank you.", "lord_pretalk",
   [
     (change_screen_give_members),
     ]],
  
  
  


  [anyone|plyr,"lord_talk",
   [
     (eq, "$g_talk_troop_faction", "$players_kingdom"),
     (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
     #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
     (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
     ],
   "I have a new task for you.", "lord_give_order_ask",[]],

  [anyone,"lord_give_order_ask", [],
   "Yes?", "lord_give_order",[]],




  [anyone|plyr,"lord_give_order", [],
   "Follow me.", "lord_give_order_answer",
   [
     (assign, "$temp", spai_accompanying_army),
     (assign, "$temp_2", "p_main_party"),
     ]],

  [anyone|plyr,"lord_give_order", [],
   "Go to...", "lord_give_order_details_ask",
   [
     (assign, "$temp", spai_holding_center),
     ]],

  [anyone|plyr,"lord_give_order", [],
   "Raid around the village of...", "lord_give_order_details_ask",
   [
     (assign, "$temp", spai_raiding_around_center),
     ]],

  [anyone|plyr,"lord_give_order", [],
   "Patrol around...", "lord_give_order_details_ask",
   [
     (assign, "$temp", spai_patrolling_around_center),
     ]],

  

  [anyone|plyr,"lord_give_order",
   [
     (neg|troop_slot_eq, "$g_talk_troop", slot_troop_player_order_state, spai_undefined),
     ],
   "I won't need you for some time. You are free to do as you like.", "lord_give_order_stop",
   []],

  [anyone|plyr,"lord_give_order", [],
   "Never mind.", "lord_pretalk",
   []],

  [anyone,"lord_give_order_details_ask", [],
   "Where?", "lord_give_order_details",[]],

  [anyone|plyr|repeat_for_parties, "lord_give_order_details",
   [
     (store_repeat_object, ":party_no"),
     (store_faction_of_party, ":party_faction", ":party_no"),
     (store_relation, ":relation", ":party_faction", "$players_kingdom"),
     (assign, ":continue", 0),
     (try_begin),
       (eq, "$temp", spai_holding_center),
       (try_begin),
         (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_castle),
         (party_slot_eq, ":party_no", slot_party_type, spt_town),
         (eq, ":party_faction", "$players_kingdom"),
         (assign, ":continue", 1),
       (try_end),
     (else_try),
       (eq, "$temp", spai_raiding_around_center),
       (try_begin),
         (party_slot_eq, ":party_no", slot_party_type, spt_village),
         (lt, ":relation", 0),
         (assign, ":continue", 1),
       (try_end),
     (else_try),
       (eq, "$temp", spai_patrolling_around_center),
       (try_begin),
         (eq, ":party_faction", "$players_kingdom"),
         (is_between, ":party_no", centers_begin, centers_end),
         (assign, ":continue", 1),
       (try_end),
     (try_end),
     (eq, ":continue", 1),
     (neq, ":party_no", "$g_encountered_party"),
     (str_store_party_name, s1, ":party_no")],
   "{s1}", "lord_give_order_answer",
   [
     (store_repeat_object, "$temp_2"),
     ]],

  [anyone|plyr, "lord_give_order_details",
   [], "Never mind.", "lord_pretalk",[]],



  [anyone,"lord_give_order_stop",
   [],
   "All right. I will do that.", "lord_pretalk",
   [
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_state, spai_undefined),
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_object, -1),
     (troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
     (try_begin),
       (gt, ":party_no", 0),
       (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
       (party_set_slot, ":party_no", slot_party_commander_party, -1),
     (try_end),
     ]],

  
  [anyone,"lord_give_order_answer",
   [
     (assign, ":continue", 0),
     (try_begin),
       (troop_slot_ge, "$g_talk_troop", slot_troop_readiness_to_follow_orders, 60),
       (assign, ":continue", 1),
     (else_try),
       (troop_slot_ge, "$g_talk_troop", slot_troop_readiness_to_follow_orders, 10),
       (neg|troop_slot_eq, "$g_talk_troop", slot_troop_player_order_state, spai_undefined),
       (assign, ":continue", 1),
     (try_end),
     (troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
     (this_or_next|le, ":party_no", 0),
     (eq, ":continue", 0),
     #Meaning that hero does not want to follow player orders for a while.
     ],
   "I am sorry. I need to attend my own business at the moment.", "lord_pretalk",
   [
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_state, spai_undefined),
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_object, -1),
     ]],

  [anyone|auto_proceed,"lord_give_order_answer",
   [],
   ".", "lord_give_order_answer_2",
   [
     (troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
     (call_script, "script_party_set_ai_state", ":party_no", "$temp", "$temp_2"),
     (try_begin),
       (eq, "$temp", spai_accompanying_army),
       (party_set_slot, ":party_no", slot_party_commander_party, "$temp_2"),
     (else_try),
       (party_set_slot, ":party_no", slot_party_commander_party, -1),
     (try_end),
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_state, "$temp"),
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_object, "$temp_2"),
     #Checking if the order is accepted by the ai
     (call_script, "script_recalculate_ai_for_troop", "$g_talk_troop"),
     ]],

  [anyone,"lord_give_order_answer_2",
   [
     (troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
     (party_slot_eq, ":party_no", slot_party_ai_state, "$temp"),
     (party_slot_eq, ":party_no", slot_party_ai_object, "$temp_2"),
     (assign, "$g_leave_encounter", 1),
     ],
   "I will do that.", "close_window",
   []],

  [anyone,"lord_give_order_answer_2",
   [
     #Meaning that the AI decision function did not follow the order.
     ],
   "I am sorry, it is not possible for me to do that.", "lord_pretalk",
   [
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_state, spai_undefined),
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_object, -1),
     ]],

  [anyone|plyr,"lord_talk",
   [
     (eq, "$g_talk_troop_faction", "$players_kingdom"),
     (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
     #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
     (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
     (faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_default),
     ],
   "I want to start a new campaign. Let us assemble the army here.", "lord_give_order_call_to_arms_verify",
   []],

  [anyone,"lord_give_order_call_to_arms_verify", [],
   "You wish to summon all lords for a new campaign?", "lord_give_order_call_to_arms_verify_2",[]],

  [anyone|plyr,"lord_give_order_call_to_arms_verify_2", [], "Yes. We must gather all our forces before we march on the enemy.", "lord_give_order_call_to_arms",[]],
  [anyone|plyr,"lord_give_order_call_to_arms_verify_2", [], "On second thought, it won't be necessary to summon everyone.", "lord_pretalk",[]],

  [anyone,"lord_give_order_call_to_arms",
   [],
   "All right then. I will send messengers and tell everyone to come here.", "lord_pretalk",
   [
     (faction_set_slot, "$players_kingdom", slot_faction_ai_state, sfai_gathering_army),
     (assign, "$g_recalculate_ais", 1),
     ]],

  [anyone|plyr,"lord_talk",
   [
     (eq, "$g_talk_troop_faction", "$players_kingdom"),
     (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
     #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
     (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
     (neg|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_default),
     ],
   "I want to end the campaign and let everyone return home.", "lord_give_order_disband_army_verify", []],

  [anyone,"lord_give_order_disband_army_verify", [],
   "You want to end the current campaign and release all lords from duty?", "lord_give_order_disband_army_2",[]],

  [anyone|plyr,"lord_give_order_disband_army_2", [], "Yes. We no longer need all our forces here.", "lord_give_order_disband_army",[]],
  [anyone|plyr,"lord_give_order_disband_army_2", [], "On second thought, it will be better to stay together for now.", "lord_pretalk",[]],

  [anyone,"lord_give_order_disband_army",
   [],
   "All right. I will let everyone know that they are released from duty.", "lord_pretalk",
   [
     (faction_set_slot, "$players_kingdom", slot_faction_ai_state, sfai_default),
     (try_for_range, ":cur_troop", kingdom_heroes_begin, kingdom_heroes_end),
       (troop_get_slot, ":party_no", ":cur_troop", slot_troop_leaded_party),
       (gt, ":party_no", 0),
       (party_slot_eq, ":party_no", slot_party_commander_party, "p_main_party"),
       (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
       (party_set_slot, ":party_no", slot_party_commander_party, -1),
     (try_end),
     (assign, "$g_recalculate_ais", 1),
     ]],

  [anyone|plyr,"lord_talk", [(ge, "$g_talk_troop_faction_relation", 0)],
   "I wish to ask you something.", "lord_talk_ask_something",[]],

  [anyone,"lord_talk_ask_something", [],
   "Aye? What is it?", "lord_talk_ask_something_2",[]],

  [anyone|plyr,"lord_talk_ask_something_2", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
  ],
   "I want to know the location of someone.", "lord_talk_ask_location",[]],

  [anyone|plyr,"lord_talk_ask_something_2", [],
   "What are you and your men doing?", "lord_tell_objective",[]],
  
  [anyone|plyr,"lord_talk_ask_something_2", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
											 (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
  ],
   "How goes the war?", "lord_talk_ask_about_war",[]],
  
  [anyone|plyr,"lord_talk_ask_something_2", [],
   "Never mind.", "lord_pretalk",[]],

  [anyone,"lord_talk_ask_location", [],
   "Very well, I may or may not have an answer for you. About whom do you wish to hear?", "lord_talk_ask_location_2",[]],

  [anyone|plyr|repeat_for_troops,"lord_talk_ask_location_2", [(store_repeat_object, ":troop_no"),
                                                              (neq, "$g_talk_troop", ":troop_no"),
                                                              (is_between, ":troop_no", heroes_begin, heroes_end),
                                                              (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                                                              (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
                                                              (store_troop_faction, ":faction_no", ":troop_no"),
                                                              (eq, "$g_encountered_party_faction", ":faction_no"),
                                                              (str_store_troop_name, s1, ":troop_no")],
   "{s1}", "lord_talk_ask_location_3",[(store_repeat_object, "$hero_requested_to_learn_location")]],

  [anyone|plyr,"lord_talk_ask_location_2", [], "Never mind.", "lord_pretalk",[]],

  [anyone,"lord_talk_ask_location_3",
   [
     (call_script, "script_update_troop_location_notes", "$hero_requested_to_learn_location", 1),
     (call_script, "script_get_information_about_troops_position", "$hero_requested_to_learn_location", 0),
     ],
   "{s1}", "lord_pretalk",[]],

  [anyone,"lord_talk_ask_about_war", [],
   "{s12}", "lord_talk_ask_about_war_2",[
                                          (assign, ":num_enemies", 0),
                                          (assign, ":num_theater_enemies", 0),
                                          (faction_get_slot, ":faction_theater", "$g_encountered_party_faction", slot_faction_active_theater),
                                          (try_for_range_backwards, ":cur_faction", kingdoms_begin, kingdoms_end),
                                            (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
                                            (store_relation, ":cur_relation", ":cur_faction", "$g_talk_troop_faction"),
                                            (lt, ":cur_relation", 0),
                                            (try_begin),
                                              (eq, ":num_enemies", 0),
                                              (str_store_faction_name_link, s12, ":cur_faction"),
                                            (else_try),
                                              (eq, ":num_enemies", 1),
                                              (str_store_faction_name_link, s11, ":cur_faction"),
                                              (str_store_string, s12, "@{s11} and {s12}"),
                                            (else_try),
                                              (str_store_faction_name_link, s11, ":cur_faction"),
                                              (str_store_string, s12, "@{s11}, {s12}"),
                                            (try_end),
                                            (val_add, ":num_enemies", 1),
                                            (faction_slot_eq, ":cur_faction", slot_faction_active_theater, ":faction_theater"),
                                            (try_begin),
                                              (eq, ":num_theater_enemies", 0),
                                              (str_store_faction_name_link, s13, ":cur_faction"),
                                            (else_try),
                                              (eq, ":num_theater_enemies", 1),
                                              (str_store_faction_name_link, s11, ":cur_faction"),
                                              (str_store_string, s13, "@{s11} and {s13}"),
                                            (else_try),
                                              (str_store_faction_name_link, s11, ":cur_faction"),
                                              (str_store_string, s13, "@{s11}, {s13}"),
                                            (try_end),
                                            (val_add, ":num_theater_enemies", 1),
                                          (try_end),
                                          (try_begin),
                                            (eq, ":num_enemies", 0),
                                            (str_store_string, s12, "@We are not at war with anyone."),
                                          (else_try),
                                            (try_begin),
                                              (gt, ":num_theater_enemies", 0),
                                              (str_store_string, s12, "@We are at war with {s12}. However, we are mostly fighting against {s13}."),
                                            (else_try),
                                              (str_store_string, s12, "@We are at war with {s12}. However, there are only skirmishes at the moment."),
                                            (try_end),
                                          (try_end),
                                          ]],

  [anyone|plyr|repeat_for_factions, "lord_talk_ask_about_war_2", [(store_repeat_object, ":faction_no"),
                                                                  (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
                                                                  (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
                                                                     (store_relation, ":cur_relation", ":faction_no", "$g_talk_troop_faction"),
                                                                     (lt, ":cur_relation", 0),
                                                                     (str_store_faction_name, s1, ":faction_no")],
   "Tell me more about the war with {s1}.", "lord_talk_ask_about_war_details",[(store_repeat_object, "$faction_requested_to_learn_more_details_about_the_war_against")]],

  [anyone|plyr,"lord_talk_ask_about_war_2", [], "That's all I wanted to know. Thank you.", "lord_pretalk",[]],

  [anyone,"lord_talk_ask_about_war_details", [],
   "We are {s22} and they are {s23}. Overall, {s9}.",
   "lord_talk_ask_about_war_2",[(call_script, "script_faction_strength_string", "$g_encountered_party_faction"),
                                (str_store_string_reg, s22, s23),
                                (call_script, "script_faction_strength_string", "$faction_requested_to_learn_more_details_about_the_war_against"),
                                (faction_get_slot, ":faction_theater", "$g_encountered_party_faction", slot_faction_active_theater),
                                (try_begin),
                                  (faction_slot_eq, "$faction_requested_to_learn_more_details_about_the_war_against", slot_faction_active_theater, ":faction_theater"),
                                  (faction_get_slot, ":our_str", "$g_encountered_party_faction", slot_faction_strength),
                                  (faction_get_slot, ":enemy_str", "$faction_requested_to_learn_more_details_about_the_war_against", slot_faction_strength),
                                  (store_sub, ":advantage", ":our_str", ":enemy_str"), #-7000 to +7000
                                  (val_div, ":advantage", 1200), # -5 to +5
                                  (val_clamp, ":advantage", -4, 5), # -4 to +4
                                  (val_add, ":advantage", 4),
                                  (store_add, ":adv_str", "str_war_report_minus_4", ":advantage"),
                                  (str_store_string, s9, ":adv_str"),
                                (else_try),
                                  (str_store_string, s9, "@we are not too concerned with them at the moment, since we are fighting other enemies closer to home"),
                                (try_end),
                                ]],


  [anyone|plyr,"lord_talk", [(eq,"$talk_context",tc_party_encounter),
                             (lt, "$g_encountered_party_relation", 0),
                             (str_store_troop_name,s4,"$g_talk_troop")],
   "I say this only once, {s4}! Surrender or die!", "party_encounter_lord_hostile_ultimatum_surrender", []],
  [anyone,"party_encounter_lord_hostile_ultimatum_surrender", [],
   "{s43}", "close_window", [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_challenged_default"),
       (call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),
       (try_begin),
         (gt, "$g_talk_troop_relation", -10),
         (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
       (try_end),
       (assign,"$encountered_party_hostile",1)]],


  [anyone|plyr,"lord_talk", [(eq,"$talk_context", tc_party_encounter),
                             (neq,"$g_encountered_party_faction","$players_kingdom"),
                             (ge, "$g_encountered_party_relation", 0),
                                 ], "I'm here to deliver you my demands!", "lord_predemand",[]],
  [anyone,"lord_predemand", [], "Eh? What do you want?", "lord_demand",[]],

  [anyone|plyr,"lord_demand", [(neq,"$g_encountered_party_faction","$players_kingdom"),
                               (ge, "$g_encountered_party_relation", 0),], "I offer you one chance to surrender or die.", "lord_ultimatum_surrender",[]],

  [anyone,"lord_ultimatum_surrender", [(ge, "$g_encountered_party_relation", 0)], "{s43}", "lord_attack_verify",[#originally, speak you rascal
        (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_unprovoked_attack_default"),
      ]],
  
  [anyone|plyr,"lord_attack_verify", [], "Forgive me sir. I don't know what I was thinking.", "lord_attack_verify_cancel",[]],
  [anyone,"lord_attack_verify_cancel", [], "Be gone, then.", "close_window",[(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),(assign, "$g_leave_encounter",1)]],
  [anyone|plyr,"lord_attack_verify", [], "That is none of your business. Prepare to fight!", "lord_attack_verify_commit",[]],

  [anyone,"lord_ultimatum_surrender", [], "{s43}", "lord_attack_verify_b", #originally, you will not survive this
   [
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_unnecessary_attack_default"),
    (call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -5),
    ]],

  [anyone|plyr,"lord_attack_verify_b", [],  "Forgive me sir. I don't know what I was thinking.", "lord_attack_verify_cancel",[]],
  [anyone|plyr,"lord_attack_verify_b", [],   "I stand my ground. Prepare to fight!", "lord_attack_verify_commit",[]],

  [anyone,"lord_attack_verify_commit", [], "{s43}", "close_window",
   [
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_challenged_default"),
    (call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -3),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -30),
    ]],
#Post 0907 changes end
  
  [anyone|plyr,"lord_demand", [], "Forgive me. It's nothing.", "lord_pretalk",[]],


##  [anyone|plyr,"lord_talk", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                             (ge, "$g_talk_troop_faction_relation", 0),
##                             ],
##   "I wish to ask for a favor.", "lord_ask_for_favor_ask",[]],



  [anyone|plyr,"lord_talk", [
                            (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                            (troop_slot_eq, "$g_talk_troop", slot_troop_discussed_rebellion, 0),                      
                            (assign, ":pretender", 0),
                            (try_for_range, ":possible_pretender", pretenders_begin, pretenders_end),
                                (troop_slot_eq, ":possible_pretender", slot_troop_original_faction, "$g_talk_troop_faction"),
                                (assign, ":pretender", ":possible_pretender"),
                            (try_end),
                            (troop_slot_ge, ":pretender", slot_troop_met, 1),
                            (str_store_troop_name, s45, ":pretender"),
                            (troop_get_type, reg3, ":pretender"),
                             ],
   "I have met in my travels one who calls {reg3?herself:himself} {s45}...", "liege_defends_claim_1",[
       ]],

  [anyone,"liege_defends_claim_1", [],
   "Oh really? It is not everyone who dares mention that name in my presence. I am not sure whether to reward your bravery, or punish you for your impudence.", "liege_defends_claim_2", [
                            (troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
                    ]],

  [anyone,"liege_defends_claim_2", [],
   "Very well. I will indulge your curiosity. But listen closely, because I do not wish to speak of this matter again.", "liege_defends_claim_3", [
                    ]],

  [anyone,"liege_defends_claim_3", [],
   "{s48}", "liege_defends_claim_4", [
                     (store_sub, ":rebellion_string", "$g_talk_troop_faction", "fac_gondor"),                                
                     (val_add, ":rebellion_string", "str_swadian_rebellion_monarch_response_1"),
                     (str_store_string, 48, ":rebellion_string"),
                     ]],

  [anyone,"liege_defends_claim_4", [],
   "{s48}", "lord_talk", [
                     (store_sub, ":rebellion_string", "$g_talk_troop_faction", "fac_gondor"),                                
                     (val_add, ":rebellion_string", "str_swadian_rebellion_monarch_response_2"),
                     (str_store_string, 48, ":rebellion_string"),
                     ]],


#Rebellion changes begin
  [anyone|plyr,"lord_talk", [
                             (gt, "$supported_pretender", 0),
                             (eq, "$supported_pretender_old_faction", "$g_talk_troop_faction"),
#                             (is_between, "$players_kingdom", rebel_factions_begin, rebel_factions_end),
#                             (faction_slot_eq, "$players_kingdom", slot_faction_rebellion_target, "$g_talk_troop_faction"),
                             (troop_slot_eq, "$g_talk_troop", slot_troop_discussed_rebellion, 0),
                             (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                             (troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1),
                             (str_store_troop_name, s12, "$supported_pretender"),
                             (str_store_faction_name, s14, "$supported_pretender_old_faction"),
                             (faction_get_slot, ":old_faction_lord", "$supported_pretender_old_faction", slot_faction_leader),
                             (str_store_troop_name, s15, ":old_faction_lord"),
                             ],
   "{s12} is the rightful ruler of {s14}. Join our cause against the usurper, {s15}!", "lord_join_rebellion_suggest",[]],
  [anyone|plyr,"lord_talk",
   [
     (eq, "$cheat_mode", 1),
     (gt, "$supported_pretender", 0),
     (eq, "$supported_pretender_old_faction", "$g_talk_troop_faction"),
     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
     (troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1),
     ],
   "CHEAT: Join our cause by force.", "lord_join_rebellion_suggest_cheat",[]],

  [anyone|plyr,"party_encounter_lord_hostile_attacker_2",
   [
     (eq, "$cheat_mode", 1),
     (gt, "$supported_pretender", 0),
     (eq, "$supported_pretender_old_faction", "$g_talk_troop_faction"),
     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
     (troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1),
     ],
   "CHEAT: Join our cause by force.", "lord_join_rebellion_suggest_cheat",[]],

  [anyone,"lord_join_rebellion_suggest_cheat",
   [], "Cheat:Allright.",
   "lord_join_rebellion_ask_for_order",
   [
     (troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
     (call_script, "script_change_troop_faction", "$g_talk_troop", "$players_kingdom"),
     (assign, "$g_leave_encounter", 1),
     ]],

  [anyone|plyr,"party_encounter_lord_hostile_attacker_2", [
                             (gt, "$supported_pretender", 0),
                             (eq, "$supported_pretender_old_faction", "$g_talk_troop_faction"),
#                             (is_between, "$players_kingdom", rebel_factions_begin, rebel_factions_end),
#                             (faction_slot_eq, "$players_kingdom", slot_faction_rebellion_target, "$g_talk_troop_faction"),
                             (troop_slot_eq, "$g_talk_troop", slot_troop_discussed_rebellion, 0),
                             (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                             (troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1),
                             (str_store_troop_name, s12, "$supported_pretender"),
                             (str_store_faction_name, s14, "$supported_pretender_old_faction"),
                             (faction_get_slot, ":old_faction_lord", "$supported_pretender_old_faction", slot_faction_leader),
                             (str_store_troop_name, s15, ":old_faction_lord"),
                             ],
   "{s12} is your rightful ruler. Join our cause against the usurper, {s15}!", "lord_join_rebellion_suggest",[]],


  [anyone,"lord_join_rebellion_suggest", [
                    (eq,"$talk_context",tc_party_encounter),
                    (encountered_party_is_attacker),
                    (lt, "$g_talk_troop_relation", -5),
      ], "I have no time to bandy words with the likes of you. Now defend yourself!",
   "party_encounter_lord_hostile_attacker_2",
   [
        (troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
    ]],

  [anyone,"lord_join_rebellion_suggest", [
                (lt, "$g_talk_troop_relation", -10),
      ], "I have no time to bandy words with the likes of you.", "lord_start",
   [
        (troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
    ]],

  [anyone,"lord_join_rebellion_suggest",
   [
     (assign, "$g_rebellion_suggest_friends_stronger", 0),
     (call_script, "script_init_ai_calculation"), #recalculating friend and enemy strengths
     (troop_get_slot, ":leaded_party", "$g_talk_troop", slot_troop_leaded_party),
     (gt, ":leaded_party", 0),
     (party_get_slot, ":friend_strength", ":leaded_party", slot_party_nearby_friend_strength),
     (party_get_slot, ":enemy_strength", ":leaded_party", slot_party_nearby_enemy_strength),
     (party_get_slot, ":cached_strength", ":leaded_party", slot_party_cached_strength),
     (val_sub, ":friend_strength", ":cached_strength"),
     (val_add, ":enemy_strength", ":cached_strength"),
     (gt, ":friend_strength", ":enemy_strength"),
     (assign, "$g_rebellion_suggest_friends_stronger", 1),
     (encountered_party_is_attacker),
     ], "{s43}", "party_encounter_lord_hostile_attacker_2", #This is hardly the time or the place for such a discussion.
   [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_talk_later_default"),
    ]],

  [anyone,"lord_join_rebellion_suggest",
   [
    (eq, "$g_rebellion_suggest_friends_stronger", 1),
    ], "{s43}", "lord_start",
   [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_talk_later_default"),
    ]],

  [anyone,"lord_join_rebellion_suggest", [
              ], "{s43}", "lord_join_rebellion_suggest_1b",
   [

       (troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1),

       (faction_get_slot, ":pretender", "$players_kingdom", slot_faction_leader),
       (troop_get_type, reg3, ":pretender"),
       (faction_get_slot, ":current_ruler", "$g_talk_troop_faction", slot_faction_leader),

       (str_store_troop_name, 45, ":pretender"),
       (str_store_troop_name, 46, ":current_ruler"),

       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_rebellion_dilemma_default"),
       (call_script, "script_find_rival_from_faction", "$g_talk_troop", "$players_kingdom"),
       (assign, "$rival_lord", reg0),
       (assign, "$rebellion_chance", 40),

       (assign, "$prior_argument_value", 0),

       (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_claim),
       (store_mul, ":prior_claim", reg0, "$player_made_legitimacy_claim"),
       (val_add, "$prior_argument_value", ":prior_claim"),        

       (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_ruler),
       (store_mul, ":prior_claim", reg0, "$player_made_ruler_claim"),
       (val_add, "$prior_argument_value", ":prior_claim"),        

       (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_victory),
       (store_mul, ":prior_claim", reg0, "$player_made_strength_claim"),
       (val_add, "$prior_argument_value", ":prior_claim"),        

       (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_benefit),
       (store_mul, ":prior_claim", reg0, "$player_made_benefit_claim"),
       (val_add, "$prior_argument_value", ":prior_claim"),        

       (val_div, "$prior_argument_value", 5),



    ]],

  [anyone,"lord_join_rebellion_suggest_1b", [
              ], "{s43}", "lord_join_rebellion_suggest_2",
   [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_rebellion_dilemma_2_default"),

]],



#Mentions prior arguments
  [anyone,"lord_join_rebellion_suggest_2", [
            (neq, "$prior_argument_value", 0),
      ], "{s47}", "lord_join_rebellion_suggest_2",
   [

           (try_begin),
                (gt, "$prior_argument_value", 10),
                (str_store_string, s47, "str_rebellion_prior_argument_very_favorable"),
                (str_store_string, s49, "str_but_comma_3"),
           (else_try),
                (gt, "$prior_argument_value", 0),
                (str_store_string, s47, "str_rebellion_prior_argument_favorable"),
                (str_store_string, s49, "str_but_comma_3"),
           (else_try),
                (is_between, "$prior_argument_value", -10, 0),
                (str_store_string, s47, "str_rebellion_prior_argument_unfavorable"),
                (str_store_string, s49, "str_and_comma_3"),
           (else_try),
                (lt, "$prior_argument_value", -10),
                (str_store_string, s47, "str_rebellion_prior_argument_very_unfavorable"),
                (str_store_string, s49, "str_and_comma_3"),
           (try_end),

            (val_add, "$rebellion_chance", "$prior_argument_value"),

            (assign, reg6, "$prior_argument_value"), #diagnostic only
            (assign, "$prior_argument_value", 0),

            (assign, reg7, "$rebellion_chance"), #diagnostic only
            (display_message, "@Prior argument effect: {reg6}, rebellion chance: {reg7}"),#diagnostic only

    ]],

#Mentions rivals
  [anyone,"lord_join_rebellion_suggest_2", [
            (gt, "$rival_lord", 0),
      ], "{s43}", "lord_join_rebellion_suggest_2",
   [
            (str_store_troop_name, 44, "$rival_lord"),
            (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_rebellion_rival_default"),

            (assign, "$rival_lord", 0),

            (val_sub, "$rebellion_chance", 30),

            (assign, reg7, "$rebellion_chance"), #diagnostic only
            (display_message, "@Rebellion chance -30 from rival = {reg7}"),#diagnostic only

    ]],



  [anyone,"lord_join_rebellion_suggest_2", [
      ], "So tell me. Why should I support {s45}?", "lord_join_rebellion_suggest_3",
   [
    ]],

  [anyone|plyr,"lord_join_rebellion_suggest_3", [(troop_get_type, reg39, "$g_talk_troop"),
      ], "Legality -- {s45} has the better claim to the throne", "lord_join_rebellion_suggest_4",
   [
        (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_claim),
        (val_add, "$player_made_legitimacy_claim", 1),


        (assign, "$current_argument", argument_claim),
        (assign, "$current_argument_value", reg0),

    ]],

  [anyone|plyr,"lord_join_rebellion_suggest_3", [(troop_get_type, reg39, "$g_talk_troop"),
      ], "Justice -- {s45} will treat {reg39?her:his} subjects better than {s46}", "lord_join_rebellion_suggest_4",
   [
        (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_ruler),
        (val_add, "$player_made_ruler_claim", 1),


        (assign, "$current_argument", argument_ruler),
        (assign, "$current_argument_value", reg0),
    ]],

  [anyone|plyr,"lord_join_rebellion_suggest_3", [(troop_get_type, reg39, "$g_talk_troop"),
      ], "Expediency -- {s45} will win, and the sooner  {reg39?she:he} wins, the sooner this war will end.", "lord_join_rebellion_suggest_4",
   [
        (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_victory),
        (val_add, "$player_made_strength_claim", 1),


        (assign, "$current_argument", argument_victory),
        (assign, "$current_argument_value", reg0),

    ]],

  [anyone|plyr,"lord_join_rebellion_suggest_3", [(troop_get_type, reg39, "$g_talk_troop"),
      ], "Self-interest -- {s45} will reward  {reg39?her:his} followers well.", "lord_join_rebellion_suggest_4",
   [
        (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_benefit),
        (val_add, "$player_made_benefit_claim", 1),
       


        (assign, "$current_argument", argument_benefit),
        (assign, "$current_argument_value", reg0),

    ]],

  [anyone|plyr,"lord_join_rebellion_suggest_3", [
      ], "None of the usual reasons. My thinking is a little different.", "lord_join_rebellion_suggest_4",
   [
        (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_none),

        (assign, "$current_argument", argument_none),
        (assign, "$current_argument_value", 0),

    ]],


  [anyone|plyr,"lord_join_rebellion_suggest_3", [
      ], "There is more than one reason. I will let you make up your own mind.", "lord_join_rebellion_suggest_4",
   [
        (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_none),

        (assign, "$current_argument", argument_none),
        (assign, "$current_argument_value", 0),

    ]],


  [anyone|plyr,"lord_join_rebellion_suggest_3", [
      ], "If that is your reasoning, perhaps you should remain loyal to {s46}.", "lord_join_rebellion_suggest_5",
   [
        (assign, "$rebellion_check", 1),
        (assign, "$rebellion_chance", 0),
    ]],

  [anyone,"lord_join_rebellion_suggest_4", [
        (neq, "$current_argument", argument_none),
        (gt, "$current_argument_value", 0),
#Check for inconsistency
        (assign, ":arguments_used", 0),
        (assign, ":most_common_argument", 0),
        (try_begin), 
            (gt, "$player_made_benefit_claim", 0),
            (val_add, ":arguments_used", 1),
            (assign, ":most_common_argument", argument_benefit),
        (try_end),
        (try_begin), 
            (gt, "$player_made_strength_claim", 0),
            (val_add, ":arguments_used", 1),
            (try_begin),
                (gt, "$player_made_strength_claim", "$player_made_benefit_claim"),
                (assign, ":most_common_argument", argument_victory),
            (try_end),
        (try_end),
        (try_begin), 
            (gt, "$player_made_ruler_claim", 0),
            (val_add, ":arguments_used", 1),
            (try_begin),
                (gt, "$player_made_ruler_claim", "$player_made_strength_claim"),
                (gt, "$player_made_ruler_claim", "$player_made_benefit_claim"),
                (assign, ":most_common_argument", argument_ruler),
            (try_end),
        (try_end),
        (try_begin), 
            (gt, "$player_made_benefit_claim", 0),
            (val_add, ":arguments_used", 1),
            (try_begin),
                (gt, "$player_made_legitimacy_claim", "$player_made_ruler_claim"),
                (gt, "$player_made_legitimacy_claim", "$player_made_strength_claim"),
                (gt, "$player_made_legitimacy_claim", "$player_made_benefit_claim"),
                (assign, ":most_common_argument", argument_claim),
            (try_end),
        (try_end),

        (neq, "$current_argument", ":most_common_argument"),
        (store_random_in_range, ":consistency", 1, 5),
        (assign, reg10, ":consistency"),
        (assign, reg11, ":arguments_used"),
        (display_message, "@Consistency check: {reg10}/{reg11}"),
        (lt, ":consistency", ":arguments_used"),

], "Hmm. Do you perhaps tell each lord something different, depending on what you think he most wants to hear?", "lord_join_rebellion_suggest_4",
[
        (assign, "$current_argument_value", -5),
]],


  [anyone,"lord_join_rebellion_suggest_4", [

      ], "Very well. {s51}{s52}{s53}{s54}{s55}", "lord_join_rebellion_suggest_5",
   [

        (try_for_range, ":clear", 51, 60),
            (str_clear, ":clear"),
        (try_end),

        (try_begin),
            (neq, "$current_argument", argument_none),
            (try_begin),
                (gt, "$current_argument_value", 0),
                (str_store_string, 51, "str_rebellion_argument_favorable"),
            (else_try),
                (eq, "$current_argument_value", 0),
                (str_store_string, 51, "str_rebellion_argument_neutral"),
            (else_try),
                (lt, "$current_argument_value", 0),
                (str_store_string, 51, "str_rebellion_argument_unfavorable"),
            (try_end),

            (val_add, "$rebellion_chance", "$current_argument_value"),
             
            (assign, reg6, "$current_argument_value"), #diagnostic only
            (assign, reg7, "$rebellion_chance"), #diagnostic only
            (display_message, "@Current argument effect: {reg6}, rebellion chance: {reg7}"),#diagnostic only

            (store_skill_level, ":persuasion_level", "skl_persuasion", "trp_player"),
            (val_mul, ":persuasion_level", 5), 
            (store_random_in_range, ":persuasion_value", -10, ":persuasion_level"),


            (store_add, ":persuasion_plus_argument", ":persuasion_value", "$current_argument_value"),

            (str_store_string, 52, "str_and_comma_1"),

            (try_begin),
                (gt, ":persuasion_value", 10),
                (str_store_string, 53, "str_rebellion_persuasion_favorable"), 
                (try_begin),
                    (lt, "$current_argument_value", 0),
                    (str_store_string, 52, "str_but_comma_1"),
                (try_end),
            (else_try),
                (lt, ":persuasion_plus_argument", 0),
                (lt, ":persuasion_value", 0),
                (str_store_string, 53, "str_rebellion_persuasion_unfavorable"), 
                (try_begin),
                    (ge, "$current_argument_value", 0),
                    (str_store_string, 52, "str_but_comma_1"),
                (try_end),
            (else_try),
                (str_store_string, 53, "str_rebellion_persuasion_neutral"), 
                (try_begin),
                    (lt, "$current_argument_value", 0),
                    (str_store_string, 52, "str_but_comma_1"),
                (try_end),
            (try_end),

            (val_add, "$rebellion_chance", ":persuasion_value"),
             
            (assign, reg6, ":persuasion_value"), #diagnostic only
            (assign, reg7, "$rebellion_chance"), #diagnostic only
            (display_message, "@Persuasion effect: {reg6}, rebellion chance: {reg7}"),#diagnostic only

            (str_store_string, 54, "str_and_comma_2"),
            (try_begin),
                (gt, ":persuasion_plus_argument", 0),
                (lt, "$g_talk_troop_relation", 5),
                (str_store_string, 54, "str_but_comma_2"),
            (else_try),
                (le, ":persuasion_plus_argument", 0),
                (ge, "$g_talk_troop_relation", 5),
                (str_store_string, 54, "str_but_comma_2"),
            (try_end),

        (try_end),

        (try_begin),
            (gt, "$g_talk_troop_relation", 20),
            (str_store_string, 55, "str_rebellion_relation_very_favorable"),
        (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (str_store_string, 55, "str_rebellion_relation_favorable"),
        (else_try),
            (gt, "$g_talk_troop_relation", -5),
            (str_store_string, 55, "str_rebellion_relation_neutral"),
        (else_try),
            (str_store_string, 55, "str_rebellion_relation_unfavorable"),
        (try_end),

        (val_add, "$rebellion_chance", "$g_talk_troop_relation"),
             
        (assign, reg6, "$g_talk_troop_relation"), #diagnostic only
        (assign, reg7, "$rebellion_chance"), #diagnostic only
        (display_message, "@Personal relation effect: {reg6}, rebellion chance: {reg7}"),#diagnostic only
        

        (store_random_in_range, "$rebellion_check", 0, 100),

        (assign, reg6, "$rebellion_check"), #diagnostic only
        (display_message, "@Rebellion check: {reg6}"),#diagnostic only


    ]],



  [anyone,"lord_join_rebellion_suggest_5", [
        (lt, "$rebellion_check", "$rebellion_chance"),
      ], "{s43}", "lord_join_rebellion_ask_for_order",
   [

        (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_rebellion_agree_default"),

        (troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
        (call_script, "script_change_troop_faction", "$g_talk_troop", "$players_kingdom"),
        (troop_get_slot, ":lords_party", "$g_talk_troop", slot_troop_leaded_party),
        (party_set_faction, ":lords_party", "$players_kingdom"),
        (assign, "$g_leave_encounter", 1),
    ]],

  [anyone,"lord_join_rebellion_suggest_5", [
            (encountered_party_is_attacker),
      ], "{s43}", "party_encounter_lord_hostile_attacker_2",
   [
        (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_rebellion_refuse_default"),

    ]],

  [anyone,"lord_join_rebellion_suggest_5", [
      ], "{s43}", "lord_talk",
   [
        (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_rebellion_refuse_default"),

    ]],

  [anyone,"lord_join_rebellion_ask_for_order", [],
   "All right. So, what's the plan? What do you want me to do?", "lord_give_order",
   []],


#Rebellion changes end

  [anyone|plyr,"lord_talk", [(eq, "$cheat_mode", 1),
                             #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             #(ge, "$g_talk_troop_faction_relation", 10),
                             ],
   "CHEAT:I want to suggest a course of action.", "lord_suggest_action_ask",[]],

  [anyone,"lord_tell_objective", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 1),
                                  (troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
  ],
   "What am I doing? What does it look like I'm doing?! I'm a prisoner here!", "lord_pretalk",[]],

  [anyone,"lord_tell_objective", [(troop_slot_eq, "$g_talk_troop", slot_troop_leaded_party, -1)],
   "I am not commanding any men at the moment.", "lord_pretalk",[]],

  [anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_holding_center),
                                  (party_get_attached_to, ":cur_center_no", "$g_talk_troop_party"),
                                  (try_begin),
                                    (lt, ":cur_center_no", 0),
                                    (party_get_cur_town, ":cur_center_no", "$g_talk_troop_party"),
                                  (try_end),
                                  (is_between, ":cur_center_no", centers_begin, centers_end),
                                  ],
   "We are resting at {s1}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                              (str_store_party_name, s1, ":ai_object")]],

  [anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_holding_center)],
   "We are travelling to {s1}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                 (str_store_party_name, s1, ":ai_object")]],

  [anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_recruiting_troops)],
   "We are recruiting new soldiers from {s1}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                 (str_store_party_name, s1, ":ai_object")]],

  [anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_patrolling_around_center)],
   "We are scouting for the enemy around {s1}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                      (str_store_party_name, s1, ":ai_object")]],

#  [anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_raiding_around_center)],
#   "We ride out to lay waste to village of {s1} to punish the foe for his misdeeds.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
#                                                               (str_store_party_name, s1, ":ai_object")]],

  [anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_raiding_around_center)],
   "We are laying waste to the village of {s1}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                               (str_store_party_name, s1, ":ai_object")]],

  [anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_retreating_to_center)],
   "We are retreating to {s1}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                               (str_store_party_name, s1, ":ai_object")]],

  [anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_besieging_center)],
   "We are besieging {s1}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                               (str_store_party_name, s1, ":ai_object")]],

  [anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_engaging_army),
                                  (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                  (party_is_active, ":ai_object"),
                                  ],
   "We are fighting against {s1}.", "lord_pretalk",
   [
     (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
     (str_store_party_name, s1, ":ai_object")
     ]],

  [anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_accompanying_army)],
   "We are accompanying {s1}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                      (str_store_party_name, s1, ":ai_object")]],


  [anyone,"lord_tell_objective",
   [
     (assign, ":pass", 0),
     (try_begin),
       (party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_undefined),
       (assign, ":pass", 1),
     (else_try),
       (party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_engaging_army),
       (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
       (neg|party_is_active, ":ai_object"),
       (assign, ":pass", 1),
     (try_end),
     (eq, ":pass", 1),
     ],
   "We are reconsidering our next objective.", "lord_pretalk",[]],

  [anyone,"lord_tell_objective", [],
   "I don't know: {reg1} {s1}", "lord_pretalk",[(party_get_slot, reg1, "$g_talk_troop_party", slot_party_ai_state),
                                                (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                               (str_store_party_name, s1, ":ai_object")]],

  [anyone|plyr,"lord_talk",
   [
     (eq, "$talk_context", tc_party_encounter),
     (eq, "$g_talk_troop_faction", "$players_kingdom"),
     (party_slot_eq, "$g_encountered_party", slot_party_following_player, 0),
     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "trp_player"),
     ],
   "Will you follow me? I have a plan.", "lord_ask_follow",[]],

  [anyone,"lord_ask_follow", [(party_get_slot, ":dont_follow_until_time", "$g_encountered_party", slot_party_dont_follow_player_until_time),
                              (store_current_hours, ":cur_time"),
                              (lt, ":cur_time", ":dont_follow_until_time")],
   "I enjoy your company, {playername}, but there are other things I must attend to. Perhaps in a few days I can ride with you again.", "close_window",
   [(assign, "$g_leave_encounter",1)]],

  [anyone,"lord_ask_follow", [(troop_get_slot, ":troop_renown", "$g_talk_troop", slot_troop_renown),
                              (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
                              (val_mul, ":troop_renown", 3),
                              (val_div, ":troop_renown", 4),
                              (lt, ":player_renown", ":troop_renown"),
                              ],
   "That would hardly be proper, {playername}. Why don't you follow me instead?", "close_window",
   [(assign, "$g_leave_encounter",1)]],

  [anyone,"lord_ask_follow", [(lt, "$g_talk_troop_relation", 25)],
   "{s43}", "close_window",
   [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_follow_refusal_default"),
       (assign, "$g_leave_encounter",1)]],
#Post 0907 changes end

  [anyone,"lord_ask_follow", [],
   "Lead the way, {playername}! Let us bring death and defeat to all our enemies.", "close_window",
   [(party_set_slot, "$g_talk_troop_party", slot_party_commander_party, "p_main_party"),
    (call_script, "script_party_decide_next_ai_state_under_command", "$g_talk_troop_party"),
    (store_current_hours, ":follow_until_time"),
    (store_add, ":follow_period", 30, "$g_talk_troop_relation"),
    (val_div, ":follow_period", 2),
    (val_add, ":follow_until_time", ":follow_period"),
    (party_set_slot, "$g_encountered_party", slot_party_follow_player_until_time, ":follow_until_time"),
    (party_set_slot, "$g_encountered_party", slot_party_following_player, 1),
    (assign, "$g_leave_encounter",1)]],

  [anyone,"lord_talk_preoffer", [], "Yes?", "lord_talk_offer",[]],

  [anyone|plyr,"lord_talk_offer", [(eq,1,0)],
   "I wish to ransom one of your prisoners.", "knight_offer_join",[
       ]],

  [anyone|plyr,"lord_talk_offer", [], "Never mind.", "lord_pretalk",[]],

  [anyone ,"knight_offer_join", [(call_script, "script_cf_is_quest_troop", "$g_talk_troop")],
   "I fear I cannot join you at the moment, {playername}, I've important business to attend to and it cannot wait.", "hero_pretalk",[]],

  [anyone ,"knight_offer_join", [(lt, "$g_talk_troop_relation", 5),
                                 (store_character_level,":player_level","trp_player"),
                                 (store_character_level,":talk_troop_level","$g_talk_troop"),
                                 (val_mul,":player_level",2),
                                 (lt, ":player_level", ":talk_troop_level")],
   "You forget your place, {sir/madam}. I do not take orders from the likes of you.", "hero_pretalk",[]],
  
  [anyone ,"knight_offer_join", [
       (assign, ":num_player_companions",0),
       (try_for_range, ":hero_id", heroes_begin, heroes_end),
         (troop_slot_eq, ":hero_id",slot_troop_occupation, slto_player_companion),
         (val_add, ":num_player_companions",1),
       (try_end),
       (assign, reg5, ":num_player_companions"),
       (store_add, reg6, reg5, 1),
       (val_mul, reg6,reg6),
       (val_mul, reg6, 1000),
       (gt, reg6,0)], #note that we abuse the value of reg6 in the next line.
 "I would be glad to fight at your side, my friend, but there is a problem...\
 The thing is, I've found myself in a bit of debt that I must repay very soon. {reg6} denars altogether,\
 and I am honour-bound to return every coin. Unless you've got {reg6} denars with you that you can spare,\
 I've to keep my mind on getting this weight off my neck.", "knight_offer_join_2",[]],
  [anyone ,"knight_offer_join", [(gt,reg6, 100000)], "Join you? I think not.", "close_window",[]],
  [anyone ,"knight_offer_join", [], "Aye, my friend, I'll be happy to join you.", "knight_offer_join_2",[]],

  [anyone|plyr,"knight_offer_join_2", [(gt, reg6,0),(store_troop_gold, ":gold", "trp_player"),(gt,":gold",reg6)],
   "Here, take it, all {reg6} denars you need. 'Tis only money.", "knight_offer_join_accept",[(troop_remove_gold, "trp_player",reg6)]],
  [anyone|plyr,"knight_offer_join_2", [(le, reg6,0)], "Then let us ride together, my friend.", "knight_offer_join_accept",[]],
   
  [anyone|plyr,"knight_offer_join_2", [(eq, "$talk_context", tc_hero_freed)], "That's good to know. I will think on it.", "close_window",[]],
  [anyone|plyr,"knight_offer_join_2", [(neq, "$talk_context", tc_hero_freed)], "That's good to know. I will think on it.", "hero_pretalk",[]],
  
  
  [anyone ,"knight_offer_join_accept", [(troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1)],
   "I've some trusted men in my band who could be of use to you. What do you wish to do with them?", "knight_offer_join_accept_party",[
      ]],
  [anyone ,"knight_offer_join_accept", [], "Ah, certainly, it might be fun!", "close_window",[
      (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
      (assign, "$g_leave_encounter",1)
      ]],
  
  [anyone|plyr,"knight_offer_join_accept_party", [], "You may disband your men. I've no need for other troops.", "knight_join_party_disband",[]],
  [anyone|plyr,"knight_offer_join_accept_party", [(troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
                                       (party_can_join_party,":companions_party","p_main_party"),
      ], "Your men may join as well. We need every soldier we can muster.", "knight_join_party_join",[]],
  [anyone|plyr,"knight_offer_join_accept_party", [(is_between,"$g_encountered_party",centers_begin, centers_end)], "Lead your men out of the town. I shall catch up with you on the road.", "knight_join_party_lead_out",[]],
  [anyone|plyr,"knight_offer_join_accept_party", [(neg|is_between,"$g_encountered_party",centers_begin, centers_end)],
   "Keep doing what you were doing. I'll catch up with you later.", "knight_join_party_lead_out",[]],


  [anyone ,"knight_join_party_disband", [], "Ah . . . Very well, {playername}. Much as I dislike losing good men,\
 the decision is yours. I'll disband my troops and join you.", "close_window",[
      (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),

      (troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
      (party_detach, ":companions_party"),
      (remove_party, ":companions_party"),
      (assign, "$g_leave_encounter",1)
      ]],

  [anyone ,"knight_join_party_join", [], "Excellent.\
 My lads and I will ride with you.", "close_window",[
      (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
      (party_remove_members, "p_main_party", "$g_talk_troop", 1),
      
      (troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
      (assign, "$g_move_heroes", 1),
      (call_script, "script_party_add_party", "p_main_party", ":companions_party"),
      (party_detach, ":companions_party"),
      (remove_party, ":companions_party"),
      (assign, "$g_leave_encounter",1)
      ]],

  [anyone ,"knight_join_party_lead_out", [], "Very well then.\
 I shall maintain a patrol of this area. Return if you have further orders for me.", "close_window",[
      (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
      (party_remove_members, "p_main_party", "$g_talk_troop", 1),
      
      (troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
      (party_set_faction, ":companions_party", "fac_player_supporters_faction"),
      (party_detach, ":companions_party"),
      (party_set_ai_behavior, ":companions_party", ai_bhvr_patrol_location),
      (party_set_flags, ":companions_party", pf_default_behavior, 0),
      ]],



#Active quests
##### TODO: QUESTS COMMENT OUT BEGIN

  [anyone,"lord_active_mission_1", [(store_partner_quest,":lords_quest"),
                                    (eq,":lords_quest","qst_lend_companion"),
                                    #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                                    (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                                    (check_quest_active,"qst_lend_companion"),
                                    (quest_slot_eq, "qst_lend_companion", slot_quest_giver_troop, "$g_talk_troop"),
                                    (store_current_day, ":cur_day"),
                                    (quest_get_slot, ":quest_target_amount", "qst_lend_companion", slot_quest_target_amount),
                                    (ge, ":cur_day", ":quest_target_amount"),
##                                    (quest_get_slot, ":quest_target_troop", "qst_lend_companion", slot_quest_target_troop),
##                                    (str_store_troop_name,s14,":quest_target_troop"),
##                                    (troop_get_type, reg3, ":quest_target_troop"),
                                    ],
   "Oh, you want your companion back? I see...", "lord_lend_companion_end",[]],




  [anyone,"lord_active_mission_1", [(store_partner_quest,":lords_quest"),(eq,":lords_quest","qst_lend_companion")],
   "{playername}, I must beg your patience, I still have need of your companion. Please return later when things have settled.", "lord_pretalk",[]],
  [anyone,"lord_active_mission_1", [], "Yes, have you made any progress on it?", "lord_active_mission_2",[]],

  [anyone|plyr,"lord_active_mission_2",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                            (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                            (check_quest_active,"qst_capture_prisoners"),
                            (quest_slot_eq, "qst_capture_prisoners", slot_quest_giver_troop, "$g_talk_troop"),
                            (quest_get_slot, ":quest_target_amount", "qst_capture_prisoners", slot_quest_target_amount),
                            (quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
                            (party_count_prisoners_of_type, ":count_prisoners", "p_main_party", ":quest_target_troop"),
                            (ge, ":count_prisoners", ":quest_target_amount"),
                            (assign, reg1, ":quest_target_amount"),
                            (str_store_troop_name_plural, s1, ":quest_target_troop")],
   "Indeed. I brought you {reg1} {s1} as prisoners.", "lord_generic_mission_thank",
   [(quest_get_slot, ":quest_target_amount", "qst_capture_prisoners", slot_quest_target_amount),
    (quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
    (party_remove_prisoners, "p_main_party", ":quest_target_troop", ":quest_target_amount"),
    (party_add_prisoners, "$g_encountered_party", ":quest_target_troop", ":quest_target_amount"),
    (call_script, "script_finish_quest", "qst_capture_prisoners", 100)]],

  [anyone|plyr,"lord_active_mission_2",[
                            (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),                           
                            (check_quest_succeeded,"qst_rescue_prisoners"),
                            (quest_slot_eq, "qst_rescue_prisoners", slot_quest_giver_troop, "$g_talk_troop"),
                            (quest_get_slot, ":quest_target_amount", "qst_rescue_prisoners", slot_quest_target_amount),
                             #slot_quest_current_state is where the actual number of rescued prisoners is kept
                            (quest_slot_ge, "qst_rescue_prisoners", slot_quest_current_state, ":quest_target_amount"),
                            (assign, reg1, ":quest_target_amount"),
                            ],
   "Indeed. I have rescued {reg1} allied prisoners and they joined my party.", "lord_generic_mission_thank",
   [(call_script, "script_finish_quest", "qst_rescue_prisoners", 100)]],

  [anyone|plyr,"lord_active_mission_2",
   [
     #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
     (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
     (store_partner_quest, ":lords_quest"),
     (eq, ":lords_quest", "qst_capture_enemy_hero"),
     (assign, ":has_prisoner", 0),
     (quest_get_slot, ":quest_target_faction", "qst_capture_enemy_hero", slot_quest_target_faction),
     (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_prisoner_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
       (troop_is_hero, ":stack_troop"),
       (store_troop_faction, ":stack_faction", ":stack_troop"),
       (eq, ":quest_target_faction", ":stack_faction"),
       (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
       (assign, ":has_prisoner", 1),
       (quest_set_slot, "qst_capture_enemy_hero", slot_quest_target_troop, ":stack_troop"),
     (try_end),
     (eq, ":has_prisoner", 1),
     (str_store_faction_name, s13, ":quest_target_faction")
     ],
   "Oh, indeed. I've captured a lord from {s13} for you.", "capture_enemy_hero_thank",
   []],

  [anyone,"capture_enemy_hero_thank", [],
   "Many thanks, my friend. He will serve very well for a bargain. You've done a fine work here. Please accept these {reg5} denars for your help.", "capture_enemy_hero_thank_2",
   [(quest_get_slot, ":quest_target_troop", "qst_capture_enemy_hero", slot_quest_target_troop),
     (quest_get_slot, ":quest_target_faction", "qst_capture_enemy_hero", slot_quest_target_faction),
     (party_remove_prisoners, "p_main_party", ":quest_target_troop", 1),
     (store_relation, ":reln", "$g_encountered_party_faction", ":quest_target_faction"),
     (try_begin),
       (lt, ":reln", 0),
       (party_add_prisoners, "$g_encountered_party", ":quest_target_troop", 1), #Adding him to the dungeon
     (else_try),
       #Do not add a non-enemy lord to the dungeon (due to recent diplomatic changes or due to a neutral town/castle)
       #(troop_set_slot, ":quest_target_troop", slot_troop_is_prisoner, 0),
       (troop_set_slot, ":quest_target_troop", slot_troop_prisoner_of_party, -1),
     (try_end),
     (quest_get_slot, ":reward", "qst_capture_enemy_hero", slot_quest_gold_reward),
     (call_script, "script_troop_add_gold", "trp_player", ":reward"),
     (add_xp_as_reward, 2500),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 4),
     (call_script, "script_end_quest", "qst_capture_enemy_hero"),
   ]],

  [anyone|plyr,"capture_enemy_hero_thank_2", [],
   "Certainly, {s65}.", "lord_pretalk",[]],
  [anyone|plyr,"capture_enemy_hero_thank_2", [],
   "It was nothing.", "lord_pretalk",[]],
  [anyone|plyr,"capture_enemy_hero_thank_2", [],
   "Give me more of a challenge next time.", "lord_pretalk",[]],

##
##  [anyone|plyr,"lord_active_mission_2", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                                         (store_partner_quest,":lords_quest"),
##                                         (eq,":lords_quest","qst_capture_messenger"),
##                                         (quest_get_slot, ":quest_target_troop", ":lords_quest", slot_quest_target_troop),
##                                         (quest_get_slot, ":quest_target_amount", ":lords_quest", slot_quest_target_amount),
##                                         (store_num_parties_destroyed_by_player, ":num_destroyed", "pt_messenger_party"),
##                                         (gt, ":num_destroyed", ":quest_target_amount"),
##                                         (party_count_prisoners_of_type, ":num_prisoners", "p_main_party", ":quest_target_troop"),
##                                         (ge, ":num_prisoners", 1),
##                                         (str_store_troop_name, 3, ":quest_target_troop")],
##   "Indeed sir. I have captured a {s3} my lord.", "lord_generic_mission_thank",[(quest_get_slot, ":quest_target_troop", "qst_capture_messenger", slot_quest_target_troop),
##                                                                     (party_remove_prisoners, "p_main_party", ":quest_target_troop", 1),
##                                                                     (party_add_prisoners, "$g_encountered_party", ":quest_target_troop", 1),#Adding him to the dungeon
##                                                                     (call_script, "script_finish_quest", "qst_capture_messenger", 100)]],
##  
##
  [anyone|plyr,"lord_active_mission_2", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
										 (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                                         (store_partner_quest,":lords_quest"),
                                         (eq,":lords_quest","qst_raise_troops"),
                                         (quest_get_slot, ":quest_target_troop", ":lords_quest", slot_quest_target_troop),
                                         (quest_get_slot, ":quest_target_amount", ":lords_quest", slot_quest_target_amount),
                                         (party_count_companions_of_type, ":num_companions", "p_main_party", ":quest_target_troop"),
                                         (ge, ":num_companions", ":quest_target_amount"),
                                         (assign, reg1, ":quest_target_amount"),
                                         (str_store_troop_name_plural, s13, ":quest_target_troop")],
   "Indeed. I have raised {reg1} {s13}. You can take them.", "lord_raise_troops_thank",[(quest_get_slot, ":quest_target_troop", "qst_raise_troops", slot_quest_target_troop),
                                                                                         (quest_get_slot, ":quest_target_amount", "qst_raise_troops", slot_quest_target_amount),
                                                                                         (call_script,"script_change_player_relation_with_troop","$g_talk_troop",8),
                                                                                         (party_remove_members, "p_main_party", ":quest_target_troop", ":quest_target_amount"),
                                                                                         (call_script, "script_end_quest", "qst_raise_troops"),
                                                                                         (troop_get_slot, ":cur_lords_party", "$g_talk_troop", slot_troop_leaded_party),
                                                                                         (gt, ":cur_lords_party", 0),
                                                                                         (party_add_members, ":cur_lords_party", ":quest_target_troop", ":quest_target_amount"),
                                                                                         ]],

  [anyone,"lord_raise_troops_thank", [],
   "These men may well turn the tide in my plans, {playername}. I am confident you've trained them well. My thanks and my compliments to you.", "lord_raise_troops_thank_2",[]],

  [anyone|plyr,"lord_raise_troops_thank_2", [],
   "Well, the lads are at your command now, sir. I am sure you will take good care of them.", "lord_pretalk",[]],

  [anyone|plyr,"lord_active_mission_2", [(store_partner_quest,":lords_quest"),
                                         (eq, ":lords_quest", "qst_hunt_down_fugitive"),
                                         (check_quest_succeeded, "qst_hunt_down_fugitive"),
                                         (quest_get_slot, ":quest_target_center", "qst_hunt_down_fugitive", slot_quest_target_center),
                                         (str_store_party_name, s3, ":quest_target_center"),
                                         (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
                                         (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
                                         (str_store_string, s4, s50),],
   "I found {s4} hiding at {s3} and gave him his punishment.", "lord_hunt_down_fugitive_success",
   []],

  [anyone|plyr,"lord_active_mission_2", [(store_partner_quest,":lords_quest"),
                                         (eq, ":lords_quest", "qst_hunt_down_fugitive"),
                                         (check_quest_failed, "qst_hunt_down_fugitive"),
                                         ],
   "I'm afraid he got away.", "lord_hunt_down_fugitive_fail",
   []],

  [anyone,"lord_hunt_down_fugitive_success", [],
   "And we'll all be a lot better off without him! Thank you, {playername},\
 for removing this long-festering thorn from my side. 'Tis good to know you can be trusted to handle things\
 with an appropriate level of tactfulness.\
 A bounty I promised, and a bounty you shall have. 300 denars and not a copper less!", "lord_hunt_down_fugitive_success_2",
   [
     (add_xp_as_reward, 300),
    ]],
  
  [anyone|plyr,"lord_hunt_down_fugitive_success_2", [],
   "Let me take the money, {s65}. Thank you.", "lord_hunt_down_fugitive_reward_accept",[]],
  [anyone|plyr,"lord_hunt_down_fugitive_success_2", [],
   "This is blood money. I can't accept it.", "lord_hunt_down_fugitive_reward_reject",[]],

#Post 0907 changes begin
  [anyone,"lord_hunt_down_fugitive_reward_accept", [],
   "Of course, {playername}. Here you are. Once again, you've my thanks for ridding me of that {s44}.", "lord_pretalk",[
       (troop_get_slot, ":insult_string", "$g_talk_troop", slot_lord_reputation_type),
       (val_add, ":insult_string", "str_lord_insult_default"),
       (str_store_string, s44, ":insult_string"),

       (call_script, "script_troop_add_gold", "trp_player", 300),
       (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
       (call_script, "script_end_quest", "qst_hunt_down_fugitive"),
       ]],

  [anyone,"lord_hunt_down_fugitive_reward_reject", [],
   "You are a {man/woman} for whom justice is its own reward, eh? As you wish it, {playername}, as you wish it.\
 An honourable sentiment, to be true. Regardless, you've my thanks for ridding me of that {s44}.", "lord_pretalk",[

       (troop_get_slot, ":insult_string", "$g_talk_troop", slot_lord_reputation_type),
       (val_add, ":insult_string", "str_lord_insult_default"),
       (str_store_string, s44, ":insult_string"),
       
       (call_script, "script_change_player_honor", 3),
       (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
       (call_script, "script_end_quest", "qst_hunt_down_fugitive"),
       ]],

  [anyone,"lord_hunt_down_fugitive_fail", [],
   "It is a sad day when that {s44} manages to avoid the hand of justice yet again.\
 I thought you would be able to do this, {playername}. Clearly I was wrong.", "lord_pretalk",
   [
    (troop_get_slot, ":insult_string", "$g_talk_troop", slot_lord_reputation_type),
    (val_add, ":insult_string", "str_lord_insult_default"),
    (str_store_string, 44, ":insult_string"),

    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (call_script, "script_end_quest", "qst_hunt_down_fugitive"),
    ]],
#Post 0907 changes end



##
##
##  [anyone|plyr,"lord_active_mission_2", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                                         (store_partner_quest,":lords_quest"),
##                                         (eq,":lords_quest","qst_bring_back_deserters"),
##                                         (quest_get_slot, ":quest_target_troop", ":lords_quest", slot_quest_target_troop),
##                                         (quest_get_slot, ":quest_target_amount", ":lords_quest", slot_quest_target_amount),
##                                         (party_count_prisoners_of_type, ":num_prisoners", "p_main_party", ":quest_target_troop"),
##                                         (ge, ":num_prisoners", ":quest_target_amount"),
##                                         (assign, reg1, ":quest_target_amount")],
##   "Yes sir. I have brought {reg1} deserters as you asked me to.", "lord_generic_mission_thank",[(quest_get_slot, ":quest_target_troop", "qst_bring_back_deserters", slot_quest_target_troop),
##                                                                                     (quest_get_slot, ":quest_target_amount", "qst_bring_back_deserters", slot_quest_target_amount),
##                                                                                     (party_remove_prisoners, "p_main_party", ":quest_target_troop", ":quest_target_amount"),
##                                                                                     (faction_get_slot, ":faction_tier_2_troop", "$g_talk_troop_faction", slot_faction_tier_2_troop),
##                                                                                     (try_begin),
##                                                                                       (gt, ":faction_tier_2_troop", 0),
##                                                                                       (troop_get_slot, ":cur_lords_party", "$g_talk_troop", slot_troop_leaded_party),
##                                                                                       (gt, ":cur_lords_party", 0),
##                                                                                       (party_add_members, ":cur_lords_party", ":faction_tier_2_troop", ":quest_target_amount"),
##                                                                                     (try_end),
##                                                                                     (call_script, "script_finish_quest", "qst_bring_back_deserters", 100)]],
## 
##
##### TODO: QUESTS COMMENT OUT END
  [anyone|plyr,"lord_active_mission_2", [], "I am still working on it.", "lord_active_mission_3",[]],
  [anyone|plyr,"lord_active_mission_2", [], "I am afraid I won't be able to do this quest.", "lord_mission_failed",[]],
                                                                                                                                                   
  [anyone,"lord_active_mission_3", [], "Good. Remember, I am counting on you.", "lord_pretalk",[]],


#Post 0907 changes begin
  [anyone,"lord_mission_failed", [], "{s43}", "lord_pretalk",
   [
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_mission_failed_default"),
    (store_partner_quest,":lords_quest"),
    (call_script, "script_abort_quest", ":lords_quest", 1)]],
#Post 0907 changes end
  

##### TODO: QUESTS COMMENT OUT BEGIN
#Request Mission

  [anyone|auto_proceed,"lord_request_mission_ask",
   [(eq, "$players_kingdom", 0),
    (ge, "$g_talk_troop_faction_relation", 0),
    (ge, "$g_talk_troop_relation", 0),
    (troop_slot_ge, "trp_player", slot_troop_renown, 30),
    (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
    (faction_get_slot, ":last_offer_time", "$g_talk_troop_faction", slot_faction_last_mercenary_offer_time),

    (assign, ":num_enemies", 0),
    (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, "$g_talk_troop_faction", slot_faction_state, sfs_active),
      (store_relation, ":reln", "$g_talk_troop_faction", ":faction_no"),
      (lt, ":reln", 0),
      (val_add, ":num_enemies", 1),
    (try_end),
    (ge, ":num_enemies", 1),
    (store_current_hours, ":cur_hours"),
    (store_add,  ":week_past_last_offer_time", ":last_offer_time", 7 * 24),
    (val_add,  ":last_offer_time", 24),
    (ge, ":cur_hours", ":last_offer_time"),
    (store_random_in_range, ":rand", 0, 100),
    (this_or_next|lt, ":rand", 20),
    (             ge, ":cur_hours", ":week_past_last_offer_time"),
    ],
   "Warning: This line should never display.", "lord_propose_mercenary",[(store_current_hours, ":cur_hours"),
                                  (faction_set_slot, "$g_talk_troop_faction", slot_faction_last_mercenary_offer_time,  ":cur_hours")]],

 
  [anyone,"lord_request_mission_ask", [(store_partner_quest,":lords_quest"),(ge,":lords_quest",0)],
   "You still haven't finished the last job I gave you, {playername}. You should be working on that, not asking me for other things to do.", "lord_pretalk",[]],

  [anyone,"lord_request_mission_ask", [(troop_slot_eq, "$g_talk_troop", slot_troop_does_not_give_quest, 1)],
   "I don't have any other jobs for you right now.", "lord_pretalk",[]],
  [anyone|auto_proceed,"lord_request_mission_ask", [], "A task?", "lord_tell_mission",
   [
       (call_script, "script_get_random_quest", "$g_talk_troop"),
       (assign, "$random_quest_no", reg0),
   ]],

  

   # TLD mission: investigate fangorn (mtarini) -- begin 
  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_investigate_fangorn")],
  "Here is a mission for a trusted and brave serve like you, {playername}.\
  The strangest rumors reach my ears from the forest of Fangorn. \
  Minions sent to harvest wood, and even my commanders traversing the place, occasionally fail to return.\
  Other times, they report of mysterious losses among their troops.\
  They blame ghosts, spirits of the wood, ancient curses... \
  Nonsense! Puny excuses for their own cowardice or ineptitude!", "lord_mission_investigate_fangorn_0", 
  []],

  [anyone|plyr,"lord_mission_investigate_fangorn_0", [], "What do you command me to do about it, Master?",
  "lord_mission_investigate_fangorn_1",[]],
  
  [anyone|plyr,"lord_mission_investigate_fangorn_0", [], "But Master, there is danger and pain in Fangorn! I've felt it myself!", "lord_mission_investigate_fangorn_rejected",[]],

    [anyone,"lord_mission_investigate_fangorn_1", [],
  "Maybe it is just that my other servants are unable to prevent the most coward worms in their troops from deserting.\
  Fools, blinded by superstitions. \
  Or, maybe, it is the treacherous ambushes of elven scum, hiding in the putrid trees as they do. \
  It could even be lowborn traitors from Rohan.\
  Or who knows what else. I want you to find out, {playername}.", "lord_mission_investigate_fangorn_2", 
  []],
  
    [anyone|plyr,"lord_mission_investigate_fangorn_2", [], "I fear no elves or spirit. Leave this to me, Master.",
  "lord_mission_investigate_fangorn_accepted",[]],
  
  [anyone|plyr,"lord_mission_investigate_fangorn_2", [], "Master, pity of your servant! Don't ask me to venture in that cursed place!", "lord_mission_investigate_fangorn_rejected",[]],

  [anyone,"lord_mission_investigate_fangorn_rejected", [], "So you are like the other worms: a superstitious, worthless coward.\
  I overestimated you. Now, begone!", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
   (assign, "$g_leave_encounter",1),]], 
 
 [anyone,"lord_mission_investigate_fangorn_accepted", [], "Good.\
 Go there and shed some light on this matter. Then return to me and report.\
 I expect to see you back with news before {reg1} dawns are passed.", "lord_pretalk",
   [
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
    (quest_get_slot, reg1, "$random_quest_no", slot_quest_expiration_days),
    
   ]],

  # TLD mission: investigate fangorn (mtarini) -- end

  # TLD mission: Find the lost spears of king Bladorthin (Kolba) -- begin

   [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_find_lost_spears")],
  "Here is a mission for a trusted and brave commander like you, {playername}.\
   We are ill equipped to fight off the Easterling hordes.\
   Our armies are losing battles one by one.\
   A legend tells that once upon a time, the spears that were made for the armies of the great King Bladorthin (long since dead),\
   each had a thrice-forged head and their shafts were inlaid with cunning gold, but they were never delivered or paid for..", "lord_mission_find_lost_spears", 
  []],

  [anyone|plyr,"lord_mission_find_lost_spears",[],
   "What do you command me to do about it, my lord?","lord_mission_find_lost_spears_1",[]],

  [anyone,"lord_mission_find_lost_spears_1",[],
  "These weapons would increase the effectiveness of our armies and let them be somewhat superior to the Easterlings. You'll have to find these spears.\
   You'll have to go ask the dwarves for permission to search for the spears in the deep of the Lonely Mountain.\
   Beware, you may encounter some orcs or trolls in the tunnels. Are you available for this task?","lord_mission_find_lost_spears_2",[]],

  [anyone|plyr,"lord_mission_find_lost_spears_2", [], "I fear no orcs nor trolls! I will find these spears for you, my king.","lord_mission_find_lost_spears_accepted",[]],
  [anyone|plyr,"lord_mission_find_lost_spears_2", [], "I'm afraid I can't help you, my lord.","lord_mission_find_lost_spears_rejected",[]],

    [anyone,"lord_mission_find_lost_spears_rejected", [], "So you are like the other weaklings: a superstitious, worthless coward.\
  I overestimated you. Now, get out of my sight!", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
   (assign, "$g_leave_encounter",1),
    ]],

    [anyone,"lord_mission_find_lost_spears_accepted", [], "Good! put some advice or something here.","lord_pretalk",
     [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
    (quest_get_slot, reg1, "$random_quest_no", slot_quest_expiration_days),
      ]],

  #TLD mission: Find the lost spears of king Bladorthin (Kolba) -- end

  #TLD mission: nowy quest (Kolba) -- begin

  

    

   
  
  
  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_deliver_message")],
   "I need to send a letter to {s13} who should be currently at {s4}.\
 If you will be heading towards there, would you deliver it to him?\
 The letter needs to be in his hands in 30 days.", "lord_mission_deliver_message",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_troop_name_link,s9,"$g_talk_troop"),
     (str_store_troop_name_link,s13,":quest_target_troop"),
     (str_store_party_name_link,s4,":quest_target_center"),
     (setup_quest_text,"$random_quest_no"),
##     (try_begin),
##       (is_between, "$g_encountered_party", centers_begin, centers_end),
##       (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##     (else_try),
##       (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##     (try_end),
     (str_store_string, s2, "@{s9} asked you to take a message to {s13}. {s13} was believed to be at {s4} when you were given this quest."),
   ]],

  [anyone|plyr,"lord_mission_deliver_message", [], "Certainly, I intend to pass by {s4} and it would be no trouble.", "lord_mission_deliver_message_accepted",[]],
  [anyone|plyr,"lord_mission_deliver_message", [], "I doubt I'll be seeing {s13} anytime soon, {s65}. You'd best send it with someone else.", "lord_mission_deliver_message_rejected",[]],
  [anyone|plyr,"lord_mission_deliver_message", [], "I am no errand boy, sir. Hire a courier for your trivialities.", "lord_mission_deliver_message_rejected_rudely",[]],

  [anyone,"lord_mission_deliver_message_accepted", [], "I appreciate it, {playername}. Here's the letter,\
 and a small sum to cover your travel expenses. Give my regards to {s13} when you see him.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_troop_add_gold", "trp_player",30),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
    (assign, "$g_leave_encounter",1),
   ]],

  [anyone,"lord_mission_deliver_message_rejected", [], "Ah, all right then. Well, I am sure I will find someone else.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
  
  [anyone,"lord_mission_deliver_message_rejected_rudely", [], "Hm, is this how you respond to a polite request\
 for a small favor? A poor show, {playername}. I didn't know you would take offence.", "lord_mission_deliver_message_rejected_rudely_2",[]],
    
  [anyone|plyr,"lord_mission_deliver_message_rejected_rudely_2", [], "Then you shall know better from now on.", "lord_mission_deliver_message_rejected_rudely_3",[]],
  [anyone|plyr,"lord_mission_deliver_message_rejected_rudely_2", [], "Forgive my temper, {s65}. I'll deliver your letter.", "lord_mission_deliver_message_accepted",[]],

  [anyone,"lord_mission_deliver_message_rejected_rudely_3", [], "All right. I will remember that.", "close_window",[
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",-4),
    (quest_set_slot, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 150),
    (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),    
    (assign, "$g_leave_encounter",1),
      ]],

  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_deliver_message_to_enemy_lord")],
   "I need to deliver a letter to {s13} of {s15}, who must be at {s4} currently.\
 If you are going towards there, would you deliver my letter to him? The letter needs to reach him in 40 days.", "lord_mission_deliver_message",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_troop_name_link,s9,"$g_talk_troop"),
##     (str_store_party_name,2,"$g_encountered_party"),
     (str_store_troop_name_link,s13,":quest_target_troop"),
     (str_store_party_name_link,s4,":quest_target_center"),
     (store_troop_faction, ":target_faction", ":quest_target_troop"),
     (str_store_faction_name_link,s15,":target_faction"),
     (setup_quest_text,"$random_quest_no"),
##     (try_begin),
##       (is_between, "$g_encountered_party", centers_begin, centers_end),
##       (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##     (else_try),
##       (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##     (try_end),
     (str_store_string, s2, "@{s9} asked you to take a message to {s13} of {s15}. {s13} was believed to be at {s4} when you were given this quest."),
   ]],

  
##
##  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_deliver_message_to_lover")],
##   "My dear friend, I have a deep affection for {s3} and I believe she feels the same way for me as well.\
## Alas, her father {s5} finds me unsuitable for her and will do anything to prevent our union.\
## I really need your help. Please, will you take this letter to her? She should be at {s4} at the moment.", "lord_mission_told",
##   [
##     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
##     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##     (str_store_troop_name_link,1,"$g_talk_troop"),
##     (str_store_party_name_link,2,"$g_encountered_party"),
##     (str_store_troop_name_link,3,":quest_target_troop"),
##     (str_store_party_name_link,4,":quest_target_center"),
##     (setup_quest_text,"$random_quest_no"),
##     (try_begin),
##       (is_between, "$g_encountered_party", centers_begin, centers_end),
##       (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##     (else_try),
##       (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##     (try_end),
##   ]],
##
  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_escort_lady")],
   "There is a small thing... My {s17} {s13} is due for a visit to her relatives at {s14}.\
 The visit has been postponed several times already with all the trouble on the roads,\
 but this time she is adamant about going. So, I want to at least make sure she's well-guarded.\
 I trust you well, {playername} so I would be very grateful if you could escort her to {s14}\
 and make sure she arrives safe and sound.", "lord_mission_told",
   [
     (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (try_begin),
       (troop_slot_eq, "$g_talk_troop", slot_troop_daughter, ":quest_object_troop"),
       (str_store_string, s17, "str_daughter"),
     (else_try),
       (str_store_string, s17, "str_wife"),
     (try_end),
     (str_store_troop_name_link, s11, "$g_talk_troop"),
     (str_store_troop_name_link, s13, ":quest_object_troop"),
     (str_store_party_name_link, s14, ":quest_target_center"),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to escort his {s17} {s13} to {s14}."),
   ]],

##
##  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_hunt_down_raiders")],
## "A messenger came with important news a few hours ago.\
## A group of enemy raiders have attacked a village near {s3}.\
## They have murdered anyone who tried to resist, stolen everything they could carry and put the rest to fire.\
## Now, they must be on their way back to their base at {s4}.\
## You must catch them on the way and make them pay for their crimes.", "lord_mission_told",
##   [
##       (quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),
##       (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##       (str_store_party_name_link,3,":quest_object_center"),
##       (str_store_party_name_link,4,":quest_target_center"),
##    ]],
##  
##  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_bring_back_deserters")],
## "I am worried about the growing number of deserters. If we don't do something about it, we may soon have noone left to fight in our wars.\
## I want you to go now and bring back {reg1} {s3}. I would ask you to hang the bastards but we are short of men and we need them back in the ranks.", "lord_mission_told",
##   [
##       (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
##       (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
##      
##       (str_store_troop_name_link,1,"$g_talk_troop"),
##       (str_store_party_name_link,2,"$g_encountered_party"),
##       (str_store_troop_name_plural,3,":quest_target_troop"),
##       (assign, reg1, ":quest_target_amount"),
##       (setup_quest_text,"$random_quest_no"),
##       (try_begin),
##         (is_between, "$g_encountered_party", centers_begin, centers_end),
##         (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##       (else_try),
##         (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##       (try_end),
##    ]],
##
##  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_deliver_supply_to_center_under_siege")],
## "The enemy has besieged {s5}. Our brothers there are doing their best to fend off attacks, but they can't hold for long without supplies.\
## We need someone to take the supplies they need and make it into the town as soon as possible.\
## It's a very dangerous job, but if there's one person who can do it, it's you {playername}.\
## You can take the supplies from seneschal {s3}. When you arrive at {s5}, give them to the seneschal of that town.", "lord_mission_told",
##   [
##       (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
##       (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##       (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
##       (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
##      
##       (str_store_troop_name_link,1,"$g_talk_troop"),
##       (str_store_party_name_link,2,"$g_encountered_party"),
##       (str_store_troop_name_link,3,":quest_object_troop"),
##       (str_store_troop_name,4,":quest_target_troop"),
##       (str_store_party_name_link,5,":quest_target_center"),
##       (assign, reg1, ":quest_target_amount"),
##       (setup_quest_text,"$random_quest_no"),
##       (try_begin),
##         (is_between, "$g_encountered_party", centers_begin, centers_end),
##         (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##       (else_try),
##         (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##       (try_end),
##    ]],
##
##  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_bring_reinforcements_to_siege")],
## "{s4} has besieged {s5} and God willing, that town will not hold for long.\
## Still I promised him to send {reg1} {s3} as reinforcements and I need someone to lead those men.\
## Can you take them to {s4}?", "lord_mission_told",
##   [
##       (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
##       (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##       (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
##       (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
##      
##       (str_store_troop_name_link,1,"$g_talk_troop"),
##       (str_store_party_name_link,2,"$g_encountered_party"),
##       (str_store_troop_name_plural,3,":quest_object_troop"),
##       (str_store_troop_name_link,4,":quest_target_troop"),
##       (str_store_party_name_link,5,":quest_target_center"),
##       (assign, reg1, ":quest_target_amount"),
##       (setup_quest_text,"$random_quest_no"),
##       (try_begin),
##         (is_between, "$g_encountered_party", centers_begin, centers_end),
##         (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##       (else_try),
##         (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##       (try_end),
##    ]],
##
##  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_rescue_lady_under_siege")],
## "The enemy has besieged {s4} and my dear {s7} {s3} has been trapped within the town walls.\
## As you may guess, I am greatly distressed by this. I need a very reliable commander, to rescue her from the town and bring her back to me.\
## Will you do that {playername}?", "lord_mission_told",
##   [
##       (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##       (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
##
##       (try_begin),
##         (troop_slot_eq, "$g_talk_troop", slot_troop_daughter, ":quest_object_troop"),
##         (str_store_string, s7, "str_daughter"),
##       (else_try),
##         (str_store_string, s7, "str_wife"),
##       (try_end),
##      
##       (str_store_troop_name_link,1,"$g_talk_troop"),
##       (str_store_party_name_link,2,"$g_encountered_party"),
##       (str_store_troop_name_link,3,":quest_object_troop"),
##       (str_store_party_name_link,4,":quest_target_center"),
##       (setup_quest_text,"$random_quest_no"),
##       (try_begin),
##         (is_between, "$g_encountered_party", centers_begin, centers_end),
##         (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##       (else_try),
##         (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##       (try_end),
##    ]],
##
##
##  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_bring_prisoners_to_enemy")],
##   "The enemy wants to ransom some of their soldiers that we captured at the last battle.\
## They'll pay 100 denars in return for giving them back {reg1} {s3}.\
## God knows I can use that money so I accepted their offer.\
## Now, what I need is someone to take the prisoners to {s4} and come back with the money.", "lord_mission_told",
##   [
##     (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
##     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##     (quest_get_slot, reg1, "$random_quest_no", slot_quest_target_amount),
##     (str_store_troop_name_link,1,"$g_talk_troop"),
##     (str_store_party_name_link,2,"$g_encountered_party"),
##     (str_store_troop_name_plural,3,":quest_object_troop"),
##     (str_store_party_name_link,4,":quest_target_center"),
##     (setup_quest_text,"$random_quest_no"),
##     (try_begin),
##       (is_between, "$g_encountered_party", centers_begin, centers_end),
##       (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##     (else_try),
##       (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##     (try_end),
##   ]],
##


# Deal with bandits
  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_deal_with_bandits_at_lords_village")],
   "A group of bandits have taken refuge in my village of {s1}.\
 They are plundering nearby farms, and getting rich and fat stealing my taxes and feasting on my cattle.\
I'd like nothing better than to go out there and teach them a lesson,\
 but I have my hands full at the moment, so I can't do anything about it.", "lord_mission_deal_with_bandits_told",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_party_name_link,s15,":quest_target_center"),
     (str_store_troop_name_link,s13,"$g_talk_troop"),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "@{s13} asked you to deal with the bandits who are occupying the village of {s15} and then report back to him."),
   ]],

  [anyone|plyr,"lord_mission_deal_with_bandits_told", [],
   "Worry not, I can go to {s1} and deal with these scum for you.", "lord_mission_deal_with_bandits_accepted",[]],
  [anyone|plyr,"lord_mission_deal_with_bandits_told", [], "You shall have to find help elsewhere, I am too busy.", "lord_mission_deal_with_bandits_rejected",[]],

  [anyone,"lord_mission_deal_with_bandits_accepted", [], "Will you do that?\
 Know that, I will be grateful to you. Here is some money for the expenses of your campaign.\
 Make an example of those {s44}s.", "close_window",
   [

    (troop_get_slot, ":insult_string", "$g_talk_troop", slot_lord_reputation_type),
    (val_add, ":insult_string", "str_lord_insult_default"),
    (str_store_string, 44, ":insult_string"),

    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_troop_add_gold", "trp_player", 200),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",3),
    (assign, "$g_leave_encounter",1),
   ]],

  [anyone,"lord_mission_deal_with_bandits_rejected", [], "Ah... Very well then, forget I brought it up.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],

# Raise troops
  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_raise_troops")],
   "No lord should have to admit this, {playername}, but I was inspecting my soldiers the other day\
 and there are men here who don't know which end of a sword to hold.\
 {s44}\
 You are a warrior of renown, {playername}. Will you train some troops for me?\
 I would be grateful to you.", "lord_tell_mission_raise_troops",[
    (troop_get_slot, ":training_string", "$g_talk_troop", slot_lord_reputation_type),
    (val_add, ":training_string", "str_troop_train_request_default"),
    (str_store_string, 44, ":training_string")
     ]],

  [anyone|plyr,"lord_tell_mission_raise_troops", [], "How many men do you need?", "lord_tell_mission_raise_troops_2",[]],

  [anyone,"lord_tell_mission_raise_troops_2", [], "If you can raise {reg1} {s14} and bring them to me, that will probably be enough.", "lord_mission_raise_troops_told",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, reg1, "$random_quest_no", slot_quest_target_amount),
     (str_store_troop_name_link,s9,"$g_talk_troop"),
     (str_store_troop_name_plural,s14,":quest_target_troop"),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to raise {reg1} {s14} and bring them to him."),
   ]],

  [anyone|plyr,"lord_mission_raise_troops_told", [(quest_get_slot, reg1, "$random_quest_no", slot_quest_target_amount)],
   "Of course, {s65}. Give me {reg1} fresh recruits and I'll train them to be {s14}.", "lord_mission_raise_troops_accepted",[]],
  [anyone|plyr,"lord_mission_raise_troops_told", [], "I am too busy these days to train anyone.", "lord_mission_raise_troops_rejected",[]],

  [anyone,"lord_mission_raise_troops_accepted", [], "You've taken a weight off my shoulders, {playername}.\
 I shall tell my sergeants to send you the recruits and attach them to your command.\
 Also, I'll advance you some money to help with expenses. Here, this purse should do it.\
 Thank you for your help.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_troop_add_gold", "trp_player",100),
    (quest_get_slot, ":recruit_troop", "$random_quest_no", slot_quest_object_troop),
    (quest_get_slot, ":num_recruits", "$random_quest_no", slot_quest_target_amount),
    (party_add_members, "p_main_party", ":recruit_troop", ":num_recruits"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",2),
    (assign, "$g_leave_encounter",1),
   ]],

  [anyone,"lord_mission_raise_troops_rejected", [], "Oh, of course. I had expected as much. Well, good luck to you then.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
  

#Collect Taxes
  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_collect_taxes"),
                                (assign, reg9, 0),
                                (try_begin),
                                  (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                  (party_slot_eq, ":quest_target_center", slot_party_type, spt_town),
                                  (assign, reg9, 1),
                                (try_end),
                                ], "You probably know that I am the lord of the {reg9?town:village} of {s3}.\
 However, it has been months since {s3} has delivered the taxes and rents due me as its rightful lord.\
 Apparently the populace there has grown unruly lately and I need someone to go there and remind them of\
 their obligations. And to . . . persuade them if they won't listen.\
 If you go there and raise the taxes they owe me, I will grant you one-fifth of everything you collect.", "lord_mission_collect_taxes_told",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_troop_name_link,s9,"$g_talk_troop"),
     (str_store_party_name_link,s3,":quest_target_center"),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to collect taxes from {s3}. He offered to leave you one-fifth of all the money you collect there."),
   ]],

  [anyone|plyr,"lord_mission_collect_taxes_told", [],
   "A fair offer, {s65}. We have an agreement.", "lord_mission_collect_taxes_accepted",[]],
  [anyone|plyr,"lord_mission_collect_taxes_told", [], "Forgive me, I don't have the time.", "lord_mission_collect_taxes_rejected",[]],

  [anyone,"lord_mission_collect_taxes_accepted", [], "Welcome news, {playername}.\
 I will entrust this matter to you.\
 Remember, those {reg9?townsmen:peasants} are foxy beasts, they will make every excuse not to pay me my rightful incomes.\
 Do not let them fool you.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",2),
    (assign, "$g_leave_encounter",1),
    (assign, reg9, 0),
    (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
    (try_begin),
      (party_slot_eq, ":quest_target_center", slot_party_type, spt_town),
      (assign, reg9, 1),
    (try_end),
   ]],
  
  [anyone,"lord_mission_collect_taxes_rejected", [], "Oh, yes. Well, good luck to you then.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],

#Hunt down fugitive
  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_hunt_down_fugitive")],
   "I have something you could help with, an issue with the lawless villain known as {s4}. \
 He murdered one of my men and has been on the run from his judgment ever since.\
 I can't let him get away with avoiding justice, so I've put a bounty of 300 denars on his head.\
 Friends of the murdered man reckon that this assassin may have taken refuge with his kinsmen at {s3}.\
 You might be able to hunt him down and give him what he deserves, and claim the bounty for yourself.", "lord_mission_hunt_down_fugitive_told",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, ":quest_target_dna", "$random_quest_no", slot_quest_target_dna),
     (str_store_troop_name_link,s9, "$g_talk_troop"),
     (str_store_party_name_link,s3, ":quest_target_center"),
     (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
     (str_store_string, s4, s50),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to hunt down a fugitive named {s4}. He is currently believed to be at {s3}."),
   ]],

  [anyone|plyr,"lord_mission_hunt_down_fugitive_told", [],
   "Then I will hunt him down and execute the law.", "lord_mission_hunt_down_fugitive_accepted",[]],
  [anyone|plyr,"lord_mission_hunt_down_fugitive_told", [], "I am too busy to go after him at the moment.", "lord_mission_hunt_down_fugitive_rejected",[]],

  [anyone,"lord_mission_hunt_down_fugitive_accepted", [], "That's excellent, {playername}.\
 I will be grateful to you and so will the family of the man he murdered.\
 And of course the bounty on his head will be yours if you can get him.\
 Well, good hunting to you.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",3),
    (assign, "$g_leave_encounter",1),
   ]],

  [anyone,"lord_mission_hunt_down_fugitive_rejected", [], "As you wish, {playername}.\
I suppose there are plenty of bounty hunters around to get the job done . . .", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],



##  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_capture_messenger")],
##   "The enemy seems to be preparing for some kind of action and I want to know what their plans are.\
## Capture one of their messengers and bring him to me.", "lord_mission_told",
##   [
##       (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
##      
##       (str_store_troop_name_link,1,"$g_talk_troop"),
##       (str_store_party_name_link,2,"$g_encountered_party"),
##       (str_store_troop_name,3,":quest_target_troop"),
##       (setup_quest_text,"$random_quest_no"),
##       (try_begin),
##         (is_between, "$g_encountered_party", centers_begin, centers_end),
##         (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##       (else_try),
##         (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##       (try_end),
##   ]],
##
  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_kill_local_merchant")],
   "The wretched truth is that I owe a considerable sum of money to one of the merchants here in {s3}.\
 I've no intention of paying it back, of course, but that loud-mouthed fool is making a terrible fuss about it.\
 He even had the audacity to come and threaten me -- me! --\
 with a letter of complaint to the trade guilds and bankers. Why, he'd ruin my good reputation!\
 So I need a {man/woman} I can trust, someone who will guarantee the man's silence. For good.", "lord_mission_told_kill_local_merchant",
   [
       (str_store_troop_name_link,s9,"$g_talk_troop"),
       (str_store_party_name_link,s3,"$current_town"),
       (setup_quest_text,"$random_quest_no"),
       (str_store_string, s2, "@{s9} asked you to assassinate a local merchant at {s3}."),
   ]],
  
  [anyone|plyr,"lord_mission_told_kill_local_merchant", [], "Worry not, he shan't breathe a word.", "lord_mission_accepted_kill_local_merchant",[]],
  [anyone|plyr,"lord_mission_told_kill_local_merchant", [], "I'm no common murderer, sir. Find someone else for your dirty job.", "lord_mission_rejected",[]],

  [anyone,"lord_mission_accepted_kill_local_merchant", [], "Very good. I trust in your skill and discretion,\
 {playername}. Do not disappoint me.\
 Go now and wait for my word, I'll send you a message telling when and where you can catch the merchant.\
 Dispose of him for me and I shall reward you generously.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (assign, "$g_leave_town",1),
    (assign, "$qst_kill_local_merchant_center", "$current_town"),
    (rest_for_hours, 10, 4, 0),
    (finish_mission),
    ]],

  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_meet_spy_in_enemy_town"),
                                (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                (str_store_party_name, s13, ":quest_target_center"),
                                (store_faction_of_party,":quest_target_center_faction",),
                                (str_store_faction_name, s14, ":quest_target_center_faction"),
                                ],
   "I have a sensitive matter which needs tending to, {playername}, and no trustworthy retainers to take care of it. The fact is that I have a spy in {s13} to keep an eye on things for me, and report anything that might warrant my attention. Every week I send someone to collect the spy's reports and bring them back to me. The job's yours if you wish it.", "lord_mission_told_meet_spy_in_enemy_town",
   [
   ]],

  [anyone|plyr,"lord_mission_told_meet_spy_in_enemy_town", [], "I don't mind a bit of skullduggery. Count me in.", "quest_meet_spy_in_enemy_town_accepted",[]],
  [anyone|plyr,"lord_mission_told_meet_spy_in_enemy_town", [], "I must decline. This cloak-and-dagger work isn't fit for me.", "quest_meet_spy_in_enemy_town_rejected",[]],

  [anyone,"quest_meet_spy_in_enemy_town_accepted", [], "Excellent! Make your way to {s13} as soon as you can, the spy will be waiting.", "quest_meet_spy_in_enemy_town_accepted_response",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, ":secret_sign", "$random_quest_no", slot_quest_target_amount),
     (store_sub, ":countersign", ":secret_sign", secret_signs_begin),
     (val_add, ":countersign", countersigns_begin),
     (str_store_troop_name_link, s9, "$g_talk_troop"),
     (str_store_string, s11, ":secret_sign"),
     (str_store_string, s12, ":countersign"),
     (str_store_party_name_link, s13, ":quest_target_center"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} has asked you to meet with a spy in {s13}."),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     (call_script, "script_cf_center_get_free_walker", ":quest_target_center"),
     (call_script, "script_center_set_walker_to_type", ":quest_target_center", reg0, walkert_spy),
     (str_store_item_name,s14,"$spy_item_worn"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter",1),
    ]],
  [anyone|plyr,"quest_meet_spy_in_enemy_town_accepted_response", [(quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                                                  (str_store_party_name_link, s13, ":quest_target_center")],
   "{s13} is heavily defended. How can I get close without being noticed?", "quest_meet_spy_in_enemy_town_accepted_2",
   []],
  [anyone,"quest_meet_spy_in_enemy_town_accepted_2", [], "You shall have to use stealth. Take care to avoid enemy strongholds, villages and patrols, and don't bring too many men with you. If you fail to sneak in the first time, give it a while for the garrison to lower its guard again, or you may have a difficult time infiltrating the town.", "quest_meet_spy_in_enemy_town_accepted_response",
   []],
  [anyone|plyr,"quest_meet_spy_in_enemy_town_accepted_response", [], "How will I recognise the spy?", "quest_meet_spy_in_enemy_town_accepted_3",
   []],
  [anyone,"quest_meet_spy_in_enemy_town_accepted_3", [(quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                                      (str_store_party_name_link, s13, ":quest_target_center"),
                                                      (troop_get_type, reg7, "$spy_quest_troop"),
                                                      (quest_get_slot, ":secret_sign", "$random_quest_no", slot_quest_target_amount),
                                                      (store_sub, ":countersign", ":secret_sign", secret_signs_begin),
                                                      (val_add, ":countersign", countersigns_begin),
                                                      (str_store_string, s11, ":secret_sign"),
                                                      (str_store_string, s12, ":countersign"),],
   "Once you get to {s13} you must talk to the locals, the spy will be one of them. If you think you've found the spy, say the phrase '{s11}' The spy will respond with the phrase '{s12}' Thus you will know the other, and {reg7?she:he} will give you any information {reg7?she:he}'s gathered in my service.", "quest_meet_spy_in_enemy_town_accepted_response",
   []],
  [anyone|plyr,"quest_meet_spy_in_enemy_town_accepted_response", [], "Will I be paid?", "quest_meet_spy_in_enemy_town_accepted_4",
   []],
  [anyone,"quest_meet_spy_in_enemy_town_accepted_4", [], "Of course, I have plenty of silver in my coffers for loyal {men/women} like you. Do well by me, {playername}, and you'll rise high.", "quest_meet_spy_in_enemy_town_accepted_response",
   []],
  [anyone|plyr,"quest_meet_spy_in_enemy_town_accepted_response", [], "I know what to do. Farewell, my lord.", "quest_meet_spy_in_enemy_town_accepted_end",
   []],
  [anyone,"quest_meet_spy_in_enemy_town_accepted_end", [(quest_get_slot, ":secret_sign", "$random_quest_no", slot_quest_target_amount),
                                                        (store_sub, ":countersign", ":secret_sign", secret_signs_begin),
                                                        (val_add, ":countersign", countersigns_begin),
                                                        (str_store_string, s11, ":secret_sign"),
                                                        (str_store_string, s12, ":countersign")],
   "Good luck, {playername}. Remember, the secret phrase is '{s11}' The counterphrase is '{s12}' Bring any reports back to me, and I'll compensate you for your trouble.", "lord_pretalk",
   []],

  [anyone,"quest_meet_spy_in_enemy_town_rejected", [], "As you wish, {playername}, but I strongly advise you to forget anything I told you about any spies. They do not exist, have never existed, and no one will ever find them. Remember that.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],


    

  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_raid_caravan_to_start_war"),
                                (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
                                (str_store_faction_name_link, s13, ":quest_target_faction")],
   "This peace with {s13} ill suits me, {playername}. We've let those swine have their way for far too long.\
 Now they get stronger with each passing and their arrogance knows no bounds.\
 I say, we must wage war on them before it's too late!\
 Unfortunately, some of the bleeding hearts among our realm's lords are blocking a possible declaration of war.\
 Witless cowards with no stomach for blood.", "lord_mission_told_raid_caravan_to_start_war",
   [
   ]],

  [anyone|plyr,"lord_mission_told_raid_caravan_to_start_war", [], "You are right, {s65}, but what can we do?", "lord_mission_tell_raid_caravan_to_start_war_2",[]],
  [anyone|plyr,"lord_mission_told_raid_caravan_to_start_war", [], "I disagree, sir. Peace is prefarable to war.", "quest_raid_caravan_to_start_war_rejected_1",[]],

  [anyone,"lord_mission_tell_raid_caravan_to_start_war_2", [(quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
                                                            (str_store_faction_name_link, s13, ":quest_target_faction")],
   "Ah, 'tis good to hear someone who understands!\
 As a matter of fact, there is something we can do, {playername}. A little bit of provocation.\
 The dogs in {s13} are very fond of their merchant caravans, and rely on them overmuch.\
 If one of our war parties managed to enter their territory and pillage some of their caravans,\
 they would have ample cause to declare war on our kingdom.\
 And then, well, even the cowards among us must rise to defend themselves.\
 So what do you say? Are you interested?", "lord_mission_tell_raid_caravan_to_start_war_3",[]],

  [anyone|plyr,"lord_mission_tell_raid_caravan_to_start_war_3", [], "An excellent plan. Count me in.", "quest_raid_caravan_to_start_war_accepted",[]],
  [anyone|plyr,"lord_mission_tell_raid_caravan_to_start_war_3", [], "Why don't you raid the caravans yourself?", "lord_mission_tell_raid_caravan_to_start_war_4",[]],

  [anyone,"lord_mission_tell_raid_caravan_to_start_war_4", [
  	], "Well, {playername}, some of the lords in our kingdom\
 won't like the idea of someone inciting a war without their consent.\
 They are already looking for an excuse to get at me, and if I did this they could make me pay for it dearly.\
 You, on the other hand, are young and well liked and daring, so you might just get away with it.\
 And of course I will back you up and defend your actions against your opponents.\
 All in all, a few lords might be upset at your endeavour, but I am sure you won't be bothered with that.", "lord_mission_tell_raid_caravan_to_start_war_5",[]],

  [anyone|plyr,"lord_mission_tell_raid_caravan_to_start_war_5", [], "Then I will go and raid those caravans!", "quest_raid_caravan_to_start_war_accepted",[]],
  [anyone|plyr,"lord_mission_tell_raid_caravan_to_start_war_5", [], "I don't like this. Find yourself someone else to take the blame for your schemes.", "quest_raid_caravan_to_start_war_rejected_2",[]],

  [anyone,"quest_raid_caravan_to_start_war_accepted", [], "Very good!\
 Now, don't forget that you must capture and loot at least {reg13} caravans to make sure that those fools in {s13} get really infuriated.\
 Once you do that, return to me and make sure you are not captured by their patrols.\
 If they catch you, our plan will fail without a doubt and you will be facing a long time in prisons.\
 Now, good luck and good hunting to you.", "close_window",
   [
     (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
     (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
     (str_store_troop_name_link, s9, "$g_talk_troop"),
     (str_store_faction_name_link, s13, ":quest_target_faction"),
     (assign, reg13, ":quest_target_amount"),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to capture and loot {reg13} caravans so as to provoke a war with {s13}."),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     (call_script, "script_change_player_relation_with_troop","$g_talk_troop",5),
     (assign, "$g_leave_encounter",1),
    ]],


  [anyone,"quest_raid_caravan_to_start_war_rejected_1", [], "Ah, you think so? But how long will your precious peace last? Not long, believe me.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
  [anyone,"quest_raid_caravan_to_start_war_rejected_2", [], "Hm. As you wish, {playername}.\
 I thought you had some fire in you, but it seems I was wrong.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],


  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_bring_back_runaway_serfs")],
 "Well, some of the serfs working my fields in {s4} have run away. The ungrateful swine,\
 I let them plough my fields and rent my cottages, and this is how they repay me!\
 From what I've been hearing, they're running to {s3} as fast as they can,\
 and have split up into three groups to try and avoid capture.\
 I want you to capture all three groups and fetch them back to {s4} by whatever means necessary.\
 I should really have them hanged for attempting to escape, but we need hands for the upcoming harvest,\
 so I'll let them go off this time with a good beating.", "lord_mission_told",
   [
       (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
       (quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),
      
       (str_store_troop_name_link, s9, "$g_talk_troop"),
       (str_store_party_name_link, s3, ":quest_target_center"),
       (str_store_party_name_link, s4, ":quest_object_center"),
       (setup_quest_text,"$random_quest_no"),
       (str_store_string, s2, "@{s9} asked you to catch the three groups of runaway serfs and bring them back to {s4}, alive and breathing. He said that all three groups are heading towards {s3}."),
    ]],

  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_follow_spy")],
 "I have good information that a man in this very town is actually an enemy spy.\
 He should be seized and hanged for his impudence,\
 but we also believe that very soon he will leave town to meet with his master,\
 the man to whom the spy feeds all his little whispers.\
 The spy himself is of little import, but the master is a dangerous man, and could tell us a great deal\
 if we could only get our hands on him...", "lord_tell_mission_follow_spy",[]],
  [anyone,"lord_tell_mission_follow_spy", [],
 "I want you to wait here until the spy leaves town. Then you must follow him, stealthily, to the meeting place.\
 You must take absolute care not to be seen by the spy on your way, else he may suspect foul play and turn back.\
 When the master appears, you must ambush and arrest them and bring the pair back to me.\
 Alive, if you please.", "lord_tell_mission_follow_spy_2",
   [
    ]],

  [anyone|plyr, "lord_tell_mission_follow_spy_2", [],
 "I'll do it, {s65}.", "lord_tell_mission_follow_spy_accepted", []],
  [anyone|plyr, "lord_tell_mission_follow_spy_2", [],
 "No, this skulking is not for me.", "lord_tell_mission_follow_spy_rejected", []],


  [anyone,"lord_tell_mission_follow_spy_accepted", [],
   "Good, I'm sure you'll do a fine job of it. One of my men will point the spy out to you when he leaves,\
 so you will know the man to follow. Remember, I want them both, and I want them alive.", "close_window",
   [
     (str_store_troop_name_link, s11, "$g_talk_troop"),
     (str_store_party_name_link, s12, "$g_encountered_party"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to follow the spy that will leave {s12}. Be careful not to let the spy see you on the way, or he may get suspicious and turn back. Once the spy meets with his accomplice, you are to capture them and bring them back to {s11}."),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),

     (spawn_around_party, "p_main_party", "pt_spy_partners"),
     (assign, "$qst_follow_spy_spy_partners_party", reg0),
     (party_set_position, "$qst_follow_spy_spy_partners_party", pos63),
     (party_set_ai_behavior, "$qst_follow_spy_spy_partners_party", ai_bhvr_hold),
     (party_set_flags, "$qst_follow_spy_spy_partners_party", pf_default_behavior, 0),
     (set_spawn_radius, 0),
     (spawn_around_party, "$g_encountered_party", "pt_spy"),
     (assign, "$qst_follow_spy_spy_party", reg0),
     (party_set_ai_behavior, "$qst_follow_spy_spy_party", ai_bhvr_travel_to_party),
     (party_set_ai_object, "$qst_follow_spy_spy_party", "$qst_follow_spy_spy_partners_party"),
     (party_set_flags, "$qst_follow_spy_spy_party", pf_default_behavior, 0),
     (assign, "$g_leave_town", 1),
     (rest_for_hours, 2, 4, 0),
     #no need to set g_leave_encounter to 1 since this quest can only be given at a town
   ]],

  [anyone,"lord_tell_mission_follow_spy_rejected", [],
   "A shame. Well, carry on as you were, {playername}...", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],




  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_capture_enemy_hero")],
 "There is a difficult job I need done, {playername}, and you may be the {man/one} who can carry it off.\
 I need someone to capture one of the noble lords of {s13} and bring him to me.\
 Afterwards, I'll be able to exchange him in return for a relative of mine held by {s13}.\
 It is a simple enough job, but whomever you choose will be guarded by an elite band of personal retainers.\
 Are you up for a fight?", "lord_tell_mission_capture_enemy_hero",
   [
     (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
     (str_store_faction_name, s13, ":quest_target_faction"),
    ]],

  [anyone|plyr, "lord_tell_mission_capture_enemy_hero", [],
 "Consider it done, {s65}.", "lord_tell_mission_capture_enemy_hero_accepted", []],
  [anyone|plyr, "lord_tell_mission_capture_enemy_hero", [],
 "I must refuse, {s65}. I am not a kidnapper.", "lord_tell_mission_capture_enemy_hero_rejected", []],

  [anyone,"lord_tell_mission_capture_enemy_hero_accepted", [],
   "I like your spirit! Go and bring me one of our enemies,\
 and I'll toast your name in my hall when you return! And reward you for your efforts, of course...", "close_window",
   [
     (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
     (str_store_troop_name_link, s11, "$g_talk_troop"),
     (str_store_faction_name_link, s13, ":quest_target_faction"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to capture a lord from {s13}, any lord, and then drag your victim back to {s11} for safekeeping."),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter",1),
   ]],

  [anyone,"lord_tell_mission_capture_enemy_hero_rejected", [],
   "Clearly you lack the mettle I had thought you possessed. Very well, {playername}, I will find someone else.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],




  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_lend_companion")],
 "I don't have a job for you right now, but your companion {s3} is a skilled {reg3?lass:fellow}\
 and I need someone with {reg3?her:his} talents. Will you lend {reg3?her:him} to me for a while?", "lord_tell_mission_lend_companion",
   [
       (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
       (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
       (val_add, ":quest_target_amount", 1),
       (assign, reg1, ":quest_target_amount"),
       (str_store_troop_name_link,s9,"$g_talk_troop"),
       (str_store_troop_name,s3,":quest_target_troop"),
       (setup_quest_text,"$random_quest_no"),
       (troop_get_type, reg3, ":quest_target_troop"),
       (str_store_string, s2, "@{s9} asked you to lend your companion {s3} to him for a week."),
    ]],
  [anyone|plyr,"lord_tell_mission_lend_companion", [],
 "How long will you be needing {reg3?her:him}?", "lord_tell_mission_lend_companion_2", []],
  [anyone,"lord_tell_mission_lend_companion_2", [],
 "Just a few days, a week at most.", "lord_mission_lend_companion_told", []],

  [anyone|plyr,"lord_mission_lend_companion_told",
   [(quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),(str_store_troop_name,s3,":quest_target_troop"),],
   "Then I will leave {s3} with you for one week.", "lord_tell_mission_lend_companion_accepted", []],
  [anyone|plyr,"lord_mission_lend_companion_told", [(quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
                                                    (str_store_troop_name,s3,":quest_target_troop"),],
   "I am sorry, but I cannot do without {s3} for a whole week.", "lord_tell_mission_lend_companion_rejected", []],

  [anyone,"lord_tell_mission_lend_companion_accepted", [],
   "I cannot thank you enough, {playername}. Worry not, your companion shall be returned to you with due haste.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",3),
    (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
    (party_remove_members, "p_main_party", ":quest_target_troop", 1),
    (assign, "$g_leave_encounter",1),
   ]],

  [anyone,"lord_tell_mission_lend_companion_rejected", [],
   "Well, that's damned unfortunate, but I suppose I cannot force you or {s3} to agree.\
 I shall have to make do without.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],

 
  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_collect_debt")],
   "Some time ago, I loaned out a considerable sum of money to {s3}. {reg4} denars, to be precise.\
 He was supposed to pay it back within a month but I haven't received a copper from him since.\
 That was months ago. If you could collect the debt from him on my behalf,\
 I would be grateful indeed. I would even let you keep one fifth of the money for your trouble.\
 What do you say?", "lord_tell_mission_collect_debt",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, reg4, "$random_quest_no", slot_quest_target_amount),
     (str_store_troop_name_link,s9,"$g_talk_troop"),
     (str_store_troop_name_link,s3,":quest_target_troop"),
     (str_store_party_name_link,s4,":quest_target_center"),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to collect the debt of {reg4} denars {s3} owes to him. {s3} was at {s4} when you were given this quest."),
   ]],
  [anyone|plyr,"lord_tell_mission_collect_debt", [],
 "Do you know where I can find {s3}, {s65}?", "lord_tell_mission_collect_debt_2", []],
  [anyone,"lord_tell_mission_collect_debt_2", [],
 "If you leave now, you should be able to find him at {s4}.\
 I've no doubt that he will be suitably embarassed by his conduct and give you all the money he owes me.", "lord_tell_mission_collect_debt_3", []],
  [anyone|plyr,"lord_tell_mission_collect_debt_3", [], "Then I will talk to {s3} on your behalf.", "lord_tell_mission_collect_debt_accepted", []],
  [anyone|plyr,"lord_tell_mission_collect_debt_3", [], "Forgive me, {s65}, but I doubt I would be more successful than yourself.", "lord_tell_mission_collect_debt_rejected", []],

  [anyone,"lord_tell_mission_collect_debt_accepted", [], "You made me very happy by accepting this {playername}. Please, talk to {s3} and don't leave him without my money.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",2),
    (assign, "$g_leave_encounter",1),
   ]],

  [anyone,"lord_tell_mission_collect_debt_rejected", [], "Perhaps not, {playername}. I suppose I'm never getting that money back...", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
 
##
##  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_capture_conspirators")],
## "TODO: I want you to capture troops in {reg1} conspirator parties that plan to rebel against me and join {s3}.", "lord_mission_told",
##   [
##       (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
##       (assign, reg1, "$qst_capture_conspirators_num_parties_to_spawn"),
##       (str_store_troop_name_link,1,"$g_talk_troop"),
##       (str_store_party_name_link,2,"$g_encountered_party"),
##       (str_store_troop_name,3,":quest_target_troop"),
##       (setup_quest_text,"$random_quest_no"),
##       (try_begin),
##         (is_between, "$g_encountered_party", centers_begin, centers_end),
##         (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##       (else_try),
##         (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##       (try_end),
##    ]],
##
##
##  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_defend_nobles_against_peasants")],
## "TODO: I want you to defend {reg1} noble parties against peasants.", "lord_mission_told",
##   [
##       (assign, reg1, "$qst_defend_nobles_against_peasants_num_noble_parties_to_spawn"),
##       (str_store_troop_name_link,1,"$g_talk_troop"),
##       (str_store_party_name_link,2,"$g_encountered_party"),
##       (setup_quest_text,"$random_quest_no"),
##       (try_begin),
##         (is_between, "$g_encountered_party", centers_begin, centers_end),
##         (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##       (else_try),
##         (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##       (try_end),
##    ]],
##
##
  [anyone,"lord_tell_mission", [(eq, "$random_quest_no", "qst_incriminate_loyal_commander"),
                                (quest_get_slot, ":quest_target_troop", "qst_incriminate_loyal_commander", slot_quest_target_troop),
                                (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
                                (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                                (str_store_troop_name_link, s13,":quest_target_troop"),
                                (str_store_party_name_link, s14,":quest_target_center"),
                                (str_store_troop_name_link, s15,":quest_object_troop"),
                                ],
 "I tell you, that blubbering fool {s13} is not fit to rule {s14}.\
 God knows he would be divested of his lands in an instant were it not for one of his loyal vassals, {s15}.\
 As long as he has his vassal aiding him, it will be a difficult job beating him.\
 So I need to get {s15} out of the picture, and I have a plan just to do that...\
 With your help, naturally.", "lord_tell_mission_incriminate_commander",[]],

  [anyone|plyr,"lord_tell_mission_incriminate_commander", [], "{s66}, I am all ears.", "lord_tell_mission_incriminate_commander_2",[]],
  [anyone|plyr,"lord_tell_mission_incriminate_commander", [], "I don't wish to involve myself in anything dishonourable against {s15}.", "lord_tell_mission_incriminate_commander_rejected",[]],

  [anyone,"lord_tell_mission_incriminate_commander_rejected", [], "Dishonourable? Bah!\
 I was hoping I could count on you, {playername}, but you've shown me what a fool I was.\
 I shall have to find someone whose loyalty I can trust.", "lord_pretalk",
   [(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-5),
    (call_script, "script_change_player_honor", 2)]],

  [anyone,"lord_tell_mission_incriminate_commander_2", [], "I have written a fake letter to {s15},\
 bearing my own seal, which implicates him in a conspiracy with us to stage a coup in {s14}, in my favour.\
 If we can make {s13} believe the letter is genuine, he will deal with {s15} very swiftly.\
 Of course, the challenge there is to convince {s13} that the letter is indeed real...", "lord_tell_mission_incriminate_commander_3",[]],

  [anyone|plyr,"lord_tell_mission_incriminate_commander_3", [], "Please continue, {s65}...", "lord_tell_mission_incriminate_commander_4",[]],
  [anyone|plyr,"lord_tell_mission_incriminate_commander_3", [], "No, I will not sully myself with this dishonourable scheme.", "lord_tell_mission_incriminate_commander_rejected",[]],

  [anyone,"lord_tell_mission_incriminate_commander_4", [], "This is where you come into play.\
 You'll take the letter to {s14}, then give it to one of your soldiers and instruct him to take it to {s15}.\
 I will have one of my spies inform the town garrison so that your man will be arrested on his way.\
 The guards will then find the letter and take it to {s13}.\
 They'll torture your man, of course, to try and get the truth out of him,\
 but all he knows is that you ordered the letter to be delivered to {s15} under the utmost secrecy.\
 {s13} knows you serve me, and the fool will certainly believe the whole charade.", "lord_tell_mission_incriminate_commander_5",[]],
  
  [anyone|plyr,"lord_tell_mission_incriminate_commander_5", [], "Is that all?", "lord_tell_mission_incriminate_commander_7",[]],
  [anyone,"lord_tell_mission_incriminate_commander_7", [(str_store_troop_name, s8, "$incriminate_quest_sacrificed_troop"),
                                                        (str_store_troop_name_plural, s9, "$incriminate_quest_sacrificed_troop"),
      ], "There is one more thing...\
 Your messenger must be someone trustworthy. If you sent the letter with a simple peasant, someone expendable,\
 {s13} might suspect a plot. He may have the wits of a snail, but even a snail can see the obvious.\
 Give the letter to someone of rank. One of your {s9}, perhaps.", "lord_tell_mission_incriminate_commander_8",[]],
  [anyone|plyr,"lord_tell_mission_incriminate_commander_8", [], "What? I can't send one of my trusted {s9} to his death!", "lord_tell_mission_incriminate_commander_9",[]],
  [anyone|plyr,"lord_tell_mission_incriminate_commander_8", [], "Then a {s8} it will be.", "lord_tell_mission_incriminate_commander_fin",[]],
  [anyone,"lord_tell_mission_incriminate_commander_9", [], "Come now, {playername}.\
 There is a place for sentimentality, but this is not it. Believe me, you shall be generously compensated,\
 and what is the purpose of soldiers if not to die at our say-so?", "lord_tell_mission_incriminate_commander_10",[]],
  [anyone|plyr,"lord_tell_mission_incriminate_commander_10", [], "A {s8} it is.", "lord_tell_mission_incriminate_commander_fin",[]],
  [anyone|plyr,"lord_tell_mission_incriminate_commander_10", [], "No, I'll not sacrifice one of my chosen men.", "lord_tell_mission_incriminate_commander_rejected",[]],
   
 [anyone,"lord_tell_mission_incriminate_commander_fin", [], "I can't tell you how pleased I am to hear that,\
 {playername}. You are removing one of the greatest obstacles in my path.\
 Here is the letter, as well as 300 denars for your expenses.\
 Remember, there'll be more once you succeed. Much, much more...", "lord_pretalk",
   [
       (quest_get_slot, ":quest_target_troop", "qst_incriminate_loyal_commander", slot_quest_target_troop),
       (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
       (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
       (call_script, "script_troop_add_gold", "trp_player",300),
       (call_script, "script_change_player_relation_with_troop","$g_talk_troop",3),
       (str_store_troop_name_link, s11,"$g_talk_troop"),
       (str_store_troop_name_link, s13,":quest_target_troop"),
       (str_store_party_name_link, s14,":quest_target_center"),
       (str_store_troop_name_plural, s15,"$incriminate_quest_sacrificed_troop"),
       (str_store_troop_name_link, s16,":quest_object_troop"),
       (setup_quest_text,"$random_quest_no"),
       (str_store_string, s2, "@{s11} gave you a fake letter to fool {s13} into banishing his vassal {s16}.\
 You are to go near {s14}, give the letter to one of your {s15} and send him into the town as a messenger,\
 believing his orders to be genuine."),
       (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],

  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_capture_prisoners")],
 "A group of my soldiers were captured in a recent skirmish with the enemy.\
 Thankfully we have a mutual agreement of prisoner exchange, and they will release my men,\
 but they want us to give them prisoners of equal rank and number. Prisoners I don't currently have.\
 So, I need a good {man/warrior} to find me {reg1} {s3} as prisoners, that I may exchange them.", "lord_mission_told",
   [
       (quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
       (quest_get_slot, ":quest_target_amount", "qst_capture_prisoners", slot_quest_target_amount),
       (assign,reg1,":quest_target_amount"),
       (str_store_troop_name_link,s9,"$g_talk_troop"),
##       (str_store_party_name,2,"$g_encountered_party"),
       (str_store_troop_name_by_count,3,":quest_target_troop",":quest_target_amount"),
       (setup_quest_text,"$random_quest_no"),
##       (try_begin),
##         (is_between, "$g_encountered_party", centers_begin, centers_end),
##         (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##       (else_try),
##         (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##       (try_end),
       (str_store_string, s2, "@{s9} has requested you to bring him {reg1} {s3} as prisoners."),
    ]],

  [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_rescue_prisoners")],
 "{s5}", "lord_mission_told",
   [
       (quest_get_slot, ":quest_target_amount", "qst_rescue_prisoners", slot_quest_target_amount),
       (assign,reg1,":quest_target_amount"),
       (str_store_troop_name_link,s9,"$g_talk_troop"),
       (try_begin),
         (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
         (str_store_string, s5, "@We have reports that several of our allied patrols were ambushed and defeated.\
 Some of the men may still yet live, captured by the enemy.\
 Yet, the morale of my troops suffers, as the captured men will surely be killed, imprisoned or worse.\
 I want you to rescue {reg1} prisoners, and bolster the morale of our troops."), #Good
       (else_try),
         (str_store_string, s5, "@We have reports that several of our patrols were ambushed and defeated.\
 Some of the cowards may still yet live, captured by the enemy.\
 As much as they are expendable, it's a waste to let them die in some prison hole.\
 I want you to rescue {reg1} prisoners, and make them fight for us again."), #Evil
       (try_end),
       (setup_quest_text,"$random_quest_no"),
       (str_store_string, s2, "@{s9} has asked you to rescue {reg1} prisoners."),
    ]],
    

  [anyone,"lord_tell_mission", [], "No {playername}. I do not need your help at this time.", "lord_pretalk",[]],


  [anyone|plyr,"lord_mission_told", [], "You can count on me, {s65}.", "lord_mission_accepted",[]],
  [anyone|plyr,"lord_mission_told", [], "I fear I cannot accept such a mission at the moment.", "lord_mission_rejected",[]],

  [anyone,"lord_mission_accepted", [], "Excellent, {playername}, excellent. I have every confidence in you.", "close_window",
   [(assign, "$g_leave_encounter",1),
    (try_begin),
      (eq, "$random_quest_no", "qst_escort_lady"),
      (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
      (troop_set_slot, ":quest_object_troop", slot_troop_cur_center, 0),
      (troop_join, ":quest_object_troop"),
##    (else_try),
##      (eq, "$random_quest_no", "qst_hunt_down_raiders"),
##      (quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),
##      (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##      (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
##      (set_spawn_radius, 3),
##      (call_script, "script_cf_create_kingdom_party", ":quest_target_faction", spt_raider),
###      (spawn_around_party,":quest_object_center",":quest_target_party_template"),
##      (assign, ":quest_target_party", reg0),
##      (party_relocate_near_party, reg0, ":quest_object_center"),
##      (quest_set_slot, "$random_quest_no", slot_quest_target_party, ":quest_target_party"),
##      (party_set_ai_behavior,":quest_target_party",ai_bhvr_travel_to_party),
##      (party_set_ai_object,":quest_target_party",":quest_target_center"),
##      (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
##      (party_set_faction,":quest_target_party",":quest_target_faction"),
##      (str_store_troop_name,1,"$g_talk_troop"),
##      (str_store_party_name,2,"$g_encountered_party"),
##      (str_store_party_name,3,":quest_object_center"),
##      (str_store_party_name,4,":quest_target_center"),
##      (setup_quest_text,"$random_quest_no"),
##      (try_begin),
##        (is_between, "$g_encountered_party", centers_begin, centers_end),
##        (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##      (else_try),
##        (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##      (try_end),
##    (else_try),
##      (eq, "$random_quest_no", "qst_bring_reinforcements_to_siege"),
##      (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
##      (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
##      (troop_get_slot, ":cur_party", "$g_talk_troop", slot_troop_leaded_party),
##      (party_remove_members, ":cur_party", ":quest_object_troop", ":quest_target_amount"),
##      (party_add_members, "p_main_party", ":quest_object_troop", ":quest_target_amount"),
##    (else_try),
##      (eq, "$random_quest_no", "qst_bring_prisoners_to_enemy"),
##      (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
##      (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
##      (party_add_prisoners, "p_main_party", ":quest_object_troop", ":quest_target_amount"),
    (else_try),
      (eq, "$random_quest_no", "qst_deliver_message_to_enemy_lord"),
      (call_script, "script_troop_add_gold", "trp_player",10),
    (else_try),
      (eq, "$random_quest_no", "qst_bring_back_runaway_serfs"),
      (quest_get_slot, ":quest_giver_center", "$random_quest_no", slot_quest_giver_center),
      (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
      (quest_get_slot, ":quest_target_party_template", "$random_quest_no", slot_quest_target_party_template),

      (set_spawn_radius, 3),
      (spawn_around_party,":quest_giver_center",":quest_target_party_template"),
      (assign, "$qst_bring_back_runaway_serfs_party_1", reg0),
      (party_set_ai_behavior,"$qst_bring_back_runaway_serfs_party_1",ai_bhvr_travel_to_party),
      (party_set_ai_object,"$qst_bring_back_runaway_serfs_party_1",":quest_target_center"),
      (party_set_flags, "$qst_bring_back_runaway_serfs_party_1", pf_default_behavior, 0),
      (spawn_around_party,":quest_giver_center",":quest_target_party_template"),
      (assign, "$qst_bring_back_runaway_serfs_party_2", reg0),
      (party_set_ai_behavior,"$qst_bring_back_runaway_serfs_party_2",ai_bhvr_travel_to_party),
      (party_set_ai_object,"$qst_bring_back_runaway_serfs_party_2",":quest_target_center"),
      (party_set_flags, "$qst_bring_back_runaway_serfs_party_2", pf_default_behavior, 0),
      (spawn_around_party,":quest_giver_center",":quest_target_party_template"),
      (assign, "$qst_bring_back_runaway_serfs_party_3", reg0),
      (party_set_ai_behavior,"$qst_bring_back_runaway_serfs_party_3",ai_bhvr_travel_to_party),
      (party_set_ai_object,"$qst_bring_back_runaway_serfs_party_3",":quest_target_center"),
      (party_set_flags, "$qst_bring_back_runaway_serfs_party_3", pf_default_behavior, 0),
      (rest_for_hours, 1, 4),
##    (else_try),
##      (eq, "$random_quest_no", "qst_capture_conspirators"),
##      (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##      (spawn_around_party,"p_main_party","pt_conspirator_leader"),
##      (assign, "$qst_capture_conspirators_party_1", reg0),
##      (assign, "$qst_capture_conspirators_num_parties_spawned", 1),
##      (party_set_ai_behavior, "$qst_capture_conspirators_party_1", ai_bhvr_hold),
##      (party_set_flags, "$qst_capture_conspirators_party_1", pf_default_behavior, 0),
##      (party_get_position, pos1, ":quest_target_center"),
##      (call_script, "script_map_get_random_position_around_position_within_range", 17, 19),
##      (party_set_position, "$qst_capture_conspirators_party_1", pos2),
##      (party_get_num_companions, ":num_companions", "$qst_capture_conspirators_party_1"),
##      (val_add, "$qst_capture_conspirators_num_troops_to_capture", ":num_companions"),
##    (else_try),
##      (eq, "$random_quest_no", "qst_defend_nobles_against_peasants"),
##      (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##      (set_spawn_radius, 9),
##      (try_for_range, ":unused", 0, "$qst_defend_nobles_against_peasants_num_peasant_parties_to_spawn"),
##        (spawn_around_party, ":quest_target_center", "pt_peasant_rebels"),
##        (try_begin),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_1", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_1", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_2", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_2", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_3", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_3", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_4", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_4", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_5", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_5", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_6", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_6", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_7", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_7", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_8", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_8", reg0),
##        (try_end),
##      (try_end),
##      (set_spawn_radius, 0),
##      (party_get_position, pos1, ":quest_target_center"),
##      (try_for_range, ":unused", 0, "$qst_defend_nobles_against_peasants_num_noble_parties_to_spawn"),
##        (spawn_around_party, ":quest_target_center", "pt_noble_refugees"),
##        (assign, ":cur_noble_party", reg0),
##        (party_set_ai_behavior, ":cur_noble_party", ai_bhvr_travel_to_party),
##        (party_set_ai_object, ":cur_noble_party", ":quest_target_center"),
##	    (party_set_flags, ":cur_noble_party", pf_default_behavior, 0),
##        (call_script, "script_map_get_random_position_around_position_within_range", 13, 17),
##        (party_set_position, ":cur_noble_party", pos2),
##        (party_get_num_companions, ":num_companions", ":cur_noble_party"),
##        (val_add, "$qst_defend_nobles_against_peasants_num_nobles_to_save", ":num_companions"),
##        (try_begin),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_1", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_1", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_2", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_2", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_3", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_3", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_4", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_4", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_5", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_5", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_6", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_6", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_7", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_7", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_8", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_8", reg0),
##        (try_end),
##      (try_end),
    (try_end),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (try_begin),
      (eq, "$random_quest_no", "qst_lend_surgeon"),
      (assign, "$g_leave_town_outside", 1),
      (assign,"$auto_enter_town","$g_encountered_party"),
#      (store_current_hours, "$quest_given_time"),
      (rest_for_hours, 4),
      (assign, "$lord_requested_to_talk_to", "$g_talk_troop"),
    (try_end),
    ]],
  [anyone,"lord_mission_rejected", [], "Is that so? Well, I suppose you're just not up to the task.\
 I shall have to look for somebody with more mettle.", "close_window",
   [(assign, "$g_leave_encounter",1),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (try_begin),
      (quest_slot_eq, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 0),
      (quest_set_slot, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 1),
    (try_end),
    (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    ]],


##### TODO: QUESTS COMMENT OUT END

#Leave
  [anyone|plyr,"lord_talk", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 1),
							 (troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
  ], "I must leave now.", "lord_leave_prison",[]],
  [anyone|plyr,"lord_talk", [(lt, "$g_talk_troop_faction_relation", 0)], "This audience is over. I leave now.", "lord_leave",[]],
  [anyone|plyr,"lord_talk", [(ge, "$g_talk_troop_faction_relation", 0)], "I must beg my leave.", "lord_leave",[]],

  [anyone,"lord_leave", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
      (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
      (lt, "$g_talk_troop_faction_relation", 0),
      (store_partner_quest,":enemy_lord_quest"),
      (lt, ":enemy_lord_quest", 0),
      (troop_slot_eq, "$g_talk_troop", slot_troop_does_not_give_quest, 0),      
      (call_script, "script_get_random_quest", "$g_talk_troop"),
      (assign, "$random_quest_no", reg0),
      (ge, "$random_quest_no", 0),
    ],
   "Before you go, {playername}, I have something to ask of you... We may be enemies in this war,\
 but I pray that you believe, as I do, that we can still be civil towards each other.\
 Thus I hoped that you would be kind enough to assist me in something important to me.", "lord_leave_give_quest",[]],

  [anyone|plyr,"lord_leave_give_quest", [],
   "I am listening.", "enemy_lord_tell_mission",[]],


  [anyone,"enemy_lord_tell_mission", [(eq,"$random_quest_no","qst_lend_surgeon")],
   "I have a friend here, an old warrior, who is very sick. Pestilence has infected an old battle wound,\
 and unless he is seen to by a surgeon soon,  he will surely die. This man is dear to me, {playername},\
 but he's also stubborn as a hog and refuses to have anyone look at his injury because he doesn't trust the physicians here.\
 I have heard that you've a capable surgeon with you. If you would let your surgeon come here and have a look,\
 {reg3?she:he} may be able to convince him to give his consent to an operation.\
 Please, I will be deeply indebted to you if you grant me this request.", "lord_mission_told",
   [
     (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
     (str_store_troop_name_link,1,"$g_talk_troop"),
##     (str_store_party_name,2,"$g_encountered_party"),
     (str_store_troop_name,3,":quest_object_troop"),
     (troop_get_type, reg3, ":quest_object_troop"),
     (setup_quest_text,"$random_quest_no"),
##     (try_begin),
##       (is_between, "$g_encountered_party", centers_begin, centers_end),
##       (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##     (else_try),
##       (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##     (try_end),
     (str_store_string, s2, "@Lend your experienced surgeon {s3} to {s1}."),
   ]],

  [anyone,"enemy_lord_tell_mission", [(str_store_quest_name, s7, "$random_quest_no")],
   "ERROR: MATCHED WITH QUEST: {s7}.", "close_window",
   []],

  [anyone,"lord_leave_prison", [],
   "We'll meet again.", "close_window",[]],

  [anyone|auto_proceed,"lord_leave", [(faction_slot_eq,"$g_talk_troop_faction",slot_faction_leader,"$g_talk_troop")],
   "Of course, {playername}. Farewell.", "close_window",[(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],
  [anyone|auto_proceed,"lord_leave", [(ge,"$g_talk_troop_relation",10)],
   "Good journeys to you, {playername}.", "close_window",[(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],
  [anyone|auto_proceed,"lord_leave", [(ge, "$g_talk_troop_faction_relation", 0)],
   "Yes, yes. Farewell.", "close_window",[(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],
  [anyone|auto_proceed,"lord_leave", [],
   "We will meet again.", "close_window",[(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],


#Royal family members

  [anyone|plyr,"member_chat", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady)],
   "Are you enjoying the journey, {s65}?", "lady_journey_1",[]],
  [anyone,"lady_journey_1", [],
   "I am doing quite fine, {playername}. Thank you for your concern.", "close_window",[]],
  
  [anyone,"start",
   [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
    (check_quest_active, "qst_duel_for_lady"),
    (check_quest_succeeded, "qst_duel_for_lady"),
    (quest_slot_eq, "qst_duel_for_lady", slot_quest_giver_troop, "$g_talk_troop"),
    (le, "$talk_context", tc_siege_commander),
    (quest_get_slot, ":quest_target_troop", "qst_duel_for_lady", slot_quest_target_troop),
    (str_store_troop_name_link, s13, ":quest_target_troop"),
    ],
   "My dear {playername}, how joyous to see you again! I heard you gave that vile {s13} a well-deserved lesson.\
 I hope he never forgets his humiliation.\
 I've a reward for you, but I fear it's little compared to what you've done for me.", "lady_qst_duel_for_lady_succeeded_1",[]],
  [anyone|plyr,"lady_qst_duel_for_lady_succeeded_1", [], "Oh, it will just have to do.", "lady_qst_duel_for_lady_succeeded_2",[
  (str_store_string,s10,"@Then take it, with my eternal thanks. You are a noble {man/woman}.\
 I will never forget that you helped me in my time of need.")
  ]],
  [anyone|plyr,"lady_qst_duel_for_lady_succeeded_1", [], "{s66}, this is far too much!", "lady_qst_duel_for_lady_succeeded_2",[
  (str_store_string,s10,"@Forgive me, {playername}, but I must insist you accept it.\
 The money means little to me, and I owe you so much.\
 Here, take it, and let us speak no more of this."),
    (call_script, "script_change_player_honor", 1),
  ]],
  [anyone|plyr,"lady_qst_duel_for_lady_succeeded_1", [], "Please, {s65}, no reward is necessary.", "lady_qst_duel_for_lady_succeeded_2",[
  (str_store_string,s10,"@{playername}, what a dear {man/woman} you are,\
 but I will not allow you to refuse this. I owe you far more than I can say,\
 and I am sure you can put this money to far better use than I."),
    (call_script, "script_change_player_honor", 2),
  ]],
  [anyone,"lady_qst_duel_for_lady_succeeded_2", [], "{s10}", "lady_pretalk",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 10),
    (add_xp_as_reward, 1000),
    (call_script, "script_troop_add_gold", "trp_player", 2000),
    (call_script, "script_end_quest", "qst_duel_for_lady"),
    ]],

  [anyone,"start",
   [
     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
     (check_quest_active, "qst_duel_for_lady"),
     (check_quest_failed, "qst_duel_for_lady"),
     (quest_slot_eq, "qst_duel_for_lady", slot_quest_giver_troop, "$g_talk_troop"),
     (le, "$talk_context", tc_siege_commander),
     (quest_get_slot, ":quest_target_troop", "qst_duel_for_lady", slot_quest_target_troop),
     (str_store_troop_name_link, s13, ":quest_target_troop"),
     ],
   "I was told that you sought satisfaction from {s13} to prove my innocence, {playername}.\
 It was a fine gesture, and I thank you for your efforts.", "lady_qst_duel_for_lady_failed", []],
  [anyone|plyr,"lady_qst_duel_for_lady_failed", [], "I beg your forgiveness for my defeat, {s65}...", "lady_qst_duel_for_lady_failed_2",[]],
  [anyone,"lady_qst_duel_for_lady_failed_2", [], "It matters not, dear {playername}. You tried.\
 The truth cannot be proven at the point of a sword, but you willingly put your life at stake for my honour.\
 That alone will convince many of my innocence.", "lady_pretalk",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 6),
    (add_xp_as_reward, 400),
    (call_script, "script_end_quest", "qst_duel_for_lady"),
    ]],


  [anyone,"start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
                    (check_quest_active, "qst_escort_lady"),
                    (eq, "$talk_context", tc_entering_center_quest_talk),
                    (quest_slot_eq, "qst_escort_lady", slot_quest_object_troop, "$g_talk_troop")],
   "Thank you for escorting me here, {playername}. Please accept this gift as a token of my gratitude.\
 I hope we shall meet again sometime in the future.", "lady_escort_lady_succeeded",
   [
     (quest_get_slot, ":cur_center", "qst_escort_lady", slot_quest_target_center),
     (add_xp_as_reward, 300),
     (call_script, "script_troop_add_gold", "trp_player", 250),
     (call_script, "script_end_quest", "qst_escort_lady"),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
     (troop_set_slot, "$g_talk_troop", slot_troop_cur_center, ":cur_center"),
     (remove_member_from_party,"$g_talk_troop"),
     ]],

  [anyone|plyr,"lady_escort_lady_succeeded", [], "It was an honor to serve you, {s65}.", "close_window",[]],

                                                                                     
  [anyone,"start", [
    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
    (le, "$talk_context", tc_siege_commander),
    (check_quest_active, "qst_rescue_lord_by_replace"),
    (check_quest_succeeded, "qst_rescue_lord_by_replace"),
    (quest_slot_eq, "qst_rescue_lord_by_replace", slot_quest_giver_troop, "$g_talk_troop"),
    (troop_get_slot, ":cur_lord", "$g_talk_troop", slot_troop_father),
    (try_begin),
      (gt, ":cur_lord", 0),
      (str_store_string, s17, "str_father"),
    (else_try),
      (str_store_string, s17, "str_husband"),
    (try_end),
    ],
   "Oh, {playername}, you brought him back to me! Thank you ever so much for rescuing my {s17}.\
 Please, take this as some small repayment for your noble deed.", "lady_generic_mission_succeeded",
   [
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 8),
     (add_xp_as_reward, 2000),
     (call_script, "script_troop_add_gold", "trp_player", 1500),
     (call_script, "script_end_quest", "qst_rescue_lord_by_replace"),
     ]],

  [anyone|plyr,"lady_generic_mission_succeeded", [], "Always an honour to serve, {s65}.", "lady_pretalk",[]],


  [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_lady),
                     (eq, "$g_talk_troop_met", 0),
                     (le,"$talk_context",tc_siege_commander),
                     ],
   "I say, you don't look familiar...", "lady_premeet", []],
  [anyone|plyr ,"lady_premeet", [],  "I am {playername}.", "lady_meet", []],
  [anyone|plyr ,"lady_premeet", [],  "My name is {playername}. At your service.", "lady_meet", []],

  [anyone, "lady_meet", [],  "{playername}? I do not believe I've heard of you before.", "lady_meet_end", []],

  [anyone, "lady_meet_end", [],  "Can I help you with anything?", "lady_talk", []],

  [anyone,"start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
                    (le,"$talk_context",tc_siege_commander),
                    ],
   "Yes?", "lady_talk",[]],

##### TODO: QUESTS COMMENT OUT BEGIN
##  [anyone|plyr,"lady_talk", [(check_quest_active, "qst_deliver_message_to_lover"),
##                             (quest_slot_eq, "qst_deliver_message_to_lover", slot_quest_target_troop, "$g_talk_troop"),
##                             (quest_get_slot, ":troop_no", "qst_deliver_message_to_lover", slot_quest_giver_troop),
##                             (str_store_troop_name_link, 3, ":troop_no")],
##   "I have brought you a message from {s3}", "lady_message_from_lover_success",[(call_script, "script_finish_quest", "qst_deliver_message_to_lover", 100)]],
##
##  [anyone|plyr,"lady_talk", [(check_quest_active, "qst_rescue_lady_under_siege"),
##                             (quest_slot_eq, "qst_rescue_lady_under_siege", slot_quest_object_troop, "$g_talk_troop"),
##                             (quest_slot_eq, "qst_rescue_lady_under_siege", slot_quest_current_state, 0)],
##   "TODO: I'm taking you home!", "lady_rescue_from_siege_check",[]],
##
##
##  [anyone,"lady_rescue_from_siege_check", [(neg|hero_can_join)],
##   "TODO: You don't have enough room for me!", "close_window",[]],
##
##
##  [anyone,"lady_rescue_from_siege_check", [], "TODO: Thank you so much!", "lady_pretalk",[(quest_set_slot, "qst_rescue_lady_under_siege", slot_quest_current_state, 1),
##                                                                                          (troop_set_slot, "$g_talk_troop", slot_troop_cur_center, 0),
##                                                                                          (troop_join, "$g_talk_troop")]],
##  [anyone,"lady_message_from_lover_success", [], "TODO: Thank you so much!", "lady_pretalk",[]],
##
  [anyone,"lady_pretalk", [], "Anything else?", "lady_talk",[]],

  [anyone|plyr,"lady_talk",
   [
     (store_partner_quest, ":ladys_quest"),
     (lt, ":ladys_quest", 0)
     ],
   "Is there anything I can do to win your favour?", "lady_ask_for_quest",[(call_script, "script_get_random_quest", "$g_talk_troop"),
                                                                 (assign, "$random_quest_no", reg0)]],
  [anyone,"lady_ask_for_quest", [(troop_slot_eq, "$g_talk_troop", slot_troop_does_not_give_quest, 1)],
   "I don't have anything else for you to do right now.", "lady_pretalk",[]],
  
  [anyone,"lady_ask_for_quest", [(eq, "$random_quest_no", "qst_rescue_lord_by_replace")],
   "Oh, I fear I may never see my {s17}, {s13}, again... He is a prisoner in the dungeon of {s14}.\
 We have tried to negotiate his ransom, but it has been set too high.\
 We can never hope to raise that much money without selling everything we own,\
 and God knows {s13} would rather spend his life in prison than make us destitute.\
 Instead I came up with a plan to get him out of there, but it requires someone to make a great sacrifice,\
 and so far my pleas have fallen on deaf ears...", "lady_mission_told",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),

     (try_begin),
       (troop_get_slot, ":cur_lord", "$g_talk_troop", slot_troop_spouse),
       (gt, ":cur_lord", 0),
       (str_store_string, s17, "str_husband"),
     (else_try),
       (str_store_string, s17, "str_father"),
     (try_end),
    
     (str_store_troop_name, s11, "$g_talk_troop"),
     (str_store_troop_name_link, s13, ":quest_target_troop"),
     (str_store_party_name_link, s14, ":quest_target_center"),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to rescue her {s17}, {s13}, from {s14} by switching clothes and taking his place in prison."),
    ]],

  [anyone,"lady_ask_for_quest", [(eq, "$random_quest_no", "qst_deliver_message_to_prisoner_lord")],
   "My poor {s17}, {s13}, is a prisoner in the {s14} dungeons.\
 The only way we can talk to each other is by exchanging letters whenever we can,\
 but the journey is so dangerous that we get little chance to do so.\
 Please, would you deliver one for me?", "lady_mission_told",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),

     (try_begin),
       (troop_get_slot, ":cur_lord", "$g_talk_troop", slot_troop_spouse),
       (gt, ":cur_lord", 0),
       (str_store_string, s17, "str_husband"),
     (else_try),
       (str_store_string, s17, "str_father"),
     (try_end),
    
     (str_store_troop_name, s11, "$g_talk_troop"),
     (str_store_troop_name_link, s13, ":quest_target_troop"),
     (str_store_party_name_link, s14, ":quest_target_center"),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to deliver a message to {s13}, who is imprisoned at {s14}."),
    ]],
  

  [anyone,"lady_ask_for_quest", [(eq, "$random_quest_no", "qst_duel_for_lady")],
   "Dear {playername}, you are kind to ask, but you know little of my troubles\
 and I can't possibly ask you to throw yourself into danger on my behalf.", "lady_quest_duel_for_lady",[]],
  [anyone|plyr,"lady_quest_duel_for_lady", [], "Tell me what the problem is, and I can make my own decision.", "lady_quest_duel_for_lady_2",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),

     (str_store_troop_name, s11, "$g_talk_troop"),
     (str_store_troop_name_link, s13, ":quest_target_troop"),
     (str_store_string, s2, "@You agreed to challenge {s13} to defend {s11}'s honour."),
     (setup_quest_text,"$random_quest_no"),
    ]],
  [anyone,"lady_quest_duel_for_lady_2", [], "Very well, as you wish it...\
 My husband has made certain enemies in his life, {playername}. One of the most insidious is {s13}.\
 He is going around making terrible accusations against me, impugning my honour at every turn!\
 Because he cannot harm my husband directly, he is using me as a target to try and stain our name.\
 You should hear the awful things he's said! I only wish there was someone brave enough to make him recant his slander,\
 but {s13} is a very fine swordsman, and he's widely feared...", "lady_quest_duel_for_lady_3",[]],

  [anyone|plyr,"lady_quest_duel_for_lady_3", [], "I fear him not, {s65}. I will make him take back his lies.", "lady_quest_duel_for_lady_3_accepted",[]],
  [anyone,"lady_quest_duel_for_lady_3_accepted", [], "Oh! I can't ask that of you, {playername}, but...\
 I would be forever indebted to you, and you are so sure. It would mean so much if you would defend my honour.\
 Thank you a thousand times, all my prayers and my favour go with you.", "close_window",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     (call_script, "script_report_quest_troop_positions", "$random_quest_no", ":quest_target_troop", 3),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
     ]],

  [anyone|plyr,"lady_quest_duel_for_lady_3", [], "If he's that dangerous, perhaps maybe it would be better to ignore him...", "lady_quest_duel_for_lady_3_rejected",[]],
  [anyone,"lady_quest_duel_for_lady_3_rejected", [], "Oh... Perhaps you're right, {playername}.\
 I should let go of these silly childhood ideas of chivalry and courage. {Men/People} are not like that,\
 not anymore. Good day to you.", "close_window",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    ]],


  [anyone,"lady_ask_for_quest", [], "No, {playername}, I've no need for a champion right now.", "lady_pretalk",[]],

  [anyone|plyr,"lady_mission_told", [], "As you wish it, {s65}, it shall be done.", "lady_mission_accepted",[]],
  [anyone|plyr,"lady_mission_told", [], "{s66}, I fear I cannot help you right now.", "lady_mission_rejected",[]],

  [anyone,"lady_mission_accepted", [], "You are a true {gentleman/lady}, {playername}.\
 Thank you so much for helping me", "close_window",
   [
     (try_begin),
       (eq, "$random_quest_no", "qst_deliver_message_to_prisoner_lord"),
       (call_script, "script_troop_add_gold", "trp_player", 10),
     (try_end),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],
  [anyone,"lady_mission_rejected", [], "You'll not help a woman in need? You should be ashamed, {playername}...\
 Please leave me, I have some important embroidery to catch up.", "close_window",
   [
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
     (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    ]],

#Leave
  [anyone|plyr,"lady_talk", [], "I want to improve my relation with a lord. Can you help me?", "lady_restore_relation",[]],
  [anyone,"lady_restore_relation", [(le, "$g_talk_troop_relation", 0)], "{playername}, I don't know you well enough to act on your behalf. I am sorry.", "lady_pretalk",[]],
  [anyone,"lady_restore_relation", [], "Hmm. I guess you got on the wrong side of somebody. Very well, who do you want to restore your relation with?", "lady_restore_relation_2",[]],

  [anyone|plyr|repeat_for_troops,"lady_restore_relation_2", [(store_repeat_object, ":troop_no"),
                                                             (is_between, ":troop_no", heroes_begin, heroes_end),
                                                             (store_troop_faction, ":faction_no", ":troop_no"),
                                                             (eq, "$g_talk_troop_faction", ":faction_no"),
                                                             (call_script, "script_troop_get_player_relation", ":troop_no"),
                                                             (lt, reg0, 0),
                                                             (str_store_troop_name, s1, ":troop_no")],
   "{s1}", "lady_restore_relation_2b",[(store_repeat_object, "$troop_to_restore_relations_with")]],
  [anyone|plyr,"lady_restore_relation_2", [], "Never mind. I get along with everyone well enough.", "lady_pretalk",[]],

  [anyone,"lady_restore_relation_2b", [(str_store_troop_name, s10, "$troop_to_restore_relations_with")], "Well I can try to help you there.\
 I am sure a few expensive gifts will make {s10} look at you more favorably.", "lady_restore_relation_3",[]],
  
  [anyone,"lady_restore_relation_3", [(str_store_troop_name, s10, "$troop_to_restore_relations_with"),
                                      (assign, "$lady_restore_cost_1", 1000),
                                      (assign, "$lady_restore_cost_2", 2000),
                                      (assign, "$lady_restore_cost_3", 3000),
                                      (assign, reg10, "$lady_restore_cost_1"),
                                      (assign, reg11, "$lady_restore_cost_2"),
                                      (assign, reg12, "$lady_restore_cost_3"),
                                      (troop_get_type, reg4, "$troop_to_restore_relations_with"),
                                      ],
   "You can improve your relation with {s10} by sending {reg4?her:him} a gift worth {reg10} denars.\
 But if you can afford spending {reg11} denars on the gift, it would make a good impression on {reg4?her:him}.\
 And if you can go up to {reg12} denars, that would really help smooth things out.", "lady_restore_relation_4",[]],

  [anyone|plyr,"lady_restore_relation_4", [(store_troop_gold,":gold", "trp_player"),
                                           (ge, ":gold", "$lady_restore_cost_1"),
                                           (assign, reg10, "$lady_restore_cost_1")],
   "I think a gift of {reg10} denars will do.", "lady_restore_relation_5",[(assign, "$temp", 1), (assign, "$temp_2", "$lady_restore_cost_1")]],
  [anyone|plyr,"lady_restore_relation_4", [(store_troop_gold,":gold", "trp_player"),
                                           (ge, ":gold", "$lady_restore_cost_2"),
                                           (assign, reg11, "$lady_restore_cost_2")],
   "Maybe I can afford {reg11} denars.", "lady_restore_relation_5",[(assign, "$temp", 2), (assign, "$temp_2", "$lady_restore_cost_2")]],
  [anyone|plyr,"lady_restore_relation_4", [(store_troop_gold,":gold", "trp_player"),
                                           (ge, ":gold", "$lady_restore_cost_3"),
                                           (assign, reg12, "$lady_restore_cost_3")],
   "In that case, I am ready to spend {reg12} denars.", "lady_restore_relation_5",[(assign, "$temp", 3), (assign, "$temp_2", "$lady_restore_cost_3")]],
  
  [anyone|plyr,"lady_restore_relation_4", [], "I don't think I can afford a gift at the moment.", "lady_restore_relation_cant_afford",[]],
  
  [anyone,"lady_restore_relation_5", [], "Excellent. Then I'll choose an appropriate gift for you and send it to {s10} with your compliments.\
 I am sure {reg4?she:he} will appreciate the gesture.", "lady_restore_relation_6",[
     (troop_remove_gold, "trp_player","$temp_2"),
     (call_script, "script_change_player_relation_with_troop", "$troop_to_restore_relations_with", "$temp"),
     (troop_get_type, reg4, "$troop_to_restore_relations_with"),
     ]],

  [anyone|plyr,"lady_restore_relation_6", [], "Thank you for your help, madame.", "lady_pretalk",[]],

  [anyone,"lady_restore_relation_cant_afford", [], "I am afraid, I can't be of much help in that case, {playername}. I am sorry.", "lady_pretalk",[]],
 
  [anyone|plyr,"lady_talk", [], "I must beg my leave.", "lady_leave",[]],
  
  [anyone|auto_proceed,"lady_leave", [], "Farewell, {playername}.", "close_window",[(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],



#Convincing bargaining
  [anyone,"convince_begin", [], "I still don't see why I should accept what you're asking of me.", "convince_options",
   [(quest_get_slot, "$convince_value", "$g_convince_quest", slot_quest_convince_value),
    ]],
    
  [anyone|plyr,"convince_options", [(assign, reg8, "$convince_value")], "Then I'll make it worth your while. ({reg8} denars)", "convince_bribe",[]],
  [anyone|plyr,"convince_options", 
  [(store_div, "$convince_relation_penalty", "$convince_value", 300),
   (val_add, "$convince_relation_penalty", 1),
   (assign, reg9, "$convince_relation_penalty")], 
   "Please, do it for the sake of our friendship. (-{reg9} to relation)", "convince_friendship",[]],
  [anyone|plyr,"convince_options", [], "Let me try and convince you. (Persuasion)", "convince_persuade_begin", []],
  [anyone|plyr,"convince_options", [], "Never mind.", "lord_pretalk",[]],

  [anyone,"convince_bribe", [], "Mmm, a generous gift to my coffers would certainly help matters...\
 {reg8} denars should do it. If you agree, then I'll go with your suggestion.", "convince_bribe_verify",[]],

  [anyone|plyr,"convince_bribe_verify", [(store_troop_gold, ":gold", "trp_player"),
                                         (lt, ":gold", "$convince_value")],
   "I'm afraid my finances will not allow for such a gift.", "convince_bribe_cant_afford",[]],
  [anyone|plyr,"convince_bribe_verify", [(store_troop_gold, ":gold", "trp_player"),
                                         (ge, ":gold", "$convince_value")],
  "Very well, please accept these {reg8} denars as a token of my gratitude.", "convince_bribe_goon",[]],
  [anyone|plyr,"convince_bribe_verify", [], "Let me think about this some more.", "convince_begin",[]],

  [anyone,"convince_bribe_cant_afford", [], "Ah. In that case, there is little I can do,\
 unless you have some further argument to make.", "convince_options",[]],
   [anyone,"convince_bribe_goon", [], "My dear {playername}, your generous gift has led me to reconsider what you ask,\
 and I have come to appreciate the wisdom of your proposal.", "convince_accept",[(troop_remove_gold, "trp_player","$convince_value")]],

  [anyone,"convince_friendship",
   [(store_add, ":min_relation", 5, "$convince_relation_penalty"),
    (ge, "$g_talk_troop_relation", ":min_relation")], "You've done well by me in the past, {playername},\
 and for that I will go along with your request, but know that I do not like you using our relationship this way.", "convince_friendship_verify",[]],

  [anyone|plyr,"convince_friendship_verify", [], "I am sorry, my friend, but I need your help in this.", "convince_friendship_go_on",[]],
  [anyone|plyr,"convince_friendship_verify", [], "If it will not please you, then I'll try something else.", "lord_pretalk",[]],

  [anyone,"convince_friendship_go_on", [], "All right then, {playername}, I will accept this for your sake. But remember, you owe me for this.", "convince_accept",
   [(store_sub, ":relation_change", 0, "$convince_relation_penalty"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",":relation_change")]],

  [anyone,"convince_friendship",
   [(ge, "$g_talk_troop_relation", -5)], "I don't think I owe you such a favor {playername}.\
 I see no reason to accept this for you.", "lord_pretalk",[]],

  [anyone,"convince_friendship", [], "Is this a joke? You've some nerve asking me for favours, {playername},\
 and let me assure you you'll get none.", "lord_pretalk",[]],

  [anyone,"convince_persuade_begin", 
  [(troop_get_slot, ":last_persuasion_time", "$g_talk_troop", slot_troop_last_persuasion_time),
   (store_current_hours, ":cur_hours"),
   (store_add, ":valid_time", ":last_persuasion_time", 24),
   (gt, ":cur_hours", ":valid_time"),
   ], 
   "Very well. Make your case.", "convince_persuade_begin_2",[]],
   
   
  [anyone|plyr,"convince_persuade_begin_2", [], "[Attempt to persuade]", "convince_persuade",[
        (try_begin),
          (store_random_in_range, ":rand", 0, 100),
          (lt, ":rand", 30),
          (store_current_hours, ":cur_hours"),
          (troop_set_slot, "$g_talk_troop", slot_troop_last_persuasion_time, ":cur_hours"),
        (try_end),
        (store_skill_level, ":persuasion_level", "skl_persuasion", "trp_player"),
        (store_add, ":persuasion_potential", ":persuasion_level", 5),

        (store_random_in_range, ":random_1", 0, ":persuasion_potential"),
        (store_random_in_range, ":random_2", 0, ":persuasion_potential"),
        (store_add, ":rand", ":random_1", ":random_2"),

        (assign, ":persuasion_difficulty", "$convince_value"),
        (convert_to_fixed_point, ":persuasion_difficulty"),
        (store_sqrt, ":persuasion_difficulty", ":persuasion_difficulty"),
        (convert_from_fixed_point, ":persuasion_difficulty"),
        (val_div, ":persuasion_difficulty", 10),
        (val_add, ":persuasion_difficulty", 4),

        (store_sub, "$persuasion_strength", ":rand", ":persuasion_difficulty"),
        (val_mul, "$persuasion_strength", 20),
        (assign, reg5, "$persuasion_strength"),
        (val_sub, "$convince_value", "$persuasion_strength"),
        (quest_set_slot, "$g_convince_quest", slot_quest_convince_value, "$convince_value"),
        (str_store_troop_name, s50, "$g_talk_troop"),
        (troop_get_type, reg51, "$g_talk_troop"),
        (try_begin),
          (lt, "$persuasion_strength", -30),
          (str_store_string, s5, "str_persuasion_summary_very_bad"),
        (else_try),
          (lt, "$persuasion_strength", -10),
          (str_store_string, s5, "str_persuasion_summary_bad"),
        (else_try),
          (lt, "$persuasion_strength", 10),
          (str_store_string, s5, "str_persuasion_summary_average"),
        (else_try),
          (lt, "$persuasion_strength", 30),
          (str_store_string, s5, "str_persuasion_summary_good"),
        (else_try),
          (str_store_string, s5, "str_persuasion_summary_very_good"),
        (try_end),
        (dialog_box, "@{s5} (Persuasion strength: {reg5})", "@Persuasion Attempt"),
  ]],
  [anyone|plyr,"convince_persuade_begin_2", [], "Wait, perhaps there is another way to convince you.", "convince_begin",[]],

  [anyone,"convince_persuade_begin", [], "By God's grace, {playername}!\
 Haven't we talked enough already? I am tired of listening to you,\
 and I do not want to hear any more of it right now.", "lord_pretalk",[]],
 
  [anyone,"convince_persuade", [(le, "$convince_value", 0)], "All right, all right. You have persuaded me to it.\
 I'll go ahead with what you suggest.", "convince_accept",[]],
  [anyone,"convince_persuade", [(gt, "$persuasion_strength", 5)], "You've a point, {playername},\
 I'll admit that much. However I am not yet convinced I should do as you bid.", "convince_options",[]],
  [anyone,"convince_persuade", [(gt, "$persuasion_strength", -5)], "Enough, {playername}.\
 You've a lot of arguments, but I find none of them truly convincing. I stand by what I said before.", "convince_options",[]],
  [anyone,"convince_persuade", [], "Truthfully, {playername}, I fail to see the virtue of your reasoning.\
 What you ask for makes even less sense now than it did before.", "convince_options",[]],

#Seneschal

  [anyone,"start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_seneschal),
                    (eq, "$talk_context", tc_siege_won_seneschal),
                    (str_store_party_name, s1, "$g_encountered_party"),
                    ],
   "I must congratulate you on your victory, my {lord/lady}. Welcome to {s1}.\
 We, the housekeepers of this castle, are at your service.", "siege_won_seneschal_1",[]],
  [anyone|plyr,"siege_won_seneschal_1", [], "Are you the seneschal?", "siege_won_seneschal_2",[]],
  [anyone,"siege_won_seneschal_2", [], "Indeed I am, my {lord/lady}.\
 I have always served the masters of {s1} to the best of my ability, whichever side they might be on.\
 Thus you may count on my utmost loyalty for as long as you are the {lord/lady} of this place.\
 Now, do you intend to keep me on as the seneschal? I promise you will not be disappointed.", "siege_won_seneschal_3",[]],
  [anyone|plyr,"siege_won_seneschal_3", [], "Very well, you may keep your post for the time being.", "siege_won_seneschal_4",[]],
  [anyone|plyr,"siege_won_seneschal_3", [], "You can stay, but I shall be keeping a close watch on you.", "siege_won_seneschal_4",[]],
  [anyone,"siege_won_seneschal_4", [], "Thank you, my {lord/lady}. If you do not mind my impudence,\
 may I inquire as to what you wish to do with the castle?", "siege_won_seneschal_5",[]],

  [anyone|plyr,"siege_won_seneschal_5", [], "I will sell it to another lord.", "siege_won_seneschal_6",[]],
  [anyone|plyr,"siege_won_seneschal_5", [], "I intend to claim it for myself.", "siege_won_seneschal_6",[]],
  
  [anyone|plyr,"siege_won_seneschal_5", [], "I haven't given it much thought. What are my options?", "siege_won_seneschal_list_options",[]],

  [anyone,"siege_won_seneschal_list_options", [], "According to our laws and traditions,\
 you can do one of several things.\
 First, you could station a garrison here to protect the castle from any immediate counterattacks,\
 then request an audience with some wealthy lord and ask him to make you an offer.\
 It would be worth a tidy sum, believe you me.\
 If you do not wish to sell, then you will have to find yourself a liege lord and protector who would accept homage from you.\
 Without a royal investiture and an army at your back, you would have a difficult time holding on to the castle.\
 Both you and {s1} would become great big targets for any man with a few soldiers and a scrap of ambition.\
 ", "siege_won_seneschal_list_options_2",[]],

  [anyone|plyr,"siege_won_seneschal_list_options_2", [], "What do you mean, a liege lord and protector? I won this place by my own hand, I don't need anyone else!", "siege_won_seneschal_list_options_3",[]],
  [anyone,"siege_won_seneschal_list_options_3", [], "Of course you don't, my {lord/lady}.\
 However, no lord in the land will recognize your claim to the castle unless it is verified by royal decree.\
 They would call {s1} an outlaw stronghold and take it from you at the earliest opportunity.\
 Surely not even you could stand against a whole army.", "siege_won_seneschal_list_options_4",[]],
  [anyone|plyr,"siege_won_seneschal_list_options_4", [], "Hmm. I'll give it some thought.", "siege_won_seneschal_6",[]],

  [anyone,"siege_won_seneschal_6", [], "I am very pleased to hear it, my {lord/lady}.\
 I am only trying to serve you to the best of my ability. Now,\
 if at any time you find you have further need of me,\
 I will be in the great hall arranging a smooth handover of the castle to your forces.\
 ", "close_window",[]],

  
  [anyone,"start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_seneschal),(eq,"$g_talk_troop_met",0),(str_store_party_name,s1,"$g_encountered_party")],
   "Good day, {sir/madam}. I do nott believe I've seen you here before.\
 Let me extend my welcome to you as the seneschal of {s1}.", "seneschal_intro_1",[]],

  [anyone|plyr,"seneschal_intro_1", [],  "A pleasure to meet you, {s65}.", "seneschal_intro_1a",[]],
  [anyone,"seneschal_intro_1a", [], "How can I help you?", "seneschal_talk",[]],
  [anyone|plyr,"seneschal_intro_1", [],  "What exactly do you do here?", "seneschal_intro_1b",[]],
  [anyone,"seneschal_intro_1b", [], "Ah, a seneschal's duties are many, good {sire/woman}.\
 For example, I collect the rents from my lord's estates, I manage the castle's storerooms,\
 I deal with the local peasantry, I take care of castle staff, I arrange supplies for the garrison...\
 All mundane matters on this fief are my responsibility, on behalf of my lord.\
 Everything except commanding the soldiers themselves.", "seneschal_talk",[]],
  
  [anyone,"start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_seneschal)],
   "Good day, {sir/madam}.", "seneschal_talk",[]],

  [anyone,"seneschal_pretalk", [], "Anything else?", "seneschal_talk",[]],


##### TODO: QUESTS COMMENT OUT BEGIN
##  [anyone|plyr,"seneschal_talk", [(check_quest_active, "qst_deliver_supply_to_center_under_siege"),
##                                  (quest_slot_eq, "qst_deliver_supply_to_center_under_siege", slot_quest_target_troop, "$g_talk_troop"),
##                                  (quest_slot_eq, "qst_deliver_supply_to_center_under_siege", slot_quest_current_state, 1),
##                                  (store_item_kind_count, ":no_supplies", "itm_siege_supply"),
##                                  (quest_get_slot, ":target_amount", "qst_deliver_supply_to_center_under_siege", slot_quest_target_amount),
##                                  (ge, ":no_supplies", ":target_amount")],
##   "TODO: Here are the supplies.", "seneschal_supplies_given",[]],
##
##  [anyone|plyr,"seneschal_talk", [(check_quest_active, "qst_deliver_supply_to_center_under_siege"),
##                                  (quest_slot_eq, "qst_deliver_supply_to_center_under_siege", slot_quest_target_troop, "$g_talk_troop"),
##                                  (quest_slot_eq, "qst_deliver_supply_to_center_under_siege", slot_quest_current_state, 1),
##                                  (store_item_kind_count, ":no_supplies", "itm_siege_supply"),
##                                  (quest_get_slot, ":target_amount", "qst_deliver_supply_to_center_under_siege", slot_quest_target_amount),
##                                  (lt, ":no_supplies", ":target_amount"),
##                                  (gt, ":no_supplies", 0)],
##   "TODO: Here are the supplies, but some of them are missing.", "seneschal_supplies_given_missing",[]],
##  
##  [anyone|plyr,"seneschal_talk", [(check_quest_active, "qst_deliver_supply_to_center_under_siege"),
##                                  (quest_slot_eq, "qst_deliver_supply_to_center_under_siege", slot_quest_object_troop, "$g_talk_troop"),
##                                  (quest_slot_eq, "qst_deliver_supply_to_center_under_siege", slot_quest_current_state, 0)],
##   "TODO: Give me the supplies.", "seneschal_supplies",[]],
##  
##  [anyone,"seneschal_supplies", [(store_free_inventory_capacity, ":free_inventory"),
##                                 (quest_get_slot, ":quest_target_amount", "qst_deliver_supply_to_center_under_siege", slot_quest_target_amount),
##                                 (ge, ":free_inventory", ":quest_target_amount"),
##                                 (quest_get_slot, ":quest_target_center", "qst_deliver_supply_to_center_under_siege", slot_quest_target_center),
##                                 (str_store_party_name, 0, ":quest_target_center"),
##                                 (troop_add_items, "trp_player", "itm_siege_supply", ":quest_target_amount")],
##   "TODO: Here, take these supplies. You must deliver them to {s0} as soon as possible.", "seneschal_pretalk",[(quest_set_slot, "qst_deliver_supply_to_center_under_siege", slot_quest_current_state, 1)]],
##
##  [anyone,"seneschal_supplies", [],
##   "TODO: You don't have enough space to take the supplies. Free your inventory and return back to me.", "seneschal_pretalk",[]],
##
##
##  [anyone,"seneschal_supplies_given", [],
##   "TODO: Thank you.", "seneschal_pretalk",[(party_get_slot, ":town_siege_days", "$g_encountered_party", slot_town_siege_days),
##                                            (quest_get_slot, ":target_amount", "qst_deliver_supply_to_center_under_siege", slot_quest_target_amount),
##                                            (val_sub, ":town_siege_days", ":target_amount"),
##                                            (try_begin),
##                                              (lt, ":town_siege_days", 0),
##                                              (assign, ":town_siege_days", 0),
##                                            (try_end),
##                                            (party_set_slot, "$g_encountered_party", slot_town_siege_days, ":town_siege_days"),
##                                            (troop_remove_items, "trp_player", "itm_siege_supply", ":target_amount"),
##                                            (call_script, "script_finish_quest", "qst_deliver_supply_to_center_under_siege", 100)]],
##
##  [anyone,"seneschal_supplies_given_missing", [],
##   "TODO: Thank you but it's not enough...", "seneschal_pretalk",[(store_item_kind_count, ":no_supplies", "itm_siege_supply"),
##                                                                  (quest_get_slot, ":target_amount", "qst_deliver_supply_to_center_under_siege", slot_quest_target_amount),
##                                                                  (assign, ":percentage_completed", 100),
##                                                                  (val_mul, ":percentage_completed", ":no_supplies"),
##                                                                  (val_div, ":percentage_completed", ":target_amount"),
##                                                                  (call_script, "script_finish_quest", "qst_deliver_supply_to_center_under_siege", ":percentage_completed"),
##                                                                  (party_get_slot, ":town_siege_days", "$g_encountered_party", slot_town_siege_days),
##                                                                  (val_sub, ":town_siege_days", ":no_supplies"),
##                                                                  (try_begin),
##                                                                    (lt, ":town_siege_days", 0),
##                                                                    (assign, ":town_siege_days", 0),
##                                                                  (try_end),
##                                                                  (party_set_slot, "$g_encountered_party", slot_town_siege_days, ":town_siege_days"),
##                                                                  (troop_remove_items, "trp_player", "itm_siege_supply", ":no_supplies"),
##                                                                  (call_script, "script_end_quest", "qst_deliver_supply_to_center_under_siege")]],
##
##### TODO: QUESTS COMMENT OUT END

  [anyone|plyr,"seneschal_talk", [(store_relation, ":cur_rel", "fac_player_supporters_faction", "$g_encountered_party_faction"),
                                  (ge, ":cur_rel", 0),],
   "I would like to ask you a question...", "seneschal_ask_something",[]],

  [anyone|plyr,"seneschal_talk", [(store_relation, ":cur_rel", "fac_player_supporters_faction", "$g_encountered_party_faction"),
                                  (ge, ":cur_rel", 0),],
   "I wish to know more about someone...", "seneschal_ask_about_someone",[]],

  [anyone,"seneschal_ask_about_someone", [],
   "Perhaps I may be able to help. Whom did you have in mind?", "seneschal_ask_about_someone_2",[]],

  [anyone|plyr|repeat_for_troops,"seneschal_ask_about_someone_2", [(store_repeat_object, ":troop_no"),
                                                                  (is_between, ":troop_no", heroes_begin, heroes_end),
                                                                  (store_troop_faction, ":faction_no", ":troop_no"),
                                                                  (eq, "$g_encountered_party_faction", ":faction_no"),
                                                                  (str_store_troop_name, s1, ":troop_no")],
   "{s1}", "seneschal_ask_about_someone_3",[(store_repeat_object, "$hero_requested_to_learn_relations")]],

  [anyone|plyr,"seneschal_ask_about_someone_2", [], "Never mind.", "seneschal_pretalk",[]],

  [anyone, "seneschal_ask_about_someone_3", [(call_script, "script_troop_write_family_relations_to_s1", "$hero_requested_to_learn_relations"),
                                           (call_script, "script_troop_write_owned_centers_to_s2", "$hero_requested_to_learn_relations")],
   "{s2}{s1}", "seneschal_ask_about_someone_4",[(add_troop_note_from_dialog, "$hero_requested_to_learn_relations", 2)]],
  
  [anyone, "seneschal_ask_about_someone_relation", [(call_script, "script_troop_count_number_of_enemy_troops", "$hero_requested_to_learn_relations"),
                                            (assign, ":no_enemies", reg0),
                                            (try_begin),
                                              (gt, ":no_enemies", 1),
                                              (try_for_range, ":i_enemy", 1, ":no_enemies"),
                                                (store_add, ":slot_no", slot_troop_enemies_begin, ":i_enemy"),
                                                (troop_get_slot, ":cur_enemy", "$hero_requested_to_learn_relations", ":slot_no"),
                                                (str_store_troop_name_link, s50, ":cur_enemy"),
                                                (try_begin),
                                                  (eq, ":i_enemy", 1),
                                                  (troop_get_slot, ":cur_enemy", "$hero_requested_to_learn_relations", slot_troop_enemy_1),
                                                  (str_store_troop_name_link, s51, ":cur_enemy"),
                                                  (str_store_string, s51, "str_s50_and_s51"),
                                                (else_try),
                                                  (str_store_string, s51, "str_s50_comma_s51"),
                                                (try_end),
                                              (try_end),
                                            (else_try),
                                              (eq, ":no_enemies", 1),
                                              (troop_get_slot, ":cur_enemy", "$hero_requested_to_learn_relations", slot_troop_enemy_1),
                                              (str_store_troop_name_link, s51, ":cur_enemy"),
                                            (else_try),
                                              (str_store_string, s51, "str_noone"),
                                            (try_end),
                                            (troop_get_type, reg1, "$hero_requested_to_learn_relations")],
   "{reg1?She:He} hates {s51}.", "seneschal_ask_about_someone_4",[(add_troop_note_from_dialog, "$hero_requested_to_learn_relations", 3)]],
# Ryan END

  [anyone|plyr,"seneschal_ask_about_someone_4", [], "Where does {s1} stand with others?.", "seneschal_ask_about_someone_relation",[]],
  [anyone|plyr,"seneschal_ask_about_someone_4", [], "My thanks, that was helpful.", "seneschal_pretalk",[]],

 
  [anyone|plyr,"seneschal_talk", [], "I must take my leave of you now. Farewell.", "close_window",[]],


  [anyone,"seneschal_ask_something", [],
   "I'll do what I can to help, of course. What did you wish to ask?", "seneschal_ask_something_2",[]],

  [anyone|plyr,"seneschal_ask_something_2", [],
   "Perhaps you know where to find someone...", "seneschal_ask_location",[]],

  [anyone,"seneschal_ask_location", [],
   "Well, a man in my position does hear a lot of things. Of whom were you thinking?", "seneschal_ask_location_2",[]],

  [anyone|plyr|repeat_for_troops,"seneschal_ask_location_2", [(store_repeat_object, ":troop_no"),
                                                              (is_between, ":troop_no", heroes_begin, heroes_end),
                                                              (store_troop_faction, ":faction_no", ":troop_no"),
                                                              (eq, "$g_encountered_party_faction", ":faction_no"),
                                                              (str_store_troop_name, s1, ":troop_no")],
   "{s1}", "seneschal_ask_location_3",[(store_repeat_object, "$hero_requested_to_learn_location")]],

  [anyone|plyr,"seneschal_ask_location_2", [], "Never mind.", "seneschal_pretalk",[]],

  [anyone,"seneschal_ask_location_3", [(call_script, "script_get_information_about_troops_position", "$hero_requested_to_learn_location", 0)],
   "{s1}", "seneschal_pretalk",[]],

#caravan merchants
  [anyone,"start",
   [(eq,"$caravan_escort_state",1),
    (eq,"$g_encountered_party","$caravan_escort_party_id"),
    (le,"$talk_context",tc_party_encounter),
    (store_distance_to_party_from_party, reg(0),"$caravan_escort_destination_town","$caravan_escort_party_id"),
    (lt,reg(0),5),
    (str_store_party_name,s3,"$caravan_escort_destination_town"),
    (assign,reg(3), "$caravan_escort_agreed_reward"),
    ],
   "There! I can see the walls of {s3} in the distance. We've made it safely.\
 Here, take this purse of {reg3} denars, as I promised. I hope we can travel together again someday.", "close_window",
   [
    (assign,"$caravan_escort_state",0),
    (call_script, "script_troop_add_gold", "trp_player","$caravan_escort_agreed_reward"),
    (assign,reg(4), "$caravan_escort_agreed_reward"),
    (val_mul,reg(4), 1),
    (add_xp_as_reward,reg(4)),
    (assign, "$g_leave_encounter",1),
    ]],
  
  [anyone,"start",
   [(eq,"$caravan_escort_state",1),
    (eq,"$g_encountered_party","$caravan_escort_party_id"),
    (eq, "$talk_context", tc_party_encounter),
    ],
   "We've made it this far... Is everything clear up ahead?", "talk_caravan_escort",[]],
  [anyone|plyr,"talk_caravan_escort", [],
   "There might be bandits nearby. Stay close.", "talk_caravan_escort_2a",[]],
  [anyone,"talk_caravan_escort_2a", [],
   "Trust me, {playername}, we're already staying as close to you as we can. Lead the way.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone|plyr,"talk_caravan_escort", [],
   "No sign of trouble, we can breathe easy.", "talk_caravan_escort_2b",[]],
  [anyone,"talk_caravan_escort_2b", [],
   "I'll breathe easy when we reach {s1} and not a moment sooner. Let's keep moving.", "close_window",[[str_store_party_name,s1,"$caravan_escort_destination_town"],(assign, "$g_leave_encounter",1)]],

  [anyone,"start", [(eq,"$talk_context", tc_party_encounter),
                    (eq, "$g_encountered_party_type", spt_kingdom_caravan),
                    (party_slot_ge, "$g_encountered_party", slot_party_last_toll_paid_hours, "$g_current_hours"),
                    ],
   "What do you want? We paid our toll to you less than three days ago.", "merchant_talk",[]],

  [anyone,"start", [(eq,"$talk_context", tc_party_encounter),(eq, "$g_encountered_party_type", spt_kingdom_caravan),(ge,"$g_encountered_party_relation",0)],
   "Hail, friend.", "merchant_talk",[]],

  [anyone,"start", [(eq,"$talk_context", tc_party_encounter),
                    (eq, "$g_encountered_party_type", spt_kingdom_caravan),
                    (lt,"$g_encountered_party_relation",0),
                    (eq, "$g_encountered_party_faction", "fac_merchants"),
                    ],
   "What do you want? We are but simple merchants, we've no quarrel with you, so leave us alone.", "merchant_talk",[]],

  [anyone,"start", [(eq,"$talk_context", tc_party_encounter),
                    (eq, "$g_encountered_party_type", spt_kingdom_caravan),
                    (lt,"$g_encountered_party_relation",0),
                    (faction_get_slot, ":faction_leader", "$g_encountered_party_faction",slot_faction_leader),
                    (str_store_troop_name, s9, ":faction_leader"),
                    ],
   "Be warned, knave! This caravan is under the protection of {s9}.\
 Step out of our way or you will face his fury!", "merchant_talk",[]],


  [anyone,"start", [(party_slot_eq, "$g_encountered_party", slot_party_type, spt_kingdom_caravan),(this_or_next|eq,"$talk_context", tc_party_encounter),(eq,"$talk_context", 0)],
   "Yes? What do you want?", "merchant_talk",[]],
  [anyone,"merchant_pretalk", [], "Anything else?", "merchant_talk",[]],

  [anyone|plyr,"merchant_talk", [(le,"$talk_context", tc_party_encounter),
                                 (check_quest_active, "qst_raid_caravan_to_start_war"),
                                 (neg|check_quest_concluded, "qst_raid_caravan_to_start_war"),
                                 (quest_slot_eq, "qst_raid_caravan_to_start_war", slot_quest_target_faction, "$g_encountered_party_faction"),
                                 (str_store_faction_name, s17, "$players_kingdom"),
                                 ],
   "You are trespassing in {s17} territory. I am confiscating this caravan and all its goods!", "caravan_start_war_quest_1",[]],
  [anyone,"caravan_start_war_quest_1", [(str_store_faction_name, s17, "$players_kingdom"),],
   "What? What nonsense is this? We are nowhere near your territory, {mate/wench},\
 and moreover we have a peace treaty with {s17}!", "caravan_start_war_quest_2",[]],
  [anyone|plyr,"caravan_start_war_quest_2", [], "We'll see about that! Defend yourselves!", "merchant_attack",[]],
  [anyone|plyr,"caravan_start_war_quest_2", [], "Never mind, 'twas but a joke. Farewell.", "close_window",[(assign, "$g_leave_encounter",1)]],


  [anyone|plyr,"merchant_talk", [(le,"$talk_context", tc_party_encounter),(eq, "$g_encountered_party_faction", "$players_kingdom")], "I have an offer for you.", "merchant_talk_offer",[]],
  [anyone,"merchant_talk_offer", [], "What is it?", "merchant_talk_offer_2",[]],
  
  [anyone|plyr,"merchant_talk_offer_2", [(eq,"$talk_context", tc_party_encounter),(eq, "$g_encountered_party_faction", "$players_kingdom")],
   "I can escort you to your destination for a price.", "caravan_offer_protection",[]],
  
##  [anyone|plyr,"merchant_talk_offer_2", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                                 (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"), #he is not a faction leader!
##                                 (call_script, "script_get_number_of_hero_centers", "$g_talk_troop"),
##                                 (eq, reg0, 0), #he has no castles or towns
##                                 (hero_can_join),
##                             ],
##   "I need capable men like you. Will you join me?", "knight_offer_join",[
##       ]],
  
  [anyone|plyr,"merchant_talk_offer_2", [], "Nothing. Forget it", "merchant_pretalk",[]],

  
  [anyone|plyr,"merchant_talk", [(eq,"$talk_context", tc_party_encounter), #TODO: For the moment don't let attacking if merchant has paid toll.
                                 (neg|party_slot_ge, "$g_encountered_party", slot_party_last_toll_paid_hours, "$g_current_hours"),
                                 ], "I demand something from you!", "merchant_demand",[]],
  [anyone,"merchant_demand", [(eq,"$talk_context", tc_party_encounter)], "What do you want?", "merchant_demand_2",[]],

  [anyone|plyr,"merchant_demand_2", [(neq,"$g_encountered_party_faction","$players_kingdom")], "There is a toll for free passage here!", "merchant_demand_toll",[]],
  
  [anyone,"merchant_demand_toll", [(gt, "$g_strength_ratio", 70),
                                        (store_div, reg6, "$g_ally_strength", 2),
                                        (val_add, reg6, 40),
                                        (assign, "$temp", reg6),
                                        ], "Please, I don't want any trouble. I can give you {reg6} denars, just let us go.", "merchant_demand_toll_2",[]],
  [anyone,"merchant_demand_toll", [(store_div, reg6, "$g_ally_strength", 4),
                                        (val_add, reg6, 10),
                                        (assign, "$temp", reg6),
                                        ], "I don't want any trouble. I can give you {reg6} denars if you'll let us go.", "merchant_demand_toll_2",[]],
  
  [anyone|plyr,"merchant_demand_toll_2", [], "Agreed, hand it over and you may go in peace.", "merchant_demand_toll_accept",[]],
  [anyone,"merchant_demand_toll_accept", [(assign, reg6, "$temp")], "Very well then. Here's {reg6} denars. ", "close_window",
   [(assign, "$g_leave_encounter",1),
    (call_script, "script_troop_add_gold", "trp_player","$temp"),
    (store_add, ":toll_finish_time", "$g_current_hours", merchant_toll_duration),
    (party_set_slot, "$g_encountered_party", slot_party_last_toll_paid_hours, ":toll_finish_time"),
    (try_begin),
      (ge, "$g_encountered_party_relation", -5),
      (store_relation,":rel", "$g_encountered_party_faction","fac_player_supporters_faction"),
      (try_begin),
        (gt, ":rel", 0),
        (val_sub, ":rel", 1),
      (try_end),
      (val_sub, ":rel", 1),
      (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":rel"),
    (try_end),
### Troop commentaries changes begin
    (call_script, "script_add_log_entry", logent_caravan_accosted, "trp_player",  -1, -1, "$g_encountered_party_faction"),
### Troop commentaries changes end
    (assign, reg6, "$temp"),
    ]],
  
  [anyone|plyr,"merchant_demand_toll_2", [], "I changed my mind, I can't take your money.", "merchant_pretalk",[]],
  
  [anyone|plyr,"merchant_demand_toll_2", [], "No, I want everything you have! [Attack]", "merchant_attack",[]],
  
  [anyone|plyr,"merchant_demand_2", [(neq,"$g_encountered_party_faction","$players_kingdom")], "Hand over your gold and valuables now!", "merchant_attack_begin",[]],
  [anyone|plyr,"merchant_demand_2", [], "Nothing. Forget it.", "merchant_pretalk",[]],
  
  
  [anyone,"merchant_attack_begin", [], "Are you robbing us?", "merchant_attack_verify",[]],
  [anyone|plyr,"merchant_attack_verify", [], "Robbing you? No, no! It was a joke.", "merchant_attack_verify_norob",[]],
  [anyone,"merchant_attack_verify_norob", [], "God, don't joke about that, {lad/lass}. For a moment I thought we were in real trouble.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone|plyr,"merchant_attack_verify", [], "Of course I'm robbing you. Now hand over your goods.", "merchant_attack",[]],
  
  [anyone,"merchant_attack", [], "Damn you, you won't get anything from us without a fight!", "close_window",
   [(store_relation,":rel", "$g_encountered_party_faction","fac_player_supporters_faction"),
    (try_begin),
      (gt, ":rel", 0),
      (val_sub, ":rel", 10),
    (try_end),
    (val_sub, ":rel", 5),
    (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":rel"),
### Troop commentaries changes begin
    (call_script, "script_add_log_entry", logent_caravan_accosted, "trp_player",  -1, -1, "$g_encountered_party_faction"),
### Troop commentaries changes end
    ]],

  [anyone,"caravan_offer_protection", [],
   "These roads are dangerous indeed. One can never have enough protection.", "caravan_offer_protection_2",
   [(get_party_ai_object,":caravan_destination","$g_encountered_party"),
    (store_distance_to_party_from_party, "$caravan_distance_to_target",":caravan_destination","$g_encountered_party"),
    (assign,"$caravan_escort_offer","$caravan_distance_to_target"),
    (val_sub, "$caravan_escort_offer", 10),
    (call_script, "script_party_calculate_strength", "p_main_party",0),
    (assign, ":player_strength", reg0),
    (val_min, ":player_strength", 200),
    (val_add, ":player_strength", 20),
    (val_mul,"$caravan_escort_offer",":player_strength"),
    (val_div,"$caravan_escort_offer",50),
    (val_max, "$caravan_escort_offer", 5),
    ]],
  [anyone,"caravan_offer_protection_2", [[lt,"$caravan_distance_to_target",10]],
   "An escort? We're almost there already! Thank you for the offer, though.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone,"caravan_offer_protection_2", [(get_party_ai_object,":caravan_destination","$g_encountered_party"),
    (str_store_party_name,1,":caravan_destination"),
    (assign,reg(2),"$caravan_escort_offer")],
   "We are heading to {s1}. I will pay you {reg2} denars if you escort us there.", "caravan_offer_protection_3",
   []],
  [anyone|plyr,"caravan_offer_protection_3", [],
   "Agreed.", "caravan_offer_protection_4",[]],
  [anyone,"caravan_offer_protection_4", [],
   "I want you to stay close to us along the way.\
 We'll need your help if we get ambushed by bandits.", "caravan_offer_protection_5",[]],
  [anyone|plyr,"caravan_offer_protection_5", [],
   "Don't worry, you can trust me.", "caravan_offer_protection_6",[]],
  [anyone,"caravan_offer_protection_6", [(get_party_ai_object,":caravan_destination","$g_encountered_party"),
    (str_store_party_name,1,":caravan_destination")],
   "Good. Come and collect your money when we're within sight of {s1}. For now, let's just get underway.", "close_window",
   [(get_party_ai_object,":caravan_destination","$g_encountered_party"),
    (assign, "$caravan_escort_destination_town", ":caravan_destination"),
    (assign, "$caravan_escort_party_id", "$g_encountered_party"),
    (assign, "$caravan_escort_agreed_reward", "$caravan_escort_offer"),
    (assign, "$caravan_escort_state", 1),
    (assign, "$g_leave_encounter",1)
   ]],
  [anyone|plyr,"caravan_offer_protection_3", [],
   "Forget it.", "caravan_offer_protection_4b",[]],
  [anyone,"caravan_offer_protection_4b", [],
   "Perhaps another time, then.", "close_window",[(assign, "$g_leave_encounter",1)]],

  [anyone|plyr,"merchant_talk", [(eq,"$talk_context", tc_party_encounter),(lt, "$g_talk_troop_faction_relation", 0)],
   "Not so fast. First, hand over all your goods and money.", "talk_caravan_enemy_2",[]],

  [anyone,"talk_caravan_enemy_2", [],
   "Never. It is our duty to protect these goods. You shall have to fight us, brigand!", "close_window",
   [
    (store_relation,":rel","$g_encountered_party_faction","fac_player_supporters_faction"),
    (val_min,":rel",0),
    (val_sub,":rel",4),
    (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":rel"),
    (call_script, "script_add_log_entry", logent_caravan_accosted, "trp_player",  -1, -1, "$g_encountered_party_faction"),
    ]],

  [anyone|plyr,"merchant_talk", [], "[Leave]", "close_window",[(assign, "$g_leave_encounter",1)]],




# Prison Guards
  [anyone,"start", [(eq, "$talk_context", 0),#(faction_slot_eq, "$g_encountered_party_faction", slot_faction_prison_guard_troop, "$g_talk_troop"),
                                             # TLD center specific guards
                    (party_slot_eq, "$g_encountered_party", slot_town_prison_guard_troop, "$g_talk_troop"),
					(this_or_next|eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
                    (             party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player")
                    ],
   "Good day, my {lord/lady}. Will you be visiting the prison?", "prison_guard_players",[]],
  [anyone|plyr,"prison_guard_players", [],
   "Yes. Unlock the door.", "close_window",[(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],
  [anyone|plyr,"prison_guard_players", [],
   "No, not now.", "close_window",[]],

  [anyone,"start", [(eq, "$talk_context", 0),#(faction_slot_eq, "$g_encountered_party_faction", slot_faction_prison_guard_troop, "$g_talk_troop")],
                                             # TLD center specific guards
                                             (party_slot_eq, "$g_encountered_party", slot_town_prison_guard_troop, "$g_talk_troop")],
   "Yes? What do you want?", "prison_guard_talk",[]],

  [anyone|plyr,"prison_guard_talk", [],
   "Who is imprisoned here?", "prison_guard_ask_prisoners",[]],
  [anyone|plyr,"prison_guard_talk", [],
   "I want to speak with a prisoner.", "prison_guard_visit_prison",[]],

  [anyone,"prison_guard_ask_prisoners", [],
   "Currently, {s51} {reg1?are:is} imprisoned here.","prison_guard_talk",[(party_clear, "p_temp_party"),
                                                                              (assign, ":num_heroes", 0),
                                                                              (party_get_num_prisoner_stacks, ":num_stacks","$g_encountered_party"),
                                                                              (try_for_range, ":i_stack", 0, ":num_stacks"),
                                                                                (party_prisoner_stack_get_troop_id, ":stack_troop","$g_encountered_party",":i_stack"),
                                                                                (troop_is_hero, ":stack_troop"),
                                                                                (party_add_members, "p_temp_party", ":stack_troop", 1),
                                                                                (val_add, ":num_heroes", 1),
                                                                              (try_end),
                                                                              (call_script, "script_print_party_members", "p_temp_party"),
                                                                              (try_begin),
                                                                                (gt, ":num_heroes", 1),
                                                                                (assign, reg1, 1),
                                                                              (else_try),
                                                                                (assign, reg1, 0),
                                                                              (try_end)]],
  
  [anyone,"prison_guard_visit_prison", [(this_or_next|faction_slot_eq, "$g_encountered_party_faction",slot_faction_marshall,"trp_player"),
                                        (this_or_next|party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
                                        (eq, "$g_encountered_party_faction", "$players_kingdom"),
                                        ],
   "Of course, {sir/madam}. Go in.", "close_window",[(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],

  [anyone,"prison_guard_visit_prison", [],
   "You need to get permission from the lord to talk to prisoners.", "prison_guard_visit_prison_2",[]],

  [anyone|plyr,"prison_guard_visit_prison_2", [], "All right then. I'll try that.", "close_window",[]],
  [anyone|plyr,"prison_guard_visit_prison_2", [], "Come on now. I thought you were the boss here.", "prison_guard_visit_prison_3",[]],
  [anyone,"prison_guard_visit_prison_3", [], "He-heh. You got that right. Still, I can't let you into the prison.", "prison_guard_visit_prison_4",[]],
  
  [anyone|plyr,"prison_guard_visit_prison_4", [], "All right then. I'll leave now.", "close_window",[]],
  [anyone|plyr,"prison_guard_visit_prison_4", [(store_troop_gold,":gold","trp_player"),(ge,":gold",100)],
   "I found a purse with 100 denars a few paces away. I reckon it belongs to you.", "prison_guard_visit_prison_5",[]],

  [anyone,"prison_guard_visit_prison_5", [], "Ah! I was looking for this all day. How good of you to bring it back {sir/madam}.\
 Well, now that I know what an honest {man/lady} you are, there can be no harm in letting you inside. Go in.", "close_window",[(troop_remove_gold, "trp_player",100),(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],

  [anyone|plyr,"prison_guard_talk", [],
   "Never mind.", "close_window",[]],




# Castle Guards
  [anyone,"start", [(eq, "$talk_context", 0),#(faction_slot_eq, "$g_encountered_party_faction", slot_faction_castle_guard_troop, "$g_talk_troop"),
                                             # TLD center specific guards
                                             (party_slot_eq, "$g_encountered_party", slot_town_castle_guard_troop, "$g_talk_troop"),
                    (this_or_next|eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
                    (             party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player")
                    ],
   "Your orders, {Lord/Lady}?", "castle_guard_players",[]],
  [anyone|plyr,"castle_guard_players", [],
   "Open the door. I'll go in.", "close_window",[(call_script, "script_enter_court", "$current_town")]],
  [anyone|plyr,"castle_guard_players", [],
   "Never mind.", "close_window",[]],


  [anyone,"start", [(eq, "$talk_context", 0),#(faction_slot_eq, "$g_encountered_party_faction", slot_faction_castle_guard_troop, "$g_talk_troop"),
                                             # TLD center specific guards
                                             (eq, "$sneaked_into_town",1),
                                             (party_slot_eq, "$g_encountered_party", slot_town_castle_guard_troop, "$g_talk_troop"),
                    (gt,"$g_time_since_last_talk",0)],
   "Get out of my sight, beggar! You stink!", "castle_guard_sneaked_intro_1",[]],
  [anyone,"start", [(eq, "$talk_context", 0),#(faction_slot_eq, "$g_encountered_party_faction", slot_faction_castle_guard_troop, "$g_talk_troop"),
                                             # TLD center specific guards
                                             (party_slot_eq, "$g_encountered_party", slot_town_castle_guard_troop, "$g_talk_troop"),
                                             (eq, "$sneaked_into_town",1)],
   "Get lost before I lose my temper you vile beggar!", "close_window",[]],
  [anyone|plyr,"castle_guard_sneaked_intro_1", [], "I want to enter the hall and speak to the lord.", "castle_guard_sneaked_intro_2",[]],
  [anyone|plyr,"castle_guard_sneaked_intro_1", [], "[Leave]", "close_window",[]],
  [anyone,"castle_guard_sneaked_intro_2", [], "Are you out of your mind, {man/woman}?\
 Beggars are not allowed into the hall. Now get lost or I'll beat you bloody.", "close_window",[]],
  
  
  [anyone,"start", [(eq, "$talk_context", 0),#(faction_slot_eq, "$g_encountered_party_faction", slot_faction_castle_guard_troop, "$g_talk_troop")
                                             # TLD center specific guards
                                             (party_slot_eq, "$g_encountered_party", slot_town_castle_guard_troop, "$g_talk_troop")],
   "What do you want?", "castle_guard_intro_1",[]],
  [anyone|plyr,"castle_guard_intro_1", [],
   "I want to enter the hall and speak to the lord.", "castle_guard_intro_2",[]],
  [anyone|plyr,"castle_guard_intro_1", [],
   "Never mind.", "close_window",[]],
  [anyone,"castle_guard_intro_2", [], "You can go in after leaving your weapons with me. No one is allowed to carry arms into the lord's hall.", "castle_guard_intro_2",
   []],
  [anyone|plyr,"castle_guard_intro_2", [], "Here, take my arms. I'll go in.", "close_window", [(call_script, "script_enter_court", "$current_town")]],
  [anyone|plyr,"castle_guard_intro_2", [], "No, I give my arms to no one.", "castle_guard_intro_2b", []],
  [anyone,"castle_guard_intro_2b", [], "Then you can't go in.", "close_window", []],
  
##  [anyone|plyr,"castle_guard_intro_1", [],
##   "Never mind.", "close_window",[]],
##  [anyone,"castle_guard_intro_2", [],
##   "Does the lord expect you?", "castle_guard_intro_3",[]],
##  [anyone|plyr,"castle_guard_intro_3", [], "Yes.", "castle_guard_intro_check",[]],
##  [anyone|plyr,"castle_guard_intro_3", [], "No.", "castle_guard_intro_no",[]],
##  [anyone,"castle_guard_intro_check", [], "Hmm. All right {sir/madam}.\
## You can go in. But you must leave your weapons with me. Noone's allowed into the court with weapons.", "close_window",[]],
##  [anyone,"castle_guard_intro_check", [], "You liar!\
## Our lord would have no business with a filthy vagabond like you. Get lost now before I kick your butt.", "close_window",[]],
##  [anyone,"castle_guard_intro_no", [], "Well... What business do you have here then?", "castle_guard_intro_4",[]],
##  [anyone|plyr,"castle_guard_intro_4", [], "I wish to present the lord some gifts.", "castle_guard_intro_gifts",[]],
##  [anyone|plyr,"castle_guard_intro_4", [], "I have an important matter to discuss with the lord. Make way now.", "castle_guard_intro_check",[]],
##  [anyone,"castle_guard_intro_gifts", [], "Really? What gifts?", "castle_guard_intro_5",[]],
##  [anyone|plyr,"castle_guard_intro_4", [], "Many gifts. For example, I have a gift of 20 denars here for his loyal servants.", "castle_guard_intro_gifts",[]],
##  [anyone|plyr,"castle_guard_intro_4", [], "My gifts are of no concern to you. They are for your lords and ladies..", "castle_guard_intro_check",[]],
##  [anyone,"castle_guard_intro_gifts", [], "Oh! you can give those 20 denars to me. I can distribute them for you.\
## You can enter the court and present your gifts to the lord. I'm sure he'll be pleased.\
## But you must leave your weapons with me. Noone's allowed into the court with weapons.", "close_window",[]],

#Kingdom Parties
#  [anyone,"start", [(this_or_next|eq,"$g_encountered_party_template","pt_swadian_foragers"),
#                    (eq,"$g_encountered_party_template","pt_vaegir_foragers"),
##  [anyone,"start", [(this_or_next|party_slot_eq,"$g_encountered_party",slot_party_type, spt_forager),
##                    (this_or_next|party_slot_eq,"$g_encountered_party",slot_party_type, spt_scout),
##                    (party_slot_eq,"$g_encountered_party",slot_party_type, spt_patrol),
##                    (str_store_faction_name,5,"$g_encountered_party_faction")],
##   "In the name of the {s5}.", "kingdom_party_encounter",[]],
##  
##  [anyone,"kingdom_party_encounter", [(le,"$g_encountered_party_relation",-10)],
##   "Surrender now, and save yourself the indignity of defeat!", "kingdom_party_encounter_war",[]],
##  [anyone|plyr,"kingdom_party_encounter_war", [],  "[Go to Battle]", "close_window",[(encounter_attack)]],
##
##  [anyone,"kingdom_party_encounter", [(ge,"$g_encountered_party_relation",10)],
##   "Greetings, fellow warrior.", "close_window",[(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],
##
##  [anyone,"kingdom_party_encounter", [],
##   "You can go.", "close_window",[]],








#Player Parties
##  [party_tpl|pt_old_garrison,"start", [],
##   "They told us to leave the castle to the new garrison {sir/madam}. So we left and came to rejoin you.", "player_old_garrison_encounter",[]],
##  
##  [anyone|plyr,"player_old_garrison_encounter", [(party_can_join)],
##   "You have done well. You'll join my command now.", "close_window",[(assign, "$g_move_heroes", 1),
##                                        (call_script, "script_party_add_party", "p_main_party", "$g_encountered_party"),
##                                        (remove_party, "$g_encountered_party"),
##                                        (assign, "$g_leave_encounter", 1)]],
##  [anyone|plyr,"player_old_garrison_encounter", [(assign, reg1, 0),
##                                                 (try_begin),
##                                                   (neg|party_can_join),
##                                                   (assign, reg1, 1),
##                                                 (try_end)],
##   "You can't join us now{reg1?, I can't command all the lot of you:}. Follow our lead.", "close_window",[(party_set_ai_behavior, "$g_encountered_party", ai_bhvr_attack_party),
##                                                                         (party_set_ai_object, "$g_encountered_party", "p_main_party"),
##                                                                         (party_set_flags, "$g_encountered_party", pf_default_behavior, 0),
##                                                                         (assign, "$g_leave_encounter", 1)]],
##
##  [anyone|plyr,"player_old_garrison_encounter", [(assign, reg1, 0),
##                                                 (try_begin),
##                                                   (neg|party_can_join),
##                                                   (assign, reg1, 1),
##                                                 (try_end)],
##   "You can't join us now{reg1?, I can't command all the lot of you:}. Stay here and wait for me.", "close_window",[
##       (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_travel_to_point),
##       (party_get_position, pos1, "$g_encountered_party"),
##       (party_set_ai_target_position, "$g_encountered_party", pos1),
##       (party_set_flags, "$g_encountered_party", pf_default_behavior, 0),
##       (assign, "$g_leave_encounter", 1)]],
##






  [anyone,"start", [(eq, "$talk_context", tc_castle_gate)],
   "What do you want?", "castle_gate_guard_talk",[]],

  [anyone,"castle_gate_guard_pretalk", [],
   "Yes?", "castle_gate_guard_talk",[]],

  [anyone|plyr,"castle_gate_guard_talk", [(ge, "$g_encountered_party_relation", 0)], 
  "We need shelter for the night. Will you let us in?", "castle_gate_open",[]],
  [anyone|plyr,"castle_gate_guard_talk", [(party_slot_ge, "$g_encountered_party", slot_town_lord, 1)], "I want to speak with the lord of the castle.", "request_meeting_castle_lord",[]],
  [anyone|plyr,"castle_gate_guard_talk", [], "I want to speak with someone in the castle.", "request_meeting_other",[]],

  [anyone|plyr,"castle_gate_guard_talk", [], "[Leave]", "close_window",[]],

  [anyone,"request_meeting_castle_lord", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
                                         (eq, "$g_encountered_party", reg0),
                                         (str_store_troop_name, s2, ":castle_lord"),
                                         (assign, "$lord_requested_to_talk_to", ":castle_lord"),
                                          ],  "Wait here. {s2} will see you.", "close_window",[]],
  
  [anyone,"request_meeting_castle_lord", [],  "My lord is not here now.", "castle_gate_guard_pretalk",[]],

  [anyone,"request_meeting_other", [],  "Who is that?", "request_meeting_3",[]],

  [anyone|plyr|repeat_for_troops,"request_meeting_3", [(store_repeat_object, ":troop_no"),
                                                       (troop_is_hero, ":troop_no"),
                                                       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                                                       (call_script, "script_get_troop_attached_party", ":troop_no"),
                                                       (eq, "$g_encountered_party", reg0),
                                                       (str_store_troop_name, s3, ":troop_no"),
                                                       ],
   "{s3}", "request_meeting_4",[(store_repeat_object, "$lord_requested_to_talk_to")]],

  [anyone|plyr,"request_meeting_3", [], "Never mind.", "close_window",[(assign, "$lord_requested_to_talk_to", 0)]],

  [anyone,"request_meeting_4", [], "Wait there. I'll send him your request.", "request_meeting_5",[]],

  [anyone|plyr,"request_meeting_5", [], "I'm waiting...", "request_meeting_6",[]],

  [anyone,"request_meeting_6",
   [
     (call_script, "script_troop_get_player_relation", "$lord_requested_to_talk_to"),
     (assign, ":lord_relation", reg0),
     (gt, ":lord_relation", -20),
    ], "All right. {s2} will talk to you now.", "close_window",[(str_store_troop_name, s2, "$lord_requested_to_talk_to")]],

  [anyone,"request_meeting_6", [(str_store_troop_name, s2, "$lord_requested_to_talk_to")], "{s2} says he will not see you. Begone now.", "close_window",[]],

  [anyone,"castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
                                         (eq, "$g_encountered_party", reg0),
                                         (ge, "$g_encountered_party_relation", 0),
                                         (call_script, "script_troop_get_player_relation", ":castle_lord"),
                                         (assign, ":castle_lord_relation", reg0),
                                         #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
                                         (ge, ":castle_lord_relation", 5),
                                         (str_store_troop_name, s2, ":castle_lord")
                                         ],  "My lord {s2} will be happy to see you {sir/madam}.\
 Come on in. I am opening the gates for you.", "close_window",[(assign,"$g_permitted_to_center",1)]],


  [anyone,"castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
                                         (neq, "$g_encountered_party", reg0),
                                         (ge, "$g_encountered_party_relation", 0),
                                         (call_script, "script_troop_get_player_relation", ":castle_lord"),
                                         (assign, ":castle_lord_relation", reg0),
                                         #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
                                         (ge, ":castle_lord_relation", 5),
                                         (str_store_troop_name, s2, ":castle_lord")
                                         ],  "My lord {s2} is not in the castle now.\
 But I think he would approve of you taking shelter here.\
 Come on in. I am opening the gates for you.", "close_window",[(assign,"$g_permitted_to_center",1)]],
 
  [anyone,"castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                               (call_script, "script_troop_get_player_relation", ":castle_lord"),
                               (assign, ":castle_lord_relation", reg0),
                               #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
                               (ge, ":castle_lord_relation", -2),
                                         ],  "Come on in. I am opening the gates for you.", "close_window",[(assign,"$g_permitted_to_center",1)]],
                                         
  [anyone,"castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                               (call_script, "script_troop_get_player_relation", ":castle_lord"),
                               (assign, ":castle_lord_relation", reg0),
                               #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
                               (ge, ":castle_lord_relation", -19),
                               (str_store_troop_name, s2, ":castle_lord")
                                         ],  "Come on in. But make sure your men behave sensibly within the walls.\
 My lord {s2} does not want trouble here.", "close_window",[(assign,"$g_permitted_to_center",1)]],
 
  [anyone,"castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                               (str_store_troop_name, s2, ":castle_lord"),
  ],  "My lord {s2} does not want you here. Begone now.", "close_window",[]],


#Enemy Kingdom Meetings


#  [anyone,"start", [(eq, "$talk_context", tc_lord_talk_in_center)],
#   "Greetings {playername}.", "request_meeting_1",[]],

#  [anyone,"request_meeting_pretalk", [(eq, "$talk_context", tc_lord_talk_in_center)],
#   "Yes?", "request_meeting_1",[]],
  
#  [anyone|plyr,"request_meeting_1", [(ge, "$g_encountered_party_faction", 0)], "Open the gates and let me in!", "request_meeting_open_gates",[]],
  
#  [anyone|plyr,"request_meeting_1", [(party_slot_ge, "$g_encountered_party", slot_town_lord, 1)], "I want to speak with the lord of the castle.", "request_meeting_castle_lord",[]],
#  [anyone|plyr,"request_meeting_1", [], "I want to speak with someone in the castle.", "request_meeting_other",[]],

##### TODO: QUESTS COMMENT OUT BEGIN
##  [anyone|plyr,"request_meeting_1",[(check_quest_active,"qst_bring_prisoners_to_enemy"),
##                                    (neg|check_quest_succeeded, "qst_bring_prisoners_to_enemy"),
##                                    (quest_get_slot, ":quest_giver_troop", "qst_bring_prisoners_to_enemy", slot_quest_giver_troop),
##                                    (quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                                    (quest_get_slot, ":quest_object_troop", "qst_bring_prisoners_to_enemy", slot_quest_object_troop),
##                                    (quest_slot_eq, "qst_bring_prisoners_to_enemy", slot_quest_target_center, "$g_encountered_party"),
##                                    (party_count_prisoners_of_type, ":num_prisoners", "p_main_party", ":quest_object_troop"),
##                                    (ge, ":num_prisoners", ":quest_target_amount"),
##                                    (str_store_troop_name,1,":quest_giver_troop"),
##                                    (assign, reg1, ":quest_target_amount"),
##                                    (str_store_troop_name_plural,2,":quest_object_troop")],
##   "TODO: Sir, lord {s1} ordered me to bring {reg1} {s2} for ransom.", "guard_prisoners_brought",
##   [(quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##    (quest_get_slot, ":quest_target_center", "qst_bring_prisoners_to_enemy", slot_quest_target_center),
##    (quest_get_slot, ":quest_object_troop", "qst_bring_prisoners_to_enemy", slot_quest_object_troop),
##    (party_remove_prisoners, "p_main_party", ":quest_object_troop", ":quest_target_amount"),
##    (party_add_members, ":quest_target_center", ":quest_object_troop", ":quest_target_amount"),
##    (call_script, "script_game_get_join_cost", ":quest_object_troop"),
##    (assign, ":reward", reg0),
##    (val_mul, ":reward", ":quest_target_amount"),
##    (val_div, ":reward", 2),
##    (call_script, "script_troop_add_gold", "trp_player",":reward"),
##    (party_get_slot, ":cur_lord", "$g_encountered_party", slot_town_lord),#Removing gold from the town owner's wealth
##    (troop_get_slot, ":cur_wealth", ":cur_lord", slot_troop_wealth),
##    (val_sub, ":cur_wealth", ":reward"),
##    (troop_set_slot, ":cur_lord", slot_troop_wealth, ":cur_wealth"),
##    (quest_set_slot, "qst_bring_prisoners_to_enemy", slot_quest_target_amount, ":reward"),
##    (succeed_quest, "qst_bring_prisoners_to_enemy"),
##    ]],
##
##  [anyone|plyr,"request_meeting_1",[(check_quest_active,"qst_bring_prisoners_to_enemy"),
##                                    (neg|check_quest_succeeded, "qst_bring_prisoners_to_enemy"),
##                                    (quest_get_slot, ":quest_giver_troop", "qst_bring_prisoners_to_enemy", slot_quest_giver_troop),
##                                    (quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                                    (quest_get_slot, ":quest_object_troop", "qst_bring_prisoners_to_enemy", slot_quest_object_troop),
##                                    (quest_slot_eq, "qst_bring_prisoners_to_enemy", slot_quest_target_center, "$g_encountered_party"),
##                                    (party_count_prisoners_of_type, ":num_prisoners", "p_main_party", ":quest_object_troop"),
##                                    (lt, ":num_prisoners", ":quest_target_amount"),
##                                    (gt, ":num_prisoners", 0),
##                                    (str_store_troop_name,1,":quest_giver_troop"),
##                                    (assign, reg1, ":quest_target_amount"),
##                                    (str_store_troop_name_plural,2,":quest_object_troop")],
##   "TODO: Sir, lord {s1} ordered me to bring {reg1} {s2} for ransom, but some of them died during my expedition.", "guard_prisoners_brought_some",
##   [(quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##    (quest_get_slot, ":quest_target_center", "qst_bring_prisoners_to_enemy", slot_quest_target_center),
##    (quest_get_slot, ":quest_object_troop", "qst_bring_prisoners_to_enemy", slot_quest_object_troop),
##    (party_count_prisoners_of_type, ":num_prisoners", "p_main_party", ":quest_object_troop"),
##    (party_remove_prisoners, "p_main_party", ":quest_object_troop", ":num_prisoners"),
##    (party_add_members, ":quest_target_center", ":quest_object_troop", ":num_prisoners"),
##    (call_script, "script_game_get_join_cost", ":quest_object_troop"),
##    (assign, ":reward", reg0),
##    (val_mul, ":reward", ":num_prisoners"),
##    (val_div, ":reward", 2),
##    (call_script, "script_troop_add_gold", "trp_player",":reward"),
##    (party_get_slot, ":cur_lord", "$g_encountered_party", slot_town_lord),#Removing gold from the town owner's wealth
##    (troop_get_slot, ":cur_wealth", ":cur_lord", slot_troop_wealth),
##    (val_sub, ":cur_wealth", ":reward"),
##    (troop_set_slot, ":cur_lord", slot_troop_wealth, ":cur_wealth"),
##    (call_script, "script_game_get_join_cost", ":quest_object_troop"),
##    (assign, ":reward", reg0),
##    (val_mul, ":reward", ":quest_target_amount"),
##    (val_div, ":reward", 2),
##    (quest_set_slot, "qst_bring_prisoners_to_enemy", slot_quest_current_state, 1),#Some of the prisoners are given, so it's state will change for remembering that.
##    (quest_set_slot, "qst_bring_prisoners_to_enemy", slot_quest_target_amount, ":reward"),#Still needs to pay the lord the full price of the prisoners
##    (succeed_quest, "qst_bring_prisoners_to_enemy"),
##    ]],
##
##
##  [anyone,"guard_prisoners_brought", [],
##   "TODO: Thank you. Here is the money for prisoners.", "request_meeting_pretalk",[]],
##
##  [anyone,"guard_prisoners_brought_some", [],
##   "TODO: Thank you, but that's not enough. Here is the money for prisoners.", "request_meeting_pretalk",[]],

#  [anyone|plyr,"request_meeting_1", [], "[Leave]", "close_window",[]],




  
##  [anyone,"request_meeting_open_gates", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
##                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
##                                         (eq, "$g_encountered_party", reg0),
##                                         (str_store_troop_name, 1, ":castle_lord")
##                                         ],  "My lord {s1} is in the castle now. You must ask his permission to enter.", "request_meeting_pretalk",[]],
##
##  [anyone,"request_meeting_open_gates", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
##                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
##                                         (neq, "$g_encountered_party", reg0),
##                                         (ge, "$g_encountered_party_relation", 0),
##                                         (troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
##                                         (ge, ":castle_lord_relation", 20),
##                                         (str_store_troop_name, 1, ":castle_lord")
##                                         ],  "My lord {s1} is not in the castle now.\
## But I think he would approve of you taking shelter here, {sir/madam}.\
## Come on in. I am opening the gates for you.", "close_window",[]],
##  
##  [anyone,"request_meeting_open_gates", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),(str_store_troop_name, 1, ":castle_lord")],
##   "My lord {s1} is not in the castle now. I can't allow you into the castle without his orders.", "request_meeting_pretalk",[]],
  

  

# Quest conversations

##### TODO: QUESTS COMMENT OUT BEGIN
  
##  [party_tpl|pt_peasant_rebels,"start", [],
##   "TODO: What.", "peasant_rebel_talk",[]],
##  [anyone|plyr, "peasant_rebel_talk", [], "TODO: Die.", "close_window",[]],
##  [anyone|plyr, "peasant_rebel_talk", [], "TODO: Nothing.", "close_window",[(assign, "$g_leave_encounter",1)]],
##
##  [party_tpl|pt_noble_refugees,"start", [],
##   "TODO: What.", "noble_refugee_talk",[]],
##  [anyone|plyr, "noble_refugee_talk", [], "TODO: Nothing.", "close_window",[(assign, "$g_leave_encounter",1)]],
##

### TLD dialogs: starting quest caravan master talk
  [trp_start_quest_caravaneer,"party_relieved", [(eq,"$talk_context",tc_starting_quest),], "Thank you for helping! We are safe now.","caravan_help0",[]], 
  [trp_start_quest_caravaneer,"caravan_help0", [], "Thank you for helping! We are safe now. Have you seen those large orcs before? Those do not look like regular mountain ilk we are used to fend off easily. And the paint on their shields is an ancient Mordor sign. I haven't seen those this side of the river for a long time. Dire things are afoot.. War is coming! I advise you to go to Edoras, the capital of your people, and deliver the message about what you've seen to whomever is in command there. It's an important matter, so please make haste.", "caravan_help1",[
       (setup_quest_text, "qst_tld_introduction"),
       (str_store_string, s2, "str_tld_introduction"),
       (add_quest_note_from_sreg, "qst_tld_introduction", 0, s2, 0),
       (start_quest, "qst_tld_introduction")]],
  [trp_start_quest_caravaneer|plyr,"caravan_help1", [], "Yeah, I never seen such a large orc before. Nasty things.", "caravan_help2",[]],
  [trp_start_quest_caravaneer,"caravan_help2", [], "Also, I see you are a capable warrior. I have a personal business I would like your help with. There is a small fort near Nindalf swamps, where common people and travellers can find food and lodge. It's run by a local chief who does not answer neither to Gondor, nor to Rohan. I'm a merchant traveller myself, so I have respect for people wishing to be free from lordship bonds, as long as they behave. But being independent, they are also powerless before enemy onslaught. War outbreak in next several days looks like a certain thing to me. I want you to get to those people and see if you can help them survive. Tell the chief, Balan, that Torbal asked you to deliver 'a fishslap'. He will recognize it was me who sent you.", "caravan_help3",[]],
  [trp_start_quest_caravaneer|plyr,"caravan_help3", [], "I'll deliver your message. Safe journey to you, Torbal. I'm sure we will meet again.", "close_window",[(assign, "$g_leave_encounter",1)]],
# end starting quest caravan master talk

  [anyone,"start", [(eq,"$talk_context",tc_join_battle_ally),
                    ],
   "You have come just in time. Let us join our forces now and teach our enemy a lesson.", "close_window",
   []],

  [anyone,"start", [(eq,"$talk_context",tc_join_battle_enemy),
                    ],
   "You are making a big mistake by fighting against us.", "close_window",
   []],

  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (eq, "$g_talk_troop_met", 0),
                    (ge, "$g_talk_troop_relation", 17),
                    ],
   "I don't think we have met properly my friend. You just saved my life out there, and I still don't know your name...", "ally_thanks_meet", []],


  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (eq, "$g_talk_troop_met", 0),
                    (ge, "$g_talk_troop_relation", 5),
                    ],
   "Your help was most welcome stranger. My name is {s1}. Can I learn yours?", "ally_thanks_meet", []],

  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (eq, "$g_talk_troop_met", 0),
                    (ge, "$g_talk_troop_relation", 0),
                    (str_store_troop_name, s1, "$g_talk_troop"),
                    ],
   "Thanks for your help, stranger. We haven't met properly yet, have we? What is your name?", "ally_thanks_meet", []],

  [anyone|plyr,"ally_thanks_meet", [], "My name is {playername}.", "ally_thanks_meet_2", []],

  [anyone, "ally_thanks_meet_2", [(ge, "$g_talk_troop_relation", 15),(str_store_troop_name, s1, "$g_talk_troop")],
   "Well met indeed {playername}. My name is {s1} and I am forever in your debt. If there is ever anything I can help you with, just let me know...", "close_window", []],
  [anyone, "ally_thanks_meet_2", [(ge, "$g_talk_troop_relation", 5),], "Well met {playername}. I am in your debt for what you just did. I hope one day I will find a way to repay it.", "close_window", []],
  [anyone, "ally_thanks_meet_2", [], "Well met {playername}. I am {s1}. Thanks for your help and I hope we meet again.", "close_window", []],

#Post 0907 changes begin
  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_talk_troop_relation", 30),
                    (ge, "$g_relation_boost", 10),
                    ],
   "Again you save our necks, {playername}! Truly, you are the best of friends. {s43}", "close_window", [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_default"),
       (try_begin),
         (party_stack_get_troop_id, ":enemy_party_leader", "p_encountered_party_backup", 0),
         (is_between, ":enemy_party_leader", kingdom_heroes_begin, kingdom_heroes_end),
         (call_script, "script_add_log_entry", logent_lord_helped_by_player, "trp_player",  -1, ":enemy_party_leader", -1),
       (try_end),
       ]],
  
  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_talk_troop_relation", 20),
                    (ge, "$g_relation_boost", 5),
                    ],
   "You arrived just in the nick of time! {playername}. You have my deepest thanks! {s43}", "close_window", [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_default"),
       (try_begin),
         (party_stack_get_troop_id, ":enemy_party_leader", "p_encountered_party_backup", 0),
         (is_between, ":enemy_party_leader", kingdom_heroes_begin, kingdom_heroes_end),
         (call_script, "script_add_log_entry", logent_lord_helped_by_player, "trp_player",  -1, ":enemy_party_leader", -1),
       (try_end),
       ]],
  
  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_talk_troop_relation", 0),
                    (ge, "$g_relation_boost", 3),
                    ],
   "You turned up just in time, {playername}. I will not forget your help. {s43}", "close_window", [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_default"),
       (try_begin),
         (party_stack_get_troop_id, ":enemy_party_leader", "p_encountered_party_backup", 0),
         (is_between, ":enemy_party_leader", kingdom_heroes_begin, kingdom_heroes_end),
         (call_script, "script_add_log_entry", logent_lord_helped_by_player, "trp_player",  -1, ":enemy_party_leader", -1),
       (try_end),
       ]],

  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_talk_troop_relation", -5),
                    ],
   "Good to see you here, {playername}. {s43}", "close_window", [
                    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_default"),
       ]],


  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_relation_boost", 4),
                    ],
   "{s43}", "close_window", [
                    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_grudging_default"),
                    ]],


  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    ],
   "{s43}", "close_window", [
                    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_unfriendly_default"),
                    ]],


#  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
#                    (troop_is_hero, "$g_talk_troop"),
#                    (ge, "$g_talk_troop_relation", -20),
#                    ],
#   "So, this is {playername}. Well, your help wasn't really needed, but I guess you had nothing better to do, right?", "close_window", []],

#  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
#                    (troop_is_hero, "$g_talk_troop"),
#                    ],
#   "Who told you to come to our help? I certainly didn't. Begone now. I want nothing from you and I will not let you steal my victory.", "close_window", []],

#Post 0907 changes begin

  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (ge, "$g_relation_boost", 10),
                    (party_get_num_companions, reg1, "$g_encountered_party"),
                    (val_sub, reg1, 1),
                    ],
   "Thank you for your help {sir/madam}. You saved {reg1?our lives:my life} out there.", "close_window", []],

  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (ge, "$g_relation_boost", 5),
                    ],
   "Thank you for your help {sir/madam}. Things didn't look very well for us but then you came up and everything changed.", "close_window", []],

  [anyone,"start", [(eq,"$talk_context",tc_ally_thanks)],
   "Thank you for your help, {sir/madam}. It was fortunate to have you nearby.", "close_window", []],
  
  [anyone,"start", [(eq, "$talk_context", tc_hero_freed),
                    (store_conversation_troop,":cur_troop"),
                    (eq,":cur_troop","trp_kidnapped_girl"),],
   "Oh {sir/madam}. Thank you so much for rescuing me. Will you take me to my family now?", "kidnapped_girl_liberated_battle",[]],

  [anyone,"start", [(eq,"$talk_context",tc_hero_freed)],
   "I am in your debt for freeing me friend.", "freed_hero_answer",
   []],

  [anyone|plyr,"freed_hero_answer", [],
   "You're not going anywhere. You'll be my prisoner now!", "freed_hero_answer_1",
   [
     (store_conversation_troop, ":cur_troop_id"), 
     (party_add_prisoners, "p_main_party", ":cur_troop_id", 1),#take prisoner
    ]],

  [anyone,"freed_hero_answer_1", [],
   "Alas. Will my luck never change?", "close_window",
   []],

  [anyone|plyr,"freed_hero_answer", [],
   "You're free to go, {s65}.", "freed_hero_answer_2",
   [
    ]],

  [anyone,"freed_hero_answer_2", [],
   "Thank you, good {sire/lady}. I never forget someone who's done me a good turn.", "close_window",
   []],

  [anyone|plyr,"freed_hero_answer", [],
   "Would you like to join me?", "freed_hero_answer_3",
   []],

  [anyone,"freed_hero_answer_3", [(store_random_in_range, ":random_no",0,2),(eq, ":random_no", 0)],
   "All right I will join you.", "close_window",
   [
     (store_conversation_troop, ":cur_troop_id"), 
     (party_add_members, "p_main_party", ":cur_troop_id", 1),#join hero
   ]],

  [anyone,"freed_hero_answer_3", [],
   "No, I want to go on my own.", "close_window",
   [
    ]],

  [anyone,"start", [(eq,"$talk_context",tc_hero_defeated)],
   "You'll not live long to enjoy your victory. My kinsmen will soon wipe out the stain of this defeat.", "defeat_hero_answer",
   [
    ]],

  [anyone|plyr,"defeat_hero_answer", [],
   "You are my prisoner now.", "defeat_hero_answer_1",
   [
     (party_add_prisoners, "p_main_party", "$g_talk_troop", 1),#take prisoner
     (troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, "p_main_party"),
    ]],

  [anyone,"defeat_hero_answer_1", [],
   "Damn you. You will regret this.", "close_window",
   []],

  [anyone|plyr,"defeat_hero_answer", [],
   "You're free to go this time, but don't cross my path again.", "defeat_hero_answer_2",
   []],

  [anyone,"defeat_hero_answer_2", [],
   "We will meet again.", "close_window",
   []],



# Local merchant

  [trp_local_merchant,"start", [], "Mercy! Please don't kill me!", "local_merchant_mercy",[]],
  [anyone|plyr,"local_merchant_mercy", [(quest_get_slot, ":quest_giver_troop", "qst_kill_local_merchant", slot_quest_giver_troop),(str_store_troop_name, s2, ":quest_giver_troop")],
   "I have nothing against you man. But {s2} wants you dead. Sorry.", "local_merchant_mercy_no",[]],
  [anyone,"local_merchant_mercy_no", [], "Damn you! May you burn in Hell!", "close_window",[]],
  [anyone|plyr,"local_merchant_mercy", [], "I'll let you live, if you promise me...", "local_merchant_mercy_yes",[]],

  [anyone,"local_merchant_mercy_yes", [], "Of course, I promise, I'll do anything. Just spare my life... ", "local_merchant_mercy_yes_2",[]],
  [anyone|plyr,"local_merchant_mercy_yes_2", [], "You are going to forget about {s2}'s debt to you.\
 And you will sign a paper stating that he owes you nothing.", "local_merchant_mercy_yes_3",[]],
  [anyone,"local_merchant_mercy_yes_3", [], "Yes, of course. I'll do as you say.", "local_merchant_mercy_yes_4",[]],
  [anyone|plyr,"local_merchant_mercy_yes_4", [], "And if my lord hears so much of a hint of a complaint about this issue, then I'll come back for you,\
 and it won't matter how much you scream for mercy then.\
 Do you understand me?", "local_merchant_mercy_yes_5",[]],
  [anyone,"local_merchant_mercy_yes_5", [], "Yes {sir/madam}. Don't worry. I won't make any complaint.", "local_merchant_mercy_yes_6",[]],
  [anyone|plyr,"local_merchant_mercy_yes_6", [], "Good. Go now, before I change my mind.", "close_window",
   [(quest_set_slot, "qst_kill_local_merchant", slot_quest_current_state, 2),
    (call_script, "script_succeed_quest", "qst_kill_local_merchant"),
    (finish_mission),
    ]],

# Village traitor

  [trp_fugitive,"start", [], "Yes, what do you want?", "fugitive_1",[]],
  [trp_fugitive|plyr,"fugitive_1", [
     (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
     (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
     (str_store_string, s4, s50),
      ], "I am looking for a murderer by the name of {s4}. You fit his description.", "fugitive_2",[]],
  [trp_fugitive|plyr,"fugitive_1", [], "Nothing. Sorry to trouble you.", "close_window",[]],
  [trp_fugitive,"fugitive_2", [], "I do not know what you are talking about {sir/madam}.\
 I assure you, I am just one of the dwellers here.", "fugitive_3",[]],
  [trp_fugitive|plyr,"fugitive_3", [], "Then drop your sword. If you are innocent, you have nothing to fear.\
 We'll go now and talk to your neighbours, and if they verify your story, I'll go my way.", "fugitive_4",[]],
  [anyone,"fugitive_4", [], "Damn you! You will not be going anywhere!", "close_window",
   [(set_party_battle_mode),
    (try_for_agents, ":cur_agent"),
      (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
      (eq, ":cur_agent_troop", "trp_fugitive"),
      (agent_set_team, ":cur_agent", 1),
    (try_end),
    (quest_set_slot, "qst_hunt_down_fugitive", slot_quest_current_state, 1),
    ]],


  [anyone,"member_chat", [(check_quest_active, "qst_incriminate_loyal_commander"),
                          (quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_current_state, 0),
                          (store_conversation_troop, "$g_talk_troop"),
                          (eq, "$g_talk_troop", "$incriminate_quest_sacrificed_troop"),
                          (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                          (store_distance_to_party_from_party, ":distance", "p_main_party", ":quest_target_center"),
                          (lt, ":distance", 10),
                          ], "Yes {sir/madam}?", "sacrificed_messenger_1",[]],

  [anyone|plyr,"sacrificed_messenger_1", [(quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                                          (str_store_party_name, s1, ":quest_target_center"),
                                          (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
                                          (str_store_troop_name, s2, ":quest_object_troop"),],
   "Take this letter to {s1} and give it to {s2}.", "sacrificed_messenger_2",[]],
  [anyone|plyr,"sacrificed_messenger_1", [],
   "Nothing. Nothing at all.", "close_window",[]],

  [anyone,"sacrificed_messenger_2", [],
   "Yes {sir/madam}. You can trust me. I will not fail you.", "sacrificed_messenger_3",[]],

  [anyone|plyr,"sacrificed_messenger_3", [],
   "Good. I will not forget your service. You will be rewarded when you return.", "close_window",[(party_remove_members, "p_main_party", "$g_talk_troop", 1),
                                     (set_spawn_radius, 0),
                                     (spawn_around_party, "p_main_party", "pt_sacrificed_messenger"),
                                     (assign, ":new_party", reg0),
                                     (party_add_members, ":new_party", "$g_talk_troop", 1),
                                     (party_set_ai_behavior, ":new_party", ai_bhvr_travel_to_party),
                                     (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                                     (party_set_ai_object, ":new_party", ":quest_target_center"),
                                     (party_set_flags, ":new_party", pf_default_behavior, 0),
                                     (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_current_state, 2),
                                     (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_target_party, ":new_party")]],
  [anyone|plyr,"sacrificed_messenger_3", [], "Arggh! I can't do this. I can't send you to your own death!", "sacrificed_messenger_cancel",[]],
  [anyone,"sacrificed_messenger_cancel", [], "What do you mean {sir/madam}", "sacrificed_messenger_cancel_2",[]],
  [anyone|plyr,"sacrificed_messenger_cancel_2", [(quest_get_slot, ":quest_giver", "qst_incriminate_loyal_commander", slot_quest_giver_troop),
                                                 (str_store_troop_name, s3, ":quest_giver"),
      ], "There's a trap set up for you in the town.\
 {s3} ordered me to sacrifice one of my chosen warriors to fool the enemy,\
 but he will just need to find another way.", "sacrificed_messenger_cancel_3",[
     (quest_get_slot, ":quest_giver", "qst_incriminate_loyal_commander", slot_quest_giver_troop),
     (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_current_state, 1),
     (call_script, "script_change_player_relation_with_troop",":quest_giver",-5),
     (call_script, "script_change_player_honor", 3),
     (call_script, "script_fail_quest", "qst_incriminate_loyal_commander"),
     ]],
  [anyone,"sacrificed_messenger_cancel_3", [], "Thank you, {sir/madam}.\
 I will follow you to the gates of hell. But this would not be a good death.", "close_window",[]],

  [party_tpl|pt_sacrificed_messenger,"start", [],
   "Don't worry, {sir/madam}, I'm on my way.", "close_window",[(assign, "$g_leave_encounter",1)]],

#Spy

  [party_tpl|pt_spy,"start", [], "Good day {sir/madam}. Such fine weather don't you think? If you'll excuse me now I must go on my way.", "follow_spy_talk",[]],

  [anyone|plyr, "follow_spy_talk",
   [
     (quest_get_slot, ":quest_giver", "qst_follow_spy", slot_quest_giver_troop),
     (str_store_troop_name, s1, ":quest_giver"),
     ],
   "In the name of {s1}, you are under arrest!", "follow_spy_talk_2", []],
  [anyone, "follow_spy_talk_2", [], "You won't get me alive!", "close_window", []],
  [anyone|plyr, "follow_spy_talk", [], "Never mind me. I was just passing by.", "close_window", [(assign, "$g_leave_encounter",1)]],

  [party_tpl|pt_spy_partners,"start", [], "Greetings.", "spy_partners_talk",[]],

  [anyone|plyr,"spy_partners_talk",
   [
     (quest_get_slot, ":quest_giver", "qst_follow_spy", slot_quest_giver_troop),
     (str_store_troop_name, s1, ":quest_giver"),
     ],
   "In the name of {s1} You are under arrest!", "spy_partners_talk_2",[]],
  [anyone,"spy_partners_talk_2", [], "You will have to fight us first!", "close_window",[]],
  [anyone|plyr,"spy_partners_talk", [], "Never mind me. I was just passing by.", "close_window",[(assign, "$g_leave_encounter",1)]],


###Conspirator
##
##  [party_tpl|pt_conspirator_leader,"start", [], "TODO: Hello.", "conspirator_talk",[]],
##  [party_tpl|pt_conspirator,"start", [], "TODO: Hello.", "conspirator_talk",[]],
##
##  [anyone|plyr,"conspirator_talk", [(gt, "$qst_capture_conspirators_leave_meeting_counter", 0),
##                                    (quest_get_slot,":quest_giver","qst_capture_conspirators",slot_quest_giver_troop),
##                                    (str_store_troop_name,s1,":quest_giver")],
##   "TODO: In the name of {s1}, you are under arrest!", "conspirator_talk_2",[]],
##
##  [anyone|plyr,"conspirator_talk", [], "TODO: Bye.", "close_window",[(assign, "$g_leave_encounter",1)]],
##
##  [anyone,"conspirator_talk_2", [], "You won't get me alive!", "close_window",[]],
##
#Runaway Peasants


  [party_tpl|pt_runaway_serfs,"start", [(party_slot_eq, "$g_encountered_party", slot_town_center, 0)],#slot_town_center is used for first time meeting
   "Good day {sir/madam}.", "runaway_serf_intro_1",
   [(party_set_slot, "$g_encountered_party", slot_town_center, 1)]],
  
  [anyone|plyr,"runaway_serf_intro_1", [(quest_get_slot, ":lord", "qst_bring_back_runaway_serfs", slot_quest_giver_troop),
                                        (str_store_troop_name, s4, ":lord")],
   "I have been sent by your {s4} whom you are running from. He will not punish you if you return now.", "runaway_serf_intro_2",[]],
   
  [anyone,"runaway_serf_intro_2", [(quest_get_slot, ":target_center", "qst_bring_back_runaway_serfs", slot_quest_target_center),
                                   (str_store_party_name, s6, ":target_center"),
                                   (quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                   (str_store_party_name, s1, ":quest_object_center")],
   "My good {sir/madam}. Our lives at our village {s1} was unbearable. We worked all day long and still went to bed hungry.\
 We are going to {s6} to start a new life, where we will be treated like humans.", "runaway_serf_intro_3",[]],

  [anyone|plyr,"runaway_serf_intro_3", [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                        (str_store_party_name, s1, ":quest_object_center"),],
   "You have gone against our laws by running from your bondage. You will go back to {s1} now!", "runaway_serf_go_back",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", -1)]],

  [anyone|plyr,"runaway_serf_intro_3", [], "Well, maybe you are right. All right then. If anyone asks, I haven't seen you.", "runaway_serf_let_go",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", 1)]],

  [party_tpl|pt_runaway_serfs,"runaway_serf_go_back", [(quest_get_slot, ":home_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                                       (str_store_party_name, s5, ":home_center")],
   "All right {sir/madam}. As you wish. We'll head back to {s5} now.", "close_window",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (party_set_ai_object, "$g_encountered_party", ":quest_object_center"),
    (assign, "$g_leave_encounter",1)]],
  
  [anyone,"runaway_serf_let_go", [], "God bless you, {sir/madam}. We will not forget your help.", "close_window",
   [(party_set_slot, "$g_encountered_party", slot_town_castle, 1),
    (assign, "$g_leave_encounter",1)]],
  

  [party_tpl|pt_runaway_serfs,"start", [(party_slot_eq, "$g_encountered_party", slot_town_castle, 1),
                                        ],
   "Good day {sir/madam}. Don't worry. If anyone asks, we haven't seen you.", "runaway_serf_reconsider",[]],

  [anyone|plyr,"runaway_serf_reconsider", [], "I have changed my mind. You must back to your village!", "runaway_serf_go_back",
   [(party_set_slot, "$g_encountered_party", slot_town_castle, 0),
    (quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", -2)]],

  [anyone|plyr,"runaway_serf_reconsider", [], "Good. Go quickly now before I change my mind.", "runaway_serf_let_go",[]],
  
  
  [party_tpl|pt_runaway_serfs,"start", [(party_slot_eq, "$g_encountered_party", slot_town_castle, 0),
                                        (get_party_ai_object, ":cur_ai_object"),
                                        (quest_get_slot, ":home_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                        (neq, ":home_center", ":cur_ai_object")],
   "Good day {sir/madam}. We were heading back to {s5}, but I am afraid we lost our way.", "runaway_serf_talk_caught",[]],

  [anyone|plyr,"runaway_serf_talk_caught", [], "Do not test my patience. You are going back now!", "runaway_serf_go_back",[]],
  [anyone|plyr,"runaway_serf_talk_caught", [], "Well, if you are that eager to go, then go.", "runaway_serf_let_go",
   [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":quest_object_center", 1)]],
  
  [party_tpl|pt_runaway_serfs,"start",
   [(quest_get_slot, ":home_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (str_store_party_name, s5, ":home_center")], "We are on our way back to {s5} {sir/madam}.", "runaway_serf_talk_again_return",[]],
  
  [anyone|plyr,"runaway_serf_talk_again_return", [], "Make haste now. The sooner you return the better.", "runaway_serf_talk_again_return_2",[]],
  [anyone|plyr,"runaway_serf_talk_again_return", [], "Good. Keep going.", "runaway_serf_talk_again_return_2",[]],
  
  [anyone|plyr,"runaway_serf_talk_again_return_2", [], "Yes {sir/madam}. As you wish.", "close_window",[(assign, "$g_leave_encounter",1)]],
  


#Deserters
  [party_tpl|pt_deserters, "start", [(eq,"$talk_context",tc_party_encounter),
                                     (party_get_slot,":protected_until_hours", "$g_encountered_party",slot_party_ignore_player_until),
                                     (store_current_hours,":cur_hours"),
                                     (store_sub, ":protection_remaining",":protected_until_hours",":cur_hours"),
                                     (gt, ":protection_remaining", 0)], "What do you want?\
 You want to pay us some more money?", "deserter_paid_talk",[]],
  [anyone|plyr,"deserter_paid_talk", [], "Sorry to trouble you. I'll be on my way now.", "deserter_paid_talk_2a",[]],
  [anyone,"deserter_paid_talk_2a", [], "Yeah. Stop fooling around and go make some money.\
 I want to see that purse full next time I see you.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone|plyr,"deserter_paid_talk", [], "No. It's your turn to pay me this time.", "deserter_paid_talk_2b",[]],
  [anyone,"deserter_paid_talk_2b", [], "What nonsense are you talking about? You want trouble? You got it.", "close_window",[
       (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,0),
       (party_ignore_player, "$g_encountered_party", 0),
    ]],

  
  [party_tpl|pt_deserters,"start", [
      (eq,"$talk_context",tc_party_encounter)
                    ], "We are the free brothers.\
 We will fight only for ourselves from now on.\
 Now give us your gold or taste our steel.", "deserter_talk",[]],
##  [anyone|plyr,"deserter_talk", [(check_quest_active, "qst_bring_back_deserters"),
##                                 (quest_get_slot, ":target_deserter_troop", "qst_bring_back_deserters", slot_quest_target_troop),
##                                 (party_count_members_of_type, ":num_deserters", "$g_encountered_party",":target_deserter_troop"),
##                                 (gt, ":num_deserters", 1)],
##   "If you surrender to me now, you will rejoin the army of your kingdom without being punished. Otherwise you'll get a taste of my sword.", "deserter_join_as_prisoner",[]],
  [anyone|plyr,"deserter_talk", [], "When I'm done with you, you'll regret ever leaving your army.", "close_window",[]],
  [anyone|plyr,"deserter_talk", [], "There's no need to fight. I am ready to pay for free passage.", "deserter_barter",[]],

##  [anyone,"deserter_join_as_prisoner", [(call_script, "script_party_calculate_strength", "p_main_party"),
##                                        (assign, ":player_strength", reg0),
##                                        (store_encountered_party,":encountered_party"),
##                                        (call_script, "script_party_calculate_strength", ":encountered_party"),
##                                        (assign, ":enemy_strength", reg0),
##                                        (val_mul, ":enemy_strength", 2),
##                                        (ge, ":player_strength", ":enemy_strength")],
##   "All right we join you then.", "close_window",[(assign, "$g_enemy_surrenders", 1)]],
##  [anyone,"deserter_join_as_prisoner", [], "TODO: We will never surrender!", "close_window",[(encounter_attack)]],

  [anyone,"deserter_barter", [], "Good. You are clever. You pay us {reg5} denars. Then you can go.", "deserter_barter_2",[(assign,"$deserter_tribute",150),(assign,reg(5),"$deserter_tribute")]],
  [anyone|plyr,"deserter_barter_2", [(store_troop_gold,reg(2)),(ge,reg(2),"$deserter_tribute"),(assign,reg(5),"$deserter_tribute")],
   "All right here's your {reg5} denars.", "deserter_barter_3a",[(troop_remove_gold, "trp_player","$deserter_tribute")]],
  [anyone|plyr,"deserter_barter_2", [],
   "I don't have that much money with me", "deserter_barter_3b",[]],
  [anyone,"deserter_barter_3b", [],
   "Too bad. Then we'll have to sell you to the slavers.", "close_window",[]],


  [anyone,"deserter_barter_3a", [], "Heh. That wasn't difficult now was it? All right. Go now.", "close_window",[
    (store_current_hours,":protected_until"),
    (val_add, ":protected_until", 72),
    (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,":protected_until"),
    (party_ignore_player, "$g_encountered_party", 72),
      
    (assign, "$g_leave_encounter",1)
    ]],

##### TODO: QUESTS COMMENT OUT END

#Tavernkeepers

  [anyone ,"start", [(store_conversation_troop,reg(1)),(ge,reg(1),tavernkeepers_begin),(lt,reg(1),tavernkeepers_end)],
   "Good day dear {sir/madam}. How can I help you?", "tavernkeeper_talk",
   [
#    (store_encountered_party,reg(2)),
#    (party_get_slot,"$tavernkeeper_party",reg(2),slot_town_mercs),
    ]],
  
  [anyone,"tavernkeeper_pretalk", [], "Anything else?", "tavernkeeper_talk",[]],

  [anyone|plyr,"tavernkeeper_talk", [(check_quest_active,"qst_deliver_wine"),
                                     (quest_slot_eq, "qst_deliver_wine", slot_quest_target_center, "$g_encountered_party"),
                                     (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
                                     (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
                                     (store_item_kind_count, ":item_count", ":quest_target_item"),
                                     (ge, ":item_count", ":quest_target_amount"),
                                     (assign, reg9, ":quest_target_amount"),
                                     (str_store_item_name, s4, ":quest_target_item"),
                                     ],
   "I was told to deliver you {reg9} units of {s4}.", "tavernkeeper_deliver_wine",[]],
  [anyone,"tavernkeeper_deliver_wine", [],
 "At last! My stock was almost depleted.\
 I had paid the cost of the {s4} in advance.\
 Here, take these {reg5} denars. That should cover your pay.\
 And give {s9} my regards.\
 I'll put in a good word for you next time I deal with him.", "tavernkeeper_pretalk",
   [(quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, ":quest_gold_reward", "qst_deliver_wine", slot_quest_gold_reward),
    (quest_get_slot, ":quest_giver_troop", "qst_deliver_wine", slot_quest_giver_troop),
    (troop_remove_items, "trp_player", ":quest_target_item", ":quest_target_amount"),
    (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    (assign, ":xp_reward", ":quest_gold_reward"),
    (val_mul, ":xp_reward", 4),
    (add_xp_as_reward, ":xp_reward"),
    (assign, reg5, ":quest_gold_reward"),
    (str_store_item_name, s4, ":quest_target_item"),
    (str_store_troop_name, s9, ":quest_giver_troop"),
    
    (quest_get_slot, ":giver_town", "qst_deliver_wine", slot_quest_giver_center),
    (call_script, "script_change_player_relation_with_center", ":giver_town", 2),
    (call_script, "script_change_player_relation_with_center", "$current_town", 1),
    (call_script, "script_end_quest", "qst_deliver_wine"),
    ]],

	
  [anyone|plyr,"tavernkeeper_talk", [(check_quest_active,"qst_deliver_wine"),
                                     (quest_slot_eq, "qst_deliver_wine", slot_quest_target_center, "$g_encountered_party"),
                                     (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
                                     (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
                                     (store_item_kind_count, ":item_count", ":quest_target_item"),
                                     (lt, ":item_count", ":quest_target_amount"),
                                     (gt, ":item_count", 0),
                                     (assign, reg9, ":quest_target_amount"),
                                     (str_store_item_name, s4, ":quest_target_item"),
                                     ],
   "I was told to deliver you {reg9} units of {s4}, but I lost some of the cargo on the way.", "tavernkeeper_deliver_wine_incomplete",[]],
  [anyone,"tavernkeeper_deliver_wine_incomplete", [],
 "Attacked by bandits eh?\
 You are lucky they left you alive.\
 Anyway, I can pay you no more than {reg5} denars for this.\
 And I will let {s1} know that my order was delivered less than completely,\
 so you will probably be charged for this loss.", "tavernkeeper_pretalk",
   [(quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, ":quest_gold_reward", "qst_deliver_wine", slot_quest_gold_reward),
    (quest_get_slot, ":quest_giver_troop", "qst_deliver_wine", slot_quest_giver_troop),
    (store_item_kind_count, ":item_count", ":quest_target_item"),
    (troop_remove_items, "trp_player", ":quest_target_item", ":item_count"),
    (val_mul, ":quest_gold_reward", ":item_count"),
    (val_div, ":quest_gold_reward", ":quest_target_amount"),
    (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    (assign, reg5, ":quest_gold_reward"),
    (assign, ":xp_reward", ":quest_gold_reward"),
    (val_mul, ":xp_reward", 4),
    (add_xp_as_reward, ":xp_reward"),
    (str_store_troop_name, s1, ":quest_giver_troop"),
    (assign, ":debt", "$qst_deliver_wine_debt"),
    (store_sub, ":item_left", ":quest_target_amount", ":item_count"),
    (val_mul, ":debt", ":item_left"),
    (val_div, ":debt", ":quest_target_amount"),
    (val_add, "$debt_to_merchants_guild", ":debt"),
    (quest_get_slot, ":giver_town", "qst_deliver_wine", slot_quest_giver_center),
    (call_script, "script_change_player_relation_with_center", ":giver_town", 1),
    (call_script, "script_end_quest", "qst_deliver_wine"),
    ]],
  
  [anyone|plyr,"tavernkeeper_talk", [(check_quest_active,"qst_deliver_wine"),
                                     (quest_slot_eq, "qst_deliver_wine", slot_quest_target_center, "$g_encountered_party"),
                                     (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
                                     (store_item_kind_count, ":item_count", ":quest_target_item"),
                                     (eq, ":item_count", 0),
                                     (quest_get_slot, reg9, "qst_deliver_wine", slot_quest_target_amount),
                                     (str_store_item_name, s4, ":quest_target_item"),
                                     ],
   "I was told to deliver you {reg9} units of {s4}, but I lost the cargo on the way.", "tavernkeeper_deliver_wine_lost",[]],
  
  [anyone,"tavernkeeper_deliver_wine_lost", [],
 "What? I was waiting for that {s4} for weeks!\
 And now you are telling me that you lost it?\
 You may rest assured that I will let {s1} know about this.", "tavernkeeper_pretalk",
   [(add_xp_as_reward, 40),
    (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_giver_troop", "qst_deliver_wine", slot_quest_giver_troop),
    (str_store_item_name, s4, ":quest_target_item"),
    (str_store_troop_name, s1, ":quest_giver_troop"),
    (val_add, "$debt_to_merchants_guild", "$qst_deliver_wine_debt"),
    (call_script, "script_end_quest", "qst_deliver_wine"),
   ]],

##  [anyone|plyr,"tavernkeeper_talk", [], "I need to hire some soldiers. Can you help me?", "tavernkeeper_buy_peasants",[]],
##  [anyone,"tavernkeeper_buy_peasants",
##   [
##       (store_encountered_party,reg(3)),
##       (store_faction_of_party,reg(4),reg(3)),
##       (store_relation,reg(5),"fac_player_supporters_faction",reg(4)),
##       (lt, reg(5), -3),
##    ], "I don't think anyone from this town will follow somebody like you. Try your luck elsewhere.", "tavernkeeper_buy_peasants_2",[]],
##  [anyone,"tavernkeeper_buy_peasants", [], "I know a few fellows who would follow you if you paid for their equipment.", "tavernkeeper_buy_peasants_2",[(set_mercenary_source_party,"$tavernkeeper_party"),[change_screen_buy_mercenaries]]],
##  [anyone,"tavernkeeper_buy_peasants_2", [], "Anything else?", "tavernkeeper_talk",[]],
##
##  [anyone|plyr,"tavernkeeper_talk", [], "I want to rest for a while.", "tavernkeeper_rest",[]],
###  [anyone,"tavernkeeper_rest", [], "Of course... How long do you want to rest?", "tavernkeeper_rest_2",[]],
##  [anyone,"tavernkeeper_rest",
##   [
##       (store_encountered_party,reg(3)),
##       (store_faction_of_party,reg(4),reg(3)),
##       (store_relation,reg(5),"fac_player_supporters_faction",reg(4)),
##       (lt, reg(5), -3),
##      ], "You look like trouble stranger. I can't allow you to stay for the night. No.", "close_window",
##   []],
##  [anyone,"tavernkeeper_rest", [], "Of course... That will be {reg3} denars for the room and food. How long do you want to rest?", "tavernkeeper_rest_2",
##   [(store_party_size,reg(3)),
##    (val_add,reg(3),1),
##    (val_div,reg(3),3),
##    (val_max,reg(3),1),
##    (assign,"$tavern_rest_cost",reg(3))]],
##  [anyone|plyr,"tavernkeeper_rest_2", [(store_time_of_day,reg(1)),
##                                       (val_add,reg(1),7),
##                                       (val_mod,reg(1),24),
##                                       (lt,reg(1),12),
##                                       (store_troop_gold,reg(8),"trp_player"),
##                                       (ge,reg(8),"$tavern_rest_cost"),
##                                       ],
##   "I want to rest until morning.", "close_window",
##   [(assign, reg(2), 13),(val_sub,reg(2),reg(1)),(assign, "$g_town_visit_after_rest", 1),(rest_for_hours, reg(2)),(troop_remove_gold, "trp_player","$tavern_rest_cost"),(call_script, "script_change_player_party_morale", 2)]],
##  [anyone|plyr,"tavernkeeper_rest_2", [(store_time_of_day,reg(1)),
##                                       (val_add,reg(1),7),
##                                       (val_mod,reg(1),24),
##                                       (ge,reg(1),12),
##                                       (store_troop_gold,reg(8),"trp_player"),
##                                       (ge,reg(8),"$tavern_rest_cost"),
##                                       ],
##   "I want to rest until evening.", "close_window",
##   [(assign, reg(2), 28),(val_sub,reg(2),reg(1)),(assign, "$g_town_visit_after_rest", 1),(rest_for_hours, reg(2)),(troop_remove_gold, "trp_player","$tavern_rest_cost"),(call_script, "script_change_player_party_morale", 2)]],
##  [anyone|plyr,"tavernkeeper_rest_2", [], "Forget it.", "close_window",[]],

  [anyone|plyr,"tavernkeeper_talk", [
      (store_current_hours,":cur_hours"),
      (val_sub, ":cur_hours", 24),
      (gt, ":cur_hours", "$buy_drinks_last_time"),
      ], "I'd like to buy every man who comes in here tonight a jar of your best wine.", "tavernkeeper_buy_drinks",[]],

  [anyone,"tavernkeeper_buy_drinks",
   [
    ], "Of course, {my lord/my lady}. I reckon {reg5} denars should be enough for that. What should I tell the lads?", "tavernkeeper_buy_drinks_2",[
        (assign, "$temp", 1000),
        (assign, reg5, "$temp"),
        ]],

  [anyone|plyr,"tavernkeeper_buy_drinks_2",
   [
        (store_troop_gold, ":gold", "trp_player"),
        (ge, ":gold", "$temp"),
        (str_store_party_name, s10, "$current_town"),
    ], "Let everyone know of the generosity of {playername} to the people of {s10}.", "tavernkeeper_buy_drinks_end",[
        
        ]],

  [anyone,"tavernkeeper_buy_drinks_end",
   [], "Don't worry {sir/madam}. Your name will be cheered and toasted here all night.", "tavernkeeper_pretalk",
   [
       (troop_remove_gold, "trp_player", "$temp"),
       (call_script, "script_change_player_relation_with_center", "$current_town", 1),
       (store_current_hours,":cur_hours"),
       (assign, "$buy_drinks_last_time", ":cur_hours"),
       ]],
    #####################################################################################
   # Test: Tavern recruitment and Ale Begin ############################################
   #####################################################################################
  [anyone|plyr,"tavernkeeper_talk", [
      (store_current_hours,":cur_hours"),
      (val_sub, ":cur_hours", 24),
      (gt, ":cur_hours", "$buy_drinks_last_time"),
      ], "I'd like to buy me and my men a barrel of your best ale.", "tavernkeeper_buy_drinks_troops",[]],

  [anyone,"tavernkeeper_buy_drinks_troops",
   [
    ], "Of course, {my lord/my lady}. I reckon {reg5} denars should be enough for that. What should I tell the lads?", "tavernkeeper_buy_drinks_troops_2",[
        (assign, "$temp", 20),
      (store_party_size_wo_prisoners, reg5, "p_main_party"),
      (store_mul, "$temp", "$temp", reg5),
        (assign, reg5, "$temp"),
        ]],

  [anyone|plyr,"tavernkeeper_buy_drinks_troops_2",
   [
        (store_troop_gold, ":gold", "trp_player"),
        (ge, ":gold", "$temp"),
        (str_store_party_name, s10, "$current_town"),
    ], "The price is fair enough, let my men have at it.", "tavernkeeper_buy_drinks_troops_end",[
       
        ]],

  [anyone,"tavernkeeper_buy_drinks_troops_end",
   [], "Don't worry {sir/madam}. Your men will enjoy their pints.", "tavernkeeper_pretalk",
   [
       (troop_remove_gold, "trp_player", "$temp"),
      (call_script, "script_change_player_party_morale", 20),
       (store_current_hours,":cur_hours"),
       (assign, "$buy_drinks_last_time", ":cur_hours"),
      (rest_for_hours, 2, 5, 0)
       ]],

#  [anyone|plyr,"tavernkeeper_buy_drinks_troops_2", [], "Actually, cancel that order.", "tavernkeeper_pretalk",[]],
   #####################################################################################
   # Test: Tavern recruitment and Ale End ##############################################
   #####################################################################################

#  [anyone|plyr,"tavernkeeper_talk", [], "I guess I should leave now.", "close_window",[]],

#Tavern Talk (with companions)
#  [anyone, "companion_recruit_yes", [(neg|hero_can_join, "p_main_party"),], "I don't think can lead any more men than you do now.\
# You need to release someone from service if you want me to join your party.", "close_window", []], 

  [anyone|plyr,"tavernkeeper_buy_drinks_2", [], "Actually, cancel that order.", "tavernkeeper_pretalk",[]],


  [anyone|plyr,"tavernkeeper_talk", [], "I guess I should leave now.", "close_window",[]],

#Tavern Talk (with companions)
#  [anyone, "companion_recruit_yes", [(neg|hero_can_join, "p_main_party"),], "I don't think can lead any more men than you do now.\
# You need to release someone from service if you want me to join your party.", "close_window", []],




#Tavern Talk (with ransom brokers)


  [anyone,"start", [(is_between, "$g_talk_troop", ransom_brokers_begin, ransom_brokers_end),
                    (eq, "$g_talk_troop_met", 0)],
   "Greetings to you, {sir/madam}. You look like someone who should get to know me.", "ransom_broker_intro",[]],

  [anyone|plyr,"ransom_broker_intro",[], "Why is that?", "ransom_broker_intro_2",[]],
  [anyone, "ransom_broker_intro_2", [], "I broker ransoms for the poor wretches who are captured in these endless wars.\
 Normally I travel between the salt mines and the slave markets on the coast, on commission from those whose relatives have gone missing.\
 But if I'm out on my errands of mercy, and I come across a fellow dragging around a captive or two,\
 well, there's no harm in a little speculative investment, is there?\
 And you look like the type who might have a prisoner to sell.", "ransom_broker_info_talk",[(assign, "$ransom_broker_families_told",0),
                                                                                            (assign, "$ransom_broker_prices_told",0),
                                                                                            (assign, "$ransom_broker_ransom_me_told",0),
                                                                                            ]],

  [anyone|plyr,"ransom_broker_info_talk",[(eq, "$ransom_broker_families_told",0)], "What if their families can't pay?", "ransom_broker_families",[]],
  [anyone, "ransom_broker_families", [], "Oh, then I spin them a few heartwarming tales of life on the galleys.\
 You'd be surprised what sorts of treasures a peasant can dig out of his cowshed or wheedle out of his cousins,\
 assuming he's got the proper motivation!\
 And if in the end they cannot come up with the silver, then there are always slave merchants who are looking for galley slaves.\
 One cannot do Heaven's work with an empty purse, you see.", "ransom_broker_info_talk",[(assign, "$ransom_broker_families_told",1)]],
  [anyone|plyr,"ransom_broker_info_talk",[(eq, "$ransom_broker_prices_told",0)], "What can I get for a prisoner?", "ransom_broker_prices",[]],
  [anyone, "ransom_broker_prices", [], "It varies. I fancy that I have a fine eye for assessing a ransom.\
 There are a dozen little things about a man that will tell you whether he goes to bed hungry, or dines each night on soft dumplings and goose.\
 The real money of course is in the gentry, and if you ever want to do my job you'll want to learn about every landowning family in Calradia,\
 their estates, their heraldry, their offspring both lawful and bastard, and, of course, their credit with the merchants.", "ransom_broker_info_talk",[(assign, "$ransom_broker_prices_told",1)]],
  [anyone|plyr,"ransom_broker_info_talk",[(eq, "$ransom_broker_ransom_me_told",0)], "Would you be able to ransom me if I were taken?", "ransom_broker_ransom_me",[]],
  [anyone, "ransom_broker_ransom_me", [], "Of course. I'm welcome in every court in Calradia.\
 There's not many who can say that! So always be sure to keep a pot of denars buried somewhere,\
 and a loyal servant who can find it in a hurry.", "ransom_broker_info_talk",[(assign, "$ransom_broker_ransom_me_told",1)]],
  [anyone|plyr,"ransom_broker_info_talk",[], "That's all I need to know. Thanks.", "ransom_broker_pretalk",[]],

  [anyone,"start", [(is_between, "$g_talk_troop", ransom_brokers_begin, ransom_brokers_end),],
   "Greetings. If you have any prisoners, I will be happy to buy them from you.", "ransom_broker_talk",[]],
  [anyone,"ransom_broker_pretalk", [],
   "Anyway, if you have any prisoners, I will be happy to buy them from you.", "ransom_broker_talk",[]],

  [anyone|plyr,"ransom_broker_talk",
   [[store_num_regular_prisoners,reg(0)],[ge,reg(0),1]],
   "Then you'd better bring your purse. I have got prisoners to sell.", "ransom_broker_sell_prisoners",[]],
  [anyone|plyr,"ransom_broker_talk", [], "Tell me about what you do again.", "ransom_broker_intro_2",[]],
  [anyone|plyr,"ransom_broker_talk",[], "Not this time. Good-bye.", "close_window",[]],
  [anyone,"ransom_broker_sell_prisoners", [],
  "Let me see what you have...", "ransom_broker_sell_prisoners_2",
   [[change_screen_trade_prisoners]]],
#  [anyone, "ransom_broker_sell_prisoners_2", [], "You take more prisoners, bring them to me. I will pay well.", "close_window",[]],
  [anyone, "ransom_broker_sell_prisoners_2", [], "I will be staying here for a few days. Let me know if you need my services.", "close_window",[]],


#Tavern Talk (with travelers)
  [anyone, "start", [(is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end),
                     (str_store_troop_name, s10, "$g_talk_troop"),
                     (eq,"$g_talk_troop_met",0),
                     ],
   "Greetings, friend. You look like the kind of {man/person} who'd do well to know me.\
 I travel a lot all across Calradia and keep an open ear.\
 I can provide you information that you might find useful. For a meager price of course.", "tavern_traveler_talk", [(assign, "$traveler_land_asked", 0)]],

  [anyone, "start",
   [
     (is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end),
     (gt, "$last_lost_companion", 0),
     (assign, ":companion_found_town", -1),
     (troop_get_slot, ":companion_found_town", "$last_lost_companion", slot_troop_cur_center),
     (is_between, ":companion_found_town", towns_begin, towns_end),
     (str_store_troop_name, s10, "$last_lost_companion"),
     (str_store_party_name, s11, ":companion_found_town"),
     ],
   "Greetings, {playername}. I saw your companion {s10} at a tavern in {s11} some days ago. I thought you might like to know.", "tavern_traveler_lost_companion_thanks",
   [(assign, "$last_lost_companion", 0)]],

  [anyone|plyr, "tavern_traveler_lost_companion_thanks", [(troop_get_type, reg3, "$last_lost_companion")], "Thanks. I'll go and find {reg3?her:him} there.", "tavern_traveler_pretalk", []],
  [anyone|plyr, "tavern_traveler_lost_companion_thanks", [], "Thanks, but I don't really care.", "tavern_traveler_pretalk", []],

  [anyone, "start", [(is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end),
                     ],
   "Greetings, {playername}.", "tavern_traveler_talk", [(assign, "$traveler_land_asked", 0)]],



  [anyone, "tavern_traveler_pretalk", [], "Yes?", "tavern_traveler_talk", []],

  [anyone|plyr, "tavern_traveler_talk", [(eq, "$traveler_land_asked", 0)], "What can you tell me about this land?", "tavern_traveler_tell_kingdoms", [(assign, "$traveler_land_asked", 1)]],
  [anyone, "tavern_traveler_tell_kingdoms", [], "Calradia is divided between rival kingdoms, which can neither manage to live in peace with their neighbours,\
 nor completely eliminate them.\
 As a result, there's seldom a break to the bitter wars which plague this land and drain its life blood.\
 Well, at least this must be a good place to be for an adventurer such as yourself.\
 With some luck and skill, you can make a name for yourself here, amass a fortune perhaps, or gain great power.\
 Opportunities are endless and so are the rewards, if you are willing to risk your life for them.", "tavern_traveler_tell_kingdoms_2", []],
  
  [anyone|plyr, "tavern_traveler_tell_kingdoms_2", [], "Tell me more about these opportunities.", "tavern_traveler_tell_kingdoms_3", []],
  [anyone|plyr, "tavern_traveler_tell_kingdoms_2", [], "Thank you. That was all I needed to know", "close_window", []],

  [anyone, "tavern_traveler_tell_kingdoms_3", [(gt, "$player_has_homage", 0)], "Well, you probably know everything I could tell you already. You seem to be doing pretty well.",
   "tavern_traveler_tell_kingdoms_4", []],
  [anyone, "tavern_traveler_tell_kingdoms_3", [], "The kingdoms will pay good money for mercenaries if they are engaged in a war.\
 If you have done a bit of fighting, speaking with one of their lords will probably result in being offered a mercenary contract.\
 However the real rewards come if you can manage to become a vassal to a king.\
 A vassal can own villages, castles and towns and get rich with the taxes and revenues of these estates.\
 Normally, only nobles of the realm own land in this way,\
 but in time of war, a king will not hesitate to accept someone who distinugishes {himself/herself} on the battlefield as a vassal, and grant {him/her} the right to own land.",
   "tavern_traveler_tell_kingdoms_4", []],

  [anyone, "tavern_traveler_tell_kingdoms_4", [], "The only path closed to a an adventurer such as you would be becoming the {king/queen} of a kingdom.\
 The people and nobles of these lands would never accept an upstart adventurer as their ruler.\
 But don't think that kings can sit on their thrones too comfortably, either. They have their own rivals,\
 those who are born to the right family, who could go around and stir up trouble saying they have a better claim to the throne than the current king.\
 If those claim holders could find supporters, they could easily start civil wars and perhaps even replace the king one day.",
   "tavern_traveler_tell_kingdoms_5", []],

  [anyone|plyr, "tavern_traveler_tell_kingdoms_5", [], "Interesting. Where can I find these claim holders?", "tavern_traveler_tell_kingdoms_6", []],
  [anyone|plyr, "tavern_traveler_tell_kingdoms_5", [], "I guess I heard enough already. Thank you.", "close_window", []],

  [anyone, "tavern_traveler_tell_kingdoms_6", [], "A claim holder's life would be in danger in his own country of course.\
 Therefore, they usually stay at rival courts, raising support and hoping to find someone willing to champion their cause.\
 I usually hear news about some of them, and may be able to tell you their location with some precision.\
 But of course, I would ask for a little something for such a service.",
   "tavern_traveler_pretalk", [(assign, "$traveller_claimants_mentioned", 1)]],

  [anyone|plyr, "tavern_traveler_talk", [(eq, "$traveller_claimants_mentioned", 1)], "I want to know the location of a claimant.", "tavern_traveler_pretender_location", []],
  [anyone, "tavern_traveler_pretender_location", [], "Whose location do you want to know?", "tavern_traveler_pretender_location_ask", []],

  [anyone|plyr|repeat_for_troops, "tavern_traveler_pretender_location_ask",
   [
     (store_repeat_object, ":troop_no"),
     (is_between, ":troop_no", pretenders_begin, pretenders_end),
     (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
     (troop_slot_ge, ":troop_no", slot_troop_cur_center, 1),
     (str_store_troop_name, s11, ":troop_no"),
     (neq, ":troop_no", "$supported_pretender"),
     ],  "{s11}", "tavern_traveler_pretender_location_ask_2",
   [
     (store_repeat_object, "$temp"),
     ]],

  [anyone|plyr, "tavern_traveler_pretender_location_ask",
   [],  "Never mind.", "tavern_traveler_pretalk", []],


  [anyone, "tavern_traveler_pretender_location_ask_2", [], "I can reveal this information to you for a small price, let's say 30 denars.", "tavern_traveler_pretender_location_ask_money", []],
  
  [anyone|plyr, "tavern_traveler_pretender_location_ask_money",
   [
     (store_troop_gold, ":cur_gold", "trp_player"),
     (ge, ":cur_gold", 30),
     ], "All right. Here is 30 denars.", "tavern_traveler_pretender_location_tell",
   [
     (troop_remove_gold, "trp_player", 30),
     ]],
  
  [anyone|plyr, "tavern_traveler_pretender_location_ask_money", [], "Never mind.", "tavern_traveler_pretalk", []],

  [anyone, "tavern_traveler_pretender_location_tell", [], "{s15} is currently at {s11}.", "tavern_traveler_pretalk",
   [
     (str_store_troop_name, s15, "$temp"),
     (troop_get_slot, ":cur_center", "$temp", slot_troop_cur_center),
     (str_store_party_name, s11, ":cur_center"),
     ]],


  [anyone|plyr, "tavern_traveler_talk", [], "I am looking for one of my companions...", "tavern_traveler_companion_location", []],

  [anyone, "tavern_traveler_companion_location", [], "Maybe I can help you. Who are you looking for?", "tavern_traveler_companion_location_ask", []],

  [anyone|plyr|repeat_for_troops, "tavern_traveler_companion_location_ask",
   [
     (store_repeat_object, ":troop_no"),
     (is_between, ":troop_no", companions_begin, companions_end),
     (troop_slot_ge, ":troop_no", slot_troop_cur_center, 1),
     (troop_slot_ge, ":troop_no", slot_troop_playerparty_history, 1),
     (str_store_troop_name, s11, ":troop_no"),
     ],  "{s11}", "tavern_traveler_companion_location_ask_2",
   [
     (store_repeat_object, "$temp"),
     ]],

  [anyone|plyr, "tavern_traveler_companion_location_ask",
   [],  "Never mind.", "tavern_traveler_pretalk", []],

  [anyone, "tavern_traveler_companion_location_ask_2", [(str_store_troop_name, s15, "$temp")], "I guess I know where {s15} is. For 30 denars, I'll tell you.", "tavern_traveler_companion_location_ask_money", []],

  [anyone|plyr, "tavern_traveler_companion_location_ask_money",
   [
     (store_troop_gold, ":cur_gold", "trp_player"),
     (ge, ":cur_gold", 30),
     ], "All right. Here is 30 denars.", "tavern_traveler_companion_location_tell",
   [
     (troop_remove_gold, "trp_player", 30),
     ]],
  
  [anyone|plyr, "tavern_traveler_companion_location_ask_money", [], "Never mind.", "tavern_traveler_pretalk", []],

  [anyone, "tavern_traveler_companion_location_tell", [], "{s15} is currently at {s11}.", "tavern_traveler_pretalk",
   [
     (str_store_troop_name, s15, "$temp"),
     (troop_get_slot, ":cur_center", "$temp", slot_troop_cur_center),
     (str_store_party_name, s11, ":cur_center"),
     ]],
  
  [anyone|plyr, "tavern_traveler_talk", [],
   "Farewell.", "close_window", []],

  [anyone, "start", [(is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end),
                     (party_get_slot, ":info_faction", "$g_encountered_party", slot_center_traveler_info_faction),
                     (str_store_faction_name, s17, ":info_faction"),
                     ],
   "Greetings. They say you're the kind of {man/woman} who'd be interested to hear that I travel frequently to {s17}. I'll tell you all I know for a mere 100 denars.", "tavern_traveler_answer", []],

  [anyone|plyr, "tavern_traveler_answer", [(store_troop_gold, ":cur_gold", "trp_player"),
                                            (ge, ":cur_gold", 100)],
   "Here's 100 denars. Tell me what you know.", "tavern_traveler_continue", [(party_get_slot, ":info_faction", "$g_encountered_party", slot_center_traveler_info_faction),
                                           (call_script, "script_update_faction_traveler_notes", ":info_faction"),
                                           (change_screen_notes, 2, ":info_faction"),
                                           ]],

  [anyone|plyr, "tavern_traveler_answer", [],
   "Sorry friend. I am not interested.", "close_window", []],

  [anyone, "tavern_traveler_continue", [],
   "Well, that's all I can tell you. Good bye.", "close_window", [(troop_remove_gold, "trp_player", 100),]],



#Tavern Talk (with minstrels)
  [anyone, "start", [(is_between, "$g_talk_troop", tavern_minstrels_begin, tavern_minstrels_end),
                     ],
   "TODO: Hello. I am a minstrel. (Not implemeted yet)", "close_window", []],

#Tavern Talk (with farmers)
  [anyone, "start", [(eq, "$talk_context", tc_tavern_talk),
                     (eq, "$g_talk_troop", "trp_farmer_from_bandit_village"),
                     (neg|check_quest_active, "qst_eliminate_bandits_infesting_village"),
                     (neg|check_quest_active, "qst_deal_with_bandits_at_lords_village"),
                     (assign, ":end_cond", villages_end),
                     (try_for_range, ":cur_village", villages_begin, ":end_cond"),
                       (party_slot_eq, ":cur_village", slot_village_bound_center, "$g_encountered_party"),
                       (party_slot_ge, ":cur_village", slot_village_infested_by_bandits, 1),
                       (str_store_party_name, s1, ":cur_village"),
                       (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_target_center, ":cur_village"),
                       (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_current_state, 0),
                       (party_get_slot, ":village_elder", ":cur_village", slot_town_elder),
                       (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_giver_troop, ":village_elder"),
                       (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_giver_center, ":cur_village"),
                       (assign, ":end_cond", 0),
                     (try_end),
                     ],
   "{My lord/Madam}, you look like a {man/lady} of the sword and someone who could help us.\
 Will you hear my plea?", "farmer_from_bandit_village_1", []],

  [anyone|plyr, "farmer_from_bandit_village_1", [],
   "What is the matter, my good man?", "farmer_from_bandit_village_2", []],
  [anyone|plyr, "farmer_from_bandit_village_1", [],
   "What are you blurbing about peasant? Speak out.", "farmer_from_bandit_village_2", []],

  [anyone, "farmer_from_bandit_village_2", [],
   "A band of brigands have taken refuge in our village. They take everything we have, force us to serve them, and do us much evil.\
 If one of us so much as breathes a word of protest, they kill the poor soul on the spot right away.\
 Our lives have become unbearable. I risked my skin and ran away to find someone who can help us.", "farmer_from_bandit_village_3", []],
  [anyone|plyr, "farmer_from_bandit_village_3", [],
   "Why don't you go to the lord of your village? He should take care of the vermin.", "farmer_from_bandit_village_4", []],
  [anyone, "farmer_from_bandit_village_4", [],
   "I did, {sir/madam}, but our lord's men did not let me see him and said he was occupied with more important matters and that we should deal with our own problem ourselves.\
 Please {sir/madam}, you look like a {man/lady} of valor and a fearsome warrior, and you have no doubt many friends and soldiers at your service.\
 If there is anyone who can help us, it's you.", "farmer_from_bandit_village_5", [(assign, "$temp", 0)]],
  [anyone|plyr, "farmer_from_bandit_village_5", [],
   "Very well, I'll help you. Where is this village?", "farmer_from_bandit_village_accepted", []],
  [anyone|plyr, "farmer_from_bandit_village_5", [],
   "I can't be bothered with this right now.", "farmer_from_bandit_village_denied", []],
  [anyone|plyr, "farmer_from_bandit_village_5", [(eq, "$temp", 0)],
   "Why would I fight these bandits? What's in it for me?", "farmer_from_bandit_village_barter", []],

  
  [anyone, "farmer_from_bandit_village_accepted", [],
   "God bless you, {sir/madam}. Our village is {s7}. It is not too far from here.", "close_window",
   [(quest_get_slot, ":target_center", "qst_eliminate_bandits_infesting_village", slot_quest_target_center),
    (str_store_party_name_link,s7,":target_center"),
    (setup_quest_text, "qst_eliminate_bandits_infesting_village"),
    (str_store_string, s2, "@A villager from {s7} begged you to save their village from the bandits that took refuge there."),
    (call_script, "script_start_quest", "qst_eliminate_bandits_infesting_village", "$g_talk_troop"),
    ]],

  [anyone, "farmer_from_bandit_village_denied", [],"As you say {sir/madam}. Forgive me for bothering you.", "close_window", []],

  [anyone, "farmer_from_bandit_village_barter", [],
   "We are but poor farmers {sir/madam}, and the bandits have already got most of what we have on this world.\
 but we'll be glad to share with you whatever we have got.\
 And we'll always be in your gratitude if you help us.", "farmer_from_bandit_village_5", [(assign, "$temp", 1)]],
  
  [anyone, "start", [(eq, "$talk_context", tc_tavern_talk),
                     (eq, "$g_talk_troop", "trp_farmer_from_bandit_village"),
                     (check_quest_active, "qst_eliminate_bandits_infesting_village"),
                     ],
   "Thank you for helping us {sir/madam}. Crush those bandits!", "close_window", []],



#Tavern Talk (with troops)

  [anyone, "start", [(eq, "$talk_context", tc_tavern_talk),
                     (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                     (party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
                     (gt, ":mercenary_amount", 0),
                     (store_sub, reg3, ":mercenary_amount", 1),
                     (store_sub, reg4, reg3, 1),
                     (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                     (assign, ":join_cost", reg0),
                     (store_mul, reg5, ":mercenary_amount", reg0),
                     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                     (val_min, ":mercenary_amount", ":free_capacity"),
                     (store_troop_gold, ":cur_gold", "trp_player"),
                     (try_begin),
                       (gt, ":join_cost", 0),
                       (val_div, ":cur_gold", ":join_cost"),
                       (val_min, ":mercenary_amount", ":cur_gold"),
                     (try_end),
                     (assign, "$temp", ":mercenary_amount"),
                     ],
   "Do you have a need for mercenaries, {sir/madam}?\
 {reg3?Me and {reg4?{reg3} of my mates:one of my mates} are:I am} looking for a master.\
 We'll join you for {reg5} denars.", "mercenary_tavern_talk", []],

  [anyone, "start", [(eq, "$talk_context", tc_tavern_talk),],
   "Any orders, {sir/madam}?", "mercenary_after_recruited", []],

  [anyone|plyr, "mercenary_after_recruited", [],
   "Make your preparations. We'll be moving at dawn.", "mercenary_after_recruited_2", []],
  [anyone|plyr, "mercenary_after_recruited", [],
   "Take your time. We'll be staying in this town for a while.", "mercenary_after_recruited_2", []],

  [anyone, "mercenary_after_recruited_2", [], "Yes {sir/madam}. We'll be ready when you tell us to leave.", "close_window", []],

  [anyone|plyr, "mercenary_tavern_talk", [(party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
                                          (eq, ":mercenary_amount", "$temp"),
                                          (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                                          (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                                          (store_mul, reg5, "$temp", reg0),                                          
                                          ],
   "All right. I will hire all of you. Here is {reg5} denars.", "mercenary_tavern_talk_hire", []],

  [anyone|plyr, "mercenary_tavern_talk", [(party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
                                          (lt, "$temp", ":mercenary_amount"),
                                          (gt, "$temp", 0),
                                          (assign, reg6, "$temp"),
                                          (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                                          (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                                          (store_mul, reg5, "$temp", reg0),
                                          ],
   "All right. But I can only hire {reg6} of you. Here is {reg5} denars.", "mercenary_tavern_talk_hire", []],


  [anyone, "mercenary_tavern_talk_hire", [(store_random_in_range, ":rand", 0, 4),
                                          (try_begin),
                                            (eq, ":rand", 0),
                                            (gt, "$temp", 1),
                                            (str_store_string, s17,
                                             "@You chose well, {sir/madam}. My lads know how to keep their word and earn their pay."),
                                          (else_try),
                                            (eq, ":rand", 1), 
                                            (str_store_string, s17,
                                             "@Well done, {sir/madam}. Keep the money and wine coming our way, and there's no foe in Calradia you need fear."),
                                          (else_try),
                                            (eq, ":rand", 2), 
                                            (str_store_string, s17,
                                             "@We are at your service, {sir/madam}. Point us in the direction of those who need hurting, and we'll do the rest."),
                                          (else_try),
                                            (str_store_string, s17,
                                             "@You will not be dissapointed {sir/madam}. You will not find better warriors in all Calradia."),
                                          (try_end),],
   "{s17}", "close_window", [
                                          (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                                          (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                                          (store_mul, ":total_cost", "$temp", reg0),
                                          (troop_remove_gold, "trp_player", ":total_cost"),
                                          (party_add_members, "p_main_party", ":mercenary_troop", "$temp"),
                                          (party_set_slot, "$g_encountered_party", slot_center_mercenary_troop_amount, 0),
                                          ]],

  [anyone|plyr, "mercenary_tavern_talk", [(eq, "$temp", 0),
                                          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                          (ge, ":free_capacity", 1)],
   "That sounds good. But I can't afford to hire any more men right now.", "tavern_mercenary_cant_lead", []],
  
  [anyone, "tavern_mercenary_cant_lead", [], "That's a pity. Well, {reg3?we will:I will} be lingering around here for a while,\
 if you need to hire anyone.", "close_window", []],
  
  [anyone|plyr, "mercenary_tavern_talk", [(eq, "$temp", 0),
                                          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                          (eq, ":free_capacity", 0)],
   "That sounds good. But I can't lead any more men right now.", "tavern_mercenary_cant_lead", []],


  [anyone|plyr, "mercenary_tavern_talk", [],
   "Sorry. I don't need any other men right now.", "close_window", []],

#Trainers

    [anyone,"start", [(is_between, "$g_talk_troop", training_gound_trainers_begin, training_gound_trainers_end)],
   "Good day. Ready for some training today?", "trainer_talk",[]],

    [anyone,"trainer_pretalk", [],
   "Ah, are you ready for some training?", "trainer_talk",[]],
  
    [anyone|plyr,"trainer_talk", [],
   "First, tell me something about combat...", "trainer_combat_begin",[]],

    [anyone|plyr,"trainer_talk", [],
   "I need to leave now. Farewell.", "close_window",[]],


    [anyone,"trainer_combat_begin", [],
   "What do you want to know?", "trainer_talk_combat",[]],
    [anyone,"trainer_combat_pretalk", [],
   "What else do you want to know?", "trainer_talk_combat",[]],

    [anyone|plyr,"trainer_talk_combat", [], "Tell me about defending myself.", "trainer_explain_defense",[]],
    [anyone|plyr,"trainer_talk_combat", [], "Tell me about attacking with weapons.", "trainer_explain_attack",[]],
    [anyone|plyr,"trainer_talk_combat", [], "Tell me about fighting on horseback.", "trainer_explain_horseback",[]],
#    [anyone|plyr,"trainer_talk_combat", [], "Tell me about using ranged weapons.", "trainer_explain_ranged",[]],
#    [anyone|plyr,"trainer_talk_combat", [], "Tell me about weapon types.", "trainer_explain_weapon_types",[]],
    [anyone|plyr,"trainer_talk_combat", [], "I guess I know all the theory I need. Let's talk about something else.", "trainer_pretalk",[]],

   [anyone,"trainer_explain_defense", [], "Good question. The first thing you should know as a fighter is how to defend yourself.\
 Keeping yourself out of harm's way is the first rule of combat, and it is much more important than giving harm to others.\
 Everybody can swing a sword around and hope to cut some flesh, but only those fighters that are experts at defense live to tell of it.",
	"trainer_explain_defense_2",[]],
  [anyone,"trainer_explain_defense_2", [], "Now. Defending yourself is easiest if you are equipped with a shield.\
 Just block with your shield. [Hold down the right mouse button to defend yourself with the shield.] In this state, you will be able to deflect all attacks that come from your front. However, you will still be open to strikes from your sides or your back.", "trainer_explain_defense_3",[]],
  [anyone|plyr,"trainer_explain_defense_3", [], "What if I don't have shield?", "trainer_explain_defense_4",[]],
  [anyone,"trainer_explain_defense_4", [], "Then you will have to use your weapon to block your opponent.\
 This is a bit more difficult than defending with a shield.\
 Defending with a weapon, you can block against only ONE attack direction.\
 That is, you block against either overhead swings, side swings or thrusts.\
 Therefore you must watch your opponent carefully and start to block AFTER he starts his attack.\
 In this way you will be able to block against the direction of his current attack.\
 If you start to block BEFORE he makes his move, he may just attack in another direction than the one you are blocking against and score a hit.", "trainer_combat_pretalk",[]],
  [anyone,"trainer_explain_attack", [], "Good question. Attacking is the best defence, they say.\
 A tactic many fighters find useful is taking an offensive stance and readying your weapon for attack, waiting for the right moment for swinging it.\
 [You can ready your weapon for attack by pressing and holding down the left mouse button.]", "trainer_explain_attack_2",[]],
  [anyone|plyr,"trainer_explain_attack_2", [], "That sounds useful.", "trainer_explain_attack_3",[]],
  [anyone,"trainer_explain_attack_3", [], "It is a good tactic, but remember that, your opponent may see that and take a defensive stance against the direction you are swinging your weapon.\
 If that happens, you must break your attack and quickly attack from another direction\
 [You may cancel your current attack by quickly tapping the right mouse button].", "trainer_explain_attack_4",[]],
  [anyone|plyr,"trainer_explain_attack_4", [], "If my opponent is defending against the direction I am attacking from, I will break and use another direction.", "trainer_explain_attack_5",[]],
  [anyone,"trainer_explain_attack_5", [], "Yes, selecting the direction you swing your weapon is a crucial skill.\
 There are four main directions you may use: right swing, left swing, overhead swing and thrust. You must use each one wisely.\
 [to control your swing direction with default controls, move your mouse in the direction you want to swing from as you press the left mouse button].", "trainer_combat_pretalk",[]],
  [anyone,"trainer_explain_horseback", [], "Very good question. A horse may be a warrior's most powerful weapon in combat.\
 It gives you speed, height, power and initiative. A lot of deadly weapons will become even deadlier on horseback.\
 However you must pay particular attention to horse-mounted enemies couching their lances, as they may take down any opponent in one hit.\
 [To use the couched lance yourself, wield a lance or similar weapon, and speed up your horse without pressing attack or defense buttons.\
 after you reach a speed, you'll lower your lance. Then try to target your enemies by maneuvering your horse.]", "trainer_combat_pretalk",[]],
 
#Crooks

##  [anyone ,"start", [(is_between,"$g_talk_troop",crooks_begin,crooks_end),(eq,"$g_talk_troop_met",0),(eq,"$sneaked_into_town",0),(store_random_in_range, reg2, 2)],
##   "You {reg2?looking for:want} something?:", "crook_intro_1",[]],
##  [anyone|plyr,"crook_intro_1",[],"I am trying to learn my way around the town.", "crook_intro_2",[]],
##  
##  [anyone,"crook_intro_2",[(eq,"$crook_talk_order",0),(val_add,"$crook_talk_order",1),(str_store_troop_name,s1,"$g_talk_troop")],
##"Then you came to the right guy. My name is {s1}, and I know everyone and everything that goes around in this town.\
## Anyone you want to meet, I can arrange it. Anything you need to know, I can find out. For the the right price, of course. Do you have gold?", "crook_intro_2a",[]],
##  [anyone|plyr,"crook_intro_2a",[],"I have gold. Plenty of it.", "crook_intro_2a_1a",[]],
##  [anyone|plyr,"crook_intro_2a",[],"Not really.", "crook_intro_2a_1b",[]],
##  [anyone,"crook_intro_2a_1a",[],"Good. That means you and I will be great friends.", "crook_talk",[]],
##  [anyone,"crook_intro_2a_1b",[],"Then you should look into earning some. Listen to me now, for I'll give you some free advice.\
## The easiest way to make money is to fight in the tournaments and bet on yourself. If you are good, you'll quickly get yourself enough money to get going.", "crook_talk",[]],
##
##  [anyone,"crook_intro_2",[(eq,"$crook_talk_order",1),(val_add,"$crook_talk_order",1),(str_store_troop_name,s1,"$g_talk_troop")],
##"Then you need to go no further. I am {s1}, and I can provide you anything... For the the right price.", "crook_intro_2b",[]],
##  [anyone|plyr,"crook_intro_2b",[],"Are you a dealer?", "crook_intro_2b_1",[]],
##  [anyone,"crook_intro_2b_1",[],"A dealer? Yes. I deal in knowledge... connections.. lies... secrets... Those are what I deal in. Interested?", "crook_talk",[]],
##
##  [anyone,"crook_intro_2",[(eq,"$crook_talk_order",2),(val_add,"$crook_talk_order",1),(str_store_troop_name,s1,"$g_talk_troop")],
##"Then this is your lucky day. Because you are talking to {s1}, and I know every piss-stained brick of this wicked town.\
##I know every person, every dirty little secret. And all that knowledge can be yours. For a price.", "crook_talk",[]],
##
##  [anyone,"crook_intro_2",[(val_add,"$crook_talk_order",1),(str_store_troop_name,s1,"$g_talk_troop")],
## "Then {s1} is at your service {sir/madam}. If you want to know what's really going on in this town, or arrange a meeting in secret, then come to me. I can help you.", "crook_talk",[]],
##
##  [anyone ,"start", [(is_between,"$g_talk_troop",crooks_begin,crooks_end),(eq,"$g_talk_troop_met",0),(eq,"$sneaked_into_town",1),(eq,"$crook_sneak_intro_order",0),(val_add,"$crook_sneak_intro_order",1)],
##   "Good day. {playername} right?", "crook_intro_sneak_1",[]],
##  [anyone|plyr,"crook_intro_sneak_1", [], "You must be mistaken. I'm just a poor pilgrim. I don't answer to that name.", "crook_intro_sneak_2",[]],
##  [anyone,"crook_intro_sneak_2", [(str_store_troop_name,s1,"$g_talk_troop")], "Of course you do. And if the town guards knew you were here, they'd be upon you this minute.\
## But don't worry. Noone knows it is {playername} under that hood. Except me of course. But I am {s1}. It is my business to know things.", "crook_intro_sneak_3",[]],
##  [anyone|plyr,"crook_intro_sneak_3", [], "You won't tip off the guards about my presence?", "crook_intro_sneak_4",[]],
##  [anyone,"crook_intro_sneak_4", [], "What? Of course not! Well, maybe I would, but the new captain of the guards is a dung-eating cheat.\
## I led him to this fugitive, and the man was worth his weight in silver as prize money. But I swear, I didn't see a penny of it.\
## The bastard took it all to himself. So your secret is safe with me.", "crook_intro_sneak_5",[]],
##  [anyone,"crook_intro_sneak_5", [], "Besides, I heard you have a talent for surviving any kind of ordeal.\
## I wouldn't want you to survive this one as well and then come after me with a sword. Ha-hah.", "crook_talk",[]],
##
##
##  [anyone ,"start", [(is_between,"$g_talk_troop",crooks_begin,crooks_end),(eq,"$g_talk_troop_met",0),(eq,"$sneaked_into_town",1),(str_store_troop_name,s1,"$g_talk_troop")],
##   "{s1} is at your service {sir/madam}. If you want to know what's really going on in this town, or arrange a meeting in secret, then come to me. I can help you.", "crook_talk",[]],
##
##  [anyone ,"start", [(is_between,"$g_talk_troop",crooks_begin,crooks_end),(store_character_level, ":cur_level", "trp_player"),(lt,":cur_level",8)],
##   "{You again?/Delighted to see you again my pretty.}", "crook_talk",[]],
##  [anyone ,"start", [(is_between,"$g_talk_troop",crooks_begin,crooks_end)],
##   "I see that you need my services {sir/madam}...", "crook_talk",[]],
##  [anyone ,"crook_pretalk", [],
##   "Is that all?", "crook_talk",[]],


  
##  [anyone|plyr,"crook_talk", [], "I'm looking for a person...", "crook_search_person",[]],
##  [anyone|plyr,"crook_talk", [], "I want you to arrange me a meeting with someone...", "crook_request_meeting",[]],
##  [anyone|plyr,"crook_talk", [], "[Leave]", "close_window",[]],



#  [anyone,"crook_enter_dungeon", [],
#   "Alright but this will cost you 50 denars.", "crook_enter_dungeon_2", []],

#  [anyone|plyr, "crook_enter_dungeon_2", [(store_troop_gold, ":cur_gold", "trp_player"),
#                                            (ge, ":cur_gold", 50)],
#   "TODO: Here it is. 50 denars.", "crook_enter_dungeon_3_1",[(troop_remove_gold, "trp_player", 50)]],

#  [anyone|plyr, "crook_enter_dungeon_2", [(store_troop_gold, ":cur_gold", "trp_player"),
#                                            (ge, ":cur_gold", 50)],
#   "Never mind then.", "crook_pretalk",[]],

#  [anyone|plyr, "crook_enter_dungeon_2", [(store_troop_gold, ":cur_gold", "trp_player"),
#                                            (lt, ":cur_gold", 50)],
#   "TODO: I don't have that much money.", "crook_enter_dungeon_3_2",[]],

#  [anyone,"crook_enter_dungeon_3_1", [],
#   "TODO: There you go.", "close_window", [(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],

#  [anyone,"crook_enter_dungeon_3_2", [],
#   "TODO: Come back later then.", "crook_pretalk",[]],
 

##  [anyone, "crook_request_meeting", [],
##   "Who do you want to meet with?", "crook_request_meeting_2",[]],
##  [anyone|plyr|repeat_for_troops,"crook_request_meeting_2", [(store_encountered_party, ":center_no"),
##                                                             (store_repeat_object, ":troop_no"),
##                                                             (is_between, ":troop_no", heroes_begin, heroes_end),
##                                                             (troop_get_slot, ":cur_center", ":troop_no", slot_troop_cur_center),
##                                                             (call_script, "script_get_troop_attached_party", ":troop_no"),
##                                                             (assign, ":cur_center_2", reg0),
##                                                             (this_or_next|eq, ":cur_center", ":center_no"),
##                                                             (eq, ":cur_center_2", ":center_no"),
##                                                             (neg|party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),#Neglect the ruler of the center
##                                                             (str_store_troop_name, s1, ":troop_no")],
##   "{s1}", "crook_request_meeting_3", [(store_repeat_object, "$selected_troop")]],
##
##  [anyone|plyr,"crook_request_meeting_2", [], "Never mind.", "crook_pretalk", []],
##
##  [anyone,"crook_request_meeting_3", [],
##   "Alright but this will cost you 50 denars.", "crook_request_meeting_4", []],
##
##  [anyone|plyr, "crook_request_meeting_4", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                            (ge, ":cur_gold", 50)],
##   "TODO: Here it is. 50 denars.", "crook_search_person_5_1",[(troop_remove_gold, "trp_player", 50)]],
##
##  [anyone|plyr, "crook_request_meeting_4", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                            (ge, ":cur_gold", 50)],
##   "Never mind then.", "crook_pretalk",[]],
##
##  [anyone|plyr, "crook_request_meeting_4", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                            (lt, ":cur_gold", 50)],
##   "TODO: I don't have that much money.", "crook_search_person_5_2",[]],
##
##  [anyone, "crook_search_person_5_1", [],
##   "TODO: Ok.", "close_window",[(party_get_slot, ":town_alley", "$g_encountered_party", slot_town_alley),
##                                (modify_visitors_at_site,":town_alley"),(reset_visitors),
##                                (set_visitor,0,"trp_player"),
##                                (set_visitor,17,"$selected_troop"),
##                                (set_jump_mission,"mt_conversation_encounter"),
##                                (jump_to_scene,":town_alley"),
##                                (assign, "$talk_context", tc_back_alley),
##                                (change_screen_map_conversation, "$selected_troop")]],
##
##  [anyone, "crook_search_person_5_2", [],
##   "TODO: Come back later then.", "crook_pretalk",[]],
##
##  [anyone, "crook_search_person", [],
##   "TODO: Who are you searching for?", "crook_search_person_2",[]],
##  [anyone|plyr|repeat_for_factions,"crook_search_person_2", [(store_repeat_object, ":faction_no"),
##                                                             (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
##                                                             (str_store_faction_name, s1, ":faction_no")],
##   "TODO: I'm looking for a {s1}.", "crook_search_person_3", [(store_repeat_object, "$selected_faction")]],
##
##  [anyone|plyr,"crook_search_person_2", [], "Never mind.", "crook_pretalk", []],
##
##  
##  [anyone, "crook_search_person_3", [],
##   "TODO: Who?", "crook_search_person_4",[]],
##  
##  [anyone|plyr|repeat_for_troops,"crook_search_person_4", [(store_repeat_object, ":troop_no"),
##                                                           (is_between, ":troop_no", heroes_begin, heroes_end),
##                                                           (store_troop_faction, ":faction_no", ":troop_no"),
##                                                           (eq, ":faction_no", "$selected_faction"),
##                                                           (str_store_troop_name, s1, ":troop_no")],
##   "{s1}", "crook_search_person_5", [(store_repeat_object, "$selected_troop")]],
##
##  [anyone|plyr,"crook_search_person_4", [], "Never mind.", "crook_pretalk", []],
##
##  [anyone, "crook_search_person_5", [(call_script, "script_get_information_about_troops_position", "$selected_troop", 0),
##                                     (eq, reg0, 1),
##                                     (str_store_troop_name, s1, "$selected_troop")],
##   "TODO: I know where {s1} is at the moment, but hearing it will cost you 50 denars.", "crook_search_person_6",[]],
##
##  [anyone, "crook_search_person_5", [],
##   "TODO: Sorry I don't know anything.", "crook_pretalk",[]],
##
##  [anyone|plyr, "crook_search_person_6", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                          (ge, ":cur_gold", 50)],
##   "TODO: Here it is. 50 denars.", "crook_search_person_7_1",[(troop_remove_gold, "trp_player", 50)]],
##
##  [anyone|plyr, "crook_search_person_6", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                          (ge, ":cur_gold", 50)],
##   "Never mind then.", "crook_pretalk",[]],
##
##  [anyone|plyr, "crook_search_person_6", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                          (lt, ":cur_gold", 50)],
##   "TODO: I don't have that much money.", "crook_search_person_7_2",[]],
##
##  [anyone, "crook_search_person_7_1", [(call_script, "script_get_information_about_troops_position", "$selected_troop", 0)],
##   "{s1}", "crook_pretalk",[]],
##
##  [anyone, "crook_search_person_7_2", [],
##   "TODO: Come back later then.", "crook_pretalk",[]],
##  

#Mayor talk (town elder)

  [anyone ,"start", [(is_between,"$g_talk_troop",mayors_begin,mayors_end),(eq,"$g_talk_troop_met",0),
                     (this_or_next|eq, "$players_kingdom", "$g_encountered_party_faction"),
                     (             eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),],
   "Good day, my lord.", "mayor_begin",[]],
  [anyone ,"start", [(is_between,"$g_talk_troop",mayors_begin,mayors_end),(eq,"$g_talk_troop_met",0),
                     (str_store_party_name, s9, "$current_town")],
   "Hello stranger, you seem to be new to {s9}. I am the guild master of the town.", "mayor_talk",[]],
  
  [anyone ,"start", [(is_between,"$g_talk_troop",mayors_begin,mayors_end)],
   "Good day, {playername}.", "mayor_begin",
   [
     #Delete last offered quest if peace is formed.
     (try_begin),
       (eq, "$merchant_offered_quest", "qst_persuade_lords_to_make_peace"),
       (party_get_slot, ":target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
       (party_get_slot, ":object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
       (store_relation, ":reln", ":target_faction", ":object_faction"),
       (ge, ":reln", 0),
       (assign, "$merchant_quest_last_offerer", -1),
       (assign, "$merchant_offered_quest", -1),
     (try_end),
     ]],


  [anyone,"mayor_begin", [(check_quest_active, "qst_persuade_lords_to_make_peace"),
                          (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_succeeded, "qst_persuade_lords_to_make_peace"),
                          (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
                          (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
                          (val_mul, ":quest_target_troop", -1),
                          (val_mul, ":quest_object_troop", -1),
                          (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
                          (quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
                          (str_store_troop_name, s12, ":quest_target_troop"),
                          (str_store_troop_name, s13, ":quest_object_troop"),
                          (str_store_faction_name, s14, ":quest_target_faction"),
                          (str_store_faction_name, s15, ":quest_object_faction"),
                          (str_store_party_name, s19, "$current_town"),
                         ],
   "{playername}, it was an incredible feat to get {s14} and {s15} make peace, and you made it happen.\
 Your involvement has not only saved our town from disaster, but it has also saved thousands of lives, and put an end to all the grief this bitter war has caused.\
 As the townspeople of {s19}, know that we'll be good on our word, and we are ready to pay the {reg12} denars we promised.", "lord_persuade_lords_to_make_peace_completed",
   [#(quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
    #(quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
    # commented by GA, no peace in TLD
	#Forcing 2 factions to make peace within 72 hours.
#    (assign, "$g_force_peace_faction_1", ":quest_target_faction"),
#    (assign, "$g_force_peace_faction_2", ":quest_object_faction"),
    (quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
    (assign, reg12, ":quest_reward"),
    #TODO: Change these values
    (add_xp_as_reward, 4000),
    ]],


  [anyone|plyr,"lord_persuade_lords_to_make_peace_completed", [],
   "Thank you. Let me have the money.", "lord_persuade_lords_to_make_peace_pay",[]],
  [anyone|plyr,"lord_persuade_lords_to_make_peace_completed", [],
   "No need for a payment. I only did what was right.", "lord_persuade_lords_to_make_peace_no_pay",[]],

  [anyone ,"lord_persuade_lords_to_make_peace_pay", [],
   "Oh, yes, of course. We had already got the money for you.\
 Here, please accept these {reg12} denars together with our most sincere thanks.\
 Me and the people of our town will not forget your help.", "close_window",
   [(quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
    (call_script, "script_troop_add_gold","trp_player",":quest_reward"),
    (call_script, "script_change_player_relation_with_center", "$current_town", 5),
    (call_script, "script_end_quest", "qst_persuade_lords_to_make_peace"),
    (quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
    (assign, reg12, ":quest_reward")
    ]],

  [anyone ,"lord_persuade_lords_to_make_peace_no_pay", [],
   "You are indeed an extraordinary person, {sir/madame}, and it is an honour for me to have known you.\
 You not only did what was impossible and put an end to this terrible war, but you won't even accept a reward for it.\
 Very well, I will not insist on the matter, but please know that you will have our eternal respect and gratitude.", "close_window",
   [
    (call_script, "script_change_player_honor", 3),
    (call_script, "script_change_player_relation_with_center", "$current_town", 8),
    (call_script, "script_end_quest", "qst_persuade_lords_to_make_peace"),
    ]],

  [anyone,"mayor_begin", [(check_quest_active, "qst_deal_with_night_bandits"),
                          (quest_slot_eq, "qst_deal_with_night_bandits", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_succeeded, "qst_deal_with_night_bandits"),
                         ],
   "Very nice work, {playername}, you made short work of those lawless curs.\
 Thank you kindly for all your help, and please accept this bounty of 150 denars.", "lord_deal_with_night_bandits_completed",
   [
     (add_xp_as_reward,200),
     (call_script, "script_troop_add_gold","trp_player", 150),
     (call_script, "script_change_player_relation_with_center", "$current_town", 1),
     (call_script, "script_end_quest", "qst_deal_with_night_bandits"),
    ]],


  [anyone|plyr,"lord_deal_with_night_bandits_completed", [],
   "It was my pleasure, {s65}.", "close_window",[]],

# Ryan BEGIN
  [anyone,"mayor_begin", [(check_quest_active, "qst_deal_with_looters"),
                          (quest_slot_eq, "qst_deal_with_looters", slot_quest_giver_troop, "$g_talk_troop"),
                         ],
   "Ah, {playername}. Have you any progress to report?", "mayor_looters_quest_response",
   [
    ]],

  [anyone|plyr,"mayor_looters_quest_response",
   [
     (store_num_parties_destroyed_by_player, ":num_looters_destroyed", "pt_looters"),
     (party_template_get_slot,":previous_looters_destroyed","pt_looters",slot_party_template_num_killed),
     (val_sub,":num_looters_destroyed",":previous_looters_destroyed"),
     (quest_get_slot,":looters_paid_for","qst_deal_with_looters",slot_quest_current_state),
     (lt,":looters_paid_for",":num_looters_destroyed"),
     ],
   "I've killed some looters.", "mayor_looters_quest_destroyed",[]],
  [anyone|plyr,"mayor_looters_quest_response", [(eq,1,0)
  ],
   "I've brought you some goods.", "mayor_looters_quest_goods",[]],
  [anyone|plyr,"mayor_looters_quest_response", [
  ],
   "Not yet, sir. Farewell.", "close_window",[]],

  [anyone,"mayor_looters_quest_destroyed", [],
   "Aye, my scouts saw the whole thing. That should make anyone else think twice before turning outlaw!\
 The bounty is 40 denars for every band, so that makes {reg1} in total. Here is your money, as promised.",
   "mayor_looters_quest_destroyed_2",[
      (store_num_parties_destroyed_by_player, ":num_looters_destroyed", "pt_looters"),
      (party_template_get_slot,":previous_looters_destroyed","pt_looters",slot_party_template_num_killed),
      (val_sub,":num_looters_destroyed",":previous_looters_destroyed"),
      (quest_get_slot,":looters_paid_for","qst_deal_with_looters",slot_quest_current_state),
      (store_sub,":looter_bounty",":num_looters_destroyed",":looters_paid_for"),
      (val_mul,":looter_bounty",40),
      (assign,reg1,":looter_bounty"),
      (call_script, "script_troop_add_gold","trp_player",":looter_bounty"),
      (assign,":looters_paid_for",":num_looters_destroyed"),
      (quest_set_slot,"qst_deal_with_looters",slot_quest_current_state,":looters_paid_for"),
      ]],
  [anyone,"mayor_looters_quest_destroyed_2", [
      (quest_get_slot,":total_looters","qst_deal_with_looters",slot_quest_target_amount),
      (quest_slot_ge,"qst_deal_with_looters",slot_quest_current_state,":total_looters"), # looters paid for >= total looters
      (quest_get_slot,":xp_reward","qst_deal_with_looters",slot_quest_xp_reward),
      (quest_get_slot,":gold_reward","qst_deal_with_looters",slot_quest_gold_reward),
      (add_xp_as_reward, ":xp_reward"),
      (call_script, "script_troop_add_gold","trp_player",":gold_reward"),
      (call_script, "script_change_troop_renown", "trp_player", 1),
      (call_script, "script_change_player_relation_with_center", "$current_town", 5),
      (call_script, "script_end_quest", "qst_deal_with_looters"),
      (try_for_parties, ":cur_party_no"),
        (party_get_template_id, ":cur_party_template", ":cur_party_no"),
        (eq, ":cur_party_template", "pt_looters"),
        (party_set_flags, ":cur_party_no", pf_quest_party, 0),
      (try_end),
  ],
   "And that's not the only good news! Thanks to you, the looters have ceased to be a threat. We've not had a single attack reported for some time now.\
   If there are any of them left, they've either run off or gone deep into hiding. That's good for business,\
   and what's good for business is good for the town!\
   I think that concludes our arrangement, {playername}. Please accept this silver as a token of my gratitude. Thank you, and farewell.",
   "close_window",[
      ]],
  [anyone,"mayor_looters_quest_destroyed_2", [],
   "Anything else you need?",
   "mayor_looters_quest_response",[
      ]],

  [anyone,"mayor_looters_quest_goods", [
      (quest_get_slot,reg1,"qst_deal_with_looters",slot_quest_target_item),
  ],
   "Hah, I knew I could count on you! Just tell me which item to take from your baggage, and I'll send some men to collect it.\
 I still need {reg1} denars' worth of goods.",
   "mayor_looters_quest_goods_response",[
      ]],
  [anyone|plyr|repeat_for_100,"mayor_looters_quest_goods_response", [
      (store_repeat_object,":goods"),
      (val_add,":goods",trade_goods_begin),
      (is_between,":goods",trade_goods_begin,trade_goods_end),
      (player_has_item,":goods"),
      (str_store_item_name,s5,":goods"),
  ],
   "{s5}.", "mayor_looters_quest_goods_2",[
      (store_repeat_object,":goods"),
      (val_add,":goods",trade_goods_begin),
      (troop_remove_items,"trp_player",":goods",1),
      (assign,":value",reg0),
      (call_script, "script_troop_add_gold","trp_player",":value"),
      (quest_get_slot,":gold_num","qst_deal_with_looters",slot_quest_target_item),
      (val_sub,":gold_num",":value"),
      (quest_set_slot,"qst_deal_with_looters",slot_quest_target_item,":gold_num"),
      (str_store_item_name,s6,":goods"),
   ]],
  [anyone|plyr,"mayor_looters_quest_goods_response", [
  ],
   "Nothing at the moment, sir.", "mayor_looters_quest_goods_3",[]],

  [anyone,"mayor_looters_quest_goods_3", [
  ],
   "Anything else you need?",
   "mayor_looters_quest_response",[
      ]],

  [anyone,"mayor_looters_quest_goods_2", [
      (quest_slot_ge,"qst_deal_with_looters",slot_quest_target_item,1),
      (quest_get_slot,reg1,"qst_deal_with_looters",slot_quest_target_item),
  ],
   "Excellent, here is the money for your {s6}. Do you have any more goods to give me? I still need {reg1} denars' worth of goods.",
   "mayor_looters_quest_goods_response",[
      ]],
  [anyone,"mayor_looters_quest_goods_2", [
      (neg|quest_slot_ge,"qst_deal_with_looters",slot_quest_target_item,1),
      (quest_get_slot,":xp_reward","qst_deal_with_looters",slot_quest_xp_reward),
      (quest_get_slot,":gold_reward","qst_deal_with_looters",slot_quest_gold_reward),
      (add_xp_as_reward, ":xp_reward"),
      (call_script, "script_troop_add_gold","trp_player",":gold_reward"),
#      (call_script, "script_change_troop_renown", "trp_player", 1),
      (call_script, "script_change_player_relation_with_center", "$current_town", 3),
      (call_script, "script_end_quest", "qst_deal_with_looters"),
      (try_for_parties, ":cur_party_no"),
        (party_get_template_id, ":cur_party_template", ":cur_party_no"),
        (eq, ":cur_party_template", "pt_looters"),
        (party_set_flags, ":cur_party_no", pf_quest_party, 0),
      (try_end),
  ],
   "Well done, {playername}, that's the last of the goods I need. Here is the money for your {s6}, and a small bonus for helping me out.\
 I'm afraid I won't be paying for any more goods, nor bounties on looters, but you're welcome to keep hunting the bastards if any remain.\
 Thank you for your help, I won't forget it.",
   "close_window",[
      ]],
# Ryan END



  [anyone,"mayor_begin", [(check_quest_active, "qst_move_cattle_herd"),
                          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_succeeded, "qst_move_cattle_herd"),
                          ],
   "Good to see you again {playername}. I have heard that you have delivered the cattle successfully.\
 I will tell the merchants how reliable you are.\
 And here is your pay, {reg8} denars.", "close_window",
   [(quest_get_slot, ":quest_gold_reward", "qst_move_cattle_herd", slot_quest_gold_reward),
    (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    (store_div, ":xp_reward", ":quest_gold_reward", 3),
    (add_xp_as_reward, ":xp_reward"),
    (call_script, "script_change_troop_renown", "trp_player", 1),
    (call_script, "script_change_player_relation_with_center", "$current_town", 3),    
    (call_script, "script_end_quest", "qst_move_cattle_herd"),
    (assign, reg8, ":quest_gold_reward"),
    ]],
  
  [anyone,"mayor_begin", [(check_quest_active, "qst_move_cattle_herd"),
                          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_failed, "qst_move_cattle_herd"),
                          ],
   "I heard that you have lost the cattle herd on your way to {s9}.\
 I had a very difficult time explaining your failure to the owner of that herd, {sir/madam}.\
 Do you have anything to say?", "move_cattle_herd_failed",
   []],

  [anyone|plyr ,"move_cattle_herd_failed", [],
   "I am sorry. But I was attacked on the way.", "move_cattle_herd_failed_2",[]],
  [anyone|plyr ,"move_cattle_herd_failed", [],
   "I am sorry. The stupid animals wandered off during the night.", "move_cattle_herd_failed_2",[]],

  [anyone,"move_cattle_herd_failed_2", [],
   "Well, it was your responsibility to deliver that herd safely, no matter what.\
 You should know that the owner of the herd demanded to be compensated for his loss, and I had to pay him 1000 denars.\
 So you now owe me that money.", "merchant_ask_for_debts",
   [(assign, "$debt_to_merchants_guild", 1000),
    (call_script, "script_end_quest", "qst_move_cattle_herd"),]],

  [anyone,"mayor_begin", [(check_quest_active, "qst_kidnapped_girl"),
                          (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 4),
                          (quest_slot_eq, "qst_kidnapped_girl", slot_quest_giver_troop, "$g_talk_troop"),
                          ],
   "Dear {playername}. I am in your debt for bringing back my friend's daughter.\
  Please take these {reg8} denars that I promised you.\
  My friend wished he could give more but paying that ransom brought him to his knees.", "close_window",
   [(quest_get_slot, ":quest_gold_reward", "qst_kidnapped_girl", slot_quest_gold_reward),
    (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    (assign, reg8, ":quest_gold_reward"),
    (assign, ":xp_reward", ":quest_gold_reward"),
    (val_mul, ":xp_reward", 2),
    (val_add, ":xp_reward", 100),
    (add_xp_as_reward, ":xp_reward"),
    (call_script, "script_change_troop_renown", "trp_player", 3),
    (call_script, "script_change_player_relation_with_center", "$current_town", 2),    
    (call_script, "script_end_quest", "qst_kidnapped_girl"),
    ]],
  
  [anyone,"mayor_begin", [(check_quest_active, "qst_troublesome_bandits"),
                          (check_quest_succeeded, "qst_troublesome_bandits"),
                          (quest_slot_eq, "qst_troublesome_bandits", slot_quest_giver_troop, "$g_talk_troop"),
                          ],
   "I have heard about your deeds. You have given those bandits the punishment they deserved.\
 You are really as good as they say.\
 Here is your reward: {reg5} denars.\
 I would like to give more but those bandits almost brought me to bankruptcy.",
   "mayor_friendly_pretalk", [(quest_get_slot, ":quest_gold_reward", "qst_troublesome_bandits", slot_quest_gold_reward),
                              (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
                              (assign, ":xp_reward", ":quest_gold_reward"),
                              (val_mul, ":xp_reward", 7),
                              (add_xp_as_reward, ":xp_reward"),
                              (call_script, "script_change_player_relation_with_center", "$current_town", 2),
                              (call_script, "script_change_troop_renown", "trp_player", 3),
                              (call_script, "script_end_quest", "qst_troublesome_bandits"),
                              (assign, reg5, ":quest_gold_reward"),
                              ]],

  [anyone,"mayor_begin", [(ge, "$debt_to_merchants_guild", 50)],
   "According to my accounts, you owe the merchants guild {reg1} denars.\
 I'd better collect that now.", "merchant_ask_for_debts",[(assign,reg(1),"$debt_to_merchants_guild")]],
  [anyone|plyr,"merchant_ask_for_debts", [[store_troop_gold,reg(5),"trp_player"],[ge,reg(5),"$debt_to_merchants_guild"]],
   "Alright. I'll pay my debt to you.", "merchant_debts_paid",[[troop_remove_gold, "trp_player","$debt_to_merchants_guild"],
                                                                [assign,"$debt_to_merchants_guild",0]]],
  [anyone, "merchant_debts_paid", [], "Excellent. I'll let my fellow merchants know that you are clear of any debts.", "mayor_pretalk",[]],

  [anyone|plyr, "merchant_ask_for_debts", [], "I'm afraid I can't pay that sum now.", "merchant_debts_not_paid",[]],
  [anyone, "merchant_debts_not_paid", [(assign,reg(1),"$debt_to_merchants_guild")], "In that case, I am afraid, I can't deal with you. Guild rules...\
 Come back when you can pay the {reg1} denars.\
 And know that we'll be charging an interest to your debt.\
 So the sooner you pay it, the better.", "close_window",[]],


  [anyone,"mayor_begin", [], "What can I do for you?", "mayor_talk", []],
  [anyone,"mayor_friendly_pretalk", [], "Now... What else may I do for you?", "mayor_talk",[]],
  [anyone,"mayor_pretalk", [], "Yes?", "mayor_talk",[]],
  
  [anyone|plyr,"mayor_talk", [], "Can you tell me about what you do?", "mayor_info_begin",[]],

  [anyone|plyr,"mayor_talk", [(store_partner_quest, ":partner_quest"),
                              (lt, ":partner_quest", 0),
                              (neq, "$merchant_quest_last_offerer", "$g_talk_troop")],
   "Do you happen to have a job for me?", "merchant_quest_requested",[
     (assign,"$merchant_quest_last_offerer", "$g_talk_troop"),
     (call_script, "script_get_random_quest", "$g_talk_troop"),
     (assign, "$random_merchant_quest_no", reg0),
     (assign,"$merchant_offered_quest","$random_merchant_quest_no"),
     ]],
  [anyone|plyr,"mayor_talk", [(store_partner_quest, ":partner_quest"),
                              (lt, ":partner_quest", 0),
                              (eq,"$merchant_quest_last_offerer", "$g_talk_troop"),
                              (ge,"$merchant_offered_quest",0)
                              ],
   "About that job you offered me...", "merchant_quest_last_offered_job",[]],
  [anyone|plyr,"mayor_talk", [(store_partner_quest,reg(2)),(ge,reg(2),0)],
   "About the job you gave me...", "merchant_quest_about_job",[]],

  [anyone|plyr,"mayor_talk", [], "[Leave]", "close_window",[]],

  [anyone, "mayor_info_begin", [(str_store_party_name, s9, "$current_town")],
   "I am the guildmaster of {s9}. You can say I am the leader of the good people of {s9}.\
 I can help you find a job if you are looking for some honest work.", "mayor_info_talk",[(assign, "$mayor_info_lord_told",0)]],

  [anyone|plyr,"mayor_info_talk",[(eq, "$mayor_info_lord_told",0)], "Who rules this town?", "mayor_info_lord",[]],
  [anyone, "mayor_info_lord", [(party_get_slot, ":town_lord","$current_town",slot_town_lord),(str_store_troop_name, s10, ":town_lord")],
   "Our town's lord and protector is {s10}. He owns the castle and sometimes resides there, and collects taxes from the town.\
 However we regulate ourselves in most of the matters that concern ourselves.\
 As the town's guildmaster I have the authority to decide those things.", "mayor_info_talk",[(assign, "$mayor_info_lord_told",1)]],
  
  [anyone|plyr,"mayor_info_talk",[], "That's all I need to know. Thanks.", "mayor_pretalk",[]],
  

  [anyone,"merchant_quest_about_job", [], "What about it?", "merchant_quest_about_job_2",[]],
  [anyone|plyr,"merchant_quest_about_job_2", [], "What if I can't finish it?", "merchant_quest_what_if_fail",[]],
  [anyone|plyr,"merchant_quest_about_job_2", [], "Well, I'm still working on it.", "merchant_quest_about_job_working",[]],
  [anyone,"merchant_quest_about_job_working", [], "Good. I'm sure you will handle it.", "mayor_pretalk",[]],


  [anyone,"merchant_quest_last_offered_job", [], "Eh, you want to reconsider that. Good...", "merchant_quest_brief",
   [[assign,"$random_merchant_quest_no","$merchant_offered_quest"]]],


  [anyone,"merchant_quest_what_if_fail", [(store_partner_quest,":partner_quest"),(eq,":partner_quest","qst_deliver_wine")],
   "I hope you don't fail. In that case, I'll have to ask for the price of the cargo you were carrying.", "mayor_pretalk",[]],
  [anyone,"merchant_quest_what_if_fail", [], "Well, just do your best to finish it.", "mayor_pretalk",[]],

  [anyone,"merchant_quest_taken", [], "Excellent. I am counting on you then. Good luck.", "mayor_pretalk",
   []],
  [anyone,"merchant_quest_stall", [], "Well, the job will be available for a few more days I guess. Tell me if you decide to take it.", "mayor_pretalk",[]],

###################################################################3
# Random Merchant quests....
##############################

# Ryan BEGIN
  # deal with looters
  [anyone,"merchant_quest_requested",
   [
     (eq,"$random_merchant_quest_no","qst_deal_with_looters"),
     ],
   "Well, you look able enough. I think I might have something you could do.", "merchant_quest_brief", []],

  [anyone,"merchant_quest_brief",
   [
     (eq,"$random_merchant_quest_no","qst_deal_with_looters"),
     (try_begin),
       (party_slot_eq,"$g_encountered_party",slot_party_type,spt_town),
       (str_store_string,s5,"@town"),
     (else_try),
       (party_slot_eq,"$g_encountered_party",slot_party_type,spt_village),
       (str_store_string,s5,"@village"),
     (try_end),
     ],
   "We've had some fighting near the {s5} lately, with all the chaos that comes with it,\
 and that's led some of our less upstanding locals to try and make their fortune out of looting the shops and farms during the confusion.\
 A lot of valuable goods were taken. I need somebody to teach those bastards a lesson.\
 Sound like your kind of work?", "merchant_quest_looters_choice", []],

  [anyone|plyr,"merchant_quest_looters_choice", [], "Aye, I'll do it.", "merchant_quest_looters_brief", []],

  [anyone|plyr,"merchant_quest_looters_choice", [], "I'm afraid I can't take the job at the moment.", "merchant_quest_stall",[]],

  [anyone,"merchant_quest_looters_brief", [
   (try_begin),
   (party_slot_eq,"$g_encountered_party",slot_party_type,spt_town),
   (str_store_string,s5,"@town"),
   (else_try),
   (party_slot_eq,"$g_encountered_party",slot_party_type,spt_village),
   (str_store_string,s5,"@village"),
   (try_end),

#     (party_get_slot,":merchant","$current_town",slot_town_merchant),
#     (troop_clear_inventory,":merchant"),
   (store_random_in_range,":random_num_looters",3,7),
   (quest_set_slot,"qst_deal_with_looters",slot_quest_target_amount,":random_num_looters"),
   (try_for_range,":unused",0,":random_num_looters"),
     (store_random_in_range,":random_radius",5,14),
     (set_spawn_radius,":random_radius"),
     (spawn_around_party,"$g_encountered_party","pt_looters"),
     (party_set_flags, reg0, pf_quest_party, 1),
   (try_end),
   (str_store_troop_name_link, s9, "$g_talk_troop"),
   (str_store_party_name_link, s13, "$g_encountered_party"),
   (str_store_party_name, s4, "$g_encountered_party"),
   (setup_quest_text, "qst_deal_with_looters"),
   (str_store_string, s2, "@The Guildmaster of {s13} has asked you to deal with looters in the surrounding countryside."),
   (call_script, "script_start_quest", "qst_deal_with_looters", "$g_talk_troop"),
   (assign, "$g_leave_encounter",1),
  ],
   "Excellent! You'll find the looters roaming around the countryside, probably trying to rob more good people.\
 Kill or capture the bastards, I don't care what you do with them.\
 I'll pay you a bounty of 40 denars on every band of looters you destroy,\
 until all the looters are dealt with.", "close_window",
   []],
# Ryan END

  # deliver wine:
  [anyone,"merchant_quest_requested", [(eq,"$random_merchant_quest_no","qst_deliver_wine"),], "You're looking for a job?\
 Actually I was looking for someone to deliver some {s4}.\
 Perhaps you can do that...", "merchant_quest_brief",
   [(quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (str_store_item_name, s4, ":quest_target_item"),
    ]],

  [anyone,"merchant_quest_brief", [(eq,"$random_merchant_quest_no","qst_deliver_wine")],
   "I have a cargo of {s6} that needs to be delivered to the tavern in {s4}.\
 If you can take {reg5} units of {s6} to {s4} in 7 days, you may earn {reg8} denars.\
 What do you say?", "merchant_quest_brief_deliver_wine",
   [(quest_get_slot, reg5, "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, reg8, "qst_deliver_wine", slot_quest_gold_reward),
    (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_target_center", "qst_deliver_wine", slot_quest_target_center),
    (str_store_troop_name, s9, "$g_talk_troop"),
    (str_store_party_name_link, s3, "$g_encountered_party"),
    (str_store_party_name_link, s4, ":quest_target_center"),
    (str_store_item_name, s6, ":quest_target_item"),
    (setup_quest_text,"qst_deliver_wine"),
    (str_store_string, s2, "@{s9} of {s3} asked you to deliver {reg5} units of {s6} to the tavern in {s4} in 7 days."),
    #s2 should not be changed until the decision is made
   ]],
  
  [anyone|plyr,"merchant_quest_brief_deliver_wine", [(store_free_inventory_capacity,":capacity"),
                                                     (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
                                                     (ge, ":capacity", ":quest_target_amount"),
                                                     ],
      "Alright. I will make the delivery.", "merchant_quest_taken",
   [(quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (troop_add_items, "trp_player", ":quest_target_item",":quest_target_amount"),
    (call_script, "script_start_quest", "qst_deliver_wine", "$g_talk_troop"),
    ]],

  [anyone|plyr,"merchant_quest_brief_deliver_wine", [], "I am afraid I can't carry all that cargo now.", "merchant_quest_stall",[]],

#escort merchant caravan:
  [anyone,"merchant_quest_requested", [(eq,"$random_merchant_quest_no","qst_escort_merchant_caravan")], "You're looking for a job?\
 Actually I was looking for someone to escort a caravan.\
 Perhaps you can do that...", "merchant_quest_brief",
   []],

  [anyone,"merchant_quest_brief", [(eq, "$random_merchant_quest_no", "qst_escort_merchant_caravan")],
   "I am going to send a caravan of goods to {s8}.\
 However with all those bandits and deserters on the roads, I don't want to send them out without an escort.\
 If you can lead that caravan to {s8} in 15 days, you will earn {reg8} denars.\
 Of course your party needs to be at least {reg4} strong to offer them any protection.", "escort_merchant_caravan_quest_brief",
   [(quest_get_slot, reg8, "qst_escort_merchant_caravan", slot_quest_gold_reward),
    (quest_get_slot, reg4, "qst_escort_merchant_caravan", slot_quest_target_amount),
    (quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
    (str_store_party_name, s8, ":quest_target_center"),
   ]],
  
  [anyone|plyr,"escort_merchant_caravan_quest_brief", [(store_party_size_wo_prisoners, ":party_size", "p_main_party"),
                                                       (quest_get_slot, ":quest_target_amount", "qst_escort_merchant_caravan", slot_quest_target_amount),
                                                       (ge,":party_size",":quest_target_amount"),
                                                       ],
   "Alright. I will escort the caravan.", "merchant_quest_taken",
   [(quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
    (set_spawn_radius, 1),
    (spawn_around_party,"$g_encountered_party","pt_merchant_caravan"),
    (assign, ":quest_target_party", reg0),
    (party_set_ai_behavior, ":quest_target_party", ai_bhvr_track_party),
    (party_set_ai_object, ":quest_target_party", "p_main_party"),
    (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
    (quest_set_slot, "qst_escort_merchant_caravan", slot_quest_target_party, ":quest_target_party"),
    (quest_set_slot, "qst_escort_merchant_caravan", slot_quest_current_state, 0),
    (str_store_party_name_link, s8, ":quest_target_center"),
    (setup_quest_text, "qst_escort_merchant_caravan"),
    (str_store_string, s2, "@Escort the merchant caravan to the town of {s8}."),
    (call_script, "script_start_quest", "qst_escort_merchant_caravan", "$g_talk_troop"),
    ]],
  
  [anyone|plyr,"escort_merchant_caravan_quest_brief", [(store_party_size_wo_prisoners, ":party_size", "p_main_party"),
                                                       (quest_get_slot, ":quest_target_amount", "qst_escort_merchant_caravan", slot_quest_target_amount),
                                                       (lt,":party_size",":quest_target_amount"),],
   "I am afraid I don't have that many soldiers with me.", "merchant_quest_stall",[]],
  [anyone|plyr,"escort_merchant_caravan_quest_brief", [(store_party_size_wo_prisoners, ":party_size", "p_main_party"),
                                                       (quest_get_slot, ":quest_target_amount", "qst_escort_merchant_caravan", slot_quest_target_amount),
                                                       (ge,":party_size",":quest_target_amount"),],
   "Sorry. I can't do that right now", "merchant_quest_stall",[]],

  [party_tpl|pt_merchant_caravan,"start", [(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                                           (eq,"$g_encountered_party",":quest_target_party"),
                                           (quest_slot_eq,"qst_escort_merchant_caravan", slot_quest_current_state, 2),
                                           ],
   "We can cover the rest of the way ourselves. Thanks.", "close_window",[(assign, "$g_leave_encounter", 1)]],
  
  [party_tpl|pt_merchant_caravan,"start", [(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                                           (eq,"$g_encountered_party",":quest_target_party"),
                                           (quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
                                           (store_distance_to_party_from_party, ":dist", ":quest_target_center",":quest_target_party"),
                                           (lt,":dist",4),
                                           (quest_slot_eq, "qst_escort_merchant_caravan", slot_quest_current_state, 1),
                                           ],
   "Well, we have almost reached {s21}. We can cover the rest of the way ourselves.\
 Here's your pay... {reg14} denars.\
 Thanks for escorting us. Good luck.", "close_window",[(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                                                       (quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
                                                       (quest_get_slot, ":quest_giver_center", "qst_escort_merchant_caravan", slot_quest_giver_center),
                                                       (quest_get_slot, ":quest_gold_reward", "qst_escort_merchant_caravan", slot_quest_gold_reward),
                                                       (party_set_ai_behavior, ":quest_target_party", ai_bhvr_travel_to_party),
                                                       (party_set_ai_object, ":quest_target_party", ":quest_target_center"),
                                                       (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
                                                       (str_store_party_name, s21, ":quest_target_center"),
                                                       (call_script, "script_change_player_relation_with_center", ":quest_giver_center", 1),
                                                       (call_script, "script_end_quest","qst_escort_merchant_caravan"),
                                                       (quest_set_slot, "qst_escort_merchant_caravan", slot_quest_current_state, 2),
                                                       (call_script, "script_troop_add_gold", "trp_player",":quest_gold_reward"),
                                                       (assign, ":xp_reward", ":quest_gold_reward"),
                                                       (val_mul, ":xp_reward", 5),
                                                       (val_add, ":xp_reward", 100),
                                                       (add_xp_as_reward, ":xp_reward"),
                                                       (call_script, "script_change_troop_renown", "trp_player", 2),
                                                       (assign, reg14, ":quest_gold_reward"),
                                                       (assign, "$g_leave_encounter", 1),
                                                       ]],
  
  [party_tpl|pt_merchant_caravan,"start", [(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                                           (eq,"$g_encountered_party",":quest_target_party"),
                                           (quest_slot_eq, "qst_escort_merchant_caravan", slot_quest_current_state, 0),
                                           ],
   "Greetings. You must be our escort, right?", "merchant_caravan_intro_1",[(quest_set_slot, "qst_escort_merchant_caravan", slot_quest_current_state, 1),]],
  
  [anyone|plyr,"merchant_caravan_intro_1", [], "Yes. My name is {playername}. I will lead you to {s1}.",
   "merchant_caravan_intro_2",[(quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
                               (str_store_party_name, s1, ":quest_target_center"),
                               ]],
  
  [anyone,"merchant_caravan_intro_2", [], "Well, It is good to know we won't travel alone. What do you want us to do now?", "escort_merchant_caravan_talk",[]],
  
  [party_tpl|pt_merchant_caravan,"start", [(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                                           (eq, "$g_encountered_party", ":quest_target_party"),
                                           ],
   "Eh. We've made it this far... What do you want us to do?", "escort_merchant_caravan_talk",[]],
  
  [anyone|plyr,"escort_merchant_caravan_talk", [], "You follow my lead. I'll take you through a safe route.", "merchant_caravan_follow_lead",[]],
  [anyone,"merchant_caravan_follow_lead", [], "Alright. We'll be right behind you.", "close_window",[(assign, "$escort_merchant_caravan_mode", 0),
                                                                                                     (assign, "$g_leave_encounter", 1)]],
  [anyone|plyr,"escort_merchant_caravan_talk", [], "You stay here for a while. I'll go ahead and check the road.", "merchant_caravan_stay_here",[]],
  [anyone,"merchant_caravan_stay_here", [], "Alright. We'll be waiting here for you.", "close_window",[(assign, "$escort_merchant_caravan_mode", 1),
                                                                                                       (assign, "$g_leave_encounter", 1)]],
#  [anyone|plyr,"escort_merchant_caravan_talk", [], "You go ahead to {s1}. I'll catch up with you.", "merchant_caravan_go_to_destination",[]],
#  [anyone,"merchant_caravan_go_to_destination", [], "Alright. But stay close.", "close_window",[[assign,"escort_merchant_caravan_mode",2]]],


# Troublesome bandits:
  [anyone,"merchant_quest_requested", [(eq, "$random_merchant_quest_no", "qst_troublesome_bandits")],
 "Actually, I was looking for an able adventurer like you.\
 There's this group of particularly troublesome bandits.\
 They have infested the vicinity of our town and are preying on my caravans.\
 They have avoided all the soldiers and the militias up to now.\
 If someone doesn't stop them soon, I am going to be ruined...", "merchant_quest_brief",
   []],

  [anyone,"merchant_quest_brief", [(eq,"$random_merchant_quest_no", "qst_troublesome_bandits")],
  "I will pay you {reg8} denars if you hunt down those troublesome bandits.\
 It's dangerous work. But I believe that you are the {man/one} for it.\
 What do you say?", "troublesome_bandits_quest_brief",[(quest_get_slot, reg8, "qst_troublesome_bandits", slot_quest_gold_reward),
                                                       ]],

  [anyone|plyr,"troublesome_bandits_quest_brief", [],
   "Alright. I will hunt down those bandits.", "merchant_quest_taken_bandits",
   [(set_spawn_radius,7),
    (quest_get_slot, ":quest_giver_center", "qst_troublesome_bandits", slot_quest_giver_center),
    (spawn_around_party,":quest_giver_center","pt_troublesome_bandits"),
    (quest_set_slot, "qst_troublesome_bandits", slot_quest_target_party, reg0),
    (store_num_parties_destroyed,"$qst_troublesome_bandits_eliminated","pt_troublesome_bandits"),
    (store_num_parties_destroyed_by_player, "$qst_troublesome_bandits_eliminated_by_player", "pt_troublesome_bandits"),
    (str_store_troop_name, s9, "$g_talk_troop"),
    (str_store_party_name_link, s4, "$g_encountered_party"),
    (setup_quest_text,"qst_troublesome_bandits"),
    (str_store_string, s2, "@Merchant {s9} of {s4} asked you to hunt down the troublesome bandits in the vicinity of the town."),
    (call_script, "script_start_quest", "qst_troublesome_bandits", "$g_talk_troop"),
    ]],
  [anyone,"merchant_quest_taken_bandits", [], "You will? I am so happy to hear that. Good luck to you.", "close_window",
   []],
  
  [anyone|plyr,"troublesome_bandits_quest_brief", [],
   "Sorry. I don't have time for this right now.", "merchant_quest_stall",[]],

# Kidnapped girl:
  [anyone,"merchant_quest_requested", [(eq, "$random_merchant_quest_no", "qst_kidnapped_girl")],
 "Actually, I was looking for a reliable {man/helper} that can undertake an important mission.\
 A group of bandits have kidnapped the daughter of a friend of mine and are holding her for ransom.\
 My friend is ready to pay them, but we still need\
 someone to take the money to those rascals and bring the girl back to safety.", "merchant_quest_brief",
   []],

  [anyone,"merchant_quest_brief", [(eq, "$random_merchant_quest_no", "qst_kidnapped_girl")],
  "The amount the bandits ask as ransom is {reg12} denars.\
 I will give you that money once you accept to take the quest.\
 You have 15 days to take the money to the bandits who will be waiting near the village of {s4}.\
 Those bastards said that they are going to kill the poor girl if they don't get the money by that time.\
 You will get your pay of {reg8} denars when you bring the girl safely back here.",
   "kidnapped_girl_quest_brief",[(quest_get_slot, ":quest_target_center", "qst_kidnapped_girl", slot_quest_target_center),
                                 (str_store_party_name, s4, ":quest_target_center"),
                                 (quest_get_slot, reg8, "qst_kidnapped_girl", slot_quest_gold_reward),
                                 (quest_get_slot, reg12, "qst_kidnapped_girl", slot_quest_target_amount),
                                 ]],

  [anyone|plyr,"kidnapped_girl_quest_brief", [],
      "Alright. I will take the ransom money to the bandits and bring back the girl.",
   "kidnapped_girl_quest_taken",[(set_spawn_radius, 4),
                                 (quest_get_slot, ":quest_target_center", "qst_kidnapped_girl", slot_quest_target_center),
                                 (quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                 (spawn_around_party,":quest_target_center","pt_bandits_awaiting_ransom"),
                                 (assign, ":quest_target_party", reg0),
                                 (quest_set_slot, "qst_kidnapped_girl", slot_quest_target_party, ":quest_target_party"),
                                 (party_set_ai_behavior, ":quest_target_party", ai_bhvr_hold),
                                 (party_set_ai_object, ":quest_target_party", "p_main_party"),
                                 (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
                                 (call_script, "script_troop_add_gold", "trp_player", ":quest_target_amount"),
                                 (assign, reg12, ":quest_target_amount"),
                                 (str_store_troop_name, s1, "$g_talk_troop"),
                                 (str_store_party_name_link, s4, "$g_encountered_party"),
                                 (str_store_party_name_link, s3, ":quest_target_center"),
                                 (setup_quest_text, "qst_kidnapped_girl"),
                                 (str_store_string, s2, "@Guildmaster of {s4} gave you {reg12} denars to pay the ransom of a girl kidnapped by bandits.\
 You are to meet the bandits near {s3} and pay them the ransom fee.\
 After that you are to bring the girl back to {s4}."),
                                 (call_script, "script_start_quest", "qst_kidnapped_girl", "$g_talk_troop"),
                                 ]],
  
  [anyone,"kidnapped_girl_quest_taken", [], "Good. I knew we could trust you at this.\
 Here is the ransom money, {reg12} denars.\
 Count it before taking it.\
 And please, don't attempt to do anything rash.\
 Keep in mind that the girl's well being is more important than anything else...", "close_window",
   []],
  
  [anyone|plyr,"kidnapped_girl_quest_brief", [],
   "Sorry. I don't have time for this right now.", "merchant_quest_stall",[]],


  [trp_kidnapped_girl,"start",
   [
     (eq, "$talk_context", tc_entering_center_quest_talk),
     ],
   "Thank you so much for bringing me back!\
  I can't wait to see my family. Good-bye.",
   "close_window",
   [(remove_member_from_party, "trp_kidnapped_girl"),
    (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 4),
    ]],



  [trp_kidnapped_girl|plyr,"kidnapped_girl_liberated_map", [], "Yes. Come with me. We are going home.", "kidnapped_girl_liberated_map_2a",[]],
  [trp_kidnapped_girl,"kidnapped_girl_liberated_map_2a", [(neg|party_can_join)], "Unfortunately. You do not have room in your party for me.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [trp_kidnapped_girl,"kidnapped_girl_liberated_map_2a", [], "Oh really? Thank you so much!",
   "close_window", [(party_join),
                    (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 3),
                    (assign, "$g_leave_encounter",1)]],
  [trp_kidnapped_girl|plyr,"kidnapped_girl_liberated_map", [], "Wait here a while longer. I'll come back for you.", "kidnapped_girl_liberated_map_2b",[]],
  [trp_kidnapped_girl,"kidnapped_girl_liberated_map_2b", [], "Oh, please {sir/madam}, do not leave me here all alone!", "close_window",[(assign, "$g_leave_encounter",1)]],


  [trp_kidnapped_girl,"start", [],
   "Oh {sir/madam}. Thank you so much for rescuing me. Will you take me to my family now?", "kidnapped_girl_liberated_map",[]],
  
  [trp_kidnapped_girl|plyr,"kidnapped_girl_liberated_battle", [], "Yes. Come with me. We are going home.", "kidnapped_girl_liberated_battle_2a",[]],
  [trp_kidnapped_girl,"kidnapped_girl_liberated_battle_2a", [(neg|hero_can_join, "p_main_party")], "Unfortunately. You do not have room in your party for me.", "kidnapped_girl_liberated_battle_2b",[]],
  [trp_kidnapped_girl,"kidnapped_girl_liberated_battle_2a", [], "Oh really? Thank you so much!",
   "close_window",[(party_add_members, "p_main_party","trp_kidnapped_girl",1),
                   (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 3),
                   ]],
  [trp_kidnapped_girl|plyr,"kidnapped_girl_liberated_battle", [], "Wait here a while longer. I'll come back for you.", "kidnapped_girl_liberated_battle_2b",[]],
  [trp_kidnapped_girl,"kidnapped_girl_liberated_battle_2b", [], "Oh, please {sir/madam}, do not leave me here all alone!",
   "close_window", [(add_companion_party,"trp_kidnapped_girl"),
                    (assign, "$g_leave_encounter",1)]],

  [trp_kidnapped_girl,"start", [], "Can I come with you now?", "kidnapped_girl_liberated_map",[]],


  [party_tpl|pt_bandits_awaiting_ransom,"start", [(quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 0),],
   "Are you the one that brought the ransom?\
 Quick, give us the money now.", "bandits_awaiting_ransom_intro_1",[(quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 1),]],
  [party_tpl|pt_bandits_awaiting_ransom,"start", [(quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 1),],
   "You came back?\
 Quick, give us the money now.", "bandits_awaiting_ransom_intro_1",[]],
  [party_tpl|pt_bandits_awaiting_ransom|plyr, "bandits_awaiting_ransom_intro_1", [(store_troop_gold, ":cur_gold"),
                                                                                  (quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                                                                  (ge, ":cur_gold", ":quest_target_amount")
                                                                                  ],
   "Here, take the money. Just set the girl free.", "bandits_awaiting_ransom_pay",[]],
  [party_tpl|pt_bandits_awaiting_ransom, "bandits_awaiting_ransom_pay", [],
   "Heh. You've brought the money all right.\
 You can take the girl now.\
 It was a pleasure doing business with you...", "close_window",
   [(quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
    (quest_get_slot, ":quest_target_party", "qst_kidnapped_girl", slot_quest_target_party),
    (quest_get_slot, ":quest_target_center", "qst_kidnapped_girl", slot_quest_target_center),
    (troop_remove_gold, "trp_player", ":quest_target_amount"),
    (remove_member_from_party, "trp_kidnapped_girl", ":quest_target_party"),
    (set_spawn_radius, 1),
    (spawn_around_party, ":quest_target_party", "pt_kidnapped_girl"),
    (assign, ":girl_party", reg0),
    (party_set_ai_behavior, ":girl_party", ai_bhvr_hold),
    (party_set_flags, ":girl_party", pf_default_behavior, 0),
    (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 2),
    (party_set_ai_behavior, ":quest_target_party", ai_bhvr_travel_to_party),
    (party_set_ai_object, ":quest_target_party", ":quest_target_center"),
    (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
    (add_gold_to_party, ":quest_target_amount", ":quest_target_party"),
    (assign, "$g_leave_encounter",1),
    ]],
  
  [anyone|plyr, "bandits_awaiting_ransom_intro_1", [],
   "No way! You release the girl first.", "bandits_awaiting_ransom_b",[]],
  [anyone, "bandits_awaiting_ransom_b", [],
   "You fool! Stop playing games and give us the money! ", "bandits_awaiting_ransom_b2",[]],
  [anyone|plyr, "bandits_awaiting_ransom_b2", [(store_troop_gold, ":cur_gold"),
                                               (quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                               (ge, ":cur_gold", ":quest_target_amount")],
   "All right. Here's your money. Let the girl go now.", "bandits_awaiting_ransom_pay",[]],
  [anyone|plyr, "bandits_awaiting_ransom_b2", [],
   "I had left the money in a safe place. Let me go fetch it.", "bandits_awaiting_ransom_no_money",[]],
  [anyone, "bandits_awaiting_ransom_no_money", [],
   "Are you testing our patience or something?  Go and bring that money here quickly.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone|plyr, "bandits_awaiting_ransom_b2", [],
   "I have no intention to pay you anything. I demand that you release the girl now!", "bandits_awaiting_ransom_fight",[]],
  [anyone, "bandits_awaiting_ransom_fight", [],
   "You won't be demanding anything when you're dead.", "close_window",[(encounter_attack),]],

  [party_tpl|pt_bandits_awaiting_ransom,"start", [(quest_slot_ge, "qst_kidnapped_girl", slot_quest_current_state, 2),],
   "What's it? You have given us the money. We have no more business.", "bandits_awaiting_remeet",[]],
  [anyone|plyr,"bandits_awaiting_remeet", [],
   "Sorry to bother you. I'll be on my way now.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone|plyr,"bandits_awaiting_remeet", [],
   "We have one more business. You'll give the money back to me.", "bandits_awaiting_remeet_2",[]],
  [anyone,"bandits_awaiting_remeet_2", [],
   "Oh, that business! Of course. Let us get down to it.", "close_window",[(encounter_attack)]],

  [party_tpl|pt_kidnapped_girl,"start", [],
   "Oh {sir/madam}. Thank you so much for rescuing me. Will you take me to my family now?", "kidnapped_girl_encounter_1",[]],
  [anyone|plyr,"kidnapped_girl_encounter_1", [], "Yes. Come with me. I'll take you home.", "kidnapped_girl_join",[]],
  [anyone,"kidnapped_girl_join", [(neg|party_can_join)], "Unfortunately. You do not have room in your party for me.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone,"kidnapped_girl_join", [], "Oh, thank you so much!",
   "close_window",[(party_join),
                   (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 3),
                   (assign, "$g_leave_encounter",1)]],
  [anyone|plyr,"kidnapped_girl_encounter_1", [], "Wait here a while longer. I'll come back for you.", "kidnapped_girl_wait",[]],
  [anyone,"kidnapped_girl_wait", [], "Oh, please {sir/madam}, do not leave me here all alone!", "close_window",[(assign, "$g_leave_encounter",1)]],

  [anyone|plyr,"merchant_quest_about_job_2", [(store_partner_quest, ":partner_quest"),
                                              (eq, ":partner_quest", "qst_kidnapped_girl"),
                                              (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 3),
                                              (neg|main_party_has_troop, "trp_kidnapped_girl")],
   "Unfortunately I lost the girl on the way here...", "lost_kidnapped_girl",[]],
  [anyone,"lost_kidnapped_girl", [],
   "Oh no! How am I going to tell this to my friend?", "lost_kidnapped_girl_2",[]],
  [anyone|plyr,"lost_kidnapped_girl_2", [],
   "I'm sorry. I could do nothing about it.", "lost_kidnapped_girl_3",[]],
  [anyone,"lost_kidnapped_girl_3", [],
   "You let me down {playername}. I had trusted you.\
 I will let people know of your incompetence at this task.\
 Also, I want back that {reg8} denars I gave you as the ransom fee.", "lost_kidnapped_girl_4",
   [(quest_get_slot, reg8, "qst_kidnapped_girl", slot_quest_target_amount),
    (try_for_parties, ":cur_party"),
      (party_count_members_of_type, ":num_members", ":cur_party", "trp_kidnapped_girl"),
      (gt, ":num_members", 0),
      (party_remove_members, ":cur_party", "trp_kidnapped_girl", 1),
      (party_remove_prisoners, ":cur_party", "trp_kidnapped_girl", 1),
    (try_end),
    (call_script, "script_end_quest", "qst_kidnapped_girl"),
    (call_script, "script_change_troop_renown", "trp_player", -5),
    ]],
  [anyone|plyr, "lost_kidnapped_girl_4", [(store_troop_gold,":gold"),
                                          (quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                          (ge,":gold",":quest_target_amount"),
                                          ],
   "Of course. Here you are...", "merchant_quest_about_job_5a",[(quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                                                (troop_remove_gold, "trp_player",":quest_target_amount"),
                                                                ]],
  [anyone,"merchant_quest_about_job_5a", [],
   "At least you have the decency to return the money.", "close_window",[]],
  [anyone|plyr,"lost_kidnapped_girl_4", [],
   "Sorry. I don't have that amount with me.", "merchant_quest_about_job_5b",[]],
  [anyone,"merchant_quest_about_job_5b", [],
   "Do you expect me to believe that? You are going to pay that ransom fee back! Go and bring the money now!",
   "close_window",[(quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                   (val_add, "$debt_to_merchants_guild", ":quest_target_amount"),
                   ]],


#  Give us the money now. Quick.
# Here, take the money. Just set the girl free.
# Heh, It was a pleasure doing business with you. 
  
# You set the girl free first. You'll have the money afterwards.
# Stop playing games.  

#persuade_lords_to_make_peace
  [anyone,"merchant_quest_requested", [(eq, "$random_merchant_quest_no", "qst_persuade_lords_to_make_peace"),
                                       (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
                                       (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
                                       (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
                                       (str_store_troop_name_link, s12, ":quest_object_troop"),
                                       (str_store_troop_name_link, s13, ":quest_target_troop"),
                                       (str_store_faction_name_link, s14, ":quest_target_faction"),
                                       (str_store_faction_name_link, s15, "$g_encountered_party_faction"),],
   "This war between {s15} and {s14} has brought our town to the verge of ruin.\
 Our caravans get raided before they can reach their destination.\
 Our merchants are afraid to leave the safety of the town walls.\
 And as if those aren't enough, the taxes to maintain the war take away the last bits of our savings.\
 If peace does not come soon, we can not hold on for much longer.", "merchant_quest_persuade_peace_1",
   []],

  [anyone|plyr,"merchant_quest_persuade_peace_1", [], "You are right. But who can stop this madness called war?", "merchant_quest_brief",[]],
  [anyone|plyr,"merchant_quest_persuade_peace_1", [], "It is your duty to help the nobles in their war effort. You shouldn't complain about it.", "merchant_quest_persuade_peace_reject",[]],

  [anyone,"merchant_quest_persuade_peace_reject", [], "Hah. The nobles fight their wars for their greed and their dreams of glory.\
 And it is poor honest folk like us who have to bear the real burden.\
 But you obviously don't want to hear about that.", "close_window",[]],

  [anyone,"merchant_quest_brief", [(eq,"$random_merchant_quest_no","qst_persuade_lords_to_make_peace")],
   "There have been attempts to reconcile the two sides and reach a settlement.\
 However, there are powerful lords on both sides whose interests lie in continuing the war.\
 These men urge all others not to heed to the word of sensible men, but to keep fighting.\
 While these leaders remain influential, no peace settlement can be reached.", "merchant_quest_persuade_peace_3",[]],

  [anyone|plyr,"merchant_quest_persuade_peace_3", [], "Who are these warmongers who block the way of peace?", "merchant_quest_persuade_peace_4",[]],
  [anyone|plyr,"merchant_quest_persuade_peace_3", [], "Who are these lords you speak of?", "merchant_quest_persuade_peace_4",[]],

  [anyone,"merchant_quest_persuade_peace_4", [], "They are {s12} from {s15} and {s13} from {s14}. Until they change their mind or lose their influence,\
 there will be no chance of having peace between the two sides.", "merchant_quest_persuade_peace_5",[
       (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
       (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
       (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
       (str_store_troop_name_link, s12, ":quest_object_troop"),
       (str_store_troop_name_link, s13, ":quest_target_troop"),
       (str_store_faction_name_link, s14, ":quest_target_faction"),
       (str_store_faction_name_link, s15, "$g_encountered_party_faction"),     
     ]],

  [anyone|plyr,"merchant_quest_persuade_peace_5", [], "What can be done about this?", "merchant_quest_persuade_peace_6",[]],
  [anyone|plyr,"merchant_quest_persuade_peace_5", [], "Alas, it seems nothing can be done about it.", "merchant_quest_persuade_peace_6",[]],

  [anyone,"merchant_quest_persuade_peace_6", [], "There is a way to resolve the issue.\
 A particularly determined person can perhaps persuade one or both of these lords to accept making peace.\
 And even if that fails, it can be possible to see that these lords are defeated by force and taken prisoner.\
 If they are captive, they will lose their influence and they can no longer oppose a settlement... What do you think? Can you do it?",
   "merchant_quest_persuade_peace_7",[]],

  [anyone|plyr,"merchant_quest_persuade_peace_7", [], "It seems difficult. But I will try.", "merchant_quest_persuade_peace_8",[]],
  [anyone|plyr,"merchant_quest_persuade_peace_7", [], "If the price is right, I may.", "merchant_quest_persuade_peace_8",[]],
  [anyone|plyr,"merchant_quest_persuade_peace_7", [], "Forget it. This is not my problem.", "merchant_quest_persuade_peace_8",[]],

  [anyone,"merchant_quest_persuade_peace_8", [], "Most of the merchants in the town will gladly open up their purses to support such a plan.\
 I think we can collect {reg12} denars between ourselves.\
 We will be happy to reward you with that sum, if you can work this out.\
 Convince {s12} and {s13} to accept a peace settlement,\
 and if either of them proves too stubborn, make sure he falls captive and can not be ransomed until a peace deal is settled.",
   "merchant_quest_persuade_peace_9",[
       (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
       (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
       (str_store_troop_name_link, s12, ":quest_object_troop"),
       (str_store_troop_name_link, s13, ":quest_target_troop"),
       (quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
       (assign, reg12, ":quest_reward")]],
  
  [anyone|plyr,"merchant_quest_persuade_peace_9", [], "All right. I will do my best.", "merchant_quest_persuade_peace_10",[]],
  [anyone|plyr,"merchant_quest_persuade_peace_9", [], "Sorry. I can not do this.", "merchant_quest_persuade_peace_no",[]],
  
  [anyone,"merchant_quest_persuade_peace_10", [], "Excellent. You will have our blessings.\
 I hope you can deal with those two old goats.\
 We will be waiting and hoping for the good news.", "close_window",[
     (str_store_party_name_link, s4, "$g_encountered_party"),
     (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
     (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
     (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
     (quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
     (assign, reg12, ":quest_reward"),
     (str_store_troop_name_link, s12, ":quest_object_troop"),
     (str_store_troop_name_link, s13, ":quest_target_troop"),
     (str_store_faction_name_link, s14, ":quest_target_faction"),
     (str_store_faction_name_link, s15, "$g_encountered_party_faction"),     
     (setup_quest_text,"qst_persuade_lords_to_make_peace"),
     (str_store_string, s2, "@Guildmaster of {s4} promised you {reg12} denars if you can make sure that\
 {s12} and {s13} no longer pose a threat to a peace settlement between {s15} and {s14}.\
 In order to do that, you must either convince them or make sure they fall captive and remain so until a peace agreement is made."),
     (call_script, "script_start_quest", "qst_persuade_lords_to_make_peace", "$g_talk_troop"),
     (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
     (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
     (call_script, "script_report_quest_troop_positions", "qst_persuade_lords_to_make_peace", ":quest_object_troop", 3),
     (call_script, "script_report_quest_troop_positions", "qst_persuade_lords_to_make_peace", ":quest_target_troop", 4),
     ]],
  
  [anyone,"merchant_quest_persuade_peace_no", [], "Don't say no right away. Think about this for some time.\
 If there is a {man/lady} who can manage to do this, it is you.",
   "close_window",[]],


#deal with night bandits
  [anyone,"merchant_quest_requested",
   [
     (eq, "$random_merchant_quest_no", "qst_deal_with_night_bandits"),
     ],
   "Do I indeed! There's a group of bandits infesting the town, and I'm at the end of my rope as to how to deal with them.\
 They've been ambushing and robbing townspeople under the cover of night,\
 and then fading away quick as lightning when the guards finally show up. We've not been able to catch a one of them.\
 They only attack lone people, never daring to show themselves when there's a group about.\
 I need someone who can take on these bandits alone and win. That seems to be the only way of bringing them to justice.\
 Are you up to the task?", "merchant_quest_deal_with_night_bandits",
   []],

  [anyone,"merchant_quest_brief",
   [
     (eq,"$random_merchant_quest_no","qst_deal_with_night_bandits"),
     ],
   "There's a group of bandits infesting the town, and I'm at the end of my rope as to how to deal with them.\
 They've been ambushing and robbing townspeople under the cover of night,\
 and then fading away quick as lightning when the guards finally show up. We've not been able to catch a one of them.\
 They only attack lone people, never daring to show themselves when there's a group about.\
 I need someone who can take on these bandits alone and win. That seems to be the only way of bringing them to justice.\
 Are you up to the task?", "merchant_quest_deal_with_night_bandits",
   []],

  [anyone|plyr,"merchant_quest_deal_with_night_bandits", [],
   "Killing bandits? Why, certainly!",
   "deal_with_night_bandits_quest_taken",
   [
     (str_store_party_name_link, s14, "$g_encountered_party"),
     (setup_quest_text, "qst_deal_with_night_bandits"),
     (str_store_string, s2, "@The Guildmaster of {s14} has asked you to deal with a group of bandits terrorising the streets of {s14}. They only come out at night, and only attack lone travellers on the streets."),
     (call_script, "script_start_quest", "qst_deal_with_night_bandits", "$g_talk_troop"),
     ]],
  
  [anyone|plyr, "merchant_quest_deal_with_night_bandits", [],
   "My apologies, I'm not interested.", "merchant_quest_stall",[]],

  [anyone,"deal_with_night_bandits_quest_taken", [], "That takes a weight off my shoulders, {playername}.\
 You can expect a fine reward if you come back successful. Just don't get yourself killed, eh?", "mayor_pretalk",[]],


#move cattle herd
  [anyone,"merchant_quest_requested", [(eq, "$random_merchant_quest_no", "qst_move_cattle_herd"),
                                       (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
                                       (str_store_party_name,s13,":target_center"),],
   "One of the merchants here is looking for herdsmen to take his cattle to the market at {s13}.", "merchant_quest_brief",
   []],

  [anyone,"merchant_quest_brief",
   [
    (eq,"$random_merchant_quest_no","qst_move_cattle_herd"),
    (quest_get_slot, reg8, "qst_move_cattle_herd", slot_quest_gold_reward),
    (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
    (str_store_party_name, s13, ":target_center"),
    ],
   "The cattle herd must be at {s13} within 30 days. Sooner is better, much better,\
 but it must be absolutely no later than 30 days.\
 If you can do that, I'd be willing to pay you {reg8} denars for your trouble. Interested?", "move_cattle_herd_quest_brief",
   []],

#MV: remove when quest dialogs are done, or bugs are fixed   
  [anyone,"merchant_quest_brief",
   [(str_store_quest_name,s4,"$random_merchant_quest_no")],
   "DEBUG: It seems some coder abused his arcane powers, and forgot to put a dialog here. The quest is {s4}.", "mayor_pretalk",
   []],
  
  [anyone|plyr,"move_cattle_herd_quest_brief", [],  "Aye, I can take the herd to {s13}.",
   "move_cattle_herd_quest_taken",
   [
     (call_script, "script_create_cattle_herd", "$g_encountered_party", 0),
     (quest_set_slot, "qst_move_cattle_herd", slot_quest_target_party, reg0),
     (str_store_party_name_link, s10,"$g_encountered_party"),
     (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
     (str_store_party_name_link, s13, ":target_center"),
     (quest_get_slot, reg8, "qst_move_cattle_herd", slot_quest_gold_reward),
     (setup_quest_text, "qst_move_cattle_herd"),
     (str_store_string, s2, "@Guildmaster of {s10} asked you to move a cattle herd to {s13}. You will earn {reg8} denars in return."),
     (call_script, "script_start_quest", "qst_move_cattle_herd", "$g_talk_troop"),
     ]],
  [anyone|plyr,"move_cattle_herd_quest_brief", [],
   "I am sorry, but no.", "merchant_quest_stall",[]],

  [anyone,"move_cattle_herd_quest_taken", [], "Splendid. You can find the herd right outside the town.\
 After you take the animals to {s13}, return back to me and I will give you your pay.", "mayor_pretalk",[]],


################################################# 
#################### Random merchant quests end

  [anyone,"merchant_quest_requested", [], "I am afraid I can't offer you a job right now.", "mayor_pretalk",[]],


#Village elders

  [anyone,"start", [(is_between,"$g_talk_troop",village_elders_begin,village_elders_end),
                    (store_partner_quest,":elder_quest"),
                    (eq,":elder_quest","qst_deliver_cattle"),
                    (check_quest_succeeded, ":elder_quest"),
                    (quest_get_slot, reg5, "qst_deliver_cattle", slot_quest_target_amount)],
   "My good {sir/madam}. Our village is grateful for your help. Thanks to the {reg5} heads of cattle you have brought, we can now raise our own herd.", "village_elder_deliver_cattle_thank",
   [(add_xp_as_reward, 400),
    (quest_get_slot, ":num_cattle", "qst_deliver_cattle", slot_quest_target_amount),
    (party_set_slot, "$current_town", slot_village_number_of_cattle, ":num_cattle"),
    (call_script, "script_change_center_prosperity", "$current_town", 4),
    (call_script, "script_change_player_relation_with_center", "$current_town", 5),
    (call_script, "script_end_quest", "qst_deliver_cattle"),
#Troop commentaries begin
    (call_script, "script_add_log_entry", logent_helped_peasants, "trp_player",  "$current_town", -1, -1),
#Troop commentaries end

    ]],

  [anyone,"village_elder_deliver_cattle_thank", [],
   "My good {lord/lady}, please, is there anything I can do for you?", "village_elder_talk",[]],
  

##  [anyone,"start",
##   [
##     (is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
##     (store_partner_quest, ":elder_quest"),
##     (eq, ":elder_quest", "qst_train_peasants_against_bandits"),
##     (check_quest_succeeded, ":elder_quest"),
##     (quest_get_slot, reg5, "qst_train_peasants_against_bandits", slot_quest_target_amount)],
##   "Oh, thank you so much for training our men. Now we may stand a chance against those accursed bandits if they come again.", "village_elder_train_peasants_against_bandits_thank",
##   [
##     (add_xp_as_reward, 400),
##     (call_script, "script_change_player_relation_with_center", "$current_town", 5),
##     (call_script, "script_end_quest", "qst_train_peasants_against_bandits"),
##     (call_script, "script_add_log_entry", logent_helped_peasants, "trp_player",  "$current_town", -1, -1),
##    ]],

#  [anyone,"village_elder_train_peasants_against_bandits_thank", [],
#   "Now, good {sire/lady}, is there anything I can do for you?", "village_elder_talk",[]],



  [anyone,"start", [(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),(eq,"$g_talk_troop_met",0),
                    (str_store_party_name, s9, "$current_town")],
   "Good day, {sir/madam}, and welcome to {s9}. I am the elder of this village.", "village_elder_talk",[]],

  [anyone,"start", [(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),(eq,"$g_talk_troop_met",0),
                    (str_store_party_name, s9, "$current_town"),
                    (party_slot_eq, "$current_town", slot_town_lord, "trp_player")],
   "Welcome to {s9}, my {lord/lady}. We were rejoiced by the news that you are the new {lord/lady} of our humble village.\
 I am the village elder and I will be honoured to serve you in any way I can.", "village_elder_talk",[]],
  
  [anyone ,"start", [(is_between,"$g_talk_troop",village_elders_begin,village_elders_end),
                     (party_slot_eq, "$current_town", slot_town_lord, "trp_player")],
   "{My lord/My lady}, you honour our humble village with your presence.", "village_elder_talk",[]],

  [anyone ,"start", [(is_between,"$g_talk_troop",village_elders_begin,village_elders_end)],
   "Good day, {sir/madam}.", "village_elder_talk",[]],

  [anyone ,"village_elder_pretalk", [],
   "Is there anything else I can do for you?", "village_elder_talk",[]],

  [anyone|plyr,"village_elder_talk", [(check_quest_active, "qst_hunt_down_fugitive"),
                                      (neg|check_quest_concluded, "qst_hunt_down_fugitive"),
                                      (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
                                      (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
                                      (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
                                      (str_store_string, s4, s50),
                                      ],
   "I am looking for a man by the name of {s4}. I was told he may be hiding here.", "village_elder_ask_fugitive",[]],

  [anyone ,"village_elder_ask_fugitive", [(is_currently_night)],
   "Strangers come and go to our village, {sir/madam}. But I doubt you'll run into him at this hour of the night. You would have better luck during the day.", "village_elder_pretalk",[]],
  [anyone ,"village_elder_ask_fugitive", [],
   "Strangers come and go to our village, {sir/madam}. If he is hiding here, you will surely find him if you look around.", "close_window",[]],

  [anyone|plyr,"village_elder_talk", [(store_partner_quest,":elder_quest"),(ge,":elder_quest",0)],
   "About the task you asked of me...", "village_elder_active_mission_1",[]],

  [anyone|plyr,"village_elder_talk", [(ge, "$g_talk_troop_faction_relation", 0),(store_partner_quest,":elder_quest"),(lt,":elder_quest",0)],
   "Do you have any tasks I can help you with?", "village_elder_request_mission_ask",[]],

  [anyone|plyr,"village_elder_talk", [(party_slot_eq, "$current_town", slot_village_state, 0),
                                      (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),],
   "I want to buy some supplies. I will pay with gold.", "village_elder_trade_begin",[]],


  [anyone ,"village_elder_trade_begin", [], "Of course, {sir/madam}. Do you want to buy goods or cattle?", "village_elder_trade_talk",[]],

  [anyone|plyr,"village_elder_trade_talk", [], "I want to buy food and supplies.", "village_elder_trade",[]],

  [anyone ,"village_elder_trade", [],
   "We have some food and other supplies in our storehouse. Come have a look.", "village_elder_pretalk",[(change_screen_trade, "$g_talk_troop"),]],

  [anyone|plyr,"village_elder_trade_talk", [(party_slot_eq, "$current_town", slot_village_state, 0),
                                      (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
                                      (assign, ":quest_village", 0),
                                      (try_begin),
                                        (check_quest_active, "qst_deliver_cattle"),
                                        (quest_slot_eq, "qst_deliver_cattle", slot_quest_target_center, "$current_town"),
                                        (assign, ":quest_village", 1),
                                      (try_end),
                                      (eq, ":quest_village", 0),
                                      ],
   "I want to buy some cattle.", "village_elder_buy_cattle",[]],
  
  [anyone|plyr,"village_elder_trade_talk", [], "I changed my mind. I don't need to buy anything.", "village_elder_pretalk",[]],

  [anyone|plyr,"village_elder_talk",
   [
     ],
   "Have you seen any enemies around here recently?", "village_elder_ask_enemies",[]],

  [anyone,"village_elder_ask_enemies",
   [
     (assign, ":give_report", 0),
     (party_get_slot, ":original_faction", "$g_encountered_party", slot_center_original_faction),
     (store_relation, ":original_faction_relation", ":original_faction", "fac_player_supporters_faction"),
     (try_begin),
       (gt, ":original_faction_relation", 0),
       (party_slot_ge, "$g_encountered_party", slot_center_player_relation, 0),
       (assign, ":give_report", 1),
     (else_try),
       (party_slot_ge, "$g_encountered_party", slot_center_player_relation, 30),
       (assign, ":give_report", 1),
     (try_end),
     (eq, ":give_report", 0),
     ],
   "I am sorry, {sir/madam}. We have neither seen nor heard of any war parties in this area.", "village_elder_pretalk",
   []],

  [anyone,"village_elder_ask_enemies",
   [],
   "Hmm. Let me think about it...", "village_elder_tell_enemies",
   [
     (assign, "$temp", 0),
     ]],

  [anyone,"village_elder_tell_enemies",
   [
     (assign, ":target_hero_index", "$temp"),
     (assign, ":end_cond", kingdom_heroes_end),
     (try_for_range, ":cur_troop", kingdom_heroes_begin, ":end_cond"),
       (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
       (gt, ":cur_party", 0),
       (store_troop_faction, ":cur_faction", ":cur_troop"),
       (store_relation, ":reln", ":cur_faction", "fac_player_supporters_faction"),
       (lt, ":reln", 0),
       (store_distance_to_party_from_party, ":dist", "$g_encountered_party", ":cur_party"),
       (lt, ":dist", 10),
       (call_script, "script_get_information_about_troops_position", ":cur_troop", 0),
       (eq, reg0, 1), #Troop's location is known.
       (val_sub, ":target_hero_index", 1),
       (lt, ":target_hero_index", 0),
       (assign, ":end_cond", 0),
       (str_store_string, s2, "@He is not commanding any men at the moment."),
       (assign, ":num_troops", 0),
       (assign, ":num_wounded_troops", 0),
       (party_get_num_companion_stacks, ":num_stacks", ":cur_party"),
       (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
         (party_stack_get_troop_id, ":stack_troop", ":cur_party", ":i_stack"),
         (neg|troop_is_hero, ":stack_troop"),
         (party_stack_get_size, ":stack_size", ":cur_party", ":i_stack"),
         (party_stack_get_num_wounded, ":num_wounded", ":cur_party", ":i_stack"),
         (val_add, ":num_troops", ":stack_size"),
         (val_add, ":num_wounded_troops", ":num_wounded"),
       (try_end),
       (gt, ":num_troops", 0),
       (call_script, "script_round_value", ":num_wounded_troops"),
       (assign, reg1, reg0),
       (call_script, "script_round_value", ":num_troops"),
       (str_store_string, s2, "@He currently commands {reg0} men{reg1?, of which around {reg1} are wounded:}."),
     (try_end),
     (eq, ":end_cond", 0),
     ],
   "{s1} {s2}", "village_elder_tell_enemies",
   [
     (val_add, "$temp", 1),
     ]],

  [anyone,"village_elder_tell_enemies",
   [(eq, "$temp", 0)],
   "No, {sir/madam}. We haven't seen any war parties in this area for some time.", "village_elder_pretalk",
   []],

  [anyone,"village_elder_tell_enemies",
   [],
   "Well, I guess that was all.", "village_elder_pretalk",
   []],


  [anyone|plyr,"village_elder_talk", [(call_script, "script_cf_village_recruit_volunteers_cond"),],
   "Are there any lads from this village who might want to seek their fortune in the wars?", "village_elder_recruit_start",[]],

  [anyone|plyr,"village_elder_talk", [],
   "[Leave]", "close_window",[]],



  [anyone ,"village_elder_buy_cattle", [(party_get_slot, reg5, "$g_encountered_party", slot_village_number_of_cattle),
                                        (gt, reg5, 0),
                                        (store_item_value, ":cattle_cost", "itm_cattle_meat"),
                                        (call_script, "script_game_get_item_buy_price_factor", "itm_cattle_meat"),
                                        (val_mul, ":cattle_cost", reg0),
                                        #Multiplied by 2 and divided by 100
                                        (val_div, ":cattle_cost", 50),
                                        (assign, "$temp", ":cattle_cost"),
                                        (assign, reg6, ":cattle_cost"),
                                        ],
   "We have {reg5} heads of cattle, each for {reg6} denars. How many do you want to buy?", "village_elder_buy_cattle_2",[]],

  [anyone ,"village_elder_buy_cattle", [],
   "I am afraid we have no cattle left in the village {sir/madam}.", "village_elder_buy_cattle_2",[]],


  [anyone|plyr,"village_elder_buy_cattle_2", [(party_get_slot, ":num_cattle", "$g_encountered_party", slot_village_number_of_cattle),
                                              (ge, ":num_cattle", 1),
                                              (store_troop_gold, ":gold", "trp_player"),
                                              (ge, ":gold", "$temp"),],
   "One.", "village_elder_buy_cattle_complete",[(call_script, "script_buy_cattle_from_village", "$g_encountered_party", 1, "$temp"),
                                                       ]],
  
  [anyone|plyr,"village_elder_buy_cattle_2", [(party_get_slot, ":num_cattle", "$g_encountered_party", slot_village_number_of_cattle),
                                              (ge, ":num_cattle", 2),
                                              (store_troop_gold, ":gold", "trp_player"),
                                              (store_mul, ":cost", "$temp", 2),
                                              (ge, ":gold", ":cost"),],
   "Two.", "village_elder_buy_cattle_complete",[(call_script, "script_buy_cattle_from_village", "$g_encountered_party", 2, "$temp"),
                                                       ]],
  
  [anyone|plyr,"village_elder_buy_cattle_2", [(party_get_slot, ":num_cattle", "$g_encountered_party", slot_village_number_of_cattle),
                                              (ge, ":num_cattle", 3),
                                              (store_troop_gold, ":gold", "trp_player"),
                                              (store_mul, ":cost", "$temp", 3),
                                              (ge, ":gold", ":cost"),],
   "Three.", "village_elder_buy_cattle_complete",[(call_script, "script_buy_cattle_from_village", "$g_encountered_party", 3, "$temp"),
                                                       ]],
  
  [anyone|plyr,"village_elder_buy_cattle_2", [(party_get_slot, ":num_cattle", "$g_encountered_party", slot_village_number_of_cattle),
                                              (ge, ":num_cattle", 4),
                                              (store_troop_gold, ":gold", "trp_player"),
                                              (store_mul, ":cost", "$temp", 4),
                                              (ge, ":gold", ":cost"),],
   "Four.", "village_elder_buy_cattle_complete",[(call_script, "script_buy_cattle_from_village", "$g_encountered_party", 4, "$temp"),
                                                       ]],
  
  [anyone|plyr,"village_elder_buy_cattle_2", [(party_get_slot, ":num_cattle", "$g_encountered_party", slot_village_number_of_cattle),
                                              (ge, ":num_cattle", 5),
                                              (store_troop_gold, ":gold", "trp_player"),
                                              (store_mul, ":cost", "$temp", 5),
                                              (ge, ":gold", ":cost"),],
   "Five.", "village_elder_buy_cattle_complete",[(call_script, "script_buy_cattle_from_village", "$g_encountered_party", 5, "$temp"),
                                                       ]],
  
  [anyone|plyr,"village_elder_buy_cattle_2", [],
   "Forget it.", "village_elder_pretalk",[]],

  [anyone ,"village_elder_buy_cattle_complete", [],
   "I will tell the herders to round up the animals and bring them to you, {sir/madam}. I am sure you will be satisfied with your purchase.", "village_elder_pretalk",[]],


  [anyone ,"village_elder_recruit_start", [(party_slot_eq, "$current_town", slot_center_volunteer_troop_amount, 0)],
   "I don't think anyone would be interested, {sir/madam}. Is there anything else I can do for you?", "village_elder_talk",[]],
  
  [anyone ,"village_elder_recruit_start", [(party_get_slot, ":num_volunteers", "$current_town", slot_center_volunteer_troop_amount),
                                           (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                           (val_min, ":num_volunteers", ":free_capacity"),
                                           (assign, "$temp",  ":num_volunteers"),
                                           (assign, reg5, ":num_volunteers"),
                                           (store_add, reg7, ":num_volunteers", -1),
                                           ],
   "I can think of {reg5} whom I suspect would jump at the chance. If you could pay 10 denars {reg7?each for their equipment:for his equipment}.\
 Does that suit you?", "village_elder_recruit_decision",[]],

  [anyone|plyr,"village_elder_recruit_decision", [(party_slot_eq, "$current_town", slot_center_volunteer_troop_amount, 0)],
   "So be it.", "village_elder_pretalk",[(party_set_slot, "$current_town", slot_center_volunteer_troop_amount, -1),]],

  [anyone|plyr,"village_elder_recruit_decision", [(assign, ":num_volunteers", "$temp"),
                                                  (ge, ":num_volunteers", 1),
                                                  (store_add, reg7, ":num_volunteers", -1)],
   "Tell {reg7?them:him} to make ready.", "village_elder_pretalk",[(call_script, "script_village_recruit_volunteers_recruit"),]],

  [anyone|plyr,"village_elder_recruit_decision", [(party_slot_ge, "$current_town", slot_center_volunteer_troop_amount, 1)],
   "No, not now.", "village_elder_pretalk",[]],

  [anyone,"village_elder_active_mission_1", [], "Yes {sir/madam}, have you made any progress on it?", "village_elder_active_mission_2",[]],

  [anyone|plyr,"village_elder_active_mission_2",[(store_partner_quest,":elder_quest"),
                                                 (eq, ":elder_quest", "qst_deliver_grain"),
                                                 (quest_get_slot, ":quest_target_amount", "qst_deliver_grain", slot_quest_target_amount),
                                                 (call_script, "script_get_troop_item_amount", "trp_player", "itm_grain"),
                                                 (assign, ":cur_amount", reg0),
                                                 (ge, ":cur_amount", ":quest_target_amount"),
                                                 (assign, reg5, ":quest_target_amount"),
                                                 ],
   "Indeed. I brought you {reg5} packs of wheat.", "village_elder_deliver_grain_thank",
   []],

  [anyone,"village_elder_deliver_grain_thank", [(str_store_party_name, s13, "$current_town")],
   "My good {lord/lady}. You have saved us from hunger and desperation. We cannot thank you enough, but you'll always be in our prayers.\
 The village of {s13} will not forget what you have done for us.", "village_elder_deliver_grain_thank_2",
   [(quest_get_slot, ":quest_target_amount", "qst_deliver_grain", slot_quest_target_amount),
    (troop_remove_items, "trp_player", "itm_grain", ":quest_target_amount"),
    (add_xp_as_reward, 400),
    (call_script, "script_change_center_prosperity", "$current_town", 4),
    (call_script, "script_change_player_relation_with_center", "$current_town", 5),
    (call_script, "script_end_quest", "qst_deliver_grain"),
#Troop commentaries begin
    (call_script, "script_add_log_entry", logent_helped_peasants, "trp_player",  "$current_town", -1, -1),
#Troop commentaries end
   ]],

  [anyone,"village_elder_deliver_grain_thank_2", [],
   "My good {lord/lady}, please, is there anything I can do for you?", "village_elder_talk",[]],


  [anyone|plyr,"village_elder_active_mission_2", [], "I am still working on it.", "village_elder_active_mission_3",[]],
  [anyone|plyr,"village_elder_active_mission_2", [], "I am afraid I won't be able to finish it.", "village_elder_mission_failed",[]],
                                                                                                                                                   
  [anyone,"village_elder_active_mission_3", [], "Thank you, {sir/madam}. We are praying for your success everyday.", "village_elder_pretalk",[]],

  [anyone,"village_elder_mission_failed", [], "Ah, I am sorry to hear that {sir/madam}. I'll try to think of something else.", "village_elder_pretalk",
   [(store_partner_quest,":elder_quest"),
    (call_script, "script_abort_quest", ":elder_quest", 1)]],
##
##  [anyone,"village_elder_generic_mission_thank", [],
##   "You have been so helpful {sir/madam}. I do not know how to thank you.", "village_elder_generic_mission_completed",[]],
##
##  [anyone|plyr,"village_elder_generic_mission_completed", [],
##   "Speak not of it. I only did what needed to be done.", "village_elder_pretalk",[]],

# Currently not needed.
##  [anyone|plyr,"village_elder_generic_mission_failed", [],
##   "TODO: I'm sorry I failed you sir. It won't happen again.", "village_elder_pretalk",
##   [(store_partner_quest,":elder_quest"),
##    (call_script, "script_finish_quest", ":elder_quest", 0),
##    ]],


  [anyone,"village_elder_request_mission_ask", [(store_partner_quest,":elder_quest"),(ge,":elder_quest",0)],
   "Well {sir/madam}, you are already engaged with a task helping us. We cannot ask more from you.", "village_elder_pretalk",[]],

  [anyone,"village_elder_request_mission_ask", [(troop_slot_eq, "$g_talk_troop", slot_troop_does_not_give_quest, 1)],
   "No {sir/madam}, We don't have any other tasks for you.", "village_elder_pretalk",[]],
  
  [anyone|auto_proceed,"village_elder_request_mission_ask", [], "A task?", "village_elder_tell_mission",
   [
       (call_script, "script_get_random_quest", "$g_talk_troop"),
       (assign, "$random_quest_no", reg0),
   ]],


  [anyone,"village_elder_tell_mission", [(eq,"$random_quest_no","qst_deliver_grain")],
   "{My good sir/My good lady}, our village has been going through such hardships lately.\
 The harvest has been bad, and recently some merciless bandits took away our seed grain that we had reserved for the planting season.\
 If we cannot find some grain soon, we will not be able to plant our fields and then we will have nothing to eat for the coming year.\
 If you can help us, we would be indebted to you forever.", "village_elder_tell_deliver_grain_mission",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_party_name_link,s3,":quest_target_center"),
     (quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "@The elder of the village of {s3} asked you to bring them {reg5} packs of wheat."),
   ]],

  [anyone|plyr,"village_elder_tell_deliver_grain_mission", [],
   "Hmmm. How much grain do you need?", "village_elder_tell_deliver_grain_mission_2",[]],
  [anyone|plyr,"village_elder_tell_deliver_grain_mission", [],
   "I can't be bothered with this. Ask help from someone else.", "village_elder_deliver_grain_mission_reject",[]],
  
  [anyone,"village_elder_tell_deliver_grain_mission_2", [(quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount)],
   "I think {reg5} packs of wheat will let us start the planting. Hopefully, we can find charitable people to help us with the rest.", "village_elder_tell_deliver_grain_mission_3",[]],
  
  [anyone|plyr,"village_elder_tell_deliver_grain_mission_3", [],
   "Then I will go and find you the wheat you need.", "village_elder_deliver_grain_mission_accept",[]],
  [anyone|plyr,"village_elder_tell_deliver_grain_mission_3", [],
   "I am afraid I don't have time for this. You'll need to find help elsewhere.", "village_elder_deliver_grain_mission_reject",[]],

  [anyone,"village_elder_deliver_grain_mission_accept", [], "Thank you, {sir/madam}. We'll be praying for you night and day.", "close_window",
   [(assign, "$g_leave_encounter",1),
    (call_script, "script_change_player_relation_with_center", "$current_town", 5),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],
  
  [anyone,"village_elder_deliver_grain_mission_reject", [], "Yes {sir/madam}, of course. I am sorry if I have bothered you with our troubles.", "close_window",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    ]],



  [anyone,"village_elder_tell_mission", [(eq,"$random_quest_no", "qst_train_peasants_against_bandits")],
   "We are suffering greatly at the hands of a group of bandits. They take our food and livestock,\
 and kill anyone who doesn't obey them immediately. Our men are angry that we cannot defend ourselves, but we are only simple farmers...\
 However, with some help, I think that some of the people here could be more than that.\
 We just need an experienced warrior to teach us how to fight.",
   "village_elder_tell_train_peasants_against_bandits_mission",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_party_name_link, s13, ":quest_target_center"),
     (quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@The elder of the village of {s13} asked you to train {reg5} peasants to fight against local bandits."),
   ]],

  [anyone|plyr, "village_elder_tell_train_peasants_against_bandits_mission", [],
   "I can teach you how to defend yourself.", "village_elder_train_peasants_against_bandits_mission_accept",[]],
  [anyone|plyr, "village_elder_tell_train_peasants_against_bandits_mission", [],
   "You peasants have no business taking up arms. Just pay the bandits and be off with it.", "village_elder_train_peasants_against_bandits_mission_reject",[]],
  
  [anyone,"village_elder_train_peasants_against_bandits_mission_accept", [], "You will? Oh, splendid!\
 We would be deeply indebted to you, {sir/madam}.\
 I'll instruct the village folk to assemble here and receive your training.\
 If you can teach us how to defend ourselves, I promise you'll receive everything we can give you in return for your efforts.", "close_window",
   [
     (assign, "$g_leave_encounter",1),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_center", "$current_town", 3),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     ]],
  
  [anyone,"village_elder_train_peasants_against_bandits_mission_reject", [], "Yes, of course {sir/madam}.\
 Thank you for your counsel.", "close_window",
   [
     (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
     ]],


  [anyone,"village_elder_tell_mission", [(eq,"$random_quest_no","qst_deliver_cattle")],
   "Bandits have driven away our cattle. Our pastures are empty. If we had just a few heads of cattle we could start to raise a herd again.",
   "village_elder_tell_deliver_cattle_mission",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_party_name_link,s3,":quest_target_center"),
     (quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "@The elder of the village of {s3} asked you to bring them {reg5} heads of cattle."),
   ]],

  [anyone|plyr,"village_elder_tell_deliver_cattle_mission", [],
   "How many animals do you need?", "village_elder_tell_deliver_cattle_mission_2",[]],
  [anyone|plyr,"village_elder_tell_deliver_cattle_mission", [],
   "I don't have time for this. Ask help from someone else.", "village_elder_deliver_cattle_mission_reject",[]],
  
  [anyone,"village_elder_tell_deliver_cattle_mission_2", [(quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount)],
   "I think {reg5} heads will suffice for a small herd.", "village_elder_tell_deliver_cattle_mission_3",[]],
  
  [anyone|plyr,"village_elder_tell_deliver_cattle_mission_3", [],
   "Then I will bring you the cattle you need.", "village_elder_deliver_cattle_mission_accept",[]],
  [anyone|plyr,"village_elder_tell_deliver_cattle_mission_3", [],
   "I am afraid I don't have time for this. You'll need to find help elsewhere.", "village_elder_deliver_cattle_mission_reject",[]],

  [anyone,"village_elder_deliver_cattle_mission_accept", [], "Thank you, {sir/madam}. We'll be praying for you night and day.", "close_window",
   [(assign, "$g_leave_encounter",1),
    (call_script, "script_change_player_relation_with_center", "$current_town", 3),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],
  
  [anyone,"village_elder_deliver_cattle_mission_reject", [], "Yes {sir/madam}, of course. I am sorry if I have bothered you with our troubles.", "close_window",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    ]],

  [anyone,"village_elder_tell_mission", [], "Thank you, {sir/madam}, but we do not really need anything right now.", "village_elder_pretalk",[]],

##  [anyone|plyr,"village_elder_mission_told", [], "TODO: As you wish sir. You can count on me.", "village_elder_mission_accepted",[]],
##  [anyone|plyr,"village_elder_mission_told", [], "TODO: I'm afraid I can't carry out this mission right now, sir.", "village_elder_mission_rejected",[]],
##
##  [anyone,"village_elder_mission_accepted", [], "TODO: Excellent. Do this {playername}. I really have high hopes for you.", "close_window",
##   [(assign, "$g_leave_encounter",1),
##    (try_begin),
##    #TODO: Add quest initializations here
##    (try_end),
##    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
##    ]],
  
##  [anyone,"village_elder_mission_rejected", [], "TODO: Is that so? Perhaps you are not up for the task anyway...", "close_window",
##   [(assign, "$g_leave_encounter",1),
##    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
##    (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
##    ]],




#Goods Merchants
  
  [anyone ,"start", [(is_between,"$g_talk_troop",goods_merchants_begin,goods_merchants_end),
                     (party_slot_eq, "$current_town", slot_town_lord, "trp_player")],
   "{My lord/my lady}, you honour my humble shop with your presence.", "goods_merchant_talk",[]],
  [anyone ,"start", [(is_between,"$g_talk_troop",goods_merchants_begin,goods_merchants_end)],
   "Welcome {sir/madam}. What can I do for you?", "goods_merchant_talk",[]],

#  [trp_salt_mine_merchant,"start", [], "Hello.", "goods_merchant_talk",[]],

#  [anyone,"merchant_begin", [], " What can I do for you?", "goods_merchant_talk",[]],

#  [anyone,"goods_merchant_pretalk", [], "Anything else?", "goods_merchant_talk",[]],

  [anyone|plyr,"goods_merchant_talk", [], "I want to buy a few items... and perhaps sell some.", "goods_trade_requested",[]],
  [anyone,"goods_trade_requested", [], "Sure, sure... Here, have a look at my stock...", "goods_trade_completed",[[change_screen_trade]]],
  [anyone,"goods_trade_completed", [], "Anything else?", "goods_merchant_talk",[]],

  [anyone|plyr,"goods_merchant_talk", [], "Nothing. Thanks.", "close_window",[]],

  

#############################################################################
#### ARENA MASTERS
#############################################################################
  [anyone ,"start", [(store_conversation_troop,reg(1)),
                     (is_between,reg(1),arena_masters_begin,arena_masters_end),
                     (assign, "$arena_reward_asked", 0), #set some variables.
                     (assign, "$arena_tournaments_asked", 0),
                     (eq,1,0),
                     ],
   ".", "arena_intro_1",[]],
  [anyone ,"start", [(store_conversation_troop,reg(1)),
                     (is_between,reg(1),arena_masters_begin,arena_masters_end),
                     (eq,"$arena_master_first_talk", 0),
                     ],
   "Good day friend. If you came to watch the tournaments you came in vain. There won't be a tournament here anytime soon.", "arena_intro_1",[(assign,"$arena_master_first_talk", 1)]],
  [anyone|plyr,"arena_intro_1", [], "Tournaments? So they hold the tournaments here...", "arena_intro_2",[]],
  [anyone,"arena_intro_2", [], "Yes. You should see this place during one of the tournament fights.\
 Everyone from the town and nearby villages comes here. The crowd becomes mad with excitement.\
 Anyway, as I said, there won't be an event here soon, so there isn't much to see.\
 Except, there is an official duel every now and then, and  of course we have melee fights almost every day.", "arena_intro_3",[]],
  [anyone|plyr,"arena_intro_3", [], "Tell me about the melee fights.", "arena_training_melee_intro",[]],
  [anyone,"arena_training_melee_intro", [], "The fighters and knights get bored waiting for the next tournament,\
 so they have invented the training melee. It is a simple idea really.\
 Fighters jump into the arena with a weapon. There are no rules, no teams.\
 Everyone beats at each other until there is only fighter left standing.\
 Sounds like fun, eh?", "arena_training_melee_intro_2",[]],
  [anyone|plyr,"arena_training_melee_intro_2", [(eq, "$arena_reward_asked", 0)], "Is there a reward?", "arena_training_melee_intro_reward",[(assign, "$arena_reward_asked", 1)]],
  [anyone,"arena_training_melee_intro_reward", [(assign, reg1, arena_tier1_opponents_to_beat),(assign, reg11, arena_tier1_prize),
      (assign, reg2, arena_tier2_opponents_to_beat),(assign, reg12, arena_tier2_prize),
      (assign, reg3, arena_tier3_opponents_to_beat),(assign, reg13, arena_tier3_prize),
      (assign, reg4, arena_tier4_opponents_to_beat),(assign, reg14, arena_tier4_prize),
      (assign, reg15, arena_grand_prize)
    ], "There is, actually. Some of the wealthy townsmen offer prizes for those fighters who show great skill in the fights.\
 If you can beat {reg1} opponents before going down, you'll earn {reg11} denars. You'll get {reg12} denars for striking down at least {reg2} opponents,\
 {reg13} denars if you can defeat {reg3} opponents, and {reg14} denars if you can survive long enough to beat {reg4} opponents.\
 If you can manage to be the last {man/fighter} standing, you'll earn the great prize of the fights, {reg15} denars. Sounds good, eh?", "arena_training_melee_intro_2",[(assign, "$arena_tournaments_asked", 1),]],
  [anyone,"arena_training_melee_explain_reward", [
      (assign, reg1, arena_tier1_opponents_to_beat),(assign, reg11, arena_tier1_prize),
      (assign, reg2, arena_tier2_opponents_to_beat),(assign, reg12, arena_tier2_prize),
      (assign, reg3, arena_tier3_opponents_to_beat),(assign, reg13, arena_tier3_prize),
      (assign, reg4, arena_tier4_opponents_to_beat),(assign, reg14, arena_tier4_prize),
      (assign, reg15, arena_grand_prize)
      ], "Some of the wealthy townsmen offer prizes for those fighters who show great skill in the fights.\
 If you can beat {reg1} opponents before going down, you'll earn {reg11} denars. You'll get {reg12} denars for striking down at least {reg2} opponents,\
 {reg13} denars if you can defeat {reg3} opponents, and {reg14} denars if you can survive long enough to beat {reg4} opponents.\
 If you can manage to be the last {man/fighter} standing, you'll earn the great prize of the fights, {reg15} denars. Sounds good, eh?", "arena_master_melee_pretalk",[]],
  [anyone|plyr,"arena_training_melee_intro_2", [], "Can I join too?", "arena_training_melee_intro_3",[]],
  [anyone,"arena_training_melee_intro_3", [], "Ha ha. You would have to be out of your mind not to. Of course. The melee fights are open to all.\
 Actually there is going to be a fight soon. You can go and hop in if you want to.", "arena_master_melee_talk",[]],


  [anyone ,"start", [(store_conversation_troop,reg(1)),
                     (is_between,reg(1),arena_masters_begin,arena_masters_end),
                     (eq,"$g_talk_troop_met", 0),
                     ],
   "Hello. You seem to be new here. Care to share your name?", "arena_master_intro_1",[]],
  [anyone|plyr,"arena_master_intro_1", [], "I am {playername}.", "arena_master_intro_2",[]],
  [anyone,"arena_master_intro_2", [(store_encountered_party,reg(2)),(str_store_party_name,1,reg(2))],
   "Well met {playername}. I am the master of the tournaments here at {s1}. Talk to me if you want to join the fights.", "arena_master_pre_talk",[]],


  [anyone|auto_proceed ,"start", [(store_conversation_troop,reg(1)),(is_between,reg(1),arena_masters_begin,arena_masters_end),
                     (eq, "$last_training_fight_town", "$current_town"),
                     (store_current_hours,":cur_hours"),
                     (val_add, ":cur_hours", -4),
                     (lt, ":cur_hours", "$training_fight_time")],
   ".", "arena_master_fight_result",[(assign, "$arena_reward_asked", 0)]],

  [anyone ,"arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (eq, "$g_arena_training_kills", 0)
     ],
   "Ha-ha, that's quite the bruise you're sporting. But don't worry; everybody gets trounced once in awhile. The important thing is to pick yourself up, dust yourself off and keep fighting. That's what champions do.", "arena_master_pre_talk",[(assign, "$last_training_fight_town", -1)]],

  [anyone ,"arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (lt, "$g_arena_training_kills", arena_tier1_opponents_to_beat),
     (assign, reg8, "$g_arena_training_kills")
     ],
   "Hey, you managed to take down {reg8} opponents. Not bad. But that won't bring you any prize money.\
 Now, if I were you, I would go back there and show everyone what I can do...", "arena_master_pre_talk",[(assign, "$last_training_fight_town", -1)]],

  [anyone ,"arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (lt, "$g_arena_training_kills", arena_tier2_opponents_to_beat),
     (assign, reg8, "$g_arena_training_kills"),
     (assign, reg10, arena_tier1_prize),
     ],
   "You put up quite a good fight there. Good moves. You definitely show promise.\
 And you earned a prize of {reg10} denars for knocking down {reg8} opponents.", "arena_master_pre_talk",[
     (call_script, "script_troop_add_gold", "trp_player",arena_tier1_prize),
     (add_xp_to_troop,5,"trp_player"),
     (assign, "$last_training_fight_town", -1)]],

  [anyone ,"arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (lt, "$g_arena_training_kills", arena_tier3_opponents_to_beat),
     (assign, reg8, "$g_arena_training_kills"),
     (assign, reg10, arena_tier2_prize),
     (assign, reg12, arena_tier2_opponents_to_beat),
     ],
   "That was a good fight you put up there. You managed to take down no less than {reg8} opponents.\
 And of course, you earned a prize money of {reg10} denars.", "arena_master_pre_talk",[
     (call_script, "script_troop_add_gold", "trp_player",arena_tier2_prize),
     (add_xp_to_troop,10,"trp_player"),
     (assign, "$last_training_fight_town", -1)]],

  [anyone ,"arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (lt, "$g_arena_training_kills", arena_tier4_opponents_to_beat),
     (assign, reg8, "$g_arena_training_kills"),
     (assign, reg10, arena_tier3_prize)
     ],
   "Your performance was amazing! You are without doubt a very skilled fighter.\
 Not everyone can knock down {reg8} people in the fights. Of course you deserve a prize with that performance: {reg10} denars. Nice, eh?", "arena_master_pre_talk",[
     (call_script, "script_troop_add_gold", "trp_player",arena_tier3_prize),
     (add_xp_to_troop,10,"trp_player"),
     (assign, "$last_training_fight_town", -1)]],

  [anyone ,"arena_master_fight_result",
   [
     (eq, "$g_arena_training_won", 0),
     (assign, reg8, "$g_arena_training_kills"),
     (assign, reg10, arena_tier4_prize),
     ],
   "That was damned good fighting, {playername}. You have very good moves, excellent tactics.\
 And you earned a prize of {reg10} denars for knocking down {reg8} opponents.", "arena_master_pre_talk",
   [
     (call_script, "script_troop_add_gold", "trp_player",arena_tier4_prize),
     (add_xp_to_troop,10,"trp_player"),
     (assign, "$last_training_fight_town", -1),
     ]],

  [anyone ,"arena_master_fight_result", [(assign, reg10, arena_grand_prize)],
   "Congratulations champion! Your fight there was something to remember! You managed to be the last fighter standing beating down everyone else. And of course you won the grand prize of the fights: {reg10} denars.", "arena_master_pre_talk",[
     (call_script, "script_troop_add_gold", "trp_player",arena_grand_prize),
     (add_xp_to_troop,200,"trp_player"),
     (assign, "$last_training_fight_town", -1)]],


  [anyone ,"start", [(store_conversation_troop,reg(1)),(is_between,reg(1),arena_masters_begin,arena_masters_end)],
   "Hello {playername}. Good to see you again.", "arena_master_pre_talk",[(assign, "$arena_reward_asked", 0)]],
  

  [anyone,"arena_master_pre_talk", [], "What would you like to do?", "arena_master_talk",[]],


#  [anyone|plyr,"arena_master_talk", [], "About the arena fights...", "arena_master_melee",[]],
  [anyone|plyr,"arena_master_talk", [], "About the melee fights...", "arena_master_melee_pretalk",[]],
  [anyone|plyr,"arena_master_talk", [(eq, "$arena_tournaments_asked", 0)], "Will there be a tournament in nearby towns soon?", "arena_master_ask_tournaments",[(assign, "$arena_tournaments_asked", 1)]],
  [anyone|plyr,"arena_master_talk", [], "I need to leave now. Good bye.", "close_window",[]],

  [anyone,"arena_master_ask_tournaments", [], "{reg2?There won't be any tournaments any time soon.:{reg1?Tournaments are:A tournament is} going to be held at {s15}.}", "arena_master_talk",
   [
       (assign, ":num_tournaments", 0),
       (try_for_range_backwards, ":town_no", towns_begin, towns_end),
         (party_slot_ge, ":town_no", slot_town_has_tournament, 1),
         (val_add, ":num_tournaments", 1),
         (try_begin),
           (eq, ":num_tournaments", 1),
           (str_store_party_name, s15, ":town_no"),
         (else_try),
           (str_store_party_name, s16, ":town_no"),
           (eq, ":num_tournaments", 2),
           (str_store_string, s15, "@{s16} and {s15}"),
         (else_try),
           (str_store_string, s15, "@{s16}, {s15}"),
         (try_end),
       (try_end),
       (try_begin),
         (eq, ":num_tournaments", 0),
         (assign, reg2, 1),
       (else_try),
         (assign, reg2, 0),
         (store_sub, reg1, ":num_tournaments", 1),
       (try_end),
   ]],

  [anyone,"arena_master_melee_pretalk", [], "There will be a fight here soon. You can go and jump in if you like.", "arena_master_melee_talk",[]],
  [anyone|plyr,"arena_master_melee_talk", [], "Good. That's what I am going to do.", "close_window",
   [
    (assign, "$last_training_fight_town", "$current_town"),
    (store_current_hours,"$training_fight_time"),
    (assign, "$g_mt_mode", abm_training),
    (party_get_slot, ":scene","$current_town",slot_town_arena),
    (modify_visitors_at_site,":scene"),
    (reset_visitors),
    (store_random_in_range, "$g_player_entry_point", 32, 40),
    (set_visitor, "$g_player_entry_point", "trp_player"),
    (set_jump_mission,"mt_arena_melee_fight"),
    (jump_to_scene, ":scene"),
    ]],
  [anyone|plyr,"arena_master_melee_talk", [], "Thanks. But I will give my bruises some time to heal.", "arena_master_melee_reject",[]],
  [anyone,"arena_master_melee_reject", [], "Good {man/girl}. That's clever of you.", "arena_master_pre_talk",[]],

  [anyone|plyr,"arena_master_melee_talk", [(eq, "$arena_reward_asked", 0)], "Actually, can you tell me about the rewards again?", "arena_training_melee_explain_reward",[(assign, "$arena_reward_asked", 1)]],


######################################################################################
  [trp_galeas,"start", [], "Hello {boy/girl}. If you have any prisoners, I will be happy to buy them from you.", "galeas_talk",[]],

  [trp_galeas|plyr,"galeas_talk",
   [[store_num_regular_prisoners,reg(0)],[ge,reg(0),1]],
   "Then you'd better bring your purse. I have got prisoners to sell.", "galeas_sell_prisoners",[]],
  [trp_galeas|plyr,"galeas_talk",[], "Not this time. Good-bye.", "close_window",[]],
  [trp_galeas,"galeas_sell_prisoners", [],
  "Let me see what you have...", "galeas_sell_prisoners_2",
   [[change_screen_trade_prisoners]]],
  [trp_galeas, "galeas_sell_prisoners_2", [], "You take more prisoners, bring them to me. I will pay well.", "close_window",[]],

##  [party_tpl|pt_refugees,"start", [], "We have been driven out of our homes because of this war.", "close_window",[(assign, "$g_leave_encounter",1)]],
##  [party_tpl|pt_farmers,"start", [], "We are just simple farmers.", "close_window",[(assign, "$g_leave_encounter",1)]],



# Ryan BEGIN
  [party_tpl|pt_mountain_bandits|auto_proceed,"start", [(eq,"$talk_context",tc_party_encounter),(encountered_party_is_attacker)],
   "Warning: This line should never display.", "bandit_introduce",[]],
  [party_tpl|pt_forest_bandits|auto_proceed,"start", [(eq,"$talk_context",tc_party_encounter),(encountered_party_is_attacker)],
   "Warning: This line should never display.", "bandit_introduce",[]],
  [anyone,"bandit_introduce", [
      (store_random_in_range, ":rand", 11, 15),
        (str_store_string, s11, "@I can smell a fat purse a mile away. Methinks yours could do with some lightening, eh?"),
        (str_store_string, s12, "@Why, it be another traveller, chance met upon the road! I should warn you, country here's a mite dangerous for a good {fellow/woman} like you. But for a small donation my boys and I'll make sure you get rightways to your destination, eh?"),
        (str_store_string, s13, "@Well well, look at this! You'd best start coughing up some silver, friend, or me and my boys'll have to break you."),
		(str_store_string, s14, "@There's a toll for passin' through this land, payable to us, so if you don't mind we'll just be collectin' our due from your purse..."),
        (str_store_string_reg, s5, ":rand"),
    ], "{s5}", "bandit_talk",[(play_sound,"snd_encounter_bandits")]],
  [anyone|plyr,"bandit_talk", [], "I'll give you nothing but cold steel, you scum!", "close_window",[[encounter_attack]]],
  [anyone|plyr,"bandit_talk", [], "There's no need to fight. I can pay for free passage.", "bandit_barter",[]],
  [anyone,"bandit_barter",
   [(store_relation, ":bandit_relation", "fac_player_faction", "$g_encountered_party_faction"),
    (ge, ":bandit_relation", -50),
    (store_mul, "$bandit_tribute", ":bandit_relation", ":bandit_relation"),
    (val_div, "$bandit_tribute", 70),
    (val_add, "$bandit_tribute", 100),
    (val_mul, "$bandit_tribute", 10),
    (assign, reg5, "$bandit_tribute")
    ], "Silver without blood, that's our favourite kind. Pay us {reg5} denars and we'll let you be on your way.", "bandit_barter_2",[]],
  [anyone|plyr,"bandit_barter_2", [[store_troop_gold,reg(2)],[ge,reg(2),"$bandit_tribute"],[assign,reg(5),"$bandit_tribute"]],
   "Very well, take it.", "bandit_barter_3a",[[troop_remove_gold, "trp_player","$bandit_tribute"]]],
  [anyone|plyr,"bandit_barter_2", [],
   "I don't have that much money with me", "bandit_barter_3b",[]],
  [anyone,"bandit_barter_3b", [],
   "That's too bad. I guess we'll just have to sell you into slavery. Take {him/her}, lads!", "close_window",[[encounter_attack]]],

  [anyone,"bandit_barter", [],
   "Hey, I've heard of you! You slaughter us freebooters like dogs, and now you expect us to let you go for a few stinking coins?\
 Forget it. You gave us no quarter, and you'll get none from us.", "close_window",[]],



  [anyone,"bandit_barter_3a", [], "Heh, that wasn't so hard, was it? All right, we'll let you go now. Be off.", "close_window",[
    (store_current_hours,":protected_until"),
    (val_add, ":protected_until", 72),
    (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,":protected_until"),
    (party_ignore_player, "$g_encountered_party", 72),
    (assign, "$g_leave_encounter",1)
    ]],
  

  [anyone,"start", [(this_or_next|eq, "$g_encountered_party_template", "pt_mountain_bandits"),(eq, "$g_encountered_party_template", "pt_forest_bandits")],
   "Eh? What is it?", "bandit_meet",[]],

  [anyone|plyr,"bandit_meet", [], "Your luck has run out, wretch. Prepare to die!", "bandit_attack",
   [
    (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until, 0),
    ]],
  
  [anyone,"bandit_attack", [
      (store_random_in_range, ":rand", 11, 15),
        (str_store_string, s11, "@Another fool come to throw {him/her}self on my weapon, eh? Fine, let's fight!"),
        (str_store_string, s12, "@We're not afraid of you, {sirrah/wench}. Time to bust some heads!"),
        (str_store_string, s13, "@That was a mistake. Now I'm going to have to make your death long and painful."),
        (str_store_string, s14, "@Brave words. Let's see you back them up with deeds, cur!"),
        (str_store_string_reg, s5, ":rand"),
      ], "{s5}", "close_window",[]],

  [anyone|plyr,"bandit_meet", [], "Never mind, I have no business with you.", "close_window",[(assign, "$g_leave_encounter", 1)]],
# Ryan END
  
#Quest dialogs
  
  [party_tpl|pt_troublesome_bandits,"start", [(quest_slot_eq, "qst_troublesome_bandits", slot_quest_target_party, "$g_encountered_party")],
   "This must be your unlucky day indeed. We are the baddest guys you could have run into in these parts...", "troublesome_bandits_intro_1",[]],
  [anyone|plyr,"troublesome_bandits_intro_1", [],
   "Heh. For me, you are nothing more than walking money bags.\
 A merchant in {s1} offered me good money for your heads.",
   "troublesome_bandits_intro_2", [(quest_get_slot, ":quest_giver_center", "qst_troublesome_bandits", slot_quest_giver_center),
                                   (str_store_party_name, s1, ":quest_giver_center")
                                   ]],
  [anyone,"troublesome_bandits_intro_2", [],
   "A bounty hunter! ... I hate bounty hunters! Kill {him/her}! Kill {him/her} now!", "close_window",[(encounter_attack)]],
 
 

  [party_tpl|pt_rescued_prisoners,"start", [(eq,"$talk_context",tc_party_encounter)], "Do you want us to follow you?", "disbanded_troop_ask",[]],
  [anyone|plyr,"disbanded_troop_ask", [], "Yes. Let us ride together.", "disbanded_troop_join",[]],
  [anyone|plyr,"disbanded_troop_ask", [], "No. Not at this time.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone,"disbanded_troop_join", [[neg|party_can_join]], "Unfortunately. You do not have room in your party for us.", "close_window",[(assign, "$g_leave_encounter",1)]],
  [anyone,"disbanded_troop_join", [], "We are at your command.", "close_window",[[party_join],(assign, "$g_leave_encounter",1)]],
   
  [party_tpl|pt_enemy,"start", [(eq,"$talk_context",tc_party_encounter)], "You will not capture me again. Not this time.", "enemy_talk_1",[]],
  [party_tpl|pt_enemy|plyr,"enemy_talk_1", [], "You don't have a chance against me. Give up.", "enemy_talk_2",[]],
  [party_tpl|pt_enemy,"enemy_talk_2", [], "I will give up when you are dead!", "close_window",[[encounter_attack]]],


  [anyone|plyr,"prisoner_chat", [], "Do not try running away or trying something stupid. I will be watching you.", "prisoner_chat_2",[]],
  [anyone,"prisoner_chat_2", [], "No, I swear I won't.", "close_window",[]],


  [anyone,"start", [(party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
                    (this_or_next|is_between,"$g_talk_troop",weapon_merchants_begin,weapon_merchants_end),
                    (this_or_next|is_between,"$g_talk_troop",armor_merchants_begin, armor_merchants_end),
                    (             is_between,"$g_talk_troop",horse_merchants_begin, horse_merchants_end),
                    ],
   "Greetings, {your lordship/my lady}. How can I serve you today?", "town_merchant_talk",[]],

  [anyone,"start", [(this_or_next|is_between,"$g_talk_troop",weapon_merchants_begin,weapon_merchants_end),
                    (this_or_next|is_between,"$g_talk_troop",armor_merchants_begin, armor_merchants_end),
                    (             is_between,"$g_talk_troop",horse_merchants_begin, horse_merchants_end)], "Good day. What can I do for you?", "town_merchant_talk",[]],

  [anyone|plyr,"town_merchant_talk", [(is_between,"$g_talk_troop",weapon_merchants_begin,weapon_merchants_end)],
   "I want to buy a new weapon. Show me your wares.", "trade_requested_weapons",[]],
  [anyone|plyr,"town_merchant_talk", [(is_between,"$g_talk_troop",armor_merchants_begin,armor_merchants_end)],
   "I am looking for some equipment. Show me what you have.", "trade_requested_armor",[]],
  [anyone|plyr,"town_merchant_talk", [(is_between,"$g_talk_troop",horse_merchants_begin,horse_merchants_end)],
   "I am thinking of buying a horse.", "trade_requested_horse",[]],

  [anyone,"trade_requested_weapons", [], "Ah, yes {sir/madam}. These arms are the best you'll find anywhere.", "merchant_trade",[[change_screen_trade]]],
  [anyone,"trade_requested_armor", [], "Of course, {sir/madam}. You won't find better quality armour than these in all Middle Earth.", "merchant_trade",[[change_screen_trade]]],
  [anyone,"trade_requested_horse", [], "You have a fine eye for horses, {sir/madam}. You won't find better beasts than these anywhere else.", "merchant_trade",[[change_screen_trade]]],


  [anyone,"merchant_trade", [], "Anything else?", "town_merchant_talk",[]],
  [anyone|plyr,"town_merchant_talk", [], "Tell me. What are people talking about these days?", "merchant_gossip",[]],
  [anyone,"merchant_gossip", [ (store_troop_faction,":faction","$g_talk_troop"),     # random faction related rumors
                               (faction_get_slot,":rumors_begin",":faction",slot_faction_rumors_begin),
                               (faction_get_slot,":rumors_end"  ,":faction",slot_faction_rumors_end),
							   (store_random_in_range,":string",":rumors_begin",":rumors_end"),
							   (str_store_string, s64, ":string"),
							   (assign, reg0,":rumors_begin"), (assign, reg1,":rumors_end"), 
							 ],"{s64}^Strings chosen from {reg0} to {reg1}" , "town_merchant_talk",[]],
  [anyone|plyr,"town_merchant_talk", [], "Good-bye.", "close_window",[]],




##  [anyone,"start", [(eq, "$talk_context", 0),
##                    (is_between,"$g_talk_troop",walkers_begin, walkers_end),
##                    (eq, "$sneaked_into_town",1),
##                     ], "Stay away beggar!", "close_window",[]],
  
  [anyone,"start", [(eq, "$talk_context", 0),
                    (agent_get_entry_no, ":entry", "$g_talk_agent"),
					(is_between,":entry",town_walker_entries_start, 40),
#					(is_between,"$g_talk_troop",walkers_begin, walkers_end),
                    (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
                     ], "My {lord/lady}?", "town_dweller_talk",[(assign, "$welfare_inquired",0),(assign, "$rumors_inquired",0),(assign, "$info_inquired",0)]],

  [anyone,"start", [(eq, "$talk_context", 0),
                    (agent_get_entry_no, ":entry", "$g_talk_agent"),
					(is_between,":entry",town_walker_entries_start, 40),
#                    (is_between,"$g_talk_troop",walkers_begin, walkers_end),
                     ], "Good day, Commander.", "town_dweller_talk",[(assign, "$welfare_inquired", 0),(assign, "$rumors_inquired",0),(assign, "$info_inquired",0)]],

  [anyone|plyr,"town_dweller_talk", [(check_quest_active, "qst_hunt_down_fugitive"),
                                     (neg|check_quest_concluded, "qst_hunt_down_fugitive"),
                                      (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
                                      (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
                                      (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
                                      (str_store_string, s4, s50),
                                      ],
   "I am looking for a man by the name of {s4}. I was told he may be hiding here.", "town_dweller_ask_fugitive",[]],
  [anyone ,"town_dweller_ask_fugitive", [],
   "Strangers come and go to our village, {sir/madam}. If he is hiding here, you will surely find him if you look around.", "close_window",[]],

# Ryan BEGIN
  [anyone|plyr,"town_dweller_talk",
   [
     (eq, 1, 0),
     (check_quest_active, "qst_meet_spy_in_enemy_town"),
     (neg|check_quest_succeeded, "qst_meet_spy_in_enemy_town"),
     (quest_slot_eq, "qst_meet_spy_in_enemy_town", slot_quest_target_center, "$current_town"),
     (str_store_item_name,s5,"$spy_item_worn"),
     ],
   "Pardon me, but is that a {s5} you're wearing?", "town_dweller_quest_meet_spy_in_enemy_town_ask_item",
   [
     ]],
  [anyone, "town_dweller_quest_meet_spy_in_enemy_town_ask_item", [
     (str_store_item_name,s5,"$spy_item_worn"),

     (try_begin),
     (troop_has_item_equipped,"$g_talk_troop","$spy_item_worn"),
     (str_store_string,s6,"@A {s5}? Well... Yes, I suppose it is. What a strange thing to ask."),
     (else_try),
     (str_store_string,s6,"@Eh? No, it most certainly is not a {s5}. I'd start questioning my eyesight if I were you."),
     (try_end),
  ],
   "{s6}", "town_dweller_talk",[]],

  [anyone|plyr|repeat_for_100,"town_dweller_talk",
   [
     (store_repeat_object,":object"),
     (lt,":object",4), # repeat only 4 times

     (check_quest_active, "qst_meet_spy_in_enemy_town"),
     (neg|check_quest_succeeded, "qst_meet_spy_in_enemy_town"),
     (quest_slot_eq, "qst_meet_spy_in_enemy_town", slot_quest_target_center, "$current_town"),

     (store_add,":string",":object","str_secret_sign_1"),
     (str_store_string, s4, ":string"),
     ],
   "{s4}", "town_dweller_quest_meet_spy_in_enemy_town",
   [
     (store_repeat_object,":object"),
     (assign, "$temp", ":object"),
     ]],

  [anyone ,"town_dweller_quest_meet_spy_in_enemy_town",
   [
     (call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
     (assign, ":walker_type", reg0),
     (eq, ":walker_type", walkert_spy),
     (quest_get_slot, ":secret_sign", "qst_meet_spy_in_enemy_town", slot_quest_target_amount),
     (val_sub, ":secret_sign", secret_signs_begin),
     (eq, ":secret_sign", "$temp"),
     (store_add, ":countersign", ":secret_sign", countersigns_begin),
     (str_store_string, s4, ":countersign"),
     ],
   "{s4}", "town_dweller_quest_meet_spy_in_enemy_town_know",[]],

  [anyone, "town_dweller_quest_meet_spy_in_enemy_town", [],
   "Eh? What kind of gibberish is that?", "town_dweller_quest_meet_spy_in_enemy_town_dont_know",[]],

  [anyone|plyr, "town_dweller_quest_meet_spy_in_enemy_town_dont_know", [],
   "Never mind.", "close_window",[]],

  [anyone|plyr, "town_dweller_quest_meet_spy_in_enemy_town_know", [
     (quest_get_slot, ":quest_giver", "qst_meet_spy_in_enemy_town", slot_quest_giver_troop),
     (str_store_troop_name, s4, ":quest_giver"),
  ],
   "{s4} sent me to collect your reports. Do you have them with you?", "town_dweller_quest_meet_spy_in_enemy_town_chat",[]],

  [anyone, "town_dweller_quest_meet_spy_in_enemy_town_chat", [
     (quest_get_slot, ":quest_giver", "qst_meet_spy_in_enemy_town", slot_quest_giver_troop),
     (str_store_troop_name, s4, ":quest_giver"),
  ],
   "I've been expecting you. Here they are, make sure they reach {s4} intact and without delay.", "town_dweller_quest_meet_spy_in_enemy_town_chat_2",[
     (call_script, "script_succeed_quest", "qst_meet_spy_in_enemy_town"),
     (call_script, "script_center_remove_walker_type_from_walkers", "$current_town", walkert_spy),
   ]],

  [anyone|plyr, "town_dweller_quest_meet_spy_in_enemy_town_chat_2", [],
   "Farewell.", "close_window",
   [
     ]],
# Ryan END  

  [anyone|plyr,"town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_village),
                                     (eq, "$info_inquired", 0)], "What can you tell me about this village?", "town_dweller_ask_info",[(assign, "$info_inquired", 1)]],
  [anyone|plyr,"town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_town),
                                     (eq, "$info_inquired", 0)], "What can you tell me about this town?", "town_dweller_ask_info",[(assign, "$info_inquired", 1)]],

  [anyone,"town_dweller_ask_info", [(str_store_party_name, s5, "$current_town"),
                                    (assign, reg4, 0),
                                    (try_begin),
                                      (party_slot_eq, "$current_town", slot_party_type, spt_town),
                                      (assign, reg4, 1),
                                    (try_end),
                                    (str_store_string, s6, "@This is the {reg4?town:village} of {s5}, {sir/madam}."),
                                    (str_clear, s10),
                                    (try_begin),
                                      (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
                                      (str_store_string, s10, "@{s6} Our {reg4?town:village} and the surrounding lands belong to you of course, my {lord/lady}."),
                                    (else_try),
                                      (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
                                      (ge, ":town_lord", 0),
                                      (str_store_troop_name, s7, ":town_lord"),
                                      (store_troop_faction, ":town_lord_faction", ":town_lord"),
                                      (str_store_faction_name, s8, ":town_lord_faction"),
                                      (str_store_string, s10, "@{s6} Our {reg4?town:village} and the surrounding lands belong to {s7} of {s8}."),
                                    (try_end),
                                    (str_clear, s5),
                                    (assign, reg20, 0),
                                    (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
                                      (store_sub, ":cur_good_slot", ":cur_good", trade_goods_begin),
                                      (val_add, ":cur_good_slot", slot_town_trade_good_productions_begin),
                                      (party_get_slot, ":production", "$g_encountered_party", ":cur_good_slot"),
                                      (ge, ":production", 10),
                                      (str_store_item_name, s3, ":cur_good"),
                                      (try_begin),
                                        (eq, reg20, 0),
                                        (str_store_string, s5, s3),
                                      (else_try),
                                        (eq, reg20, 1),
                                        (str_store_string, s5, "@{s3} and {s5}"),
                                      (else_try),
                                        (str_store_string, s5, "@{s3}, {s5}"),
                                      (try_end),
                                      (val_add, reg20, 1),
                                    (try_end),
                                    (str_store_string, s11, "@{reg20?We mostly produce {s5} here:We don't produce much here these days}.\
 If you would like to learn more, you can speak with our {reg4?guildmaster:village elder}. He is nearby, right over there."),
                                    ],
   "{s10} {s11}", "close_window",[]],

  [anyone|plyr,"town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_village),
                                     (eq, "$welfare_inquired", 0)], "How is life here?", "town_dweller_ask_situation",[(assign, "$welfare_inquired", 1)]],
  [anyone|plyr,"town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_town),
                                     (eq, "$welfare_inquired", 0)], "How is life here?", "town_dweller_ask_situation",[(assign, "$welfare_inquired", 1)]],


  [anyone,"town_dweller_ask_situation", [(call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
                                         (assign, ":walker_type", reg0),
                                         (eq, ":walker_type", walkert_needs_money),
                                         (party_slot_eq, "$current_town", slot_party_type, spt_village)],
   "Disaster has struck my family, {sir/madam}. A pestilence has ruined the crops on our fields, and my poor children lie at home hungry and sick.\
 My neighbours are too poor themselves to help me.", "town_dweller_poor",[]],

  [anyone,"town_dweller_ask_situation", [(call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
                                         (assign, ":walker_type", reg0),
                                         (eq, ":walker_type", walkert_needs_money)],
   "My life is miserable, {sir/madam}. I haven't been able to find a job for months, and my poor children go to bed hungry each night.\
 My neighbours are too poor themselves to help me.", "town_dweller_poor",[]],

  [anyone|plyr,"town_dweller_poor", [(store_troop_gold, ":gold", "trp_player"),
                                     (ge, ":gold", 300),
                                     ],
   "Then take these 300 denars. I hope this will help you and your family.", "town_dweller_poor_paid",
   [(troop_remove_gold, "trp_player", 300),
    ]],

  [anyone|plyr,"town_dweller_poor", [],
   "Then you must work harder and bear your burden without complaining.", "town_dweller_poor_not_paid",[]],

  [anyone,"town_dweller_poor_not_paid", [], "Yes {sir/madam}. I will do as you say.", "close_window",[]],

  [anyone,"town_dweller_poor_paid", [], "{My lord/My good lady}. \
 You are so good and generous. I will tell everyone how you helped us.", "close_window",
   [(call_script, "script_change_player_relation_with_center", "$g_encountered_party", 1),
    (call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
    (assign, ":walker_no", reg2),
    (call_script, "script_center_set_walker_to_type", "$g_encountered_party", ":walker_no", walkert_needs_money_helped),
    ]],

  [anyone,"town_dweller_ask_situation", [(call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
                                         (assign, ":walker_type", reg0),
                                         (eq, ":walker_type", walkert_needs_money_helped)
                                         ],
   "Thank you for your kindness {sir/madam}. With your help our lives will be better. I will pray for you everyday.", "close_window",[]],

  [anyone,"town_dweller_ask_situation", [(neg|party_slot_ge, "$current_town", slot_town_prosperity, 30)],
   "Times are hard, {sir/madam}. We work hard all day and yet we go to sleep hungry most nights.", "town_dweller_talk",[]],
  
  [anyone,"town_dweller_ask_situation", [(neg|party_slot_ge, "$current_town", slot_town_prosperity, 70)],
   "Times are hard, {sir/madam}. But we must count our blessings.", "town_dweller_talk",[]],
  [anyone,"town_dweller_ask_situation", [],
   "We are not doing too badly {sir/madam}. We must count our blessings.", "town_dweller_talk",[]],

  [anyone|plyr,"town_dweller_talk", [(eq, "$rumors_inquired", 0)], "What is the latest rumor around here?", "town_dweller_ask_rumor",[(assign, "$rumors_inquired", 1)]],
  [anyone,"town_dweller_ask_rumor", [(neg|party_slot_ge, "$current_town", slot_center_player_relation, -5)], "I don't know anything that would be of interest to you.", "town_dweller_talk",[]],
  
  [anyone,"town_dweller_ask_rumor", [(store_mul, ":rumor_id", "$current_town", 197),
                                     (val_add,  ":rumor_id", "$g_talk_agent"),
                                     (call_script, "script_get_rumor_to_s61", ":rumor_id"),
                                     (gt, reg0, 0)], "{s61}", "town_dweller_talk",[]],

  [anyone,"town_dweller_ask_rumor", [], "I haven't heard anything interesting lately.", "town_dweller_talk",[]],

  [anyone|plyr,"town_dweller_talk", [], "[Leave]", "close_window",[]],

  [anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (party_slot_eq,"$current_town",slot_town_lord, "trp_player"),
                     ], "Yes {sir/madam}?", "player_castle_guard_talk",[]],
  [anyone|plyr,"player_castle_guard_talk", [], "How goes the watch, soldier?", "player_castle_guard_talk_2",[]],
  [anyone,"player_castle_guard_talk_2", [], "All is quiet {sir/madam}. Nothing to report.", "player_castle_guard_talk_3",[]],
  [anyone|plyr,"player_castle_guard_talk_3", [], "Good. Keep your eyes open.", "close_window",[]],


  [anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end),
                    (eq, "$players_kingdom", "$g_encountered_party_faction"),
                    (troop_slot_ge, "trp_player", slot_troop_renown, 100),
                    (str_store_party_name, s10, "$current_town"),
                     ], "Good day, {sir/madam}. It's nice having you here in {s10}.", "close_window",[]],

  [anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end),
                     ], "Mind your manners within the walls and we'll have no trouble.", "close_window",[]],

  [anyone,"start", [(eq, "$talk_context", tc_court_talk),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end),
                    (party_slot_eq,"$current_town",slot_town_lord, "trp_player"),
                     ], "Your orders, {my lord/my lady}?", "hall_guard_talk",[]],

  [anyone,"start", [(eq, "$talk_context", tc_court_talk),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end),
                     ], "We are not supposed to talk while on guard, {sir/madam}.", "close_window",[]],
                     
  [anyone|plyr,"hall_guard_talk", [], "Stay on duty and let me know if anyone comes to see me.", "hall_guard_duty",[]],
  [anyone,"hall_guard_duty", [], "Yes, {my lord/my lady}. As you wish.", "close_window",[]],
  
  [anyone|plyr,"hall_guard_talk", [], "I want you to arrest this man immediately!", "hall_guard_arrest",[]],
  [anyone,"hall_guard_arrest", [], "Who do you want arrested {sir/madam}?", "hall_guard_arrest_2",[]],
  [anyone|plyr,"hall_guard_arrest_2", [], "Ah, never mind my high spirits lads.", "close_window",[]],
  [anyone|plyr,"hall_guard_arrest_2", [], "Forget it. I will find another way to deal with this.", "close_window",[]],

  [anyone,"enemy_defeated", [], "Arggh! I hate this.", "close_window",[]],

  [anyone,"party_relieved", [], "Thank you for helping us against those bastards.", "close_window",[]],

  [anyone,"start", [(eq,"$talk_context", tc_party_encounter),(store_encountered_party, reg(5)),(party_get_template_id,reg(7),reg(5)),(eq,reg(7),"pt_sea_raiders")],
   "I will drink from your skull!", "battle_reason_stated",[(play_sound,"snd_encounter_sea_raiders")]],
  
######################################
# GENERIC MEMBER CHAT
######################################

   
  [anyone,"member_chat", [
      (troop_slot_eq,  "$g_talk_troop", slot_troop_upkeep_not_paid,0), # or else, incipit is different
  ], "Your orders {sir/madam}?", "regular_member_talk",[]],

  [anyone|plyr,"regular_member_talk", [], "Tell me about yourself", "view_regular_char_requested",[]],
	  
  [anyone,"view_regular_char_requested", [], "Aye {sir/madam}. Let me tell you all there is to know about me.", "do_regular_member_view_char",[[change_screen_view_character]]],
  [anyone,"do_regular_member_view_char", [], "Anything else?", "regular_member_talk",[]],

  # TLD: can disband members for Res Point (mtarini)
  
  [anyone,"member_chat", [
      (neg|troop_slot_eq, reg11, "$g_talk_troop", slot_troop_upkeep_not_paid,0), # if the troop wasn't paid last time, and it is on the leave
     (store_partner_faction, reg10),
    (str_store_faction_name, s12, reg10),
	(call_script, "script_get_troop_disband_cost", "$g_talk_troop",0,0),
 ], "It has been an honour to serve {s12} under your command, {sir/madam}.^^Now, as you know, I've been reassigned to home defence.^I shall soon leave.^^^[you will gain {reg15} Resource Pts. ({s12})]", 
  "disband_regular_member_confirm_yn",[]],

  [anyone|plyr,"regular_member_talk", [
    (troop_slot_eq, "$g_talk_troop", slot_troop_upkeep_not_paid,0), # it was paid... still player can send him away
	(call_script, "script_cf_is_troop_in_party_not_wounded", "$g_talk_troop", "p_main_party"), # not wounded 
    (store_partner_faction, reg10),
    (str_store_faction_name, s12, reg10),
  ], "Your services are now more urgent back home in {s12}, than here with me.", "disband_regular_member_confirm",[]],

  [anyone|plyr,"regular_member_talk", [
    (troop_slot_eq, "$g_talk_troop", slot_troop_upkeep_not_paid,0),  # it was paid... still player can send him away
	(call_script, "script_cf_is_troop_in_party_wounded", "$g_talk_troop", "p_main_party"),# wounded 
    (store_partner_faction, reg10),
    (str_store_faction_name, s12, reg10),
  ], "You are wounded... you should go back home in {s12}, where you can be more useful than here.", "disband_regular_member_confirm",[]],

  [anyone|plyr,"regular_member_talk", [], "Nothing. Keep moving.", "close_window",[]],
  
  [anyone,"disband_regular_member_confirm", [
	(call_script, "script_get_troop_disband_cost", "$g_talk_troop",0,0),
    (store_partner_faction, reg10),
    (str_store_faction_name, s12, reg10),
  ], "Shall I leave your command, and go back home to defend {s12}?^^[you will gain {reg15} Resource Pts ({s12})]", "disband_regular_member_confirm_yn",[]],

  [anyone|plyr,"disband_regular_member_confirm_yn", [
     (call_script,"script_store_troop_king_in_s15","$g_talk_troop"),
  ], "Yes, go there and wait further orders from {s15}. Good luck, soldier!", "close_window",[ 
	(call_script, "script_get_troop_disband_cost", "$g_talk_troop",0,0),
	(assign, ":gain", reg15),
    #(party_remove_members_wounded_first,"p_main_party","$g_talk_troop",1),
	(remove_member_from_party,"$g_talk_troop"),
	(store_partner_faction, reg10),
	(call_script, "script_add_faction_respoint", reg10, ":gain"),
  ]],

  [anyone|plyr,"disband_regular_member_confirm_yn", [
    (troop_slot_eq, "$g_talk_troop", slot_troop_upkeep_not_paid,0),
  ], "Not yet, I still need you here.", "close_window",[ ]],

 [anyone|plyr,"disband_regular_member_confirm_yn", [
    (neg|troop_slot_eq, "$g_talk_troop", slot_troop_upkeep_not_paid,0),
  ], "But you are still needed here, as well!", "disband_regular_member_insist",[ ]],

  [anyone,"disband_regular_member_insist", [ ], "I know, but my duty brings me to different battles.^I will soon leave.", "close_window",[ ]],


######################################
# GENERIC PARTY ENCOUNTER
######################################

  [anyone,"start", [(eq,"$talk_context",tc_party_encounter),
                    (gt,"$encountered_party_hostile",0),
                    (encountered_party_is_attacker),
                    ],
   "You have no chance against us. Surrender now or we will kill you all...", "party_encounter_hostile_attacker",
   [(try_begin),
      (eq,"$g_encountered_party_template","pt_steppe_bandits"),
      (play_sound, "snd_encounter_steppe_bandits"),
    (try_end)]],
  [anyone|plyr,"party_encounter_hostile_attacker", [
                    ],
   "Don't attack! We surrender.", "close_window", [(assign,"$g_player_surrenders",1)]],
#  [anyone|plyr,"party_encounter_hostile_attacker", [
#                    ],
#   "I will pay you 1000 denars if you just let us go.", "close_window", []],
  [anyone|plyr,"party_encounter_hostile_attacker", [
                    ],
   "We will fight you to the end!", "close_window", []],
  
  [anyone,"start", [(eq,"$talk_context",tc_party_encounter),
                    (neg|encountered_party_is_attacker),
                    ],
   "What do you want?", "party_encounter_hostile_defender",
   []],

  [anyone|plyr,"party_encounter_hostile_defender", [],
   "Surrender or die!", "party_encounter_hostile_ultimatum_surrender", [

       ]],

#post 0907 changes begin
  [anyone,"party_encounter_hostile_ultimatum_surrender", [],
   "{s43}", "close_window", [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_challenged_default"),
       ]],
#post 0907 changes end

  [anyone|plyr,"party_encounter_hostile_defender", [],
   "Nothing. We'll leave you in peace.", "close_window", [(assign, "$g_leave_encounter",1)]],

  [anyone,"start", [], "Surrender or die. Make your choice", "battle_reason_stated",[]],
  [anyone|plyr,"battle_reason_stated", [], "I am not afraid of you. I will fight.", "close_window",[[encounter_attack]]],

  [anyone,"start", [], "Hello. What can I do for you?", "free",[]],
  [anyone|plyr,"free", [[neg|in_meta_mission]], "Tell me about yourself", "view_char_requested",[]],
  [anyone,"view_char_requested", [], "Very well, listen to this...", "view_char",[[change_screen_view_character]]],
  [anyone,"view_char", [], "Anything else?", "free",[]],

  [anyone|plyr,"end", [], "[Done]", "close_window",[]],
  
  [anyone|plyr,"start", [], "Drop your weapons and surrender if you want to live", "threaten_1",[]],
  [anyone,"threaten_1", [], "We will fight you first", "end",[[encounter_attack]]],

#  [anyone|plyr,"free", [[partner_is_mercmaster]], "I need to hire some mercenaries.", "mercenaries_requested",[]],
#  [anyone,"mercenaries_requested", [], "I have the toughest fighters in all Calradia.", "buy_mercenaries",[[change_screen_buy_mercenaries]]],
#  [anyone,"buy_mercenaries", [], "Anything else?", "free",[]],

#  [anyone|plyr,"free", [[partner_is_recruitable]], "I need a capable sergeant like yourself. How much do you ask to work for me?", "employ_mercenary_requested",[]],
#  [anyone,"employ_mercenary_requested", [[store_mercenary_price,0],[store_mercenary_wage,1]], "I want {reg0} denars now and {reg1} denars as monthly payment.", "employ_mercenary_2",[]],
#  [anyone|plyr,"employ_mercenary_2", [], "I see I need to think of this.", "employ_mercenary_giveup",[]],
#  [anyone|plyr,"employ_mercenary_2", [[neg|hero_can_join]], "I don't have any more room in my party right now. I will talk to you again later.", "employ_mercenary_giveup",[]],
#  [anyone|plyr,"employ_mercenary_2", [[player_gold_ge,reg(0)],[hero_can_join]], "That's fine. Here's the {reg0} denars. From now on you work for me.", "employ_mercenary_commit",[[troop_remove_gold, "trp_player",reg(0)],[recruit_mercenary]]],
#  [anyone,"employ_mercenary_giveup", [], "Suits me.", "free",[]],
#  [anyone,"employ_mercenary_commit", [], "You got yourself the best fighter in the land.", "end",[]],



  [anyone|plyr,"free", [[in_meta_mission]], " Good-bye.", "close_window",[]],
  [anyone|plyr,"free", [[neg|in_meta_mission]], " [Leave]", "close_window",[]],
#  [anyone,"free", [], "NO MATCHING SENTENCE!", "close_window",[]],
]
