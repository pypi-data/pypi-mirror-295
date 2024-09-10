import gspread as gs
from .SpreadsheetTab import SpreadsheetTab


class Spreadsheet:
    def __init__(self, sheet: gs.Spreadsheet):
        self.__sheet = sheet

    def get_tab(self, name: str) -> SpreadsheetTab:
        tab = self.__sheet.worksheet(name)
        return SpreadsheetTab(tab=tab)
