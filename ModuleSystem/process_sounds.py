from header_common import *
from module_info import *
from module_sounds import *

def write_python_header(sounds):
  file = open("./ID_sounds.py","w")
  for i_sound in xrange(len(sounds)):
    file.write("snd_%s = %d\n"%(sounds[i_sound][0],i_sound))
  file.write("\n\n")
  file.close()

def write_sounds(sound_samples, sounds):
  ofile = open(export_dir + "sounds.txt","w")
  ofile.write("soundsfile version 2\n")
  ofile.write("%d\n"%len(sound_samples))
  for sound_sample in sound_samples:
    ofile.write(" %s %d\n"%sound_sample)
  ofile.write("%d\n"%len(sounds))
  for sound in sounds:
    ofile.write("snd_%s %d %d "%(sound[0], sound[1],len(sound[2])))
    sample_list = sound[2]
    for s in  sample_list:
      ofile.write("%d "%(s))
    ofile.write("\n")
  ofile.close()

def compile_sounds(sounds):
  all_sounds = []
  for sound in sounds:
    sound_files = sound[2]
    sound_flags = sound[1]
    for i_sound_file in xrange(len(sound_files)):
      sound_file = sound_files[i_sound_file]
      sound_no = 0
      found = 0
      while (sound_no< (len(all_sounds))) and (not found):
        if all_sounds[sound_no][0] == sound_file:
          found = 1
        else:
          sound_no += 1
      if not found:
        all_sounds.append((sound_file,sound_flags))
        sound_no = len(all_sounds) - 1
      sound_files[i_sound_file] = sound_no
  return all_sounds

print "Exporting sounds..."
sound_samples = compile_sounds(sounds)
write_sounds(sound_samples, sounds)
write_python_header(sounds)
