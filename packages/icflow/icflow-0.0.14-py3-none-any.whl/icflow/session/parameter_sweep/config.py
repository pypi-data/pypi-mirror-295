"""
This module is for a parameter sweep config file
"""

from pathlib import Path
import logging
import itertools

from iccore.serialization import read_yaml, Serializable

from icflow.utils.dict_utils import merge_dicts, split_dict_on_type

logger = logging.getLogger(__name__)


class ParameterSweepConfig(Serializable):

    """
    This class handles reading a parameter sweep config file and
    also expansion of parameter ranges in lists
    """

    def __init__(self) -> None:
        self.stop_on_error: bool = False
        self.title: str = ""
        self.program: str = ""
        self.parameters: dict = {}
        self.tasks: dict = {}

    def serialize(self) -> dict:
        return {
            "stop_on_error": self.stop_on_error,
            "title": self.title,
            "program": self.program,
            "parameters": self.parameters,
            "tasks": self.tasks,
        }

    def deserialize(self, content: dict):
        if "title" in content:
            self.title = content["title"]
        if "program" in content:
            self.program = content["program"]
        if "stop_on_error" in content:
            self.stop_on_error = content["stop_on_error"]
        if "parameters" in content:
            self.parameters = content["parameters"]
        if "tasks" in content:
            self.tasks = content["tasks"]

    def read(self, path: Path):

        """
        Read the config from file
        """

        logger.info("Reading config from: %s", path)
        self.deserialize(read_yaml(path))

    def get_expanded_parameters(self) -> list:
        """
        Produce a list of dictionaries from a single dictionary containing list values.
        Each dictionary in this list is a unique permutation from the list entries of
        the original dictionary.
        """
        no_lists, with_lists = split_dict_on_type(self.parameters, list)
        items = []
        list_keys, values = zip(*with_lists.items())
        permutations = itertools.product(*values)
        for perm in permutations:
            perm_dict = dict(zip(list_keys, perm))
            item = merge_dicts(perm_dict, no_lists)
            items.append(item)
        return items
