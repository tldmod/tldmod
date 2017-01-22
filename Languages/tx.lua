-- http://stackoverflow.com/a/11130774
-- Lua implementation of PHP scandir function
function scandir()
    local ffi = require 'ffi'
    
    local command = {
    Windows = 'dir *.csv /s /b',
       Unix = 'find ./ -name "*.csv"'
    }
    
    -- added *nix compatibility so that Fantu can do things!
    command = (ffi.os == "Windows") and command[ffi.os]
                                     or command['Unix']
    
    local i, t, popen, os = 0, {}, io.popen, ffi.os
    for filename in popen(command):lines() do
        --print(filename)
        i = i + 1
        t[i] = filename
    end
    return t
end

function load(fi)
  local f,x = io.open(fi,'r'),{}
  while 1 do
      local l = f:read()
      if not l then break end
      table.insert( x, (l:gsub(regex[1],regex[2])) )
      
      --Fix the quotes from Transifex, which thinks that we're using Joomla!
      if l:find([["_QQ_"]]) ~= nil then x[#x]=(x[#x]):gsub([["?_QQ_"]],[["]]) end
      --Fix the stubborn /\\ to /\
      if l:find([[/\\]]) ~= nil then x[#x]=(x[#x]):gsub([[/\\]],[[/\]]) end
      --Fix the occasional |" to |
      x[#x]=(x[#x]):gsub([[|"]],[[|]])

  end
  f:close(); f = io.open(fi,'w')
  
  for _,out in pairs(x) do
    f:write(out.."\n")
  end
  
  f:close()
end


if arg[1] == "convert" then
  regex = {"^([^%|]+)%|([^\n\r]*)","%1  = \"%2\""} print("Converting format...")
else
  regex = {"  %= \"(.*)\"","|%1"} print("Reverting format...")
end

for _,file in pairs( scandir() ) do
  --print('<'..file:match("\\([^\\]+)$")..'>')
  load(file)
end
