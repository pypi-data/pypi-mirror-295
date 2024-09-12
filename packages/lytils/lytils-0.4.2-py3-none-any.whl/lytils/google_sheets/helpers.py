import pandas as pd
from lytils.regex import match, replace


def convert_accounting_to_numeric(column: pd.Series):
    def transform_column(text: str) -> float:
        text = replace(r"[\$,-]", "", text).strip()
        return float(text) if text != "" else 0

    return column.apply(transform_column)


def get_column_letter(column_number):
    """
    Get column letter given column number.
    1 = A, 2 = B, ...,  27 = AA, 28 = AB, etc
    """
    dividend = column_number
    letter = ""
    while dividend > 0:
        remainder = (dividend - 1) % 26
        letter = chr(65 + remainder) + letter
        dividend = (dividend - remainder) // 26
    return letter


def get_column_number(column_letter):
    """
    Get column number given column letter.
    A = 1, B = 2, ...,  AA = 27, AB = 28, etc
    """
    number = 0
    for char in column_letter:
        number = number * 26 + (ord(char) - ord("A") + 1)
    return number


def get_header_range(range: str):
    """
    Get header range (first row) given a range in a1 notation
    """
    first_column = match(r"[A-Z]+", range, group=1)
    last_column = match(r"[A-Z]+", range, group=2)
    first_row = match(r"[0-9]+", range, group=1)

    return f"{first_column}{first_row}:{last_column}{first_row}"


# Get data range from a range in a1 notation
def get_data_range(range: str):
    """
    Get data range (everything except first row) given a range in a1 notation
    """
    first_column = match(r"[A-Z]+", range, group=1)
    first_row = match(r"[0-9]+", range, group=1)
    last_column = match(r"[A-Z]+", range, group=2)
    last_row = match(r"[0-9]+", range, group=2)

    # Increment first row by 1
    return f"{first_column}{int(first_row) + 1}:{last_column}{last_row}"
