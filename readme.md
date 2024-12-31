## Usage

Download Oracle cards as default-cards.json from https://scryfall.com/docs/api/bulk-data. Put your decklist to a text-file and run.

```bash
python ./tokens.py -p "decklist.txt"
```

Format options (WIP):

default

```bash
1 Raise the Alarm
1 [BFZ#144] Dragonmaster Outcast
```

`-f justName`

```bash
Raise the Alarm
[BFZ#144] Dragonmaster Outcast
```
