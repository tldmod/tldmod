@echo off && title building tld for 1.011--
set PATH="C:\Python24";"C:\Python26";%PATH%
set PYTHONPATH=%cd%;%cd%\data;%cd%\header;%cd%\id;%cd%\process

:top
cls

python -B -OO process\process_init.py
python -B -OO process\process_global_variables.py
python -B -OO process\process_strings.py
python -B -OO process\process_skills.py
python -B -OO process\process_music.py
python -B -OO process\process_animations.py
python -B -OO process\process_meshes.py
python -B -OO process\process_sounds.py
python -B -OO process\process_skins.py
python -B -OO process\process_map_icons.py
python -B -OO process\process_factions.py
python -B -OO process\process_items.py
python -B -OO process\process_scenes.py
python -B -OO process\process_troops.py
python -B -OO process\process_particle_sys.py
python -B -OO process\process_scene_props.py
python -B -OO process\process_tableau_materials.py
python -B -OO process\process_presentations.py
python -B -OO process\process_party_tmps.py
python -B -OO process\process_parties.py
python -B -OO process\process_quests.py
python -B -OO process\process_scripts.py
python -B -OO process\process_mission_tmps.py
python -B -OO process\process_game_menus.py
python -B -OO process\process_simple_triggers.py
python -B -OO process\process_dialogs.py
python -B -OO process\process_global_variables_unused.py
:: @del *.pyc -- not needed anymore
REM
REM adding scripts on map with mapscribbler... (mtarini)
echo Adding text map-icons with MapScribbler...
copy /Y ..\parties.txt ..\parties.orig.txt  >nul
copy /Y ..\map_icons.txt ..\map_icons.orig.txt >nul
cd mapScribbler_0.7
mapScribbler.exe -b
type stderr.txt
cd ..
REM
REM count objects... (mtarini)
set /a cnt=0
set /a max=915
for /f %%a in ('type ".\ID\ID_items.py"^|find "" /v /c') do set /a cnt=%%a
set /a cnt = cnt-1 
IF /I %cnt% LSS %max% ( 
echo Item count: %cnt%/%max% ... ok.
) ELSE ( 
echo Item count: %cnt%/%max% ... ERROR ERROR ERROR TOO MANY!!!.
)
REM
REM 
echo ______________________________
echo.
echo Script processing has ended.
echo Press any key to restart . . .
pause>nul && goto :top