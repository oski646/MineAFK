import configparser

file = configparser.ConfigParser()
file.read("config.ini")

# Global variables
version = file["Version"]["version"]
stones = int(file["Config"]["stones"])
pickaxe = int(file["Config"]["pickaxe"])
food = int(file["Config"]["food"])
dropSlots = file["Config"]["dropSlots"].split(",")
activityRoundsConfig = int(file["Config"]["activityRounds"])
activityCommands = file["Config"]["activityCommands"].split(",")
cobblexRoundsConfig = int(file["Config"]["cobblexRounds"])
cobblexCommands = file["Config"]["cobblexCommands"].split(",")
dropRoundsConfig = int(file["Config"]["dropRounds"])
eatRoundsConfig = int(file["Config"]["eatRounds"])
commandsDelayInSeconds = float(file["Config"]["commandsDelayInSeconds"])
slots = {
    'firstRowX': int(file["Slots"]["firstRowX"]),
    'firstRowY': int(file["Slots"]["firstRowY"]),
    'secondRowX': int(file["Slots"]["secondRowX"]),
    'secondRowY': int(file["Slots"]["secondRowY"]),
    'thirdRowX': int(file["Slots"]["thirdRowX"]),
    'thirdRowY': int(file["Slots"]["thirdRowY"]),
    'fourthRowX': int(file["Slots"]["fourthRowX"]),
    'fourthRowY': int(file["Slots"]["fourthRowY"]),
    'dropX': int(file["Slots"]["dropX"]),
    'dropY': int(file["Slots"]["dropY"]),
    'difference': int(file["Slots"]["difference"])
}
