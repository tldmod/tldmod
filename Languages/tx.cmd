MODE CON: COLS=110
@echo off && title Updating translations from Transifex... && set path=%cd%/.tx
:up
::convert everything to Joomla INI format
luajit tx.lua convert

::push our latest strings to the web
::tx push -s -t -f --skip --no-interactive
::tx push -s -f --skip --no-interactive
::tx push -s -t -f --skip --no-interactive
::tx push -t -l sv --skip --no-interactive

::pull latest translations
tx pull -a -f --skip --minimum-perc=100 --mode=reviewer

::revert back to mab format
luajit tx.lua revert

pause
cls && goto :up