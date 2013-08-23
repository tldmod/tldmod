@echo off && title building tld for 1.011--
set PATH="C:\Python24";"C:\Python26";%PATH%

:top
cls

python -B -OO process_init.py
python -B -OO process_global_variables.py
python -B -OO process_strings.py
python -B -OO process_skills.py
python -B -OO process_music.py
python -B -OO process_animations.py
python -B -OO process_meshes.py
python -B -OO process_sounds.py
python -B -OO process_skins.py
python -B -OO process_map_icons.py
python -B -OO process_factions.py
python -B -OO process_items.py
python -B -OO process_scenes.py
python -B -OO process_troops.py
python -B -OO process_particle_sys.py
python -B -OO process_scene_props.py
python -B -OO process_tableau_materials.py
python -B -OO process_presentations.py
python -B -OO process_party_tmps.py
python -B -OO process_parties.py
python -B -OO process_quests.py
python -B -OO process_info_pages.py
python -B -OO process_scripts.py
python -B -OO process_mission_tmps.py
python -B -OO process_game_menus.py
python -B -OO process_simple_triggers.py
python -B -OO process_dialogs.py
python -B -OO process_global_variables_unused.py
python -B -OO process_postfx.py
:: @del *.pyc -- not needed anymore
echo.
echo ______________________________
echo.
echo Script processing has ended.
echo Press any key to restart. . .
pause>nul && goto :top