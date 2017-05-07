#!/bin/bash

#swy-- this does nothing, just ignore any `title whateverstring` calls from the msys
title() { true; }; export -f title

#swy-- set the ModuleSystem folder as the current directory ($PWD)
cd "$(dirname "$0")" || exit

title 'building tld for [wait for it]--'
PYTHONPATH="$PWD:$PWD/Data:$PWD/Header:$PWD/ID:$PWD/Process"; export PYTHONPATH

clear

python()
{
    test -e /usr/bin/python2 && python2 "$@" || python "$@"
}

#swy-- make it fast by calling the python2 interpreter only once
#      goes from 31.4s to 8.2s, a huge improvement in my book.
python -B -OO ./Process/process_all.py

# python -B -OO ./Process/process_init.py
# python -B -OO ./Process/process_global_variables.py
# python -B -OO ./Process/process_strings.py
# python -B -OO ./Process/process_skills.py
# python -B -OO ./Process/process_music.py
# python -B -OO ./Process/process_animations.py
# python -B -OO ./Process/process_meshes.pyddd
# python -B -OO ./Process/process_sounds.py
# python -B -OO ./Process/process_skins.py
# python -B -OO ./Process/process_map_icons.py
# python -B -OO ./Process/process_factions.py
# python -B -OO ./Process/process_items.py
# python -B -OO ./Process/process_scenes.py
# python -B -OO ./Process/process_troops.py
# python -B -OO ./Process/process_particle_sys.py
# python -B -OO ./Process/process_scene_props.py
# python -B -OO ./Process/process_tableau_materials.py
# python -B -OO ./Process/process_presentations.py
# python -B -OO ./Process/process_party_tmps.py
# python -B -OO ./Process/process_parties.py
# python -B -OO ./Process/process_quests.py
# python -B -OO ./Process/process_info_pages.py # <-- just for wb
# python -B -OO ./Process/process_scripts.py
# python -B -OO ./Process/process_mission_tmps.py
# python -B -OO ./Process/process_game_menus.py
# python -B -OO ./Process/process_simple_triggers.py
# python -B -OO ./Process/process_dialogs.py
# python -B -OO ./Process/process_postfx.py     # <-- just for wb
# python -B -OO ./Process/process_global_variables_unused.py
# rm *.pyc -- not needed anymore


#
# convert to MS-DOS/Windows newline format (swyter)
# needs this: http://linux.maruhn.com/sec/flip.html
#

if [ -e /usr/bin/flip ]; then
    flip -d ID/*.py
    flip -d ../*.txt
    flip -d ../_wb/*.txt
    flip -d  ./*.txt
    flip -u ../_wb/_tweaks_done_to_the_existing_res_tree.txt
fi

# --

msys_check()
{
    cnt=$((`cat "${1}" | wc -l` - 1))
    max=${3}

    echo -en "${2} count: $cnt/$max ... "
	
    if [ ${cnt} -lt "${max}" ]; then
        echo 'ok.'
    else
        echo 'ERROR ERROR ERROR TOO MANY!!!.'
    fi
}

#
# count objects... (mtarini)
#

msys_check ID/ID_items.py 'item' 915

# 
# count map_icons... (mtarini)
#

msys_check ID/ID_map_icons.py ' map' 256


echo ______________________________
echo ''
echo Script processing has ended.
echo Press any key to restart. . .

