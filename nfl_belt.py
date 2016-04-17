#!/usr/bin/env python
"""
Create graphs for possible paths the NFL title belt can take during the season.

Requires graphviz

Run:

> "python nfl_belt.py | bash"

to create all the graphs or

> "python nfl_belt.py"

to just create the *.dot files

"""

import csv
import networkx as nx
from jinja2 import Template

# config
current_holder =("Denver Broncos", 1)
schedule_file = 'schedule.csv'

teams = [
 "New England Patriots",
 "New York Jets",
 "Buffalo Bills",
 "Miami Dolphins",

 "Pittsburgh Steelers",
 "Cleveland Browns",
 "Baltimore Ravens",
 "Cincinnati Bengals",

 "Tennessee Titans",
 "Houston Texans",
 "Jacksonville Jaguars",
 "Indianapolis Colts",

 "Oakland Raiders",
 "Denver Broncos",
 "San Diego Chargers",
 "Kansas City Chiefs",

 "Philadelphia Eagles",
 "New York Giants",
 "Washington Redskins",
 "Dallas Cowboys",

 "Detroit Lions",
 "Chicago Bears",
 "Green Bay Packers",
 "Minnesota Vikings",

 "Carolina Panthers",
 "Atlanta Falcons",
 "New Orleans Saints",
 "Tampa Bay Buccaneers",

 "Los Angeles Rams",
 "San Francisco 49ers",
 "Arizona Cardinals",
 "Seattle Seahawks"]
# end config

g = nx.DiGraph()
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


desc = nx.descendants(g, current_holder)
desc.add(current_holder)
from_holder = g.subgraph(desc)
graphs = {}
edge_sets = {}

for t in teams:
    edge_sets[t] = [set() for n in range(1,20)]
    prev_graph = nx.Graph()
    for w in range(1,19):
        n = (t,w)
        if n in from_holder.nodes():
            reversed_ = from_holder.reverse()
            desc = nx.descendants(reversed_, n)
            desc.add(n)
            to_team = from_holder.subgraph(desc)
            edge_set = set(to_team.edges()) - set(prev_graph.edges())
            prev_graph = to_team
            graphs[t] = to_team
            # if w > 17:
                # import pdb; pdb.set_trace()
            edge_sets[t][w] = edge_set

edge_sets = {t: [w for w in weeks if w] for t, weeks in edge_sets.items()}

#layout params

height = 1000
width = 1080
stroke_width = 0.007 * width
gutter= [50,190,60,30]
div_sep = 0.02 * width
conf_sep = 0.01 * width
team_sep = (width - gutter[0] - gutter[2] - 7 * div_sep - conf_sep) / 31.0
week_sep = (height - gutter[1] - gutter[3]) / 18
img_dim = 1.0 * team_sep

x = {}
xi = gutter[0]
for t, i in zip(teams, range(1,33)):
    x[t] = xi
    xi += team_sep
    if not i % 4:
        xi += div_sep
    if not i % 16:
        xi += conf_sep
y = {week: gutter[1] + week_sep * week for week in range(1,19)}
from math import log
log_diffs = {t1: {t2:  log(1 + abs(x[t1] - x[t2]))  for t2 in teams} for t1 in teams}

import re
pat = re.compile(r'([.]|\s)+')
team_ids = {team: pat.sub('-', team).lower() for team in teams}
logos = {team: '/nfl/title-belt/nfl-belt/logos/' + pat.sub('_', team) + '_logo.svg' for team in teams}
template_file = "template.html"

out_file = "belt-possibilities.html"
with open(template_file, 'r') as t:
    template = Template(t.read())
    with open(out_file, 'w') as f:
        f.write(template.render(
            x=x, y=y,
            height=height, width=width,
            gutter=gutter,
            teams=teams,
            logos=logos,
            team_ids=team_ids,
            graphs=graphs,
            edge_sets=edge_sets,
            stroke_width=stroke_width,
            img_dim=img_dim,
            log_diffs=log_diffs,
            team_sep=team_sep
            ))
