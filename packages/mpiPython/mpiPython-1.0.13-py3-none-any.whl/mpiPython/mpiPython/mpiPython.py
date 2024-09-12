"""
File: mpiPython.py
Modification Date: 8/14/24
Time Modified: 12:56pm CT
Created by: Judah Nava
Last Modified By: Judah Nava
Organization: Parallel Solvit LLC and MSUM CSIS Department
"""

import os, atexit, subprocess, sys, ctypes as CT

from .CWrap import (
    CWrap,
)

class MPIpyWrongArgument(Exception):
    pass

class MPI_Status:
    pass

class MPIpy(CWrap):
    # The initialization of this class is in CWrap

    """
        Thets reserved tags should not be used by the programmer,
        they are needed for meta communication by the Class
    """
    reserved_tags = [
        -1,
        -2,
        -3,
    ]
    
    def Rank(self, comm = CWrap.cworld) -> int:
        """Rank of the individual node."""
        return self.rankf()

    def Size(self, comm = CWrap.cworld) -> int:
        """Size of working pool"""
        return self.sizef()

    def send_int(self, data: int, dest: int, tag: int, comm_m = CWrap.cworld) -> None:
        """Sends data over MPI_Send, default only needs 3 arguments."""
        return self._CWrap__int_send(data, 1, dest, tag, comm_m)

    def recv_int(self, source: int, tag: int, comm_m = CWrap.cworld) -> int:
        """Return data sent over MPI_Send, default only needs 2 arguments"""
        return self._CWrap__int_recv(1, source, tag, comm_m)

    def send_int_array(self, data: list, dest: int, tag: int, comm_m = CWrap.cworld) -> None:
        """Sends a list of integers over mpi."""
        length = len(data)
        parsedData = (CT.c_long * length)(*data)
        self._CWrap__array_send_int(parsedData, length, dest, tag, comm_m)

    def send_double_array(self, data: list, dest: int, tag: int, comm_m = CWrap.cworld) -> None:
        """Sends a list of floats over mpi."""
        length = len(data)
        parsedData = (CT.c_double * length)(*data)
        self._CWrap__array_send_double(parsedData, length, dest, tag, comm_m)

    def recv_int_array(self, dataE: list,  source: int, tag: int, comm_m = CWrap.cworld) -> None:
        """Overwrites a given list of integers sent over mpi."""
        length = self._CWrap__array_recv_int(CT.pointer(self.temp_P), source, tag, comm_m)
        test2 = (CT.c_long * length).from_address(self.temp_P.value)
        dataE.clear()
        dataE.extend(test2[::])
        self._CWrap__super_free(CT.pointer(self.temp_P))

    def recv_double_array(self, dataE: list, source: int, tag: int, comm_m = CWrap.cworld) -> None:
        """Overwrites a given list of doubles (floats) sent over mpi."""
        length = self._CWrap__array_recv_double(CT.pointer(self.temp_P), source, tag, comm_m)
        test2 = (CT.c_double * length).from_address(self.temp_P.value)
        dataE.clear()
        dataE.extend(test2[::])
        self._CWrap__super_free(CT.pointer(self.temp_P))

    def reduceChoiceInt(self, data: int | list[int], root: int, choice:str, comm_m = CWrap.cworld ) -> list[int]:
        dataRe = []
        try:
            ch = MPIpy.minidict[choice]
        except:
            print("redice choice invalid")
            exit(-1)
        if type(data) == int:
            data = list(data)
        length = len(data)
        parsedData = (CT.c_long * length)(*data)
        self.__reduceChoiceInt(CT.pointer(parsedData),length, CT.pointer(self.temp_P), root, comm_m,  ch)
        if root == self.rank:
            data = (CT.c_long * length).from_address(self.temp_P.value)
            dataRe.extend(data[::])
            self.__super_free(CT.pointer(self.temp_P))
            return dataRe
        else:
            return data

    def reduceSumInt(self, sum, master, comm_m = CWrap.cworld) -> int:
        """All nodes include their parial sum for it to be added
            all together then returned to everyone what the total sum is."""
        return self._CWrap__reduce_Sum_int(sum, master, comm_m)

    def reduceSumDouble(self, sum, master, comm_m=CWrap.cworld) -> float:
        """All nodes include their partial sum for it to be added
            all together when returned to everyone what the total sum is."""
        return self._CWrap__reduce_Sum_double(sum, master, comm_m)
    
    def Bcast_int(self, data, sender: int, comm_m = CWrap.cworld) -> None:
        """Use MPI Bcast send over an int or a list of int's to all.
            !!non-senders must always pass in an empty list into data.
        """
        if type(data) == int:
            data = [data]
        temp_ar = 1 * CT.c_int
        temp = temp_ar()
        if self.rank == sender:
            temp[0] = len(data)
            self.__Bcast_int(CT.pointer(temp), 1, sender, comm_m)
            temp_ar = temp[0] * CT.c_int
            temp = temp_ar()
            for i in range(len(data)):
                temp[i] = data[i]
            self.__Bcast_int(CT.pointer(temp), len(data), sender, comm_m)
        else:
            self.__Bcast_int(CT.pointer(temp), 1, sender, comm_m)
            length = temp[0]
            temp_ar2 = length * CT.c_int
            temp2 = temp_ar2()
            self.__Bcast_int(CT.pointer(temp2), length, sender, comm_m)
            for i in range(length):
                data.append(temp2[i])
    
    def Bcast_double(self, data, sender: int, comm_m = CWrap.cworld) -> None:
        """Use MPI Bcast send over an float or a list of float's to all.
            !!non-senders must always pass in an empty list into data.
            is a single float is sent over, a list with 2 values, 0.0 being the seccond will return.
        """
        if type(data) == float:
            data = [data,0.0] # python seems to make a mess unless i add the 0.0
        temp_ar = 1 * CT.c_int
        temp = temp_ar()
        if self.rank == sender:
            temp[0] = len(data)
            self._CWrap__Bcast_int(CT.pointer(temp), 1, sender, comm_m)
            temp_ar = temp[0] * CT.c_double
            temp = temp_ar()
            for i in range(len(data)):
                temp[i] = data[i]
            self._CWrap__Bcast_double(CT.pointer(temp), len(data), sender, comm_m)
        else:
            self._CWrap__Bcast_int(CT.pointer(temp), 1, sender, comm_m)
            length = temp[0]
            temp_ar2 = length * CT.c_double
            temp2 = temp_ar2()
            self._CWrap__Bcast_double(CT.pointer(temp2), length, sender, comm_m)
            for i in range(length):
                data.append(temp2[i])

    def Scatter(self, dataList: list, sender, comm_m = CWrap.cworld) -> None:
        """MPI_Scatter for MPIpy."""
        scrap_data = CT.c_int * 2
        scrap = scrap_data()
        scrapP = CT.pointer(scrap)


        if self.rank == sender:
            lengthM = len(dataList)
            lengthS = int(lengthM / self.size)

            if (lengthM % self.size) != 0:
                self.Bcast_int([0, 0, 0], sender)
                print("The data needs to be equally divided among all in the comm.")
                print("Stopped MPI_Scatter")
                return
            
            if type(dataList[0]) == int:
                sType = 1
                temp_ar = lengthM * CT.c_int
                temp = temp_ar()
                for i in range(lengthM):
                    temp[i] = dataList[i]
                mast_ar = lengthS * CT.c_int
                mast = mast_ar()
            elif type(dataList[0]) == float:
                sType = 2
                temp_ar = lengthM * CT.c_double
                temp = temp_ar()
                for i in range(lengthM):
                    temp[i] = dataList[i]
                mast_ar = lengthS * CT.c_double
                mast = mast_ar()
                
            else:
                self.Bcast_int([0, 0, 0], sender, comm_m)
                print("The data was not recognised.")
                print("Stopped MPI_Scatter")
                return

            self.Bcast_int([lengthM, lengthS, sType], sender, comm_m)

            self.__scatter(CT.pointer(temp), lengthS, sType, CT.pointer(mast), lengthS, sender, comm_m)
            # temp_l = dataList[:lengthS]
            dataList.clear()
            for i in range(lengthS):
                dataList.append(mast[i])

        else:
            data = []
            self.Bcast_int(data, sender, comm_m)
            if data[0] == 0:
                print("Was given an error commnd, stopped MPI_Scatter")
                return
            lengthM = data[0]
            lengthS = data[1]
            sType = data[2]
            if sType == 1:
                temp_ar = lengthS * CT.c_int
            if sType == 2:
                temp_ar = lengthS * CT.c_double
            temP = temp_ar()
            temp = CT.pointer(temP)
            self._CWrap__scatter(scrapP, lengthS, sType, temp, lengthS, sender, comm_m)
            for i in range(lengthS):
                dataList.append(temp.contents[i])

    def gather(self, dataList: list, sender, comm_m = CWrap.cworld) -> int | None:
        """MPI_Gather for MPIpy."""

        lengthS = len(dataList)

        if type(dataList[0]) == int:
            sType = 1
            temp_ar = lengthS * CT.c_int
            temp = temp_ar()
            for i in range(lengthS):
                temp[i] = dataList[i]

        elif type(dataList[0]) == float:
            sType = 2
            temp_ar = lengthS * CT.c_double
            temp = temp_ar()
            for i in range(lengthS):
                temp[i] = dataList[i]

        self._CWrap__gather(CT.pointer(temp), lengthS, sType, CT.pointer(self.temp_P), sender, comm_m)

        dataList.clear()
        if self.rank == sender:
            if sType == 1: # int
                tmp2 = (CT.c_int * (lengthS * self.size))
                tmp2 = tmp2.from_address(self.temp_P.value)
                # dataList.extend(tmp2[::]) 
            if sType == 2: # float
                tmp2 = (CT.c_double * (lengthS * self.size))
                tmp2 = tmp2.from_address(self.temp_P.value)
                # dataList.extend(tmp2[::]) 
            self._CWrap__super_free(CT.pointer(self.temp_P))
            return tmp2[::]
        else:
            self._CWrap__super_free(CT.pointer(self.temp_P))

    def Get_processor_name(self, comm = CWrap.cworld) -> str:
        """Get the name of the processor."""
        # name = CT.create_string_buffer(256)
        self._CWrap__get_processor_name(CT.pointer(self.temp_P))
        test2 = (CT.c_char * 256).from_address(self.temp_P.value) # switched to c_char
        self._CWrap__super_free(CT.pointer(self.temp_P))
        return test2.value  # changed to test2.value

    def barrier(self, comm_m = CWrap.cworld) -> None:
            """MPI_Barrier"""        
            self._CWrap__barrier(comm_m)
    
    def matmulC(self, LA: list, LB: list, rowA: int, shareB: int, colC: int, LC: list) -> None:
        """Uses a simple matrix algorithm but in c... so its allot faster.
            LA[rowA][shareB]
            LB[shareB][colC]
            LC[rowA][colC] this needs to be an empty python list to append to.   
        """
  
        lengthA = rowA * shareB
        lengthB = shareB * colC
        lengthC = rowA * colC
        parsedDataA = (CT.c_double * lengthA)(*LA)
        parsedDataB = (CT.c_double * lengthB)(*LB)
        self.__matmul_double(
            parsedDataA, parsedDataB, 
            rowA, shareB, colC,
            CT.pointer(self.temp_P),
            )
        test2 = (CT.c_double * lengthC).from_address(self.temp_P.value)
        LC.extend(test2[::])
        self._CWrap__super_free(CT.pointer(self.temp_P))



