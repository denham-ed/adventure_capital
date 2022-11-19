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

main()