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
  ("custom_battle_2", "Celeborn from Lorien is leading a patrol of horsemen and archers\
 when forward lookout brings a warning of a force of ash-faced evil men approaching.\
 It's the dreaded Black Numenoreans! Those were not seen near Lothlorien for ages,\
 but now they must be driven back to the neverworld."),
  ("custom_battle_3", "Lord Grimbold of Rohan is leading the last defence of the walls against an army if Isengard.\
 Now, as the besiegers prepare for a final assault on the walls, he must hold the walls with courage and bright steel."),
  ("custom_battle_4", "When the scouts inform Lord Beranhelm of the approach of an Rhun war band,\
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
  ("npc9_intro", "Ssh! If you just as wave to the guards, I'll slice out your gizzard and feed it to the wargs!"),
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
  ("npc16_backstory_a", "Well now, it is the stranger who should declare himself first. Nevertheless, I am Varfang of the Balcoth kin... I can tell that you have not yet heard the songs or tales of my land that speak the name of the Balcoth, for the very name would check your courage and fill your heart with woe."),
  ("npc17_backstory_a", "They call me Dímborn and I work in the woods. It is nice there. I like the woods. Many trees in the woods. I like trees. I've worked in the woods all my life, because I am strong and because I like trees."),

#backstory main body
  ("npc1_backstory_b", "You should know that I am an Ithilien Ranger of Dúnedain descent and valor. I know much of tracking and scouting and my skill with bow and sword is known to the orc. I can also train any soul that's willing to fight the coming Shadow."),
  ("npc2_backstory_b", "I have been trained as a Minas Tirith watchman, to keep order in the White City and serve my lord Steward."),
  ("npc3_backstory_b", "I am a Rider of the West Emnet éored - they left without me on a long patrol to the Isen fords. I know their conduct will be worthy of the green banner, but I fear many won't return."),
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
  ("npc16_backstory_b", "The Balcoth were a fierce race of men from my home land, slaughtered by these westerlings to all but a few men. Chased down like beasts of burden as food for their blades. The blood spilt by those blades is the same blood that flows within me, for within me their house continues."),
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
  ("npc16_backstory_later", "Long does the history of my people recount these lands. I know not what their treacherous histories say of days when my people before entered this land, but sad and dark will their histories be as my people enter it now. Like a storm of hooves and swords and arrows, we will bring them doom like the Balcoth before us."),
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


  ("npc1_2ary_morality_speech", "Captain, I have been raised as a Dúnedain, both in valor and honour. I would prefer if we don't {s21}."),
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
   
  ("npc1_personalitymatch_speech_b", "I find the company of {s11} very pleasing and her native woodcraft a rare glimpse in what remains of Sindarin skills in the world. You know, my father named me after the legendary Sindarin Elf captain serving King Thingol of Doriath and I always feel a special bond to the fair race."),
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
  ("npc5_home_intro", "Daro! That's Isengard and the black tower of Orthanc ahead. Much have changed since I last saw them, and none for the better."),
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
  ("npc6_home_description", "I have never ventured this far, but I overheard our Greenwood scouts say there may be Nazguls here. I feel an evil presence, but I cannot put a name to it. It is powerful, though, so let us be prepared."),
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
  ("npc7_home_description_2", "If the fates of war ever provide us with a large army, we should risk the entrance to the Mines and retrieve their mighty riches."),
  ("npc8_home_description_2", "I can smell the fragrance of many sweet flowers and see the bees harvesting their nectar. If you don't mind, I will gather some herbs for our own use, it will only take a moment."),
  ("npc9_home_description_2", "There's no use trudging around here if we are not backed by a large Uruk-hai horde. Unless you want to make faces at the lookouts on the wall, that is."),
  ("npc10_home_description_2", "Minas Morgul, where Nazguls drink all day, har-har!"),
  ("npc11_home_description_2", "Doesn't Orthanc look like a giant... something?"),
  ("npc12_home_description_2", "Doesn't Orthanc look like a giant... something?"),
  ("npc13_home_description_2", "Minas Morgul, where Nazguls drink all day, har-har!"),
  ("npc14_home_description_2", "Minas Morgul, where Nazguls drink all day, har-har!"),
  ("npc15_home_description_2", "Minas Morgul, where Nazguls drink all day, har-har!"),
  ("npc16_home_description_2", "Minas Morgul, where Nazguls drink all day, har-har!"),
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

  # ("swadian_rebellion_pretender_intro",    "I am Isolla, rightful Queen of the Swadians."),
  # ("vaegir_rebellion_pretender_intro",     "My name is Valdym. Some men call me 'the Bastard.' I am a prince of the Vaegirs, but by all rights I should be their king, instead of my cousin Yaroglek."),
  # ("khergit_rebellion_pretender_intro",    "I am Dustum Khan, son of Janakir Khan, and rightful Khan of the Khergits."),
  # ("nord_rebellion_pretender_intro",       "I am Lethwin Far-Seeker, son of Hakrim the Old, who should be king of the Nords of Calradia."),
  # ("rhodok_rebellion_pretender_intro",     "I am Lord Kastor, the rightful King of the Rhodoks, who will free them from tyranny."),

  # ("swadian_rebellion_pretender_story_1",  "I was the only child of my father, King Esterich. Although I am a woman, he loved me like a son and named me his heir -- not once, but several times, before the grandest nobles of the land so that none could doubt his intention. There is no law that bars a woman from ruling -- indeed, we Swadians tell tales of warrior queens who ruled us in our distant past."),
  # ("vaegir_rebellion_pretender_story_1",   "My father died when I was young, leaving me in the care of his brother, the regent Burelek. But rather than hold the throne until I came of age, this usurper used his newfound power to accuse my mother of adultery, and to claim that I was not my father's son. She was executed for treason, and I was declared a bastard."),
  # ("khergit_rebellion_pretender_story_1",  "Sanjar Khan and I are brothers, sons of the old Janakir Khan, although of different mothers. Although I was the younger brother, all those who knew the old Khan will testify that throughout my father's life, I was his favorite, entrusted with the responsibilities of government. Sanjar busied himself with hunts and feasts to win the affection of the more dissolate of my father's commanders."),
  # ("nord_rebellion_pretender_story_1",     "I am called the Far-Seeker because I have travelled great distances, even by the standards of the Nords, in search of knowledge. Before I came of age, my father sent me abroad on a tour of study at the courts and universities in the lands overseas. If the Nords are to call themselves the heirs of the Calradian empire, then they must act the part, and know something of law and letters, and not call themselves content merely to fight, plunder, and drink."),
  # ("rhodok_rebellion_pretender_story_1",   "The Rhodoks are a free people, and not slaves to any hereditary monarch. The king must be chosen from one of the leading noble families of the land, by a council drawn by lot from the patricians of the cities of Jelkala, Veluca, and Yalen. The council meets on a field before Jelkala, and no man is allowed to appear in arms during their deliberations, on pain of death."),

  # ("swadian_rebellion_pretender_story_2",  "Yet when my father died, his cousin Harlaus convinced the nobles that no Swadian king of sound mind could name a woman as his heir. Harlaus said that his designation of me was the act of a madman, and thus had no legal standing, and that he, as my father's closest male relative, should of take the throne."),
  # ("vaegir_rebellion_pretender_story_2",   "I was smuggled abroad by a faithful servant, but now I am of age and have returned to reclaim what is rightfully mine. Burelek died soon after his act of perfidy -- the judgment of heaven, no doubt. His son Yaroglek now calls himself king, but as his claim is tainted, he is no less a usurper than his father, and I will topple him from his throne."),
  # ("khergit_rebellion_pretender_story_2",  "According to Khergit custom, when a man dies his herds are split between all his sons, equally. So too it is with the khanate. When I heard of my father's death, I was away inspecting our borders, but I hurried home to Tulga, ready to give Sanjar his due and share the khanate with him. But when I arrived, I found that he rushed his supporters to the court, to have himself proclaimed as the sole khan."),
  # ("nord_rebellion_pretender_story_2",     "My father died however before I completed my course of study, and as I hurried home to claim his throne my ship was wrecked by a storm. One of my father's thanes, Ragnar, seized this opportunity and spread rumors that I had died abroad. He summoned a gathering of his supporters to have himself proclaimed king, and has taken the past few years to consolidate his power."),
  # ("rhodok_rebellion_pretender_story_2",   "During the last selection, there were but two candidates, myself, and Lord Graveth. While the council was deliberating, Graveth appeared, sword in hand, telling them that a Swadian raiding party was about to descend on the field of deliberation -- which was true, by the way -- and if he were not elected king, then he would leave them to their fate."),

  # ("swadian_rebellion_pretender_story_3",  "I will admit that I did my cause no good by cursing Harlaus and all who listened to him as traitors, but I also believe that the magistrates who ruled in his favor were bought. No matter -- I will raise an army of loyal subjects, who would honour their old king's memory and will. And if anyone doubts that a woman can wield power, then I will prove them wrong by taking Harlaus' ill-gotten crown away from him."),
  # ("vaegir_rebellion_pretender_story_3",   "Until I have my rights restored in the sight of all the Vaegirs, I will bear the sobriquet, 'the Bastard', to remind me of what I must do."),
  # ("khergit_rebellion_pretender_story_3",  "My brother thinks that Khergits will only respect strength: a leader who takes what he wants, when he wants it. But I think that he misreads the spirit of our people.--we admire a resolute leader, but even more we a just one, and we know that a man who does not respect his own brother's rights will not respect the rights of his followers."),
  # ("nord_rebellion_pretender_story_3",     "So I remain in exile -- except now I am not looking for sages to tutor me in the wisdom of faraway lands, but warriors, to come with me back to the land of the Nords and regain my throne. If Ragnar doubts my ability to rule, then let him say so face to face, as we stare at each other over the rims of our shields. For a warrior can be a scholar, and a scholar a warrior, and to my mind, only one who combines the two is fit to be king!"),
  # ("rhodok_rebellion_pretender_story_3",   "Well, Graveth defeated the Swadians, and for that, as a Rhodok, I am grateful. When I am king, I will myself place the wreath of victory on his head. But after that I will have it separated from his shoulders, for by his actions he has shown himself a traitor to the Rhodok confederacy and its sacred custom."),

  # ("swadian_rebellion_monarch_response_1", "Isolla thinks she should be Queen of the Swadians? Well, King Esterich had a kind heart, and doted on his daughter, but a good-hearted king who doesn't use his head can be a curse to his people. Isolla may tell you stories of warrior queens of old, but you might also recall that all the old legends end in the same way -- with the Swadians crushed underfoot by the armies of the Calradic Emperor."),
  # ("vaegir_rebellion_monarch_response_1",  "Were Valdym to come to me in peace, I would laden him with titles and honours, and he would become the greatest of my vassals. But as he comes in war, I will drag him before me in chains and make him acknowledge me as rightful sovereign, then cut his tongue from his mouth so that he cannot recant."),
  # ("khergit_rebellion_monarch_response_1", "My brother Dustum has perhaps told you of his insistence upon splitting the khanate, as though it were a herd of sheep. Let me tell you something. Ever since the Khergits established themselves on this land, the death of every khan has had the same result -- the land was divided, the khan's sons went to war, and the strongest took it all anyway. I simply had the foresight to stave off the civil war in advance."),
  # ("nord_rebellion_monarch_response_1",    "Lethwin 'Far-Seeker'? Lethwin Inkfingers, is more like it. Perhaps you have heard the expression, 'Unhappy is the land whose king is a child.' Unhappy too is the land whose king is a student. You want the Nords to be ruled by a beardless youth, whose hand bears no callouses left by a sword's grip, who has never stood in a shield wall? If Lethwin were king, his thanes would laugh at him to his face!"),
  # ("rhodok_rebellion_monarch_response_1",  "No doubt Lord Kastor told you that I defiled the hallowed Rhodok custom by interfering with the patricians' election of a king. Well, let me tell you something. The patricians of the towns make longwinded speeches about our ancient liberties, but then choose as their king whichever noble last sat in their villa and sipped a fine wine and promised to overlook their unpaid taxes."),

  # ("swadian_rebellion_monarch_response_2", "Those who weep for the plight of a Swadian princess denied her father's throne should reflect instead on the fate of a Swadian herdswoman seized by a Vaegir raider and taken as chattel to the slave markets. Talk to me of queens and old stories when our warlike neighbors are vanquished, and our land is at peace."),
  # ("vaegir_rebellion_monarch_response_2",  "Whatever my father may or may not have done to secure the throne does not matter. I have inherited it, and that is final. If every old claim were to be brought up anew, if every man's inheritance could be called into question at any time, then it would be the end of the institution of kingship, and we would live in a state of constant civil war."),
  # ("khergit_rebellion_monarch_response_2", "Dustum would make a fine assessor of flocks, or adjudicator of land disputes. But can you imagine such a man as khan? We would be run off of our land in no time by our neighbors, and return to our old days of starving and freezing on the steppe."),
  # ("nord_rebellion_monarch_response_2",    "Old Hakrim may have had fancy ideas about how to dispose of his kingdom, but it is not just royal blood that makes a King of the Nords. I am king by acclamation of the thanes, and by right of being the strongest. That counts for more than blood, and woe to any man in this land who says otherwise."),
  # ("rhodok_rebellion_monarch_response_2",  "The only liberty that concerns them is their liberty to grow fat. Meanwhile, my men sleep out on the steppe, and eat dry bread and salt fish, and scan the horizon for burning villages, and shed our blood to keep the caravan routes open. Here's an idea -- if I ever meet a merchant who limps from a Khergit arrow-wound or a Swadian sword-stroke, then I'll say, 'Here's a man whose counsel is worth taking.'"),


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
("gondor_rumor_17", "There is a strange black rock near Erech. I went to see it once with my father. People say it's laid over a chamber where the last son of the sea kings sleeps. I think it's just a rock."),
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
("dunland_rumor_3", "Strawheads will cough out our land! Together with their blood! Gah!"),
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
("beorn_rumor_13", "*GROWLS*   Do you have any honey?"),
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
("woodelf_rumor_3", "Darknes and evil creep over these once beautiful woods. Unless they are stopped, they will smother all hope, all light."), 
("woodelf_rumor_4", "Quick and nimble, quiet and precise, we can yet keep the Darkness at bay. But how much longer?"),
("woodelf_rumor_5", "Shhh, no dhínen! There may be orcs lurking around. We must be on guard!"),
("woodelf_rumor_6", "*stares at you, obviously annoyed by your presence*"), #[color=red]removed text, because the player could be a Woodelf too and stil get this rumour as if he's foreign[/color]
("woodelf_rumor_7", "Oduleg hi am man theled? We need to know your purpose here. Sorcerrer's spies are everywhere."),
("woodelf_rumor_8", "Edain of Dale make intricate toys these days! They've learnt much from the Naugrim."),
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
("harad_rumor_7", "I'd never set foot on a ship. Corsairs can have all the seas as far as I am concerned."),
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
("umbar_rumor_3", "Umbar is our fate! And it will be Gondor's too."),
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
("neutral_rumor_4", "Stay clear of Fangorn forest."),

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
("fullname_region_subfac_dol_amroth", "Belfalas, the costal region in the Shouth of Gondor"), #subfac_dol_amroth
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
("fullname_region_gap_of_rohan","the Gap of Rohan, the eastermost border of Rohan, a contested area between the Rohirrim and the Dunlendings."),

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
("fullname_region_n_mirkwood", "the dense forests of northen Mirkwood, home of the Woodelves" ),#region_n_mirkwood = 33
("fullname_region_s_mirkwood", "the dense forest of southern Mirkwood, said to be infested by strange creatures" ),#region_s_mirkwood = 34
("fullname_region_above_mirkwook", "Northen Rhovanion, the area between Mirkwood and the Grey Mountains in the North" ),#region_above_mirkwook = 35  (FOR LACK OF A BETTER GEOGRAPHICAL NAME)
("fullname_region_grey_mountains", "the foothills of Grey Mountains, where Dwarves dwell" ),#region_grey_mountains = 36
("fullname_region_mordor", "Mordor, the dark Realm of Sauron" ),#region_mordor = 37



("shortname_region_unknown", "an unnamed region"), # -1

("shortname_region_pelennor", "Pelennor Fields"), #0
("shortname_region_subfac_pelargir", "Fiefdom of Lebennin"), # pelargir
("shortname_region_subfac_dol_amroth", "Belfalas"), #subfac_dol_amroth
("shortname_region_subfac_ethring", "Ringló Vale"), # subfac_ethring
("shortname_region_subfac_lossarnach", "Fiefdom of Lossarnach"),
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


# Traits - titles and descriptions (the first is used in constants!)
# Also note: these need to be of the same order and number as slot_trait_* in constants

("trait_title_elf_friend", "Elf_Friend"),
("trait_desc_elf_friend", "You_have_become_highly_esteemed_by_the_Elves_and_they_now_regard_you_as_a_trusted_ally._The_cost_to_recruit_elves_has_been_reduced_and_you_may_now_attempt_to_give_orders_to_elven_armies."),

("trait_title_gondor_friend", "Steward's_Blessing"),
("trait_desc_gondor_friend", "You_have_become_highly_esteemed_by_the_Steward_Denethor_and_your_status_has_risen_among_the_men_of_Gondor_as_a_result._The_cost_to_recruit_Gondorians_has_been_reduced_and_you_may_now_attempt_to_give_orders_to_Gondorian_armies."),

("trait_title_rohan_friend", "King's_Man"),
("trait_desc_rohan_friend", "You_have_become_highly_esteemed_by_King_Theoden_of_Rohan_and_your_status_has_risen_among_the_men_of_Rohan_as_a_result._The_cost_to_recruit_Rohirrim_men_has_been_reduced_and_you_may_now_attempt_to_give_orders_to_the_armies_of_the_Riddermark."),

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
("trait_desc_berserker", "After_many_battles_where_you_eschewed_the_use_of_armor_your_ferocious_will_has_become_like_iron._In_battles_where_you_are_gravely_wounded_you_will_receive_a_health_bonus_once_per_battle._This_will_not_restore_you_to_full_strength_but_may_keep_you_going_long_after_others_would_have_succumbed_to_their_wounds."),

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
("dwarf_gift4", "Marvellous Jewellry"),

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
("imladris_gift4", "Healing Herbs and Oitments"),

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

]
