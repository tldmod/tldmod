#!/bin/bash

set -e -u

TLD_module_name="TLD_nightly"

steam_native_path="$HOME/.steam/steam/steamapps/common/MountBlade Warband/"
steam_modules_path="$HOME/.steam/steam/steamapps/common/MountBlade Warband/Modules/"
base_path="./../"
mnb_path="./../"
wb_path="./../_wb/"

#swy-- set the _wb folder as the current directory (for the relative paths)
cd "$(dirname "$0")" || exit

if [ ! -d "$steam_modules_path" ]; then
	echo "No Warband Detected"
	exit
fi

TLD_dest_path="$steam_modules_path$TLD_module_name"

mkdir -p "$TLD_dest_path"
mkdir -p "$TLD_dest_path/Data"
mkdir -p "$TLD_dest_path/GLShaders"
mkdir -p "$TLD_dest_path/GLShadersOptimized"
mkdir -p "$TLD_dest_path/languages"
mkdir -p "$TLD_dest_path/Music"
mkdir -p "$TLD_dest_path/Resource"
mkdir -p "$TLD_dest_path/SceneObj"
mkdir -p "$TLD_dest_path/Sounds"
mkdir -p "$TLD_dest_path/Textures"

echo "Installing base files"
cp -pu "$mnb_path/main.bmp"   "$TLD_dest_path/main.bmp"
cp -pu  "$wb_path/module.ini" "$TLD_dest_path/module.ini"
cp -pu "$mnb_path/map.txt"    "$TLD_dest_path/map.txt"

# First, copy all the txt files
for f in $wb_path/*.txt; do
    dest_file="$TLD_dest_path/$(basename "$f")"

    cp -pu "$f" "$dest_file"
done

# Now, copy all the Data
echo "Installing Data"
cp -pu "$wb_path/Data/flora_kinds.txt"     "$TLD_dest_path/Data/flora_kinds.txt"
cp -pu "$wb_path/Data/ground_specs.txt"    "$TLD_dest_path/Data/ground_specs.txt"
cp -pu "$wb_path/Data/skeleton_bodies.xml" "$TLD_dest_path/Data/skeleton_bodies.xml"

cp -pu "$mnb_path/Data/font_data.xml" "$TLD_dest_path/Data/font_data.xml"
cp -pu "$mnb_path/Data/TLDintro.bik"  "$TLD_dest_path/Data/tldintro.bik"


# Now, the Shaders. Copy the techniques from GLShaders and the shaders from the
# native installation, fill with the TLD ones
echo "Installing Shaders"
cp -pu  "$wb_path/GLShaders/techniques.xml"      "$TLD_dest_path/GLShaders/techniques.xml" 
cp -rpu "$steam_native_path/GLShadersOptimized/" "$TLD_dest_path/" 
cp -pu  "$wb_path/GLShaders/"*.glsl              "$TLD_dest_path/GLShadersOptimized" 

# Now, copy the languages (only directories)
echo "Installing Languages"
for f in $mnb_path/Languages/*; do
    [ ! -d "$f" ] && continue
    [ $(basename "$f") = "_base" -o \
      $(basename "$f") = "_base_new_language" ] && continue

    dest_file="$TLD_dest_path/languages/$(basename "$f")"

    cp -pru "$f" "$dest_file"
done

# Now, copy the Music
echo "Installing Music"
cp -pru "$mnb_path/Music/Battle"        "$TLD_dest_path/Music/"
cp -pru "$mnb_path/Music/Day-Night-Map" "$TLD_dest_path/Music/"

for f in $mnb_path/Music/*.mp3; do
    dest_file="$TLD_dest_path/Music/$(basename "$f")"

    cp -pu "$f" "$dest_file"
done


# Now, copy the Sounds
echo "Installing Sounds"
for f in $mnb_path/Sounds/*.wav; do
    dest_file="$TLD_dest_path/Sounds/$(basename "$f")"

    cp -pu "$f" "$dest_file"
done

# Finally, we have to copy the Resources, Scene Objects and Textures
# according to this rule: Copy from the Warband data and fill with the
# Mount and Blade.

echo "Installing Resources"
cp -pru "$wb_path/Resource/" "$TLD_dest_path/"

for f in $mnb_path/Resource/*.brf; do
    [ -e "$wb_path/Resource/"$(basename "$f") ] && continue

    dest_file="$TLD_dest_path/Resource/$(basename "$f")"

    cp -pu "$f" "$dest_file"
done

echo "Installing Scenes"
cp -pru "$wb_path/SceneObj/" "$TLD_dest_path/"

for f in $mnb_path/SceneObj/*.sco; do
    [ -e "$wb_path/SceneObj/"$(basename "$f") ] && continue

    dest_file="$TLD_dest_path/SceneObj/$(basename "$f")"

    cp -pu "$f" "$dest_file"
done

echo "Installing Textures"
cp -pru "$wb_path/Textures/" "$TLD_dest_path/"

for f in $mnb_path/Textures/*.{dds,DDS}; do
    [ -e "$wb_path/Textures/""$(basename "$f")" ] && continue

    dest_file="$TLD_dest_path/Textures/$(basename "$f")"

    cp -pu "$f" "$dest_file"
done
