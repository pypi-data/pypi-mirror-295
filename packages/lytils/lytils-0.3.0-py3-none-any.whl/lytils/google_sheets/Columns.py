# Third-party libraries
from gspread_formatting import CellFormat

# Local libraries
from lytils.file import write_to_file
from .format import DefaultFormat


class Column:
    """
    Used for defining columns and how they're to be formatted.

    Args:
        id (str): The unique identifier for the column. Should be snake_case.
        header (str): The header text for the column.
        format (CellFormat, optional): The format to apply to the column. Defaults to DefaultFormat().
        width (int, optional): The width of the column. Defaults to 100.
    """

    def __init__(
        self,
        id: str,
        header: str,
        format: CellFormat = DefaultFormat(),
        width: int = 100,
    ):
        self.__id = id
        self.__header = header
        self.__format = format
        self.__width = width

    def get_id(self):
        return self.__id

    def get_header(self):
        return self.__header

    def get_format(self):
        return self.__format

    def get_width(self):
        return self.__width


class Columns:
    """
    Used for grouping Column objects.

    Args:
        columns (list): A list of Column objects.
    """

    def __init__(self, columns: list[Column]):
        self.__columns = {column.get_id(): column for column in columns}
        self.__order = [column.get_id() for column in columns]

    def output_item_class(self, output_path: str):
        """
        Generates a Python class definition for a data structure with attributes
        based on the columns specified in `self.__order` and writes it to a file.

        The generated class is a dataclass named `CustomItem` with each column
        in `self.__order` as a string attribute initialized to an empty string.

        Args:
            output_path (str): The file path where the generated class definition
                               will be written.

        Example:
            If `self.__order` is ['id', 'name', 'age'], the generated class will be:

            from dataclasses import dataclass

            @dataclass
            class CustomItem:
                id: str = ""
                name: str = ""
                age: str = ""

        This class definition will be written to the file specified by `output_path`.
        Item values default to an empty string, but can be changed as needed.
        """
        file_str = "from dataclasses import dataclass\n\n"
        file_str = "".join(
            [
                "from dataclasses import dataclass\n",
                "\n",
                "@dataclass\n",
                "class CustomItem:\n",
                *[f'    {column}: str = ""\n' for column in self.__order],
                "\n",
            ]
        )
        write_to_file(output_path, file_str)
