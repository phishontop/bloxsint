import bloxsint
import threading
from colorama import Fore, Back, Style


def bloxflip(robloxId):
    bloxflipObj = bloxsint.Bloxflip(robloxId=robloxId)
    bloxflipData = bloxflipObj.getData()
    print(f"\033[1m{Fore.MAGENTA}[BLOXFLIP STATS]")
    if bloxflipData["success"] == True:
        print(f"    {Fore.BLACK}Rank: {Fore.WHITE}{bloxflipData['rank']}")
        print(f"    {Fore.BLACK}Total Wager: {Fore.WHITE}{round(bloxflipData['wager'], 2)}")
        print(f"    {Fore.BLACK}Games Played: {Fore.WHITE}{bloxflipData['gamesPlayed']}")
        print(f"    {Fore.BLACK}Rain Winnings: {Fore.WHITE}{round(bloxflipData['rainWinnings'], 2)}")
    else:
        print(f"    {Fore.RED}Error user not found on bloxflip")


def rbxflip(robloxId):
    rbxflipObj = bloxsint.Rbxflip(robloxId=robloxId)
    rbxflipData = rbxflipObj.getData()
    print(f"\033[1m{Fore.MAGENTA}[RBXFLIP STATS]")
    try:
        rbxflipData['error']
        print(f"    {Fore.RED}Error user not found on rbxflip")
        
    except KeyError as err:
        print(f"    {Fore.BLACK}Lifetime Bet: {Fore.WHITE}{rbxflipData['data']['user']['lifeTimeBet']}")
        print(f"    {Fore.BLACK}Net Profit: {Fore.WHITE}{rbxflipData['data']['user']['netProfit']}")
        print(f"    {Fore.BLACK}Games Lost: {Fore.WHITE}{rbxflipData['data']['user']['gamesLost']}")
        print(f"    {Fore.BLACK}Games Won: {Fore.WHITE}{rbxflipData['data']['user']['gamesWon']}")


def games(robloxId):
    gamesObj = bloxsint.Games(robloxId=robloxId)
    gameIds = gamesObj.getBadges()
    threads = []
    for gameId in gameIds:
        threads.append(
            threading.Thread(target=gamesObj.getUniverseId, args=(gameId,))
        )
    for i in threads:
        i.start()
    for i in threads:
        i.join()
        
    gamesPlayed = gamesObj.getGamesPlayed()
    print(f"\033[1m{Fore.MAGENTA}[GAMES PLAYED]")
    for gamePlayed in gamesPlayed:
        print(f"    {Fore.BLACK}Game: {Fore.WHITE}{gamePlayed}")
        
def ropro(robloxId):
    roproObj = bloxsint.Ropro(robloxId=robloxId)
    roproData = roproObj.getData()
    print(f"\033[1m{Fore.MAGENTA}[ROPRO STATS]")
    print(f"    {Fore.BLACK}Discord: {Fore.WHITE}{roproData['discord']}")
    print(f"    {Fore.BLACK}Reputation: {Fore.WHITE}{roproData['reputation']}")
    
        

def osint(robloxId):     
    tasks = [
        bloxflip, rbxflip, games, ropro
    ]
    threads = []

    for task in tasks:
        threads.append(
            threading.Thread(target=task, args=(robloxId,))    
        )

    for i in threads:
        i.start()
    for i in threads:
        i.join()
    
choice = input("Enter Roblox Id -> ")
osint(choice)
