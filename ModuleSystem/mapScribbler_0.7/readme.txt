MapScribbler v0.6

by Marco Tarini, 2007-2009  - all rights reserved.


What is this?
-------------

MapScribbler is an unofficial tool for editing MODs (scenarios) for the beautiful game 
Mount&Blade (by TalesWorld).

MapScribbler lets you create writings over the main map.
 
It works for Mount&Blade version 1.011.



How to use MapScribbler:
------------------------

1) Before running it for the first time:

   Get files ready:

   - edit "MapScribbler.cfg" and insert your module path there
     (and set other options if you want to).

   - in the mod directory, make two backup copies:
     copy "parties.txt" into "parties.orig.txt",
     and 
     copy "map_icons.txt" into "map_icons.orig.txt"
     both in the same directoty.

     (MapScribbler *needs* these "orig" files, and will read data from them).


2) Run it and play with it.

   Follow online instructions (F1)
   - just make sure to Export data (F12) at some point.


3) After running it for the first time:
   - in <mod directory> edit the file "module.ini" and 
     add the resource "map_names"
     by adding anywhere the line "load_mod_resource = map_names".


Now your new scribbled map it is ready. 
Just run Mount&Blade on the chosen module, and start a *new* game, to see it.


Troubleshooting:
---------------

If it does not start, look at the file "output.txt".



How to batch it:
----------------

Dedicated module builder might want to use MapScribbler in a batched 
procedure to be run after each build of the module.
Just run it with "-b": MapScribbler will load its labels, and quitely 
export data, without opening the interactive GUI.

The batched procedure to run after the build should include something like:

 copy <modDir>\parties.txt <modDir>\parties.orig.txt
 copy <modDir>\map_icons.txt <modDir>\map_icons.orig.txt
 cd <mapScribblerDir>
 mapScribbler.exe -b

(but, take care not to give to mapscribbler any orig files that  
are (a copy of) its own exported output, otherwise it will add the 
writings again and probably cause M&B to crash for duplicates.)



History
-------

Ver 0.6: (ago 2009)

ported to Mount and Blade 1.011.

Now exploits opportunity to duplicated letters to save icon space (256 limit).
(hint: letter icons can only use duplicated if they uses the same attributes (transparency, size,
case and italicization), and if they are on the same terrain slop. Use Ctrl-c and Ctrl-v
to cut and paste the attributes - use Ctrl-d to count current duplicatable letters.)


Ver 0.5. (ago 2007)

works for Mount and Blade 0.808.