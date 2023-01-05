# Bloxsint V2.5
- One of the first overpowered roblox OSINT tools
- Requires just the username or ID of the target

# Features
- Gambling information (bloxflip + rbxflip)
- Game Played Scraper
- Personal information (age, birthday)
- Roblox -> Discord (discord id + username + tag) no rover or bloxlink
- Friends name finder
- Database storing and data caching
- Previous usernames

# Setup
```console
$ git clone https://github.com/phishontop/bloxsint
$ cd bloxsint
$ pip3 install requests
```

# Usage
```bash
python3 main.py --target-id 1 --file roblox.txt --game-limit 5 --cookie "enter roblox cookie here or delete the cookie arg" --database "mongodb atlas link here"
```

```
  -t <id>, --target-id <id>
                        Target roblox id to lookup
  -f <file>, --file <file>
                        Stores information gathered in the file
  -s <style>, --style <style>
                        Changes the information style and format
  -gl <int>, --game-limit <int>
                        Sets the limit to how many games are stored or displayed
  -c <cookie>, --cookie <cookie>
                        authenticates as a user to access other API endpoints
  -d <link>, --database <link>
                        Mongodb Key for your atlas database
```
