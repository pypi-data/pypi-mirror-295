#
# Copyright (C) 2024, Northwestern University and Argonne National Laboratory
# See COPYRIGHT notice in top-level directory.
#

"""
   This example program is intended to illustrate the use of the pnetCDF python API. The
   program sets the default fill mode for a netCDF file open for writing using `File` class
   method set_fill(). This call will change the fill mode for all non-record variables
   defined so far and change the default fill mode for new non-record variables defined following
   this call. The library will internally invoke ncmpi_set_fill in C.
"""
import pnetcdf
from numpy.random import seed, randint
from numpy.testing import assert_array_equal, assert_equal, assert_array_almost_equal
import tempfile, unittest, os, random, sys
import numpy as np
from mpi4py import MPI
from utils import validate_nc_file
import io

seed(0)
file_formats = ['NC_64BIT_DATA', 'NC_64BIT_OFFSET', None]
file_name = "tst_file_fill.nc"


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

xdim = ydim = size + 10


class FileTestCase(unittest.TestCase):

    def setUp(self):
        if (len(sys.argv) == 2) and os.path.isdir(sys.argv[1]):
            self.file_path = os.path.join(sys.argv[1], file_name)
        else:
            self.file_path = file_name
        # select next file format for testing
        self._file_format = file_formats.pop(0)
        f = pnetcdf.File(filename=self.file_path, mode = 'w', format=self._file_format, comm=comm, info=None)
        # define variables and dimensions for testing
        f.def_dim('x',xdim)
        f.def_dim('y',ydim)
        # define a netCDF variable before setting file filling mode
        v1 = f.def_var('data1', pnetcdf.NC_INT, ('x','y'))
        # enable fill mode at file-level which applies to all netCDF variables of the file
        old_fillmode = f.set_fill(pnetcdf.NC_FILL)
        # check old_fillmode
        assert(old_fillmode == pnetcdf.NC_NOFILL)
        # define a netCDF variable after setting file filling mode
        v2 = f.def_var('data2', pnetcdf.NC_INT, ('x','y'))
        # enter data mode and write partially values to the variable
        f.enddef()
        v1 = f.variables['data1']
        v2 = f.variables['data2']
        v1.put_var_all(np.int32(rank), start = (rank, rank))
        v2.put_var_all(np.int32(rank), start = (rank, rank))
        f.close()
        assert validate_nc_file(os.environ.get('PNETCDF_DIR'), self.file_path) == 0 if os.environ.get('PNETCDF_DIR') is not None else True


    def tearDown(self):
        # remove the temporary files
        comm.Barrier()
        if (rank == 0) and not((len(sys.argv) == 2) and os.path.isdir(sys.argv[1])):
            os.remove(self.file_path)
            pass

    def runTest(self):
        """testing file set fill mode for CDF-5/CDF-2/CDF-1 file format"""
        f = pnetcdf.File(self.file_path, 'r')
        for i in [1,2]:
            v = f.variables[f'data{i}']
            # check the fill mode settings of each variable
            no_fill, fill_value = v.inq_fill()
            # check if no_fill flag is set to 0
            self.assertTrue(no_fill == 0)
            # check if fill_value equals default fill value
            self.assertTrue(fill_value == pnetcdf.NC_FILL_INT)
        f.close()

if __name__ == '__main__':
    suite = unittest.TestSuite()
    for i in range(len(file_formats)):
        suite.addTest(FileTestCase())
    runner = unittest.TextTestRunner()
    output = io.StringIO()
    runner = unittest.TextTestRunner(stream=output)
    result = runner.run(suite)
    if not result.wasSuccessful():
        print(output.getvalue())
        sys.exit(1)
