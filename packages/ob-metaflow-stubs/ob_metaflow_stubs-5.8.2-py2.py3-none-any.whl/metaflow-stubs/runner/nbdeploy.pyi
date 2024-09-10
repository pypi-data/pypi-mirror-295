##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.19.1+ob(v1)                                                   #
# Generated on 2024-09-09T18:18:13.649465                                        #
##################################################################################

from __future__ import annotations

import typing

class Deployer(object, metaclass=type):
    def __init__(self, flow_file: str, show_output: bool = True, profile: typing.Optional[str] = None, env: typing.Optional[typing.Dict] = None, cwd: typing.Optional[str] = None, file_read_timeout: int = 3600, **kwargs):
        ...
    def _Deployer__make_function(self, deployer_class):
        """
        Create a function for the given deployer class.
        
        Parameters
        ----------
        deployer_class : Type[DeployerImpl]
            Deployer implementation class.
        
        Returns
        -------
        Callable
            Function that initializes and returns an instance of the deployer class.
        """
        ...
    ...

def get_current_cell(ipython):
    ...

def format_flowfile(cell):
    """
    Formats the given cell content to create a valid Python script that can be executed as a Metaflow flow.
    """
    ...

DEFAULT_DIR: str

class NBDeployerInitializationError(Exception, metaclass=type):
    ...

class NBDeployer(object, metaclass=type):
    def __init__(self, flow, show_output: bool = True, profile: typing.Optional[str] = None, env: typing.Optional[typing.Dict] = None, base_dir: str = "/tmp", file_read_timeout: int = 3600, **kwargs):
        ...
    def cleanup(self):
        """
        Delete any temporary files created during execution.
        """
        ...
    ...

