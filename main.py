from core.lookup import Lookup
from argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument("-t", "--target-id", help="Target roblox id to lookup", metavar="<id>")
parser.add_argument("-f", "--file", help="Stores information gathered in the file", metavar="<file>")
parser.add_argument("-s", "--style", help="Changes the information style and format", metavar="<style>")
parser.add_argument("-gl", "--game-limit", help="Sets the limit to how many games are stored or displayed", metavar="<int>")
parser.add_argument("-c", "--cookie", help="authenticates as a user to access other API endpoints", metavar="<cookie>")
parser.add_argument("-d", "--database", help="Mongodb Key for your atlas database", metavar="<link>")

args = parser.parse_args()
target_id = args.target_id

if not args.game_limit:
    args.game_limit = 10

if target_id:
    bloxsint = Lookup(roblox_id=int(target_id), args=args)
    bloxsint.run()
    print(bloxsint.stats)
