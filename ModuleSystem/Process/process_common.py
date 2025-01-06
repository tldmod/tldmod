import string
import types

from module_info import wb_compile_switch as is_wb

def convert_to_identifier(s0):
  s1 = s0.replace(" ","_")
  s2 = s1.replace("'","_")
  s3 = s2.replace("`","_")
  s4 = s3.replace("(","_")
  s5 = s4.replace(")","_")
  s6 = s5.replace("-","_")
  s7 = s6.replace(",","")
  s8 = s7.replace("|","")
  s9 = s8.lower()
  return s9

def convert_to_identifier_with_no_lowercase(s0):
  s1 = s0.replace(" ","_")
  s2 = s1.replace("'","_")
  s3 = s2.replace("`","_")
  s4 = s3.replace("(","_")
  s5 = s4.replace(")","_")
  s6 = s5.replace("-","_")
  s7 = s6.replace(",","")
  s8 = s7.replace("|","")
  return s8

def replace_spaces(s0):
  return s0.replace(" ","_")

   
def sf(input):
    try:
        int(float(input))
    except ValueError:
        return input
    
    """
    --swyter. build msys with short floats
    """
    #print("after:"+str(input))
    input=str("%.11f" % input)
    
    '''
    fixes a bug in scenes.txt, otherwise it munches the non-decimal zeroes,
    leaving the player potentiall trapped into a teensy tiny space :(
    '''
    if ("." in input):
     input=input.rstrip('0').rstrip(".")
    #if (input[-1]=="."):
    # input+="0"
    if (input==""):
     input="0"
    #print("befor:"+input)
    return input

# swy: InVain noticed that the {!} string prefix to ignore translations was added on Warband, and on M&B 1.011 it shows an "Unrecognized token"
#      entry, so turn it into the supported {***} untranslated string marker to make sure it gets ignored.
def remove_exclamation_marker_on_mb1011(input):
    if not is_wb:
        return input.replace("{!}", "{***}")
    else:
        return input