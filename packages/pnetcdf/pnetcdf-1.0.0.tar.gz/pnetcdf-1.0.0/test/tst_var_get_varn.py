#
# Copyright (C) 2024, Northwestern University and Argonne National Laboratory
# See COPYRIGHT notice in top-level directory.
#

import pnetcdf
from numpy.testing import assert_array_equal
import unittest, os, sys
import numpy as np
from mpi4py import MPI
from utils import validate_nc_file
import io
import argparse

file_formats = ['NC_64BIT_DATA', 'NC_64BIT_OFFSET', None]
file_name = "tst_var_get_varn.nc"

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
xdim = 4
ydim = 10

MAX_NUM_REQS = 6
NDIMS = 2
# data to store in NetCDF variable
data = np.array([[3, 3, 3, 1, 1, 0, 0, 2, 1, 1],
                 [0, 2, 2, 2, 3, 1, 1, 2, 2, 2],
                 [1, 1, 2, 3, 3, 3, 0, 0, 1, 1],
                 [0, 0, 0, 2, 1, 1, 1, 3, 3, 3]], np.float32)

starts = np.zeros((MAX_NUM_REQS, NDIMS), dtype=np.int64)
counts = np.zeros((MAX_NUM_REQS, NDIMS), dtype=np.int64)

#initialize variable values
if rank == 0:
    num_reqs = 4
    starts[0][0] = 0; starts[0][1] = 5; counts[0][0] = 1; counts[0][1] = 2
    starts[1][0] = 1; starts[1][1] = 0; counts[1][0] = 1; counts[1][1] = 1
    starts[2][0] = 2; starts[2][1] = 6; counts[2][0] = 1; counts[2][1] = 2
    starts[3][0] = 3; starts[3][1] = 0; counts[3][0] = 1; counts[3][1] = 3
    # rank 0 is reading the following locations: ("-" means skip)
    #               -  -  -  -  -  0  0  -  -  -
    #               0  -  -  -  -  -  -  -  -  -
    #               -  -  -  -  -  -  0  0  -  -
    #               0  0  0  -  -  -  -  -  -  -
elif rank == 1:
    num_reqs = 6
    starts[0][0] = 0; starts[0][1] = 3; counts[0][0] = 1; counts[0][1] = 2
    starts[1][0] = 0; starts[1][1] = 8; counts[1][0] = 1; counts[1][1] = 2
    starts[2][0] = 1; starts[2][1] = 5; counts[2][0] = 1; counts[2][1] = 2
    starts[3][0] = 2; starts[3][1] = 0; counts[3][0] = 1; counts[3][1] = 2
    starts[4][0] = 2; starts[4][1] = 8; counts[4][0] = 1; counts[4][1] = 2
    starts[5][0] = 3; starts[5][1] = 4; counts[5][0] = 1; counts[5][1] = 3
    # rank 1 is reading the following locations: ("-" means skip)
    #               -  -  -  1  1  -  -  -  1  1
    #               -  -  -  -  -  1  1  -  -  -
    #               1  1  -  -  -  -  -  -  1  1
    #               -  -  -  -  1  1  1  -  -  -
elif rank == 2:
    num_reqs = 5
    starts[0][0] = 0; starts[0][1] = 7; counts[0][0] = 1; counts[0][1] = 1
    starts[1][0] = 1; starts[1][1] = 1; counts[1][0] = 1; counts[1][1] = 3
    starts[2][0] = 1; starts[2][1] = 7; counts[2][0] = 1; counts[2][1] = 3
    starts[3][0] = 2; starts[3][1] = 2; counts[3][0] = 1; counts[3][1] = 1
    starts[4][0] = 3; starts[4][1] = 3; counts[4][0] = 1; counts[4][1] = 1
    # rank 2 is reading the following locations: ("-" means skip)
    #         -  -  -  -  -  -  -  2  -  -
    #         -  2  2  2  -  -  -  2  2  2
    #         -  -  2  -  -  -  -  -  -  -
    #         -  -  -  2  -  -  -  -  -  -
elif rank == 3:
    num_reqs = 4
    starts[0][0] = 0; starts[0][1] = 0; counts[0][0] = 1; counts[0][1] = 3
    starts[1][0] = 1; starts[1][1] = 4; counts[1][0] = 1; counts[1][1] = 1
    starts[2][0] = 2; starts[2][1] = 3; counts[2][0] = 1; counts[2][1] = 3
    starts[3][0] = 3; starts[3][1] = 7; counts[3][0] = 1; counts[3][1] = 3
    # rank 3 is reading the following locations: ("-" means skip)
    #         3  3  3  -  -  -  -  -  -  -
    #         -  -  -  -  3  -  -  -  -  -
    #         -  -  -  3  3  3  -  -  -  -
    #         -  -  -  -  -  -  -  3  3  3
else:
    num_reqs = 0

# Obtain the size of returned array, needed for generating reference array
buf_len = np.sum(np.prod(counts, axis=1))

class VariablesTestCase(unittest.TestCase):

    def setUp(self):
        if (len(sys.argv) == 2) and os.path.isdir(sys.argv[1]):
            self.file_path = os.path.join(sys.argv[1], file_name)
        else:
            self.file_path = file_name
        self._file_format = file_formats.pop(0)
        f = pnetcdf.File(filename=self.file_path, mode = 'w',
                         format=self._file_format, comm=comm, info=None)

        # define dimensions and variables
        f.def_dim('x',xdim)
        f.def_dim('y',ydim)

        var1 = f.def_var('var1', pnetcdf.NC_FLOAT, ('x', 'y'))

        f.enddef()
        var1[:] = data

        comm.Barrier()
        if os.environ.get('PNETCDF_DIR') is not None:
            assert validate_nc_file(os.environ.get('PNETCDF_DIR'), self.file_path) == 0

    def tearDown(self):
        # Remove the temporary files
        comm.Barrier()
        if (rank == 0) and not((len(sys.argv) == 2) and os.path.isdir(sys.argv[1])):
            os.remove(self.file_path)

    def runTest(self):
        """testing variable get varn for CDF-5/CDF-2/CDF-1 file"""
        dataref = np.full((buf_len,), rank, np.float32)
        f = pnetcdf.File(self.file_path, 'r')

        # test collective i/o get_varn
        v1 = f.variables['var1']
        buff = np.empty((buf_len,), v1.dtype)
        v1.get_varn_all(buff, num_reqs, starts, counts)
        assert_array_equal(buff, dataref)

        # test independent i/o get_varn
        f.begin_indep()
        buff = np.empty((buf_len,), v1.dtype)
        v1.get_varn(buff, num_reqs, starts, counts)
        assert_array_equal(buff, dataref)

        f.close()

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

