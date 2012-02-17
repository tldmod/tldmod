import string
from process_common import *
from module_info import *
from module_skins import *

import string

# WARNING: The following should be the same as the number in face_generator.h
num_voice_types = 2
#####################


def replace_spaces(s0):
  return string.replace(s0," ","_")


def write_face_tex(ofile,tex_set):
  ofile.write(" %d "%len(tex_set)) 
  for tex in tex_set:
    color = tex[1]
    hair_mats = tex[2]
    hair_colors = []
    if len(tex) > 3:
      hair_colors = tex[3]
    ofile.write(" %s %d %d %d "%(tex[0],color, len(hair_mats), len(hair_colors)))
    for hair_mat in hair_mats:
      ofile.write(" %s "%(replace_spaces(hair_mat)))
    for hair_color in hair_colors:
      ofile.write(" %d "%(hair_color))
  ofile.write("\n")

def write_textures(ofile,tex_set):
  ofile.write(" %d "%len(tex_set)) 
  for tex in tex_set:
    ofile.write(" %s "%tex)
  ofile.write("\n")

def write_voices(ofile, voices):
  ofile.write(" %d "%(len(voices)))
  for voice_rec in voices:
    ofile.write(" %d %s "%(voice_rec[0],voice_rec[1]))
  ofile.write("\n")
    
def export_skins(skins):
  ofile = open(export_dir + "skins.txt","w")
  ofile.write("skins_file version 1\n")
  if len(skins) > 16:
    skins = skins[0:15]
  ofile.write("%d\n"%len(skins))
  for skin in skins:
    skin_name      = skin[0]
    skin_flags     = skin[1]
    body_name      = skin[2]
    calf_name      = skin[3]
    hand_name      = skin[4]

    head_mesh      = skin[5]
    face_keys      = skin[6]
    hair_meshes    = skin[7]
    beard_meshes   = skin[8]
    hair_textures  = skin[9]
    beard_textures = skin[10]
    face_textures  = skin[11]
    voices         = skin[12]
    skeleton_name  = skin[13]
    scale          = skin[14]

    blood_particles_1 = 0
    blood_particles_2 = 0
    constraints = []
    if len(skin) > 15:
      blood_particles_1 = skin[15]
    if len(skin) > 16:
      blood_particles_2 = skin[16]
    if len(skin) > 17:
      constraints = skin[17]
    
    ofile.write("%s %d\n %s %s %s\n"%(skin_name, skin_flags, body_name, calf_name, hand_name))
    ofile.write(" %s %d "%(head_mesh,len(face_keys)))
    for face_key in face_keys:
      ofile.write("skinkey_%s %d %d %f %f %s "%(convert_to_identifier(face_key[4]), face_key[0],face_key[1],face_key[2],face_key[3],replace_spaces(face_key[4])))
    ofile.write("\n%d\n"%len(hair_meshes))
    for mesh_name in hair_meshes:
      ofile.write(" %s "%mesh_name)
    ofile.write("\n %d\n"%len(beard_meshes)) 
    for bmn in beard_meshes:
      ofile.write("  %s\n"%bmn)
    ofile.write("\n")
    write_textures(ofile,hair_textures)
    write_textures(ofile,beard_textures)
    write_face_tex(ofile,face_textures)
    write_voices(ofile, voices)
    ofile.write(" %s %f "%(skeleton_name, scale))
    ofile.write("\n%d %d\n"%(blood_particles_1, blood_particles_2))
    ofile.write("%d\n"%(len(constraints)))
    for constraint in constraints:
      ofile.write("\n%f %d %d "%(constraint[0], constraint[1], (len(constraint) - 2)))
      for i_pair in xrange(len(constraint)):
        if i_pair > 1:
          ofile.write(" %f %d"%(constraint[i_pair][0], constraint[i_pair][1]))
    ofile.write("\n")
  ofile.close()

print "Exporting skins..."
export_skins(skins)
