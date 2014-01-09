@echo off
:start
fxc64 /D /nologo /D PS_2_X=ps_2_b /Tfx_2_0 /Fomb.fx mb_src.fx


echo Shader processing has ended.
echo Press any key to recompile. . .
echo ___________________________________
pause>nul
goto :start