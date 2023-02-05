# swy: as seen here <https://github.com/travis-ci/travis-ci/issues/2285> but made prettier with custom wrappers
_fold_start_() { echo -en "::group::" && echo -ne '\033[1;33m' && echo $1 && echo -ne '\e[0m'; }
_fold_final_() { echo "::endgroup::"; }


echo HI THERE!

# grab the revision count between the oldest and the latest commit,
# parse the changelog page to find the previous one on steam
SVNREV=$((`curl -u "$ghuser:$ghtoken" -s "https://api.github.com/repos/tldmod/tldmod/compare/BASE...HEAD" | jq '.total_commits'` + 1)); export SVNREV

PREREV=$(curl -s 'http://steamcommunity.com/sharedfiles/filedetails/changelog/299974223' | \
         sed -n 's/^.*Equivalent to nightly r\([0-9]*\).*$/\1/p' | head -1); export PREREV


# prefix the new changelog with the standard introduction and
# make the bullet points and em-dashes pretty
echo -e "Submitted a new build. Equivalent to nightly r$SVNREV.\r\n\r\n\
Main changes since the previous r$PREREV build are:\r\n\
`git log -1 --pretty=%B`" > /tmp/desc.txt

WORKSHOP_DESC="`cat '/tmp/desc.txt'`"

echo "$WORKSHOP_DESC"
echo "----"

cd ModuleSystem

_fold_start_ "[Compiling retail revision $SVNREV]"
    # disable cheat mode for the generated nightly builds...
    sed -i 's/cheat_switch = 1/cheat_switch = 0/' module_constants.py

    # redirect stderr to avoid log spam...
    ./build_module.sh     2> /dev/null
    ./build_module_wb.sh  2> /dev/null

_fold_final_

cd ..


_fold_start_ "[Composite custom launcher images for revision $SVNREV]"
    # use a formatted variant of the current date and revision count in the launcher
    IMAGE_TEXT="`date "+v%Y.%m.%d [$SVNREV]" -u`"

    # grab the clean backplate and the pixel font i made in 2013 so it's identical
    curl --fail -LOJ https://github.com/tldmod/tldmod/releases/download/TLD3.3REL/main_swy_pngquant.png
    curl --fail -LOJ https://github.com/tldmod/tldmod/releases/download/TLD3.3REL/Retrovirus.ttf

    # draw the text and shadow over the backplate, overwriting the original main.bmp
    # (the older BMP3 format doesn't support alpha channels, but is the only thing the launcher reads)
    convert main_swy_pngquant.png -font Retrovirus.ttf -pointsize 16 -gravity SouthWest \
      -fill '#28292c' -annotate +10+8 "$IMAGE_TEXT" \
      -fill '#e4eca0' -annotate +09+9 "$IMAGE_TEXT" \
      -type truecolor bmp3:main.bmp

    # add a copy for warband, delete the things we just downloaded
    cp main.bmp ./_wb/ && rm main_swy_pngquant.png && rm Retrovirus.ttf

_fold_final_


# --- deploy to the steam workshop if a tag triggered this build, if not go on
if [ ! -z $TRAVIS_TAG ]; then
    source ./.travis.workshop.sh
    exit
fi
# ---

_fold_start_ '[Initial TLD tree view]'
    tree -h .

_fold_final_


_fold_start_ '[Turning original shallow clone into a full one, this will take a while]'
    git fetch --unshallow
    git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
    git fetch origin

_fold_final_


_fold_start_ "[Packaging and stripping revision $SVNREV into usable incremental patches]"
    git config --global core.quotepath false
    git diff --name-status --diff-filter=ACMRTUXB TLD3.6REL ./ > diff.txt

    cat diff.txt | sed -r -e  s/^D.+// \
                          -e 's/.+modulesystem.+//I' \
                          -e 's/.*unused.*//I' \
                          -e 's/.*src.*//I' \
                          -e 's/.*cmd.*//I' \
                          -e 's/.*exe.*//I' \
                          -e 's/.*\.yml.*//I' \
                          -e 's/.*\.sh.*//I' \
                          -e 's/.*\.git.*//I' \
                          -e 's/.*\.py.*//I' \
                          -e 's/.*\.log.*//I' \
                          -e 's/.*\.exe.*//I' \
                          -e 's/.*\.tx\/.*//I' \
                          -e 's/.*\.bat.*//I' \
                          -e 's/.*\.odt.*//I' \
                          -e 's/.*\.psd.*//I' \
                          -e 's/.*\.xcf.*//I' \
                          -e 's/.*\.zip.*//I' \
                          -e 's/.*\.rar.*//I' \
                          -e 's/.*\.cdd.*//I' \
                          -e 's/.*\.lua.*//I' \
                          -e 's/.*\.nsi.*//I' \
                          -e 's/.*\/[\_|\.][^wT][^b].*//' \
                          -e '/^$/d' \
                          -e 's/^.+TLD_GA\///' > diff_mod.txt

    # swy: fix the "R099	_wb/Resource/iv_fake_houses.brf	Resource/iv_fake_houses.brf" lines by changing
    #      them to "R	Resource/iv_fake_houses.brf"; that way we handle the copying correctly after this
    sed -ri 's/^R[0-9]+.+\t(.*)$/R\t\1/' diff_mod.txt

    mkdir ../TLD

    cat ./diff_mod.txt | while read i; do cp --parents "${i:2}" "../TLD/"; done

    cd ../TLD
    #tree -h .

    # fixed Linux case-sensitive language files detection
    mv Languages languages

    # swy: also remove the .github folder
    rm -rf  ./.*/

    cd ..

    # make a copy for the warband version
    cp -rf TLD TLD_WB

    # remove the now unneeded warband subfolder from the TLD dir
    rm -rf TLD/_wb

    # overwrite the content in the warband version with the files from the _wb subfolder
    cp -rf TLD_WB/_wb/* TLD_WB/

    # remove the now empty _wb subfolder from the warband version
    rm -rf TLD_WB/_wb
    rm -f  TLD_WB/Data/mb.fxo

    # paste the original optimized warband glsl shaders in GLShadersOptimized
    curl --fail -LOJ https://github.com/tldmod/tldmod/releases/download/TLD3.3REL/vanilla_glsl_opt.zip
    unzip vanilla_glsl_opt.zip -d ./TLD_WB

    # move our custom tld shaders into their rightful place
    mv TLD_WB/GLShaders/*.glsl TLD_WB/GLShadersOptimized/

    #tree -h .

    #bbfile=TLD_3.3_nightly_patch_r$SVNREV.7z
    #bbfilewb=TLD_3.3_wbcompat_nightly_patch_r$SVNREV.7z
    #bbfile=TLD_3.5_nightly_patch_$(date +%Y.%m.%d-%H.%M -u)_r$SVNREV.7z
    #bbfilewb=TLD_3.5_wb_nightly_patch_$(date +%Y.%m.%d-%H.%M -u)_r$SVNREV.7z
    bbfile=TLD_3.6_nightly_patch_$(date +%Y.%m.%d-%H.%M -u)_r$SVNREV.7z
    bbfilewb=TLD_3.6_wb_nightly_patch_$(date +%Y.%m.%d-%H.%M -u)_r$SVNREV.7z

    # a small notice
    echo -e "This release has been churned out by an automated process, generated directly from our dev repository at revision $SVNREV,\r\n\
that doesn't mean it has to be broken, but *may* not work as well as a stable release due to lack of testing and other things.\r\n\
\r\n\
They have not been supervised by a real person, treat them as such. Also, have fun! :)\r\n\
\r\n\
--swyter\r\n\
\r\n\
PS: For more info and official support/updates take a look to <https://tldmod.github.io> and <http://moddb.com/mods/the-last-days>" > notice

    cp notice "THIS IS AN AUTOMATED RELEASE OF TLD FOR M&B 1.011, REVISION $SVNREV"
    cp notice "THIS IS AN AUTOMATED RELEASE OF TLD FOR WARBAND, REVISION $SVNREV"

_fold_final_

_fold_start_ '[Compressing finished TLD packages with 7-Zip]'
    7zr a -mx9 -r -y $bbfile TLD "THIS IS AN AUTOMATED RELEASE OF TLD FOR M&B 1.011, REVISION $SVNREV"

    # swap the M&B 1.011 folder by the Warband one
    rm -rf TLD && mv TLD_WB TLD

    7zr a -mx9 -r -y $bbfilewb TLD "THIS IS AN AUTOMATED RELEASE OF TLD FOR WARBAND, REVISION $SVNREV"

_fold_final_

_fold_start_ '[Final tree view]'
    ls -lash

_fold_final_

_fold_start_ '[Uploading finished TLD packages to Bitbucket]'
    curl --fail -LOJ https://bitbucket.org/Swyter/bitbucket-curl-upload-to-repo-downloads/raw/default/upload-to-bitbucket.sh && chmod +x ./upload-to-bitbucket.sh

    sh ./upload-to-bitbucket.sh $bbuser $bbpass $bbpage "$bbfile"   | tee    bitbucket.log
    sh ./upload-to-bitbucket.sh $bbuser $bbpass $bbpage "$bbfilewb" | tee -a bitbucket.log

    # fail the build if things didn't go as expected
    grep --no-messages 'error' bitbucket.log && exit 1;
    
_fold_final_

_fold_start_ '[Uploading finished TLD packages to GitHub]'
    owner="tldmod"; repo="tldmod-downloads"; release_id="24712210"
    ghasset="https://uploads.github.com/repos/$owner/$repo/releases/$release_id/assets"

    curl --fail --location --data-binary @"$bbfile"   -H "Authorization: token $ghauth" -H "Content-Type: application/octet-stream" "$ghasset?name=$bbfile"
    curl --fail --location --data-binary @"$bbfilewb" -H "Authorization: token $ghauth" -H "Content-Type: application/octet-stream" "$ghasset?name=$bbfilewb"
_fold_final_

_fold_start_ '[Archiving packages in the Wayback Machine]'
    # wait a bit for the servers to flush their caches
    sleep 4

    # archive the downloads in the Wayback Machine; to make them future-proof, in case Bitbucket goes nuts again
    curl -L -I "https://web.archive.org/save/https://bitbucket.org$bbpage/$bbfile"
    curl -L -I "https://web.archive.org/save/https://bitbucket.org$bbpage/$bbfilewb"
    curl -L -I "https://web.archive.org/save/https://bitbucket.org$bbpage/"

_fold_final_
