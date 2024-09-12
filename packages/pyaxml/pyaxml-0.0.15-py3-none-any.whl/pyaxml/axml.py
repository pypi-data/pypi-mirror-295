import sys
try:
    from pyaxml.proto import axml_pb2
except ImportError:
    print("proto is not build")
    sys.exit(1)
from struct import pack, unpack
from pyaxml import public
import re
import ctypes
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree
from typing import Union
import logging

AXML_HEADER_SIZE=8
AXML_STRING_POOL_HEADER_SIZE=28
AXML_RES_TABLE_HEADER_SIZEM=AXML_HEADER_SIZE+4

class AConfiguration:

    # See http://aospxref.com/android-13.0.0_r3/xref/frameworks/native/include/android/configuration.h#56

    ORIENTATION_ANY  = 0x0000
    ORIENTATION_PORT = 0x0001
    ORIENTATION_LAND = 0x0002
    ORIENTATION_SQUARE = 0x0003
    TOUCHSCREEN_ANY = 0x0000
    TOUCHSCREEN_NOTOUCH = 0x0001
    TOUCHSCREEN_STYLUS = 0x0002
    TOUCHSCREEN_FINGER = 0x0003
    DENSITY_DEFAULT = 0
    DENSITY_LOW = 120
    DENSITY_MEDIUM = 160
    DENSITY_TV = 213
    DENSITY_HIGH = 240
    DENSITY_XHIGH = 320
    DENSITY_XXHIGH = 480
    DENSITY_XXXHIGH = 640
    DENSITY_ANY = 0xfffe
    DENSITY_NONE = 0xffff
    KEYBOARD_ANY  = 0x0000
    KEYBOARD_NOKEYS = 0x0001
    KEYBOARD_QWERTY = 0x0002
    KEYBOARD_12KEY = 0x0003
    NAVIGATION_ANY  = 0x0000
    NAVIGATION_NONAV = 0x0001
    NAVIGATION_DPAD = 0x0002
    NAVIGATION_TRACKBALL = 0x0003
    NAVIGATION_WHEEL = 0x0004
    KEYSHIDDEN_ANY = 0x0000
    KEYSHIDDEN_NO = 0x0001
    KEYSHIDDEN_YES = 0x0002
    KEYSHIDDEN_SOFT = 0x0003
    NAVHIDDEN_ANY = 0x0000
    NAVHIDDEN_NO = 0x0001
    NAVHIDDEN_YES = 0x0002
    SCREENSIZE_ANY = 0x00
    SCREENSIZE_SMALL = 0x01
    SCREENSIZE_NORMAL = 0x02
    SCREENSIZE_LARGE = 0x03
    SCREENSIZE_XLARGE = 0x04
    SCREENLONG_ANY = 0x00
    SCREENLONG_NO = 0x1
    SCREENLONG_YES = 0x2
    SCREENROUND_ANY = 0x00
    SCREENROUND_NO = 0x1
    SCREENROUND_YES = 0x2
    WIDE_COLOR_GAMUT_ANY = 0x00
    WIDE_COLOR_GAMUT_NO = 0x1
    WIDE_COLOR_GAMUT_YES = 0x2
    HDR_ANY = 0x00
    HDR_NO = 0x1
    HDR_YES = 0x2
    UI_MODE_TYPE_ANY = 0x00
    UI_MODE_TYPE_NORMAL = 0x01
    UI_MODE_TYPE_DESK = 0x02
    UI_MODE_TYPE_CAR = 0x03
    UI_MODE_TYPE_TELEVISION = 0x04
    UI_MODE_TYPE_APPLIANCE = 0x05
    UI_MODE_TYPE_WATCH = 0x06
    UI_MODE_TYPE_VR_HEADSET = 0x07
    UI_MODE_NIGHT_ANY = 0x00
    UI_MODE_NIGHT_NO = 0x1
    UI_MODE_NIGHT_YES = 0x2
    SCREEN_WIDTH_DP_ANY = 0x0000
    SCREEN_HEIGHT_DP_ANY = 0x0000
    SMALLEST_SCREEN_WIDTH_DP_ANY = 0x0000
    LAYOUTDIR_ANY = 0x00
    LAYOUTDIR_LTR = 0x01
    LAYOUTDIR_RTL = 0x02
    MCC = 0x0001
    MNC = 0x0002
    LOCALE = 0x0004
    TOUCHSCREEN = 0x0008
    KEYBOARD = 0x0010
    KEYBOARD_HIDDEN = 0x0020
    NAVIGATION = 0x0040
    ORIENTATION = 0x0080
    DENSITY = 0x0100
    SCREEN_SIZE = 0x0200
    VERSION = 0x0400
    SCREEN_LAYOUT = 0x0800
    UI_MODE = 0x1000
    SMALLEST_SCREEN_SIZE = 0x2000
    LAYOUTDIR = 0x4000
    SCREEN_ROUND = 0x8000
    COLOR_MODE = 0x10000
    MNC_ZERO = 0xffff

class TypedValue:

    TYPE_NULL=0x0
    TYPE_REFERENCE=0x1
    TYPE_ATTRIBUTE = 0x02
    TYPE_STRING = 0x03
    TYPE_FLOAT = 0x04
    TYPE_DIMENSION = 0x05
    TYPE_FRACTION = 0x06
    TYPE_FIRST_INT = 0x10
    TYPE_INT_DEC = 0x10
    TYPE_INT_HEX = 0x11
    TYPE_INT_BOOLEAN = 0x12
    TYPE_FIRST_COLOR_INT = 0x1c
    TYPE_INT_COLOR_ARGB8 = 0x1c
    TYPE_INT_COLOR_RGB8 = 0x1d
    TYPE_INT_COLOR_ARGB4 = 0x1e
    TYPE_INT_COLOR_RGB4 = 0x1f
    TYPE_LAST_COLOR_INT = 0x1f
    TYPE_LAST_INT = 0x1f

    COMPLEX_RADIX_SHIFT = 4
    COMPLEX_RADIX_MASK = 0x3
    COMPLEX_UNIT_SHIFT = 0
    COMPLEX_UNIT_MASK = 0xf

    COMPLEX_MANTISSA_SHIFT = 8
    COMPLEX_MANTISSA_MASK = 0xffffff

    DIMENSION_UNIT_STRS = [
        "px",
        "dip",
        "sp",
        "pt",
        "in",
        "mm"
    ]

    FRACTION_UNIT_STRS = [
        "%",
        "%p"
    ]


    def get_type(t : int):
        return t >> 24
    
    MANTISSA_MULT = 1.0 / float(1<<COMPLEX_MANTISSA_SHIFT)
    RADIX_MULTS = [1.0*MANTISSA_MULT, 1.0/float(1<<7)*MANTISSA_MULT,
                   1.0/(1<<15)*MANTISSA_MULT, 1.0/float(1<<23)*MANTISSA_MULT]

    def complexToFloat(complex : int):
        return (complex & (TypedValue.COMPLEX_MANTISSA_MASK<<TypedValue.COMPLEX_MANTISSA_SHIFT)) * TypedValue.RADIX_MULTS[(complex>>TypedValue.COMPLEX_RADIX_SHIFT) & TypedValue.COMPLEX_RADIX_MASK]
    
    def coerceToString(type : int, data : int):
        if type == TypedValue.TYPE_NULL:
            return "nil"
        elif type == TypedValue.TYPE_REFERENCE:
            return "@" + hex(data)[2:]
        elif type == TypedValue.TYPE_ATTRIBUTE:
            return "?" + hex(data)[2:]
        elif type == TypedValue.TYPE_FLOAT:
            return str(ctypes.c_float(data).value)
        elif type == TypedValue.TYPE_DIMENSION:
            return str(ctypes.c_float(data).value) + TypedValue.DIMENSION_UNIT_STRS[(data>>TypedValue.COMPLEX_UNIT_SHIFT)&TypedValue.COMPLEX_UNIT_MASK]
        elif type == TypedValue.TYPE_FRACTION:
            return str(TypedValue.complexToFloat(data).value * 100) + TypedValue.FRACTION_UNIT_STRS[(data>>TypedValue.COMPLEX_UNIT_SHIFT)&TypedValue.COMPLEX_UNIT_MASK]
        elif type == TypedValue.TYPE_INT_HEX:
            return hex(data)
        elif type == TypedValue.TYPE_INT_BOOLEAN:
            return "true" if data != 0 else "false"
        elif type >= TypedValue.TYPE_FIRST_COLOR_INT and type <= TypedValue.TYPE_LAST_COLOR_INT:
            return "#" + hex(data)[2:]
        elif type >= TypedValue.TYPE_FIRST_INT and type <= TypedValue.TYPE_LAST_INT:
            return str(ctypes.c_int32(data).value)

        return None
    



class AXMLHeader:
    """AXMLHeader class to build an AXMLHeader
    """

    def __init__(self, type : int = 0, size : int = 0, proto : axml_pb2.AXMLHeader = None, base_proto: axml_pb2.AXMLHeader = None):
        """Initialize an AXMLHeader

        Args:
            type (int, optional): type element from ResType. Defaults to 0.
            size (int, optional): size of data contain belong to this AXMLHeader. Defaults to 0.
            proto (axml_pb2.AXMLHeader, optional): define AXMLHeader by a protobuff. Defaults to None.
        """
        
        if proto is None:
            if base_proto:
                self.proto = base_proto
            else:
                self.proto = axml_pb2.AXMLHeader()
            self.proto.type = type
            self.proto.size = size
            self.proto.header_size = AXML_HEADER_SIZE
        else:
            self.proto = proto
        

    def pack(self) -> bytes:
        """pack the AXMLHeader element

        Returns:
            bytes: return the AXMLHeader element packed
        """
        return pack("<HHL", self.proto.type, self.proto.header_size, self.proto.size)
    
    def from_axml(buff : bytes, proto=None):
        """Convert AXMLHeader buffer to AXMLHeader object

        Args:
            buff (bytes): buffer contain AXMLHeader object

        Returns:
            tuple[pyaxml.AXMLHeader, bytes]: return AXMLHeader element and buffer offset at the end of the reading
        """
        header = AXMLHeader()
        if proto:
            header.proto = proto 
        header.proto.type, header.proto.header_size, header.proto.size = unpack('<HHL', buff[:8])
        return header, buff[8:]
    

class AXMLHeader_XML(AXMLHeader):
    """AXMLHeader_XML class to build an AXMLHeader with the type RES_XML_TYPE
    """

    def __init__(self, size : int = 0, proto : axml_pb2.AXMLHeader = None):
        """Initialize an AXMLHeader with the type RES_XML_TYPE

        Args:
            size (int, optional): size of data contain belong to this AXMLHeader. Defaults to 0.
            proto (axml_pb2.AXMLHeader, optional): define AXMLHeader by a protobuff. Defaults to None.
        """
        if proto is None:
            super().__init__(axml_pb2.RES_XML_TYPE, size)
        else:
            self.proto = proto

    def from_axml(buff : bytes, proto = None):
        """Convert AXMLHeader_XML buffer to AXMLHeader_XML object

        Args:
            buff (bytes): buffer contain AXMLHeader_XML object

        Returns:
            tuple[pyaxml.AXMLHeader_XML, bytes]: return AXMLHeader_XML element and buffer offset at the end of the reading
        """
        header_xml = AXMLHeader_XML()
        if proto:
            header_xml.proto = proto 
        header, buff = AXMLHeader.from_axml(buff)
        if header.proto.type != axml_pb2.RES_XML_TYPE:
            raise Exception("AXMLHeader_XML file wrong format no XML_TYPE")
        return header_xml, buff

class AXMLHeader_RES_TABLE:
    """AXMLHeader_RES_TABLE class to build an AXMLHeader with the type RES_RES_TABLE_TYPE
    """

    def __init__(self, size : int = 0, package_count : int = 0, proto : axml_pb2.AXMLHeader_RES_TABLE = None):
        """Initialize AXMLHeader for RES_TABLE

        Args:
            size (int, optional): size of the RES_HEADER block. Defaults to 0.
            package_count (int, optional): number of package. Defaults to 0.
            proto (axml_pb2.AXMLHeader_RES_TABLE, optional): protobuff of AXMLHeader_RES_TABLE. Defaults to None.
        """
        
        if proto is None:
            self.proto = axml_pb2.AXMLHeader_RES_TABLE()
            self.proto.package_count = package_count
            AXMLHeader(axml_pb2.RES_TABLE_TYPE, size, base_proto=self.proto.hnd)
            self.proto.hnd.header_size = AXML_RES_TABLE_HEADER_SIZEM
        else:
            self.proto = proto
    
    def pack(self) -> bytes:
        """pack the AXMLHeader element

        Returns:
            bytes: return the AXMLHeader element packed
        """
        return AXMLHeader(proto=self.proto.hnd).pack() + pack("<L", self.proto.package_count)
    
    def from_axml(buff : bytes, proto = None):
        """Convert AXMLHeader_RES_TABLE buffer to AXMLHeader_RES_TABLE object

        Args:
            buff (bytes): buffer contain AXMLHeader_RES_TABLE object

        Returns:
            tuple[pyaxml.AXMLHeader_RES_TABLE, bytes]: return AXMLHeader_RES_TABLE element and buffer offset at the end of the reading
        """
        restable_header = AXMLHeader_RES_TABLE()
        if proto:
            restable_header.proto = proto
        _, buff = AXMLHeader.from_axml(buff, proto=restable_header.proto.hnd)
        restable_header.proto.package_count = unpack('<L', buff[:4])[0]
        return restable_header, buff[4:]
    
    


class AXMLHeader_STRING_POOL:
    """AXMLHeader_STRING_POOL class to build an AXMLHeader_STRING_POOL element
    """

    def __init__(self, sb : list = None, size : int = 0, proto : axml_pb2.AXMLHeader_STRING_POOL = None):
        """Initialize an AXMLHeader of STRING_POOL

        Args:
            sb (list, optional): list of Stringblock elements. Defaults to None.
            size (int, optional): size of data contain belong to this AXMLHeader. Defaults to 0.
            proto (axml_pb2.AXMLHeader_STRING_POOL, optional): define AXMLHeader_STRING_POOL by a protobuff. Defaults to None.
        """
        # TODO make version with initilisation without proto
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.AXMLHeader_STRING_POOL()
    
    def compute(self):
        """Compute all fields to have a Stringpool element
        """
        pass

    def pack(self) -> bytes:
        """pack the AXMLHeader_STRING_POOL element

        Returns:
            bytes: return the AXMLHeader_STRING_POOL element packed
        """
        # TODO add style block for the moment force to 0
        self.proto.len_styleblocks = 0
        return AXMLHeader(proto=self.proto.hnd).pack() + pack("<LLLLL", self.proto.len_stringblocks, self.proto.len_styleblocks,
                                                                        self.proto.flag, self.proto.stringoffset, self.proto.styleoffset)
    
    def from_axml(buff : bytes, proto=None):
        """Convert AXMLHeader_STRING_POOL buffer to AXMLHeader_STRING_POOL object

        Args:
            buff (bytes): buffer contain AXMLHeader_STRING_POOL object

        Returns:
            tuple[pyaxml.AXMLHeader_STRING_POOL, bytes]: return AXMLHeader_STRING_POOL element and buffer offset at the end of the reading
        """
        hnd_str_pool = AXMLHeader_STRING_POOL()
        if proto:
            hnd_str_pool.proto = proto
        _, buff = AXMLHeader.from_axml(buff, proto=hnd_str_pool.proto.hnd)
        hnd_str_pool.proto.len_stringblocks, hnd_str_pool.proto.len_styleblocks, hnd_str_pool.proto.flag, \
              hnd_str_pool.proto.stringoffset, hnd_str_pool.proto.styleoffset = unpack("<LLLLL", buff[:5*4])
        return hnd_str_pool, buff[5*4:]


##############################################################################
#
#                              STRINGBLOCKS
#
##############################################################################


class StringBlock:
    """StringBlock class to build an StringBlock element
    """

    def __init__(self, data : str = "", size : int = 0, utf8 : bool = False, proto : axml_pb2.StringBlock = None):
        """initialize a stringblock element

        Args:
            data (str, optional): value of the stringblock. Defaults to "".
            size (int, optional): size of data contain belong to this Stringblock. Defaults to 0.
            utf8 (bool, optional): Stringblock can be encoded in UTF8 or UTF16. set True if you want to encode in UTF8 else UTF16. Defaults to False.
            proto (axml_pb2.StringBlock, optional): define StringBlock by a protobuff. Defaults to None.
        """
        self.not_decoded = False
        if proto:
            self.proto = proto
            self.utf8= utf8
        else:
            self.proto = axml_pb2.StringBlock()
            self.utf8= utf8
            if self.utf8:
                self.proto.data = data.encode('utf-8')
                self.proto.padding = b"\x00"
            else:
                self.proto.data = data.encode('utf-16')[2:]
                self.proto.padding = b"\x00\x00"
            self.proto.size = size

    
    def compute(self):
        """Compute all fields to have a StringBlock element
        """
        tmp_size = self.proto.size
        if self.utf8:
            size = len(self.proto.data)
            if size > 0x7F:
                self.proto.size = (size & 0xFF) << 8 | (size & 0xFF00) >> 8 | 0x80
                self.proto.redundant_size = self.proto.size
            else:
                self.proto.size = size | size << 8
        else:
            size = int(len(self.proto.data)/2)
            if size > 0x7FFF:
                self.proto.size = (size >> 16) | 0x8000
                self.proto.redundant_size = size & 0xFFFF
            else:
                self.proto.size = size
    
    def pack(self) -> bytes:
        """pack the StringBlock element

        Returns:
            bytes: return the StringBlock element packed
        """
        redundant = b""
        if self.proto.HasField('redundant_size'):
            redundant = pack('<H', self.proto.redundant_size)
        if self.utf8:
            return pack('<H', self.proto.size) + redundant + self.proto.data + self.proto.padding
        else:
            return pack('<H', self.proto.size) + redundant + self.proto.data + self.proto.padding
    
    def from_axml(buff : bytes, utf8 : bool, proto = None):
        """Convert StringBlock buffer to StringBlock object

        Args:
            buff (bytes): buffer contain StringBlock object
            utf8 (bool) : specify the encoding of string

        Returns:
            tuple[pyaxml.StringBlock, bytes]: return StringBlock element and buffer offset at the end of the reading
        """
        str_block = StringBlock()
        if proto:
            str_block.proto = proto
        str_block.utf8 = utf8
        if str_block.utf8:
            str_block.proto.size = unpack('<H', buff[:2])[0]
            size = str_block.proto.size >> 8
            if str_block.proto.size & 0x80 != 0:
                redundant = unpack('<H', buff[2:4])[0]
                size = ((redundant & 0xff00) >> 8 | (redundant & 0xf) << 8)
                buff = buff[2:]
                str_block.proto.redundant_size = redundant
        else:
            str_block.proto.size = unpack('<H', buff[:2])[0]
            if str_block.proto.size & 0x8000 != 0:
                redundant = unpack('<H', buff[2:4])[0]
                size = ((str_block.proto.size & 0x7FFF) << 16) | redundant
                buff = buff[2:]
                str_block.proto.redundant_size = redundant
            size = str_block.proto.size * 2

        while buff[2+size] != 0:
            size +=1

        str_block.proto.data = buff[2:2+size]
        str_block.proto.padding = buff[2+size:]
        return str_block, b""

class StringBlocks:
    """StringBlocks class to build all StringBlocks elements
    """
 
    def __init__(self, proto : axml_pb2.StringBlocks = None):
        """initialize the bunch of StringBlocks element

        Args:
            proto (axml_pb2.StringBlocks, optional): define Stringblocks by a protobuff. Defaults to None.
        """
        
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.StringBlocks()
    
    def compute(self, update_size=False):
        """Compute all fields to have all StringBlocks elements
        """

        idx = 0
        del self.proto.stringoffsets[:]
        for s in self.proto.stringblocks:
            self.proto.stringoffsets.append(idx)
            s_obj = StringBlock(proto=s, utf8=self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG)
            if update_size:
                s_obj.compute()
                s.CopyFrom(s_obj.proto)
            idx += len(s_obj.pack())
            

        self.proto.hnd.stringoffset = AXML_STRING_POOL_HEADER_SIZE + \
            len(b"".join(pack('<I', x) for x in self.proto.stringoffsets)) + \
            len(b"".join(pack('<I', x) for x in self.proto.styleoffsets))
        
        self.proto.hnd.styleoffset = self.proto.hnd.stringoffset + len(b"".join(StringBlock(proto=elt, utf8=self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG).pack() for elt in self.proto.stringblocks))
        #self.proto.hnd.styleoffset = self.proto.hnd.stringoffset + len(self.align(b"".join(StringBlock(proto=elt, utf8=self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG).pack() for elt in self.proto.stringblocks)))
        AXMLHeader(axml_pb2.RES_STRING_POOL_TYPE, len(self.pack()), base_proto=self.proto.hnd.hnd)
        self.proto.hnd.hnd.header_size = AXML_STRING_POOL_HEADER_SIZE
        self.proto.hnd.len_stringblocks = len(self.proto.stringoffsets)
        self.proto.hnd.len_styleblocks = len(self.proto.styleoffsets)
    
    def align(self, buf : bytes) -> bytes:
        """Align stringblocks elements

        Args:
            buf (bytes): align the buffer given in input

        Returns:
            bytes: return the element with padding to align
        """
        pad = b"\x00" * (4 - (len(buf) % 4))
        if len(pad) == 4:
            return buf
        else:
            return buf + pad

    def get(self, name : str) -> int:
        """Get index of a stringblock or if it doesn't exist append a new one.

        Args:
            name (str): the name of the stringblock

        Returns:
            int: return the index of the stringblock
        """
        try:
            index = self.index(name)
        except ValueError:
            index = len(self.proto.stringblocks)
            tmp = StringBlock(data=name, utf8=self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG)
            tmp.compute()
            self.proto.stringblocks.append(tmp.proto)
        return index
    
    def index(self, name : str) -> int:
        """Get index of a stringblock or if it doesn't exist raise an error

        Args:
            name (str): the name of the stringblock
        
        Raises:
            ValueError: raise ValueError if this element didn't exist

        Returns:
            int: return the index of the stringblock
        """
        name_encoded = StringBlock(data=name, utf8=self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG)
        for i in range(0, len(self.proto.stringblocks)):
            if self.proto.stringblocks[i].data == name_encoded.proto.data:
                return i
        raise ValueError
    
    def update(self, index : int, name : str):
        name_encoded = StringBlock(data=name, utf8=self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG)
        name_encoded.compute()
        self.proto.stringblocks[index].CopyFrom(name_encoded.proto)

    def replace(self, old_name : str, new_name : str):
        index = self.index(old_name)
        self.update(index, new_name)

    def switch(self, name1 : str, name2 : str):
        index1 = self.index(name1)
        index2 = self.index(name2)
        self.update(index1, name2)
        self.update(index2, name1)

    def decode_str(self, index : int) -> str:
        data = self.proto.stringblocks[index].data
        try:
            return data.decode('utf-8') if self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG else data.decode('utf-16')
        except UnicodeDecodeError:
            return data
    def pack(self) -> bytes:
        """pack the StringBlocks element

        Returns:
            bytes: return the StringBlocks element packed
        """
        sb_offsets = b"".join(pack('<I', x) for x in self.proto.stringoffsets)
        st_offsets = b"".join(pack('<I', x) for x in self.proto.styleoffsets)
        #sb = self.align(b"".join(StringBlock(proto=elt, utf8=self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG).pack() for elt in self.proto.stringblocks))
        sb = b"".join(StringBlock(proto=elt, utf8=self.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG).pack() for elt in self.proto.stringblocks)
        st = b"" # TODO
        return AXMLHeader_STRING_POOL(proto=self.proto.hnd).pack() + sb_offsets + st_offsets + sb + st
    
    def from_axml(buff : bytes, proto=None):
        """Convert StringBlocks buffer to StringBlocks object

        Args:
            buff (bytes): buffer contain StringBlocks object

        Returns:
            tuple[pyaxml.StringBlocks, bytes]: return StringBlocks element and buffer offset at the end of the reading
        """
        rest = buff
        cur_buff=buff
        str_blocks = StringBlocks()
        if proto:
            str_blocks.proto = proto
        hnd, buff = AXMLHeader_STRING_POOL.from_axml(buff, proto=str_blocks.proto.hnd)
        buff = buff[:hnd.proto.hnd.size-hnd.proto.hnd.header_size]
        rest = rest[hnd.proto.hnd.size:]
        for i in range(str_blocks.proto.hnd.len_stringblocks):
            str_blocks.proto.stringoffsets.append(unpack('<I', buff[i*4:(i+1)*4])[0])
        buff = buff[str_blocks.proto.hnd.len_stringblocks*4:]
        for i in range(str_blocks.proto.hnd.len_styleblocks):
            str_blocks.proto.styleoffsets.append(unpack('<I', buff[i*4:(i+1)*4])[0])
        buff = buff[str_blocks.proto.hnd.len_styleblocks*4:]
        if len(str_blocks.proto.stringoffsets) > 0:
            if str_blocks.proto.hnd.len_styleblocks > 0:
                temp_buff = cur_buff[str_blocks.proto.hnd.stringoffset:str_blocks.proto.hnd.styleoffset]
            else:
                temp_buff = cur_buff[str_blocks.proto.hnd.stringoffset:hnd.proto.hnd.size]
            st_offsets_sort = list(str_blocks.proto.stringoffsets).copy()
            st_offsets_sort.sort()
            for i in range(str_blocks.proto.hnd.len_stringblocks):
                next_index = st_offsets_sort.index(str_blocks.proto.stringoffsets[i]) + 1
                if len(st_offsets_sort) > next_index:
                    next_value = st_offsets_sort[next_index]
                    stbl , _ = StringBlock.from_axml(temp_buff[str_blocks.proto.stringoffsets[i]:next_value], str_blocks.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG)
                else:
                    last_str , _ = StringBlock.from_axml(temp_buff[str_blocks.proto.stringoffsets[i]:], str_blocks.proto.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG)
                    stbl = last_str
                str_blocks.proto.stringblocks.append(stbl.proto)
            buff = buff[str_blocks.proto.stringoffsets[-1] + len(last_str.pack()):]
        #TODO style
        return str_blocks, rest

##############################################################################
#
#                              RESOURCEMAP
#
##############################################################################

class ResourceMap:
    """ResourceMap class to build all ResourceMap elements
    """


    def __init__(self, res : [StringBlock] = [], proto : axml_pb2.ResourceMap = None):
        """initialize ResourceMap element

        Args:
            res (StringBlock], optional): List of StringBlock elements. Defaults to [].
            proto (axml_pb2.ResourceMap, optional): define ResourceMap by a protobuff. Defaults to None.
        """
        if proto is None:
            self.proto = axml_pb2.ResourceMap()
            self.proto.res.extend(res)
            AXMLHeader(axml_pb2.RES_XML_RESOURCE_MAP_TYPE, 8, base_proto=self.proto.header)
            self.proto.header.size = AXML_HEADER_SIZE + 4 * len(res)
        else:
            self.proto = proto
    
    def pack(self) -> bytes:
        """pack the ResourceMap element

        Returns:
            bytes: return the ResourceMap element packed
        """
        return AXMLHeader(proto=self.proto.header).pack() + b"".join(pack("<L", x) for x in self.proto.res)
    
    def from_axml(buff : bytes, proto=None):
        """Convert ResourceMap buffer to ResourceMap object

        Args:
            buff (bytes): buffer contain ResourceMap object

        Returns:
            tuple[pyaxml.ResourceMap, bytes]: return ResourceMap element and buffer offset at the end of the reading
        """
        res_maps = ResourceMap()
        if proto:
            res_maps.proto = proto
        _, buff = AXMLHeader.from_axml(buff, proto=res_maps.proto.header)
        for _ in range(int((res_maps.proto.header.size-res_maps.proto.header.header_size)/4) ):
            res_maps.proto.res.append(unpack('<L', buff[:4])[0])
            buff = buff[4:]
        return res_maps, buff

##############################################################################
#
#                              XML ELEMENTS
#
##############################################################################

class AXMLHeader_RES_XML(AXMLHeader):
    """AXMLHeader_RES_XML class to build an header of RES_XML
    """

    def __init__(self, type=0, size=0, proto : axml_pb2.AXMLHeader = None):
        """Initialize header of Res_XML

        Args:
            type (int, optional): define the type. Defaults to 0.
            size (int, optional): define the size of whole element. Defaults to 0.
            proto (axml_pb2.AXMLHeader, optional): define RES_XML header by a protobuff. Defaults to None.
        """
        if proto is None:
            super().__init__(type, size + 8, proto)
            self.proto.header_size = 16
        else:
            self.proto = proto 

class AXMLHeader_START_ELEMENT(AXMLHeader_RES_XML):
    """AXMLHeader_START_ELEMENT class to build an header of Start element
    """

    def __init__(self, size : int):
        """initialize START_ELEMENT element

        Args:
            size (int): size of START_ELEMENT and its header
        """
        super().__init__(axml_pb2.RES_XML_START_ELEMENT_TYPE, size)

class AXMLHeader_END_ELEMENT(AXMLHeader_RES_XML):
    """AXMLHeader_END_ELEMENT class to build an header of End element
    """

    def __init__(self, size : int):
        """initialize END_ELEMENT element

        Args:
            size (int): size of END_ELEMENT and its header
        """
        super().__init__(axml_pb2.RES_XML_END_ELEMENT_TYPE, size)

class AXMLHeader_START_NAMESPACE(AXMLHeader_RES_XML):
    """AXMLHeader_START_NAMESPACE class to build an header of Start namespace
    """

    def __init__(self, size : int):
        """initialize START_NAMESPACE element

        Args:
            size (int): size of START_NAMESPACE and its header
        """
        super().__init__(axml_pb2.RES_XML_START_NAMESPACE_TYPE, size)

class AXMLHeader_END_NAMESPACE(AXMLHeader_RES_XML):
    """AXMLHeader_END_NAMESPACE class to build an header of End namespace
    """

    def __init__(self, size : int):
        """initialize END_NAMESPACE element

        Args:
            size (int): size of END_NAMESPACE and its header
        """
        super().__init__(axml_pb2.RES_XML_END_NAMESPACE_TYPE, size)

class Classical_RES_XML:
    """RES_XML class to build RES_XML element
    """

    def __init__(self, lineNumber : int = 0, Comment : int = 0xffffffff, proto : axml_pb2.ResXML = None):
        """initialize RES_XML element

        Args:
            lineNumber (int, optional): _description_. Defaults to 0.
            Comment (int, optional): _description_. Defaults to 0xffffffff.
            proto (axml_pb2.ResXML, optional): define RES_XML by a protobuff. Defaults to None.
        """
        if proto is None:
            self.proto.generic.lineNumber = lineNumber
            self.proto.generic.Comment = Comment
        else:
            self.proto.generic.CopyFrom(proto)

    @property
    def content(self):
        return pack('<LL', self.proto.generic.lineNumber, self.proto.generic.Comment)
    
    def compute(self):
        """Compute all fields to have all RES_XML elements
        """
        pass

    def pack(self) -> bytes:
        """pack the RES_XML element

        Returns:
            bytes: return the RES_XML element packed
        """
        return self.content

    def from_axml(buff : bytes, class_xml):
        """Convert Classical_RES_XML buffer to Classical_RES_XML object

        Args:
            buff (bytes): buffer contain Classical_RES_XML object
            class_xml (pyaxml.Classical_RES_XML): _description_

        Returns:
            tuple[pyaxml.Classical_RES_XML, bytes]: return Classical_RES_XML element and buffer offset at the end of the reading
        """
        class_xml.proto.generic.lineNumber, \
                class_xml.proto.generic.Comment = unpack('<LL', buff[:8])
        return class_xml, buff[8:]

class RES_XML_START_ELEMENT(Classical_RES_XML):

    def __init__(self, namespaceURI : int = 0xffffffff, name : int =0xffffffff, attributes : list = [],
            styleAttribute : int = -1, classAttribute : int = -1, lineNumber : int = 0, Comment : int = 0xffffffff,
            at_start = 0x14, at_size=0x14,
            proto : axml_pb2.ResXMLStartElement = None):
        """_summary_

        Args:
            namespaceURI (int, optional): _description_. Defaults to 0xffffffff.
            name (int, optional): _description_. Defaults to 0xffffffff.
            attributes (list, optional): _description_. Defaults to [].
            styleAttribute (int, optional): _description_. Defaults to -1.
            classAttribute (int, optional): _description_. Defaults to -1.
            lineNumber (int, optional): _description_. Defaults to 0.
            Comment (int, optional): _description_. Defaults to 0xffffffff.
            proto (axml_pb2.ResXMLStartElement, optional): _description_. Defaults to None.
        """
        if proto is None:
            self.proto = axml_pb2.ResXMLStartElement()
            super().__init__(lineNumber, Comment)
            self.proto.namespaceURI = namespaceURI
            self.proto.name = name
            self.proto.attributes.extend(attributes)
            self.proto.styleAttribute = styleAttribute
            self.proto.classAttribute = classAttribute
            self.proto.at_start = at_start
            self.proto.at_size = at_size
        else:
            self.proto = proto
            super().__init__(proto=proto.generic)
            

    def compute(self):
        """Compute all fields to have all RES_XML_START_ELEMENT elements
        """
        self.proto.len_attributes = len(self.proto.attributes)
        super().compute()

    @property
    def content(self) -> bytes:
        """_summary_

        Returns:
            bytes: _description_
        """
        return super().content + pack('<LLhhLhh',
                self.proto.namespaceURI,
                self.proto.name,
                self.proto.at_start,
                self.proto.at_size,
                self.proto.len_attributes,
                self.proto.styleAttribute,
                self.proto.classAttribute) + \
                        b"".join(Attribute(proto=a).pack() for a in self.proto.attributes)
    
    def from_axml(buff : bytes, proto=None):
        """Convert RES_XML_START_ELEMENT buffer to RES_XML_START_ELEMENT object

        Args:
            buff (bytes): buffer contain RES_XML_START_ELEMENT object

        Returns:
            tuple[pyaxml.RES_XML_START_ELEMENT, bytes]: return RES_XML_START_ELEMENT element and buffer offset at the end of the reading
        """
        class_xml = RES_XML_START_ELEMENT()
        if proto:
            class_xml.proto = proto
        class_xml, buff = Classical_RES_XML.from_axml(buff, class_xml=class_xml)

        class_xml.proto.namespaceURI, class_xml.proto.name, class_xml.proto.at_start, class_xml.proto.at_size, class_xml.proto.len_attributes,  class_xml.proto.styleAttribute,  class_xml.proto.classAttribute = unpack('<LLhhLhh', buff[:20])
        buff = buff[20:]

        for i in range(class_xml.proto.len_attributes):
            padding = class_xml.proto.at_size - 0x14
            attr, buff = Attribute.from_axml(buff, padding)
            class_xml.proto.attributes.append(attr.proto)

        return class_xml, buff

class RES_XML_END_ELEMENT(Classical_RES_XML):

    def __init__(self, namespaceURI : int = 0xffffffff, name : int = 0xffffffff,
                 lineNumber : int = 0, Comment : int = 0xffffffff,
                 proto : axml_pb2.ResXMLEndElement = None):
        """_summary_

        Args:
            namespaceURI (int, optional): _description_. Defaults to 0xffffffff.
            name (int, optional): _description_. Defaults to 0xffffffff.
            lineNumber (int, optional): _description_. Defaults to 0.
            Comment (int, optional): _description_. Defaults to 0xffffffff.
            proto (axml_pb2.ResXMLEndElement, optional): _description_. Defaults to None.
        """
        if proto is None:
            self.proto = axml_pb2.ResXMLEndElement()
            super().__init__(lineNumber, Comment)
            self.proto.namespaceURI = namespaceURI
            self.proto.name = name
        else:
            self.proto = proto
            super().__init__(proto=proto.generic)


    @property
    def content(self) -> bytes:
        """_summary_

        Returns:
            bytes: _description_
        """
        return super().content + pack('<LL',
                self.proto.namespaceURI,
                self.proto.name)

    def from_axml(buff, proto=None):
        """Convert RES_XML_END_ELEMENT buffer to RES_XML_END_ELEMENT object

        Args:
            buff (bytes): buffer contain RES_XML_END_ELEMENT object

        Returns:
            tuple[pyaxml.RES_XML_END_ELEMENT, bytes]: return RES_XML_END_ELEMENT element and buffer offset at the end of the reading
        """
        class_xml = RES_XML_END_ELEMENT()
        if proto:
            class_xml.proto = proto
        class_xml, buff = Classical_RES_XML.from_axml(buff, class_xml=class_xml)
        class_xml.proto.namespaceURI, \
                class_xml.proto.name = unpack('<LL', buff[:8])
        return class_xml, buff[8:]


class RES_XML_START_NAMESPACE(Classical_RES_XML):

    def __init__(self, prefix : int = 0xffffffff, uri : int = 0xffffffff,
                lineNumber : int = 0, Comment : int = 0xffffffff,
                proto : axml_pb2.ResXMLStartNamespace = None):
        """_summary_

        Args:
            prefix (int, optional): _description_. Defaults to 0xffffffff.
            uri (int, optional): _description_. Defaults to 0xffffffff.
            lineNumber (int, optional): _description_. Defaults to 0.
            Comment (int, optional): _description_. Defaults to 0xffffffff.
            proto (axml_pb2.ResXMLStartNamespace, optional): _description_. Defaults to None.
        """
        if proto is None:
            self.proto = axml_pb2.ResXMLStartNamespace()
            super().__init__(lineNumber, Comment)
            self.proto.prefix = prefix
            self.proto.uri = uri
        else:
            self.proto = proto
            super().__init__(proto=proto.generic)
            

    @property
    def content(self) -> bytes:
        """_summary_

        Returns:
            bytes: _description_
        """
        return super().content + pack('<LL',
                self.proto.prefix,
                self.proto.uri)
    
    def from_axml(buff : bytes, proto = None):
        """Convert RES_XML_START_NAMESPACE buffer to RES_XML_START_NAMESPACE object

        Args:
            buff (bytes): buffer contain RES_XML_START_NAMESPACE object

        Returns:
            tuple[pyaxml.RES_XML_START_NAMESPACE, bytes]: return RES_XML_START_NAMESPACE element and buffer offset at the end of the reading
        """
        class_xml = RES_XML_START_NAMESPACE()
        if proto:
            class_xml.proto = proto
        class_xml, buff = Classical_RES_XML.from_axml(buff, class_xml=class_xml)
        class_xml.proto.prefix, \
                class_xml.proto.uri = unpack('<LL', buff[:8])
        return class_xml, buff[8:]

class RES_XML_END_NAMESPACE(Classical_RES_XML):

    def __init__(self, prefix : int = 0xffffffff, uri : int = 0xffffffff,
                 lineNumber : int = 0, Comment : int = 0xffffffff,
                 proto : axml_pb2.ResXMLEndNamespace = None):
        """_summary_

        Args:
            prefix (int, optional): _description_. Defaults to 0xffffffff.
            uri (int, optional): _description_. Defaults to 0xffffffff.
            lineNumber (int, optional): _description_. Defaults to 0.
            Comment (int, optional): _description_. Defaults to 0xffffffff.
            proto (axml_pb2.ResXMLEndNamespace, optional): _description_. Defaults to None.
        """
        if proto is None:
            self.proto = axml_pb2.ResXMLEndNamespace()
            super().__init__(lineNumber, Comment)
            self.proto.prefix = prefix
            self.proto.uri = uri
        else:
            self.proto = proto
            super().__init__(proto=proto.generic)
            

    @property
    def content(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return super().content + pack('<LL',
                self.proto.prefix,
                self.proto.uri)
    
    def from_axml(buff : bytes, proto=None):
        """Convert RES_XML_END_NAMESPACE buffer to RES_XML_END_NAMESPACE object

        Args:
            buff (bytes): buffer contain RES_XML_END_NAMESPACE object

        Returns:
            tuple[pyaxml.RES_XML_END_NAMESPACE, bytes]: return RES_XML_END_NAMESPACE element and buffer offset at the end of the reading
        """
        class_xml = RES_XML_END_NAMESPACE()
        if proto:
            class_xml.proto = proto
        class_xml, buff = Classical_RES_XML.from_axml(buff, class_xml=class_xml)
        class_xml.proto.prefix, \
                class_xml.proto.uri = unpack('<LL', buff[:8])
        return class_xml, buff[8:]
    

class Attribute:

    def __init__(self, namespaceURI : int = 0xffffffff, name : int = 0xffffffff, value : int = 0xffffffff, type : int = 0xffffffff, data : int = 0xffffffff, proto : axml_pb2.Attribute = None):
        """Initialize an Attribute element from protobuff or parameters

        Args:
            namespaceURI (int, optional): namespace of Attribute. Defaults to 0xffffffff.
            name (int, optional): name of Attribute. Defaults to 0xffffffff.
            value (int, optional): value of the attribute. Defaults to 0xffffffff.
            type (int, optional): type of attribute. Defaults to 0xffffffff.
            data (int, optional): data of the parameter in function of the type it could be store in value or data. Defaults to 0xffffffff.
            proto (axml_pb2.Attribute, optional): protobuff of Attribute content. Defaults to None.
        """
        if proto is None:
            self.proto = axml_pb2.Attribute()
            self.proto.namespaceURI = namespaceURI
            self.proto.name = name
            self.proto.value = value
            self.proto.type = type
            self.proto.data = data
        else:
            self.proto = proto

    def pack(self) -> bytes:
        """pack the Attribute element

        Returns:
            bytes: return the Attribute element packed
        """
        return pack('<LLLLL', self.proto.namespaceURI, self.proto.name, self.proto.value,
                self.proto.type, self.proto.data) + self.proto.padding

    def from_axml(buff, padding=0, proto=None):
        """Convert Attribute buffer to Attribute object

        Args:
            buff (bytes): buffer contain Attribute object

        Returns:
            tuple[pyaxml.Attribute, bytes]: return Attribute element and buffer offset at the end of the reading
        """
        attr = Attribute()
        if proto:
            attr.proto = proto
        attr.proto.namespaceURI, \
        attr.proto.name, \
        attr.proto.value, \
        attr.proto.type, \
        attr.proto.data = unpack('<LLLLL', buff[:20])
        attr.proto.padding = buff[20:20+padding]
        return attr, buff[20+padding:]

class RES_XML_CDATA(Classical_RES_XML):
    
    def __init__(self, proto : axml_pb2.ResXMLCDATA = None):
        """Initialize an RES_XML_CDATA element from protobuff or parameters

        Args:
            TODO
        """
        if proto is None:
            self.proto = axml_pb2.ResXMLCDATA()
        else:
            self.proto = proto
    
    @property
    def content(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return super().content + pack('<L', self.proto.name) + ARSCResStringPoolRef(proto=self.proto.res).pack()

    def from_axml(buff, proto=None):
        """Convert RES_XML_CDATA buffer to RES_XML_CDATA object

        Args:
            buff (bytes): buffer contain RES_XML_CDATA object

        Returns:
            tuple[pyaxml.RES_XML_CDATA, bytes]: return RES_XML_CDATA element and buffer offset at the end of the reading
        """
        class_xml = RES_XML_CDATA()
        if proto:
            class_xml.proto = proto
        class_xml, buff = Classical_RES_XML.from_axml(buff, class_xml=class_xml)
        class_xml.proto.name = unpack('<L', buff[:4])[0]
        _, buff = ARSCResStringPoolRef.from_axml(buff[4:], proto=class_xml.proto.res)
        return class_xml, buff



class ResourceXML:

    def __init__(self, proto : axml_pb2.ResourceXML = None) -> None:
        """_summary_

        Args:
            proto (axml_pb2.ResourceXML, optional): protobuff of ResourceXML content. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.ResourceXML()
    
    def pack(self) -> bytes:
        """pack the ResourceXML element

        Returns:
            bytes: return the ResourceXML element packed
        """
        buf = b""
        for elt in self.proto.elts:
            header = AXMLHeader(proto=elt.header).pack()
            if elt.HasField('start_elt'):
                buf += header + RES_XML_START_ELEMENT(proto=elt.start_elt).pack()
            elif elt.HasField('end_elt'):
                buf += header + RES_XML_END_ELEMENT(proto=elt.end_elt).pack()
            elif elt.HasField('start_ns'):
                buf += header + RES_XML_START_NAMESPACE(proto=elt.start_ns).pack()
            elif elt.HasField('end_ns'):
                buf += header + RES_XML_END_NAMESPACE(proto=elt.end_ns).pack()
            elif elt.HasField('cdata'):
                buf += header + RES_XML_CDATA(proto=elt.cdata).pack()
        return buf

    def from_axml(buff : bytes, proto=None):
        """Convert ResourceXML buffer to ResourceXML object

        Args:
            buff (bytes): buffer contain ResourceXML object

        Returns:
            tuple[pyaxml.ResourceXML, bytes]: return ResourceXML element and buffer offset at the end of the reading
        """
        xml = ResourceXML()
        if proto:
            xml.proto = proto
        while len(buff) > 0:
            elt = axml_pb2.XMLElement()
            hnd, buff = AXMLHeader.from_axml(buff, proto=elt.header)
            if hnd.proto.type == axml_pb2.RES_XML_START_ELEMENT_TYPE:
                _, buff2 = RES_XML_START_ELEMENT.from_axml(buff, proto=elt.start_elt)
            elif hnd.proto.type == axml_pb2.RES_XML_END_ELEMENT_TYPE:
                _, buff2 = RES_XML_END_ELEMENT.from_axml(buff, proto=elt.end_elt)
            elif hnd.proto.type == axml_pb2.RES_XML_START_NAMESPACE_TYPE:
                _, buff2 = RES_XML_START_NAMESPACE.from_axml(buff, proto=elt.start_ns)
            elif hnd.proto.type == axml_pb2.RES_XML_END_NAMESPACE_TYPE:
                _, buff2 = RES_XML_END_NAMESPACE.from_axml(buff, proto=elt.end_ns)
            elif hnd.proto.type == axml_pb2.RES_XML_CDATA_TYPE:
                _, buff2 = RES_XML_CDATA.from_axml(buff, proto=elt.cdata)
            else:
                raise ValueError("RES_XML element header incorrect type")
            buff = buff[hnd.proto.size-hnd.proto.header_size+8:]
            if buff != buff2:
                logging.warning(f"Size of resourceXML element incorrect from type {hnd.proto.type} the size difference is {len(buff2) - len(buff)}")
            xml.proto.elts.append(elt)
        return xml, buff


##############################################################################
#
#                              ARSC OBJECT
#
##############################################################################

class ARSC:

    def __init__(self, proto : axml_pb2.ARSC = None):
        """_summary_

        Args:
            proto (axml_pb2.AXML, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.ARSC()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self, recursive=True):
        """Compute all fields to have all AXML elements
        """
        if recursive:
            s = StringBlocks(proto=self.proto.stringblocks)
            s.compute(update_size=True)
            self.proto.stringblocks.CopyFrom(s.proto)
            for i in range(len(self.proto.restablespackage)):
                package = AXML_Res_Table_Package(proto=self.proto.restablespackage[i])
                package.compute(recursive=recursive)
                self.proto.restablespackage[i].CopyFrom(package.proto)
            
        self.proto.header_res.hnd.size = len(self.pack())
        self.proto.header_res.package_count = len(self.proto.restablespackage)

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        sb_pack = StringBlocks(proto=self.proto.stringblocks).pack()
        header_res = AXMLHeader_RES_TABLE(proto=self.proto.header_res).pack()
        packages = b""
        for package in self.proto.restablespackage:
            packages += AXML_Res_Table_Package(proto=package).pack()
        return header_res + sb_pack + packages
    
    def from_axml(buff : str, proto = None):
        """read an AXML ARSC file to convert in pyaxml.ARSC object

        Args:
            buff (str): the string buffer to read

        Returns:
            ARSC: the ARSC object
            str: index of the reading string, if it's a valid file it should be the EOF.
        """
        arsc = ARSC()
        if proto:
            arsc.proto = proto
        header, buff = AXMLHeader_RES_TABLE.from_axml(buff, proto=arsc.proto.header_res)
        _, buff = StringBlocks.from_axml(buff, proto=arsc.proto.stringblocks)
        for i in range(header.proto.package_count):
            restablepackage, buff = AXML_Res_Table_Package.from_axml(buff)
            arsc.proto.restablespackage.append(restablepackage.proto)
            

        return arsc, buff
    
    def convert_id(type_id : int, id : int) -> int:
        """convert id and type to a general id used on AXML file to refer to resources

        Args:
            type_id (int): type of value (xml, string, etc.)
            id (int): index from the list of type value

        Returns:
            int: the id built
        """
        return 0x7f000000 | (type_id & 0xff) << 16 | type_id & 0xff00 | id

    def get_type_from_id(id : int) -> int:
        return (id & 0xff0000) >> 16 | id & 0xff00
    
    def get_local_id_from_id(id : int) -> int:
        return id & 0xff
    
    def get_id_public(self, package : str, type_ : str, name : str) -> tuple[int, int] | None:
        """get ID public from resource

        Args:
            package (str): package name
            type_ (str): type string
            name (str): name of value

        Returns:
            tuple[int, int] | None: return the id and the stringblock index of the value
        """
        for p in self.proto.restablespackage:
            n2 = p.name.split('\x00')[0]
            if n2 == package:
                for r in p.restypes:
                    if r.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                        for id in range(len(r.typetype.tables)):
                            table = r.typetype.tables[id]
                            index= table.index
                            n = StringBlocks(proto=p.key_sp_string).decode_str(index)
                            t = StringBlocks(proto=p.type_sp_string).decode_str(r.typetype.id-1)
                            if n == name and t == type_:
                                return ARSC.convert_id(r.typetype.id, id), table.key.data
        return None
    
    def get_id(self, package : str, rid : int):
        for p in self.proto.restablespackage:
            n2 = p.name.split('\x00')[0]
            if n2 == package:
                for r in p.restypes:
                    if r.hnd.type != axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                        continue
                    if r.typetype.id != ARSC.get_type_from_id(rid):
                        continue
                    local_id = ARSC.get_local_id_from_id(rid)
                    if local_id >= len(r.typetype.tables):
                        continue
                    table = r.typetype.tables[local_id]
                    n = StringBlocks(proto=p.key_sp_string).decode_str(table.index)
                    t = StringBlocks(proto=p.type_sp_string).decode_str(r.typetype.id-1)
                    return t, n, rid
        return None, None, None
    
    def get_resource_xml_name(self, r_id:int, package:Union[str,None]=None) -> str:
        if package:
            resource, name, i_id = self.get_id(package, r_id)
            if not i_id:
                return None
            return "@{}/{}".format(resource, name)
        else:
            for p in self.get_packages():
                r, n, i_id = self.get_id(p, r_id)
                if i_id:
                    # found the resource in this package
                    package = p
                    resource = r
                    name = n
                    break
            if not package:
                return None
            else:
                return "@{}:{}/{}".format(package, resource, name)
    
    def get_value(self, package : str, rid : int):
        general_st = StringBlocks(proto=self.proto.stringblocks)
        for p in self.proto.restablespackage:
            n2 = p.name.split('\x00')[0]
            if n2 == package:
                for r in p.restypes:
                    if r.hnd.type != axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                        continue
                    if r.typetype.id != ARSC.get_type_from_id(rid):
                        continue
                    local_id = ARSC.get_local_id_from_id(rid)
                    if local_id >= len(r.typetype.tables):
                        continue
                    table = r.typetype.tables[local_id]
                    if table.key.data_type == 3:
                        return general_st.decode_str(table.key.data)

    
    
    def add_id_public(self, package : str, type_ : str, name : str, path : str) -> int | None:
        """Add a new id in public string on ARSC resource

        Args:
            package (str): target package
            type_ (str): type of public element
            name (str): name of public element
            path (str): value of element

        Returns:
            int | None: return the id injected
        """
        for p in self.proto.restablespackage:
            n2 = p.name.split('\x00')[0]
            if n2 == package:
                s = StringBlocks(proto=self.proto.stringblocks)
                id_path = s.get(path)
                self.proto.stringblocks.CopyFrom(s.proto)
                res = AXML_Res_Table_Package(proto=p)
                ret = res.add_id_public(type_, name, id_path)
                return ret
        return None

    def list_packages(self):
        """print all package content
        """
        ret = ""
        general_st = StringBlocks(proto=self.proto.stringblocks)
        for package in self.proto.restablespackage:
            #ret += f"{package.name}\n"
            for r in package.restypes:
                if r.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                    for id in range(len(r.typetype.tables)):
                        table = r.typetype.tables[id]
                        index= table.index
                        name = StringBlocks(proto=package.key_sp_string).decode_str(index)
                        type_ = StringBlocks(proto=package.type_sp_string).decode_str(r.typetype.id-1)
                        identifiant = ARSC.convert_id(r.typetype.id, id)
                        if table.key.data_type == 3:
                            data = general_st.decode_str(table.key.data)
                        else:
                            data = hex(table.key.data)
                        data_size = table.key.size
                        ret += f"<public type=\"{type_}\" name=\"{name}\" id=\"{hex(identifiant)}\" data={data} data_size={data_size}/>\n"
        return ret
    
    def get_packages(self) -> list[str]:
        """get in a list all package name of the resources.

        Returns:
            list[str]: the list of all packages
        """
        packages = []
        for p in self.proto.restablespackage:
            packages.append(p.name.split('\x00')[0])
        return packages
    
    def get_type_configs(self, package_name, type_name=None):
        if package_name is None:
            package_name = self.get_packages()[0]
        result = []

        for restype in self.proto.restablespackage[0].restypes:
            if restype.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                t_name = StringBlocks(proto=self.proto.restablespackage[0].type_sp_string).decode_str(restype.typetype.id - 1) 
                if type_name is None or t_name == type_name:
                    result[t_name].append(restype.typetype.config)

        return result

    def get_res_configs(self, rid:int, config=None, fallback:bool=True) -> list:

        if not rid:
            raise ValueError("'rid' should be set")
        if not isinstance(rid, int):
            raise ValueError("'rid' must be an int")
        res = []
        p=self.proto.restablespackage[0]
        for r in p.restypes:
            if r.hnd.type != axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                continue
            if r.typetype.id != ARSC.get_type_from_id(rid):
                continue
            local_id = ARSC.get_local_id_from_id(rid)
            if local_id >= len(r.typetype.tables):
                continue
            table = r.typetype.tables[local_id]
            res.append(ARSCResTableConfig(proto=r.typetype.config), ARSCResTableEntry(proto=table))
        return res
    
    def get_resolved_res_configs(self, rid:int, config=None) -> list[tuple]:
        """
        Return a list of resolved resource IDs with their corresponding configuration.
        It has a similar return type as :meth:`get_res_configs` but also handles complex entries
        and references.
        Also instead of returning :class:`ARSCResTableEntry` in the tuple, the actual values are resolved.

        This is the preferred way of resolving resource IDs to their resources.

        :param int rid: the numerical ID of the resource
        :param ARSCTableResConfig config: the desired configuration or None to retrieve all
        :return: A list of tuples of (ARSCResTableConfig, str)
        """
        resolver = ARSC.ResourceResolver(self, config)
        return resolver.resolve(rid)
    
    class ResourceResolver:
        """
        Resolves resources by ID and configuration.
        This resolver deals with complex resources as well as with references.
        """
        def __init__(self, android_resources, config=None) -> None:
            """
            :param ARSCParser android_resources: A resource parser
            :param ARSCResTableConfig config: The desired configuration or None to resolve all.
            """
            self.resources = android_resources
            self.wanted_config = config

        def resolve(self, res_id: int) -> list:
            """
            the given ID into the Resource and returns a list of matching resources.

            :param int res_id: numerical ID of the resource
            :return: a list of tuples of (ARSCResTableConfig, str)
            """
            result = []
            self._resolve_into_result(result, res_id, self.wanted_config)
            return result

        def _resolve_into_result(self, result, res_id, config):
            # First: Get all candidates
            configs = self.resources.get_res_configs(res_id, config)

            for config, ate in configs:
                # deconstruct them and check if more candidates are generated
                self.put_ate_value(result, ate, config)

        def put_ate_value(self, result: list, ate:axml_pb2.ARSCResTableEntry, config) -> None:
            """
            Put a ResTableEntry into the list of results
            :param list result: results array
            :param ARSCResTableEntry ate:
            :param ARSCResTableConfig config:
            :return:
            """
            if ate.is_complex():
                complex_array = []
                result.append((config, complex_array))
                for _, item in ate.item.items:
                    self.put_item_value(complex_array, item, config, ate, complex_=True)
            else:
                self.put_item_value(result, ate.key, config, ate, complex_=False)

        def put_item_value(self, result:list, item, config, parent, complex_:bool)->None:
            """
            Put the tuple (ARSCResTableConfig, resolved string) into the result set

            :param list result: the result set
            :param ARSCResStringPoolRef item:
            :param ARSCResTableConfig config:
            :param ARSCResTableEntry parent: the originating entry
            :param bool complex_: True if the originating :class:`ARSCResTableEntry` was complex
            :return:
            """
            if item.is_reference():
                res_id = item.proto.data
                if res_id:
                    # Infinite loop detection:
                    # TODO should this stay here or should be detect the loop much earlier?
                    #if res_id == parent.mResId: # mResId == AXML_Res_Table_Package.id
                    #    logger.warning("Infinite loop detected at resource item {}. It references itself!".format(parent))
                    #    return

                    self._resolve_into_result(result, item.proto.data, self.wanted_config)
            else:
                if complex_:
                    if item.proto.data_type == TypedValue.TYPE_STRING:
                        v = str(item.proto.value) # TODO string
                    else:
                        v = TypedValue.coerceToString(t, item.proto.data)
                    result.append(v)
                else:
                    result.append((config, item.format_value()))

            
                               

class AXML_Res_Table_Package:

    def __init__(self, proto : axml_pb2.AXML_Res_Table_Package = None):
        """_summary_

        Args:
            proto (axml_pb2.AXML, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.AXML_Res_Table_Package()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self, recursive : bool = True):
        """Compute all fields to have all AXML elements

        Args:
            recursive (bool, optional): need to recompute field recursively. Defaults to True.
        """

        if recursive:
            type_sp_string = StringBlocks(proto=self.proto.type_sp_string)
            type_sp_string.compute(update_size=True)
            self.proto.type_sp_string.CopyFrom(type_sp_string.proto)
            
            key_sp_string =  StringBlocks(proto=self.proto.key_sp_string)
            key_sp_string.compute(update_size=True)
            self.proto.key_sp_string.CopyFrom(key_sp_string.proto)

            for restype in self.proto.restypes:
                if restype.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_SPEC_TYPE:
                    t = ARSCResTypeSpec(proto=restype.typespec)
                    t.compute(restype.hnd)
                    restype.typespec.CopyFrom(t.proto)
                elif restype.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                    t = ARSCResTypeType(proto=restype.typetype)
                    t.compute(restype.hnd)
                    restype.hnd.header_size = 20 + len(ARSCResTableConfig(proto=t.proto.config).pack())
                    restype.typetype.CopyFrom(t.proto)
        
        for restype in self.proto.restypes:
            if restype.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_SPEC_TYPE:
                restype.hnd.size = len(ARSCResTypeSpec(proto=restype.typespec).pack()) + AXML_HEADER_SIZE
            elif restype.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                restype.hnd.size = len(ARSCResTypeType(proto=restype.typetype).pack()) + AXML_HEADER_SIZE #- restype.hnd.header_size + AXML_HEADER_SIZE

        # TODO analyse if it is needed
        type_sp_string = StringBlocks(proto=self.proto.type_sp_string).pack()
        self.proto.typeStrings = self.proto.hnd.header_size
        self.proto.keyStrings = self.proto.typeStrings + len(type_sp_string)
        
        self.proto.hnd.size = len(self.pack())

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        header = AXMLHeader(proto=self.proto.hnd).pack()
        name = self.proto.name.encode('utf-16')[2:]
        name.ljust(256, b"\x00")
        type_sp_string = StringBlocks(proto=self.proto.type_sp_string).pack()
        key_sp_string =  StringBlocks(proto=self.proto.key_sp_string).pack()
        data = b""
        for restype in self.proto.restypes:
            hnd = AXMLHeader(proto=restype.hnd)
            data += hnd.pack()
            if hnd.proto.type == axml_pb2.ResType.RES_TABLE_TYPE_SPEC_TYPE:
                d = ARSCResTypeSpec(proto=restype.typespec).pack()
                data += d
            elif hnd.proto.type == axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                d = ARSCResTypeType(proto=restype.typetype).pack()
                data += d
        return header + pack("<L", self.proto.id) + name + pack("<LLLL", self.proto.typeStrings, self.proto.lastPublicType, self.proto.keyStrings, self.proto.lastPublicKey) + self.proto.padding + type_sp_string + key_sp_string + data
    
    def from_axml(buff : bytes, proto=None):
        """Convert AXML_Res_Table_Package buffer to AXML_Res_Table_Package object

        Args:
            buff (bytes): buffer contain AXML_Res_Table_Package object

        Returns:
            tuple[pyaxml.AXML_Res_Table_Package, bytes]: return AXML_Res_Table_Package element and buffer offset at the end of the reading
        """
        content = buff
        res_table_package = AXML_Res_Table_Package()
        if proto:
            res_table_package.proto = proto
        header, buff = AXMLHeader.from_axml(buff, proto=res_table_package.proto.hnd)
        rest = content[header.proto.size:]
        content = content[:header.proto.size]
        #buff = buff[32-8:]
        res_table_package.proto.id = unpack("<L", buff[:4])[0]
        buff = buff[4:]
        res_table_package.proto.name = buff[:256].decode('utf-16')
        buff = buff[256:]
        res_table_package.proto.typeStrings, res_table_package.proto.lastPublicType, \
            res_table_package.proto.keyStrings, res_table_package.proto.lastPublicKey = \
            unpack("<LLLL", buff[:4*4])
        buff = buff[4*4:]

        t_str_off = len(content[res_table_package.proto.typeStrings:])
        k_str_off = len(content[res_table_package.proto.keyStrings:])
        if t_str_off > k_str_off:
            len_pad = len(buff)-t_str_off
        else:
            len_pad = len(buff)-k_str_off
        res_table_package.proto.padding = buff[:len_pad]

        

        _, at = StringBlocks.from_axml(content[res_table_package.proto.typeStrings:], proto=res_table_package.proto.type_sp_string)

        _, ak = StringBlocks.from_axml(content[res_table_package.proto.keyStrings:], proto=res_table_package.proto.key_sp_string)


        if len(ak) < len(at):
            content = ak
        else:
            content = at
        

        while len(content) > 0:
            spec = axml_pb2.ARSCResType()
            hdr, _ = AXMLHeader.from_axml(content, proto=spec.hnd)
            if hdr.proto.type == axml_pb2.ResType.RES_TABLE_TYPE_SPEC_TYPE:
                _, _ = ARSCResTypeSpec.from_axml(content[8:hdr.proto.size], proto=spec.typespec)
                res_table_package.proto.restypes.append(spec)
            elif hdr.proto.type == axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                _, _ = ARSCResTypeType.from_axml(content[8:hdr.proto.size], proto=spec.typetype)
                res_table_package.proto.restypes.append(spec)
            else:
                print("other types ??")
            content = content[hdr.proto.size:]


        return res_table_package, rest
    
    def set_spec_entry(self, id : int, entry : int, index : int):
        """Add a spec entry

        Args:
            id (int): id of spec entry
            entry (int): _description_
            index (int): index in typetype stringblock of the element to set
        """
        for r in self.proto.restypes:
            if r.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_SPEC_TYPE and r.typespec.id == id:
                if len(r.typespec.entries) < index:
                    r.typespec.entries[index] = entry
                else:
                    while index > len(r.typespec.entries):
                        r.typespec.entries.append(0)
                    r.typespec.entries.append(entry)
    
    def add_id_public(self, type_ : str, name : str, id_path : int):
        """Add a public id in ARSC

        Args:
            type_ (str): type of public element
            name (str): name of public element
            id_path (int): id of element value to add in public

        Returns:
            _type_: return the id of this element
        """
        for r in self.proto.restypes:
            if r.hnd.type == axml_pb2.ResType.RES_TABLE_TYPE_TYPE:
                t = StringBlocks(proto=self.proto.type_sp_string).decode_str(r.typetype.id-1)
                if t == type_:
                    st_key = StringBlocks(proto=self.proto.key_sp_string)
                    spec = ARSCResTableEntry.create_element(st_key.get(name), id_path)
                    self.proto.key_sp_string.CopyFrom(st_key.proto)
                    self.set_spec_entry(r.typetype.id, 0, len(r.typetype.tables))
                    r.typetype.tables.append(spec.proto)
                    return ARSC.convert_id(r.typetype.id, len(r.typetype.tables)-1)
        
        
        st_type = StringBlocks(proto=self.proto.type_sp_string)
        id = st_type.get(type_)
        typetype = ARSCResTypeType.create_element(id=id+1)
        r = axml_pb2.ARSCResType()
        r.hnd.CopyFrom(AXMLHeader(axml_pb2.ResType.RES_TABLE_TYPE_TYPE).proto)
        r.typetype.CopyFrom(typetype.proto)
        
        st_key = StringBlocks(proto=self.proto.key_sp_string)
        spec = ARSCResTableEntry.create_element(st_key.get(name), id_path)
        self.proto.key_sp_string.CopyFrom(st_key.proto)
        r.typetype.tables.append(spec.proto)

        r_spec = axml_pb2.ARSCResType()
        r_spec.hnd.CopyFrom(AXMLHeader(axml_pb2.ResType.RES_TABLE_TYPE_SPEC_TYPE).proto)
        r_spec.hnd.header_size = 16
        r_spec.typespec.id = id+1

        self.proto.restypes.append(r_spec)
        self.proto.restypes.append(r)
        self.set_spec_entry(id+1, 0, 0)
        # TODO not appear on Androguard but type exist
        return ARSC.convert_id(r.typetype.id, len(r.typetype.tables)-1)
        

class ARSCResTypeType:

    def __init__(self, proto : axml_pb2.ARSCResTypeType = None):
        """_summary_

        Args:
            proto (axml_pb2.ARSCResTypeType, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.ARSCResTypeType()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self, hnd : axml_pb2.AXMLHeader, recursive=True):
        """Compute all fields to have all ARSCResTypeType elements

        Args:
            hnd (axml_pb2.AXMLHeader): header of ARSCResTypeType element
            recursive (bool, optional): need to compute all field recursively. Defaults to True.
        """
        cur = 0
        index_cur = 0
        for i in self.proto.tables:
            if len(self.proto.entries) <= index_cur:
                self.proto.entries.append(cur)
            else:
                while self.proto.entries[index_cur] == 0xffffffff:
                    index_cur+=1
                self.proto.entries[index_cur] = cur
            index_cur += 1
            cur += len(ARSCResTableEntry(proto=i).pack())
        self.proto.entryCount = len(self.proto.entries)
        self.proto.entryStart = hnd.header_size + 4 * self.proto.entryCount

        pass

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        head = pack("<BBHII", self.proto.id, self.proto.flags, self.proto.reserved, self.proto.entryCount, self.proto.entryStart)
        config = ARSCResTableConfig(proto=self.proto.config).pack()
        data = b""
        for i in self.proto.entries:
            data += pack('<I', i)
        for i in self.proto.tables:
            data += ARSCResTableEntry(proto=i).pack() 
        return head + config + data
    
    def from_axml(buff : bytes, proto = None):
        """Convert ARSCResTypeType buffer to ARSCResTypeType object

        Args:
            buff (bytes): buffer contain ARSCResTypeType object

        Returns:
            tuple[pyaxml.ARSCResTypeType, bytes]: return ARSCResTypeType element and buffer offset at the end of the reading
        """
        res_table_typespec = ARSCResTypeType()
        if proto:
            res_table_typespec.proto = proto
        res_table_typespec.proto.id, res_table_typespec.proto.flags, res_table_typespec.proto.reserved, res_table_typespec.proto.entryCount, res_table_typespec.proto.entryStart  = unpack("<BBHII", buff[:12])
        buff = buff[12:]  
        _, buff = ARSCResTableConfig.from_axml(buff, proto=res_table_typespec.proto.config)

        for i in range(res_table_typespec.proto.entryCount):
            res_table_typespec.proto.entries.append(unpack('<I', buff[:4])[0])
            buff = buff[4:]
        
        entrie_cur = buff
        for i in res_table_typespec.proto.entries:
            if i == 0xffffffff:
                continue # TODO handle item with -1 entry
            table, buff = ARSCResTableEntry.from_axml(entrie_cur[i:])
            res_table_typespec.proto.tables.append(table.proto)
        return res_table_typespec, buff
    
    def create_element(id : int):
        typetype = ARSCResTypeType()
        typetype.proto.id = id
        typetype.proto.flags = 0
        typetype.proto.reserved = 0
        typetype.proto.entryCount = 0
        typetype.proto.config.CopyFrom(ARSCResTableConfig().proto)
        typetype.proto.entryStart = AXML_HEADER_SIZE + 64 + 12
        return typetype
    

class ARSCResTableEntry:

    # If set, this is a complex entry, holding a set of name/value
    # mappings.  It is followed by an array of ResTable_map structures.
    FLAG_COMPLEX = 1

    # If set, this resource has been declared public, so libraries
    # are allowed to reference it.
    FLAG_PUBLIC = 2

    # If set, this is a weak resource and may be overriden by strong
    # resources of the same name/type. This is only useful during
    # linking with other resource tables.
    FLAG_WEAK = 4

    def __init__(self, proto : axml_pb2.ARSCResTableEntry = None):
        """_summary_

        Args:
            proto (axml_pb2.ARSCResTableEntry, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.ARSCResTableEntry()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self):
        """Compute all fields to have all ARSCResTableEntry elements
        """
        pass

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        data = pack('<HHI', self.proto.size, self.proto.flags, self.proto.index)
        if self.is_complex():
            data += ARSCComplex(proto=self.proto.item).pack()
        else:
            data += ARSCResStringPoolRef(proto=self.proto.key).pack()
        
        return  data
    
    def is_public(self) -> bool:
        """check if element is public

        Returns:
            bool: True if element is public
        """
        return (self.proto.flags & self.FLAG_PUBLIC) != 0

    def is_complex(self) -> bool:
        """check if element is complex

        Returns:
            bool: True if element is complex
        """
        return (self.proto.flags & self.FLAG_COMPLEX) != 0

    def is_weak(self) -> bool:
        """check if element is weak

        Returns:
            bool: True if element is weak
        """
        return (self.proto.flags & self.FLAG_WEAK) != 0
    
    def create_element(index_name : int, data : int):
        """Create a new ARSCResTableEntry element

        Args:
            index_name (int): The index element
            data (int): index of data element

        Returns:
            pyaxml.ARSCResTableEntry: _description_
        """
        spec = ARSCResTableEntry()
        spec.proto.size = 8
        spec.proto.index = index_name
        spec.proto.key.size = 8
        spec.proto.key.data_type = 3
        spec.proto.key.data = data
        return spec
    
    def from_axml(buff : bytes, proto = None):
        """Convert ARSCResTableEntry buffer to ARSCResTableEntry object

        Args:
            buff (bytes): buffer contain ARSCResTableEntry object

        Returns:
            tuple[pyaxml.ARSCResTableEntry, bytes]: return ARSCResTableEntry element and buffer offset at the end of the reading
        """
        table = ARSCResTableEntry()
        if proto:
            table.proto = proto
        table.proto.size, table.proto.flags, table.proto.index = unpack('<HHI', buff[:8])
        buff = buff[8:]
        if table.is_complex():
            _, buff =  ARSCComplex.from_axml(buff, proto=table.proto.item)
        else:
            # If FLAG_COMPLEX is not set, a Res_value structure will follow
            _, buff = ARSCResStringPoolRef.from_axml(buff, proto=table.proto.key)
        #table.proto.input = buff[8:]
        return table, buff  
    

class ARSCComplex:
   
    def __init__(self, proto : axml_pb2.ARSCComplex = None):
        """Initialize ARSCComplex element 

        Args:
            proto (axml_pb2.ARSCComplex, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.ARSCComplex()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self):
        """Compute all fields to have all AXML elements
        """
        pass

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        data = pack('<II', self.proto.id_parent, self.proto.count)
        for item in self.proto.items:
            data += pack('<I', item.id)
            data += ARSCResStringPoolRef(proto=item.data).pack()
        return data
    
    def from_axml(buff : bytes, proto=None):
        """Convert ARSCComplex buffer to ARSCComplex object

        Args:
            buff (bytes): buffer contain ARSCComplex object

        Returns:
            tuple[pyaxml.ARSCComplex, bytes]: return ARSCComplex element and buffer offset at the end of the reading
        """
        complex = ARSCComplex()
        if proto:
            complex.proto = proto

        complex.proto.id_parent, complex.proto.count = unpack('<II', buff[:8])
        buff = buff[8:]
        # Parse self.count number of `ResTable_map`
        # these are structs of ResTable_ref and Res_value
        # ResTable_ref is a uint32_t.
        for i in range(0, complex.proto.count):
            item = axml_pb2.ItemComplex()
            item.id = unpack('<I', buff[:4])[0]
            buff = buff[4:]
            _, buff = ARSCResStringPoolRef.from_axml(buff, proto=item.data)
            complex.proto.items.append(item)

        return complex, buff

class ARSCResStringPoolRef:
   
    def __init__(self, proto : axml_pb2.ARSCResStringPoolRef = None):
        """_summary_

        Args:
            proto (axml_pb2.ARSCResStringPoolRef, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.ARSCResStringPoolRef()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self):
        """Compute all fields to have all AXML elements
        """
        pass

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        data = pack('<HBBI', self.proto.size, self.proto.res0, self.proto.data_type, self.proto.data)
        return data
    
    def from_axml(buff : bytes, proto=None):
        """Convert ARSCResStringPoolRef buffer to ARSCResStringPoolRef object

        Args:
            buff (bytes): buffer contain ARSCResStringPoolRef object

        Returns:
            tuple[pyaxml.ARSCResStringPoolRef, bytes]: return ARSCResStringPoolRef element and buffer offset at the end of the reading
        """
        ref = ARSCResStringPoolRef()
        if proto:
            ref.proto = proto

        ref.proto.size, ref.proto.res0, ref.proto.data_type, ref.proto.data  = unpack('<HBBI', buff[:8])
        buff = buff[8:]
        return ref, buff
    
    def is_reference(self) -> bool:
        """
        Returns True if the Res_value is actually a reference to another resource
        """
        return self.proto.data_type == TypedValue.TYPE_REFERENCE

class ARSCResTableConfig:
    
    #http://aospxref.com/android-13.0.0_r3/xref/frameworks/base/libs/androidfw/include/androidfw/ResourceTypes.h#946

    ORIENTATION_ANY = AConfiguration.ORIENTATION_ANY
    ORIENTATION_PORT = AConfiguration.ORIENTATION_PORT
    ORIENTATION_LAND = AConfiguration.ORIENTATION_LAND
    ORIENTATION_SQUARE = AConfiguration.ORIENTATION_SQUARE

    TOUCHSCREEN_ANY = AConfiguration.TOUCHSCREEN_ANY
    TOUCHSCREEN_NOTOUCH = AConfiguration.TOUCHSCREEN_NOTOUCH
    TOUCHSCREEN_STYLUS = AConfiguration.TOUCHSCREEN_STYLUS
    TOUCHSCREEN_FINGER = AConfiguration.TOUCHSCREEN_FINGER

    DENSITY_DEFAULT = AConfiguration.DENSITY_DEFAULT
    DENSITY_LOW = AConfiguration.DENSITY_LOW
    DENSITY_MEDIUM = AConfiguration.DENSITY_MEDIUM
    DENSITY_TV = AConfiguration.DENSITY_TV
    DENSITY_HIGH = AConfiguration.DENSITY_HIGH
    DENSITY_XHIGH = AConfiguration.DENSITY_XHIGH
    DENSITY_XXHIGH = AConfiguration.DENSITY_XXHIGH
    DENSITY_XXXHIGH = AConfiguration.DENSITY_XXXHIGH
    DENSITY_ANY = AConfiguration.DENSITY_ANY
    DENSITY_NONE = AConfiguration.DENSITY_NONE

    KEYBOARD_ANY = AConfiguration.KEYBOARD_ANY
    KEYBOARD_NOKEYS = AConfiguration.KEYBOARD_NOKEYS
    KEYBOARD_QWERTY = AConfiguration.KEYBOARD_QWERTY
    KEYBOARD_12KEY = AConfiguration.KEYBOARD_12KEY

    NAVIGATION_ANY = AConfiguration.NAVIGATION_ANY
    NAVIGATION_NONAV = AConfiguration.NAVIGATION_NONAV
    NAVIGATION_DPAD = AConfiguration.NAVIGATION_DPAD
    NAVIGATION_TRACKBALL = AConfiguration.NAVIGATION_TRACKBALL
    NAVIGATION_WHEEL = AConfiguration.NAVIGATION_WHEEL

    MASK_KEYSHIDDEN = 0x0003
    KEYSHIDDEN_ANY = AConfiguration.KEYSHIDDEN_ANY
    KEYSHIDDEN_NO = AConfiguration.KEYSHIDDEN_NO
    KEYSHIDDEN_YES = AConfiguration.KEYSHIDDEN_YES
    KEYSHIDDEN_SOFT = AConfiguration.KEYSHIDDEN_SOFT

    MASK_NAVHIDDEN = 0x000c
    SHIFT_NAVHIDDEN = 2
    NAVHIDDEN_ANY = AConfiguration.NAVHIDDEN_ANY << SHIFT_NAVHIDDEN
    NAVHIDDEN_NO = AConfiguration.NAVHIDDEN_NO << SHIFT_NAVHIDDEN
    NAVHIDDEN_YES = AConfiguration.NAVHIDDEN_YES << SHIFT_NAVHIDDEN

    SCREENWIDTH_ANY = 0
    SCREENHEIGHT_ANY = 0
    SDKVERSION_ANY = 0
    MINORVERSION_ANY = 0

    MASK_SCREENSIZE = 0x0f
    SCREENSIZE_ANY = AConfiguration.SCREENSIZE_ANY
    SCREENSIZE_SMALL = AConfiguration.SCREENSIZE_SMALL
    SCREENSIZE_NORMAL = AConfiguration.SCREENSIZE_NORMAL
    SCREENSIZE_LARGE = AConfiguration.SCREENSIZE_LARGE
    SCREENSIZE_XLARGE = AConfiguration.SCREENSIZE_XLARGE

    MASK_SCREENLONG = 0x30
    SHIFT_SCREENLONG = 4
    SCREENLONG_ANY = AConfiguration.SCREENLONG_ANY << SHIFT_SCREENLONG
    SCREENLONG_NO = AConfiguration.SCREENLONG_NO << SHIFT_SCREENLONG
    SCREENLONG_YES = AConfiguration.SCREENLONG_YES << SHIFT_SCREENLONG

    MASK_LAYOUTDIR = 0xC0
    SHIFT_LAYOUTDIR = 6
    LAYOUTDIR_ANY = AConfiguration.LAYOUTDIR_ANY << SHIFT_LAYOUTDIR
    LAYOUTDIR_LTR = AConfiguration.LAYOUTDIR_LTR << SHIFT_LAYOUTDIR
    LAYOUTDIR_RTL = AConfiguration.LAYOUTDIR_RTL << SHIFT_LAYOUTDIR

    MASK_UI_MODE_TYPE = 0x0f
    UI_MODE_TYPE_ANY = AConfiguration.UI_MODE_TYPE_ANY
    UI_MODE_TYPE_NORMAL = AConfiguration.UI_MODE_TYPE_NORMAL
    UI_MODE_TYPE_DESK = AConfiguration.UI_MODE_TYPE_DESK
    UI_MODE_TYPE_CAR = AConfiguration.UI_MODE_TYPE_CAR
    UI_MODE_TYPE_TELEVISION = AConfiguration.UI_MODE_TYPE_TELEVISION
    UI_MODE_TYPE_APPLIANCE = AConfiguration.UI_MODE_TYPE_APPLIANCE
    UI_MODE_TYPE_WATCH = AConfiguration.UI_MODE_TYPE_WATCH
    UI_MODE_TYPE_VR_HEADSET = AConfiguration.UI_MODE_TYPE_VR_HEADSET

    MASK_UI_MODE_NIGHT = 0x30
    SHIFT_UI_MODE_NIGHT = 4
    UI_MODE_NIGHT_ANY = AConfiguration.UI_MODE_NIGHT_ANY << SHIFT_UI_MODE_NIGHT
    UI_MODE_NIGHT_NO = AConfiguration.UI_MODE_NIGHT_NO << SHIFT_UI_MODE_NIGHT
    UI_MODE_NIGHT_YES = AConfiguration.UI_MODE_NIGHT_YES << SHIFT_UI_MODE_NIGHT

    MASK_SCREENROUND = 0x03
    SCREENROUND_ANY = AConfiguration.SCREENROUND_ANY
    SCREENROUND_NO = AConfiguration.SCREENROUND_NO
    SCREENROUND_YES = AConfiguration.SCREENROUND_YES

    MASK_WIDE_COLOR_GAMUT = 0x03
    WIDE_COLOR_GAMUT_ANY = AConfiguration.WIDE_COLOR_GAMUT_ANY
    WIDE_COLOR_GAMUT_NO = AConfiguration.WIDE_COLOR_GAMUT_NO
    WIDE_COLOR_GAMUT_YES = AConfiguration.WIDE_COLOR_GAMUT_YES

    MASK_HDR = 0x0c
    SHIFT_HDR = 2
    HDR_ANY = AConfiguration.HDR_ANY << SHIFT_HDR
    HDR_NO = AConfiguration.HDR_NO << SHIFT_HDR
    HDR_YES = AConfiguration.HDR_YES << SHIFT_HDR


    def __init__(self, proto : axml_pb2.ARSCResTableConfig = None):
        """_summary_

        Args:
            proto (axml_pb2.ARSCResTableConfig, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.ARSCResTableConfig()
            self.proto.size = 16
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self):
        """Compute all fields to have all AXML elements
        """
        pass

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        extra = b""
        if self.proto.HasField("input"):
            extra += pack('<I', self.proto.input)
            if self.proto.HasField("screenSize"):
                extra += pack('<I', self.proto.screenSize)
                if self.proto.HasField("version"):
                    extra += pack('<I', self.proto.version)
                    if self.proto.HasField("screenConfig"):
                        extra += pack('<I', self.proto.screenConfig)
                        if self.proto.HasField("screenSizeDp"):
                            extra += pack('<I', self.proto.screenSizeDp)
                            if self.proto.HasField("localeScript"):
                                extra += pack('<I', self.proto.localeScript)
                                if self.proto.HasField("localeVariant"):
                                    extra += pack('<I', self.proto.localeVariant)
                                    if self.proto.HasField("screenConfig2"):
                                        extra += pack('<I', self.proto.screenConfig2)
        extra += self.proto.padding
        return pack('<IIII', self.proto.size, self.proto.imsi, self.proto.locale, self.proto.screenType) + extra
    
    def from_axml(buff : bytes, proto=None):
        """Convert ARSCResTableConfig buffer to ARSCResTableConfig object

        Args:
            buff (bytes): buffer contain ARSCResTableConfig object

        Returns:
            tuple[pyaxml.ARSCResTableConfig, bytes]: return ARSCResTableConfig element and buffer offset at the end of the reading
        """
        config = ARSCResTableConfig()
        if proto:
            config.proto = proto
        config.proto.size, config.proto.imsi, config.proto.locale, config.proto.screenType = unpack('<IIII', buff[:16])
        off=0
        if config.proto.size >= 20:
            config.proto.input = unpack('<I', buff[16:20])[0]
            off += 4
        if config.proto.size >= 20 + off:
            config.proto.screenSize = unpack('<I', buff[16 + off:20 + off])[0]
            off += 4
        if config.proto.size >= 20 + off:
            config.proto.version = unpack('<I', buff[16 + off:20 + off])[0]
            off += 4
        if config.proto.size >= 20 + off:
            config.proto.screenConfig = unpack('<I', buff[16 + off:20 + off])[0]
            off += 4
        if config.proto.size >= 20 + off:
            config.proto.screenSizeDp = unpack('<I', buff[16 + off:20 + off])[0]
            off += 4
        if config.proto.size >= 20 + off:
            config.proto.localeScript = unpack('<I', buff[16 + off:20 + off])[0]
            off += 4
        if config.proto.size >= 20 + off:
            config.proto.localeVariant = unpack('<I', buff[16 + off:20 + off])[0]
            off += 4
        if config.proto.size >= 20 + off:
            config.proto.screenConfig2 = unpack('<I', buff[16 + off:20 + off])[0]
            off += 4
        config.proto.padding = buff[16+off:config.proto.size]
        return config, buff[config.proto.size:]
    
    def _unpack_language_or_region(self, char_in, char_base):
        char_out = ""
        if char_in[0] & 0x80:
            first = char_in[1] & 0x1f
            second = ((char_in[1] & 0xe0) >> 5) + ((char_in[0] & 0x03) << 3)
            third = (char_in[0] & 0x7c) >> 2
            char_out += chr(first + char_base)
            char_out += chr(second + char_base)
            char_out += chr(third + char_base)
        else:
            if char_in[0]:
                char_out += chr(char_in[0])
            if char_in[1]:
                char_out += chr(char_in[1])
        return char_out

    def _pack_language_or_region(self, char_in: str) -> list[int]:
        char_out = [0x00, 0x00]
        if len(char_in) != 2:
            return char_out
        char_out[0] = ord(char_in[0])
        char_out[1] = ord(char_in[1])
        return char_out

    def set_language_and_region(self, language_region):
        try:
            language, region = language_region.split("-r")
        except ValueError:
            language, region = language_region, None
        language_bytes = self._pack_language_or_region(language)
        if region:
            region_bytes = self._pack_language_or_region(region)
        else:
            region_bytes = [0x00, 0x00]
        self.proto.locale = language_bytes[0] | (language_bytes[1] << 8) | (region_bytes[0] << 16) | (region_bytes[1] << 24)

    def get_language_and_region(self) -> str:
        """
        Returns the combined language+region string or \x00\x00 for the default locale
        :return:
        """
        if self.proto.locale != 0:
            _language = self._unpack_language_or_region([self.proto.locale & 0xff, (self.proto.locale & 0xff00) >> 8, ], ord('a'))
            _region = self._unpack_language_or_region([(self.proto.locale & 0xff0000) >> 16, (self.proto.locale & 0xff000000) >> 24, ], ord('0'))
            return (_language + "-r" + _region) if _region else _language
        return "\x00\x00"

    def get_config_name_friendly(self) -> str:
        """
        Here for legacy reasons.

        use :meth:`~get_qualifier` instead.
        """
        return self.get_qualifier()

    def get_qualifier(self) -> str:
        """
        Return resource name qualifier for the current configuration.
        for example
        * `ldpi-v4`
        * `hdpi-v4`

        All possible qualifiers are listed in table 2 of https://developer.android.com/guide/topics/resources/providing-resources

        You can find how android process this at http://aospxref.com/android-13.0.0_r3/xref/frameworks/base/libs/androidfw/ResourceTypes.cpp#3243

        :return: str
        """
        res = []

        mcc = self.proto.imsi & 0xFFFF
        mnc = (self.proto.imsi & 0xFFFF0000) >> 16
        if mcc != 0:
            res.append("mcc%d" % mcc)
        if mnc != 0:
            res.append("mnc%d" % mnc)

        if self.proto.locale != 0:
            res.append(self.proto.get_language_and_region())

        screenLayout = self.proto.screenConfig & 0xff
        if (screenLayout & ARSCResTableConfig.MASK_LAYOUTDIR) != 0:
            if screenLayout & ARSCResTableConfig.MASK_LAYOUTDIR == ARSCResTableConfig.LAYOUTDIR_LTR:
                res.append("ldltr")
            elif screenLayout & ARSCResTableConfig.MASK_LAYOUTDIR == ARSCResTableConfig.LAYOUTDIR_RTL:
                res.append("ldrtl")
            else:
                res.append("layoutDir_%d" % (screenLayout & ARSCResTableConfig.MASK_LAYOUTDIR))

        smallestScreenWidthDp = (self.proto.screenConfig & 0xFFFF0000) >> 16
        if smallestScreenWidthDp != 0:
            res.append("sw%ddp" % smallestScreenWidthDp)

        screenWidthDp = self.proto.screenSizeDp & 0xFFFF
        screenHeightDp = (self.proto.screenSizeDp & 0xFFFF0000) >> 16
        if screenWidthDp != 0:
            res.append("w%ddp" % screenWidthDp)
        if screenHeightDp != 0:
            res.append("h%ddp" % screenHeightDp)

        if (screenLayout & ARSCResTableConfig.MASK_SCREENSIZE) != ARSCResTableConfig.SCREENSIZE_ANY:
            if screenLayout & ARSCResTableConfig.MASK_SCREENSIZE == ARSCResTableConfig.SCREENSIZE_SMALL:
                res.append("small")
            elif screenLayout & ARSCResTableConfig.MASK_SCREENSIZE == ARSCResTableConfig.SCREENSIZE_NORMAL:
                res.append("normal")
            elif screenLayout & ARSCResTableConfig.MASK_SCREENSIZE == ARSCResTableConfig.SCREENSIZE_LARGE:
                res.append("large")
            elif screenLayout & ARSCResTableConfig.MASK_SCREENSIZE == ARSCResTableConfig.SCREENSIZE_XLARGE:
                res.append("xlarge")
            else:
                res.append("screenLayoutSize_%d" % (screenLayout & ARSCResTableConfig.MASK_SCREENSIZE))
        if (screenLayout & ARSCResTableConfig.MASK_SCREENLONG) != 0:
            if screenLayout & ARSCResTableConfig.MASK_SCREENLONG == ARSCResTableConfig.SCREENLONG_NO:
                res.append("notlong")
            elif screenLayout & ARSCResTableConfig.MASK_SCREENLONG == ARSCResTableConfig.SCREENLONG_YES:
                res.append("long")
            else:
                res.append("screenLayoutLong_%d" % (screenLayout & ARSCResTableConfig.MASK_SCREENLONG))

        screenLayout2 = self.proto.screenConfig2 & 0xff
        if (screenLayout2 & ARSCResTableConfig.MASK_SCREENROUND) != 0:
            if screenLayout2 & ARSCResTableConfig.MASK_SCREENROUND == ARSCResTableConfig.SCREENROUND_NO:
                res.append("notround")
            elif screenLayout2 & ARSCResTableConfig.MASK_SCREENROUND == ARSCResTableConfig.SCREENROUND_YES:
                res.append("round")
            else:
                res.append("screenRound_%d" % (screenLayout2 & ARSCResTableConfig.MASK_SCREENROUND))

        colorMode = (self.proto.screenConfig2 & 0xff00) >> 8
        if (colorMode & ARSCResTableConfig.MASK_WIDE_COLOR_GAMUT) != 0:
            if colorMode & ARSCResTableConfig.MASK_WIDE_COLOR_GAMUT == ARSCResTableConfig.WIDE_COLOR_GAMUT_NO:
                res.append("nowidecg")
            elif colorMode & ARSCResTableConfig.MASK_WIDE_COLOR_GAMUT == ARSCResTableConfig.WIDE_COLOR_GAMUT_YES:
                res.append("widecg")
            else:
                res.append("wideColorGamut_%d" % (colorMode & ARSCResTableConfig.MASK_WIDE_COLOR_GAMUT))

        if (colorMode & ARSCResTableConfig.MASK_HDR) != 0:
            if colorMode & ARSCResTableConfig.MASK_HDR == ARSCResTableConfig.HDR_NO:
                res.append("lowdr")
            elif colorMode & ARSCResTableConfig.MASK_HDR == ARSCResTableConfig.HDR_YES:
                res.append("highdr")
            else:
                res.append("hdr_%d" % (colorMode & ARSCResTableConfig.MASK_HDR))

        orientation = self.proto.screenType & 0xff
        if orientation != ARSCResTableConfig.ORIENTATION_ANY:
            if orientation == ARSCResTableConfig.ORIENTATION_PORT:
                res.append("port")
            elif orientation == ARSCResTableConfig.ORIENTATION_LAND:
                res.append("land")
            elif orientation == ARSCResTableConfig.ORIENTATION_SQUARE:
                res.append("square")
            else:
                res.append("orientation_%d" % orientation)

        uiMode = (self.proto.screenConfig & 0xff00) >> 8
        if (uiMode & ARSCResTableConfig.MASK_UI_MODE_TYPE) != ARSCResTableConfig.UI_MODE_TYPE_ANY:
            ui_mode = uiMode & ARSCResTableConfig.MASK_UI_MODE_TYPE
            if ui_mode == ARSCResTableConfig.UI_MODE_TYPE_DESK:
                res.append("desk")
            elif ui_mode == ARSCResTableConfig.UI_MODE_TYPE_CAR:
                res.append("car")
            elif ui_mode == ARSCResTableConfig.UI_MODE_TYPE_TELEVISION:
                res.append("television")
            elif ui_mode == ARSCResTableConfig.UI_MODE_TYPE_APPLIANCE:
                res.append("appliance")
            elif ui_mode == ARSCResTableConfig.UI_MODE_TYPE_WATCH:
                res.append("watch")
            elif ui_mode == ARSCResTableConfig.UI_MODE_TYPE_VR_HEADSET:
                res.append("vrheadset")
            else:
                res.append("uiModeType_%d" % ui_mode)

        if (uiMode & ARSCResTableConfig.MASK_UI_MODE_NIGHT) != 0:
            if uiMode & ARSCResTableConfig.MASK_UI_MODE_NIGHT == ARSCResTableConfig.UI_MODE_NIGHT_NO:
                res.append("notnight")
            elif uiMode & ARSCResTableConfig.MASK_UI_MODE_NIGHT == ARSCResTableConfig.UI_MODE_NIGHT_YES:
                res.append("night")
            else:
                res.append("uiModeNight_%d" % (uiMode & ARSCResTableConfig.MASK_UI_MODE_NIGHT))

        density = (self.proto.screenType & 0xffff0000) >> 16
        if density != ARSCResTableConfig.DENSITY_DEFAULT:
            if density == ARSCResTableConfig.DENSITY_LOW:
                res.append("ldpi")
            elif density == ARSCResTableConfig.DENSITY_MEDIUM:
                res.append("mdpi")
            elif density == ARSCResTableConfig.DENSITY_TV:
                res.append("tvdpi")
            elif density == ARSCResTableConfig.DENSITY_HIGH:
                res.append("hdpi")
            elif density == ARSCResTableConfig.DENSITY_XHIGH:
                res.append("xhdpi")
            elif density == ARSCResTableConfig.DENSITY_XXHIGH:
                res.append("xxhdpi")
            elif density == ARSCResTableConfig.DENSITY_XXXHIGH:
                res.append("xxxhdpi")
            elif density == ARSCResTableConfig.DENSITY_NONE:
                res.append("nodpi")
            elif density == ARSCResTableConfig.DENSITY_ANY:
                res.append("anydpi")
            else:
                res.append("%ddpi" % (density))

        touchscreen = (self.proto.screenType & 0xff00) >> 8
        if touchscreen != ARSCResTableConfig.TOUCHSCREEN_ANY:
            if touchscreen == ARSCResTableConfig.TOUCHSCREEN_NOTOUCH:
                res.append("notouch")
            elif touchscreen == ARSCResTableConfig.TOUCHSCREEN_FINGER:
                res.append("finger")
            elif touchscreen == ARSCResTableConfig.TOUCHSCREEN_STYLUS:
                res.append("stylus")
            else:
                res.append("touchscreen_%d" % touchscreen)

        keyboard = self.proto.input & 0xff
        navigation = (self.proto.input & 0xff00) >> 8
        inputFlags = (self.proto.input & 0xff0000) >> 16

        if inputFlags & ARSCResTableConfig.MASK_KEYSHIDDEN != 0:
            input_flags = inputFlags & ARSCResTableConfig.MASK_KEYSHIDDEN
            if input_flags == ARSCResTableConfig.KEYSHIDDEN_NO:
                res.append("keysexposed")
            elif input_flags == ARSCResTableConfig.KEYSHIDDEN_YES:
                res.append("keyshidden")
            elif input_flags == ARSCResTableConfig.KEYSHIDDEN_SOFT:
                res.append("keyssoft")

        if keyboard != ARSCResTableConfig.KEYBOARD_ANY:
            if keyboard == ARSCResTableConfig.KEYBOARD_NOKEYS:
                res.append("nokeys")
            elif keyboard == ARSCResTableConfig.KEYBOARD_QWERTY:
                res.append("qwerty")
            elif keyboard == ARSCResTableConfig.KEYBOARD_12KEY:
                res.append("12key")
            else:
                res.append("keyboard_%d" % keyboard)

        if inputFlags & ARSCResTableConfig.MASK_NAVHIDDEN != 0:
            input_flags = inputFlags & ARSCResTableConfig.MASK_NAVHIDDEN
            if input_flags == ARSCResTableConfig.NAVHIDDEN_NO:
                res.append("navexposed")
            elif input_flags == ARSCResTableConfig.NAVHIDDEN_YES:
                res.append("navhidden")
            else:
                res.append("inputFlagsNavHidden_%d" % input_flags)

        if navigation != ARSCResTableConfig.NAVIGATION_ANY:
            if navigation == ARSCResTableConfig.NAVIGATION_NONAV:
                res.append("nonav")
            elif navigation == ARSCResTableConfig.NAVIGATION_DPAD:
                res.append("dpad")
            elif navigation == ARSCResTableConfig.NAVIGATION_TRACKBALL:
                res.append("trackball")
            elif navigation == ARSCResTableConfig.NAVIGATION_WHEEL:
                res.append("wheel")
            else:
                res.append("navigation_%d" % navigation)

        screenSize = self.proto.screenSize
        if screenSize != 0:
            screenWidth = self.screenSize & 0xffff
            screenHeight = (self.screenSize & 0xffff0000) >> 16
            res.append("%dx%d" % (screenWidth, screenHeight))

        version = self.proto.version
        if version != 0:
            sdkVersion = self.proto.version & 0xffff
            minorVersion = (self.proto.version & 0xffff0000) >> 16
            res.append("v%d" % sdkVersion)
            if minorVersion != 0:
                res.append(".%d" % minorVersion)

        return "-".join(res)

    def get_language(self) -> str:
        x = self.proto.locale & 0x0000ffff
        return chr(x & 0x00ff) + chr((x & 0xff00) >> 8)

    def get_country(self) -> str:
        x = (self.proto.locale & 0xffff0000) >> 16
        return chr(x & 0x00ff) + chr((x & 0xff00) >> 8)

    def get_density(self) -> str:
        x = ((self.proto.screenType >> 16) & 0xffff)
        return x

    def is_default(self) -> bool:
        """
        Test if this is a default resource, which matches all

        This is indicated that all fields are zero.
        :return: True if default, False otherwise
        """
        return all(map(lambda x: x == 0, self._get_tuple()))

    def _get_tuple(self):
        return (
            self.proto.imsi,
            self.proto.locale,
            self.proto.screenType,
            self.proto.input,
            self.proto.screenSize,
            self.proto.version,
            self.proto.screenConfig,
            self.proto.screenSizeDp,
            self.proto.screenConfig2,
        )

    def __hash__(self):
        return hash(self._get_tuple())

    def __eq__(self, other):
        return self._get_tuple() == other._get_tuple()

    def __repr__(self):
        return "<ARSCResTableConfig '{}'={}>".format(self.get_qualifier(), repr(self._get_tuple()))


class ARSCResTypeSpec:
    
    def __init__(self, proto : axml_pb2.ARSCResTypeSpec = None):
        """_summary_

        Args:
            proto (axml_pb2.ARSCResTypeSpec, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
        else:
            self.proto = axml_pb2.ARSCResTypeSpec()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto
    
    def compute(self, hnd : axml_pb2.AXMLHeader):
        """Compute all fields to have all AXML elements
        """
        self.proto.entryCount = len(self.proto.entries)
        pass

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        data = pack("<BBHI", self.proto.id, self.proto.res0, self.proto.res1, self.proto.entryCount)
        for entry in self.proto.entries:
            data += pack('<I', entry)
        return data
    
    def from_axml(buff : bytes, proto = None):
        """Convert ARSCResTypeSpec buffer to ARSCResTypeSpec object

        Args:
            buff (bytes): buffer contain ARSCResTypeSpec object

        Returns:
            tuple[pyaxml.ARSCResTypeSpec, bytes]: return ARSCResTypeSpec element and buffer offset at the end of the reading
        """
        res_table_typespec = ARSCResTypeSpec()
        if proto:
            res_table_typespec.proto = proto
        res_table_typespec.proto.id, res_table_typespec.proto.res0, res_table_typespec.proto.res1, res_table_typespec.proto.entryCount  = unpack("<BBHI", buff[:8])
        buff = buff[8:]        
        for i in range(res_table_typespec.proto.entryCount):
            res_table_typespec.proto.entries.append(unpack('<I', buff[:4])[0])
            buff = buff[4:]


        return res_table_typespec, buff


##############################################################################
#
#                              AXML OBJECT
#
##############################################################################

class AXML:

    def __init__(self, proto : axml_pb2.AXML = None):
        """_summary_

        Args:
            proto (axml_pb2.AXML, optional): _description_. Defaults to None.
        """
        if proto:
            self.proto = proto
            self.stringblocks = StringBlocks(proto=self.proto.stringblocks)
        else:
            self.proto = axml_pb2.AXML()
            self.stringblocks = StringBlocks()
    
    @property
    def get_proto(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.proto

    ###########################################
    #                                         #
    #           ENCODE from XML               #
    #                                         #
    ###########################################
    
    def from_xml(self, root):
        """Convert Xml to Axml object

        Args:
            root (etree.ElementBase): Xml representation of AXML object
        """
        
        self.add_all_attrib(root)
        self.start_namespace("http://schemas.android.com/apk/res/android", "android")
        self.__from_xml_etree(root)
        self.end_namespace("http://schemas.android.com/apk/res/android", "android")
        self.compute()
   
    
    def __from_xml_etree(self, root):
        """Convert Xml to Axml object internally

        Args:
            root (etree.ElementBase): Xml representation of AXML object
        """
        self.start(root.tag, root.attrib)
        for e in root:
            self.__from_xml_etree(e)
        self.end(root.tag)

    
    def add_xml_elt(self, res_xml : Classical_RES_XML, header_xml : AXMLHeader_RES_XML):
        """Function to add an element in function of the type

        Args:
            res_xml (Classical_RES_XML): Element
            header_xml (AXMLHeader_RES_XML): Header
        """
        res_xml.compute()

        header = header_xml(len(res_xml.content))

        elt = axml_pb2.XMLElement()
        elt.header.CopyFrom(header.proto)
        if type(res_xml.proto) is axml_pb2.ResXMLStartElement:
            elt.start_elt.CopyFrom(res_xml.proto)
        elif type(res_xml.proto) is axml_pb2.ResXMLStartNamespace:
            elt.start_ns.CopyFrom(res_xml.proto)
        elif type(res_xml.proto) is axml_pb2.ResXMLEndNamespace:
            elt.end_ns.CopyFrom(res_xml.proto)
        elif type(res_xml.proto) is axml_pb2.ResXMLEndElement:
            elt.end_elt.CopyFrom(res_xml.proto)
        self.proto.resourcexml.elts.append(elt)

    def start(self, root : str, attrib : dict):
        """Create start of element

        Args:
            root (str): Name of element
            attrib (dict): dict of all attribute of this element
        """
        index = self.stringblocks.get(root)
        i_namespace = self.stringblocks.get("android")
        attributes = []

        dic_attrib = attrib.items()
        for k, v in dic_attrib:
            tmp = k.split('{')
            if len(tmp) > 1:
                tmp = tmp[1].split('}')
                name = self.stringblocks.get(tmp[1])
                namespace = self.stringblocks.get(tmp[0])
            else:
                namespace = 0xffffffff
                name = self.stringblocks.get(k)

            

            if v == "true":
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x12000000, 1).proto)
            elif v == "false":
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x12000000, 0).proto)
            elif re.search("^@android:[0-9a-fA-F]+$", v):
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x1000000, int(v[-8:], 16)).proto)
            elif re.search("^@[0-9a-fA-F]+$", v):
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x1000000, int(v[1:], 16)).proto)
            elif re.search("^0x[0-9a-fA-F]+$", v):
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x11000000, int(v[2:], 16)).proto)
            elif re.search("^#[0-9a-fA-F]+$", v):
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x1c000000, int(v[2:], 16)).proto)
            elif re.search("^\?[0-9a-fA-F]+$", v):
                attributes.append(Attribute(namespace, name, 0xffffffff, 0x02000000, int(v[2:], 16)).proto)
            else:
                if self.stringblocks.proto.stringblocks[name].data == "versionName":
                    value = self.stringblocks.get(v)
                    attributes.append(Attribute(namespace, name, value, 0x3000008, value).proto)
                elif self.stringblocks.proto.stringblocks[name].data == "compileSdkVersionCodename":
                    value = self.stringblocks.get(v)
                    attributes.append(Attribute(namespace, name, value, 0x3000008, value).proto)
                else:
                    try:
                        value = ctypes.c_uint32(int(v)).value
                        attributes.append(Attribute(namespace, name, 0xffffffff, 0x10000008, value).proto)
                    except ValueError:
                        try:
                            value = unpack('>L', pack('!f', float(v)))[0]
                            attributes.append(Attribute(namespace, name, 0xffffffff, 0x04000008, value).proto)
                        except ValueError:
                            value = self.stringblocks.get(v)
                            attributes.append(Attribute(namespace, name, value, 0x3000008, value).proto)


        content = RES_XML_START_ELEMENT(0xffffffff, index, attributes)
        self.add_xml_elt(content, AXMLHeader_START_ELEMENT)


    def start_namespace(self, prefix : str, uri : str):
        """Create start of namespace

        Args:
            prefix (str): prefix of namespace
            uri (str): uri of namespace
        """
        index = self.stringblocks.get(prefix)
        i_namespace = self.stringblocks.get(uri)


        content = RES_XML_START_NAMESPACE(i_namespace, index)
        self.add_xml_elt(content, AXMLHeader_START_NAMESPACE)

    def end_namespace(self, prefix : str, uri : str):
        """Create end of namespace

        Args:
            prefix (str): prefix of namespace
            uri (str): uri of namespace
        """
        index = self.stringblocks.get(prefix)
        i_namespace = self.stringblocks.get(uri)


        content = RES_XML_END_NAMESPACE(i_namespace, index)
        self.add_xml_elt(content, AXMLHeader_END_NAMESPACE)

    def end(self, attrib : str):
        """Create end of element

        Args:
            attrib (str): name of end element
        """
        index = self.stringblocks.index(attrib)
        i_namespace = self.stringblocks.index("android")

        content = RES_XML_END_ELEMENT(0xffffffff, index)
        self.add_xml_elt(content, AXMLHeader_END_ELEMENT)

    def add_all_attrib(self, root):
        """Create Resource Map

        Args:
            root (etree.ElementBase): XML representation of AXML
        """
        res = []
        namespace = "{http://schemas.android.com/apk/res/android}"
        queue = [root]
        while len(queue) > 0:
            r = queue.pop()
            for child in r:
                queue.append(child)
            for k in r.attrib.keys():
                if k.startswith(namespace):
                    name = k[len(namespace):]
                    if name in public.SYSTEM_RESOURCES['attributes']['forward']:
                        val = public.SYSTEM_RESOURCES['attributes']['forward'][name]
                        if not val in res:
                            self.stringblocks.get(name)
                            res.append(val)
        self.proto.resourcemap.CopyFrom(ResourceMap(res=res).proto)

    ###########################################
    #                                         #
    #           ENCODE from XML               #
    #                                         #
    ###########################################
    
    def compute(self):
        """Compute all fields to have all AXML elements
        """
        self.stringblocks.compute()
        self.proto.header_xml.CopyFrom(AXMLHeader_XML(len(self.pack())).proto)

    def pack(self) -> bytes:
        """pack the AXML element

        Returns:
            bytes: return the AXML element packed
        """
        self.proto.stringblocks.CopyFrom(self.stringblocks.proto)
        sb_pack = self.stringblocks.pack()
        res = ResourceMap(proto=self.proto.resourcemap).pack()
        resxml = ResourceXML(proto=self.proto.resourcexml).pack()
        header_xml = AXMLHeader_XML(proto=self.proto.header_xml).pack()
        return header_xml + sb_pack + res + resxml
    
    def from_axml(buff : bytes, proto = None):
        """Convert AXML buffer to AXML object

        Args:
            buff (bytes): buffer contain AXML object

        Returns:
            tuple[pyaxml.AXML, bytes]: return AXML element and buffer offset at the end of the reading
        """
        axml = AXML()
        if proto:
            axml.proto = proto
        _, buff = AXMLHeader.from_axml(buff, proto=axml.proto.header_xml)
        sb, buff = StringBlocks.from_axml(buff, proto=axml.proto.stringblocks)
        _, buff = ResourceMap.from_axml(buff, proto=axml.proto.resourcemap)
        _, buff = ResourceXML.from_axml(buff, proto=axml.proto.resourcexml)

        axml.stringblocks = sb

        return axml, buff

    def get_elt_string(self, index : int) -> str:
        """Get string element decoded at index

        Args:
            index (int): index of target element

        Returns:
            str: the string element decoded
        """
        if index == 4294967295:
            return ""
        if index < len(self.proto.resourcemap.res) and self.proto.resourcemap.res[index] != 0: # TODO check if this value could be equal to zero in Android implementation
            return public.SYSTEM_RESOURCES['attributes']['inverse'][self.proto.resourcemap.res[index]]
        else:
            
            data = self.proto.stringblocks.stringblocks[index].data
            if self.proto.stringblocks.hnd.flag & axml_pb2.UTF8_FLAG == axml_pb2.UTF8_FLAG:
                return data.decode('utf-8')
            else:
                return data.decode('utf-16')

    def to_xml(self) -> etree.Element:
        """Convert AXML to XML to manipulate XML Tree

        Returns:
            etree.Element: XML element of all AXML files
        """
        root = None
        cur = root
        NSMAP = {"android" : 'http://schemas.android.com/apk/res/android'}

        for xmlelt in self.proto.resourcexml.elts:
            if xmlelt.HasField('start_elt'):
                ns = self.get_elt_string(xmlelt.start_elt.namespaceURI)
                name = self.get_elt_string(xmlelt.start_elt.name)
                if ns == "":
                    node = etree.Element(f"{name}")
                else:
                    node = etree.Element("{" + ns + "}" + name)
                for att in xmlelt.start_elt.attributes:
                    ns_att = self.get_elt_string(att.namespaceURI)
                    name_att = self.get_elt_string(att.name)
                    v = str(att.value)
                    t = TypedValue.get_type(att.type)
                    if t == TypedValue.TYPE_STRING:
                        v = self.get_elt_string(att.value)
                    else:
                        v = TypedValue.coerceToString(t, att.data)
                    if ns_att == "":
                        node.attrib[f"{name_att}"] = v
                    else:
                        node.attrib["{" + ns_att +"}" + name_att] = v
                if root == None:
                    node = etree.Element(node.tag, attrib=node.attrib, nsmap=NSMAP)
                    root = node
                    cur = node
                else:
                    cur.append(node)
                    cur = node
            elif xmlelt.HasField('end_elt'):
                cur = cur.getparent()
                #xmlelt.end_elt
            elif xmlelt.HasField('start_ns'):
                xmlelt.start_ns
            elif xmlelt.HasField('end_ns'):
                xmlelt.end_ns
            elif xmlelt.HasField('cdata'):
                cur.text = self.get_elt_string(xmlelt.cdata.name)
        return root

class AXML_guess:
    def from_axml(buff : bytes):
        if len(buff) < 8:
            logging.error("file too small")
            return None
        hnd, _ = AXMLHeader.from_axml(buff[:8])
        if hnd.proto.type == axml_pb2.RES_XML_TYPE:
            return AXML.from_axml(buff)
        elif hnd.proto.type == axml_pb2.RES_TABLE_TYPE:
            return ARSC.from_axml(buff)
        elif hnd.proto.type & 0x00ff == 0x003c:
            logging.warning("You probably parse an xml file")
            root = etree.fromstring(buff)
            ret = AXML()
            ret.from_xml(root)
            return ret 
        else:
            logging.error("file type not found")
            return None
        

