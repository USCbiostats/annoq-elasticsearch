import argparse
from enum import Enum
import json
from os.path import isdir, isfile
import pickle


class TableAggType(Enum):
    ANNOTATION = 'annotation'


def file_path(path):
    """
    Checks if a is valid 
    """
    print(path)
    if isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f"{path} is not a valid path")

def dir_path(path):
    if isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f"{path} is not a valid directory")

def load_json(filepath):
    with open(filepath) as f:
        return json.load(f)


def load_pickle(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)


def write_to_json(data, output_file, indent=None):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=indent)
