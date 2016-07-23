import string
from header_common import *
from module_info import *
from module_meshes import *

from process_common import *

def save_meshes():
  ofile = open(export_dir + "meshes.txt","w")
  ofile.write("%d\n"%len(meshes))
  for i_mesh in xrange(len(meshes)):
    mesh = meshes[i_mesh]
    ofile.write("mesh_%s %d %s %s %s %s %s %s %s %s %s %s\n"%(mesh[0],mesh[1],replace_spaces(mesh[2]),sf(mesh[3]),sf(mesh[4]),sf(mesh[5]),sf(mesh[6]),sf(mesh[7]),sf(mesh[8]),sf(mesh[9]),sf(mesh[10]),sf(mesh[11])))
  ofile.close()

def save_python_header():
  if (wb_compile_switch):
    ofile = open("./ID/ID_meshes_wb.py","w")
  else:
    ofile = open("./ID/ID_meshes_mb.py","w")
  for i_mesh in xrange(len(meshes)):
    ofile.write("mesh_%s = %d\n"%(meshes[i_mesh][0],i_mesh))
  ofile.write("\n\n")
  ofile.close()

print "Exporting meshes..."
save_python_header()
save_meshes()
