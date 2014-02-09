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

function load(fi)
  local f,x = io.open(fi,'r'),{}
  while 1 do
      local l = f:read()
      if not l then break end
      table.insert( x, (l:gsub(regex[1],regex[2])) )
      
      --Fix the quotes from Transifex, which thinks that we're using Joomla!
      if l:find([["_QQ_"]]) ~= nil then x[#x]=(x[#x]):gsub([["?_QQ_"]],[["]]) end

  end
  f:close(); f = io.open(fi,'w')
  
  for _,out in pairs(x) do
    f:write(out.."\n")
  end
  
  f:close()
end


if arg[1] == "convert" then
  regex = {"^([^%|]+)%|(.*)","%1  = \"%2\""} print("Converting format...")
else
  regex = {"  %= \"(.*)\"","|%1"} print("Reverting format...")
end

for _,file in pairs( scandir() ) do
  --print('<'..file:match("\\([^\\]+)$")..'>')
  load(file)
end