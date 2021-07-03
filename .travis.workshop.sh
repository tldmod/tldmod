#!/bin/bash

_fold_start_ "[Packaging and stripping revision $SVNREV into a Steam Workshop build]"
    # override the M&B 1.011 files with the Warband counterparts
    cp -rf ./_wb/* ./
    rm -rf _wb

    # fixed Linux case-sensitive language files detection
    mv -T Languages languages

    # paste the original optimized warband glsl shaders in GLShadersOptimized
    curl --fail -LOJ https://github.com/tldmod/tldmod/releases/download/TLD3.3REL/vanilla_glsl_opt.zip
    unzip vanilla_glsl_opt.zip -d ./ && rm vanilla_glsl_opt.zip

    # move our custom tld shaders into their rightful place
    mv GLShaders/*.glsl GLShadersOptimized/

    # strip it accordingly
   #rm -rf ./Data
    rm -f  ./Data/*.py
    rm -f  ./Data/*.log
    rm -f  ./Data/*.exe
    rm -f  ./Data/*.bik
    rm -f  ./Data/*.fxo
    rm -f  ./Data/*.bat
    rm -f  ./Data/*_old.xml
    rm -f  ./Data/*.xml.weapons_lay_down
    rm -f  ./Data/flora_kinds_*.txt

    rm -f  ./languages/*
    rm -rf ./languages/.tx
    rm -rf ./languages/_base
    rm -rf ./languages/_base_new_language
    rm -rf ./languages/_*

    rm -rf ./ModuleSystem

    rm -f  ./Music/Readme.txt
    rm -rf ./Music/LowQualityTLDSoundtrack

    rm -rf ./Resource/_*

    rm -f  ./SceneObj/*.exe
    rm -rf ./SceneObj/_*

    rm -rf ./Sounds/_*
    rm -f  ./Sounds/Readme.txt

    rm -rf ./Textures/_*
    rm -rf ./Textures/Merl\'s\ old\ original\ textures
    rm -f  ./Textures/*.xcf
    rm -f  ./Textures/*.psd
    rm -f  ./Textures/*.jpg
    rm -f  ./Textures/*.png
    rm -f  ./Textures/Readme.txt


    rm -f  ./*.bat
    rm -f  ./*.cmd
    rm -f  ./*.exe
    rm -f  ./*.dll
    rm -f  ./*.h
    rm -f  ./*src*
    rm -f  ./*.odt
    rm -f  ./*.psd
    rm -f  ./*.zip
    rm -f  ./*.rar
    rm -f  ./.*
    rm -f  ./*.yml
    rm -f  ./*.cdd
    rm -f  ./*.lua
    rm -f  ./*.htm
    rm -f  ./*.nsi
    rm -f  ./module-wb.ini
    rm -f  ./game_variables-wb.txt
    rm -f  ./*orc*
    rm -rf ./_*.txt
   #rm -rf ./_*
   #rm -f  ./*.md

    rm -rf .git

    # swy: also remove the .github folder
    rm -rf  ./.*/
    
    # add a watermark to make it clear that this is not the official build
   #convert main.bmp -gravity center -pointsize 30 -fill red -stroke darkred -annotate -10 '(TEST THINGIE)' -type truecolor main.bmp

_fold_final_


_fold_start_ '[Final Workshop tree view]'
    ls -lash
   #tree .

_fold_final_


_fold_start_ '[Deploying Steam Workshop build]'

    CONT_FLDR='The Last Days of the Third Age' # (TEST THINGIE)'

    cd .. && cp -r tldmod "$CONT_FLDR"

    echo '"workshopitem"                           '   > workshop_entry.vdf
    echo '{                                        '  >> workshop_entry.vdf
    echo '   "appid"                       "48700" '  >> workshop_entry.vdf
    echo '   "publishedfileid"         "299974223" '  >> workshop_entry.vdf
    echo "  \"contentfolder\"       \"$CONT_FLDR\" "  >> workshop_entry.vdf
   #echo "  \"changenote\"      \"$WORKSHOP_DESC\" "  >> workshop_entry.vdf
    echo "  \"changenote\" \"r$SVNREV - r$PREREV\" "  >> workshop_entry.vdf
    echo '}                                        '  >> workshop_entry.vdf

    curl --fail -LOJs 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz' && tar xvf steamcmd_linux.tar.gz

    # do the actual submission using this (totally stable) work of art
    ./steamcmd.sh +login "$steam_ac" "$steam_tk" +workshop_build_item workshop_entry.vdf +quit | tee workshop.log

    # fail the build if things didn't go as expected
    grep --no-messages 'Success.' workshop.log || exit 1;

_fold_final_
