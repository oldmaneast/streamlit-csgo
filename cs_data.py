import pandas as pd
from collections import Counter

host_player = "Old Man East"
html_file = "CSGO_OME.html"

# Split the rounds won and lost data and return the selected side
# as an integer
def split_and_convert(text, position, split_on=' : '):
    t = text.split(split_on)[position]
    return int(t)


# Return a list of the number_to_get amount of players that played with host_player
# The returned result includes the host player and the amount of games played together
def get_friendlies_with_count(data, number_to_get=4, host_player=host_player):
    friendly_players = []
    for x in data:
        # Find if host_player was on team 1 or team 2 via the index. 0-4 == team 1, 6-10 == team 2
        player_number = x['Player Name'].str.find(host_player).idxmax()
        if player_number <= 4:
            for i in range(0,5):
                friendly_players.append(x['Player Name'][i])
        else:
            for i in range(6,11):
                friendly_players.append(x['Player Name'][i])

    return Counter(friendly_players).most_common(number_to_get)


def get_friendlies_list(data, number_to_get=5, host_player=host_player):
    friendly_players = []
    for x in data:
        # Find if host_player was on team 1 or team 2 via the index. 0-4 == team 1, 6-10 == team 2
        player_number = x['Player Name'].str.find(host_player).idxmax()
        if player_number <= 4:
            for i in range(0,5):
                friendly_players.append(x['Player Name'][i])
        else:
            for i in range(6,11):
                friendly_players.append(x['Player Name'][i])

    most_common =  Counter(friendly_players).most_common(number_to_get)
    result_lst = []
    for x in most_common:
        result_lst.append(x[0])
    return result_lst


# Returns the average score for matches involving host_player and player
def get_average_score_with_player(data, player, host_player=host_player):
    average_won_lst = []
    average_lost_lst = []
    for x in data:
        if x['Player Name'].str.contains(player).any():
            player_number = x['Player Name'].str.find(host_player).idxmax()
            if player_number <= 4:
                average_won_lst.append(split_and_convert(x['Player Name'][5], 0))
                average_lost_lst.append(split_and_convert(x['Player Name'][5], 1))
            else:
                average_won_lst.append(split_and_convert(x['Player Name'][5], 1))
                average_lost_lst.append(split_and_convert(x['Player Name'][5], 0))
    print(average_won_lst)
    average_rounds_won = sum(average_won_lst) /len(average_won_lst)
    average_rounds_lost = sum(average_lost_lst)/len(average_lost_lst)

    return [round(average_rounds_won,2), round(average_rounds_lost,2)]


# Returns the average rounds won : rounds lost per match for the host_players
# most common partners as dictated by number_of_players. Result includes host_player
def get_average_for_x_players(data, number_of_players=4, host_player=host_player):
    friendly_lst = get_friendlies_with_count(data, number_of_players, host_player=host_player)
    average_lst = []
    for x in friendly_lst:
        wins_losses = get_average_score_with_player(data, x[0])
        average_lst.append([x[0], wins_losses])
    return average_lst


# Returns a dictionary of win/lose/draw data for the given player
def get_win_lose_draw(data, host_player=host_player):
    win, lose, draw = 0, 0, 0
    for x in data:
        player_number = x['Player Name'].str.find(host_player).idxmax()
        team1 = split_and_convert(x['Player Name'][5], 0)
        team2 = split_and_convert(x['Player Name'][5], 1)

        if team1 == team2:
            draw = draw + 1
        elif team1 > team2:
            if player_number <= 4:
                win = win + 1
            else:
                lose = lose + 1
        else:
            if player_number <= 4:
                lose = lose + 1
            else:
                win = win + 1

    return {'win': win, 'lose': lose, 'draw': draw}


# Returns Win, Loss, Draw for an individual match for given player number
# Return 0 for win, 1 for lose and 2 for draw
def get_single_wld(data, player_number):
    team1 = split_and_convert(data['Player Name'][5], 0)
    team2 = split_and_convert(data['Player Name'][5], 1)
    if team1 == team2:
        return 2
    elif team1 > team2:
        if player_number <= 4:
            return 0
        else:
            return 1
    else:
        if player_number >= 6:
            return 0
        else:
            return 1


# Takes a list of DataFrames and outputs a dictionary of player stats
def get_specific_player_data(data, player):
    matches, k, a, d, mvp, score = 0, 0, 0, 0, 0, 0
    win, lose, draw = 0, 0, 0
    for x in data:
        if x['Player Name'].str.contains(player).any():
            player_number = x['Player Name'].str.find(player).idxmax()
            matches = matches + 1
            k = k + int(x['K'][player_number])
            a = a + int(x['A'][player_number])
            d = d + int(x['D'][player_number])
            mvp = mvp + int(x['★'][player_number])
            score = score + int(x['Score'][player_number])

            wld = get_single_wld(x, player_number)
            if wld == 0:
                win = win + 1
            elif wld == 1:
                lose = lose + 1
            else:
                draw = draw + 1

    return {'Name' : player,'Matches' : matches, 'Kills' : k, 'Assists' : a, 'Deaths': d, 'MVPs' : mvp,
            'Score': score, 'Win' : win, 'Lose' : lose, 'Draw' : draw}


# Generates stats table for kills, deaths, assists and other stats,
# Not sorted except by the order of the list of players it takes as an argument
def generate_player_stats_table(data, list_of_players):
    result_lst = []
    for x in list_of_players:
        result_lst.append(get_specific_player_data(data, x))

    return pd.DataFrame(result_lst)


# Add addition information not calculated by the original data
def add_stats_to_player_stats_table(df):
    df['KD'] = df['Kills']/df['Deaths']
    df['Win PCT'] = (2*df['Win']+df['Draw'])/(2*df['Matches'])*100
    df['Avg. Score'] = df['Score'] / df['Matches']
    return df


# This function is called by the function generate_in_depth_df()
def generate_in_depth_data(data, player):
    k, a, d, mvp, score = [], [], [], [], []
    for x in data:
        if x['Player Name'].str.contains(player).any():
            player_number = x['Player Name'].str.find(player).idxmax()
            k.append(int(x['K'][player_number]))
            a.append(int(x['A'][player_number]))
            d.append(int(x['D'][player_number]))
            mvp.append(int(x['★'][player_number]))
            score.append(int(x['Score'][player_number]))

    return {'Name' : player, 'Kills' : k, 'Assists' : a, 'Deaths': d, 'MVPs' : mvp,
            'Score' : score}


# This will generate a DataFrame of all the individual match stats
# linked to each player, useful for making Boxplot and other charts
def generate_in_depth_df(data, lst_of_players):
    result_lst = []
    for x in lst_of_players:
        result_lst.append(generate_in_depth_data(data, x))

    return pd.DataFrame(result_lst)


# This function sorts the data of detailed_df in order of score
# which should keep a generally well formed boxplots for each stat
def sort_data(df):
    l = []
    for index, row in df.iterrows():
        l.append(sum(row['Score'])/len(row['Score']))
    df['Score Mean'] = l
    df.sort_values(by=['Score Mean'], ascending=False, inplace=True)
    return df


all_data = pd.read_html(html_file)
all_matches = [x for x in all_data if len(x) == 11]

for x in all_matches:
    # Set NaN to 0, where only 1 MVP change ★ to 1, if more than 1 MVP remove the ★
    x['★'] = x['★'].fillna(0)
    x['★'].replace('★', 1, inplace=True)
    x['★'].replace('★', '', regex=True, inplace=True)

df = generate_player_stats_table(all_matches, get_friendlies_list(all_matches, number_to_get=10))
df = add_stats_to_player_stats_table(df)

detailed_df = generate_in_depth_df(all_matches, get_friendlies_list(all_matches, number_to_get=10))
detailed_df = sort_data(detailed_df)


# Save the DataFrames
df.to_csv('top_10.csv')
detailed_df.to_csv('detailed_top_10.csv')