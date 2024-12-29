import argparse
import json

def find_tokens(db, card_name):
    if card_name[0:2] == '//' or card_name.rstrip() == "":
        return []
    name = " ".join(card_name.rsplit(" ")[1:]).rstrip()
    card = [item for item in db if item.get("name")==name]
    if len(card) == 0:
        return []
    else:
        tokens = [item for item in card[0]["all_parts"] if item.get("component")=="token"]
        token_ids = []
        for i in tokens:
            token_ids.append(i["id"])

        return token_ids

def applicable_cards(oracle_cards):
    return [item for item in oracle_cards if item.get("all_parts") ]

def tokens(oracle_cards):
    return [item for item in oracle_cards if "Token" in item.get("type_line") ]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str)
    parser.add_argument("-f", "--format", type=str)

    args = parser.parse_args()

    with open("oracle-cards.json", encoding="utf8") as oracle_cards_file:
        oracle_cards = json.load(oracle_cards_file)

    db = applicable_cards(oracle_cards)
    token_db = tokens(oracle_cards)

    with open(args.path, encoding="utf8") as decklist_file:
        rows = decklist_file.readlines()

    token_ids = []
    for i in rows:
        token_ids.extend(find_tokens(db, i))

    tokens = []

    for id in list(set(token_ids)):
        found_token = ([ item for item in token_db if item.get("id") == id ])
        if len(found_token) > 0:
            token = found_token[0]
            tokens.append({"name": token["name"], "type": token["type_line"], "colors": token["colors"], "oracle": token["oracle_text"]})

    with open("tokens.json", "w", encoding="utf8") as file:
        json.dump(tokens, file, indent=2)
