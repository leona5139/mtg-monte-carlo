import pandas as pd

full_cards = pd.read_csv("./project/data/cards/cards.csv")

# create a file of only cards on arena
set_list = {"YTDM",
            "TDM",
            "YDFT",
            "DFT",
            "PIO",
            "FDN",
            "YDSK",
            "DSK",
            "YBLB",
            "BLB",
            "MH3",
            "YOTJ",
            "OTJ",
            "MKM",
            "YMKM",
            "KTK",
            "YLCI",
            "LCI",
            "YWOE",
            "WOE",
            "LTR",
            "MAT",
            "YMOM",
            "MOM",
            "SIR",
            "YONE",
            "ONE",
            "YBRO",
            "BRO",
            "YDMU",
            "DMU",
            "HBG",
            "YSNC",
            "SNC",
            "YNEO",
            "NEO",
            "YMID",
            "MID",
            "VOW",
            "AFR",
            "STX",
            "KHM",
            "KLR",
            "ZNR",
            "AKR",
            "M21",
            "IKO",
            "THB",
            "ELD",
            "M20",
            "WAR",
            "RNA",
            "GRN",
            "DOM",
            "RIX",
            "XLN",
            "M19",
            "ANB"}

def has_matching_set(set_str):
    card_sets = {s.strip() for s in set_str.split(',')}
    return not set_list.isdisjoint(card_sets)

arena_cards = full_cards[full_cards['printings'].apply(has_matching_set)]

arena_cards = arena_cards[arena_cards['name'].str.count(r' // ') < 2]

columns_of_interest = ['name', 'printings', 'rarity']

arena_cards = arena_cards[columns_of_interest]

arena_cards = arena_cards.drop_duplicates(subset='name')

print(arena_cards.head())

arena_cards.to_csv("./project/data/cards/cards_arena.csv", index=False)

# create an individual file for cards in each set on arena
for set_code in set_list:
    def in_this_set(printings):
        return set_code in {s.strip() for s in printings.split(',')}
    
    cards_in_set = arena_cards[arena_cards['printings'].apply(in_this_set)]

    cards_in_set = cards_in_set[['name', 'rarity']]

    if not cards_in_set.empty:
        cards_in_set.to_csv(f"./project/data/cards/cards_{set_code}.csv", index=False)