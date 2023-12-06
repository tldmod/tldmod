#!/bin/sh

echo "Updating translations from Transifex..."

# convert everything to Joomla INI format
luajit tx.lua convert

# push our latest strings to the web (uncomment the first line and comment out the `tx pull` and three italian lines below before running it)
# tx push --source --use-git-timestamps
# tx push --source --use-git-timestamps --resources tld.item_kinds,tld.troops
# tx push -s --skip --no-interactive
# tx push -s -t -f --skip --no-interactive
# tx push -t -l sv --skip --no-interactive
# tx push -t -l zh-Hant --skip --no-interactive

# pull latest translations
tx pull -a -f --skip --minimum-perc 40 --workers 20 --silent
# tx pull -a -f --skip --minimum-perc 1 --workers 20 --silent

# revert back to mab format
luajit tx.lua revert

# the italian ui.csv file has manual additions from the M&B third-party translation project
# don't replace it, or entries will be lost; instead we append the result to it at the end
cp  it/ui.csv it/ui_transifex.csv
cat it/ui_native_template.csv  > it/ui.csv
cat it/ui_transifex.csv       >> it/ui.csv
rm  it/ui_transifex.csv


echo "Done!"