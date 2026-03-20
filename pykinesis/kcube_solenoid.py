from .core._kcube_solenoid import _OperatingMode, _OperatingState, _SolenoidState
from .core._kcube_solenoid import _buildDeviceList, _getDeviceListExt, _open, _close, _getOperatingMode, \
                                  _setOperatingMode, _getSolenoidState, _getOperatingState, _setOperatingState

class KCubeSolenoid:

    def __init__(self, solenoidIndex):

        # Check if solenoidIndex is valid
        _buildDeviceList()
        solenoidList = _getDeviceListExt()
        if solenoidIndex >= len(solenoidList):
            raise IndexError(f"Solenoid index {solenoidIndex} out of range (available solenoids: {len(solenoidList)})")

        self._index    = solenoidIndex
        self._serialNo = solenoidList[self._index]

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


    def _closeInstance(self):
        if not self._isClosed:
            _close(self._serialNo)
            self._isClosed = True

    def __del__(self):
        self._closeInstance()

    def __exit__(self, exceptionType, exceptionValue, traceback):
        self._closeInstance()