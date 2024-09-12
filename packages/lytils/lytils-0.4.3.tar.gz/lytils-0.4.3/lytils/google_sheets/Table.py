from lytils.google_sheets.Columns import Columns
from lytils.google_sheets.SpreadsheetTab import SpreadsheetTab
from lytils.google_sheets.helpers import get_data_range, get_header_range


class Table:
    def __init__(self, tab: SpreadsheetTab, range: str, columns: Columns = None):
        self.__tab = tab
        self.__range = range
        self.__columns = columns

    def setup(self):
        header_range = get_header_range(self.__range)
        data_range = get_data_range(self.__range)
        pass
