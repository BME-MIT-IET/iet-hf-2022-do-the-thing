import inspect
import logging
import os


def logger():
    global _logger_instances
    # inspect.stack(1)[2]: caller infomations.
    caller_filename = inspect.stack(1)[2][1]
    if caller_filename not in _logger_instances:
        caller = caller_filename.split(os.sep)[-1]
        _logger_instances[caller_filename] = logging.getLogger(caller)
    return _logger_instances[caller_filename]


_logger_instances = {}
