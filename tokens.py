import argparse
import json
import ijson
import time 

def find_token_ids(db, card_name, format):
    if card_name[0:2] == '//' or card_name.rstrip() == "":
        return []
    if format == "justName":
        name = card_name.rstrip()
    else:
        name = " ".join(card_name.rsplit(" ")[1:]).strip()

    if "]" in name:
        name = "".join(name.split("]")[1:]).lstrip()

    card = [item for item in db if item.get("name")==name]
    if len(card) == 0:
        return []
    else:
        tokens = [item for item in card[0]["all_parts"] if item.get("component")=="token"]
        token_ids = []
        for i in tokens:
            token_ids.append(i["id"])

        return token_ids

if __name__ == '__main__':
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str)
    parser.add_argument("-f", "--format", type=str)

    args = parser.parse_args()
    format
    if args.format and args.format == "justName":
        format = "justName"
    else:
        format = "default"

    print("%.2f parse args done" % (time.time() - start))

    db = []
    token_db = []
    with open("default-cards.json", encoding="utf8") as oracle_cards_file:
        for card in ijson.items(oracle_cards_file, "item"):
            if card.get("all_parts"):
                db.append(card)
            if card.get("type_line") and "Token" in card.get("type_line"):
                token_db.append(card)

    print("%.2f read db from file done" % (time.time() - start))

    with open(args.path, encoding="utf8") as decklist_file:
        rows = decklist_file.readlines()

    token_ids = []
    for i in rows:
        token_ids.extend(find_token_ids(db, i, format))
    
    del db
    del decklist_file
    print("%.2f read deck from file done" % (time.time() - start))

    tokens = []

    for id in list(set(token_ids)):
        token = (next(item for item in token_db if item.get("id") == id ))
        if token:
            element = { "name": token["name"]}
            element.update( { "type": token["type_line"].replace("\u2014", "-") } )

            if token.get("colors") and len(token["colors"]) > 0:
                element.update( {"colors": "".join(token["colors"]) })
            else:
                element.update( {"colors": "C" })
            
            if token.get("power"):
                element.update( {"stats": token["power"]+"/"+token["toughness"] })
            
            if token.get("oracle_text"):
                element.update( {"oracle": token["oracle_text"].replace("\u2014", "-")})
            
            if len(next((item for item in tokens if item == element), [])) == 0:
                tokens.append(element)

    print("%.2f token mapping done" % (time.time() - start))

    if len(tokens) > 0:
        tokens = sorted(tokens, key=lambda d: d["name"])
        for i in range(0, len(tokens)):
            tokens[i].update( {"id": i+1})

    with open("tokens.json", "w", encoding="utf8") as file:
        json.dump(tokens, file, indent=2)

    print("%.2f all done" % (time.time() - start))