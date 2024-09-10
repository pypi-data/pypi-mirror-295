##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.19.1+ob(v1)                                                   #
# Generated on 2024-09-09T18:18:13.665284                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.event_logger

class DebugEventLogger(metaflow.event_logger.NullEventLogger, metaclass=type):
    @classmethod
    def get_worker(cls):
        ...
    ...

class DebugEventLoggerSidecar(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    ...

