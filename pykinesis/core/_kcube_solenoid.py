import ctypes
import enum
import platform
import os

from ._errors import _error_restype


# Cosing and reading correct dll
system = platform.system()
arch   = platform.architecture()[0]
if system == "Windows":
    if arch == '64bit':
        dllPath = os.path.join(os.path.dirname(__file__), '../dependencies', system, 'x64', 'Thorlabs.MotionControl.KCube.Solenoid.dll')
    else:
         raise ValueError(f"Unsupported architecture: {arch}. Currently only 64bit is supported.")
else:
    raise ValueError(f"Unsupported system: {system}. Currently only Windows is supported.")
lib = ctypes.cdll.LoadLibrary(dllPath)


# Number of enum and structs binded: 3 / 12

# typedef enum SC_OperatingModes : byte
class _OperatingMode(enum.IntEnum):
    _Manual    = 0x01
    _Single    = 0x02
    _Auto      = 0x03
    _Triggered = 0x04

    @property
    def label(self) -> str:
        mapping = {
            self._Manual   : "Manual",
            self._Single   : "Single",
            self._Auto     : "Auto",
            self._Triggered: "Triggered",
        }
        return mapping.get(self, "Unknown")

    @classmethod
    def _missing_(cls, value: str):
        value   = value.strip().lower()
        mapping = {
            "manual"   : cls._Manual,
            "single"   : cls._Single,
            "auto"     : cls._Auto,
            "triggered": cls._Triggered,
        }
        if value in mapping: return mapping[value]

        raise ValueError(f"{value} is not a valid {cls.__name__}")

# typedef enum SC_OperatingStates : byte
class _OperatingState(enum.IntEnum):
    _Active   = 0x01
    _Inactive = 0x02

    @property
    def label(self) -> str:
        mapping = {
            self._Active  : "Active",
            self._Inactive: "Inactive",
        }
        return mapping.get(self, "Unknown")

    @classmethod
    def _missing_(cls, value: str):
        value   = value.strip().lower()
        mapping = {
            "active"  : cls._Active,
            "inactive": cls._Inactive,
        }
        if value in mapping: return mapping[value]

        raise ValueError(f"{value} is not a valid {cls.__name__}")

# typedef enum SC_SolenoidStates : byte
class _SolenoidState(enum.IntEnum):
    _Opened = 0x01
    _Closed = 0x02

    @property
    def label(self) -> str:
        mapping = {
            self._Opened: "Opened",
            self._Closed: "Closed",
        }
        return mapping.get(self, "Unknown")

    @classmethod
    def _missing_(cls, value: str):
        value   = value.strip().lower()
        mapping = {
            "opened": cls._Opened,
            "closed": cls._Closed,
        }
        if value in mapping: return mapping[value]

        raise ValueError(f"{value} is not a valid {cls.__name__}")

# Number of functions binded: 10 / 68


# KCUBESOLENOID_API short __cdecl TLI_BuildDeviceList(void)
lib.TLI_BuildDeviceList.restype  =  _error_restype
lib.TLI_BuildDeviceList.argtypes = []
def _buildDeviceList() -> None:
    lib.TLI_BuildDeviceList()

# KCUBESOLENOID_API short __cdecl TLI_GetDeviceListSize()
# ------------------------- TO-DO -----------------------

# KCUBESOLENOID_API short __cdecl TLI_GetDeviceList(SAFEARRAY** stringsReceiver)
# This function should not be used in the Python binding. It should be preferred
# the following : TLI_GetDeviceListExt(char *receiveBuffer, DWORD sizeOfBuffer).

# KCUBESOLENOID_API short __cdecl TLI_GetDeviceListByType(SAFEARRAY** stringsReceiver, int typeID)
# ------------------------- TO-DO ----------------------------------------------------------------

# KCUBESOLENOID_API short __cdecl TLI_GetDeviceListByTypes(SAFEARRAY** stringsReceiver, int * typeIDs, int length)
# ------------------------- TO-DO --------------------------------------------------------------------------------

# KCUBESOLENOID_API short __cdecl TLI_GetDeviceListExt(char *receiveBuffer, DWORD sizeOfBuffer)
lib.TLI_GetDeviceListExt.restype  =  _error_restype
lib.TLI_GetDeviceListExt.argtypes = [ctypes.c_char_p, ctypes.c_uint]
def _getDeviceListExt() -> list[str]:
    bufferSize = 256
    buffer     = ctypes.create_string_buffer(bufferSize)

    lib.TLI_GetDeviceListExt(buffer, bufferSize)
    devices = buffer.value.decode('utf-8')

    return devices.split(',') if devices else []

# KCUBESOLENOID_API short __cdecl TLI_GetDeviceListByTypeExt(char *receiveBuffer, DWORD sizeOfBuffer, int typeID)
# ------------------------- TO-DO -------------------------------------------------------------------------------

# KCUBESOLENOID_API short __cdecl TLI_GetDeviceListByTypesExt(char *receiveBuffer, DWORD sizeOfBuffer, int * typeIDs, int length)
# ------------------------- TO-DO -----------------------------------------------------------------------------------------------

# KCUBESOLENOID_API short __cdecl TLI_GetDeviceInfo(char const * serialNo, TLI_DeviceInfo *info)
# ------------------------- TO-DO --------------------------------------------------------------

# KCUBESOLENOID_API void __cdecl TLI_InitializeSimulations()
# ------------------------- TO-DO --------------------------

# KCUBESOLENOID_API void __cdecl TLI_UninitializeSimulations()
# ------------------------- TO-DO ----------------------------

# KCUBESOLENOID_API short __cdecl SC_Open(char const * serialNo)
lib.SC_Open.restype  =  _error_restype
lib.SC_Open.argtypes = [ctypes.c_char_p]
def _open(serialNo: str) -> None:
    lib.SC_Open(serialNo.encode('utf-8'))

# KCUBESOLENOID_API void __cdecl SC_Close(char const * serialNo)
lib.SC_Close.restype  =  _error_restype
lib.SC_Close.argtypes = [ctypes.c_char_p]
def _close(serialNo: str) -> None:
    lib.SC_Close(serialNo.encode('utf-8'))

# KCUBESOLENOID_API bool __cdecl SC_CheckConnection(char const * serialNo)
# ------------------------- TO-DO ----------------------------------------

# KCUBESOLENOID_API void __cdecl SC_Identify(char const * serialNo)
# ------------------------- TO-DO ---------------------------------

# 27 functions are still missing before the next one

# KCUBESOLENOID_API SC_OperatingModes __cdecl SC_GetOperatingMode(char const * serialNo)
lib.SC_GetOperatingMode.restype  =  ctypes.c_ubyte # Prefer unsigned rather than c_byte
lib.SC_GetOperatingMode.argtypes = [ctypes.c_char_p]
def _getOperatingMode(serialNo: str) -> _OperatingMode:
    mode = lib.SC_GetOperatingMode(serialNo.encode("utf-8"))

    try:               return _OperatingMode(mode)
    except ValueError: raise   RuntimeError(f"Unknown operating mode: {mode}")

# KCUBESOLENOID_API short __cdecl SC_SetOperatingMode(char const * serialNo, SC_OperatingModes mode)
lib.SC_SetOperatingMode.restype  =  _error_restype
lib.SC_SetOperatingMode.argtypes = [ctypes.c_char_p, ctypes.c_ubyte] # Prefer c_ubyte than c_byte
def _setOperatingMode(serialNo: str, operatingMode: _OperatingMode) -> None:
    lib.SC_SetOperatingMode(serialNo.encode("utf-8"), operatingMode)

# KCUBESOLENOID_API SC_SolenoidStates __cdecl SC_GetSolenoidState(char const * serialNo)
lib.SC_GetSolenoidState.restype  =  ctypes.c_ubyte # Prefer unsigned rather than c_byte
lib.SC_GetSolenoidState.argtypes = [ctypes.c_char_p]
def _getSolenoidState(serialNo: str) -> _SolenoidState:
    state = lib.SC_GetSolenoidState(serialNo.encode("utf-8"))

    try:               return _SolenoidState(state)
    except ValueError: raise   RuntimeError(f"Unknown solenoid state: {state}")

# KCUBESOLENOID_API short __cdecl SC_RequestOperatingState(char const * serialNo)
# ------------------------- TO-DO -----------------------------------------------

# KCUBESOLENOID_API SC_OperatingStates __cdecl SC_GetOperatingState(char const * serialNo)
lib.SC_GetOperatingState.restype  =  ctypes.c_ubyte # Prefer unsigned rather than c_byte
lib.SC_GetOperatingState.argtypes = [ctypes.c_char_p]
def _getOperatingState(serialNo: str) -> _OperatingState:
    state = lib.SC_GetOperatingState(serialNo.encode("utf-8"))

    try:               return _OperatingState(state)
    except ValueError: raise   RuntimeError(f"Unknown operating state: {state}")

# KCUBESOLENOID_API short __cdecl SC_SetOperatingState(char const * serialNo, SC_OperatingStates state)
lib.SC_SetOperatingState.restype  =  _error_restype
lib.SC_SetOperatingState.argtypes = [ctypes.c_char_p, ctypes.c_ubyte] # Prefer c_ubyte than c_byte
def _setOperatingState(serialNo: str, operatingState: _OperatingState) -> None:
    lib.SC_SetOperatingState(serialNo.encode("utf-8"), operatingState)

# 20 functions are still missing before the end of the file