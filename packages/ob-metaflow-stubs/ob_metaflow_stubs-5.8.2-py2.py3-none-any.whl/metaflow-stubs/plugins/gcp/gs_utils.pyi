##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.19.1+ob(v1)                                                   #
# Generated on 2024-09-09T18:18:13.708671                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

class MetaflowInternalError(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowGSPackageError(metaflow.exception.MetaflowException, metaclass=type):
    ...

def parse_gs_full_path(gs_uri):
    ...

def check_gs_deps(func):
    """
    The decorated function checks GS dependencies (as needed for Google Cloud storage backend). This includes
    various GCP SDK packages, as well as a Python version of >=3.7
    """
    ...

def process_gs_exception(*args, **kwargs):
    ...

