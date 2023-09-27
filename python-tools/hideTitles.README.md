# Game Hider for EmulationStation gamelist.xml

# Description:

This script provides a way to hide game titles in the EmulationStation gamelist.xml based on various criteria. It's particularly useful when setting up large collections of games (e.g., thousands of arcade ROMs) to help manage and hide groups of games based on the specified conditions.

# Features:

- `Hide by Title Substring`: You can specify a substring of a game title, and all games with titles containing that substring will be hidden.
- `Hide by Empty Description`: Hide all games that either have an empty description or don't have a description tag at all.
- `Hide by Rating`: Hide all games that have a rating below a specified threshold (rating range is from 0 to 1).
- `Hide Games Without Images`: Hide all games that don't have an associated image.
- `Hide by Genre Substring`: Hide games based on a specified substring in their genre.
  
### Note: All text-based searches (title and genre) are case-insensitive.

# Usage:

```
python3 script_name.py --gamelist /path/to/gamelist.xml [options]
```

# Options:

`--hide-title [TITLE_SUBSTRING]`: Hide games that have the specified substring in their title.

`--hide-empty-desc`: Hide games that don't have a description or have an empty description.

`--hide-rating [RATING_VALUE]`: Hide games with a rating below the specified threshold. The rating value should be between 0 and 1.

`--hide-no-image`: Hide games that don't have an associated image.

`--hide-genre [GENRE_SUBSTRING]`: Hide games that have the specified substring in their genre.

# Example:

To hide all games that have "demo" in their title and games without an image:
```
python3 script_name.py --gamelist /path/to/gamelist.xml --hide-title demo --hide-no-image
```

# Prerequisites:

- Python 3
- The xml.etree.ElementTree library (included in the standard library of Python)

# Final Thoughts:

This tool is an excellent aid for those looking to curate large collections for EmulationStation, ensuring that the game list presented is fine-tuned to the user's preferences.
