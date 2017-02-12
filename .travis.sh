# swy: as seen here <https://github.com/travis-ci/travis-ci/issues/2285> but made prettier with custom wrappers
_fold_start_() { echo -en "travis_fold:start:script.$(( ++fold_count ))\\r" && echo -ne '\033[1;33m' && echo $1 && echo -ne '\e[0m'; }
_fold_final_() { echo -en "travis_fold:end:script.$fold_count\\r"; }

_fold_start_ '[Turning original shallow clone into a full one]'
    git fetch --unshallow

_fold_final_


echo HI THERE!

# grab the revision count of the latest merge commit,
# parse the changelog page to find the previous one
SVNREV=$(git rev-list --count "`git rev-list --min-parents=2 --max-count=1 HEAD`")
PREREV=$(curl -s http://steamcommunity.com/sharedfiles/filedetails/changelog/299974223 | \
         sed -n 's/^.*Equivalent to nightly r\([0-9]*\).*$/\1/p' | head -1)


# prefix the new changelog with the standard introduction and
# make the bullet points and em-dashes pretty
echo -e "Submitted a new build. Equivalent to nightly r$SVNREV.\r\n\r\n\
Main changes since the previous r$PREREV build are:\r\n\
`git log -1 --pretty=%B`" > /tmp/desc.txt

WORKSHOP_DESC="`cat '/tmp/desc.txt'`"

echo "$WORKSHOP_DESC"
echo "----"

_fold_start_ "[Installing Wine Staging]"
    sudo add-apt-repository ppa:wine/wine-builds -yy
    sudo apt-get update -yy
    sudo apt-get install --install-recommends wine-staging winehq-staging -yy --force-yes

_fold_final_

cd ModuleSystem

_fold_start_ "[Compiling retail revision $SVNREV]"
    # disable cheat mode for the generated nightly builds...
    sed -i 's/cheat_switch = 1/cheat_switch = 0/' module_constants.py

    ./build_module.sh     2> /dev/null
    ./build_module_wb.sh  2> /dev/null

_fold_final_

cd ..

_fold_start_ "[Packaging and stripping revision $SVNREV into a Steam Workshop build]"
    # override the M&B 1.011 files with the Warband counterparts
    cp -rf ./_wb/* ./
    rm -rf _wb

    # fixed Linux case-sensitive language files detection
    mv Languages languages

    # paste the original optimized warband glsl shaders in GLShadersOptimized
    curl https://github.com/tldmod/tldmod/releases/download/TLD3.3REL/vanilla_glsl_opt.zip -L -O
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

    rm -rf .git
    
    # add a watermark to make it clear that this is not the official build
    convert main.bmp -gravity center -pointsize 30 -fill red -stroke darkred -annotate -10 '(TEST THINGIE)' -type truecolor main.bmp

_fold_final_


_fold_start_ '[Final tree view]'
    ls -lash
    #tree .

_fold_final_


_fold_start_ '[Initializing Steamworks service]'
    cd .. && mkdir steam && cd steam
    
    Xvfb :1 -screen 0 800x600x16 2> /dev/null &
    export DISPLAY=:1
    
    curl -LOJs https://github.com/tldmod/tldmod/releases/download/TLD3.3REL/Steam.exe && curl -LOJs "$STEAM_SS"

    # initialize the Wine environment and disable the sound driver output (travis-ci doesn't have any dummy ALSA devices)
    export WINEDLLOVERRIDES="mscoree,mshtml="
    export WINEDEBUG=-all

    # pre-generate the Wine environment, disable ALSA integration (Travis CI machines don't have virtual sound cards)
    # and run the SteamWorks service in the background, parse the connection status and continue when finished
    wineboot -u
    winetricks sound=disabled
    wine steam -silent -forceservice -no-browser -no-cef-sandbox -opengl -login "$STEAM_AC" "`openssl base64 -d <<< "$STEAM_TK"`" &

    ((t = 290)); while ((t > 0)); do
        grep --no-messages 'RecvMsgClientLogOnResponse()' logs/connection_log.txt | grep 'OK'                   && echo '>> OK'                   && break;
        grep --no-messages 'RecvMsgClientLogOnResponse()' logs/connection_log.txt | grep 'Invalid Password'     && echo '>> Invalid Password'     && exit 1;
        grep --no-messages 'RecvMsgClientLogOnResponse()' logs/connection_log.txt | grep 'Account Logon Denied' && echo '>> Account Logon Denied' && exit 1;

        if ((t == 1)); then
            curl -LOJ https://raw.githubusercontent.com/tremby/imgur.sh/master/imgur.sh && chmod +x ./imgur.sh
            
            ls -lash && scrot screenshot.png && ls -lash;
            ./imgur.sh screenshot.png;
            
            exit 1;
        fi;

        sleep 1 && echo ' >>' $[ t-- ];
    done
    
    # give it some seconds to settle down, slowpoke!
    sleep 20

_fold_final_


_fold_start_ '[Uploading Steam Workshop build]'
    cd .. && mv tldmod 'The Last Days of the Third Age (TEST THINGIE)'
    
    # get all we need
    curl -LOJs https://github.com/tldmod/tldmod/releases/download/TLD3.3REL/mbw_workshop_uploader_glsl_pdf_no_ogg.exe
    curl -LOJs https://github.com/tldmod/tldmod/releases/download/TLD3.3REL/steam_api.dll
    curl -LOJs https://github.com/tldmod/tldmod/releases/download/TLD3.3REL/tldmod.ini
    curl -LOJs https://github.com/tldmod/tldmod/releases/download/TLD3.3REL/tldmod.png

    echo 48700 > steam_appid.txt
    
    # don't make the test entry public
    sed -e 's/visibility = public/visibility = friends only/' tldmod.ini --in-place
    sed -e 's/The Last Days of the Third Age/The Last Days of the Third Age (TEST THINGIE)/' tldmod.ini --in-place
    
    # add a watermark to make it clear that this is not the official build
    convert tldmod.png -gravity center -pointsize 30 -fill red -stroke darkred -annotate -10 '(TEST THINGIE)' tldmod.png

    # do the actual submission using this (totally stable) work of art
    yes NO | wine mbw_workshop_uploader_glsl_pdf_no_ogg.exe update -mod tldmod.ini \
                                                                    -id 742666341  \
                                                                  -icon tldmod.png \
                                                               -changes "$WORKSHOP_DESC" | tee workshop.log
    
    ls -lash && ps
    
    # get rid of the resident background processes, we don't want travis-ci to timeout
    sleep 10 && killall -I steam.exe && killall -I Xvfb && rm -rf steam
    
    # fail the build if things didn't go as expected
    grep --no-messages 'Uploading done!' workshop.log || exit 1;

_fold_final_
