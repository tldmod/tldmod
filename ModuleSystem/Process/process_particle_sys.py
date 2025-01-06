from module_info import *
from module_particle_systems import *
from process_common import *

id_pos        = 0
flags_pos     = 1
mesh_name_pos = 2
num_particles_pos = 3
life_pos      = 4
damping_pos   = 5
gravity_pos   = 6
turb_size_pos = 7
turb_wt_pos   = 8
alpha_key_pos = 9
red_key_pos         = alpha_key_pos + 2
green_key_pos       = red_key_pos   + 2
blue_key_pos        = green_key_pos + 2
scale_key_pos       = blue_key_pos  + 2
emit_box_size_pos   = scale_key_pos + 2
emit_velocity_pos   = emit_box_size_pos + 1
emit_rndmness_pos   = emit_velocity_pos + 1
angular_speed_pos   = emit_rndmness_pos + 1
angular_damping_pos = angular_speed_pos + 1

def save_psys_keys(ofile, keys1, keys2):
    ofile.write("%s %s   %s %s\n"%(sf(keys1[0]), sf(keys1[1]), sf(keys2[0]), sf(keys2[1])))

def save_particle_systems():
  ofile = open(export_dir + "particle_systems.txt","w")
  ofile.write("particle_systemsfile version 1\n")
  ofile.write("%d\n"%len(particle_systems))
  for psys in particle_systems:
    ofile.write("psys_%s %d %s  "%(psys[0], psys[1], psys[2]))
    ofile.write("%d %s %s %s %s %s \n"%(psys[num_particles_pos], sf(psys[life_pos]), sf(psys[damping_pos]), sf(psys[gravity_pos]), sf(psys[turb_size_pos]), sf(psys[turb_wt_pos])))
    save_psys_keys(ofile,psys[alpha_key_pos],psys[alpha_key_pos+1])
    save_psys_keys(ofile,psys[red_key_pos],psys[red_key_pos+1])
    save_psys_keys(ofile,psys[green_key_pos],psys[green_key_pos+1])
    save_psys_keys(ofile,psys[blue_key_pos],psys[blue_key_pos+1])
    save_psys_keys(ofile,psys[scale_key_pos],psys[scale_key_pos+1])
    ofile.write("%s %s %s   "%(sf(psys[emit_box_size_pos][0]),sf(psys[emit_box_size_pos][1]),sf(psys[emit_box_size_pos][2])))
    ofile.write("%s %s %s   "%(sf(psys[emit_velocity_pos][0]),sf(psys[emit_velocity_pos][1]),sf(psys[emit_velocity_pos][2])))
    ofile.write("%s \n"%sf(psys[emit_rndmness_pos]))
    if (len(psys) >= (angular_speed_pos + 1)):
      ofile.write("%s "%sf(psys[angular_speed_pos]))
    else:
      ofile.write("0 ")
    if (len(psys) >= (angular_damping_pos + 1)):
      ofile.write("%s "%sf(psys[angular_damping_pos]))
    else:
      ofile.write("0 ")
    ofile.write("\n")
  ofile.close()

def save_python_header():
  ofile = open("./ID/ID_particle_systems.py","w")
  for i_particle_system in range(len(particle_systems)):
    ofile.write("psys_%s = %d\n"%(particle_systems[i_particle_system][0],i_particle_system))
  ofile.close()

print("Exporting particle data...")
save_particle_systems()
save_python_header()
