import csv
import json
import os

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


def get_last_id_in_csv_file(file_name, column="id"):
    with open(file_name, "r") as file:
        reader = csv.DictReader(file)

        # Iterate over each row in the CSV file
        for row in reader:
            # Assign the last row to the last_row variable
            last_row = row

        try:
            # Get the value you want from the last row by column name
            desired_value = last_row[column]

            return int(desired_value)
        except:
            return -1


def load_json_from_file(path):
    """
    Load json object from file.
    """
    with open(path, "r") as file:
        return json.load(file)


def create_file_at_path(path: str):
    """
    Creates a blank file at path.
    """
    # Split path into directory and filename
    directory, _ = os.path.split(path)

    # If directory was included, create it if it doesn't exist
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    open(path, "w").close()  # Create file


def write_to_file(path: str, text: str, encoding: str = "utf-8"):
    """
    Write text to file at path.
    """
    create_file_at_path(path)

    with open(path, "w", encoding=encoding) as file:
        file.write(f"{text}")


def write_html_to_file(path: str, html, encoding: str = "utf-8"):
    """
    Write html to file.
    """
    create_file_at_path(path)

    soup = BeautifulSoup(html, "html.parser")
    formatted_html = soup.prettify()
    with open(path, "w", encoding=encoding) as file:
        file.write(formatted_html)


def write_json_to_file(path: str, data, encoding: str = "utf-8", indent: int = 4):
    """
    Write json object to file.
    """
    create_file_at_path(path)

    with open(path, "w", encoding=encoding) as file:
        json.dump(data, file, indent=indent)


class LyFile:
    def __init__(self, path: str = "LyFile/file.txt"):
        self._path = path

    def exists(self):
        return os.path.exists(self._path)

    def create(self):
        create_file_at_path(self._path)

    def append(self, text: str, encoding: str = "utf-8"):
        """
        Appends text to file at path.
        """
        with open(self._path, "a", encoding=encoding) as file:
            file.write(f"{text}\n")

    def append_json(self, data: dict, encoding: str = "utf-8", indent: int = 4):
        """
        Appends json data to file at path.
        """
        with open(self._path, "a", encoding=encoding) as file:
            json.dump(data, file, indent=indent)
            file.write("\n")
