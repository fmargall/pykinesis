import codecs
import ctypes

from enum import IntEnum

def _error_restype(code):
    code = ctypes.c_uint32(code).value
    
    if code != _ErrorCode.FT_OK:
        raise KinesisError(code)

    return _ErrorCode(code)


class KinesisError(Exception):
    def __init__(self, code: int):
        try:
            self.code    = _ErrorCode(code)
            self.name    = self.code.name
            self.message = self.code.message
        except ValueError:
            self.code    = code
            self.name    = "UnknownError"
            self.message = "Unknown Kinesis SDK Error."

        super().__init__(f"[{self.name}] (0x{int(code):08X}) {self.message}")

class _ErrorCode(IntEnum):
    FT_OK = 0x00

    # FTDI and Communication errors
    FT_InvalidHandle   = 0x01
    FT_DeviceNotFound  = 0x02
    FT_DeviceNotOpened = 0x03

    @property
    def message(self) -> str:
        return {
            # FTDI and Communication errors
            _ErrorCode.FT_InvalidHandle   : "The FTDI functions have not been initialized"       ,
            _ErrorCode.FT_DeviceNotFound  : "The device could not be found"                      ,
            _ErrorCode.FT_DeviceNotOpened : "The device must be opened before it can be accessed" 
        
        }.get(self, "Unknown Kinesis SDK error.")