# -------------------------------------------------------------------------------
# (c) Copyright 2024 Sony Semiconductor Israel, Ltd. All rights reserved.
#
#      This software, in source or object form (the "Software"), is the
#      property of Sony Semiconductor Israel Ltd. (the "Company") and/or its
#      licensors, which have all right, title and interest therein, You
#      may use the Software only in accordance with the terms of written
#      license agreement between you and the Company (the "License").
#      Except as expressly stated in the License, the Company grants no
#      licenses by implication, estoppel, or otherwise. If you are not
#      aware of or do not agree to the License terms, you may not use,
#      copy or modify the Software. You may use the source code of the
#      Software only for your internal purposes and may not distribute the
#      source code of the Software, any part thereof, or any derivative work
#      thereof, to any third party, except pursuant to the Company's prior
#      written consent.
#      The Software is the confidential information of the Company.
# -------------------------------------------------------------------------------
"""
Created on 7/8/24

@author: irenab
"""
from enum import Enum
from typing import Optional
import logging

from uni.common.logger import ContextInfo
try:
    from uni.common.logger import set_logging
except ImportError:
    from uni.common.logger import _set_logging as set_logging


def setup_uni_logging(logger_name: str,
                      logger_level: 'SDSPLoggerLevel',
                      logger_format: 'LoggerFormat',
                      context: str,
                      component: str,
                      component_suffix: Optional[str] = None):
    level = _sdsp_level_to_python_logging[logger_level]
    if level is not None:
        component_name = f'{component}-{component_suffix}' if component_suffix else component
        ctx = ContextInfo(logger=logger_name, context=context, component_type=component, component_name=component_name)
        set_logging(level, ctx, logger_format)


class LoggerFormat(str, Enum):
    JSON = 'json'
    TEXT = 'text'

    @classmethod
    def values(cls):
        return [v.value for v in cls]


class SDSPLoggerLevel(str, Enum):
    # values are level strings defined for all conv tools
    TRACE = 'trace'
    DEBUG = 'debug'
    INFO = 'info'
    WARN = 'warn'
    ERROR = 'error'
    OFF = 'off'

    @classmethod
    def values(cls):
        return [v.value for v in cls]


# keys are the sdsp logger level options
_sdsp_level_to_python_logging = {
    SDSPLoggerLevel.TRACE: logging.DEBUG,
    SDSPLoggerLevel.DEBUG: logging.DEBUG,
    SDSPLoggerLevel.INFO: logging.INFO,
    SDSPLoggerLevel.WARN: logging.WARNING,
    SDSPLoggerLevel.ERROR: logging.ERROR,
    SDSPLoggerLevel.OFF: None,
}
