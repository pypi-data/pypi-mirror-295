# cython: language_level=3

"""
This is an extension contains pure C implementations, i.e. there is no members
which can be imported by Python code.
Use this extension along with its `.pxd` file to build other Cython extensions.

"""

from cypkgdemo.c_exports cimport sin

cdef double c_sa(double x):
    if x == 0.:
        return 1.

    return sin(x) / x