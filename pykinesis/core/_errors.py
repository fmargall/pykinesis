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
    FT_InvalidHandle         = 0x01
    FT_DeviceNotFound        = 0x02
    FT_DeviceNotOpened       = 0x03
    FT_IOError               = 0x04
    FT_InsufficientResources = 0x05
    FT_InvalidParameter      = 0x06
    FT_DeviceNotPresent      = 0x07
    FT_IncorrectDevice       = 0x08

    # Device libraries errors
    FT_NoDLLLoaded          = 0x10
    FT_NoFunctoinsAvailable = 0x11
    FT_FunctionNotAvailable = 0x12
    FT_BadFunctionPointer   = 0x13
    FT_GenericFunctionFail  = 0x14
    FT_SpecificFunctionFail = 0x15

    # General DLL control errors
    TL_ALREADY_OPEN           = 0x20
    TL_NO_RESPONSE            = 0x21
    TL_NOT_IMPLEMENTED        = 0x22
    TL_FAULT_REPORTED         = 0x23
    TL_INVALID_OPERATION      = 0x24
    TL_DISCONNECTING          = 0x28
    TL_FIRMWARE_BUG           = 0x29
    TL_INITIALIZATION_FAILURE = 0x2A
    TL_INVALID_CHANNEL        = 0x2B

    # Motor specific errors
    TL_UNHOMED                    = 0x25
    TL_INVALID_POSITION           = 0x26
    TL_INVALID_VELOCITY_PARAMETER = 0x27
    TL_CANNOT_HOME_DEVICE         = 0x2C
    TL_JOG_CONTINOUS_MODE         = 0x2D
    TL_NO_MOTOR_INFO              = 0x2E
    TL_CMD_TEMP_UNAVAILABLE       = 0x2F

    @property
    def message(self) -> str:
        return {
            # FTDI and Communication errors
            _ErrorCode.FT_InvalidHandle   : "The FTDI functions have not been initialized"       ,
            _ErrorCode.FT_DeviceNotFound  : "The device could not be found"                      ,
            _ErrorCode.FT_DeviceNotOpened : "The device must be opened before it can be accessed" 
        
        }.get(self, "Unknown Kinesis SDK error.")