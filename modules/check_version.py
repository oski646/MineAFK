import modules.logger as logger
import modules.config as config
import requests
import json

def run():
    logger.info("Sprawdzanie aktualizacji...")
    response = requests.get("https://raw.githubusercontent.com/oski646/MineAFK/master/version.txt")
    responseVersion = response.text
    if responseVersion != config.version:
        logger.info("Twoja wersja jest nieaktualna, pobierz aktualną z: https://github.com/oski646/MineAFK")
        changesResponse = requests.get("https://api.github.com/repos/oski646/MineAFK/commits/master")
        changesResponse = requests.get("https://api.github.com/repos/oski646/MineAFK/commits/master")
        changesJson = json.loads(changesResponse.text)
        changes = changesJson["commit"]["message"]
        print("")
        print("Changelog")
        print(changes)
        print("")
    else:
        logger.info("Posiadasz aktualną wersję skryptu.")
