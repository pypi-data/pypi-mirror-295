#
# Copyright (C) 2024, Northwestern University and Argonne National Laboratory
# See COPYRIGHT notice in top-level directory.
#

"""
This example shows how to use `Variable` method `put_var()` to write a 2D
integer array variable into a file. The variable in the file is a dimensional
transposed array from the one stored in memory. In memory, a 2D array is
partitioned among all processes in a block-block fashion in YX (i.e.
row-major) order. The dimension structure of the transposed array is arrays are
    int YX_var(Y, X) ;
    int XY_var(X, Y) ;

To run:
  % mpiexec -n num_process python3 transpose2D.py [filename] [-l len]

  where len decides the size of local array, which is len x (len+1).
  So, each variable is of size len*(len+1) * nprocs * sizeof(int)

   % mpiexec -n 4 python3 transpose2D.py testfile.nc
   % ncdump testfile.nc
     netcdf testfile {
     dimensions:
              Y = 4 ;
              X = 6 ;
     variables:
             int YX_var(Y, X) ;
             int XY_var(X, Y) ;
     data:

     YX_var =
       0, 1, 2, 3, 4, 5,
       6, 7, 8, 9, 10, 11,
       12, 13, 14, 15, 16, 17,
       18, 19, 20, 21, 22, 23 ;

     XY_var =
       0, 6, 12, 18,
       1, 7, 13, 19,
       2, 8, 14, 20,
       3, 9, 15, 21,
       4, 10, 16, 22,
       5, 11, 17, 23 ;
     }

"""

import sys, os, argparse
import numpy as np
from mpi4py import MPI
import pnetcdf

def pnetcdf_io(filename, file_format, length):
    NDIMS = 2

    if verbose and rank == 0:
        print("Number of dimensions = ", NDIMS)

    gsizes = np.zeros(NDIMS, dtype=np.int64)
    start = np.zeros(NDIMS, dtype=np.int64)
    count = np.zeros(NDIMS, dtype=np.int64)
    imap = np.zeros(NDIMS, dtype=np.int64)
    startT = np.zeros(NDIMS, dtype=np.int64)
    countT = np.zeros(NDIMS, dtype=np.int64)

    psizes = MPI.Compute_dims(nprocs, NDIMS)

    if verbose and rank == 0:
        str = "psizes= "
        for i in range(NDIMS):
            str += "%d " % psizes[i]
        print(str)

    # set subarray access pattern
    lower_dims = 1
    for i in range(NDIMS - 1, -1, -1):
        start[i] = rank // lower_dims % psizes[i]
        lower_dims *= psizes[i]

    if verbose:
        str = "proc %d: dim rank= " % rank
        for i in range(NDIMS):
            str += "%d " % start[i]
        print(str)

    bufsize = 1
    gsizes = np.zeros(NDIMS, dtype=np.int64)
    for i in range(NDIMS):
        gsizes[i] = (length + i) * psizes[i]
        start[i] *= (length + i)
        count[i] = (length + i)
        bufsize *= (length + i)

    # initialize write buffer
    buf = np.zeros(bufsize, dtype=np.int32)
    for i in range(count[0]):
        for j in range(count[1]):
            buf[i * count[1] + j] = (start[0] + i) * gsizes[1] + (start[1] + j)


    # Create the file
    f = pnetcdf.File(filename = filename,
                     mode = 'w',
                     format = file_format,
                     comm = comm,
                     info = None)

    # Define dimensions
    dim_y = f.def_dim("Y", gsizes[0])
    dim_x = f.def_dim("X", gsizes[1])

    # Define variable with no transposed file layout: ZYX
    var_yx = f.def_var("YX_var", pnetcdf.NC_INT, (dim_y, dim_x))
    var_xy = f.def_var("XY_var", pnetcdf.NC_INT, (dim_x, dim_y))

    # Exit the define mode
    f.enddef()

    # Write the whole variable in file: ZYX
    var_yx.put_var_all(buf, start=start, count=count)

    # Transpose YX -> XY */
    imap[0] = 1
    imap[1] = count[1]
    startT[0] = start[1]
    startT[1] = start[0]
    countT[0] = count[1]
    countT[1] = count[0]
    var_xy.put_var_all(buf, start = startT, count = countT, imap = imap)

    # Close the file
    f.close()


def parse_help():
    help_flag = "-h" in sys.argv or "--help" in sys.argv
    if help_flag and rank == 0:
        help_text = (
            "Usage: {} [-h] | [-q] [file_name]\n"
            "       [-h] Print help\n"
            "       [-q] Quiet mode (reports when fail)\n"
            "       [-k format] file format: 1 for CDF-1, 2 for CDF-2, 5 for CDF-5\n"
            "       [-l len] size of each dimension of the local array\n"
            "       [filename] (Optional) output netCDF file name\n"
        ).format(sys.argv[0])
        print(help_text)
    return help_flag

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nprocs = comm.Get_size()

    if parse_help():
        MPI.Finalize()
        sys.exit(1)

    # get command-line arguments
    args = None
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", nargs="?", type=str, help="(Optional) output netCDF file name",\
                         default = "testfile.nc")
    parser.add_argument("-q", help="Quiet mode (reports when fail)", action="store_true")
    parser.add_argument("-k", help="File format: 1 for CDF-1, 2 for CDF-2, 5 for CDF-5")
    parser.add_argument("-l", help="size of each dimension of the local array")
    args = parser.parse_args()

    verbose = False if args.q else True

    file_format = None
    if args.k:
        kind_dict = {'1':None, '2':"NC_64BIT_OFFSET", '5':"NC_64BIT_DATA"}
        file_format = kind_dict[args.k]

    length = 2
    if args.l and int(args.l) > 0: length = int(args.l)

    filename = args.dir

    if verbose and rank == 0:
        print("{}: example of put/get 2D transposed arrays".format(os.path.basename(__file__)))

    try:
        pnetcdf_io(filename, file_format, length)
    except BaseException as err:
        print("Error: type:", type(err), str(err))
        raise

    MPI.Finalize()

