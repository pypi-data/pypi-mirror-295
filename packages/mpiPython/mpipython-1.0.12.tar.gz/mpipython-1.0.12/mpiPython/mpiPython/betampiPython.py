"""
File: mpiPython.py
Modification Date: 8/13/24
Time Modified: 11:23pm CT
Created by: Judah Nava
Last Modified By: Judah Nava
Organization: Parallel Solvit LLC and MSUM CSIS Department
"""

import os, atexit, subprocess, sys, ctypes as CT
import pickle

from .mpiPython import (
    MPIpy,
    MPI_Status,
)

class betaMPIpy(MPIpy):

    
    def __init__(self):
        super().__init__()

        self.__double_send = MPIpy.c_code.mpi_send_double
        self.__double_send.argtypes = [CT.c_double, CT.c_int, CT.c_int, CT.c_int, CT.c_int]

        self.__double_recv = MPIpy.c_code.mpi_recv_double
        self.__double_recv.argtypes = [CT.c_int, CT.c_int, CT.c_int]
        self.__double_recv.restype = CT.c_double

        self.__MPI_Abort = MPIpy.c_code.MPI_Abort
                                    # comm     error code
        self.__MPI_Abort.argtypes = [CT.c_int, CT.c_int]
        self.__MPI_Abort.restype = CT.c_int

        self.__MPI_Allgather = MPIpy.c_code.mpi_allgather
        self.__MPI_Allgather.argtypes = [CT.c_void_p, CT.c_int, CT.c_int, CT.c_int]
        self.__MPI_Allgather.restype = CT.c_void_p

        self.__MPI_pSend = MPIpy.c_code.mpi_pSend
        self.__MPI_pSend.argtypes = [CT.c_void_p, CT.c_int, CT.c_int, CT.c_int, CT.c_int]


        

        print("!!! You are using the beta MPIpy class, not meant for production. !!!")
    
    def MPI_Send(self, value, dest, tag, comm_m = MPIpy.cworld ) -> None:
        """
            Here is what is should support:
            Send_beta(3, 1, 1) ;
            Send_beta([3,5], 1, 1) ;
            Send_beta(3.4564, 1, 1) ;
            Send_beta([3.2, 5.9, 1.234], 1, 1) ;
            Send_beta(4j+2, 1, 1) ;
            Send_beta([4j+1, 7.3j+99, 1j+58.3], 1, 1)
        """
        typ = type(value)
        if typ == int:
            self.send_int(1,dest,tag)
            self._CWrap__int_send(value, 1, dest, tag, comm_m)
            pass
        elif typ == float:
            self.send_int(2,dest,tag)
            self.__double_send(value, 1, dest, tag, comm_m)
            pass
        elif typ == list:
            if not value:
                #list is empty
                self.send_int(5,dest,tag)
                return None
            length = len(value)
            typ = type(value[0])
            if typ == int:
                if not all(isinstance(x,int) for x in value):
                    self.send_int(5,dest,tag)
                    return None
                self.send_int(3,dest,tag)
                parsedData = (CT.c_long * length)(*value)
                self._CWrap__array_send_int(parsedData, length, dest, tag, comm_m)
                pass
            elif typ == float:
                if not all(isinstance(x,float) for x in value):
                    self.send_int(5,dest,tag)
                    return None
                self.send_int(4,dest,tag)
                parsedData = (CT.c_double * length)(*value)
                self._CWrap__array_send_double(parsedData, length, dest, tag, comm_m)
                pass
            else:
                # Error
                self.send_int(5,dest,tag)
                return None

        else:
            # Error
            self.send_int(5,dest,tag)
            return None

    def MPI_Recv(self, source, tag, comm_m = MPIpy.cworld, MPI_STATUS:MPI_Status = None) -> list[int,float,list[int],list[float]]:
        typ = self.recv_int(source,tag)
        if typ == 1:
            return self._CWrap__int_recv(1, source, tag, comm_m)
        elif typ == 2:
            return self.__double_recv(source, tag, comm_m)
        elif typ == 3:
            length = self._CWrap__array_recv_int(CT.pointer(self.temp_P), source, tag, comm_m)
            test2 = (CT.c_long * length).from_address(self.temp_P.value)
            tmp = test2[::]
            self._CWrap__super_free(CT.pointer(self.temp_P))
            return tmp
        elif typ == 4:
            length = self._CWrap__array_recv_double(CT.pointer(self.temp_P), source, tag, comm_m)
            test2 = (CT.c_double * length).from_address(self.temp_P.value)
            tmp = test2[::]
            self._CWrap__super_free(CT.pointer(self.temp_P))
            return tmp
        elif typ == 5:
            print("Unnown send call issue sent over, semantic error")
            self.__MPI_Abort(comm_m, 17)

    def MPI_pSend(self, value, dest, tag, comm_m = MPIpy.cworld ) -> None:
        value_pickled = pickle.dumps(value)
        length = len(value_pickled)
        parsedData = (CT.c_byte * length)(*value_pickled)
        self.__MPI_pSend(parsedData, length, dest, tag, comm_m)
    
    def MPI_pRecv(self, source, tag, comm_m = MPIpy.cworld, MPI_STATUS:MPI_Status = None): # Can return anything.
        pass


    def MPI_Allgather(self, source: list[int,float], comm = MPIpy.cworld) -> list[int,float]:
        """
            This needs to be checked for memory leaks!
        """
        lengthS = len(source)
        sType = 0
        if type(source[0]) == int:
            sType = 1
            temp_ar = lengthS * CT.c_int
            temp = temp_ar()
            for i in range(lengthS):
                temp[i] = source[i]

        elif type(source[0]) == float:
            sType = 2
            temp_ar = lengthS * CT.c_double
            temp = temp_ar()
            for i in range(lengthS):
                temp[i] = source[i]
        
        if sType == 0:
            print("Error")
            self.__MPI_Abort()
        
        self.temp_P = self.__MPI_Allgather(CT.pointer(temp),lengthS,sType,comm)
        if sType == 1: # int
            tmp2 = (CT.c_int * (lengthS * self.size))
            tmp2 = tmp2.from_address(self.temp_P)
            
        elif sType == 2: # float
            tmp2 = (CT.c_double * (lengthS * self.size))
            tmp2 = tmp2.from_address(self.temp_P)
        # self._CWrap__super_free(self.temp_P)
        return tmp2[::]



