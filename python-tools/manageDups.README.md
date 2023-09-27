# Manage duplicates

This script provides a mechanism to process and identify duplicate game entries in an XML file (gamelist.xml). It allows users to interactively choose which duplicate to keep or automatically report on the duplicates.

# Functional Overview:

* Finding Games by Path: It checks for game entries using their path in the XML structure.
* Title Stripping: The game titles are stripped of any version numbers and brackets to get a more standardized title.
* Sorting & Displaying: Duplicates are presented in a specific order based on their hidden status, region, and language. They are color-coded in the terminal for better visibility.
* Reporting and Interactive Processing: Users can choose to get a report on duplicates or interactively process duplicates. Interactively means the script will prompt the user for which duplicate to keep.
Main Functionalities:

`Finding Duplicates`: By stripping and standardizing titles, it groups games that might have slight title variations but are essentially duplicates.

`Interactive Mode`: When enabled, it lets users decide which among the duplicate entries they want to keep.

`Skipping Processed Entries`: If a set of duplicates already has one entry unhidden, it can skip this set, preventing unnecessary decisions by the user.

`Unhide All`: It provides a mechanism to reset the 'hidden' status of all games, essentially making everything visible.

`Starting Point`: If the user wants to begin interactive processing from a particular game, they can provide its title as a starting point.
How to Use the Script:

Simply run the script for a default behavior (scanning `./gamelist.xml` and reporting duplicates).

Use `--interactive` to manually decide which duplicate to keep.

Use `--skip` to skip already processed duplicate sets.

`--unhide-all` will make all entries visible and save the file.

To start the interactive mode from a specific game, use `--start-at` followed by a part of the game title.

Use `--gamelist` to specify a different XML file path if your `gamelist.xml` is located elsewhere.

# Example Commands:

For a regular report on duplicates:
```
python script_name.py
```

For interactive mode:
```
python script_name.py --interactive
```

For resetting all hidden values:
```
python script_name.py --unhide-all
```

For starting interactive mode from a specific game:
```
python script_name.py --interactive --start-at "Super Mario"
```

# Noteworthy Information:

The script uses regular expressions to strip titles of specific patterns like version numbers and bracketed content.
The script gives priority to games that are not hidden, then based on the region (US, EU, and then WR), and lastly, prioritizes English language games.

The interactive mode lets users save the XML file after processing duplicates, ensuring data isn't lost.

# Usage Scenario:

This script is especially handy for game enthusiasts with a large collection of ROMs. Sometimes, they might have multiple versions of the same game (e.g., US and EU releases). This tool helps in organizing the list, keeping it clean, and ensuring that only the desired version of the game appears in the game list.
