import random
import time
from uuid import uuid4
import gspread
from google.oauth2.service_account import Credentials
from geographiclib.geodesic import Geodesic
from rich import print as rprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('adventure_capital')
SCORE_SHEET = SHEET.worksheet("scores")
CAPITALS_SHEET = SHEET.worksheet("capitals")


class Capital:
    """
    Initiates a new instance of a capital city
    """
    def __init__(self, city, country, continent, longitude, latitude):
        self.city = city
        self.country = country
        self.continent = continent
        self.longitute = longitude
        self.latitude = latitude


class Game:
    """
    Initiates an instance of a new game
    """
    def __init__(self, in_progress, user_name, guess_count, total_distance, hint_on):
        self.in_progress = in_progress
        self.user_name = user_name
        self.guess_count = guess_count
        self.total_distance = total_distance
        self.hint_on = hint_on
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
    """
    Takes a style and text value (both strings)
    Prints the text with the colour (either foreground or background)
    corresponding style, from colorama.
    """
    if style == 'warning':
        colour = "[bold red]"
    elif style == 'incorrect_answer':
        colour = "[white on red]"
    elif style == 'correct_answer':
        colour = "[white on green]"
    elif style == "intro":
        colour = "[white on blue]"
    elif style == "prompt":
        colour = "[bold green]"
    rprint(f"{colour}{text}")


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
    Checks the API for a match
    If found, returns that city's infromation as a list
    If not found, returns None.
    """

    cell = CAPITALS_SHEET.find(city, None, 1)
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
    city_info = CAPITALS_SHEET.row_values(row_num)
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
    Generates a random number which is used to select a city at random 
    from the API
    Returns the city's details as an instance of a Capital class
    """
    cities_count = len(CAPITALS_SHEET.col_values(1)[1:])
    index = random.randint(1, cities_count)
    city = get_city_info_by_row(index)
    city, country, continent, longitude, latitude = city
    random_city = Capital(city, country, continent, longitude, latitude)
    return random_city


def get_user_name():
    """
    Prompts user to enter their name
    Validates that the name is a string and has a length of more than 0
    Returns the name
    """
    colour_print("prompt", "Firstly, what shall I call you?")
    while True:
        user_name = input("Please enter your name \n")
        if type(user_name) == str and len(user_name) > 0:
                print(f"\nGreat, nice to meet you {user_name}")
                return user_name
        else:
            print('warning', "Sorry! I didn't catch that.")
            continue


def ask_for_hints(user_name):
    """
    Asks user whether they would like to have a hint displayed 
    before their 5th and 10th guess
    Loops until user provides valid input
    Returns True or False
    """
    colour_print("prompt", f"So tell me {user_name}\nWould you like to have hints, if you haven't guessed correctly after 5 and 10 guesses?")
    while True:
        user_hint = input("Write 'y' for yes, and 'n' for no \n")
        if (user_hint.lower() == 'y'):
            print("\nYep, let's have some hints.")
            return True
        if (user_hint.lower() == 'n'):
            print("\nOh wow - no hints for you. Pretty confident eh?")
            return False
        else:
            print('warning', "\nI'm sorry I didn't catch that.")
            continue


def get_ordinal(n):
    # Adapted from : https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712
    """
    Takes a number (n) and returns a string with the number as an ordinal.
    eg. 1 => 1st, 2 => 2nd
    """
    ordinal = "%d%s" % (n, "tsnrhtdd"[(n//10 % 10 != 1) * (n % 10 < 4) * n % 10::4])
    return ordinal


def get_user_guess(user_name, guess_count,game):
    """
    Prompt's user to make a guess
    Checks that the city appears in the database
    If yes, returns the city as an instance of the Capital class
    If no, prompts the user to make another guess until there is a match
    """
    colour_print("prompt", f"\nOk {user_name}. Time to make your {get_ordinal(guess_count)} guess!")
    while True:
        initial_guess = input("Please enter a capital city \n")
        validated_guess = get_city_by_name(initial_guess.lower())
        if validated_guess is not None:
            city, country, continent,longitude, latitude = validated_guess
            user_capital = Capital(city,country,continent,longitude,latitude)
            return user_capital
        else: 
            colour_print("warning", "\nSorry! I don't think that's a capital city!")
            colour_print("warning", "I only hide in capitals...")
            print("\nPlease have another guess")
            continue




def show_hints(guess_count, opponent_capital):
    """
    Checks if the user has made exactly 5 or 10 guesses.
    If yes, prints a hint about the location of the opponent
    If no, passes
    """
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


def post_high_score(user_name, guess_count, total_distance, game_id):
    """
    Appends a list of values to the API
    New row contains the user's name, total guesses, 
    cumulative distance and game id.
    """
    SCORE_SHEET.append_row([user_name, guess_count, total_distance, game_id])


def get_all_scores():
    """
    Add docstring here
    """
    #FINISH THIS!
    scores = SCORE_SHEET.get_all_records()
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
    """
    Finds player's score in relation to all scores
    Returns a string indicating the player's percentile
    """
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
            print("warning","\nI'm sorry I didn't catch that.")
            continue


def play_game(game):
    """
    Initates loop - prompts user to make a guess
    If the user guesses correctly, calls end game function
    If the user is incorrect, they are advised of the direction and distance
    to the correct city.
    """
    print("Ok, let's start!") 
    opponent_capital = get_random_city()
    print(opponent_capital.city) #COMMENT OUT!
    while game.in_progress:

        user_capital = get_user_guess(game.user_name, game.guess_count,game)                
        if user_capital.city == opponent_capital.city:
            game.in_progress = False
            post_high_score(game.user_name, game.guess_count, game.total_distance, str(game.game_id))
            all_scores = get_all_scores()
            colour_print("correct_answer", "\nWell done! You found me!")
            colour_print("correct_answer", f"I was hiding in {opponent_capital.city.title()}!\n")
            time.sleep(1)
            print(f"You took a total of {game.guess_count} guess(es) and a cumulative distance of {game.total_distance}km!")
            time.sleep(1)
            user_ranking = get_user_ranking(str(game.game_id), all_scores)
            print(user_ranking)
            show_high_scores(all_scores)
            # Check Whether User Will Play Again
            play_again = check_play_again()
            if play_again:
                print("Great! I'll start thinking of another city...")
                new_game = Game(True, game.user_name, 1, 0, game.hint_on)
                play_game(new_game)
            else:
                colour_print("intro", "\nNo problem! See you again soon!\n")
        
        else:
            colour_print("incorrect_answer", f"\nNope! I'm not in {user_capital.city.title()}!")
            inverse = game.find_distance_between_capitals(user_capital, opponent_capital)
            # Increment counters
            game.guess_count = game.guess_count + 1
            game.total_distance = game.total_distance + int(inverse['dist'])
            # Show user distance and direction
            print(f"\n{user_capital.city.title()} is {int(inverse['dist'])} kilometres from where I am hiding!")
            bearing = get_text_bearing(inverse['azimuth'])
            print(f"You'll need to head {bearing} to find me...")
            # Check for hints
            if game.hint_on:
                show_hints(game.guess_count, opponent_capital)
            continue

def prepare_game():
    """
    Calls preparatory functions (get user name and hints)
    Returns information in a dictionary
    """
    user_name = get_user_name().capitalize()
    hints = ask_for_hints(user_name)
    return {
        "user_name":user_name,
        "hints":hints
    }

def main():
    """
    Displays intro text and offers instructions
    Calls preparatory game functions
    Calls game function
    """
    colour_print("intro","Welcome to Adventure Capital! \n")
    colour_print('intro', logo)
    print("I'm hiding in a capital city, somewhere in the world")
    print("You have to guess where! \n")
    prepared_game = prepare_game()
    game = Game(True, prepared_game["user_name"], 1, 0, prepared_game["hints"])
    play_game(game)
                
main()




