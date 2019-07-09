# built into python
from json import load, loads, dump, dumps
from config import FONT_SIZE, TOPSCORES
import logging

# installed using pip (pip install <packagename>
from flask import Flask
import xlrd # TODO come back set the needed functions
import xlwt


class Team():
    def init(self, number=None, name=None, json_data=None):
        if number is not None and name is not None:
            self.number = number
            self.name = name
            self.scores = []
            self.average = self.gen_average()
        elif json_data is not None:
            self.number = json_data['number']
            self.name = json_data['name']
            self.scores = json_data['scores']
            self.average = self.gen_average()

    def add_score(self, score):
        self.scores.append(score)
        self.average = self.gen_average()

    def gen_average(self):
        self.scores.sort()
        average = 0
        spots = 1
        for i in range(TOPSCORES):
            try:
                average += self.scores[i]
                spots += 1
            except:
                break

        return round(average/spots)

    def kill(self):
        return dumps({
            'number': self.number,
            'name': self.name,
            'scores': self.scores,
            'average': self.average
        })


teams = []

def readTeamsXL(file):
    # Opens the sheet to create the teams it is configured
    # Team Number, Team Name, <Non import information>
    sheet=xlrd.open_workbook(file).sheet_by_index(0)

    for i in range(sheet.nrows - 1):
        number = sheet.cell(0, i).value
        name = sheet.cell(1, i).value
        try:
            teams.append(Team(number=number, name=name))
        except:
            logging.error('Failed to add {number} {name}'.format(number=number, name=name))

def readTeamsJSON():
    with open('Teams.json', 'r') as inRead:
        data = load(inRead)

        for i in data:
            teams.append(Team(json_data=i))
    
def endProcess():
    endTeams = []
    for i in teams:
        endTeams.append(i.kill())

    dump(dumps(endTeams),'Teams.json')