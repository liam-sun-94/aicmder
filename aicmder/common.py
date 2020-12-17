import pickle
from pathlib import Path
import ruamel.yaml as yaml
from typing import Text, Any, Dict, Union, List, Type, Callable
import logging
import os, json

__all__ = ['set_logger', 'read_yaml_file', 'read_json_file', 'pickle_load']

# for log
LOG_VERBOSE = False


def set_logger(context, verbose=False):
    if os.name == 'nt':  # for Windows
        return NTLogger(context, verbose)
    # logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    logger = logging.getLogger(context)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    formatter = logging.Formatter(
        '%(levelname)-.1s:' + context + ':[%(filename).3s:%(funcName).3s:%(lineno)3d]:%(message)s', datefmt='%m-%d %H:%M:%S')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(console_handler)
    return logger


class NTLogger:
    def __init__(self, context, verbose):
        self.context = context
        self.verbose = verbose

    def info(self, msg, **kwargs):
        print('I:%s:%s' % (self.context, msg), flush=True)

    def debug(self, msg, **kwargs):
        if self.verbose:
            print('D:%s:%s' % (self.context, msg), flush=True)

    def error(self, msg, **kwargs):
        print('E:%s:%s' % (self.context, msg), flush=True)

    def warning(self, msg, **kwargs):
        print('W:%s:%s' % (self.context, msg), flush=True)


# for io

DEFAULT_ENCODING = "utf-8"


def _is_ascii(text: Text) -> bool:
    return all(ord(character) < 128 for character in text)


def fix_yaml_loader() -> None:
    """Ensure that any string read by yaml is represented as unicode."""

    def construct_yaml_str(self, node):
        # Override the default string handling function
        # to always return unicode objects
        return self.construct_scalar(node)

    yaml.Loader.add_constructor("tag:yaml.org,2002:str", construct_yaml_str)
    yaml.SafeLoader.add_constructor(
        "tag:yaml.org,2002:str", construct_yaml_str)


def replace_environment_variables() -> None:
    """Enable yaml loader to process the environment variables in the yaml."""
    import re
    import os

    # eg. ${USER_NAME}, ${PASSWORD}
    env_var_pattern = re.compile(r"^(.*)\$\{(.*)\}(.*)$")
    yaml.add_implicit_resolver("!env_var", env_var_pattern)

    def env_var_constructor(loader, node):
        """Process environment variables found in the YAML."""
        value = loader.construct_scalar(node)
        expanded_vars = os.path.expandvars(value)
        if "$" in expanded_vars:
            not_expanded = [w for w in expanded_vars.split() if "$" in w]
            raise ValueError(
                "Error when trying to expand the environment variables"
                " in '{}'. Please make sure to also set these environment"
                " variables: '{}'.".format(value, not_expanded)
            )
        return expanded_vars

    yaml.SafeConstructor.add_constructor("!env_var", env_var_constructor)


def read_yaml(content: Text) -> Union[List[Any], Dict[Text, Any]]:
    """Parses yaml from a text.

     Args:
        content: A text containing yaml content.
    """
    fix_yaml_loader()

    replace_environment_variables()

    yaml_parser = yaml.YAML(typ="safe")
    # yaml_parser.version = YAML_VERSION

    if _is_ascii(content):
        # Required to make sure emojis are correctly parsed
        content = (
            content.encode("utf-8")
            .decode("raw_unicode_escape")
            .encode("utf-16", "surrogatepass")
            .decode("utf-16")
        )

    return yaml_parser.load(content) or {}


def read_file(filename: Union[Text, Path], encoding: Text = DEFAULT_ENCODING) -> Any:
    """Read text from a file."""

    try:
        with open(filename, encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise ValueError(f"File '{filename}' does not exist.")


def read_yaml_file(filename: Text) -> Union[List[Any], Dict[Text, Any]]:
    """Parses a yaml file.

     Args:
        filename: The path to the file which should be read.
    """
    return read_yaml(read_file(filename, DEFAULT_ENCODING))


def pickle_load(filename: Union[Text, Path]) -> Any:
    """Loads an object from a file.

    Args:
        filename: the filename to load the object from

    Returns: the loaded object
    """
    with open(filename, "rb") as f:
        return pickle.load(f)


def read_json_file(filename: Union[Text, Path]) -> Any:
    """Read json from a file."""
    content = read_file(filename)
    try:
        return json.loads(content)
    except ValueError as e:
        raise ValueError(
            "Failed to read json from '{}'. Error: "
            "{}".format(os.path.abspath(filename), e)
        )
