MODE CON: COLS=110
@echo off && title Updating translations from Transifex... && set path=%cd%/.tx
:up

:: the italian ui.csv file has manual additions from the M&B third-party translation project
:: don't replace it, or entries will be lost
::@move it\ui.csv it\ui.csv_bak


::convert everything to Joomla INI format
luajit tx.lua convert

::push our latest strings to the web
::tx push -s -t -f --skip --no-interactive
::tx push -s -f --skip --no-interactive
::tx push -s -t -f --skip --no-interactive
::tx push -t -l sv --skip --no-interactive
::tx push -t -l zh-Hant --skip --no-interactive

::pull latest translations
tx pull -a -f --skip --minimum-perc=40 --mode=reviewer
::tx pull -a -f --skip --minimum-perc=0 --mode=reviewer

::revert back to mab format
luajit tx.lua revert

:: the italian ui.csv file has manual additions from the M&B third-party translation project
:: don't replace it, or entries will be lost
::del   it\ui.csv
::@move it\ui.csv_bak it\ui.csv

pause
cls && goto :up