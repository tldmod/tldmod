from module_info import *

sf_day        = 0x00000000
sf_dawn       = 0x00000001
sf_night      = 0x00000002

sf_clouds_0   = 0x00000000
sf_clouds_1   = 0x00000010
sf_clouds_2   = 0x00000020
sf_clouds_3   = 0x00000030

sf_no_shadows = 0x10000000
sf_HDR        = 0x20000000  # this will generate HDR-shaded skyboxes, you should make a LDR version of your skybox for compatibility

# mesh_name, flags, sun_heading, sun_altitude, flare_strength, postfx, sun_color, hemi_color, ambient_color, (fog_start, fog_color),

# to generate new skybox textures with hdr option:
# hdr images are required to generate our RGBE coded skybox images


# To add a skybox, you should first edit this file and put new skyboxes.txt file into the "Data/" folder of your module. 
# The first "mesh_name" parameter is the name of the skybox mesh to be used for that entry. 
# You can check our meshes from the "skyboxes.brf" file with OpenBRF and copy them, 
# just replace the material's textures with yours. And you will also have to change the 
# specular color parameters for correct hdr rendering. of course specular color does not 
# corresponds to specular lighting, those parameters are used as compression values 
# for RGBE decoding and should be generated while you generate RGBE textures. 
# (specular.red = Scale component, specular.green = Bias component) 
# You can check our materials for the instances of this usage. 
#
# For skybox textures, we are using uncompressed *.hdr files to generate *_rgb.dds and *_exp.dds files. 
# its just a RGBE encoding of the skybox for hdr lighting. here is an example: 
# "skybox.dds" -> simple non-hdr (LDR) image, used when you dont use hdr (DXT1 format is good)
# "skybox_rgb.dds" -> RGB components of the HDR image (DXT1 format is preffered)
# "skybox_exp.dds" -> E (exponent) component of the HDR image (L16 format is good, you can use half resolution for this texture)
# We are using our own command line tool to generete those files from "skybox.hdr" image. 
# But you can generate them with some of the hdr-image editors too. The images should be gamma corrected and should not have mipmaps. 
# You can use Photoshop with DDS plug-ins or DirectX Texture Viewer to see the contents of our dds images. 
# 
# ..visit Taleworlds Forums for more information..

skyboxes = [

  ("skybox_cloud_1", sf_day|sf_clouds_1, 179.0, 52.0, 0.85, "pfx_sunny", (1.39*1.32,1.39*1.21,1.39*1.08), (0.0, 0.0, 0.0), (0.96*16.0/255,0.96*23.5/255,0.96*44.5/255), (300, 0xFF8CA2AD)),
  ("skybox_cloud_1", sf_day|sf_clouds_1|sf_HDR, 179.0, 52.0, 0.85, "pfx_sunny", (1.39*1.32,1.39*1.21,1.39*1.08), (0.0, 0.0, 0.0), (0.86*16.0/255,0.86*23.5/255,0.86*44.5/255), (300, 0xFF8CA2AD)),

  ("skybox_night_1", sf_night|sf_clouds_1, 152.0, 38.0, 0.0, "pfx_night", (1.0*17.0/255,1.0*21.0/255,1.0*27.0/255),(0.0,0.0,0.0), (0.9*5.0/255,0.9*5.0/255,0.9*15.0/255), (500, 0xFF152035)),
  ("skybox_night_1", sf_night|sf_clouds_1|sf_HDR, 152.0, 38.0, 0.0, "pfx_night", (1.0*17.0/255,1.0*21.0/255,1.0*27.0/255),(0.0,0.0,0.0), (0.9*5.0/255,0.9*5.0/255,0.9*15.0/255), (500, 0xFF152035)),
  ("skybox_night_2", sf_night|sf_clouds_3, 152.0, 38.0, 0.0, "pfx_night", (1.0*17.0/255,1.0*21.0/255,1.0*27.0/255),(0.0,0.0,0.0), (0.9*5.0/255,0.9*5.0/255,0.9*15.0/255), (500, 0xFF152035)),
  ("skybox_night_2", sf_night|sf_clouds_3|sf_HDR, 152.0, 38.0, 0.0, "pfx_night", (1.0*17.0/255,1.0*21.0/255,1.0*27.0/255),(0.0,0.0,0.0), (0.9*5.0/255,0.9*5.0/255,0.9*15.0/255), (500, 0xFF152035)),
  
  ("skybox_sunset_1", sf_dawn|sf_clouds_1, 180.0, 9.146, 0.7, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),
  ("skybox_sunset_1", sf_dawn|sf_clouds_1|sf_HDR, 180.0, 9.146, 0.7, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),
  
  ("skybox_cloud_2", sf_day|sf_clouds_2, 180.0, 19.17, 0.4, "pfx_cloudy", (0.8*0.9,0.8*0.85,0.8*0.75),(0.0,0.0,0.0), (0.8*40.0/255,0.8*46.5/255,0.8*77.0/255), (120, 0xFF607090)),
  ("skybox_cloud_2", sf_day|sf_clouds_2|sf_HDR, 180.0, 19.17, 0.4, "pfx_cloudy", (0.8*0.9,0.85*0.8,0.8*0.75),(0.0,0.0,0.0), (0.8*40.0/255,0.8*46.5/255,0.8*77.0/255), (120, 0xFF607090)),
  
  ("skybox_cloud_2", sf_day|sf_clouds_3|sf_no_shadows, 180.0, 19.17, 0.4, "pfx_overcast", (0.4,0.35,0.31),(0.0,0.0,0.0), (50.0/255,60.0/255,103.0/255), (120, 0xFF607090)),
  ("skybox_cloud_2", sf_day|sf_clouds_3|sf_no_shadows|sf_HDR, 180.0, 19.17, 0.4, "pfx_overcast", (0.4,0.35,0.31),(0.0,0.0,0.0), (50.0/255,60.0/255,103.0/255), (120, 0xFF607090)),
  
  ("skybox_clearday", sf_day|sf_clouds_0, 179.0, 80.0, 0.95, "pfx_sunny", (0.99*1.32,0.99*1.21,0.99*1.08), (0.0, 0.0, 0.0), (0.96*16.0/255,0.96*23.5/255,0.96*44.5/255), (300, 0xFF8CA2AD)),
  ("skybox_clearday", sf_day|sf_clouds_0|sf_HDR, 179.0, 80.0, 0.95, "pfx_sunny", (0.99*1.32,0.99*1.21,0.99*1.08), (0.0, 0.0, 0.0), (0.86*16.0/255,0.86*23.5/255,0.86*44.5/255), (300, 0xFF8CA2AD)),
]



def save_skyboxes():
  file = open("../"+export_dir+"/data/skyboxes.txt","w+")
  file.write("%d\n"%len(skyboxes))
  for skybox in  skyboxes:
    file.write("%s %d %f %f %f %s\n"%(skybox[0],skybox[1],skybox[2],skybox[3],skybox[4],skybox[5]))
    file.write(" %f %f %f "%skybox[6])
    file.write(" %f %f %f "%skybox[7])
    file.write(" %f %f %f "%skybox[8])
    file.write(" %f %d\n"%skybox[9])
  file.close()

print "Exporting skyboxes..."
save_skyboxes()
print "Finished."
  
