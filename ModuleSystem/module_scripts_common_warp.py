from header_common import *
from header_operations import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from ID_animations import *
from ID_troops import *
from ID_factions import *
#from module_troops import *

from module_info import wb_compile_switch as is_a_wb_script

# Credits to Autolykos, thread https://forums.taleworlds.com/index.php?topic=335511.0
# Removed: Roman numeral script
# Added: script_warp_array_create, script_warp_temp_array_create, script_warp_get_quick_array
#        script_warp_array_delete, script_cf_warp_array_get_random, script_warp_array_truncate
# Modified: script_warp_array_sort & script_warp_array_sort_range to not require a static party

common_warp_templates = [
  ("warp_array","warp_array",pf_disabled|pf_no_label|pf_is_static,0,fac_commoners,0,[]),
  ("warp_temp_array","warp_temp_array",pf_disabled|pf_no_label|pf_is_static,0,fac_commoners,0,[]),
]

common_warp_scripts = [
###################################
# Common Warband ARray Processing #
###################################
# Functional programming using Party Slots as arrays (or stacks)
# Parties are the only way to dynamically allocate memory in WB scripts
# Slots are already arrays of integers (or IDs), making them ideal for storage
# Slot zero is reserved for the number of elements

# Part I - Building Blocks
##########################

  # script_warp_array_create
  # Creates a clear array. They dont get autopruned, so doublecheck that the array is properly deleted when not longer in use.
  # For local use, when data persistence over some game map hours is not required, use script_warp_temp_array_create instead.
  # Input: nothing
  # Output: reg0 = party_id of the array
  ("warp_array_create",[
    (spawn_around_party,"p_main_party","pt_warp_array"),
    (party_set_ai_behavior,reg0, ai_bhvr_hold),
    # Debug info, translation not needed
    (assign,":tmp",reg1),(store_current_hours,reg1),(party_set_name,reg0,"@warp_array created at {reg1}"),(assign,reg1,":tmp"),
  ]),

  # script_warp_temp_array_create
  # Creates a clear temporary array. They are deleted from time to time, so don't use them for persistent data storage.
  # Temp arrays should still be properly deleted
  # Input: nothing
  # Output: reg0 = party_id of the temp array
  ("warp_temp_array_create",[
    (spawn_around_party,"p_main_party","pt_warp_temp_array"),
    (party_set_ai_behavior,reg0, ai_bhvr_hold),
    # Debug info, translation not needed
    (assign,":tmp",reg1),(store_current_hours,reg1),(party_set_name,reg0,"@warp_temp_array created at {reg1}"),(assign,reg1,":tmp"),
  ]),


  # script_warp_array_delete
  # Deletes an array. Always delete the arrays after use, or junk parties will populate your savegames.
  # Input: arg1 = array_id
  # Output: nothing
  ("warp_array_delete",[
    (store_script_param, ":array_id", 1),

    (party_get_template_id, ":template", ":array_id"),
    (try_begin),
      (this_or_next|eq,":template","pt_warp_array"),
                   (eq,":template","pt_warp_temp_array"),
      (neq,":array_id","$warp_quick_array"),
     #(remove_party,":array_id"),
      (call_script,"script_safe_remove_party",":array_id"),
    (try_end),
  ]),

  # script_warp_get_quick_array
  # Returns, creating if necessary, the global quick array. Also clears it so it can be used right away.
  # QUICK ARRAY USE INSTRUCTIONS:
  # - The quick array is just a global array meant to be used locally. While it saves the overhead of creating a new array and the troubles of making sure
  #   it gets deleted after use, the usual array operations won't be quicker than on other arrays.
  #   So the quick stands mainly for 'quick use', not for 'quicker operations'.
  # - Always call this function to retrieve it at the script using it, as using the global var directly will cause trouble with older saves.
  # - As a rule of thumb, only use the quick array on blocks of code that don't call other scripts, as they could also be using the quick array,
  #   or could be using it on the future if their implementation changes. Within that code block opcodes and WARP scripts are fine.
  # - If those conditions are met, using the quick array can prevent a lot of party spawning/removal, so a liberal use of it can be made.
  # - Also, no deletion of the quick array after use is needed. In fact, while using the script_warp_array_delete function on it is harmless,
  #   deleting the party storing the quick array by other means will very probably lead to game crashes, so don't do it.
  # Input: nothing
  # Output: reg0 and $warp_quick_array = party_id of the quick array. Don't thinker with the $warp_quick_array value.
  ("warp_get_quick_array",[
    (try_begin),
      (eq,"$warp_quick_array",0),
      (call_script,"script_warp_array_create"), # Creates a permanent array. Oh, the irony.
      (assign,"$warp_quick_array",reg0),
    (else_try),
      (assign,reg0,"$warp_quick_array"),
      (party_set_slot,reg0, 0, 0), # Clears the array
    (try_end),
  ]),


  # script_warp_array_clear
  # Clears an array by setting its length to zero
  # Input: arg1 = array_id
  # Output: nothing
  ("warp_array_clear",
  [ (store_script_param, ":array_id", 1),
    (party_set_slot, ":array_id", 0, 0),
  ]),

  # script_warp_array_length
  # Returns the length of an array
  # Input: arg1 = array_id
  # Output: reg0 = length
  ("warp_array_length",
  [ (store_script_param, ":array_id", 1),
    (party_get_slot, reg0, ":array_id", 0),
  ]),  

  # script_warp_array_init_value
  # Fills the array with (arg2) repetitions of (arg3)
  # Input: arg1 = array_id
  #        arg2 = length
  #        arg3 = value
  # Output: nothing
  ("warp_array_init_value",
  [ (store_script_param, ":array_id", 1),
    (store_script_param, ":length", 2),
    (store_script_param, ":value", 3),
	
    (party_set_slot, ":array_id", 0, ":length"),
    (val_add, ":length", 1),
    (try_for_range, ":i", 1, ":length"), 
        (party_set_slot, ":array_id", ":i", ":value"),
    (try_end),
  ]),  
  
  # script_warp_array_init_range
  # Fills the array with the numbers/IDs from (arg2) to (arg3)
  # Input: arg1 = array_id
  #        arg2 = first
  #        arg2 = end
  # Output: nothing
  ("warp_array_init_range",
  [ (store_script_param, ":array_id", 1),
    (store_script_param, ":first", 2),
    (store_script_param, ":end", 3),
	
    (assign, ":slot", 0),
    (try_for_range, ":i", ":first", ":end"), 
        (val_add, ":slot", 1),
        (party_set_slot, ":array_id", ":slot", ":i"),
    (try_end),
    (party_set_slot, ":array_id", 0, ":slot"),
  ]),  
  
  # script_warp_array_init_random
  # Fills the array with (arg2) random numbers in the range between (arg3) and (arg4)
  # Input: arg1 = array_id
  #        arg2 = length
  #        arg3 = min_value
  #        arg4 = max_value
  # Output: nothing
  ("warp_array_init_random",
  [ (store_script_param, ":array_id", 1),
    (store_script_param, ":length", 2),
    (store_script_param, ":min", 3),
    (store_script_param, ":max", 4),
	
    (party_set_slot, ":array_id", 0, ":length"),
        (val_add, ":length", 1),
    (try_for_range, ":i", 1, ":length"), 
        (store_random_in_range, ":value", ":min", ":max"),
        (party_set_slot, ":array_id", ":i", ":value"),
    (try_end),
  ]),  
  
  # script_warp_array_push
  # Appends an element to an array
  # Input: arg1 = array_id
  #        arg2 = element
  # Output: nothing
  ("warp_array_push",
  [ (store_script_param, ":array_id", 1),
    (store_script_param, ":element", 2),
	
    (party_get_slot, ":length", ":array_id", 0),
    (val_add, ":length", 1),
    (party_set_slot, ":array_id", ":length", ":element"),
    (party_set_slot, ":array_id", 0, ":length"),
  ]),
  
  # script_cf_warp_array_pop
  # Removes the last element and writes it to reg0
  # Fails if the array is empty
  # Input: arg1 = array_id
  # Output: reg0 = popped element
  ("cf_warp_array_pop",
  [ (store_script_param, ":array_id", 1),
	
    (party_get_slot, ":length", ":array_id", 0),
    (gt, ":length", 0),
    (party_get_slot, reg0, ":array_id", ":length"),
    (val_sub, ":length", 1),
    (party_set_slot, ":array_id", 0, ":length"),
  ]),
  
  # script_warp_array_remove_last
  # Removes the last element if it exists
  # Input: arg1 = array_id
  # Output: nothing
  ("warp_array_remove_last",
  [ (store_script_param, ":array_id", 1),
	
    (party_get_slot, ":length", ":array_id", 0),
    (val_sub, ":length", 1),
    (val_max, ":length", 0),
    (party_set_slot, ":array_id", 0, ":length"),
  ]),
  
  # script_cf_warp_array_last
  # Writes the last element to reg0
  # Fails if the array is empty
  # Input: arg1 = array_id
  # Output: reg0 = last element
  ("cf_warp_array_last",
  [ (store_script_param, ":array_id", 1),
	
    (party_get_slot, ":length", ":array_id", 0),
    (gt, ":length", 0),
    (party_get_slot, reg0, ":array_id", ":length"),
  ]),
  
  # script_cf_warp_array_set
  # Sets the (arg2)th element to (arg3)
  # Fails if the array is too small
  # Input: arg1 = array_id
  #        arg2 = index
  #        arg3 = value
  # Output: nothing
  ("cf_warp_array_set",
  [ (store_script_param, ":array_id", 1),
    (store_script_param, ":index", 2),
    (store_script_param, ":value", 3),
	
    (gt, ":index", 0),
    (store_sub, ":index-1", ":index", 1),
    (party_slot_ge, ":array_id", 0, ":index-1"),
    (try_begin),
        (party_slot_eq, ":array_id", 0, ":index-1"),
        (party_set_slot, ":array_id", 0, ":index"),
    (try_end),
    (party_set_slot, ":array_id", ":index", ":value"),
  ]),
  
  # script_cf_warp_array_get
  # Writes the (arg2)ths element to reg0
  # Fails if the index is out of bounds
  # Input: arg1 = array_id
  #        arg2 = index
  # Output: reg0 = value
  ("cf_warp_array_get",
  [ (store_script_param, ":array_id", 1),
    (store_script_param, ":index", 2),
	
    (gt, ":index", 0),
    (party_slot_ge, ":array_id", 0, ":index"),
    (party_get_slot, reg0, ":array_id", ":index"),
  ]),
  
  # script_warp_array_copy
  # Copies array 1 from array 2
  # Input: arg1 = dest_array
  #        arg2 = src_array
  # Output: nothing
  ("warp_array_copy",
  [ (store_script_param, ":dest_array", 1),
    (store_script_param, ":src_array", 2),
    
    (party_get_slot, ":length", ":src_array", 0),
    (party_set_slot, ":dest_array", 0, ":length"),
    (val_add, ":length", 1),
    (try_for_range, ":i", 1, ":length"), 
        (party_get_slot, ":v", ":src_array", ":i"),
        (party_set_slot, ":dest_array", ":i", ":v"),
    (try_end),
  ]),
    
  # script_cf_warp_array_copy_range
  # Copies the subrange (arg2)..(arg3) from array 1 to array 2
  # Input: arg1 = dest_array
  #        arg2 = src_array
  #        arg3 = first
  #        arg4 = end
  #        
  # Output: nothing
  ("cf_warp_array_copy_range",
  [ (store_script_param, ":dest_array", 1),
    (store_script_param, ":src_array", 4),
    (store_script_param, ":first", 2),
    (store_script_param, ":end", 3),
	
    (store_sub,":last",":end",1),
    (party_slot_ge, ":src_array",0,":last"), # Is the source array long enough?
    (assign, ":j", 0),
    (try_for_range, ":i", ":first", ":end"), 
        (val_add,":j",1), # count the elements written
        (party_get_slot, ":v", ":src_array", ":i"),
        (party_set_slot, ":dest_array", ":j", ":v"),
    (try_end),
    (party_set_slot, ":dest_array", 0, ":j"),
  ]),
  
  # script_warp_array_reverse
  # Reverses the array in place
  # Input: arg1 = array_id
  # Output: nothing
  ("warp_array_reverse",
  [ (store_script_param, ":array_id", 1),
	
    (party_get_slot, ":last", ":array_id", 0),
    (try_for_range, ":i", 1, ":last"), 
        (gt,":last",":i"), # otherwise, we're done
        (party_get_slot, ":v1", ":array_id", ":i"),
        (party_get_slot, ":v2", ":array_id", ":last"),
        (party_set_slot, ":array_id", ":i", ":v2"),
        (party_set_slot, ":array_id", ":last", ":v1"),
        (val_sub,":last",1),
    (try_end),
  ]),
  
  # script_warp_array_filter
  # Removes all elements that fail the check of cf_filter
  # Input: arg1 = array_id
  #        arg2 = cf_filter
  # Output: nothing
  ("warp_array_filter",
  [ (store_script_param, ":array_id", 1),
    (store_script_param, ":cf_filter", 2),

    (party_get_slot, ":end", ":array_id", 0),
    (val_add, ":end", 1),
    (assign, ":matches", 0),
    (try_for_range, ":i", 1, ":end"), 
        (party_get_slot, ":ce", ":array_id", ":i"),
        (call_script,":cf_filter",":ce"),
        (val_add,":matches",1),
        (gt,":i",":matches"),
        (party_set_slot, ":array_id", ":matches", ":ce"),
    (try_end),
    (party_set_slot, ":array_id", 0, ":matches"),
  ]),
  
  # script_warp_array_map
  # Applies a mapping function (p1->reg0) to every element and writes the result in its place
  # Elements are removed if the mapping function fails
  # Input: arg1 = array_id
  #        arg2 = cf_map
  # Output: nothing
  ("warp_array_map",
  [ (store_script_param, ":array_id", 1),
    (store_script_param, ":cf_map", 2),
	
    (party_get_slot, ":end", ":array_id", 0),
    (val_add, ":end", 1),
    (assign, ":matches", 0),
    (try_for_range, ":i", 1, ":end"), 
        (party_get_slot, ":ce", ":array_id", ":i"),
        (call_script,":cf_map",":ce"),
        (val_add,":matches",1),
        (party_set_slot, ":array_id", ":matches", reg0),
    (try_end),
    (party_set_slot, ":array_id", 0, ":matches"),
  ]),
  
  # script_warp_array_unique
  # Makes sure the array contains each element only once
  # Input: arg1 = array_id
  # Output: nothing
  ("warp_array_unique",
  [ (store_script_param, ":array_id", 1),
	
    (party_get_slot, ":end", ":array_id", 0),
    (val_add, ":end", 1),
    (assign, ":unique", 0),
    (try_for_range, ":i", 1, ":end"), 
        (party_get_slot, ":ce", ":array_id", ":i"),
        (assign,":found",0),
        (try_for_range, ":j", 1, ":i"),
            (party_slot_eq, ":array_id", ":j", ":ce"),
            (assign,":found",1),
            (assign,":j",":i"),
        (try_end),
        (eq,":found",0),
        (val_add,":unique",1),
        (gt,":i",":unique"),
        (party_set_slot, ":array_id", ":unique", ":ce"),
    (try_end),
    (party_set_slot, ":array_id", 0, ":unique"),
  ]),

  # script_warp_array_sort
  # Sorts the array using natural merge sort and a function cf_order(a,b) that fails iff a,b is the wrong order
  # Input: arg1 = array_id
  #        arg2 = cf_order
  # Output: nothing
  ("warp_array_sort",
  [ (store_script_param, ":array_id", 1),
    (store_script_param, ":cf_order", 2),
	
    (party_get_slot, ":end", ":array_id", 0),
    (try_begin),
      (gt,":end",0),
      (val_add, ":end", 1),
      (call_script,"script_warp_temp_array_create"),
      (assign,":temp_array",reg0),
  
      (call_script,"script_warp_array_sort_range_aux",":array_id",":temp_array",1,":end",":cf_order"),
      (try_begin),
          (eq,reg0,":temp_array"),
          (try_for_range, ":i", 1, ":end"),
              (party_get_slot, ":v", ":temp_array", ":i"),
              (party_set_slot, ":array_id", ":i", ":v"),
          (try_end),
      (try_end),
  
      (call_script,"script_warp_array_delete",":temp_array"),
    (try_end),
  ]),
  
  # script_warp_array_sort_range
  # Sorts only a subrange of the array; otherwise same as "script_warp_array_sort"
  # Input: arg1 = array_id
  #        arg2 = first
  #        arg3 = end
  #        arg4 = cf_order
  # Output: nothing
  ("warp_array_sort_range",
  [ (store_script_param, ":array_id", 1),
    (store_script_param, ":first", 2),
    (store_script_param, ":end", 3),
    (store_script_param, ":cf_order", 4),

	
    (party_get_slot, ":length", ":array_id", 0),
    (try_begin),
      (gt,":length",0), # Range checks, we don't want to leave created arrays behind
      (gt,":first",0),
      (le,":end",":length"),
      (lt,":first",":end"),

      (call_script,"script_warp_temp_array_create"),
      (assign,":temp_array",reg0),
  
      (call_script,"script_warp_array_sort_range_aux",":array_id",":temp_array",":first",":end",":cf_order"),
      (try_begin),
          (eq,reg0,":temp_array"),
          (try_for_range, ":i", ":first", ":end"),
              (party_get_slot, ":v", ":temp_array", ":i"),
              (party_set_slot, ":array_id", ":i", ":v"),
          (try_end),
      (try_end),

      (call_script,"script_warp_array_delete",":temp_array"),
    (try_end),
  ]),
  
  # Auxiliary function; recursively performs one round of mergesort from array_1 to array_2 and writes the sorted array_id to reg0 when done
  ("warp_array_sort_range_aux",
  [ (store_script_param, ":array_1", 1),
    (store_script_param, ":array_2", 2),
    (store_script_param, ":first", 3),
    (store_script_param, ":end", 4),
    (store_script_param, ":cf_order", 5),
	
    (assign,":p1",1),
    (assign,":p2",-1),
    (assign,":sorted",1),

    (store_add, ":second", ":first", 1),
    (store_sub, ":last", ":end", 1),
    (try_for_range, ":i", ":second", ":last"),
        (store_sub, ":i-1", ":i", 1),
        (party_get_slot, ":val_a", ":array_1", ":i-1"),
        (party_get_slot, ":val_b", ":array_1", ":i"),
        (try_begin),
            (call_script,":cf_order", ":val_a", ":val_b"),
        (else_try), # Check failed -> wrong order!
            (assign,":sorted",0),
            (try_begin),
                (le,":p2",0),
                (assign,":p2",":i"),
            (else_try),
                (call_script,"script_warp_array_merge_range_aux",":array_1",":array_2",":p1",":p2",":i",":cf_order"),
                (assign,":p1",":i"),
                (assign,":p2",-1),
            (try_end),
        (try_end),
    (try_end),
        (try_begin), # Merge last two runs (if there are)
            (gt,":p2",0),
            (lt,":p2",":end"),
            (call_script,"script_warp_array_merge_range_aux",":array_1",":array_2",":p1",":p2",":end",":cf_order"),
        (else_try), # Or copy the last run (if necessary)
            (lt,":p1",":end"),
            (eq,":sorted",0), # otherwise, just return array_1
            (try_for_range, ":i", ":p1", ":end"),
                (party_get_slot, ":v", ":array_1", ":i"),
                (party_set_slot, ":array_2", ":i", ":v"),
            (try_end),
        (try_end),
        (try_begin),
            (eq,":sorted",1), # Am I done yet?
            (assign,reg0,":array_1"),
        (else_try),
            (call_script,"script_warp_array_sort_range_aux",":array_2",":array_1",":first",":end",":cf_order"),
        (try_end),
    #(try_end),
  ]),  
  ("warp_array_merge_range_aux",
  [ (store_script_param, ":array_1", 1),
    (store_script_param, ":array_2", 2),
    (store_script_param, ":pos1", 3),
    (store_script_param, ":pos2", 4),
    (store_script_param, ":pos3", 5),
    (store_script_param, ":cf_order", 6),
	
    (assign,":c1",":pos1"),
    (assign,":c2",":pos2"),
	
    (try_for_range, ":i", ":pos1", ":pos3"), 
        (try_begin),
            (eq,":c1",":pos2"),
            (party_get_slot, ":v", ":array_1", ":c2"),
            (party_set_slot, ":array_2", ":i", ":v"),
            (val_add,":c2",1),
        (else_try),
            (eq,":c2",":pos3"),
            (party_get_slot, ":v", ":array_1", ":c1"),
            (party_set_slot, ":array_2", ":i", ":v"),
            (val_add,":c1",1),
        (else_try),
            (party_get_slot, ":val_a", ":array_1", ":c1"),
            (party_get_slot, ":val_b", ":array_1", ":c2"),
            (try_begin),
                (call_script,":cf_order", ":val_a", ":val_b"),
                (party_get_slot, ":v", ":array_1", ":c1"),
                (party_set_slot, ":array_2", ":i", ":v"),
                (val_add,":c1",1),
            (else_try),
                (party_get_slot, ":v", ":array_1", ":c2"),
                (party_set_slot, ":array_2", ":i", ":v"),
                (val_add,":c2",1),
            (try_end),
        (try_end),
    (try_end),
  ]),  
  
  # script_warp_array_shuffle
  # Shuffles the array (puts all elements in random order)
  # Input: arg1 = array_id
  # Output: nothing
  ("warp_array_shuffle",
  [ (store_script_param, ":array_id", 1),
	
    (party_get_slot, ":end", ":array_id", 0),
    (val_add, ":end", 1),
    (call_script,"script_warp_array_shuffle_range",":array_id",1,":end"),
  ]),
  
  # script_warp_array_shuffle_range
  # Shuffles a subrange of the array
  # Input: arg1 = array_id
  #        arg2 = first
  #        arg3 = end
  # Output: nothing
  ("warp_array_shuffle_range",
  [ (store_script_param, ":array_id", 1),
    (store_script_param, ":first", 2),
    (store_script_param, ":end", 3),

    (try_for_range, ":i", ":first", ":end"),
        (store_random_in_range,":j",":i",":end"),
        (neq,":i",":j"),
        (party_get_slot, ":vi", ":array_id", ":i"),
        (party_get_slot, ":vj", ":array_id", ":j"),
        (party_set_slot, ":array_id", ":i", ":vj"),
        (party_set_slot, ":array_id", ":j", ":vi"),
    (try_end),
  ]),

  # script_cf_warp_array_get_random
  # Writes at reg0 a random element of the array, or fails if it's empty
  # Input: arg1 = array_id
  # Output: reg0: a random element of the array
  ("cf_warp_get_random",[
    (store_script_param, ":array_id",1),
    (party_get_slot,":length",":array_id",0),
    (gt,":length",0),
    (store_random_in_range,":rnd",0,":length"),
    (val_add,":rnd",1),
    (party_get_slot,reg0,":array_id",":rnd"),
  ]),

  # script_warp_array_truncate
  # Removes the array elements after a given position.
  # Input: arg1 = array_id
  #        arg2 = position to truncate the array after
  # Output: none
  ("warp_array_truncate", [
    (store_script_param, ":array_id",1),
    (store_script_param, ":pos",2),
    (try_begin),
      (ge,":pos",0),
      (party_get_slot,":length",":array_id",0),
      (try_begin),
        (lt,":pos",":length"),
        (party_set_slot,":array_id",0,":pos"),
      (try_end),
    (else_try),
      (party_set_slot,":array_id",0,0),
    (try_end),
  ]),
  
  # script_warp_print_array
  # Writes an array's content to s3, using a map function and custom separators
  # e.g. (1,4,6,9),"script_warp_roman","@ or ","@ or maybe" -> "I or IV or VI or maybe IX"
  # Input: arg1 = array_id
  # 	   arg2 = script that writes the ID's name to s0 - MUST NOT TOUCH s1, s2 or s3!
  # Set before calling:
  # 	   s1 = middle separator (usually comma or space)
  # 	   s2 = last separator (usually and)
  # Output: s3 = List of strings returned by arg4
  ("warp_print_array",
  [
    (store_script_param, ":array_id", 1),
    (store_script_param, ":script_name", 2),
	
    (party_get_slot, ":array_last", ":array_id", 0),
    (str_clear,s3),
	
    (try_begin),
        (eq,":array_last",1),
        (party_get_slot, ":v", ":array_id", ":array_last"),
        (call_script,":script_name",":v"),
        (str_store_string,s3,"@{s0}"),
    (else_try),
        (ge,":array_last",2),
        (party_get_slot, ":v", ":array_id", 1),
        (call_script,":script_name",":v"),
        (str_store_string,s3,"@{s0}"),
        (try_for_range, ":i", 2, ":array_last"),
            (party_get_slot, ":v", ":array_id", ":i"),
            (call_script,":script_name",":v"),
            (str_store_string,s3,"@{s3}{s1}{s0}"),
        (try_end),
        (party_get_slot, ":v", ":array_id", ":array_last"),
        (call_script,":script_name",":v"),
        (str_store_string,s3,"@{s3}{s2}{s0}"),
    (try_end),
  ]),
  
  # script_warp_print_array_comma
  # Writes an array's content to s1, separated by commas and using a map function
  # e.g. (1,4,6,9),"script_warp_roman" -> "I, IV, VI, IX"
  # Input: arg1 = array_id
  # 	   arg2 = script that writes the ID's name to s0 - MUST NOT TOUCH s1!
  # Output: s1 = List of strings returned by arg4
  ("warp_print_array_comma",
  [ (store_script_param, ":array_id", 1),
    (store_script_param, ":script_name", 2),
	
    (party_get_slot, ":array_last", ":array_id", 0),
    (store_add,":array_end",":array_last",1),
    (str_clear,s1),
	
    (try_begin),
        (eq,":array_last",1),
        (party_get_slot, ":v", ":array_id", ":array_last"),
        (call_script,":script_name",":v"),
        (str_store_string,s1,"@{s0}"),
    (else_try),
        (ge,":array_last",2),
        (party_get_slot, ":v", ":array_id", 1),
        (call_script,":script_name",":v"),
        (str_store_string,s1,"@{s0}"),
        (try_for_range, ":i", 2, ":array_end"),
            (party_get_slot, ":v", ":array_id", ":i"),
            (call_script,":script_name",":v"),
            (str_store_string,s1,"@{s1}, {s0}"),
        (try_end),
    (try_end),
  ]),
  
  # script_warp_print_array_and
  # Writes an array's content to s1, separated by commas, a final "and" and using a map function
  # e.g. (1,4,6,9),"script_warp_roman" -> "I, IV, VI and IX"
  # Input: arg1 = array_id
  # 	   arg2 = script that writes the ID's name to s0 - MUST NOT TOUCH s1!
  # Output: s1 = List of strings returned by arg4
  ("warp_print_array_and",
  [ (store_script_param, ":array_id", 1),
    (store_script_param, ":script_name", 2),
	
    (party_get_slot, ":array_last", ":array_id", 0),
    (str_clear,s1),
	
    (try_begin),
        (eq,":array_last",1),
        (party_get_slot, ":v", ":array_id", ":array_last"),
        (call_script,":script_name",":v"),
        (str_store_string,s1,"@{s0}"),
    (else_try),
        (ge,":array_last",2),
        (party_get_slot, ":v", ":array_id", 1),
        (call_script,":script_name",":v"),
        (str_store_string,s1,"@{s0}"),
        (try_for_range, ":i", 2, ":array_last"),
            (party_get_slot, ":v", ":array_id", ":i"),
            (call_script,":script_name",":v"),
            (str_store_string,s1,"@{s1}, {s0}"),
        (try_end),
        (party_get_slot, ":v", ":array_id", ":array_last"),
        (call_script,":script_name",":v"),
        (str_store_string,s1,"@{s1} and {s0}"),
    (try_end),
  ]),
  
# Part II - Helper Scripts
##########################
  # script_warp_number
  # Takes a number and writes it to s0
  # Input: arg1 = number
  # Output: s0 = number string
  ("warp_number",
  [ (store_script_param, ":number", 1),
    (assign,reg0,":number"),
    (str_store_string,s0,"@{reg0}"),
  ]),

# Printing
  ("warp_troop_name",[(store_script_param, ":troop", 1), (str_store_troop_name, s0, ":troop")]),
  ("warp_party_name",[(store_script_param, ":party", 1), (str_store_party_name, s0, ":party")]),
  ("warp_item_name",[(store_script_param, ":item", 1), (str_store_item_name, s0, ":item")]),
# Some basic sorting functions
  ("cf_ascending",
  [ (store_script_param, ":a", 1),
    (store_script_param, ":b", 2),
    (ge,":b",":a"),
  ]),
  ("cf_descending",
  [ (store_script_param, ":a", 1),
    (store_script_param, ":b", 2),
    (ge,":a",":b"),
  ]),

]