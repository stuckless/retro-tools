Game Path Validator for EmulationStation

# Overview:
This script is designed to validate game paths specified in an EmulationStation gamelist.xml file. If any paths to game files are invalid (i.e., the file does not exist), the script will report these entries and offer the user the option to remove them from the XML file.

# Requirements:
- Python 3.x
- An EmulationStation gamelist.xml file to validate.

# gamelist.xml Format:
The script expects the gamelist.xml file to follow the # EmulationStation format:
```
<gameList>
  <game id="XXXXX">
    <path>PATH_TO_GAME_FILE</path>
    <name>GAME_NAME</name>
    <!-- Other game metadata... -->
  </game>
  <!-- Additional game entries... -->
</gameList>
```

# Usage:
To use the script, you can run it from the command line and specify the path to your gamelist.xml file:
```
python3 path_to_script.py --gamelist /path/to/your/gamelist.xml
```

After execution, if any invalid game paths are detected, the script will print these entries and offer the option to remove them. If you choose to remove them, the script will create a backup of the original gamelist.xml file with a .bak extension before saving the updated XML.

# Note:
Always ensure you have backups of your gamelist.xml file, especially if making changes. While this script does create a backup before modifying the XML, having multiple backups is always a good practice.
