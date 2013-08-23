import string
import types

from module_info import *
from module_tableau_materials import *

from process_common import *
from process_operations import *

def save_tableau_materials(variable_list,variable_uses,tag_uses,quick_strings):
  ofile = open(export_dir + "tableau_materials.txt","w")
  ofile.write("%d\n"%(len(tableaus)))
  for tableau in tableaus:
    ofile.write("tab_%s %d %s %d %d %d %d %d %d"%(tableau[0], tableau[1], tableau[2], tableau[3], tableau[4], tableau[5], tableau[6], tableau[7], tableau[8]))
    save_statement_block(ofile, 0, 1, tableau[9], variable_list, variable_uses, tag_uses, quick_strings)
    ofile.write("\n")
  ofile.close()

def save_python_header():
  ofile = open("./ID_tableau_materials.py","w")
  for i_tableau in xrange(len(tableaus)):
    ofile.write("tableau_%s = %d\n"%(tableaus[i_tableau][0],i_tableau))
  ofile.close()

print "Exporting tableau materials data..."
save_python_header()
variable_uses = []
variables = load_variables(export_dir, variable_uses)
tag_uses = load_tag_uses(export_dir)
quick_strings = load_quick_strings(export_dir)
save_tableau_materials(variables,variable_uses,tag_uses,quick_strings)
save_variables(export_dir,variables,variable_uses)
save_tag_uses(export_dir, tag_uses)
save_quick_strings(export_dir,quick_strings)
