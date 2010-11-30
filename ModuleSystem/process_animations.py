import string
from header_common import *
from module_info import *
from module_animations import *
from process_common import *

def compile_action_sets(actions):
  action_codes = []
  for action in actions:
    index = -1
    for i_action_code in xrange(len(action_codes)):
      if action_codes[i_action_code] == action[0]:
        index = i_action_code
        break
    if index == -1:
      pos = len(action_codes)
      action_codes.append(action[0])
      action[0] = pos
    else:
      action[0] = index
  return action_codes

def write_actions(action_set,num_action_codes,action_codes,file_name):
  file = open(export_dir + file_name,"w")
  file.write("%d\n"%num_action_codes)
  for i_action_code in xrange(num_action_codes):
    action_found = 0
    for action in action_set:
      if action[0] == i_action_code:
        file.write(" %s %d "%(action_codes[i_action_code],action[1])) #print flags
        file.write(" %d\n"%(len(action)-2))
        for elem in action[2:]:
          file.write("  %f %s %d %d %d "%(elem[0],elem[1],elem[2],elem[3],elem[4]))
          if (len(elem) > 5):
            file.write("%d "%elem[5])
          else:
            file.write("0 ")
          if (len(elem) > 6):
            file.write("%f %f %f  "%elem[6])
          else:
            file.write("0.0 0.0 0.0 ")
          if (len(elem) > 7):
            file.write("%f \n"%(elem[7]))
          else:
            file.write("0.0 \n")
        action_found = 1
        break
    if not action_found:
      file.write(" none 0 0\n") #oops

def save_python_header(action_codes):
  ofile = open("./ID_animations.py","w")
  for i_anim in xrange(len(action_codes)):
    ofile.write("anim_%s = %d\n"%(action_codes[i_anim],i_anim))
  ofile.write("\n\n")
  ofile.close()

print "Exporting animations..."
action_codes = compile_action_sets(animations)
save_python_header(action_codes)
write_actions(animations,len(action_codes),action_codes,"actions.txt")
