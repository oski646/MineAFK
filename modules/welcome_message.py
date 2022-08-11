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
    print("Ilość stoniarek w bok - " + str(config.horizontal_stones))
    print("Ilość stoniarek w przód - " + str(config.vertical_stones))
    print("Slot kilofa - " + str(config.pickaxe))
    print("Slot mięska - " + str(config.food) + " (jedzone co " + str(config.eat_rounds_config) + " rund)")
    print("Sloty do wyrzucenia - " + str(config.drop_slots) + " (wyrzucane co " + str(config.drop_rounds_config) + " rund)")
    print("Komendy aktywności - " + str(config.activity_commands) + " (wykonywane co " + str(config.activity_rounds_config) + " rund)")
    print("Cobblex - " + str(config.cobblex_commands) + " (tworzone co " + str(config.cobblex_rounds_config) + " rund)")
    print("Odstęp pomiędzy wysyłaniem komend - " + str(config.commands_delay_in_seconds) + " sek.")

    print("")
    print("")
