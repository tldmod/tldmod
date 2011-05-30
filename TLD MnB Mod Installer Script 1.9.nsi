# Nullsoft Install System (NSIS) Script for Mount&Blade Mod Installation

; You'll notice comments start with a "#" or ";". ";" is more appropriate for commenting out whole lines.


!define PRODUCT_NAME "The Last Days"     #The title of your mod goes here
!define PRODUCT_FOLDER_NAME "The Last Days"  #The folder name for your mod; spaces are fine, just mind Windows restrictions (no /\:*?"<>| )
!define PRODUCT_VERSION "1.0"                #The mod version

!define MB_VERSION "1011"                   #The version of M&B the mod was created for, ex. "808" is version 0.808 of M&B.
            #The above line is used to warn people trying to install to a different M&B version that it probably won't work.
            #For any version older than 808, you should instead list 808 as the version since earlier versions cannot be properly detected.
            #If you want your mod to be installable without warning on any version of M&B, you can comment out the MB_VERSION line (with a ";")

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"    #The title given during setup of your mod, defaults to mod title and version
OutFile "The_Last_Days_${PRODUCT_VERSION}.exe"  #The filename of the installer you're creating. Change "amazing_stuff_mod" to an 'internet friendly' version of your mod's title

!define README_FILE "readme.txt"             #Change "readme.txt" to your mod's readme filename, or comment out this line (with a ";") to not have "Show Readme" option at finish
;!define INSTALL_TEXT "installer.txt"         #"installer.txt" contents will be displayed on the second (license) screen; comment out this line (with a ";") to have it skip that screen

!define MUI_ICON "tld2.ico"       #Icon your installer will use
!define MUI_UNICON "tld2.ico"     #Icon for the uninstaller (make SURE icon format is same as installer icon, can be same icon)


# Optional Graphics
# make ABSOLUTELY sure the BMP files used in the below lines exist if you uncomment the line, or installer creation will fail

;!define MUI_WELCOMEFINISHPAGE_BITMAP "welcome.bmp" #Large side bitmap for the Welcome page and the Finish page (should be 164x314 pixels)

!define MUI_HEADERIMAGE                      #If this isn't defined, the below line does nothing. You should leave this line as it is.
;!define MUI_HEADERIMAGE_BITMAP "header.bmp"        #Small bitmap image to display in the top left corner of the header on all other pages (should be 150x57 pixels)


!define CREATE_UNINSTALLER "no"         #If you want an uninstaller to be created for your mod to be listed in Add/Remove Programs, change this to "yes"



##########
#You probably shouldn't edit below this point.
#Really, I'm serious. Don't cry to me if you screw it up.
##########

# Use LZMA (best) compression method
SetCompressor lzma

# Needed so Vista and up don't nag "did installation complete successfully?" after installation
RequestExecutionLevel admin

ShowInstDetails show                         #It will show a progress text of files transferring when it installs
ShowUnInstDetails show                       #Same goes for uninstall process

!define PRODUCT_UNINST_ROOT_KEY "HKLM"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"

; MUI 1.67 compatible ------
!include "MUI.nsh"
!include "WordFunc.nsh"
!insertmacro WordFind
;!insertmacro StrFilter

; MUI Settings
!define MUI_ABORTWARNING

; Language Selection Dialog Settings
!define MUI_LANGDLL_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_LANGDLL_REGISTRY_KEY "${PRODUCT_UNINST_KEY}"
!define MUI_LANGDLL_REGISTRY_VALUENAME "NSIS:Language"

; Welcome page
!insertmacro MUI_PAGE_WELCOME                 #First thing shown is welcome screen

; LICENSE PAGE    ************************    
!ifdef INSTALL_TEXT                           #If the install.txt is defined at the top of this file,
  !define MUI_LICENSEPAGE_BUTTON "Next >"     #add in the "License" page between the welcome screen and directory screen
  !define MUI_LICENSEPAGE_TEXT_TOP "Installation Notes:"
  !define MUI_LICENSEPAGE_TEXT_BOTTOM "You should read the above for important notes about the mod, or special instructions."
  !insertmacro MUI_PAGE_LICENSE "${INSTALL_TEXT}"  #Show license screen, with text read from "installer.txt" or whatever
!endif

; Directory page
!insertmacro MUI_PAGE_DIRECTORY               #Then screen where is asks for install directory

; Instfiles page
!insertmacro MUI_PAGE_INSTFILES               #Then do actual install process

; Finish page
!ifdef README_FILE                            #If the readme is set at the top,
  !define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\${README_FILE}"  #Go ahead and set it as the readme so that the "Show Readme" option is given
!endif
!insertmacro MUI_PAGE_FINISH                  #Then show finished screen

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES             #For uninstaller creation

; Language files
!insertmacro MUI_LANGUAGE "English"           #Only english supported (could add more, but if the game is only in English, why?)

; MUI end ------


# Steam Pseudo-registry handling code

!macro ReadSteamReg This In Return
Push "${This}" ; the target variable
Push "${In}" ; the file to search within
 Call ReadSteamReg
Pop "${Return}" ; the returned data for that variable
!macroend
!define ReadSteamReg "!insertmacro ReadSteamReg"
 
Function ReadSteamReg  # this function will read a specified Steam registry file, find the specified variable name, and return the data
 Exch $R0 ; the file to search within
 Exch
 Exch $R1 ; the target variable
 Push $R6 ; file handle
 Push $R7 ; current line string
 
 FileOpen $R6 $R0 r
 
 StrCpy $R0 ""
 
 ReadSteam1:
  ClearErrors
  FileRead $R6 $R7 ; variable names and their data are separated by null characters (chr(0)), which NSIS treats like just another endline... perfect
  IfErrors ReadSteamDone
  StrCmp $R7 "$R1" 0 ReadSteam1 ; if variable name doesn't match, loop back to read and check the next line; all variable names are preceded by ""
  FileRead $R6 $R0 ; bingo, we got a variable name match, so read the next line for the data to be returned
 
 ReadSteamDone:
  FileClose $R6
 
 Pop $R7
 Pop $R6
 Pop $R1
 Exch $R0
FunctionEnd



Var /GLOBAL RPATH      ;regular M&B folder, from Windows registry
Var /GLOBAL RVER       ;regular M&B version, from Windows registry
Var /GLOBAL SAPATH     ;Steam core folder, from Windows registry
Var /GLOBAL SPATH      ;Steam M&B folder, from Steam's registry files
Var /GLOBAL SVER       ;Steam M&B version, from Steam's registry files
Var /GLOBAL NATIVE     ;"Native" mod folder
Var /GLOBAL VER_MOD    ;display string for M&B version mod works with
Var /GLOBAL VER_MB     ;display string for M&B version user has
Var /GLOBAL MOD_FOLDER ;display string for M&B version user has



Function .onInit                               #This section gets MnB directory from registry and sets variables, when installer initializes
  ReadRegStr $RPATH HKLM Software\Mount&Blade ""  #RPATH variable is MnB folder location stored in registry  
  IfFileExists "$RPATH\*.*" +2
    StrCpy $RPATH ""
  ReadRegStr $SAPATH HKLM Software\Valve\Steam "InstallPath"  #SAPATH variable is Steam Path, so we can check if M&B was installed through Steam
  StrCmp $SAPATH "" CheckedSteam             #If the Steam registry entry was blank, Steam isn't present, so M&B obviously isn't there either
	IfFileExists "$SAPATH\appcache\app_22100.vdf" 0 NoSteamFull  #full version of M&B registry found under Steam?
	  ${ReadSteamReg} "version" "$SAPATH\appcache\app_22100.vdf" "$SVER" #yes, so read the version and the folder name
	  ${ReadSteamReg} "gamedir" "$SAPATH\appcache\app_22100.vdf" "$R0"
      StrCpy $SPATH "$SAPATH\SteamApps\common\$R0" #set the full path based on the folder name
      IfFileExists "$SPATH\*.*" CheckedSteam #if the path exists, that confirms it, so don't bother checking for demo version
        StrCpy $SPATH "" #otherwise, reset the variables and then continue to check for demo version
        StrCpy $SVER ""
	NoSteamFull:
	IfFileExists "$SAPATH\appcache\app_22110.vdf" 0 CheckedSteam #demo version of M&B registry found under Steam?
	  ${ReadSteamReg} "version" "$SAPATH\appcache\app_22110.vdf" "$SVER"
	  ${ReadSteamReg} "gamedir" "$SAPATH\appcache\app_22110.vdf" "$R0"
      StrCpy $SPATH "$SAPATH\SteamApps\common\$R0"
      IfFileExists "$SPATH\*.*" CheckedSteam
        StrCpy $SPATH ""
        StrCpy $SVER ""
  CheckedSteam:
  StrCmp $RPATH "" 0 RegFine                      #If the Registry entry was present, continue
  StrCmp $SPATH "" 0 RegFine                      #If the Steam entry was present, continue	
	#uh-oh, neither the registry entry or Steam entry was present...
    MessageBox MB_ICONSTOP|MB_OK "Mount&Blade installation directory could not be determined from Registry or Steam game data! You should make absolutely sure the installation path is correct when asked."
    StrCpy $RPATH "$PROGRAMFILES\Mount&Blade"     #Use default install path instead; hopefully it is correct
  RegFine:

  !ifdef MB_VERSION                            #if the MB_VERSION setting wasn't defined at the top, skip this version checking routine
    StrCpy $R7 "${MB_VERSION}"
	StrCmp $RPATH "" +2                      #Is the regular (non-Steam) version of M&B present?
      ReadRegStr $RVER HKLM Software\Mount&Blade "Version"  #yes, so set RVER variable to MnB version value stored in registry
    StrCmp $RVER "" 0 +2                      #If the Registry entry was blank, version is assumed to be 0.808 or earlier
      StrCpy $RVER "808"                             #so, set it to 808
	
	StrCmp $RVER "1010" 0 +2           #Special consideration for 1.010/1.011, which are compatible
	  StrCpy $RVER "1011"
	StrCmp $SVER "1010" 0 +2
	  StrCpy $SVER "1011"
	StrCmp $R7 "1010" 0 +2
	  StrCpy $R7 "1011"

    StrCmp $RVER "${MB_VERSION}" RegVerFine              #See if the regular M&B version matches
    StrCmp $SVER "${MB_VERSION}" 0 RegVerBad             #apparently not, so see if the Steam M&B version matches
	  StrCpy $RPATH $SPATH                               #it does indeed,  so act accordingly
	  Goto RegVerFine
	  
	RegVerBad:                                           #neither version matches the one which the mod was made for, so...
    StrCpy $R0 "${MB_VERSION}"                           #Get display formatted copies of version numbers, i.e. "1.011" instead of "1011"
	  
	StrLen $R5 $R0
	IntCmp $R5 4 VerHighOne
	  StrCpy $VER_MOD "0.${MB_VERSION}"
	  Goto VerHighCheckTwo
	 VerHighOne:
	  StrCpy $R5 "${MB_VERSION}" 3 -3
	  StrCpy $VER_MOD "1.$R5"
	  
	VerHighCheckTwo:
	StrLen $R5 $RVER
    IntCmp $R5 4 VerHighTwo
	  StrCpy $VER_MB "0.$RVER"
	  Goto VerHighCheckThree
	 VerHighTwo:
	  StrCpy $R5 $RVER 3 -3
	  StrCpy $VER_MB "1.$R5"
	  
	VerHighCheckThree:
	StrCmp $SVER "" VerHighDone              #if Steam version wasn't set, skip Steam version reporting
	StrCmp $SVER $RVER VerHighDone           #also skip Steam version reporting if it matches regular M&B version
	  StrCmp $RVER "808" 0 +3                #if regular version wasn't set (thus 808) but Steam one is, clear formatted string
	    StrCpy $R6 ""
		Goto DoSteamVerString
	   StrCpy $R6 "$VER_MB and "
	  DoSteamVerString:
	  StrLen $R5 $SVER
	  IntCmp $R5 4 VerHighThree
		StrCpy $VER_MB "$R60.$SVER"
		Goto VerHighDone
	   VerHighThree:
		StrCpy $R5 $SVER 3 -3
		StrCpy $VER_MB "$R61.$R5"
	VerHighDone:
    MessageBox MB_ICONSTOP|MB_YESNO "This mod was created for version $VER_MOD of Mount&Blade while you appear to have M&B version $VER_MB installed. You should make sure your version of M&B is the one which this mod was created for, or it will almost certainly not work.$\n$\nDo you want to continue the installation anyway?" IDYES RegVerFine
	Quit
    
	RegVerFine:
	
  !endif
  
  StrCpy $NATIVE "$RPATH\Modules\Native"              #NATIVE variable is "Native" folder
  StrCpy $INSTDIR "$RPATH\Modules\${PRODUCT_FOLDER_NAME}"  #INSTDIR is a globally used variable for the install dir
FunctionEnd



Function .onVerifyInstDir                      #These 6 lines make sure person installing selects a folder within
  ${WordFind} $INSTDIR "Modules\" "*" $R0      #the "Modules" directory, otherwise it disables the Install
  StrCmp $R0 $INSTDIR 0 NoAbort                #button on the directory choice screen so they can't continue
    Abort
  NoAbort:
FunctionEnd


Section "MainSection" SEC01                   #Once the actual install process starts, it does this section
  SetOutPath "$INSTDIR"                        #Set the output path to the global INSTDIR variable
  SetOverwrite on                              #Always overwrite files, no matter which is newer

  ${WordFind} $INSTDIR "\" "-1*}" $MOD_FOLDER          #This line sets MOD_FOLDER to the output folder ("My Cool Mod" or whatever) 

  ${WordFind} $INSTDIR "\Modules" "-2{*" $R0   #These 4 lines check to see if MnB folder changed (person might have another MnB installation)
  StrCmp $RPATH $R0 ResetDone                     #if so, it resets variables
    StrCpy $RPATH $R0                             #Reset R4 MnB folder
    StrCpy $NATIVE "$RPATH\Modules\Native"            #Reset R6 Native folder
  ResetDone:
    
  CreateDirectory "$INSTDIR"                   #Make sure the install folder exists, create it if not

#  StrCmp $MOD_FOLDER "native" NativeContinue           #This line checks if install folder is "Native", if so, goes to NativeContinue label below
#    IfFileExists "$INSTDIR\SceneObj\*.*" NativeContinue #If there are already files here, no need to copy from Native
#      CreateDirectory "$INSTDIR\SceneObj"      #Make sure SceneObj subfolder exists, create it if not 
#      CopyFiles $NATIVE\*.* $INSTDIR               #Copy over all the files from the "Native" folder
#      CopyFiles $NATIVE\SceneObj\*.* $INSTDIR\SceneObj
#  NativeContinue:

  SetOutPath "$INSTDIR\SceneObj"                 #Change the output path to the SceneObj folder, for Scene definition files
  File /nonfatal /x *.bak /x *.orig /x *.lnk SceneObj\*.* #Don't fail creation if no files are found; exclude BAK, ORIG, and LNK files
  SetOutPath "$INSTDIR\Resource"                 #Change the output path to the Resource folder, for additional BRF files
  File /nonfatal /x *.bak /x *.orig /x *.lnk Resource\*.* #Don't fail creation if no files are found; exclude BAK, ORIG, and LNK files
  SetOutPath "$INSTDIR\Textures"                 #etc.
  File /nonfatal /x *.bak /x *.orig /x *.lnk Textures\*.*
  SetOutPath "$INSTDIR\Sounds"
  File /nonfatal /x *.bak /x *.orig /x *.lnk Sounds\*.*
  SetOutPath "$INSTDIR\Music"
  File /nonfatal /x *.bak /x *.orig /x *.lnk Music\*.*

  SetOutPath "$INSTDIR\Languages"                #note the "/r" switch on the line below, it makes the files include all files and subfolders recursively
  File /nonfatal /r /x *.bak /x *.orig /x ".*" /x *.lnk Languages\*.*
  SetOutPath "$INSTDIR\Data"                     #TLD specific
  File /nonfatal /x *.bak /x *.orig /x *.lnk Data\*.*

  SetOutPath "$INSTDIR"                          #Change the output path back to the main mod folder

  #Below File line gets files in current folder of installer script and adds them to the installer
  #Then, when the installation actually takes place, it's also used to indicate the files to extract
  #It excludes ("/x ") some files, such as NSIS scripts (this file you're looking at), icons, zip files, etc.
  #The *.* at the end makes it include every file, besides those specific filetypes it has already excluded
  #"nonfatal" switch means installer creation won't fail if no valid files are found; useful for mods with only new SCO files
  File /nonfatal /x *.nsi /x *.zip /x *.bak /x *.orig /x *.lnk /x installer.txt /x readme_installer.rtf *.*
  
SectionEnd


#Everything below this is related to the uninstaller created

Section -Post                               #this stuff creates the uninstaller after installation process completes
  StrCmp $MOD_FOLDER "native" SkipUninstCreation     #If the person installed to Native folder, don't create Uninstaller as it would delete all files in the Native folder... bad idea
  StrCmp ${CREATE_UNINSTALLER} "no" SkipUninstCreation #See if it's set (from the top of this file) to create uninstaller
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  SkipUninstCreation:
SectionEnd

Function un.onUninstSuccess                  #more stuff for uninstaller
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit                           #more stuff for uninstaller
!insertmacro MUI_UNGETLANGUAGE
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall                            #what the uninstaller actually deletes... everything including the folder, for simplicity and thoroughness
  RMDir /r "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd