# mab flora_kinds decompiler by swyter -- 19-jan-2014

result = []

tflags = [
  #terrain condition flags -- lifted from wb's module_data thing!
  ["fkf_plain"            , 0x00000004],
  ["fkf_steppe"           , 0x00000008],
  ["fkf_snow"             , 0x00000010],
  ["fkf_desert"           , 0x00000020],
  ["fkf_plain_forest"     , 0x00000400],
  ["fkf_steppe_forest"    , 0x00000800],
  ["fkf_snow_forest"      , 0x00001000],
  ["fkf_desert_forest"    , 0x00002000],
  ["fkf_terrain_mask"     , 0x0000ffff],

  ["fkf_realtime_ligting" , 0x00010000],  #deprecated
  ["fkf_point_up"         , 0x00020000],  #uses auto-generated point-up(quad) geometry for the flora kind
  ["fkf_align_with_ground", 0x00040000],  #align the flora object with the ground normal
  ["fkf_grass"            , 0x00080000],  #is grass
  ["fkf_on_green_ground"  , 0x00100000],  #populate this flora on green ground
  ["fkf_rock"             , 0x00200000],  #is rock 
  ["fkf_tree"             , 0x00400000],  #is tree -> note that if you set this parameter, you should pass additional alternative tree definitions
  ["fkf_snowy"            , 0x00800000],
  ["fkf_guarantee"        , 0x01000000],

  ["fkf_speedtree"        , 0x02000000],  #NOT FUNCTIONAL: we have removed speedtree support on M&B Warband

  ["fkf_has_colony_props" , 0x04000000],  # if fkf_has_colony_props -> then you can define colony_radius and colony_treshold of the flora kind
]

with open("flora_kinds.txt") as f:
    for line in f:
        result.append(line.split())
        
nlines = 0
nflora = int(result[nlines][0]); nlines+=1

pyresult = []

print("there are %u plants in there!"%nflora)

for n in range(0,nflora):
  cur_line = result[nlines]
  
  thiid=str(cur_line[0])
  flags=int(cur_line[1])
  nmesh=int(cur_line[2])
  
  
  dflag = []
  
  for x in tflags:
    if flags & x[1]==x[1]:
      dflag.append(x[0])
      
  grass_density = (flags >> 32 & 0xfff !=0 and "density(%u)"%(flags >> 32 & 0xfff))
  if grass_density: dflag.append(grass_density)
  
  dflag = "|".join(dflag)
  
  if dflag == "":
    dflag = "0"
  
  print("\n\tid: %s flags: 0x%x dflag: %s nmeshes: %u"%(thiid, flags, dflag, nmesh))
  
  pymesh = []
  
  nlines+=1
  
  for i in range(0,nmesh):
    cur_line = result[nlines]
    
    tmesh_nm = str(cur_line[0])
    tcoll_nm = str(cur_line[1])
    
    print("\t\tmesh_nm: %s tcol_nm: %s"%(tmesh_nm, tcoll_nm))
    
    pymesh.append([cur_line[0], cur_line[1]])
    nlines+=1
    
  pyresult.append(tuple([thiid, dflag, pymesh]))
    
    
import pprint
pp = pprint.PrettyPrinter()
pp.pprint(pyresult)