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
  ofile = open(export_dir + "skills.txt","w")
  ofile.write("%d\n"%(len(skills)))
  for i_skill in xrange(len(skills)):
    skill = skills[i_skill]
    ofile.write("skl_%s %s "%(skill[0], replace_spaces(skill[1])))
    ofile.write("%d %d %s\n"%(skill[skill_attribute_pos],skill[skill_max_level_pos],(string.replace(skill[skill_desc_pos]," ","_"))))
  ofile.close()

def save_python_header():
  ofile = open("./ID_skills.py","w")
  for i_skill in xrange(len(skills)):
    ofile.write("skl_%s = %d\n"%(skills[i_skill][0],i_skill))
  ofile.write("\n\n")
  ofile.close()

print "Exporting skills..."
save_python_header()
save_skills()
