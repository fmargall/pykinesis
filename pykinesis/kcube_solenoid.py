from .core._kcube_solenoid import _OperatingMode, _OperatingState, _SolenoidState
from .core._kcube_solenoid import _buildDeviceList, _getDeviceListExt, _open, _close, _getOperatingMode, \
                                  _setOperatingMode, _getSolenoidState, _getOperatingState, _setOperatingState

class KCubeSolenoid:

    @staticmethod
    def listDevices() -> list[str]:
        _buildDeviceList()
        return _getDeviceListExt()

    @classmethod
    def fromSerialNo(cls, serialNo: str):
        _buildDeviceList()
        deviceList = _getDeviceListExt()

        # Check if serial number is valid
        if serialNo not in deviceList:
            raise ValueError(f"Serial number {serialNo} not found")

        return cls(serialNo)

    @classmethod
    def fromIndex(cls, index: int):
        # Check if index is valid
        _buildDeviceList()
        deviceList = _getDeviceListExt()
        if index >= len(deviceList):
            raise IndexError(f"Solenoid index {index} out of range (available solenoids: {len(deviceList)})")

        serialNo = deviceList[index]
        return cls(serialNo)

    def __init__(self, serialNo: str):

        # Check if serial number is valid
        _buildDeviceList()
        deviceList = _getDeviceListExt()
        if serialNo not in deviceList:
            raise ValueError(f"Serial number {serialNo} not found")

        self._index    = deviceList.index(serialNo)
        self._serialNo = serialNo

        # Opening the instance
        _open(self._serialNo)
        self._isClosed = False

        # Initialize state and mode. For safety it will
        # always originally be set to "Manual / Closed"
        self.operatingMode  = "manual"
        self.operatingState = "inactive" # ie., closed

    def __enter__(self):
        return self


    @property
    def operatingMode(self) -> str:
        return _getOperatingMode(self._serialNo).label

    @operatingMode.setter
    def operatingMode(self, operatingMode: str):
        _setOperatingMode(self._serialNo, _OperatingMode(operatingMode))

    @property
    def operatingState(self) -> str:
        return _getOperatingState(self._serialNo).label

    @operatingState.setter
    def operatingState(self, operatingState: str):
        _setOperatingState(self._serialNo, _OperatingState(operatingState))

    def openSolenoid(self):
        # Force the solenoid to be opened until new update
        self.operatingMode  = "manual"
        self.operatingState = "active" # ie., opened

    def closeSolenoid(self):
        # Force the solenoid to be closed until new update
        self.operatingMode  = "manual"
        self.operatingState = "inactive" # ie., closed

    # Pythonic aliases
    open  = openSolenoid
    close = closeSolenoid


    def _closeInstance(self):
        if not self._isClosed:
            _close(self._serialNo)
            self._isClosed = True

    def __del__(self):
        self._closeInstance()

    def __exit__(self, exceptionType, exceptionValue, traceback):
        self._closeInstance()