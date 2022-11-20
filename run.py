import gspread
import random
from google.oauth2.service_account import Credentials
from math import radians, cos, sin, asin, sqrt


def get_ordinal(n):
    # Adapted from : https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712
    """
    COMMENT COMMENT
    """
    ordinal = "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    return ordinal


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
    def __init__(self, city, country, continent, easy, longitude, latitude):
        self.city = city
        self.country = country
        self.continent = continent
        self.easy = easy
        self.longitute = longitude
        self.latitude = latitude

class Game:
    """ 
    Initiates an instance of a new game
    """
    def __init__(self, inProgress, user_name, guess_count, difficulty , hintOn):
        self.inProgress = inProgress
        self.user_name = user_name
        self.guess_count = guess_count
        self.difficulty = difficulty
        self.hintOn = hintOn
    
    def find_distance_between_capitals(self, user_capital,opponent_capital):
        # https://www.geeksforgeeks.org/program-distance-two-points-earth/
        # The math module contains a function named
        # radians which converts from degrees to radians.
        lon1 = radians(float(opponent_capital.longitute))
        lon2 = radians(float(user_capital.longitute))
        lat1 = radians(float(opponent_capital.latitude))
        lat2 = radians(float(user_capital.latitude))
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))

        # Radius of earth in kilometers. Use 3956 for miles
        r = 3956
        
        # calculate the result
        return(c * r)


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

def get_city_info_by_row(row_num):
    """
    Takes an index or row number and returns city from API from that row
    Returns city information as a list of values
    """
    capitals_sheet = SHEET.worksheet("capitals")
    city_info = capitals_sheet.row_values(row_num)
    return city_info




# result = get_city_details()
# city, country, continent, easy,longitude, latitude, hint = result
# userGuess = Capital(city, country, continent, easy,longitude, latitude, hint)
# print(userGuess.hint)

def ask_for_hints(user_name):
    """
    Asks user whether they would like to have a hint displayed before their guess
    Loops until user provides valid input
    Returns True or False
    """
    user_hint = input(f"So tell me {user_name}, would you like to have a hint if you haven't guessed correctly after 5 guesses? Write 'y' for yes, and 'n' for no \n")
    while True:
            if (user_hint == 'y'):
                return True
            if (user_hint == 'n'):
                return False
            else:
                print("I'm sorry I didn't catch that. Please only write 'y' for yes or 'n' for no")
                continue
            

def get_random_city():
    """
    Generates a random number which is used to select a city at random from the API
    Returns the city's details as an instance of a Capital class
    """
    capitals_sheet = SHEET.worksheet("capitals")
    cities_count = len(capitals_sheet.col_values(1)[1:])
    index = random.randint(1,cities_count)
    city = get_city_info_by_row(index)
    city, country, continent, easy,longitude, latitude = city
    random_city = Capital(city, country, continent, easy,longitude, latitude)
    return random_city
    


def get_user_guess(user_name, guess_count):
    print(f"Ok {user_name}. Time to make your {get_ordinal(guess_count)} guess!")
    while True:
        initial_guess = input("Please enter a capital city \n")
        validated_guess = get_city_by_name(initial_guess)
        if validated_guess is not None:
            city, country, continent, easy,longitude, latitude = validated_guess
            user_capital = Capital(city,country,continent,easy,longitude,latitude)
            return user_capital
        else: 
            print("Sorry! I don't think that's a capital city!")
            print("I only hide in capitals...")
            print("Please have another gues")
            continue

def post_high_score(user_name, guess_count):
    score_sheet = SHEET.worksheet("scores")
    score_sheet.append_row([user_name,guess_count])



def main():
    """
    Runs game etc.
    """
    print("Welcome to Where Am I Hiding? \n")
    print("I'm hiding in a capital city, somewhere in the world")
    print("You have to guess where! \n")
    user_name = input("Firstly, what should I call you? \n")
    print (f"Great, nice to meet you {user_name}")
    hints = ask_for_hints(user_name)
    print("Ok, let's start!") 
    opponent_capital = get_random_city()
    print(opponent_capital.city)
    game = Game(True,user_name,1,'Normal',hints)

    while game.inProgress:
        user_capital = get_user_guess(user_name, game.guess_count)
        # Check for Hints
        if game.hintOn and game.guess_count == 5:
            print ("Not to worry - this is a hard one! Your first hint...\n")
            print (f"I'm hiding somewhere in the continent of {opponent_capital.continent}!")
        if game.hintOn and game.guess_count == 8:
            print ("OK, you're struggling - your second hint, coming up...\n")
            print (f"I'm hiding somewhere in the capital ciry of {opponent_capital.country}!")
                
        if user_capital.city == opponent_capital.city:

 
            game.inProgress = False
            print("You found me!")
            print (f"I was hiding in {opponent_capital.city}! \n")
            post_high_score(user_name, game.guess_count)
        else:
            game.guess_count = game.guess_count + 1
            print("You are wrong, loser.")
            distance = game.find_distance_between_capitals(user_capital,opponent_capital)
            message = f"{user_capital.city} is {int(distance)} miles from where I am hiding! Try again!"
            print(message)
            continue
                


main()


