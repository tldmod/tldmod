# mab flora_kinds decompiler by swyter -- 19-jan-2014

result = []

with open("flora_kinds.txt") as f:
    for line in f:
        result.append(line.split())
        
nlines = 0
nflora = int(result[nlines][0]); nlines+=1

print("there are %u plants in there!\n"%nflora)

for n in range(0,nflora):
  cur_line = result[nlines]
  #print(cur_line)
  
  thiid=str(cur_line[0])
  flags=int(cur_line[1])
  nmesh=int(cur_line[2])
  
  print("\tid: %s flags: 0x%x nmeshes: %u"%(thiid, flags, nmesh))
  
  nlines+=1
  
  for i in range(0,nmesh):
    cur_line = result[nlines]
    print("\t\tmesh_nm: %s tcol_nm: %s\n"%(cur_line[0],cur_line[1]))
    nlines+=1