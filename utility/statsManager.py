from shutil import copyfile
import json
import os
from os import path


def checkStats(server):
    if not path.exists('SETTINGS/' + server.id):
        os.makedirs('SETTINGS/' + server.id)
    if not path.isfile('SETTINGS/' + server.id + '/stats.json'):
        copyfile('SETTINGS/stats_default.json', 'SETTINGS/' + server.id + '/stats.json')

def getStats(server):

    checkStats(server)
    with open('SETTINGS/' + server.id + '/stats.json') as file:
        return json.load(file)


def saveStats(server, data):

    checkStats(server)
    print(json.dumps(data, indent=4, sort_keys=True))
    with open("SETTINGS/" + server.id + "/stats.json", "w") as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
