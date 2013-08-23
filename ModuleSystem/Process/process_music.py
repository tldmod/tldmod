import string
from header_common import *
from module_info import *
from module_music import *
from process_common import *

def save_python_header():
  ofile = open("./ID_music.py","w")
  for i_track in xrange(len(tracks)):
    ofile.write("track_%s = %d\n"%(tracks[i_track][0],i_track))
  ofile.write("\n\n")
  ofile.close()

def save_tracks():
  file = open(export_dir + "music.txt","w")
  file.write("%d\n"%len(tracks))
  for track in tracks:
    file.write("%s %d %d\n"%(track[1], track[2], (track[2] | track[3])))
  file.close()

print "Exporting tracks..."
save_python_header()
save_tracks()
