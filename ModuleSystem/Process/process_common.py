import string
import types

def convert_to_identifier(s0):
  s1 = string.replace(s0," ","_")
  s2 = string.replace(s1,"'","_")
  s3 = string.replace(s2,"`","_")
  s4 = string.replace(s3,"(","_")
  s5 = string.replace(s4,")","_")
  s6 = string.replace(s5,"-","_")
  s7 = string.replace(s6,",","")
  s8 = string.replace(s7,"|","")
  s9 = string.lower(s8)
  return s9

def convert_to_identifier_with_no_lowercase(s0):
  s1 = string.replace(s0," ","_")
  s2 = string.replace(s1,"'","_")
  s3 = string.replace(s2,"`","_")
  s4 = string.replace(s3,"(","_")
  s5 = string.replace(s4,")","_")
  s6 = string.replace(s5,"-","_")
  s7 = string.replace(s6,",","")
  s8 = string.replace(s7,"|","")
  return s8

def replace_spaces(s0):
  return string.replace(s0," ","_")

def sf(input):
    """
    --swyter. build msys with short floats
    """
    #print("after:"+str(input))
    input=str(input)
    
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