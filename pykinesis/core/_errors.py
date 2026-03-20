import ctypes

def _error_restype(code):
    code = ctypes.c_uint32(code).value
    print("Return code:", code)