--[[ IRON LAUNCHER CORE FUNTIONS FILE - ONLY FOR ADVANCED USERS, 
 [!] DON'T MODIFY IT IF YOU AREN'T SURE YOU'RE DOING!!  
 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
 ## M&B Iron Launcher for Warband | Copyright © 2009-2010 Created by Swyter. All rights reserved. ##  ]]

-- // Init Variable stuff
--[Iron Launcher]

--#{?} This option is self-explained... optional because the new Multiplayer in-hot module swap...  [1] = On  [0] = Off  | Disabled by Default
-- |-> [!] Deprecated, comment out HideOtherModules() and UnhideOtherModules()  functions instead!!
--HideOtherModules = 0

--#{?} Creates a readable and cute Log file where is explained the entire Iron Launcher tasks in your system...  [1] = On  [0] = Off  | Disabled by Default
DebugMode = 1

--#{?} Shows ugly messages if Iron Launcher fails... [1] = On  [0] = Off  | Disabled by Default
BreakPoints = 0

--#{?} Configures Iron Launcher to find the correct texture bitmap...
--FontDDS_AlternativeFilename = "FONT_SWC.dds"


-- // Restrict Modules

-- // Module Data
	--ModuleData2Data("Data\\","falls.txt");
	ModuleData2Data("Data\\","flora_kinds.txt");
	ModuleData2Data("Data\\","Font_data.xml");
	ModuleData2Data("Data\\","ground_specs.txt");
	--ModuleData2Data("Data\\","item_modifiers.txt");
	--ModuleData2Data("Data\\","mission_types.txt");
	ModuleData2Data("Data\\","skeleton_bodies.xml");
	--ModuleData2Data("Data\\","skyboxes.txt");
	--ModuleData2Data("Data\\","sound_samples1.txt");


-- // Core Resource
	CoreResources2CommonRes("Data\\","materials.brf")
	--CoreResources2CommonRes("Data\\","pictures.brf")
	CoreResources2CommonRes("Data\\","shaders.brf")
	CoreResources2CommonRes("Data\\","textures.brf")
	CoreResources2CommonRes("Data\\","ui_meshes.brf")

-- // Module Root

	ModuleRoot2CommonRoot("Data\\","mb.fx")
	ModuleRoot2CommonRoot("Data\\","mb.fxo")

--videos (wb & orig)
	--ModuleRoot2CommonRoot("Data\\","taleworlds_intro.bik")
	--ModuleRoot2CommonRoot("Data\","paradox.bik")

-- hide the other modules
	--HideOtherModules()
	--PatchRegistry()


Window.Hide(Application.GetWndHandle()); --> Useful


--#@> start the game
--------------------------------------------------------------------
WriteLogFile("["..System.GetTime(TIME_FMT_AMPM).."] Starting the game at "..MBexec.." ["..Game.."] \r\n     >Waiting for M&B close...\r\n")


find_exec = File.Find(current_folder.."\\..\\..", "m*b*a*d*.exe", false, false, nil, nil); --> dynamic exe loader
if find_exec then Shell.Execute(find_exec[1], "open", "", "..\\..\\", SW_SHOWNORMAL, true) end --> Launches the game and waits for close / with right exitcode

--Shell.Execute("..\\..\\"..MBexec, "open", "", "..\\..\\", SW_SHOWNORMAL, true);  -> old code


ErrorHandle() --> Diagnoses errors (IL hardcoded)

WriteLogFile("["..System.GetTime(TIME_FMT_AMPM).."] "..Game.." has closed, Undoing all the changes...\r\n")


--#@> when the game exits
--------------------------------------------------------------------


-- // Module Data

	--Data2trash("falls.txt");
	Data2trash("flora_kinds.txt");
	Data2trash("Font_data.xml");
	Data2trash("ground_specs.txt");
	--Data2trash("item_modifiers.txt");
	--Data2trash("mission_types.txt");
	Data2trash("skeleton_bodies.xml");
	--Data2trash("skyboxes.txt");
	--Data2trash("sound_samples1.txt");


-- // Core Resource COMMENTED (mtarini)

	CommonRes2trash("materials.brf")
	--CommonRes2trash("pictures.brf")
	CommonRes2trash("shaders.brf")
	CommonRes2trash("textures.brf")
	CommonRes2trash("ui_meshes.brf")

-- // Shader file
	CommonRoot2trash("mb.fx")
	CommonRoot2trash("mb.fxo")

--videos (wb & orig)
	--CommonRoot2trash("taleworlds_intro.bik")
	--CommonRoot2trash("paradox.bik")

--restaurar la visibilidad del resto de módulos...
    --UnhideOtherModules()
	--UnPatchRegistry()

-- Restores old rgl_config.txt / optional  :P
	--RestoreWarbandConfig()

-- work finished & ends (hardwired)