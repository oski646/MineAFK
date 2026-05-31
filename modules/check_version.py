import json

import requests

import modules.config as config
import modules.logger as logger


def run(log=None):
    write_log = log or logger.info
    write_log("Sprawdzanie aktualizacji...")

    response = requests.get("https://raw.githubusercontent.com/oski646/MineAFK/master/version.txt", timeout=10)
    response.raise_for_status()

    if response.text.strip() != config.version:
        write_log("Twoja wersja jest nieaktualna. Pobierz najnowszą wersję z: https://github.com/oski646/MineAFK")
        changes_response = requests.get("https://api.github.com/repos/oski646/MineAFK/commits/master", timeout=10)
        changes_response.raise_for_status()
        changes_json = json.loads(changes_response.text)
        write_log("Lista zmian")
        write_log(changes_json["commit"]["message"])
    else:
        write_log("Masz najnowszą wersję skryptu.")
