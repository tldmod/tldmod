-- http://stackoverflow.com/a/11130774
-- Lua implementation of PHP scandir function
function scandir()
    local i, t, popen = 0, {}, io.popen
    for filename in popen('dir *.csv /s /b'):lines() do
        --print(filename)
        i = i + 1
        t[i] = filename
    end
    return t
end

function ssSplit(str, delim, maxNb) --from <http://lua-users.org/wiki/SplitJoin> #Function: Split a string with a pattern, Take Three
    -- Eliminate bad cases...
    if string.find(str, delim) == nil then
        return { str }
    end
    if maxNb == nil or maxNb < 1 then
        maxNb = 0    -- No limit
    end
    local result = {}
    local pat = "(.-)" .. delim .. "()"
    local nb = 0
    local lastPos
    for part, pos in string.gfind(str, pat) do
        nb = nb + 1
        result[nb] = part
        lastPos = pos
        if nb == maxNb then break end
    end
    -- Handle the last field
    if nb ~= maxNb then
        result[nb + 1] = string.sub(str, lastPos)
    end
    return result
end


function Split(str, delim, maxNb) --from <http://lua-users.org/wiki/SplitJoin> #Function: Split a string with a pattern, Take Three
    -- Eliminate bad cases...
    if string.find(str, delim) == nil then
        return { str }
    end
    if maxNb == nil or maxNb < 1 then
        maxNb = 0    -- No limit
    end
    local result = {}
    local pat = "(.-)%|?(.*)"
    local nb = 0
    local lastPos
    for part, pos in string.gfind(str, pat) do
        nb = nb + 1
        result[nb] = part
        lastPos = pos
        if nb == maxNb then break end
    end
    -- Handle the last field
    if nb ~= maxNb then
        result[nb + 1] = string.sub(str, lastPos)
    end
    return result
end

function load(fi)
  
  local f,xb = io.open("_base\\"..fi:match("\\([^\\]+)$"),'r'),{}
  if f then
    -- print("-----base ")
    while 1 do
        local l = f:read()
        if not l then break end
        
        -- id,str=l:match("^(.+)%|(.+)$")
        local id,str=l:match("^(.-)|(.*)$")
        --local split=Split(l,"|")
        --if l:find("[%|%=]%<(.+)%>$") == nil then table.insert(xb, {id, str}) end
        -- if l:find("[%|%=]%<(.+)%>$") == nil then xb[id]=str end
        if id and str then xb[id]=str else print("empty id:"..(id or "").." or str:"..(str or "")) end
        --table.insert(xt, split)
        --print(xb[#xb])
        --print(x[#x])
    end f:close()
    print(("\tbase (%d)"):format(#xb))
    
    
    --print("-----trans")
    local f,xt = io.open(fi,'r'),{}
    while 1 do
        local l = f:read()
        if not l then break end
        
        --id,str=l:match("^(.+)%|(.+)$")
        -- id,str=Split(l,"|")
        
        -- xb[id]=str
        
        --local split=Split(l,"|")
        -- xt[split[1]]=split[2]
        ----table.insert(xt, {id=split[1],str=split[2]})
        
        
        local id,str=l:match("^(.-)|(.*)$")
        table.insert(xt, {id=id,str=str})
        
        
        -- if l:find("[%|%=]%<(.+)%>$") == nil then table.insert(xt, l) end
        -- if l:find("[%|%=]%<(.+)%>$") == nil then xt[id]=str end
        --print(x[#x])
    end f:close(); -- f = io.open(fi,'w')
    
    print(("\ttran/base (%d/%d)"):format(#xt,#xb))
    
    
    f = io.open(fi,'w')
    for id,var in pairs(xt) do
      if var.str and xb[var.id]~=var.str then
        f:write(var.id.."|"..(var.str).."\n")
        --print(id.." || "..str.."\n")
      else print("\tnot original: "..(var.id or "")) end
    end
    f:close()
    
  else print("\twe don't have any _base reference!") end
  -- for _,out in pairs(x) do
    -- f:write(out.."\n")
  -- end
end

for _,file in pairs( scandir() ) do
  --print(file,file:match("\\([^\\]+)\\[^\\]+$"))
  print('\n<'..file:match("\\([^\\]+)\\[^\\]+$")..":"..file:match("\\([^\\]+)$")..'>')
  
  base=file:match("\\([^\\]+)\\[^\\]+$")
  --print("--"..base)
  if  base ~= "_base"
  and base ~= "en"
  and base ~= "pl-a"
  and base ~= "pl-b" then
    --print("--file: "..file)
    --print('\n<'..file:match("\\([^\\]+)\\[^\\]+$")..":"..file:match("\\([^\\]+)$")..'>')
    load(file)
  else print("\tnot translatable, blacklisted!") end
end