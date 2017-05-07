# swy: make it fast by calling the python2 interpreter only once!

try:
    import process_init
    import process_global_variables
    import process_strings
    import process_skills
    import process_music

    # swy: importing the animation processor here causes problems for the others modules
    #      so just move it at the end and call it a day
    # import process_animations

    import process_meshes
    import process_sounds
    import process_skins
    import process_map_icons
    import process_factions
    import process_items
    import process_scenes
    import process_troops
    import process_particle_sys

    import process_scene_props
    import process_tableau_materials
    import process_presentations
    import process_party_tmps
    import process_parties
    import process_quests
    import process_info_pages # <-- just for wb
    import process_scripts
    import process_mission_tmps
    import process_game_menus
    import process_simple_triggers
    import process_dialogs
    import process_postfx     # <-- just for wb

    # swy: moved down here, now it's harmless :)
    import process_animations

    import process_global_variables_unused
    
    


except:
    import traceback
    print(traceback.format_exc())
