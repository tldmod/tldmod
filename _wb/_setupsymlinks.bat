@echo off && title creating wb symlinks-- && goto :start
:: echo. > _setupsymlinks.log

:createlink
 if not exist "%2" (
	echo [/] Creating junction for ^<%2^>...
 ) else (
	echo [!] File already there ^<%2^>...
	
	:: swy: running 'fsutil hardlink list <file>' shows a the list of paths that share the same file
	::      we can count the lines that the command outputs and if they are more than 1 then that
	::      probably means this file is a symlink. at least under the _wb folder.
	for /f "usebackq" %%b in (`fsutil hardlink list "%2" ^| find "" /v /c`) do (
		
		:: swy: 1 normal file: ignore. 2 or more: symlink. get rid of it so that we can recreate it afterwards
		::      we want to recreate links because files and folders may have moved around, and the
		::      links may no longer point to the right file, as the mod changes
		if %%b geq 2 (
			echo  [i] This is a junction; line count is %%b. deleting first:
			echo       %~f2
			del "%2"
		)
	)
 )
 
 if %1 neq "H" (
	mklink /%1 "%2" "../%2" && rem >> _setupsymlinks.log 2>>&1
 ) else (
	mklink /%1 "%2" "../%2" && rem >> _setupsymlinks.log 2>>&1
 )
 
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
call :createlink H Data/item_modifiers.txt
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
set /p wbpath=Type something like [C:\Program Files (x86)\Mount^&Blade Warband\Modules\tld] : 
mklink /J "%wbpath%" .

echo. && echo --- && echo It^'s done, you can close this window now... How cool is that?
                     echo Oh, and compile Warband to generate the text files! && pause>nul
