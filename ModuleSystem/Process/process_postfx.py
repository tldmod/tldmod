from header_common import *
from process_common import *
from module_info import *
from module_postfx import *

def write_python_header(postfx_params_list):
  file = open("./ID/ID_postfx_params.py","w", encoding='utf-8')
  for i_postfx_param in range(len(postfx_params_list)):
    file.write("pfx_%s = %d\n"%(postfx_params_list[i_postfx_param][0],i_postfx_param))
  file.write("\n\n")
  file.close()

def write_postfx_params(postfx_params_list):
  ofile = open(export_dir + "postfx.txt","w", encoding='utf-8')
  ofile.write("postfx_paramsfile version 1\n")
  ofile.write("%d\n"%len(postfx_params_list))
  for postfx_param in postfx_params_list:
    ofile.write("pfx_%s %d %d"%(postfx_param[0], postfx_param[1],postfx_param[2]))
    params_list1 = postfx_param[3]
    params_list2 = postfx_param[4]
    params_list3 = postfx_param[5]
    ofile.write("  %s %s %s %s"%(sf(params_list1[0]), sf(params_list1[1]), sf(params_list1[2]), sf(params_list1[3])))
    ofile.write("  %s %s %s %s"%(sf(params_list2[0]), sf(params_list2[1]), sf(params_list2[2]), sf(params_list2[3])))
    ofile.write("  %s %s %s %s\n"%(sf(params_list3[0]), sf(params_list3[1]), sf(params_list3[2]), sf(params_list3[3])))
  ofile.close()

if (wb_compile_switch):
  print("Exporting postfx_params for Warband...")
  write_postfx_params(postfx_params)
  write_python_header(postfx_params)
