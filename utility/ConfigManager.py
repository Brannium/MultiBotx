from shutil import copyfile
import json
import os
from os import path


def checkConfig(server):
    if not path.exists('SETTINGS/' + server.id):
        os.makedirs('SETTINGS/' + server.id)
    if not path.isfile('SETTINGS/' + server.id + '/config.json'):
        copyfile('SETTINGS/config_default.json', 'SETTINGS/' + server.id + '/config.json')

def getConfig(server):

    checkConfig(server)
    with open('SETTINGS/' + server.id + '/config.json') as file:
        return json.load(file)


def saveConfig(server, data):

    checkConfig(server)
    print(json.dumps(data, indent=4, sort_keys=True))
    with open("SETTINGS/" + server.id + "/config.json", "w") as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
