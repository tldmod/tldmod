import io
import struct
import os
import collections

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
  
with open('CWE_AppleTreeLeaves_1.dds', 'rb+') as f:
    print(f)
    magic = struct.unpack('4s', f.read(4))[0]
    f.seek(0x54)
    fourc = struct.unpack('4s', f.read(4))[0];
    
    print("magic", (magic), magic == b'DDS ', fourc, len(fourc[:4]), len(b'DX10'), fourc[:4] == b'DX10')

    # swy: first things first, try to convert a newer DirectX 10-style (expanded) header to a DirectX 9, as they contain the same data
    #      so that the game and OpenBRF can actually open and read it. we should be able to map them without much fuss.
    if fourc == b"DX10":
        print("wut")
    
        f.seek(0x80) # dxgiFormat
        dxgi = struct.unpack('<I', f.read(4))[0]
        
        f.seek(0x90) # miscFlags2
        alph = struct.unpack('<I', f.read(4))[0]
        
        oldf = False
        
        if dxgi in [ \
        DXGI.FORMAT_BC1_UNORM, \
        DXGI.FORMAT_BC1_UNORM_SRGB, \
        DXGI.FORMAT_BC1_TYPELESS]:
            oldf = b'DXT1'
        
        if dxgi in [ \
        DXGI.FORMAT_BC2_UNORM, \
        DXGI.FORMAT_BC2_UNORM_SRGB, \
        DXGI.FORMAT_BC2_TYPELESS ]:
        
            if alph == DDS.ALPHA_MODE_PREMULTIPLIED:
                oldf = b'DXT2'
            else:
                oldf = b'DXT3'

        if dxgi in [ \
        DXGI.FORMAT_BC3_UNORM, \
        DXGI.FORMAT_BC3_UNORM_SRGB, \
        DXGI.FORMAT_BC3_TYPELESS ]:
        
            if alph == DDS.ALPHA_MODE_PREMULTIPLIED:
                oldf = b'DXT4'
            else:
                oldf = b'DXT5'
        
        if dxgi in [ \
        DXGI.FORMAT_BC4_UNORM, \
        DXGI.FORMAT_BC4_SNORM, \
        DXGI.FORMAT_BC4_TYPELESS ]:
            oldf = b'ATI1'

        if dxgi in [ \
        DXGI.FORMAT_BC5_UNORM, \
        DXGI.FORMAT_BC5_SNORM, \
        DXGI.FORMAT_BC5_TYPELESS]:
            oldf = b'ATI2'
            
            
        print("oldf", oldf, fourc)
        if oldf:
            f.seek(os.SEEK_END); total_size = f.tell()
            
            print("fixo", alph, dxgi, oldf, total_size);
            
            # swy: replace that DX10 tag by the actual thing
            f.seek(0x54) # fourCC
            f.write(oldf)
            
            # swy: get rid of the extended header; move the data back and truncate the difference
            f.seek(0x80 + 0x14) # 0x94
            block_data = f.read(-1)
            f.seek(0x80)
            f.write(block_data)
            f.truncate() #total_size - 0x14)
            
            fourc = oldf
            
        
    # swy: we couldn't convert it to a valid DX9 format; unchanged, leave it alone
    if fourc == b'DX10':
        print("unchanged; this is probably BC7 or other DX10-exclusive DDS format that we can't map back.")
        exit()
        
    if (fourc not in [b'DXT1', b'DXT2', b'DXT3', b'DXT4', b'DXT5', b'ATI1', b'ATI2']):
        print("the", fourc, " DDS type is unsupported; skipping")
        exit()

    # swy: now let's try to fix the pitch/linear size mess; every encoder uses their own combination of flags, screw the standards ¯\_(ツ)_/¯
    #      MSDN says that compressed textures should always use DDSD_LINEARSIZE, because this is an union we find all kinds of things here;
    #      it's either zeroed out, or it actually contains the pitch size or it *even* may be correct, maybe.
    
    #      specially-important for openbrf: https://github.com/Swyter/openbrf/blob/583356dfd0aef4b7d58139ebae22f337d47efc78/bindTexturePatch.h#L165
    
    f.seek(0x8)
    flags  = struct.unpack('<I', f.read(4))[0]
    width  = struct.unpack('<I', f.read(4))[0]
    height = struct.unpack('<I', f.read(4))[0]
    linear_or_pitch = struct.unpack('<I', f.read(4))[0]
    
    linearsize = int(int(width    + 3) / 4) * \
                 int(int(height   + 3) / 4) * \
                 int(int(fourc in [b'DXT1', b'ATI1']) and 8 or 16) # swy: all the other formats use 16 bytes per 4x4 pixel block; only those two are 8 bytes
                 
    pitchsize  = int(int(width    + 3) / 4) * \
                 int(int(fourc in [b'DXT1', b'ATI1']) and 8 or 16) # swy: all the other formats use 16 bytes per 4x4 pixel block; only those two are 8 bytes

    f.seek(0x14)
    print("chabnge", linear_or_pitch, linearsize, pitchsize, fourc, fourc in [b'DXT1', b'ATI1'] and 8 or 16)
    
    if linear_or_pitch != 0: # swy: not exactly standard-compliant; but we'll let it (empty fields) slide     
        if (flags & DDSD.LINEARSIZE) and not linear_or_pitch == linearsize:
            f.write(struct.pack('<I', linearsize)); print("a")
        elif (flags & DDSD.PITCH) and not linear_or_pitch == pitchsize:
            f.write(struct.pack('<I', pitchsize)); print("b")
        else:
            f.write(struct.pack('<I', linearsize)); print("c")
            f.seek(0x8)
            f.write(struct.pack('<I', (flags & ~DDSD.PITCH) | DDSD.LINEARSIZE))