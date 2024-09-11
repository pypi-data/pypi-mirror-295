#
# Copyright (C) 2024, Northwestern University and Argonne National Laboratory
# See COPYRIGHT notice in top-level directory.
#

"""
   This example program is intended to illustrate the use of the pnetCDF python API.
   The program write an array of values into a netCDF variable of an opened netCDF file using
   put_var method of `Variable` class. The library will internally invoke ncmpi_iput_vara in C.
"""
import pnetcdf
from numpy.random import seed, randint
from numpy.testing import assert_array_equal, assert_equal, assert_array_almost_equal
import tempfile, unittest, os, random, sys
import numpy as np
from mpi4py import MPI
from utils import validate_nc_file
import io
import argparse


seed(0)
file_formats = ['NC_64BIT_DATA', 'NC_64BIT_OFFSET', None]
file_name = "tst_var_put_vara.nc"


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
xdim=9; ydim=10; zdim=size*10
# initial values for netCDF variable
data = np.zeros((xdim,ydim,zdim)).astype('i4')
# new array that will be written using iput_var (overwriting some parts of initial values)
datam = randint(0,10, size=(1,5,10)).astype('i4')
# reference array for comparison in the testing phase
datares1, datares2 = data.copy(), data.copy()
for i in range(size):
    datares1[3:4,:5,i*10:(i+1)*10] = datam
for i in range(min(2,size)):
    datares2[3:4,:5,i*10:(i+1)*10] = datam


class VariablesTestCase(unittest.TestCase):

    def setUp(self):
        if (len(sys.argv) == 2) and os.path.isdir(sys.argv[1]):
            self.file_path = os.path.join(sys.argv[1], file_name)
        else:
            self.file_path = file_name
        self._file_format = file_formats.pop(0)
        f = pnetcdf.File(filename=self.file_path, mode = 'w', format=self._file_format, comm=comm, info=None)
        f.def_dim('x',xdim)
        f.def_dim('xu',-1)
        f.def_dim('y',ydim)
        f.def_dim('z',zdim)

        v1_u = f.def_var('data1u', pnetcdf.NC_INT, ('xu','y','z'))
        v2_u = f.def_var('data2u', pnetcdf.NC_INT, ('xu','y','z'))

        #initialize variable values
        f.enddef()
        v1_u[:] = data
        v2_u[:] = data
        f.close()


        f = pnetcdf.File(filename=self.file_path, mode = 'r+', format=self._file_format, comm=comm, info=None)
        # define variables and dimensions for testing
        v1_u = f.variables['data1u']
        # equivalent code to the following using indexer syntax: v1_u[3:4,:5,10*rank:10*(rank+1)] = datam
        starts = np.array([3, 0, 10 * rank])
        counts = np.array([1, 5, 10])
        # test collective i/o put_var_all
        # all processes write an array of values to variable with put_var_all (collective i/o)
        # each process write to their assigned coordinates within the variable
        v1_u.put_var_all(datam, start = starts, count = counts)

        # write subarray to variable with put_var (independent i/o)
        v2_u = f.variables['data2u']
        # test independent i/o put_var
        f.begin_indep()
        if rank < 2:
            # mpi process rank 0 and 1 write an array of values to their assigned coordinates
            v2_u.put_var(datam, start = starts, count = counts)

        f.end_indep()
        f.close()
        comm.Barrier()
        assert validate_nc_file(os.environ.get('PNETCDF_DIR'), self.file_path) == 0 if os.environ.get('PNETCDF_DIR') is not None else True


    def tearDown(self):
        # remove the temporary files
        comm.Barrier()
        if (rank == 0) and not((len(sys.argv) == 2) and os.path.isdir(sys.argv[1])):
            os.remove(self.file_path)

    def runTest(self):
        """testing variable put vara all for CDF-5/CDF-2/CDF-1 file format"""
        f = pnetcdf.File(self.file_path, 'r')
        # test collective i/o put_var
        v1 = f.variables['data1u']
        # compare returned array against reference array
        assert_array_equal(v1[:], datares1)
        # test independent i/o put_var
        v2 = f.variables['data2u']
        # compare returned array against reference array
        assert_array_equal(v2[:], datares2)
        f.close()


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for i in range(len(file_formats)):
        suite.addTest(VariablesTestCase())
    output = io.StringIO()
    runner = unittest.TextTestRunner(stream=output)
    result = runner.run(suite)
    if not result.wasSuccessful():
        print(output.getvalue())
        sys.exit(1)
