import configparser

file = configparser.ConfigParser()
file.read("config.ini")

# Global variables
version = file["Version"]["version"]
horizontalStones = int(file["Config"]["horizontalStones"])
verticalStones = int(file["Config"]["verticalStones"])
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
fastPickaxe = file["Config"]["fastPickaxe"].lower() == "true"
backgroundMining = {
    'windowName': file["BackgroundMining"]["windowName"],
    'isBlazingPack': file["BackgroundMining"]["isBlazingPack"].lower() == "true",
}
# - 20 dla normalnego mc w Y
slots = {
    'firstRowX': int(file["Slots"]["firstRowX"]),
    'firstRowY': -int(file["Slots"]["firstRowY"]) + 50,
    'secondRowX': int(file["Slots"]["secondRowX"]),
    'secondRowY': -int(file["Slots"]["secondRowY"]) + 50,
    'thirdRowX': int(file["Slots"]["thirdRowX"]),
    'thirdRowY': -int(file["Slots"]["thirdRowY"]) + 50,
    'fourthRowX': int(file["Slots"]["fourthRowX"]),
    'fourthRowY': -int(file["Slots"]["fourthRowY"]) + 50,
    'dropX': int(file["Slots"]["dropX"]),
    'dropY': -int(file["Slots"]["dropY"]) + 50,
    'difference': int(file["Slots"]["difference"])
}
