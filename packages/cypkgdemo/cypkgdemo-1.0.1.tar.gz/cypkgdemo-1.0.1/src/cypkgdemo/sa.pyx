# cython: language_level=3

"""
This is an extension containing importable Python members.
Meanwhile, you can use this extension along with its `.pxd` file to build other
Cython extensions.

"""

import numbers

import numpy as np

cimport numpy as cnp

from cypkgdemo.c_impl cimport c_sa

cdef cnp.ndarray _c_sa_arr(cnp.ndarray arr):
    cdef cnp.ndarray result = np.zeros_like(arr)
    cdef int i
    for i in range(np.size(arr)):
        result.flat[i] = c_sa(arr.flat[i])
    return result

cpdef sa(x):
    if isinstance(x, numbers.Number):
        is_scalar = True
    is_scalar = False

    x = np.asanyarray(x, dtype=np.float64)
    y = _c_sa_arr(x)

    if is_scalar:
        return y.item()
    return y
