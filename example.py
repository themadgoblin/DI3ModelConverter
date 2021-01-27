import struct

def HalfToFloat(h):
    s = int((h >> 15) & 0x00000001)     # sign
    e = int((h >> 10) & 0x0000001f)     # exponent
    f = int(h &         0x000003ff)     # fraction

    if e == 0:
       if f == 0:
          return int(s << 31)
       else:
          while not (f & 0x00000400):
             f <<= 1
             e -= 1
          e += 1
          f &= ~0x00000400
          print (s,e,f)
    elif e == 31:
       if f == 0:
          return int((s << 31) | 0x7f800000)
       else:
          return int((s << 31) | 0x7f800000 | (f << 13))

    e = e + (127 -15)
    f = f << 13

    return int((s << 31) | (e << 23) | f)


if __name__ == "__main__":

    # a half precision binary floating point string
    FP16=b'\x00\x3c'
    FP16=b'\x00\x36'
    FP16=b'\x00\x3f'


    v = struct.unpack('H', FP16)
    x = HalfToFloat(v[0])

    # hack to coerce to float
    str = struct.pack('I',x)
    f=struct.unpack('f', str)

    # print the resulting floating point
    print (f[0])
