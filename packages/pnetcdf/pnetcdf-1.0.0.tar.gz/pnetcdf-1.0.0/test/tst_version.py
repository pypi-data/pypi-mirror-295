#
# Copyright (C) 2024, Northwestern University and Argonne National Laboratory
# See COPYRIGHT notice in top-level directory.
#

import re
import pnetcdf

version_str = pnetcdf.__version__
pattern = r'^\d+\.\d+\.\d+$'
# Assert that the version string matches the pattern
assert re.match(pattern, version_str), f"Version string '{version_str}' does not match the expected format 'x.x.x'"
