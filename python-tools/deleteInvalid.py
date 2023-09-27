#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import os
import argparse

def validate_game_paths(root, base_dir):
    """Returns a list of games with invalid paths"""
    invalid_entries = []
    for game in root.findall('game'):
        path_element = game.find('path')
        if path_element is not None:
            game_path = path_element.text
            # If the path is not an absolute path, consider it relative to the XML file location.
            if not os.path.isabs(game_path):
                game_path = os.path.join(base_dir, game_path)
            if not os.path.exists(game_path):
                invalid_entries.append(game)
    return invalid_entries

def main():
    parser = argparse.ArgumentParser(description="Validate game paths in gamelist.xml.")
    parser.add_argument("--gamelist", required=True, help="Path to the gamelist.xml file.")
    args = parser.parse_args()

    if not os.path.exists(args.gamelist):
        print(f"File {args.gamelist} does not exist!")
        return

    tree = ET.parse(args.gamelist)
    root = tree.getroot()

    base_dir = os.path.dirname(args.gamelist)
    invalid_entries = validate_game_paths(root, base_dir)

    if not invalid_entries:
        print("All game paths are valid!")
        return

    print("Invalid game entries:")
    for game in invalid_entries:
        game_path = game.find('path').text if game.find('path') is not None else "N/A"
        game_name = game.find('name').text if game.find('name') is not None else "N/A"
        print(f"{game_path}: {game_name}")

    choice = input("\nDo you want to remove these invalid entries? (y/n): ")

    if choice.lower() == 'y':
        # Backup the original file
        backup_filename = args.gamelist + ".bak"
        os.rename(args.gamelist, backup_filename)

        # Remove invalid entries
        for game in invalid_entries:
            root.remove(game)

        # Save updated XML
        tree.write(args.gamelist)
        print(f"Invalid entries removed! Original file backed up as {backup_filename}")
    else:
        print("No changes made.")

if __name__ == "__main__":
    main()    