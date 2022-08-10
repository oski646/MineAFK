import modules.config as config

def send():
    print("")
    print("##################  MineAFK  ##################")
    print("")
    print("Autor: oski646")
    print("WWW: https://github.com/oski646")
    print("Jeśli chcesz tu coś zmieniać proszę bardzo, lecz pamiętaj o twórcy tego skryptu.")
    print("")
    print("##################  MineAFK  ##################")
    print("")

    print("## Konfiguracja ##")
    print("Ilość stoniarek w bok - " + str(config.horizontalStones))
    print("Ilość stoniarek w przód - " + str(config.verticalStones))
    print("Slot kilofa - " + str(config.pickaxe))
    print("Slot mięska - " + str(config.food) + " (jedzone co " + str(config.eatRoundsConfig) + " rund)")
    print("Sloty do wyrzucenia - " + str(config.dropSlots) + " (wyrzucane co " + str(config.dropRoundsConfig) + " rund)")
    print("Komendy aktywności - " + str(config.activityCommands) + " (wykonywane co " + str(config.activityRoundsConfig) + " rund)")
    print("Cobblex - " + str(config.cobblexCommands) + " (tworzone co " + str(config.cobblexRoundsConfig) + " rund)")
    print("Odstęp pomiędzy wysyłaniem komend - " + str(config.commandsDelayInSeconds) + " sek.")

    print("")
    print("")
