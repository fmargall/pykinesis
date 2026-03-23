from pykinesis import KCubeSolenoid


if __name__ == "__main__":
    # List all KCube Solenoid connected
    devicesList = KCubeSolenoid.listDevices()

    # Take the first one as example
    if len(devicesList) > 0:
        serialNo = devicesList[0]

        with KCubeSolenoid(serialNo) as cube:
            # Open or close the solenoid as needed
            cube.open()
            cube.close()