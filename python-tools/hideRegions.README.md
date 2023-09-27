# Game Region Hider for EmulationStation

# Overview:
The primary purpose of this script is to hide non-English game entries in an EmulationStation gamelist.xml file. The script evaluates games based on their 'region' and 'lang' attributes, and hides those that don't match the allowed regions. By default, if a game lacks either a 'region' or 'lang' tag, the script assumes it's in English ('en').

# Requirements:
- Python 3.x
- An EmulationStation gamelist.xml file.

# Usage:
To use the script, run it from the command line specifying the path to your gamelist.xml file and optionally, the list of allowed regions:
```
python3 path_to_script.py --gamelist /path/to/your/gamelist.xml --allow-regions en eu us wr
```

By default, the allowed regions are 'en', 'eu', 'us', and 'wr'. You can specify a different set of regions using the `--allow-regions` argument.

# Details:
The script considers 'wr' as a special region. Even if 'wr' is in the allowed regions, the game will be hidden if its language ('lang' attribute) is not English ('en').

Once the script identifies games to be hidden, it will print a list of affected game entries and prompt you for confirmation before making changes to the gamelist.xml file.

# Note:
It's a good practice to backup your gamelist.xml file before making changes using this or any other script.
