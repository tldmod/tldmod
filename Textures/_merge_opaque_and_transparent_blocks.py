import io
import struct
import os
import collections
import sys

from pathlib import Path

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


if len(sys.argv) < 4:
    print("usage: source_opaque.dds source_transparent.dds output_combined.dds")
    print("       (keep in mind that the resolution and number of mipmaps must match)")
    exit(-2)

src_opq = sys.argv[1]
src_tra = sys.argv[2]
dst     = sys.argv[3]

src_opq_t = load_texture(src_opq)
src_tra_t = load_texture(src_tra)

# print(src_opq_t, src_tra_t)

if src_opq_t['width']   != src_tra_t['width']:
    print("   [i] the width doesn't match.")
    exit(1)

if src_opq_t['height']  != src_tra_t['height']:
    print("   [i] the height doesn't match.")
    exit(1)

if src_opq_t['mipmaps'] != src_tra_t['mipmaps']:
    print("   [i] the amount of mipmaps doesn't match.")
    exit(1)

# swy: use the transparent texture as base; as it always has to be either DXT3 or DXT5,
#      so it's a good template. if the mips didn't match it would be strange.
dst_fin_t = src_tra_t

offset_src = 0x80 # swy: end of the DDS header, start of the actual data
offset_dst = offset_src

# swy: the transparent part (if any) goes first; skip it
if src_opq_t['blocksz'] == 16: offset_src += 8
if dst_fin_t['blocksz'] == 16: offset_dst += 8

cur_width  = dst_fin_t['width']
cur_height = dst_fin_t['height']

# for i, mip in enumerate(dst_t.mipmaps):
for mip in range(dst_fin_t['mipmaps']):

    no_of_blocks_in_mip = int(int(cur_width  + 3) / 4) * \
                          int(int(cur_height + 3) / 4)
                          
    cur_width /= 2; cur_height /= 2

    for block in range(no_of_blocks_in_mip):

        # swy: copy the DXT1/3/5 opaque block over the original one in the opaque+transparent DXT3/5 block
        #      DXT1   ->                          OO OO OO OO OO OO OO OO ( 8 bytes)
        #      DXT3,5 ->  AA AA AA AA AA AA AA AA OO OO OO OO OO OO OO OO (16 bytes)
        dst_fin_t['data'][offset_dst:offset_dst + 8] = src_opq_t['data'][offset_src:offset_src + 8]
        
        offset_src += src_opq_t['blocksz']
        offset_dst += dst_fin_t['blocksz']

# swy: done; save the thing
with open(dst, 'wb') as f:
    print (" [+] opening %s for writing" % dst)
    f.write(dst_fin_t['data'])
