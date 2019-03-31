from os import makedirs
from os.path import join, exists, isdir, isfile
from typing import Any

from definitions import CLASSIFIERS_PATH, REGEX_PATH
import jsonpickle
from pandas import DataFrame, read_csv


def is_directory(path: str) -> bool:
    return isdir(path)


def is_file(path: str) -> bool:
    return isfile(path)


def create_directory_if_not_exists(path: str) -> None:
    if not exists(path):
        makedirs(path)
    elif is_file(path):
        raise BlockingIOError("Expected path, got file: " + path)


def prepare_storage_get_full_path(path: str, filename: str) -> str:
    """
    Prepares a folder for the specified classifier and returns its path
    :param path: The path of the file
    :param filename: The name of the file
    :return: The full path to the file
    """
    create_directory_if_not_exists(path)
    return join(path, filename)


def prepare_read_get_full_path(path: str, filename: str) -> str:
    """
    Prepares a folder for the specified classifier and returns its path
    :param path: The path of the file
    :param filename: The name of the file
    :return: The full path to the file
    """
    file_path = join(path, filename)
    if not isfile(file_path):
        raise IOError(f"No such file: {file_path}")
    return file_path


def store_dataframe(dataframe: DataFrame, path: str, filename: str):
    output_path = prepare_storage_get_full_path(path, filename)
    dataframe.to_csv(output_path, index=True, index_label="id")


def load_dataframe(path: str, filename: str) -> DataFrame:
    read_path = prepare_read_get_full_path(path, filename)
    return read_csv(read_path, index_col=0)


def load_regex(regex_file_name: str) -> str:
    file_path = prepare_read_get_full_path(REGEX_PATH, regex_file_name)
    with open(file=file_path, mode='r', encoding='utf-8-sig') as file:
        return file.read()


def store_serializable_object(serializable_object: Any, path: str, filename: str):
    output_path = prepare_storage_get_full_path(path, filename)
    json_object = jsonpickle.encode(serializable_object)
    with open(output_path, 'w') as my_file:
        my_file.write(json_object)


def load_serializable_object(path: str, filename: str) -> Any:
    read_path = prepare_read_get_full_path(path, filename)
    with open(read_path, 'r') as my_file:
        raw_text = my_file.read()
    return jsonpickle.decode(raw_text)


def store_figure(figure: Any, path: str, filename: str):
    output_path = prepare_storage_get_full_path(path, filename)
    figure.savefig(output_path)
