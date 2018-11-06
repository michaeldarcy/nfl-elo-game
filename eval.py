from util import *
from forecast import *

# Read historical games from CSV
games = Util.read_games("data/AT_games.csv")

# Forecast every game
teams = Forecast.forecast(games)

# Evaluate our forecasts against Elo
#Util.evaluate_forecasts(games)

elos = []
for team in teams:
    elos.append((teams[team]['name'], int(teams[team]['elo']), teams[team]['season']))
    sorted_elos = sorted(elos, key = lambda x:x[1])
for item in sorted_elos:
    print(item)
