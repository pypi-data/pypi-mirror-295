#
# Copyright (C) 2024, Northwestern University and Argonne National Laboratory
# See COPYRIGHT notice in top-level directory.
#

"""
This example shows how to use `Variable` method `put_var()` to write six 3D
integer array variables into a file. Each variable in the file is a dimensional
transposed array from the one stored in memory. In memory, a 3D array is
partitioned among all processes in a block-block-block fashion and in ZYX (i.e.
C) order. The dimension structures of the transposed six arrays are
        int ZYX_var(Z, Y, X) ;     ZYX -> ZYX
        int ZXY_var(Z, X, Y) ;     ZYX -> ZXY
        int YZX_var(Y, Z, X) ;     ZYX -> YZX
        int YXZ_var(Y, X, Z) ;     ZYX -> YXZ
        int XZY_var(X, Z, Y) ;     ZYX -> XZY
        int XYZ_var(X, Y, Z) ;     ZYX -> XYZ

To run:
  % mpiexec -n num_process python3 transpose.py [filename] [-l len]

  where len decides the size of local array, which is len x (len+1) x (len+2).
  So, each variable is of size len*(len+1)*(len+2) * nprocs * sizeof(int)

"""

import sys, os, argparse
import numpy as np
from mpi4py import MPI
import pnetcdf

def pnetcdf_io(filename, file_format, length):

    NDIMS = 3
    if verbose and rank == 0:
        print("Number of dimensions = ", NDIMS)

    gsizes = np.zeros(NDIMS, dtype=np.int64)
    start  = np.zeros(NDIMS, dtype=np.int64)
    count  = np.zeros(NDIMS, dtype=np.int64)
    imap   = np.zeros(NDIMS, dtype=np.int64)
    startT = np.zeros(NDIMS, dtype=np.int64)
    countT = np.zeros(NDIMS, dtype=np.int64)

    # calculate number of processes along each dimension
    psizes = MPI.Compute_dims(nprocs, NDIMS)
    if rank == 0 and verbose:
        print("psizes =", psizes)

    # for each MPI rank, find its local rank IDs along each dimension in start[]
    lower_dims = 1
    for i in range(NDIMS-1, -1, -1):
        start[i] = rank // lower_dims % psizes[i]
        lower_dims *= psizes[i]
    if verbose:
        print("proc {}: dim rank = {}".format(rank, start))

    # set up subarray access pattern
    bufsize = 1
    for i in range(NDIMS):
        gsizes[i]  = (length + i) * psizes[i]  # global array size
        start[i]  *= (length + i)  # start indices
        count[i]   = (length + i)  # array elements
        bufsize   *= (length + i)

    # allocate buffer and initialize with contiguous numbers
    buf = np.empty(bufsize, dtype=int)
    index = 0
    for k in range(count[0]):
        for j in range(count[1]):
            for i in range(count[2]):
                buf[index] = (start[0]+k)*gsizes[1]*gsizes[2] + \
                             (start[1]+j)*gsizes[2] + \
                             (start[2]+i)
                index += 1

    # Create the file
    f = pnetcdf.File(filename = filename,
                     mode = 'w',
                     format = file_format,
                     comm = comm,
                     info = None)

    # Define dimensions
    dim_z = f.def_dim("Z", gsizes[0])
    dim_y = f.def_dim("Y", gsizes[1])
    dim_x = f.def_dim("X", gsizes[2])

    # Define variable with no transposed file layout: ZYX
    var_zyx = f.def_var("ZYX_var", pnetcdf.NC_INT, (dim_z, dim_y, dim_x))

    # Define variable with transposed file layout: ZXY
    var_zxy = f.def_var("ZXY_var", pnetcdf.NC_INT, (dim_z, dim_x, dim_y))

    # Define variable with transposed file layout: YZX
    var_yzx = f.def_var("YZX_var", pnetcdf.NC_INT, (dim_y, dim_z, dim_x))

    # Define variable with transposed file layout: YXZ
    var_yxz = f.def_var("YXZ_var", pnetcdf.NC_INT, (dim_y, dim_x, dim_z))

    # Define variable with transposed file layout: XZY
    var_xzy = f.def_var("XZY_var", pnetcdf.NC_INT, (dim_x, dim_z, dim_y))

    # Define variable with transposed file layout: XYZ
    var_xyz = f.def_var("XYZ_var", pnetcdf.NC_INT, (dim_x, dim_y, dim_z))

     # Exit the define mode
    f.enddef()
    # Write the whole variable in file: ZYX
    var_zyx.put_var_all(buf, start=start, count=count)

    # ZYX -> ZXY:
    imap[1] = 1;  imap[2] = count[2]; imap[0] = count[1]*count[2]
    startT[0] = start[0]; startT[1] = start[2]; startT[2] = start[1]
    countT[0] = count[0]; countT[1] = count[2]; countT[2] = count[1]
    var_zxy.put_var_all(buf, start = startT, count = countT, imap = imap)

    # ZYX -> ZXY:
    imap[1] = 1; imap[2] = count[2]; imap[0] = count[1]*count[2]
    startT[0] = start[0]; startT[1] = start[2]; startT[2] = start[1]
    countT[0] = count[0]; countT[1] = count[2]; countT[2] = count[1]
    var_zxy.put_var_all(buf, start=startT, count=countT, imap=imap)

    # ZYX -> YZX:
    imap[2] = 1; imap[0] = count[2]; imap[1] = count[1]*count[2]
    startT[0] = start[1]; startT[1] = start[0]; startT[2] = start[2]
    countT[0] = count[1]; countT[1] = count[0]; countT[2] = count[2]
    var_yzx.put_var_all(buf, start=startT, count=countT, imap=imap)

    # ZYX -> YXZ:
    imap[1] = 1; imap[0] = count[2]; imap[2] = count[1]*count[2]
    startT[0] = start[1]; startT[1] = start[2]; startT[2] = start[0]
    countT[0] = count[1]; countT[1] = count[2]; countT[2] = count[0]
    var_yxz.put_var_all(buf, start=startT, count=countT, imap=imap)

    # ZYX -> XZY:
    imap[0] = 1; imap[2] = count[2]; imap[1] = count[1]*count[2]
    startT[0] = start[2]; startT[1] = start[0]; startT[2] = start[1]
    countT[0] = count[2]; countT[1] = count[0]; countT[2] = count[1]
    var_xzy.put_var_all(buf, start=startT, count=countT, imap=imap)

    # ZYX -> XYZ:
    imap[0] = 1; imap[1] = count[2]; imap[2] = count[1]*count[2]
    startT[0] = start[2]; startT[1] = start[1]; startT[2] = start[0]
    countT[0] = count[2]; countT[1] = count[1]; countT[2] = count[0]
    var_xyz.put_var_all(buf, start=startT, count=countT, imap=imap)

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

    length = 10
    if args.l and int(args.l) > 0: length = int(args.l)

    filename = args.dir

    if verbose and rank == 0:
        print("{}: example of put/get 3D transposed arrays".format(os.path.basename(__file__)))

    try:
        pnetcdf_io(filename, file_format, length)
    except BaseException as err:
        print("Error: type:", type(err), str(err))
        raise

    MPI.Finalize()

