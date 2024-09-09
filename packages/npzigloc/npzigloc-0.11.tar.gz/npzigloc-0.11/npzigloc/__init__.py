from __future__ import annotations
import numpy as np
import os

thisfolder = os.path.dirname(__file__)
try:
    import npzigwhere

except Exception as e:
    import Cython, setuptools, platform, subprocess, os, sys, time
    import ziglang

    iswindows = "win" in platform.platform().lower()
    if iswindows:
        addtolist = []
    else:
        addtolist = ["&"]

    olddict = os.getcwd()
    dirname = os.path.dirname(__file__)
    os.chdir(dirname)
    compile_file = os.path.join(dirname, "npzigwhere_compile.py")
    subprocess._USE_VFORK = False
    subprocess._USE_POSIX_SPAWN = False
    subprocess.run(
        " ".join(
            [
                sys.executable,
                compile_file,
                "build_ext",
                "--inplace",
            ]
            + addtolist
        ),
        shell=True,
        env=os.environ,
        cwd=thisfolder,
        preexec_fn=None
        if iswindows
        else os.setpgrp
        if hasattr(os, "setpgrp")
        else None,
    )
    if not iswindows:
        time.sleep(30)
    import npzigwhere

    os.chdir(olddict)

operation_lookup = {"<": 0, "<=": 1, "==": 2, ">=": 3, ">": 4, "!=": 5}

functiondict_npwhere_argwhere = {
    "i": b"npwhere_argwhere_c_int",
    "l": b"npwhere_argwhere_c_int",
    "L": b"npwhere_argwhere_c_uint",
    "I": b"npwhere_argwhere_c_uint",
    "b": b"npwhere_argwhere_c_char",
    "B": b"npwhere_argwhere_u8",
    "h": b"npwhere_argwhere_c_short",
    "H": b"npwhere_argwhere_c_ushort",
    "q": b"npwhere_argwhere_c_longlong",
    "Q": b"npwhere_argwhere_c_ulonglong",
    "f": b"npwhere_argwhere_f32",
    "d": b"npwhere_argwhere_f64",
    "D": b"npwhere_argwhere_f128",
}
functiondict_np_boolean_numpy_array = {
    "i": b"np_boolean_numpy_array_c_int",
    "l": b"np_boolean_numpy_array_c_int",
    "L": b"np_boolean_numpy_array_c_uint",
    "I": b"np_boolean_numpy_array_c_uint",
    "b": b"np_boolean_numpy_array_c_char",
    "B": b"np_boolean_numpy_array_u8",
    "h": b"np_boolean_numpy_array_c_short",
    "H": b"np_boolean_numpy_array_c_ushort",
    "q": b"np_boolean_numpy_array_c_longlong",
    "Q": b"np_boolean_numpy_array_c_ulonglong",
    "f": b"np_boolean_numpy_array_f32",
    "d": b"np_boolean_numpy_array_f64",
    "D": b"np_boolean_numpy_array_f128",
}
# _npwhere_argwhere(size_t array_len,tuple array_shape,size_t array_address, cython.uchar[:] search_for_value, size_t operation=2,str np_function=b"npwhere_argwhere_u8",bint no_gil=False,bint flip_array=True,transpose=False )

# npwhere_bool_compare(size_t array_len,tuple array_shape,size_t array_address, size_t search_for_value_address, size_t operation=2,bytes np_function=b"np_boolean_numpy_array_u8",bint no_gil=False ):
def npwhere_bool_compare(
    img, search_for=255, operation="==", no_gil=False, 
):
    array_shape = img.shape
    if not img.flags["C_CONTIGUOUS"] or not img.flags["ALIGNED"]:
        img = img.copy()
    array_address = img.ctypes._arr.__array_interface__["data"][0]
    array_len = np.prod(img.shape)
    search_for_value = np.require([search_for], dtype=img.dtype)
    np_function = functiondict_np_boolean_numpy_array[img.dtype.char]
    # if img.dtype == ctypes.c_uint8:
    #     np_function = b"np_boolean_numpy_array_u8"
    # else:
    #     np_function = b"np_boolean_numpy_array_u8"
    return npzigwhere._npwhere_bool_compare(
        array_len=array_len,
        array_shape=array_shape,
        array_address=array_address,
        search_for_value_address=search_for_value.ctypes._arr.__array_interface__[
            "data"
        ][0],
        operation=operation_lookup[operation],
        np_function=np_function,
        no_gil=no_gil,
    )




def np_argwhere_values(img, search_for=255, operation='==', no_gil=False, flip_array=True):
    array_shape = img.shape
    if not img.flags["C_CONTIGUOUS"] or not img.flags["ALIGNED"]:
        img = img.copy()
    array_address = img.ctypes._arr.__array_interface__["data"][0]
    array_len = np.prod(img.shape)
    search_for_value = np.require([search_for], dtype=img.dtype.char)
    np_function = functiondict_npwhere_argwhere[img.dtype.char]
    
    # if img.dtype == ctypes.c_uint8:
    #     np_function = b"npwhere_argwhere_u8"
    # else:
    #     np_function = b"npwhere_argwhere_u8"
    return npzigwhere._npwhere_argwhere(
        array_len=array_len,
        array_shape=array_shape,
        array_address=array_address,
        search_for_value_address=search_for_value.ctypes._arr.__array_interface__[
            "data"
        ][0],
        operation=operation_lookup[operation],
        np_function=np_function,
        no_gil=no_gil,
        flip_array=flip_array,
        transpose=False,
    )




def np_where_values(img, search_for=255, operation="==", no_gil=False, flip_array=True):
    array_shape = img.shape
    if not img.flags["C_CONTIGUOUS"] or not img.flags["ALIGNED"]:
        img = img.copy()
    array_address = img.ctypes._arr.__array_interface__["data"][0]
    array_len = np.prod(img.shape)
    search_for_value = np.require([search_for], dtype=img.dtype)
    np_function = functiondict_npwhere_argwhere[img.dtype.char]

    return npzigwhere._npwhere_argwhere(
        array_len=array_len,
        array_shape=array_shape,
        array_address=array_address,
        search_for_value_address=search_for_value.ctypes._arr.__array_interface__[
            "data"
        ][0],
        operation=operation_lookup[operation],
        np_function=np_function,
        no_gil=no_gil,
        flip_array=flip_array,
        transpose=True,
    )


def np_argwhere_bool(barray, no_gil=False, flip_array=True):
    return npzigwhere._np_argwhere_bool(
        array_address=barray.ctypes._arr.__array_interface__["data"][0],
        array_len=np.prod(barray.shape),
        array_shape=barray.shape,
        no_gil=no_gil,
        transpose=False,
        npfunction=b"npwhere_argwhere_bool",
        flip_array=flip_array,
    )


def np_where_bool(barray, no_gil=False, flip_array=True):
    return npzigwhere._np_argwhere_bool(
        array_address=barray.ctypes._arr.__array_interface__["data"][0],
        array_len=np.prod(barray.shape),
        array_shape=barray.shape,
        no_gil=no_gil,
        transpose=True,
        npfunction=b"npwhere_argwhere_bool",
        flip_array=flip_array,
    )
