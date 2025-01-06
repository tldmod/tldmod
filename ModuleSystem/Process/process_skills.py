import string
from header_common import *
from module_info import *
from module_skills import *
from process_common import *

skill_name_pos = 1
skill_attribute_pos = 2
skill_max_level_pos= 3
skill_desc_pos = 4



def save_skills():
  ofile = open(export_dir + "skills.txt","w", encoding='utf-8')
  ofile.write("%d\n"%(len(skills)))
  for i_skill in range(len(skills)):
    skill = skills[i_skill]
    ofile.write("skl_%s %s "%(skill[0], remove_exclamation_marker_on_mb1011(replace_spaces(skill[1]))))
    ofile.write("%d %d %s\n"%(skill[skill_attribute_pos],skill[skill_max_level_pos],remove_exclamation_marker_on_mb1011(replace_spaces(skill[skill_desc_pos]))))
  ofile.close()

def save_python_header():
  ofile = open("./ID/ID_skills.py","w", encoding='utf-8')
  for i_skill in range(len(skills)):
    ofile.write("skl_%s = %d\n"%(skills[i_skill][0],i_skill))
  ofile.write("\n\n")
  ofile.close()

print("Exporting skills...")
save_python_header()
save_skills()
