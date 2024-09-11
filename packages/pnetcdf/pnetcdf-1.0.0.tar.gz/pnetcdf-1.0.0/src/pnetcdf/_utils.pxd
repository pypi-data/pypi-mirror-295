###############################################################################
#
#  Copyright (C) 2024, Northwestern University and Argonne National Laboratory
#  See COPYRIGHT notice in top-level directory.
#
###############################################################################

include "PnetCDF.pxi"
cdef _check_err(ierr, err_cls=*, filename=*)
cdef _strencode(pystr, encoding=*)
cdef _set_att(file, int varid, name, value, nc_type xtype=*)
cdef _get_att(file, int varid, name, encoding=*)
cdef _get_att_names(int file_id, int varid)
cdef _nptonctype, _notcdf2dtypes, _nctonptype, _nptompitype, _supportedtypes, _supportedtypescdf2, default_fillvals, _private_atts
cdef _tostr(s)
cdef _safecast(a,b)
cdef _StartCountStride(elem, shape, dimensions=*, file=*, datashape=*, put=*)
cdef _out_array_shape(count)
cdef _get_format(int ncid)
cpdef chartostring(b,encoding=*)
cpdef stringtochar(a,encoding=*)
cpdef strerror(err_code)
cpdef strerrno(err_code)
cpdef set_default_format(int new_format)
cpdef inq_default_format()
cpdef inq_file_format(str file_name)
cpdef inq_malloc_max_size()
cpdef inq_malloc_size()
cpdef inq_clibvers()
