##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.19.1+ob(v1)                                                   #
# Generated on 2024-09-09T18:18:13.648959                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.runner.deployer
    import metaflow.runner.subprocess_manager
    import metaflow.exception

class MetaflowNotFound(metaflow.exception.MetaflowException, metaclass=type):
    ...

class CommandManager(object, metaclass=type):
    def __init__(self, command: typing.List[str], env: typing.Optional[typing.Dict[str, str]] = None, cwd: typing.Optional[str] = None):
        """
        Create a new CommandManager object.
        This does not run the process itself but sets it up.
        
        Parameters
        ----------
        command : List[str]
            The command to run in List form.
        env : Optional[Dict[str, str]], default None
            Environment variables to set for the subprocess; if not specified,
            the current enviornment variables are used.
        cwd : Optional[str], default None
            The directory to run the subprocess in; if not specified, the current
            directory is used.
        """
        ...
    def __aenter__(self) -> metaflow.runner.subprocess_manager.CommandManager:
        ...
    def __aexit__(self, exc_type, exc_value, traceback):
        ...
    def wait(self, timeout: typing.Optional[float] = None, stream: typing.Optional[str] = None):
        """
        Wait for the subprocess to finish, optionally with a timeout
        and optionally streaming its output.
        
        You can only call `wait` if `async_run` has already been called.
        
        Parameters
        ----------
        timeout : Optional[float], default None
            The maximum time to wait for the subprocess to finish.
            If the timeout is reached, the subprocess is killed.
        stream : Optional[str], default None
            If specified, the specified stream is printed to stdout. `stream` can
            be one of `stdout` or `stderr`.
        """
        ...
    def run(self, show_output: bool = False):
        """
        Run the subprocess synchronously. This can only be called once.
        
        This also waits on the process implicitly.
        
        Parameters
        ----------
        show_output : bool, default False
            Suppress the 'stdout' and 'stderr' to the console by default.
            They can be accessed later by reading the files present in:
                - self.log_files["stdout"]
                - self.log_files["stderr"]
        """
        ...
    def async_run(self):
        """
        Run the subprocess asynchronously. This can only be called once.
        
        Once this is called, you can then wait on the process (using `wait`), stream
        logs (using `stream_logs`) or kill it (using `kill`).
        """
        ...
    def stream_log(self, stream: str, position: typing.Optional[int] = None, timeout_per_line: typing.Optional[float] = None, log_write_delay: float = 0.01) -> typing.Iterator[typing.Tuple[int, str]]:
        """
        Stream logs from the subprocess line by line.
        
        Parameters
        ----------
        stream : str
            The stream to stream logs from. Can be one of "stdout" or "stderr".
        position : Optional[int], default None
            The position in the log file to start streaming from. If None, it starts
            from the beginning of the log file. This allows resuming streaming from
            a previously known position
        timeout_per_line : Optional[float], default None
            The time to wait for a line to be read from the log file. If None, it
            waits indefinitely. If the timeout is reached, a LogReadTimeoutError
            is raised. Note that this timeout is *per line* and not cumulative so this
            function may take significantly more time than `timeout_per_line`
        log_write_delay : float, default 0.01
            Improves the probability of getting whole lines. This setting is for
            advanced use cases.
        
        Yields
        ------
        Tuple[int, str]
            A tuple containing the position in the log file and the line read. The
            position returned can be used to feed into another `stream_logs` call
            for example.
        """
        ...
    def emit_logs(self, stream: str = "stdout", custom_logger: typing.Callable[..., None] = print):
        """
        Helper function that can easily emit all the logs for a given stream.
        
        This function will only terminate when all the log has been printed.
        
        Parameters
        ----------
        stream : str, default "stdout"
            The stream to emit logs for. Can be one of "stdout" or "stderr".
        custom_logger : Callable[..., None], default print
            A custom logger function that takes in a string and "emits" it. By default,
            the log is printed to stdout.
        """
        ...
    def cleanup(self):
        """
        Clean up log files for a running subprocesses.
        """
        ...
    def kill(self, termination_timeout: float = 1):
        """
        Kill the subprocess and its descendants.
        
        Parameters
        ----------
        termination_timeout : float, default 1
            The time to wait after sending a SIGTERM to the process and its descendants
            before sending a SIGKILL.
        """
        ...
    ...

class SubprocessManager(object, metaclass=type):
    def __init__(self):
        ...
    def __aenter__(self) -> metaflow.runner.subprocess_manager.SubprocessManager:
        ...
    def __aexit__(self, exc_type, exc_value, traceback):
        ...
    def run_command(self, command: typing.List[str], env: typing.Optional[typing.Dict[str, str]] = None, cwd: typing.Optional[str] = None, show_output: bool = False) -> int:
        """
        Run a command synchronously and return its process ID.
        
        Parameters
        ----------
        command : List[str]
            The command to run in List form.
        env : Optional[Dict[str, str]], default None
            Environment variables to set for the subprocess; if not specified,
            the current enviornment variables are used.
        cwd : Optional[str], default None
            The directory to run the subprocess in; if not specified, the current
            directory is used.
        show_output : bool, default False
            Suppress the 'stdout' and 'stderr' to the console by default.
            They can be accessed later by reading the files present in the
            CommandManager object:
                - command_obj.log_files["stdout"]
                - command_obj.log_files["stderr"]
        Returns
        -------
        int
            The process ID of the subprocess.
        """
        ...
    def async_run_command(self, command: typing.List[str], env: typing.Optional[typing.Dict[str, str]] = None, cwd: typing.Optional[str] = None) -> int:
        """
        Run a command asynchronously and return its process ID.
        
        Parameters
        ----------
        command : List[str]
            The command to run in List form.
        env : Optional[Dict[str, str]], default None
            Environment variables to set for the subprocess; if not specified,
            the current enviornment variables are used.
        cwd : Optional[str], default None
            The directory to run the subprocess in; if not specified, the current
            directory is used.
        
        Returns
        -------
        int
            The process ID of the subprocess.
        """
        ...
    def get(self, pid: int) -> typing.Optional["CommandManager"]:
        """
        Get one of the CommandManager managed by this SubprocessManager.
        
        Parameters
        ----------
        pid : int
            The process ID of the subprocess (returned by run_command or async_run_command).
        
        Returns
        -------
        Optional[CommandManager]
            The CommandManager object for the given process ID, or None if not found.
        """
        ...
    def cleanup(self):
        """
        Clean up log files for all running subprocesses.
        """
        ...
    ...

def read_from_file_when_ready(file_path: str, timeout: float = 5):
    ...

def handle_timeout(tfp_runner_attribute, command_obj: metaflow.runner.subprocess_manager.CommandManager, file_read_timeout: int):
    """
    Handle the timeout for a running subprocess command that reads a file
    and raises an error with appropriate logs if a TimeoutError occurs.
    
    Parameters
    ----------
    tfp_runner_attribute : NamedTemporaryFile
        Temporary file that stores runner attribute data.
    command_obj : CommandManager
        Command manager object that encapsulates the running command details.
    
    Returns
    -------
    str
        Content read from the temporary file.
    
    Raises
    ------
    RuntimeError
        If a TimeoutError occurs, it raises a RuntimeError with the command's
        stdout and stderr logs.
    """
    ...

def get_lower_level_group(api, top_level_kwargs: typing.Dict, _type: typing.Optional[str], deployer_kwargs: typing.Dict):
    """
    Retrieve a lower-level group from the API based on the type and provided arguments.
    
    Parameters
    ----------
    api : MetaflowAPI
        Metaflow API instance.
    top_level_kwargs : Dict
        Top-level keyword arguments to pass to the API.
    _type : str
        Type of the deployer implementation to target.
    deployer_kwargs : Dict
        Keyword arguments specific to the deployer.
    
    Returns
    -------
    Any
        The lower-level group object retrieved from the API.
    
    Raises
    ------
    ValueError
        If the `_type` is None.
    """
    ...

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

class TriggeredRun(object, metaclass=type):
    def __init__(self, deployer: DeployerImpl, content: str):
        ...
    def wait_for_run(self, timeout = None):
        """
        Wait for the `run` property to become available.
        
        Parameters
        ----------
        timeout : int, optional
            Maximum time to wait for the `run` to become available, in seconds. If None, wait indefinitely.
        
        Raises
        ------
        TimeoutError
            If the `run` is not available within the specified timeout.
        """
        ...
    @property
    def run(self):
        """
        Retrieve the `Run` object for the triggered run.
        
        Note that Metaflow `Run` becomes available only when the `start` task
        has started executing.
        
        Returns
        -------
        Run, optional
            Metaflow Run object if the `start` step has started executing, otherwise None.
        """
        ...
    ...

class DeployedFlow(object, metaclass=type):
    def __init__(self, deployer: DeployerImpl):
        ...
    ...

class DeployerImpl(object, metaclass=type):
    def __init__(self, flow_file: str, show_output: bool = True, profile: typing.Optional[str] = None, env: typing.Optional[typing.Dict] = None, cwd: typing.Optional[str] = None, file_read_timeout: int = 3600, **kwargs):
        ...
    def __enter__(self) -> DeployerImpl:
        ...
    def create(self, **kwargs) -> DeployedFlow:
        """
        Create a deployed flow using the deployer implementation.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments to pass to `create` corresponding to the
            command line arguments of `create`
        
        Returns
        -------
        DeployedFlow
            DeployedFlow object representing the deployed flow.
        
        Raises
        ------
        Exception
            If there is an error during deployment.
        """
        ...
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Cleanup resources on exit.
        """
        ...
    def cleanup(self):
        """
        Cleanup resources.
        """
        ...
    ...

