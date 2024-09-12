# cython: language_level=3

"""
This is a declaration file exporting C functions.

"""

cdef extern from "math.h":
    cdef double sin(double x)