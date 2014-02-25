:start

@echo off && title compiling the tld hlsl shaders thing-- && echo ^[working hard...^] ^[started at %time%^] && echo. 
start /b /wait /i /high /realtime fxc64 /D /nologo /D PS_2_X=ps_2_a /Tfx_2_0 /Fo..\mb.fx ..\mb_src.fx

echo. && echo Shader processing has ended at %time%.
echo Press any key to recompile. . .
echo ___________________________________
pause>nul
goto :start