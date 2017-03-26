
TLD 3.5 changes:
- Swyter:
 - Added to Steam Workshop
 - Ported TLD to Mac / Linux
 - Fixed animated wavy banners
 - Fixed lone warg fork-bomb
 - Fix ghost-owned wargs respawning again and again
 - Mitigate player teleporting to Mordor on defeat
 - Limit crafting to 0, as the feature is unfinished
 - Comment out music checker thing
 - Update Iron Launcher
 - Workaround viewport popping of ancillary skybox elements in WB
 - Fix Custom Camera keys by masking them behind Ctrl modifier
 - Added a brand new signed distance font bitmap
 - Fix party troop number in overall map
 - Added high-res signed distance font
 - Spirit Shader

- Merlkir:
 - Added female frame to Woodsmen, Beorning, Khand, and Rhun Armours
 - Dialogues for Starting Quests
 - Dialogues for Ring Hunters
 - Added Lumberjack Orcs drawing overlay
 - Added Kneel at Mound drawing overlay
 - Added Ring Hunter Quest drawings
 - Added Dale Victory Drawings
 - Add more troll sounds
 - Design Black Shield, Black Shield's Men, Vengeful Spirit troops for Spears quest
 - Concept art for Shield Bear Shield & Club
 - Add Lorien Victory drawing overlay

- Kham:
 - Implement Troop Tree Viewer under Reports
 - Implement Custom Camera to improve Orc/Dwarf gameplay
 - Added validator to CppCoder's Morale Code to fix a script error
 - Hooked up Dwarven Fortress for Spears quest
 - Added Viking Conquest Module.ini changes to WB module.ini
 - Added Ring Hunters Quest
 - Added More Town Walkers to certain towns
 - Make Elves slightly taller using scale
 - Fix to Siege Doors so that they are properly attacked by troops
 - Added Faction Starting Quests to tutorialize resource points & influence, and overall add immersion.
 - Added Defend / Raid Village Pre-War quests
 - Added Destroy Scout Camp War quest
 - Improve Thrust Speed of Spears (VC)
 - Added restrictions to Orc Mutiny
 - Bumped up the number of parties
 - Prepare Mission Templates and Menus for Spears quest completion
 - Added XP for discovering town NPCs
 - Added town mission message about rumours
 - Added battle mission message about formations
 - Added Shield Bear troop for Beornings
 - Added fix to siege mission templates to prevent archers from stalling on ladders (In Vain's suggestion)
 - Gondor Reinforcement Event scripts and triggers
 - Refactor Oath Of Vengeance to Troop Kills instead of Party Kills
 - Eliminate Patrol Quest gets cancelled when target faction is defeated
 - Fixes to Formations
 - Eliminate Patrols Refactor
 - Player Initiated Siege

- In Vain:
 - Multiple Siege Scene fixes
 - New Dale / Esgaroth Scenes (WB only)
 - Scout Camp Scenes (Good, Evil, North, Mirkwood + Large / Small versions of each)
 - Multiple Scene fixes
 - Black Shield Fortress for the Spears quest
 - Added new Dale map icon
 - Added CWE Flora for Scening
 - Added temporary siege scenes for future use

- Yarrum
 - Spears Quest - Black Shield Menu Descriptions
 - Lore consultation & descriptions
 - Rohan reward helm
 - Dialogue fixes

- Mandible
 - 3D models of Shield Bear Shield, Shield Bear Club

- Multiple Translations
 - Chinese Simplified
 - German
 - Italian
 - Russian
 - Spanish
 - French
 - Turkish
 - Japanese
 - Polish
 - and many more!



TLD 3.3.1 changes:
- Swyter:
 - Reimplement the death camera in Warband using MadVader's code as reference.
 - Make the Nazgûl, alarm levels and thunder sounds audible in Warband.
 - Added LODs to the reward swords and a better scabbard version of another one.
 - Fix undefined path material under the character creation terrain mesh in Warband, looked like blonde hair.
 - Fix invisible mesh of the "Sword of The Great Serpent" reward item in Warband.
 - Added a subtle hint of scrolling clouds projecting shadows in the overall map, done with shaders, only for Warband.
 - Enhanced waterfall, lava and fountain shaders, including transparency.
 - Wavy shaders for both Meduseld and per-faction banners, made from scratch.
 - Revised siege scenes and AI meshes, mainly from Osgiliath, Helm's Deep and Minas Morgul.
 - Updated overall map with passable fords and some optimizations.
 - Reimplemented the lone wargs mechanics in Warband, making riderless wargs aggressive.
 - Added scrollbars back to Warband.
 - Fixed ramp meshes in Erech and Calembel, in Warband.
 - Fixed crash when encountering wargs and warg mounted troops, caused by LODs, in Warband.
 - Add code guards to prevent possible player teleporting in the overall map.
 - Training in barracks will spawn the player with (correct) weapons, in Warband.
 - Hide the HP overlay during cutscenes using shader and uniform black magic, in Warband.
 - Make the cutscene overlay persist after coming back from the Esc menu, in Warband.
 - Make spears couchable in Warband.
 - Special items like troll clubs can no longer be picked up in the battlefield.
 - Now uruks and other races are sized correctly in Warband.
 - Upgrading troops in Warband is free and doesn't cost local resources, keeping with the original mechanic in M&B 1.011.
 - Fixed the blue underwater fog in Edoras and other places, caused by the fountain in Warband.
 - Fixed the shading glitches in Meduseld's floor.
 - Workaround Warband bug when populating smiths inventories which caused incorrect items like tools and other faction's weapons to be added by mistake.
 - Gandalf no longer appears bald or as a cute redhead, in Warband.
 - Fixed wobbly map trees in Mirkwood, in Warband.
 - Add entry points for enemies in the Rhûn Main Camp siege scene.
 - Fixed unwanted transparency of body parts when LODs are triggered.
 - Add "Accompany" option to the right-click party menu for allies, in Warband.
 - Fix some remaining inaccessible lords, like Burza in Gundabad.
 - Make use of Warband's muddy water in some scenes like Dead Marshes or Minas Morgul.
 - Fix ragdoll animations of troll victims.
 - Complete French translation of the entire mod by ALG and his team from MundusBellicus.fr.
 - Additional corrections and additions to other languages in Transifex.
 - New LODs for trolls.
 
- Merlkir:
 - Ten new illustrations by Merlkir, plus some that weren't added before, mainly for encounters and victory.
     - Rivendell victory
     - Mirkwood victory
     - Black numeroneans victory
     - Rhûn victory
     - Dunland victory
     - Khand victory
     - Bear attack
     - Wolf attack
     - Mountain goblins attack
     - Corsair renegades attack
     - Good vs Evil reused as Quick Battles background 
     - Troll attack also used in quest menus
 - Written a brand new series of gameplay-related info pages from scratch.
 - New good/evil sounds for rank promotion, by Merlkir.
 - Better hit sounds for Trolls, by Merlkir.

- CppCoder:
 - Fix the "terrible" moral problem for the player's party.
 
- mtarini
 - Better skeleton rigging for bears.


TLD 3.3 changes:
- Swyter:
  - Port to Warband.
  - New, easier and less obtrusive install method for 1.011. (Rewritten Iron Launcher into a proxy DLL with IAT hooks)
  - Optimize flying missiles to avoid fillrate issues on sieges.
  - Optimize animal meshes, better rigging for wolves, moving ears, added LODs and AO.
  - Optimize a good part of the Mordor weapon meshes, added manual LODs.
  - Add per-vertex ambient occlusion to Mirkwood helmets and shields, some Lothlorien props too.
  - Tidy up internal scripts, simplifying logic and cleaning them up.
  - Redone Iron Hills Quarry and West Emmet AI meshes so that NPCs don't get stuck.
  - Add lightweight capsule collisions to Dwarven statues, like the one amid the Iron Hills Quarry.
  - Add a new localization back-end on Transifex (Transifex.com).
  - Add finished and reviewed es_ES translation by HoJu and Swyter.
  - Add purchasable ponies to the Iron Hills Quarry merchant.
  - Manually fix border seams (visible as striped patterns on the ground) of some tiling terrain normal maps.
  - Re-encode the Bink intro video using the older audio codec so it can be played with the stock binkplay.exe instead of bundling it.
    
  - WB: Added flowmap shader to rivers and sea, adds directionality to water surfaces.
  - WB: Make sitting lords accessible for talk on their throne rooms. (Denethor, Thranduil, Theoden, Saruman, Gothmog, M. of Sauron)
  - WB: Fix l(e)adders not appearing in sieges, Taleworlds typo.
  - WB: Redo the loading, main, and escape menus to make them look like their 1.011 counterparts.
  - WB: Turn the module system into something dual, multi-target.
  - WB: Port mtarini shaders to Warband (windy flora/red eyes/skeleton hackery/...).
  - WB: Fix broken marshes shader in the overall map when HDR is enabled.
  - WB: Fix non-manifold collision meshes which caused Warband to crash on loading.
  - WB: Decompiled and rebuild the flora_kinds.txt for Warband, fixed some broken flags too (caused crashes on some scenes).
  - WB: Complete the rewritten animations file (module_animations_wb.py) started by GetAssista. Adds Warband animations to TLD.
  - WB: Fix gansta bows for evil races using the gun animation.
  - WB: Fix scene entry point item overriding, fixing Galadriel, Merry, Pippin and other special agents with transparent parts.
  - WB: Fix in-battle command overlay toggling. Now it can be closed.
  - WB: Fix exit of cutscenes instead of repeating in an endless loop.
  - WB: Fix division by zero when entering West Emmet castle menu.
  - WB: Fix ragdolls (skeleton_bodies.xml) with buggy possessed wobbly legs.
  - WB: Fix troop, center and faction notes not appearing in the interface.
  - WB: Add HDR shader, materials and textures to TLD skyboxes.
  - WB: Changed the lame horse mechanic to trigger randomly only when the horse starts trotting. (Fairer)


TLD 3.23 changes:
- CppCoder:
  - Animal Ambushes become less likely the more attacks you've experienced.
  - Morale System Tweaks (should make it more enjoyable and playable)
  - Guldur and Mordor resource sharing bug fixed. (hopefully :P )
  - Spiders are less powerful (5-10 damage, was 10-20)
  - Mordor legions more powerful and balanced.
  - Quest for dead lords are ended.
  - Minor tweaks.

TLD 3.2 changes:
- CppCoder:
  - Elven Hero Parties are 3/4 of normal size. 
  - Rhun Hero Parties are now 4/3 of normal size.
  - Kingdom Heroes now need at least 50 troops to besiege. (should fix infinite siege bug).
  - Resource Point Cap (200,000).
  - Gift Giving through faction leaders. (Exchange Resource Points).
  - Berserker Troops no longer flee from battle.
  - Command Cursor Mini Mod.
  - Galadriel's Quest (Mirkwood Sorcerer. lvl 10+).
  - Animal Ambushes (Mirkwood or Northern Mountains).
  - Mordor Legions (when mordor is last faction standing with less than 2500 strength).
  - Isengard and Mirkwood guardian parties should spawn now.
  - Influence traits give/take influence (for player's faction only).
  - Party Limit Option in camp->TLD options->Gameplay Tweaks->Compatibility tweaks.
  - Starting equipment bug fixed.
  - Battle Morale System.
  - Battle Morale System: After Battle summary now reports routed troops.
  - Battle Morale System: Tweaking of morale values. (still WIP).
  - Riders falling off horses recieve damage.
  - Wounded agents move slower.
  - Trolls no longer appear as prisoners in review troops.
  - Trolls no longer speak in party/prisoner dialog.
  - Oathbreaker/keeper quest fixed.
  - Fangorn and Capture Troll quest have text now.
  - Mearh Stallion no longer roars like a warg.
  - Nazgul Sweeps ingame. (Attack a mordor war party to see them).
  - Injury Summary in Character Reports.
  - Companions tell you their exact injuries.
  - Companions lost due to lack of RPs can rejoin you again.
  - Many other small bug fixes.
  - More bugfixing.
- Merlkir:
  - Graphic tweak(s).
- Mandible:
 - Beorning armors redone.
- vota dc:
  - More item/troop balancing. (I think?)

TLD 3.15 changes:
- Octoburn: added unused dwarven helmets to Dale
- Strategy tweaks (a submenu under Actions->TLD mod options)
  - Siege strength requirements: Normal/Defender only/None
  - Siege str. req. relaxation rate: 50/100(default)/200
  - Strength regen rate: Normal/Halved/Battles only/None
  - Factions don't regen below: 500(default)/1000/1500/2000
- Influence rebalanced (made easier)
  - Companions cost halved again (Glorfindel is 50 now)
  - 25% more influence from rank point gain (was: rank points/10, now: rank points/8)
  - Changed formula for rank points gained in allied battles, now based on Native renown, as in single battles. Additional points from allies.
- Campaign AI
  - Removed a restriction that prevented weak factions to go patrolling; fixed an old bug that made patrols much less likely
  - Less canceled campaigns if there's any reason to patrol for enemies; especially if the player is following the marshall and has a quest
  - Max faction strength is now 8000 (from 9999) - less grind
  - Slightly more lords spawn with full armies when strength is low
  - Last-stand parties only for Mirkwood and Isengard
  - Strong factions spawn less patrols


TLD 3.14 changes:
- Vota: MANY troops and items rebalanced
- CppCoder: bugfixes
- MV: Defense strength for siege requirements relaxes with player level (opens up the game)


3.11-3.13 Unknown changes :)


TLD 3.1 changes

Major updates:
- Massive music update
- Strategy:
  -- More aggresive AI in campaigns and sieges; riskier attacks against very weak factions
  -- Highly-ranked players can suggest siege targets to marshalls
  -- Last-stand guardian parties spawn when a faction is almost crushed (allowing to defeat it by defeating the guardian party)

Minor updates:
- New battle scenes and landmarks
- Hit-boxes revamp
- Evil companion dialogs (Bolzog by Amman, the rest by Taal - thanks guys!)
- Companions cost influence
- Rhun and Gundabad parties made tougher, less camps are immediately siegable
- Factions stop regenerating strength when brought down under 500
- Marshalls will engage in defensive patrols against enemy patrols, not just lords
- New sounds: quest events, lord deaths, rank promotion
- Captured dwarves in chains
- Gondor Lords hire more of their native (fiefdom-specific) troops
- Meshes optimizations (redundant vertices), especially LODs

Fixes:
- Party members exchange problems fixed?
- Lost companions can be always rehired
- Corrupt save problem delayed by spawning less parties less frequently
- Several sticky map places fixed (including Aldburg) 
- Parties getting stuck in rivers get unstuck every few days (doesn't solve all map problems)
- Empty parties get removed every few days
- Empty volunteer parties removed from destroyed towns
- Plenty of other stuff

3.01 Changelog (most important issues):
- Elves nerfed somewhat, -40 weapon proficiencies across the board, fewer volunteers, a bit slower training
- Gunda and Rhun buffed somewhat, to not suck on dwarves and Dale too fast
- Marshalls made more persistent in campains. How it plays out actually is for you to test
- Dwarves got LODs, will be less demanding to video
- Fixed MANY bugs, see forum 1st post in bugreport thread

Regards,
TLD team

