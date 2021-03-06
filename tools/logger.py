# -*- coding: utf_8 -*-
"""Logger Config."""
from datetime import datetime
import sys
import logging
from colorama import Back, Fore, Style
from pygments.lexers.smalltalk import SmalltalkLexer
from pygments.styles.solarized import SolarizedDarkStyle
from pygments.formatters import TerminalFormatter
from pygments import highlight


class ColorLogsWrapper(object):
    COLOR_MAP = {
        'debug': Fore.BLUE,
        'info': Fore.CYAN,
        'warning': Fore.YELLOW,
        'error': Fore.RED,
        'critical': Back.RED,
    }

    def __init__(self, logger):
        self.logger = logger

    def __getattr__(self, attr_name):
        """Getattr."""
        if attr_name == 'info':
            attr_name = 'info'
        if attr_name not in 'debug info warning error critical l2':
            return getattr(self.logger, attr_name)
        if attr_name == 'l2':
            log_level = getattr(logging, 'info'.upper())
        else:
            log_level = getattr(logging, attr_name.upper())

        # mimicking logging/__init__.py behaviour
        # if not self.logger.isEnabledFor(log_level):
        #     return

        def wrapped_attr(msg, *args, **kwargs):
            if not self.logger.isEnabledFor(log_level):
                return
            # style_prefix = self.COLOR_MAP[attr_name]
            # msg = style_prefix + str(msg) + Style.RESET_ALL
            if attr_name == 'l2':
                msg = highlight(f'    {str(msg)}', SmalltalkLexer(encoding='utf-8'),
                                TerminalFormatter(style=SolarizedDarkStyle))
                # log_level = getattr(logging, 'info'.upper())
            else:
                msg = highlight(f'{str(msg)}', SmalltalkLexer(encoding='utf-8'),
                                TerminalFormatter(style=SolarizedDarkStyle))
            # We call _.log directly to not increase the callstack
            # so that Logger.findCaller extract the corrects filename/lineno
            return self.logger._log(log_level, msg, args, **kwargs)

        return wrapped_attr


def init_logger(module_name) -> logging.Logger:
    """Setup logger."""
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(stream=sys.stderr,
                        format=log_format,
                        level=logging.INFO)
    logger_obj = logging.getLogger(module_name)
    logger = ColorLogsWrapper(logger_obj)
    return logger
