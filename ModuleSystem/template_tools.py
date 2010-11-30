from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *

class Game_Menu_Template(object):
  """
  This class allows the user to define a template for a M&B game menu.
  The attributes of the Menu_Template object correspond to the field values
  of each M&B game menu tuple.  A template is different than a normal game
  menu in that it allows long chains of menus with huge lists of options
  to be dynamically generated from an input list. For example, given a list
  of all units in the game, one could define a template that would generate
  a list of their names on the screen. See the included examples.
  
  """
  
  def __init__(self, id="", flags=0, text="", mesh="none",opers=[],
               optn_id="", optn_cond=[], optn_text="", optn_consq=[]):
    """See the documentation of module_game_menus"""
    self.id = id
    self.flags = flags
    self.text = text
    self.mesh = mesh
    self.opers = opers
    self.optn_id = optn_id
    self.optn_cond = optn_cond
    self.optn_text = optn_text
    self.optn_consq = optn_consq
  
  def generate_menus(self, input_list, pagelen=13):
    """
    generates the game menu based on the template and the input list
    
    Arguments:
    input_list -- list of values which will be used to format template strings
    
    Keyword Arguments:
    pagelen -- number of template options to show on a page. Do not use values larger than
               13, as there are currently a maximum of 16 option slots per game menu and
               3 of them need to be used for the next, previous and go back options.
               
    """
    def format_strings(str_or_obj):
      """Helper function for generate_menus.
      
      Contains the format fields that will be used to replace template strings
      
      """
      format_fields = {
          "list_len" : len(input_list),
          "list_item": input_list[page_group + page],
          "list_index": page_group + page,
          "current_page": page_group/pagelen + 1,
          "num_pages": len(input_list)/pagelen + 1,
      }
      
      if type(str_or_obj) == str:
        return str_or_obj.format(**format_fields)
      else:
        formatted_obj = []
        try:
          formatted_obj = [format_strings(sub_obj) for sub_obj in str_or_obj]
          if type(str_or_obj) == tuple: formatted_obj = tuple(formatted_obj)
          return formatted_obj
        except TypeError: return str_or_obj

    #main method starts here#
    
    menus = []

    for page_group in xrange(0, len(input_list), pagelen):
      page = 0
      optns = []
      next_page = page_group + pagelen
      prev_page = page_group - pagelen
      menu = [self.id + str(page_group)]
      menu += format_strings([self.flags, self.text, self.mesh, self.opers])
      
      optns.append(
        ("back",[],"Go back.",
          [(change_screen_quit)]
        )
      )  
      if next_page < len(input_list):
        optns.append(
          ("next",[],"Next...",
            [(jump_to_menu, "mnu_" + self.id + str(next_page))]
          )
        )
      if prev_page >= 0:
        optns.append(
          ("previous",[],"Previous...",
            [(jump_to_menu, "mnu_" + self.id + str(prev_page))]
          )
        )
        
      while page < min(pagelen, len(input_list) - page_group):
        current_index = page_group + page
        optn_list = [self.optn_id + str(current_index)]
        optn_list += format_strings([self.optn_cond,self.optn_text, self.optn_consq])
        optns.append(optn_list)
        page += 1
  
      menu.append(tuple(optns))
      menus.append(menu)
      
    return menus
    
def get_flags_from_bitmap(header_module, flag_prefix, bitmap):
  flags = []
  header_dict = header_module.__dict__
  for key in header_dict.keys():
    if key.startswith(flag_prefix):
      flag_bitmap = header_dict[key]
      if bitmap & flag_bitmap != 0: flags.append(key)
  if flags == []: return ""
  else:
    flags = [flag[3:] for flag in flags]
    return ": " + "|".join(flags)