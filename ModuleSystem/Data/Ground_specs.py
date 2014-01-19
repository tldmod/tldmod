from module_info import *

gtf_overlay = 0x00000001 #deprecated
gtf_dusty   = 0x00000002 #controls dustiness of the ground for foot dust particle systems 
gtf_has_color  = 0x00000004 #you can overwrite the ambient color of the ground spec (default: 0.61, 0.72, 0.15)

#IMPORTANT NOTE: Ground_specs have dependency on mnodule system and the engine c++ code!
#                You cannot add new ground types as they are hardcoded in the engine code.
#                Make sure you have updated your module's header_ground_types.py file 

#arguments:
#spec_name, flags, material, uv_scale, multitex_material_name, gtf_has_color->color
ground_specs = [
    ("gray_stone",gtf_has_color,"stone_a",4.0,"none",(0.7,0.7,0.7)),
    ("brown_stone",gtf_has_color,"patch_rock",2,"none",(0.7,0.7,0.7)),
    ("turf",gtf_overlay|gtf_has_color,"grassy_ground",3.3,"ground_earth_under_grass",(0.42,0.59,0.17)),
    ("steppe",gtf_overlay|gtf_dusty|gtf_has_color,"ground_steppe",3.0,"ground_earth_under_steppe",(0.85,0.73,0.36)),
    ("snow",gtf_overlay|gtf_has_color,"snow",5.2,"none",(1.4,1.4,1.4)),
    ("earth",gtf_overlay|gtf_dusty|gtf_has_color,"ground_earth",4.5,"none",(0.7,0.5,0.23)),
    ("desert",gtf_overlay|gtf_dusty|gtf_has_color,"ground_desert", 2.5,"none",(1.4,1.2,0.4)),
    ("forest",gtf_overlay|gtf_has_color,"ground_forest",4.2,"ground_forest_under_grass",(0.6,0.42,0.28)),
    ("pebbles",gtf_overlay|gtf_has_color,"pebbles",4.1,"none",(0.7,0.7,0.7)),
    ("village",gtf_overlay|gtf_has_color,"ground_village",7.0,"none",(1.0,0.9,0.59)),
    ("path",gtf_overlay|gtf_dusty|gtf_has_color,"ground_path",6.0,"none",(0.93,0.68,0.34)),
]

def write_vec(file,vec):
  file.write(" %f %f %f "%vec)
  
def save_ground_specs():
  file = open("../"+export_dir+"/data/ground_specs.txt","w")
  for ground_spec in ground_specs:
    file.write(" %s %d %s %f %s"%(ground_spec[0],ground_spec[1],ground_spec[2],ground_spec[3],ground_spec[4]))
    if (ground_spec[1] & gtf_has_color):
      file.write(" %f %f %f"%ground_spec[5])
    file.write("\n")
  file.close()

def save_c_header():
  file = open("./ground_spec_codes.h","w")
  file.write("#ifndef _GROUND_SPEC_CODES_H\n")
  file.write("#define _GROUND_SPEC_CODES_H\n\n")
  file.write("typedef enum {\n")
  for ground_spec in ground_specs:
    file.write("  ground_%s,\n"%ground_spec[0])
  file.write("}Ground_spec_codes;\n")
  file.write("const int num_ground_specs = %d;\n"%(len(ground_specs)))
  file.write("\n\n")
  file.write("\n#endif\n")
  file.close()
  
def save_python_header():
  file = open("../header/header_ground_types.py","w")
  for ig in xrange(len(ground_specs)):
    ground_spec = ground_specs[ig]
    file.write("ground_%s = %d\n"%(ground_spec[0], ig))
  file.write("\n\n")
  file.close()

print "Exporting ground_spec data..."
save_ground_specs()
save_c_header()
save_python_header()
#print "Finished."
  
