#
# Copyright (C) 2024, Northwestern University and Argonne National Laboratory
# See COPYRIGHT notice in top-level directory.
#

"""
   This example program is intended to illustrate the use of the pnetCDF python API.
   The program runs in non-blocking mode and makes a request to read a single element
   from a netCDF variable of an opened netCDF file using iget_var method of `Variable` class. The
   library will internally invoke ncmpi_iget_var1 in C.
"""
import pnetcdf
from numpy.random import seed, randint
from numpy.testing import assert_array_equal, assert_equal, assert_array_almost_equal
import tempfile, unittest, os, random, sys
import numpy as np
from mpi4py import MPI
from pnetcdf import strerror, strerrno
from utils import validate_nc_file
import io

seed(0)
file_formats = ['NC_64BIT_DATA', 'NC_64BIT_OFFSET', None]
file_name = "tst_var_iget_var1.nc"

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
xdim= size + 9; ydim= size + 10; zdim= size + 11
data = randint(0,10, size=(xdim,ydim,zdim)).astype('i4')
datarev = data[:,::-1,:].copy()
# print(datarev)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
num_reqs = 10

# initialize a list to store references of variable values
v_datas = []

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

        # define 20 netCDF variables
        for i in range(num_reqs * 2):
            v = f.def_var(f'data{i}', pnetcdf.NC_INT, ('xu','y','z'))
        # initialize variable values
        f.enddef()
        for i in range(num_reqs * 2):
            v = f.variables[f'data{i}']
            v[:,::-1,:]= data
        f.close()
        assert validate_nc_file(os.environ.get('PNETCDF_DIR'), self.file_path) == 0 if os.environ.get('PNETCDF_DIR') is not None else True



        f = pnetcdf.File(self.file_path, 'r')
        # each process post 10 requests to read a single element
        req_ids = []
        v_datas.clear()
        start = (rank, rank, rank)
        for i in range(num_reqs):
            v = f.variables[f'data{i}']
            buff = np.empty(shape = (1,), dtype = v.datatype)
            # post the request to read one part of the variable
            req_id = v.iget_var(buff, start)
            # track the reqeust ID for each read reqeust
            req_ids.append(req_id)
            # store the reference of variable values
            v_datas.append(buff)
        f.end_indep()
        # commit those 10 requests to the file at once using wait_all (collective i/o)
        req_errs_1 = [None] * (num_reqs // 2)
        req_errs_2 = [None] * (num_reqs - len(req_errs_1))
        f.wait_all(5, req_ids[:5], req_errs_1)
        f.wait_all(5, req_ids[5:], req_errs_2)
        req_errs = req_errs_1 + req_errs_2
        # check request error msg for each unsuccessful requests
        for i in range(num_reqs):
            if strerrno(req_errs[i]) != "NC_NOERR":
                print(f"Error on request {i}:",  strerror(req_errs[i]))

         # post 10 requests to read a single element for the last 10 variables w/o tracking req ids
        for i in range(num_reqs, num_reqs * 2):
            v = f.variables[f'data{i}']
            buff = np.empty(shape = (1,), dtype = v.datatype)
            # post the request to read a single element of values
            v.iget_var(buff, start)
            # store the reference of variable values
            v_datas.append(buff)

        # commit all pending get requests to the file at once using wait_all (collective i/o)
        req_errs = f.wait_all(num = pnetcdf.NC_GET_REQ_ALL)
        f.close()
        assert validate_nc_file(os.environ.get('PNETCDF_DIR'), self.file_path) == 0 if os.environ.get('PNETCDF_DIR') is not None else True


    def tearDown(self):
        # remove the temporary files
        comm.Barrier()
        if (rank == 0) and not((len(sys.argv) == 2) and os.path.isdir(sys.argv[1])):
            os.remove(self.file_path)

    def runTest(self):
        """testing variable iget_var1 method for CDF-5/CDF-2/CDF-1 file format"""
        # test iget_var1 and collective i/o wait_all
        for i in range(num_reqs * 2):
            assert_array_equal(v_datas[i], np.array(datarev[rank][rank][rank]))

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
