![alt text](https://ppg.ellegirl.ru/img/section-one-mob-decor-intro.png)

# Powerpuff-girls

### Bot for the server game "World of Tanks: Strategy"

***Brief description of the game:***
<br>
A server game in the strategy genre.
3 players (or bots) fight on a hexagonal map using their own equipment (tanks). Each player has 5 tanks of different types with individual behaviors and characteristics. The goal of the game is to capture the central base or destroy the largest number of enemy vehicles.
<br>
<br>
***Brief description of the bot:***
<br>
AI is based on Utility AI system. The key to decision making is to calculate a utility score for every action the AI agent can take and then choose the action with the highest score.
***
***Installation:***
<br>
First you have to download this repository.
Now go to the root folder of the project and run the following command:
<br>
```
pip install -r requirements.txt
```
***
***how to launch***
<br>
Run the command in the root folder of the project without arguments to run a test game with 3 players controlled by one bot:

```
python main.py
```

Run the command in the root folder of the project with optional arguments to run a test game with 1 players:

```
python main.py -n [player name] -p [password] -g [game name] -np [number of players] -nt [number of turns] -obs [0/1 is observer]
```
##### competitive game mode (1 player): #####
***
***Our team:***
<br>
[Vyachaslau Sitkin](https://github.com/HardCrabS)
<br>
[Maksim Ganusevich](https://github.com/maksim-ganusevich)
<br>
[Andrei Yatsushkevuich](https://github.com/nutakoooye)
***
*This game bot is written as a coursework for the WG Forge educational project.*

