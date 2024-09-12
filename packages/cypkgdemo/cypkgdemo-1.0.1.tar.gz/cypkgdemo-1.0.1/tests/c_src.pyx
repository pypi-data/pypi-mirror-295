# cython: language_level = 3
# distutils: language = c++

from libcpp.vector cimport vector

from cypkgdemo.c_impl cimport c_sa

cpdef vector[double] my_sa(vector[double] vec):
    cdef vector[double] output = vector[double](vec.size())
    cdef int i
    for i in range(vec.size()):
        output[i] = c_sa(vec[i])
    return output
