#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as ET

def find_games_by_genre(root, hide_genre):
    games_to_hide = []
    for game in root.findall('game'):
        genre_node = game.find('genre')
        hidden_node = game.find('hidden')
        is_already_hidden = hidden_node is not None and hidden_node.text == 'true'
        if genre_node is not None and hide_genre.lower() in genre_node.text.lower() and not is_already_hidden:
            games_to_hide.append(game)
    return games_to_hide

def find_games_without_image(root):
    games_to_hide = []
    for game in root.findall('game'):
        image_node = game.find('image')
        hidden_node = game.find('hidden')
        is_already_hidden = hidden_node is not None and hidden_node.text == 'true'
        if image_node is None and not is_already_hidden:
            games_to_hide.append(game)
    return games_to_hide

def find_games_by_title(root, hide_title):
    games_to_hide = []
    for game in root.findall('game'):
        game_name = game.find('name')
        hidden_node = game.find('hidden')
        is_already_hidden = hidden_node is not None and hidden_node.text == 'true'
        if game_name is not None and hide_title.lower() in game_name.text.lower() and not is_already_hidden:
            games_to_hide.append(game)
    return games_to_hide

def find_games_by_empty_desc(root):
    games_to_hide = []
    for game in root.findall('game'):
        desc_node = game.find('desc')
        hidden_node = game.find('hidden')
        is_already_hidden = hidden_node is not None and hidden_node.text == 'true'
        if (desc_node is None or not desc_node.text.strip()) and not is_already_hidden:
            games_to_hide.append(game)
    return games_to_hide

def find_games_by_rating(root, rating_threshold):
    games_to_hide = []
    for game in root.findall('game'):
        rating_node = game.find('rating')
        hidden_node = game.find('hidden')
        is_already_hidden = hidden_node is not None and hidden_node.text == 'true'
        if rating_node is not None and float(rating_node.text) < rating_threshold and not is_already_hidden:
            games_to_hide.append(game)
    return games_to_hide

def prompt_and_hide_games(games_to_hide, tree, file_path):
    # If no games matched criteria, exit
    if not games_to_hide:
        print("No games matched the criteria or games are already hidden.")
        return

    # Print the games to be hidden
    for game in games_to_hide:
        print(game.find('name').text)
    print(f"\nCount of games that will be hidden: {len(games_to_hide)}")

    # Ask the user for confirmation
    choice = input("Do you want to hide these games? (y/n) ")
    if choice.lower() == 'y':
        for game in games_to_hide:
            if game.find('hidden') is not None:
                game.find('hidden').text = 'true'
            else:
                hidden_elem = ET.SubElement(game, 'hidden')
                hidden_elem.text = 'true'
        tree.write(file_path)

def main():
    parser = argparse.ArgumentParser(description="Hide game titles in gamelist.xml based on criteria.")
    parser.add_argument("--gamelist", required=True, help="Path to the gamelist.xml file.")
    parser.add_argument("--hide-title", help="Substring of game title to hide in the XML.")
    parser.add_argument("--hide-empty-desc", action="store_true", help="Hide games with empty descriptions in the XML.")
    parser.add_argument("--hide-rating", type=float, help="Hide games with a rating below the specified threshold (0-1).")
    parser.add_argument("--hide-no-image", action="store_true", help="Hide games without an image in the XML.")
    parser.add_argument("--hide-genre", help="Hide games of a specific genre in the XML.")
    
    args = parser.parse_args()
    
    tree = ET.parse(args.gamelist)
    root = tree.getroot()

    games_to_hide = []
    if args.hide_title:
        games_to_hide.extend(find_games_by_title(root, args.hide_title))
    if args.hide_empty_desc:
        games_to_hide.extend(find_games_by_empty_desc(root))
    if args.hide_rating is not None and 0 <= args.hide_rating <= 1:
        games_to_hide.extend(find_games_by_rating(root, args.hide_rating))
    elif args.hide_rating is not None:
        print("Error: hide-rating should be a value between 0 and 1.")
        return
    if args.hide_no_image:
        games_to_hide.extend(find_games_without_image(root))
    if args.hide_genre:
        games_to_hide.extend(find_games_by_genre(root, args.hide_genre))

    prompt_and_hide_games(games_to_hide, tree, args.gamelist)

if __name__ == "__main__":
    main()