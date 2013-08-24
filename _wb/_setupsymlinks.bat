@echo off && title creating wb symlinks-- && goto :start

:createlink
 echo Creating junction for ^<%2^>...
 mklink /%1 "%2" "../%2"
 goto :eof

:start
call :createlink J Data
call :createlink J Languages
call :createlink J Music
call :createlink J Resource
call :createlink J SceneObj
call :createlink J Sounds
call :createlink J Textures

call :createlink H main.bmp
call :createlink H module.ini
call :createlink H map.txt

echo. 
echo Now comes the fun part. Enter the path to the warband folder.
echo. 
echo [!] A junction is just a shortcut which acts like a real folder,
echo     so don't create a module folder manually under WB, it's automatic!
echo. 
echo     Close to skip, in case it^'s already done.
echo. 
set /p wbpath=Type something like [c:\wb\modules\tld] : 
mklink /J %wbpath% .

echo. && echo --- && echo It^'s done, you can close this window now... How cool is that?
                     echo Oh, and compile Warband to generate the text files! && pause>nul