MODE CON: COLS=110
@echo off && title Updating translations from Transifex... && set path=%cd%/.tx
:up

:: mab calls zh => cnt and zh-Hans => cns
rename cnt zh
rename cns zh-Hans

::convert everything to Joomla INI format
luajit tx.lua convert

::push our latest strings to the web
::tx push -s -t -f --skip --no-interactive
::tx push -s -f --skip --no-interactive
::tx push -s -t -f --skip --no-interactive
::tx push -t -l sv --skip --no-interactive

::pull latest translations
tx pull -a -f --skip --minimum-perc=40 --mode=reviewer

::revert back to mab format
luajit tx.lua revert

:: mab calls zh => cnt and zh-Hans => cns
rename zh      cnt
rename zh-Hans cns

pause
cls && goto :up