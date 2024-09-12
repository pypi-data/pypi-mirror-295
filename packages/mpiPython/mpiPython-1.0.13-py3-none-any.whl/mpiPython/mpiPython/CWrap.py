"""
File: CWrap.py
Modification Date: 8/12/24
Time Modified: 1:30pm CT
Created by: Judah Nava
Last Modified By: Judah Nava
Organization: Parallel Solvit LLC and MSUM CSIS Department
"""

import ctypes as CT
import os
import atexit


class CWrap():
    script_dir = os.getcwd()
    lib_path = os.path.join(script_dir, 'libcode.so')
    # print(lib_path)
    
    c_code = CT.CDLL(lib_path)
    comm_func = c_code.communicator
    comm_func.restype = CT.c_int
    cworld = comm_func()

    minidict = {
        "MAX": 1,
        "MIN":2,
        "SUM":3,
        "PROD":4,
        "LAND":5, #!! be carefull with these.
        "LOR":6,  #!! python datatype of int might mess things up.
        "BAND":7, #!!
        "BOR":8   #!!
    }

    def __init__(self):
        """
        This is set up so that the user does not have to initialize,
        finalize, and acknoledge comm (at bottom of init).
        Need to go over reduce, bcast, scatter... reduce the code.
        """

        # all function preperation.
        self.__rank = CWrap.c_code.mpi_comm_rank
        self.__rank.argtypes = [CT.c_int]
        self.__rank.restype = CT.c_int

        self.__size = CWrap.c_code.mpi_comm_size
        self.__size.argtypes = [CT.c_int]
        self.__size.restype = CT.c_int

        self.__int_send = CWrap.c_code.mpi_send_int
        self.__int_send.argtypes = [CT.c_int, CT.c_int, CT.c_int, CT.c_int, CT.c_int]

        self.__int_recv = CWrap.c_code.mpi_recv_int
        self.__int_recv.argtypes = [CT.c_int, CT.c_int, CT.c_int, CT.c_int]
        self.__int_recv.restype = CT.c_int

        self.__array_send_int = CWrap.c_code.mpi_send_int_array
        self.__array_send_int.argtypes = [CT.c_void_p, CT.c_int, CT.c_int, CT.c_int, CT.c_int]
        self.__array_send_int.restype = CT.c_int

        self.__array_send_double = CWrap.c_code.mpi_send_double_array
        self.__array_send_double.argtypes = [CT.c_void_p, CT.c_int, CT.c_int, CT.c_int, CT.c_int]

        self.__array_recv_int = CWrap.c_code.mpi_recv_int_array
        self.__array_recv_int.argtypes = [CT.c_void_p, CT.c_int, CT.c_int, CT.c_int]
        self.__array_recv_int.restype = CT.c_int

        self.temp_P = CT.c_void_p()

        self.__array_recv_double = CWrap.c_code.mpi_recv_double_array
        self.__array_recv_double.argtypes = [CT.c_void_p, CT.c_int, CT.c_int, CT.c_int]
        self.__array_recv_double.restype = CT.c_int

        self.__reduce_Sum_int = CWrap.c_code.reduceSum
        self.__reduce_Sum_int.argtypes = [CT.c_int, CT.c_int, CT.c_int]
        self.__reduce_Sum_int.restype = CT.c_int

        self.__reduce_Sum_double = CWrap.c_code.reduceSumDouble
        self.__reduce_Sum_double.argtypes = [CT.c_double, CT.c_int, CT.c_int]
        self.__reduce_Sum_double.restype = CT.c_double

        self.__Bcast_int = CWrap.c_code.mpi_Bcast_int
        self.__Bcast_int.argtypes = [CT.c_void_p,CT.c_int, CT.c_int, CT.c_int]

        self.__Bcast_double = CWrap.c_code.mpi_Bcast_double
        self.__Bcast_double.argtypes = [CT.c_void_p,CT.c_int, CT.c_int, CT.c_int]

        self.__scatter = CWrap.c_code.mpi_scatter
        self.__scatter.argtypes = [CT.c_void_p, CT.c_int, CT.c_int, CT.c_void_p, CT.c_int, CT.c_int, CT.c_int]

        self.__gather = CWrap.c_code.mpi_gather_s
        self.__gather.argtypes = [CT.c_void_p, CT.c_int, CT.c_int, CT.c_void_p, CT.c_int, CT.c_int]

        self.__barrier = CWrap.c_code.barrier
        self.__barrier.argtypes = [CT.c_int]
        self.__barrier.restype = CT.c_int

        self.__super_free = CWrap.c_code.super_free
        self.__super_free.argtypes = [CT.c_void_p]

        self.__matmul_double = CWrap.c_code.matmul_double
        self.__matmul_double.argtypes = [
            CT.c_void_p, CT.c_void_p, CT.c_int,
            CT.c_int, CT.c_int, CT.c_void_p
        ]

        self.__get_processor_name = CWrap.c_code.mpi_get_processor_name
        self.__get_processor_name.argtypes = [CT.c_void_p]

        self.__reduceChoiceInt = CWrap.c_code.reduceChoiceInt
        self.__reduceChoiceInt.argtypes = [CT.c_void_p, CT.c_int, CT.c_void_p, CT.c_int, CT.c_int, CT.c_int]
        self.__reduceChoiceInt.restype = CT.c_int

        self.__finalize = CWrap.c_code.MPI_Finalize

        CWrap.c_code.MPI_Init()
        self.rank = self.rankf()
        self.size = self.sizef()
        self.sizeS = self.size - 1 # when main is not considered a worker.
        atexit.register(self.__finalize)

    def rankf(self, comm = cworld) -> int:
        """Rank of the individual node."""
        return self.__rank(comm)

    def sizef(self, comm = cworld) -> int:
        """Size of working pool"""
        return self.__size(comm)