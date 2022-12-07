# -*- coding: utf8 -*-
import copy
import io
import struct
import os
import collections
import sys

class DXGI:
    FORMAT_BC1_TYPELESS = 70
    FORMAT_BC1_UNORM = 71
    FORMAT_BC1_UNORM_SRGB = 72
    FORMAT_BC2_TYPELESS = 73
    FORMAT_BC2_UNORM = 74
    FORMAT_BC2_UNORM_SRGB = 75
    FORMAT_BC3_TYPELESS = 76
    FORMAT_BC3_UNORM = 77
    FORMAT_BC3_UNORM_SRGB = 78
    FORMAT_BC4_TYPELESS = 79
    FORMAT_BC4_UNORM = 80
    FORMAT_BC4_SNORM = 81
    FORMAT_BC5_TYPELESS = 82
    FORMAT_BC5_UNORM = 83
    FORMAT_BC5_SNORM = 84
  
class DDS:
    ALPHA_MODE_PREMULTIPLIED = 2
  
class DDSD:
    PITCH = 0x8
    LINEARSIZE = 0x80000


def load_texture(file_path):
  with open(file_path, 'rb') as f:
    magic = struct.unpack('4s', f.read(4))[0]
    f.seek(0x54)
    fourc = struct.unpack('4s', f.read(4))[0];
    
    assert(magic == b'DDS ')
    
    print (" [-] opening %s" % file_path)
        
    # swy: we couldn't convert it to a valid DX9 format; unchanged, leave it alone
    if fourc == b'DX10':
        print("   [!] seems like a DX10-style DDS format; convert it to a DX9 header and try again.")
        exit(-1)
        
    if (fourc not in [b'DXT1', b'DXT2', b'DXT3', b'DXT4', b'DXT5', b'ATI1', b'ATI2']):
        print("   [!] the", fourc, " DDS type is unsupported; skipping")
        exit(-1)

    # swy: now let's try to fix the pitch/linear size mess; every encoder uses their own combination of flags, screw the standards ¯\_(ツ)_/¯
    #      MSDN says that compressed textures should always use DDSD_LINEARSIZE, because this is an union we find all kinds of things here;
    #      it's either zeroed out, or it actually contains the pitch size or it *even* may be correct, maybe.
    
    #      specially-important for openbrf: https://github.com/Swyter/openbrf/blob/583356dfd0aef4b7d58139ebae22f337d47efc78/bindTexturePatch.h#L165
    
    f.seek(0x8)
    flags           = struct.unpack('<I', f.read(4))[0]
    width           = struct.unpack('<I', f.read(4))[0]
    height          = struct.unpack('<I', f.read(4))[0]
    linear_or_pitch = struct.unpack('<I', f.read(4))[0]
    depth           = struct.unpack('<I', f.read(4))[0]
    mipmap_count    = struct.unpack('<I', f.read(4))[0]
    
    # swy: all the other formats use 16 bytes per 4x4 pixel block; only those two are 8 bytes
    block_size      = (fourc in [b'DXT1', b'ATI1']) and 8 or 16
    
    linearsize = int(int(width    + 3) / 4) * \
                 int(int(height   + 3) / 4) * \
                 int(block_size)
                 
    pitchsize  = int(int(width    + 3) / 4) * \
                 int(block_size)
                 
    # swy: read the entire thing; from beginning to end
    f.seek(0x0)
    data = f.read(-1)

    tx = {}
    tx['width']   = width
    tx['height']  = height
    tx['mipmaps'] = mipmap_count
    tx['fourcc']  = fourc
    tx['blocksz'] = block_size
    tx['linsz']   = linearsize
    tx['pitchsz'] = pitchsize
    tx['data']    = bytearray(data) # https://stackoverflow.com/a/1934649/674685
    
    return tx


if len(sys.argv) < 3:
    print("usage: source.dds output.dds")
    print("       (keep in mind that the resolution and number of mipmaps must match)")
    exit(-2)

src = sys.argv[1] # '/home/swyter/.local/share/Steam/steamapps/common/MountBlade Warband/_renderdoc_dumped_tld_interface_corrupted_text.dds'
dst = sys.argv[2] # src + '_flipped.dds'

src_t = load_texture(src)

# print(src_opq_t, src_tra_t)

# swy: use the transparent texture as base; as it always has to be either DXT3 or DXT5,
#      so it's a good template. if the mips didn't match it would be strange.
dst_fin_t = copy.deepcopy(src_t) # swy: i was getting mirrored images because i was writing in a mirrored copy of src_t by mistake; make dst_fin_t have its own buffer/copy of the data. lost a lot of time thanks to this :)

offset_src = 0x80 # swy: end of the DDS header, start of the actual data
offset_dst = offset_src

cur_width  = dst_fin_t['width']
cur_height = dst_fin_t['height']

# for i, mip in enumerate(dst_t.mipmaps):
for mip in range(dst_fin_t['mipmaps']):

    no_of_blocks_in_mip = int(int(cur_width  + 3) / 4) * \
                          int(int(cur_height + 3) / 4)

    if no_of_blocks_in_mip <= 0:
        break

    no_of_bytes_in_mip = no_of_blocks_in_mip * dst_fin_t['blocksz']

    #dst_fin_t['data'][offset_dst:offset_dst + dst_fin_t['linsz']] = b'0'

    no_of_blocks_in_stride = int(int(cur_width + 3) / 4)
    no_of_bytes_in_stride = no_of_blocks_in_stride * dst_fin_t['blocksz']
    no_of_total_strides = no_of_bytes_in_mip // no_of_bytes_in_stride

    offset_dst += no_of_bytes_in_mip
    
    for stride in range(no_of_total_strides + 1):

        # swy: copy the DXT1/3/5 opaque block over the original one in the opaque+transparent DXT3/5 block
        #      DXT1   ->                          OO OO OO OO OO OO OO OO ( 8 bytes)
        #      DXT3,5 ->  AA AA AA AA AA AA AA AA OO OO OO OO OO OO OO OO (16 bytes)
        dst_fin_t['data'][offset_dst:offset_dst + no_of_bytes_in_stride] = src_t['data'][offset_src:offset_src + no_of_bytes_in_stride]

        print(stride, hex(offset_dst), hex(offset_src), src_t['data'][offset_src:offset_src + 6])
        
        offset_src += no_of_bytes_in_stride
        offset_dst -= no_of_bytes_in_stride


    for block in range(no_of_blocks_in_mip):
        cur_offset = 0x80 + (block * 16)
        block_data = dst_fin_t['data'][cur_offset:cur_offset + 16]
        block_data_src = copy.deepcopy(block_data)


        # swy: reordering the BC3/DXT5 indices is a bit more involved than what one would expect, each palette index has 3 bits, so there are 4 of them every three 4-bit nibbles
        #      as we don't need to swap the bits in the same row we don't need to edit the nibbles themselves, the bitflag struct field ordering makes this a bit of a chore

        # ____ ____/\____ ____/\____
        # 111
        #    2 22
        #        33  3
        #             444
        #                 555
        #                    6  66
        #                         77

        # DE 13  1C 91 C9 1C 91 C9 (swy: example 1, maybe wrong, but we can see how the patterns move around without changing the nibbles themselves)
        # DE 13  99 CC 11 9C CC 11

        # FF FF  12 34 56 78 9A BC (swy: example 2, manually set the nibbles to be incremental and moved the indices around in the 010 editor template to get the thing below)
        # FF FF  C9 8B A7 63 25 41

        def top_nibble(val):
            return (val & 0xF0) >> 4
        def bot_nibble(val):
            return (val & 0x0F) >> 0

        def get_nibble(val):
            return (top_nibble(val), bot_nibble(val))

        _1, _2 = get_nibble(block_data[2])
        _3, _4 = get_nibble(block_data[3])
        _5, _6 = get_nibble(block_data[4])
        _7, _8 = get_nibble(block_data[5])
        _9, _A = get_nibble(block_data[6])
        _B, _C = get_nibble(block_data[7])
        
        def comp_byte_from_nibbles(top, bot):
            return (top << 4) | (bot << 0)

        block_data[2] = comp_byte_from_nibbles(_C, _9)
        block_data[3] = comp_byte_from_nibbles(_8, _B)
        block_data[4] = comp_byte_from_nibbles(_A, _7)
        block_data[5] = comp_byte_from_nibbles(_6, _3)
        block_data[6] = comp_byte_from_nibbles(_2, _5)
        block_data[7] = comp_byte_from_nibbles(_4, _1)


        # swy: as for BC1/DXT1, vertically-swapping the indices is way easier because there are four texel indices in each byte; four rows, rows and bytes line up
        block_data[12] = block_data_src[15]
        block_data[13] = block_data_src[14]
        block_data[14] = block_data_src[13]
        block_data[15] = block_data_src[12]

        # swy: replace the whole block with the modified copy
        dst_fin_t['data'][cur_offset:cur_offset + 16] = block_data

    cur_width /= 2; cur_height /= 2

# swy: done; save the thing
with open(dst, 'wb') as f:
    print (" [+] opening %s for writing" % dst)
    f.write(dst_fin_t['data'])
