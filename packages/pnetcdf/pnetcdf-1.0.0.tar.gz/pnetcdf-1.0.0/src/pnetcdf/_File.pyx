###############################################################################
#
#  Copyright (C) 2024, Northwestern University and Argonne National Laboratory
#  See COPYRIGHT notice in top-level directory.
#
###############################################################################

import sys
import os
import subprocess
import warnings
include "PnetCDF.pxi"

cimport mpi4py.MPI as MPI
from mpi4py.libmpi cimport MPI_Comm, MPI_Info, MPI_Comm_dup, MPI_Info_dup, \
                               MPI_Comm_free, MPI_Info_free, MPI_INFO_NULL,\
                               MPI_COMM_WORLD, MPI_Offset



from libc.string cimport memcpy, memset
from libc.stdlib cimport malloc, free

from ._Dimension cimport Dimension
from ._Variable cimport Variable
from ._utils cimport _strencode, _check_err, _set_att, _get_att, _get_att_names, _get_format, _private_atts
from._utils cimport _nctonptype
import numpy as np



cdef class File:
    def __init__(self, filename, mode="w", format=None, MPI.Comm comm=None, MPI.Info info=None):
        """
        __init__(self, filename, format=None, mode="w", MPI.Comm comm=None, MPI.Info info=None)

        The constructor for :class:`pnetcdf.File`.

        :param str filename: Name of the new file.

        :param str mode: Access mode.

            - ``r``: Open a file for read-only mode. An error will return if
              the file does not exist.
            - ``w``: Create a new file. If a file with the same name has
              already  existed, the file will be clobbered to zero size.
            - ``x``: Create a new file, but return an error if the file has
              already existed.
            - ``a`` or ``r+``: append mode. It creates the file if it does not
              exist.

        :param str format: [Optional] underlying file format. Only relevant
            when creating a new file.

            - ``NETCDF3_64BIT_OFFSET`` or ``NC_64BIT_OFFSET``: CDF-2 format
            - ``NETCDF3_64BIT_DATA`` or ``NC_64BIT_DATA``: CDF-5 format
            - ``NETCDF3_CLASSIC`` or `None` defaults to default file format
              (CDF-1 format)

        :param comm: [Optional]
            MPI communicator to use for file access. `None` defaults to
            ``MPI_COMM_WORLD``.
        :type comm: mpi4py.MPI.Comm or None

        :param info: [Optional]
            MPI info object to use for file access. `None` defaults to
            ``MPI_INFO_NULL``.
        :type info: mpi4py.MPI.Info or None

        :return: The created file instance.
        :rtype: :class:`pnetcdf.File`
        """
        cdef int ncid
        encoding = sys.getfilesystemencoding()
        cdef char* path
        cdef MPI_Comm mpicomm = MPI_COMM_WORLD
        cdef MPI_Info mpiinfo = MPI_INFO_NULL
        cdef int cmode

        if comm is not None:
            mpicomm = comm.ob_mpi
        if info is not None:
            mpiinfo = info.ob_mpi
        bytestr = _strencode(filename, encoding=encoding)
        path = bytestr
        if format:
            supported_formats = ["NETCDF3_64BIT_OFFSET", "NETCDF3_64BIT_DATA", "NETCDF3_CLASSIC", "NC_64BIT_OFFSET", "NC_64BIT_DATA"]
            if format not in supported_formats:
                msg="underlying file format must be one of `'NETCDF3_CLASSIC'`, `'NETCDF3_64BIT_OFFSET'` (same as `'NC_64BIT_OFFSET'`) or `'NETCDF3_64BIT_DATA'` (same as `'NC_64BIT_DATA'`)"
                raise ValueError(msg)

        clobber = True
        # mode='x' is the same as mode='w' with clobber=False
        if mode == 'x':
            mode = 'w'
            clobber = False

        if mode == 'w' or (mode in ['a','r+'] and not os.path.exists(filename)):
            cmode = 0
            if not clobber:
                cmode = NC_NOCLOBBER
            if format in ['NETCDF3_64BIT_OFFSET', 'NETCDF3_64BIT_DATA', 'NC_64BIT_OFFSET', 'NC_64BIT_DATA']:
                file_cmode = NC_64BIT_OFFSET_C if format in ['NETCDF3_64BIT_OFFSET', 'NC_64BIT_OFFSET'] else NC_64BIT_DATA_C
                cmode = cmode | file_cmode
            with nogil:
                ierr = ncmpi_create(mpicomm, path, cmode, mpiinfo, &ncid)

        elif mode == "r":
            with nogil:
                ierr = ncmpi_open(mpicomm, path, NC_NOWRITE, mpiinfo, &ncid)

        elif mode in ['a','r+'] and os.path.exists(filename):
            with nogil:
                ierr = ncmpi_open(mpicomm, path, NC_WRITE, mpiinfo, &ncid)
        else:
            raise ValueError("mode must be 'w', 'x', 'r', 'a' or 'r+', got '%s'" % mode)


        _check_err(ierr, err_cls=OSError, filename=path)
        self._isopen = 1
        self.indep_mode = 0
        self._ncid = ncid
        self.file_format = _get_format(ncid)
        self.dimensions = _get_dims(self)
        self.variables = _get_variables(self)

    def close(self):
        """
        close(self)

        Close the opened netCDF file
        """
        self._close(True)

    def _close(self, check_err):
        cdef int ierr
        with nogil:
            ierr = ncmpi_close(self._ncid)
        if check_err:
            _check_err(ierr)
        self._isopen = 0 # indicates file already closed, checked by __dealloc__

    def filepath(self, encoding=None):
        """
        filepath(self, encoding=None)

        Method to return the file system path which was used to open/create the
        Dataset.  The path is decoded into a string using
        `sys.getfilesystemencoding()` by default.

        :param str encoding: [Optional]
            character encoding of a string attribute (default is `utf-8`).

        :return: The file path
        :rtype: str
        """
        cdef int ierr
        cdef int pathlen
        cdef char *c_path
        if encoding is None:
            encoding = sys.getfilesystemencoding()
        with nogil:
            ierr = ncmpi_inq_path(self._ncid, &pathlen, NULL)
        _check_err(ierr)

        c_path = <char *>malloc(sizeof(char) * (pathlen + 1))
        if not c_path:
            raise MemoryError()
        try:
            with nogil:
                ierr = ncmpi_inq_path(self._ncid, &pathlen, c_path)
            _check_err(ierr)

            py_path = c_path[:pathlen] # makes a copy of pathlen bytes from c_string
        finally:
            free(c_path)
        return py_path.decode(encoding)


    def __dealloc__(self):
        # close file when there are no references to object left
        if self._isopen:
           self._close(False)

    def __enter__(self):
        return self
    def __exit__(self,atype,value,traceback):
        self.close()

    def sync(self):
        """
        sync(self)

        Writes all buffered data in the `File` to the disk file."""
        cdef int ierr
        with nogil:
            ierr = ncmpi_sync(self._ncid)
        _check_err(ierr)

    def redef(self):
        """
        redef(self)

        Enter define mode, so that dimensions, variables, and attributes can be
        added or renamed and attributes can be deleted

        .. note:: In PnetCDF implementation, a file mode can be in either
            define or data mode. While in the define mode, metadata can be
            created and modified, for instance, creating new dimension,
            variables, and attributes. Variables that have been defined can
            only be read and written while in the data mode. This requirement
            is to guarantee the data consistency when running application
            programs in parallel.
        """
        self._redef()

    def _redef(self):
        cdef int ierr
        cdef int fileid= self._ncid
        with nogil:
            ierr = ncmpi_redef(fileid)
        _check_err(ierr)

    def enddef(self):
        """
        enddef(self)

        Method to exit the current file's mode from define mode and place the
        file in data mode, so variable data can be read or written.

        .. note:: In PnetCDF implementation, a file mode can be in either
            define or data mode. While in the define mode, metadata can be
            created and modified, for instance, creating new dimension,
            variables, and attributes. Variables that have been defined can
            only be read and written while in the data mode. This requirement
            is to guarantee the data consistency when running application
            programs in parallel.
        """
        self._enddef()

    def _enddef(self):
        cdef int ierr
        cdef int fileid = self._ncid
        with nogil:
            ierr = ncmpi_enddef(fileid)
        _check_err(ierr)

    def begin_indep(self):
        """
        begin_indep(self)

        Method to leave the file's current mode from collective data mode and
        enter into independent data mode. The default mode is collective data
        mode.
        """
        cdef int ierr
        cdef int fileid = self._ncid
        with nogil:
            ierr = ncmpi_begin_indep_data(fileid)
        _check_err(ierr)
        self.indep_mode = 1

    def end_indep(self):
        """
        end_indep(self)

        Method to leave the file's current mode from independent data mode and
        enter into collective data mode. The default mode is collective data
        mode.
        """
        cdef int ierr
        cdef int fileid = self._ncid
        with nogil:
            ierr = ncmpi_end_indep_data(fileid)
        _check_err(ierr)
        self.indep_mode = 0

    def flush(self):
        """
        flush(self)

        Flush data cached in memory to the file system.
        """
        cdef int ierr
        cdef int fileid = self._ncid
        with nogil:
            ierr = ncmpi_flush(fileid)
        _check_err(ierr)


    def def_dim(self, dimname, size=-1):
        """
        def_dim(self, dimname, size=-1)

        Creates a new dimension with the given `dimname` and `size`.  `size`
        must be a positive integer or `-1`, which stands for "unlimited"
        (default is `-1`). The return value is the `Dimension` class instance
        describing the new dimension.  To determine the current maximum size of
        the dimension, use the `len` function on the `Dimension` instance. To
        determine if a dimension is 'unlimited', use the
        :meth:`Dimension.isunlimited` method of the `Dimension` instance.

        :param str dimname: Name of the new dimension.

        :param int size: [Optional] Size of the new dimension.
        """
        self.dimensions[dimname] = Dimension(self, dimname, size=size)
        return self.dimensions[dimname]

    def createDimension(self, dimname, size=-1):
        """
        createDimension(self, dimname, size=-1)

        Same as :meth:`File.def_dim`
        """
        return self.def_dim(dimname, size)

    def rename_var(self, oldname, newname):
        """
        rename_var(self, oldname, newname)

        Rename a `Variable` named `oldname` to `newname`

        :param str oldname: Old name of the variable.

        :param str newname: New name of the variable.

        :Operational mode: this method is collective subroutine, argument
            new name must be consistent among all calling processes. If the new
            name is longer than the old name, then the netCDF file must be in
            define mode. Otherwise, the netCDF file can be in either define or
            data mode.
        """

        cdef char *namstring
        cdef Variable var
        cdef int _file_id, _varid
        try:
            var = self.variables[oldname]
        except KeyError:
            raise KeyError('%s not a valid variable name' % oldname)
        bytestr = _strencode(newname)
        namstring = bytestr
        _file_id = self._ncid
        _var_id = var._varid
        with nogil:
            ierr = ncmpi_rename_var(_file_id, _var_id, namstring)
        _check_err(ierr)
        # remove old key from dimensions dict.
        self.variables.pop(oldname)
        # add new key.
        self.variables[newname] = var

    def renameVariable(self, oldname, newname):
        """
        renameVariable(self, oldname, newname)

        Same as :meth:`File.rename_var`
        """
        self.rename_var(oldname, newname)

    def rename_dim(self, oldname, newname):
        """
        rename_dim(self, oldname, newname)

        Rename a ``Dimension`` named `oldname` to `newname`

        :param str oldname: Old name of the dimension.

        :param str newname: New name of the dimension.

        :Operational mode: this method is collective subroutine, argument new
            name must be consistent among all calling processes. If the new
            name is longer than the old name, then the netCDF file must be in
            define mode. Otherwise, the netCDF file can be in either define or
            data mode.
        """
        cdef char *namstring
        cdef Variable var
        cdef int _file_id, _dim_id
        try:
            dim = self.dimensions[oldname]
        except KeyError:
            raise KeyError('%s not a valid dimension name' % oldname)
        bytestr = _strencode(newname)
        namstring = bytestr
        _file_id = self._ncid
        _dim_id = dim._dimid
        with nogil:
            ierr = ncmpi_rename_dim(_file_id, _dim_id, namstring)
        _check_err(ierr)
        # remove old key from dimensions dict.
        self.dimensions.pop(oldname)
        # add new key.
        self.dimensions[newname] = dim

    def renameDimension(self, oldname, newname):
        """
        renameDimension(self, oldname, newname)

        Same as :meth:`File.rename_dim`
        """
        self.rename_dim(oldname, newname)

    def def_var(self, varname, datatype, dimensions=(), fill_value=None):
        """
        def_var(self, varname, datatype, dimensions=(), fill_value=None)

        Create a new variable with the given parameters.

        :param str varname: Name of the new variable.

        :param datatype: The data type of the new variable.
            It can be a string that describes a numpy dtype object, a numpy
            dtype object, or one of PnetCDF data type constant, as shown below.

              - ``pnetcdf.NC_CHAR`` for text data
              - ``pnetcdf.NC_BYTE`` for 1-byte signed integer
              - ``pnetcdf.NC_SHORT`` for 2-byte signed integer
              - ``pnetcdf.NC_INT`` for 4-byte signed integer
              - ``pnetcdf.NC_FLOAT`` for 4-byte floating point number
              - ``pnetcdf.NC_DOUBLE`` for 8-byte real number in double precision

            The following are additional data types supported by `CDF-5` format.

              - ``pnetcdf.NC_UBYTE`` for unsigned 1-byte integer
              - ``pnetcdf.NC_USHORT`` for unsigned 2-byte integer
              - ``pnetcdf.NC_UINT`` for unsigned 4-byte intege
              - ``pnetcdf.NC_INT64`` for signed 8-byte integer
              - ``pnetcdf.NC_UINT64`` for unsigned 8-byte integer

        :param dimensions: [Optional]
            The dimensions of the new variable. Can be either dimension names
            or dimension class instances. Default is an empty tuple which means
            the variable is a scalar (and therefore has no dimensions).
        :type dimensions: tuple of str or :class:`pnetcdf.Dimension` instances

        :param fill_value: [Optional] The fill value of the new variable.
            Accepted values are shown below.

            - ``None`` to use the default netCDF fill value for the given data type.
            - ``False`` to turn off the fill mode.
            - If specified with other value, the default netCDF `_FillValue`
              (the value that the variable gets filled with before any data is
              written to it) is replaced with this value.

        :return: The created variable
        :rtype: :class:`pnetcdf.Variable`
        """

        # the following should be added to explanation of variable class.
        # # A list of names corresponding to netCDF variable attributes can be
        # # obtained with the `Variable` method `Variable.ncattrs`. A dictionary
        # # containing all the netCDF attribute name/value pairs is provided by
        # # the `__dict__` attribute of a `Variable` instance.

        # # `Variable` instances behave much like array objects. Data can be
        # # assigned to or retrieved from a variable with indexing and slicing
        # # operations on the `Variable` instance. A `Variable` instance has six
        # # Dataset standard attributes: `dimensions, dtype, shape, ndim, name`.
        # # Application programs should never modify these attributes. The `dimensions`
        # #     attribute is a tuple containing the
        # # names of the dimensions associated with this variable. The `dtype`
        # # attribute is a string describing the variable's data type (`i4, f8,
        # # S1,` etc). The `shape` attribute is a tuple describing the current
        # # sizes of all the variable's dimensions. The `name` attribute is a
        # # string containing the name of the Variable instance. The `ndim` attribute
        # # is the number of variable dimensions.
        # # """

        # if dimensions is a single string or Dimension instance,
        # convert to a tuple.
        # This prevents a common error that occurs when
        # dimensions = 'lat' instead of ('lat',)
        if isinstance(dimensions, (str, bytes, Dimension)):
            dimensions = dimensions,
        # convert elements of dimensions tuple to Dimension
        # instances if they are strings.
        # _find_dim looks for dimension in this file, and if not
        # found there, looks in parent (and it's parent, etc, back to root).
        dimensions =\
        tuple(self.dimensions[d] if isinstance(d,(str,bytes)) else d for d in dimensions)
        # create variable.
        self.variables[varname] = Variable(self, varname, datatype,
                                           dimensions=dimensions,
                                           fill_value=fill_value)
        return self.variables[varname]

    def createVariable(self, varname, datatype, dimensions=(), fill_value=None):
        """
        createVariable(self, varname, datatype, dimensions=(), fill_value=None)

        Same as :meth:`File.def_var`
        """
        return self.def_var(varname, datatype, dimensions, fill_value)


    def ncattrs(self):
        """
        ncattrs(self)

        Return netCDF attribute names for this File in a list.

        :rtype: list
        """
        return _get_att_names(self._ncid, NC_GLOBAL)

    def put_att(self,name,value):
        """
        put_att(self,name,value)

        Set a global attribute for this file using name,value pair. Especially
        useful when you need to set a netCDF attribute with the
        with the same name as one of the reserved python attributes.

        :param name: Name of the new attribute.
        :type name: str

        :param value: Value of the new attribute.
        :type value: str, int, float or list of int and float

        :Operational mode: This method must be called while the file is in
            define mode.
        """
        cdef nc_type xtype
        xtype=-99
        _set_att(self, NC_GLOBAL, name, value, xtype=xtype)


    def get_att(self, name, encoding='utf-8'):
        """
        get_att(self, name, encoding='utf-8')

        Retrieve a netCDF file attribute.  Useful when you need to get a netCDF
        attribute with the same name as one of the reserved python attributes.

        :param name: Name of the attribute.
        :type name: str

        :param encoding: [Optional]
            character encoding of a string attribute (default is `utf-8`).
        :type encoding: str

        :rtype: str or ``numpy.ndarray``

        :Operational mode: This method can be called while the file is in
            either define or data mode (collective or independent).
        """
        return _get_att(self, NC_GLOBAL, name, encoding=encoding)


    def __delattr__(self, name):
        # if it's a netCDF attribute, remove it
        if name not in _private_atts:
            self.del_att(name)
        else:
            raise AttributeError(
            "'%s' is one of the reserved attributes %s, cannot delete. Use del_att instead." % (name, tuple(_private_atts)))

    def del_att(self, name):
        """
        del_att(self, name)

        Delete a netCDF attribute.

        :param name: Name of the attribute
        :type name: str

        :Operational mode: This method must be called while the file is in
            define mode.
        """
        cdef char *attname
        cdef int ierr
        bytestr = _strencode(name)
        attname = bytestr
        with nogil:
            ierr = ncmpi_del_att(self._ncid, NC_GLOBAL, attname)
        _check_err(ierr)

    def __setattr__(self,name,value):
    # if name in _private_atts, it is stored at the python
    # level and not in the netCDF file.
        if name not in _private_atts:
            self.put_att(name, value)
        elif not name.endswith('__'):
            if hasattr(self,name):
                raise AttributeError(
            "'%s' is one of the reserved attributes %s, cannot rebind. Use put_att instead." % (name, tuple(_private_atts)))
            else:
                self.__dict__[name]=value

    def __getattr__(self,name):
        # if name in _private_atts, it is stored at the python
        # level and not in the netCDF file.
        if name.startswith('__') and name.endswith('__'):
            # if __dict__ requested, return a dict with netCDF attributes.
            if name == '__dict__':
                names = self.ncattrs()
                values = []
                for name in names:
                    values.append(_get_att(self, NC_GLOBAL, name))
                return dict(zip(names, values))
            else:
                raise AttributeError
        elif name in _private_atts:
            return self.__dict__[name]
        else:
            return self.get_att(name)

    def rename_att(self, oldname, newname):
        """
        rename_att(self, oldname, newname)

        Rename a `File` attribute named `oldname` to `newname`

        :param oldname: Old name of the attribute.
        :type oldname: str

        :Operational mode: If the new name is longer than the original name,
            the netCDF file must be in define mode.  Otherwise, the netCDF file
            can be in either define or data mode.
        """
        cdef char *oldnamec
        cdef char *newnamec
        cdef int ierr
        cdef int _file_id
        _file_id = self._ncid
        bytestr = _strencode(oldname)
        oldnamec = bytestr
        bytestr = _strencode(newname)
        newnamec = bytestr

        with nogil:
            ierr = ncmpi_rename_att(_file_id, NC_GLOBAL, oldnamec, newnamec)
        _check_err(ierr)

    def renameAttribute(self, oldname, newname):
        """
        renameAttribute(self, oldname, newname)

        Same as :meth:`File.rename_att`
        """
        self.rename_att(oldname, newname)


    def _wait(self, num=None, requests=None, status=None, collective=False):
        cdef int _file_id, ierr
        cdef int num_req
        cdef int *requestp
        cdef int *statusp
        _file_id = self._ncid
        if num is None:
            num = NC_REQ_ALL_C
        if num in [NC_REQ_ALL_C, NC_PUT_REQ_ALL_C, NC_GET_REQ_ALL_C]:
            num_req = num
            if not collective:
                with nogil:
                    ierr = ncmpi_wait(_file_id, num_req, NULL, NULL)
            else:
                with nogil:
                    ierr = ncmpi_wait_all(_file_id, num_req, NULL, NULL)
            _check_err(ierr)
        else:
            requestp = <int *>malloc(sizeof(int) * num)
            statusp = <int *>malloc(sizeof(int) * num)
            num_req = num
            for n from 0 <= n < num:
                requestp[n] = requests[n]
            if not collective:
                with nogil:
                    ierr = ncmpi_wait(_file_id, num_req, requestp, statusp)
            else:
                with nogil:
                    ierr = ncmpi_wait_all(_file_id, num_req, requestp, statusp)
            for n from 0 <= n < num:
                requests[n] = requestp[n]

            if status is not None:
                for n from 0 <= n < num:
                    status[n] = statusp[n]
            _check_err(ierr)
        return None

    def wait(self, num=None, requests=None, status=None):
        """
        wait(self, num=None, requests=None, status=None)

        This method is a blocking call that wait for the completion of
        nonblocking I/O requests made by :meth:`Variable.iput_var`,
        :meth:`Variable.iget_var` and :meth:`Variable.bput_var`

        :param int num: [Optional]
            number of requests. It is also the array size of the next two
            arguments. Alternatively it can be module-level constants:

            - ``pnetcdf.NC_REQ_ALL`` or ``None``: flush all pending nonblocking requests
            - ``pnetcdf.NC_GET_REQ_ALL``: flush all pending nonblocking GET requests
            - ``pnetcdf.NC_PUT_REQ_ALL``: flush all pending nonblocking PUT requests

        :param requests: [Optional]
            Integers specifying the nonblocking request IDs returned from the
            nonblocking requests posted earlier.
        :type requests: list of int

        :param status: [Optional]
            List of integers to hold returned error codes from the call, each
            specifying the status of corresponding nonblocking request. The
            values can be used in a call to :meth:`pnetcdf.strerror` to obtain
            the error messages.
        :type status: list

        :Operational mode: it is an independent subroutine and must be called
            while the file is in independent data mode.
        """
        return self._wait(num, requests, status, collective=False)

    def wait_all(self, num=None, requests=None, status=None):
        """
        wait_all(self, num=None, requests=None, status=None)

        Same as :meth:`File.wait` but in collective data mode

        :Operational mode: it is an collective subroutine and must be called
            while the file is in collective data mode.
        """
        return self._wait(num, requests, status, collective=True)

    def cancel(self, num=None, requests=None, status=None):
        """
        cancel(self, num=None, requests=None, status=None)

        This method cancels a list of pending nonblocking requests made by the
        nonblocking methods, such as :meth:`Variable.iput_var`,
        :meth:`Variable.iget_var`, and :meth:`Variable.bput_var`

        :param int num: [Optional]
            Number of requests. It is also the array size of the next two
            arguments. Alternatively it can be module-level constants:

            - ``pnetcdf.NC_REQ_ALL`` or ``None``: flush all pending nonblocking requests
            - ``pnetcdf.NC_GET_REQ_ALL``: flush all pending nonblocking GET requests
            - ``pnetcdf.NC_PUT_REQ_ALL``: flush all pending nonblocking PUT requests

        :param requests: [Optional]
            Integers specifying the nonblocking request IDs that were made
            earlier.
        :type requests: list of int

        :param status: [Optional]
            List of integers to hold returned error codes from the call, each
            specifying the status of corresponding nonblocking request. The
            values can be used in a call to :meth:`pnetcdf.strerror` to obtain
            the status messages.
        :type status: list

        :Operational mode: it can be called in either independent or collective
            data mode or define mode.
        """
        cdef int _file_id, ierr
        cdef int num_req
        cdef int *requestp
        cdef int *statusp
        _file_id = self._ncid
        if num is None:
            num = NC_REQ_ALL_C
        if num in [NC_REQ_ALL_C, NC_PUT_REQ_ALL_C, NC_GET_REQ_ALL_C]:
            num_req = num
            with nogil:
                ierr = ncmpi_cancel(_file_id, num_req, NULL, NULL)
            _check_err(ierr)
        else:
            requestp = <int *>malloc(sizeof(int) * num)
            statusp = <int *>malloc(sizeof(int) * num)
            num_req = num
            for n from 0 <= n < num:
                requestp[n] = requests[n]
            with nogil:
                ierr = ncmpi_cancel(_file_id, num_req, requestp, statusp)
            for n from 0 <= n < num:
                requests[n] = requestp[n]
            if status is not None:
                for n from 0 <= n < num:
                    status[n] = statusp[n]
            _check_err(ierr)


    def inq_nreqs(self):
        """
        inq_nreqs(self)

        Method to return the number of pending nonblocking requests.

        :rtype: int
        """
        cdef int _file_id, ierr
        cdef int num_req
        _file_id = self._ncid
        with nogil:
            ierr = ncmpi_inq_nreqs(_file_id, &num_req)
        _check_err(ierr)
        return num_req

    def attach_buff(self, bufsize):
        """
        attach_buff(self, bufsize)

        Allow PnetCDF to allocate an internal buffer for accommodating the
        write requests. This method call is the prerequisite of buffered
        non-blocking write. A call to :meth:`File.detach_buff` is required when
        this buffer is no longer needed.

        :param bufsize:
            Size of the buffer in the unit of bytes. Can be obtained using
            ``numpy.ndarray.nbytes``
        :type bufsize: int

        """
        cdef MPI_Offset buffsize
        cdef int _file_id
        buffsize = bufsize
        _file_id = self._ncid
        with nogil:
            ierr = ncmpi_buffer_attach(_file_id, buffsize)
        _check_err(ierr)

    def detach_buff(self):
        """
        detach_buff(self)

        Detach the write buffer previously attached for buffered non-blocking
        write
        """
        cdef int _file_id = self._ncid
        with nogil:
            ierr = ncmpi_buffer_detach(_file_id)
        _check_err(ierr)

    def inq_buff_usage(self):
        """
        inq_buff_usage(self)

        Return the current usage of the internal attached buffer, set in the
        call to :meth:`File.attach_buff`.

        :rtype: int
        """
        cdef int _file_id
        cdef MPI_Offset usage
        _file_id = self._ncid
        with nogil:
            ierr = ncmpi_inq_buffer_usage(_file_id, <MPI_Offset *>&usage)
        _check_err(ierr)
        return usage

    def inq_buff_size(self):
        """
        inq_buff_size(self)

        Return the size (in number of bytes) of the attached buffer. This value
        is the same as the one used in a call to :meth:`File.attach_buff`
        earlier.
        :rtype: int

        """
        cdef int _file_id
        cdef MPI_Offset buffsize
        _file_id = self._ncid
        with nogil:
            ierr = ncmpi_inq_buffer_size(_file_id, <MPI_Offset *>&buffsize)
        _check_err(ierr)
        return buffsize

    def inq_unlimdim(self):
        """
        inq_unlimdim(self)

        Return the unlimited dim instance of the file

        :return: The dimension instance with unlimited size
        :rtype: :class:`pnetcdf.Dimension`
        """

        cdef int ierr, unlimdimid
        with nogil:
            ierr = ncmpi_inq_unlimdim(self._ncid, &unlimdimid)
        _check_err(ierr)
        if unlimdimid == -1:
            return None
        for name, dim in self.dimensions.items():
            if dim._dimid == unlimdimid:
                return dim


    def set_fill(self, fillmode):
        """
        set_fill(self, fillmode)

        Sets the fill mode for a netCDF file open for writing and returns the
        current fill mode. The fill mode can be specified as either NC_FILL or
        NC_NOFILL. The default mode of PnetCDF is NC_NOFILL. The method call
        will change the fill mode for all variables defined so far at the time
        this API is called. In other words, it overwrites the fill mode for all
        variables previously defined. This method will also change the default
        fill mode for new variables defined following this call. In PnetCDF,
        this API only affects non-record variables. In addition, it can only be
        called while in the define mode. All non-record variables will be
        filled with fill values (either default or user-defined) at the time
        :meth:`File.enddef` is called.

        :param fillmode: ``pnetcdf.NC_FILL`` or ``pnetcdf.NC_NOFILL``
        :type fillmode: int

        :Operational mode: This method is a collective subroutine and must be
            called in define mode
        """
        cdef int _file_id, _fillmode, _old_fillmode
        _file_id = self._ncid
        _fillmode = fillmode
        with nogil:
            ierr = ncmpi_set_fill(_file_id, _fillmode, &_old_fillmode)
        _check_err(ierr)
        return _old_fillmode

    def set_auto_chartostring(self, value):
        """
        set_auto_chartostring(self, value)

        Call :meth:`Variable.set_auto_chartostring` for all variables
        contained in this `File`. Calling this function only affects existing
        variables.  Variables defined after calling this function will follow
        the default behaviour.

        :param value: True or False
        :type value: bool

        :Operational mode: Any
        """

        _vars = self.variables
        for var in _vars.values():
            var.set_auto_chartostring(value)


    def inq_num_rec_vars(self):
        """
        inq_num_rec_vars(self)

        Returns the number of record variables defined for this netCDF file

        :rtype: int

        """
        cdef int ierr, num_rec_vars
        with nogil:
            ierr = ncmpi_inq_num_rec_vars(self._ncid, &num_rec_vars)
        _check_err(ierr)
        return num_rec_vars

    def inq_num_fix_vars(self):
        """
        inq_num_fix_vars(self)

        Return the number of fixed-size variables defined for this netCDF file

        :rtype: int

        """
        cdef int ierr, num_fix_vars
        with nogil:
            ierr = ncmpi_inq_num_fix_vars(self._ncid, &num_fix_vars)
        _check_err(ierr)
        return num_fix_vars

    def inq_striping(self):
        """
        inq_striping(self)

        Return the file system striping size.

        :rtype: int
        """
        cdef int ierr, striping_size, striping_count
        with nogil:
            ierr = ncmpi_inq_striping(self._ncid, &striping_size, &striping_count)
        _check_err(ierr)
        return striping_size, striping_count

    def inq_recsize(self):
        """
        inq_recsize(self)

        Return the size of record block, sum of individual record sizes (one
        record each) of all record variables, for this netCDF file.

        :rtype: int

        """
        cdef int ierr
        cdef MPI_Offset recsize
        with nogil:
            ierr = ncmpi_inq_recsize(self._ncid, <MPI_Offset *>&recsize)
        _check_err(ierr)
        return recsize

    def inq_version(self):
        """
        inq_version(self)

        Return the file format version, one of the following PnetCDf constants.

            - ``pnetcdf.NC_CLASSIC_MODEL`` indicating the file is CDF-1 format
            - ``pnetcdf.NC_64BIT_OFFSET`` indicating the file is CDF-2 format
            - ``pnetcdf.NC_64BIT_DATA`` indicating the file is CDF-5 format
            - ``pnetcdf.NC_NETCDF4`` indicating the file is HDF5 format

        :rtype: int
        """
        cdef int ierr, nc_mode
        with nogil:
            ierr = ncmpi_inq_version(self._ncid, &nc_mode)
        _check_err(ierr)
        return nc_mode


    def inq_info(self):
        """
        inq_info(self)

        Returns an MPI info object containing all the file hints used by
        PnetCDF library.

        :rtype:  mpi4py.MPI.Info

        """
        cdef MPI_Info *mpiinfo
        cdef int ierr
        cdef MPI.Info info_py
        info_py = MPI.Info.Create()
        with nogil:
            ierr = ncmpi_inq_file_info(self._ncid, &info_py.ob_mpi)
        _check_err(ierr)
        return info_py

    def inq_header_size(self):
        """
        inq_header_size(self)

        Reports the current file header size (in bytes) of an opened netCDF
        file. Note this is the amount of space used by the metadata.

        :rtype: int
        """
        cdef int ierr
        cdef MPI_Offset size
        with nogil:
            ierr = ncmpi_inq_header_size(self._ncid, <MPI_Offset *>&size)
        _check_err(ierr)
        return size

    def inq_put_size(self):
        """
        inq_put_size(self)

        Reports the amount of data that has actually been written to the file
        since the file is opened/created.

        :rtype: int
        """
        cdef int ierr
        cdef MPI_Offset size
        with nogil:
            ierr = ncmpi_inq_put_size(self._ncid, <MPI_Offset *>&size)
        _check_err(ierr)
        return size

    def inq_get_size(self):
        """
        inq_get_size(self)

        Reports the amount of data that has actually the amount of data that
        has been actually read from the file since the file is opened/created.

        :rtype: int
        """
        cdef int ierr
        cdef MPI_Offset size
        with nogil:
            ierr = ncmpi_inq_get_size(self._ncid, <MPI_Offset *>&size)
        _check_err(ierr)
        return size

    def inq_header_extent(self):
        """
        inq_header_extent(self)

        Reports the current file header extent of an opened netCDF file. The
        amount is the file space allocated for the file header.

        :rtype: int
        """
        cdef int ierr
        cdef MPI_Offset extent
        with nogil:
            ierr = ncmpi_inq_header_extent(self._ncid, <MPI_Offset *>&extent)
        _check_err(ierr)
        return extent

cdef _get_dims(file):
    # Private function to create `Dimension` instances for all the
    # dimensions in a `File`
    cdef int ierr, numdims, n, _file_id
    cdef int *dimids
    cdef char namstring[NC_MAX_NAME+1]
    # get number of dimensions in this file.
    _file_id = file._ncid
    with nogil:
        ierr = ncmpi_inq_ndims(_file_id, &numdims)
    _check_err(ierr)
    # create empty dictionary for dimensions.
    dimensions = dict()
    if numdims > 0:
        dimids = <int *>malloc(sizeof(int) * numdims)
        for n from 0 <= n < numdims:
            dimids[n] = n
        for n from 0 <= n < numdims:
            with nogil:
                ierr = ncmpi_inq_dimname(_file_id, dimids[n], namstring)
            _check_err(ierr)
            name = namstring.decode('utf-8')
            dimensions[name] = Dimension(file = file, name = name, id=dimids[n])
        free(dimids)
    return dimensions

cdef _get_variables(file):
    # Private function to create `Variable` instances for all the
    # variables in a `File`
    cdef int ierr, numvars, n, nn, numdims, varid, classp, iendian, _file_id
    cdef int *varids
    cdef int *dimids
    cdef nc_type xtype
    cdef char namstring[NC_MAX_NAME+1]
    cdef char namstring_cmp[NC_MAX_NAME+1]
    # get number of variables in this File.
    _file_id = file._ncid
    with nogil:
        ierr = ncmpi_inq_nvars(_file_id, &numvars)
    _check_err(ierr, err_cls=AttributeError)
    # create empty dictionary for variables.
    variables = dict()
    if numvars > 0:
        # get variable ids.
        varids = <int *>malloc(sizeof(int) * numvars)
        for n from 0 <= n < numvars:
            varids[n] = n
        # loop over variables.
        for n from 0 <= n < numvars:
            varid = varids[n]
            # get variable name.
            with nogil:
                ierr = ncmpi_inq_varname(_file_id, varid, namstring)
            _check_err(ierr)
            name = namstring.decode('utf-8')
            # get variable type.
            with nogil:
                ierr = ncmpi_inq_vartype(_file_id, varid, &xtype)
            _check_err(ierr)
            # check to see if it is a supported user-defined type.
            try:
                datatype = _nctonptype[xtype]
            except KeyError:
                msg="WARNING: variable '%s' has unsupported datatype, skipping .." % name
                warnings.warn(msg)
                continue
            # get number of dimensions.
            with nogil:
                ierr = ncmpi_inq_varndims(_file_id, varid, &numdims)
            _check_err(ierr)
            dimids = <int *>malloc(sizeof(int) * numdims)
            # get dimension ids.
            with nogil:
                ierr = ncmpi_inq_vardimid(_file_id, varid, dimids)
            _check_err(ierr)
            dimensions = []
            for nn from 0 <= nn < numdims:
                for key, value in file.dimensions.items():
                    if value._dimid == dimids[nn]:
                        dimensions.append(value)
                        break
            # create variable instance
            variables[name] = Variable(file, name, xtype, dimensions, id=varid)
        free(varids) # free pointer holding variable ids.
    return variables

cdef class Dataset(File):
    pass
