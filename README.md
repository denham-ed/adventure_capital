# Adventure Capital
*Adventure Capital* is a geography-based command line game written in Python.
The player is invited to guess which capital city I am hiding; if they are incorrect, I will telll them how far and in which direction they need to go, in order to find me.

This project was build as part the Full Stack Software Development course with Code Institute.
## User Stories

### Game Designer
As a developed and designer for this game, I wanted to create a simple, intuitive yet enjoyable game.
The game should be immediately understandable but provide enough feedback to keep players returning to beat their previous scores, and to challange others.

The language and tone of the game should be distinctive, cheeky and informal throughout to create a sense that the player is in dialogue with the 'hiding' character.

Simple design (colour, spacing and timing) should be used to provide feedback and prompt the user for information, as well as creating a natural 'flow' to the game.


### Game Player
As a user, I want to experience an enjoyable, easy-to-learn game which will improve my lateral thinking and knowledge of the world's capitals.

The game should be complete-able on early attempts but should offer a scalable challenge that will keep me returning. I want the game to keep track of previous attempts so I can challenge myself and other players.

Any prompts or displayed information should be concise and unambiguous.

## Rules of the Game
The game is a dialogue between the player(the user) and the hider (the computer)

1. The player enters their name and decides whether they want hints to assist them
2. The hider hides - they choose a random capital city.
3. The player guesses a capital city.
    - If they are correct, they win the game.
    - If they are incorrect, the hider will them how far away they are and what direction they need to travel. The player repeats this step until they find the hider.

## Game Design

### Game Play
The logical flow of the game is essentially two loops as shown in the diagram below.
![Flow Chart of Where Am I Game Play](assets/where_am_i_flow.png)

**This is wrong now - adjust loop!!**

The first outer loop encourages the user remain engaged and play consecutive games. It is worth nothign that the user is prompted to provide their name hint preference again - this is to encourage multiple players sharing one terminal to play, without the need to restart the game manually.

The inner loop represents the guess and response dialogue within the game itself - the user(player) continues to guess until locate the opponent's (hider's) city.
### Class Design
There are two classes used in this game: **Capital** and **Game**. The initial design of these classes is shown below.

**Class**

![Capital Class](assets/capital_class.png)

**Game**

![Game Class](assets/game_class.png)

## Features

### Input Validation

### Hints
To assist with guessing more remote and lesser known capitals, the player can opt to have hints (providing the continent and country of the city) after 5 and 10 unsuccessful guesses

### Logo
The ASCII image of the world map acts as a eye-catching introduction to new players and immediately indicates the subject of the game.

### Colour Print
[Rich](https://rich.readthedocs.io/en/stable/introduction.html#:~:text=Rich%20is%20a%20Python%20library,in%20a%20more%20readable%20way.) is used throughout this project to add colour to key text

### Geodesic Functions
The geodesic functions (determining the distance and bearing) in this programme are handled by the library [GeographicLib](https://geographiclib.sourceforge.io/html/python/code.html#module-geographiclib.geodesic)
The underlying mathematical principles are fascinating, however, and well worth a further explore. A good starting place is [here.](https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/)

### High Score
At the end of a successul game, the player will be shown the top 10 scores of all players. Scores are ranked by number of guesses (the lower the better) and then by the cumulative kilometers of error in the incorrect guesses.

The player will also be given a percentile ranking (eg. *You are better than 60% of all players*). This will add a competitive element for players who do not make the top 10.

## Upcoming Features

### Difficulty Settings

## Testing

### Validation

### User Testing (Table etc)

### Fixed Bugs

**

**Credentials**

Regrettably the service account credentials for the Google Drive API were pushed to GitHub in an early commit. This error was discovered by the developer and confirmed by Google, via email. 

The following steps were taken to ensure that the account was not compromised:
1. A review of activity via the Google Cloud Console
2. All credentials for the compromised service account was revoked. The account deleted.
3. The Google Sheet containig the data was duplicated and renamed, and the original was deleted.
4. A new service account and new credentials were generated for the new sheet.

After following these steps and taking advice from the Code Institute community, I am confident that this account remains secure.

### Unfixed Bugs

## Deployment

## Credits

### Libraries

### Code

### Acknowledgements
