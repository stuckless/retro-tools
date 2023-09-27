#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import re
import argparse

def findByPath(root, target_path):
    for game in root.findall("./game"):
        path_elem = game.find("path")
        if path_elem is not None and path_elem.text == target_path:
            return game
    return None

def strip_title(title):
    title = re.sub(r'\(.*?\)', '', title)
    title = re.sub(r'\s*[Vv]\d+(\.\d+)?$', '', title)
    return title.strip()

def sort_key(entry):
    _, _, region, lang, is_hidden = entry
    if region is None: region = ""
    if lang is None: lang = ""

    order_regions = ["us", "eu", "wr"]
    if region not in order_regions:
        order_region = len(order_regions)
    else:
        order_region = order_regions.index(region)
    
    order_lang = 0 if lang == "en" else 1

    order_hidden = 0 if not is_hidden else 1

    return (order_hidden, order_region, order_lang)

def display_entry(entry, field1Len, field2Len):
    path, name, region, lang, is_hidden = entry
    
    # Define the ANSI color codes
    WHITE = "\033[97m"
    YELLOW = "\033[93m"
    ORANGE = "\033[91m"  # approximation for orange
    RESET = "\033[0m"
    
    display = "*" if not is_hidden else " "
    
    # Pad the path with spaces and color it white
    display += f"{WHITE}{path: <{field1Len}}: "
    
    # Pad the name with spaces and color it yellow
    display += f"{YELLOW}{name: <{field2Len}}"
    
    if region:
        # Color the lang and region with orange
        display += f" {ORANGE}[region:{region}"
        if lang:
            display += f", lang:{lang}"
        display += "]"
    else:
        if lang:
            display += f" {ORANGE}[lang:{lang}]"

    # Add RESET at the end of the entire display string
    display += RESET
    
    return display

def main(interactive=False, skip_existing=False, unhide_all_flag=False, start_at=None, gamelist='gamelist.xml'):
    tree = ET.parse(gamelist)
    root = tree.getroot()

    if unhide_all_flag:
        for game in root.findall("game"):
            hidden_elem = game.find("hidden")
            if hidden_elem is not None:
                game.remove(hidden_elem)
        tree.write(gamelist)
        return

    games = {}
    for game in root.findall("game"):
        path = game.find("path").text
        name = game.find("name").text
        region = game.find("region")
        region = region.text if region is not None else None
        lang = game.find("lang")
        lang = lang.text if lang is not None else None
        hidden = game.find("hidden")
        is_hidden = hidden is not None and hidden.text == "true"
        stripped_title = strip_title(name)
        games[path] = (name, stripped_title, region, lang, is_hidden)

    games_by_title = {}
    for path, (name, stripped_title, region, lang, is_hidden) in games.items():
        if stripped_title not in games_by_title:
            games_by_title[stripped_title] = []
        games_by_title[stripped_title].append((path, name, region, lang, is_hidden))

    duplicates = {k: v for k, v in games_by_title.items() if len(v) > 1}

    if not interactive:
        report_duplicates(duplicates, games)
    else:
        process_duplicates_interactively(duplicates, root, tree, skip_existing, start_at, gamelist)

def report_duplicates(duplicates, games):
    total_games = sum(len(entries) for entries in duplicates.values())
    print("Duplicates Found:")
    for stripped_title, duplicate_entries in sorted(duplicates.items(), key=lambda item: item[0]):
        sorted_entries = sorted(duplicate_entries, key=sort_key)
        for entry in sorted_entries:
            print(display_entry(entry, 50, 50))
        print()

    print(f"Total games in the list: {len(games)}")
    print(f"Number of duplicate games: {total_games}")
    print(f"Games that can be hidden if we only kept one of the duplicates: {total_games - len(duplicates)}")

def process_duplicates_interactively(duplicates, root, tree, skip_existing, start_at, gamelist):
    starting = True
    changed = False
    entryIdx = 1
    for stripped_title, duplicate_entries in sorted(duplicates.items(), key=lambda item: item[0]):
        if start_at and starting and start_at.lower() not in stripped_title.lower():
            continue
        starting = False
        
        if skip_existing and sum(1 for _, _, _, _, is_hidden in duplicate_entries if not is_hidden) <= 1:
            entryIdx += 1
            continue

        sorted_entries = sorted(duplicate_entries, key=sort_key)
        print(f"\nDuplicates Found ({entryIdx} of {len(duplicates)}):")
        entryIdx += 1
        for idx, entry in enumerate(sorted_entries, 1):
            print(f"{idx}. {display_entry(entry, 50, 50)}")
        
        choice = input("\nEnter the number of the game to keep (or 'q' to quit and save, 'x' to quit with nosave): ").strip().lower()
        if choice == 'q':
            break

        if choice == 'x':
            changed=False
            break

        if choice == '':
            print("Skipping")
            continue

        if choice.isdigit() and 1 <= int(choice) <= len(sorted_entries):
            changed = True
            chosen_idx = int(choice) - 1

            for idx, (path, _, _, _, _) in enumerate(sorted_entries):
                game_elem = findByPath(root, path)
                # game_elem = root.find(f"./game[path='{path}']")
                if idx == chosen_idx:
                    hidden_elem = game_elem.find("hidden")
                    if hidden_elem != None:
                        game_elem.remove(hidden_elem)
                else:
                    hidden_elem = game_elem.find("hidden")
                    if hidden_elem == None:
                        hidden_elem = ET.SubElement(game_elem, "hidden")
                    hidden_elem.text = "true"
        else:
            print("Skipping")
        
    if changed:
        tree.write(gamelist)
        print(f"Wrote file: {gamelist}")
    else:
        print("No changes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan gamelist.xml for duplicate games based on name.")
    parser.add_argument('--interactive', action='store_true', help="Enable interactive mode to choose which duplicates to keep.")
    parser.add_argument('--skip', action='store_true', help="When used with --interactive, skip entries if one and only one of the duplicates is currently unhidden.")
    parser.add_argument('--unhide-all', action='store_true', help="Reset all hidden values to false and then exit.")
    parser.add_argument('--start-at', type=str, help="With --interactive, skip all duplicate entries and start at the group where a game title contains this text.")
    parser.add_argument('--gamelist', type=str, default='./gamelist.xml', help="Specify the path to the gamelist.xml file. Defaults to './gamelist.xml'")
    args = parser.parse_args()

    main(interactive=args.interactive, skip_existing=args.skip, unhide_all_flag=args.unhide_all, start_at=args.start_at, gamelist=args.gamelist)
