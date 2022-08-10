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
slots = {
    'firstRowX': int(file["Slots"]["firstRowX"]),
    'firstRowY': int(file["Slots"]["firstRowY"]),
    'dropX': int(file["Slots"]["dropX"]),
    'dropY': int(file["Slots"]["dropY"]),
    'difference': int(file["Slots"]["difference"])
}
