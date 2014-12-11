import numpy as np
import csv
import networkx as nx
from pprint import pprint

schedule_file = 'schedule.csv'

g = nx.DiGraph()

teams=["Seattle Seahawks", "New York Jets", "Houston Texans",
       "Carolina Panthers", "Atlanta Falcons", "Pittsburgh Steelers",
       "Minnesota Vikings", "Buffalo Bills", "Tennessee Titans",
       "Denver Broncos", "Miami Dolphins", "Cincinnati Bengals",
       "San Francisco 49ers", "Philadelphia Eagles", "Detroit Lions",
       "Arizona Cardinals", "Green Bay Packers", "Oakland Raiders",
       "Washington Redskins", "Tampa Bay Buccaneers", "New Orleans Saints",
       "Cleveland Browns", "St. Louis Rams", "Chicago Bears",
       "Kansas City Chiefs", "Indianapolis Colts", "New England Patriots",
       "Baltimore Ravens", "Dallas Cowboys", "Jacksonville Jaguars",
       "New York Giants", "San Diego Chargers"]

for team in teams:
    g.add_node((team, 1))
    for week in range(2, 18):
        g.add_node((team, week))
        g.add_edge((team, week - 1), (team, week))

for row in csv.DictReader(open(schedule_file, 'rb')):
    week = int(row['Week'])
    visitor = row['VisTm']
    home = row['HomeTm']
    g.add_edge((visitor, week), (home, week + 1))
    g.add_edge((home, week), (visitor, week + 1))


current_holder =("St. Louis Rams", 10)
desc = nx.descendants(g, current_holder)
desc.add(current_holder)
belt_paths = g.subgraph(desc)

print belt_paths.nodes()
for team in teams:
    reachables = [(t, w) for t, w in belt_paths.nodes() if t == team]
    reachables = sorted(reachables, lambda x,y: cmp(x[1], y[1]))
    if reachables:
        print "Team: ", team
        for reachable in reachables:
            for path in nx.all_simple_paths(belt_paths, current_holder, reachable):
                print "\tpath:"
                prev = path.pop(0)[0]
                for node in path:
                    print "\t\t{}: {} -> {}".format(node[1] - 1, prev, node[0])
                    prev = node[0]
