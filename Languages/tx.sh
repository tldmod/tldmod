#!/bin/sh

echo "Updating translations from Transifex..."

# mab calls zh => cnt and zh-Hans => cns
mv cnt zh
mv cns zh-Hans

# the italian ui.csv file has manual additions from the M&B third-party translation project
# don't replace it, or entries will be lost
mv it/ui.csv it/ui.csv_bak


# convert everything to Joomla INI format
luajit tx.lua convert

# push our latest strings to the web
# tx push -s -t -f --skip --no-interactive
# tx push -s -f --skip --no-interactive
# tx push -s -t -f --skip --no-interactive
# tx push -t -l sv --skip --no-interactive

# pull latest translations
tx pull -a -f --skip --minimum-perc=1

# mab calls zh => cnt and zh-Hans => cns
mv zh      cnt
mv zh-Hans cns

# the italian ui.csv file has manual additions from the M&B third-party translation project
# don't replace it, or entries will be lost
rm it/ui.csv
mv it/ui.csv_bak it/ui.csv

# revert back to mab format
luajit tx.lua revert

echo "Done!"
