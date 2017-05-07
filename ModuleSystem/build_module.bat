@echo off && title building tld for [wait for it]--
set PATH="C:\Python24";"C:\Python26";C:\Python27;%PATH%
set PYTHONPATH=%cd%;%cd%\data;%cd%\header;%cd%\id;%cd%\process

:top
cls

python -B -OO process\process_all.py

:: python -B -OO process\process_init.py
:: python -B -OO process\process_global_variables.py
:: python -B -OO process\process_strings.py
:: python -B -OO process\process_skills.py
:: python -B -OO process\process_music.py
:: python -B -OO process\process_animations.py
:: python -B -OO process\process_meshes.py
:: python -B -OO process\process_sounds.py
:: python -B -OO process\process_skins.py
:: python -B -OO process\process_map_icons.py
:: python -B -OO process\process_factions.py
:: python -B -OO process\process_items.py
:: python -B -OO process\process_scenes.py
:: python -B -OO process\process_troops.py
:: python -B -OO process\process_particle_sys.py
:: python -B -OO process\process_scene_props.py
:: python -B -OO process\process_tableau_materials.py
:: python -B -OO process\process_presentations.py
:: python -B -OO process\process_party_tmps.py
:: python -B -OO process\process_parties.py
:: python -B -OO process\process_quests.py
:: python -B -OO process\process_info_pages.py && rem <-- just for wb
:: python -B -OO process\process_scripts.py
:: python -B -OO process\process_mission_tmps.py
:: python -B -OO process\process_game_menus.py
:: python -B -OO process\process_simple_triggers.py
:: python -B -OO process\process_dialogs.py
:: python -B -OO process\process_postfx.py     && rem <-- just for wb
:: python -B -OO process\process_global_variables_unused.py
:: @del *.pyc -- not needed anymore

REM count objects... (mtarini)

set /a cnt=0
set /a max=915
for /f %%a in ('type ".\ID\ID_items.py"^|find "" /v /c') do set /a cnt=%%a
set /a cnt = cnt-1 

IF /I %cnt% LSS %max% ( 
	echo item count: %cnt%/%max% ... ok.
) ELSE ( 
	echo item count: %cnt%/%max% ... ERROR ERROR ERROR TOO MANY!!!.
)

REM
REM 
REM count map_icons... (mtarini)

set /a cnt=0
set /a max=256
for /f %%a in ('type ".\ID\ID_map_icons.py"^|find "" /v /c') do set /a cnt=%%a

IF /I %cnt% LSS %max% ( 
	echo  map icons: %cnt%/%max% ... ok.
) ELSE ( 
	echo  map icons: %cnt%/%max% ... ERROR ERROR ERROR TOO MANY!!!.
)
REM
REM 
echo ______________________________
echo.
echo Script processing has ended.
echo Press any key to restart. . .
pause>nul && goto :top
