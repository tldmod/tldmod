# -*- coding: utf-8 -*-
####################################################################################################################
#  Each quest record contains the following fields:
#  1) Info page idnt: Used for referencing info pages in other files. The prefix ip_ is automatically added before each info page id.
#  2) Info page name: Name displayed in the info page screen.
#  3) Info page text: Text displayed in the info page screen.
####################################################################################################################

info_pages = [
 ("formations_and_morale",
  "Formations and Morale",
  '''
  Your troops will position themselves and hold at the beginning of each battle, instead of blindly charging. Only major factions (all 18 of them) use formations (+deserters), bandits will simply charge. There is a slight difference between good and evil factions, good infantry will form shield walls (usually defensive - shielded troops first, but it can form a phalanx if you have pikemen), while evil infantry will form ranks (best troops first). Formations only work in field battles (meaning not in custom battles and sieges).
  
  Any time in-game that you have a formation form or "Hold", it will set up near the position that the player had when the command was issued: infantry to the left, cavalry to the right, and archers up front. Additionally, the formations may maintain the same FACING that the player had (depending on mod design). Whenever a unit first forms a particular formation, troops may spread out for ease of forming up (depending on mod design). Player troops start every battle in formation. Unless changed by mod design, formation key bindings are: "J" for ranks, "K" for weapon-based ranks (shieldwall, phalanx),"L" for wedge (the player ought to reassign the "L" for "Log" mapping)";" for square, "U" for no formation (undo formation). The "ranks" command for archers puts them in a staggered line. Cavalry will not make any formation other than the wedge.
  
  Charge (and Dismount for cavalry) will undo a formation. The player may Advance multiple times to have a formation move toward the average position of the enemy. Or use the order panel or hold-F1 to place them (or sweep them across the enemy for the cavalry wedge). As a leader it's your responsibility to keep your troops in order during battle. The more casualties your side suffers, the more their morale crumbles. Keep watching for messages popping up! You can support your troops in two ways:

  1. Killing enemies. If you do well, you impress your men and they fight harder and don't flee.
  
  2. Rallying them. If your troops are fleeing, press "V". Your character will sound a horn and rally the troops. You get only a limited amount of rallies per battle! (the amount is based on your Charisma and Leadership)

  It can be quite the advantage if you manage to defeat the enemy commander, because that robs enemies of their leader, they cannot be rallied. Therefore once you manage to rout them, they're gone.
  '''),

 ("economy",
  "Economy",
  '''
  There is no money in TLD. Instead you develop relationships with factions - represented by Resources, Influence and Rank.
  
  Resources are what's needed to sustain the faction in war - you can redeem looted scraps and items for it and you're also given a certain number of resource allowance each week depending on your rank within a faction. You can use this allowance to get soldiers, gear, horses for you to command and companions to follow you, but only if you accumulated enough. You have a separate resource/influence/rank pool for each Faction, remember that!
  Influence points are awarded for finishing quests and winning tough battles. They can later be spent on special items as a reward from the rulers of factions you got the influence with.

  Rank points allow you to rise up in the ranks of your faction - this will determine your max party size, weekly resource income and unlock other stuff.
  Due to being true to lore, we have also disabled by default the option of the so called "cross-dressing": a Gondorian wouldn't likely ever wear looted orc armour, and vice-versa. After most battles, you will find few or no items in the loot which can be used directly. Instead, "metal scraps" are dropped, which represent salvageable equipment and can then be given to your smiths who require them, for Resource Points.
  '''),

 ("war_of_the_ring",
  "War of the Ring",
  '''
  At the beginning of the game the War between good and evil hasn't started yet. You'll be notified when it does. (This does NOT depend on time spent playing, rather on how ready your character is for the war.) While Middle Earth might look like a pretty empty and quiet place at start, it gets filled with hostile parties very quickly once the War starts. Be prepared and use your few days of peace wisely! You can perform quests for the lords and leaders of all allied factions, raise troops and train yourself in the barracks.

  The war itself can be won or lost, unlike in the original M&B. Every faction has a strength rating - which changes according to faction successes or failures in battles. With strength dropping low enough, it becomes possible for enemies to siege faction cities/camps. When a faction drops to the lowest status, it is possible to defeat it completely by storming its capital.

  Note that player himself cannot initiate sieges in TLD. He can only help his faction and allies in siege battles if their leaders decide that it is time to go storm the enemy settlement.

  (This is a design decision, not a bug. It's also something we want to tweak in future releases, so the option to siege is available, but very costly and difficult to obtain)

  There are several theatres of war in TLD, defined by geography. When one side eliminates all the enemies in its current theatre, it will send an expeditionary force to help allies on other theatres. Expeditionary force will build an advance camp in the other theatre and operate from there. If the good forces are completely defeated, but Mordor and Isengard still stand strong, the two towers will battle each other over total dominance.
  '''),

 ("starting_tips",
  "Starting Tips",
  '''
  You choose your faction at the start and you can't change it later. You can also choose from different races: men, elves, dwarves, uruks, uruk-hais or orcs. Remember that both the faction and the race you choose will limit you in certain ways. Some factions provide excellent soldiers, but in small numbers. Some have weak troops, but you can hire many. Smaller orcs can't wear armors designed for big guys, but can ride some beasts instead. Dwarves have exceptional gear, but can't ride mounts.
  
  This is not designed to be fully (artificially) balanced. Playing weaker races or factions can be more challenging (as a first game, you might want to prefer options, in the starting menus, which are placed on top of the list of alternatives).
  
  You choose a faction and you fight for it until your side wins the great war, or until your faction gets wiped out. In that case you can still keep fighting for your allies.
  
  - wandering around aimlessly is not a great idea, the War requires purpose and intent on your part. Before the war starts, you're trying to assemble a party of warriors, get the low requirement companions and some gear to be ready. After the war starts, your strategies may vary. Remember, it's important to both help your allies AND bring down the enemy.
  - doing missions for faction lords is a good way to rise up in rank and to get resource and influence points.
  - take multiple missions/quests at the time, ask everyone! You can often "do the rounds" and have several others done while delivering a letter for instance. Don't waste time!
  '''),

 ("rumours_and_legendary_places",
  "Rumours and Legendary Places",
  '''
  Talking to people in settlements, you can read commentary from their faction's perspective. This will often contain interesting lore and sometimes even information unlocking special Legendary Locations on the world map.
  
  Some of these are only for exploration and don't serve any other purpose, some of them contain unique quests and easter eggs. When you unlock one, you'll be notified by a message.
  '''),

 ("trolls",
  "Trolls",
  '''
  Trolls are very powerful. Evil players can't simply recruit them, but there are other ways of obtaining a troll or two. They do not listen to orders, so keep your troops far away from their devastating attacks!

  If you're looking for trolls as a mission, they can be found roaming around settlements they've been harassing (although friendly parties sometimes drive them further away, or outright deal with them before you do), or they roam the Misty Mountains, mostly nearby to their home caves.
  '''),

("custom_camera",
  "Custom Camera",
  '''
  The Last Days of the Third Age has implemented a Custom Camera in order to bypass the current camera limitation with regards to shorter races (i.e Orcs and Dwarves). It is easy to use, but can take some time to get used to.

  There are 2 modes: Fixed Position and Free-Mode.

  Fixed position is the optimal position for all races, however it cannot be configured.

  Free-Mode Camera puts the character in the middle of the screen. This camera can be adjusted to player preference. When aiming during archery or throwing, it snaps back to default camera for better aiming (which can be quite hard in the beginning, but one can get accustomed to). Once the projectile is used, it goes back to the custom camera.


  Controls:

  Press the Ctrl+End keys together to switch between the three different camera modes: Default Camera / Fixed Camera / Free-Mode Camera.
  
  When in "Free-Mode Camera", Press and hold Ctrl and Page Up (or Page Down) to adjust camera height (Tilt).

  When in "Free-Mode Camera", Press and hold Ctrl and Numpad + (or Numpad -) to adjust camera distance (Zoom).

  Additionally, you can also press Shift while moving/zooming the camera to enable smoothing.


  '''),
]

for indx, page in enumerate(info_pages):
  #swy-- convert the tuple into a modify-able list,
  #      replace the new lines with the caret symbol
  #      strip the blank spaces and put it back in place.
  page = list(page)
  page[2] = "^".join([x.strip() for x in page[2].split("\n")]).strip("^")
  info_pages[indx] = tuple(page)
