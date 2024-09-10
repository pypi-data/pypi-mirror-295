# Third-party Libraries
import gspread as gs

# Local Libraries
from lytils.google_sheets.Spreadsheet import Spreadsheet


# src: https://practicaldatascience.co.uk/data-science/how-to-read-google-sheets-data-in-pandas-with-gspread
class GoogleSheets:
    """
    Creates a GoogleSheets object that allows for interfacing with the Google Sheets API.
    Using this GoogleSheets object, you can access any sheet by its URL, assuming the service account has permissions.

    Rough steps to get started:
    1. Create a Google Cloud Platform project
    2. Enable the Google Sheets API
    3. Create a service account and add a JSON key to it
    4. Download the JSON key and move it to your project directory
    5. Share any desired sheet with the service account email
    6. Initialize a GoogleSheets object with the path to the service account JSON
    7. Plug the desire sheet url into the get_sheet method
    """

    def __init__(self, service_account: str):
        # Authenticate with Google Sheets
        self.__service_account = gs.service_account(filename=service_account)

    def get_sheet(self, url) -> Spreadsheet:
        sheet = self.__service_account.open_by_url(url)
        return Spreadsheet(sheet=sheet)
