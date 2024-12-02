from header_common import *	
from header_skills import *

####################################################################################################################
#  Each skill contains the following fields:
#  1) Skill id (string): used for referencing skills in other files. The prefix skl_ is automatically added before each skill-id .
#  2) Skill name (string).
#  3) Skill flags (int). See header_skills.py for a list of available flags
#  4) Maximum level of the skill (int).
#  5) Skill description (string): used in character window for explaining the skills.
# 
####################################################################################################################

#Hardcoded skills are {names (indexes, beginning with 0)}:
# Trade (1)
# Leadership (2)
# Prisoner Management (3)
# First Aid (9)
# Surgery (10)
# Wound Treatment (11)
# Inventory Management (12)
# Spotting (13)
# Pathfinding (14)
# Tactics (15)
# Tracking (16)
# Trainer (17)
# Engineer (18)
# Horse Archery (24)
# Riding (25)
# Athletics (26)
# Shield (27)
# Weapon Master (28)
# Power Draw (34)
# Power Throw (35)
# Power Strike (36)
# Ironflesh (37)
#
# The effects of these skills can only be removed if the skill is disabled with sf_inactive flag.
# If you want to add a new skill, use the reserved skills or use non-hardcoded skills.

skills = [
  ("trade","Bargainer",sf_base_att_int|sf_effects_party,10,"Makes smiths and supply masters more cooperative and offer better equipment. (Party skill)"),
  ("leadership","Leadership",sf_base_att_cha,10,"Every point increases maximum number of troops you can command by 5 (3 for companions), increases your party morale and coherence in battle. Makes more and stronger volunteers willing to follow you. (Personal skill)"),
  ("prisoner_management", "Prisoner Management",sf_base_att_cha|sf_effects_party,10,"Every level of this skill increases maximum number of prisoners by %d. Improves chances of capturing and keeping prisoners .(Party skill)"), 
  ("reserved_1","{!}Reserved Skill 1",sf_base_att_cha|sf_inactive,10,"{!}This is a reserved skill."), 
  ("reserved_2","{!}Reserved Skill 2",sf_base_att_cha|sf_inactive,10,"{!}This is a reserved skill."), 
  ("reserved_3","{!}Reserved Skill 3",sf_base_att_cha|sf_inactive,10,"{!}This is a reserved skill."), 
  ("reserved_4","{!}Reserved Skill 4",sf_base_att_cha|sf_inactive,10,"{!}This is a reserved skill."), 
  ("persuasion","Wildcraft", sf_base_att_int|sf_effects_party,10, "The ability to survive in the wilderness and bend it to your will. This skill affects the party's ability to hide from the enemy, and the party's speed while in wooded terrain. (Party skill)"),
  ("engineer","-----",sf_base_att_int|sf_effects_party,0,"-----"),
  ("first_aid", "First Aid",sf_base_att_int|sf_effects_party,10,"Heroes regain 5%% per skill level of hit-points lost during mission. (Party skill)"), 
  ("surgery","Surgery",sf_base_att_int|sf_effects_party,10,"Each point to this skill gives a 4%% chance that a mortally struck party member will be wounded rather than killed. (Party skill)"), 
  ("wound_treatment","Wound Treatment",sf_base_att_int|sf_effects_party,10,"Party healing speed is increased by 20%% per level of this skill. (Party skill)"), 
  ("inventory_management","Inventory Management",sf_base_att_int,10,"Increases inventory capacity by +6 per skill level. Reduces food consumption. (Leader skill)"), 
  ("spotting","Spotting",sf_base_att_int|sf_effects_party,10,"Party seeing range is increased by 10%% per skill level. (Party skill)"),
  ("pathfinding","Path-finding",sf_base_att_int|sf_effects_party,10,"Party map speed is increased by 3%% per skill level. (Party skill)"), 
  ("tactics","Tactics",sf_base_att_int,10,"Improves battle advantage. Increases battle join distance for enemy parties and decreases battle join distance for friendly parties by 3%% per level. (Leader skill)"),
  ("tracking","Tracking",sf_base_att_int|sf_effects_party,10,"Tracks become more informative. (Party skill)"),
  ("trainer","Trainer",sf_base_att_cha,10,"Every day, each hero with this skill adds some experience to every other member of the party whose level is lower than his/hers. Experience gained goes as: {0,4,10,16,23,30,38,46,55,65,80}. (Personal skill)"),
  ("reserved_5","{!}Reserved Skill 5",sf_base_att_int|sf_inactive,10,"{!}This is a reserved skill."), 
  ("reserved_6","{!}Reserved Skill 6",sf_base_att_int|sf_inactive,10,"{!}This is a reserved skill."), 
  ("reserved_7","{!}Reserved Skill 7",sf_base_att_int|sf_inactive,10,"{!}This is a reserved skill."), 
  ("reserved_8","{!}Reserved Skill 8",sf_base_att_int|sf_inactive,10,"{!}This is a reserved skill."), 
  ("looting","Looting",sf_base_att_agi|sf_effects_party,10,"Increases amount and quality of loot gained after battles. (Party skill)"), 
  ("horse_archery","Mounted Archery",sf_base_att_agi,10,"Reduces damage and accuracy penalties for archery and throwing when mounted. (Personal skill)"),
  ("riding","Riding",sf_base_att_agi,10,"enables you to ride horses (or other beasts) of higher difficulty levels and increases your riding speed and manuever. (Personal skill)"),
  ("athletics","Athletics",sf_base_att_agi,10,"improves your running speed. (Personal skill)"),
  ("shield","Shield",sf_base_att_agi,10,"reduces damage to shields (by 8%% per skill level), improves shield speed and coverage, reduces shield penalty when used with bows. (Personal skill)"),
  ("weapon_master","Weapon Master",sf_base_att_agi,10,"makes it easier to learn weapon proficiencies and increases the proficiency limits. Limits go as: 60, 100, 140, 180, 220, 260, 300, 340, 380, 420. (Personal skill)"),
  ("reserved_9","{!}Reserved Skill 9",sf_base_att_agi|sf_inactive,10,"{!}This is a reserved skill."), 
  ("reserved_10","{!}Reserved Skill 10",sf_base_att_agi|sf_inactive,10,"{!}This is a reserved skill."), 
  ("reserved_11","{!}Reserved Skill 11",sf_base_att_agi|sf_inactive,10,"{!}This is a reserved skill."), 
  ("reserved_12","{!}Reserved Skill 12",sf_base_att_agi|sf_inactive,10,"{!}This is a reserved skill."), 
  ("reserved_13","{!}Reserved Skill 13",sf_base_att_agi|sf_inactive,10,"{!}This is a reserved skill."), 
  ("power_draw","Power Draw",sf_base_att_str,10,"lets character use more powerful bows. Each point to this skill (up to four plus power-draw requirement of the bow) increases bow damage by 14%%. (Personal skill)"),
  ("power_throw","Power Throw",sf_base_att_str,10,"Each point to this skill increases throwing damage by 10%%. (Personal skill)"),
  ("power_strike","Power Strike",sf_base_att_str,10,"Each point to this skill increases melee damage by 8%%. (Personal skill)"),
  ("ironflesh","Ironflesh",sf_base_att_str,10,"Each point to this skill increases hit points by +2, and lets you shrug off some damage without being wounded. (Personal skill)"), 
  ("reserved_14","{!}Reserved Skill 14",sf_base_att_str|sf_inactive,10,"{!}This is a reserved skill."), 
  ("reserved_15","{!}Reserved Skill 15",sf_base_att_str|sf_inactive,10,"{!}This is a reserved skill."), 
  ("reserved_16","{!}Reserved Skill 16",sf_base_att_str|sf_inactive,10,"{!}This is a reserved skill."), 
  ("reserved_17","{!}Reserved Skill 17",sf_base_att_str|sf_inactive,10,"{!}This is a reserved skill."), 
  ("reserved_18","{!}Reserved Skill 18",sf_base_att_str|sf_inactive,10,"{!}This is a reserved skill."), 
]
