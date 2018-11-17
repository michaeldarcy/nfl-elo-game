from util import *
from forecast import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Read historical games from CSV
games = Util.read_games("data/AT_games.csv")

# Forecast every game
teams, games = Forecast.forecast(games, 150, .2, 500)

def search_params(games):
    games_with_memory = games
    # Evaluate our forecasts against Elo
    #Util.evaluate_forecasts(games)
    for game in games_with_memory:
        game['elo_prob1'] = game['my_prob1']
    params = [[],[]]
    params[0] = np.arange(10,200,10)
    params[1] = np.arange(1, 9, 1)

    params[0], params[1] = np.meshgrid(params[0], params[1])
    Z = np.zeros(params[0].shape)
    for k in range(10,200,10):
        i = 0
        for revert in range (1 , 9 , 1):
            j = 0
            revert = revert/10
            
            for scale in range (100,1000,100):
                print (k, revert, scale)
                teams,games_with_memory = Forecast.forecast(games_with_memory, k, revert, scale)
                my_avg, elo_avg = Util.evaluate_forecasts(games_with_memory)
                
                if my_avg > elo_avg:
                    for game in games_with_memory:
                        game['elo_prob1'] = game['my_prob1']
                    best_k = k
                    best_revert = revert
                    best_scale = scale
                    print (my_avg, k, revert, scale)
                if scale == 100:
                    Z[i,j] = my_avg
                    i = i+1
                    j = j+1


    print('Optimal game weight:', best_k, '  Optimal loss season over season', best_revert, '   Difference needed for 90% win', best_scale)
    teams, games = Forecast.forecast(games, best_k, best_revert, best_scale )

elos = []
for team in teams:
       elos.append((teams[team]['name'], int(teams[team]['elo']), teams[team]['season']))
       sorted_elos = sorted(elos, key = lambda x:x[1])
for item in sorted_elos:
    print(item)

    
