﻿from module_constants import *

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
  ("s5_s_party", "_{s5}'s Party"),
  ("s5_s_host", "_{s5}'s Host"),

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
 Your first task in the training is to locate the flag in the room and move over it.\
 You can press the Tab key at any time to quit this tutorial or to exit any other area in the game.\
 Go to the flag now."),
  ("tutorial_1_msg_2","Well done. Next we will cover attacking with weapons.\
 For the purposes of this tutorial you have been equipped with bow and arrows, a sword and a shield.\
 You can draw different weapons from your weapon slots by using the scroll wheel of your mouse.\
 In the default configuration, scrolling up pulls out your next weapon, and scrolling down pulls out your shield.\
 If you are already holding a shield, scrolling down will put your shield away instead.\
 Try changing your wielded equipment with the scroll wheel now. When you are ready,\
 go to the flag to move on to your next task."),
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
  ("tutorial_2_msg_8","Very good. Your last task before finishing this tutorial is to face the squire.\
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
 Go pick up up the axe now to begin practice."),
  ("tutorial_3_msg_2","By default, the direction in which you defend (by clicking and holding your right mouse button) is determined by the attack direction of your closest opponent.\
 For example, if your opponent is readying a thrust attack, pressing and holding the right mouse button will parry thrust attacks, but not side or overhead attacks.\
 You must watch your opponent carefully and only initiate your parry AFTER the enemy starts to attack.\
 If you start BEFORE he readies an attack, you may parry the wrong way altogether!\
 Now it's time for you to move on to the next room, where you'll have to defend yourself against an armed opponent.\
 Your task is to defend yourself successfully for thirty seconds with no equipment other than a simple axe.\
 Your axe's attacks are disabled for this tutorial, so don't worry about attacking and focus on your defence instead.\
 Move on to the next room when you are ready to initiate the fight."),
  ("tutorial_3_msg_3","Press and hold down the right mouse button to defend yourself with your axe after your opponent starts his attack.\
 Try to remain standing for thirty seconds. You have {reg3} seconds to go."),
  ("tutorial_3_msg_4","Well done, you've succeeded this trial!\
 Now you will be pitted against a more challenging opponent that will make things more difficult for you.\
 Move on to the next room when you're ready to face him."),
  ("tutorial_3_msg_5","Press and hold down the right mouse button to defend yourself with your axe after your opponent starts his attack.\
 Try to remain standing for thirty seconds. You have {reg3} seconds to go."),
  ("tutorial_3_msg_6","Congratulations, you still stand despite the enemy's best efforts.\
 The time has now come to attack as well as defend.\
 Approach the door and press the F key when you see the word 'Go'."),

  ("tutorial_3_2_msg_1","Your axe's attacks have been enabled again. Your first opponent is waiting in the next room.\
 Defeat him by a combination of attack and defence."),
  ("tutorial_3_2_msg_2","Defeat your opponent with your axe."),
  ("tutorial_3_2_msg_3","Excellent. Now the only thing standing in your way is one last opponent.\
 He is in the next room. Move in and knock him down."),
  ("tutorial_3_2_msg_4","Defeat your opponent with your axe."),
  ("tutorial_3_2_msg_5","Well done! In this tutorial you have learned how to fight ably without a shield.\
 Train hard and train well, and no one shall be able to lay a stroke on you.\
 In the next tutorial you may learn horseback riding and cavalry combat.\
 You can press the Tab key at any time to return to the tutorial menu."),

  ("tutorial_4_msg_1","Welcome to the fourth tutorial.\
 In this sequence you'll learn about riding a horse/warg and how to perform various martial exercises on horseback.\
 We'll start by getting you mounted up.\
 Approach the horse, and press the 'F' key when you see the word 'Mount'."),
  ("tutorial_4_msg_2","While on horseback, the WASD keys control your horse's movement, not your own.\
 Ride your horse and try to follow the flag around the course.\
 When you reach the flag, it will move to the next waypoint on the course until you reach the finish."),
  ("tutorial_4_msg_3","Very good. Next we'll cover attacking enemies from horseback. Approach the flag now."),
  ("tutorial_4_msg_4","Draw your sword (using the mouse wheel) and destroy the four targets.\
 Try hitting the dummies as you pass them at full gallop -- this provides an extra challenge,\
 but the additional speed added to your blow will allow you to do more damage.\
 The easiest way of doing this is by pressing and holding the left mouse button until the right moment,\
 releasing it just before you pass the target."),
  ("tutorial_4_msg_5","Excellent work. Now let us try some target shooting from horseback. Go near the flag now."),
  ("tutorial_4_msg_6","Locate the archery target beside the riding course and shoot it three times with your bow.\
 Although you are not required to ride while shooting, it's recommended that you try to hit the target at various speeds and angles\
 to get a feel for how your horse's speed and course affects your aim."),
  ("tutorial_4_msg_7","Congratulations, you have finished this tutorial.\
 You can press the Tab key at any time to return to the tutorial menu."),
# Ryan END

("tutorial_5_msg_1","Welcome to the fifth and final tutorial, which gives you a brief overview of how to command troops in battle, one of the most important aspects in Mount & Blade.^^\
The first command menu that you have to learn are movement commands, which can be found by pressing the F1 key. Press that now and explore the many movement options you can give your troops in battle.^^\
For this first step, command your troops to follow you and move up the hill where the flag and pointer is."),

("tutorial_5_msg_2","Excellent. Your troops have followed you up the hill. Now you have a good view of the battlefield.^^\
This time, ask your troops to hold this hill by pressing the F1 command menu again, and selecting Hold this Position (F1).^^\
Once you have done that, you will notice your troops stop following you and hold the position you asked them to.^^\
This is a good time to learn the second command menu, which revolves around troop basic formations.^^\
This menu allows you to command your troops to tighten up their ranks, to hold against infantry charges, or spread apart to resist archer volleys.^^\
Commanding your troops to move forward or backward ten paces using this command menu allows your troops to move while keeping their formation.^^\
After exploring the different options, keep your troops holding this hill and move alone towards the opposite hill, where the flag and the pointer is."),

("tutorial_5_msg_3","Great. As you can see, your infantry is holding where you asked them to. Now, move towards the windmill by yourself."),

("tutorial_5_msg_4","Now you have archers join your command. In Mount & Blade, you can give separate commands to specific divisions of troops such as infantry, archers, and cavalry.^^\
Pressing the number keys will choose the division of your choice (1 for Infantry, 2 for Archers, 3 for Cavalry). You can then use the command menus that appear to command the specific division.^^\
Note that the choice will persist, and pressing any of the command menus (F1, F2, F3) will be for the last division chosen. Read the messages that appear on your screen to see which division is being commanded.^^\
Now, ask your Infantry to follow you, then ask your Archers to follow you too. Once they are all together, go back to the hill you came from.^^\
Once there, look for the pointer and command your infantry to move and hold there by pressing 1, then holding the F1 key to reveal a banner. You can use this to move your troops in a precise location of your choice.^^\
Ask your archers to move towards the flag behind the pointer, and on high ground."),

("tutorial_5_msg_5","Your men are in position, the enemies have gathered and are charging towards you. Use what you learned to maneuver your infantry forward in formation, or ask them to charge. Charging breaks all formations, and moves your troops towards the nearest enemies.^^\
You can also keep your archers above ground for a better vantage point, or also ask them to move elsewhere.^^\
You can also press F3 to reveal the third command menu and learn about the different weapon orders you can give your troops."),

("tutorial_5_msg_6","Excellent! You have completed your first field battle in Mount & Blade. Intelligent command of your troops in battle is paramount to your success as a commander in battle. Make sure to learn the different how to move your troops in advantageous positions.^^\
In The Last Days of the Third Age, there are complex formations for more advanced maneouvers such as Infantry Shieldwall and Cavalry Wedges. You can learn more about it in-game.^^\
You can press TAB anytime to leave the tutorial."),

  ("trainer_help_1", "This is a training ground where you can learn the basics of the game. Use A, S, D, W keys to move and the mouse to look around."),
  ("trainer_help_2", "To speak with the trainer, go near him, look at him and press the 'F' key when you see the word 'Talk' under his name.\
 When you wish to leave this or any other area or retreat from a battle, you can press the TAB key."),

  ("custom_battle_1", "Angbor the Fearless and his Gondor company intercepted a Harad reinforcement group.\
 Shouting out his warcry, he spurs his horse forward, and leads his loyal men to a fierce battle."),
  ("custom_battle_2", "Celeborn from Lorien is leading a patrol of horsemen and archers\
 when a forward lookout brings a warning of a force of ash-faced evil men approaching.\
 It's the dreaded Black Numenoreans! Those were not seen near Lothlorien for ages,\
 but now they must be driven back to the neverworld."),
  ("custom_battle_3", "Lord Grimbold of Rohan is leading the last defence of the walls against an army of Isengard.\
 Now, as the besiegers prepare for a final assault on the walls, he must hold the walls with courage and bright steel."),
  ("custom_battle_4", "When the scouts inform Lord Beranhelm of the approach of a Rhun war band,\
 he decides to quickly prepare the defences of his camp and try to hold against superior numbers."),
  ("custom_battle_5", "Ugluk has brought his fierce orksies into the west with the promise of plunder.\
 If he can make this dwarf stronghold fall to him today, his masters in Barad-Dur will be mightily pleased."),
  ("custom_battle_6", "Ugluk and his orc raider squad were as keen as possible in escaping Elven patrols.\
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
  ("1_denar", "1 Resource Point."),
  ("reg1_denars", "{reg1} Resource Points."),

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
  ("april_reg1_reg2",     "T.A.{reg2}, Víressë {reg1} (Apr)"),
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

  ("town_nighttime"," It is late at night."),
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
  ("player_down", "You have been knocked out, but your troops fight on!"),

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
  ("center_captured", "{s2} have taken {s1} from {s3}!"),

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
  # ("secret_sign_1",  "The armoire dances at midnight..."),
  # ("secret_sign_2",  "I am selling these fine Khergit tapestries. Would you like to buy some?"),
  # ("secret_sign_3",  "The friend of a friend sent me..."),
  # ("secret_sign_4",  "The wind blows hard from the east and the river runs red..."),
  
  # ("countersign_1",  "But does he dance for the dresser or the candlestick?"),
  # ("countersign_2",  "Yes I would, do you have any in blue?"),
  # ("countersign_3",  "But, my friend, your friend's friend will never have a friend like me."),
  # ("countersign_4",  "Have you been sick?"),

# Names
#MV: source http://www.kirith.com/name/jsgenerator/
#human
  ("name_1",  "Adanedhel"),
  ("name_2",  "Ondoher"),
  ("name_3",  "Aerandir"),
  ("name_4",  "Agarwaen"),
  ("name_5",  "Ailinel"),
  ("name_6",  "Aldarion"),
  ("name_7",  "Almarian"),
  ("name_8",  "Amandil"),
  ("name_9",  "Amlaith"),
  ("name_10", "Anardil"),
  ("name_11", "Anborn"),
  ("name_12", "Andróg"),
  ("name_13", "Angbor"),
  ("name_14", "Arador"),
  ("name_15", "Araglas"),
  ("name_16", "Arahael"),
  ("name_17", "Arantar"),
  ("name_18", "Arassuil"),
  ("name_19", "Alcarin"),
  ("name_20", "Belegund"),
  ("name_21", "Bereg"),
  ("name_22", "Bergil"),
  ("name_23", "Borthand"),
  ("name_24", "Ceorl"),
  ("name_25", "Ciryon"),
  ("name_26", "Damrod"),
  ("name_27", "Derufin"),
  ("name_28", "Dorlas"),
  ("name_29", "Duilin"),
  ("name_30", "Duinhir"),
  ("name_31", "Egalmoth"),
  ("name_32", "Emeldir"),
  ("name_33", "Eradan"),
  ("name_34", "Erellont"),
  ("name_35", "Erendis"),
  ("name_36", "Falathar"),
  ("name_37", "Fengel"),
  ("name_38", "Forweg"),
  ("name_39", "Frumgar"),
  ("name_40", "Fuinur"),
  ("name_41", "Galdor"),
  ("name_42", "Gethron"),
  ("name_43", "Gorlim"),
  ("name_44", "Grithnir"),
  ("name_45", "Gundor"),
  ("name_46", "Hador"),
  ("name_47", "Haldar"),
  ("name_48", "Hallacar"),
  ("name_49", "Hathol"),
  ("name_50", "Herion"),
  ("name_51", "Hild"),
  ("name_52", "Hunthor"),
  ("name_53", "Imlach"),
  ("name_54", "Ioreth"),
  ("name_55", "Ivorwen"),
  ("name_56", "Labadal"),
  ("name_57", "Larnach"),
  ("name_58", "Magor"),
  ("name_59", "Mairen"),
  ("name_60", "Malach"),
  ("name_61", "Malantur"),
  ("name_62", "Malvegil"),
  ("name_63", "Mardil"),
  ("name_64", "Meneldur"),
  ("name_65", "Minalcar"),
  ("name_66", "Minohtar"),
  ("name_67", "Ondoher"),
  ("name_68", "Orleg"),
  ("name_69", "Orodreth"),
  ("name_70", "Ostoher"),
  ("name_71", "Pelendur"),
  ("name_72", "Ragnor"),
  ("name_73", "Sador"),
  ("name_74", "Súrion"),
  ("name_75", "Thorongil"),
  ("name_76", "Turambar"),
  ("name_77", "Ulfast"),
  ("name_78", "Ulwarth"),
  ("name_79", "Valacar"),
  ("name_80", "Wulf"),
#elf
  ("name_elf_1",  "Merlkir"), #:)
  ("name_elf_2",  "Romanoir"), #:)
  ("name_elf_3",  "Aegnor"),
  ("name_elf_4",  "Amdír"),
  ("name_elf_5",  "Amras"),
  ("name_elf_6",  "Annael"),
  ("name_elf_7",  "Aredhel"),
  ("name_elf_8",  "Arminas"),
  ("name_elf_9",  "Caranthir"),
  ("name_elf_10", "Curufin"),
  ("name_elf_11", "Daeron"),
  ("name_elf_12", "Eluchíl"),
  ("name_elf_13", "Edrahil"),
  ("name_elf_14", "Eluréd"),
  ("name_elf_15", "Erestor"),
  ("name_elf_16", "Faelivrin"),
  ("name_elf_17", "Finrod"),
  ("name_elf_18", "Felagund"),
  ("name_elf_19", "Galathil"),
  ("name_elf_20", "Galdor"),
  ("name_elf_21", "Gelmir"),
  ("name_elf_22", "Gildor"),
  ("name_elf_23", "Guilin"),
  ("name_elf_24", "Ithilbor"),
  ("name_elf_25", "Lindir"),
  ("name_elf_26", "Lómion"),
  ("name_elf_27", "Maedhros"),
  ("name_elf_28", "Maeglin"),
  ("name_elf_29", "Malgalad"),
  ("name_elf_30", "Nellas"),
  ("name_elf_31", "Nerdanel"),
  ("name_elf_32", "Nerwen"),
  ("name_elf_33", "Nimloth"),
  ("name_elf_34", "Orodreth"),
  ("name_elf_35", "Oropher"),
  ("name_elf_36", "Orophin"),
  ("name_elf_37", "Saeros"),
 # ("name_elf_38", "Coder"), #:)
#dwarf
  ("name_dwarf_1",  "Assistnik"), #:)
  ("name_dwarf_2",  "Vader"), #:)
  ("name_dwarf_3",  "Azaghâl"),
  ("name_dwarf_4",  "Bifur"),
  ("name_dwarf_5",  "Bofur"),
  ("name_dwarf_6",  "Bombur"),
  ("name_dwarf_7",  "Borin"),
  ("name_dwarf_8",  "Dori"),
  ("name_dwarf_9",  "Dwalin"),
  ("name_dwarf_10", "Farin"),
  ("name_dwarf_11", "Frár"),
  ("name_dwarf_12", "Frerin"),
  ("name_dwarf_13", "Frór"),
  ("name_dwarf_14", "Gamil"),
  ("name_dwarf_15", "Gróin"),
  ("name_dwarf_16", "Grór"),
  ("name_dwarf_17", "Ibun"),
  ("name_dwarf_18", "Khîm"),
  ("name_dwarf_19", "Lóni"),
  ("name_dwarf_20", "Mîm"),
  ("name_dwarf_21", "Nár"),
  ("name_dwarf_22", "Narvi"),
  ("name_dwarf_23", "Nori"),
  ("name_dwarf_24", "Óin"),
  ("name_dwarf_25", "Ori"),
  ("name_dwarf_26", "Telchar"),
  ("name_dwarf_27", "Marco"), #:)
  ("name_dwarf_28", "Octo"), #:)
#orc, from http://www.orcs.ca/orcsmain/resourcename.html#ONL
  ("name_orc_1",  "Triglav"), #:)
  ("name_orc_2",  "Adgulg"),
  ("name_orc_3",  "Aghed"),
  ("name_orc_4",  "Aguk"),
  ("name_orc_5",  "Alog"),
  ("name_orc_6",  "Azhug"),
  ("name_orc_7",  "Bagdud"),
  ("name_orc_8",  "Bargulg"),
  ("name_orc_9",  "Bog"),
  ("name_orc_10", "Borug"),
  ("name_orc_11", "Bulgan"),
  ("name_orc_12", "Bumhug"),
  ("name_orc_13", "Carguk"),
  ("name_orc_14", "Dalthu"),
  ("name_orc_15", "Derthag"),
  ("name_orc_16", "Dregu"),
  ("name_orc_17", "Dugarod"),
  ("name_orc_18", "Ertguth"),
  ("name_orc_19", "Fandagh"),
  ("name_orc_20", "Farghed"),
  ("name_orc_21", "Fozhug"),
  ("name_orc_22", "Furbog"),
  ("name_orc_23", "Gholug"),
  ("name_orc_24", "Gnalurg"),
  ("name_orc_25", "Grug"),
  ("name_orc_26", "Haguk"),
  ("name_orc_27", "Hoknuk"),
  ("name_orc_28", "Igmut"),
  ("name_orc_29", "Jolagh"),
  ("name_orc_30", "Jukha"),
  ("name_orc_31", "Karguk"),
  ("name_orc_32", "Klog"),
  ("name_orc_33", "Krothu"),
  ("name_orc_34", "Kulgha"),
  ("name_orc_35", "Margulg"),
  ("name_orc_36", "Mazhug"),
  ("name_orc_37", "Naghat"),
  ("name_orc_38", "Nugbu"),
  ("name_orc_39", "Nurbag"),
  ("name_orc_40", "Oggha"),
  ("name_orc_41", "Olodagh"),
  ("name_orc_42", "Omogulg"),
  ("name_orc_43", "Opoguk"),
  ("name_orc_44", "Orgoth"),
  ("name_orc_45", "Perthag"),
  ("name_orc_46", "Pofhug"),
  ("name_orc_47", "Prutha"),
  ("name_orc_48", "Raguk"),
  ("name_orc_49", "Romarod"),
  ("name_orc_50", "Rugbu"),
  ("name_orc_51", "Sargulg"),
  ("name_orc_52", "Slog"),
  ("name_orc_53", "Suhgan"),
  ("name_orc_54", "Surgha"),
  ("name_orc_55", "Torug"),
  ("name_orc_56", "Turbag"),
  ("name_orc_57", "Urghat"),
  ("name_orc_58", "Varguk"),
  ("name_orc_59", "Zlog"),
  ("name_orc_60", "Zunuguk"),
  
# Surname
  ("surname_1",  "{s50} of Tarnost"),
  ("surname_2",  "{s50} of Lossarnach"),
  ("surname_3",  "{s50} of Erech"),
  ("surname_4",  "{s50} of Edhellond"),
  ("surname_5",  "{s50} of Pelargir"),
  ("surname_6",  "{s50} of Linhir"),
  ("surname_7",  "{s50} of Ethring"),
  ("surname_8",  "{s50} of Aldburg"),
  ("surname_9",  "{s50} of Isengard"),
  ("surname_10", "{s50} of Westfold"),
  ("surname_11", "{s50} of Erebor"),
  ("surname_12", "{s50} of Eastfold"),
  ("surname_13", "{s50} of Morannon"),
  ("surname_14", "{s50} of Cirith Ungol"),
  ("surname_15", "{s50} of Osgiliath"),
  ("surname_16", "{s50} of Moria"),
  ("surname_17", "{s50} of Dale"),
  ("surname_18", "{s50} of Esgaroth"),
  ("surname_19", "{s50} of Dol Guldur"),
  ("surname_20", "{s50} of Gundabad"),
#nicknames start here
  ("surname_21", "{s50} the Long"),
  ("surname_22", "{s50} the Gaunt"),
  ("surname_23", "{s50} the Nazgul"),
  ("surname_24", "{s50} the Sparrow"),
  ("surname_25", "{s50} the Cursed"),
  ("surname_26", "{s50} the Scarred"),
  ("surname_27", "{s50} the Fair"),
  ("surname_28", "{s50} the Grim"),
  ("surname_29", "{s50} the Red"),
  ("surname_30", "{s50} the Black"),
  ("surname_31", "{s50} the Tall"),
  ("surname_32", "{s50} the Star-Eyed"),
  ("surname_33", "{s50} the Fearless"),
  ("surname_34", "{s50} the Tree-biter"),
  ("surname_35", "{s50} the Cunning"),
  ("surname_36", "{s50} the Coward"),
  ("surname_37", "{s50} the Bright"),
  ("surname_38", "{s50} the Quick"),
  ("surname_39", "{s50} the Minstrel"),
  ("surname_40", "{s50} the Bold"),
  ("surname_41", "{s50} the Hot-Head"),
  
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


# Retirement Texts: s7=village name; s8=castle name; s9=town name #No retirement in TLD
  ("retirement_text_1", "Unused"),
  ("retirement_text_2", "Unused"),
  ("retirement_text_3", "Unused"),
  ("retirement_text_4", "Unused"),
  ("retirement_text_5", "Unused"),
  ("retirement_text_6", "Unused"),
  ("retirement_text_7", "Unused"),
  ("retirement_text_8", "Unused"),
  ("retirement_text_9", "Unused"),
  ("retirement_text_10", "Unused"),


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
  ("excessive_casualties", "sacrifice so many of our soldiers"),

# chivalric - aristocratic
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
#npc1 = Mablung (Gondor)
#npc2 = Cirdil (Gondor)
#npc3 = Ulfas (Rohan)
#npc4 = Gálmynë (Rohan)
#npc5 = Glorfindel (Lorien)
#npc6 = Luevanna (Mirkwood Elves)
#npc7 = Kíli (Erebor)
#npc8 = Faniul (Dale)
#npc9 = Gulm (Isengard)
#npc10 = Durgash (Isengard)
#npc11 = Ufthak (Mordor)
#npc12 = Gorbag (Mordor)
#npc13 = Lykyada (Harad)
#npc14 = Fuldimir (Umbar)
#npc15 = Bolzog (Moria)
#npc16 = Varfang (Rhun)
#npc17 = Dímborn (Beornings)
  
  ("npc1_intro", "Hail, warrior, and welcome to Henneth Annûn."),
  ("npc2_intro", "Hail, visitor! Might I ask what is your business here?"),
  ("npc3_intro", "Ho! Keep the racket down if you please, traveller."),
  ("npc4_intro", "Welcome to Meduseld, warrior!"),
  ("npc5_intro", "Hail {playername}. Mae govannen!"),
  ("npc6_intro", "Leave me alone, stranger, I do not wish to speak to you."),
  ("npc7_intro", "Kíli, son of Dwalin, at your service!"),
  ("npc8_intro", "Welcome to Dale, traveller! How can I help you?"),
  ("npc9_intro", "Ssh! If you so much as wave to the guards, I'll slice out your gizzard and feed it to the wargs!"),
  ("npc10_intro", "You!"),
  ("npc11_intro", "Ar! You're not from around here are you? I can smell it, an' if you say I can't in front of the Bosses I'll squeeze your eyes out!"),
  ("npc12_intro", "Oho! What are you doing, lurking up here?"),
  ("npc13_intro", "Hold there! What brings you to the Chieftain's tent?"),
  ("npc14_intro", "You have the walk of a man whose legs have seen too few days at sea, stranger."),
  ("npc15_intro", "Praise the Eye, oh Warrior!"),
  ("npc16_intro", "It is not often one strange to my eyes walks among tents of the eastern lands. What brings you here? Speak now and be swift."),
  ("npc17_intro", "Hey. Fancy them woods there?"),

  ("npc1_intro_response_1", "Hail, Master Tracker. How fare the Rangers of the South?"),
  ("npc2_intro_response_1", "My business is Gondor's business, and who are you?"),
  ("npc3_intro_response_1", "And a good day to you too, is there something amiss?"),
  ("npc4_intro_response_1", "Greetings, my Lady. With whom do I have the honour to speak?"),
  ("npc5_intro_response_1", "Hail Elf-lord! It's a great honour to meet you."),
  ("npc6_intro_response_1", "Is this how the Silvan Elves greet their guests?"),
  ("npc7_intro_response_1", "{playername} at your service. How fare the Durin's folk?"),
  ("npc8_intro_response_1", "Greetings. I was wondering if there are any volunteers here to join us in our travels."),
  ("npc9_intro_response_1", "Hold your threats, Uruk, before it comes to blows - I am not a snitch."),
  ("npc10_intro_response_1", "Who are you?"),
  ("npc11_intro_response_1", "Who are you?"),
  ("npc12_intro_response_1", "Who are you?"),
  ("npc13_intro_response_1", "Who are you?"),
  ("npc14_intro_response_1", "Who are you?"),
  ("npc15_intro_response_1", "Praise the Eye, Snaga. What's your story?"),
  ("npc16_intro_response_1", "Who are you?"),
  ("npc17_intro_response_1", "Mirkwood is a magnificent forest. Who are you? Do you know much about the woods?"),

  ("npc1_intro_response_2", "Never mind, I fear caves do not make a pleasant place for conversation."),
  ("npc2_intro_response_2", "Never mind, I don't have time to speak to guards."),
  ("npc3_intro_response_2", "Never mind, I'll make 'racket' elsewhere."),
  ("npc4_intro_response_2", "Excuse me, I have urgent matters elsewhere."),
  ("npc5_intro_response_2", "Excuse me, I have less important people to talk to."),
  ("npc6_intro_response_2", "The feeling is mutual. Goodbye."),
  ("npc7_intro_response_2", "Never mind, I need some fresh air."),
  ("npc8_intro_response_2", "Never mind, we are merely sight-seeing."),
  ("npc9_intro_response_2", "I'll just be on my way then, or my sword arm will start to itch."),
  ("npc10_intro_response_2", "[Ignore and leave]"),
  ("npc11_intro_response_2", "Mind your business, maggot!"),
  ("npc12_intro_response_2", "Mind your business, maggot!"),
  ("npc13_intro_response_2", "Mind your business!"),
  ("npc14_intro_response_2", "Mind your business!"),
  ("npc15_intro_response_2", "Hmmf. Keep your little claws to yourself, Snaga."),
  ("npc16_intro_response_2", "Mind your business!"),
  ("npc17_intro_response_2", "Yes, the woods are lovely, but I've got to run along now."),

#backstory intro
  ("npc1_backstory_a", "You come at a difficult time, friend. Ithilien is flooded by enemy scouts and raiders, and some had seen great hosts of orcs on the move. We do try to prevent the foul creatures from crossing the great river and I have led a group of skilled Rangers to many a success. My Captain Faramir is bold and I don't despair of the Shadow hanging over us."),
  ("npc2_backstory_a", "Ah, how graceful to inquire about me. I have been newly assigned as a guard of His Stewardship's hallways, a proud duty, if I may say so, if not very eventful."),
  ("npc3_backstory_a", "Well, my old helmet here is getting smaller by the minute and the ground seems wobbly as if I rode a mischievous foil. Ah, if I only hadn't drank all that ale last night - I normally have a good head for drink, so it must have been some nasty orc brew."),
  ("npc4_backstory_a", "My name is Gálmynë, and I made it my business to know yours, {playername}. Let me explain why."),
  ("npc5_backstory_a", "You may have heard tales of my deeds in battles past and forgotten by mortal Men. In the fullness of time this War is yet another time of danger for the Eldar, but it will be the Last War."),
  ("npc6_backstory_a", "Excuse my brashness, stranger, but we don't have many visitors here and those that come do not look very trustworthy. Only a week ago, this dwarf appeared and... Never mind. My name is Luevanna, of the Silvan Elves of Mirkwood."),
  ("npc7_backstory_a", "Polite of you to ask, {playername}. We are fighting off incursions from Easterlings and Gundabad orcs, but so far nothing we and our Dale allies can't handle."),
  ("npc8_backstory_a", "I'm sure you can find some fine volunteers if you speak to the quartermaster in the barracks. As for me, I'm merely a healer and herbalist of modest skills."),
  ("npc9_backstory_a", "Good for you! They call me Gulm. I have gutted my sergeant and his snaga s now hunt for me.^The worthless piglet had it coming! Once, we got ambushed by a strawheads patrol... and he lost it. 'Fall back' he screams, then flees. Only Gulm and a few others stood firm, and broke their horses charge. Then we bludgeoned the yellow-haired into paste (heh heh heh). But if it wasn't for us strong ones, all would be worm food!"),
  ("npc10_backstory_a", "I am Durgash!"),
  ("npc11_backstory_a", "Nar! Not a tracker, that's who. They threw me out! I tell you they've lost their heads, that's what it is. Curse 'em! First they say I shoot wild, then I run too slow, and then I have a useless snuffler. Garn! If they don't find a rabble for me soon I'll be for the Black Pits, if what I hear is true. I'll make sure some of those Bosses lose their skins sooner than putting me in there!"),
  ("npc12_backstory_a", "I'm in command of a band of lads up here. I'm Gorbag and you'd best learn quick lubber us Uruks are the real bosses 'round here. The Big Bosses makes slips, 'ay, even the Biggest can make mistakes, and always the poor Uruks to put slips right, and small thanks. They don't even tell us all they know, do they? Not by half. Grr!"),
  ("npc13_backstory_a", "I? I am a grain of soil from southern sands, blown north by cold and dark night winds. I am Lykyada, a Serpent Lord of Haradwaith. Lord of the Gold Serpent, bane of the Black Serpent Tribe, now allied to serve the will of the Dark Lord."),
  ("npc14_backstory_a", "I am Fuldimir, son of the southern realm of Umbar, south of Harondor, and the Bay of Belfalas, for both are home to my heart and my people. We are the lords of sea and sail, corsairs to some, kin of the Bay of Belfalas for her waters we tame."),
  ("npc15_backstory_a", "I am Bolzog the Gifted, Setter of Bones, Closer of Cuts, and Shaman of Healing. If you go to war for The Eye, you will no doubt have one or other of your little fellows cut about a bit by pale-faced foresters or the horse-lovers. Now, -nar-nar-nar! - Orcs are easy to replace, Oh Great Leader, but can you replace a Warg? A Giant? A Cave Troll? Shi-shi! No! You need me, the Great Bolzog!"),
  ("npc16_backstory_a", "Well now, it is the stranger who should declare himself first. Nevertheless, I am Varfang of the Balchoth kin... I can tell that you have not yet heard the songs or tales of my land that speak the name of the Balchoth, for the very name would check your courage and fill your heart with woe."),
  ("npc17_backstory_a", "They call me Dímborn and I work in the woods. It is nice there. I like the woods. Many trees in the woods. I like trees. I've worked in the woods all my life, because I am strong and because I like trees."),

#backstory main body
  ("npc1_backstory_b", "You should know that I am an Ithilien Ranger of Dúnedain descent and valor. I know much of tracking and scouting and my skill with bow and sword is known to the orc. I can also train any soul that's willing to fight the coming Shadow."),
  ("npc2_backstory_b", "I have been trained as a Minas Tirith watchman, to keep order in the White City and serve my lord Steward."),
  ("npc3_backstory_b", "I am a Rider of the Westfold éored - they left without me on a long patrol to the Isen fords. I know their conduct will be worthy of the green banner, but I fear many won't return."),
  ("npc4_backstory_b", "I was born into a noble family and I have been serving Lady Éowyn as a maid of honour ever since we were little girls. Our fathers were wise enough to allow us to train alongside our brothers in matters of combat, to become shieldmaidens of Rohan."),
  ("npc5_backstory_b", "Lord Elrond sent me as an emissary to Lord Celeborn, to give aid and advice as it's needed in the War in this part of Rhovanion."),
  ("npc6_backstory_b", "I like to walk the hidden paths in our beautiful forest. Sometimes I move quietly through the trees and observe the habits of the many woodland animals. The song of a rare bird, the nesting of a wild boar are as beautiful to me as the clash of weapons and great walls are to the Edain."),
  ("npc7_backstory_b", "I helped improve the Erebor defenses and trained some younger dwarven folk, under the direction of my venerated father Dwalin, as is our custom."),
  ("npc8_backstory_b", "I have treated my King Brand for constipation, a common malaise affecting men going to war. A light brew of wormwood, and both the bowels and the mind are put at ease."),
  ("npc9_backstory_b", "So I said to myself, 'Gulm, you want end up as carrion?' and I answered, 'No'.^Next battle, I fell back pretending I was injured. Then, with no one watching, I fell upon my sergeant! Cleaved him almost in half, gharr! Then cut his sidekick snaga nicely^^...Turned out that bloody creeper survived somehow, and started waggling his tongue about all this. Next time I make sure his head is off, gharr..."),
  ("npc10_backstory_b", "I am a Wolf Rider of Isengard and a tracker."),
  ("npc11_backstory_b", "Ar! It's only 'cause my nose was snotty. An' what good is it wearing my nose out on stones anyhow? Nar! It was those filthy Uruks! Those cursed peaching sneakthiefs! I only lost the scent through giving way to them. They messed up the scent back there, pinching anything they found, and stomping all round the place before I could get there."),
  ("npc12_backstory_b", "And those Nazgul give me the creeps. And they skin the body off you as soon as look at you, and leave you all cold in the dark on the other side. But He likes 'em; they're His favourites nowadays, so it's no use grumbling. I tell you, it's no game serving in the city. I'd like to try somewhere where there's none of 'em."),
  ("npc13_backstory_b", "I saw of late the word of the Dark Lord spread among my kin, and in their hearts and minds his will crept. Most were drawn to his darkness, and in place of their courage grew an insatiable lust for slaughter so that when their ears heard his call few puppets were so willing to answer."),
  ("npc14_backstory_b", "There is much change in a man who rides the tumult of the winds and seas of the Belfalas waters, and those yet to battle her will are but children. For stout men are they who meet her tempest and ride her storm. I have laid eyes on her darkest tide and yet remain her master."),
  ("npc15_backstory_b", "Many moons ago, when I was just a fresh little thing, my Grandsire led the tribe down into the mines, where the dwarves had recently died. A Fire Wraith had passed through, and it was comfortable and warm. We prospered, but every so often some cruel adventurer, or Dwarf hero, would come and kill and maim us in our peaceful tunnels. My hands learned to close the wound of sword or axe, and my mind learned to see the outline of bone and sinew below any hide. These days, I can work a potion or set a break with equal skill."),
  ("npc16_backstory_b", "The Balchoth were a fierce race of men from my home land, slaughtered by these westerlings to all but a few men. Chased down like beasts of burden as food for their blades. The blood spilt by those blades is the same blood that flows within me, for within me their house continues."),
  ("npc17_backstory_b", "You can make many things out of the trees, you know. It's what I do. I work with trees and make things out of trees. Sometimes bushes also. But I like trees more."),

#backstory recruit pitch
  ("npc1_backstory_c", "However, I fear we are hopelessly outnumbered here in Ithilien and we won't last long without reinforcements or bolder action by our Steward. I might as well help where my actions would account for more, if my Captain Faramir gives me leave."),
  ("npc2_backstory_c", "However important my duty here is, I'm quite anxious to see real combat and... elves and talking trees and oliphaunts! You seem well-travelled, commander, and I don't mean that as a slight on your appearance, not by a fathom. I learn quickly and can cook... well, good enough for soldiers that is. Am I not mistaken that you are looking for volunteers?"),
  ("npc3_backstory_c", "So, here I am, disgraced and bitter. My éored must be miles away now, and I wouldn't have a fair chance of catching up with them, not with all the orcs and wildmen roaming the plains. Are you by any chance in need of a fine Rohirrim rider?"),
  ("npc4_backstory_c", "You might know that women, however skilled, are not allowed to ride with the éoredas. However, I do not think that waiting by the hearth for the warriors to return is my fate. I will not sit idle until all chance of great deeds is gone in this War, and I would welcome your assistance, warrior."),
  ("npc5_backstory_c", "However, if the enemies of Lothlórien are on the run, I might consider joining you for a while, {playername}. I sense our fates in this War are interwoven."),
  ("npc6_backstory_c", "You wouldn't understand that, I think, seeing you prepared for war. But you must have travelled far and wide - have you seen the other great forests? Can you take me there?"),
  ("npc7_backstory_c", "There is a lull in the fighting that ill-suits a dwarven warrior of my ancestry and temperament. I gather you get to see much more action in your travels and your cause is friendly with the dwarves? I know a fighting dwarf will greatly improve your chances of survival."),
  ("npc8_backstory_c", "I hear there is much fighting elsewhere and our lands are gratefully spared for now. From the scratches on your armor you must have been in danger many times. Maybe my humble skills could be better used with your company, for the greater good of all."),
  ("npc9_backstory_c", "I am a fighting Uruk-hai, and a berserker! What there is to know of killing men, I know it. I was in the service of the White Hand, but now the Hand would as likely throw me into the fire-pits.^^I would come with you and hunt men in the south, while the snagas of Isengard gnash their teeth."),
  ("npc10_backstory_c", "Maybe you can be my next master."),
  ("npc11_backstory_c", "All right, all right! My nose isn't much use. I reckon my eyes are better than my nose. Ai! But my nose is only no good cause it don't know what nothing smells like. It don't even know what it's looking for, I tell you. Ar! I just need to go lopin' off and start sniffing places."),
  ("npc12_backstory_c", "Eh, if I get a chance, I'll slip off and set up somewhere on my own with a few trusty lads, somewhere there's good loot nice and handy, and no big bosses. I'd like to try somewhere where there's none of 'em, like old times."),
  ("npc13_backstory_c", "I followed my kin north, and heeded his dark call, to fulfill the duty I have to my people. But in them I see his darkness dwell and I seek to do my part in this war elsewhere, until the sands of my time no longer fall. Even now I feel them begin to trickle where before there was a cascade."),
  ("npc14_backstory_c", "But there comes yet the darkest tide, a black tide of shadow, which will rise over these lands such as which no mortal eyes will have seen. This is the tide I seek to master, but I am without a crew hardy enough to ride this storm."),
  ("npc15_backstory_c", "After many winters I came up out of the tunnels, and looked about in the Dark Forests for a good place to live and practice my arts. I was doing fine, until some big ugly bastards with white tattoos – eugh! White! Like an elf face! – big bastards, they were. They fired my little place in the Forest, and I had to hide in the caves again... In here... Say, have you anything to eat? Maybe a nice horse?"),
  ("npc16_backstory_c", "That was many lives of men ago, a different time, but the time for grief and tales are over. The time for my people's retribution has come and I will carve my people's vengeance on the face of these western lands. By my hand, their homes will waste and wither until their clan is no more!"),
  ("npc17_backstory_c", "If you're going into the forest, maybe I come along and tell you about the trees there? Many very interesting trees there, you know."),


### use these if there is a short period of time between the last meeting 
  ("npc1_backstory_later", "I have been leading scouting parties to the south, as far as Emyn Arnen. There is much Enemy activity and many an orc fell to our ambush. Alas, that's only so many orc heads rolling down the gullies, we saw a myriad of foul creatures on the march. I fear for my Ithilien and the fate of Gondor."),
  ("npc2_backstory_later", "We've had a few visitors lately, and there are fewer to come. I reckon that doesn't bode well."),
  ("npc3_backstory_later", "Still no news of my éored, and I'm keen on riding down some orcs."),
  ("npc4_backstory_later", "More riders return with their bodies broken, and I try to give aid where I can. But I still feel trapped in a cage."),
  ("npc5_backstory_later", "Have you reconsidered? The time for the Eldar grows short."),
  ("npc6_backstory_later", "I've been observing a nest of giant spiders for a couple of days. Ugly creatures, they seem at first, but they keep intruders at bay. Did you come to ask me to travel with you?"),
  ("npc7_backstory_later", "Building up defensive walls is worthy of any dwarf. But I need to use my axe too. Soon. Let me come with you."),
  ("npc8_backstory_later", "I made another call to our King, this time for vomiting. I hope his resolve to engage the enemy is not related to his conditions. Do you suffer from constipation and vomiting too?"),
  ("npc9_backstory_later", "What do you think I do? Gulm is sitting here and waiting for some sneaky snaga to stick him in the dark. Take me with you - I will serve well."),
  ("npc10_backstory_later", "Have you reconsidered? I will serve well."),
  ("npc11_backstory_later", "Ar! It was you! I smelt you, I knew you were coming. Tell the Bosses that, will ya? They think since I was kicked out of the trackers that it's safe to flout me, well they're mistaken, I'll put an arrow in their guts first. And whose blames was that? Not mine!"),
  ("npc12_backstory_later", "I have my orders. Any trespasser found by my lads up here are to be stripped; teeth, nails, hair and all. But I've got my watchers. We know there are funny things going on: with the big bosses going off to war, and all that. Big things going on away west, they say. Sitting here doin' nothing is more than my belly's worth."),
  ("npc13_backstory_later", "My role here goes well for the dark cause, and once more the Northerners fear the south. I see great victories ahead, and rivers of blood left in our wake. But with each victory I see my kin corrupted, their hearts twisted to his evil will. The sight of it leads me to despair."),
  ("npc14_backstory_later", "You have returned stranger, it is perhaps an omen. I have been reading the waters, and I have seen them darken. The sea changes the eyes of a man, and teaches him to use his eyes to listen to her language."),
  ("npc15_backstory_later", "Many have been the great ones who have begged to be healed by my potions.   Horselovers and the pale-faced elves are many though, and I have had to abandon my hut once more, and am... well, Great Lord, I am not so lucky as when we fought together, and you were grateful for my skills..."),
  ("npc16_backstory_later", "Long does the history of my people recount these lands. I know not what their treacherous histories say of days when my people before entered this land, but sad and dark will their histories be as my people enter it now. Like a storm of hooves and swords and arrows, we will bring them doom like the Balchoth before us."),
  ("npc17_backstory_later", "I've seen a very old pine the other day. Pines can get very old. You have to respect old trees. But I've also seen some that don't respect trees at all. You respect trees, don't you?"),


  ("npc1_backstory_response_1", "If you can get leave, I have much need of an experienced warrior and a tracker."),
  ("npc2_backstory_response_1", "You are correct, I am looking for volunteers."),
  ("npc3_backstory_response_1", "If you can do without ale, I would welcome a good horseman."),
  ("npc4_backstory_response_1", "I would welcome the help of a Rohan shieldmaiden, if offered."),
  ("npc5_backstory_response_1", "It may be presumptuous of me to ask, but my company could use your skill in the coming battles."),
  ("npc6_backstory_response_1", "We travel the world, but to defend all that is fair, we give battle to the enemy."),
  ("npc7_backstory_response_1", "Indeed, a dwarven warrior would be welcome in my company."),
  ("npc8_backstory_response_1", "We can use a healer and a herbalist."),
  ("npc9_backstory_response_1", "I reckon we could put a berserker to a good use."),
  ("npc10_backstory_response_1", "You will do."),
  ("npc11_backstory_response_1", "How 'bout loping off with me?"),
  ("npc12_backstory_response_1", "How 'bout slippin' off with me."),
  ("npc13_backstory_response_1", "How about following me?"),
  ("npc14_backstory_response_1", "How about joining me?"),
  ("npc15_backstory_response_1", "Aha... A healer, heh? And you are good at it, you say? I could use someone like you."),
  ("npc16_backstory_response_1", "What are you doing here?"),
  ("npc17_backstory_response_1", "Well, one can always learn more about trees. We'd be glad to have you along."),

  ("npc1_backstory_response_2", "I am sorry to hear that. May your faith sustain your valor."),
  ("npc2_backstory_response_2", "No, sorry. I'm looking for seasoned warriors."),
  ("npc3_backstory_response_2", "No, sorry. I'm looking for someone more reliable."),
  ("npc4_backstory_response_2", "I am sorry, my Lady, there's nothing I can do."),
  ("npc5_backstory_response_2", "I'll be back when Lothlórien is in less danger."),
  ("npc6_backstory_response_2", "No, sorry. We cannot take hangers-on."),
  ("npc7_backstory_response_2", "No, sorry. We do well on our own."),
  ("npc8_backstory_response_2", "No, sorry. We only visit healers when we need them."),
  ("npc9_backstory_response_2", "Bah. I don't trust traitors."),
  ("npc10_backstory_response_2", "I don't need you, slave."),
  ("npc11_backstory_response_2", "I don't want to hear your skulking."),
  ("npc12_backstory_response_2", "The Big Bosses know best. You better follow orders."),
  ("npc13_backstory_response_2", "That is your fate to suffer."),
  ("npc14_backstory_response_2", "I've had enough of this."),
  ("npc15_backstory_response_2", "Bah! I need fighters, not skulkers."),
  ("npc16_backstory_response_2", "I've had enough of this."),
  ("npc17_backstory_response_2", "No, I'm sorry. We're off to war, not to a botanical journey."),

  ("npc1_signup", "I am sure Captain Faramir would understand there are others who can keep the Enemy at bay with even more valor and courage."),
  ("npc2_signup", "Oh, a happy day! I would be glad to join your company."),
  ("npc3_signup", "Trust me, commander, all the ale I need is the sweet drink of victory. If you can lead me against the enemy, they will soon feel the business end of a Rohirrim spear!"),
  ("npc4_signup", "It is gladly offered, and you can welcome me to your company, commander."),
  ("npc5_signup", "I see. I admit I have heard of you and your exploits."),
  ("npc6_signup", "I dislike violence and weapons of war, but I know how to defend myself in a hurry."),
  ("npc7_signup", "I am skilled with an axe, both the wielding and the throwing type. I can also keep your bills low if you let me talk to the merchants. And I have an eye for finding the best pieces of loot from fallen enemies on the battlefield."),
  ("npc8_signup", "Indeed? Well then, I merely need to gather my herbs and recipees."),
  ("npc9_signup", "A fighting Uruk is worth more than all your snagas. A fighting Uruk never runs from battle."),
  ("npc10_signup", "Really? You would do well to enlist me."),
  ("npc11_signup", "Follow your mob Ai? Ar! I hear about all these goings-ons out west, raids and all, and hundreds of our lads done in. I'll come and have a look with you all the same, and see what you're up to."),
  ("npc12_signup", "Follow your rabble, 'ay? I may 'ave struck a bit of luck at last. I give a good rumble, I reckon, and my whip is vigilant. It's tasted its fair share of my lads' orc hide."),
  ("npc13_signup", "I may follow you if you will have me. My legs make good heading of a horse between them and my hands know well the feel of blades of the crescent moon. My fingers can make fall arrows like the plight of stars upon our enemy, be it on horse or feet, though how I fight will be at your command."),
  ("npc14_signup", "Perhaps, know though that I am no thief or brigand. I will not steal, nor take that which other lives may find needed."),
  ("npc15_signup", "Heh-heh. You are right! Yeesss! You are wise, Great Captain."),
  ("npc16_signup", "I wait for orders, with every second passing darkening my heart. I can no longer stand to wait for the plans of far away lords and captains so unseen their existence is believed more in legend than in flesh. Lords whose whispered orders are brought forth and shouted by lesser men. I wait, and with me, my people's vengeance waits also."),
  ("npc17_signup", "Very good! I know many trees. Soon you will know many trees too. Like me. Because I know many trees."),

  ("npc1_signup_2", "It would take a moment to talk to my Captain and gather my things."),
  ("npc2_signup_2", "I'll need to talk to my Sergeant first and then off we go - there are glorious battles to be fought and all manners of strange creatures to see!"),
  ("npc3_signup_2", "I've been waiting for someone to take me on, so I only need to saddle up my horse and we are ready to ride."),
  ("npc4_signup_2", "I have hunted game many times with bows and throwing spears. I will hunt orc under your command. And I have some skill in healing I'm certain will be needed."),
  ("npc5_signup_2", "Perhaps by joining your company and striking hard where I am not expected, the Enemy will be unbalanced. I will come."),
  ("npc6_signup_2", "Perhaps I can teach you to move faster and make less noise. Let's go."),
  ("npc7_signup_2", "If you can keep the tall-folk in your company in line, especially the sneaky Elves, I'll gladly join you."),
  ("npc8_signup_2", "I must warn you though, I am fairly useless in battle. But I'm sure you are able to keep a woman of my age safe."),
  ("npc9_signup_2", "But you must decide quickly, the guards here are getting suspicious."),
  ("npc10_signup_2", "You won't regret taking me on."),
  ("npc11_signup_2", "Lots of stuff out there for my nose to smell too, and my knife to taste. They don't know too much now but they're quick learners alright. What d'you say?"),
  ("npc12_signup_2", "I'll show your slugs where there's a whip there's a will and give 'em as much lash as their skins will carry. If your lads take it well it should put 'em in a good trot. What d'you say?"),
  ("npc13_signup_2", "Know, though, that my loyalty lie always with my kin. I have fought this far and lost too much for them. I will not turn my back on them for their fate will be my own."),
  ("npc14_signup_2", "It is just fortunate that those no longer of this world find no need of this world's treasures and I am fortunate to be skilled in ways that I may assist in relieving the worldly needs of the owners of those treasures."),
  ("npc15_signup_2", "Oh, this is a great moment for Bolzog The Gifted, and for you, Great Lord! We shall conquer together, you, indestructible with my healing touch, and I, the Great Orc Sage who shall support you!"),
  ("npc16_signup_2", "I fear that I will not wait any longer. I intend on joining the next party to leave camp, with my Chieftain's approval or not. I fear the war will be over long ere I leave to join it."),
  ("npc17_signup_2", "I'll just get some of my tools, and we can be off. There is this oak just down the road I must show you!"),


  ("npc1_signup_response_1", "I could use a skilled ranger, you are welcome to join."),
  ("npc2_signup_response_1", "Very well. We could use some cheer in these dark times."),
  ("npc3_signup_response_1", "Very well. Saddle up - we shall be leaving shortly."),
  ("npc4_signup_response_1", "Impressive. We are ready to leave, whenever you are, my Lady."),
  ("npc5_signup_response_1", "We will be honoured to have the company of an Elf-lord."),
  ("npc6_signup_response_1", "Very well. I hope you won't run away from the first orc we see."),
  ("npc7_signup_response_1", "Very well, Master Dwarf, you are welcome to join us."),
  ("npc8_signup_response_1", "You will be safe with us, I promise. We will be leaving shortly."),
  ("npc9_signup_response_1", "Very good. Do as you are told, and I'll feed you well."),
  ("npc10_signup_response_1", "Very well. Let's go."),
  ("npc11_signup_response_1", "Very well. Let's go."),
  ("npc12_signup_response_1", "I_reckon_we_could_put_you_to_good_use."),
  ("npc13_signup_response_1", "I_reckon_we_could_put_you_to_good_use."),
  ("npc14_signup_response_1", "Very well. Let's go."),
  ("npc15_signup_response_1", "Hmmm. I admire your... confidence. Get your gear together."),
  ("npc16_signup_response_1", "How about following me?"),
  ("npc17_signup_response_1", "Great! I hope you won't talk of trees all the time though."),

#11
  ("npc1_signup_response_2", "I have no need of your company at the moment, good luck to you."),
  ("npc2_signup_response_2", "Sorry, I've changed my mind."),
  ("npc3_signup_response_2", "Sorry, I've changed my mind - maybe next time."),
  ("npc4_signup_response_2", "I apologize, my Lady, perhaps another time."),
  ("npc5_signup_response_2", "On second thought, maybe we need to help Lothlórien on our own."),
  ("npc6_signup_response_2", "Sorry, I just can't imagine you on a battlefield."),
  ("npc7_signup_response_2", "Sorry, I happen to like Elves."),
  ("npc8_signup_response_2", "I'm sorry, everyone fights in my company."),
  ("npc9_signup_response_2", "I've changed my mind. Whoever is looking for you might come for me next."),
  ("npc10_signup_response_2", "I've changed my mind."),
  ("npc11_signup_response_2", "I don't need you, slave."),
  ("npc12_signup_response_2", "I've changed my mind."),
  ("npc13_signup_response_2", "I've changed my mind."),
  ("npc14_signup_response_2", "I've changed my mind."),
  ("npc15_signup_response_2", "Actually, I think I'll look for a real healer and not a braggart."),
  ("npc16_signup_response_2", "I've had enough of this."),
  ("npc17_signup_response_2", "On the other hand, I think I've changed my mind. You're a bit of a nut, aren't you?"),

  ("npc1_payment", "I would join you, but my Captain Faramir would miss my presence here." + costs_reg14_inf_with_s14),
  ("npc2_payment", "The guard Sergeant would not let me go, I'm afraid." + costs_reg14_inf_with_s14),
  ("npc3_payment", "Ahem, it seems that I have ran up quite a tab in the fine tavern here, so I'll need to settle my account before I can leave." + costs_reg14_inf_with_s14),
  ("npc4_payment", "I would join you, but who will care for the wounded if the city is attacked?" + costs_reg14_inf_with_s14),
  ("npc5_payment", "We should be off soon. The value of my coming will be diminished if the Enemy senses my presence before we have struck. But Lothlórien also needs me here." + costs_reg14_inf_with_s14),
  ("npc6_payment", "I would join you, but my duty is here." + costs_reg14_inf_with_s14),
  ("npc7_payment", "I would join you, but I'm afraid my honorable father Dwalin will not understand why I left the town in a time of need." + costs_reg14_inf_with_s14),
  ("npc8_payment", "I cannot abandon my duties here, my King still needs me. I'm too concerned for his health." + costs_reg14_inf_with_s14),
  ("npc9_payment", "I want to leave with you, but the guards at the gate won't let me.^Trust me, I've tried." + costs_reg14_inf_with_s14),
  ("npc10_payment", "I would join you, but my duty is here." + costs_reg14_inf_with_s14),
  ("npc11_payment", "I just need someone to do in the Boss. We could wait till he closes his eyes to lop off, but I reckon someone really high up can force his eyes shut. Ai!" + costs_reg14_inf_with_s14),
  ("npc12_payment", "Hai! Yoi! I'll need to remind the boys to keep their mangy gobs shut or the High Ups will get my number and 'ave it out for me, they will." + costs_reg14_inf_with_s14),
  ("npc13_payment", "Alas the Chieftains here will not to allow my leave. Are you able to convince them otherwise?" + costs_reg14_inf_with_s14),
  ("npc14_payment", "The captain of the Haven will require much persuasion for my leave. Convince him and we shall set sail through this storm." + costs_reg14_inf_with_s14),
  ("npc15_payment", "Ah, yes. Noble Warrior-Lord! One small impediment is there! A great injustice befell me, that the master of this cave did not like my offer of healing, and has stolen all my gear! The cheek! To steal from the Great Bolzog! Master, I can't recover my priceless equipment from his filthy claws!" + costs_reg14_inf_with_s14),
  ("npc16_payment", "I will not follow you, I will go my own path; but your path may go along with mine for a while. Though, before I travel these lands I must first pay tribute to those who died trying before us. Show them your tribute and we may make our leave. We must never forget our ancestors. They have not forgotten us." + costs_reg14_inf_with_s14),
  ("npc17_payment", "I like trees, but my old uncle needs me here." + costs_reg14_inf_with_s14),

  ("npc1_payment_response", "Don't worry, I'll arrange your leave with him." + spend_reg14_inf_on_reg15),
  ("npc2_payment_response", "Don't worry, I'll talk with your Sergeant." + spend_reg14_inf_on_reg15 ),
  ("npc3_payment_response", "This better be worth it. I'll settle with the barkeep."+spend_reg14_inf_on_reg15),
  ("npc4_payment_response", "It's a noble cause, but I'm sure a replacement can be found."+spend_reg14_inf_on_reg15),
  ("npc5_payment_response", "Trust me, you will be more useful with me."+spend_reg14_inf_on_reg15),
  ("npc6_payment_response", "From now on, your duty is with me."+spend_reg14_inf_on_reg15),
  ("npc7_payment_response", "Master Dwalin will understand that a battle-worthy dwarf should not be kept from our enemies for too long."+spend_reg14_inf_on_reg15),
  ("npc8_payment_response", "The King's well-being is important, but you will save more lives with me."+spend_reg14_inf_on_reg15),
  ("npc9_payment_response", "Oh, but the guard won't dare stop you, if you are with me."+spend_reg14_inf_on_reg15),
  ("npc10_payment_response", "From now on, your duty is with me."+spend_reg14_inf_on_reg15),
  ("npc11_payment_response", "Never mind your Boss, you serve me now."+spend_reg14_inf_on_reg15),
  ("npc12_payment_response", "Your boys will get new orders, I'll worry about the High Ups."+spend_reg14_inf_on_reg15),
  ("npc13_payment_response", "They will see otherwise, for I'm your Chieftain now."+spend_reg14_inf_on_reg15),
  ("npc14_payment_response", "You don't need to worry about the old Harbor-master."+spend_reg14_inf_on_reg15),
  ("npc15_payment_response", "Priceless, is it? I'll get your gear."+spend_reg14_inf_on_reg15),
  ("npc16_payment_response", "I honor the ancestors, yours and mine."+spend_reg14_inf_on_reg15),
  ("npc17_payment_response", "Your uncle will be fine. You are with me now."+spend_reg14_inf_on_reg15),



  ("npc1_morality_speech", "Captain, I can't understand how you can {s21} and forsake our men. Captain Faramir would have never lost sight of compassion for his Rangers and caused them to suffer without need."),
  ("npc2_morality_speech", "I hope you don't mind my saying so, but it's a bit hard for me to see us {s21}. Maybe I ought to try to be more of a hardened soldier, but if you could try to be more... caring about our soldiers, I'd sleep better."),
  ("npc3_morality_speech", "Commander, we Eorlingas never {s21}. Our horses don't tire easily and, once we regroup, there is no situation a well-timed charge can't decide in our favour. Take heed the next time we battle against the odds."),
  ("npc4_morality_speech", "Take no heed to what the soldiers say, sometimes to {s21} is the wisest course of action. I for one appreciate the lives spared and limbs unbroken, if for nothing else but to fight another day, when fate looks upon us with favor."),
  ("npc5_morality_speech", "You must reconsider your actions, commander. To {s21} makes us no more honourable than the Enemy and diminishes the confidence of our friends."),
  ("npc6_morality_speech", "[No primary moral code]"),
  ("npc7_morality_speech", "I was not pleased that you decided to {s21}. To fall in battle is an honour for any right-thinking dwarf, but to fight in a company led by a coward is a disgrace. What will my cousins say if they learn of this?"),
  ("npc8_morality_speech", "Commander, I must object. To {s21} is harsh on the men and unnecessary. I do what I can to ease their suffering, but please don't make another costly mistake."),
  ("npc9_morality_speech", "The fighting Uruk-hai don't {s21}. If the Master has little guts, he might find himself without them one night. Gulm has spoken."), #run from battle
  ("npc10_morality_speech", "[No primary moral code]"),
  ("npc11_morality_speech", "[No primary moral code]"),
  ("npc12_morality_speech", "[No primary moral code]"),
  ("npc13_morality_speech", "[No primary moral code]"),
  ("npc14_morality_speech", "[No primary moral code]"),
  ("npc15_morality_speech", "You may think that Bolzog the Great can cure all, {playername}, but even I have my limits! If you continue to {s21} even my talent will struggle! You must give me some support! I cannot resurrect the dead, whether they starve or are hacked to pieces!"),
  ("npc16_morality_speech", "[No primary moral code]"),
  ("npc17_morality_speech", "[No primary moral code]"),


  ("npc1_2ary_morality_speech", "Captain, I have been raised as a Dúnadan, both in valor and honour. I would prefer if we don't {s21}."),
  ("npc2_2ary_morality_speech", "[No secondary moral code]"),
  ("npc3_2ary_morality_speech", "[No secondary moral code]"),
  ("npc4_2ary_morality_speech", "Your pardon, commander. Women of my station will accept death but not dishonour. To {s21} brings shame to my house and ancestors."),
  ("npc5_2ary_morality_speech", "[No secondary moral code]"),
  ("npc6_2ary_morality_speech", "[No secondary moral code]"),
  ("npc7_2ary_morality_speech", "[No secondary moral code]"),
  ("npc8_2ary_morality_speech", "[No secondary moral code]"),
  ("npc9_2ary_morality_speech", "[No secondary moral code]"),
  ("npc10_2ary_morality_speech", "[No secondary moral code]"),
  ("npc11_2ary_morality_speech", "[No secondary moral code]"),
  ("npc12_2ary_morality_speech", "[No secondary moral code]"),
  ("npc13_2ary_morality_speech", "[No secondary moral code]"),
  ("npc14_2ary_morality_speech", "[No secondary moral code]"),
  ("npc15_2ary_morality_speech", "Hi-hi-hi! You are cunning, Oh Lord! You take the gold, and nod, and say 'yes master' but all the time you planned this! Hi-Hi! Only, we must be careful, that The Big One does not see you deceiving him..."),
  ("npc16_2ary_morality_speech", "[No secondary moral code]"),
  ("npc17_2ary_morality_speech", "[No secondary moral code]"),

  ("npc1_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc2_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc3_personalityclash_speech", "Commander, how come we ended up with {s11} in our company? He's nimble enough on foot, I reckon, but he talks of ambushes too often for my liking - not unlike the cautious nature of his people."),
  ("npc4_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc5_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc6_personalityclash_speech", "{playername}, I just saw {s11} walk brazenly over a nest of young birds. His clumsiness destroyed the young lives of innocent creatures."),
  ("npc7_personalityclash_speech", "Lord {s11} does well in a battle, but I wonder if he blinds the enemy by the shine of his hair? Or they fall in awe of his fame and uppity demeanor?"),
  ("npc8_personalityclash_speech", "Commander, I must lodge a complaint against {s11}. He continues to pester me about making him a certain brew called 'the green fairy'."), 
  ("npc9_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc10_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc11_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc12_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc13_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc14_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc15_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc16_personalityclash_speech", "Did I mention I hate {s11}?"),
  ("npc17_personalityclash_speech", "Did I mention I hate {s11}?"),

  ("npc1_personalityclash_speech_b", "I hate {s11}."),
  ("npc2_personalityclash_speech_b", "I hate {s11}."),
  ("npc3_personalityclash_speech_b", "I don't have a quarrel with the people of Gondor, but we would do better with more bold horsemen and less reluctant ground-huggers, if you catch my drift."),
  ("npc4_personalityclash_speech_b", "I hate {s11}."),
  ("npc5_personalityclash_speech_b", "I hate {s11}."),
  ("npc6_personalityclash_speech_b", "His dwarven ways may serve him well underground, albeit it's a wonder he hasn't fallen down an ugly shaft. Maybe he should have."),
  ("npc7_personalityclash_speech_b", "We would do better with a dwarven hero, someone like Durin the Deathless of old, and let the Elves prance around their forests."),
  ("npc8_personalityclash_speech_b", "It is made from wormwood soaked in liquor and apparently favored by minstrels and vagrants for seeing things that are not there. I doubt you'll approve of your soldiers chasing air on the battlefield, as much as it may be amusing to watch."),
  ("npc9_personalityclash_speech_b", "I hate {s11}."),
  ("npc10_personalityclash_speech_b", "I hate {s11}."),
  ("npc11_personalityclash_speech_b", "I hate {s11}."),
  ("npc12_personalityclash_speech_b", "I hate {s11}."),
  ("npc13_personalityclash_speech_b", "I hate {s11}."),
  ("npc14_personalityclash_speech_b", "I hate {s11}."),
  ("npc15_personalityclash_speech_b", "I hate {s11}."),
  ("npc16_personalityclash_speech_b", "I hate {s11}."),
  ("npc17_personalityclash_speech_b", "I hate {s11}."),

 
### set off by behavior after victorious battle
  ("npc1_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc2_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc3_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc4_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc5_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc6_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc7_personalityclash2_speech", "A nice little scrap, eh captain? If only slightly ruined by the conduct of that Elf-woman {s11}."), 
  ("npc8_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc9_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc10_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc11_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc12_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc13_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc14_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc15_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc16_personalityclash2_speech", "Did I mention I hate {s11}?"),
  ("npc17_personalityclash2_speech", "Did I mention I hate {s11}?"),
   
  ("npc1_personalityclash2_speech_b", "I hate {s11}."), 
  ("npc2_personalityclash2_speech_b", "I hate {s11}."),
  ("npc3_personalityclash2_speech_b", "I hate {s11}."),
  ("npc4_personalityclash2_speech_b", "I hate {s11}."),
  ("npc5_personalityclash2_speech_b", "I hate {s11}."),
  ("npc6_personalityclash2_speech_b", "I hate {s11}."),
  ("npc7_personalityclash2_speech_b", "I saw her cowering in the rear, barely releasing an arrow or two in the general direction of the enemy. I say let her go to take care of the birds and bees, so we can go on with the bloody work of slaying the enemy."),
  ("npc8_personalityclash2_speech_b", "I hate {s11}."),
  ("npc9_personalityclash2_speech_b", "I hate {s11}."),
  ("npc10_personalityclash2_speech_b", "I hate {s11}."), 
  ("npc11_personalityclash2_speech_b", "I hate {s11}."),
  ("npc12_personalityclash2_speech_b", "I hate {s11}."),
  ("npc13_personalityclash2_speech_b", "I hate {s11}."),
  ("npc14_personalityclash2_speech_b", "I hate {s11}."),
  ("npc15_personalityclash2_speech_b", "I hate {s11}."),
  ("npc16_personalityclash2_speech_b", "I hate {s11}."),
  ("npc17_personalityclash2_speech_b", "I hate {s11}."),


  ("npc1_personalitymatch_speech", "Have you noticed the grace of {s11} in that last battle? The way she moves around the enemy just before striking the final blow? It's like the stories of old, when elven maidens displayed as much poise on the battlefield as in their beautiful forest courts."),
  ("npc2_personalitymatch_speech", "Excuse me, commander. I was just helping {s11} with minor weapon repairs after that last scrap, and he even promised to teach me how to improve my strikes."),
  ("npc3_personalitymatch_speech", "Is not a Rohan shieldmaiden in full charge a sight to behold? Granted, our womenfolk are better off by the hearth, but after seeing {s11} strike down the enemy in that last battle, I'm beginning to have doubts."),
  ("npc4_personalitymatch_speech", "A battle of great deeds, commander, and my congratulations on the victory. I noticed how {s11} quietly and surely took care of the wounded and ailing, even as the last of the enemy got what they deserved."),
  ("npc5_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc6_personalitymatch_speech", "{playername}, as much as I hate battles, I can't help but notice my Lord {s11} riding out in full splendor and bearing down on the ugly creatures like a hawk."),
  ("npc7_personalitymatch_speech", "Bloody and victorious, just as I like it! I did, however, sustain a flesh wound that {s11} was kind enough to bandage promptly."),
  ("npc8_personalitymatch_speech", "Another victory for you, commander, and I admire your skill in sparing the lives of our men. Warriors like {s11} seem to be of great use in your battle plans."),
  ("npc9_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc10_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc11_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc12_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc13_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc14_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc15_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc16_personalitymatch_speech", "Did I mention I like {s11}?"),
  ("npc17_personalitymatch_speech", "Umm, chief. I think {s11} could make it well in the woods. Can tell an ash from a willow."),
   
  ("npc1_personalitymatch_speech_b", "I find the company of {s11} very pleasing and her native woodcraft a rare glimpse of what remains of Sindarin skills in the world. You know, my father named me after the legendary Sindarin Elf captain serving King Thingol of Doriath and I always feel a special bond to the fair race."),
  ("npc2_personalitymatch_speech_b", "My folks at home always told me stories about the Ithilien Rangers and now I can see for myself they are all true. If they are all like {s11}, I feel Gondor is safer for it."),
  ("npc3_personalitymatch_speech_b", "Commander, as a personal favour, might I ask if you can order {s11} to stay more to the rear in the next battle? I could not stand to see her harmed, and it's not the ale talking."),
  ("npc4_personalitymatch_speech_b", "To preserve lives is the noblest deed, and I feel kinship with that kind soul, even if our worlds are far apart."),
  ("npc5_personalitymatch_speech_b", "I like {s11}."),
  ("npc6_personalitymatch_speech_b", "I wonder just how old is he. Maybe a dozen of centuries older than me? Never mind, you wouldn't understand."),
  ("npc7_personalitymatch_speech_b", "{s11} and her Dale-kin, even if not quite up to dwarven warrior standards, have proven to be steadfast allies in this War. A good choice for a friend and companion among Men, if I may say so."),
  ("npc8_personalitymatch_speech_b", "The people of Dale have a deep regard for the hardy Lonely Mountain Dwarven-folk, as friends and protectors despite our different race and customs."),
  ("npc9_personalitymatch_speech_b", "I like {s11}."),
  ("npc10_personalitymatch_speech_b", "I like {s11}."),
  ("npc11_personalitymatch_speech_b", "I like {s11}."),
  ("npc12_personalitymatch_speech_b", "I like {s11}."),
  ("npc13_personalitymatch_speech_b", "I like {s11}."),
  ("npc14_personalitymatch_speech_b", "I like {s11}."),
  ("npc15_personalitymatch_speech_b", "I like {s11}."),
  ("npc16_personalitymatch_speech_b", "I like {s11}."),
  ("npc17_personalitymatch_speech_b", "My people get along well with the Woodelves. They like trees too. I like trees too. We all like trees."),

#these are not used  
  ("npc1_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc2_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc3_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc4_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc5_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc6_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc7_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc8_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc9_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc10_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc11_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc12_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc13_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc14_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc15_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc16_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
  ("npc17_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),

  ("npc1_rehire_speech", "It is good to see you again, Captain. Shall I join you once more?"),
  ("npc2_rehire_speech", "Happy days! Commander, can I please join you again?"),
  ("npc3_rehire_speech", "Ho! Shall we ride again together?"),
  ("npc4_rehire_speech", "Welcome again. Shall we continue where we left off?"),
  ("npc5_rehire_speech", "It's good to see you, {playername}. Let us travel together again."),
  ("npc6_rehire_speech", "It's good to see you, {playername}. Let us walk the same path again."),
  ("npc7_rehire_speech", "My axe is ready, {playername}. Shall I rejoin you?"),
  ("npc8_rehire_speech", "You are a welcome sight. Shall I join you once again?"),
  ("npc9_rehire_speech", "Gulm is ready to kill for you again. Are we going?"),
  ("npc10_rehire_speech", "Can I serve you once again?"),
  ("npc11_rehire_speech", "Can I serve you once again?"),
  ("npc12_rehire_speech", "Can I serve you once again?"),
  ("npc13_rehire_speech", "Can I serve you once again?"),
  ("npc14_rehire_speech", "Can I serve you once again?"),
  ("npc15_rehire_speech", "Aah, Great Lord! I have searched so long for you, as word of your glorious deeds rings across Middle Earth! Surely you have missed my skills? You will welcome me once more to complete your Great Army?"),
  ("npc16_rehire_speech", "Can I serve you once again?"),
  ("npc17_rehire_speech", "Hey. Time to move on again? Trees don't move much. But I like to move. But I like trees too."),

#local color strings
  ("npc1_home_intro", "Captain, we are approaching Osgiliath now, so let us be on the lookout for friend and foe alike."),
  ("npc2_home_intro", "Be vigilant, commander, that must be Minas Morgul over there. Do you feel that something is watching us?"),
  ("npc3_home_intro", "A word of advice, commander. We are getting mighty close to Entwood now and the horses are getting restless. Some call the forest Fangorn, too."),
  ("npc4_home_intro", "Let's stop here for a minute, commander. Ahead of us, between the Anduin and the Limlight, lies the Field of Celebrant, where Eorl the Young rode to the aid of our Gondor allies."),
  ("npc5_home_intro", "Daro! That's Angrenost and the black tower of Orthanc ahead. Much has changed since I last saw them, and none for the better."),
  ("npc6_home_intro", "Excuse me, {playername}. The paths in this part become more twisted and some lead to dead-ends. We must be approaching Dol Guldur."),
  ("npc7_home_intro", "Oy, captain! This must be the old path to the Eastern Gates of Khazad-dûm, or Moria as you may prefer. You can see in the distance the glittering lake of Kheled-zâram, and, through the clouds, the three peaks known to grace this part of the Misty Mountains."),
  ("npc8_home_intro", "Oh, a curious sight! I heard stories about this place where sturdy woodmen are said to live in harmony with animals and plants. Beornings they are called, I gather."),
  ("npc9_home_intro", "Curses! That must be Hornburg over there, master."),
  ("npc10_home_intro", "Hey, look!"),
  ("npc11_home_intro", "Hey, look!"),
  ("npc12_home_intro", "Hey, look!"),
  ("npc13_home_intro", "Hey, look!"),
  ("npc14_home_intro", "Hey, look!"),
  ("npc15_home_intro", "Hey, look!"),
  ("npc16_home_intro", "Hey, look!"),
  ("npc17_home_intro", "Ooooo, mallorns grow here! One should never cut down a mallorn, they're just too beautiful!"),


  ("npc1_home_description", "It was a fair city once, the capital of Gondor of old, full of people and laughter. Now it lies deserted and ruined, the old Anduin flowing wearily through a ghost town."),
  ("npc2_home_description", "It was called Minas Ithil many years ago, and stories are told of how moonlight filled its inner courts with silver light and its walls gleamed silver and white. Gondor watchmen peered over the walls to the east and kept watch beyond Ephel Dúath."),
  ("npc3_home_description", "It's thick with trunks and branches and all manner of trees, and I wouldn't venture there as strange creatures roam the forest, not all of them harmless."),
  ("npc4_home_description", "'Where now the horse and the rider? where is the horn that was blowing?^Where is the helm and the hauberk and the bright hair flowing?...^They have passed like rain on the mountain, like a wind in the meadow;^The days have gone down in the West behind the hills into shadow...'"),
  ("npc5_home_description", "Once built by the Southern Kingdom, now home to one that we called the White Wizard, scheming, no doubt, how to increase his power further at the expense of others."),
  ("npc6_home_description", "I have never ventured this far, but I overheard our Greenwood scouts say there may be Nazgul here. I feel an evil presence, but I cannot put a name to it. It is powerful, though, so let us be prepared."),
  ("npc7_home_description", "Judging by the desolation, and the many orc-tracks, I fear for the fate of the courageous Balin and his expedition. It seems that Moria has fallen to the Shadow and we should tread carefully."),
  ("npc8_home_description", "Not too often, a travelling merchant comes to the Dale market and offers the finest honey I have ever tasted. For some curious reason, he says that 'it was made by bears' and laughs."),
  ("npc9_home_description", "Its damned walls are too high and too hard for my hammer to break. I reckon if we ever chase away the manlings from their Edoras pig-sties, they'll run off here and cower behind the walls."),
  ("npc10_home_description", "Do you know that town?"),
  ("npc11_home_description", "Do you know that town?"),
  ("npc12_home_description", "Do you know that town?"),
  ("npc13_home_description", "Do you know that town?"),
  ("npc14_home_description", "Do you know that town?"),
  ("npc15_home_description", "Do you know that town?"),
  ("npc16_home_description", "Do you know that town?"),
  ("npc17_home_description", "I didn't know there were such lovely woods here too. I wonder if any woodsmen work here."),

  ("npc1_home_description_2", "If Gondor is doomed, West Osgiliath shall fall first to the foul hordes of the Eye. I only hope Captain Faramir would be in command that day and stem the tide. If we could spare any men to bolster the defences here, I would be most grateful, Captain."),
  ("npc2_home_description_2", "It is said it's full of terrible orcs now and dread spirits and worse. I pray for the day when Gondor will reclaim it and cleanse it of all things foul."),
  ("npc3_home_description_2", "If we must cross Entwood, let us do so with haste and stealth. I don't know who might be listening to our hooves and I don't care to find out."),
  ("npc4_home_description_2", "We would do well to remember the great deeds of the past and the sacrifices that were made. The Alliance between Rohan and Gondor shall save our peoples from doom once again."),
  ("npc5_home_description_2", "Let it be a reminder that even the greatest, even one of the Istari, can be corrupted and fall. Those who lust for power can be defeated by power, so let us not tarry much longer."),
  ("npc6_home_description_2", "I sense the evil armies behind its walls prepare to march... To fair Lothlórien? To Dale? To my Greenwood homeland? I cannot tell, but please do everything you can to thwart them."),
  ("npc7_home_description_2", "If the fortunes of war ever provide us with a large army, we should risk the entrance to the Mines and retrieve their mighty riches."),
  ("npc8_home_description_2", "I can smell the fragrance of many sweet flowers and see the bees harvesting their nectar. If you don't mind, I will gather some herbs for our own use, it will only take a moment."),
  ("npc9_home_description_2", "There's no use trudging around here if we are not backed by a large Uruk-hai horde. Unless you want to make faces at the lookouts on the wall, that is."),
  ("npc10_home_description_2", "Minas Morgul, where Nazgul drink all day, har-har!"),
  ("npc11_home_description_2", "Doesn't Orthanc look like a giant... something?"),
  ("npc12_home_description_2", "Doesn't Orthanc look like a giant... something?"),
  ("npc13_home_description_2", "Minas Morgul, where Nazgul drink all day, har-har!"),
  ("npc14_home_description_2", "Minas Morgul, where Nazgul drink all day, har-har!"),
  ("npc15_home_description_2", "Minas Morgul, where Nazgul drink all day, har-har!"),
  ("npc16_home_description_2", "Minas Morgul, where Nazgul drink all day, har-har!"),
  ("npc17_home_description_2", "I could chisel you a nice pipe. Would you like a pipe?"),

  ("npc1_home_recap", "I was born and raised in Ithilien, in a long line of warriors tracing back to the Southern Dúnedain."),
  ("npc2_home_recap", "I was born in Minas Tirith, in a humble, but proud family."),
  ("npc3_home_recap", "I am one of the Eorlingas, or Rohirrim, as foreigners call us."),
  ("npc4_home_recap", "I don't find it amusing that you should forget so easily."),
  ("npc5_home_recap", "I'll indulge your curiosity, but let us not tarry."),
  ("npc6_home_recap", "I was born and raised in Mirkwood, a Silvan Elf. Our race's woodcraft skills are known to all."),
  ("npc7_home_recap", "I am son of Dwalin of the Durin's folk."),
  ("npc8_home_recap", "I am a healer and a herbalist from Dale."),
  ("npc9_home_recap", "Gulm will tell you if you must know. But talk doesn't make enemies dead."),
  ("npc10_home_recap", "I'll make this short."),
  ("npc11_home_recap", "I'll make this short."),
  ("npc12_home_recap", "I'll make this short."),
  ("npc13_home_recap", "I'll make this short."),
  ("npc14_home_recap", "I'll make this short."),
  ("npc15_home_recap", "I'll make this short."),
  ("npc16_home_recap", "I'll make this short."),
  ("npc17_home_recap", "I was born at the edge of the woods, but spent all my life in the woods. Did I tell you of the many trees there?"),

  ("npc1_honorific", "Captain"),
  ("npc2_honorific", "commander"),
  ("npc3_honorific", "commander"),
  ("npc4_honorific", "commander"),
  ("npc5_honorific", "commander"),
  ("npc6_honorific", "warrior"),
  ("npc7_honorific", "captain"),
  ("npc8_honorific", "commander"),
  ("npc9_honorific", "Master"),
  ("npc10_honorific", "Master"),
  ("npc11_honorific", "Master"),
  ("npc12_honorific", "Master"),
  ("npc13_honorific", "Chieftain"),
  ("npc14_honorific", "Captain"),
  ("npc15_honorific", "Master"),
  ("npc16_honorific", "Chieftain"),
  ("npc17_honorific", "Chief"),

  ("companion_strings_end", "INVALID"),


#NPC companion changes end

#Troop Commentaries begin
#Tags for comments are = allied/enemy, friendly/unfriendly, and then those related to specific reputations
#Also, there are four other tags which refer to groups of two or more reputations (spiteful, benevolent, chivalrous, and coldblooded)
#The game will select the first comment in each block which meets all the tag requirements

#Beginning of game comments

("comment_intro_liege_affiliated", "Unused"),

("comment_intro_famous_liege", "Unused"),
("comment_intro_famous_martial", "Unused"),
("comment_intro_famous_badtempered", "Unused"),
("comment_intro_famous_pitiless", "Unused"),
("comment_intro_famous_cunning", "Unused"),
("comment_intro_famous_sadistic", "Unused"),
("comment_intro_famous_goodnatured", "Unused"),
("comment_intro_famous_upstanding", "Unused"),

("comment_intro_noble_liege", "Unused"),
("comment_intro_noble_martial", "Unused"),
("comment_intro_noble_badtempered", "Unused"),
("comment_intro_noble_pitiless", "Unused"),
("comment_intro_noble_cunning", "Unused"),
("comment_intro_noble_sadistic", "Unused"),
("comment_intro_noble_goodnatured", "Unused"),
("comment_intro_noble_upstanding", "Unused"),

("comment_intro_common_liege", "Unused"),
("comment_intro_common_martial", "Unused"),
("comment_intro_common_badtempered", "Unused"),
("comment_intro_common_pitiless", "Unused"),
("comment_intro_common_cunning", "Unused"),
("comment_intro_common_sadistic", "Unused"),
("comment_intro_common_goodnatured", "Unused"),
("comment_intro_common_upstanding", "Unused"),


#Actions vis-a-vis civilians
  ("comment_you_raided_my_village_enemy_benevolent",    "Unused"), 
  ("comment_you_raided_my_village_enemy_spiteful",      "Unused"), 
  ("comment_you_raided_my_village_enemy_coldblooded",   "Unused"), 
  ("comment_you_raided_my_village_enemy",              "Unused"), 
  ("comment_you_raided_my_village_unfriendly_spiteful", "Unused"), 
  ("comment_you_raided_my_village_friendly",            "Unused"), 
  ("comment_you_raided_my_village_default",             "Unused"), 

  ("comment_you_robbed_my_village_enemy_coldblooded", "Unused"), 
  ("comment_you_robbed_my_village_enemy",             "Unused"), 
  ("comment_you_robbed_my_village_friendly_spiteful", "Unused"), 
  ("comment_you_robbed_my_village_friendly",          "Unused"), 
  ("comment_you_robbed_my_village_default",          "Unused"), 

  ("comment_you_accosted_my_caravan_enemy",          "Unused"), 
  ("comment_you_accosted_my_caravan_default",        "Unused"), 

  ("comment_you_helped_villagers_benevolent",                "Unused"), 
  ("comment_you_helped_villagers_friendly_cruel",            "Unused"), 
  ("comment_you_helped_villagers_friendly",                  "Unused"), 
  ("comment_you_helped_villagers_unfriendly_spiteful",       "Unused"), 
  ("comment_you_helped_villagers_cruel",                     "Unused"), 
  ("comment_you_helped_villagers_default",                   "Unused"), 


#Combat-related events


  ("comment_you_captured_a_castle_allied_friendly",            "I heard that you have besieged and taken {s51}. That was a great dead, and I am proud to call you my friend!"), 
  ("comment_you_captured_a_castle_allied_spiteful",            "I heard that you have besieged and taken {s51}. Good work! Soon, we will have all their fortresses to despoil, their treasuries to ransack, their grieving widows to serve us our wine."), 
  ("comment_you_captured_a_castle_allied_unfriendly_spiteful", "I heard that you have besieged and taken {s51}. Well, every dog has his day, or so they say. Enjoy it while you can, until your betters kick you back out in the cold where you belong."), 
  ("comment_you_captured_a_castle_allied_unfriendly",          "I heard that you have besieged and taken {s51}. Whatever our differences in the past, I must offer you my congratulations."), 
  ("comment_you_captured_a_castle_allied",                     "I heard that you have besieged and taken {s51}. We have them on the run!"), 

  ("comment_you_captured_my_castle_enemy_spiteful",            "Unused"), 
  ("comment_you_captured_my_castle_enemy_chivalrous",         "Unused"), 
  ("comment_you_captured_my_castle_enemy",                     "Unused"), 

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

  ("comment_you_captured_a_lord_allied_friendly_spiteful",   "Unused"), 
  ("comment_you_captured_a_lord_allied_unfriendly_spiteful", "Unused"), 
  ("comment_you_captured_a_lord_allied_chivalrous",          "Unused"), 
  ("comment_you_captured_a_lord_allied",                     "Unused"), 

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
  ("comment_pledged_allegiance_allied_martial_unfriendly",             "Unused"), 
  ("comment_pledged_allegiance_allied_martial",                        "Unused"), 
  ("comment_pledged_allegiance_allied_quarrelsome_unfriendly",         "Unused"), 
  ("comment_pledged_allegiance_allied_quarrelsome",                    "Unused"), 
  ("comment_pledged_allegiance_allied_selfrighteous_unfriendly",       "Unused"), 
  ("comment_pledged_allegiance_allied_selfrighteous",                  "Unused"), 
  ("comment_pledged_allegiance_allied_cunning_unfriendly",             "Unused"), 
  ("comment_pledged_allegiance_allied_cunning",                        "Unused"), 
  ("comment_pledged_allegiance_allied_debauched_unfriendly",           "Unused"), 
  ("comment_pledged_allegiance_allied_debauched",                      "Unused"), 
  ("comment_pledged_allegiance_allied_goodnatured_unfriendly",         "Unused"), 
  ("comment_pledged_allegiance_allied_goodnatured",                    "Unused"), 
  ("comment_pledged_allegiance_allied_upstanding_unfriendly",          "Unused"), 
  ("comment_pledged_allegiance_allied_upstanding",                     "Unused"), 


  ("comment_our_king_granted_you_a_fief_allied_friendly_cruel",     "Unused"), 
  ("comment_our_king_granted_you_a_fief_allied_friendly_cynical",   "Unused"), 

  ("comment_our_king_granted_you_a_fief_allied_friendly",              "Unused"), 
  ("comment_our_king_granted_you_a_fief_allied_unfriendly_upstanding", "Unused"), 
  ("comment_our_king_granted_you_a_fief_allied_unfriendly_spiteful",   "Unused"), 
  ("comment_our_king_granted_you_a_fief_allied_spiteful",             "Unused"), 

  ("comment_our_king_granted_you_a_fief_allied",                       "Unused"), 

  ("comment_you_renounced_your_alliegance_enemy_friendly",             "Unused"), 
  ("comment_you_renounced_your_alliegance_friendly",                  "Unused"), 
  ("comment_you_renounced_your_alliegance_unfriendly_spiteful",        "Unused"), 
  ("comment_you_renounced_your_alliegance_unfriendly_moralizing",      "Unused"), 
  ("comment_you_renounced_your_alliegance_enemy",                      "Unused"), 
  ("comment_you_renounced_your_alliegance_default",                    "Unused"), 


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
 ("faction_strength_fair"              , "fair"),
 ("faction_strength_average"           , "average"),
 ("faction_strength_strong"            , "strong"),
 ("faction_strength_quite strong"      , "quite strong"),
 ("faction_strength_very strong"       , "very strong"),
 ("faction_strength_unmatched"         , "unmatched"),
 ("faction_strength_last"       , "INVALID"),

# TLD theater names
 ("theater_SE", "Gondor"),
 ("theater_SW", "Rohan"),
 ("theater_C", "South Rhovanion"),
 ("theater_N", "North Rhovanion"), 

 ("faction_side_name",  "the Free People"),
 ("faction_side_name1", "the Naked Eye"),
 ("faction_side_name2", "the White Hand"),
 
# TLD party encounter greetings - depends on faction IDs staying in the same order
 ("party_greet_friend_gondor", "Hail, friend of the White Tree!"), 
 ("party_greet_enemy_gondor", "Draw your swords if you dare, enemies of Gondor!"), 
 ("party_greet_friend_dwarf", "Hail from the Durin's folk, dwarf-friend!"), 
 ("party_greet_enemy_dwarf", "Baruk Khazâd! Khazâd ai-mênu!"), 
 ("party_greet_friend_rohan", "Hail and well met, Rohirrim friend!"), 
 ("party_greet_enemy_rohan", "The Riders of Rohan are here to challenge you!"), 
 ("party_greet_friend_mordor", "Victory for the Eye!"), 
 ("party_greet_enemy_mordor", "Your heads will look nice on the gates of Morannon!"), 
 ("party_greet_friend_isengard", "Hail the White Hand!"), 
 ("party_greet_enemy_isengard", "The Wise Master shall be pleased when I show him your bodies!"), 
 ("party_greet_friend_lorien", "Hail, friend of fair Lorien!"), 
 ("party_greet_enemy_lorien", "Foul thing, we will put an end to your suffering!"), 
 ("party_greet_friend_imladris", "Hail, friend of Imladris and Elrond!"), 
 ("party_greet_enemy_imladris", "Today we make battle, enemies of Imladris and all that is fair!"), 
 ("party_greet_friend_woodelf", "Hail, friend of the Silvan Elves of Mirkwood!"), 
 ("party_greet_enemy_woodelf", "All who enter Mirkwood with malice shall never leave!"), 
 ("party_greet_friend_dale", "Hail, friend of proud Dale!"), 
 ("party_greet_enemy_dale", "Draw your swords, we are the Men of Dale!"), 
 ("party_greet_friend_harad", "Welcome, friend of the Haradrim!"), 
 ("party_greet_enemy_harad", "Your many bodies shall be ground into the sand!"), 
 ("party_greet_friend_rhun", "Greetings, friend of the Easterling tribes and Dorwinion!"), 
 ("party_greet_enemy_rhun", "Dwarves and Men are no match for our fierceness!"), 
 ("party_greet_friend_khand", "Jus jívati jyók, friend of the Variags! Your battle scars honour you."), 
 ("party_greet_enemy_khand", "Put on the masks of warriors, for today you shall meet your doom!"), 
 ("party_greet_friend_umbar", "Ni-yôzi zirbîth kiyad, friend of the Corsairs!"), 
 ("party_greet_enemy_umbar", "If we were at sea, you would dance on a plank soon enough!"), 
 ("party_greet_friend_moria", "Hail the White Hand!"), 
 ("party_greet_enemy_moria", "You shall have your throats cut by the orcs of Moria!"), 
 ("party_greet_friend_guldur", "Victory for the Eye!"), 
 ("party_greet_enemy_guldur", "The Elves and their friends shall fall under our blades!"), 
 ("party_greet_friend_gundabad", "Fear the power of Angmar!"), 
 ("party_greet_enemy_gundabad", "We shall descend on you and feast on your entrails!"), 
 ("party_greet_friend_dunland", "Hail, enemy of the horse-people!"), 
 ("party_greet_enemy_dunland", "Your homes will burn and your families shall be cut down!"), 
 ("party_greet_friend_beorn", "Hail, friend of Beorn!"), 
 ("party_greet_enemy_beorn", "You will taste the fury of the bear people!"), 



# #################################
# # TLD faction ranks
# #
     # ("tfr_name_strings_begin", "tfr_name_strings_begin"),
     # ]+concatenate_scripts([
        # concatenate_scripts([
                # [(tld_faction_ranks[fac][rnk][2][pos][0].lower().replace(" ", "_"), tld_faction_ranks[fac][rnk][2][pos][0]) for pos in range(len(tld_faction_ranks[fac][rnk][2]))
            # ] for rnk in range(len(tld_faction_ranks[fac]))
        # ]) for fac in range(len(tld_faction_ranks))
     # ])+[
    # ("promote", "You have been working well for the realm. Now you can be:"),
# #
# # TLD faction ranks end
# #################################

 ("subfaction_gondor_name_begin" , "Gondor"),
 
 ("subfaction_gondor_name1" , "Pelargir" ) ,
 ("subfaction_gondor_name2" , "Dol Amroth" ),
 ("subfaction_gondor_name3" , "Lamedon" ) ,
 ("subfaction_gondor_name4" , "Lossarnach" ),
 ("subfaction_gondor_name5" , "Pinnath Gelin" ),
 ("subfaction_gondor_name6" , "Blackroot Vale" ) ,
 ("subfaction_gondor_name7" , "Ithilien" ), 
 
#### TLD shop/bar rumors
("default_rumor", "The War. Everybody is talking about the war."),
#Rohan
#general idea=Enthusiastic about their horseplay and way of life, angry with Saruman.
("rohan_rumor_begin", "It breaks my heart to see my babies off to war! But without them the men would have to walk."),
("rohan_rumor_2", "I hear orcs eat horses. Foul beasts! They also eat prisoners. That is bad too, of course."),
("rohan_rumor_3", "There are no horses finer than Rohan's. Even the Elves get their horses from us!"),
("rohan_rumor_4", "If you can heal men, please treat my horses with just as much care should they be wounded."),
("rohan_rumor_5", "Bring me eight Sumpter Horses, he says... after the seven he asked for yesterday.  Makes you wonder."),
("rohan_rumor_6", "Gondor prefers sturdier horses. Our riders enjoy speed. The Elves get only the best. And our enemies steal them!"),
("rohan_rumor_7", "I've seen breeds of the desert mare and Variag horse. Rohan horses are clearly superiour but require a more experienced rider to handle."),
("rohan_rumor_8", "Wargs are slower than horses but can turn faster. They are also quite fragile compared to a well-bred warhorse."),
("rohan_rumor_9", "Armies march on Rohan with pikes and spears set against our fine horsemen. The traitor Saruman will cut down the whole Fangorn forest equipping his armies before this war is over."),
("rohan_rumor_10", "Being the best horsemen in the realm starts with raising the best horses."),
("rohan_rumor_11", "Most of the horses you see in Gondor came from us. They prefer a slightly stronger, slower horse that can carry their heavy armour."),
("rohan_rumor_12", "We say in Rohan that a horse is like a man. That if a horse is good it is like a man is good, and that if a horse is bad, is like a man is bad. And if a horse is hungry is like a man is hungry, and if a horse is sad is like if a man is sad. And we say if a horse is happy is like when a man is happy. We say if a horse is angry is like if man is angry. We say if a horse walk is like when a man walk, we say if a horse is old is like when a man is old, and we say if horse is young is like when a man is young. And the same we say if a horse is old is like when a man is old. And if a horse small, is like when a man's small."), #maybe we could do the whole endless Borat thing here, with player only being able to say "Yes" until the guy is finished. http://www.youtube.com/watch?v=i_KH28KuZ3I
("rohan_rumor_13", "Saruman's orcs are nasty but don't wear much protection. They're no match for a good axe."),
("rohan_rumor_14", "Our throwing axes and spears may seem bulky, but how many chances do you have to throw a missile before you ride down the foe? Make it count by throwing something with some heft."),
("rohan_rumor_15", "Hitting an orc with an arrow loosed from horseback looks difficult because it is, but the price of charging a rank of long pikes is higher."),
("rohan_rumor_16", "Gondor practices archery. We practice horse archery. Dunlendings practice neither."),
("rohan_rumor_17", "Many of Saruman's orcs are deadly archers. Many are not. A wise cavalry commander shouldn't wait to discover which is which."),
("rohan_rumor_18", "We are all friends here. Or should be; for the laughter of Mordor will be our only reward, if we quarrel."), #Gandalf quote
("rohan_rumor_19", "Long we have tended our beasts and our fields, built our houses, wrought our tools, or ridden away to help in the wars of Minas Tirith. And that we called the life of Men, the way of the world."), #Theoden quote
#Gondor
#general idea: Gloom, spread from depressive Denethor downwards gripping the hearts of Gondorians
("gondor_rumor_begin", "Gondor has no king and enemies are at the doorstep. The shadow grows in the east. Things do not look good."),
("gondor_rumor_2", "In Gondor there is nothing under the sun we don't make, build, or grow in some quantity. But for how much longer?"),
("gondor_rumor_3", "Mordor is a dry, infertile land. What do the creatures there eat? Surely not one another? Or maybe..."),
("gondor_rumor_4", "We toil our lands, as we have done for generations. Our past is glorious and brave, but our future looks uncertain."),
("gondor_rumor_5", "The Shadow's resources for war seem limitless, but they are borne on the backs of a vast pool of slave labour."),
("gondor_rumor_6", "We know of the elves in the north, but nowadays noone gets to see them anymore."),
("gondor_rumor_7", "I would see the White Tree in flower again in the courts of the kings, and the Silver Crown return, and Minas Tirith in peace: Minas Anor again as of old, full of light, high and fair, beautiful as a queen among other queens."), #Faramir quote
("gondor_rumor_8", "Why does Umbar keep invading us? Their Corsairs would have profited far more from trading with us. What plunder could match the riches they'd have hauled away selling old Numenorian artifacts to Gondorian nobles?"),
("gondor_rumor_9", "War must be, while we defend our lives against a destroyer who would devour all; but I do not love the bright sword for its sharpness, nor the arrow for its swiftness, nor the warrior for his glory. I love only that which they defend."), #Faramir quote
("gondor_rumor_10", "Gil-galad was an Elven-king. Of him the harpers sadly sing: the last whose realm was fair and free between the Mountains and the Sea."), #The Fall of Gil-galad poem
("gondor_rumor_11", "Dol Guldur? Never heard of it."),
("gondor_rumor_12", "Moria? The dwarves mine there, don't they?"),
("gondor_rumor_13", "Don't tell anyone I said this, but I think Prince Imrahil should perhaps become king. Lord Denethor is a noble man, but Gondor has faded much during his reign. And not only since his older son left."),
("gondor_rumor_14", "People say the Nine rode out of Minas Morgul again. I wish we had more brave captains like Boromir to lead our men into battle against such ancient foes."),
("gondor_rumor_15", "The Southerners are pushing us out of Harondor. They've been raiding us hard for some time. I wish I could walk safely through the green fields of Lebennin again. But we are told 'No.', our soldiers are to protect the heart of the realm."),
("gondor_rumor_16", "My friend's cousin is a bowman in service of Hirluin the Fair. They have by far the best looking uniforms, if you ask me."), #:) I like
("gondor_rumor_17", "Those who dwell in the deep vale of the Morthond are accustomed to the shadows. I heard that they see well at night."),
#("gondor_rumor_17", "There is a strange black rock near Erech. I went to see it once with my father. People say it's laid over a chamber where the last son of the sea kings sleeps. I think it's just a rock."),
("gondor_rumor_18", "We are truth-speakers, we Gondorians. We boast seldom, and then perform, or die in the attempt."), #Faramir quote.
#Erebor
#general idea: greedy, grubby, grumpy comic releif dwarves
("dwarf_rumor_begin", "They ask us if dwarves have any friends. Of course we have friends. But we don't like them."), #A variation on an old joke about Slovenians.
("dwarf_rumor_2", "Orcs? Pfft! Axe-grease, all they are."),
("dwarf_rumor_3", "What's that you're wearing? It doesn't look like it would protect you from a bee sting. And it looks funny."),
("dwarf_rumor_4", "Of course we can ride horses. We just don't want to!"),
("dwarf_rumor_5", "Bugger off! We don't need your sort around here, the orcs are bad enough."),
("dwarf_rumor_6", "Who are you calling short?"),
("dwarf_rumor_7", "You should see the caves of Hornburg. If we could only mine all the gems there..."),
("dwarf_rumor_8", "No word from our brothers in Moria for a while now. I bet they just want to keep all the riches to themselves!"),
("dwarf_rumor_9", "Elves? What have the elves ever done for us? Ok, healing arts, but besides that? Ok, some smithing techniques, but anything else? Ok, they fight the Shadow, but besides what have they really ever done for us, I ask you?"), #Monty Python paraphrase
("dwarf_rumor_10", "A flagon of ale, a roast pig, a girl with a thick beard and I'm happy!"),
("dwarf_rumor_11", "Well, Brian, I'm opening a mine! What? Ugh? Well, Brian, I'm opening a mine!"), #Monty Python paraphrase
("dwarf_rumor_12", "We, Dwarves always build more than one entry into our mines. And then there's the secret ones too."),
("dwarf_rumor_13", "Strange are the ways of men."), #Gimli quote
("dwarf_rumor_14", "Unwearied then were Durin's folk beneath the mountains music woke: The harpers harped, the minstrels sang, and at the gates the trumpets rang."), #Song of Durin
("dwarf_rumor_15", "*humms quietly* Kill the Men! Kill the Elves! Save the gold for ourselves!"), #Hobbit quote.
#Mordor
#general idea= not much to say except Black Speech, fear and hate
("mordor_rumor_begin", "Lugbúrz commands!"),
("mordor_rumor_2", "Nazgûl will defeat the world of men!"),
("mordor_rumor_3", "Why aren't you working, glob! The Eye is watching!"),
("mordor_rumor_4", "Soon, darkness comes! Durb-burz!"),
("mordor_rumor_5", "Hungry! Where is food?"),
("mordor_rumor_6", "We will feast on men of the White city!"),
("mordor_rumor_7", "Master trains Olog-hai for war!"),
("mordor_rumor_8", "Warg bit my finger. And it really hurts! Warg-filth!"),
("mordor_rumor_9", "Don't trust Saruman-glob!"),
("mordor_rumor_10", "Mountain orcs are weak! We are strong! We will eat tribal snagas!"),
("mordor_rumor_11", "Uruk glob ishi krimp shar-kûk."),
("mordor_rumor_12", "Nazgûl ronk ishi gimb olog-hosh sha uruk-bag. Ha ha ha!"),
("mordor_rumor_13", "Snaga stole my meat, pushdug!"),
("mordor_rumor_14", "Gu kibum kelkum-ishi, burzum-ishi. Akha-gum-ishi ashi gurum."),
("mordor_rumor_15", "Isengard uruk-hai u bagronk sha pushdug Saruman-glob bubhosh skai!"),
("mordor_rumor_16", "If it insults you - kill it. If it fights you - kill it. If it looks at you - kill it. If it's dead - eat it."),
("mordor_rumor_17", "Saruman's uruk-hai say they don't mind the sun. Bûbhosh skai!"),
("mordor_rumor_18", "All dead, all rotten. Elves and Men and Orcs. In the Dead Marshes!"), #Gollum quote, but it'll fit orcs too.
("mordor_rumor_19", "Come not between the Nazgûl and his prey!"), #Nazgul quote
("mordor_rumor_20", "Isengarders? The muck-rakers of a dirty little wizard! It's orc-flesh they eat, I'll warrant."),
("mordor_rumor_21", "Mirkwood is in our hands already, but the elves don't know it yet."),
("mordor_rumor_22", "Crank up yer spotting if you don't want to get ambushed in Ithilien. Those damn greenhoods..."),
("mordor_rumor_23", "Where there's a whip there's a way."),
#Isengard
#general idea= confidence in technology and wise leadership
("isengard_rumor_begin", "Sharkû commands!"),
("isengard_rumor_2", "Horse-men are food! Bubhosh!"),
("isengard_rumor_3", "Horse-men will get a pike surprise! Ha ha ha!"),
("isengard_rumor_4", "Saruman has many tricks! Strong steel and fire-stone!"),
("isengard_rumor_5", "Wild-men stink! But Sharkû is wise. He knows how to use them."),
("isengard_rumor_6", "Moria-scum breed olog-hai! Big! Skai!"),
("isengard_rumor_7", "Wise master make uruk-hai strong!"),
("isengard_rumor_8", "Warg is faster than horse! Warg eats horse!"),
("isengard_rumor_9", "Uruk-hai will trample the horse-men!"),
("isengard_rumor_10", "Grind! Grind! Grind!"),
("isengard_rumor_11", "Uruk glob ishi krimp shar-kûk."),
("isengard_rumor_12", "Burn forest! Make weapons! Kill horse-men!"),
("isengard_rumor_13", "Keep away from the berserker before he starts chopping us up!"),
("isengard_rumor_14", "I saw a berserker get speared through by a horse-man lance. He pulled the manling off his horse by the lance through his guts."),
("isengard_rumor_15", "I don't trust those little mountain orc swines. Isengarders will win this war, with or without them."),
("isengard_rumor_16", "By the White Hand! What's the use of sending mountain-maggots to fight for us, only half-trained! Cursed goblins and orcs of the North!"),
("isengard_rumor_17", "I'd tickle some prisoners with my knife. Sometimes you need to make those miserable rats squeak!"),
("isengard_rumor_18", "There's only one thing the maggots and rats of Lugbúrz can do: they can see like gimlets in the dark."),
("isengard_rumor_19", "We're cutting down the forest, but many orcs that go in, never come out."),
("isengard_rumor_20", "Where there's a whip there's a way."),
#[b]Rhun[/b]
#[i]general idea= ok barbarian types, actually, not evil, just mislead[/i]
("rhun_rumor_begin", "Ride like the wind of the steppes!"),
("rhun_rumor_2", "The Dwarves are greedy and vile. And Dale-men help them exploit and cheat us."),
("rhun_rumor_3", "Three wizards came to our lands a while ago. I wonder what they are up to."),
("rhun_rumor_4", "Our lands are vast and sparsely populated. But we know how to survive there."),
("rhun_rumor_5", "We used to trade with Elves and Dwarves our wine and pipe-weed from the fertile lands. But they cheat and lie!"),
("rhun_rumor_6", "Our cousins from Khand prefer to fight on foot, but we know being on a horse is better."),
("rhun_rumor_7", "We have defeated Gondor legions before, and we will do it again!"),
("rhun_rumor_8", "We fight to the death! Never retreat, never turn and run! Not a step backwards!"),
("rhun_rumor_9", "A red dawn has risen in the east. A red dusk awaits the west!"),
("rhun_rumor_10", "Elven women? Nah. Too fragile!"),
("rhun_rumor_11", "Each of my sons has already brought me a head of an enemy. And my daughter the testicles of one. Ha ha ha!"),
("rhun_rumor_12", "Orcs are filthy beasts with no skill or courage. They have no place on the field of battle."),
("rhun_rumor_13", "What's best in life? To crush your enemies, see them driven before you, and to hear the lamentation of their women."), #[color=green]#Conan quote[/color]
#Dunlendings
#general idea= Rohirrim pissed in their cereal
("dunland_rumor_begin", "We won't rest until we are avenged and the strawheads are on their knees!"),
("dunland_rumor_2", "Rohirrim bastards are friendly with their horses at night! Ha ha ha!"),
("dunland_rumor_3", "Night Wolfs can see in the darkness. Even at night, their throwing spears never miss their target."),
#("dunland_rumor_3", "Strawheads will cough out our land! Together with their blood! Gah!"),
("dunland_rumor_4", "Death to the Forgoil! Death to the Strawheads! Death to the robbers from the North!"),
("dunland_rumor_5", "They call it Rohan now, but it's our ancestral land! We will avenge our forfathers and chase off the dirty land-thieves."),
("dunland_rumor_6", "Don't let the Forgoil catch you, or they will torture and burn you alive!"),
("dunland_rumor_7", "We are the bloodlust of the wolf and the strength of the boar!"),
("dunland_rumor_8", "Forgoil think we are savage and stupid. Let's see what they think after their horsemen meet our pikemen."),
("dunland_rumor_9", "Isengard's crows will peck out Strawheads' eyes, Dunland's wolves will bite their throats."),
("dunland_rumor_10", "I caught and killed a wolf with my bare hands. I will snap a horse-man's neck like a twig! Grrr!"),
("dunland_rumor_11", "Our chief found an old bronze sword in a barrow. He bent it and threw it in the marsh. Spirits of the hills will be on our side for sure. It is the old way."),
("dunland_rumor_12", "My forefathers fought with Freca and later Wulf against the bloodied Forgoil. We remember their courage."),
#Beornings/Woodsmen
#general idea= haughty, happy types, somewhat detached from the wars
("beorn_rumor_begin", "The woods are vast and all manner of creatures live inside."),
("beorn_rumor_2", "Wild bees make the best honey!"),
("beorn_rumor_3", "Elves of the woods are elusive, but kind. Dwarves from the mountains are loud and cheerful. Men of Dale are hardworking."),
("beorn_rumor_4", "We see many strange beasts passing through our lands."),
("beorn_rumor_5", "I sleep all night, and I work all day!"),
("beorn_rumor_6", "Evil is creeping from the mountains yonder."),
("beorn_rumor_7", "The great forest is not as it used to be anymore!"),
("beorn_rumor_8", "The strength of the axe is not in the blade, but in the haft."),
("beorn_rumor_9", "We slept through the last winter. What? Yes, you need to eat a lot in the autumn to last through winter like this."),
("beorn_rumor_10", "Men of Rohan are our kin, bears are our blood, goblins are our prey!"),
("beorn_rumor_11", "Turn into bears? Of course we don't. Who told you that? Ha ha ha!"),
("beorn_rumor_12", "Beorn was a great man. No, not a man, a giant!"),
#("beorn_rumor_13", "*GROWLS*   Do you have any honey?"),
("beorn_rumor_13", "The best and boldest woodmen warriors do not fear the shadows of the forest. They can fight in the darkness just as well as orcs and other filth who stalk the woods."),
("beorn_rumor_14", "Don't wander off alone in the mountains! Bears and wolves stay away from larger groups of men. But hunger, or as some say - shadow spirits, may drive them close enough to attack you."), 
#[b]Lothlorien[/b]
#[i]general idea= Merl? Marco? - slight depression about shit that's going down, thoughts about leaving this goddamn continent mixed with semi-confident feeling of safety in the woods.[/i]
("lorien_rumor_begin", "O Lórien! The Winter comes, the bare and leafless Day; The leaves are falling in the stream, the River flows away. "), #[color=red]Galadriel's Song of Eldamar[/color]
("lorien_rumor_2", "Speak no evil of the Lady Galadriel! There is in her and in this land, no evil, unless a man bring it hither himself. Then let him beware!"), #[color=red]Aragorn quote of Galadriel[/color]
("lorien_rumor_3", "The world is indeed full of peril, and in it there are many dark places; but still there is much that is fair, and though in all lands love is now mingled with grief, it grows perhaps the greater."), #[color=red]Haldir quote[/color]
("lorien_rumor_4", "Good and ill have not changed since yesteryear; nor are they one thing among Elves and Dwarves, and another among Men. It is a man's part to discern them, as much in the Golden Wood as in his own house."), #[color=red]Aragorn quote[/color]
("lorien_rumor_5", "Often does hatred hurt itself!"), #[color=red]Gandalf quote[/color]
("lorien_rumor_6", "Ancient magic protects Lothlórien, so powerful the Darkness does not yet dare challenge it."),
("lorien_rumor_7", "Nathlo i nathal! You are safe within the golden woods. Posto vae - rest now, eat and drink. If you must leave then, carry with you a memory of how Lorien once was."),
("lorien_rumor_8", "It is said that the sea calls to everyone, sooner or later. I too shall hear the gulls one day, leave Laurelindórenan for good. I Harthon an lend and. "),
("lorien_rumor_9", "Av-'osto - do not be afraid! More than our grey cloaks protect us from the enemy here."),
#[b]Rivendell a.k.a. Imladris[/b]
#[i]general idea= Merl? Marco? - feeling of a tiresome, ancient watch they keep, but pride of culture and heritage - a duty that bids them take up dusty arms and join the battlefield again .[/i]
("imladris_rumor_begin", "May the blessing of Elves and Men and all Free Folk go with you."), #[color=red]Elrond quote[/color]
("imladris_rumor_2", "May the stars shine upon your faces!"), #[color=red]Elrond quote[/color]
("imladris_rumor_3", "He that breaks a thing to find out what it is has left the path of wisdom."), #[color=red]Gandalf at council of Elrond.[/color]
("imladris_rumor_4", "We must take a hard road, a road unforeseen. There lies our hope, if hope it be."), #[color=red]Elrond at council of Elrond.[/color]
("imladris_rumor_5", "Despair is only for those who see the end beyond all doubt. We do not."), #[color=red]Gandalf at council of Elrond.[/color]
("imladris_rumor_6", "Even after the coldest winter flowers do spring. And after the longest night, comes a new dawn."),
("imladris_rumor_7", "So many had gathered when last I rode to war. The light of the drawing of our swords was like a fire in a field of reeds. So few have left Imladris now. "),
("imladris_rumor_8", "Áva rucë! The Eldar have taken arms to fight the enemy alongside brave Edain once more.  Perhaps for the last time, who knows? We sing of war, of fire and the end of the Night."),
("imladris_rumor_9", "I see the men from the East ride under the Dark Lord's banner and it is as though I watched their ancestors again - waves of horsemen shattering upon the gleaming shieldwall of the Last Alliance. If only the memory of Edain was as long as ours."),
#[b]Mirkwood Elves[/b]
#[i]general idea= Merl? Marco? - quite paranoid, slightly bigheaded about their own importance, secretly enjoying the fruits of their trade with Dale and dwarves.[/i]
("woodelf_rumor_begin", "An Elven-maid there was of old, /A shining star by day: /Her mantle white was hemmed with gold, /Her shoes of silver-grey."), #[color=red]Song of Nimrodel sung by Legolas[/color]
("woodelf_rumor_2", "Time does not tarry ever, but change and growth is not in all things and places alike. For the Elves the world moves, and it moves both very swift and very slow. Swift, because they themselves change little, and all else fleets by: it is a grief to them. Slow, because they do not count the running years, not for themselves."), #[color=red]Legolas quote[/color]
("woodelf_rumor_3", "Darkness and evil creep over these once beautiful woods. Unless they are stopped, they will smother all hope, all light."), 
("woodelf_rumor_4", "Quick and nimble, quiet and precise, we can yet keep the Darkness at bay. But how much longer?"),
("woodelf_rumor_5", "Shhh, no dhínen! There may be orcs lurking around. We must be on guard!"),
("woodelf_rumor_6", "*stares at you, obviously annoyed by your presence*"), #[color=red]removed text, because the player could be a Woodelf too and stil get this rumour as if he's foreign[/color]
("woodelf_rumor_7", "Oduleg hi am man theled? We need to know your purpose here. Sorcerer's spies are everywhere."),
("woodelf_rumor_8", "Edain of Dale make intricate toys these days! They've learnt much from the Naugrim."),
##
("woodelf_rumor_9", "The shadow of Dol Guldur is spreading. Dark creatures have been seen in the woods, our outposts attacked, hunters disappear and are never seen again. Our patrols now number at least 35 soldiers, we have grown that fearful!"),
#[b]Dale[/b]
#[i]general idea= fearful because of the assault from several fronts[/i]
("dale_rumor_begin", "First there was the dragon, now this..."), 
("dale_rumor_2", "As if the orcs coming from the north weren't bad enough, now the hordes from the east are upon us!"), 
("dale_rumor_3", "Ever since the defeat of the dragon, we know how to look for the enemy's weak spot."), 
("dale_rumor_4", "Easterlings will never make it past us and our dwarven allies."), 
("dale_rumor_5", "Have you ever seen the sun rise over the Long lake? The colours used to make my heart sing. But now all I see is a red dawn. A bad omen."), 
("dale_rumor_6", "Dwarves are a bit too attached to treasures. We still don't know what to think of Thorin Oakenshield."),
("dale_rumor_7", "The men of Rohan are our cousins and our own language is very similar to theirs."),
("dale_rumor_8", "Esgaroth got its name from an Elven word for reeds, because of its reed banks. Did you know that?"),
("dale_rumor_9", "The dragon was a sort of a monster noone wants to see ever again."),
("dale_rumor_10", "Our prosperity comes from trade with the Dwarves and the Elves. But it's hard to bargain with Dwarves. Very little profit there."),
#[b]Harad[/b]
#[i]general idea= Merl? This should be Merl's forte.[/i]
("harad_rumor_begin", "The Black Snake will strike swift and deadly."), 
("harad_rumor_2", "By the Serpent! Our beasts will trample Gondorians into the dirt."), 
("harad_rumor_3", "Odum vermajál otí verthaba av daranaja-e-jatánus!"), 
("harad_rumor_4", "There is much gold and gems in Gondor. And even more in the lands beyond."),
("harad_rumor_5", "We will catch many western weaklings and sacrifice them to the Serpent God."),
("harad_rumor_6", "Corsairs have their uses, they sail well, but are rowdy and unclean in appearance and sneaky in behaviour."),
#("harad_rumor_7", "I'd never set foot on a ship. Corsairs can have all the seas as far as I am concerned."),
("harad_rumor_7", "The Panthers from Far Harad hunt their prey in the cover of the night. Our enemies will not see them coming."),
("harad_rumor_8", "Warriors of Khand are fierce and fearless, but their strategy is too simple."),
("harad_rumor_9", "I'm counting on good loot in the West. We were promised it. Then I can return home and run my carpet shop in peace."),
("harad_rumor_10", "Keep away from the Mumakil. They are ill-tempered beasts and will squash you in an instant."),
("harad_rumor_11", "In Harad we have deserts and jungles, mountains and sea. Our peoples are as diverse as our lands and as numerous as the grains of sand."),
("harad_rumor_12", "Many knights from Harondor prefer sabres over straight blades. They're quite good for cutting down running peasants, but you need a spear or a good sword to penetrate strong armour."),
("harad_rumor_13", "My blood brother signed up with the Karka - he's a scout now. Riders of 'The Fang' lead a dangerous life, but it is good experience for young hot-headed boys."),
("harad_rumor_14", "Don't ever pick a fight with the Lion brotherhood! Their reputation is well earned."),
("harad_rumor_15", "I wish we had more weapons made of black iron. Many still have to manage with bronze, some even with wooden clubs and javelins of black glass, running into battle naked."),
#[b]Mt.Gundabad[/b]
# [color=green]orcs from cold north in search for warmer places?[/color]
("gunda_rumor_begin", "Take warm lands from men we come!"),
("gunda_rumor_2", "Sharkû promised warm caves."),
("gunda_rumor_3", "Enough hiding in the cold mountains! Now we march into warm lands of men."),
("gunda_rumor_4", "We saw a slimy skulker in our mountain tunnels, but could never catch him. He just disappeared when we got close."),
("gunda_rumor_5", "The Isengarders think they're something special because the old man is equipping them."),
("gunda_rumor_6", "We will burn the villages of men to keep us warm."),
("gunda_rumor_7", "Manlings will feel the frostbite we will bring to them. And afterwards the fire. Ha ha ha!"),
("gunda_rumor_8", "Azog and Bolg almost defeated dwarves, elves and manlings last time. But bird-monsters and bear-men saved them. *spit*"),
("gunda_rumor_9", "Dwarf-flesh is tough and stringy. Man-flesh is better."),
("gunda_rumor_10", "Bear-men came from the woods and ate Boldush. Bad luck for Boldush! Ha ha ha!"),
("gunda_rumor_11", "Some moved to Moria, much room there. But also Ghâsh in the deep. Best stay away!"),
#[b]Moria[/b]
#[color=green]terror from the deep?[/color]
("moria_rumor_begin", "When you hear drums - run and hide!"),
("moria_rumor_2", "Ghâsh is in the deep!"),
("moria_rumor_3", "Doom! Doom! Doom! Drums of the deep."),
("moria_rumor_4", "Moria is big, but no dwarves hide in it anymore."),
("moria_rumor_5", "Dwarves dug too deep. All the better for us. Ha ha ha!"),
("moria_rumor_6", "Many tunnels in Moria. We don't go to all."),
("moria_rumor_7", "Some manlings and dwarves sneaked past our sentries in the mines a while ago. We doubled the watch since."),
("moria_rumor_8", "Dwarves will never set foot here again! Ever!"),
("moria_rumor_9", "When we gather enough troops, we will go and burn down woods of elves."),
("moria_rumor_10", "Not much food in Moria. We're hungry. Must catch men and elves!"),
("moria_rumor_11", "Some go to the forest in the south. None come out."),
#[b]Umbar[/b]
#[i]general idea= Pirates and the old grudge against Gondor[/i]
("umbar_rumor_begin", "All the seas will belong to the black sails!"),
("umbar_rumor_2", "There's no Gondor ships left to sink, now we go plunder inland."),
#("umbar_rumor_3", "Umbar is our fate! And it will be Gondor's too."),
("umbar_rumor_3", "Our Night Raiders can fight in the dark just as well as in broad daylight. They lead our scouting parties far inland."),
("umbar_rumor_4", "Gondorians can't sail! They've got land-legs."),
("umbar_rumor_5", "We've killed Gondorian kings in the past. Now they don't even have a king for us to kill."),
("umbar_rumor_6", "The sneaky Gondorians burned our fleet years ago. Now it's Gondor that'll burn."),
("umbar_rumor_7", "Nothing the sea can throw at us frightens a corsair. But we heard some disturbing rumours about abominations on land."),
("umbar_rumor_8", "We will spill over Gondor like a giant wave and reclaim our long lost lands."),
("umbar_rumor_9", "Haradrim don't drink rum. Did you know that? We like some, to steady the harpoon hand."),
("umbar_rumor_10", "I saw some Variags of Khand fighting. I wouldn't want to be facing them in battle. It is a good thing they are on our side."),
#[b]Khand[/b]
#[i]general idea= More hardcore Easterling types[/i]
("khand_rumor_begin", "A fight is a fight, no matter how bloody. But retreat is the greatest shame!"),
("khand_rumor_2", "Our swords once drawn, must have blood!"),
("khand_rumor_3", "The ground trembles under our heavy cataphract cavalry, but our enemies tremble at the mere mention of us!"),
("khand_rumor_4", "This time we left the Wainriders behind, our attack will catch the enemies off guard."),
("khand_rumor_5", "We are the Variags of Khand, the fiercest warriors anywhere!"),
("khand_rumor_6", "Rhun warriors are fierce too, but they fight on horseback, we rather maul our enemies on foot."),
("khand_rumor_7", "We have fought Gondorians in the past, this time we will finish them for good!"),
("khand_rumor_8", "The West is weak and decadent. They have no warrior spirit. They will fall to our swords and axes."),
("khand_rumor_9", "We do not fight for gold or slaves, we fight for honour and glory!"),
("khand_rumor_10", "The men of the West are arrogant, they do not know what might they are facing!"),
("khand_rumor_11", "We trade with Rhun, Mordor and Harad. And sometimes we fight them too. It is the way of our people."),
("khand_rumor_12", "Have you made your warrior mask yet? You'll need one soon! If the enemy can't see your face, his spirit won't be able to find you."),
#[b]Dol Guldur[/b]
#[color=green]same as Mordor for the time being[/color]
#[b]Other[/b]
#[i]We must also have the "hints and tips" category that all good on one, and all bad on the other side will use. These should be general enough to transcend race and faction.[/i]

("good_rumor_begin", "From the ashes a fire shall be woken, A light from the shadows shall spring; Renewed shall be blade that was broken, The crownless again shall be king."), #[color=red]Gandalf quote[/color]
("good_rumor_2", "Orcs fight better at night but are weaker by day."),
("good_rumor_3", "Urukhai are a different breed of orc that doesn't fear sunlight!"),
("good_rumor_4", "Always after a defeat and a respite, the Shadow takes another shape and grows again."), #[color=red]Gandalf quote[/color]
("good_rumor_5", "The Dead Marshes... a land defiled, diseased beyond all healing."), #[color=red]Chapter 'The Passage of the Marshes'.[/color]
("good_rumor_6", "The Shadow that bred can only mock, it cannot make: not real new things of its own. I don't think it gave life to the orcs, it only ruined them and twisted them."), #[color=red]Frodo quote[/color]
("good_rumor_7", "Greenwood it used to be called and full of elves it was. Greatest of the forests of the Northern world. But now it's Mirkwood. Crawling with all manner of evil creatures."),
("good_rumor_8", "The Argonath, The Pillars of the Kings, great guardians of the old northern border of Gondor."),
("good_rumor_9", "Amon Hen is the westernmost of the three peaks at the southern end of Nen Hithoel."),

("neutral_rumor_begin", "Tomorrow everything could change..."),
("neutral_rumor_2", "Dead Marshes... a place defiled and diseased."), #[color=red]Chapter 'The Passage of the Marshes'.[/color]
("neutral_rumor_3", "The land used to be much different once."),
("neutral_rumor_4", "Men fight weaker at night. But there are some who are used to seeing in the dark."),
#("neutral_rumor_4", "Stay clear of Fangorn forest."),

("evil_rumor_begin", "Orcs fight better at night, men fight better by day."),
("evil_rumor_2", "Fight horseman with pike, footman with arrow and archer with shield!"),
("evil_rumor_3", "Large statues of weaklings on the big river will not stand much longer."),

("legendary_rumor_begin", "Legend says that trees meet to talk in Fangorn."),
("legendary_rumor_amonhen", "They say there is a special place on the Anduin, somewhere where the big statues stand."),
("legendary_rumor_deadmarshes", "It is rumoured all dead seems alive in the middle of Dead Marshes."),
("legendary_rumor_mirkwood", "Creatures other than orcs crawl around Mirkwood."),
("legendary_rumor_fangorn", "Fangorn is a forest best avoided. Unusual things happen there."),

("last_rumor", "I haven't heard anything interesting lately."),
#[i]For good player only we should make an Entmoot location in Fangorn, and a wee chat with the Ents. We have Ent brew planned and ready as reward for +STR, good player should be able to make permanent peace with Ents so Fangorn no longer attacks, etc...[/i]
("ent_rumor_begin", "Do not be hasty now..."), 
("ent_rumor_2", "Learn now the lore of Living Creatures! First name the four, the free peoples: Eldest of all, the elf-children; Dwarf the delver, dark are his houses; Ent the earthborn, old as mountains; Man the mortal, master of horses."), #[color=red]The Long List of the Ents from Treebeard[/color]
("ent_rumor_3", "The Old Entish is a lovely language, but it takes a very long time to say anything in it, because we do not say anything in it, unless it is worth taking a long time to say, and to listen to."), #[color=red]Treebeard quote[/color]

### TLD home faction ranks - faction order must be kept 
("gondor_rank_0", "Commoner of Gondor"),
("gondor_rank_1", "Soldier of Gondor"),
("gondor_rank_2", "Sergeant of Gondor"),
("gondor_rank_3", "Knight of Gondor"),
("gondor_rank_4", "Tower Guard of Gondor"),
("gondor_rank_5", "Citadel Knight of Gondor"),
("gondor_rank_6", "Steward's Guard of Gondor"),
("gondor_rank_7", "Captain of Gondor"),
("gondor_rank_8", "Champion of Gondor"),
("gondor_rank_9", "Hero of Gondor"),

("dwarf_rank_0", "Dwarven Greenbeard"),
("dwarf_rank_1", "Dwarven Miner"),
("dwarf_rank_2", "Dwarven Warrior"),
("dwarf_rank_3", "Dwarven Longbeard"),
("dwarf_rank_4", "Dwarven Axe"),
("dwarf_rank_5", "Dwarven Master Axe"),
("dwarf_rank_6", "Dwarven Greybeard"),
("dwarf_rank_7", "Dwarven Captain"),
("dwarf_rank_8", "Dwarven Chief"),
("dwarf_rank_9", "Hero of the Halls"),

("rohan_rank_0", "Ceorl, Commoner of Rohan"),
("rohan_rank_1", "Thain, Servant of Rohan"),
("rohan_rank_2", "Léod, Freeman of Rohan"),
("rohan_rank_3", "Rohir, Rider of Rohan"),
("rohan_rank_4", "Scyldbora, Shieldbearer of Rohan"),
("rohan_rank_5", "Swéordbora, Swordbearer of Rohan"),
("rohan_rank_6", "Frumgar, First Spear of Rohan"),
("rohan_rank_7", "Bealdoraed, Master Adviser of Rohan"),
("rohan_rank_8", "Eorl, Nobleman of Rohan"),
("rohan_rank_9", "Haleth, Hero of Rohan"),

("mordor_rank_0", "Worm"),
("mordor_rank_1", "Snaga"),
("mordor_rank_2", "Backstabber of Gorgoroth"),
("mordor_rank_3", "Sentry of Cirith Ungol"),
("mordor_rank_4", "Slavedriver of Udûn"),
("mordor_rank_5", "Despoiler of Durthang"),
("mordor_rank_6", "Watchman of Morannon"),
("mordor_rank_7", "Captain of Minas Morgul"),
("mordor_rank_8", "Commander of Barad-dûr"),
("mordor_rank_9", "Scourge of Mankind"),

("isengard_rank_0", "Rat"),
("isengard_rank_1", "Snaga"),
("isengard_rank_2", "Crankturner"),
("isengard_rank_3", "Treeburner"),
("isengard_rank_4", "Wargfeeder"),
("isengard_rank_5", "Ironsmelter"),
("isengard_rank_6", "Forgemaster"),
("isengard_rank_7", "Captain of Orthanc"),
("isengard_rank_8", "Commander of Legions"),
("isengard_rank_9", "White Right Hand of the Wizard"),

("lorien_rank_0", "Sador, Faithful to Lorien"),
("lorien_rank_1", "Tauron, Forester of Lorien"),
("lorien_rank_2", "Mifaron, Grey Hunter of Lorien"),
("lorien_rank_3", "Thindirith, Grey Guard of Lorien"),
("lorien_rank_4", "Thangyl, Shieldbearer of Lorien"),
("lorien_rank_5", "Maglagyl, Swordbearer of Lorien"),
("lorien_rank_6", "Tiribrannon, Warden of Lorien"),
("lorien_rank_7", "Glaurchir, Grandmaster of Lorien"),
("lorien_rank_8", "Galadhîr, Radiant Lord of Lorien"),
("lorien_rank_9", "Thalion, Hero of Lorien"),

("imladris_rank_0", "Háno, Brother of Imladris"),
("imladris_rank_1", "Macar, Warrior of Imladris"),
("imladris_rank_2", "Sindacollo, Grey Cloak of Imladris"),
("imladris_rank_3", "Luinëcollo, Blue Cloak of Imladris"),
("imladris_rank_4", "Turmacolindo, Shieldbearer of Imladris"),
("imladris_rank_5", "Langocolindo, Swordbearer of Imladris"),
("imladris_rank_6", "Aráto, Champion of Imladris"),
("imladris_rank_7", "Hesto, Captain of Imladris"),
("imladris_rank_8", "Runando, Redeemer of Imladris"),
("imladris_rank_9", "Callo, Hero of Imladris"),

("woodelf_rank_0", "Sador, Faithful to Greenwood"),
("woodelf_rank_1", "Tauron, Forester of Greenwood"),
("woodelf_rank_2", "Hirfaron, Master Hunter of Greenwood"),
("woodelf_rank_3", "Calendirith, Green Guard of Greenwood"),
("woodelf_rank_4", "Thangyl, Shieldbearer of Greenwood"),
("woodelf_rank_5", "Maglagyl, Swordbearer of Greenwood"),
("woodelf_rank_6", "Tiribrannon, Warden of Greenwood"),
("woodelf_rank_7", "Pengherdir, Bowmaster of Greenwood"),
("woodelf_rank_8", "Armagor, Royal Swordsman of Greenwood"),
("woodelf_rank_9", "Thalion, Hero of Greenwood"),

("dale_rank_0", "Commoner of Dale"),
("dale_rank_1", "Freeman of Dale"),
("dale_rank_2", "Soldier of Dale"),
("dale_rank_3", "Boatman of Dale"),
("dale_rank_4", "Shieldbearer of Dale"),
("dale_rank_5", "Swordbearer of Dale"),
("dale_rank_6", "Barding, Archer of Dale"),
("dale_rank_7", "Captain of Dale"),
("dale_rank_8", "Lake Master of Dale"),
("dale_rank_9", "Hero of Dale"),

("harad_rank_0", "Initiate of the Tribe"),
("harad_rank_1", "Adult of the Tribe"),
("harad_rank_2", "Warrior of the Tribe"),
("harad_rank_3", "Lionslayer"),
("harad_rank_4", "Snakecharmer"),
("harad_rank_5", "Mumakil Handler"),
("harad_rank_6", "Black Snake Guard"),
("harad_rank_7", "Captain of Harondor"),
("harad_rank_8", "General of the Great Desert"),
("harad_rank_9", "The Golden Serpent"),

("rhun_rank_0", "Plainsman of Rhun"),
("rhun_rank_1", "Serf of Rhun"),
("rhun_rank_2", "Warrior of Rhun"),
("rhun_rank_3", "Bull Warrior of Rhun"),
("rhun_rank_4", "Shieldbearer of Rhun"),
("rhun_rank_5", "Swordbearer of Rhun"),
("rhun_rank_6", "Horsemaster of Rhun"),
("rhun_rank_7", "Warlord of Rhun"),
("rhun_rank_8", "Chief of the Steppe Clans"),
("rhun_rank_9", "Khamûl's Right Hand"),

("khand_rank_0", "Plainsman of Khand"),
("khand_rank_1", "Serf of Khand"),
("khand_rank_2", "Warrior of Khand"),
("khand_rank_3", "Hawk Warrior of Khand"),
("khand_rank_4", "Shieldbearer of Khand"),
("khand_rank_5", "Swordbearer of Khand"),
("khand_rank_6", "Horsemaster of Khand"),
("khand_rank_7", "Warlord of the Variags"),
("khand_rank_8", "Chief of the Variag Clans"),
("khand_rank_9", "Legendary Conqueror"),

("umbar_rank_0", "Landlubber"),
("umbar_rank_1", "Deck Hand"),
("umbar_rank_2", "Sailor"),
("umbar_rank_3", "Harpooner"),
("umbar_rank_4", "Throatcutter"),
("umbar_rank_5", "Plunderer"),
("umbar_rank_6", "Sailmaster"),
("umbar_rank_7", "Captain of Umbar"),
("umbar_rank_8", "Commander of the Fleet"),
("umbar_rank_9", "Grand Admiral of the Seas"),

("moria_rank_0", "Maggot"),
("moria_rank_1", "Snaga"),
("moria_rank_2", "Tunnel Rat"),
("moria_rank_3", "Cave Forager"),
("moria_rank_4", "Plunderer of the Mines"),
("moria_rank_5", "Despoiler of the Halls"),
("moria_rank_6", "Dwarfbane"),
("moria_rank_7", "Goblin Warlord"),
("moria_rank_8", "Goblin Chief"),
("moria_rank_9", "Terror from the Deep"),

#same as Mordor
("guldur_rank_0", "Worm"),
("guldur_rank_1", "Snaga"),
("guldur_rank_2", "Backstabber of Gorgoroth"),
("guldur_rank_3", "Sentry of Cirith Ungol"),
("guldur_rank_4", "Slavedriver of Udûn"),
("guldur_rank_5", "Despoiler of Durthang"),
("guldur_rank_6", "Watchman of Morannon"),
("guldur_rank_7", "Captain of Minas Morgul"),
("guldur_rank_8", "Commander of Barad-dûr"),
("guldur_rank_9", "Scourge of Mankind"),

("gundabad_rank_0", "Turd"),
("gundabad_rank_1", "Snaga"),
("gundabad_rank_2", "Tunnel Rat"),
("gundabad_rank_3", "Cave Forager"),
("gundabad_rank_4", "Plunderer of the Hills"),
("gundabad_rank_5", "Despoiler of the Mountains"),
("gundabad_rank_6", "Dwarfbane"),
("gundabad_rank_7", "Wargrider Warlord"),
("gundabad_rank_8", "Great Goblin"),
("gundabad_rank_9", "Pillager of the North"),

("dunland_rank_0", "Pup"),
("dunland_rank_1", "Dog"),
("dunland_rank_2", "Wardog"),
("dunland_rank_3", "Wolf"),
("dunland_rank_4", "Strong Wolf"),
("dunland_rank_5", "Dire Wolf"),
("dunland_rank_6", "Great Wolf"),
("dunland_rank_7", "Wolfpack Leader"),
("dunland_rank_8", "Chief of the Clans"),
("dunland_rank_9", "Freca's Avenger"),

("beorn_rank_0", "Forest Cub"),
("beorn_rank_1", "Forest Tracker"),
("beorn_rank_2", "Forest Hunter"),
("beorn_rank_3", "Forest Ranger"),
("beorn_rank_4", "Forest Shieldbearer"),
("beorn_rank_5", "Forest Axebearer"),
("beorn_rank_6", "Forest Bear"),
("beorn_rank_7", "Forest Great Bear"),
("beorn_rank_8", "Forest Giant"),
("beorn_rank_9", "Hero of the Forests"),
# end of ranks

("tld_introduction","TLD Introduction - you should go to Edoras."),

("tld_erebor_dungeon","The smell of death surrounds this place. I'd better be careful."),
("tld_spear_hit","Ouch!"),    


("fullname_region_unknown", "an unnamed region, somewhere in Middle Earth"), # -1

("fullname_region_pelennor", "Pelennor Fields, the plains around Minas Tirith, capital of the Realm of Gondor"), #0
("fullname_region_subfac_pelargir", "the Fiefdom of Lebennin, part of the Realm of Gondor"), # pelargir
("fullname_region_subfac_dol_amroth", "Belfalas, the costal region in the South of Gondor"), #subfac_dol_amroth
("fullname_region_subfac_ethring", "Ringló Vale, a valley of the Realm of Gondor"), # subfac_ethring
("fullname_region_subfac_lossarnach", "the Fiefdom of Lossarnach, also known as the Vale of Flowers, part of the Realm of Gondor"),
("fullname_region_subfac_pinnath_gelin", "the Green Hills of Pinnath Gelin, a region in the Realm of Gondor"),
("fullname_region_subfac_blackroot", "the Fiefdom of Lamedon, part of the Realm of Gondor"), # subfac_blackroot
("fullname_region_n_ithilien", "North Ithilien, easternmost province of the Realm of Gondor"),
("fullname_region_c_ithilien", "Emyn Arnen, a range of hills in the central regions of Ithilien, across the Great River from Minas Tirith"),
("fullname_region_s_ithilien", "South Ithilien, easternmost province of the Realm of Gondor"),

("fullname_region_druadan_forest", "Drúadan Forest, the Gondor Forest of the Drúedain"), #9
("fullname_region_firien_wood","Firien wood, the Whispering Wood, a Gondor forest of oaks"), #10

("fullname_region_anorien", "Anórien, the Sun-land, a valley between the White Mountains and the Anduin river"), #11

("fullname_region_rohan0", "the Folde, the heart of Rohan"), 
("fullname_region_rohan1", "the Eastemnet, a part of Rohan, the Riddermark"), 
("fullname_region_rohan2", "the Westemnet, a part of Rohan, the Riddermark"), 
("fullname_region_rohan3", "the Eastfold, a part of Rohan, the Riddermark"), 
("fullname_region_rohan4", "the Westfold, a part of Rohan, the Riddermark"), 
("fullname_region_rohan5", "Helm's Deep, a valley of the White Mountains, in Rohan"), 

("fullname_region_the_wold", "the Wold, the Northeastern area of the Riddermark of Rohan"), # region_the_wold
("fullname_region_gap_of_rohan","the Gap of Rohan, the westernmost border of Rohan, a contested area between the Rohirrim and the Dunlendings."),

("fullname_region_entwash", "the Mouths of the Entwash, where the Rohan river Entwash joins the Anduin"), # region_entwash = 20
("fullname_region_wetwang", "Nindalf, the swamps of Wetwang"), # region_wetwang = 21

("fullname_region_dead_marshes", "the Dead Marshes, the ancient battlefield of the great Battle of Dagor Dagorlad, now a cursed place"), #region_dead_marshes = 22

("fullname_region_isengard", "the plains around Isengard" ),#region_isengard = 23

("fullname_region_fangorn", "the Fangorn forest, where trees are said to talk." ),#region_fangorn

("fullname_region_brown_lands", "the Brown Lands, covering the expanse between the Emyn Muil and Mirkwood" ),#region_brown_lands = 25
("fullname_region_dagorlad", "the Dagorlad, the great, treeless, expanse of The Battle Plain, before the gates of Mordor"), # = 26
("fullname_region_n_undeep", "the North Undeep, the larger of the two Anduin meanders"), # = 27
("fullname_region_s_undeep", "the South Undeep, the lesser of the two large Anduin bends"), # = 28
("fullname_region_emyn_muil", "Emyn Muil, the rocky hills above the inflow of the Entwash"), # = 29 

("fullname_region_misty_mountains", "the foothills of Misty Mountains" ),#region_misty_mountains = 30
("fullname_region_lorien", "Lothlórien, the forest of the Sindar elves, where the golden Mallorns grow" ),#region_lorien = 31
("fullname_region_anduin_banks", "the valley of Anduin, between Misty Mountains and Mirkwood" ),#region_anduin_banks = 32 (FOR LACK OF A BETTER GEOGRAPHICAL NAME)
("fullname_region_n_mirkwood", "the dense forests of northern Mirkwood, home of the Woodelves" ),#region_n_mirkwood = 33
("fullname_region_s_mirkwood", "the dense forest of southern Mirkwood, said to be infested by strange creatures" ),#region_s_mirkwood = 34
("fullname_region_above_mirkwook", "Northen Rhovanion, the area between Mirkwood and the Grey Mountains in the North" ),#region_above_mirkwook = 35  (FOR LACK OF A BETTER GEOGRAPHICAL NAME)
("fullname_region_grey_mountains", "the foothills of Grey Mountains, where Dwarves dwell" ),#region_grey_mountains = 36
("fullname_region_mordor", "Mordor, the dark Realm of Sauron" ),#region_mordor = 37
("fullname_region_dimrill", "Dimrill Dale, at the feet of the Mountains of Moria" ),#region_Dimrill = 38 InVain
("fullname_region_s_rebor", "the realm of Dale, at the feet of the Lonely Mountain" ),#region_s_rebor = 39 InVain


("shortname_region_unknown", "an unnamed region"), # -1

("shortname_region_pelennor", "Pelennor Fields"), #0
("shortname_region_subfac_pelargir", "the Fiefdom of Lebennin"), # pelargir
("shortname_region_subfac_dol_amroth", "Belfalas"), #subfac_dol_amroth
("shortname_region_subfac_ethring", "Ringló Vale"), # subfac_ethring
("shortname_region_subfac_lossarnach", "the Fiefdom of Lossarnach"),
("shortname_region_subfac_pinnath_gelin", "the region of Pinnath Gelin"),
("shortname_region_subfac_blackroot", "the Fiefdom of Lamedon"), # subfac_blackroot
("shortname_region_n_ithilien", "North Ithilien"),
("shortname_region_c_ithilien", "Emyn Arnen"),
("shortname_region_s_ithilien", "South Ithilien"),

("shortname_region_druadan_forest", "Drúadan Forest"), #9
("shortname_region_firien_wood","Firien wood"), #10

("shortname_region_anorien", "Anórien"), #11

("shortname_region_rohan0", "the Folde"), 
("shortname_region_rohan1", "Eastemnet"), 
("shortname_region_rohan2", "Westemnet"), 
("shortname_region_rohan3", "Eastfold"), 
("shortname_region_rohan4", "Westfold"), 
("shortname_region_rohan5", "Helm's Deep"), 
("shortname_region_the_wold", "the Wold"), # region_the_wold
("shortname_region_gap_of_rohan","the Gap of Rohan"),

("shortname_region_entwash", "the Mouths of the Entwash"), # region_entwash = 19
("shortname_region_wetwang", "Nindalf"), # region_wetwang = 20

("shortname_region_dead_marshes", "the Dead Marshes"), #region_dead_marshes = 21

("shortname_region_isengard", "the plains around Isengard" ),#region_isengard = 22

("shortname_region_fangorn", "Fangorn" ),#region_fangorn

("shortname_region_brown_lands", "the Brown Lands" ),#region_brown_lands = 25
("fullname_region_dagorlad", "Dagorlad"), # = 26
("fullname_region_n_undeep", "the North Undeep"), # = 27
("fullname_region_s_undeep", "the South Undeep"), # = 28
("fullname_region_emyn_muil", "Emyn Muil"), # = 29 

("shortname_region_misty_mountains", "the foothills of Misty Mountains" ),#region_misty_mountains = 30
("shortname_region_lorien ", "Lorien" ),#region_lorien = 31
("shortname_region_anduin_banks ", "the valley of Anduin" ),#region_anduin_banks = 32
("shortname_region_n_mirkwood ", "North Mirkwood" ),#region_n_mirkwood = 33
("shortname_region_s_mirkwood ", "South Mirkwood" ),#region_s_mirkwood = 34
("shortname_region_above_mirkwook", "Northen Rhovanion" ),#region_above_mirkwook = 35
("shortname_region_grey_mountains", "the foothills of Grey Mountains" ),#region_grey_mountains = 36
("shortname_region_mordor", "the Land of Mordor" ),#region_mordor = 37
("shortname_region_dimrill", "Dimrill Dale" ),#region_Dimrill = 38 InVain
("shortname_region_s_erebor", "the realm of Dale" ),#region_s_erebor = 39 InVain

# Traits - titles and descriptions (the first is used in constants!)
# Also note: these need to be of the same order and number as slot_trait_* in constants

("trait_title_elf_friend", "Elf_Friend"),
("trait_desc_elf_friend", "You_have_become_highly_esteemed_by_the_Elves_and_they_now_regard_you_as_a_trusted_ally._The_cost_to_recruit_elves_has_been_reduced."),

("trait_title_gondor_friend", "Steward's_Blessing"),
("trait_desc_gondor_friend", "You_have_become_highly_esteemed_by_the_Steward_Denethor_and_your_status_has_risen_among_the_men_of_Gondor_as_a_result._The_cost_to_recruit_Gondorians_has_been_reduced."),

("trait_title_rohan_friend", "King's_Man"),
("trait_desc_rohan_friend", "You_have_become_highly_esteemed_by_King_Theoden_of_Rohan_and_your_status_has_risen_among_the_men_of_Rohan_as_a_result._The_cost_to_recruit_Rohirrim_men_has_been_reduced.."),

("trait_title_brigand_friend", "Barbarian_Champion"),
("trait_desc_brigand_friend", "You_have_become_highly_esteemed_by_the_barbarian_tribes_serving_Sauron_as_a_result_of_your_impressive_displays_in_the_arena._You_may_now_recruit_barbarians_at_reduced_cost."),

("trait_title_blessed", "Blessed"),
("trait_desc_blessed", "You_sense_that_you_have_been_blessed_by_powers_from_beyond_the_sea,_and_perhaps_further_away_still._You_do_not_know_why_this_has_happened_or_what_it_may_mean_but_you_are_certain_that_it_is_so."),

("trait_title_reverent", "Reverent"),
("trait_desc_reverent", "You_have_acquired_a_reputation_for_reverence_and_wisdom._Men_and_Elves_are_more_likely_to_listen_to_your_counsel."),

("trait_title_merciful", "Merciful"),
("trait_desc_merciful", "You_have_aquired_a_reputation_for_merciful_treatment_towards_the_evil_men_who_serve_the_Enemy._Many_of_the_hardened_men_who_serve_you_are_conflicted_by_your_behavior_and_suffer_a_morale_penalty._Among_the_wise,_however,_your_mercy_is_seen_as_evidence_of_high_character_and_you_recieve_an_influence_bonus."),

("trait_title_bravery", "Bravery"),
("trait_desc_bravery", "You_have_aquired_a_reputation_for_bravery_in_the_face_of_great_danger._Your_courage_is_spoken_of_in_both_quiet_taverns_and_the_halls_of_the_wise._Your_deeds_inspire_your_men_and_they_recieve_a_weekly_morale_bonus."),

("trait_title_oathkeeper", "Oathkeeper"),
("trait_desc_oathkeeper", "You_have_sworn_grim_oaths_and_lived_to_see_them_fulfilled._Subsequently_you_have_aquired_a_reputation_as_a_man_of_his_word._You_receive_a_weekly_influence_bonus."),

("trait_title_oathbreaker", "Oathbreaker"),
("trait_desc_oathbreaker", "You_have_sworn_grim_oaths_and_failed_to_see_them_through_to_their_conclusion._Subsequently_you_have_aquired_a_reputation_as_a_man_whose_passion_outstrips_his_prowess._You_receive_a_weekly_influence_penalty."),

("trait_title_orc_pit_champion", "Orc_Pit_Champion"),
("trait_desc_orc_pit_champion", "You_have_become_renowned_as_a_brutal_warrior_who_was_able_to_survive_the_cruelest_of_the_orcish_fighting_contests._Such_strength_is_both_respected_and_feared_by_your_black_hearted_followers_and_they_now_receive_a_weekly_morale_bonus."),

("trait_title_despoiler", "Despoiler"),
("trait_desc_despoiler", "You_have_aquired_a_reputation_for_leaving_behind_wanton_destruction_wherever_you_travel._Such_behavior_is_valued_by_the_dark_powers_you_serve_and_your_receive_a_weekly_influence_bonus."),

("trait_title_accursed", "Accursed"),
("trait_desc_accursed", "You_sense_that_you_have_drawn_the_ire_of_powers_beyond_the_sea._Your_followers_sense_this_doom_as_well_and_fear_being_around_you._They_receive_a_weekly_morale_penalty."),

("trait_title_stealthy", "Stealthy"),
("trait_desc_stealthy", "You_have_developed_uncanny_skill_in_the_art_of_stealthy_infiltration._You_receive_a_bonus_to_your_stealth_rating_when_undertaking_such_missions."),

("trait_title_berserker", "Berserker"),
("trait_desc_berserker", "After_many_battles_where_you_eschewed_the_use_of_armor_your_ferocious_will_has_become_like_iron._While_fighting_lightly_armoured,_each_slain_foe_fills_you_with_grim_vigor."),

("trait_title_infantry_captain", "Infantry_Captain"),
("trait_desc_infantry_captain", "You_have_developed_uncanny_skill_in_the_command_of_infantry_troops._Due_to_rigorous_and_specialized_training_such_troops_will_receive_a_small_health_boost,_once_per_battle."),

("trait_title_archer_captain", "Archery_Captain"),
("trait_desc_archer_captain", "You_have_developed_uncanny_skill_in_the_command_of_missile_troops._Due_to_rigorous_and_specialized_training_such_troops_will_receive_a_small_health_boost,_once_per_battle."),

("trait_title_cavalry_captain", "Cavalry_Captain"),
("trait_desc_cavalry_captain", "You_have_developed_uncanny_skill_in_the_command_of_mounted_troops._Due_to_rigorous_and_specialized_training_such_troops_will_receive_a_small_health_boost,_once_per_battle."),

("trait_title_command_voice", "Command_Voice"),
("trait_desc_command_voice", "Your_experience_with_commanding_men_in_the_field_has_lent_you_an_air_of_authority._The_influence_cost_to_give_orders_to_armies_in_the_field_has_been_reduced."),

("trait_title_foe_hammer", "Foe_Hammer"),
("trait_desc_foe_hammer", "Having_slain_many_of_the_great_captains_of_the_enemy_you_find_that_you_have_earned_a_reputation_as_a_fearsome_warrior._Troops_under_your_command_now_receive_a_weekly_morale_bonus._Your_experiences_have_also_honed_your_skill_in_battle."),

("trait_title_battle_scarred", "Battle_Scars"),
("trait_desc_battle_scarred", "You_have_suffered_horrific_wounds_during_your_many_campaigns_yet_you_still_live_to_tell_the_tale._Your_scarred_and_knotted_flesh_now_conspires_with_hard_experience_to_increase_your_resistance_to_injury._While_others_may_find_your_appearance_somewhat_shocking_your_followers_consider_it_an_affirmation_of_your_battle_experience._They_subsequently_receive_a_weekly_morale_bonus."),

("trait_title_fell_beast", "Fell_Beast"),
("trait_desc_fell_beast", "Your_hide_is_riven_with_the_knotted_scars_of_countless_battles_and_your_evil_will_is_likewise_hard_and_unyielding._Even_by_the_standards_of_orc,_uruk_and_troll-kind_you_are_judged_a_fell_and_dangerous_beast._Those_who_serve_you_cry_your_name_in_joy_when_you_take_to_the_field._You_are_an_avatar_of_war_itself_and_there_is_little_you_fear."),

("trait_title_butcher", "Butcher"),
("trait_desc_butcher", "Experience_has_honed_your_skill_in_extracting_more_meat_from_the_flesh_of_your_enemies._You_gain_an_extra_pound_of_flesh_every_time_you_slaughter_one_of_your_prisoners_for_meat._You_also_get_more_human_meat_after_every_battle."),

("trait_title_well_travelled", "Well-Travelled"),
("trait_desc_well_travelled", "On_stone_paved_roads_and_mossy_animal_paths,_over_the_tallest_mountains_and_in_the_deepest_vales,_you've_discovered_hidden_places_and_seen_long_forgotten_marvels._From_your_experiences,_you've_learnt_to_spot_enemies_before_they_see_you,_and_the_easiest_route_for_your_troops."),

("trait_title_bear_shape", "Skinchanger"),
("trait_desc_bear_shape", "It_is_said_that_men_of_Beorn's_line_have_the_ability_to_take_bear_form._Through_your_kinship_with_bears_you_have_discovered_that_you_too_have_that_gift."),

# END Traits

# BEGIN Wound Strings
# These are used for reporting injuries. :) -CC

("wound_head", "a_heavy_blow_to_the_head"),
("wound_chest", "some_cracked_ribs"),
("wound_arm", "a_badly_maimed_arm"),
("wound_leg", "a_badly_maimed_leg"),

# END Wound Strings
# BEGIN Gifts (Faction order must be kept) -(CppCoder & Merlkir)

("gondor_gift0", "Fresh Fruit and Wine"),
("gondor_gift1", "Richly Dyed Cloth"),
("gondor_gift2", "Ancient Tomes and Family Trees"),
("gondor_gift3", "Spices and Incense"),
("gondor_gift4", "Auroch War Horns"),

("dwarf_gift0", "Strong Beer and Rock Salt"),
("dwarf_gift1", "Hardened Shovels and Axes"),
("dwarf_gift2", "Harps and Flutes"),
("dwarf_gift3", "Robes Embroidered With Golden Thread and Gems"),
("dwarf_gift4", "Marvellous Jewelry"),

("rohan_gift0", "Mead and Apple Wine"),
("rohan_gift1", "Embroided Tunics and Silver-Studded Belts"),
("rohan_gift2", "Golden Torcs and Engraved Drinking Horns"),
("rohan_gift3", "Fine Horse Barding"),
("rohan_gift4", "Rohan Horses"),

("mordor_gift0", "Weak Peat Beer"),
("mordor_gift1", "Snaga Oil"),
("mordor_gift2", "Mordor Fly Larvae"),
("mordor_gift3", "Orodruin Obsidian"),
("mordor_gift4", "Farmer Slaves"),

("isengard_gift0", "Dried Human Meat"),
("isengard_gift1", "Black Iron Chains"),
("isengard_gift2", "Tools of Torture"),
("isengard_gift3", "Alchemist Glasswork"),
("isengard_gift4", "Saruman's Petty Rings"),

("lorien_gift0", "Seeds, Nuts and Berries"),
("lorien_gift1", "Cold Lanterns and Strong Rope"),
("lorien_gift2", "Lembas"),
("lorien_gift3", "Silver Belts and Broaches"),
("lorien_gift4", "Elven Cloaks"),

("imladris_gift0", "White Bread and Herbal Butter"),
("imladris_gift1", "Crystal Glassware"),
("imladris_gift2", "Miruvor"),
("imladris_gift3", "Embroidered Banners and Silver-Inlaid Horns"),
("imladris_gift4", "Healing Herbs and Ointments"),

("woodelf_gift0", "Soft Animal Hides"),
("woodelf_gift1", "Arrow Heads and Fletching"),
("woodelf_gift2", "Hunting Spears"),
("woodelf_gift3", "Trained Birds of Prey"),
("woodelf_gift4", "Drinking Cups of Red Gold"),

("dale_gift0", "Semi-Precious Stones and Glass Beads"),
("dale_gift1", "Codexes of Heroic Sagas"),
("dale_gift2", "Dorwinion Wine"),
("dale_gift3", "Luxurious Furs"),
("dale_gift4", "Intricate Toys and Instruments"),

("harad_gift0", "Figs and Pomegranates"),
("harad_gift1", "Warrior Necklaces"),
("harad_gift2", "Carved Ivory"),
("harad_gift3", "Sacred Snake Wine"),
("harad_gift4", "Golden Serpent Statues"),

("rhun_gift0", "Waterskins"),
("rhun_gift1", "Tattoo Ink"),
("rhun_gift2", "Headgear with Horns and Antlers"),
("rhun_gift3", "Horsehair Whips"),
("rhun_gift4", "Horse Meat and Milk"),

("khand_gift0", "Colourful Spices"),
("khand_gift1", "Rolls of Silk"),
("khand_gift2", "Hunting Falcons"),
("khand_gift3", "Ingots of Water Steel"),
("khand_gift4", "Sacred Warrior Masks"),

("umbar_gift0", "Oysters and Sea Salt"),
("umbar_gift1", "Whalebone Combs and Fishing Hooks"),
("umbar_gift2", "Pleasure Slaves"),
("umbar_gift3", "Sailing Maps of the Southern Seas"),
("umbar_gift4", "Mysterious Numenorean Schematics"),

("moria_gift0", "Putrid Dwarven Ale"),
("moria_gift1", "Coal"),
("moria_gift2", "Luminescent Deep-Worms"),
("moria_gift3", "Black Cave Pearls"),
("moria_gift4", "Dwarven Metal Scraps"),

("guldur_gift0", "Black Liquor"),
("guldur_gift1", "Poisonous Vines of Torture"),
("guldur_gift2", "Wheeled Slave Cages"),
("guldur_gift3", "Giant Spider Eggs"),
("guldur_gift4", "Tomes of Dark Sorcery"),

("gundabad_gift0", "Spiky Bone Piercings"),
("gundabad_gift1", "Protective Warpaints"),
("gundabad_gift2", "Boiled Dwarven Lard"),
("gundabad_gift3", "Mummified Corpse Idols"),
("gundabad_gift4", "Black Wargs"),

("dunland_gift0", "Stinky Goat Cheese"),
("dunland_gift1", "Flint Sacrificial Knives"),
("dunland_gift2", "Bronze Arm Rings"),
("dunland_gift3", "Goats"),
("dunland_gift4", "Wolf Skulls and Claws"),

("beorn_gift0", "Honey Cakes and Mead"),
("beorn_gift1", "Bee Wax and Hemp Cloth"),
("beorn_gift2", "Bee Hives"),
("beorn_gift3", "Amber Necklaces"),
("beorn_gift4", "Well Trained Ponies"),

# END Gifts

("cmenu_follow", "Accompany"),
("fake_party",   "TLD temp terrain finder, you shouldn't be seeing this in a savegame [!]"),

("reset_to_default", "Reset to Default"),
("done", "Done"),
  
# Kham - Armor Customization Strings

# Padded Cloth Begin
("gondor1", "Gondor1"),
("gondor2", "Gondor2"),
("gondor3", "Gondor3"),  
("gondor4", "Gondor4"),
("gondor5", "Gondor5"),
("gondor6", "Gondor6"),
("gondor7", "Gondor7"),  
("gondor8", "Gondor8"),
("gondor_end", "Gondor1"),

# Custom Armour END 

# Intro Strings
("gondor_intro", "^It is a bitter thought, that a hero of this great kingdom should die within the sight of his land, unaided and helpless.^^\
The news of Boromir’s death passed like a swift wind through all of Gondor, even to the plains of Pinnath Gelin and the hills of Lamedon, even to the shores of Pelargir and the coasts of Dol Amroth. The hearts of all your people are filled with grief and pity; and more besides, with fear and foreboding, for Gondor is hard pressed and sore beset, ringed by implacable foes or uncertain friends.^^\
The Shadow rises in the East, as of old; the fractious Corsairs of Umbar grow bolder; the wild men of the East and South press their claims upon Gondorian land.^^\
No longer can you stand by and wait. Trust you have placed in your captains; sword and spear they will place in your hand. Gondor wanes, but Gondor still stands; and even the end of its strength is still very strong. You have resolved yourself to play what part you may in this coming war against the servants of the Nameless. Much is spoken of in the councils of the great and wise, to which you are not privy, but there is one thing you feel you can be sure of.^^\
If the valiant hearts of Gondor should fail, and Minas Tirith be lost, then the last light of the West will be extinguished. All will fall beneath the Shadow."),

("dwarf_intro", "^The Kingdom under the Mountain has done well, of that there can be no dispute. Old King Dáin has just passed his two hundred and fiftieth year, and by any measure he is fabulously wealthy. Under his rule, Erebor thrives, and knows greatness. The waterways, fountains and pools of neighbouring Dale bear witness to how your builders have surpassed the skill of even your forefathers, though their secrets of metalwork have regrettably been lost.^^\
Yet a darkness from Mordor entered these halls, when Sauron’s foul envoy, with his breath like the hiss of snakes, came bearing evil words. Heavy have been the hearts of your chieftains since then, for the power that has re-entered Mordor has not changed. The Shadow grows and draws nearer - already the Enemy is moving, and war will soon begin.^^\
You have sworn to take up arms, and stand with your friends against your foes. You will resist, with hope or without it.^^\
But if the bravery of the Dwarves of Erebor should prove insufficient, then the glory of Durin’s folk will fade away and be forgotten. All will fall beneath the Shadow."),

("rohan_intro", "^In these days of doubt, one thing you know to be true: open war lies before the proud people of Rohan. None may live now as they have lived, and few shall keep what they call their own. Some close to the King’s ear speak craven counsels, but you have determined to go to him, take a grim oath of service, and stand with such fell-handed captains and thanes as will protect the herds and herdfolk.^^\
Saruman of Isengard has declared lordship over the lands of Rohan, and bitter is the fighting with Orcs, Wolf-riders and the evil Men of Dunland. The Lord of the Black Land to the east sends raiding parties to steal your horses, choosing always the black ones. Your heart misgives you, for it seems to you that enemies beset your people both east and west.^^\
But still you will give battle, for if aught is said of the Rohirrim, it is of your unfailing valour in arms, though foe should beleaguer you, or fire encircle you. The steeds of Rohan will stride as wind in the morning. And if death should come for you, then a mound will be raised, but for now, war calls you. Let horse be bridled, horn be sounded!^^\
Yet, if even the courage of the Sons and Daughters of Eorl should fail, then the last hope of Rohan will fade and die away. The horn will blow no more. All will fall beneath the Shadow."),

("mordor_intro", "^The dark power rises again in the East. The numbers of the Dark Lord’s legions swell - Easterling men come to serve and pay tribute, hollow-eyed renegades from ancient Numenor craving a chance to regain what their ancestors lost, great hosts of orcs and uruks slavering at the thought of war and killing. The pens are filled with ferocious, fearsome wargs. And high above, in the black skies, fly the winged Nazgûl… the apple of the Great Eye, with power deep beyond the reach of your muddy dreams.^^\
You have resolved to rise in the ranks, by any means, and gain the favour of Lugbúrz. By wit, hardiness, and ruthless skill in battle you shall crush all who stand in your way. You will earn the favour of the Dark Lord of Mordor, he who is to rule all after this coming War… or you will die trying.^^\
The light of the West shall be snuffed out. The time of Mordor has come!"),

("isengard_intro","^A new power is rising, and you are part of that power. You march and fight under the banner of the White Hand, and your allegiance is sworn to crafty old Saruman the Great, wise and cunning, who gives you the tasty flesh of man and horse to eat.^^\
Under his banner march the fighting Uruk-hai. They are slayers of great warriors, winners of battles. Their armour is thick and their shields broad. You will make a name for yourself among your fellows, and hew down many Whiteskins. You will not stop, by sun or moon, by fair weather or storm, until your enemies lie dead and broken.^^\
The skill of Saruman is great. With it, you will throw down the power of the horse people, and their weak allies; yes, even elf-flesh will be yours to feast upon. Their villages and forests will burn, and their cities too. And then… who is to say if the maggots and apes of Lugbúrz will not defer to the mighty ones of Orthanc, eh? The strong command. The weak will serve.^^\
The Age of Man is ending. The time of Isengard has come!"),

("lorien_intro", "^It is the custom of your people, the Galadhrim of Laurelindórenan, to dwell in the treetops. The great trees of mighty girth bear leaves of gold and blossoms of yellow, and by the waters of the Nimrodel one may find restful sleep and forgetfulness of grief; but in these darkening days none may long forget the Shadow that hovers near, pressing in from the east, from the dark land of Mordor and nearer still.^^\
For many a long year, your kin of Lothlórien have had few dealings with other folk. Indeed in nothing is the power of the Dark Lord more clearly shown than in the estrangement that divides those who still oppose him. Yet you are one of those who can perceive that to keep living thus, an island amid many perils, will bring only despair. Some there are among you who sing that the Shadow will draw back, and peace shall come again; and though the world can never be as it was of old, yet will you take up sword and bow, and play your part in the War to come, to defend not only the Dreamflower that you love, but perhaps lands beyond, that will otherwise fall to evil.^^\
For if the old friendships are not renewed, and thought is taken only to fight the long defeat, then shall the last light of Lórien go out forevermore. All will fall beneath the Shadow."),

("imladris_intro", "^Alas, for these latter days of grieving memory! In Imladris, the homely house of Elrond Halfelven, one may recall somewhat of the glory and splendour of Eregion in the Elder Days. But the world will never again be as it was of old.^^\
The fields of Eriador, though lovely to behold, are tilled no more by the hands of Men. The Dúnedain, much diminished in number after the breaking of Arnor, keep their lonely vigils in the desolate wilderness of the North. And the days of Gil-Galad are forever gone, for the Firstborn decrease, and go into the west, while the blood of ancient Númenor dwindles and the race of Westernesse decays.^^\
Though Rivendell remains a place of sanctuary, the days darken in all the lands around.^^\
A last rallying call has gone forth, and a great host from Imladris - perhaps the last such in all the Ages of the world - shall march. You are part of this host, and though you will do your duty as instructed by the wise and the great, your heart is not without misgivings. Neither in Imladris, nor in the Grey Havens, nor even in Lórien the Golden Wood, is there strength to withstand the full might of the Enemy, should it come assailing when all else is overthrown.^^\
Yet a slim hope remains: if the old friendships can be renewed, and all who stand against evil join strength against the common foe, some time may yet be won, so that the final end of the menace of Mordor may yet be sought.^^\
But if the old alliances should fail, and old friends come to ruin, then nothing shall be left but the days of lengthening darkness, before true Night comes. All will fall beneath the Shadow."),

("woodelf_intro", "^A shadow lies over the Woodland Realm, a poison spreading through the air itself from Dol Guldur. The Lord of Mordor has returned to his dark tower, and his lieutenants in Dol Guldur have turned much of Greenwood the Great, Eryn Galen, into places of great fear, where even your people, the Silvan Elves of the north, will not freely go.^^\
Thranduil son of Oropher leads your people, but has been cautious in his policy - fresh is the grief of Dagorlad, perhaps, to his memory. Yet, now that the men of Dale are threatened by the coming war, your king has roused himself. Ever does he look to the south with a deep shadow in his heart, and long will he tarry ere he leads his people into likely ruin, but the day of decision is upon him.^^\
With spear and blade and bow, you will defend the borders of your realm at your king’s command - and if need be, you are resolved to aid any who would stand against the common foe alongside the Elves of Mirkwood.^^\
For fear speaks in your heart, as it does for many of your fellows, that if the old friendships are not renewed, and old allies come to ruin, then Mirkwood shall be darkened forever. All will fall beneath the Shadow."),

("dale_intro", "^For three generations of men, the Kingdom of Dale has prospered. King Brand, grandson of Bard the Bowman, rules justly, and trade has enriched the realm.^^\
But enemies now encroach, gathering across the border to the east - fractious, quarrelsome nomads, with whom speech is difficult and trust harder still. Toys and bells and pretty dolls must now be set aside, for spear and bow and sturdy shield. Trees must be hewn not for the walls of a new steading, but for quivers and the arrows to fill them with. Young men go not to till the fields or harvest the orchards, but to the barracks, to war and a red dawn.^^\
Yet Dale has stalwart allies: the Dwarves of the Lonely Mountain, whose masonry decorates every street of Dale. And, too, the Elves of Mirkwood have had traffic with your people, to the good of all. The stout Beornings of the Ford keep the trade routes safe and open. In these dark days, all who reject the overlordship of Mordor must stand together, or be singly cut down like wheat stalks in the field.^^\
You have resolved to do your part, for if the steadfast defenders of Dale should fail, then the line of Bard will be ended, and the last kingdom of Men in the north will be no more. All will fall beneath the Shadow."),

("harad_intro", "^From the deep deserts, the thick jungles and the sun-soaked riverlands, we have come. Let the people of Gondor stand in awe of us, and make submission.^^\
They have said that the lands south of the river Poros are theirs by ancient right, and they therefore call it Harondor, “South Gondor”, and call us invaders. This their claim, we have not understood. Was it not in the time of the Plague that the Great Serpent made his will known in driving the Gondorians out by death and illness, and allowed our forefathers to settle there and grow in numbers? How could any men, without the blessings of the Powers and merely from their own strength, claim this land? Did our ancestors not live here, when theirs died or left?^^\
Furthermore, they have said that in times long past they first gave us crafts and the skill of growing food upon the land; therefore we should become as vassals unto them. This, too, we have not understood, for well our learned men remember the days of their king Tar-Ciryatan and those after him who took from our people much tribute, and plundered for themselves the richest treasures of our lands. And when they behave arrogantly, saying, “Be grateful, and pay tribute to the Steward of Gondor,” having no king for many long years by reason of immense foolishness, how do they dare to press their claims upon us?^^\
We like not the company of foul orcs, and the Dark Sorcerer demands great sacrifice. Many young men and women we have given up to him, in the Dark Land, and still he wants more. Yet, with his power and aid, all the lands from the rising of the sun to its setting shall come to us, and we shall own them.^^\
The Age of Gondor is ending. Let battle be joined!"),

("rhun_intro", "^The wagon cities of your people have roamed the high steppes for many moons. Your chieftains have taken counsel from the power that has once again risen in the land of Mordor. They promise many things to you and your fellow warriors: they will avenge the defeat of the Wainriders and the humiliation of the Balchoth; they will wipe clean for once and all the stain of Gondorian rule, under the ancient kings who had the audacity to name themselves “Vanquishers of the East”; they will win for the clans many slaves and much wealth.^^\
They say many things, but you know you do not fight for a life of ease, like the fat and weak Lake-people, or the short greedy diggers scurrying around in their tunnels of stone, or the cowardly elves skulking in the trees singing songs.^\
All that matters is glory, won in battle, and it is not the promises of chieftains that will win you a place of honour on the great Mountain after you die; it is by skill and strength that you will win the right to stand there. If you must fight alongside filthy honourless Orcs for a time, so be it - but your deeds will be your own, and they will be told over and over, around the campfires, for many generations to come.^^\
The Age of the West is ending. The time of the East has come!"),

("khand_intro", "^The strong rule, and the weak serve. This truth is known to your people, the people of Khand, from birth. Boys and girls alike must survive the fighting pits for many moons, before they may take their place among grown men and women. Such ways have made your people strong. Little wonder, then, that the Lord of the Black Land speaks so fairly to your Shibh! He knows a single sharp halberd in the hands of a Variag of Khand is worth twenty spears in the hands of worthless orcs.^^\
Many promises have been made to your leaders. A great host has been assembled, the greatest yet in living memory. From the farthest reaches of your lands, the fiercest fighters among your people have answered the summons. You will plunder the lands of the weak, decadent Gondorians. You will take many of them as slaves, and make them work their rich green lands for you, as is the right of the conqueror.^^\
The Age of the West is ending. The time of the East has come!"),

("umbar_intro", "^The puffed-up nobles in Gondor, so proud of their vast and fertile estates, are sitting on stolen land - it was Castamir, of old, who was rightful king of the realm, before his throne was usurped by faithless curs. His descendants have led your nation well, winning many great victories on the seas and the coasts.^^\
Time and again, however, the bitter winds of defeat have blown in your face - some years ago, the faithless Gondorians launched a cowardly night attack upon the main haven, sending the better part of Umbar’s strength down to the sea floor. Your ship was lost, your captain with it, and you were among the few survivors of your erstwhile crew.^^\
But fifty great ships remain, and countless smaller vessels besides. The Dark Lord of Mordor has issued the call. Now is the time for a reckoning. You will join hands with your brothers-in-arms of the Southern lands, the grim-eyed men of Harad, and you will exact your vengeance upon the treacherous men of Gondor, until all Belfalas and Anfalas is in flames, and your coffers overflow with the wealth that is rightfully yours.^^\
The Age of Gondor is ending. The time of Umbar has come!"),

("moria_intro", "^You have come from the Mines, to avenge your folk, killed by manlings and diggers and elf scum! Your tribe was strong, and rich - the Moria-silver you gathered, in great heaps, and with it won great favour from the Dark Lord in the East. The short ones came, thinking to make their homes here - but you slaughtered them and had great sport in the doing. Then a small band of thieves and brigands came through, and awoke the deep Fire. Ruin, ruin for all! Many places cannot now be reached. Much wealth, much Moria-silver, and all too deep to dig up!^^\
But now the Dark Lord calls. War comes. The Great Eye will reward faithful servants, yes. He will remember who it was who sent him so much of this shiny Moria-silver, and you will obey him - you will kill, and feast upon the Whiteskins, and all will be well for you and your tribe. And those proud elves, in their golden forest, they won’t be so proud when you and your folk burn their trees down around them!^^\
The light in the woods shall be snuffed out. The time of Moria has come!"),

("guldur_intro", "^The dark power rises again in the East. The Lord of Barad-dûr has sent his servants to Dol Guldur, where his will once more shall hold sway. The forges overflow with weapons and armour, the pens house thousands of ferocious wargs, the barracks are full to the brim with orcs ready to fight and die.^^\
And high above, in the darkening skies over Mirkwood, fly the winged Nazgûl… the apple of the Great Eye, with power deep beyond the reach of your muddy dreams. No fewer than three has the Dark Lord sent to this place, from which his power will reach, subduing all who resist, until the enemies of Mordor are broken forever.^^\
You have resolved to rise in the ranks, by any means, and gain the favour of Dol Guldur and Lugbúrz. By wit, hardiness, and ruthless skill in battle you shall crush all who stand in your way. You will earn the favour of the Dark Lord, he who is to rule all after this coming War… or you will die trying.^^\
The shadow of Dol Guldur shall spread. The light of the West shall be snuffed out. The time of Mordor has come!"),

("dunland_intro", "^Your people have known nothing but foul injustice at the hands of the black-hearted Forgoil, the strawhead paleskins of Rohan. From the time of mighty Freca, felled by a cowardly blow from the man-eater beast Helm, he whom the Rohirrim called Hammerhand, you have suffered grievously under their heavy yoke. High-handed are their treacheries, too many to number.^^\
 But now the wind is changing. Wise Saruman, the cunning old master of Isengard, has made promises of friendship to your people. With his help, surely the claim of noble King Wulf, who in happier days rightfully sat the throne of Meduseld in Edoras, will be upheld.^^\
No longer will your people scrabble in the rocky soil for a hard living. No longer will babes in arms die in the embrace of their mothers, because the milk flows too weakly. No longer will your people cower in fear of the murdering usurpers of Rohan. Your pikes are long, and your axes cruel and sharp. With the help of Saruman the Wise, you cannot fail. You will take back what is rightfully yours.^^\
You will fight for Saruman. You will die for Saruman!"),

("beorn_intro", "^These woods, these old paths, and the Ford are the only home you have ever known, but old Beorn was one who remembered an older home, far away in the mountains. His son, Chief Grimbeorn the Old, now stands foremost among your people, and like his father, he is apt to sit on the great Carrock at night, setting his sight to the west, deep in his own thoughts.^^\
For your part, your thoughts are simple. The woods grow dangerous. Foul orcs grow bolder, and walk about even in daylight. The wolves they ride will not listen even to one of your people, so twisted have they become by goblin ways. The air feels and smells different, bad. The further south you go, closer to Dol Guldur, where not so long ago the Sorcerer dwelled and did things unworthy of naming, the worse it gets.^^\
The Elves huddle in their caves to the north. Most will not come out to protect the woodland, its animals and trees and other things that move and live.^^\
Your people will fight, as you always have, to keep the Ford and the forest safe. With a stout stick in your hands, you will smash any orcs that dare intrude. And if it should come to greater blows, why, many among your people are more than they seem…^^\
But if even the grim battle-strength of the Beornings should fail, then the world will know no more the joy of sweet honey, bright flowers, shady forest paths and all things good. All will fall beneath the Shadow."),

("intro_strings_end", "Intro END"),

("gondor_intro_2","^While travelling to swear service to your liege lord, you chance upon a caravan being attacked by orcs."),
("dwarf_intro_2","^On your way to the gates of Erebor, you chance upon a caravan being attacked by orcs."),
("rohan_intro_2","^On your way to Edoras, you chance upon a caravan being attacked by orcs."),
("mordor_intro_2","^On your way to the Morannon to report to Lugbúrz, you chance upon some orcs raiding a caravan."),
("isengard_intro_2","^On your way to Isengard, you chance upon some orcs raiding a caravan."),
("lorien_intro_2","^On your way to Caras Galadhon for an audience with the Lady Galadriel, you come upon some allies preparing to ambush a company of Orcs."),
("imladris_intro_2","^On your way back to the main Rivendell camp after a scouting mission, you come upon some allies preparing to ambush a company of Orcs."),
("woodelf_intro_2", "^On your way back to the Elvenking’s Halls after a patrol in the woods, you come upon some allies preparing to ambush a company of Orcs."),
("dale_intro_2","^On your way to the city of Dale, you chance upon a caravan being attacked by orcs."),
("harad_intro_2", "^Your fellow warriors and riders, as well as the mighty Mûmakil, have established your main camp across the river from the fortified city of the Gondorians, the one they call Pelargir. No doubt when it falls, your chieftains will think of a more fitting name for it. Then shall you hold it forevermore against the dwindling men of the West.^^\
As you walk through a wooded vale, a sudden small rustling makes you stop. You have heard many tales of the Gondorians who skulk around in these lands, sneaking like cowards - Rangers, they are called. They are deadly with the bow and arrow, like the Gold Serpents of high renown. Are some of them preparing to ambush your party? You had better sound the warning!"),
("rhun_intro_2","^On your way to the main battle-camp of your people, you chance upon some orcs raiding a caravan."),
("khand_intro_2","^Your fellow Variags have been summoned to the Morannon, the Black Gates that lead into Mordor. You do not relish having to camp so near to filthy honourless orc-kind, but for a time you will oblige. Still, the Lord of Mordor would be foolish indeed not to recognise the worth of your people, and treat you accordingly!^^\
As you walk through a wooded vale, a sudden small rustling makes you stop. You have heard many tales of the Gondorians who skulk around in these lands, sneaking like cowards - Rangers, they are called. They are deadly with the bow and arrow. Are some of them preparing to ambush your party? You had better sound the warning!"),
("umbar_intro_2", "^On your way to where the Admiral has established the beachhead fortifications, you chance upon some orcs raiding a caravan."),
("moria_intro_2", "^While returning from a scouting mission in the dale, you chance upon some orcs raiding a caravan."),
("guldur_intro_2","^On your way to Dol Guldur, you chance upon some orcs raiding a caravan."),
("gundabad_intro_2", "^On your way to Mt. Gundabad, you chance upon some orcs raiding a caravan."),
("dunland_intro_2","^On your way to the main battle-camp of your people, you chance upon some orcs raiding a caravan."),
("beorn_intro_2", "^On your way to Beorn’s House, you come upon some allies preparing to ambush a company of Orcs."),

("intro_strings_2_end", "Intro 2 END"),

("gondor_faction_intro","^The South Kingdom of Gondor, “land of stone” in Sindarin, is inhabited by descendants of the ancient Númenoreans. Under the rule of Steward Denethor, these proud men stand as the first and perhaps last line of defence against the Enemy.^^\
Gondor’s military consists of forces coming from all the different fiefdoms. You get the standard army with solid and well-armoured troops overall: Dol Amroth’s heavy cavalry, green-clad archers and spearmen from Pinnath Gelin, bowmen from the Blackroot Vale, axemen of Lossarnach, heavy marines from Pelargir or hardened clansmen of Lamedon."),

("dwarf_faction_intro","^Dwarves, also known as Durin’s Folk, are short, tough and doughty warriors. They are renowned for the craftsmanship of their weaponry and armour, though they say with regret that they cannot match the lost arts of their ancestors. In these latter days, they come from the Lonely Mountain and the Iron Hills.^^\
Their army consists of an infantry line, a scout/archer line and an Iron Hills line (their heaviest hard-hitting infantry)."),

("rohan_faction_intro","^Rohirrim are the horse lords of the Mark of Rohan, led by king Théoden.^^\
Rohirrim have very good cavalry, ranging from heavy lancers to agile horse archers. They have an infantry line as well, branching into shieldwall-forming troops and heavy swordsmen bearing longswords."),

("mordor_faction_intro","^Mordor represents Sauron’s own forces bred in the darkness of the Black Land.^^\
Armies of Mordor consist of orcs, Uruks and evil men (Black Númenoreans). Uruks of Mordor are a better-equipped and stronger breed of orcs, but have no archery line. Most regular orcs are infantry, skirmishers or archers, but there are also orc warg-riders. Black Númenoreans are comparatively rare, but very dangerous as infantry or cavalry. Sauron has also bred fierce battle trolls, but they’re extremely hard to obtain."),

("isengard_faction_intro","^Isengard is ruled by Saruman, the traitor wizard. He created his own version of orcs: the Uruk-hai.^^\
The forces of Isengard are quite well-equipped, though the weapons and armour may seem crude. The orcs are comparable to any other orcs, but the Uruk-hai are truly deadly killing machines wielding pikes, halberds, heavy axes and nasty cleavers. They also have the largest and most powerful bows among any of the orcish races."),

("lorien_faction_intro","^The Elves of Lothlórien, known as the tree-dwelling “Galadhrim”, are a powerful group of Nandor and Sindar living in the Lórien woods, led by Lord Celeborn and Lady Galadriel.^^\
Their forces consist of an infantry line and a scout line, with the occasional incorporation of an elite unit of Noldorin horse archers. All their troops are highly skilled, equipped with the finest arms and armour of Elven make, and overall extremely deadly in combat. A rain of arrows from under the forest cover, followed by a devastating infantry charge, is their main tactic."),

("imladris_faction_intro","^The Elves of Imladris (Rivendell) are Sindar and Noldor led by Lord Elrond and his two sons. They are custodians of the ancient lore of the west, as well as powerful and ancient artifacts dating back to the First Age. Under their banner, the Dúnedain of the North march as well – the remnants of the broken Northern kingdoms of Men are tall dark-haired rangers and nobles, clad in sturdy leathers or ancient maille.^^\
The soldiers of Imladris are among the most highly-skilled in Middle-Earth, and are extremely well-equipped. Their armies are capable of considerable tactical flexibility."),

("woodelf_faction_intro", "^The Silvan Elves, called “wood-elves” in ancient times, live today in Mirkwood, led by King Thranduil.^^\
The Elves of Mirkwood have a competent infantry line that features both spears and swords. Their scouts and archers are the mainstay of their armies, more so than for their cousins of Lórien. Their armour is light but affords a great deal of protection."),

("dale_faction_intro","^Dale is a city rebuilt by Northmen who share ancestry with the Rohirrim, joined by the survivors from the lake city of Esgaroth (after it was burnt down by Smaug).^^\
Men of Dale provide tough infantry focused on polearms, famous archer troops including the legendary Barding bowmen, and a merchant guard line acting as reasonably good cavalry."),

("harad_faction_intro", "^The Haradrim, the “hosts of the South” in Sindarin, come from the deserts and rainforests of the far South. They have a fondness for wearing bright colours and heavy gold ornamentation in warfare.^^\
Haradrim have average but competent infantry (skirmishers/archers and spearmen/swordsmen) from Great Harad, a cavalry line (incorporating both heavy cavalry and horse archers) from Harondor and a Far Harad line of tribal warriors."),

("rhun_faction_intro","^Men of Rhûn are tribal Easterlings hailing from around the sea of Rhûn, far to the east.^^\
The bulk of their army is cavalry - horse archers and lancers, both very lightly-equipped. Their top-tier cavalrymen ride much larger and heavier mounts, with more barding. Their infantrymen are also quite lightly-armoured and wield large axes and swords. In the open field, a cavalry host of Rhûn can be a fearsome force to face."),

("khand_faction_intro","^The Variags of Khand are fierce Easterling raiders who wear terrifying battlemasks into battle.^^\
They rely on fast light infantry (skirmishers and blademasters) and heavy axemen, while their cavalry line contains both light agile skirmishers and heavy kataphracts. The light infantry fling devastating volleys of throwing spears while screening the advance of the main host. The most savage among them charge into battle wearing little armour, attacking with great strength and ferocity."),

("umbar_faction_intro", "^The Corsairs of Umbar are southern enemies of Gondor, descendants of the Black Númenoreans who conduct numerous raids on Gondor’s coastlines.^^\
Corsairs employ both lightly-armoured skirmishers and heavier swordmasters as well as skilled longbowmen. Being a mainly seafaring force, they favour armour that sacrifices toughness for mobility."),

("moria_faction_intro", "^Orcs of Moria occupy the halls of Khazad Dúm, once a mighty Dwarven kingdom.^^\
Like regular orcs, their forces consist of a mix of infantry, archers, skirmishers and warg-riders, but generally they have better equipment than other orcs, because they use metal scraps found in Moria. Some lucky few among them also have access to bits of looted dwarven armour and weapons. Orc Chieftains of Moria have proved themselves stronger and fiercer than their kin, and they are fearsome in battle."),

("guldur_faction_intro","^Dol Guldur is an old fortress of Sauron in Mirkwood – indeed, it is the reason “Greenwood the Great” is now known by this darker name.^^\
Here, a contingent loyal to Mordor trains and prepares a great host, sending out frequent raiding parties against the Elves as well as the parties of Men who pass through the woods. The troops of Dol Guldur are mostly orcs, with a lineup very similar to Mordor’s (infantry, skirmishers, archers, warg riders), but with somewhat less variety."),

("gundabad_faction_intro", "^Gundabad was a place sacred to the Dwarves, but in these days it has become a massive Orc stronghold in the northern mountains.^^\
The Gundabad orcs, though more savage than their fellows from other places, fight much like any other orcs, with a similar army lineup (infantry, archers, skirmishers, warg riders). Their equipment is primitive and their fighting style barbaric. Their warg riders are unrivalled in toughness and ferocity. Some among the orcs of Gundabad can even whip themselves into a battle-frenzy."),

("dunland_faction_intro","^The Dunlendings are the “wild men of Dunland”, enemies of the Rohirrim who drove them from their homeland.^^\
Dunland is barren and poor. The Dunlendings wear very little real armour – mostly furs and cured leather, with some metal signifying status. For weaponry, they wield long pikes and antler axes, with rare swords serving as emblems of prestige. Their horses are thin and weak, certainly no match for the steeds of Rohan, though occasionally the Dunlendings will ride them into battle as skirmishers. In battle, the pikemen advance en masse, presenting a crude but formidable wall of sharp polearms. Some Dunlendings have also cultivated affinity with creatures of the wild, and may unleash packs of savage wolves against their foes."),

("beorn_faction_intro", "^Beornings, the descendants of Beorn, are a people of the upper Vales of Anduin, between Mirkwood and the Misty Mountains. They dwell mostly in the forests, though they keep the Old Ford clear for trade, exacting a toll on merchant caravans for their service.^^\
As woodsmen, they wield stout sticks and sharp axes, but wear little in the way of armour. Heavier Beorning infantry fight with shields as well. Beorning foresters are skilled bowmen and provide a valuable archer line."),


("intro_faction_intro_strings_end", "faction intro END"),


("gondor_extra_info","Good^^Hard^^Gondor (South-East)^^Prince Imrahil^^Mordor, Umbar, Khand, Harad"),
("dwarf_extra_info","Good^^Easy^^North Rhovanion (North)^^King Dain II Ironfoot^^Rhun, Gundabad"),
("rohan_extra_info","Good^^Average^^Rohan (South-West)^^King Theoden^^Isengard, Dunland"),
("mordor_extra_info","Sauron^^Easy^^Gondor (South-East)^^Gothmog^^Gondor"),
("isengard_extra_info","Saruman^^Easy^^Rohan (South-West)^^Ugluk^^Rohan"),
("lorien_extra_info","Good^^Very Easy^^South Rhovanion (Center)^^Celeborn^^Moria, Dol Guldur"),
("imladris_extra_info","Good^^Very Easy^^South Rhovanion (Center)^^Lord Elrond^^Moria, Dol Guldur"),
("woodelf_extra_info", "Good^^Very Easy^^South Rhovanion (Center)^^King Thranduil^^Moria, Dol Guldur"),
("dale_extra_info","Good^^Average^^North Rhovanion (North)^^King Brand^^Rhun, Gundabad"),
("harad_extra_info", "Sauron^^Easy^^Gondor (South-East)^^Chief_Ul-Ulcari^^Gondor"),
("rhun_extra_info","Sauron^^Hard^^North Rhovanion (North)^^Jarl Helcaroth^^Dale, Dwarves, Mirkwood, Beornings"),
("khand_extra_info","Sauron^^Easy^^Gondor (South-East)^^Shibh Krukmahur^^Gondor"),
("umbar_extra_info", "Sauron^^Easy^^Gondor (South-East)^^Admiral Tulmir^^Gondor"),
("moria_extra_info", "Saruman^^Very Hard^^South Rhovanion (Center)^^Master Bolg the Lesser^^Imladris, Lothlorien"),
("guldur_extra_info","Sauron^^Very Hard^^South Rhovanion (Center)^^Master Fuinur^^Imladris, Lothlorien"),
("gundabad_extra_info", "Saruman^^Very Hard^^North Rhovanion (North)^^Master Burza Krual^^Dale, Dwarves, Mirkwood, Beornings"),
("dunland_extra_info","Saruman^^Hard^^Rohan (South-West)^^Chief Daeglaf the Black^^Rohan"),
("beorn_extra_info", "Good^^Hard^^North Rhovanion (North)^^Chief_Grimbeorn_the_Old^^Rhun, Gundabad"),

("intro_strings_extra_end", "Intro EXTRA END"),

("gundabad_intro", "You have come from the far north, from the lands of long-lost Angmar, after receiving tidings of the war to come. For years beyond count you and your folk have broken many dwarf shields with your axes and spears, crushed many broken bodies of men and elves below the claws of your fierce wargs, skinned the hides of the bear-people to wear as furs. The great halls of Gundabad in the Misty Mountains are now yours once again, as they were in the time of Bolg and Azog.^^\
Many of you have perished over the years, somemany of them slain in these very halls and tunnels - but many still remain. Great sport you have had with the greedy little diggers and their friends, in the past - and greater sport you will have now, when you march upon them and take everything for yourselves!^^\
Vengeance for Bolg, for Azog, for the Great Goblin - vengeance for the goblins of Gundabad!"),

("show_keybinds", "Special Key Bindings: ^^ Formation Keys:^ Ranks - J ^ Shieldwall - K ^ Wedge - L ^ Square - ; ^ Clear Formations - U ^^ Cycle Through Weapon Usage - O ^^ Cycle Through Camera Type - CTRL+END ^^ Rally - V ^^ Call Horse - M ^^ View Orders / Minimap - Backspace"),

("tactical_controls", "Use the keyboard NUMBERS to select a division. Press 0 to select your entire force.^^\
Use F1-F4 to order selected divisions. Keep the F1 key down to place selected divisions. One may target an enemy division through this mechanism.^^\
Pressing the ENTER key often initiates an overhead Strategy Camera.^^\
Pressing the BACKSPACE key often initiates a Battle Command Display with 'radar.'"),
  ("division_placement", "When ONE division is selected, the center of its front rank is placed at the spot indicated.^^\
When MANY divisions are selected, they are separated and spread out as if the player were standing at the spot indicated.^^\
One may memorize the placement of selected divisions relative to the player by pressing F2, F7. Default is infantry to the left, cavalry right, and ranged forward."),
  ("formations", "The Complex Formations on the Battle Menu are:^^\
- RANKS with best troops up front^\
- SHIELD WALL, ranks with shields in front and longer weapons in back^\
- WEDGE with best troops up front^\
- SQUARE in no particular order^\
- NO FORMATION^^\
Even in the last case, the player can make formations up to four lines by ordering Stand Closer enough times."),

#Dale Walker Customization strings

("dale_coat", "dale_coat"),
("dale_coat_2", "dale_coat_2"),
("dale_coat_3", "dale_coat_3"),
("tld_wear", "tld_wear"),
("tld_wear_2", "tld_wear_2"),
("tld_wear_3", "tld_wear_3"),
("dale_coat_end", "dale_coat_end"),

#Female Materials
("rhunarmortexture_fem", "rhunarmortexture_fem"),
("female_mats_end", "female_mats_end"),
("beornings_female", "beornings_female"),
("khand_light_fem", "khand_light_fem"),


#New Companion Strings

("npc18_intro" , "Great One, hold a moment! I would speak with you!"),
("npc19_intro" , "Hold a moment, Commander. I would have words with you. No, no, you need not kneel, even though you speak to one of royal blood."),
("npc20_intro" , "Wait. You. I've seen you. I know your face. A dream I had, of you - but why would it be you? Now that I see you with mine own eyes, you are little more than a lowly snaga!"),
("npc21_intro", "Welcome to Meduseld, warrior!"),
("npc22_intro", "Hail {playername}. Mae govannen!"),
("npc23_intro", "Leave me alone, stranger, I do not wish to speak to you."),
("npc24_intro", "Kíli, son of Dwalin, at your service!"),
("npc25_intro", "Welcome to Dale, traveller! How can I help you?"),
("npc26_intro", "Ssh! If you so much as wave to the guards, I'll slice out your gizzard and feed it to the wargs!"),
("npc27_intro", "You!"),

("npc18_intro_response_1", "A slave in stocks, bound for death, would speak with me? What have you to say?"),
("npc19_intro_response_1" , "Royal blood you say? Ha! What makes you think you have even a drop of it?"),
("npc20_intro_response_1" , "Look here, what do you mean by this, witch? Who are you?"),
("npc21_intro_response_1", "Greetings, my Lady. With whom do I have the honour to speak?"),
("npc22_intro_response_1", "Hail Elf-lord! It's a great honour to meet you."),
("npc23_intro_response_1", "Is this how the Silvan Elves greet their guests?"),
("npc24_intro_response_1", "{playername} at your service. How fare the Durin's folk?"),
("npc25_intro_response_1", "Greetings. I was wondering if there are any volunteers here to join us in our travels."),
("npc26_intro_response_1", "Hold your threats, Uruk, before it comes to blows - I am not a snitch."),
("npc27_intro_response_1", "Who are you?"),

("npc18_intro_response_2" , "I will not waste words on a slave bound for death."),
("npc19_intro_response_2" , "Impudent wretch. Out of my way."),
("npc20_intro_response_2" , "I have no time for your mad ravings, sorceress."),
("npc21_intro_response_2", "Excuse me, I have urgent matters elsewhere."),
("npc22_intro_response_2", "Excuse me, I have less important people to talk to."),
("npc23_intro_response_2", "The feeling is mutual. Goodbye."),
("npc24_intro_response_2", "Never mind, I need some fresh air."),
("npc25_intro_response_2", "Never mind, we are merely sight-seeing."),
("npc26_intro_response_2", "I'll just be on my way then, or my sword arm will start to itch."),
("npc27_intro_response_2", "[Ignore and leave]"),

#backstory intro
("npc18_backstory_a" , "I am no mere slave! I am a head-taking warrior, cheated of my rightful place among the ranks! You see that I am a woman, but I am stronger and swifter than many others, and I've outfought more men than I can count. The Pit Master - accursed be he! He set me a test, to fight three men at once. Three!"),
("npc19_backstory_a" , "A small drop, to be sure, but my dam has told me all about my lineage. I am Heidrek, direct descendant of King Fengel, closer to the throne of Rohan and Dunland than any of our chieftains! Dark is my hair, but I fancy I have more than a strand of yellow in there somewhere."),
("npc20_backstory_a" , "In my dream, there was a tree. A tree, all of white. And you, you were there, standing beside it. You placed your hand upon its trunk, and lo, it withered down to its very roots. And the shadow in the sky lengthened, and the air grew heavy. I heard a laughter then, from far away in the east. "),
("npc21_backstory_a", "My name is Gálmynë, and I made it my business to know yours, {playername}. Let me explain why."),
("npc22_backstory_a", "You may have heard tales of my deeds in battles past and forgotten by mortal Men. In the fullness of time this War is yet another time of danger for the Eldar, but it will be the Last War."),
("npc23_backstory_a", "Excuse my brashness, stranger, but we don't have many visitors here and those that come do not look very trustworthy. Only a week ago, this dwarf appeared and... Never mind. My name is Luevanna, of the Silvan Elves of Mirkwood."),
("npc24_backstory_a", "Polite of you to ask, {playername}. We are fighting off incursions from Easterlings and Gundabad orcs, but so far nothing we and our Dale allies can't handle."),
("npc25_backstory_a", "I'm sure you can find some fine volunteers if you speak to the quartermaster in the barracks. As for me, I'm merely a healer and herbalist of modest skills."),
("npc26_backstory_a", "Good for you! They call me Gulm. I have gutted my sergeant and his snaga s now hunt for me.^The worthless piglet had it coming! Once, we got ambushed by a strawheads patrol... and he lost it. 'Fall back' he screams, then flees. Only Gulm and a few others stood firm, and broke their horses charge. Then we bludgeoned the yellow-haired into paste (heh heh heh). But if it wasn't for us strong ones, all would be worm food!"),
("npc27_backstory_a", "I am Durgash!"),

#backstory main body
("npc18_backstory_b" , "I prevailed! I defeated them! But... one of them was so weak that he perished from the blows I dealt him. If he had been a simple bondsman, that would have been the end of it. But no. He was one of Great Lord Lurmsakun's many sons, by a lesser wife."),
("npc19_backstory_b" , "Well, you will not find any of Rohan or Dunland who will accept my claim, but it is a true one nonetheless. My grand-dam was a herdswoman, living in the hills, and one day it chanced that old King Fengel, the greedy grasping grandfather of Theoden the Pretender, happened to see her on the banks of the Isen. He took a fancy to her, and my dam was his child."),
("npc20_backstory_b" , "Do you not know before whom you stand? Ignorant fool. Know that I am Zigûrphel, of ancient Akallabêth - but like as not you know nothing of that name! Know, also, that I seek to redress the wrongs of long ago, the wrongs wrought upon me and my people by the spite of the Valar, they who sank our Great Armament and our home. Ah, Ar-Pharazôn, great and glorious! Shall your vision be unremembered evermore? No, not so long as Zigûrphel lives and has hands to do her work!"),
("npc21_backstory_b", "I was born into a noble family and I have been serving Lady Éowyn as a maid of honour ever since we were little girls. Our fathers were wise enough to allow us to train alongside our brothers in matters of combat, to become shieldmaidens of Rohan."),
("npc22_backstory_b", "Lord Elrond sent me as an emissary to Lord Celeborn, to give aid and advice as it's needed in the War in this part of Rhovanion."),
("npc23_backstory_b", "I like to walk the hidden paths in our beautiful forest. Sometimes I move quietly through the trees and observe the habits of the many woodland animals. The song of a rare bird, the nesting of a wild boar are as beautiful to me as the clash of weapons and great walls are to the Edain."),
("npc24_backstory_b", "I helped improve the Erebor defenses and trained some younger dwarven folk, under the direction of my venerated father Dwalin, as is our custom."),
("npc25_backstory_b", "I have treated my King Brand for constipation, a common malaise affecting men going to war. A light brew of wormwood, and both the bowels and the mind are put at ease."),
("npc26_backstory_b", "So I said to myself, 'Gulm, you want end up as carrion?' and I answered, 'No'.^Next battle, I fell back pretending I was injured. Then, with no one watching, I fell upon my sergeant! Cleaved him almost in half, gharr! Then cut his sidekick snaga nicely^^...Turned out that bloody creeper survived somehow, and started waggling his tongue about all this. Next time I make sure his head is off, gharr..."),
("npc27_backstory_b", "I am a Wolf Rider of Isengard and a tracker."),


#backstory recruit pitch
("npc18_backstory_c" , "And so here I am, cursed at and spit upon, condemned to die for being mightier than the dogs who mock me! Free me, Great One. Free me, speak for me - and my strength is yours. My blade is yours. My life is yours!"),
("npc19_backstory_c" , "Naturally, Chief Daeglaf and the rest wish to give me no chance at all for glory, for if I were to perform great deeds in battle, it would lend wings to my claim. Men would flock to my banner then! Your fame runs before you, Commander. If you will allow me to serve under your banner, I can perform those great deeds for you."),
("npc20_backstory_c" , "O Akallabêth, where are you now? Faded, all faded away... Where there once was light, the glory of our nation that was great above all others, now there is only the Shadow. My beautiful home now knows the eternal silence of the sea. But my heart is still full of fire, and dark beasts run wild within it. I know potent arts that you and your kind have never even imagined. Hearken unto me, now! Will you beg for my aid, as you should, or will you go from here skulking, like a worm? Choose swiftly!"),
("npc21_backstory_c", "You might know that women, however skilled, are not allowed to ride with the éoredas. However, I do not think that waiting by the hearth for the warriors to return is my fate. I will not sit idle until all chance of great deeds is gone in this War, and I would welcome your assistance, warrior."),
("npc22_backstory_c", "However, if the enemies of Lothlórien are on the run, I might consider joining you for a while, {playername}. I sense our fates in this War are interwoven."),
("npc23_backstory_c", "You wouldn't understand that, I think, seeing you prepared for war. But you must have travelled far and wide - have you seen the other great forests? Can you take me there?"),
("npc24_backstory_c", "There is a lull in the fighting that ill-suits a dwarven warrior of my ancestry and temperament. I gather you get to see much more action in your travels and your cause is friendly with the dwarves? I know a fighting dwarf will greatly improve your chances of survival."),
("npc25_backstory_c", "I hear there is much fighting elsewhere and our lands are gratefully spared for now. From the scratches on your armor you must have been in danger many times. Maybe my humble skills could be better used with your company, for the greater good of all."),
("npc26_backstory_c", "I am a fighting Uruk-hai, and a berserker! What there is to know of killing men, I know it. I was in the service of the White Hand, but now the Hand would as likely throw me into the fire-pits.^^I would come with you and hunt men in the south, while the snagas of Isengard gnash their teeth."),
("npc27_backstory_c", "Maybe you can be my next master."),

### use these if there is a short period of time between the last meeting 
("npc18_backstory_later" , "I have been fortunate, I suppose, that Great Lord Lurmsakun has been occupied elsewhere. His intendants have left me here to rot. But my destiny is not to die as a prisoner! Have you come to grant me my rightful death on the battlefield?"),
("npc19_backstory_later" , "Ho there! You have returned, as I knew you would. My hands are kept idle by my jealous chiefs. Let us speak, Commander! I would follow you, and fight in your ranks to win for myself renown."),
("npc20_backstory_later" , "You trouble my dreams still! Will you give me no peace? My dreaming eye sees deep and far. Here in Dol Guldur I still have visions of your works. I say this: if you were wise, you would have asked for my aid again ere now."),
("npc21_backstory_later", "More riders return with their bodies broken, and I try to give aid where I can. But I still feel trapped in a cage."),
("npc22_backstory_later", "Have you reconsidered? The time for the Eldar grows short."),
("npc23_backstory_later", "I've been observing a nest of giant spiders for a couple of days. Ugly creatures, they seem at first, but they keep intruders at bay. Did you come to ask me to travel with you?"),
("npc24_backstory_later", "Building up defensive walls is worthy of any dwarf. But I need to use my axe too. Soon. Let me come with you."),
("npc25_backstory_later", "I made another call to our King, this time for vomiting. I hope his resolve to engage the enemy is not related to his conditions. Do you suffer from constipation and vomiting too?"),
("npc26_backstory_later", "What do you think I do? Gulm is sitting here and waiting for some sneaky snaga to stick him in the dark. Take me with you - I will serve well."),
("npc27_backstory_later", "Have you reconsidered? I will serve well."),

("npc18_backstory_response_1" , "If you are truly as ferocious as you look, perhaps you could fight for me. After we feed you up a bit, of course."),
("npc19_backstory_response_1" , "Very well. As long as you can fight in the battle line, you can be of use, Dunlending."),
("npc20_backstory_response_1" , "Strange way of asking to join me, witch. But very well, you may come along."),
("npc21_backstory_response_1", "I would welcome the help of a Rohan shieldmaiden, if offered."),
("npc22_backstory_response_1", "It may be presumptuous of me to ask, but my company could use your skill in the coming battles."),
("npc23_backstory_response_1", "We travel the world, but to defend all that is fair, we give battle to the enemy."),
("npc24_backstory_response_1", "Indeed, a dwarven warrior would be welcome in my company."),
("npc25_backstory_response_1", "We can use a healer and a herbalist."),
("npc26_backstory_response_1", "I reckon we could put a berserker to a good use."),
("npc27_backstory_response_1", "You will do."),

("npc18_backstory_response_2" , "Pah! A murderous pit dog is not fit to be a companion of mine."),
("npc19_backstory_response_2" , "You talk of great deeds. Go and do some of your own, before you approach me again!"),
("npc20_backstory_response_2" , "Pah! I'm guessing your bark is far worse than your bite. I have work to do!"),
("npc21_backstory_response_2", "I am sorry, my Lady, there's nothing I can do."),
("npc22_backstory_response_2", "I'll be back when Lothlórien is in less danger."),
("npc23_backstory_response_2", "No, sorry. We cannot take hangers-on."),
("npc24_backstory_response_2", "No, sorry. We do well on our own."),
("npc25_backstory_response_2", "No, sorry. We only visit healers when we need them."),
("npc26_backstory_response_2", "Bah. I don't trust traitors."),
("npc27_backstory_response_2", "I don't need you, slave."),

("npc18_signup" , "Oh, to sink my teeth into meat again! You'll see my true mettle soon enough, once my hands and feet are free, and I have food in my belly!"),
("npc19_signup" , "Yes, you may call me that for now, for I am not ashamed of my Dunlending blood. My people have suffered greatly under the tyrant kings of Rohan, and I feel no small kinship with them. I will aid you in this war, and in all your efforts. But in return, Commander, you must help me press my claim when the time comes."),
("npc20_signup" , "I will overlook your haughtiness for a time, but know that someday we shall have words. Perhaps by then, we shall both be standing before the Dark Lord, whom I once knew by a much different name, and then we shall see who has his ear. Perhaps then I shall teach you manners."),
("npc21_signup", "It is gladly offered, and you can welcome me to your company, commander."),
("npc22_signup", "I see. I admit I have heard of you and your exploits."),
("npc23_signup", "I dislike violence and weapons of war, but I know how to defend myself in a hurry."),
("npc24_signup", "I am skilled with an axe, both the wielding and the throwing type. I can also keep your bills low if you let me talk to the merchants. And I have an eye for finding the best pieces of loot from fallen enemies on the battlefield."),
("npc25_signup", "Indeed? Well then, I merely need to gather my herbs and recipees."),
("npc26_signup", "A fighting Uruk is worth more than all your snagas. A fighting Uruk never runs from battle."),
("npc27_signup", "Really? You would do well to enlist me."),

("npc18_signup_2" , "My mother once told me, I was born to hew many foemen. For you, I will slay many soft weaklings of the West. Only put a good blade into my hands, and I will do the rest!"),
("npc19_signup_2" , "I fight as my people do, like wolves in the night - I may fling a spear, or drive a pike into the chest of a charging horseman. Limbs I hew with axe or sword. With you, I will speak openly: I care not if you give more service to the Eye or the White Hand. It is all one to me, as long as I can sit my rightful throne in the Golden Hall."),
("npc20_signup_2" , "But for now, let my lore and craft founded in long years be yoked to your service. Know this: with Zigûrphel's aid, you are as a dragon given its wings in the pit of Utumno. Great things I will do for you and your purpose, though you comprehend them not!"),
("npc21_signup_2", "I have hunted game many times with bows and throwing spears. I will hunt orc under your command. And I have some skill in healing I'm certain will be needed."),
("npc22_signup_2", "Perhaps by joining your company and striking hard where I am not expected, the Enemy will be unbalanced. I will come."),
("npc23_signup_2", "Perhaps I can teach you to move faster and make less noise. Let's go."),
("npc24_signup_2", "If you can keep the tall-folk in your company in line, especially the sneaky Elves, I'll gladly join you."),
("npc25_signup_2", "I must warn you though, I am fairly useless in battle. But I'm sure you are able to keep a woman of my age safe."),
("npc26_signup_2", "But you must decide quickly, the guards here are getting suspicious."),
("npc27_signup_2", "You won't regret taking me on."),

("npc18_signup_response_1" , "I like your spirit. Very well, I will send word to Lurmsakun on your behalf."),
("npc19_signup_response_1" , "Well, then, 'Prince', take up your weapons. You fight for me, now."),
("npc20_signup_response_1" , "I hope, for your sake, that your words are not idle boasting. Do not disappoint me, Zigûrphel."),
("npc21_signup_response_1", "Impressive. We are ready to leave, whenever you are, my Lady."),
("npc22_signup_response_1", "We will be honoured to have the company of an Elf-lord."),
("npc23_signup_response_1", "Very well. I hope you won't run away from the first orc we see."),
("npc24_signup_response_1", "Very well, Master Dwarf, you are welcome to join us."),
("npc25_signup_response_1", "You will be safe with us, I promise. We will be leaving shortly."),
("npc26_signup_response_1", "Very good. Do as you are told, and I'll feed you well."),
("npc27_signup_response_1", "Very well. Let's go."),

#11
("npc18_signup_response_2" , "Your are fierce... perhaps too fierce. A little more time in the stocks for now might teach you obedience."),
("npc19_signup_response_2" , "You shall have to sit on these bales of hay for a little longer, 'Prince'."),
("npc20_signup_response_2" , "Your brag and abuse grate upon my ears. Tame your tongue before we speak again!"),
("npc21_signup_response_2", "I apologize, my Lady, perhaps another time."),
("npc22_signup_response_2", "On second thought, maybe we need to help Lothlórien on our own."),
("npc23_signup_response_2", "Sorry, I just can't imagine you on a battlefield."),
("npc24_signup_response_2", "Sorry, I happen to like Elves."),
("npc25_signup_response_2", "I'm sorry, everyone fights in my company."),
("npc26_signup_response_2", "I've changed my mind. Whoever is looking for you might come for me next."),
("npc27_signup_response_2", "I've changed my mind."),

("npc18_payment" , "Surely, a mighty commander of your stature has only but to say the word, and they will release me."  + costs_reg14_inf_with_s14),
("npc19_payment" , "It seems Daeglaf the Black may seek some excuse to hold me here, Commander." + costs_reg14_inf_with_s14),
("npc20_payment" , "Rather, it is you who would do well not to disappoint me or the Master we both serve. Have you done well enough in his estimation?" + costs_reg14_inf_with_s14),
("npc21_payment", "I would join you, but who will care for the wounded if the city is attacked?" + costs_reg14_inf_with_s14),
("npc22_payment", "We should be off soon. The value of my coming will be diminished if the Enemy senses my presence before we have struck. But Lothlórien also needs me here." + costs_reg14_inf_with_s14),
("npc23_payment", "I would join you, but my duty is here." + costs_reg14_inf_with_s14),
("npc24_payment", "I would join you, but I'm afraid my honorable father Dwalin will not understand why I left the town in a time of need." + costs_reg14_inf_with_s14),
("npc25_payment", "I cannot abandon my duties here, my King still needs me. I'm too concerned for his health." + costs_reg14_inf_with_s14),
("npc26_payment", "I want to leave with you, but the guards at the gate won't let me.^Trust me, I've tried." + costs_reg14_inf_with_s14),
("npc27_payment", "I would join you, but my duty is here." + costs_reg14_inf_with_s14),

("npc18_payment_response" , "No doubt of that. Lurmsakun's subordinates will not dare refuse me."  + spend_reg14_inf_on_reg15 ),
("npc19_payment_response" , "Chief Daeglaf will have to give way before my wish, once I make it plain." + spend_reg14_inf_on_reg15 ),
("npc20_payment_response" , "Indeed I have. Come now! It is not, after all, a lowly snaga you will follow."  + spend_reg14_inf_on_reg15),
("npc21_payment_response", "It's a noble cause, but I'm sure a replacement can be found."+spend_reg14_inf_on_reg15),
("npc22_payment_response", "Trust me, you will be more useful with me."+spend_reg14_inf_on_reg15),
("npc23_payment_response", "From now on, your duty is with me."+spend_reg14_inf_on_reg15),
("npc24_payment_response", "Master Dwalin will understand that a battle-worthy dwarf should not be kept from our enemies for too long."+spend_reg14_inf_on_reg15),
("npc25_payment_response", "The King's well-being is important, but you will save more lives with me."+spend_reg14_inf_on_reg15),
("npc26_payment_response", "Oh, but the guard won't dare stop you, if you are with me."+spend_reg14_inf_on_reg15),
("npc27_payment_response", "From now on, your duty is with me."+spend_reg14_inf_on_reg15),

("npc18_morality_speech" , "Great One! My thirst for blood is unslaked! Why do we {s21}, like cowards? Let me fight them!"),
("npc19_morality_speech" , "Commander, I mislike it greatly that we {s21}. A king like myself should ever be open-handed, but if the larders are empty I have nothing to give, and our soldiers will desert us."),
("npc20_morality_speech" , "I would say I had expected better of you, Commander, but that would be a lie. Beware, lest your self-serving ways do harm to the lofty designs of your betters!"),
("npc21_morality_speech", "Take no heed to what the soldiers say, sometimes to {s21} is the wisest course of action. I for one appreciate the lives spared and limbs unbroken, if for nothing else but to fight another day, when fate looks upon us with favor."),
("npc22_morality_speech", "You must reconsider your actions, commander. To {s21} makes us no more honourable than the Enemy and diminishes the confidence of our friends."),
("npc23_morality_speech", "[No primary moral code]"),
("npc24_morality_speech", "I was not pleased that you decided to {s21}. To fall in battle is an honour for any right-thinking dwarf, but to fight in a company led by a coward is a disgrace. What will my cousins say if they learn of this?"),
("npc25_morality_speech", "Commander, I must object. To {s21} is harsh on the men and unnecessary. I do what I can to ease their suffering, but please don't make another costly mistake."),
("npc26_morality_speech", "The fighting Uruk-hai don't {s21}. If the Master has little guts, he might find himself without them one night. Gulm has spoken."), #run from battle
("npc27_morality_speech", "[No primary moral code]"),

("npc18_2ary_morality_speech" , "I joined you not to {s21}, Great One, but to bathe in the blood of our foes! You may employ your guile for now, but give me a good slaughter soon, I beg you!"),
("npc19_2ary_morality_speech", "[No secondary moral code]"),
("npc20_2ary_morality_speech" , "Ah, our mighty Commander. Great deeds you performed, you say? I wonder how many other of your battles ended this way, with you advancing recklessly into the jaws of a trap, and fleeing with as much haste."),
("npc21_2ary_morality_speech", "Your pardon, commander. Women of my station will accept death but not dishonour. To {s21} brings shame to my house and ancestors."),
("npc22_2ary_morality_speech", "[No secondary moral code]"),
("npc23_2ary_morality_speech", "[No secondary moral code]"),
("npc24_2ary_morality_speech", "[No secondary moral code]"),
("npc25_2ary_morality_speech", "[No secondary moral code]"),
("npc26_2ary_morality_speech", "[No secondary moral code]"),
("npc27_2ary_morality_speech", "[No secondary moral code]"),

("npc18_personalityclash_speech" , "Great One, if you value Varfang as a warrior, I beg that you keep him as far away from me as possible. I have already warned him that his hands must not go where I will not let them, or I shall chop them off and feed them to his horse. "),
("npc19_personalityclash_speech" , "Commander, I wonder greatly that you retain the services of a lowly creature like Ufthak. Of course, the orc-kind are scum and arrow-shields for our true warriors, but he stalks around the camp giving orders to man and orc alike, as if he were one with authority. I hope you do not miss him too greatly if I slay him. Or perhaps I will simply cleave off the end of his ugly nose."),
("npc20_personalityclash_speech" , "The Southron Lykyada should learn manners, and be taught humility. Insolent is his tongue, and overproud his bearing! I care not that he is a captain among his men - a foolish lesser race they are, in any case, slow to recognise greatness or bow to their betters as they should! If he knew but a small part of what I could do to him..."),
("npc21_personalityclash_speech", "Did I mention I hate {s11}?"),
("npc22_personalityclash_speech", "Did I mention I hate {s11}?"),
("npc23_personalityclash_speech", "{playername}, I just saw {s11} walk brazenly over a nest of young birds. His clumsiness destroyed the young lives of innocent creatures."),
("npc24_personalityclash_speech", "Lord {s11} does well in a battle, but I wonder if he blinds the enemy by the shine of his hair? Or they fall in awe of his fame and uppity demeanor?"),
("npc25_personalityclash_speech", "Commander, I must lodge a complaint against {s11}. He continues to pester me about making him a certain brew called 'the green fairy'."), 
("npc26_personalityclash_speech", "Did I mention I hate {s11}?"),
("npc27_personalityclash_speech", "Did I mention I hate {s11}?"),

("npc18_personalityclash_speech_b" , "Great One, I wish to ask, what is the blood price you have set on Varfang's head? If it happens that I kill or maim him, I would pay it to you as recompense. He was leering at me after that battle, licking his foul lips. If he looks at me that way again, I'll carve his eyeballs out and feed them to him."),
("npc19_personalityclash_speech_b", "As I expected, the cowardly orc calling himself Ufthak is of little worth in battle. He skulks behind the line, doing but little to aid his fellows. Your cause - and my fight for my throne - will not be helped overmuch by his kind, I think."),
("npc20_personalityclash_speech_b" , "If Lykyada's hands were not of such use to us, Commander, I should remove them from his arms. You know that I am in the habit of walking among our fallen foes after a battle - there is great power in the fear and pain of the dying for one who has the art to use it, though none of you have the knowing of it. Yet he, that swarthy Southron, stalks around giving the gift of a swift death to those whose hurts are too deep for capture. That grain of mercy in his heart prevented me from basking in the death-glow of the fallen! How important is his precious honour to you, I wonder?"),
("npc21_personalityclash_speech_b", "I hate {s11}."),
("npc22_personalityclash_speech_b", "I hate {s11}."),
("npc23_personalityclash_speech_b", "His dwarven ways may serve him well underground, albeit it's a wonder he hasn't fallen down an ugly shaft. Maybe he should have."),
("npc24_personalityclash_speech_b", "We would do better with a dwarven hero, someone like Durin the Deathless of old, and let the Elves prance around their forests."),
("npc25_personalityclash_speech_b", "It is made from wormwood soaked in liquor and apparently favored by minstrels and vagrants for seeing things that are not there. I doubt you'll approve of your soldiers chasing air on the battlefield, as much as it may be amusing to watch."),
("npc26_personalityclash_speech_b", "I hate {s11}."),
("npc27_personalityclash_speech_b", "I hate {s11}."),

### set off by behavior after victorious battle
("npc18_personalityclash2_speech" , "Gulm is not only a treacherous beast, Great One - he is proud of being one. He was telling us his story again around the campfire last night, and boasting of his foul deed. You would do well to watch that creature, Great One. If he could betray his commanders when serving the White Hand, what's to stop him from doing the same with you?"),
("npc19_personalityclash2_speech" , "I hate {s11}"),
("npc20_personalityclash2_speech" , "Every time I set eyes upon Fuldimir, a nameless rage within me rises. No, no, it is nothing he has done. But he and his people, the sea-dogs of Umbar, are most unworthy of their blood. They dare call themselves heirs of ancient Anadûnê - but of course, they say 'Númenor', not knowing any better. Why, I would suppose that barely a drop of the true blood is to be found in Fuldimir's veins! Perhaps, if you can spare him, I could find out for myself..."),
("npc21_personalityclash2_speech", "Did I mention I hate {s11}?"),
("npc22_personalityclash2_speech", "Did I mention I hate {s11}?"),
("npc23_personalityclash2_speech", "Did I mention I hate {s11}?"),
("npc24_personalityclash2_speech", "A nice little scrap, eh captain? If only slightly ruined by the conduct of that Elf-woman {s11}."), 
("npc25_personalityclash2_speech", "Did I mention I hate {s11}?"),
("npc26_personalityclash2_speech", "Did I mention I hate {s11}?"),
("npc27_personalityclash2_speech", "Did I mention I hate {s11}?"),
 
("npc18_personalityclash2_speech_b" , "That misshapen creature Gulm had better guard his neck, or I'll slice through it! I was about to slay a foe, but he stepped in front of me and made the kill that should have been mine. Then he had the gall to turn around and sneer at me! He and his kind had better remember that they were bred to serve us! Honourless curs."),
("npc19_personalityclash2_speech_b", "I hate {s11}."),
("npc20_personalityclash2_speech_b" , "He cannot possibly be one of us. No, not one like Fuldimir. No, our blood cannot have thinned so much, our line cannot have fallen so far! Do none of you mark how little he speaks of the true speech, how in appearance he is much more like unto those of Haradwaith than of my lost home? We had heroes among us - heroes, who fought with swiftness and strength to rival the Eldar! Fuldimir is slow, and clumsy, and... No, I feel the cold wind blowing out of the West. It chills me... it chills me!"),
("npc21_personalityclash2_speech_b", "I hate {s11}."),
("npc22_personalityclash2_speech_b", "I hate {s11}."),
("npc23_personalityclash2_speech_b", "I hate {s11}."),
("npc24_personalityclash2_speech_b", "I saw her cowering in the rear, barely releasing an arrow or two in the general direction of the enemy. I say let her go to take care of the birds and bees, so we can go on with the bloody work of slaying the enemy."),
("npc25_personalityclash2_speech_b", "I hate {s11}."),
("npc26_personalityclash2_speech_b", "I hate {s11}."),
("npc27_personalityclash2_speech_b", "I hate {s11}."), 

("npc18_personalitymatch_speech" , "Great One, do you mark how deadly Lykyada is in battle? How swift his arrows, how sharp his blade! With your permission, Great One, I should like to spend more time training under his tutelage. He has much he could teach me that could make me more useful to you."),
("npc19_personalitymatch_speech" , "The joy of battle sings in my blood! And in Varfang's too, I can see. The man is a terror to behold on the battlefield, laughing as he rides down the worthless foes who flee. These men from the East intrigue me, Commander. We could learn much of horsemanship from them, if the Rohirrim will not teach the Dunlendings after I come into my own."),
("npc20_personalitymatch_speech" , "Behold Bolzog. Bolzog the Great! See how he scurries with his bow-legged gait, coming and going at my whim, doing everything I ask of him. Just as a proper little 'urku' should, I say. I quite like him, Commander. Bolzog! Bring me the unguent! Now!"),
("npc21_personalitymatch_speech", "A battle of great deeds, commander, and my congratulations on the victory. I noticed how {s11} quietly and surely took care of the wounded and ailing, even as the last of the enemy got what they deserved."),
("npc22_personalitymatch_speech", "Did I mention I like {s11}?"),
("npc23_personalitymatch_speech", "{playername}, as much as I hate battles, I can't help but notice my Lord {s11} riding out in full splendor and bearing down on the ugly creatures like a hawk."),
("npc24_personalitymatch_speech", "Bloody and victorious, just as I like it! I did, however, sustain a flesh wound that {s11} was kind enough to bandage promptly."),
("npc25_personalitymatch_speech", "Another victory for you, commander, and I admire your skill in sparing the lives of our men. Warriors like {s11} seem to be of great use in your battle plans."),
("npc26_personalitymatch_speech", "Did I mention I like {s11}?"),
("npc27_personalitymatch_speech", "Did I mention I like {s11}?"),
 
("npc18_personalitymatch_speech_b" , "Great One, it speaks well of you that a warrior like Lykyada fights under your banner. I had thought all Southerners weak and decadent, not so different from the men of the West, but if they have more like him among their ranks, then the days of the West are indeed coming to an end."),
("npc19_personalitymatch_speech_b" , "Commander, Varfang and I were sharing a skin of wine around the campfires last night. Deep-counselled I deem him, for ever mindful is he of the deeds of his forebears, as one should be. I know not if, as he says, the spirits of our ancestors are with us. Indeed, I like not the thought. But a king must know the story of his blood, of mothers and fathers aforetimes. Varfang is one such who knows this."),
("npc20_personalitymatch_speech_b" , "I have never met an 'urku' quite like Bolzog. Oh, I grant you he is unlovely to look upon, but in all my long years he is the first one I've ever encountered who can do more than simply sneak, skulk and slaughter. His gnarled hands are surprisingly deft. Yes, so surprisingly deft... It may be that he can learn more of the arts of bone and sinew than I had reckoned at first."),
("npc21_personalitymatch_speech_b", "To preserve lives is the noblest deed, and I feel kinship with that kind soul, even if our worlds are far apart."),
("npc22_personalitymatch_speech_b", "I like {s11}."),
("npc23_personalitymatch_speech_b", "I wonder just how old is he. Maybe a dozen of centuries older than me? Never mind, you wouldn't understand."),
("npc24_personalitymatch_speech_b", "{s11} and her Dale-kin, even if not quite up to dwarven warrior standards, have proven to be steadfast allies in this War. A good choice for a friend and companion among Men, if I may say so."),
("npc25_personalitymatch_speech_b", "The people of Dale have a deep regard for the hardy Lonely Mountain Dwarven-folk, as friends and protectors despite our different race and customs."),
("npc26_personalitymatch_speech_b", "I like {s11}."),
("npc27_personalitymatch_speech_b", "I like {s11}."),

#these are not used  
("npc18_retirement_speech" , "I think I want to settle down and raise a family and, I dunno, do embroidery or shit. Bye."),
("npc19_retirement_speech" , "Listen, strange men standing around claiming royal bastardy is no basis for a system of government."),
("npc20_retirement_speech" , "Maybe anger isn't the way. All we need is love. Why can't we all get along?"),
("npc21_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
("npc22_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
("npc23_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
("npc24_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
("npc25_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
("npc26_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),
("npc27_retirement_speech", "I'm getting a bit tired of the warrior's life, I'll retire."),

("npc18_rehire_speech" , "My blade yet thirsts for blood, Great One. Let me come with you again!"),
("npc19_rehire_speech" , "It is good to see you again, Commander. Give me leave to rejoin your company."),
("npc20_rehire_speech" , "Let us be off, Commander. This war will not be won with idleness!"),
("npc21_rehire_speech", "Welcome again. Shall we continue where we left off?"),
("npc22_rehire_speech", "It's good to see you, {playername}. Let us travel together again."),
("npc23_rehire_speech", "It's good to see you, {playername}. Let us walk the same path again."),
("npc24_rehire_speech", "My axe is ready, {playername}. Shall I rejoin you?"),
("npc25_rehire_speech", "You are a welcome sight. Shall I join you once again?"),
("npc26_rehire_speech", "Gulm is ready to kill for you again. Are we going?"),
("npc27_rehire_speech", "Can I serve you once again?"),

#local color strings
("npc18_home_intro" , "Ah, the Anduin. Great One, you will have heard of the great victories of the Wainriders many generations ago? They made an alliance with us Variags, and together our warriors crushed the pitiful armies of Gondor, under the king they called Ondoher. What a glorious slaughter our forefathers must have enjoyed!"),
("npc19_home_intro" , "Ah, Edoras. My rightful seat. Look up there, Commander, at the Golden Hall. Only a few generations ago, it was at the very doors of Meduseld that the last son of Helm Hammerhand was slain, and thereafter Wulf was King, for a time. Not the Wulf who is a Chief of Dunland now, of course - that one is a mere mongrel bearing the name of a greater creature."),
("npc20_home_intro" , "Ah, the Lonely Mountain. The last bastion of Durin's Folk, is it not, in these latter days? It is pleasant to see it with my own eyes at last. Pleasant, yes... but not as pleasant as the memory of that Dwarf's dying moments, which I made longer with my arts. Hardy are the Dwarfs, indeed! Yet Aulë the Maker did them no favours in making them so capable of suffering."),
("npc21_home_intro", "Let's stop here for a minute, commander. Ahead of us, between the Anduin and the Limlight, lies the Field of Celebrant, where Eorl the Young rode to the aid of our Gondor allies."),
("npc22_home_intro", "Daro! That's Angrenost and the black tower of Orthanc ahead. Much has changed since I last saw them, and none for the better."),
("npc23_home_intro", "Excuse me, {playername}. The paths in this part become more twisted and some lead to dead-ends. We must be approaching Dol Guldur."),
("npc24_home_intro", "Oy, captain! This must be the old path to the Eastern Gates of Khazad-dûm, or Moria as you may prefer. You can see in the distance the glittering lake of Kheled-zâram, and, through the clouds, the three peaks known to grace this part of the Misty Mountains."),
("npc25_home_intro", "Oh, a curious sight! I heard stories about this place where sturdy woodmen are said to live in harmony with animals and plants. Beornings they are called, I gather."),
("npc26_home_intro", "Curses! That must be Hornburg over there, master."),
("npc27_home_intro", "Hey, look!"),

("npc18_home_description" , "Our wise ones told us all about that war. If it hadn't been for the weakness of the Southerners, losing a battle they should have won, the Gondorians would never have won the Battle of the Camp. The chariots of the Wainriders were smashed, and many fierce heroes died in the swamps of the Dead Marshes."),
("npc19_home_description" , "I would see our peoples united, as they have been in the past. No more will women of dun hair nurse sickly babies at their bosoms, while their fair-haired cousins feast on meat and swoon from wine in warm halls. No more will the black-haired hill man look with resentment upon the herds of horses owned by a crofter with hair of gold. As king, I will see justice done - but first, let the tyrants of Rohan pay their weregild."),
("npc20_home_description" , "I remember him well - Thráin, son of Thrór. Foolhardy, vainglorious would-be scion of a broken line, claimant of a worthless throne! Great torment he endured at my hands. But no one withstands the will of Zigûrphel for long, Commander. No one. I took his Ring from him, in the dungeons of Dol Guldur, and sent it on to the Dark Tower for a great reward. High I rose then, in the Dark Lord's favour!"),
("npc21_home_description", "'Where now the horse and the rider? where is the horn that was blowing?^Where is the helm and the hauberk and the bright hair flowing?...^They have passed like rain on the mountain, like a wind in the meadow;^The days have gone down in the West behind the hills into shadow...'"),
("npc22_home_description", "Once built by the Southern Kingdom, now home to one that we called the White Wizard, scheming, no doubt, how to increase his power further at the expense of others."),
("npc23_home_description", "I have never ventured this far, but I overheard our Greenwood scouts say there may be Nazgul here. I feel an evil presence, but I cannot put a name to it. It is powerful, though, so let us be prepared."),
("npc24_home_description", "Judging by the desolation, and the many orc-tracks, I fear for the fate of the courageous Balin and his expedition. It seems that Moria has fallen to the Shadow and we should tread carefully."),
("npc25_home_description", "Not too often, a travelling merchant comes to the Dale market and offers the finest honey I have ever tasted. For some curious reason, he says that 'it was made by bears' and laughs."),
("npc26_home_description", "Its damned walls are too high and too hard for my hammer to break. I reckon if we ever chase away the manlings from their Edoras pig-sties, they'll run off here and cower behind the walls."),
("npc27_home_description", "Do you know that town?"),

("npc18_home_description_2" , "It pleases me to be marching with you, Great One. The leaders of my people will want to have this land again, which was once theirs. They may take as much as they like from Gondor and the West. For my part, if I can spill the blood of more enemies on this soil, I will count myself happy."),
("npc19_home_description_2" , "You will speak for me, won't you, Commander, when the long war is over? To whichever Power holds sway over the other - Eye or Hand? You will lend your voice to my claim, that I may hold Edoras and all Rohan in fief to an overlord, as my home and holding?"),
("npc20_home_description_2" , "We shall crush the works of the Valar, of which these Dwarfs are a chief part, here in Middle-earth. Yes, it would be sweet to unmake what the Maker wrought. We will grind the Dwarves beneath our heels, shatter the last kingdoms of low Men, and laugh as the Elves fade into the mists like ghosts. Then the day will come when I stand before the Caves of the Forgotten, in Valinor, and call forth my king again!"),
("npc21_home_description_2", "We would do well to remember the great deeds of the past and the sacrifices that were made. The Alliance between Rohan and Gondor shall save our peoples from doom once again."),
("npc22_home_description_2", "Let it be a reminder that even the greatest, even one of the Istari, can be corrupted and fall. Those who lust for power can be defeated by power, so let us not tarry much longer."),
("npc23_home_description_2", "I sense the evil armies behind its walls prepare to march... To fair Lothlórien? To Dale? To my Greenwood homeland? I cannot tell, but please do everything you can to thwart them."),
("npc24_home_description_2", "If the fortunes of war ever provide us with a large army, we should risk the entrance to the Mines and retrieve their mighty riches."),
("npc25_home_description_2", "I can smell the fragrance of many sweet flowers and see the bees harvesting their nectar. If you don't mind, I will gather some herbs for our own use, it will only take a moment."),
("npc26_home_description_2", "There's no use trudging around here if we are not backed by a large Uruk-hai horde. Unless you want to make faces at the lookouts on the wall, that is."),
("npc27_home_description_2", "Minas Morgul, where Nazgul drink all day, har-har!"),

("npc18_home_recap" , "I was a prisoner in stocks, condemned to die for slaying a son of Lurmsakun in the training pit. Three of them set upon me, and I beat them, but one died of his wounds. Then you spoke for me, and freed me. Now I kill for you, and I would die for you if need be."),
("npc19_home_recap" , "I am of the royal blood of Rohan, I swear - King Fengel was my grandfather, though he never took my grandmother to wife. The Chiefs of Dunland are jealous of me, and kept me away from the fighting so I would do no great deeds, and win no glory nor men to my banner. Then you took my under your banner. Now I await the day I can sit in Edoras on my rightful throne."),
("npc20_home_recap" , "What more is there to tell, Commander? I practised my arts in the dungeons of Dol Guldur. My dreaming eye sees deep and far, and I saw you and your works in this War. It would seem I must give you what aid I can, so that the powers of the West may fail and the Power in the East may rise once more and rule until the world's ending."),
("npc21_home_recap", "I don't find it amusing that you should forget so easily."),
("npc22_home_recap", "I'll indulge your curiosity, but let us not tarry."),
("npc23_home_recap", "I was born and raised in Mirkwood, a Silvan Elf. Our race's woodcraft skills are known to all."),
("npc24_home_recap", "I am son of Dwalin of the Durin's folk."),
("npc25_home_recap", "I am a healer and a herbalist from Dale."),
("npc26_home_recap", "Gulm will tell you if you must know. But talk doesn't make enemies dead."),
("npc27_home_recap", "I'll make this short."),

("npc18_honorific" , "Great One"),
("npc19_honorific" , "Commander"),
("npc20_honorific" , "Commander"),
("npc21_honorific", "commander"),
("npc22_honorific", "commander"),
("npc23_honorific", "warrior"),
("npc24_honorific", "captain"),
("npc25_honorific", "commander"),
("npc26_honorific", "Master"),
("npc27_honorific", "Master"),

("new_companion_strings_end", "INVALID"),


## Companion Guildmaster Tip Offs Begin

("gondor_guildmaster_companion_player_ask", "By leave of the Lord of Gondor, I seek valiant confederates. Are there such in this place?"),
("gondor_guildmaster_companion_none", "Nay, Commander. What valour we have is needed to defend our own walls. You may go to the barracks and find soldiers of courage and experience - mayhap more the former than the latter, I fear. Ever have we been traders, crafters and farmers. The finest of our soldiers go to the capital to enlist - perhaps you should try the White City."),
("gondor_guildmaster_companion_player_none_ok", "Very well. I thank you for your counsel."),
("gondor_guildmaster_player_found_ok", "I thank you. May the good will of all good people go with you."),

("gondor_mt_guildmaster_companion", "Why, Commander, there is one, and gladly shall I tell you of him; he is a gate guard, by the name of Cirdil, and even now I warrant you’ll find him at his rounds. He is dutiful and brave - but I spoke with him of late, and it seems to me he wishes to do more than simply stand his watch on the walls while the Shadow gathers beyond them. Surely he will be happy to venture out from the White City in your company."),
("gondor_ha_guildmaster_companion", " Indeed there are. High in the esteem of our Captain Faramir are two of our commanders, Mablung and Damrod. Damrod is away at our Captain’s behest; but Mablung may be found in the cave yonder, a little way along this path here. We Rangers know much of woodlore and archery; Mablung stands above many of us. He is a man of prowess, and accounted one of our finest. Mayhap he will be given leave to accompany you for a time."),

("rohan_guildmaster_companion_player_ask", "By leave of Theoden King, I seek the aid of valiant Rohirrim. Will any stout warriors here follow me?"),
("rohan_guildmaster_companion_none", "It were better if you sought to bring aid, rather than asked for it. Horses, swords, spears - these things we need at present. As for your question: go to the barracks. There you will find those of our people willing to ride forth, such as they are - many beardless youths still, and still others unskilled herders and tenders of flocks."),
("rohan_guildmaster_companion_player_none_ok", "I do take thought for your people as well, Thain. Farewell."),
("rohan_guildmaster_player_found_ok", "That counsel seems good to me. Health be with thee at thy coming and going!"),

("rohan_edoras_guildmaster_companion", "Indeed, there may be. Dark indeed must the days become before our women ride out to war alongside the menfolk - yet our fearless and high-hearted Lady Eowyn, whom all love, rides and fights as well as any Marshal. Some shieldmaidens have trained with her from childhood, and several may be found around the Golden Hall. Hardy indeed are our women! Seek one called Galmyne - she is skilled in many arts of war, and goes about like a mare chafing at an ill-fitting bridle, for she has not been given leave to ride out with the men."),

("lorien_guildmaster_companion_player_ask", "Elder, I seek aid. The least among the Elves of Lorien fight like heroes of old; will any here join my cause?"),
("lorien_guildmaster_companion_none", "Evil has been seen and heard even here, among the mallorn-trees; sorrow has been known. In happier days we plucked the strings of harps; in these days we have indeed become skilled at the plucking of bowstrings. I cannot speak of heroes among us, but you should speak to the commander of our garrison here. Perhaps some few of our people may consent to join you for a time."),
("lorien_guildmaster_companion_player_none_ok", "I had hoped for fairer words in this fair land of yours. But it shall be as you say, Elder."),
("lorien_guildmaster_player_found_ok", "I thank you for your counsel, Elder. Tiro ven Elbereth!"),

("lorien_ca_guildmaster_companion", "Nan Belain, here is a wonder indeed! At any other time I might have had naught but disappointment for you, but now in the company of the Lord and Lady of the Wood stands none other than the Lord Glorfindel, hero of more battles than even I can remember. I know little of such a great champion’s purpose here - he arrived with the host of Elrond, Lord of Imladris, and his own counsel he keeps, speaking only with Lord Celeborn and Lady Galadriel. Seek him out, Commander. Perhaps his cause may be joined to yours."),

("beorn_guildmaster_companion_player_ask", "Your advice, good fellow - are there any warriors of remarkable prowess here?"),
("beorn_guildmaster_companion_none", "Well, I don’t know about that. Your question isn’t very clear. What kind of “remarkable prowess” do you want that you can’t find among our garrison, I ask you? We fight with stout staves and sharp hatchets, we shoot well enough with bows. I don’t know what more you could ask for."),
("beorn_guildmaster_companion_player_none_ok", "Well, then, I suppose I’d best be off. Good day to you, woodsman."),
("beorn_guildmaster_player_found_ok", "I see. Well, I shall look around for this “Dimborn”. Good day to you, woodsman."),

("beorn_house_guildmaster_companion", "Well, now, there’s a question. I’d say any of us could fight off a goblin or warg well enough, but our chief’s nephew is stouter than most. Spends most of his time just staring at trees, though. Or at nothing in particular. More thew than thought, if you take my meaning. Still, he’s gentle with his friends but fierce to his enemies, as one should be. Walks the woods as well as any Elf, I’d say. We call him Dimborn; not to be unkind, you understand, but we like calling things and people what they are. He ought to be around here somewhere."),

("woodelf_guildmaster_companion_player_ask", "By leave of Thranduil Elvenking, I seek champions of the Greenwood to fight in my command, Elder."),
("woodelf_guildmaster_companion_none", "Indeed? Then you may ask those of our garrison, and mayhap some will be willing to follow you. But I sense your desire runs deeper than that. Do you fancy yourself a great hero, like those from Nargothrond or Gondolin of old? Our finest warriors are needed to guard against the growing shadow in Mirkwood. Take with you what soldiers we can spare, and be content."),
("woodelf_guildmaster_companion_player_none_ok", "Very well, Elder. As you say."),
("woodelf_guildmaster_player_found_ok", "I thank you for your counsel, Elder. Navaer!"),

("woodelf_halls_guildmaster_companion", "Indeed? There is one among us whose aid you should not despise. Luevanna is her name, and she is kin to me, as it happens. She is young, as our people reckon it, and has an abiding love for the woods and all the creatures in it, save those which are evil. Hers is a gentle spirit - she has not fought in our array. Still, I have a hope that she may be persuaded to follow you, for then she may come to learn that though we love peaceful ways in peaceful days, times of war call for warlike deeds. See, there she stands - you may speak with her. Harthon gerithach lend vaer!"),

("dale_guildmaster_companion_player_ask", "Good master, I seek stout warriors of prowess to fight beside me in this war."),
("dale_guildmaster_companion_none", "Well, now. Here in our town, we have always plied our trades and managed our affairs quietly, and not until recently have we had a great need for fighting men. I suppose you might ask at our barracks, and find what recruits you can from our garrison. I know of none among our captains here who would abandon his post to follow you."),
("dale_guildmaster_companion_player_none_ok", "I will do that, good master. Farewell to you."),
("dale_guildmaster_player_found_ok", "Oft the unbidden gift proves the best value. I will speak to Faniul. Farewell!"),

("dale_main_guildmaster_companion", "Well, the King and his Lords have the best claim on the service of good captains. I don’t know that any of great renown are left to follow you - but are mere fighting men all you need? What about binders of wounds, versed in herblore? I know of one such - Faniul, personal healer to the King. She was midwife to my sister - and do not look askance at her age: she is of stout heart and sturdier than she looks. I warrant she’ll bear up well under the strains of travel. Why, I think I see her taking her ease over there, in this courtyard."),

("dwarf_guildmaster_companion_player_ask", "Good master, there seem to be some valiant warriors here. Will any follow my company?"),
("dwarf_guildmaster_companion_none", "Well, you’re not wrong, there, about our skill in battle, but aren’t our lads from our garrison here good enough for you? Apart from them, I don’t know anyone else who might satisfy you - you talk as though you were a king of some sort, looking for a great champion, like in the old days. Valiant is as valiant does, say I!"),
("dwarf_guildmaster_companion_player_none_ok", "You needn’t get so annoyed, good master, I was simply asking. Good day to you."),
("dwarf_guildmaster_player_found_ok", "That is excellent to hear, good master. Good day to you!"),

("dwarf_erebor_guildmaster_companion", "Oh ho! It’s warriors you’re after, are you? Then I have just the Dwarf for you: look for one Kili Goldfinger. A most excellent and audacious Dwarf he is, and a credit to his clan. Fights almost as well as a Longbeard, though he’s still fairly young as we reckon it. Quite good at story-telling, too, and he favours the cheerful sort of tale. Go and have a talk with him - I shouldn’t think he needs much persuading to follow you out into the wide world and do his bit for the war. Now, let me see… he’s not down here at the moment. Not the Great Chamber, either. The upper halls, perhaps - look for him there."),

("rhun_guildmaster_companion_player_ask", "I heard there were great warriors here. Where are they? Who are worthy to join me?"),
("rhun_guildmaster_companion_none", "Not all our warriors here are blooded, but each of them is stronger and braver than any ten Dalishmen! Go and ask the arms master to see if he can spare any for you."),
("rhun_guildmaster_companion_player_none_ok", "I ask for great warriors, and you show me drinkers of mother’s milk. Pah!"),
("rhun_guildmaster_player_found_ok", "That is good to hear. Finally - a warrior with spirit!"),

("rhun_maincamp_guildmaster_companion", "Our greatest swordbearers and riders fight in the retinues of our warlords. But there is one who has found favour with none of our chiefs so far. Not because he is weak; far from it! He does not curb his tongue when he speaks, and he has spoken loudly against our chieftains, saying they are slow to act and over-cautious. If he had his way, I wager the countryside would be covered in flames by now. His name is Varfang, and he spends his hours training near the prisoner cages, not far from this tent."),


("guldur_guildmaster_companion_player_ask", "All I see here is a rabble of treacherous skulkers, more likely to run than fight. Where are your proper warriors?"),
("guldur_guildmaster_companion_none", "O ho! What do we have here? A great captain, are you? I reckon your bark’s worse than your bite, and no mistake. Orders are orders: you draw your troops from our garrison here, and that’s that. Keep talking like that where they’ve got ears to hear, though, and someone will stick a knife in your back one of these days, see if they don’t."),
("guldur_guildmaster_companion_player_none_ok", "You’ll watch your words with me, if you know what’s good for you."),
("guldur_guildmaster_player_found_ok", "Scared witless by this woman, are you? I’ll go see if she’s all you make her out to be. This had better not be a waste of my time!"),

("guldur_main_guildmaster_companion", "We’ve got stout lads aplenty, curse you. Ha… I know what you’re really after. Oh yes, indeed, I know just where you should go, Commander. See that cave over there, with steps leading down? If our boys get hurt badly enough we send them down there, and I reckon almost a third of them make it back up, har! They can do very strange things, down there… and that one in particular, the woman… she gives me the shivers, and that’s saying something. They say she’s got something to do with Number One, or even Higher Up, if you take my meaning. Talk to her, if you dare."),


("moria_guildmaster_companion_player_ask", "All I see here is a rabble of treacherous skulkers, more likely to run than fight. Where are your proper warriors?"),
("moria_guildmaster_companion_none", "Proper warriors, {she/he} says! I reckon any of our snaga could give any of your lubbers a good drubbing. We’re a tough lot, we are, and no mistake. Go speak to our barracks master - but speak with respect, mind, or you’ll not get our stout fellows to follow you. Knife you as soon as your back is turned, if you don’t speak proper."),
("moria_guildmaster_companion_player_none_ok", "I’ll speak how I like to the lot of you. I save my respect for those much Higher Up than your sort!"),
("moria_guildmaster_player_found_ok", "Garn! A sawbones, you say? Among this lot? All right, I’ll have a talk with him, but you’d better hope you aren’t telling me a crock of rubbish."),

("moria_main_guildmaster_companion", "Ha! Losing more than you can keep, are you? Throwing our stout lads into the meat grinder, and then cursing when you find you haven’t got enough left to win your battles? A right splendid commander you are, oh yes. Very well - look over there! I’ll give you a helpful hint now, and you’ll remember it, yes? You see that fellow on the crates, the one with blood all over his hands, muttering to himself? Not much of a killer, but where’s the blood from, I hear you ask? Why, it’s the blood from some of our fighters he’s helped put back on their feet. He’s a sawbones, that one. You’ll see for yourself, the next time you lead your troops into another mess and find you need some stitching done."),


("isengard_guildmaster_companion_player_ask", "I’ve heard about the fighting Uruk-hai. So far, I’m not impressed. Where are the greatest among them?"),
("isengard_guildmaster_companion_none", "Leading patrols and armies of their own, no doubt - why would they lower themselves to fight under your command? They’ve got their own Orders to follow, from Higher Up. If you want fighting lads, go talk to the garrison chief! We’ve got stout fellows aplenty."),
("isengard_guildmaster_companion_player_none_ok", "This rabble isn’t what you make it out to be. Stout fellows? Fighting lads? Snagas aplenty, more like. Slavering swine."),
("isengard_guildmaster_player_found_ok", "If he kills well, I’ll take him. If not, I’ll gut him like a fish. And if he does turn out to be just another worthless maggot, I’ll come back and pay you for wasting my time!"),

("isengard_main_guildmaster_companion", "A great commander you are, it is plain to see, and wisely do you choose to take only the bravest and most skilled fighters under your banner. And yet, if you will take my counsel - a battle is won not merely with iron and sinew, Commander, but with guile and foreknowledge of the foeman’s doings, his comings and goings. We have a scoutmaster here, an Orc who has sworn allegiance to Saruman the Great. I have heard that he spent many years in the Misty Mountains, catching and taming wargs. A skilled tracker and hunter is Durgash. You will find him a most useful helper, Commander. He's usually lurking around the warg pits."),
("isengard_hunting_camp_guildmaster_companion", "O ho! So you think our finest lads should humble themselves and take orders from you, do you? You’re a bold one, and no mistake. I know just the fellow for you. Calls himself Gulm, and he’s a proper fierce one, he is. Never seen anyone take so much pleasure in bashing in skulls and breaking bones with that mallet of his. And the more foes he kills, the more savage he seems to get. I don’t rightly know where he is at the moment, though - but he’s in this camp for sure, trying not to attract attention for some reason. Does that sound suitable for you, O Great Commander, taking an Uruk-hai berserker into your camp?"),

("dunland_guildmaster_companion_player_ask", "So, these are the Men of the hills who serve the White Hand! A sorry-looking lot. Where are your fighters of note?"),
("dunland_guildmaster_companion_none", "Following those greater than you, no doubt. If you want warriors, speak to the training masters. See for yourself if any of our young pups will follow you into battle."),
("dunland_guildmaster_companion_player_none_ok", "Curs and whelps! It is no wonder your people were driven into the hills by the men of Rohan."),
("dunland_guildmaster_player_found_ok", "A treacherous wolf, I would hardly keep by my side. But a tame hunting dog, I might consider. Let me see which one this Heidrek proves to be."),

("dunland_main_guildmaster_companion", "Despise us at your peril! Even a wretched cur will snap at your heels in a fight. We will have our vengeance on the Forgoil and their allies - and likely it will be Heidrek whom we’ll follow into Edoras. He’s a mongrel, that one - says he’s the grandson of a strawhead king, for all that he looks no different from any of us. He’s a terror in the training yard. If Chief Daeglaf doesn’t watch his back he just might find Heidrek’s spear in it one of these days. Maybe he’ll deign to follow you, if he thinks you’re worth his time. Look for him at the main campfire, where our chieftains stand."),


("khand_guildmaster_companion_player_ask", "I heard there were great warriors here. Where are they? Who are worthy to join me?"),
("khand_guildmaster_companion_none", "Those who have earned their death masks wish to follow commanders of still greater renown, but you may look for new recruits among our pitfighters and levies. Do not presume more than your station, Commander! "),
("khand_guildmaster_companion_player_none_ok", "I ask for warriors and you show me pit slaves and unblooded peasants. Waste my time at your peril."),
("khand_guildmaster_player_found_ok", "She sounds like a killer, right enough - but can her ferocity be leashed to useful purpose? We shall have to see."),

("khand_main_guildmaster_companion", "So you want great warriors? We have them aplenty. But let me tell you of one whose savagery even we find astonishing. Her name is Turmbathu - yes, a woman! I would not have believed it myself had I not seen her in the fighting pit with my own eyes. Defeated three men at once, and killed one of them. Unfortunate, that - the one she killed was a son of Great Lord Lurmsakun, and so now you may find her among the prisoners, awaiting a painful death… unless you, Commander, can intercede. Such a pity, to waste such strength."),

("umbar_guildmaster_companion_player_ask", "So, the people here fancy themselves heirs of greatness, do they? Can anyone here stand proof of such claims?"),
("umbar_guildmaster_companion_none", "You come at the wrong time, Commander. Now we’re all basking in the glory of capturing this holding, and working out the equitable distribution of its wealth - to put it another way, the captains are all at one another’s throats, heated words are being said, and it will not be long ere blood of Umbar is spilled by Umbar hands. Some of the sailors are unhappy, and may consent to follow you instead of their former captains. That’s the best I can do for you at the moment, Commander."),
("umbar_guildmaster_companion_player_none_ok", "Disappointing. But not unexpected of sea-dogs. I shall have to look elsewhere for the quality I seek."),
("umbar_guildmaster_player_found_ok", "A corsair with a code of honour! Not unheard of, but not often found. I care only that he will go where I command, and kill as I instruct."),

("umbar_main_guildmaster_companion", "Why, if I guess aright you seek the finest fighters among us to join your ranks. After the recent burning of our Haven, I’m afraid our best sailors and raiders follow only our most experienced captains. But I have a friend, named Fuldimir, who has been passed over for promotion too many times, to my mind. It’s that strange way of thinking he has - he will not steal, he says, from any who still draw breath. Where’s the sense in that, I ask you? Still, he is handy with a cutlass, and as tough as any hardy seafarer. Here he is, in this tent - you may speak with him."),


("mordor_guildmaster_companion_player_ask", "So, these are the finest in the Black Land, are they? Not much to look at. Tell me who’s actually useful in a scrap."),
("mordor_guildmaster_companion_none", "O ho, a mighty champion is here, I see! And of course, the mighty champion wants only the very best fighters, and no mistake! Well, well! Maybe you’ll find that some of the lads here have plans of their own, to rise high in the sight of the Eye. Maybe you’ll find Lugbúrz thinks a little better of them than of you. Won’t surprise me, ha! Why don’t you just go along to the barracks and requisition your troops like everyone else."),
("mordor_guildmaster_companion_player_none_ok", "Oh, I’ll remember this slight, mark my words. Do me a good turn, and I’ll not forget it, but speak uncivilly to me, and you’ll soon see what I can do about that."),
("mordor_guildmaster_player_found_ok", "Well, I’ve struck a bit of luck at last, I see! You’ve done well. I’ll report your contribution."),

("mordor_morgul_guildmaster_companion", "You’ll want an Uruk for that, mark my words. The best fighters for sure in this sorry-looking lot. Now, if you’re looking for a trusty lad to watch your back in a fight, I’ll tell you straight: you’ll not find better than old Gorbag. Used to be a comrade of mine, before I got assigned here, a while after the Great Signal went up. Now that he’s off the patrol lists, he could join up with you right enough. He ought to be up there somewhere, by that big ruined Tower where the Bosses meet to talk sometimes. Looking down at the rest of these dunghill rats - he likes to do that, he does, ha!"),


("harad_guildmaster_companion_player_ask", "I heard there were great warriors here. Where are they? Who are worthy to join me?"),
("harad_guildmaster_companion_none", "It is not accordant to our creed for our greatest to join with such as thee, O Commander. In the world, there are the great and the small; for soldiers such as ourselves, always we stand in this relation to one another. I counsel you to seek out those who could learn from you in battle; it is better not to try yoking a mighty stallion to a weakly-made plow, for the stallion would then destroy the plow, to the detriment of all."),
("harad_guildmaster_companion_player_none_ok", "If I understand you correctly, you’ve just disrespected me. I’ll remember this."),
("harad_guildmaster_player_found_ok", "I see. I hope this Lykyada is as great a warrior as you say he is."),

("harad_main_guildmaster_companion", " I heard a story around the fires: when the Black Serpent called his bannermen, who are some of our finest horse archers, many boasted of how all the treasures of the West would soon be theirs; but one whom we call Lykyada stood apart and remained silent. And when they asked him what he hoped to take from the West, he stooped, scooped up a handful of sand, and said, “What do I require that the land of my birth has not already given me? Behold, I make a gift to them of the sand on which I have stood.” And so saying, he let the wind from the east blow the sand away, into the west. Then all who heard this repented of their injudicious words, and swore to follow his lead. If he finds you worthy, Commander, he may follow yours. Look for him where he stands in attendance upon our chieftains."),

#Rohan Horburg Companion added down here for savegame compat.
("rohan_hornburg_guildmaster_companion", "All here at the Hornburg have their given duties, Commander - all save one, I should say. Maybe that one will ride out with you, for otherwise he should be lucky if another Éored will consent to have him! A drunken sot is our Ulfas - good cheer he brings to his comrades, and he is a skilled Rider, but loth is he to set down a tankard without first draining it! Look for him in the hall yonder, if that does not trouble you."),

# Imladris Strings

("imladris_guildmaster_companion_player_ask", "Elder, I seek the aid of renowned warriors, Man or Elf, from the fabled North."),
("imladris_guildmaster_companion_none", "Look well, Commander. Before you is perhaps the last great muster of the North, in this Age and any Age hereafter. Man and Elf alike, we who have come here do not hope to return. From the Last Homely House we have come; from the vales and forests of Eriador the last of the Núnatani, whom you call Dúnedain, have come. Each of us has his appointed tasks - none may follow you as you wish, save that you exercise your writ and recruit from our garrison. "),
("imladris_guildmaster_companion_player_none_ok", "I understand, Elder. I thank you for your time."),
("imladris_guildmaster_player_found_ok", "I understand, Elder. I thank you for your time."),

# Show Keybind for New Form
("show_keybinds_form", "Special Key Bindings: ^^ Formation Keys:^ Use F1-F4 to order selected divisions. ^Keep the F1 key down to place selected divisions.^Place on enemy division to target.^^ Cycle Through Weapon Usage - O ^^ Cycle Through Camera Type - CTRL+END ^^ Rally - V ^^ Call Horse - M ^^ View Orders / Minimap - Backspace"),

#Mordor Orc patrol camp (internally named cirith ungol) Companion added down here for savegame compat.
("mordor_cungol_guildmaster_companion", "O ho, you want a fighter! I’ve got just the lad for you. He’s a favourite of the Big Bosses, that one. Do not be deceived by his small stature, oh no! Why, I warrant he’d be a Boss himself before too long, the way he’s been carrying on! Just put a nice big axe in old Ufthak’s hands, put him right in the front, and watch him go! Cause the enemy no end of grief, he will, and no mistake! ‘Ere, pipe down, lads! What’re you laughing about? Go on about your rounds, you maggots! Sorry about that, Commander, these louts are an undisciplined lot. Not like Ufthak! Take him along, Commander, you won’t regret it. You can trust Ufthak with your very life. See, there he stands his watch, atop the tower. Cuts a majestic figure, eh?"),
]
