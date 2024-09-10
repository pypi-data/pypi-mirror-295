##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.19.1+ob(v1)                                                   #
# Generated on 2024-09-09T18:18:13.670415                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow._vendor.click.core
    import metaflow.exception
    import metaflow.plugins.logs_cli

LOGGER_TIMESTAMP: str

class CommandException(metaflow.exception.MetaflowException, metaclass=type):
    ...

LOG_SOURCES: list

class CustomGroup(metaflow._vendor.click.core.Group, metaclass=type):
    def __init__(self, name = None, commands = None, default_cmd = None, **attrs):
        ...
    def get_command(self, ctx, cmd_name):
        ...
    def parse_args(self, ctx, args):
        ...
    def resolve_command(self, ctx, args):
        ...
    def format_commands(self, ctx, formatter):
        ...
    ...

class CustomFormatter(object, metaclass=type):
    def __init__(self, default_cmd, original_formatter):
        ...
    def __getattr__(self, name):
        ...
    def write_dl(self, rows):
        ...
    ...

logs: CustomGroup

