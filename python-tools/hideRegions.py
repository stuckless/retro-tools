#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import sys
import argparse

def hide_regions(xml_file, allowed_regions):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    affected_games = []

    for game in root.findall('game'):
        region = game.find('region')
        lang = game.find('lang')
        hidden = game.find('hidden')
        
        if hidden is not None and hidden.text == 'true':
            continue

        # If region or lang doesn't exist, assume 'en'
        region_text = 'en' if region is None else region.text
        lang_text = 'en' if lang is None else lang.text

        should_hide = False

        if region_text not in allowed_regions:
            should_hide = True

        # For region 'wr', hide if language is not 'en'
        if region_text == 'wr' and lang_text != 'en':
            should_hide = True

        if should_hide:
            name = game.find('name')
            path = game.find('path')
            
            game_identifier = path.text if name is None else name.text
            affected_games.append(game_identifier)
            
            if hidden is None:
                hidden_tag = ET.SubElement(game, 'hidden')
                hidden_tag.text = 'true'
            else:
                hidden.text = 'true'

    return tree, affected_games

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hide games in gamelist.xml based on region.")
    parser.add_argument('--gamelist', required=True, help='Path to gamelist.xml file.')
    parser.add_argument('--allow-regions', nargs='+', default=['en', 'eu', 'us', 'wr'], help='List of allowed regions.')

    args = parser.parse_args()

    tree, affected = hide_regions(args.gamelist, args.allow_regions)

    print(f"Total games affected: {len(affected)}")
    if affected:
        print("Affected game entries:")
        for entry in affected:
            print(entry)

        confirm = input("You are about to affect these items, are you sure? [y/n] ")
        if confirm.lower() == 'y':
            tree.write(args.gamelist)
            print("Changes written successfully!")
        else:
            print("No changes were written.")
