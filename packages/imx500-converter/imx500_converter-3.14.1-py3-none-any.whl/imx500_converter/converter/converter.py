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
import argparse
import logging
import os
import shutil
import sys
import tempfile
from typing import Callable, List, Optional

from imx500_converter.converter.util.error import ValidationErrors, ConverterError
from imx500_converter.converter.util.logger import setup_uni_logging, SDSPLoggerLevel, LoggerFormat
from imx500_converter.converter.imx_cfg import MemoryUnits, ConverterCfg, NetworkCfg

from imx500_converter import __version__
from imx500_converter.converter.imx_cfg_file_reader import CfgFileReader
from imx500_converter.converter.sdspconv_runner import SDSPConvRunner
from imx500_converter.converter.uni_converter_runner import UniConverterRunner

LOGGER_COMPONENT = "IMX"
CONTEXT_LOGGER_NAME = 'IMX'


def convert(uni_main: Callable, uni_exec: str, cli_args: Optional[List] = None):
    try:
        config = _process_args(uni_exec, cli_args)

        _setup_logging(config)

        uni_fw_out_dir = _get_uni_out_dir(config.output_dir, config.keep_temp)
        ret = UniConverterRunner(uni_main).run(config, uni_fw_out_dir)
        if ret:
            return ret

        ret = SDSPConvRunner().run(config, uni_fw_out_dir)
        if ret:
            logging.error(f'sdspconv exited with error code: {ret}, uni files can be found in {uni_fw_out_dir}')
        elif not config.keep_temp:
            shutil.rmtree(uni_fw_out_dir)
        return ret

    except ValidationErrors as e:
        for err in e.errors:
            logging.error(err)
    except ConverterError as e:
        logging.error(f'Convertion failed with: {e}')
    except Exception as e:
        logging.exception(e)
    return 1


def _get_uni_out_dir(output_dir: str, keep_temp: bool) -> str:
    if keep_temp:
        os.makedirs(output_dir, exist_ok=True)
        uni_out_dir = output_dir
    else:
        uni_out_dir = tempfile.TemporaryDirectory().name
    return uni_out_dir


def _setup_logging(cfg: ConverterCfg):
    context = cfg.logger_context or str(os.getpid())
    setup_uni_logging(logger_name=CONTEXT_LOGGER_NAME,
                      logger_level=SDSPLoggerLevel(cfg.logger_level),
                      logger_format=LoggerFormat(cfg.logger_format),
                      context=context,
                      component=LOGGER_COMPONENT,
                      component_suffix=None)


def _process_args(uni_exec: str, cli_args: Optional[List]) -> ConverterCfg:
    p = _setup_parser()
    args = _parse_args(p, uni_exec, cli_args)
    cfg = _convert_args(args)
    return cfg


def _setup_parser() -> argparse.ArgumentParser:
    """
    Note: all defaults are set to None so that we can identify args that were and were not passed in cli, in order
    to be able to handle cli precedence over config file correctly.
    Defaults shown in help should be the actual default.
    """
    defaults = ConverterCfg.get_fields_info().defaults
    defaults['input_persistency'] = NetworkCfg.get_fields_info().defaults['input_persistency']

    p = argparse.ArgumentParser()

    # defined as a regular arg so that it can be used with logger-level to show sub-tools versions
    p.add_argument('-v', '--version', default=None, action='store_true')

    # required (mutually exclusive)
    p.add_argument('-c', '--config', default=None, help=argparse.SUPPRESS)
    # -----------------------------------------------------------------------------
    p.add_argument('-i', '--input-path', default=None, help='Input network file path')
    p.add_argument('-o', '--output-dir', default=None, help='Output directory path')

    # optional
    p.add_argument('--overwrite-output',
                   default=None,
                   action='store_true',
                   help='Allow overwriting of existing files in output-dir. By default, an error will be raised')

    p.add_argument('--report-size-unit',
                   default=None,
                   type=str,
                   choices=MemoryUnits.values(),
                   help=f'Units of memory size in memory report. Default: {defaults["report_size_unit"]}')
    p.add_argument('--memory-report',
                   default=None,
                   action='store_true',
                   help='Produce memory report and dnnParams.xml file without converting the network')
    p.add_argument('--model-insight',
                   default=None,
                   action='store_true',
                   help='Produce model insight files. Experimental feature')
    p.add_argument('--no-verify-java',
                   default=None,
                   action='store_true',
                   help='Skip java availability verification (supported on Linux OS only)')
    group_input_persistency = p.add_mutually_exclusive_group(required=False)
    group_input_persistency.add_argument('--input-persistency',
                                         dest='input_persistency',
                                         default=None,
                                         action='store_true',
                                         help=f'Enable input persistency during inference '
                                         f'{"(default)" if defaults["input_persistency"] else ""}')
    group_input_persistency.add_argument('--no-input-persistency',
                                         dest='input_persistency',
                                         default=None,
                                         action='store_false',
                                         help=f'Disable input persistency during inference '
                                         f'{"(default)" if not defaults["input_persistency"] else ""}')

    group_logger = p.add_argument_group(title='Logging options')
    group_logger.add_argument('--logger-format',
                              default=None,
                              type=str,
                              choices=LoggerFormat.values(),
                              help=f'The format of the logging output. Default: {defaults["logger_format"]}')
    group_logger.add_argument('--logger-level',
                              default=None,
                              type=str,
                              choices=SDSPLoggerLevel.values(),
                              help=f'Set the verbosity level of the application. Default: {defaults["logger_level"]}')
    group_logger.add_argument('--logger-context', default=None, help=argparse.SUPPRESS)

    # suppressed
    p.add_argument('--keep-temp', default=None, action='store_true', help=argparse.SUPPRESS)
    p.add_argument('--extra-sdspconv-args', default=None, help=argparse.SUPPRESS)
    return p


def _parse_args(parser: argparse.ArgumentParser, uni_exec: str, cli_args: Optional[List] = None) -> argparse.Namespace:
    """
    uni_exec: the name of uni-converter executable to use for obtaining its version
    """
    args = parser.parse_args(cli_args) if cli_args else parser.parse_args()

    if args.version:
        print(f"{parser.prog} {__version__}")
        sys.stdout.flush()

        if args.logger_level in [SDSPLoggerLevel.DEBUG]:
            os.system(f"{uni_exec} --version")
            os.system(f"sdspconv --version --logger-level {args.logger_level}")
        parser.exit(0)

    if args.config:
        if args.input_path or args.output_dir:
            parser.error('Cannot use both configuration file and direct input/output.\n'
                         'Either use: -i/--input-path and -o/--output-dir for single conversion '
                         'or use: -c/--config to specify a configuration file.')
        # NOTE!!! if this changes or any cli flag needs to override network flags, need to update _convert_args
        if args.input_persistency is not None:
            parser.error('Cannot use --input-persistency / --no-input-persistency with a configuration file. '
                         'please specify in the configuration file which network should run with this flag.')
    else:
        if args.input_path is None or args.output_dir is None:
            # TODO update error message once cfg is un-hidden
            parser.error('Please specify mandatory flags --input-path and --output-dir')
    return args


def _convert_args(args: argparse.Namespace) -> ConverterCfg:
    # filter args that were explicitly passed
    passed_cli_args = {k: v for k, v in vars(args).items() if v is not None and k not in ['version', 'config']}
    if args.config:
        cfg: ConverterCfg = CfgFileReader(args.config).parse()
        # override top level args (network args from cli is not currently allowed)
        cfg = cfg.updated(**passed_cli_args)
    else:
        net_kwargs = {}
        if args.input_persistency is not None:
            net_kwargs = {'input_persistency': args.input_persistency}
            del passed_cli_args['input_persistency']
        network = NetworkCfg(input_path=passed_cli_args.pop('input_path'), ordinal=0, **net_kwargs)
        cfg = ConverterCfg(networks=[network], **passed_cli_args)
    return cfg
