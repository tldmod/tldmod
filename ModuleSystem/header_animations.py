arf_blend_in_0               = 0x00000001
arf_blend_in_1               = 0x00000002
arf_blend_in_2               = 0x00000003
arf_blend_in_3               = 0x00000004
arf_blend_in_4               = 0x00000005
arf_blend_in_5               = 0x00000006
arf_blend_in_6               = 0x00000007
arf_blend_in_7               = 0x00000008
arf_blend_in_8               = 0x00000009
arf_blend_in_9               = 0x0000000a
arf_blend_in_10              = 0x0000000b
arf_blend_in_11              = 0x0000000c
arf_blend_in_12              = 0x0000000d
arf_blend_in_13              = 0x0000000e
arf_blend_in_14              = 0x0000000f
arf_blend_in_15              = 0x00000010
arf_blend_in_16              = 0x00000011
arf_blend_in_17              = 0x00000012
arf_blend_in_18              = 0x00000013
arf_blend_in_19              = 0x00000014
arf_blend_in_20              = 0x00000015
arf_blend_in_21              = 0x00000016
arf_blend_in_22              = 0x00000017
arf_blend_in_23              = 0x00000018
arf_blend_in_24              = 0x00000019
arf_blend_in_25              = 0x0000001a
arf_blend_in_26              = 0x0000001b
arf_blend_in_27              = 0x0000001c
arf_blend_in_28              = 0x0000001d
arf_blend_in_29              = 0x0000001e
arf_blend_in_30              = 0x0000001f
arf_blend_in_31              = 0x00000020
arf_blend_in_32              = 0x00000021
arf_blend_in_48              = 0x00000031
arf_blend_in_64              = 0x00000041
arf_blend_in_128             = 0x00000081
arf_blend_in_254             = 0x000000ff

arf_make_walk_sound          = 0x00000100
arf_make_custom_sound        = 0x00000200

##arf_start_pos_0               = 0x00000100
##arf_end_pos_0                 = 0x00000200
##arf_start_pos_0_25            = 0x00000400
##arf_end_pos_0_25              = 0x00000800
##arf_start_pos_0_5             = 0x00001000
##arf_end_pos_0_5               = 0x00002000
##arf_start_pos_0_75            = 0x00004000
##arf_end_pos_0_75              = 0x00008000

##arf_loop_pos_0     = arf_start_pos_0    | arf_end_pos_0
##arf_loop_pos_0_25  = arf_start_pos_0_25 | arf_end_pos_0_25
##arf_loop_pos_0_5   = arf_start_pos_0_5  | arf_end_pos_0_5
##arf_loop_pos_0_75  = arf_start_pos_0_75 | arf_end_pos_0_75

##arf_phase_even               = 0x00010000
##arf_phase_odd                = 0x00030000
##arf_phase_inverse_even       = 0x00050000
##arf_phase_inverse_odd        = 0x00070000
arf_two_handed_blade         = 0x01000000
arf_lancer                   = 0x02000000
arf_cyclic                   = 0x10000000

arf_use_walk_progress        = 0x20000000
arf_use_stand_progress       = 0x40000000
arf_use_inv_walk_progress    = 0x80000000

##arf_walk = arf_phase_even | arf_cyclic

#-----------------------------------------

acf_synch_with_horse         = 0x00000001
acf_align_with_ground        = 0x00000002
acf_enforce_lowerbody        = 0x00000100
acf_enforce_rightside        = 0x00000200
acf_enforce_all              = 0x00000400
acf_parallels_for_look_slope = 0x00001000
acf_rotate_body              = 0x00002000
acf_displace_position        = 0x00004000
acf_ignore_slope             = 0x00008000
acf_thrust                   = 0x00010000
acf_right_cut                = 0x00020000
acf_left_cut                 = 0x00040000
acf_overswing                = 0x00080000
acf_lock_camera              = 0x00100000
acf_anim_length_mask         = 0xff000000

acf_anim_length_bits         = 24
def acf_anim_length(x):
  return (x << acf_anim_length_bits) & acf_anim_length_mask
#------------------------------------------



#### Do not edit these lines

def get_byte(f):
  if f == 0.0:
    return 0
  i = int(f * 255.0)
  if (i< 1):
    i=1
  elif (i > 255):
    i = 255
  return i

def pack2f(a,b):
  ai = get_byte(a)
  bi = get_byte(b)
  return ((bi << 8) | ai)

def pack4f(a,b,c,d):
  ai = get_byte(a)
  bi = get_byte(b)
  ci = get_byte(c)
  di = get_byte(d)
  return ((di << 24) | (ci << 16) | (bi << 8) | ai)
