import string
import types

from module_info import *
from module_game_menus import *

from process_common import *
from process_operations import *

def save_game_menu_item(ofile,variable_list,variable_uses,menu_item,tag_uses,quick_strings):
  ofile.write(" mno_%s "%(menu_item[0]))
  save_statement_block(ofile,0, 1, menu_item[1], variable_list, variable_uses,tag_uses,quick_strings)
  ofile.write(" %s "%(string.replace(menu_item[2]," ","_")))
  save_statement_block(ofile,0, 1, menu_item[3], variable_list, variable_uses,tag_uses,quick_strings)
  door_name = "."
  if (len(menu_item) > 4):
    door_name = menu_item[4]
  ofile.write(" %s "%(string.replace(door_name," ","_")))
    

def save_game_menus(variable_list,variable_uses,tag_uses,quick_strings):
  ofile = open(export_dir + "menus.txt","w")
  ofile.write("menusfile version 1\n")
  ofile.write(" %d\n"%(len(game_menus)))
  for game_menu in game_menus:
    ofile.write("menu_%s %d %s %s"%(game_menu[0],game_menu[1],string.replace(game_menu[2]," ","_"),game_menu[3]))
    save_statement_block(ofile,0,1, game_menu[4]  , variable_list, variable_uses,tag_uses,quick_strings)
    menu_items = game_menu[5]
    ofile.write("%d\n"%(len(menu_items)))
    for menu_item in menu_items:
      save_game_menu_item(ofile,variable_list,variable_uses,menu_item,tag_uses,quick_strings)
    ofile.write("\n")
  ofile.close()

def save_python_header():
  ofile = open("./ID_menus.py","w")
  for i_game_menu in xrange(len(game_menus)):
    ofile.write("menu_%s = %d\n"%(game_menus[i_game_menu][0],i_game_menu))
  ofile.close()

print "Exporting game menus data..."
save_python_header()
variable_uses = []
variables = load_variables(export_dir, variable_uses)
tag_uses = load_tag_uses(export_dir)
quick_strings = load_quick_strings(export_dir)
save_game_menus(variables,variable_uses,tag_uses,quick_strings)
save_variables(export_dir,variables,variable_uses)
save_tag_uses(export_dir, tag_uses)
save_quick_strings(export_dir,quick_strings)