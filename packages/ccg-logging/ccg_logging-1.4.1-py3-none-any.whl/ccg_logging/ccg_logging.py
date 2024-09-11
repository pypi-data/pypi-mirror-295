import sys
import warnings
from pathlib import Path
from typing import Any

import pandas as pd
from loguru import logger


FORMAT = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {message}'


def setup(path: Path = None, format: str = FORMAT):
    """Sets up the logger to log in the format we want.
    
    This is done because technically every log entry is made from this file - and
    the default format records only that.

    We use our custom format here that removes that (and we add the actual 
    function to the message itself).
    """
    logger.remove()  # remove the default one

    if path is not None:
        logger.add(path, format=format)

    logger.add(sys.stderr, format=format)


def log_function_call(level: str = 'DEBUG', **kwargs):  # ALL "include" PARAMS NOW DEPRECATED, remove in 1.5
    """Logs a function call.

    For a decorated function, two log entries will be made:
    - When the function is initially called - including parameters
    - When the function returns - including parameters and the output

    Any parameter / return values that aren't appropriate to log are coerced to
    a cleaner format.

    For example, a DataFrame with 100 rows and 3 columns is represented by "DataFrame<shape=(100, 3)>".

    Args:
        level (str, default = 'DEBUG'):
            The logging level to use. 

    """
    if kwargs:
        msg = 'All arguments apart from `level` are now deprecated'
        warnings.warn(msg, category=UserWarning)

    def decorator(function: callable):

        def wrapper(*args, **kwargs):
            function_call_str = _get_function_call_str(function, args, kwargs)
            logger.log(level, function_call_str)

            try:
                output = function(*args, **kwargs)
            except Exception as error:
                error_str = _get_error_str(error, function_call_str)
                logger.log('ERROR', error_str)
                raise error

            output_str = _get_output_str(output, function_call_str)
            logger.log(level, output_str)

            return output

        return wrapper

    return decorator    


def _get_function_call_str(function: callable, args: tuple, kwargs: dict) -> str:
    function_call_params_str = _get_function_call_params_str(args, kwargs)
    return f'{function.__module__}:{function.__name__}({function_call_params_str})'


def _get_function_call_params_str(args: str, kwargs: dict) -> str:
    return ', '.join(
        [
            _coerce_value(arg)
            for arg 
            in args
        ]
        + [
            f'{k}={_coerce_value(v)}' 
            for k, v 
            in kwargs.items()
        ]
    )


def _get_output_str(output: Any, function_call_str: str) -> str:
    return function_call_str + f' -> {_coerce_value(output)}'


def _get_error_str(error: Exception, function_call_str: str) -> str:
    return function_call_str + f' -> {error.__repr__()}'


def _coerce_value(value: Any) -> Any:
    if value is None:
        return 'None'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        return _coerce_str(value)
    elif isinstance(value, (list, set, tuple, dict)):
        return _coerce_basic_iterable(value)
    elif isinstance(value, pd.DataFrame):
        return _coerce_dataframe(value)
    elif isinstance(value, pd.Series):
        return _coerce_series(value)
    else:
        return _coerce_other(value)


def _coerce_str(value: str) -> str:
    # Limit the string the 50 characters.
    if len(value) <= 50:
        return value.__repr__()
    else:
        truncated = value[:47] + '...'
        return truncated.__repr__()


def _coerce_basic_iterable(value: list | set | tuple | dict) -> str:
    if len(value.__repr__()) <= 50:
        return value.__repr__()
    else:
        return f'{value.__class__.__name__}<len={len(value)}>'


def _coerce_dataframe(value: pd.DataFrame) -> str:
    return f'DataFrame<shape={value.shape}>'


def _coerce_series(value: pd.Series) -> str:
    return f'Series<len={len(value)}>'


def _coerce_other(value: Any) -> str:
    return value.__class__.__name__
