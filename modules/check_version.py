import modules.logger as logger
import modules.config as config
import requests
import json

def run():
    logger.info("Sprawdzanie aktualizacji...")
    response = requests.get("https://raw.githubusercontent.com/oski646/MineAFK/master/version.txt")
    response_version = response.text
    if response_version != config.version:
        logger.info("Twoja wersja jest nieaktualna, pobierz aktualną z: https://github.com/oski646/MineAFK")
        changes_response = requests.get("https://api.github.com/repos/oski646/MineAFK/commits/master")
        changes_response = requests.get("https://api.github.com/repos/oski646/MineAFK/commits/master")
        changes_json = json.loads(changes_response.text)
        changes = changes_json["commit"]["message"]
        print("")
        print("Changelog")
        print(changes)
        print("")
    else:
        logger.info("Posiadasz aktualną wersję skryptu.")
