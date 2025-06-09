import pandas as pd
import random
import numpy as np

class Player:
    def __init__(self, num, main_format, best_of, buying_strat, starting, win_rate):
        # set profile
        self.main_format = main_format
        self.best_of = best_of
        self.buying_strat = buying_strat
        self.winrate = win_rate
        self.id = f'{main_format}_{best_of}_{buying_strat}_{starting}_{win_rate}_{num}'
        self.num_packs = 0
        self.starting = starting

        # set initial conditions
        self.day = 0
        self.wild_cards = {'c':10,
                           'u':5,
                           'r':0,
                           'm':0}
        self.rare_track = 1
        self.mythic_track = 1
        self.uncommon_track = 4    

        # initialize collection
        self.initialize_collection()

        # set starting currency
        self.gold = 2000
        self.exp = 0
        self.vault = 0
        self.mastery_pass_lvl = 1
        if self.starting == 0:
            self.gems = 0
            self.mastery_pass = False
        elif self.starting == 1:
            self.gems = 1500
            self.mastery_pass = False
            for i in range(5):
                self.open_pack("FDN")
        elif self.starting == 2:
            self.gems = 3500-3400
            self.mastery_pass = True


    def find_optimal_pack(self):
        # max_copies_needed × 
        # rarity_factor (should scale based on proportion of rarities given in a pack) × 
        # best_deck_completion_percentage × 
        # cross_decks_factor (1 + 1/2 × (number_of_decks_using_card_i - 1)
        if self.main_format == "standard":
            set_list = ["TDM","DFT","FDN","DSK","BLB","OTJ","MKM","LCI","WOE","MAT","MOM","ONE","BRO","DMU"]
        elif self.main_format == "pioneer":
            set_list = ["TDM","DFT","PIO","FDN","DSK","BLB","OTJ","MKM","KTK","SIR","LCI","WOE","MAT","MOM","ONE","BRO","DMU","SNC","NEO","MID","VOW","AFR","STX","KHM","KLR","ZNR","AKR","M21","IKO","THB","ELD","M20","WAR","RNA","GRN","DOM","RIX","XLN","M19"]
        elif self.main_format == "historic_brawl":
            set_list = ["YTDM","TDM","YDFT","DFT","PIO","FDN","YDSK","DSK","YBLB","BLB","MH3","YOTJ","OTJ","MKM","YMKM","KTK","YLCI","LCI","YWOE","WOE","LTR","MAT","YMOM","MOM","SIR","YONE","ONE","YBRO","BRO","YDMU","DMU","HBG","YSNC","SNC","YNEO","NEO","YMID","MID","VOW","AFR","STX","KHM","KLR","ZNR","AKR","M21","IKO","THB","ELD","M20","WAR","RNA","GRN","DOM","RIX","XLN","M19","ANB"]

        best_pack = ''
        best_ev = 0
        for s in set_list:
            ev = 0 
            cards = pd.read_csv(f"./project/data/cards/cards_{s}.csv")
            cards = cards['name']
            for c in cards:
                # max needed
                try:
                    max_need = self.collection_need.loc[self.collection_need['name'] == c, 'max_need'].item()
                except:
                    continue
                # rarity factor
                rarity = self.collection_full.loc[self.collection_full['name'] == c, 'rarity'].item()
                if rarity == 'common':
                    rarity_factor = 1
                elif rarity == 'uncommon':
                    rarity_factor = 2.5
                elif rarity == 'rare':
                    rarity_factor = 5
                elif rarity == 'mythic':
                    rarity_factor = 35

                # best deck completion
                decks_in = self.collection_need.loc[self.collection_need['name'] == c, 'included_in'].item()
                decks_in = np.unique(decks_in.split(',')[0:-1])
                best_completion = 0
                for d in decks_in:
                    completion = self.deck_completion.loc[self.deck_completion['deck'] == int(d[-1]), 'completeness'].item()
                    if completion > best_completion:
                        best_completion = completion

                # cross deck factor
                cross_deck = len(decks_in)

                ev += max_need*rarity_factor*best_completion*(1+0.5*cross_deck)

            #print(s, ev)
            if ev >= best_ev:
                best_pack = s
                best_ev = ev

        return best_pack
        

    def open_pack(self, selected_set, pack="normal"):
        print(f"--- Opening {pack} {selected_set} ---")
        self.num_packs += 1
        if pack != "draft":
            self.rare_track += 1
            self.mythic_track += 1
            if self.rare_track >= 6:
                if self.mythic_track >= 30:
                    self.wild_cards["m"] += 1
                    self.mythic_track = 0
                else:
                    self.wild_cards["r"] += 1
                self.rare_track = 0

            self.uncommon_track += 1
            if self.uncommon_track >= 6:
                self.wild_cards["u"] += 1
                self.uncommon_track = 0
            
        if pack == "normal" or pack == "mythic":
            # select commons
            for c in range(5):
                if c == 0:
                    wild = random.randint(1,3)
                    if wild == 1:
                        self.wild_cards['c'] += 1
                        continue

                commons = pd.read_csv(f"./project/data/cards/cards_{selected_set}.csv")
                commons = commons.loc[commons['rarity'] == "common", 'name']
                if len(commons) == 0:
                    break
                
                while True:
                    try:
                        selection = random.randint(0,len(commons)-1)
                        card = commons.iloc[selection]
                        #print(self.collection_full.loc[self.collection_full['name'] == card, 'count'])

                        if self.collection_full.loc[self.collection_full['name'] == card, 'count'].item() >= 4: # duplicate protection
                            self.vault += 1
                        else:
                            self.collection_full.loc[self.collection_full['name'] == card, 'count'] += 1
                            if card in self.collection_need['name'].values:
                                self.collection_need.loc[self.collection_need['name'] == card, 'count'] += 1
                            
                            print("Selected: " + card)
                            break
                    except:
                        continue

            # select uncommons        
            for u in range(2):
                if u == 0:
                    wild = random.randint(1,5)
                    if wild == 1:
                        self.wild_cards['c'] += 1
                        continue
                uncommons = pd.read_csv(f"./project/data/cards/cards_{selected_set}.csv")
                uncommons = uncommons.loc[uncommons['rarity'] == "uncommon", 'name']

                
                while True:
                    try:
                        selection = random.randint(0,len(uncommons)-1)
                        card = uncommons.iloc[selection]
                        #print(self.collection_full.loc[self.collection_full['name'] == card, 'count'])
                        if self.collection_full.loc[self.collection_full['name'] == card, 'count'].item() >= 4: # duplicate protection
                            self.vault += 3
                        else:
                            self.collection_full.loc[self.collection_full['name'] == card, 'count'] += 1
                            if card in self.collection_need['name'].values:
                                self.collection_need.loc[self.collection_need['name'] == card, 'count'] += 1
                            
                            print("Selected: " + card)
                            break
                    except:
                        continue

            # check if rare gets upgraded (odds determined by set)
            upgrade = False
            if set == "YMID":
                upgrade_roll = random.randint(1,94)
                if upgrade_roll <= 10:
                    upgrade = True
            elif selected_set == "YNEO":
                upgrade_roll = random.randint(1,9)
                if upgrade_roll == 1:
                    upgrade = True
            elif selected_set in ["XLN", "RIX", "DOM", "M19", "GRN", "RNA", "WAR", "M20", "ELD", "THB", "IKO", "M21", "STX", "NEO", "KTK","MKM"]:
                upgrade_roll = random.randint(1,8)
                if upgrade_roll == 1:
                    upgrade = True
            elif selected_set in ["ZNR", "KHM", "MID", "VOW"]:
                upgrade_roll = random.randint(1,74)
                if upgrade_roll <= 10:
                    upgrade = True
            elif selected_set in ["KLR", "AFR", "SNC", "YSNC", "HBG", "DMU", "ONE", "YONE", "LTR", "WOE", "YWOE", "YLCI", "YMKM", "OTJ", "MH3", "BLB", "YBLB", "DSK", "YDSK", "FDN", "DFT", "YDFT", "TDM", "YTDM"]:
                upgrade_roll = random.randint(1,7)
                if upgrade_roll == 1:
                    upgrade = True
            elif selected_set == "SIR":
                upgrade_roll = random.randint(1,65)
                if upgrade_roll <= 10:
                    upgrade = True        
            elif selected_set in ["AKR", "MOM"]:
                upgrade_roll = random.randint(1,6)
                if upgrade_roll == 1:
                    upgrade = True
            elif selected_set == "LCI":
                upgrade_roll = random.randint(1,68)
                if upgrade_roll <= 10:
                    upgrade = True
            elif selected_set == "BRO":
                upgrade_roll = random.randint(1,58)
                if upgrade_roll <= 10:
                    upgrade = True
            elif selected_set == "YBRO":
                upgrade_roll = random.randint(1,5)
                if upgrade_roll == 1:
                    upgrade = True

            if upgrade == False and pack != "mythic":
                # select rare
                wild = random.randint(1,30)
                if wild == 1:
                    self.wild_cards['r'] += 1
                else:
                    # select rare
                    rares = pd.read_csv(f"./project/data/cards/cards_{selected_set}.csv")
                    rares = rares.loc[rares['rarity'] == "rare", 'name']
                    while True:
                        try:
                            selection = random.randint(0,len(rares)-1)
                            card = rares.iloc[selection]
                            #print(self.collection_full.loc[self.collection_full['name'] == card, 'count'])
                        
                            if self.collection_full.loc[self.collection_full['name'] == card, 'count'].item() >= 4: # duplicate protection
                                continue
                            else:
                                self.collection_full.loc[self.collection_full['name'] == card, 'count'] += 1
                                if card in self.collection_need['name'].values:
                                    self.collection_need.loc[self.collection_need['name'] == card, 'count'] += 1
                                
                                print("Selected: " + card)
                                break
                        except:
                            continue
            else:
                # select mythic
                wild = random.randint(1,30)
                if wild == 1:
                    if pack == "mythic":
                        self.wild_cards['r'] += 1
                    else:
                        self.wild_cards['m'] += 1
                else:
                    # select mythic
                    mythics = pd.read_csv(f"./project/data/cards/cards_{selected_set}.csv")
                    mythics = mythics.loc[mythics['rarity'] == "mythic", 'name']
                    while True:
                        try:
                            selection = random.randint(0,len(mythics)-1)
                            card = mythics.iloc[selection]
                            #print(self.collection_full.loc[self.collection_full['name'] == card, 'count'])
                        
                            if self.collection_full.loc[self.collection_full['name'] == card, 'count'].item() >= 4: # duplicate protection
                                continue
                            else:
                                self.collection_full.loc[self.collection_full['name'] == card, 'count'] += 1
                                if card in self.collection_need['name'].values:
                                    self.collection_need.loc[self.collection_need['name'] == card, 'count'] += 1
                                
                                print("Selected: " + card)
                                break
                        except:
                            continue
        
        elif pack == "golden":
            set_list = ["TDM","DFT","DSK","BLB","OTJ","MKM","LCI","WOE","MOM","ONE","BRO","DMU"]
            rares = pd.Series(dtype=object)
            last_2_rares = pd.Series(dtype=object)
            mythics = pd.Series(dtype=object)
            last_2_mythics = pd.Series(dtype=object)
            for s in set_list:
                cards = pd.read_csv(f"./project/data/cards/cards_{s}.csv")
                rares = pd.concat([rares,cards.loc[cards['rarity'] == "rare", 'name']])
                mythics = pd.concat([mythics,cards.loc[cards['rarity'] == "mythic", 'name']])
                if s == "TDM" or s == "DFT":
                    last_2_rares = pd.concat([last_2_rares,cards.loc[cards['rarity'] == "rare", 'name']])
                    last_2_mythics = pd.concat([last_2_mythics,cards.loc[cards['rarity'] == "mythic", 'name']])

            for c in range(2):
                last_upgrade = random.randint(1,6)
                if last_upgrade == 1:
                    while True:
                            try:
                                selection = random.randint(0,len(last_2_mythics)-1)
                                card = last_2_mythics.iloc[selection]
                            
                                if self.collection_full.loc[self.collection_full['name'] == card, 'count'].item() >= 4: # duplicate protection
                                    continue
                                else:
                                    self.collection_full.loc[self.collection_full['name'] == card, 'count'] += 1
                                    if card in self.collection_need['name'].values:
                                        self.collection_need.loc[self.collection_need['name'] == card, 'count'] += 1
                                    
                                    print("Selected: " + card)
                                    break
                            except:
                                continue
                else:
                    while True:
                            try:
                                selection = random.randint(0,len(last_2_rares)-1)
                                card = last_2_rares.iloc[selection]
                            
                                if self.collection_full.loc[self.collection_full['name'] == card, 'count'].item() >= 4: # duplicate protection
                                    continue
                                else:
                                    self.collection_full.loc[self.collection_full['name'] == card, 'count'] += 1
                                    if card in self.collection_need['name'].values:
                                        self.collection_need.loc[self.collection_need['name'] == card, 'count'] += 1
                                    
                                    print("Selected: " + card)
                                    break
                            except:
                                continue

            for c in range(3):
                upgrade = random.randint(1,6)
                if upgrade == 1:
                    while True:
                            try:
                                selection = random.randint(0,len(last_2_mythics)-1)
                                card = mythics.iloc[selection]
                            
                                if self.collection_full.loc[self.collection_full['name'] == card, 'count'].item() >= 4: # duplicate protection
                                    continue
                                else:
                                    self.collection_full.loc[self.collection_full['name'] == card, 'count'] += 1
                                    if card in self.collection_need['name'].values:
                                        self.collection_need.loc[self.collection_need['name'] == card, 'count'] += 1
                                    
                                    print("Selected: " + card)
                                    break
                            except:
                                continue
                else:
                    while True:
                            try:
                                selection = random.randint(0,len(last_2_rares)-1)
                                card = rares.iloc[selection]
                            
                                if self.collection_full.loc[self.collection_full['name'] == card, 'count'].item() >= 4: # duplicate protection
                                    continue
                                else:
                                    self.collection_full.loc[self.collection_full['name'] == card, 'count'] += 1
                                    if card in self.collection_need['name'].values:
                                        self.collection_need.loc[self.collection_need['name'] == card, 'count'] += 1
                                    
                                    print("Selected: " + card)
                                    break
                            except:
                                continue
        
            while True:
                    try:
                        selection = random.randint(0,len(last_2_mythics)-1)
                        card = mythics.iloc[selection]
                    
                        if self.collection_full.loc[self.collection_full['name'] == card, 'count'].item() >= 4: # duplicate protection
                            continue
                        else:
                            self.collection_full.loc[self.collection_full['name'] == card, 'count'] += 1
                            if card in self.collection_need['name'].values:
                                self.collection_need.loc[self.collection_need['name'] == card, 'count'] += 1
                            
                            print("Selected: " + card)
                            break
                    except:
                        continue
        
        elif pack == "draft":
            # select commons
            for c in range(8):
                commons = pd.read_csv(f"./project/data/cards/cards_{selected_set}.csv")
                commons = commons.loc[commons['rarity'] == "common", 'name']
                if len(commons) == 0:
                    break

                while True:
                    try:
                        selection = random.randint(0,len(commons)-1)
                        card = commons.iloc[selection]
                    #print(self.collection_full.loc[self.collection_full['name'] == card, 'count'])
                    
                        self.collection_full.loc[self.collection_full['name'] == card, 'count'] += 1
                        if card in self.collection_need['name'].values:
                            self.collection_need.loc[self.collection_need['name'] == card, 'count'] += 1
                        
                        print("Selected: " + card)
                        break
                    except:
                        continue

            # select uncommons        
            for u in range(3):
                uncommons = pd.read_csv(f"./project/data/cards/cards_{selected_set}.csv")
                uncommons = uncommons.loc[uncommons['rarity'] == "uncommon", 'name']
                while True:
                    try:
                        selection = random.randint(0,len(uncommons)-1)
                        card = uncommons.iloc[selection]
                        #print(self.collection_full.loc[self.collection_full['name'] == card, 'count'])
                    
                        self.collection_full.loc[self.collection_full['name'] == card, 'count'] += 1
                        if card in self.collection_need['name'].values:
                            self.collection_need.loc[self.collection_need['name'] == card, 'count'] += 1
                        
                        print("Selected: " + card)
                        break
                    except:
                        continue

            # check if rare gets upgraded (odds determined by set)
            upgrade = False
            upgrade_roll = random.randint(1,7)
            if upgrade_roll == 1:
                upgrade = True

            if upgrade == False:
                # select rare
                rares = pd.read_csv(f"./project/data/cards/cards_{selected_set}.csv")
                rares = rares.loc[rares['rarity'] == "rare", 'name']
                while True:
                    try:
                        selection = random.randint(0,len(rares)-1)
                        card = rares.iloc[selection]
                        #print(self.collection_full.loc[self.collection_full['name'] == card, 'count'])
                    
                        self.collection_full.loc[self.collection_full['name'] == card, 'count'] += 1
                        if card in self.collection_need['name'].values:
                            self.collection_need.loc[self.collection_need['name'] == card, 'count'] += 1
                            
                        print("Selected: " + card)
                        break
                    except:
                        continue
            else:
                # select mythic
                mythics = pd.read_csv(f"./project/data/cards/cards_{selected_set}.csv")
                mythics = mythics.loc[mythics['rarity'] == "mythic", 'name']
                while True:
                    try:
                        selection = random.randint(0,len(mythics)-1)
                        card = mythics.iloc[selection]
                        #print(self.collection_full.loc[self.collection_full['name'] == card, 'count'])
                                            
                        self.collection_full.loc[self.collection_full['name'] == card, 'count'] += 1
                        if card in self.collection_need['name'].values:
                            self.collection_need.loc[self.collection_need['name'] == card, 'count'] += 1
                        
                        print("Selected: " + card)
                        break
                    except:
                        continue

    def open_icr(self,rarity):
        cards = pd.read_csv(f"./project/data/cards/cards_TDM.csv")   
        options = cards.loc[cards['rarity'] == rarity, 'name']
        while True:
            try:
                selection = random.randint(0,len(options)-1)
                card = options.iloc[selection]
            
                if self.collection_full.loc[self.collection_full['name'] == card, 'count'].item() >= 4: # duplicate protection
                    if rarity == 'uncommon':
                        self.wild_cards['u'] += 1
                    else:
                        continue
                else:
                    self.collection_full.loc[self.collection_full['name'] == card, 'count'] += 1
                    if card in self.collection_need['name'].values:
                        self.collection_need.loc[self.collection_need['name'] == card, 'count'] += 1
                    
                    print("Selected: " + card)
                    break
            except:
                continue     

    def update_deck_completion(self):
        for d in self.deck_completion["deck"]:
            needed_c = 0
            needed_u = 0
            needed_r = 0
            needed_m = 0
            for index,row in self.collection_need.iterrows():
                card = row['name']
                rarity = self.collection_full.loc[self.collection_full['name'] == card, 'rarity'].item()
                if rarity == 'common':
                    needed_c += max(0,row[f'deck_{d}']-row['collected'])
                elif rarity == 'uncommon':
                    needed_u += max(0,row[f'deck_{d}']-row['collected'])
                elif rarity == 'rare':
                    needed_r += max(0,row[f'deck_{d}']-row['collected'])
                else:
                    needed_m += max(0,row[f'deck_{d}']-row['collected'])

            needed_c = max(0,needed_c - self.wild_cards['c'])
            needed_u = max(0,needed_u - self.wild_cards['u'])
            needed_r = max(0,needed_r - self.wild_cards['r'])
            needed_m = max(0,needed_m - self.wild_cards['m'])
            
            needed_total = needed_c + needed_u + needed_r + needed_m
            
            if self.best_of == "bo1":
                completeness = 1 - needed_total/60
            elif self.main_format == "historic_brawl":
                if d == 3:
                    completeness = 1-needed_total/54
                else:
                    completeness = 1- needed_total/100
            else:
                completeness = 1 - needed_total/75

            self.deck_completion.loc[self.deck_completion["deck"] == d, "completeness"] = completeness

    def initialize_collection(self):
        self.collection_full = pd.read_csv('./project/data/cards/cards_arena.csv')
        self.collection_full['count'] = 0

        self.collection_need = pd.DataFrame(columns = ['name','deck_0','deck_1','deck_2','deck_3','deck_4','deck_5','deck_6','deck_7','deck_8','deck_9','collected','max_need','included_in'])

        # for loop going through decks to fill out collection_need
        for j in range(0,10):
            needed_cards = pd.read_csv(f'./project/data/decks/{self.main_format}_{self.best_of}_deck{j}.csv', header = None)
            for index,row in needed_cards.iterrows():
                count = row.iloc[0]
                name = row.iloc[1]
                # add card if not already present
                if name not in self.collection_need['name'].values:
                    new_row = pd.DataFrame([[name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '']], columns=self.collection_need.columns)
                    self.collection_need = pd.concat([self.collection_need, new_row], ignore_index=True)
                
                # update needs for card in decks
                self.collection_need.loc[self.collection_need['name']==name,f'deck_{j}'] += count
                self.collection_need.loc[self.collection_need['name']==name,f'included_in'] += f'deck_{j},'

                # update max need if necessary
                max_need = self.collection_need.loc[self.collection_need['name'] == name, 'max_need'].item()
                current_need = self.collection_need.loc[self.collection_need['name'] == name, f'deck_{j}'].item()
                if current_need > max_need:
                    self.collection_need.loc[self.collection_need['name'] == name, 'max_need'] = current_need
                

        # for loop going through cards_starter.csv to fill out both collection_full and collection_need
        cards_starter = pd.read_csv("./project/data/cards/cards_starter.csv")
        self.collection_full['collected'] = 0
        for index,row in cards_starter.iterrows():
            self.collection_full.loc[self.collection_full['name']==row['name'], 'collected'] = row['count']
            try:
                self.collection_need.loc[self.collection_need['name']==row['name'], 'collected'] = row['count']
            except:
                pass

        # go through initial packs to also instantiate the collection
        initial_packs = ["WOE", "WOE", "WOE",
         "OTJ", "OTJ", "OTJ",
         "FDN", "FDN", "FDN",
         "BLB", "BLB", "BLB",
         "YDFT", "YDFT", "YDFT",
         "MKM", "MKM", "MKM",
         "MOM", "MOM", "MOM",
         "YBLB", "YBLB", "YBLB",
         "YDSK", "YDSK", "YDSK",
         "MH3", "MH3", "MH3",
         "YTDM", "YTDM", "YTDM",
         "LCI", "LCI", "LCI",
         "DFT", "DFT", "DFT",
         "ONE", "ONE", "ONE",
         "DSK", "DSK", "DSK",
         "YOTJ", "YOTJ", "YOTJ",
         "PIO", "PIO", "PIO",
         "TDM", "TDM", "TDM",
         "MAT", "MAT", "MAT",
         "YBRO", "YBRO", "YBRO", "YBRO", "YBRO", "YBRO"
        ]
        
        pack_num = 1
        for p in initial_packs:
            print(f"Opening initial pack {pack_num}/63: {p}")
            pack_num += 1
            self.open_pack(p)

        self.deck_completion = pd.DataFrame({
            'deck': list(range(10)),
            'completeness': [0] * 10
        })

        self.update_deck_completion()
        print(f"Collection initialized for player {self.id}")

    def update_mastery_pass(self):
        while self.exp >= 1000:
            self.exp -= 1000
            self.mastery_pass_lvl += 1
            if self.mastery_pass_lvl%2 == 0:
                self.open_pack("TDM")
            if self.mastery_pass:
                if self.mastery_pass_lvl == 2:
                    self.open_pack("TDM")
                elif self.mastery_pass_lvl == 5:
                    self.open_pack("DFT")
                elif self.mastery_pass_lvl == 7:
                    self.open_icr("mythic")
                elif self.mastery_pass_lvl == 9:
                    self.open_pack("FDN")
                elif self.mastery_pass_lvl == 10:
                    self.gold += 1000
                elif self.mastery_pass_lvl == 12:
                    self.open_pack("DSK")
                elif self.mastery_pass_lvl == 14:
                    self.open_icr("mythic")
                elif self.mastery_pass_lvl == 16:
                    self.open_pack("BLB")
                elif self.mastery_pass_lvl == 19:
                    self.open_pack("TDM")
                elif self.mastery_pass_lvl == 21:
                    self.open_icr("mythic")
                elif self.mastery_pass_lvl ==23:
                    self.open_pack("DFT")
                elif self.mastery_pass_lvl == 26:
                    self.open_pack("FDN")
                elif self.mastery_pass_lvl == 28:
                    self.open_icr("mythic")
                elif self.mastery_pass_lvl == 29:
                    self.gems += 400
                elif self.mastery_pass_lvl == 30:
                    self.open_pack("DSK")
                elif self.mastery_pass_lvl == 32:
                    self.open_pack("BLB")
                elif self.mastery_pass_lvl == 34:
                    self.gold += 1000
                elif self.mastery_pass_lvl == 35:
                    self.open_icr("mythic")
                elif self.mastery_pass_lvl == 37:
                    self.open_pack("TDM")
                elif self.mastery_pass_lvl ==40:
                    self.open_pack("DFT")
                elif self.mastery_pass_lvl == 41:
                    self.gems += 400
                elif self.mastery_pass_lvl == 42:
                    self.open_icr('mythic')
                elif self.mastery_pass_lvl == 44:
                    self.open_pack("FDN")
                elif self.mastery_pass_lvl == 47:
                    self.open_pack("DSK")
                elif self.mastery_pass_lvl == 48:
                    self.gold += 1000
                elif self.mastery_pass_lvl == 49:
                    self.open_icr('mythic')
                elif self.mastery_pass_lvl == 51:
                    self.open_pack('BLB')
                elif self.mastery_pass_lvl == 54:
                    self.open_pack('TDM')
                elif self.mastery_pass_lvl == 55:
                    self.gems += 400
                elif self.mastery_pass_lvl == 56:
                    self.open_icr('mythic')
                elif self.mastery_pass_lvl == 58:
                    self.open_pack('DFT')
                elif self.mastery_pass_lvl == 61:
                    self.open_pack('FDN')
                elif self.mastery_pass_lvl == 62:
                    self.gold += 1000
                elif self.mastery_pass_lvl == 63:
                    self.open_icr('mythic')
                elif self.mastery_pass_lvl == 65:
                    self.open_pack('DSK')
                elif self.mastery_pass_lvl == 68:
                    self.open_pack('BLB')
                elif self.mastery_pass_lvl == 70:
                    self.open_icr('mythic')
                elif self.mastery_pass_lvl > 70:
                    upgrade = random.randint(1,20)
                    if upgrade == 1:
                        self.open_icr('rare')
                    else:
                        self.open_icr('uncommon')
        self.update_deck_completion()


    def play_draft(self, selected_set):
        self.open_pack(selected_set, "draft")
        self.open_pack(selected_set, "draft")
        self.open_pack(selected_set, "draft")

        wins = 0
        losses = 0
        while losses < 3 and wins < 7:
            roll = random.randint(1,100)
            if roll <= self.winrate:
                wins += 1
            else:
                losses += 1
        if wins == 0:
            self.gems += 50
            packs = 1
        elif wins == 1:
            self.gems += 100
            packs = 1
        elif wins == 2:
            self.gems += 250
            packs = 2
        elif wins == 3:
            self.gems += 1000
            packs = 2
        elif wins == 4:
            self.gems += 1400
            packs = 3
        elif wins == 5:
            self.gems += 1600
            packs = 4
        elif wins == 6:
            self.gems += 1800
            packs = 5
        elif wins == 7:
            self.gems += 2200
            packs = 6

        for p in range(packs):
            self.open_pack(selected_set)