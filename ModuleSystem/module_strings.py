from module_constants import *

strings = [
  ("no_string", "NO STRING!"),
  ("empty_string", " "),
  ("yes", "Yes."),
  ("no", "No."),
# Strings before this point are hardwired.  
  ("blank_string", " "),
  ("error_string", "ERROR!!!ERROR!!!!ERROR!!!ERROR!!!ERROR!!!ERROR!!!!ERROR!!!ERROR!!!!ERROR!!!ERROR!!!!ERROR!!!ERROR!!!!ERROR!!!ERROR!!!!ERROR!!!ERROR!!!!!"),
##  ("none", "none"),
  ("noone", "no one"),
##  ("nothing", "nothing"),
  ("s0", "{s0}"),
  ("blank_s1", " {s1}"),
  ("reg1", "{reg1}"),
  ("s50_comma_s51", "{s50}, {s51}"),
  ("s50_and_s51", "{s50} and {s51}"),
  ("s5_s_party", "{s5}'s Party"),

  ("given_by_s1_at_s2", "Given by {s1} at {s2}"),
  ("given_by_s1_in_wilderness", "Given by {s1} whilst in the field"),
  ("s7_raiders", "{s7} Raiders"),

  ("bandits_eliminated_by_another", "The troublesome bandits have been eliminated by another party."),
  ("msg_battle_won","Battle won! Press tab key to leave..."),
  ("tutorial_map1","You are now viewing the overland map. Left-click on the map to move your party to that location, enter the selected town, or pursue the selected party. Time will pause on the overland map if your party is not moving, waiting or resting. To wait anywhere simply press and hold down the space bar."),


  ("change_color_1", "Change Color 1"),
  ("change_color_2", "Change Color 2"),
  ("change_background", "Change Background Pattern"),
  ("change_flag_type", "Change Flag Type"),
  ("change_map_flag_type", "Change Map Flag Type"),
  ("randomize", "Randomize"),
  ("sample_banner", "Sample banner:"),
  ("sample_map_banner", "Sample map banner:"),
  ("number_of_charges", "Number of charges:"),
  ("change_charge_1",       "Change Charge 1"),
  ("change_charge_1_color", "Change Charge 1 Color"),
  ("change_charge_2",       "Change Charge 2"),
  ("change_charge_2_color", "Change Charge 2 Color"),
  ("change_charge_3",       "Change Charge 3"),
  ("change_charge_3_color", "Change Charge 3 Color"),
  ("change_charge_4",       "Change Charge 4"),
  ("change_charge_4_color", "Change Charge 4 Color"),
  ("change_charge_position", "Change Charge Position"),
  ("choose_position", "Choose position:"),
  ("choose_charge", "Choose a charge:"),
  ("choose_background", "Choose background pattern:"),
  ("choose_flag_type", "Choose flag type:"),
  ("choose_map_flag_type", "Choose map flag type:"),
  ("choose_color", "Choose color:"),
  ("accept", "Accept"),
  ("charge_no_1", "Charge #1:"),
  ("charge_no_2", "Charge #2:"),
  ("charge_no_3", "Charge #3:"),
  ("charge_no_4", "Charge #4:"),
  ("change", "Change"),
  ("plus", "+"),
  ("minus", "-"),
  ("color_no_1", "Color #1:"),
  ("color_no_2", "Color #2:"),
  ("charge", "Charge"),
  ("color", "Color"),
  ("flip_horizontal", "Flip Horizontal"),
  ("flip_vertical", "Flip Vertical"),
  ("hold_fire", "Hold Fire"),
  ("blunt_hold_fire", "Blunt / Hold Fire"),
  
  
##  ("tutorial_camp1","This is training ground where you can learn the basics of the game. Use A, S, D, W keys to move and the mouse to look around."),
##  ("tutorial_camp2","F is the action key. You can open doors, talk to people and pick up objects with F key. If you wish to leave a town or retreat from a battle, press the TAB key."),
##  ("tutorial_camp3","Training Ground Master wishes to speak with you about your training. Go near him, look at him and press F when you see the word 'Talk' under his name. "),
##  ("tutorial_camp4","To see the in-game menu, press the Escape key. If you select Options, and then Controls from the in-game menu, you can see a complete list of key bindings."),
##  ("tutorial_camp6","You've received your first quest! You can take a look at your current quests by pressing the Q key. Do it now and check the details of your quest."),
##  ("tutorial_camp7","You've completed your quest! Go near Training Ground Master and speak with him about your reward."),
##  ("tutorial_camp8","You've gained some experience and weapon points! Press C key to view your character and increase your weapon proficiencies."),
##  ("tutorial_camp9","Congratulations! You've finished the tutorial of Mount&Blade. Press TAB key to leave the training ground."),

##  ("tutorial_enter_melee", "You are entering the melee weapon training area. The chest nearby contains various weapons which you can experiment with. If you wish to quit this tutorial, press TAB key."),
##  ("tutorial_enter_ranged", "You are entering the ranged weapon training area.  The chest nearby contains various ranged weapons which you can experiment with. If you wish to quit this tutorial, press TAB key."),
##  ("tutorial_enter_mounted", "You are entering the mounted training area. Here, you can try different kinds of weapons while riding a horse. If you wish to quit this tutorial, press TAB key."),

#  ("tutorial_usage_sword", "Sword is a very versatile weapon which is very fast in both attack and defense. Usage of one handed swords are affected by your one handed weapon proficiency. Focus on the sword and press F key to pick it up."),
#  ("tutorial_usage_axe", "Axe is a heavy (and therefore slow) weapon which can deal high damage to the opponent. Usage of one handed axes are affected by your one handed weapon proficiency. Focus on the axe and press F key to pick it up."),
#  ("tutorial_usage_club", "Club is a blunt weapon which deals less damage to the opponent than any other one handed weapon, but it knocks you opponents unconscious so that you can take them as a prisoner. Usage of clubs are affected by your one handed weapon proficiency. Focus on the club and press F key to pick it up."),
#  ("tutorial_usage_battle_axe", "Battle axe is a long weapon and it can deal high damage to the opponent. Usage of battle axes are affected by your two handed weapon proficiency. Focus on the battle axe and press F key to pick it up."),
#  ("tutorial_usage_spear", "Spear is a very long weapon which lets the wielder to strike the opponent earlier. Usage of the spears are affected by your polearm proficiency. Focus on the spear and press F key to pick it up."),
#  ("tutorial_usage_short_bow", "Short bow is a common ranged weapon which is easy to reload but hard to master at. Usage of short bows are affected by your archery proficiency. Focus on the short bow and arrows and press F key to pick them up."),
#  ("tutorial_usage_crossbow", "Crossbow is a heavy ranged weapon which is easy to use and deals high amount of damage to the opponent. Usage of crossbows are affected by your crossbow proficiency. Focus on the crossbow and bolts and press F key to pick them up."),
#  ("tutorial_usage_throwing_daggers", "Throwing daggers are easy to use and throwing them takes a very short time. But they deal light damage to the opponent. Usage of throwing daggers are affected byyour throwing weapon proficiency. Focus on the throwing daggers and press F key to pick it up."),
#  ("tutorial_usage_mounted", "You can use your weapons while you're mounted. Polearms like the lance here can be used for couched damage against opponents. In order to do that, ride your horse at a good speed and aim at your enemy. But do not press the attack button."),

##  ("tutorial_melee_chest", "The chest near you contains some of the melee weapons that can be used throughout the game. Look at the chest now and press F key to view its contents. Click on the weapons and move them to your Arms slots to be able to use them."),
##  ("tutorial_ranged_chest", "The chest near you contains some of the ranged weapons that can be used throughout the game. Look at the chest now and press F key to view its contents. Click on the weapons and move them to your Arms slots to be able to use them."),
##
##  ("tutorial_item_equipped", "You have equipped a weapon. Move your mouse scroll wheel up to wield your weapon. You can also switch between your weapons using your mouse scroll wheel."),

  ("tutorial_ammo_refilled", "Ammo refilled."),
  ("tutorial_failed", "You have been beaten this time, but don't worry. Follow the instructions carefully and you'll do better next time.\
 Press the Tab key to return to to the menu where you can retry this tutorial."),

  ("tutorial_1_msg_1","In this tutorial you will learn the basics of movement and combat.\
 In Mount&Blade you use the mouse to control where you are looking, and the WASD keys of your keyboard to move.\
 Your first task in the training is to locate the yellow flag in the room and move over it.\
 You can press the Tab key at any time to quit this tutorial or to exit any other area in the game.\
 Go to the yellow flag now."),
  ("tutorial_1_msg_2","Well done. Next we will cover attacking with weapons.\
 For the purposes of this tutorial you have been equipped with bow and arrows, a sword and a shield.\
 You can draw different weapons from your weapon slots by using the scroll wheel of your mouse.\
 In the default configuration, scrolling up pulls out your next weapon, and scrolling down pulls out your shield.\
 If you are already holding a shield, scrolling down will put your shield away instead.\
 Try changing your wielded equipment with the scroll wheel now. When you are ready,\
 go to the yellow flag to move on to your next task."),
  ("tutorial_1_msg_3","Excellent. The next part of this tutorial covers attacking with melee weapons.\
 You attack with your currently wielded weapon by using your left mouse button.\
 Press and hold the button to ready an attack, then release the button to strike.\
 If you hold down the left mouse button for a while before releasing, your attack will be more powerful.\
 Now draw your sword and destroy the four dummies in the room."),
  ("tutorial_1_msg_4","Nice work! You've destroyed all four dummies. You can now move on to the next room."),
  ("tutorial_1_msg_5","As you see, there is an archery target on the far side of the room.\
 Your next task is to use your bow to put three arrows into that target. Press and hold down the left mouse button to notch an arrow.\
 You can then fire the arrow by releasing the left mouse button. Note the targeting reticule in the centre of your screen,\
 which shows you the accuracy of your shot.\
 In order to achieve optimal accuracy, let fly your arrow when the reticule is at its smallest.\
 Try to shoot the target now."),
  ("tutorial_1_msg_6","Well done! You've learned the basics of moving and attacking.\
 With a little bit of practice you will soon master them.\
 In the second tutorial you can learn more advanced combat skills and face armed opponents.\
 You can press the Tab key at any time to return to the tutorial menu."),

  ("tutorial_2_msg_1","This tutorial will teach you how to defend yourself with a shield and how to battle armed opponents.\
 For the moment you are armed with nothing but a shield.\
 Your task is not to attack, but to successfully protect yourself from harm with your shield.\
 There is an armed opponent waiting for you in the next room.\
 He will try his best to knock you unconscious, while you must protect yourself with your shield\
 by pressing and holding the right mouse button.\
 Go into the next room now to face your opponent.\
 Remember that you can press the Tab key at any time to quit this tutorial or to exit any other area in the game."),
  ("tutorial_2_msg_2","Press and hold down the right mouse button to raise your shield. Try to remain standing for thirty seconds. You have {reg3} seconds to go."),
  ("tutorial_2_msg_3","Well done, you've succeeded in defending against an armed opponent.\
 The next phase of this tutorial will pit you and your shield against a force of enemy archers.\
 Move on to the next room when you're ready to face the archers."),
  ("tutorial_2_msg_4","Defend yourself from arrows by raising your shield with the right mouse button. Try to remain standing for thirty seconds. You have {reg3} seconds to go."),
  ("tutorial_2_msg_5","Excellent, you've put up a succesful defence against archers.\
 There is a reward waiting for you in the next room."),
  ("tutorial_2_msg_6","In the default configuration,\
 the F key on your keyboard is used for non-violent interaction with objects and humans in the gameworld.\
 To pick up the sword on the altar, look at it and press F when you see the word 'Equip'."),
  ("tutorial_2_msg_7","A fine weapon! Now you can use it to deliver a bit of payback.\
 Go back through the door and dispose of the archers you faced earlier."),
  ("tutorial_2_msg_8","Very good. Your last task before finishing this tutorial is to face the maceman.\
 Go through the door now and show him your steel!"),
  ("tutorial_2_msg_9","Congratulations! You have now learned how to defend yourself with a shield and even had your first taste of combat with armed opponents.\
 Give it a bit more practice and you'll soon be a renowned swordsman.\
 The next tutorial covers directional defence, which is one of the most important elements of Mount&Blade combat.\
 You can press the Tab key at any time to return to the tutorial menu."),

  ("tutorial_3_msg_1","This tutorial is intended to give you an overview of parrying and defence without a shield.\
 Parrying attacks with your weapon is a little bit more difficult than blocking them with a shield.\
 When you are defending with a weapon, you are only protected from one direction, the direction in which your weapon is set.\
 If you are blocking upwards, you will parry any overhead swings coming against you, but you will not stop thrusts or attacks to your sides.\
 Either of these attacks would still be able to hit you.\
 That's why, in order to survive without a shield, you must learn directional defence.\
 Go pick up up the quarterstaff now to begin practice."),
  ("tutorial_3_msg_2","By default, the direction in which you defend (by clicking and holding your right mouse button) is determined by the attack direction of your closest opponent.\
 For example, if your opponent is readying a thrust attack, pressing and holding the right mouse button will parry thrust attacks, but not side or overhead attacks.\
 You must watch your opponent carefully and only initiate your parry AFTER the enemy starts to attack.\
 If you start BEFORE he readies an attack, you may parry the wrong way altogether!\
 Now it's time for you to move on to the next room, where you'll have to defend yourself against an armed opponent.\
 Your task is to defend yourself successfully for thirty seconds with no equipment other than a simple quarterstaff.\
 Your quarterstaff's attacks are disabled for this tutorial, so don't worry about attacking and focus on your defence instead.\
 Move on to the next room when you are ready to initiate the fight."),
  ("tutorial_3_msg_3","Press and hold down the right mouse button to defend yourself with your staff after your opponent starts his attack.\
 Try to remain standing for thirty seconds. You have {reg3} seconds to go."),
  ("tutorial_3_msg_4","Well done, you've succeeded this trial!\
 Now you will be pitted against a more challenging opponent that will make things more difficult for you.\
 Move on to the next room when you're ready to face him."),
  ("tutorial_3_msg_5","Press and hold down the right mouse button to defend yourself with your staff after your opponent starts his attack.\
 Try to remain standing for thirty seconds. You have {reg3} seconds to go."),
  ("tutorial_3_msg_6","Congratulations, you still stand despite the enemy's best efforts.\
 The time has now come to attack as well as defend.\
 Approach the door and press the F key when you see the word 'Go'."),

  ("tutorial_3_2_msg_1","Your staff's attacks have been enabled again. Your first opponent is waiting in the next room.\
 Defeat him by a combination of attack and defence."),
  ("tutorial_3_2_msg_2","Defeat your opponent with your quarterstaff."),
  ("tutorial_3_2_msg_3","Excellent. Now the only thing standing in your way is one last opponent.\
 He is in the next room. Move in and knock him down."),
  ("tutorial_3_2_msg_4","Defeat your opponent with your quarterstaff."),
  ("tutorial_3_2_msg_5","Well done! In this tutorial you have learned how to fight ably without a shield.\
 Train hard and train well, and no one shall be able to lay a stroke on you.\
 In the next tutorial you may learn horseback riding and cavalry combat.\
 You can press the Tab key at any time to return to the tutorial menu."),

  ("tutorial_4_msg_1","Welcome to the fourth tutorial.\
 In this sequence you'll learn about riding a horse and how to perform various martial exercises on horseback.\
 We'll start by getting you mounted up.\
 Approach the horse, and press the 'F' key when you see the word 'Mount'."),
  ("tutorial_4_msg_2","While on horseback, the WASD keys control your horse's movement, not your own.\
 Ride your horse and try to follow the yellow flag around the course.\
 When you reach the flag, it will move to the next waypoint on the course until you reach the finish."),
  ("tutorial_4_msg_3","Very good. Next we'll cover attacking enemies from horseback. Approach the yellow flag now."),
  ("tutorial_4_msg_4","Draw your sword (using the mouse wheel) and destroy the four targets.\
 Try hitting the dummies as you pass them at full gallop -- this provides an extra challenge,\
 but the additional speed added to your blow will allow you to do more damage.\
 The easiest way of doing this is by pressing and holding the left mouse button until the right moment,\
 releasing it just before you pass the target."),
  ("tutorial_4_msg_5","Excellent work. Now let us try some target shooting from horseback. Go near the yellow flag now."),
  ("tutorial_4_msg_6","Locate the archery target beside the riding course and shoot it three times with your bow.\
 Although you are not required to ride while shooting, it's recommended that you try to hit the target at various speeds and angles\
 to get a feel for how your horse's speed and course affects your aim."),
  ("tutorial_4_msg_7","Congratulations, you have finished this tutorial.\
 You can press the Tab key at any time to return to the tutorial menu."),
# Ryan END

  ("tutorial_5_msg_1","TODO: Follow order to the flag"),
  ("tutorial_5_msg_2","TODO: Move to the flag, keep your units at this position"),
  ("tutorial_5_msg_3","TODO: Move to the flag to get the archers"),
  ("tutorial_5_msg_4","TODO: Move archers to flag1, infantry to flag2"),
  ("tutorial_5_msg_5","TODO: Enemy is charging. Fight!"),
  ("tutorial_5_msg_6","TODO: End of battle."),

  ("trainer_help_1", "This is a training ground where you can learn the basics of the game. Use A, S, D, W keys to move and the mouse to look around."),
  ("trainer_help_2", "To speak with the trainer, go near him, look at him and press the 'F' key when you see the word 'Talk' under his name.\
 When you wish to leave this or any other area or retreat from a battle, you can press the TAB key."),

  ("custom_battle_1", "Captain Malvogil and his Gondor company intercepted Harad reinforcement group.\
 Shouting out his warcry, he spurs his horse forward, and leads his loyal men to a fierce battle."),
  ("custom_battle_2", "Lord Mleza is leading a patrol of horsemen and archers\
 in search of a group of bandits who plundered a caravan and ran away to the hills.\
 Unfortunately the bandits have recently met two other large groups who want a share of their booty,\
 and spotting the new threat, they decide to combine their forces."),
  ("custom_battle_3", "Lord Grimbold of Rohan is leading the last defence of the walls against an army if Isengard.\
 Now, as the besiegers prepare for a final assault on the walls, he must hold the walls with courage and bright steel."),
  ("custom_battle_4", "When the scouts inform Lord Grainwad of the approach of an Rhun war band,\
 he decides to quickly prepare the defences of his camp and try to hold against superior numbers."),
  ("custom_battle_5", "Captain Ugluk has brought his fierce orksies into the west with the promise of plunder.\
 If he can make this dwarf stronghold fall to him today, his masters in Barad-Dur will be mightily pleased."),
  ("custom_battle_6", "Grishnakh and his orc raider squad were as keen as possible in escaping Elven patrols.\
 But one's good fortunes may not last forever, and it seems like filthy paleskins will have their share now."),
  ("custom_battle_7", "Cosairs have set up their camp on the shores of Gondor! How dare they.\
 Let us strike them before they get reinforcements and drive them off into the sea, where they belong."),
 
  ("finished", "(Finished)"),

  ("delivered_damage", "Delivered {reg60} damage."),
  ("archery_target_hit", "Distance: {reg61} yards. Score: {reg60}"),
  
  ("use_baggage_for_inventory","Use your baggage to access your inventory during battle (it's at your starting position)."),
##  ("cant_leave_now","Can't leave the area now."),
  ("cant_use_inventory_now","Can't access inventory now."),
  ("cant_use_inventory_arena","Can't access inventory in the arena."),
  ("cant_use_inventory_disguised","Can't access inventory while you're disguised."),
  ("cant_use_inventory_tutorial","Can't access inventory in the training camp."),
  ("1_denar", "1 Resource Pts."),
  ("reg1_denars", "{reg1} Resource Pts."),

  # Eglish calendar TLD -- mtarini
#  ("january_reg1_reg2", "T.A. {reg2}, January {reg1}"),
#  ("february_reg1_reg2", "T.A. {reg2}, February {reg1}"),
#  ("march_reg1_reg2", "T.A. {reg2}, March {reg1}"),
#  ("april_reg1_reg2", "T.A. {reg2}, April {reg1}"),
#  ("may_reg1_reg2", "T.A. {reg2}, May {reg1}"),
#  ("june_reg1_reg2", "T.A. {reg2}, June {reg1}"),
#  ("july_reg1_reg2", "T.A. {reg2}, July {reg1}"),
#  ("august_reg1_reg2", "T.A. {reg2}, August {reg1}"),
#  ("september_reg1_reg2", "T.A. {reg2}, September {reg1}"),
#  ("october_reg1_reg2", "T.A. {reg2}, October {reg1}"),
#  ("november_reg1_reg2", "T.A. {reg2}, November {reg1}"),
#  ("december_reg1_reg2", "T.A. {reg2}, December {reg1}"),
 

# TLD -- Quenya name (Steward's Reckoning)  MONTHS -- mtarini
#  
  ("january_reg1_reg2",   "T.A.{reg2}, Narvinyë {reg1} (Jan)"),
  ("february_reg1_reg2",  "T.A.{reg2}, Nénimë {reg1} (Feb)"),
  ("march_reg1_reg2",     "T.A.{reg2}, Súlìmë {reg1} (Mar)"),
  ("april_reg1_reg2",     "T.A.{reg2}, Víressë {reg1 (Apr)}"),
  ("may_reg1_reg2",       "T.A.{reg2}, Lótessë {reg1} (May)"),
  ("june_reg1_reg2",      "T.A.{reg2}, Náríë {reg1} (Jun)"),
  ("july_reg1_reg2",      "T.A.{reg2}, Cermië {reg1} (Jul)"),
  ("august_reg1_reg2",    "T.A.{reg2}, Urimë {reg1} (Aug)"),
  ("september_reg1_reg2", "T.A.{reg2}, Yavannië {reg1} (Sep)"),
  ("october_reg1_reg2",   "T.A.{reg2}, Narquelië {reg1} (Oct)"),
  ("november_reg1_reg2",  "T.A.{reg2}, Hísimë {reg1} (Nov)"),
  ("december_reg1_reg2",  "T.A.{reg2}, Ringarë {reg1} (Dec)"),

# TLD -- Quenya name (Steward's Reckoning) SPECIAL DAYS-- mtarini
  ("calendar_spec_day_1", "T.A.{reg2}, Yestarë (First Day)"),
  ("calendar_spec_day_2", "T.A.{reg2}, Tuilérë (Spring Day)"),
  ("calendar_spec_day_3", "T.A.{reg2}, Loëndë (Midyear's Day)"),
  ("calendar_spec_day_4", "T.A.{reg2}, Yáviérë (Harvest Day)"),
  ("calendar_spec_day_5", "T.A.{reg2}, Mettarë (Last Day)"),
  
  
##  ("you_approach_town","You approach the town of "),
##  ("you_are_in_town","You are in the town of "),
##  ("you_are_in_castle","You are at the castle of "),
##  ("you_sneaked_into_town","You have sneaked into the town of "),

  ("town_nighttime"," It is late at night and honest folk have abandoned the streets."),
  ("door_locked","The door is locked."),
  ("castle_is_abondened","The castle seems to be unoccupied."),
  ("town_is_abondened","The town has no garrison defending it."),
  ("place_is_occupied_by_player","The place is held by your own troops."),
  ("place_is_occupied_by_enemy", "The place is held by hostile troops."),
  ("place_is_occupied_by_friendly", "The place is held by friendly troops."),

  ("do_you_want_to_retreat", "Are you sure you want to retreat?"),
  ("give_up_fight", "Give up the fight?"),
  ("do_you_wish_to_leave_tutorial", "Do you wish to leave the tutorial?"),
  ("do_you_wish_to_surrender", "Do you wish to surrender?"),
  ("can_not_retreat", "Can't retreat, there are enemies nearby!"),
##  ("can_not_leave", "Can't leave. There are enemies nearby!"),

  ("s1_joined_battle_enemy", "{s1} has joined the battle on the enemy side."),
  ("s1_joined_battle_friend", "{s1} has joined the battle on your side."),

#  ("entrance_to_town_forbidden","It seems that the town guards have been warned of your presence and you won't be able to enter the town unchallenged."),
  ("entrance_to_town_forbidden","The town guards are on the lookout for intruders and it seems that you won't be able to pass through the gates unchallenged."),
  ("sneaking_to_town_impossible","The town guards are alarmed. You wouldn't be able to sneak through that gate no matter how well you disguised yourself."),

  ("battle_won", "You have won the battle!"),
  ("battle_lost", "You have lost the battle!"),

  ("attack_walls_success", "After a bloody fight, your brave soldiers manage to claim the walls from the enemy."),
  ("attack_walls_failure", "Your soldiers fall in waves as they charge the walls, and the few who remain alive soon rout and run away, never to be seen again."),
  ("attack_walls_continue", "A bloody battle ensues and both sides fight with equal valour. Despite the efforts of your troops, the castle remains in enemy hands."),

  ("order_attack_success", "Your men fight bravely and defeat the enemy."),
  ("order_attack_failure", "You watch the battle in despair as the enemy cuts your soldiers down, then easily drives off the few ragged survivors."),
  ("order_attack_continue", "Despite an extended skirmish, your troops were unable to win a decisive victory."),

  ("join_order_attack_success", "Your men fight well alongside your allies, sharing in the glory as your enemies are beaten."),
  ("join_order_attack_failure", "You watch the battle in despair as the enemy cuts your soldiers down, then easily drives off the few ragged survivors."),
  ("join_order_attack_continue", "Despite an extended skirmish, neither your troops nor your allies were able to win a decisive victory over the enemy."),

  ("siege_defender_order_attack_success", "The men of the garrison hold their walls with skill and courage, breaking the enemy assault and skillfully turning the defeat into a full-fledged rout."),
  ("siege_defender_order_attack_failure", "The assault quickly turns into a bloodbath. Valiant efforts are for naught; the overmatched garrison cannot hold the walls, and the enemy puts every last defender to the sword."),
  ("siege_defender_order_attack_continue", "Repeated, bloody attempts on the walls fail to gain any ground, but too many enemies remain for the defenders to claim a true victory. The siege continues."),


  ("hero_taken_prisoner", "{s1} of {s3} has been taken prisoner by {s2}."),
  ("hero_freed", "{s1} of {s3} has been freed from captivity by {s2}."),
  ("center_captured", "{s2} have taken {s1} from {s3}."),

  ("troop_relation_increased", "Your relation with {s1} has increased from {reg1} to {reg2}."),
  ("troop_relation_detoriated", "Your relation with {s1} has deteriorated from {reg1} to {reg2}."),
  ("faction_relation_increased", "Your relation with {s1} has increased from {reg1} to {reg2}."),
  ("faction_relation_detoriated", "Your relation with {s1} has deteriorated from {reg1} to {reg2}."),
  
  ("party_gained_morale", "Your party gains {reg1} morale."),
  ("party_lost_morale",   "Your party loses {reg1} morale."),

  ("qst_follow_spy_noticed_you", "The spy has spotted you! He's making a run for it!"),
  ("father", "father"),
  ("husband", "husband"),
  ("wife", "wife"),
  ("daughter", "daughter"),
  ("mother", "mother"),
  ("son", "son"),
  ("brother", "brother"),
  ("sister", "sister"),
  ("he", "He"),
  ("she", "She"),
  ("s3s_s2", "{s3}'s {s2}"),
  ("s5_is_s51", "{s5} is {s51}."),
  ("s5_is_the_ruler_of_s51", "{s5} is the ruler of {s51}. "),
  ("s5_is_a_nobleman_of_s6", "{s5} is a nobleman of {s6}. "),
##  ("your_debt_to_s1_is_changed_from_reg1_to_reg2", "Your debt to {s1} is changed from {reg1} to {reg2}."),

  ("relation_mnus_100", "Vengeful"), # -100..-94
  ("relation_mnus_90",  "Vengeful"),  # -95..-84
  ("relation_mnus_80",  "Vengeful"),
  ("relation_mnus_70",  "Hateful"),
  ("relation_mnus_60",  "Hateful"),
  ("relation_mnus_50",  " Hostile"),
  ("relation_mnus_40",  "  Angry"),
  ("relation_mnus_30",  "    Resentful"),
  ("relation_mnus_20",  "      Grumbling"),
  ("relation_mnus_10",  "        Suspicious"),
  ("relation_plus_0",   "         Indifferent"),# -5...4
  ("relation_plus_10",  "          Cooperative"), # 5..14
  ("relation_plus_20",  "           Welcoming"),
  ("relation_plus_30",  "            Favorable"),
  ("relation_plus_40",  "             Supportive"),
  ("relation_plus_50",  "              Friendly"),
  ("relation_plus_60",  "               Gracious"),
  ("relation_plus_70",  "                 Fond"),
  ("relation_plus_80",  "                  Loyal"),
  ("relation_plus_90",  "                   Devoted"),

  ("relation_mnus_100_ns", "{s60} is vengeful towards you."), # -100..-94
  ("relation_mnus_90_ns",  "{s60} is vengeful towards you."),  # -95..-84
  ("relation_mnus_80_ns",  "{s60} is vengeful towards you."),
  ("relation_mnus_70_ns",  "{s60} is hateful towards you."),
  ("relation_mnus_60_ns",  "{s60} is hateful towards you."),
  ("relation_mnus_50_ns",  "{s60} is hostile towards you."),
  ("relation_mnus_40_ns",  "{s60} is angry towards you."),
  ("relation_mnus_30_ns",  "{s60} is resentful against you."),
  ("relation_mnus_20_ns",  "{s60} is grumbling against you."),
  ("relation_mnus_10_ns",  "{s60} is suspicious towards you."),
  ("relation_plus_0_ns",   "{s60} is indifferent against you."),# -5...4
  ("relation_plus_10_ns",  "{s60} is cooperative towards you."), # 5..14
  ("relation_plus_20_ns",  "{s60} is welcoming towards you."),
  ("relation_plus_30_ns",  "{s60} is favorable to you."),
  ("relation_plus_40_ns",  "{s60} is supportive to you."),
  ("relation_plus_50_ns",  "{s60} is friendly to you."),
  ("relation_plus_60_ns",  "{s60} is gracious to you."),
  ("relation_plus_70_ns",  "{s60} is fond of you."),
  ("relation_plus_80_ns",  "{s60} is loyal to you."),
  ("relation_plus_90_ns",  "{s60} is devoted to you."),
  
  ("relation_reg1", " Relation: {reg1}"),

  ("center_relation_mnus_100", "The populace hates you with a passion"), # -100..-94
  ("center_relation_mnus_90",  "The populace hates you intensely"), # -95..-84
  ("center_relation_mnus_80",  "The populace hates you strongly"), 
  ("center_relation_mnus_70",  "The populace hates you"), 
  ("center_relation_mnus_60",  "The populace is hateful to you"), 
  ("center_relation_mnus_50",  "The populace is extremely hostile to you"), 
  ("center_relation_mnus_40",  "The populace is very hostile to you"), 
  ("center_relation_mnus_30",  "The populace is hostile to you"), 
  ("center_relation_mnus_20",  "The populace is against you"), 
  ("center_relation_mnus_10",  "The populace is opposed to you"), 
  ("center_relation_plus_0",   "The populace is indifferent to you"), 
  ("center_relation_plus_10",  "The populace is acceptive to you"), 
  ("center_relation_plus_20",  "The populace is cooperative to you"), 
  ("center_relation_plus_30",  "The populace is somewhat supportive to you"), 
  ("center_relation_plus_40",  "The populace is supportive to you"), 
  ("center_relation_plus_50",  "The populace is very supportive to you"), 
  ("center_relation_plus_60",  "The populace is loyal to you"), 
  ("center_relation_plus_70",  "The populace is highly loyal to you"), 
  ("center_relation_plus_80",  "The populace is devoted to you"), 
  ("center_relation_plus_90",  "The populace is fiercely devoted to you"),

  ("town_prosperity_0",   "The poverty of the town of {s60} is unbearable"),
  ("town_prosperity_10",   "The squalorous town of {s60} is all but deserted."),
  ("town_prosperity_20",   "The town of {s60} looks a wretched, desolate place."),
  ("town_prosperity_30",   "The town of {s60} looks poor and neglected."),
  ("town_prosperity_40",   "The town of {s60} appears to be struggling."),
  ("town_prosperity_50",   "The town of {s60} seems unremarkable."),
  ("town_prosperity_60",   "The town of {s60} seems to be flourishing."),
  ("town_prosperity_70",   "The prosperous town of {s60} is bustling with activity."),
  ("town_prosperity_80",   "The town of {s60} looks rich and well-maintained."),
  ("town_prosperity_90",   "The town of {s60} is opulent and crowded with well-to-do people."),
  ("town_prosperity_100",  "The glittering town of {s60} openly flaunts its great wealth."),

  ("village_prosperity_0",   "The poverty of the village of {s60} is unbearable."),
  ("village_prosperity_10",  "The village of {s60} looks wretchedly poor and miserable."),
  ("village_prosperity_20",  "The village of {s60} looks very poor and desolate."),
  ("village_prosperity_30",  "The village of {s60} looks poor and neglected."),
  ("village_prosperity_40",  "The village of {s60} appears to be somewhat poor and struggling."),
  ("village_prosperity_50",  "The village of {s60} seems unremarkable."),
  ("village_prosperity_60",  "The village of {s60} seems to be flourishing."),
  ("village_prosperity_70",  "The village of {s60} appears to be thriving."),
  ("village_prosperity_80",  "The village of {s60} looks rich and well-maintained."),
  ("village_prosperity_90",  "The village of {s60} looks very rich and prosperous."),
  ("village_prosperity_100", "The village of {s60}, surrounded by vast, fertile fields, looks immensely rich."),

  ("war_report_minus_4",   "we are about to lose the war"),
  ("war_report_minus_3",   "the situation looks bleak"),
  ("war_report_minus_2",   "things aren't going too well for us"),
  ("war_report_minus_1",   "we can still win the war if we rally"),
  ("war_report_0",   "we are evenly matched with the enemy"),
  ("war_report_plus_1",   "we have a fair chance of winning the war"),
  ("war_report_plus_2",   "things are going quite well"),
  ("war_report_plus_3",   "we should have no difficulty defeating them"),
  ("war_report_plus_4",   "we are about to win the war"),


  ("persuasion_summary_very_bad", "You try your best to persuade {s50},\
 but none of your arguments seem to come out right. Every time you start to make sense,\
 you seem to say something entirely wrong that puts you off track.\
 By the time you finish speaking you've failed to form a single coherent point in your own favour,\
 and you realise that all you've done was dig yourself deeper into a hole.\
 Unsurprisingly, {s50} does not look impressed."),
  ("persuasion_summary_bad",      "You try to persuade {s50}, but {reg51?she:he} outmanoeuvres you from the very start.\
 Even your best arguments sound hollow to your own ears. {s50}, likewise,\
 has not formed a very high opinion of what you had to say."),
  ("persuasion_summary_average",  "{s50} turns out to be a skilled speaker with a keen mind,\
 and you can't seem to bring forth anything concrete that {reg51?she:he} cannot counter with a rational point.\
 In the end, neither of you manage to gain any ground in this discussion."),
  ("persuasion_summary_good",     "Through quick thinking and smooth argumentation, you manage to state your case well,\
 forcing {s50} to concede on several points. However, {reg51?she:he} still expresses doubts about your request."),
  ("persuasion_summary_very_good","You deliver an impassioned speech that echoes through all listening ears like poetry.\
 The world itself seems to quiet down in order to hear you better .\
 The inspiring words have moved {s50} deeply, and {reg51?she:he} looks much more well-disposed towards helping you."),
  

# meet_spy_in_enemy_town quest secret sentences
  ("secret_sign_1",  "The armoire dances at midnight..."),
  ("secret_sign_2",  "I am selling these fine Khergit tapestries. Would you like to buy some?"),
  ("secret_sign_3",  "The friend of a friend sent me..."),
  ("secret_sign_4",  "The wind blows hard from the east and the river runs red..."),
  
  ("countersign_1",  "But does he dance for the dresser or the candlestick?"),
  ("countersign_2",  "Yes I would, do you have any in blue?"),
  ("countersign_3",  "But, my friend, your friend's friend will never have a friend like me."),
  ("countersign_4",  "Have you been sick?"),

# Names  
  ("name_1",  "Albard"),
  ("name_2",  "Euscarl"),
  ("name_3",  "Sigmar"),
  ("name_4",  "Talesqe"),
  ("name_5",  "Ritmand"),
  ("name_6",  "Aels"),
  ("name_7",  "Raurqe"),
  ("name_8",  "Bragamus"),
  ("name_9",  "Taarl"),
  ("name_10", "Ramin"),
  ("name_11", "Shulk"),
  ("name_12", "Putar"),
  ("name_13", "Tamus"),
  ("name_14", "Reichad"),
  ("name_15", "Walcheas"),
  ("name_16", "Rulkh"),
  ("name_17", "Marlund"),
  ("name_18", "Auguryn"),
  ("name_19", "Daynad"),
  ("name_20", "Joayah"),
  ("name_21", "Ramar"),
  ("name_22", "Caldaran"),
  ("name_23", "Brabas"),
  ("name_24", "Kundrin"),
  ("name_25", "Pechnak"),

# Surname
  ("surname_1",  "{s50} of Uxhal"),
  ("surname_2",  "{s50} of Wercheg"),
  ("surname_3",  "{s50} of Reyvadin"),
  ("surname_4",  "{s50} of Suno"),
  ("surname_5",  "{s50} of Jelkala"),
  ("surname_6",  "{s50} of Veluca"),
  ("surname_7",  "{s50} of Halmar"),
  ("surname_8",  "{s50} of Curaw"),
  ("surname_9",  "{s50} of Sargoth"),
  ("surname_10", "{s50} of Tihr"),
  ("surname_11", "{s50} of Zendar"),
  ("surname_12", "{s50} of Rivacheg"),
  ("surname_13", "{s50} of Wercheg"),
  ("surname_14", "{s50} of Ehlerdag"),
  ("surname_15", "{s50} of Yaragar"),
  ("surname_16", "{s50} of Burglen"),
  ("surname_17", "{s50} of Shapeshte"),
  ("surname_18", "{s50} of Hanun"),
  ("surname_19", "{s50} of Saren"),
  ("surname_20", "{s50} of Tosdhar"),
  ("surname_21", "{s50} the Long"),
  ("surname_22", "{s50} the Gaunt"),
  ("surname_23", "{s50} Silkybeard"),
  ("surname_24", "{s50} the Sparrow"),
  ("surname_25", "{s50} the Pauper"),
  ("surname_26", "{s50} the Scarred"),
  ("surname_27", "{s50} the Fair"),
  ("surname_28", "{s50} the Grim"),
  ("surname_29", "{s50} the Red"),
  ("surname_30", "{s50} the Black"),
  ("surname_31", "{s50} the Tall"),
  ("surname_32", "{s50} Star-Eyed"),
  ("surname_33", "{s50} the Fearless"),
  ("surname_34", "{s50} the Valorous"),
  ("surname_35", "{s50} the Cunning"),
  ("surname_36", "{s50} the Coward"),
  ("surname_37", "{s50} Bright"),
  ("surname_38", "{s50} the Quick"),
  ("surname_39", "{s50} the Minstrel"),
  ("surname_40", "{s50} the Bold"),
  ("surname_41", "{s50} Hot-Head"),
  
  ("surnames_end", "surnames_end"),
  

  ("number_of_troops_killed_reg1", "Number of troops killed: {reg1}"),
  ("number_of_troops_wounded_reg1", "Number of troops wounded: {reg1}"),
  ("number_of_own_troops_killed_reg1", "Number of friendly troops killed: {reg1}"),
  ("number_of_own_troops_wounded_reg1", "Number of friendly troops wounded: {reg1}"),

  ("retreat", "Retreat!"),
  ("siege_continues", "Fighting Continues..."),
  ("casualty_display", "Your casualties: {s10}^Enemy casualties: {s11}{s12}"),
  ("casualty_display_hp", "^You were wounded for {reg1} hit points."),

# Quest log texts
  ("quest_log_updated", "Quest log has been updated..."),

  ("banner_selection_text", "You have been awarded the right to carry a banner.\
 Your banner will signify your status and bring you honour. Which banner do you want to choose?"),


# Retirement Texts: s7=village name; s8=castle name; s9=town name
  ("retirement_text_1", "Only too late do you realise that your money won't last.\
 It doesn't take you long to fritter away what little you bothered to save,\
 and you fare poorly in several desperate attempts to start adventuring again.\
 You end up a beggar in {s9}, living on alms and the charity of the church."),
  ("retirement_text_2", "Only too late do you realise that your money won't last.\
 It doesn't take you long to fritter away what little you bothered to save.\
 Once every denar has evaporated in your hands you are forced to start a life of crime in the backstreets of {s9},\
 using your skills to eke out a living robbing coppers from women and poor townsmen."),
  ("retirement_text_3", "Only too late do you realise that your money won't last.\
 It doesn't take you long to fritter away what little you bothered to save,\
 and you end up a penniless drifter, going from tavern to tavern\
 blagging drinks from indulgent patrons by regaling them with war stories that no one ever believes."),
  ("retirement_text_4", "The silver you've saved doesn't last long,\
 but you manage to put together enough to buy some land near the village of {s7}.\
 There you become a free farmer, and you soon begin to attract potential {wives/husbands}.\
 In time the villagers come to treat you as their local hero.\
 You always receive a place of honour at feasts, and your exploits are told and retold in the pubs and taverns\
 so that the children may keep a memory of you for ever and ever."),
  ("retirement_text_5", "The silver you've saved doesn't last long,\
 but it's enough to buy a small tavern in {s9}. Although the locals are wary of you at first,\
 they soon accept you into their midst. In time your growing tavern becomes a popular feasthall and meeting place.\
 People come for miles to eat or stay there due to your sheer renown and the epic stories you tell of your adventuring days."),
  ("retirement_text_6", "You've saved wisely throughout your career,\
 and now your silver and your intelligence allow you to make some excellent investments to cement your future.\
 After buying several shops and warehouses in {s9}, your shrewdness turns you into one of the most prominent merchants in town,\
 and you soon become a wealthy {man/woman} known as much for your trading empire as your exploits in battle."),
  ("retirement_text_7", "As a landed noble, however minor, your future is all but assured.\
 You settle in your holdfast at {s7}, administrating the village and fields,\
 adjudicating the local courts and fulfilling your obligations to your liege lord.\
 Occasionally your liege calls you to muster and command in his campaigns, but these stints are brief,\
 and you never truly return to the adventuring of your younger days. You have already made your fortune.\
 With your own hall and holdings, you've few wants that your personal wealth and the income of your lands cannot afford you."),
  ("retirement_text_8", "There is no question that you've done very well for yourself.\
 Your extensive holdings and adventuring wealth are enough to guarantee you a rich and easy life for the rest of your days.\
 Retiring to your noble seat in {s8}, you exchange adventure for politics,\
 and you soon establish yourself as a considerable power in your liege lord's kingdom.\
 With intrigue to busy yourself with, your own forests to hunt, a hall to feast in and a hundred fine war stories to tell,\
 you have little trouble making the best of the years that follow."),
  ("retirement_text_9", "As a reward for your competent and loyal service,\
 your liege lord decrees that you be given a hereditary title, joining the major nobility of the realm.\
 Soon you complete your investitute as baron of {s7}, and you become one of your liege's close advisors\
 and adjutants. Your renown garners you much subtle pull and influence as well as overt political power.\
 Now you spend your days playing the games of power, administering your great fiefs,\
 and recounting the old times of adventure and glory."),
  ("retirement_text_10", "Though you started from humble beginnings, your liege lord holds you in high esteem,\
 and a ripple of shock passes through the realm when he names you to the hereditary title of {count/countess} of {s9}.\
 Vast fiefs and fortunes are now yours to rule. You quickly become your liege's most trusted advisor,\
 almost his equal and charged with much of the running of his realm,\
 and you sit a throne in your own splendourous palace as one of the most powerful figures in Calradia."),


#NPC companion changes begin


# Objectionable actions

# humanitarian
  ("loot_village", "attack innocent villagers"),
  ("steal_from_villagers", "steal from poor villagers"),
  ("rob_caravan", "rob a merchant caravan"), # possibly remove
  ("sell_slavery", "sell people into slavery"),

# egalitarian
  ("men_hungry", "run out of food"), ##Done - simple triggers
  ("men_unpaid", "not be able to pay the men"),
#  ("party_crushed", "get ourselves slaughtered"), ##Done - game menus
  ("excessive_casualties", "turn every battle into a bloodbath for our side"),

# chivalric
  ("surrender", "surrender to the enemy"), ##Done - game menus
  ("flee_battle", "run from battle"), ##Done - game menus
  ("pay_bandits", "pay off common bandits"),

# honest
  ("fail_quest", "fail a quest which we undertook on word of honour"),

# quest-related strings
  ("squander_money", "squander money given to us in trust"),
  ("murder_merchant", "involve ourselves in cold-blooded murder"),
  ("round_up_serfs", "round up serfs on behalf of some noble"),


# Fates suffered by companions in battle
  ("battle_fate_1", "We were separated in the heat of battle"),
  ("battle_fate_2", "I was wounded and left for dead"),
  ("battle_fate_3", "I was knocked senseless by the enemy"),
  ("battle_fate_4", "I was taken and held for ransom"),
  ("battle_fate_5", "I got captured, but later managed to escape"),


# strings for opinion
  ("npc_morale_report", "I'm {s6} your choice of companions, {s7} your style of leadership, and {s8} the general state of affairs"), 
  ("happy", "happy about"),
  ("content", "content with"),
  ("concerned", "concerned about"),
  ("not_happy", "not at all happy about"),
  ("miserable", "downright appalled at"),  


  ("morale_reg1",    " Morale: {reg1}"),
  ("bar_enthusiastic", "                   Enthusiastic"),  
  ("bar_content",      "              Content"),
  ("bar_weary",        "          Weary"),
  ("bar_disgruntled",  "     Disgruntled"),
  ("bar_miserable",    "  Miserable"),  


#other strings
  ("here_plus_space", "here "),

#NPC strings
#npc1 = borcha
#npc2 = marnid
#npc3 = ymira  
#npc4 = rolf
#npc5 = baheshtur
#npc6 = firentis
#npc7 = deshavi
#npc8 = matheld
#npc9 = alayen
#npc10 = bunduk
#npc11 = katrin
#npc12 = jeremus
#npc13 = nizar
#npc14 = lazalit
#npc15 = artimenner
#npc16 = klethi
  
  ("npc1_intro", "Ho there, traveller. You wouldn't by chance be in the market for a tracker, would you?"),
  ("npc2_intro", "Hello. Would you be so kind as to have a cup with me? I'm down to my last five denars and I'd rather not drink alone."),
  ("npc3_intro", "Good day to you!"),
  ("npc4_intro", "Greetings. I am Rolf, son of Rolf, of the most ancient and puissant House of Rolf."),
  ("npc5_intro", "Greetings, traveller. Would you join me for a drink?"),
  ("npc6_intro", "I am lost... Lost..."),
  ("npc7_intro", "Yes? Keep your distance, by the way."),
  ("npc8_intro", "What do you want?"),
  ("npc9_intro", "You there, good {man/woman}, be so kind as to fetch me another drink, eh?"),
  ("npc10_intro", "Greetings there, {Brother/Sister}! Here's to the doom and downfall of all high-born lords and ladies!"),
  ("npc11_intro", "Hello there, {laddie/lassie}. Have a drink on me."),
  ("npc12_intro", "Greetings, fellow traveller. Perhaps you can help me."),
  ("npc13_intro", "Greetings, traveller. I am Nizar. No doubt you will have heard of me."),
  ("npc14_intro", "Yes? What is it you wish?"),
  ("npc15_intro", "Oh! Say, friend, are you by chance heading out of town anytime soon?"),
  ("npc16_intro", "Hello there. I couldn't help noticing that you came into town at the head of a company of soldiers. Are you by any chance looking for new hands?"),

  ("npc1_intro_response_1", "Perhaps. What's the urgency?"),
  ("npc2_intro_response_1", "Your last five denars? What happened to you?"),
  ("npc3_intro_response_1", "Hello. What's a clearly well-brought up young lady like you doing in a place like this?"),
  ("npc4_intro_response_1", "Hmm... I have never heard of the House of Rolf."),
  ("npc5_intro_response_1", "Certainly. With whom do I have the pleasure of drinking?"),
  ("npc6_intro_response_1", "Why so gloomy, friend?"),
  ("npc7_intro_response_1", "My apologies. I was merely going to say that you look a bit down on your luck."),
  ("npc8_intro_response_1", "Merely to pass the time of day, ma'am, if you're not otherwise engaged."),
  ("npc9_intro_response_1", "You must have me confused with the tavernkeep, sir."),
  ("npc10_intro_response_1", "Why do you say that, sir?"),
  ("npc11_intro_response_1", "What's the occasion?"),
  ("npc12_intro_response_1", "How is that?"),
  ("npc13_intro_response_1", "Um... I don't think so."),
  ("npc14_intro_response_1", "To pass the time of day with a fellow traveller, if you permit."),
  ("npc15_intro_response_1", "I am. What concern is it of your, may I ask?"),
  ("npc16_intro_response_1", "I could be. What's your story?"),

  ("npc1_intro_response_2", "Step back, sir, and keep your hand away from my purse."),
  ("npc2_intro_response_2", "I have better things to do."),
  ("npc3_intro_response_2", "Run along now, girl. I have work to do."),
  ("npc4_intro_response_2", "Eh? No thanks, we don't want any."),
  ("npc5_intro_response_2", "I have no time for that."),
  ("npc6_intro_response_2", "No doubt. Well, good luck getting found."),
  ("npc7_intro_response_2", "Right. I'll not bother you, then."),
  ("npc8_intro_response_2", "Nothing at all, from one so clearly disinclined to pleasantries. Good day to you."),
  ("npc9_intro_response_2", "Fetch it yourself!"),
  ("npc10_intro_response_2", "That's rebel talk, and I'll hear none of it. Good day to you."),
  ("npc11_intro_response_2", "I think not, madame."),
  ("npc12_intro_response_2", "Sorry, I am afraid that I am otherwise engaged right now."),
  ("npc13_intro_response_2", "No, and I can't say that I much want to make your acquaintance."),
  ("npc14_intro_response_2", "Nothing at all. My apologies."),
  ("npc15_intro_response_2", "I'd be obliged if you minded your own business, sir."),
  ("npc16_intro_response_2", "Mind your own business, lass."),

#backstory intro
  ("npc1_backstory_a", "Well, {sir/madame}, it's a long story..."),
  ("npc2_backstory_a", "It's a tragic tale, sir."),
  ("npc3_backstory_a", "A good question, and I shall tell you!"),
  ("npc4_backstory_a", "Really? Well, perhaps your ignorance can be forgiven. Our ancestral lands are far away, over the mountains."),
  ("npc5_backstory_a", "I am Baheshtur, son of Azabei, grandson of Badzan. Were you not a barbarian, you would likely know from my lineage that I am a Roan Horse Khergit of the highlands, of the tribe of Shamir, of the clan of Dulam, of the family of Ubayn, from the Pantash valley, and you might be able to guess why I am so far from home."),
  ("npc6_backstory_a", "I have commited the greatest of sins, {sir/madame}, and it is to my shame that I must appoint you my confessor, if you should like to hear it."),
  ("npc7_backstory_a", "My luck? You could say that."),
  ("npc8_backstory_a", "Ah. Well, if you must know, I shall tell you."),
  ("npc9_backstory_a", "My most humble apologies. It is sometimes hard to recognize folk amid the smoke and gloom here. I still cannot believe that I must make my home in such a place."),
  ("npc10_backstory_a", "It's a long story, but if you get yourself a drink, I'll be glad to tell it."),
  ("npc11_backstory_a", "Why, I managed to sell my wagon and pots, {lad/lass}. For once I've got money to spend and I intend to make the best of it."),
  ("npc12_backstory_a", "I shall tell you -- but know that it is a tale of gross iniquity. I warn you in advance, lest you are of a choleric temperament, and so become incensed at the injustice done unto me that you do yourself a mischief."),
  ("npc13_backstory_a", "You have not? Then perhaps you will have heard of my steed, who cuts across the Calradian plains like a beam of moonlight? Or of my sword, a connoisseur of the blood of the highest-born princes of the land?"),
  ("npc14_backstory_a", "Very well. I do not mind. My name is Lazalet."),
  ("npc15_backstory_a", "I'm an engineer, specialized in the art of fortification. If you need a wall knocked down, I can do that, given enough time. If you need a wall built back up, I can do that too, although it will take longer and cost you more. And you can't cut costs, either, unless you want your new edifice coming down underneath you, as someone around here has just found out."),
  ("npc16_backstory_a", "Well, {sir/madame}, as long as I can remember I've had a weakness for pretty things, and it's gotten me into trouble, you see."),

#backstory main body
  ("npc1_backstory_b", "I had a bit of a misunderstanding {s19}in {s20} about a horse that I found tied up outside the inn. It was the spitting image of a beast that threw me a few days back and ran off. Naturally I untied it for a closer look. As it turns out, the horse belonged to a merchant, a pinch-faced old goat who wouldn't accept that it all was a simple misunderstanding, and went off to get the guard."),
  ("npc2_backstory_b", "A while back, I left Geroia with a caravan of goods. I was hoping to sell it all in Sargoth and make a hefty sum. But, what do you know... we were ambushed by a party of Khergit raiders who rode away with most of the horses and goods. And two days later, my own caravan guards ran away with the rest of what I had."),
  ("npc3_backstory_b", "My father, a well-known merchant {s19}in {s20}, decided that I should be married to one of his business partners, a man well past the age of 30. I have been an obedient daughter all of my life, but it was a ridiculous and horrid proposition. So I ran away!"),
  ("npc4_backstory_b", "Like all the men of my family, I have come to a foreign land to make a name for myself in the profession of arms before returning home to take over custodianship of my estates. Unfortunately, the authorities in these lands have little understanding of the warrior code, and have chosen to call me a bandit and brigand, and put a price on my head -- a most unfair libel to throw at a gentleman adventurer, you will surely agree."),
  ("npc5_backstory_b", "For as long as any one can remember, our people have feuded with the tribe of Humyan, many of whom have settled in the next valley over. Many men have died in this feud, on both sides, including two of my brothers. The Khan himself has ordered us to cease, to save men for the wars in Calradia. But I know my rights, and my brothers' blood cries out for vengeance. I waylaid and killed a Humyan on a track over the mountains, and I rode out of our village the same night, without even having had the chance to bid farewell to my father. I will bide my time in Calradia, for a year or two, then return home when the Khan's men have forgotten. The Humyan will not forget, of course, but such is the price of honour."),
  ("npc6_backstory_b", "I was a captain of horse in the service of the lord {s19}in {s20}, and my brother served with me. But we were both in love with the same woman, a courtesan -- a temptress, who played upon our jealousies! My brother and I quarreled. I had drunk too much. He slapped me with his glove, and I spit him upon my sword... My own brother! My sword-arm was stained with the blood of my kin!"),
  ("npc7_backstory_b", "It was my bad luck to be born to a weak father who married me off to a drunken layabout, who beat me. It was my bad luck, when I ran away from my husband, to be taken by a group of bandits. It was my bad luck that the only one among them who was kind to me, who taught me to hunt and to fight, inspired the jealousy of the others, who knifed him and forced me to run away again."),
  ("npc8_backstory_b", "I am from an old family in the northern lands, the daughter of a thane and also wife to one. I fought by my husband's side, his partner both in war and in peace. But my husband died of the plague, when I was still childless. My husband had decreed that I should inherit his lands, in the absence of an heir. My brother-in-law, cursed be his name, said that it was not our custom that women could inherit a thanedom. That was nonsense, but his gold bought the loyalties of enough of my husband's faithless servants for him to install himself in my hall. So I fled, something I was raised never to do, and something I hope never to do again."),
  ("npc9_backstory_b", "I was my father's first son, and his heir. But my mother died, and my father remarried. His new wife thought that her son should inherit. She could not move against me openly, but the other day I fed a pot of suet that had been left out for me to one of my hounds, and it keeled over. I accused my stepmother, but my father, befuddled by her witchcraft, refused to believe me and ordered me to leave his sight."),
  ("npc10_backstory_b", "A sergeant I was, in the garrison {s19} at {s20}. Twenty years I stood guard for the city, taking many a hard knock in many a tough fight, until they appointed a snot-nosed, downy-lipped princeling, barely out of his mother's cradle, as commander of the garrison. He came upon me standing watch atop the tower, with my crossbow unstrung -- on account of the rain, you see... Can't have the cord loosen... But Little Prince Snot-Nose tells me that an unstrung bow is dereliction of duty. Says he'll have me horsewhipped. And something in me snapped. So I walked off my post."),
  ("npc11_backstory_b", "For 30 years I followed the armies of this land, selling them victuals and drink, watching their games of dice and finding them girls, and nary a denar was left in my purse at the end."),
  ("npc12_backstory_b", "I am by training a natural philosopher, but condemned by the jealousy of the thick-headed doctors of my university to make my living as an itinerant surgeon. I was hired by a merchant of this city to cure his son, who fell into a coma after a fall from his balcony. I successfully trepanned the patient's skull to reduce the cranial swelling, but the family ignored my advice to treat the ensuing fevers with a tincture of willow bark, and the boy died. The father, rather than reward me for my efforts, charged me with sorcery -- me, a philosopher of nature! Such is the ignorance and ingratitude of mankind."),
  ("npc13_backstory_b", "I am a warrior by profession. But perhaps you may also have heard of my prowess as a poet, who can move the iciest of maidens to swoon. Or of my prowess in the art of the bedchamber, in which I must confess a modest degree of skill. I confess a modest affection for Calradia, and for the past several years have visited its towns, castles, and villages, making the most of my talents."),
  ("npc14_backstory_b", "I am the second son of the count of Geroia, of whom you have no doubt heard. Having no inheritance of my own, I came here to seek my fortune in Calradia, training men in the art of battle. Unfortunately, the lords here in {s20} has no taste for the disciplinary methods needed to turn rabble into soldiers. I told him it was wiser to flog them now, then bury them later. But he would not listen, and I was told to take my services elsewhere."),
  ("npc15_backstory_b", "The castellan {s19}in {s20} wanted a new tower added to the wall. Trouble is, he ran out of cash halfway through the process, before I could complete the supports. I told him that it would collapse, and it did. Unfortunately he was standing on it, at the time. The new castellan didn't feel like honouring his predecessor's debts and implied that I might find myself charged with murder if I push the point."),
  ("npc16_backstory_b", "I grew up in Malayurg castle as a bonded servant, working alongside my mother in the kitchens. I would amuse myself by hunting mice through the pantries and sculleries. I was so good at it that I put the castle cats out of a job, and eventually the lord realized that I might also be employed to track down bigger game, on certain errands of a type perhaps better left unsaid. Needless to say, I found a number of opportunities to avail myself of trinkets that had formerly belonged to my lord's enemies. So I was able to buy myself out of bondage, and find hire as a free agent. My last job was {s19}in {s20}."),

#backstory recruit pitch
  ("npc1_backstory_c", "But if I was with a larger group who could vouch for me, they might let it pass. I'd be very grateful to you."),
  ("npc2_backstory_c", "So here I am, no money and no way home."),
  ("npc3_backstory_c", "I shall marry whom I want, when I want. Moreover, regardless of what my father might think, I am perfectly capable of taking care of myself. I was thinking that I should perhaps join a band of gypsies, or perhaps a troop of mercenaries!"),
  ("npc4_backstory_c", "But I am anxious to avoid any further trouble, so if you knew of any company of fighting men where I might enlist, I would be most grateful."),
  ("npc5_backstory_c", "In the meantime, any opportunities to earn a living with my sword would be most welcome."),
  ("npc6_backstory_c", "Do you believe there is hope for a man like me? Can I find the path of righteousness, or am I doomed to follow the demons that dwell inside of me?"),
  ("npc7_backstory_c", "But I do not count myself unlucky, stranger, no more than any other woman of Calradia, this fetid backwater, this dungheap among the nations, populated by apes and jackals."),
  ("npc8_backstory_c", "When I have enough gold to raise an army I shall go back and take what it is mine."),
  ("npc9_backstory_c", "I hope to offer my sword to some worthy captain, as it is the only honourable profession for a man of my birth apart from owning land, but in the meantime I am condemned to make my bed among thieves, vagabonds, merchants, and the other riff-raff of the road."),
  ("npc10_backstory_c", "Now I'm here getting drunk, and the Devil take tomorrow."),
  ("npc11_backstory_c", "It's no kind of life, victualling the armies. You earn a bit here and a bit there as the soldiers spend their money, and then along comes one defeat and you have to start over, endebting yourself to buy a new wagon and new oxen. So I've decided to get out of the business, but army life is all I know."),
  ("npc12_backstory_c", "The lord of this castle is reluctant to place me under arrest, but I am anxious to move on elsewhere."),
  ("npc13_backstory_c", "Which reminds me -- somewhere out there in the city is a rather irate husband. I don't suppose you might consider helping me leave town?"),
  ("npc14_backstory_c", "So, if you know of any commander who believes that his purpose is to win battles, rather than pamper his soldiers, I would be pleased if you directed me to him ."),
  ("npc15_backstory_c", "More fool me for having taken the contract without an advance, I suppose, but the end of it all is that I'm in a difficult spot, with the roads full of bandits and no money to pay for an escort. So I'd be much obliged if a well-armed party heading out in the next few days could take me along."),
  ("npc16_backstory_c", "Unfortunately, my last employer's wife had a lovely amulet, of a kind I simply could not resist. She doesn't know it's missing, yet, but she might soon. So tell me, are you looking for helpers?"),


### use these if there is a short period of time between the last meeting 
  ("npc1_backstory_later", "I've been here and about, you know, doing my best to keep out of trouble. I'm desperately in need of work, however."),
  ("npc2_backstory_later", "I sold my boots and have managed to make a few denars peddling goods from town to town, but it's a hard living."),
  ("npc3_backstory_later", "I hired myself on as a cook for some passing caravans, and that at least keeps me fed. But it is rough company on the road, and I grow weary of fighting off guards and others who would try to take liberties. I was thinking that if I could find work as a warrior, men would know to leave me alone."),
  ("npc4_backstory_later", "I went back to my ancestral barony, to inspect my lands. But we had locusts, you see, and bad rains, and other things, so here I am again, looking for work."),
  ("npc5_backstory_later", "I've been wandering through this war-torn land, looking for a leader who is worth following."),
  ("npc6_backstory_later", "I have been wandering Calradia, but have yet to find redemption."),
  ("npc7_backstory_later", "I have been wandering, looking for work as a tracker, but it has not been easy. Calradians are mostly ill-bred, lice-ridden, and ignorant, and it is not easy to work with such people."),
  ("npc8_backstory_later", "I am still seeking a war leader in whose shield wall I would fight. But I need gold, and fast, and the lords of this land as often as not prefer to stay behind the walls of their fortresses, rather march out to where glory and riches can be won."),
  ("npc9_backstory_later", "I've offered my sword to a few lords in these parts. But I find as often as not they'll ask me to run messages, or train peasants, or some other job not fit for a gentleman."),
  ("npc10_backstory_later", "I don't know if I told you or not, but I deserted my unit after I struck a young noble who had ordered me to be horsewhipped without cause. Since then I've been laying low. Thankfully I had the wit to pilfer my captain's purse before heading out, but the money is running low."),
  ("npc11_backstory_later", "I've been around and about. But it's a rare captain who'll take on an old bag of bones like me as a fighter, even if I could whip half the boys in his outfit."),
  ("npc12_backstory_later", "I have been here and about, tending to the sick and taking what reward I can. But the people of these parts are ignorant, and have little respect for my craft. The few denars I make are barely enough for me to replenish my stock of medicine. I should be grateful for the chance to find other work."),
  ("npc13_backstory_later", "I have been wandering through the cities of Calradia, leaving a string of love-sick women and cuckolded husbands in my wake. But I grow weary of such simple challenges, and had been thinking of turning myself to more martial pastimes."),
  ("npc14_backstory_later", "I have gone from court to court, but I have not yet found a lord who is to my liking."),
  ("npc15_backstory_later", "I've been going from castle to castle, looking to see if walls or towers need repair. But either the lord's away, or he's got other things on his mind, or I run into his creditors on the street, begging for change, and I realize that here's one job not to take. So if you hear of anything, let me know."),
  ("npc16_backstory_later", "I do the odd job from time to time. But there's naught like steady employment, and a regular run of corpses to loot."),


  ("npc1_backstory_response_1", "Perhaps. But how do I know that there won't be a 'misunderstanding' about one of my horses?"),
  ("npc2_backstory_response_1", "Well, perhaps I could offer you work. Can you fight?"),
  ("npc3_backstory_response_1", "Well, as it happens I run a company of mercenaries."),
  ("npc4_backstory_response_1", "I run such a company, and might be able to hire an extra hand."),
  ("npc5_backstory_response_1", "That's the spirit! I might be able to offer you something."),
  ("npc6_backstory_response_1", "Hmm. You might consider joining us. Right wrongs, fight oppressors, redeem yourself, that kind of thing."),
  ("npc7_backstory_response_1", "Hmm... Are you by any chance looking for work?"),
  ("npc8_backstory_response_1", "I can offer you opportunities to make money through good honest fighting and pillaging."),
  ("npc9_backstory_response_1", "Perhaps you would like to join my company for a while."),
  ("npc10_backstory_response_1", "If you're looking for work, I can use experienced fighters."),
  ("npc11_backstory_response_1", "What will you do now?"),
  ("npc12_backstory_response_1", "Well, you could travel with us, but you'd have to be able to fight in our battle line."),
  ("npc13_backstory_response_1", "I might be able to use an extra sword in my company."),
  ("npc14_backstory_response_1", "I might be able to use you in my company."),
  ("npc15_backstory_response_1", "Where do you need to go?"),
  ("npc16_backstory_response_1", "I might be. What can you do?"),

  ("npc1_backstory_response_2", "I'll do no such thing. I have better things to do then to help thieves avoid justice."),
  ("npc2_backstory_response_2", "Hard luck, friend. Good day to you."),
  ("npc3_backstory_response_2", "Go back to your family, lass. Fathers must always be obeyed."),
  ("npc4_backstory_response_2", "No, sorry, I haven't heard of one."),
  ("npc5_backstory_response_2", "Sigh.. So long as you hill clans fight tribe against tribe, you will remain a silly, weak people."),
  ("npc6_backstory_response_2", "Away with you, accursed fraticide!"),
  ("npc7_backstory_response_2", "Actually, I'm rather fond of the place. Good day to you."),
  ("npc8_backstory_response_2", "Your brother-in-law was right -- women should not rule. Go back home and tend your hearth."),
  ("npc9_backstory_response_2", "Some of my best friends are riff-raff. Good day to you, sir."),
  ("npc10_backstory_response_2", "No doubt you'll wake up with your head in a noose, and you'll deserve it. Good day."),
  ("npc11_backstory_response_2", "Very interesting, madame, but I have work to do."),
  ("npc12_backstory_response_2", "Sorry. I can't take on any new hands."),
  ("npc13_backstory_response_2", "No, sorry. Nothing I can do for you."),
  ("npc14_backstory_response_2", "I'll let you know if I hear of anything. Good day."),
  ("npc15_backstory_response_2", "Sorry. I've got all the men that I can manage right now."),
  ("npc16_backstory_response_2", "Sorry, lass. You sound like you might be trouble."),

  ("npc1_signup", "{Sir/Madame} -- I'm offended that you would even think such a thing. I'd be most indebted to you, and you'll see that I show my gratitude."),
  ("npc2_signup", "Well, I will confess that I am not a warrior by trade."),
  ("npc3_signup", "Do you? Well, I am in no position to be picky! I would be pleased to join you."),
  ("npc4_signup", "Good! I look forward to vanquishing your enemies."),
  ("npc5_signup", "Why, that is a most generous offer."),
  ("npc6_signup", "Yes! You must have been sent by divine providence! Lead me -- lead me away from darkness!"),
  ("npc7_signup", "I might be. I could certainly use the money."),
  ("npc8_signup", "Can you? I shall accept your offer."),
  ("npc9_signup", "I would very much like that, sir"),
  ("npc10_signup", "Are you, now? Well, that's a sight better than swinging from a gibbet for desertion."),
  ("npc11_signup", "Why, I'll be a soldier myself! Help my old hands to a bit of loot to comfort me in my retirement. Two boys I bore, both soldiers' brats, and they became soldiers themselves. One had his head split by a Khergit war club, the other died of the pox, but at least they didn't die hungry."),
  ("npc12_signup", "As I told you, I am a surgeon, not some silk-robed university physician who has never touched a body. I can get my hands dirty."),
  ("npc13_signup", "Indeed? You would do well to enlist me."),
  ("npc14_signup", "I would be pleased to ride with you, at least for a little while, for pay and a share of any loot."),
  ("npc15_signup", "Geroia, eventually, but I'd welcome the opportunity to get a few denars in my pocket, first, so I don't come home empty handed. So if you promise me food and a share of the loot, I'd be happy to fight with you for a while."),
  ("npc16_signup", "Well, {sir/madame}, let me tell you. I may not know how to read and write, but I know the quickest way to a man's heart is between his fourth and fifth rib, if you understand me. "),

  ("npc1_signup_2", "I've ridden over a fair amount of rough country in my time, more often than not in a hurry. I'm a good tracker and I've got a good eye for terrain. So what do you say?"),
  ("npc2_signup_2", "I'm a fast learner. I can ride, and know a fair bit about trade, prices and such."),
  ("npc3_signup_2", "I think you would find I would be a most valuable addition to your ranks. I am well versed in the classics of literature and can declaim several of the epic poems of my people. I play the lute and am a skilled manager of household servants."),
  ("npc4_signup_2", "Note however that as a gentleman and the holder of a barony, I expect to be in a position of command, and not be treated as one of the common soldiers."),
  ("npc5_signup_2", "I shall not betray you -- so long, of course, as you do your duty to me by feeding me, paying me, and not dragging my miserable hide into a battle where there is no chance of winning. Hand me some salt, if you will -- it is the custom of our people to take salt from our captains, as a token of their concern for our well-being."),
  ("npc6_signup_2", "I am well practiced in the arts of war -- but I beg you, sir, I wish to use my skills to defend the innocent, the pure, and the defenseless, not to be a common brigand and wreak more misery than I have already wrought."),
  ("npc7_signup_2", "But let your followers know that I do not suffer louts and brutes. Anyone who misbehaves around me will quickly find an arrow in their gullet."),
  ("npc8_signup_2", "I shall be pleased to fight in your shield wall. But I warn you -- if you ask me to gather the firewood, or cook a meal, you will not like the consequences."),
  ("npc9_signup_2", "I am a gentleman, and prefer to fight with sword and lance. I recognize that you are of lower birth than I, there is no shame for me to serve under an experienced captain -- presuming, of course, that your followers do not become too familiar with me. I assume that will not be a problem?"),
  ("npc10_signup_2", "You won't regret taking me on, {Brother/Sister}. I'm a dead eye with a crossbow -- a beautiful weapon, it can right punch through a nobleman's armour and spill his blue blood upon the ground. And I've trained more raw recruits than you've had hot dinners, begging your pardon. I don't toadie to the high-born."),
  ("npc11_signup_2", "I know how to swing a blade, staunch a wound, and feed an army on the march. It would be a foolish captain who passed up the opportunity to hire an experienced campaigner like me! Say, {laddie/lassie}, don't you command a war party of your own, now?"),
  ("npc12_signup_2", "I have treated every variety of wound that can be inflicted by the hand of man. Before I was a surgeon, I was a student, so you may be sure that I have inflicted wounds as well as healed them."),
  ("npc13_signup_2", "Sword, lance, the bow -- my skill in all such martial pursuits is the stuff of epic verse.  Together we will perform such feats as will be recounted in festivals and campfires, in filthy taverns and in the halls of kings, for many generations to come."),
  ("npc14_signup_2", "I am a skilled swordsman, and I can also instruct your men in fighting. But I warn you that I do not care to fight for a leader who is lax in discipline with {his/her} men, for in the long run they will not respect a soft hand. "),
  ("npc15_signup_2", "Siegework is my speciality, although I reckon can handle myself well enough in an open battle, if need be."),
  ("npc16_signup_2", "I can throw knives, in addition to stabbing with them, and I'm slippery as quicksilver. You'll find me useful in a fight, I'll warrant."),


  ("npc1_signup_response_1", "Good. You can be useful to us."),
  ("npc2_signup_response_1", "That will do."),
  ("npc3_signup_response_1", "Um, that's a start. We can teach you the rest."),
  ("npc4_signup_response_1", "Very well. I'll be glad to have you with us, um, 'Baron.'"),
  ("npc5_signup_response_1", "Certainly. Here, have some salt."),
  ("npc6_signup_response_1", "Happy to be of service! Get your things together, and we shall be on our way."),
  ("npc7_signup_response_1", "I will hire you. Try not to shoot anyone on your first day."),
  ("npc8_signup_response_1", "No fear, ma'am. You're the widow and the daughter of a thane, and you'll be treated as such."),
  ("npc9_signup_response_1", "Well, it shouldn't be. I'll have a talk with them."),
  ("npc10_signup_response_1", "Good man. We'll treat you with the respect you deserve."),
  ("npc11_signup_response_1", "It sounds like you'll be useful. You are hired."),
  ("npc12_signup_response_1", "Then welcome to our company, doctor"),
  ("npc13_signup_response_1", "Good. Make yourself ready, and we'll be on our way. "),
  ("npc14_signup_response_1", "Good. I'll be happy to hire someone like you."),
  ("npc15_signup_response_1", "That works for me. I will be pleased to hire you."),
  ("npc16_signup_response_1", "It sounds like you can do the job. I will hire you."),

#11
  ("npc1_signup_response_2", "I'd prefer not to take the risk. Good day, sir."),
  ("npc2_signup_response_2", "I'm afraid I'm only looking for men with some experience. Good day to you."),
  ("npc3_signup_response_2", "Actually, we were looking for a slightly different skill-set."),
  ("npc4_signup_response_2", "Actually, we are not in the habit of hiring bandits with invented pedigrees. Good day, sir."),
  ("npc5_signup_response_2", "Actually, on second thought, I prefer to keep more civilized company."),
  ("npc6_signup_response_2", "On second thought, maybe a mercenary company is not what you need right now."),
  ("npc7_signup_response_2", "Actually, on second thought, you sound like you might be trouble. Good day to you. "),
  ("npc8_signup_response_2", "Ah. Actually, if you don't do whatever I order you to do, you'd best seek your fortune elsewhere."),
  ("npc9_signup_response_2", "You assume wrong, sir. In my company we respect courage and skill, rather than noble birth."),
  ("npc10_signup_response_2", "On second thought, we value discipline pretty highly in our company. Good day to you."),
  ("npc11_signup_response_2", "Sorry, madame. We've already got as many in our company as we can handle."),
  ("npc12_signup_response_2", "A battle is not the same thing as a tavern brawl. Perhaps you should look elsewhere for work."),
  ("npc13_signup_response_2", "Actually, on second thought, a fighter overeager for glory is dangerous to have in one's company."),
  ("npc14_signup_response_2", "Actually, I have no wish to provoke a mutiny in my ranks. Good day, sir."),
  ("npc15_signup_response_2", "Actually, I need a different kind of expertise. My apologies."),
  ("npc16_signup_response_2", "To be honest, I'd prefer someone who was a little less tempted to larceny."),

  ("npc1_payment", "I will be very useful to you, {sir/madame}, you can bet on that. Just one more thing before we leave, would you mind lending me {reg3} denars? I am ashamed to say it, but I have made myself a bit of debt here, staying in this tavern over the last few weeks and the tavern owners no longer believe that I am loaded with gold as I used to tell them. You know, things could get ugly here if they see me leaving with you before paying them."),
  ("npc2_payment", "."),
  ("npc3_payment", "."),
  ("npc4_payment", "Excellent. Before we depart, would you be so kind to lend me {reg3} denars? I had to pawn a family heirloom at a pawnbroker here in {s20}, and I would like to retrieve it before we leave."),
  ("npc5_payment", "Thank you. Now, to seal off our agreement, I ask for {reg3} denars from you. It's an advice my father gave me. He told me 'Baheshtur, never fight for a barbarian before {he/she} pays you your worth of gold first'."),
  ("npc6_payment", "."),
  ("npc7_payment", "All right then. I will come with you. But I want a payment of {reg3} denars first. You aren't expecting me to work for free, do you?"),
  ("npc8_payment", "Then I will fight your enemies for you. But first I want a bounty of {reg3} denars. If you are a worthy captain who can lead {his/her} company to riches and plunder, you should have no trouble paying. I cannot afford to follow a pauper."),
  ("npc9_payment", "That's very good of you. And before I join, can you lend me {reg3} denars, so that I can buy some proper clothing that befits a gentleman of noble birth such as myself. The coat on me has been worn down badly due to my recent bad fortune, and I cannot let common soldiers mistake me as one of their own."),
  ("npc10_payment", "That's good news. But I'll ask for one last thing, captain. I have a woman here in {s20}, a tavern wench, and she says she has my child in her belly. I want to give her some money before I leave... for the child, you know. Do you think you can spare {reg3} denars?"),
  ("npc11_payment", "Hey thank you captain. But before joining up with you, I would ask for a payment of {reg3} denars. I know that in war parties soldiers can go on for weeks without seeing any wages. I am wise enough not to sign anywhere without having myself covered."),
  ("npc12_payment", "."),
  ("npc13_payment", "Before I sign up, there is the small matter of some expenses I have incurred while staying here -- {reg3} denars. Do you think that you could cover those for me, as a gesture of friendship?"),
  ("npc14_payment", "Ah, one last thing. I would ask for an initial bounty of {reg3} denars before I join your command. It's my principle never to enter someone's service without receiving the payment I deserve."),
  ("npc15_payment", "Good. By the way, as a skilled engineer I would expect a payment for my services. A signing bonus of {reg3} denars would be fair, I think."),
  ("npc16_payment", "Now, that's good news, captain. So, how about paying me a little something to seal off our agreement? A mere {reg3} would be enough. Please don't take this the wrong way, but I've had some bad luck with employers in the past. "),

  ("npc1_payment_response", "Very well, here's {reg3} denars. Now, fall in with the rest."),
  ("npc2_payment_response", "."),
  ("npc3_payment_response", "."),
  ("npc4_payment_response", "Certainly. Here's {reg3} denars."),
  ("npc5_payment_response", "Well... here's {reg3} denars, then. Your first payment."),
  ("npc6_payment_response", "."),
  ("npc7_payment_response", "No, of course not. Here's {reg3} denars."),
  ("npc8_payment_response", "Oh, I am no pauper, madame. Here's {reg3} denars for you."),
  ("npc9_payment_response", "Very well, here's {reg3} denars."),
  ("npc10_payment_response", "Of course. Here, {reg3} denars."),
  ("npc11_payment_response", "Very well, here's {reg3} denars. Make yourself ready. We leave soon."),
  ("npc12_payment_response", "."),
  ("npc13_payment_response", "Of course, here's {reg3} denars. Make ready to leave soon."),
  ("npc14_payment_response", "All right, here's {reg3} denars. You are most welcome in our company."),
  ("npc15_payment_response", "All right, here's {reg3} denars. Glad to have you with us."),
  ("npc16_payment_response", "All right, here's {reg3} denars for you. Make yourself ready."),




  ("npc1_morality_speech", "Oy -- boss. Please don't take this the wrong way, but it's a hard life and it's a bit much that we {s21}. Take a little more care in the future, captain, if you don't mind my saying."),
  ("npc2_morality_speech", "I hope you don't mind my saying so, but it's a bit hard for me to see us {s21}. Maybe I ought to try to be more of a hardened soldier, but if we could try to exercise a little mercy from time to time, I'd sleep better."),
  ("npc3_morality_speech", "Perhaps it is not my place to say so, {sir/madame}, but I confess that I am somewhat shocked that we {s21}. Of course I realize that war is cruel, but there is no need to make it more cruel than necessary."),
  ("npc4_morality_speech", "Your pardon -- just so you know, the men of the House of Rolf do not care to {s21}. I will not be pleased if you continue to take this course."),
  ("npc5_morality_speech", "Pardon me, captain. It is not good to {s21}. Your first duty is to the men who have taken your salt. The least they can expect is food, pay, the opportunity to loot, and that you not waste their lives needlessly."),
  ("npc6_morality_speech", "Excuse me, {sir/madame}. As you know, I joined with you to right wrongs, protect the innocent, and make amends for my sin. I did not expect to {s21}."),
  ("npc7_morality_speech", "Captain -- I do not like to see us {s21}. Such are the actions of a common bandit chief, with no regard for his followers."),
  ("npc8_morality_speech", "I was not pleased that you decided to {s21}. To fall in battle is an honour, but to fight in a warband led by a coward is a disgrace."),
  ("npc9_morality_speech", "{Sir/Madame} -- it is not my way to {s21}. Men of my house will accept death but not dishonour. Please do not make me ashamed to serve under you."),
  ("npc10_morality_speech", "Begging your pardon, captain. I can't say that I'm happy to see us {s21}. Those are just simple people, trying to make a living. If we could try to go easy on the poor wretches, captain, I'd feel much better."),
  ("npc11_morality_speech", "Excuse me, captain. It's not good that we {s21}. I've followed armies and warbands for 30 years, and the least the soldiers expect of a leader is to feed them, pay them, and do {his/her} best to keep their sorry skins intact as best {he/she} can."),
  ("npc12_morality_speech", "Captain -- I do not like to see us {s21}. I am prepared to be a warrior, but not a brigand. Pray let us try to show a little more compassion."),
  ("npc13_morality_speech", "Captain, if we can avoid it, I'd prefer not to {s21}. Calradia is a small place, and one's reputation is precious. I would not care for one of my rivals to include this latest unfortunate incident in a satirical verse."),
  ("npc14_morality_speech", "I do not care to {s21}. No one with a reputation for cowardice will be properly feared by his men."),
  ("npc15_morality_speech", "{Sir/Madame} -- just so you know my opinion, any commander with sense will not let his company {s21}.I hope you don't mind me speaking so bluntly."),
  ("npc16_morality_speech", "Captain. I don't like to {s21}. So many throats left uncut, and so many purses left unexplored..."),


  ("npc1_2ary_morality_speech", "Boss -- just so you know, I've got no problem if we {s21}. Living to fight another day makes good sense to me."),
  ("npc2_2ary_morality_speech", "{Sir/Madame} -- I'm not altogether happy that we {s21}. I'm a merchant, and in our business one is bonded by one's word. I don't want a reputation for dishonesty -- that would spell my end as a trader, {sir/madame}."),
  ("npc3_2ary_morality_speech", "{Sir/Madame} -- I think it was a brave decision you took to {s21}. There is no shame in finding a way to avoid the spilling of blood."),
  ("npc4_2ary_morality_speech", "Your pardon -- whatever anyone else says, I think nothing of it that you {s21}. You should adopt whatever ruse you need to survive in these troubled times."),
  ("npc5_2ary_morality_speech", "[No secondary moral code]"),
  ("npc6_2ary_morality_speech", "{Sir/Madame} -- you may choose to {s21}, but would prefer to have no part in it. Such is not the path to my redemption."),
  ("npc7_2ary_morality_speech", "[No secondary moral code]"),
  ("npc8_2ary_morality_speech", "[No secondary moral code]"),
  ("npc9_2ary_morality_speech", "Captain, I am dismayed that you {s21}. A {gentleman/gentlewoman} such as yourself should exhibit the highest standards of honour at all times."),
  ("npc10_2ary_morality_speech", "{Brother/Sister} -- I can't say I like to see us {s21}. You should treat your men well, and they'll repay with interest."),
  ("npc11_2ary_morality_speech", "[No secondary moral code]"),
  ("npc12_2ary_morality_speech", "[No secondary moral code]"),
  ("npc13_2ary_morality_speech", "[No secondary moral code]"),
  ("npc14_2ary_morality_speech", "Captain -- you should not let it bother you that you {s21}. Armies are made to do their leaders' bidding, and hardships are part of a soldier's life."),
  ("npc15_2ary_morality_speech", "You know, friend {playername}, it's none too reassuring to see how you just {s21}. If you can break your word to them, you can break your word to me, is how I figure it."),
  ("npc16_2ary_morality_speech", "Captain -- just so you know, it's no problem by me that we {s21}. We do what we need to do to live, and they'd do the same to us if they were in our shoes."),

  ("npc1_personalityclash_speech", "Captain -- no offense, but I'm a bit tired of {s11}, who puts on airs like she's something better than your humble servant Borcha."),
  ("npc2_personalityclash_speech", "{Sir/Madame} -- as you recall I was a merchant before I signed on with you. I respect men who make their living peacefully, risking all to bring goods for far away lands."),
  ("npc3_personalityclash_speech", "Captain -- in my opinion, {s11} is a hard and cruel man. He speaks of nothing but the need to flog, beat, and hang his fellow soldiers."),
  ("npc4_personalityclash_speech", "{Sir/Madame}. The House of Rolf is one of the most ancient and respected families in this part of the world, with a provenance dating back to the Old Calradic Empire. Yet {s11} openly shows me disrespect, and casts doubt on the provenance of my house."),
  ("npc5_personalityclash_speech", "A moment of your time, captain. {s11} seems to think me a common bandit, just because I have rewarded myself in the past to the legitimate spoils of war from caravans passing through my family's lands."),
  ("npc6_personalityclash_speech", "Your pardon, {sir/madame}, but I cannot keep my tongue stilled any longer. That harlot, {s11} -- every time she sees me she points the five fingers of her hand at me -- a peasant's sign to ward off evil."),
  ("npc7_personalityclash_speech", "Captain, I have done my best to put up with your followers' rude talk and filthy habits. But that one who calls himself {s11} is beyond tolerance."),
  ("npc8_personalityclash_speech", "Just so you know, I cannot abide that insolent mountebank {s11}. Some minutes ago, I was remarking to our companions how the peasants of this region were more than usually slack-jawed and beetle-browed, and speculated that perhaps they had bred with apes."), 
  ("npc9_personalityclash_speech", "Sir -- {s11} is a base braggart, a man with no respect for the honour of women. I am tired of hearing how he conquered this or that damsel."),
  ("npc10_personalityclash_speech", "Excuse me, captain. I hate to trouble you with such things, but I just wanted to let you know that I can't abide that fellow Rolf, the one who calls himself a baron."),
  ("npc11_personalityclash_speech", "Begging your pardon, captain, but I can't keep silent. That man, {s11} -- he killed his own brother."),
  ("npc12_personalityclash_speech", "My lord. The barbarian woman, {s11}, complained of headaches -- a possible symptom of excess of sanguinity. I thought to apply my leeches."),
  ("npc13_personalityclash_speech", "Captain, I weary of {s11}, who talks of nothing but chivalry and feats of arms."),
  ("npc14_personalityclash_speech", "Excuse me, captain. A few minutes ago, I had expressed the opinion that liberal use of the lash and occasional use of the gallows is essential to keep soldiers in line. Men without a healthy fear of their commanders are more likely to run from battle."),
  ("npc15_personalityclash_speech", "Excuse me. I hope you don't mind me telling you that in my opinion, that girl {s11} is a danger to the party. She's a feral brat, disrespectful of authority and the basic principles of the military art."),
  ("npc16_personalityclash_speech", "Oy, captain. Just so you know -- there's something funny about {s11}. He makes strange scrawlings in the dirt, and mutters to himself."),

  ("npc1_personalityclash_speech_b", "She's a common bandit, just like myself, and she has no right to tell me to keep my distance from her, as she did just now."),
  ("npc2_personalityclash_speech_b", "I don't much care to hear {s11} gloat about the caravans he has looted, or he plans to loot, like he has no respect for good honest trade."),
  ("npc3_personalityclash_speech_b", "I know that an army is not a nursery, and that strong discipline is important, but I do believe that man enjoys cruelty for cruelty's sake. I hope you do not mind me saying so."),
  ("npc4_personalityclash_speech_b", "{Sir/madame}, these are indeed sorry days if common folk are allowed to mock their betters. That is all."),
  ("npc5_personalityclash_speech_b", "I told him that if the warrior's way bothers him so much, that he become a priest or a beggar and so not have to worry about such things. I hope you do not mind that I said such things."),
  ("npc6_personalityclash_speech_b", "I know the crime I committed was an abomination, but I am seeking repentance, and I deserve better than to be the object of some witch's superstition. I just thought you should know."),
  ("npc7_personalityclash_speech_b", "I do not care for how he stares at me around the campfire after a meal, as he picks his teeth. I believe I recognize him from my days as a bandit. He is base and ignorant. I do not care to travel with such people."),
  ("npc8_personalityclash_speech_b", "{s11}, that font of impudence, overheard me, and called me ignorant, and a savage, and other words I do not care to repeat. It was only out of respect for you that I refrained from cutting his throat then and there. I thought it only fit that I should warn you."),
  ("npc9_personalityclash_speech_b", "If he persists, I shall tell him that he is a base varlot, and if it comes to blows I will not apologize. That is all, {sir/madame}."),
  ("npc10_personalityclash_speech_b", "He's just a simple brigand, as far as I can tell. House of Rolf, my arse. Genuine blue-bloods are bad enough, but those who pretend to be blue-bloods are bloody intolerable. Anyway, I might have said something a bit sharp to him a minute ago. He seemed to take offense, anyway. I just thought you should know."),
  ("npc11_personalityclash_speech_b", "He's a kinslayer, cursed by heaven, and he'll bring misfortune and sorrow upon us, that's for certain. I don't like being around him and I don't think he should be with us. That's all. Sorry for troubling you."),
  ("npc12_personalityclash_speech_b", "But when I tried to afix them, she recoiled and struck me, and accused me of witchcraft. Captain, I am deeply tired of attending to the complaints of such an ungrateful and ignorant lot."),
  ("npc13_personalityclash_speech_b", "Valorous deeds are all very well, but they are not the only goals worth pursuing in life. Personally, I never trust any man who has not at least once woken up drunk in a ditch, or been beaten by the slipper of his lover."),
  ("npc14_personalityclash_speech_b", "That chit {s11} saw fit to admonish me for this. I will not have my methods questioned in front of the men, and I will not serve any commander who tolerates such insubordination in his company. Thank you for allowing me to speak my peace."),
  ("npc15_personalityclash_speech_b", "What's more, I suspect she's a thief. I found her going through my baggage and pawing some of my schematics, and she pulled a knife on me when I thought fit to object. A wise captain would not allow her in his company."),
  ("npc16_personalityclash_speech_b", "Fearing witchcraft, I asked him about it, and he told me that a chit of a girl like myself should mind her own business. So I had a look in his baggage, and found strange plans and diagrams. I think he's a sorceror, {sir/madame}, and if I catch him trying to hex me he'll have a knife in his throat."),

 
### set off by behavior after victorious battle
  ("npc1_personalityclash2_speech", "Oy -- boss, I don't fancy myself a sensitive soul, but I don't particularly like how {s11} went about cutting the throats of the enemy wounded, back there."),
  ("npc2_personalityclash2_speech", "{Sir/Madame}. If you don't mind, I'd prefer not to be deployed anywhere near {s11}, after what he said to me during that last battle."),
  ("npc3_personalityclash2_speech", "{Sir/Madame}. Since I have joined your company, I have tried hard to learn how to live like a soldier, and how to honour the warrior's code. If I occasionally make mistakes, I would hope to be forgiven."),
  ("npc4_personalityclash2_speech", "{Sir/Madame}. I happened to exchange a few words with {s11} as we were dividing up the spoils of battle. Please inform her that when she speaks to me, she should call me 'Baron' or perhaps 'Baron Rolf,' or 'Your Grace,' but certainly not just 'Rolf.'"),
  ("npc5_personalityclash2_speech", "Captain. {s11} needs to have her tongue cut out."),
  ("npc6_personalityclash2_speech", "My lord. Did you see {s11} during that last battle? He taunts the fallen foe as they lay stricken and helpless on the battlefield, mocking their parentage, their foolishness for having fought us."),
  ("npc7_personalityclash2_speech", "Captain -- I have been searching my mind trying to remember where I have seen {s11}, the one who calls himself a baron. As I watched him in action during that last battle, I suddenly remembered. He is a good fighter, but also a vicious one."), 
  ("npc8_personalityclash2_speech", "Captain. {s11} is a most insolent girl. I have tried to be polite, even friendly, only to have her rebuff me."),
  ("npc9_personalityclash2_speech", "{Sir/My lady}, I hope you do not mind me telling you this, but in my opinion {s11}, the merchant, does not know his place. During that last battle, he cut in front of me to engage a foe whom I had marked for my own."),
  ("npc10_personalityclash2_speech", "{Brother/Sister} -- a question for you. Are you in charge of this company, or is it {s11}?"),
  ("npc11_personalityclash2_speech", "Captain. I don't much care for that {s11}. After that last battle, he went around muttering some heathen incantation, as he went through the slain looking for loot."),
  ("npc12_personalityclash2_speech", "Captain. I can no longer abide the rank ignorance of {s11}. As I was treating the wounded during our last battle, he saw fit to disparage my use of laudanum in relieving the pain while I conducted surgery, and of treating wounds with a poultice of honey."),
  ("npc13_personalityclash2_speech", "Hello, captain! {s11} is a temperamental one, isn't he? During that last battle, I was merely having a friendly chat with our foes about their mothers as we exchanged swordblows, and it caused him to throw a fit!"),
  ("npc14_personalityclash2_speech", "Sir. {s11} is incorrigibly indisciplined. During that skirmish, I called out to him that he should hold ranks with the rest of our battle array. He called back to me that I should 'get stuffed.'"),
  ("npc15_personalityclash2_speech", "Captain -- I must tell you that I question {s11}'s medical credentials. As he was tending to our wounded after that last battle, I saw fit to remind him that the peerless Galerian often advocated administering a distillation of beetroot, to restore the humor imbalance brought by loss of sanguinity."),
  ("npc16_personalityclash2_speech", "Beg your pardon, sir. {s11} might have been a very good thief, but he's not got the stomach to be a warrior, if you ask me."),
   
  ("npc1_personalityclash2_speech_b", "The way she whistles cheerfully as she does it -- it puts a chill down my spine, it does."),#borcha - klethi 
  ("npc2_personalityclash2_speech_b", "The enemy was bearing down on us, and he says, 'Step aside, merchant, this is knight's work.' Next time I will step aside, and let him take a spear in the gut."), #marnid - alayen
  ("npc3_personalityclash2_speech_b", "After our last victory I was picking through the slain, and availed myself of one of our foe's purses. No sooner had I done so then {s11} came up behind me and struck it from my hands, saying that it was she who had made the kill, and thus she deserved the spoils. My lord, I could not tell in the heat of battle who had struck whom. If {s11} had simply told me that she deserved the purse, I would gladly have given it to her."),#Ymira - matheld
  ("npc4_personalityclash2_speech_b", "I am of noble blood, and she is of the basest birth. She must remember her place."),#Rolf - deshavi
  ("npc5_personalityclash2_speech_b", "When the loot was piled up after the last battle, I found among the enemy's baggage a very decent cooking pot. Often I had wished to find such a pot, so I could boil some of the stews that my people use to warm their bellies during the winter months. But {s11} grabs the pot, and tells me that I will not be allowed to 'taint' it with heathen food, and that it should properly belong to her. I yielded the pot to her, but I will not tolerate such disrespect in the future."), #beheshtur- katrin
  ("npc6_personalityclash2_speech_b", "My lord -- such hubris will not be overlooked by Heaven, and I fear we shall all of us pay the price."), #firentis - nizar
  ("npc7_personalityclash2_speech_b", "Back when I lived in the ravines, we would sometimes fight with a rival band called the Brethen of the Woods. Captain -- I would not trust any man who hides his origins, and particularly would not trust a common bandit who calls himself a lord."),#deshavi - rolf
  ("npc8_personalityclash2_speech_b",  "As we were cleaning our weapons after that last battle, I remarked that I thought her a handsome girl, and after I regained my lands I would happily find her a match with one of my warriors. I thought it was a very generous offer, as a woman disinherited by her father is hardly going to find herself awash in prospects. But rather than thank me, she simply turned her back without a word. It was only out of respect for your leadership that I did not immediately try to teach her some manners."),  #matheld - ymira
  ("npc9_personalityclash2_speech_b", "I appreciate that he is willing to risk his life in battle, but that alone does not make a gentleman. He is not of noble birth, and his family's wealth comes from commerce and usury. He may fight with us as an auxiliary, but should not attempt to steal glory from his betters."),# alayen - marnid
  ("npc10_personalityclash2_speech_b", "In that last battle he was shouting at me: 'Go forward, go back, hold the line.' When I told him to mind his own trimming he said he'd have me flogged.  Captain, that man is looking for a crossbow bolt in his chest, begging your pardon."), 
  ("npc11_personalityclash2_speech_b", "He said it was a prayer of thanksgiving for victory, but it didn't sound like that to me. Captain, I don't want him raising up the ghosts of the dead to make trouble for us on our travels. I think you had best be rid of him"),
  ("npc12_personalityclash2_speech_b", "Captain, if that man knew the slightest thing about medical matters, he would know that one should never undermine a patient's confidence in his doctor, particularly not during a complicated operation. If you would be kind enough to dismiss him from this company, you would be doing all of us a great service."), # jeremenus - artimenner
  ("npc13_personalityclash2_speech_b", "When all the dust settled, {s11} turned on me and told me not to 'tempt the wrath of the Heavens' with my 'hubris.' I responded that at least I hadn't killed my own brother, which I think bothers the Heavens a lot more than battlefield small talk. {s11} turns red like a baboon's arse and would have struck me had I not artfully dodged out of his away. Tell him to lighten up, will you?"), #nizar - firentis
  ("npc14_personalityclash2_speech_b", "{Sir/Madame}, such defiance of proper authority is a corrosive influence on our company, and I shall have him flogged if he does so again."), #lazalit - bunduk
  ("npc15_personalityclash2_speech_b", "{s11} responded that Galenian was an 'antiquated know-nothing.' Captain, no true doctor would have such disrespect for the great masters of the past. I do not believe you should employ such an obvious impostor."), #artimenner - jeremus
  ("npc16_personalityclash2_speech_b", "After our last scrap, I was slicing open the guts of some our foes to check for hidden gold, as a girl who counts her pennies ought. He gagged and muttered that I was an 'animal.' I'll inspect his innards for contraband if he doesn't keep a civil tongue in his head."), #klethi - borcha


  ("npc1_personalitymatch_speech", "Boss. {s11} back there didn't do badly in that last fight at all. He's a good egg, too."),
  ("npc2_personalitymatch_speech", "{Sir/Madame}. I just wanted to tell you that {s11} may be a rough sort, and I'll venture a thoroughgoing rogue as well, but I'm proud to call him my companion."),
  ("npc3_personalitymatch_speech", "Hello, {sir/madame}! I had just wanted to tell you that {s11} is a most gallant knight. Did you see him in our last battle?"),
  ("npc4_personalitymatch_speech", "Excuse me, {sir/madame}. I just wanted to say a word in praise of {s11}. He did well in that last battle."),
  ("npc5_personalitymatch_speech", "That was a fine battle, {playername} Bahadur! {s11} is a good man to have by our side in a fight."),
  ("npc6_personalitymatch_speech", "Captain. Sometimes I am troubled by all this bloodshed, although I know that proud warlords must be humbled, and cruel bandits tamed, if we are to restore peace to Calradia."),
  ("npc7_personalitymatch_speech", "Captain. I was just talking to {s11}. She may be a bit savage, but I believe that she is a faithful friend."),
  ("npc8_personalitymatch_speech", "A fine battle that was, captain. And I have to say, I admire the taunts that {s11} hurled at our enemy."),
  ("npc9_personalitymatch_speech", "Captain. {s11} acquitted herself well in that fight back there. A fine, modest maiden she is, if I dare say so myself."),
  ("npc10_personalitymatch_speech", "Ahoy, Brother! I wish you joy of your victory! Say, old Mother {s11}'s not bad in a scrap, is she, for a woman of her years? Although I'm getting to be a bit of an old dog myself, now."),
  ("npc11_personalitymatch_speech", "Ach, captain! A fight like that one sets my old joints a-creaking. Still, we licked them pretty good, didn't we?"),
  ("npc12_personalitymatch_speech", "A bloody business, captain, a bloody business -- although a necessary one, of course. {s11}, I believe, shares my ambivalence about this constant fighting."),
  ("npc13_personalitymatch_speech", "You have earned your name today, oh valorous one! And {s11}, too! I like that one. She sings the songs of her people as she goes into battle, which appeals to an artistic soul like my own."),
  ("npc14_personalityclash_speech", "Captain. It is a pleasure going into battle with men like {s11} by my side."),
  ("npc15_personalitymatch_speech", "Captain. I was just having a word with {s11} after our last battle, and it strikes me that the man has got a good head on his shoulders."),
  ("npc16_personalitymatch_speech", "Oy -- captain. I was just having a chat with {s11}, as we picked through the bodies after our last little scrap."),
   
  ("npc1_personalitymatch_speech_b", "Without good honest souls like him to bring silver into Calradia, scoundrels like me would have a hard time in life, I'll warrant. I'm glad to have him with us."),
  ("npc2_personalitymatch_speech_b", "Based on how he did in that last fight, I'd say that I'd trust my back to him any day, although I'd still keep a hand on my purse."),
  ("npc3_personalitymatch_speech_b", "I also confess that I find him a truly delightful companion, a man of both wit and manners. Perhaps, perhaps... Ah, but I say too much. Good day, {sir/madame}."),
  ("npc4_personalitymatch_speech_b", "You chose well to enlist him in our company. He knows a thing or two about a fight, and also knows the importance of respecting his comrades-in-arms, unlike some others I might mention."),
  ("npc5_personalitymatch_speech_b", "As for his other attributes, I doubt that he is any more a Baron than I am, but I have to admire the brazen way he makes that claim."),
  ("npc6_personalitymatch_speech_b", "I must say that {s11} is a source of great comfort to me. I have told him of my sin, and he said to me that Heaven will forgive my transgression, if I truly repent and truly desire such forgiveness. He is wise, and I am glad that he is with us."),
  ("npc7_personalitymatch_speech_b", "At some point in the future, if you have no need of our services, she has promised to go back to the ravines with me and find the bandits who murdered my lover, and help me take my revenge. It was a kind offer. I am glad that she is with us."),
  ("npc8_personalitymatch_speech_b", "He managed to include their geneology, their appearance, and their eating habits in a well-framed Old Calradic quatrain. I personally prefer the saga, but we Nords respect poetic craftwork when we hear it."),
  ("npc9_personalitymatch_speech_b", "Were she of noble blood, I might ask for her hand. It is a pity that she is a merchant's daughter. But speaking with her is a pleasant way to pass time on the march."),
  ("npc10_personalitymatch_speech_b", "Heh. It just goes to show that youth ain't everything, that experience also wins battles. I reckon she and I could teach the young puppies of the world a thing or two, couldn't we?"),
  ("npc11_personalitymatch_speech_b", "Old {s11} in particular showed them a thing or two, I thought. Not bad for the pair of us, I thought, given that between us we've probably seen close to a hundred winters."),
  ("npc12_personalitymatch_speech_b", "It saddens him deeply to take the lives of his fellow men, however just the cause. He and I have talked together of a brighter future, of the need to unite these petty warring kingdoms of Calradia, so that we may bring this time of troubles to an end."),
  ("npc13_personalitymatch_speech_b", "Also, although I normally prefer the coy to the Amazonesque, I confess that I have also noticed the femininity she tries to hide beneath her martial demeanour. True, she is a bit aloof on the march and in camp, but perhaps my fair words can melt the Nordic ice around her heart."),
  ("npc14_personalityclash_speech_b", "He is a professional soldier, and though he may not be as fast on his feet as some others, he knows the wisdom of holding together in a disciplined battle-line. You showed good sense in bringing him into this company."),
  ("npc15_personalitymatch_speech_b", "War, like any other affair, requires careful planning and preparation, and a firm grasp of strategic principals. All other things being equal, the best trained army will win the battle, an observation that I think our last fight bears out. The men may curse him now, but they'll learn to thank him, I'll warrant."),
  ("npc16_personalitymatch_speech_b", "Have you heard her story? Can you believe the wrongs done to her? I tell you, it makes my blood boil. I want to cut off all the little bits of those bastards who mistreated her -- and I'll do it, too, if we ever run into them in our travels."),

  
  ("npc1_retirement_speech", "I'm a bit tired of marching up and down the land, shedding my blood for someone else's cause. The loot is good, but I think I've got enough of that, now. I'm going to head back to my village, take a wife, settle down, maybe raise horses if I can afford it."),
  ("npc2_retirement_speech", "I'm getting a bit tired of the warrior's life. I'm going to invest my share of our loot into a cargo of goods -- furs, linens, velvets, probably -- and take them back over the mountains. I would like to thank you again for taking me on, and wish you the best of luck."),
  ("npc3_retirement_speech", "I am afraid I have something to tell you. I have decided that the warrior's life is not for me. I think it is probably too late for me to find a good marriage -- no one of my people would take a wife who had served with a company of soldiers -- but I may have enough money to start myself up as a merchant. I hope you will not be angry, {sir/madame}."),
  ("npc4_retirement_speech", "I have fought with you honourably, as befits a son of the House of Rolf, but I am not altogether satisfied with your leadership. I will go home to my ancestral estates, which are much in need of my services."),
  ("npc5_retirement_speech", "Bahadur -- since I have taken your salt, I have fought for you fiercely, and loyally. But you have not always repayed my service with the kind of leadership that I deserve. So I am going home, in the hope that the Khan's men have forgotten me, to see my father and brothers again."),
  ("npc6_retirement_speech", "I joined this company in the hope that you would lead me out of darkness, and indeed I have found a measure of peace here. But I have some qualms about your leadership, and have begun to suspect that the path to redemption can be found elsewhere."),
  ("npc7_retirement_speech", "I am tired of this squalid life of endless warfare, seeing men debased by fear, greed, lust, and a hundred other sins. I have money in my purse. I am going overseas to look for a better land than Calradia. I assume that you will fare well without me."),
  ("npc8_retirement_speech", "I have fought in your shield wall, and done well by it. But your leadership is not always to my liking, and anyways I have another task. I will take what plunder I have won and raise a warband of my own and sail to Nordland to take back my husband's hall from my treacherous brother-in-law. I wish you well."),
  ("npc9_retirement_speech", "We have fought well together, and earned ourselves much glory. But I have some reservations about your leadership, and at any rate have my patrimony to reclaim. I will be leaving you. Perhaps we will meet again."),
  ("npc10_retirement_speech", "I've had enough of tromping up and down the length and breadth of Calradia. I've got enough to buy a small bit of land somewhere, so I think I'll give that a try. So long, and best of luck to you."),
  ("npc11_retirement_speech", "You did an old woman a great service by taking her into your company. But I'm afraid I'm finding this life no more to my liking than driving a wagon. Too much cold, too much hunger, and at the end all I see in front of me is a hole in the ground. So I'll be off, although I don't know where."),
  ("npc12_retirement_speech", "I've done all right in your company. I filled my belly, put some gold in my purse, and broadened my knowledge of wounds and injury -- I can't complain about that! But I think right now that service in this company is holding me back. I have a duty to share my findings with other surgeons, and for that I need to hire scribes, who are rare in Calradia. I shall be going home"),
  ("npc13_retirement_speech", "As the luster of your name grows ever brighter, I fear that my own reputation will seem pale in comparison, as the moon is outshined by the sun. I have decided to strike out on my own. The very best of luck to you!"),
  ("npc14_retirement_speech", "I would like to inform you that I wish to sever our relationship. I intend to seek alternative employment."),
  ("npc15_retirement_speech", "I appreciate that you took me on, but I'm not altogether happy about how things have worked out. I'm going to head off elsewhere -- maybe go home, maybe find another job, I haven't quite decided yet."),
  ("npc16_retirement_speech", "I've had good times in this company, and I've found myself a pretty trinket or two on the battlefield, but right now it isn't working out. I'm leaving you to go offer my talents to someone else."),

  ("npc1_rehire_speech", "Boss -- it's good to see you again. I know we had our differences in the past, but to tell you the truth, those were some of the best days I've known. And, to tell you the truth, I've had a bit of difficulty finding work. Listen, if you'd be willing to have me back, I'd be willing to sign up with your company again."),
  ("npc2_rehire_speech", "{Sir/Madame}! It's good to see you again. But I'll confess -- I've been looking for you. I bought a load of goods like I told you I would, loaded them up, and took them back across the steppe -- but wouldn't you know it, I was hit again by Khergits, and lost it all. I guess I'm just destined to fight for my fortune. Also, people tell me that you've done very well for yourself. So tell me, {sir/madame}, would you have me back?"),
  ("npc3_rehire_speech", "Well, hello {sir/madame}! It is very good to see you again. I have not fared so well since we parted, I am afraid. My mother's family. whom I hoped would give me a start in trading, have not been as welcoming as I have hoped. I receive nothing but lectures from my aunts, on how I have ruined my prospects for marriage by taking service in a mercenary company. Perhaps I am better suited to war than to commerce, to share a meal over a campfire with rough fellows than to drink wine with the burghers of Veluca. {Sir/Madame}, I must ask you -- will you take me back?"),
  ("npc4_rehire_speech", "Why hello, captain. It's been a while. You've done well for yourself, I hear. For my part, I've been having some difficulties coaxing a living from my estates -- locusts, bad rains, unruly serfs, that sort of thing. I thought I might take up the sword once more. I know there's been some bad blood between us, but I'd be honoured to fight in your ranks once again."),
  ("npc5_rehire_speech", "{playername} Bahadur! Your fame grows ever greater -- even as far as my homeland, beyond the mountains. I'd returned there, hoping that the Khan's men had forgotten. Well, they had not -- even before I set foot in my valley, I had word from my family that both the Khan and the Humyan were looking for me. So I came back again, hoping you might forget any harsh words I had spoken, to see if I could fight with you once again."),
  ("npc6_rehire_speech", "It is good to see you, {sir/madame}. Everywhere I go, men are in awe of your deeds. I have not had it so well since I left. Wherever I go, I feel my demons returning. My soul is in turmoil. For reasons that I cannot fully explain, I had found peace in your company, even if I had questions about your leadership. Will you allow me to serve with you once again?"),
  ("npc7_rehire_speech", "Captain! It is good to see you. Forgive what I may have said when we parted. I took a ship out of Wercheg, bound for the east, but it was taken by pirates and after my ransom I was set ashore back here. There may be better places in the world than Calradia, but I have yet to see them. So I think, if it is my lot to live here, then your company is as good a livelihood as any. Will you have me back?"),
  ("npc8_rehire_speech", "Greetings to you, {playername}. I was wondering if the harsh words spoken between us in the past could be forgotten. I have been hunting among the Nords here, to see if I could find enough men to take back my husband's hall. But I could not find enough men to crew a longship, and those whom I gathered quickly got bored and wandered off -- not, I will add, before they drank away such gold as I had accumulated. So I thought back to the battles we fought together. Those were good days, and profitable ones too."),
  ("npc9_rehire_speech", "My dear, dear {man/lady}! So good it is to see you! I have sought service with the lords of this land, but have been most grieviously disappointed. Half of them ask me to collect debts from fellow lords, as though I were a banker's errand boy, or chase down his serfs, as though I were a farm overseer. One even asked me to murder one of his creditors! I have looked for you, to see if you would wish me to join you again."), #Alayen
  ("npc10_rehire_speech", "Captain! It's good to see you. You see, it turns out I'm not much of a farmer. Too soft on the hired hands, I figure. I let them rob me blind. I guess fighting is what I know best. So tell me, captain, are you still looking for good men?"),
  ("npc11_rehire_speech", "Captain! So good to see you! People say that you've been making gold hand over foot. I'm a fidgety old bag of bones, I'll admit. I left you because I wasn't satisfied with the warrior's life, but I spend a bit of time in town and I realize that there's worse things in life than a full belly, honest companions, and the joy of seeing the enemy run before you. So, would you be hiring again"),
  ("npc12_rehire_speech", "Captain! It's a fine thing to see an honest face like yours. This world is full of lies. I went home to publish my findings, hired some scribes and made a handful of codices, and waited for the commissions. But it turns out that the universities don't care about real medical knowledge rather than warmed-over Galerian. And publishers -- let me tell you, you never saw anyone so unscrupulous. They rent the books out chapter to by chapter to students to copy, but half of them aren't returned, and those that are have pages soaked in wine, and there's no longer a complete copy of my work anywhere. I'll keep trying, but first I need a bit of money in my pocket, first. Are you looking for a surgeon?"),
  ("npc13_rehire_speech", "Well hello there, oh valorous one. I had been hoping to see you again. Everywhere I go, I hear tales and songs of your deeds. I will admit that I felt a twinge of regret that we had parted ways, and, I'll confess, a twinge of jealousy as well at your reputation. I thought that once again I might fight by your side, and thus bask in the reflection of your glory. Perhaps we might ride together again, for a little while?"),
  ("npc14_rehire_speech", "Captain. It is good to see you. When last we parted, I was ready to swear that I would not serve you again, but perhaps I judged you too harshly. All over Calradia, men sing your praises. I have tried serving in other lords' armies, and believe me, what I have seen of them restores my opinion of your leadership. If you would have me in your company, I would fight for you again."),
  ("npc15_rehire_speech", "Why hello, {playername}. I can't say I'm entirely displeased to see you. You see, I took on another contract before I left, and sure enough, when it came time to collect the pay, the lord had nothing but talk and excuses and petty little complaints about my handiwork. I can't say I was always happy in your company, but at least I put gold directly into my purse after every battle. You still offering work?"),
  ("npc16_rehire_speech", "Captain! They say that you've done well for yourself since we last met. I'll come out and admit that I cursed your name when we parted ways, but thinking back on it you weren't all that bad. All these lords, they're glad enough to send me on little side errands, but they don't much care to have me in their main battle-line. Apparently I spook the men. I've heard it muttered that I'm a witch, or that I eat men's hearts after killing them, or other rot. Not that I mind stabbing a man while he's asleep, but it's a lot more gratifying when he's awake and kicking. So I thought I'd try to find you again, see if you'll take me on."),

#local color strings
  ("npc1_home_intro", "Boss -- did you know that I was born around here, in the high steppe? This is where I got my eye for horseflesh, because this is good land for horses, although a hard land for men. I suppose that's why the Khergits like it."),
  ("npc2_home_intro", "We're approaching Sargoth. That's where I was headed when the Khergits got me."),
  ("npc3_home_intro", "Can you smell that? Lemon trees, apples and crocus flowers, it's the scent of Veluca. I spent many a happy summer here when I was a girl, playing in the gardens of my mother's family while my father was away trading."),
  ("npc4_home_intro", "The Woods of Ehlerdah. Bah. This place is thick with bandits and outlaws."),
  ("npc5_home_intro", "Bahadur, we are nearing Halmar, largest town in the lower steppe. My mother's sister went here to marry a townsman and I thought to seek service with the lord here. That is when I ran into you."),
  ("npc6_home_intro", "I can see by the vines and terraces on the hillside that I am near home. I have no wish to see my family, so I will linger outside the walls if you go into town. I am sure that you will understand."),
  ("npc7_home_intro", "Do you smell that? Salt fish, rotting flax and river mud. The smells of my childhood. I want to retch."),
  ("npc8_home_intro", "Hmf. Do you hear that? It must be the crash of waves on the headland. We must be near Gundig's Point."),
  ("npc9_home_intro", "Behold the Rock of Rivacheg! The strongest fortress in Calradia. My father was one of those who held the line here against the Nords, when they first tried to push inland from the coast."),
  ("npc10_home_intro", "D'you smell that fresh air, Brother? This was my home, before I went abroad in search of coin. It's good to be up in the hills again. It's the smell of freedom. This is the cradle of Rhodok liberty, here under Grunwalder Castle"),
  ("npc11_home_intro", "I see the mountains. We must be getting near home."),
  ("npc12_home_intro", "We're passing by the site of one of my greatest medical triumphs, if that interests you."),
  ("npc13_home_intro", "Ah, Castle Ergellon! Such a lovely spot, by the deep lake. Such happy days I spent here, the summer before last."),
  ("npc14_home_intro", "Do you see that fortress up there, on the spur over the valley? Ismirala? I spent a winter there some years back, trying to train the lord's men."),
  ("npc15_home_intro", "You see that castle up on the hill? Culmarr Castle, it's called. I did some work there, not long ago. It's not as showy as some of the other castles in this land, but it's the finest stonework you ever saw."),
  ("npc16_home_intro", "Aye, captain, do you see those? Those are hare tracks in the snow. We must be getting near to my birthplace."),


  ("npc1_home_description", "Well, Khergits always lived here, even back in the old days, as the Emperor gave them gold and lands to keep out the other tribes. I'm told my grandfather was a Khergit chieftain, although my mother didn't know him, any more than I knew my father. When my mother was a lass, the Khergit started coming over the mountains in larger numbers, and now there's a Khergit Khan in Tulga."),
  ("npc2_home_description", "People say that the Nords are a bunch of bloodthirsty barbarians, but they have a good head for trade, if you ask me. They make the people up and down the coast grow flax, which they weave here into linen. It can't compete with Jelkala silks and velvets as a luxury fabric, but it makes good summertime wear and you can use it for the sails of ships. More importantly, linen was one of the few goods that someone else in Calradia wasn't already making."),
  ("npc3_home_description", "Veluca has wet winters and hot summers, but the people here build great cisterns to water their crops. They grow grapes -- Velucan wine is famous, {sir/madame} -- and those who can afford it make walled gardens, where fruit trees grow in abundance, and we sit at night listening to music, or playing chess, or merely sniff the night air."),
  ("npc4_home_description", "Well, you see, the King of Swadia declared this to be his personal hunting preserve, and said he'd kill any man who as much as strung his bow here. So what happens? Some family goes hungry, and succumbs to the temptation to poach, and the king's sheriff comes along and strings him up and takes his land. His sons, rather than starve, go bandit. And so naturally anyone in the whole valley who feels the need to run away from a debt or a nagging wife or a vengeful noble comes up here to join them, living on wild pigs and berries and the purses of unwary travellers."),
  ("npc5_home_description", "Khergits had always come here, to trade and raid, and in the last days of the Empire we began to settle. Just like the Vaegirs, Swadians, Rhodoks and Nords, we took the Emperor's coin to keep the other tribes at bay. But when the Great Horde attacked our homeland in my grandfather's day, we moved into this region in force. We pushed the Vaegirs back, and made their fortresses our own."),
  ("npc6_home_description", "Here in the Vale of Suno, our dialect and customs are closer than anywhere else in Calradia to those of the old Calrad Empire. We grow olives and wine, both crops brought to this land from overseas by the emperors, and also follow the old Calradic ways. We keep our pledges and pay our debts."),
  ("npc7_home_description", "Before I was married off, and before I was taken by bandits, I lived here. I was born in a hovel and spent my childhood in the fields. Our landlords were Nord, but we never saw them, merely their cursed minions and overseers. My father, coward that he was, cringed before them."),
  ("npc8_home_description", "You haven't heard the story? When Gundig Hairy-Breeks came to Calradia from Nordland, he planted his banner on the headland and said that it would remain there until he recaptured his 'inheritance.' His 'inheritance', he called it. Gundig believed the skalds who told him that the Emperor had bequeathed Calradia to the Nords, when in fact he just gave us a small strip of land along the coast, so that we would crew his galleys."),
  ("npc9_home_description", "The Nords would sail up the river in their longships. The townsmen of the coast could have stopped them, but they were cowards then, as they are today, and paid them a yearly stipend, known as the Nordgeld, to be let in peace. But the Vaegir king would not pay. My father decided to come over the mountains, to fight with the Vaegir hosts. Three summers in a row they tried to take the Rock, and each time the Vaegir lords held them back."),
  ("npc10_home_description", "In my father's day the Swadians would come calling, thinking to make us knuckle our foreheads and call them their overlords. But Grunwalder, an old veteran of the wars from the hills, showed us how to form a battleline with spear and crossbow that could break a Swadian charge. He fell in battle, but the people gave his name to the castle that was built here, where he fell, so that we would remember, and always stand firm against the horsemens' onslaught."),
  ("npc11_home_description", "I'm from Praven. You know the saying, {sir/madame} -- 'Barley grown in Uxkhal is made into ale in Praven, and we're all the better for it.' Not sure what that means, {sir/madame}, but it's true about the barley. And wheat, and oats. We grow more grain here in the Vale of Uxkhall then all the rest of Calradia put together, and our ale is the best, too. You can see it in the soil here -- rich and black, and smells of good harvests and full bellies."),
  ("npc12_home_description", "The lord over there in Almerra Castle had the dropsy, and had requested a doctor from Uxkhal to treat him. Like a typical university-educated doctor, he went right to Galerian for a cure. Galerian commends sun-metal for dropsy. Now most of Galerian's writings were useless back in the days of the Calradic emperors when they were first written down, and they're doubly worthless today, but he sometimes he hits upon the right cure by chance: sun-metal does cure some kinds of dropsy in small doses. However, sun-metal in large doses is poison, something that the Galerian-worshippers never grasped."),
  ("npc13_home_description", "I had come up here with a small Swadian force, but they were caught by the Rhodoks in the woods and their horsemen cut down amid the trees. I fled and found shelter by the lake, in the arms of the comeliest cowherd you ever saw. She took me to a cave near the high pastures, and would bring me cheese and berries, and tell me the tale from the hills. They say the lake is a gateway to the underworld, and sometimes on the fringes you can the noxious fumes beneath bubbling up to the surface. Such rustics they are!"),
  ("npc14_home_description", "I say 'trying' because in my opinion, Vaegirs don't take well to discipline. Finest archers you ever saw, and good riders too, but they have no stomach for fighting in ranks. Their skills serve them well enough against Khergits and Nords, particularly when they can hide behind walls, but I've seen Swadian knights cut through Vaegirs like a knife through butter. Now, a Rhodok spear-wall is designed to stop a Swadian charge in its tracks, and usually does."),
  ("npc15_home_description", "Like most castles that last around here, it's got foundations that are old Imperial Calradic. You can't see them any more with all the rebuilding, but the slabs are the size of a house. They must have been real sorcerors back in those days, because I don't see how they moved those things otherwise. Beautiful location, too -- Culmarr sits right in front of the pass leading out of Calradia, which allows the lord to charge a pretty penny in tolls during the three months of the year that it's not snowed in."),
  ("npc16_home_description", "The snows in these valleys don't melt until late in the year, and the land is hard to plough. You can grow a bit of barley, but not much else. But there's wealth here in the woods: deer, rabbit and lynx, meat and furs, and the mountains have iron, and traders would ship enough saltfish up the river from the coast to keep the people fed for the winter."),

  ("npc1_home_description_2", "They go easy on us Old Calradians, and don't ask for much in tax -- not that we would be able to pay in any case. The land isn't good enough for most crops. Frankly, it's only good for horse-rearing, and that only for half of the year, in the winter after the rains. In the summer they take their herds back into the mountains. Caravans come over the hills and bring spice to Tulga, but we don't see much of that money down in the villages."),
  ("npc2_home_description_2", "I had loaded up on saffron, cinnamon, cloves, pepper and other spices and a chest full of denars. I estimated that I could buy linens, furs, velvet, iron and wool, and the extra horses to carry them back, and I'd still make a profit. I just hadn't figured in the Khergits, who apparently don't care for others cutting in on their monopoly."),
  ("npc3_home_description_2", "The poets call Veluca a paradise, and I think for once that they do not exaggerate."),
  ("npc4_home_description_2", "How do I know this, you ask? Well... I was taken by them, and held for ransom, but I got away. That's really all there is to tell."),
  ("npc5_home_description_2", "Of course, you know how things go. My father's generation were hard warriors from the cold lands across the mountains, but this generation all has houses in the town and great estates and spend time as much trading as they do practicing archery. The next generation will grow soft on Velucan wine and will lose their lands to the next batch of illiterate hill-raiders to come over the mountains, just you watch. It's how things always were, and how things always will be."),
  ("npc6_home_description_2", "We men of Suno also never forget an insult, and avenge any wrong done unto us. Old-fashioned Calradic honour, I dare say, has brought me to my current fallen state. But despite that, I am proud to be from this region. Our lord is a vassal of the Swadian king in Praven, but as far as we are concerned his is just yet another barbarian chieftain, and we are the Empire's true heirs."),
  ("npc7_home_description_2", "We were allowed to fish the river, raise pigs amid the reedbeds, and grow whatever we could in our private plots, but in the open fields we were only permitted to grow flax, to be taken to Sargoth and woven into linen. So we were always hungry, and weak, and never had the courage to rebel."),
  ("npc8_home_description_2", "The skalds' tales at least gave Gundig an excuse to raise a warband -- not that we Nords ever need an excuse, mind. He sailed across the sea, rallied the Calradian Nords to his banner, and marched on the Rock of Rivacheg. The Vaegirs killed him, and threw his banner into the surf. But the Nords keep coming, and some day all of Calradia will be ours."),
  ("npc9_home_description_2", "Just as the Nords can call on their kinfolk overseas, so does the Vaegir king call on his kinfolk from over the mountains. Had my father not disinherited me, I would also have taken an oath of fealty to the lord of Reyvadin. But just as I was shorn of my inheritance, so also was I shown of my obligations, and it is the Vaegir king's loss."),
  ("npc10_home_description_2", "We grow mulberry trees here for silk and kermes too for the dye. We take it to Jelkala where they weave it into the finest velvet -- not that I have ever had enough denars in my pocket to buy velvet, mind. But the craftsmen of Jelkala also make good crossbows, and for that I'll not begrudge them their little luxuries"),
  ("npc11_home_description_2", "The Swadian king will tell you that Praven was the biggest city in Calradia back under the Empire, and that's why he should rule the whole land today. Mind you, I don't care much about politics, {sir/madame} -- I've sold provisions to every army that ever marched in Calradia, and I tell you that I wouldn't give a single one of them a single biscuit unless I had the cold, hard denars in my hand first. Why these high and mighty kings and nobles can't pay their bills, I'll never know. But I prattle on a bit, there, don't I?"),
  ("npc12_home_description_2", "The difference between poison and cure is the dose. You tell that to everyone you meet, and tell them you heard it first from Jeremus the Great. People think that all the wisdom worth knowing was written in Old Calradic, but I say you can learn twice as much from village midwives and careful examination of nature than from the entire imperial corpus. That's why they threw me out of the university, although in retrospect that was a blessing. Anyway, I put that lord back on his feet, and he availed me of a sack of gold and the corpse of a freshly hanged criminal to dissect. Ha! To think of the lengths I had to go to get specimens back in those days."),
  ("npc13_home_description_2", "Eventually I had to leave, and sometimes I wonder if there is a little herdsboy swaddled on her back, as she takes the cows up to pasture each morning. I'd be tempted to try to find her -- but no, no, one should never look back."),
  ("npc14_home_description_2", "If anyone were ever to unify this little land of ours, I'd sign up to serve them, free of charge. I'd put together an army of Rhodok spears with Nord footmen on the flanks and Vaegir archers in front, take along some Khergit scouts to find and fix the enemy, and some Swadian lancers to finish them off. I'd take that army over the mountains and make the whole world kneel to Calradia.... Of course, that's what the Emperors thought, and in the end the tribes took away their Empire."),
  ("npc15_home_description_2", "And here's the funny thing -- when the Rhodok lands first rebelled against the Swadians, they all said they weren't going to have any noble lords ruling over them. You can guess how long that lasted. One Rhodok hill chieftain sets himself up in Culmarr, calls himself 'Count', and the good burghers of Jelkala and Veluca have to lick his boots if they want to sell their wine and velvet outside Calradia. And if you want to keep the counts under control, and the peasants providing the towns with food rather than selling to the highest bidder, then you need a King too, don't you? The Rhodok lands are no different than anyone else, whatever guff they talk about 'ancient liberties' and 'freedom.'"),
  ("npc16_home_description_2", "Still, it was a thin living, and there were always too many mouths around to feed. The Vaegir king and the Khergit khan don't make life any easier for us, squeezing for tax money the villages they control, and raiding for plunder the villages they don't. Of course, I can't say I'd do any differently do the same if I had a castle and an army all of my own. The mighty do whatever the can, and the humble do whatever they must."),

  ("npc1_home_recap", "I'm from the high steppe, near {s21}."),
  ("npc2_home_recap", "I was born over the mountains.  I'm a merchant, the son of a merchant, and the grandson of a merchant."),
  ("npc3_home_recap", "I used to live in my father's house in {s20}, but I spent much of my childhood in {s21}."),
  ("npc4_home_recap", "Our ancestral barony is over the mountains, across the Culdarr pass."),
  ("npc5_home_recap", "I was born in the highlands on the other side of the mountains, past Tulga, but I have relatives in {s21}."),
  ("npc6_home_recap", "My family lives in {s21}, but I cannot bear to face them."),
  ("npc7_home_recap", "I was born in a hovel in the fens, not far from {s21}."),
  ("npc8_home_recap", "I was born overseas, in Nordland, and my husband's hall also was in Nordland."),
  ("npc9_home_recap", "I am from the Vaegir homeland over the mountains, where the Vaegir lords lived before the Emperor brought them in Calradia."),
  ("npc10_home_recap", "Born and raised in Jelkala, {Brother/Sister}, and I hope some day to buy land there. But I had a mind to see a bit of the world first, so I took my crossbow and went off to the wars."),
  ("npc11_home_recap", "I was born in the train of an army, and lived all my days in the train of an army. My folk are from Praven, however, so I guess that's as much home to me as anywhere."),
  ("npc12_home_recap", "I come from overseas. I travel the world in search of medical lore."),
  ("npc13_home_recap", "Oh, far away from here, my {lord/lady}, else you would already have heard about me, and would not need to ask such things."),
  ("npc14_home_recap", "I am the younger son of the Count of Geroia."),
  ("npc15_home_recap", "I'm from over the hills. But Calradia is where the money is to be made, these days, if your trade is siegecraft."),
  ("npc16_home_recap", "Why, captain, I was born in Uslum village, but my mother lost her land to a scheming relative and had to put herself in bond to a nearby lord."),

  ("npc1_honorific", "boss"), #Borcha
  ("npc2_honorific", "{sir/madame}"), #marnid
  ("npc3_honorific", "{sir/madame}"),
  ("npc4_honorific", "{sir/madame}"),
  ("npc5_honorific", "{playername} Bahadur"), #beheshtur
  ("npc6_honorific", "captain"), #firentis
  ("npc7_honorific", "captain"), #deshavi
  ("npc8_honorific", "{playername}"), #matheld
  ("npc9_honorific", "{my good sir/my good lady}"), #Alayen
  ("npc10_honorific", "{Brother/Sister}"), #Bunduk
  ("npc11_honorific", "{laddie/lassie} -- I mean Captain"), #katrin
  ("npc12_honorific", "captain"),
  ("npc13_honorific", "oh valorous one"), #nizar
  ("npc14_honorific", "commander"), #lazalit
  ("npc15_honorific", "captain"), #artimenner
  ("npc16_honorific", "captain"), #klethi


#NPC companion changes end

#Troop Commentaries begin
#Tags for comments are = allied/enemy, friendly/unfriendly, and then those related to specific reputations
#Also, there are four other tags which refer to groups of two or more reputations (spiteful, benevolent, chivalrous, and coldblooded)
#The game will select the first comment in each block which meets all the tag requirements

#Beginning of game comments
("comment_intro_liege_affiliated", "I am told that you are pledged to one of the pretenders who disputes my claim to the crown of Calradia. But we may still talk."),

("comment_intro_famous_liege", "Your fame runs before you! Perhaps it is time that you sought a liege worthy of your valor."),
("comment_intro_famous_martial", "Your fame runs before you! Perhaps we shall test each other's valor in a tournament, or on the battlefield!"),
("comment_intro_famous_badtempered", "I've heard of you. Well, I'm not one for bandying words, so if you have anything to say, out with it."),
("comment_intro_famous_pitiless", "I know your name. It strikes fear in men's hearts. That is good. Perhaps we should speak together, some time."),
("comment_intro_famous_cunning", "Ah, yes. At last we meet. You sound like a good {man/woman} to know. Let us speak together, from time to time."),
("comment_intro_famous_sadistic", "I know your name -- and from what I hear, I'll warrant that many a grieving widow knows too. But that is no concern of mine."),
("comment_intro_famous_goodnatured", "I've heard of you! It's very good to finally make your acquaintance."),
("comment_intro_famous_upstanding", "I know your name. They say you are a most valiant warrior. I can only hope that your honour and mercy matches your valor."),

("comment_intro_noble_liege", "I see that you carry a nobleman's banner, although I do not recognize the device. Know that I am always looking for good men to fight for me, once they prove themselves to be worthy of my trust."),
("comment_intro_noble_martial", "I see that you carry a nobleman's banner, but I do not recognize the device. Perhaps one day we shall test each other's valor in a tournament, or on the battlefield!"),
("comment_intro_noble_badtempered", "I don't recognize the device on your banner. No doubt another foreigner come to our lands, as if we didn't have so many here already."),
("comment_intro_noble_pitiless", "I see that you carry a nobleman's banner, but I do not recognize the device. Another vulture come to grow fat on the leftovers of war, no doubt!"),
("comment_intro_noble_cunning", "I see that you carry a nobleman's banner, but I do not recognize the device. Still, it is always worthwhile to make the acquaintance of {men/women} who may one day prove themselves to be great warriors."),
("comment_intro_noble_sadistic", "I see that you carry a nobleman's banner, but I do not recognize the device. Perhaps you are the bastard {son/daughter} of a puffed-up cattle thief? Or perhaps you stole it?"),
("comment_intro_noble_goodnatured", "I see that you carry a nobleman's banner, but I do not recognize the device. Forgive my ignorance, {sir/madame}! It is good to make your acquaitance."),
("comment_intro_noble_upstanding", "I see that you carry a nobleman's banner, but I do not recognize the device. No doubt you have come to Calradia in search of wealth and glory. If this indeed is the case, then I only ask that you show mercy to those poor souls caught in the path of war."),

("comment_intro_common_liege", "You may be of common birth, but know that I am always looking for good men to fight for me, if they can prove themselves to be worthy of my trust."),
("comment_intro_common_martial", "Perhaps you are not of gentle birth, but if you prove yourself a {man/woman} of valor, then I would be pleased to try my strength against yours in the tournament or on the battlefield."),
("comment_intro_common_badtempered", "Speak quickly, if you have anything to say, for I have no time to be bandying words with common soldiers of fortune."),
("comment_intro_common_pitiless", "You have the look of a mercenary, another vulture come to grow fat on the misery of this land."),
("comment_intro_common_cunning", "Well... I have not heard of you, but you have the look of a {man/woman} who might make something of {himself/herself}, some day."),
("comment_intro_common_sadistic", "Normally I cut the throats of impudent commoners who barge into my presence uninvited, but I am in a good mood today."),
("comment_intro_common_goodnatured", "Well, you look like a good enough sort."),
("comment_intro_common_upstanding", "Peace to you, and always remember to temper your valor with mercy, your courage with honour."),


#Actions vis-a-vis civilians
  ("comment_you_raided_my_village_enemy_benevolent",    "You have attacked innocent farmers under my protection in the village of {s51}.  I will punish you for your misdeeds!"), 
  ("comment_you_raided_my_village_enemy_spiteful",      "You have raided my village of {s51}, destroying my property and killing the tenants. I will take my compensation in blood!"), 
  ("comment_you_raided_my_village_enemy_coldblooded",   "You have raided my village of {s51}, destroying my property and killing the tenants. I will make you think twice before you disrupt my revenues like that again."), 
  ("comment_you_raided_my_village_enemy",               "You have raided my village of {s51}, destroying my property and killing tenants under my protection. You will pay the price for your crime!"), 
  ("comment_you_raided_my_village_unfriendly_spiteful", "You have raided my village of {s51}. Do it again and I'll gut you like a fish."),
  ("comment_you_raided_my_village_friendly",            "You have raided my village of {s51}. This will place a grave strain on our friendship."),
  ("comment_you_raided_my_village_default",             "You have raided my village of {s51}. If you continue to behave this way, we may soon come to blows."),

  ("comment_you_robbed_my_village_enemy_coldblooded", "You have robbed my tenants in the village of {s51}. I take that as a personal insult."), 
  ("comment_you_robbed_my_village_enemy",             "You have robbed innocent farmers under my protection in the village of {s51}.  I will punish you for your misdeeds!"), 
  ("comment_you_robbed_my_village_friendly_spiteful", "I have heard that you pinched some food from my tenants at {s51}. Well, I'll not begrudge you a scrap or two, but keep in mind that I'm the one who must listen to their whining afterward."),
  ("comment_you_robbed_my_village_friendly",          "I have heard that you requisitioned supplies from my tenants at {s51}. I am sure that you would not have done so were you not desperately in need."),
  ("comment_you_robbed_my_village_default",           "You have robbed my tenants in the village of {s51}. If you continue to behave this way, we may soon come to blows."),

  ("comment_you_accosted_my_caravan_enemy",          "You have been accosting caravans under my protection. But your trail of brigandage will soon come to an end."),
  ("comment_you_accosted_my_caravan_default",        "You have been accosting caravans under my protection. This sort of behavior must stop."),

  ("comment_you_helped_villagers_benevolent",                "I heard that you gave charity to my tenants in the village of {s51}. I had been neglectful in my duties as lord and protector, and I appreciate what you have done."),
  ("comment_you_helped_villagers_friendly_cruel",            "I heard that you gave charity to my tenants in the village of {s51}. I appreciate that you meant well, but I'd rather you not undercut my authority like that."),
  ("comment_you_helped_villagers_friendly",                  "I heard that you gave charity to my tenants in the village of {s51}. Times are hard, and I know that you mean well, so I will not object to you providing them with assistance."),
  ("comment_you_helped_villagers_unfriendly_spiteful",       "I heard that you gave charity to my tenants in the village of {s51}. As amusing as it is to see you grubbing for favor among my vassals, I would ask you to mind your own business."),
  ("comment_you_helped_villagers_cruel",                     "I heard that you gave charity to my tenants in the village of {s51}. As the peasants' lord and protector, it is most properly my duty to assist them in times of hardship. You may mean well, but your actions still undercut my authority. I would thank you to leave them alone."),
  ("comment_you_helped_villagers_default",                   "I heard that you gave charity to my tenants in the village of {s51}. Times are hard, and I know that you mean well, but try not to make a habit of it. I am their lord and protector, and I would rather not have them go looking to strangers for assistance."),


#Combat-related events


  ("comment_you_captured_a_castle_allied_friendly",            "I heard that you have besieged and taken {s51}. That was a great dead, and I am proud to call you my friend!"), 
  ("comment_you_captured_a_castle_allied_spiteful",            "I heard that you have besieged and taken {s51}. Good work! Soon, we will have all their fortresses to despoil, their treasuries to ransack, their grieving widows to serve us our wine."), 
  ("comment_you_captured_a_castle_allied_unfriendly_spiteful", "I heard that you have besieged and taken {s51}. Well, every dog has his day, or so they say. Enjoy it while you can, until your betters kick you back out in the cold where you belong."), 
  ("comment_you_captured_a_castle_allied_unfriendly",          "I heard that you have besieged and taken {s51}. Whatever our differences in the past, I must offer you my congratulations."), 
  ("comment_you_captured_a_castle_allied",                     "I heard that you have besieged and taken {s51}. We have them on the run!"), 

  ("comment_you_captured_my_castle_enemy_spiteful",            "I hear that you have broken into my home at {s51}. I hope the dungeon is to your liking, as you will be spending much time there in the years to come."),
  ("comment_you_captured_my_castle_enemy_chivalrous",          "You hold {s51}, my rightful fief. I hope you will give me the chance to win it back!"),
  ("comment_you_captured_my_castle_enemy",                     "You have something that belongs to me -- {s51}. I will make you relinquish it."),

###Add some variation to these
  ("comment_we_defeated_a_lord_unfriendly_spiteful",           "I suppose you will want to drink to the memory of our victory over {s54}. Well, save your wine -- it will take more than that to wipe out the stain of your earlier disgraces."), 
  ("comment_we_defeated_a_lord_unfriendly",                    "I will not forget how we fought together against {s54}, but I can also not forget the other matters that lie between us."), 
  ("comment_we_defeated_a_lord_cruel",                         "That was a great victory over {s54}, wasn't it? We made of his army a feast for the crows!"), 
  ("comment_we_defeated_a_lord_quarrelsome",                   "I won't forget how we whipped {s54}? I enjoyed that."), 
  ("comment_we_defeated_a_lord_upstanding",                    "I will not forget our victory over {s54}. Let us once again give thanks to heaven, and pray that we not grow too proud."), 
  ("comment_we_defeated_a_lord_default",                       "That was a great victory over {s54}, wasn't it? I am honoured to have fought by your side."), 

  ("comment_we_fought_in_siege_unfriendly_spiteful",           "I suppose you will want to drink to the memory of our capture of {s51}. Well, save your wine -- it will take more than that to wipe out the stain of your earlier disgraces."), 
  ("comment_we_fought_in_siege_unfriendly",                    "I will not forget how we together we stormed {s51}, but I can also not forget the other matters that lie between us."), 
  ("comment_we_fought_in_siege_cruel",                         "I won't forget how we broke through the walls of {s51} and put its defenders to the sword. It is a sweet memory."), 
  ("comment_we_fought_in_siege_quarrelsome",                   "Remember how the enemy squealed when we came over the walls of {s51}? They had thought they were safe! We wiped the smug smiles of their faces!"), 
  ("comment_we_fought_in_siege_upstanding",                    "I will not forget our capture of {s51}. Let us once again give thanks to heaven, and pray that we not grow too proud."), 
  ("comment_we_fought_in_siege_default",                       "I will not forget how together we captured {s51}. I am honoured to have fought by your side."), 

  ("comment_we_fought_in_major_battle_unfriendly_spiteful",    "I suppose you will want to drink to the memory of our great victory near {s51}. Well, save your wine -- it will take more than that to wipe out the stain of your earlier disgraces."), 
  ("comment_we_fought_in_major_battle_unfriendly",             "I will not forget how we fought together in the great battle near {s51}, but I can also not forget the other matters that lie between us."), 
  ("comment_we_fought_in_major_battle_cruel",                  "I won't forget the great battle near {s51}, when we broke through the enemy lines and they ran screaming before us. It is a sweet memory."), 
  ("comment_we_fought_in_major_battle_quarrelsome",            "That was a fine fight near {s51}, when we made those bastards run!"), 
  ("comment_we_fought_in_major_battle_upstanding",             "I will not forget how we fought side by side at the great battle near {s51}. Let us once again give thanks to heaven, and pray that we not grow too proud."), 
  ("comment_we_fought_in_major_battle_default",                "I will not forget how we fought side by side at the great battle near {s51}. I am honoured to have fought by your side."), 




  ("comment_you_defeated_a_lord_allied_liege",                   "So, you crossed swords with that rascal they call {s54}, and emerged victorious. I am very happy to hear that."), 
  ("comment_you_defeated_a_lord_allied_unfriendly_spiteful",     "I heard that you fought and defeated {s54}. Every dog has its day, I suppose."), 
  ("comment_you_defeated_a_lord_allied_spiteful",                "I heard that you fought and defeated that dog {s54}. Ah, if only I could have heard him whimpering for mercy."), 
  ("comment_you_defeated_a_lord_allied_unfriendly_chivalrous",   "I heard that you fought and defeated {s54}. I hope that you did not use dishonourable means to do so."),
  ("comment_you_defeated_a_lord_allied",                         "I heard that you fought and defeated {s54}. I wish you joy of your victory."), 

  ("comment_you_defeated_me_enemy_chivalrous", "I will not begrudge you your victory the last time that we met, but I am anxious for another round!"), 
  ("comment_you_defeated_me_enemy_spiteful",   "I have been looking forward to meeting you again. Your tricks will not deceive me a second time, and I will relish hearing your cries for mercy."), 
  ("comment_you_defeated_me_enemy",            "When last we met, {playername}, you had the better of me. But I assure you that it will not happen again!"), 

  ("comment_I_defeated_you_enemy_spiteful",          "Back for more? Make me fight you again, and I'll feed your bowels to my hounds."), 
  ("comment_I_defeated_you_enemy_chivalrous",        "Come to test your valor against me again, {playername}?"), 
  ("comment_I_defeated_you_enemy_benevolent",        "So once again you come at me? Will you ever learn?"), 
  ("comment_I_defeated_you_enemy_coldblooded",       "You are persistent, but a nuisance."),
  ("comment_I_defeated_you_enemy",                   "How many times must I chastise you before you learn to keep your distance?"), 


  ("comment_we_were_defeated_unfriendly_spiteful",   "Last I saw you, you had been struck down by the men of {s54}. I blame you for that disaster. What a pity to see that you survived."), 
  ("comment_we_were_defeated_unfriendly",            "Last I saw you, you had been struck down by the men of {s54}. Well, I see that you survived."), 
  ("comment_we_were_defeated_cruel",                 "Last I saw you, you had been struck down by the men of {s54}. Don't worry -- we'll find him, and make him choke on his victory."), 
  ("comment_we_were_defeated_default",               "Last I saw you, you had been struck down by the men of {s54}. It is good to see you alive and well."), 

  ("comment_you_were_defeated_allied_friendly_spiteful",      "I heard that {s54} gave you a hard time. Don't worry, friend -- I'll find him for you, and make you a gift of his head."), 
  ("comment_you_were_defeated_allied_unfriendly_cruel",       "I had heard that {s54} slaughtered your men like sheep. But here you are, alive. Such a disappointment!"), 
  ("comment_you_were_defeated_allied_spiteful",               "I heard that {s54} crushed you underfoot like an ant. Hah! Children should not play games made for grown-ups, little {boy/girl}!"), 
  ("comment_you_were_defeated_allied_pitiless",               "I heard that {s54} defeated you, and scattered your forces. That is most disappointing..."), 
  ("comment_you_were_defeated_allied_unfriendly_upstanding",  "I heard that {s54} defeated you. Perhaps you should consider if you have considered any misdeeds, that might cause heaven to rebuke you in this way."), 
  ("comment_you_were_defeated_allied_unfriendly",             "I heard that {s54} defeated you. Look, try not to get too many of our men killed, will you?"), 
  ("comment_you_were_defeated_allied",                        "I heard that {s54} defeated you. But take heart -- the tables will soon be turned!"), 

  ("comment_you_helped_my_ally_unfriendly_chivalrous",        "I heard that you saved {s54} from likely defeat. Whatever else I may think of you, I must at least commend you for that."), 
  ("comment_you_helped_my_ally_unfriendly",                   "[revelance should be zero, and this message should not appear]"), 
  ("comment_you_helped_my_ally_liege",                        "I heard that you saved my vassal {s54} from likely defeat. "), 
  ("comment_you_helped_my_ally_unfriendly_spiteful",          "I heard that you rode to the rescue of our poor {s54}. Did you think him a damsel in distress? No matter -- it's a common mistake."), 
  ("comment_you_helped_my_ally_spiteful",                     "I heard that you saved {s54} from a whipping. You should have let him learn his lesson, in my opinion."), 
  ("comment_you_helped_my_ally_chivalrous",                   "I heard that you got {s54} out of a tight spot. That was a noble deed."), 
  ("comment_you_helped_my_ally_default",                   "I heard that you got {s54} out of a tight spot. Good work!"), 
 
  ("comment_you_were_defeated_allied_unfriendly",             "I heard that {s54} defeated you. Look, try not to get too many of our men killed, will you?"), 
  ("comment_you_were_defeated_allied",                        "I heard that {s54} defeated you. But take heart -- the tables will soon be turned!"), 

  ("comment_you_abandoned_us_unfriendly_spiteful",     "You worm! You left us alone to face {s54}, didn't you? I spit at you."), 
  ("comment_you_abandoned_us_unfriendly_pitiless",     "Well... You abandoned me in the middle of a battle with {s54}, didn't you? I'll see you buried in a traitor's grave."), 
  ("comment_you_abandoned_us_spiteful",                "You disappeared in the middle of that battle with {s54}... I hope you have a good explanation. Did your bowels give out? Were you shaking too hard with fear to hold your weapon?"), 
  ("comment_you_abandoned_us_chivalrous",              "What happened? You disappeared in the middle of that battle against {s54}. I can only hope that you were too badly wounded to stand, for I would be ashamed to have gone into battle alongside a coward."), 
  ("comment_you_abandoned_us_benefitofdoubt",          "What happened? You disappeared in the middle of that battle against {s54}. I assume that you must have been wounded, but it did look suspicious."), 
  ("comment_you_abandoned_us_default",                 "What happened? One moment you were fighting with us against {s54}, the next moment you were nowhere to be found?"), 

  ("comment_you_ran_from_me_enemy_spiteful",          "Last time we met, you ran from me like a whipped dog. Have you come back to bark at me again, or to whine for mercy?"), 
  ("comment_you_ran_from_me_enemy_chivalrous",        "Last time we met, you fled from me. Learn to stand and fight like a gentleman!"), 
  ("comment_you_ran_from_me_enemy_benevolent",        "When I saw you flee the last time that we met, I had hoped that I would not have to fight you again."), 
  ("comment_you_ran_from_me_enemy_coldblooded",       "Last time we met, you fled from me. That was a wise decision"),
  ("comment_you_ran_from_me_enemy",                   "You may have been able to escape the last time we crossed paths, but the next time I doubt that you be so lucky."), 

  ("comment_you_ran_from_foe_allied_chivalrous",      "They say that you fled from {s54}, leaving your men behind. I pray that this is not true, for such conduct does dishonour to us all."), 
  ("comment_you_ran_from_foe_allied_upstanding",      "They say that you fled from {s54}, leaving your men behind. I do not always believe such rumors, and I also know that desperate straits call for desperate measures. But I beg you to take more care of your good name, for men will not fight in our armies if they hear that we abandon them on the field of battle."), 
  ("comment_you_ran_from_foe_allied_spiteful",        "By the way, they said that you ran away from {s54} like a quaking little rabbit, leaving your men behind to be butchered. Ha! What a sight that would have been to see!"), 


  ("comment_you_defeated_my_friend_enemy_pragmatic",  "You may have bested {s54}, but you cannot defeat us all."), 
  ("comment_you_defeated_my_friend_enemy_chivalrous", "I have heard that you defeated {s54}, and ever since have been anxious to cross swords with you."), 
  ("comment_you_defeated_my_friend_enemy_spiteful",   "Your fame runs before you, {playername}. {s54} may have fallen for your tricks, but if you fight me, you'll find a me a much more slippery foe."), 
  ("comment_you_defeated_my_friend_enemy",            "They say that you have defeated {s54}. But I will be a truer test of your skill at arms."), 

  ("comment_you_captured_a_lord_allied_friendly_spiteful",   "I heard that you captured {s54}. I hope that you squeezed him for every denar."), 
  ("comment_you_captured_a_lord_allied_unfriendly_spiteful", "I heard that you captured {s54}. Your coffers must be well-bloated with ransom by now. Such a pity that money cannot transform a low-born cur into a gentleman!"), 
  ("comment_you_captured_a_lord_allied_chivalrous",          "I heard that you captured {s54}. Well done. I assume, of course, that he has been been treated with the honours due his rank."), 
  ("comment_you_captured_a_lord_allied",                     "I heard that you captured {s54}. Well done. His ransom must be worth quite something."), 

  ("comment_you_let_go_a_lord_allied_chivalrous",            "I heard that you captured {s54}, but then let him go. Such chivalry does a credit to our cause."),
  ("comment_you_let_go_a_lord_allied_upstanding",            "I heard that you captured {s54}, but then let him go. Well, that was an honourable course of action, if possibly also a dangerous one."),
  ("comment_you_let_go_a_lord_allied_coldblooded",           "I heard that you captured {s54}, but then let him go. That was most chivalrous of you, but chivalry does not win wars."),
  ("comment_you_let_go_a_lord_allied_unfriendly_spiteful",   "I heard that you captured {s54}, but then let him go. How very chivalrous of you! No doubt the widows and orphans he leaves in his wake will want to commend you in person."),
  ("comment_you_let_go_a_lord_allied",                       "I heard that you captured {s54}, but then let him go. Well, I will not tell you what to do with your own prisoners."),


  ("comment_you_let_me_go_spiteful",                    "When last we met, you had me at your mercy and allowed me to go free. I hope you enjoyed toying with me, like a cat with a mouse, because soon I will have you at my mercy, to slay or humiliate according to my fancy."),
  ("comment_you_let_me_go_enemy_chivalrous",            "When last we met, you had me at your mercy and allowed me to go free. That was most chivalrous of you, and I will not forget. But I also must remember my oath to my liege, and our kingdoms are still at war."),
  ("comment_you_let_me_go_enemy_coldblooded",           "When last we met, you had me at your mercy and allowed me to go free. But we are still enemies, and I cannot promise to repay your mercy in kind."),
  ("comment_you_let_me_go_enemy",                       "When last we met, you had me at your mercy and allowed me to go free. That was kind of you. But we are still at war."),
  ("comment_you_let_me_go_default",                     "When last we met, you had me at your mercy and allowed me to go free. That was kind of you, and I am glad that our kingdoms are no longer at war."),


#Internal faction events
  ("comment_pledged_allegiance_allied_martial_unfriendly",             "I heard that you have pledged allegiance to our lord, {s54}. Pray do not disgrace us by behaving in a cowardly fashion."),
  ("comment_pledged_allegiance_allied_martial",                        "I heard that you have pledged allegiance to our lord, {s54}. I look forward to fighting alongside you against our foes."),
  ("comment_pledged_allegiance_allied_quarrelsome_unfriendly",         "I heard that you have pledged allegiance to our lord, {s54}. Bah. Do yourself a favor, and stay out of my way."),
  ("comment_pledged_allegiance_allied_quarrelsome",                    "I heard that you have pledged allegiance to our lord, {s54}. Fight hard against our foes, respect your betters, and don't cross me, and we'll get along fine."),
  ("comment_pledged_allegiance_allied_selfrighteous_unfriendly",       "I heard that you have pledged allegiance to our lord, {s54}. If I were he, I would not trust you to clean the sculleries."),
  ("comment_pledged_allegiance_allied_selfrighteous",                  "I heard that you have pledged allegiance to our lord, {s54}. Fight bravely and you will be well-rewarded. Betray us, and we shall make of you the kind of example that will not soon be forgotten."),
  ("comment_pledged_allegiance_allied_cunning_unfriendly",             "I heard that you have pledged allegiance to our lord, {s54}. I do not pretend to be happy about his decision, but perhaps it is better to have you inside our tent pissing out, than the other way around."),
  ("comment_pledged_allegiance_allied_cunning",                        "I heard that you have pledged allegiance to our lord, {s54}. That is good. The more skilled fighters we have with us in these troubled times, the better. I shall be watching your progress."),
  ("comment_pledged_allegiance_allied_debauched_unfriendly",           "I heard that you have pledged allegiance to our lord, {s54}. No doubt you will soon betray him, and I will have the pleasure of watching you die a traitor's death."),
  ("comment_pledged_allegiance_allied_debauched",                      "I heard that you have pledged allegiance to our lord, {s54}. Excellent... I am sure that you and I will become very good friends. But remember -- if you betray us, it will be the biggest mistake you will ever make."),
  ("comment_pledged_allegiance_allied_goodnatured_unfriendly",         "I heard that you have pledged allegiance to our lord, {s54}. Well, I can't say that I would have trusted you, but perhaps you deserve the benefit of the doubt."),
  ("comment_pledged_allegiance_allied_goodnatured",                    "I heard that you have pledged allegiance to our lord, {s54}. Good {man/woman}! Our lord is a noble soul, and rewards loyalty and valor with kindness and generosity."),
  ("comment_pledged_allegiance_allied_upstanding_unfriendly",          "I heard that you have pledged allegiance to our lord, {s54}. Alas, from what I know of you I fear that you will disgrace us, but I will be happy if you prove me wrong."),
  ("comment_pledged_allegiance_allied_upstanding",                     "I heard that you have pledged allegiance to our lord, {s54}. Fight against our foes with valor, but also with honour and compassion. A good name is as valuable as a sharp sword or a swift horse in affairs of arms."),


  ("comment_our_king_granted_you_a_fief_allied_friendly_cruel",     "I heard that {s54} granted you {s51} as a fief. Don't forget -- spare the whip and spoil the peasant!"),
  ("comment_our_king_granted_you_a_fief_allied_friendly_cynical",   "I heard that {s54} granted you {s51} as a fief. I am glad to see you prosper -- but be careful. Men are vipers, envious and covetous of their neighbours' wealth. Stay close to me, and I'll watch your back."),

  ("comment_our_king_granted_you_a_fief_allied_friendly",              "I heard that {s54} granted you {s51} as a fief. May your new lands prosper."),
  ("comment_our_king_granted_you_a_fief_allied_unfriendly_upstanding", "I heard that {s54} granted you {s51} as a fief. But keep in mind that pride goes before a fall."),
  ("comment_our_king_granted_you_a_fief_allied_unfriendly_spiteful",   "I heard that {s54} granted you {s51} as a fief. I suspect, however, that fortune is only raising you up so as to humble you even more, when it casts you back into the dung from whence you came."),
  ("comment_our_king_granted_you_a_fief_allied_spiteful",              "I heard that {s54} granted you {s51} as a fief. Let's hope you are indeed deserving of our lord's favor."),

  ("comment_our_king_granted_you_a_fief_allied",                       "I heard that {s54} granted you {s51} as a fief. You seem to be doing very well for yourself."),

  ("comment_you_renounced_your_alliegance_enemy_friendly",             "I heard that you renounced your allegiance to our lord, {s54}. It grieves me that we must now meet on the field of battle."),
  ("comment_you_renounced_your_alliegance_friendly",                   "I heard that you renounced your allegiance to our lord, {s54}. Let us pray that we may not come to blows."),
  ("comment_you_renounced_your_alliegance_unfriendly_spiteful",        "I always had you figured for a traitor to {s54}, and now it seems I was proven right. I hope you are prepared to die a traitor's death!"),
  ("comment_you_renounced_your_alliegance_unfriendly_moralizing",      "I heard that you renounced your allegiance to our lord, {s54}. I am forced to consider you a traitor."),
  ("comment_you_renounced_your_alliegance_enemy",                      "I heard that you renounced your allegiance to our lord, {s54}. Well, it is the way of the world for old comrades to become enemies."),
  ("comment_you_renounced_your_alliegance_default",                    "I heard that you renounced your allegiance to our lord, {s54}. Well, that is your decision, but do not expect me to go easy on you when we meet on the battlefield."),


  ("personality_archetypes",   "liege"),
  ("martial",                  "martial"),
  ("quarrelsome",              "bad-tempered"),
  ("selfrighteous",            "pitiless"),
  ("cunning",                  "cunning"),
  ("debauched",                "sadistic"),
  ("goodnatured",              "good-natured"),
  ("upstanding",               "upstanding"),

  ("surrender_demand_default",        "Yield or die!"),
  ("surrender_demand_martial",        "The odds are not in your favor today. You may fight us, but there is also no shame if you yield now."),
  ("surrender_demand_quarrelsome",    "I've got you cornered. Give up, or I'll ride you down like a dog."),
  ("surrender_demand_pitiless",       "You cannot defeat me, and I'll teach you a painful lesson if you try. Yield!"),
  ("surrender_demand_cunning",        "You are outmatched today. Give up -- if not for your own sake, then think of your men!"),
  ("surrender_demand_sadistic",       "Surrender or I'll gut you like a fish!"),
  ("surrender_demand_goodnatured",    "We have the advantage of you. Yield, and you will be well-treated."),
  ("surrender_demand_upstanding",     "You may fight us, but many of your men will be killed, and you will probably lose. Yield, and spare us both the unnecessary bloodshed."),

  ("surrender_offer_default",        "Stop! I yield!"),
  ("surrender_offer_martial",        "Stop! I yield!"),
  ("surrender_offer_quarrelsome",    "Enough! You win today, you dog! Ach, the shame of it!"),
  ("surrender_offer_pitiless",       "I yield! You have won. Cursed be this day!"),
  ("surrender_offer_cunning",        "Stop! I yield to you!"),
  ("surrender_offer_sadistic",       "I give up! I give up! Call back your dogs!"),
  ("surrender_offer_goodnatured",    "I yield! Congratulations on your victory, {sir/madame}!"),
  ("surrender_offer_upstanding",     "I yield! Grant me the honours of war, and do yourself credit!"),

  ("prisoner_released_default",       "You have my gratitude, {sir/madame}. I shall not forget your kindness."),
  ("prisoner_released_martial",       "You are indeed a {man/woman} of honour, {sir/madame}. I shall not forget this!"),
  ("prisoner_released_quarrelsome",   "I'm free? Well... Good bye, then."),
  ("prisoner_released_pitiless",      "Thank you. When you are finally defeated, I will request for your death to be swift and merciful. Unless, that is, you care to join us... Good bye, for now."),
  ("prisoner_released_cunning",       "Am I? You are a good {man/woman}. I will try to find a way to repay you."),
  ("prisoner_released_sadistic",      "Am I? So refined is your cruelty, that you would rather see me free and humiliated, than in chains. Enjoy your triumph!"),
  ("prisoner_released_goodnatured",   "You are indeed a {man/woman} of honour, {sir/madame}. I shall not forget this!"),
  ("prisoner_released_upstanding",    "You are indeed a {man/woman} of honour, {sir/madame}. I shall not forget this!"),

#Post 0907 changes begin
  ("enemy_meet_default",              "Who are you, that comes in arms against me?"),
  ("enemy_meet_martial",              "What is your name, {sir/madame}? If we come to blows, I would know whom I fight."),
  ("enemy_meet_quarrelsome",          "Who the hell are you?"),
  ("enemy_meet_pitiless",             "Who are you? Speak, so that I may know whom I slay."),
  ("enemy_meet_cunning",              "Tell me your name. It is always good to know your enemy."),
  ("enemy_meet_sadistic",             "Who are you? Speak quick, before I cut your tongue out."),
  ("enemy_meet_goodnatured",          "What is your name, {sir/madame}? If we come to blows, I would know whom I fight."),
  ("enemy_meet_upstanding",           "Who are you, who would come in arms to dispute our righteous cause?"),

  ("battle_won_default",              "You have proven yourself a most valued ally, today."),
  ("battle_won_martial",              "There is no greater fortune than the chance to show one's valor on the field of arms!"),
  ("battle_won_quarrelsome",          "Hah! We showed those bastards a thing or two, there, didn't we?"),
  ("battle_won_pitiless",             "Together, we will make the foe learn to fear our names, and to quail at our coming!"),
  ("battle_won_cunning",              "Now, we must be sure to press our advantage, so that the blood shed today is not wasted."),
  ("battle_won_sadistic",             "Now let us strip their dead and leave them for the crows, so that all will know the fate of those who come against us."),
  ("battle_won_goodnatured",          "That was a good scrap! No joy like the joy of victory, eh?"),
  ("battle_won_upstanding",           "Now, let us give thanks to the heavens for our victory, and mourn the many fine men who have fallen today."),

  ("battle_won_grudging_default",     "You helped turn the tide on the field, today. Whatever I may think of you, I cannot fault you for your valor."),
  ("battle_won_grudging_martial",     "{playername} -- you have shown yourself a worthy {man/woman} today, whatever your misdeeds in the past."),
  ("battle_won_grudging_quarrelsome", "Hmf. Yours is not a face which I normally like to see, but I suppose today I should thank you for your help."),
  ("battle_won_grudging_pitiless",    "Your help was most valuable today. I would not imagine that you came to help me out of kindness, but I nonetheless thank you."),
  ("battle_won_grudging_cunning",     "It would be unwise of me not to thank you for coming to help me in my hour of need. So... You have my gratitude."),
  ("battle_won_grudging_sadistic",    "Well! How touching! {playername} has come to rescue me."),
  ("battle_won_grudging_goodnatured", "{playername}! I can't say that we've always gotten along in the past, but you fought well today. My thanks to you!"),
  ("battle_won_grudging_upstanding",  "Perhaps I was wrong about you. Your arrival was most timely. You have my gratitude."),

  ("battle_won_unfriendly_default",         "So you're here. Well, better late than never, I suppose."),
  ("battle_won_unfriendly_martial",         "We have hard harsh words in the past, but for now let us simply enjoy our victory."),
  ("battle_won_unfriendly_quarrelsome",     "If you're standing there waiting for thanks, you can keep waiting. Your help wasn't really needed, but I guess you had nothing better to do, right?"),
  ("battle_won_unfriendly_pitiless",        "You have come here, like a jackal to a lion's kill. Very well then, help yourself to the spoils. I shall not stop you."),
  ("battle_won_unfriendly_cunning",         "{playername}... Well, I suppose your arrival didn't hurt, although I won't pretend that I'm happy to see you."),
  ("battle_won_unfriendly_sadistic",        "Back off, carrion fowl! This was my victory, however hard you try to steal the glory for yourself."),
  ("battle_won_unfriendly_goodnatured",     "Oh, it's you. Well, I suppose I should thank you for your help."),
  ("battle_won_unfriendly_upstanding",      "Thank you for coming to my support. Now I will be off, before I say something that I regret."),

  ("troop_train_request_default",               "I need someone like you to knock them into shape."),
  ("troop_train_request_martial",               "They need someone to show them the meaning of valor."),
  ("troop_train_request_quarrelsome",           "Fat lazy bastards. They make me puke."),
  ("troop_train_request_pitiless",              "They are more afraid of the enemy than they are of me, and this will not do."),
  ("troop_train_request_cunning",               "But men, like swords, are tempered and hardened by fire."),
  ("troop_train_request_sadistic",              "They need someone with steel in his back to flog some courage into them, or kill them trying."),
  ("troop_train_request_goodnatured",           "They're good enough lads, but I am afraid that they are not quite ready for a battle just yet."),
  ("troop_train_request_upstanding",            "It would be tantamount to murder for me to lead them into combat in their current state."),

  ("unprovoked_attack_default",               "What? Why do you attack us? Speak, you rascal!"),
  ("unprovoked_attack_martial",               "I have no objection to a trial of arms, but I would ask you for what reason you attack us?"),
  ("unprovoked_attack_quarrelsome",           "You're making a big mistake, {boy/girl}. What do you think you're doing?"),
  ("unprovoked_attack_pitiless",              "Indeed? If you really want to die today, I'd be more than happy to oblige you, but I am curious as to what you hope to accomplish."),
  ("unprovoked_attack_cunning",               "Really? I think that you are acting most unwisely. What do you hope to gain by this?"),
  ("unprovoked_attack_sadistic",              "What's this? Do you enjoy having your eyes put out?"),
  ("unprovoked_attack_goodnatured",           "Why do you do this? We've got no quarrel, {sir/madame}."),
  ("unprovoked_attack_upstanding",            "I consider this an unprovoked assault, and will protest to your king. Why do you do this?"),

  ("unnecessary_attack_default",               "I will not hesitate to cut you down if pressed, but I will offer you the chance to ride away from this."),
  ("unnecessary_attack_martial",               "I am eager to take you up on your challenge, {sir/madame}, although I will give you a minute to reconsider."),
  ("unnecessary_attack_quarrelsome",           "Bah! I'm in no mood for this nonsense today. Get out of my way."),
  ("unnecessary_attack_pitiless",              "I am in a merciful mood today. I will pretend that I did not hear you."),
  ("unnecessary_attack_cunning",               "I don't see what you have to gain by making an enemy of me. Maybe you should just ride away."),
  ("unnecessary_attack_sadistic",              "I have no time to waste on a worm like you. Get out of my way."),
  ("unnecessary_attack_goodnatured",           "I don't see what you have to gain by picking a fight, {sir/madame}. You can still ride away."),
  ("unnecessary_attack_upstanding",            "If a fight is what you wish, {sir/madame}, then you will have one, but I will yet offer you the chance to back down."),

  ("lord_challenged_default",                   "As you wish. Prepare to die!"),
  ("lord_challenged_martial",                   "So be it. Defend yourself!"),
  ("lord_challenged_quarrelsome",               "You impudent whelp! I'll crush you!"),
  ("lord_challenged_pitiless",                  "If you so badly wish to die, then I have no choice but to oblige you."),
  ("lord_challenged_cunning",                   "Well, if you leave me no choice..."),
  ("lord_challenged_sadistic",                  "You heap of filth! I'll make you wish you'd never been born."),
  ("lord_challenged_goodnatured",               "Very well. I had hoped that we might avoid coming to blows, but I see that have no choice."),
  ("lord_challenged_upstanding",                "So be it. It saddens me that you cannot be made to see reason."),

  ("lord_mission_failed_default",               "Well, I am disappointed, but I am sure that you will have many chances to redeem yourself."),
  ("lord_mission_failed_martial",               "There is no honour in failing a quest which you endeavoured to take, but I will accept your word on it."),
  ("lord_mission_failed_quarrelsome",           "You failed? Bah. I should have expected as much from the likes of you."),
  ("lord_mission_failed_pitiless",              "You failed? Well. You disappoint me. That is a most unwise thing to do."),
  ("lord_mission_failed_cunning",               "Well, I am disappointed, but no one can guarantee that the winds of fortune will always blow their way."),
  ("lord_mission_failed_sadistic",              "Indeed? Those who fail me do not always live to regret it."),
  ("lord_mission_failed_goodnatured",           "Oh well. It was a long shot, anyway. Thank you for making an effort."),
  ("lord_mission_failed_upstanding",            "Very well. I am sure that you gave it your best effort."),

  ("lord_follow_refusal_default",       "Follow you? You forget your station, {sir/madame}."),
  ("lord_follow_refusal_martial",       "Perhaps if you one day prove yourself a valorous and honourable warrior, then I would follow you. But not today."),
  ("lord_follow_refusal_quarrelsome",   "Follow someone like you? I don't think so."),
  ("lord_follow_refusal_pitiless",      "Lords like me do not follow people like you, {sir/madame}."),
  ("lord_follow_refusal_cunning",       "First show me that you are the type of {man/woman} who will not lead me into disaster, and then perhaps I will follow you."),
  ("lord_follow_refusal_sadistic",      "I think not! Rather, you should follow me, as a whipped cur follows {his/her} master."),
  ("lord_follow_refusal_goodnatured",   "Um, I am a bit pressed with errands right now. Perhaps at a later date."),
  ("lord_follow_refusal_upstanding",    "First show me that you are worthy to lead, and then perhaps I will follow."),



  ("lord_insult_default",               "base varlot"),
  ("lord_insult_martial",               "dishonourable knave"),
  ("lord_insult_quarrelsome",           "filth-swilling bastard"),
  ("lord_insult_pitiless",              "low-born worm"),
  ("lord_insult_cunning",               "careless oaf"),
  ("lord_insult_sadistic",              "sniveling cur"),
  ("lord_insult_goodnatured",           "unpleasant fellow"),
  ("lord_insult_upstanding",            "disgraceful scoundrel"),


  ("rebellion_dilemma_default",                 "[liege]"),
  ("rebellion_dilemma_martial",                 "{s45} was clearly wronged. Although I gave an oath to {s46}, it does not bind me to support him if he usurped his throne illegally."),
  ("rebellion_dilemma_quarrelsome",             "Hmm. {s46} has never given me my due, so I don't figure I owe him much. However, maybe {s45} will be no better, and {s46} has at least shown himself ."),
  ("rebellion_dilemma_pitiless",                "Hmm. {s45} says {reg3?she:he} is the rightful heir to the throne. That is good -- it absolves me of my oath to {s46}. But still I must weight my decision carefully."),
  ("rebellion_dilemma_cunning",                 "Hmm. I gave an oath of homage to {s46}, yet the powerful are not bound by their oaths as our ordinary people. Our duty is to our own ability to rule, to impose order and prevent the war of all against all."),
  ("rebellion_dilemma_sadistic",                "Hmm. In this vile world, a wise man must think of himself, for no one else will. So -- what's in it for me?"),
  ("rebellion_dilemma_goodnatured",             "I do not know what to say. I gave an oath to {s46} as the lawful ruler, but if he is not the lawful ruler, I don't know if I am still bound."),
  ("rebellion_dilemma_upstanding",              "This is troublesome. It is a grave thing to declare my homage to {s46} to be null and void, and dissolve the bonds which keep our land from sinking into anarchy. Yet I am also pledged to support the legitimacy of the succession, and {s45} also has a valid claim to the throne."),

  ("rebellion_dilemma_2_default",               "[liege]"),
  ("rebellion_dilemma_2_martial",               "On the other hand, {s46} has led us in war and peace, and I am loathe to renounce my allegiance."),
  ("rebellion_dilemma_2_quarrelsome",           "So tell me, why should I turn my back on the bastard I know, in favor of {reg3?a woman:the bastard} I don't know?"),
  ("rebellion_dilemma_2_pitiless",              "It is a most perilous position to be in, to be asked whom I would make {reg3?ruler:king} of this land. Yet it is also a time of opportunity, for me to reap the rewards that have always been my due!"),
  ("rebellion_dilemma_2_cunning",               "{s46} has been challenged, and thus he will never be able to rule as strongly as one whose claim has never been questioned. Yet if {s45} takes the throne by force, {reg3?she:he} will not be as strong as one who succeeded peacefully."),
  ("rebellion_dilemma_2_sadistic",              "Perhaps if I join {s45} while {reg3?she:he} is still weak {reg3?she:he} will enrich me, but perhaps if I bring {s46} your head he will give me an even greater reward."),
  ("rebellion_dilemma_2_goodnatured",           "{s46} has always treated me decently, yet it's true that he did wrong to {s45}. I hesitate to renounce my homage to {s46}, yet I also don't think it's right to support injustice."),
  ("rebellion_dilemma_2_upstanding",            "I feel that I must do whatever is best for the realm, to avoid it being laid waste by civil war and ravaged by its enemies."),


  ("rebellion_prior_argument_very_favorable",   "I have already heard some arguments for supporting your candidate for the throne, and I tend to agree with them."),
  ("rebellion_prior_argument_favorable",        "I have already heard some arguments for supporting your candidate for the throne, and I tend to agree with them."),
  ("rebellion_prior_argument_unfavorable",      "I have already heard some arguments for supporting your candidate for the throne, but I do not find them convincing."),
  ("rebellion_prior_argument_very_unfavorable", "I have already heard some arguments for supporting your candidate for the throne, but I disagree with most of them."),

  ("rebellion_rival_default",                   "[liege]"),
  ("rebellion_rival_martial",                   "{s49} your ally {s44} once questioned my honour and my bravery. It's not often I get the chance to face him in battle, and make him retract his statement."),
  ("rebellion_rival_quarrelsome",               "{s49} you're working with {s44}. He's a crafty weasel, and I don't trust him one bit."),
  ("rebellion_rival_pitiless",                  "{s49} you seem to have enlisted the support of {s44} -- who is soft, and weak, and not fit to govern a fief, and whom I have always detested."),
  ("rebellion_rival_cunning",                   "{s49} {s44}, who has already joined you, is headstrong and quarrelsome, and a bit of liability."),
  ("rebellion_rival_sadistic",                  "{s49} I have no desire to fight alongside your ally {s44}, who puts on such a nauseating display of virtue."),
  ("rebellion_rival_goodnatured",               "{s49} I'd be reluctant to be on the same side as {s44}, who has quite a reputation for cruelty."),
  ("rebellion_rival_upstanding",                "{s49} your ally {s44} is in my opinion a dangerous, unreliable, and highly unprincipled man."),

  ("rebellion_argument_favorable",              "I respect your line of argument"),
  ("rebellion_argument_neutral",                "I find your line of argument only moderately compelling"),
  ("rebellion_argument_unfavorable",            "I do not find your line of argument compelling"),

  ("rebellion_persuasion_favorable",            "you state your case eloquently"),
  ("rebellion_persuasion_neutral",              "you make a reasonable case"),
  ("rebellion_persuasion_unfavorable",          "you make an unconvincing case"),

  ("rebellion_relation_very_favorable",         "I have the greatest respect for you personally."),
  ("rebellion_relation_favorable",              "I know and respect you personally."),
  ("rebellion_relation_neutral",                "I do not know you as well as I might like."),
  ("rebellion_relation_unfavorable",            "I do not trust you."),

  ("and_comma_3", "Furthermore, "),
  ("but_comma_3", "However,"),

  ("and_comma_1", ", and "),
  ("but_comma_1", ", but "),

  ("and_comma_2", ". Moreover, "),
  ("but_comma_2", ". Nonetheless, "),


  ("rebellion_agree_default",               "[liege]"),
  ("rebellion_agree_martial",               "I have decided. I will back {s45} as the rightful heir."),
  ("rebellion_agree_quarrelsome",           "Ahh, I've thought long enough. I never did like {s46} much anyway. Let's go take his throne away from him."),
  ("rebellion_agree_pitiless",              "You are fortunate. I have decided to join you. Pray do not give me cause to regret this decision."),
  ("rebellion_agree_cunning",               "This is a most dangerous decision, but after careful consideration, I have decided that I will join you. Let's hope it is for the best."),
  ("rebellion_agree_sadistic",              "I have decided. I will back your {reg3?woman:man} {s45}. But you'd best make sure that {reg3?she:he} rewards me well!"),
  ("rebellion_agree_goodnatured",           "All right. I think your {reg3?woman:man} will be a good ruler. I'll join you."),
  ("rebellion_agree_upstanding",            "So be it. My first duty is to this realm, and to save it from lawlessness I will back {s45} and renounce my homage to {s46}. May the Heavens forgive me if I do wrong."),


  ("rebellion_refuse_default",              "[liege]"),
  ("rebellion_refuse_martial",              "I am sorry. {s45} has a good claim, but it's not enough for me to turn my back on {s46}. I will remain loyal to my liege."),
  ("rebellion_refuse_quarrelsome",          "Nah. Your whelp {s45} doesn't have what it takes to rule this realm. I'm sticking with {s46}."),
  ("rebellion_agree_pitiless",              "No. I will not join your rebellion. I count it little more than the tantrum of a child, denied a bauble which {reg3?she:he} thinks should be {reg3?hers:his}. I will stick with {s46}, whose ability to rule is well-tested."),
  ("rebellion_agree_cunning",               "I am sorry. You do not give me reason for confidence that you will win. Many will die, but I do not wish to be among them. I will continue to back {s46}."),
  ("rebellion_agree_sadistic",              "No. I won't play your little game. You grasp at a crown, but I think instead you'll get a quick trip to the scaffold, and I'll be there by {s46}'s side to watch the headsman's axe drop."),
  ("rebellion_agree_goodnatured",           "I am sorry. I don't feel right turning my back on {s46}. No hard feelings when me meet on the battlefield."),
  ("rebellion_agree_upstanding",            "I am sorry. {s45}'s claim is not strong enough for me to inflict the curse of civil disorder on the poor wretches of this land. I will continue to back {s46}. May the Heavens forgive me if I do wrong."),

  ("talk_later_default",                    "[liege]"),
  ("talk_later_martial",                    "Now is not the time to talk politics! I am here today with my fellow lords, armed for battle. You'd better prepare to fight."),
  ("talk_later_quarrelsome",                "Do you expect me to discuss betraying my liege with you, while we are surrounded by his army? What do you take me for, a bloody idiot?"),
  ("talk_later_pitiless",                   "Still your tongue! Whatever I have to say on this matter, I will not say it here and now, while we are in the midst of our army."),
  ("talk_later_cunning",                    "This is hardly the time or the place for such a discussion. Perhaps we can discuss it at a later time and a different place, but for now we're still foes."),
  ("talk_later_sadistic",                   "You should have your mouth sewn shut! Can you imagine what would happen if the other vassals see me talking to you of treason?"),
  ("talk_later_goodnatured",                "So you wish to discuss your rebellion with me? Try that again when we aren't surrounded by my liege's army, and I will hear what you have to say."),
  ("talk_later_upstanding",                 "Whatever my thoughts on the legitimacy of the succession, I am not about to discuss them here and now. If we meet again when we can talk in privacy, I will hear what you have to say on the matter. But for now, consider me your enemy."),


  ("gossip_about_character_default",        "They say that {s6} doesn't possess any interesting character traits."),
  ("gossip_about_character_martial",        "They say that {s6} loves nothing more than war."),
  ("gossip_about_character_quarrelsome",    "They say that {s6} almost came to blows with another lord lately, because the man made a joke about his nose."),
  ("gossip_about_character_selfrighteous",  "I heard that {s6} had a squire executed because the unfortunate man killed a deer in his forest."),
  ("gossip_about_character_cunning",        "They say that {s6} is a cunning opponent."),
  ("gossip_about_character_sadistic",       "They say that {s6} likes to torture his enemies. I wouldn't want to get on the bad side of that man."),
  ("gossip_about_character_goodnatured",    "They say that {s6} is a good man and treats people living in his lands decently. That is more than what can be said for most of the nobles."),
  ("gossip_about_character_upstanding",     "People say that it is good to be in the service of {s6}. He is good to his followers, and rewards them if they work well."),

  ("latest_rumor",        "The latest rumor you heard about {s6} was:"),


#steve post 0912 changes begin

  ("swadian_rebellion_pretender_intro",    "I am Isolla, rightful Queen of the Swadians."),
  ("vaegir_rebellion_pretender_intro",     "My name is Valdym. Some men call me 'the Bastard.' I am a prince of the Vaegirs, but by all rights I should be their king, instead of my cousin Yaroglek."),
  ("khergit_rebellion_pretender_intro",    "I am Dustum Khan, son of Janakir Khan, and rightful Khan of the Khergits."),
  ("nord_rebellion_pretender_intro",       "I am Lethwin Far-Seeker, son of Hakrim the Old, who should be king of the Nords of Calradia."),
  ("rhodok_rebellion_pretender_intro",     "I am Lord Kastor, the rightful King of the Rhodoks, who will free them from tyranny."),

  ("swadian_rebellion_pretender_story_1",  "I was the only child of my father, King Esterich. Although I am a woman, he loved me like a son and named me his heir -- not once, but several times, before the grandest nobles of the land so that none could doubt his intention. There is no law that bars a woman from ruling -- indeed, we Swadians tell tales of warrior queens who ruled us in our distant past."),
  ("vaegir_rebellion_pretender_story_1",   "My father died when I was young, leaving me in the care of his brother, the regent Burelek. But rather than hold the throne until I came of age, this usurper used his newfound power to accuse my mother of adultery, and to claim that I was not my father's son. She was executed for treason, and I was declared a bastard."),
  ("khergit_rebellion_pretender_story_1",  "Sanjar Khan and I are brothers, sons of the old Janakir Khan, although of different mothers. Although I was the younger brother, all those who knew the old Khan will testify that throughout my father's life, I was his favorite, entrusted with the responsibilities of government. Sanjar busied himself with hunts and feasts to win the affection of the more dissolate of my father's commanders."),
  ("nord_rebellion_pretender_story_1",     "I am called the Far-Seeker because I have travelled great distances, even by the standards of the Nords, in search of knowledge. Before I came of age, my father sent me abroad on a tour of study at the courts and universities in the lands overseas. If the Nords are to call themselves the heirs of the Calradian empire, then they must act the part, and know something of law and letters, and not call themselves content merely to fight, plunder, and drink."),
  ("rhodok_rebellion_pretender_story_1",   "The Rhodoks are a free people, and not slaves to any hereditary monarch. The king must be chosen from one of the leading noble families of the land, by a council drawn by lot from the patricians of the cities of Jelkala, Veluca, and Yalen. The council meets on a field before Jelkala, and no man is allowed to appear in arms during their deliberations, on pain of death."),

  ("swadian_rebellion_pretender_story_2",  "Yet when my father died, his cousin Harlaus convinced the nobles that no Swadian king of sound mind could name a woman as his heir. Harlaus said that his designation of me was the act of a madman, and thus had no legal standing, and that he, as my father's closest male relative, should of take the throne."),
  ("vaegir_rebellion_pretender_story_2",   "I was smuggled abroad by a faithful servant, but now I am of age and have returned to reclaim what is rightfully mine. Burelek died soon after his act of perfidy -- the judgment of heaven, no doubt. His son Yaroglek now calls himself king, but as his claim is tainted, he is no less a usurper than his father, and I will topple him from his throne."),
  ("khergit_rebellion_pretender_story_2",  "According to Khergit custom, when a man dies his herds are split between all his sons, equally. So too it is with the khanate. When I heard of my father's death, I was away inspecting our borders, but I hurried home to Tulga, ready to give Sanjar his due and share the khanate with him. But when I arrived, I found that he rushed his supporters to the court, to have himself proclaimed as the sole khan."),
  ("nord_rebellion_pretender_story_2",     "My father died however before I completed my course of study, and as I hurried home to claim his throne my ship was wrecked by a storm. One of my father's thanes, Ragnar, seized this opportunity and spread rumors that I had died abroad. He summoned a gathering of his supporters to have himself proclaimed king, and has taken the past few years to consolidate his power."),
  ("rhodok_rebellion_pretender_story_2",   "During the last selection, there were but two candidates, myself, and Lord Graveth. While the council was deliberating, Graveth appeared, sword in hand, telling them that a Swadian raiding party was about to descend on the field of deliberation -- which was true, by the way -- and if he were not elected king, then he would leave them to their fate."),

  ("swadian_rebellion_pretender_story_3",  "I will admit that I did my cause no good by cursing Harlaus and all who listened to him as traitors, but I also believe that the magistrates who ruled in his favor were bought. No matter -- I will raise an army of loyal subjects, who would honour their old king's memory and will. And if anyone doubts that a woman can wield power, then I will prove them wrong by taking Harlaus' ill-gotten crown away from him."),
  ("vaegir_rebellion_pretender_story_3",   "Until I have my rights restored in the sight of all the Vaegirs, I will bear the sobriquet, 'the Bastard', to remind me of what I must do."),
  ("khergit_rebellion_pretender_story_3",  "My brother thinks that Khergits will only respect strength: a leader who takes what he wants, when he wants it. But I think that he misreads the spirit of our people.--we admire a resolute leader, but even more we a just one, and we know that a man who does not respect his own brother's rights will not respect the rights of his followers."),
  ("nord_rebellion_pretender_story_3",     "So I remain in exile -- except now I am not looking for sages to tutor me in the wisdom of faraway lands, but warriors, to come with me back to the land of the Nords and regain my throne. If Ragnar doubts my ability to rule, then let him say so face to face, as we stare at each other over the rims of our shields. For a warrior can be a scholar, and a scholar a warrior, and to my mind, only one who combines the two is fit to be king!"),
  ("rhodok_rebellion_pretender_story_3",   "Well, Graveth defeated the Swadians, and for that, as a Rhodok, I am grateful. When I am king, I will myself place the wreath of victory on his head. But after that I will have it separated from his shoulders, for by his actions he has shown himself a traitor to the Rhodok confederacy and its sacred custom."),

  ("swadian_rebellion_monarch_response_1", "Isolla thinks she should be Queen of the Swadians? Well, King Esterich had a kind heart, and doted on his daughter, but a good-hearted king who doesn't use his head can be a curse to his people. Isolla may tell you stories of warrior queens of old, but you might also recall that all the old legends end in the same way -- with the Swadians crushed underfoot by the armies of the Calradic Emperor."),
  ("vaegir_rebellion_monarch_response_1",  "Were Valdym to come to me in peace, I would laden him with titles and honours, and he would become the greatest of my vassals. But as he comes in war, I will drag him before me in chains and make him acknowledge me as rightful sovereign, then cut his tongue from his mouth so that he cannot recant."),
  ("khergit_rebellion_monarch_response_1", "My brother Dustum has perhaps told you of his insistence upon splitting the khanate, as though it were a herd of sheep. Let me tell you something. Ever since the Khergits established themselves on this land, the death of every khan has had the same result -- the land was divided, the khan's sons went to war, and the strongest took it all anyway. I simply had the foresight to stave off the civil war in advance."),
  ("nord_rebellion_monarch_response_1",    "Lethwin 'Far-Seeker'? Lethwin Inkfingers, is more like it. Perhaps you have heard the expression, 'Unhappy is the land whose king is a child.' Unhappy too is the land whose king is a student. You want the Nords to be ruled by a beardless youth, whose hand bears no callouses left by a sword's grip, who has never stood in a shield wall? If Lethwin were king, his thanes would laugh at him to his face!"),
  ("rhodok_rebellion_monarch_response_1",  "No doubt Lord Kastor told you that I defiled the hallowed Rhodok custom by interfering with the patricians' election of a king. Well, let me tell you something. The patricians of the towns make longwinded speeches about our ancient liberties, but then choose as their king whichever noble last sat in their villa and sipped a fine wine and promised to overlook their unpaid taxes."),

  ("swadian_rebellion_monarch_response_2", "Those who weep for the plight of a Swadian princess denied her father's throne should reflect instead on the fate of a Swadian herdswoman seized by a Vaegir raider and taken as chattel to the slave markets. Talk to me of queens and old stories when our warlike neighbors are vanquished, and our land is at peace."),
  ("vaegir_rebellion_monarch_response_2",  "Whatever my father may or may not have done to secure the throne does not matter. I have inherited it, and that is final. If every old claim were to be brought up anew, if every man's inheritance could be called into question at any time, then it would be the end of the institution of kingship, and we would live in a state of constant civil war."),
  ("khergit_rebellion_monarch_response_2", "Dustum would make a fine assessor of flocks, or adjudicator of land disputes. But can you imagine such a man as khan? We would be run off of our land in no time by our neighbors, and return to our old days of starving and freezing on the steppe."),
  ("nord_rebellion_monarch_response_2",    "Old Hakrim may have had fancy ideas about how to dispose of his kingdom, but it is not just royal blood that makes a King of the Nords. I am king by acclamation of the thanes, and by right of being the strongest. That counts for more than blood, and woe to any man in this land who says otherwise."),
  ("rhodok_rebellion_monarch_response_2",  "The only liberty that concerns them is their liberty to grow fat. Meanwhile, my men sleep out on the steppe, and eat dry bread and salt fish, and scan the horizon for burning villages, and shed our blood to keep the caravan routes open. Here's an idea -- if I ever meet a merchant who limps from a Khergit arrow-wound or a Swadian sword-stroke, then I'll say, 'Here's a man whose counsel is worth taking.'"),


#steve post 0912 changes end




  ("credits_1", "Mount&Blade Copyright 2001-2008 Taleworlds Entertainment"),
  ("credits_2", "Game design:^Armagan Yavuz^Steve Negus^Cem Cimenbicer"),
  ("credits_3", "Programming:^Armagan Yavuz^Cem Cimenbicer"),
  ("credits_4", "CG Artists:^Ipek Yavuz^Ozgur Saral^Mustafa Ozturk"),
  ("credits_8", "Animation:^Pinar Cekic^Umit Singil"),
  ("credits_5", "Concept Artist:^Ganbat Badamkhand"),
  ("credits_6", "Writing:^Steve Negus^Ryan A. Span^Armagan Yavuz"),
  ("credits_9", "Original Music:^Jesse Hopkins"),
  ("credits_7", "Additional Modeling:^Hilmi Aric^Ahmet Sarisakal^Katie Beedham^^^Additional Writing:^Michael Buhler^Patrick Desjardins^^^Voice Talents:^Tassilo Egloffstein^Jade E Henderson^^^\
Original Music Composed by:^Jesse Hopkins^\
Violin Solos Performed by:^Zoriy Zinger^\
Main Theme and Scherzo Performed by:^The Russian State Symphony Cinema Orchestra, Conducted by Sergei Skripka^^^\
Sound Samples:^Audiosparx.com^^^\
Mount&Blade Map Editor:^Matt Stentiford^^^\
Taleworlds Forum Programming:^Brett Flannigan www.fenrisoft.com^^^\
Mount&Blade Tutorial written by:^Edward Spoerl^^^\
Gameplay Videos:^Jemes Muia^^^\
Motion Capture System:^NaturalPoint-Optitrack Arena^^^\
Horse Motion Capture Animation Supplied by:^Richard Widgery & Kinetic Impulse^^^\
Ragdoll Physics:^Newton Game Dynamics^^^\
Sound and Music Program Library:^FMOD Sound System by Firelight Technologies^^^\
Copy Protection:^Themida by Oreans Technologies^^^\
Skybox Textures:^Jay Weston www.hyperfocaldesign.com^^^\
Third Party Art Libraries Used:^Texturemonk^Mayang Textures^cgtextures.com^3d.sk^^\
Unofficial Mount&Blade Editor:^Josh Dahlby^^^\
Many thanks to Marco Tarini for the Mountain shader idea!^^^\
Special Thanks to:^Ibrahim Dogan^Nova Language Works^Selim Kurtulus and UPS Turkey^^^\
Taleworlds.com Forum Administrators and Moderators:^Janus^Archonsod^Narcissus^Nairagorn^Lost Lamb^Deus Ex^Merentha^Volkier^Okin^Instag0\
^Deniz^ego^Guspav^Hallequin^Invictus^okiN^Raz^rejenorst^Skyrage^ThVaz^^^\
Spanish Translation^^Translators:^Anabel 'Rhaenys' Diaz^Analia 'Immortality' Dobarro^Anoik^^Medieval Consultant:^Enric 'Palafoxx' Clave^^Language Tester:^Theo de Moree^^^\
Mount&Blade Community Suggestions and Feedback:^\
13 Chain Bloody Spider^\
Aenarion^\
AgentSword^\
Ahadhran^\
Albino^\
Allegro^\
allthesedamnnamesare^\
Amman de Stazia^\
Ancientwanker^\
Anrea 'Skree' Giongiani^\
Aqtai^\
Art Falmingaid^\
bryce777^\
Bugman^\
Buxton^\
Calandale^\
Cartread^\
Chel^\
Chilly5^\
Cirdan^\
Cleaning agent^\
Cymro^\
DaBlade^\
DaLagga^\
Damien^\
danover^\
Dearahn^\
Deathblow^\
Destichado^\
Dryvus^\
dunnno^\
D'Sparil^\
ealabor^\
Ealdormann Hussey^\
EasyCo506^\
El Duke^\
Elias Maluco^\
Eogan^\
ex_ottoyuhr^\
Fisheye^\
Fossi^\
fujiwara^\
Fuzzpilz^\
GandalfTheGrey^\
Gerif^\
Grocat^\
Guspav^\
Halden The Borch shooter^\
Hallequin^\
Handel^\
Hardcode^\
Haupper^\
Hellequin^\
Highelf^\
Highlander^\
Ibrahim Turgut^\
Iesu^\
Ilex^\
Ingolifs^\
Invictus^\
Itchrelief^\
Jlgx50^\
JHermes^\
Jik^\
john259^\
JonathanStrange^\
jpgray^\
kamov23^\
Kayback^\
Khalid Ibn Walid^\
KON_Air^\
Lady Tanith^\
Larry Knight^\
LavaLampMaster^\
Leprechaun^\
Lhorkan^\
Llew2^\
Maelstorm^\
Manitas^\
Maw^\
MAXHARDMAN^\
Merentha^\
Merlkir^\
Michael Elijah 'ironpants' Bell-Rao^\
mihoshi^\
Mirathei^\
mkeller^\
Momaw^\
Morgoth2005^\
MrCrotch^\
mtarini^\
n00854180t^\
Naridill^\
Nicholas Altaman\
okiN^\
oksir^\
Oldtimer^\
Ollieh^\
oRGy^\
Oubliette^\
Patrick 'nox' Gallaty^\
Pavlov^\
Rando^\
Raz^\
rejenorst^\
Rjii^\
Ron Losey^\
Rorthic^\
RR_raptor^\
Scion^\
Seff^\
shenzay^\
Shadowmoses^\
shikamaru 1993^\
Silver^\
silverkatana^\
Sir Prince^\
Sirgigor^\
Skyrage^\
Smoson^\
sneakey pete^\
Stefano^\
Stella^\
Stonewall382^\
Talak^\
Tankai^\
TG^\
thelast^\
The Phoenix^\
The Pope^\
The Yogi^\
Thingy Master^\
Thormac^\
Thus_Spake_Nosferatu^\
ThVaz^\
Toygar Birinci^\
Tuckles^\
Tul^\
Ursca^\
Vaerraent^\
Vilhjalmr^\
Volkier^\
vuk^\
Wanderer^\
WhoCares^\
Winter^\
Worbah^\
Yoshiboy^\
...and many many other wonderful Mount&Blade players!^^\
(This is only a small sample of all the players who have contributed to the game by providing suggestions and feedback.^\
This list has been compiled by sampling only a few threads in the Taleworlds Forums.^\
Unfortunately compiling an exhaustive list is almost impossible.^\
We apologize sincerely if you contributed your suggestions and feedback but were not listed here, and please know that we are grateful to you all the same...)\
"),
  ("credits_10", "Paradox Interactive^^President and CEO:^Theodore Bergqvist^^Executive Vice President:^Fredrik Wester\
^^Chief Financial Officer:^Lena Eriksson^^Finance & Accounting:^Annlouise Larsson^^VP Sales & Marketing US:^Reena M. Miranda\
^^VP Sales & Marketing EU:^Martin Sirc^^Distribution Manager Nordic:^Erik Helmfridsson^^Director of PR & Marketing:^Susana Meza\
^^PR & Marketing:^Sofia Forsgren^^Product Manager:^Boel Bermann\
"),
  ("credits_11", "Logotype:^Jason Brown^^Cover Art:^Piotr Fox Wysocki\
^^Layout:^Christian Sabe^Melina Grundel^^Poster:^Piotr Fox Wysocki^^Map & Concept Art:^Ganbat Badamkhand\
^^Manual Editing:^Digital Wordsmithing: Ryan Newman, Nick Stewart^^Web:^Martin Ericsson^^Marketing Assets:^2Coats\
^^Localization:^S&H Entertainment Localization^^GamersGate:^Ulf Hedblom^Andreas Pousette^Martin Ericson^Christoffer Lindberg\
"),
  ("credits_12", "Thanks to all of our partners worldwide, in particular long-term partners:\
^Koch Media (Germany & UK)^Blue Label (Italy & France)^Friendware (Spain)^New Era Interactive Media Co. Ltd. (Asia)\
^Snowball (Russia)^Pinnacle (UK)^Porto Editora (Portugal)^Hell-Tech (Greece)^CD Projekt (Poland, Czech Republic, Slovakia & Hungary)\
^Paradox Scandinavian Distribution (Scandinavia)\
"),

### TLD strings
 ("faction_strength_crushed"           , "crushed"),
 ("faction_strength_spent_and_wavering", "spent and wavering"),
 ("faction_strength_weakened"          , "weakened"),
 ("faction_strength_in_good_state"     , "in a good state"),
 ("faction_strength_strong"            , "strong"),
 ("faction_strength_very strong"       , "very strong"),
 ("faction_strength_unmatched"         , "unmatched"),

#################################
# TLD faction ranks
#
     ("tfr_name_strings_begin", "tfr_name_strings_begin"),
     ]+concatenate_scripts([
        concatenate_scripts([
                [(tld_faction_ranks[fac][rnk][2][pos][0].lower().replace(" ", "_"), tld_faction_ranks[fac][rnk][2][pos][0]) for pos in range(len(tld_faction_ranks[fac][rnk][2]))
            ] for rnk in range(len(tld_faction_ranks[fac]))
        ]) for fac in range(len(tld_faction_ranks))
     ])+[
    ("promote", "You have been working well for the realm. Now you can be:"),
#
# TLD faction ranks end
#################################

 ("subfaction_gondor_name_begin" , "Gondor"),
 
 ("subfaction_gondor_name1" , "Pelargir" ) ,
 ("subfaction_gondor_name2" , "Dol Amroth" ),
 ("subfaction_gondor_name3" , "Lamedon" ) ,
 ("subfaction_gondor_name4" , "Lossarnach" ),
 ("subfaction_gondor_name5" , "Pinnath Gelin" ),
 ("subfaction_gondor_name6" , "Ithilien" ), 
 ("subfaction_gondor_name7" , "Blackroot Vale" ) ,
 
#### TLD shop/bar rumors
("default_rumor", "The War. Everybody is talking about the war."),
# Rohan
("rohan_rumor_begin", "It breaks my heart to see my babies off to war!  But without them the men would have to walk."),
("rohan_rumor_2", "I hear the Orcs eat horses.  Savages!  Oh, yeah, they also eat prisoners.  That's bad, too, of course."),
("rohan_rumor_3", "There are no horses finer than Rohan's. Even the Elves get their horses from us!"),
("rohan_rumor_4", "If you're a healer of men please treat my horses with just as much care should they be wounded."),
("rohan_rumor_5", "Bring me 8 Sumpter Horses, - he says... after the 7 he asked for yesterday.  Makes you wonder."),
("rohan_rumor_6", "Gondor prefers sturdier horses. Our riders enjoy speed. The Elves buy only the best, which means from us of course -- so to get the very best Rohan horse you'll have to buy it from them."),
("rohan_rumor_7", "I've seen examples of the Desert Mare and Variag Kataphract.  Rohan horses are superior but require a more experienced rider to handle."),
("rohan_rumor_8", "Wargs are slow but very maneuverable.  They're also quite fragile compared to a well-bred warhorse."),
("rohan_rumor_9", "No army fights Rohan without pikes and spears to set against our horsemen.  Saruman will cut down the whole Fangorn forest equipping his armies before this war is done."),
("rohan_rumor_10", "Being the best horsemen in the realm starts with raising the best horses."),
("rohan_rumor_11", "Most of the horses for sale in Gondor came from us. They prefer a slightly stronger, slower horse that can carry a little more armor."),
("rohan_rumor_12", "orses are the backbone of our economy, you know. Everybody gets their horses from us!"),
("rohan_rumor_13", "Orcs are tough but don't wear much protection. They're no match for a good axe."),
("rohan_rumor_14", "Our throwing axes and spears are bulky, but how many chances do your cavalry have to throw a missile before they ride down the foe? Make your one shot count by throwing something with some heft."),
("rohan_rumor_15", "Hitting an orc with an arrow loosed from the back of a horse looks difficult because it is, but the price of charging a rank of long pikes is higher."),
("rohan_rumor_16", "Gondor practices archery. We practice horse archery. Dunlendings practice neither."),
("rohan_rumor_17", "Many of Saruman's orcs are deadly archers. Many are not. A wise cavalry commander shouldn't wait to discover which is which."),

("gondor_rumor_begin", "If everyone traded horses for wargs tomorrow Rohan's children would be thrown into poverty the day after. But then who'd want to ride a warg?"),
("gondor_rumor_2", "Here in Gondor there is nothing under the sun we don't make, build, or grow in some quantity."),
("gondor_rumor_3", "We speculate that food is the orcs' most limiting resource. That would explain the cannibalism, wouldn't it?"),
("gondor_rumor_4", "Rohan has a reputation for its horses, but they also produce an abundance of basic foods at lower cost than Gondor. It may be bland, but it keeps their armies in the field and their people hard at work."),
("gondor_rumor_5", "The Shadow's near-limitless supplies are borne on the backs of an equally vast pool of slave labor."),
("gondor_rumor_6", "Elves build a few things extremely well and charge outrageously for them. Fortunately their demand for human spices is insatiable. Lembas must've tasted terrible before we came along."),
("gondor_rumor_7", "Orcs are literally born into slavery. We don't know exactly how long it takes to birth one -- if they even have mothers -- but we do know they're born ready to work. The economics of sustained conflict look very bleak."),
("gondor_rumor_8", "The Corsairs would've profited far more from trading with us than invading. What plunder could've matched the booty they'd have hauled away selling old Numenorian artifacts to every minor noble in Gondor?"),
("gondor_rumor_9", "Horses? Yes, I sell them. Yes, they're genuine Rohan. You military types think Gondor horses aren't fit for pulling carts, never mind that they were sired by beasts imported from Rohan.  *sigh*"),
("gondor_rumor_10", "Between Sauron and Saruman it is only Saruman who exhibits greed in the conventional sense. He'll deal with anyone and do anything if there's profit in it. What he does with his money is anyone's guess, but rumor has it his agents are well-paid. Whether his lust for money is a sign of weakness or wisdom I cannot say."),
("gondor_rumor_11", "Dol Guldur ... a slave economy built mostly underground, that's all I know."),
("gondor_rumor_12", "Moria? Ahh, the treasures they used to bring out of there! They paid well, too, for food, supplies, wine and ale ... all that's gone, now."),
("other_rumor_begin", "Moria? Ahh, the treasures they used to bring out of there! They paid well, too, for food, supplies, wine and ale ... all that's gone, now."),

("tld_introduction","TLD Introduction - you should go to Edoras."),

("tld_erebor_dungeon","The smell of death surrounds me. I'd better be careful"),
("tld_spear_hit","Ouch!"),    

]
