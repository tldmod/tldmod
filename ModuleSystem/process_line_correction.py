file = open("module_scripts.py","r")
lines = file.readlines()
file.close()

file = open("module_scripts.py","w")

level = 0
for line in lines:
  line = line.strip()
  acceptableindex = line.find("#")
  if (acceptableindex == -1):
      acceptableindex = len(line)
  level -= line.count("try_end", 0, acceptableindex)
  level -= line.count("end_try", 0, acceptableindex)
  level -= line.count("else_try", 0, acceptableindex)
  newlevel = level
  level_positive_change = 0
  newlevel += line.count("else_try", 0, acceptableindex)
  newlevel += line.count("(", 0, acceptableindex)
  newlevel += line.count("[", 0, acceptableindex)
  newlevel += line.count("try_begin", 0, acceptableindex)
  newlevel += line.count("try_for", 0, acceptableindex)
  level_positive_change = newlevel - level
  newlevel -= line.count(")", 0, acceptableindex)
  newlevel -= line.count("]", 0, acceptableindex)
  if (level_positive_change == 0):
    level = newlevel
  for i in xrange(level):
    file.write("  ")
  level = newlevel
  file.write("%s\n"%line)
file.close()
