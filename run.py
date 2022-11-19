import gspread
import random
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

class Capital:
    """ 
    Initiates a new instance of a capital city
    """ 
    def __init__(self, city, country, continent, easy, longitude, latitude, hint):
        self.city = city
        self.country = country
        self.continent = continent
        self.easy = easy
        self.longitute = longitude
        self.latitude = latitude
        self.hint = hint

class Game:
    """ 
    Initiates an instance of a new game
    """
    def __init__(self, inProgress, userName, guessCount, difficulty , hintOn):
        self.inProgress = inProgress
        self.userName = userName
        self.guessCount = guessCount
        self.difficulty = difficulty
        self.hintOn = hintOn
    
    def findDistanceBetweenCapitals(self, userCapital,opponentCapital):
        return "Oh man, that's so far away,"

def get_city_by_name(city):
    """
    Asks for user to guess a capital city.
    Checks the API for a match and, if found, returns that city's infromation AS CLASS?!?!?!
    If not found, returns None.
    """
    capitals_sheet = SHEET.worksheet("capitals")
    # city = input("Please guess a capital city: \n")
    cell = capitals_sheet.find(city)
    if cell is not None:
        city_stats = capitals_sheet.row_values(cell.row)
        return city_stats
    else:
        return None

def get_city_by_row(row_num):
    """
    Takes an index or row number and returns city from API from that row
    Returns information as a list.!?!?!
    """
    capitals_sheet = SHEET.worksheet("capitals")
    city_keys = capitals_sheet.row_values(1)
    city_values = capitals_sheet.row_values(row_num)
    city_info = dict(zip(city_keys,city_values))
    return city_info




# result = get_city_details()
# city, country, continent, easy,longitude, latitude, hint = result
# userGuess = Capital(city, country, continent, easy,longitude, latitude, hint)
# print(userGuess.hint)

def ask_for_hints(userName):
    """
    Asks user whether they would like to have a hint displayed before their guess
    Loops until user provides valid input
    Returns True or False
    """
    userHint = input(f"So tell me {userName}, would you like to have a hint when you make your guess? Write 'y' for yes, and 'n' for no \n")
    while True:
            if (userHint == 'y'):
                return True
            if (userHint == 'n'):
                return False
            else:
                print("I'm sorry I didn't catch that. Please only write 'y' for yes or 'n' for no")
                continue

def get_random_city():
    """
    Generates a random number which is used to select a city at random from the API
    Returns the city's details as a dictionary
    """
    capitals_sheet = SHEET.worksheet("capitals")
    cities_count = len(capitals_sheet.col_values(1)[1:])
    index = random.randint(1,cities_count)
    city = get_city_by_row(index)
    return city




def main():
    """
    Runs game etc.
    """
    print("Welcome to Where Am I Hiding? \n")
    print("I'm hiding in a capital city, somewhere in the world")
    print("You have to guess where! \n")
    userName = input("Firstly, what should I call you? \n")
    print (f"Great, nice to meet you {userName}")
    hints = ask_for_hints(userName)
    print("Ok, let's start!")
    game = Game(True,userName,0,'Normal',hints)
    message = game.findDistanceBetweenCapitals('London','Budapest')
    print(message)
    #Ask user for guess
    #  ∏∏

# main()
random_city1 = get_random_city()
print(random_city1)
random_city2 = get_random_city()
print(random_city2)
random_city3 = get_random_city()
print(random_city3)