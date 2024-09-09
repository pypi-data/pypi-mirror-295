import cython
cimport cython
import os
import numpy as np
cimport numpy as np
import ctypes
import re
from libcpp.string cimport string
from libcpp.utility cimport pair
from libc.stdlib cimport free
import time, subprocess
from libcpp.unordered_map cimport unordered_map
import platform
import sys 
this_folder = os.path.dirname(__file__)
_func_cache = []
subprocess._USE_VFORK = False
subprocess._USE_POSIX_SPAWN = False
iswindows = "win" in platform.platform().lower()
if iswindows:
    addtolist = []
else:
    addtolist = ["&"]

ctypedef pair[size_t,size_t] ipair
ctypedef size_t* (*fu0)(size_t,size_t,size_t,size_t,size_t,size_t,size_t) noexcept nogil
ctypedef void (*fu1)(size_t,size_t,size_t,size_t,size_t) noexcept nogil
ctypedef void (*fu2)(size_t,size_t,size_t,size_t,size_t,size_t) noexcept nogil
ctypedef size_t* (*fu4)(size_t,size_t,size_t,size_t,size_t) noexcept nogil
ctypedef size_t* (*fu3)(size_t,size_t,size_t,size_t) noexcept nogil

cdef ctypes_arg_dict={0:{'arg':[ctypes.c_size_t]*7,'res':ctypes.POINTER(ctypes.c_size_t)},
                 1:{'arg':[ctypes.c_size_t]*5,'res':None},
                 2:{'arg':[ctypes.c_size_t]*6,'res':None},
                 3:{'arg':[ctypes.c_size_t]*4,'res':ctypes.POINTER(ctypes.c_size_t)},
                 4:{'arg':[ctypes.c_size_t]*5,'res':ctypes.POINTER(ctypes.c_size_t)},
}
ctypedef unordered_map[string, ipair] functiondict
cdef zig_functions_ctypes={}



def compile_it(ziglibfile):
    zigpathstr = os.path.normpath(os.path.join(this_folder, ziglibfile))
    winpathstr = re.sub(r'\.zig$','.dll',zigpathstr)
    linuxpathstr = re.sub(r'\.zig$','.so',zigpathstr)
    win_path=os.path.exists(winpathstr)
    linux_path=os.path.exists(linuxpathstr)
    if not os.path.exists(winpathstr) and not os.path.exists(winpathstr) :
        old_folder=os.getcwd()
        os.chdir(this_folder)
        subprocess.run(
        [sys.executable, "-m", "ziglang", "build-lib", ziglibfile, "-dynamic",'-lc', "-O", "ReleaseFast"]+addtolist,
        shell=True,
        env=os.environ,
        cwd=this_folder,
        preexec_fn=None

        if iswindows
        else os.setpgrp
        if hasattr(os, "setpgrp")
        else None,
        )
        time.sleep(1)
        if not iswindows:
            time.sleep(20)
        win_path=os.path.exists(winpathstr)
        linux_path=os.path.exists(linuxpathstr)
        os.chdir(old_folder)
    if win_path:
        return winpathstr
    if linux_path:
        return linuxpathstr
    raise OSError('Zig library not found')

ziglibfile='zignpwhere.zig'
library_path_string=compile_it(ziglibfile)
cdef functiondict get_lookup_dict(str dllpathstr,dict function_dict_names):
    cdef:
        functiondict zig_functions
    cta = ctypes.cdll.LoadLibrary(dllpathstr)
    _func_cache.append(cta)
    for dtypechar,zigfunction in function_dict_names.items():
        ctypes_f=getattr(cta, zigfunction[0])
        ctypes_f.argtypes=ctypes_arg_dict[zigfunction[1]]['arg']
        ctypes_f.restype=ctypes_arg_dict[zigfunction[1]]['res']
        zig_functions_ctypes[dtypechar]=ctypes_f
        _func_cache.append(ctypes_f)
        zig_functions[<string>dtypechar]=ipair(zigfunction[1],(<size_t>ctypes.addressof(ctypes_f)))
    return zig_functions

cdef:
    dict zig_function_names={
        'flatten_index':['flatten_index',3],
        'npwhere_argwhere_bool':['npwhere_argwhere_bool',4],
        'npwhere_argwhere_u8':['npwhere_argwhere_u8',0],
        "npwhere_argwhere_c_int":["npwhere_argwhere_c_int",0],
        "npwhere_argwhere_c_int":["npwhere_argwhere_c_int",0],
        "npwhere_argwhere_c_uint":["npwhere_argwhere_c_uint",0],
        "npwhere_argwhere_c_uint":["npwhere_argwhere_c_uint",0],
        "npwhere_argwhere_c_char":["npwhere_argwhere_c_char",0],
        "npwhere_argwhere_c_short":["npwhere_argwhere_c_short",0],
        "npwhere_argwhere_c_ushort":["npwhere_argwhere_c_ushort",0],
        "npwhere_argwhere_c_longlong":["npwhere_argwhere_c_longlong",0],
        "npwhere_argwhere_c_ulonglong":["npwhere_argwhere_c_ulonglong",0],
        "npwhere_argwhere_f32":["npwhere_argwhere_f32",0],
        "npwhere_argwhere_f64":["npwhere_argwhere_f64",0],
        "npwhere_argwhere_f128":["npwhere_argwhere_f128",0],
        "np_boolean_numpy_array_c_int":["np_boolean_numpy_array_c_int",1],
        "np_boolean_numpy_array_c_int":["np_boolean_numpy_array_c_int",1],
        "np_boolean_numpy_array_c_uint":["np_boolean_numpy_array_c_uint",1],
        "np_boolean_numpy_array_c_uint":["np_boolean_numpy_array_c_uint",1],
        "np_boolean_numpy_array_c_char":["np_boolean_numpy_array_c_char",1],
        "np_boolean_numpy_array_u8":["np_boolean_numpy_array_u8",1],
        "np_boolean_numpy_array_c_short":["np_boolean_numpy_array_c_short",1],
        "np_boolean_numpy_array_c_ushort":["np_boolean_numpy_array_c_ushort",1],
        "np_boolean_numpy_array_c_longlong":["np_boolean_numpy_array_c_longlong",1],
        "np_boolean_numpy_array_c_ulonglong":["np_boolean_numpy_array_c_ulonglong",1],
        "np_boolean_numpy_array_f32":["np_boolean_numpy_array_f32",1],
        "np_boolean_numpy_array_f64":["np_boolean_numpy_array_f64",1],
        "np_boolean_numpy_array_f128":["np_boolean_numpy_array_f128",1],
    }
    functiondict zig_compare_all_bool_arrays = get_lookup_dict(library_path_string,zig_function_names)


cpdef _npwhere_bool_compare(size_t array_len,tuple array_shape,size_t array_address, size_t search_for_value_address, size_t operation=2,bytes np_function=b"np_boolean_numpy_array_u8",bint no_gil=False ):
    cdef:
        str np_functionstr=np_function.decode()
        string np_function_cpp = <string>np_function
        ipair right_function = zig_compare_all_bool_arrays[np_function_cpp]
        np.ndarray bool_array_result=np.zeros(array_shape,dtype=bool)
        size_t bool_array_result_view=bool_array_result.ctypes._arr.__array_interface__["data"][0]
    if no_gil:
        zig_functions_ctypes[np_functionstr](
                    array_address,
                    search_for_value_address,
                    array_len,
                    operation,
                    bool_array_result_view
                )
    else:
        (<fu1*>right_function.second)[0](
                    array_address,
                    search_for_value_address,
                    array_len,
                    operation,
                    bool_array_result_view
                    )
    return bool_array_result




cpdef _npwhere_argwhere(size_t array_len,tuple array_shape,size_t array_address, size_t search_for_value_address, size_t operation=2,bytes np_function=b"npwhere_argwhere_u8",bint no_gil=False,bint flip_array=True,transpose=False ):
    cdef:
        np.ndarray[np.npy_uintp, ndim=1, mode="c", cast=False] array_shapenp_full = np.array(array_shape,dtype=np.uint64)
        size_t[:] array_shapenp = array_shapenp_full
        size_t np_shape_len = array_shapenp_full.shape[0]
        np.ndarray[np.npy_uintp, ndim=1, mode="c", cast=False]  len_address=np.zeros(2,dtype=np.uint64)
        size_t[:] len_address_view = len_address
        str np_functionstr=np_function.decode()
        string np_function_cpp = <string>np_function
        ipair right_function = zig_compare_all_bool_arrays[np_function_cpp]
        size_t array_shapenp_address =<size_t>(&array_shapenp[0])
        size_t len_address_view_address =<size_t>(&len_address_view[0])
        size_t* cpointer_size_t
    if not no_gil:
        pox=zig_functions_ctypes[np_functionstr](
            array_address,
            search_for_value_address,
            array_len,
            operation,
            array_shapenp_address,
            np_shape_len,
            len_address_view_address
        )
    else:
        cpointer_size_t=(<fu0*>right_function.second)[0](
                array_address,
                search_for_value_address,
                array_len,
                operation,
                array_shapenp_address,
                np_shape_len,
                    len_address_view_address)
    try:
        return convert_results(array_shape=array_shape,len_address=len_address,transpose=transpose,flip_array=flip_array)
    finally:
        free(<size_t*>(len_address[1]))




cdef convert_results(tuple array_shape,size_t[:] len_address,bint transpose=False,bint flip_array=True):
        cr=(ctypes.c_uint8 * (int(len_address[0]))).from_address(int(len_address[1]))
        if not transpose:
            if flip_array:
                return  np.flip(np.flip(np.frombuffer(cr, dtype=np.uint64).reshape((-1,len(array_shape)))),0).copy()
            else:
                return  (np.flip(np.frombuffer(cr, dtype=np.uint64).reshape((-1,len(array_shape))),0)).copy()

        else:
            if flip_array:
                return tuple(np.flip(np.flip(np.frombuffer(cr, dtype=np.uint64).reshape((-1,len(array_shape)))),0).T.copy())
            else:
                return tuple(np.flip(np.frombuffer(cr, dtype=np.uint64).reshape((-1,len(array_shape))),0).T.copy())


cpdef _np_argwhere_bool(size_t array_address,size_t array_len, tuple array_shape, bint no_gil=True,bint transpose=False,bytes npfunction=b'npwhere_argwhere_bool',bint flip_array=True ) :
    cdef:
        np.ndarray[np.npy_uintp, ndim=1, mode="c", cast=False] array_shapenp_full = np.array(array_shape,dtype=np.uint64)
        size_t[:] array_shapenp = array_shapenp_full
        size_t np_shape_len = array_shapenp_full.shape[0]
        size_t array_shapenp_address =<size_t>(&array_shapenp[0])
        np.ndarray[np.npy_uintp, ndim=1, mode="c", cast=False]  len_address=np.zeros(2,dtype=np.uint64)
        size_t[:] len_address_view = len_address
        size_t len_address_view_address =<size_t>(&len_address_view[0])
        str npfunctionstr=npfunction.decode('utf-8')
        string np_function_cpp = <string>npfunction
        ipair right_function = zig_compare_all_bool_arrays[np_function_cpp]
        size_t* cpointer_size_t

    if not no_gil:
        pox=zig_functions_ctypes[npfunctionstr](
        array_address,
        array_len,
        array_shapenp_address,
        np_shape_len,
        len_address_view_address
    )
    else:
        with nogil:
            cpointer_size_t=(<fu4*>right_function.second)[0](
                    array_address,
                    array_len,
                    array_shapenp_address,
                    np_shape_len,
                    len_address_view_address)
    try:
        return convert_results(array_shape=array_shape,len_address=len_address,transpose=transpose,flip_array=flip_array)
    finally:
        free(<size_t*>(len_address[1]))


cpdef flatten_np_index(tuple array_shape, bint no_gil=False,bint transpose=False,bytes npfunction=b'flatten_index',bint flip_array=True ):
    cdef:
        np.ndarray[np.npy_uintp, ndim=1, mode="c", cast=False] array_shapenp_full = np.array(array_shape,dtype=np.uint64)
        size_t[:] array_shapenp = array_shapenp_full
        size_t np_shape_len = array_shapenp_full.shape[0]
        size_t array_shapenp_address =<size_t>(&array_shapenp[0])
        np.ndarray[np.npy_uintp, ndim=1, mode="c", cast=False]  len_address=np.zeros(2,dtype=np.uint64)
        size_t[:] len_address_view = len_address
        size_t len_address_view_address =<size_t>(&len_address_view[0])
        string np_function_cpp = <string>npfunction
        str npfunctionstr=npfunction.decode('utf-8')
        ipair right_function = zig_compare_all_bool_arrays[np_function_cpp]
        size_t* cpointer_size_t
        size_t counter = np.prod(array_shape)

    if not no_gil:
        pox=zig_functions_ctypes[npfunctionstr](
                array_shapenp_address,
                np_shape_len,
                counter,
                len_address_view_address
    )

    else:
        with nogil:
            cpointer_size_t=(<fu3*>right_function.second)[0](
            array_shapenp_address,
            np_shape_len,
            counter,
            len_address_view_address
        )
    try:
        return convert_results(array_shape=array_shape,len_address=len_address,transpose=transpose,flip_array=flip_array)
    finally:
        free(<size_t*>(len_address[1]))