import csv
import networkx as nx

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
    for week in range(2, 19):
        g.add_node((team, week))
        g.add_edge((team, week - 1), (team, week))

for row in csv.DictReader(open(schedule_file, 'rb')):
    week = int(row['Week'])
    visitor = row['VisTm']
    home = row['HomeTm']
    g.add_edge((visitor, week), (home, week + 1))
    g.add_edge((home, week), (visitor, week + 1))


current_holder =("St. Louis Rams", 14)
desc = nx.descendants(g, current_holder)
desc.add(current_holder)
from_holder = g.subgraph(desc)

print "run:"
for team in teams:
    team_18 = (team, 18)
    if team_18 in from_holder.nodes():
        reversed_ = from_holder.reverse()
        desc = nx.descendants(reversed_, team_18)
        desc.add(team_18)
        to_team = from_holder.subgraph(desc)
        nx.write_dot(to_team,"{}.dot".format(team))
        print '\tdot -Tpng "{0}.dot" > "{0}.png"'.format(team)

