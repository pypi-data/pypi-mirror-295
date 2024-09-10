##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.19.1+ob(v1)                                                   #
# Generated on 2024-09-09T18:18:13.665511                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.monitor

class DebugMonitor(metaflow.monitor.NullMonitor, metaclass=type):
    @classmethod
    def get_worker(cls):
        ...
    ...

class DebugMonitorSidecar(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    ...

