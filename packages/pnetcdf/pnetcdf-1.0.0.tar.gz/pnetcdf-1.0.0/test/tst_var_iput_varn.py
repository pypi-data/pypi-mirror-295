#
# Copyright (C) 2024, Northwestern University and Argonne National Laboratory
# See COPYRIGHT notice in top-level directory.
#

"""
This program tests nonblocking method, iput_varn() of `Variable` class, by
making a write request consisting of multiple subarrays to a variable of an
opened netCDF file.  The library will internally invoke ncmpi_iput_varn() in C.
"""
import pnetcdf
from numpy.testing import assert_array_equal
import unittest, os, sys
import numpy as np
from mpi4py import MPI
from pnetcdf import strerror, strerrno
from utils import validate_nc_file
import io

file_formats = ['NC_64BIT_DATA', 'NC_64BIT_OFFSET', None]
file_name = "tst_var_iput_varn.nc"

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()
xdim = 4
ydim = 10

# max number of subarrays requested among all iput requests from all ranks
max_num_subarray = 6
ndims = 2

starts = np.zeros((max_num_subarray, ndims), dtype=np.int64)
counts = np.zeros((max_num_subarray, ndims), dtype=np.int64)

# initialize variable values
if rank == 0:
    # number of subarrays to request for each process
    num_subarrays = 4
    starts[0][0] = 0; starts[0][1] = 5; counts[0][0] = 1; counts[0][1] = 2
    starts[1][0] = 1; starts[1][1] = 0; counts[1][0] = 1; counts[1][1] = 1
    starts[2][0] = 2; starts[2][1] = 6; counts[2][0] = 1; counts[2][1] = 2
    starts[3][0] = 3; starts[3][1] = 0; counts[3][0] = 1; counts[3][1] = 3
    # rank 0 is writing the following locations: ("-" means skip)
    #               -  -  -  -  -  0  0  -  -  -
    #               0  -  -  -  -  -  -  -  -  -
    #               -  -  -  -  -  -  0  0  -  -
    #               0  0  0  -  -  -  -  -  -  -
elif rank == 1:
    num_subarrays = 6
    starts[0][0] = 0; starts[0][1] = 3; counts[0][0] = 1; counts[0][1] = 2
    starts[1][0] = 0; starts[1][1] = 8; counts[1][0] = 1; counts[1][1] = 2
    starts[2][0] = 1; starts[2][1] = 5; counts[2][0] = 1; counts[2][1] = 2
    starts[3][0] = 2; starts[3][1] = 0; counts[3][0] = 1; counts[3][1] = 2
    starts[4][0] = 2; starts[4][1] = 8; counts[4][0] = 1; counts[4][1] = 2
    starts[5][0] = 3; starts[5][1] = 4; counts[5][0] = 1; counts[5][1] = 3
    # rank 1 is writing the following locations: ("-" means skip)
    #               -  -  -  1  1  -  -  -  1  1
    #               -  -  -  -  -  1  1  -  -  -
    #               1  1  -  -  -  -  -  -  1  1
    #               -  -  -  -  1  1  1  -  -  -
elif rank == 2:
    num_subarrays = 5
    starts[0][0] = 0; starts[0][1] = 7; counts[0][0] = 1; counts[0][1] = 1
    starts[1][0] = 1; starts[1][1] = 1; counts[1][0] = 1; counts[1][1] = 3
    starts[2][0] = 1; starts[2][1] = 7; counts[2][0] = 1; counts[2][1] = 3
    starts[3][0] = 2; starts[3][1] = 2; counts[3][0] = 1; counts[3][1] = 1
    starts[4][0] = 3; starts[4][1] = 3; counts[4][0] = 1; counts[4][1] = 1
    # rank 2 is writing the following locations: ("-" means skip)
    #         -  -  -  -  -  -  -  2  -  -
    #         -  2  2  2  -  -  -  2  2  2
    #         -  -  2  -  -  -  -  -  -  -
    #         -  -  -  2  -  -  -  -  -  -
elif rank == 3:
    num_subarrays = 4
    starts[0][0] = 0; starts[0][1] = 0; counts[0][0] = 1; counts[0][1] = 3
    starts[1][0] = 1; starts[1][1] = 4; counts[1][0] = 1; counts[1][1] = 1
    starts[2][0] = 2; starts[2][1] = 3; counts[2][0] = 1; counts[2][1] = 3
    starts[3][0] = 3; starts[3][1] = 7; counts[3][0] = 1; counts[3][1] = 3
    # rank 3 is writing the following locations: ("-" means skip)
    #         3  3  3  -  -  -  -  -  -  -
    #         -  -  -  -  3  -  -  -  -  -
    #         -  -  -  3  3  3  -  -  -  -
    #         -  -  -  -  -  -  -  3  3  3
else:
    num_subarrays = 0

# reference data for size >=4 (rank 0 - 3 all participated)
dataref = np.array([[3, 3, 3, 1, 1, 0, 0, 2, 1, 1],
                    [0, 2, 2, 2, 3, 1, 1, 2, 2, 2],
                    [1, 1, 2, 3, 3, 3, 0, 0, 1, 1],
                    [0, 0, 0, 2, 1, 1, 1, 3, 3, 3]], np.float32)


# total number of put requests for the test programs
num_reqs = 10 if rank < 4 else 0
num_vars = 20

# allocate write buffer
buf_len = 0
for i in range(num_subarrays):
    w_req_len = np.prod(counts[i,:])
    buf_len += w_req_len
data = np.empty(buf_len, dtype=np.float32)
data.fill(rank)

class VariablesTestCase(unittest.TestCase):

    def setUp(self):
        if (len(sys.argv) == 2) and os.path.isdir(sys.argv[1]):
            self.file_path = os.path.join(sys.argv[1], file_name)
        else:
            self.file_path = file_name
        self._file_format = file_formats.pop(0)

        f = pnetcdf.File(filename=self.file_path, mode = 'w',
                         format=self._file_format, comm=comm, info=None)

        dx = f.def_dim('x',xdim)
        dy = f.def_dim('y',ydim)

        # define 20 netCDF variables
        for i in range(num_vars):
            v = f.def_var(f'data{i}', pnetcdf.NC_FLOAT, (dx, dy))

        # leaving define mode
        f.enddef()

        # initialize variable values
        for i in range(num_vars):
            v = f.variables[f'data{i}']
            v[:] = np.full((xdim, ydim), -1, dtype=np.float32)

        # each process post 10 requests to write an array of values
        req_ids = []
        for i in range(num_reqs):
            v = f.variables[f'data{i}']
            # post the request to write an array of values
            req_id = v.iput_varn(data, num_subarrays, starts, counts)
            # track the reqeust ID for each write reqeust
            req_ids.append(req_id)

        # all processes commit those 10 requests to the file at once using
        # wait_all (collective i/o)
        req_errs = [None] * num_reqs
        f.wait_all(num_reqs, req_ids, req_errs)

        # check request error msg for each unsuccessful requests
        for i in range(num_reqs):
            if strerrno(req_errs[i]) != "NC_NOERR":
                print(f"Error on request {i}:",  strerror(req_errs[i]))

        # post 10 requests to write an array of values for the last 10
        # variables w/o tracking req ids
        for i in range(num_reqs):
            v = f.variables[f'data{num_reqs + i}']
            # post the request to write an array of values
            v.iput_varn(data, num_subarrays, starts, counts)

        # all processes commit all pending requests to the file at once using
        # wait_all (collective I/O)
        f.wait_all(num = pnetcdf.NC_PUT_REQ_ALL)
        f.close()

        if rank == 0:
            if os.environ.get('PNETCDF_DIR') is not None:
                assert validate_nc_file(os.environ.get('PNETCDF_DIR'), self.file_path) == 0

    def runTest(self):
        if nprocs < 4:
            return

        if rank == 0:
            # check contents of the output file
            f = pnetcdf.File(self.file_path, 'r', comm=MPI.COMM_SELF)
            for i in range(num_vars):
                v = f.variables[f'data{i}']
                assert_array_equal(v[:], dataref)
            f.close

if __name__ == '__main__':
    suite = unittest.TestSuite()
    for i in range(len(file_formats)):
        suite.addTest(VariablesTestCase())
    runner = unittest.TextTestRunner()
    output = io.StringIO()
    runner = unittest.TextTestRunner(stream=output)
    result = runner.run(suite)
    if not result.wasSuccessful():
        print(output.getvalue())
        sys.exit(1)

