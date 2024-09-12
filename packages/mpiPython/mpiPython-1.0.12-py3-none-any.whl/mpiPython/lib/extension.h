/*
File: extension.h
Modification Date: 8/13/24
Time Modified: 11:23pm CT
Created by: Judah Nava
Last Modified By: Judah Nava
Organization: Parallel Solvit LLC and MSUM CSIS Department
*/
#ifndef EXTENSION_H_
#define EXTENSION_H_

/*
    These are beta functions that are planned on being added. 
*/

void mpi_alllgather(void* ,int, int, void*, int) ;


void* mpi_allgather(void* sendbuf, int count, int datatypeKey, int comm)
/*
    Note, since all processes have to call this, the code assumes that rank
    zero is also calling it.
    Note, this also frees the sendbuf at the end!
*/
{
	MPI_Datatype data;
    void* recvbuf ;
    int rank ;
    int size ;
    MPI_Comm_size(comm, &size) ;
    MPI_Comm_rank(comm, &rank) ;
    int maxCount ;
    MPI_Reduce(&count, &maxCount, 1, MPI_INT, MPI_MAX, 0, comm) ;
    MPI_Bcast(&maxCount, 1, MPI_INT, 0, comm) ;
    
	if (datatypeKey == 1)
	{
		data = MPI_INT;
        recvbuf = (void*) malloc (sizeof(int)*size*count) ;
	}
	else if (datatypeKey == 2)
	{
		data = MPI_DOUBLE;
        recvbuf = (void*) malloc (sizeof(double)*size*count) ;
	}
	MPI_Allgather(sendbuf, maxCount, data, recvbuf, maxCount, data, comm) ;
    // free(sendbuf) ;
    return recvbuf ;
}

void* mpi_allgather_Alpha(void* sendbuf, int count, int datatypeKey, int comm)
/*
    This is scratch work for a version of allgather that does not require that
    all lists are of the same size. 
    Note, since all processes have to call this, the code assumes that rank
    zero is also calling it.
*/
{
	MPI_Datatype data;
    void* recvbuf ;
    int rank ;
    int size ;
    MPI_Comm_size(comm, &size) ;
    MPI_Comm_rank(comm, &rank) ;
    int maxCount ;
    MPI_Reduce(&count, &maxCount, 1, MPI_INT, MPI_MAX, 0, comm) ;
    MPI_Bcast(&maxCount, 1, MPI_INT, 0, comm) ;
    
	if (datatypeKey == 1)
	{
		data = MPI_INT;
        recvbuf = (void*) malloc (sizeof(int)*size) ;
        sendbuf = (void*) malloc (sizeof(int)*maxCount+1) ;
	}
	else if (datatypeKey == 2)
	{
		data = MPI_DOUBLE;
        recvbuf = (void*) malloc (sizeof(double)*size) ;
        sendbuf = (void*) malloc (sizeof(double)*maxCount+1) ;
	}
	MPI_Allgather(sendbuf, maxCount+1, data, recvbuf, 1, data, comm) ;
    return recvbuf ;
}

#endif