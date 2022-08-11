import configparser

file = configparser.ConfigParser()
file.read("config.ini")

# Global variables
version = file["Version"]["version"]
horizontal_stones = int(file["Config"]["horizontal_stones"])
vertical_stones = int(file["Config"]["vertical_stones"])
pickaxe = int(file["Config"]["pickaxe"])
food = int(file["Config"]["food"])
drop_slots = file["Config"]["drop_slots"].split(",")
activity_rounds_config = int(file["Config"]["activity_rounds"])
activity_commands = file["Config"]["activity_commands"].split(",")
cobblex_rounds_config = int(file["Config"]["cobblex_rounds"])
cobblex_commands = file["Config"]["cobblex_commands"].split(",")
drop_rounds_config = int(file["Config"]["drop_rounds"])
eat_rounds_config = int(file["Config"]["eat_rounds"])
commands_delay_in_seconds = float(file["Config"]["commands_delay_in_seconds"])
fast_pickaxe = file["Config"]["fast_pickaxe"].lower() == "true"
slots = {
    'first_row_x': int(file["Slots"]["first_row_x"]),
    'first_row_y': int(file["Slots"]["first_row_y"]),
    'drop_x': int(file["Slots"]["drop_x"]),
    'drop_y': int(file["Slots"]["drop_y"]),
    'difference': int(file["Slots"]["difference"])
}
