import gspread
import random
from uuid import uuid4
from google.oauth2.service_account import Credentials
from math import radians, cos, sin, asin, sqrt
from pprint import pprint
from geographiclib.geodesic import Geodesic
import time
from colorama import init, Fore, Back

#  Resets Default Colour Scheme
init(autoreset=True)

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
    def __init__(self, inProgress, user_name, guess_count, total_distance, difficulty, hintOn):
        self.inProgress = inProgress
        self.user_name = user_name
        self.guess_count = guess_count
        self.total_distance = total_distance
        self.difficulty = difficulty
        self.hintOn = hintOn
        self.game_id = uuid4()

    def find_distance_between_capitals(self, user_capital, opponent_capital):
        """
        Calculates distance and bearing between two coordinate points.
        Uses World Geodetic System 1984 (WGS84).
        Returns a dictionary with the
        azimuth (initial bearing) and distance (in kilometres).
        """
        geod = Geodesic.WGS84
        lon2 = float(opponent_capital.longitute)
        lon1 = float(user_capital.longitute)
        lat2 = float(opponent_capital.latitude)
        lat1 = float(user_capital.latitude)
        g = geod.Inverse(lat1, lon1, lat2, lon2)
        inverse = {
            "dist": g["s12"]/1000,
            "azimuth": g["azi1"]
        }

        return inverse

def colour_print(style, text):
    if style == 'warning':
        colour = Fore.RED
    elif style == 'incorrect_answer':
        colour = Back.RED
    elif style == 'correct_answer':
        colour = Back.GREEN
    elif style == "intro":
        colour = Back.BLUE
    elif style == "prompt":
        colour = Fore.GREEN
    
    print(f"{colour}{text}")


logo = """. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . .#######. . . . . . . . . . . . . . . . . .
. . . . . . . .#. .#### . . . ####. . .###############. . .
. . . ########. ##. ##. . . ######################### . . .
. . . . ##########. . . . ######################. . . . . .
. . . . .######## . . . .   ################### . . . . . .
. . . . . ### .   . . . .#####. ##############. # . . . . .
. . . . . . ##### . . . .#######. ##########. . . . . . . .
. . . . . . .###### . . . .#### . . . . .## . . . . . . . .
. . . . . . . ##### . . . .#### # . . . . . ##### . . . . .
. . . . . . . ### . . . . . ##. . . . . . . . ### .#. . . .
. . . . . . . ##. . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."""


def get_city_by_name(city):
    """
    Asks for user to guess a capital city.
    Checks the API for a match and, if found, returns that city's infromation AS CLASS?!?!?!
    If not found, returns None.
    """
    capitals_sheet = SHEET.worksheet("capitals")
    # city = input("Please guess a capital city: \n")
    cell = capitals_sheet.find(city, None, 1)
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


def get_text_bearing(azimuth):
    """
    Converts azimut (initial bearing in degrees)
    Returns a compass point direction as a string
    """
    # Handles negative azimuths
    if (azimuth < 0):
        azimuth = azimuth + 360
    # Returns string depending on azimuth value
    if 11.25 <= azimuth < 33.75:
        return "North North East"
    elif 33.75 <= azimuth < 56.25:
        return "North East"
    elif 56.25 <= azimuth < 78.75:
        return "East North East"
    elif 78.75 <= azimuth < 101.25:
        return "East"
    elif 101.25 <= azimuth < 123.75:
        return "East South East"
    elif 123.75 <= azimuth < 146.75:
        return "South East"
    elif 146.25 <= azimuth < 168.75:
        return "South South East"
    elif 168.75 <= azimuth < 191.75:
        return "South"
    elif 191.25 <= azimuth < 213.75:
        return "South South West"
    elif 213.75 <= azimuth < 236.25:
        return "South West"
    elif 236.25 <= azimuth < 258.75:
        return "West South West"
    elif 258.75 <= azimuth < 281.25:
        return "West"
    elif 281.25 <= azimuth < 303.75:
        return "West North West"
    elif 303.75 <= azimuth < 326.25:
        return "North West"
    elif 326.25 <= azimuth < 348.75:
        return "North North West"
    else:
        return ("North")


def get_random_city():
    """
    Generates a random number which is used to select a city at random from the API
    Returns the city's details as an instance of a Capital class
    """
    capitals_sheet = SHEET.worksheet("capitals")
    cities_count = len(capitals_sheet.col_values(1)[1:])
    index = random.randint(1, cities_count)
    city = get_city_info_by_row(index)
    city, country, continent, easy, longitude, latitude = city
    random_city = Capital(city, country, continent, easy, longitude, latitude)
    return random_city


def get_user_name():
    colour_print("prompt", "Firstly, what shall I call you?")
    while True:
        user_name = input("Please enter your name \n")
        if type(user_name) == str and len(user_name) > 0:
                print (f"\nGreat, nice to meet you {user_name}")
                return user_name
        else:
            colour_print('warning', "Sorry! I didn't catch that.")
            continue


def ask_for_hints(user_name):
    """
    Asks user whether they would like to have a hint displayed before their guess
    Loops until user provides valid input
    Returns True or False
    """
    colour_print("prompt",f"So tell me {user_name}, would you like to have a hint if you haven't guessed correctly after 5 guesses?")
    while True:
        user_hint = input("Write 'y' for yes, and 'n' for no \n")
        if (user_hint.lower() == 'y'):
            print("\nYep, let's have some hints.")
            return True
        if (user_hint.lower() == 'n'):
            print("\nOh wow - no hints for you. Pretty confident eh?")
            return False
        else:
            colour_print('warning', "\nI'm sorry I didn't catch that.")
            continue


def get_ordinal(n):
    # Adapted from : https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712
    """
    COMMENT COMMENT
    """
    ordinal = "%d%s" % (n, "tsnrhtdd"[(n//10 % 10 != 1) * (n % 10 < 4) * n % 10::4])
    return ordinal


def get_user_guess(user_name, guess_count):
    colour_print("prompt", f"\nOk {user_name}. Time to make your {get_ordinal(guess_count)} guess!")
    while True:
        initial_guess = input("Please enter a capital city \n")
        validated_guess = get_city_by_name(initial_guess.lower())
        if validated_guess is not None:
            city, country, continent, easy,longitude, latitude = validated_guess
            user_capital = Capital(city,country,continent,easy,longitude,latitude)
            return user_capital
        else: 
            colour_print("warning", "\nSorry! I don't think that's a capital city!")
            colour_print("warning", "I only hide in capitals...")
            print("\nPlease have another guess")
            continue


def show_hints(guess_count, opponent_capital):
    if guess_count == 5:
        time.sleep(1)
        print ("\nNot to worry - this is a hard one! Your first hint...\n")
        time.sleep(1)
        print (f"I'm hiding somewhere in the continent of {opponent_capital.continent}!")
    elif guess_count == 10:
        time.sleep(1)
        print ("\nOK, you're struggling - your second hint, coming up...\n")
        time.sleep(1)
        print (f"I'm hiding somewhere in the capital city of {opponent_capital.country}!")
        print("Have another try...")
    else:
        pass


def post_high_score(user_name, guess_count,total_distance,game_id):
    """ 
    Add docstring here!
    """
    score_sheet = SHEET.worksheet("scores")
    score_sheet.append_row([user_name, guess_count, total_distance, game_id])


def get_all_scores():
    """ 
    Add docstring here
    """
    score_sheet = SHEET.worksheet("scores")
    scores = score_sheet.get_all_records()
    sorted_scores = sorted(scores, key=lambda d: (d['score'],d['distance']))
    return sorted_scores


def show_high_scores(all_scores):
    """ 
    Loops through the first ten scores and prints a statement to user.
    Statement shows name, number of guesses and total kilometers
    """
    print ('The top 10 players are:')
    for index, score in enumerate(all_scores):
        if index > 9:
            break
        print (f"{index +1}: {score['user_name']} - {score['score']} guesses - {score['distance']} total kilometres" )


def get_user_ranking(game_id, all_scores):
    player_game_index = next((i for i, score in enumerate(all_scores) if score['game_id']==str(game_id)), None)
    player_percentile = int(100 - (player_game_index / len(all_scores)) * 100)
    return f"You are better than {player_percentile}% of all players! \n"


def check_play_again():
    """
    Checks whether user wants to play again
    Returns true of false
    """
    colour_print("prompt","\nWould you like to play again?")
    while True:
        play_again = input("Enter 'y' for yes, or 'n' for no.\n")    
        if play_again.lower() == 'y':
            return True
        elif play_again.lower() == 'n':
            return False
        else:
            colour_print("warning","\nI'm sorry I didn't catch that.")
            continue


def main():
    """
    Runs game etc.
    """
    colour_print('intro', "Welcome to Where Am I Hiding? \n")
    colour_print('intro', logo)
    print("I'm hiding in a capital city, somewhere in the world")
    print("You have to guess where! \n")
    user_name = get_user_name().capitalize()
    hints = ask_for_hints(user_name)
    print("Ok, let's start!") 
    opponent_capital = get_random_city()
    print(opponent_capital.city)
    game = Game(True,user_name,1,0,'Normal',hints)

    while game.inProgress:
        user_capital = get_user_guess(user_name, game.guess_count)                
        if user_capital.city == opponent_capital.city:
            game.inProgress = False
            post_high_score(user_name, game.guess_count, game.total_distance, str(game.game_id))
            all_scores = get_all_scores()
            colour_print("correct_answer", "\nWell done! You found me!")
            colour_print("correct_answer", f"I was hiding in {opponent_capital.city.title()}!\n")
            time.sleep(1)
            print(f"You took a total of {game.guess_count} guess(es) and a cumulative distance of {game.total_distance}km!")
            time.sleep(1)
            user_ranking = get_user_ranking(str(game.game_id), all_scores)
            print(user_ranking)
            show_high_scores(all_scores)
            #Check Whether User Will Play Again
            play_again = check_play_again()
            if play_again:
                print("Great! I'll start thinking of another city...")
                main()
            else:
                print ("\nNo problem! See you again soon!\n")
     
        else:
            colour_print("incorrect_answer", f"\nNope! I'm not in {user_capital.city.title()}!")
            inverse = game.find_distance_between_capitals(user_capital,opponent_capital)
            # Increment counters
            game.guess_count = game.guess_count + 1
            game.total_distance = game.total_distance + int(inverse['dist'])
            # Show user distance and direction
            print(f"\n{user_capital.city.title()} is {int(inverse['dist'])} kilometres from where I am hiding!")
            bearing = get_text_bearing(inverse['azimuth'])
            print(f"You'll need to head {bearing} to find me...")
            # Check for Hints
            if game.hintOn:
                show_hints(game.guess_count, opponent_capital)
            continue
                


main()




