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
Created on 7/10/24

@author: irenab
"""
import logging
from typing import Callable

from imx500_converter.converter.imx_cfg import ConverterCfg
from imx500_converter.converter.util.cli import split_cli_args


class UniConverterRunner:
    # tiresome black list so that we don't silently ignore new keys
    IGNORE_KEYS_FOR_CLI = [
        'networks', 'output_dir', 'overwrite_output', 'report_size_unit', 'memory_report', 'model_insight', 'keep_temp',
        'extra_sdspconv_args', 'no_verify_java'
    ]

    def __init__(self, uni_main: Callable):
        self.uni_main = uni_main

    def run(self, cfg: ConverterCfg, uni_out_dir: str) -> int:
        for network_cfg in cfg.networks:
            cli_args = f'--input-path {network_cfg.input_path} --output-dir {uni_out_dir} '
            cli_args += cfg.to_cli_args(exclude_fields=self.IGNORE_KEYS_FOR_CLI)
            logging.debug(f'running {self.uni_main.__module__} {cli_args}')
            ret_code = self.uni_main(split_cli_args(cli_args), setup_logging=False)
            # even if one conversion fails, the flow stops
            if ret_code:
                return ret_code
        return 0
