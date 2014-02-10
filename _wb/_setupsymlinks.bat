@echo off && title creating wb symlinks-- && goto :start
:: echo. > _setupsymlinks.log

:createlink
 if not exist %2 (
	echo [/] Creating junction for ^<%2^>...
 ) else (
	echo [!] File already there ^<%2^>...
 )
 
 mklink /%1 "%2" "../%2" && rem >> _setupsymlinks.log 2>>&1
 goto :eof

:start
::call :createlink J Data
call :createlink J Languages
call :createlink J Music
::call :createlink J Resource
::call :createlink J SceneObj
call :createlink J Sounds
::call :createlink J Textures

call :createlink H main.bmp
call :createlink H module.ini
call :createlink H map.txt

mkdir Data
call :createlink H Data/font_data.xml
call :createlink H Data/ground_specs.txt
call :createlink H Data/tldintro.bik

::for /f %%f in ('dir /b ..\Data') do call :createlink H Data\%%f
for /f %%f in ('dir /b ..\Resource\*.brf') do call :createlink H Resource\%%f
for /f %%f in ('dir /b ..\SceneObj\*.sco') do call :createlink H SceneObj\%%f
for /f %%f in ('dir /b ..\Textures\*.dds') do call :createlink H Textures\%%f

echo. 
echo Now comes the fun part. Enter the path to the warband folder.
echo We'll turn this _wb subfolder into a working module which the game can run.
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