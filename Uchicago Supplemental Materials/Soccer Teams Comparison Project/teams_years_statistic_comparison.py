### IMPORTS### 
from urllib import request
from bs4 import BeautifulSoup
import os, ssl
import requests
import csv
import json
import lxml.html as lh
import time
import pandas as pd
import urllib3
import re
import random
import datetime
import matplotlib.pyplot as plt
import unidecode
import matplotlib.patches as mpatches
### IMPORTS### 



#----------------TBD----------------# 
###Future### 
# GUI?
# Color/font etc. the inputs and prints 
# Algorithm that if team name or/and league name spelled incorrectly than finds closest one
# Have Processing animation
###Future### 

# TBD using csv is causing some kind of issue 
# On step 7. (then go to 3); right now need to test main function when not preset (just did the inputs function thats why)
# CHANGE MADE, MIGHT HAVE EFFECTS: values_plot1 = list(averages1.values())

# GET THESE DONE BEFORE PUBLISHING 
# 3. make it so that if their is no data from those teams for those years than dot is different color
# 4. If certain amount of years (too long) than zoom out, and only show every x amount of years
# 6. comment all of code/clean up
# 7. make inputs function 
# 8. Implement 


# fbref does have data on champions league stuff 

# Things that I could add to make this project better or i could move on: 
# Do things like comparing certain range of teams between certain years, so like 
# average wins of top 4 - 9 teams of la liga compared to average wins of top 3 - 5 teams of Seria A
# from 2006 to 2012 and be able to do multiple or even compare in same league 
# Be able to do champions leageu 
#----------------TBD----------------# 



# list of all the leagues
list_leagues = ['/en/squads/country/FRA/France-Football-Clubs','/en/squads/country/GER/Germany-Football-Clubs','/en/squads/country/ENG/England-Football-Clubs','/en/squads/country/NZL/New-Zealand-Football-Clubs','/en/squads/country/AUS/Australia-Football-Clubs','/en/squads/country/AUT/Austria-Football-Clubs','/en/squads/country/TUR/Turkey-Football-Clubs','/en/squads/country/RUS/Russia-Football-Clubs','/en/squads/country/USA/United-States-Football-Clubs','/en/squads/country/SUI/Switzerland-Football-Clubs','/en/squads/country/CRO/Croatia-Football-Clubs','/en/squads/country/UKR/Ukraine-Football-Clubs','/en/squads/country/BEL/Belgium-Football-Clubs',
 '/en/squads/country/SCO/Scotland-Football-Clubs','/en/squads/country/BUL/Bulgaria-Football-Clubs','/en/squads/country/ATG/Antigua-and-Barbuda-Football-Clubs','/en/squads/country/POR/Portugal-Football-Clubs','/en/squads/country/GRE/Greece-Football-Clubs','/en/squads/country/MEX/Mexico-Football-Clubs','/en/squads/country/NED/Netherlands-Football-Clubs','/en/squads/country/POL/Poland-Football-Clubs','/en/squads/country/PUR/Puerto-Rico-Football-Clubs','/en/squads/country/DEN/Denmark-Football-Clubs','/en/squads/country/LIE/Liechtenstein-Football-Clubs','/en/squads/country/ITA/Italy-Football-Clubs','/en/squads/country/CAN/Canada-Football-Clubs','/en/squads/country/ESP/Spain-Football-Clubs']

# prints out all the teams from certain country
def getting_countries_teams(country):
    # sleep list
    sleep_list = [3, 3.25, 3.5, 3.75, 4, 4.25, 4.5]
    # sleeping
    time.sleep(random.choice(sleep_list))
    link_countries_leagues = ["https://fbref.com" + x for x in list_leagues if country in x][0]
    # sleeping
    time.sleep(random.choice(sleep_list))
    # getting links from page
    page_teams = requests.get(link_countries_leagues)
    doc_teams = lh.fromstring(page_teams.content)
    table_elements_teams = doc_teams.xpath('//a/@href')
    # New Method
    main_teams = [str(x) for x in table_elements_teams if "/en/squads/" in str(x) and "history" in str(x)]
    # removes link part of all the teams in main_teams
    main_teams = [x.split("/")[-1].replace("-Stats", "").replace("-", " ") for x in main_teams]
    # Old method
    '''
    # making list of links with /en/squads/
    main_teams = [str(x) for x in table_elements_teams if "/en/squads/" in str(x) and str(x).count("/") == 4]
    # list of the indices for parsing
    indices_ID_string = [i for i, x in enumerate(main_teams) if x == "/en/squads/country/"]
    # removes link part of all the teams in main_teams
    main_teams = [x.split("/")[4].replace("-Stats", "").replace("-", " ") for i, x in enumerate(main_teams) if i < indices_ID_string[1] and i > indices_ID_string[0]]
    '''
    # prints out all the teams without anny normal characters
    for team in main_teams:
        print(unidecode.unidecode(team))

# order to go: https://fbref.com/en/squads/  ->   https://fbref.com/en/squads/country/ENG/England-Football-Clubs   ->    https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats
def getting_teams_table(country_of_league, team):
    # sleep list
    sleep_list = [3, 3.25, 3.5, 3.75, 4, 4.25, 4.5]
    # gets link of the countries leagues using list_leagues
    link_countries_leagues = ["https://fbref.com" + x for x in list_leagues if country_of_league in x][0]

    # sleeping
    time.sleep(random.choice(sleep_list))
    # getting link of team
    try:
        page_teams = requests.get(link_countries_leagues)
    except:
        long_sleep_list = [10, 10.5, 11, 12, 15]
        time.sleep(random.choice(long_sleep_list))
        page_teams = requests.get(link_countries_leagues)
    doc_teams = lh.fromstring(page_teams.content)
    table_elements_teams = doc_teams.xpath('//a/@href')

    # getting the team link
    # New Method
    main_teams = [str(x) for x in table_elements_teams if "/en/squads/" in str(x) and "history" in str(x)]
    # Old method
    '''
    # indices_ID_string = [i for i, x in enumerate(main_teams) if x == "/en/squads/country/"]
    print(indices_ID_string)
    main_teams = [x for i, x in enumerate(main_teams) if i < indices_ID_string[1] and i > indices_ID_string[0]]
    '''
    team_link = str(["https://fbref.com" + x for x in main_teams if x.split("/")[-1].replace("-Stats", "").replace("-", " ").lower() == team.lower()])[2:-2]

    # sleeping
    time.sleep(random.choice(sleep_list))
    # getting table
    try:
        url = requests.get(team_link).text
    except:
        long_sleep_list = [10, 10.5, 11, 12, 15]
        time.sleep(random.choice(long_sleep_list))
        url = requests.get(team_link).text
    soup = BeautifulSoup(url, 'lxml')
    soup = soup.find_all('td')
    list_all = []
    for thing in soup:
        list_all.append(thing.contents)
    # narrowing down and taking out things that are not needed for table
    list_all = [str(x[0]) for x in list_all if len(x) != 0 and str(x).count("country") != 1 and str(x).count("player") != 1]
    list_all = [x.split("<")[1].split(">")[1] if x[0:5] == "<span" else x for x in list_all]
    list_all = [x for x in list_all if "<span class=" not in x]
    list_all = [x for x in list_all if x.count("players") != 1]
    # finding indices of team to split by
    indices_team = [i for i, x in enumerate(list_all) if team.replace(" ", "-").lower() in unidecode.unidecode(x).lower()]
    # making an array, each list is list of one seasons stats
    array_all_contents = [list_all[x: indices_team[i + 1]] if i != (len(indices_team) - 1) else list_all[x:] for i, x in enumerate(indices_team)]
    
    '''
    # changes first value of array_all_contents to current year if there is 6 "/"
    if array_all_contents[0][0].count("/") == 6:
        array_all_contents[0][0] = "2018/2019"
    '''
    
    # making list of years
    years_list = [x[0].split("/")[4] for x in array_all_contents]
    # parsing array_all_contents
    array_all_contents = [x[1:12] for x in array_all_contents]
    # making pandas table
    table = pd.DataFrame(array_all_contents, index = years_list, columns = ["comp", "lgrank", "apps", "w", "d", "l", "gf", "ga", "gdiff", "pts", "attendance"])
    # remove string part from league rank
    table["lgrank"] = [int(''.join(y for y in x if y.isdigit())) for x in list(table["lgrank"])]
    # making attendance values into acceptable numbers (86,039 to 86039)
    table["attendance"] = [int(str(x).replace(",", "")) for x in list(table["attendance"])]
    # making comp values just tier level of league ("2. league 2" -> int(2))
    table["comp"] = [int(x.split(".")[0]) for x in list(table.loc[:, "comp"])]
    # replacing the first row index if it is not a year which is happening for the first row if it is the current year
    if not table.index[0].replace("-", "").isdigit():
        # gets current year
        full_time = datetime.datetime.now()
        current_year = str(full_time.year - 1) + "-" + str(full_time.year)
        table.rename(index={table.index[0]:current_year}, inplace=True)
    # returns the finished pandas table
    return table


#-----------------CSV-----------------# 
# gets a full pandas dataframe of all the teams from the csv file with all the teams 
def get_all_teams_csv():
    table = pd.read_csv('/Users/shashank/Library/Mobile Documents/com~apple~CloudDocs/ExtraTime/Programming/Python/Webscraping/TeamsComparison/All.csv')
    list_tables = []
    indices_to_split = [0]
    # gets indices to split the table into each of its team components 
    for index, row in table.iterrows():
        if index == 0:
            pass
        else:
            if list(row)[1] != table.iloc[index - 1, 1] and list(row)[1] != "Squad":
                indices_to_split.append(index)
    indices_to_split.append(len(table.index))
    # splits the table into each team, so there is list of all the teams tables 
    for i, val in enumerate(indices_to_split):
        if i != 0 and i != len(indices_to_split) - 1:
            list_tables.append(table.iloc[indices_to_split[i - 1]:val - 1, :])
        elif i == len(indices_to_split) - 1:
            list_tables.append(table.iloc[indices_to_split[i - 1]:val, :])
    # returns the list of the different teams tables 
    return list_tables

# the list of all the tables from the all.csv is made global so that it only has to be defined once 
list_tables = get_all_teams_csv()

# getting the right pandas table and iterates it from get_all_teams_csv()
def get_table_from_all_csv(team):
    # locates right table 
    for unfinished_table in list_tables:
        if unfinished_table.iloc[0, 1].lower() == team.lower():
            table = unfinished_table
            break
    # putting table in right format
    # changes the indexes
    table.index = list(table.iloc[:, 0])
    # changes the index name
    table.index.name = list(table.columns.values)[0]
    # removes the first column which was actually indexes
    table.drop(table.index.name, axis = 1, inplace = True)
    # making lgrank values into just numbers
    table["LgRank"] = [int(''.join(y for y in x if y.isdigit())) for x in list(table["LgRank"])]
    # making attendance values into acceptable numbers (86,039 to 86039)
    table["Attendance"] = [int(str(x).replace(",", "")) for x in list(table["Attendance"])]
    # making comp values just tier level of league ("2. league 2" -> int(2))
    table["Comp"] = [int(x.split(".")[0]) for x in list(table.loc[:, "Comp"])]
    # changing column names to lower case
    table.columns = [x.lower() for x in table.columns]
    # keeping only columns needed
    list_columns_needed = ["comp", "lgrank", "apps", "w", "d", "l", "gf", "ga", "gdiff", "pts", "attendance"]
    for header in table.columns:
        if header not in list_columns_needed:
            table.drop(header, axis=1, inplace=True)
    return table

# print(get_table_from_all_csv("Manchester United"))
#-----------------CSV-----------------# 


# returns dictionary of Seasons:Apps, Seasons:Values and Seasons:Division number
def get_statistic(country_of_league, team, statistic, years_sequence_list, csv_or_webscraping):
    # gets table calling appropiate function based on whether webscraping or getting from files
    if csv_or_webscraping == 0:
        # gets from the csv file with all the tables 
        table = get_table_from_all_csv(team)
    else:
        table = getting_teams_table(country_of_league, team)
    years_list = years_sequence_list.copy()
    # list of Division number
    comp_vals_list = list(table.loc[years_list[-1]:years_list[0], "comp"])
    comp_vals_list.reverse()
    # list of years for that
    years_table = list(table.loc[years_list[-1]:years_list[0], "comp"].index.values)
    years_table.reverse()
    # dictionary of  which Seasons:Division number
    dict_not_first_division = dict(zip(years_table, comp_vals_list))
    
    values = []
    apps_list = []
    # iterating through years_sequence_list to get values and apps
    for year in years_sequence_list:
        if year in list(table.index):
            # making list of values
            values.append(table.loc[year, statistic])
            # making list of apps
            apps_list.append(table.loc[year, "apps"])
        else:
            # remove the year from the years list as no vals for it
            years_list.remove(year)
    # dict of values 
    dict_values = dict(zip(years_list, values))
    # dict of apps
    apps_dict = dict(zip(years_list, apps_list))
    return apps_dict, dict_values, dict_not_first_division
    
# handles the input values 
def inputs(preset):
    # preset values for testing 
    if preset:
        csv_or_webscraping = 1
        # 1
        teams1 = ["Barcelona"]
        teams1_for_legend = "[PRESET]"
        leagues1 = ["ESP"]
        teams_leagues_dict1 = dict(zip(teams1, leagues1))
        # 2
        teams2 = ["Real Madrid"]
        teams2_for_legend = "[PRESET]"
        leagues2 = ["ESP"]
        teams_leagues_dict2 = dict(zip(teams2, leagues2))
        # rest
        start_year = 1990
        end_year = 2019
        statistic = "W"
        statistic = statistic.lower()
        difference_bool = "y"
        type_statistic = 1
        statistic_dict = {"lgrank":"LgRank", "pts":"Pts", "gdiff":"GDiff", "w":"W", "d":"D", "l":"L", "gf":"GF", "ga":"GA", "attendance":"Attendance (avg/home game)"}
        statistic_to_print = statistic_dict[statistic]
        print_values = "y"
        print_values_round = 5

        csv_or_webscraping, teams1, teams1_for_legend, leagues1, teams_leagues_dict1, teams2, teams2_for_legend, \
        leagues2, teams_leagues_dict2, start_year, end_year, statistic, difference_bool, type_statistic, \
        statistic_dict, statistic_to_print, print_values, print_values_round

    # user input 
    else:
        # seeing team options from country
        print("Country Options: ENG, ESP, ITA, GER, FRA, POR, RUS, BEL, GRE, NED, TUR, NZL, AUS, USA, SUI, CRO, UKR, SCO, BUL, ATG, MEX, POL, PUR, DEN, LIE, CAN")
        look_up_bool = input("Would you like to see all teams from one of these countries (Y/N)? ")
        if look_up_bool.lower() == "y":
            print("To quit enter Q")
            countries_league_to_show = input("What country would you like to see all the teams from? ")
            while countries_league_to_show.lower() != "q":
                getting_countries_teams(countries_league_to_show)
                print("Country Options: ENG, ESP, ITA, GER, FRA, POR, RUS, BEL, GRE, NED, TUR, NZL, AUS, USA, SUI, CRO, UKR, SCO, BUL, ATG, MEX, POL, PUR, DEN, LIE, CAN")
                countries_league_to_show = input("What country would you like to see all the teams from? ")
                
        # input to go by csv or by webscraping
        csv_or_webscraping = int(input("Get files by csv (0) or webscrape (1): "))
        # teams1 and leagues1
        teams1 = input("Input first group of teams: ")
        teams1 = teams1.split(",")
        teams1 = [x.lstrip() for x in teams1]
        teams1_for_legend = teams1.copy()
        # changing teams1_for_legend depending on size of list
        if len(", ".join(teams1)) > 23 and len(", ".join(teams1)) < 50:
            teams1_for_legend = [x[0:2] for x in teams1_for_legend]
            teams1_for_legend = "[" + ", ".join(teams1_for_legend) + "]"
        elif len(", ".join(teams1)) >= 50:
            teams1_for_legend = "[" + teams1_for_legend[0] + "]"
        else:
            teams1_for_legend = "[" + ", ".join(teams1_for_legend) + "]"
        leagues1 = input("Input the leagues for each team: ")
        leagues1 = leagues1.split(",")
        leagues1 = [x.lstrip().upper() for x in leagues1]
        teams_leagues_dict1 = dict(zip(teams1, leagues1))
        # teams2 and leagues2
        teams2 = input("Input the second group of teams: ")
        teams2 = teams2.split(",")
        teams2 = [x.lstrip() for x in teams2]
        teams2_for_legend = teams2.copy()
        # changing teams2_for_legend depending on size of list
        if len(", ".join(teams2)) > 23 and len(", ".join(teams2)) < 50:
            teams2_for_legend = [x[0:2] for x in teams2_for_legend]
            teams2_for_legend = "[" + ", ".join(teams2_for_legend) + "]"
        elif len(", ".join(teams2)) >= 50:
            teams2_for_legend = "[" + teams2_for_legend[0] + "]"
        else:
            teams2_for_legend = "[" + ", ".join(teams2_for_legend) + "]"
        leagues2 = input("Input the leagues for each team: ")
        leagues2 = leagues2.split(",")
        leagues2 = [x.lstrip().upper() for x in leagues2]
        teams_leagues_dict2 = dict(zip(teams2, leagues2))
        
        # years
        print("E.G. for season 2015/2016, you would enter 2016")
        start_year = int(input("Start year: "))
        end_year = int(input("End year: "))
        # statistic
        print("Statistic options: League Tier, LgRank, Pts, GDiff, W, D, L, GF, GA, Avg Attendance/Home game (Attendance)")
        statistic = input("Input statistic you would like to look at: ")
        # getting type_statistic
        statistic = statistic.lower()
        statistic_dict = {"league tier":"League Tier", "lgrank":"LgRank", "pts":"Pts", "gdiff":"GDiff", "w":"W", "d":"D", "l":"L", "gf":"GF", "ga":"GA", "attendance":"Attendance (avg/home game)"}
        statistic_to_print = statistic_dict[statistic]
        # different options based on statistic
        if statistic in ["pts", "gdiff", "w", "d", "l", "gf", "ga"]:
            print("Options: Avg %s/Game (1), Total %s/Season (2), Avg %s/Season (3)" % (statistic_to_print, statistic_to_print, statistic_to_print))
        elif statistic == "attendance":
            print("Options: Total %s/Season (1), Avg %s/Season (2)" % (statistic_to_print, statistic_to_print))
        elif statistic == "league tier" or statistic == "lgrank":
            print("Options: Avg %s/Season (1)" % (statistic_to_print))
        # turning league tier to comp because in table, comp is the column index
        if statistic == "league tier":
            statistic = "comp"
        type_statistic = int(input("Type: "))
        # menu options
        difference_bool = input("Would you like a difference plot (Y/N)? ")
        # printing values 
        print_values = input("Would you like to print the values? ")
        print_values_round = input("What value would you like to round to? ")

    return csv_or_webscraping, teams1, teams1_for_legend, leagues1, teams_leagues_dict1, teams2, teams2_for_legend, \
        leagues2, teams_leagues_dict2, start_year, end_year, statistic, difference_bool, type_statistic, \
        statistic_dict, statistic_to_print, print_values, print_values_round

# main function, does calculations and graphing 
def main(plt, preset):
    csv_or_webscraping, teams1, teams1_for_legend, leagues1, teams_leagues_dict1, teams2, teams2_for_legend, leagues2, teams_leagues_dict2, start_year, end_year, statistic, difference_bool, type_statistic, statistic_dict, statistic_to_print, print_values, print_values_round = inputs(preset)
    


    ### INPUT CALCULATIONS### 
    start_year_season_format = str(start_year - 1) + "-" + str(start_year)
    end_year_season_format = str(end_year - 1) + "-" + str(end_year)
    years_sequence_list = [str(x - 1) + "-" + str(x) for x in range(start_year, end_year + 1)]
    years_plotting_list = [x[2:5] + x[7:] for x in years_sequence_list]
    # creating the dict_colors
    dict_colors1 = {}
    dict_colors2 = {}
    # setting defaults for dict_colors
    for year in years_sequence_list:
        dict_colors1[year] = 'r'
        dict_colors2[year] = 'b'
    if statistic.lower() in ["attendance"]:
        if type_statistic == 1:
            type_statistic = 2
        elif type_statistic == 2:
            type_statistic = 3
    elif statistic.lower() in ["comp", "lgrank"]:
        if type_statistic == 1:
            type_statistic = 3
    ### INPUT CALCULATIONS### 

    ### STATISTIC CALCULATIONS### 
    # teams1 calculations
    years_app_totals1 = dict(zip(years_sequence_list, [0 for x in range(len(years_sequence_list))]))
    years_values_totals1 = years_app_totals1.copy()
    averages1 = years_app_totals1.copy()
    for team in teams_leagues_dict1:
        print(team)
        # getting the dicts from get_statistic()
        apps_dict, dict_values, dict_first_division1 = get_statistic(teams_leagues_dict1[team], team, statistic, years_sequence_list, csv_or_webscraping)
        # values from dicts just gotten from one team are added to the totals dicts
        for key in apps_dict:
            years_app_totals1[key] += int(apps_dict[key])
            years_values_totals1[key] += float(dict_values[key])
        # making dicts for coloring dots based on whether team in first division
        for key in dict_first_division1:
            if dict_colors1[key] != 'violet' and int(dict_first_division1[key]) == 1:
                dict_colors1[key] = 'r'
            else:
                dict_colors1[key] = 'violet'
    # teams2 calculations
    years_app_totals2 = dict(zip(years_sequence_list, [0 for x in range(len(years_sequence_list))]))
    years_values_totals2 = years_app_totals2.copy()
    averages2 = years_app_totals2.copy()
    for team in teams_leagues_dict2:
        print(team)
        # getting the dicts from get_statistic()
        apps_dict, dict_values, dict_first_division2  = get_statistic(teams_leagues_dict2[team], team, statistic, years_sequence_list, csv_or_webscraping)
        # values from dicts just gotten from one team are added to the totals dicts
        for key in apps_dict:
            years_app_totals2[key] += int(apps_dict[key])
            years_values_totals2[key] += float(dict_values[key])
        # making dicts for coloring dots based on whether team in first division
        for key in dict_first_division2:
            if dict_colors2[key] != 'violet' and int(dict_first_division2[key]) == 1:
                dict_colors2[key] = 'b'
            else:
                dict_colors2[key] = 'violet'
    ### STATISTIC CALCULATIONS### 


    ### PLOTTING### 
    plt.figure(1)
    plt.rcParams["figure.figsize"] = (13, 7)
    # based on the type of statistic, getting the values to plot
    # Statistic/Game
    if type_statistic == 1:
        statistic_to_print += "/Game"
        for key in years_app_totals1:
            # preventing dividing by zero based on scenario
            if years_app_totals1[key] == 0 and years_app_totals2[key] != 0:
                averages1[key] = 0
                averages2[key] = (years_values_totals2[key] / years_app_totals2[key])
            elif years_app_totals1[key] != 0 and years_app_totals2[key] == 0:
                averages1[key] = (years_values_totals1[key] / years_app_totals1[key])
                averages2[key] = 0
            elif years_app_totals1[key] == 0 and years_app_totals2[key] == 0:
                averages1[key] = 0
                averages2[key] = 0
            else:
                averages1[key] = (years_values_totals1[key] / years_app_totals1[key])
                averages2[key] = (years_values_totals2[key] / years_app_totals2[key])
        values_plot1 = list(averages1.values())
        values_plot2 = list(averages2.values())
    # Statistic in total for all teams
    elif type_statistic == 2:
        statistic_to_print += " in Total"
        values_plot1 = list(years_values_totals1.values())
        values_plot2 = list(years_values_totals2.values())
    # Statistic/Season
    elif type_statistic == 3:
        statistic_to_print += "/Season"
        for key in years_app_totals1:
            averages1[key] = years_values_totals1[key] / len(teams1)
            averages2[key] = years_values_totals2[key] / len(teams2)
        values_plot1 = list(averages1.values())
        values_plot2 = list(averages2.values())
    # making difference list 
    difference = [x1 - x2 for (x1, x2) in zip(values_plot1, values_plot2)]
    difference_plot = [abs(x) for x in difference]
    # printing values if input == "y"
    if print_values.lower() == "y":
        # figuring out which dict to print
        if type_statistic == 1 or type_statistic == 3:
            dict_to_print1 = averages1
            dict_to_print2 = averages2 
        else:
            dict_to_print1 = years_values_totals1
            dict_to_print2 = years_values_totals2
        # printing 
        print("--------------------" + teams1_for_legend + "--------------------")
        for key, value in dict_to_print1.items():
            print(key, " : ", round(value, print_values_round))
        print("--------------------" + teams2_for_legend + "--------------------")
        for key, value in dict_to_print2.items():
            print(key, " : ", round(value, print_values_round))
        # printing values for difference plot 
        if difference_bool.lower() == "y":
            print("--------------------Difference Plot Values--------------------")
            for index, key in enumerate(list(dict_to_print1.keys())):
                print(key, " : ", round(difference_plot[index], print_values_round))
    # plotting both the dots and lines, dots colors are deteremined by dict_colors
    plt.scatter(years_plotting_list, values_plot1, c = list(dict_colors1.values()), s = 80, zorder = 3)
    plt.plot(values_plot1, 'r', zorder = 1, linewidth = 2.0)
    plt.scatter(years_plotting_list, values_plot2, c = list(dict_colors2.values()), s = 80, zorder = 4)
    plt.plot(values_plot2, 'b', linewidth = 2.0, zorder = 2)
    
    # x and y labels
    plt.xlabel("Seasons")
    plt.ylabel(statistic_to_print)
    # legend
    red_patch = mpatches.Patch(color = 'red', label = str(teams1_for_legend))
    blue_patch = mpatches.Patch(color = 'blue', label = str(teams2_for_legend))
    not_first_divions_path = mpatches.Patch(color = 'violet', label = "Team(s) not in first division that season")
    plt.legend(handles = [red_patch, blue_patch, not_first_divions_path], bbox_to_anchor=(0.5, 1.05), loc='lower center', ncol=2)
    # xticks
    plt.xticks(rotation=45)
    # having ylim as 0 if no negative values otherwise there is no ylim
    negatives = False
    for value in values_plot1 and values_plot2:
        if value < 0:
            negatives = True
    if negatives == False:
        plt.ylim(bottom=0)
    # title
    plt.title("Comparison of " + statistic_to_print +  " of Two Groups of Teams From " + start_year_season_format + " To " + end_year_season_format)
    # difference plotting
    if difference_bool.lower() == "y":
        plt.figure(2)
        plt.rcParams["figure.figsize"] = (13, 7)
        barlist  = plt.bar(years_plotting_list, difference_plot, color = 'gray')
        for num in range(len(difference)):
            if difference[num] > 0:
                barlist[num].set_color('r')
            elif difference[num] < 0:
                barlist[num].set_color('b')
        # annotations for bar graphs, disabled 
        '''
        for i, j in zip(years_plotting_list, difference_plot):
            plt.annotate(str(round(j, 3)), xy = (i, j), size = 10, ha = 'center')
        '''
        # gray_patch = mpatches.Patch(color = 'w', label = "Equal")
        plt.legend(handles = [red_patch, blue_patch], bbox_to_anchor=(0.5, 1.05), loc='lower center', ncol=2)
        plt.title("Difference of " + statistic_to_print +  " of Two Groups of Teams From " + start_year_season_format + " To " + end_year_season_format)
        plt.xticks(rotation=45)
    plt.show()


main(plt, True)
