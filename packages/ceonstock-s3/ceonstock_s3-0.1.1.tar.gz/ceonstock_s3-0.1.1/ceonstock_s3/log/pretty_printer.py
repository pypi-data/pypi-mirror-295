from typing import List, Dict, Callable, Optional, Union, Type

from ceonstock.log import module_logger

logger = module_logger()
logger.setLevel("INFO")


def printify(
    data: Union[Dict, List], msg: Optional[str] = None, indent: int = 1
) -> str:
    logger.debug(f"Got data of type {type(data)}: {data}")
    """ Returns data object as a string formmatted for printing """
    fn = get_printify_function(data)
    logger.debug(f"Chosen fn: {fn}")
    as_str = "\n" + fn(data, indent=indent)
    if msg:
        as_str = msg + as_str
    return as_str


def get_printify_function(data: Union[Dict, List]) -> Callable:
    LOOKUP = {dict: printify_dict, list: printify_list}
    logger.debug(f"LOOKUP: {LOOKUP}")
    try:
        fn = LOOKUP[type(data)]
    except KeyError as e:
        logger.debug(f"KeyError: {e}")
        try:  # Try to convert data type to a dict.
            test = data.__dict__
            return printify_class
        except AttributeError:
            logger.warn(f"Invalid data type: {type(data)}")
        return printify_str
    logger.debug(f"fn: {fn}")
    return fn


def printify_str(data, indent=1) -> str:
    tabs = "\t" * indent
    return tabs + str(data)


def printify_dict(data: Dict, indent: int = 1) -> str:
    """Returns data object as a string formmatted for printing"""
    dict_to_print = {key: str(value) for (key, value) in data.items()}
    tabs = "\t" * indent
    lines = []
    for name, path in dict_to_print.items():
        lines.append(f"{tabs}{name}:\t{path}")
    as_str = "\n".join([line for line in lines])
    return as_str


def printify_list(data: list, indent: int = 1) -> str:
    """Returns data object as a string formmatted for printing"""
    list_to_print = [str(value) for value in data]
    tabs = "\t" * indent
    lines = []
    for item in list_to_print:
        lines.append(f"{tabs}{item}")
    as_str = "\n".join([line for line in lines])
    return as_str


def printify_class(data, indent: int = 1) -> str:
    return printify_dict(data.__dict__, indent=indent)
