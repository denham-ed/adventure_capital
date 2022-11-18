import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('whereami')

class Capital

def get_city_details():
    """
    Asks for user to guess a capital city.
    Checks the API for a match and, if found, returns that city's infromation AS CLASS?!?!?!
    If not found, returns None.
    """
    worksheet = SHEET.worksheet("capitals")
    city = input("Please guess a capital city: \n")
    cell = worksheet.find(city)
    if cell is not None:
        city_stats = worksheet.row_values(cell.row)
        return city_stats
    else:
        return None


result = get_city_details()
print(result)