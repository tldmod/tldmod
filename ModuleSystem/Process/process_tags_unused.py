from module_info import *
from process_common import *
from process_operations import *


print "Checking tag usages..."
tag_uses = load_tag_uses(export_dir)

#Processing strings
length = 0
for i in xrange(len(tag_uses[tag_string])):
  if tag_uses[tag_string][i] > 0:
    length = i
    
for i in xrange(length):
  if tag_uses[tag_string][i] == 0:
    if i > 3:
      print "WARNING: String is never used: " + strings[i][0].lower()

#Processing items
length = 0
for i in xrange(len(tag_uses[tag_item])):
  if tag_uses[tag_item][i] > 0:
    length = i
    
for i in xrange(length):
  if tag_uses[tag_item][i] == 0 and i > 1:
    print "WARNING: Item is never used: " + items[i][0].lower()

#Processing troops
length = 0
for i in xrange(len(tag_uses[tag_troop])):
  if tag_uses[tag_troop][i] > 0:
    length = i
    
for i in xrange(length):
  if tag_uses[tag_troop][i] == 0:
    if i > 3:
      print "WARNING: Troop is never used: " + troops[i][0].lower()

#Processing factions
length = 0
for i in xrange(len(tag_uses[tag_faction])):
  if tag_uses[tag_faction][i] > 0:
    length = i
    
for i in xrange(length):
  if tag_uses[tag_faction][i] == 0:
    print "WARNING: Faction is never used: " + factions[i][0].lower()

#Processing quests
length = 0
for i in xrange(len(tag_uses[tag_quest])):
  if tag_uses[tag_quest][i] > 0:
    length = i
    
for i in xrange(length):
  if tag_uses[tag_quest][i] == 0:
    print "WARNING: Quest is never used: " + quests[i][0].lower()

#Processing party_templates
length = 0
for i in xrange(len(tag_uses[tag_party_tpl])):
  if tag_uses[tag_party_tpl][i] > 0:
    length = i
    
for i in xrange(length):
  if tag_uses[tag_party_tpl][i] == 0:
    if i > 3:
      print "WARNING: Party template is never used: " + party_templates[i][0].lower()

#Processing parties
length = 0
for i in xrange(len(tag_uses[tag_party])):
  if tag_uses[tag_party][i] > 0:
    length = i
    
for i in xrange(length):
  if tag_uses[tag_party][i] == 0:
    if parties[i][0].lower().find("temp_") == -1:
      print "WARNING: Party is never used: " + parties[i][0].lower()

#Processing scenes
#length = 0
#for i in xrange(1024):
#  if tag_uses[tag_scene][i] > 0:
#    length = i
#    
#for i in xrange(length):
#  if tag_uses[tag_scene][i] == 0:
#    print "WARNING: Scene is never used: " + scenes[i][0].lower()

#Processing mission_templates
length = 0
for i in xrange(len(tag_uses[tag_mission_tpl])):
  if tag_uses[tag_mission_tpl][i] > 0:
    length = i
    
for i in xrange(length):
  if tag_uses[tag_mission_tpl][i] == 0:
    print "WARNING: Mission template is never used: " + mission_templates[i][0].lower()

#Processing game_menus
length = 0
for i in xrange(len(tag_uses[tag_menu])):
  if tag_uses[tag_menu][i] > 0:
    length = i
    
for i in xrange(length):
  if tag_uses[tag_menu][i] == 0 and i > 0:
    if i > 1:
      print "WARNING: Game menu is never used: " + game_menus[i][0].lower()

#Processing scripts
length = 0
for i in xrange(len(tag_uses[tag_script])):
  if tag_uses[tag_script][i] > 0:
    length = i
    
for i in xrange(length):
  if tag_uses[tag_script][i] == 0:
    if scripts[i][0].lower().find("game_") == -1:
      print "WARNING: Script is never used: " + scripts[i][0].lower()

#Processing particle systems
length = 0
for i in xrange(len(tag_uses[tag_particle_sys])):
  if tag_uses[tag_particle_sys][i] > 0:
    length = i
    
for i in xrange(length):
  if tag_uses[tag_particle_sys][i] == 0:
    if particle_systems[i][0].lower().find("game_") == -1:
      print "WARNING: Particle system is never used: " + particle_systems[i][0].lower()

#Processing scene props
#length = 0
#for i in xrange(1024):
#  if tag_uses[tag_scene_prop][i] > 0:
#    length = i
#    
#for i in xrange(length):
#  if tag_uses[tag_scene_prop][i] == 0:
#    print "WARNING: Scene prop is never used: " + scene_props[i][0].lower()

#Processing sounds
#length = 0
#for i in xrange(1024):
#  if tag_uses[tag_sound][i] > 0:
#    length = i
#    
#for i in xrange(length):
#  if tag_uses[tag_sound][i] == 0:
#    print "WARNING: Sound is never used: " + sounds[i][0].lower()

#Processing map icons
#length = 0
#for i in xrange(1024):
#  if tag_uses[tag_map_icon][i] > 0:
#    length = i
#    
#for i in xrange(length):
#  if tag_uses[tag_map_icon][i] == 0:
#    print "WARNING: Map icon is never used: " + map_icons[i][0].lower()
