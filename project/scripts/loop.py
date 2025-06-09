from player import Player
import random
import pandas as pd

for buying_strat in ["normal", "mythic"]:#, "draft"]:
    for best_of in ["bo1", "bo3"]:
        for starting in [0,1,2]:
            for main_format in ["standard", "pioneer"]:
                #for winrate in [40,50,60]:
                    winrate = 50
                    if buying_strat != "draft" or starting != 0 or best_of != "bo3":
                        continue
                
                    start = 0

                    headers = ['player_id', 'deck', 'day', 'num_packs']
                    empty_df = pd.DataFrame(columns=headers)
                    empty_df.to_csv(f'./project/data/results/{main_format}_{best_of}_{buying_strat}_{starting}_{winrate}_results.csv', mode='a', index=False)

                    for n in range(start,50):
                        print(f"-----\nPlayer {n}:\n-----\n")    
                        completed = False
                        player = Player(n, main_format, best_of, buying_strat, starting, winrate)

                        headers = ['gold_earned', 'gold_end', 'exp_eanred', 'exp_end', 'vault', 'packs_opened', 'deck_0_completeness', 'deck_1_completeness',
                                'deck_2_completeness', 'deck_3_completeness', 'deck_4_completeness', 'deck_5_completeness', 'deck_6_completeness', 
                                'deck_7_completeness',  'deck_8_completeness', 'deck_9_completeness']
                        empty_df = pd.DataFrame(columns=headers)
                        empty_df.to_csv(f'./project/data/logs/{player.id}_logs.csv', index=False)

                        day = 0

                        while not completed:
                            gold_earned = 0
                            exp_earned = 0
                            day += 1
                            print(f"----- DAY {day} -----")

                            # daily quests
                            roll = random.randint(1,4)
                            if roll == 1:
                                player.gold += 500
                                gold_earned += 500
                                player.exp += 500
                                exp_earned += 500
                                print("Low roll daily quest")
                            else:
                                player.gold += 750
                                gold_earned += 750
                                player.exp += 500
                                exp_earned += 500
                                print("High roll daily quest")

                            # daily wins
                            player.gold += 550
                            gold_earned += 550
                            # weekly wins (4 per week, up to 15)
                            if day%7 == 1 or day%7 == 2 or day%7 == 3:
                                player.exp += 4*250
                                exp_earned += 4*250
                                print("1000 exp from weekly wins")
                            elif day%7 == 4:
                                player.exp += 3*250
                                exp_earned += 3*250
                                print("1000 exp from weekly wins")

                            # check mastery pass progress
                            player.update_mastery_pass()

                            # buy packs/play draft if possible
                            if player.buying_strat == "normal":
                                while player.gold >= 1000:
                                    optimal_set = player.find_optimal_pack()
                                    print(f"Bought normal {optimal_set} pack with gold")
                                    player.gold -= 1000
                                    player.open_pack(optimal_set)
                                while player.gems >= 200:
                                    optimal_set = player.find_optimal_pack()
                                    print(f"Bought normal {optimal_set} pack with gems")
                                    player.gems -= 200
                                    player.open_pack(optimal_set)

                            elif player.buying_strat == "mythic":
                                while player.gold >= 1300:
                                    optimal_set = player.find_optimal_pack()
                                    print(f"Bought mythic {optimal_set} pack with gold")
                                    player.gold -= 1300
                                    player.open_pack(optimal_set, "mythic")
                                while player.gems >= 260:
                                    optimal_set = player.find_optimal_pack()
                                    print(f"Bought mythic {optimal_set} pack with gems")
                                    player.gems -= 260
                                    player.open_pack(optimal_set, "mythic")
                            

                            # elif player.buying_strat == "draft":
                            #     if player.main_format == "standard":
                            #         set_list = ["TDM","DFT","FDN","DSK","BLB","OTJ","MKM","LCI","WOE","MAT","MOM","ONE","BRO","DMU"]
                            #     else:
                            #         set_list = ["TDM","DFT","PIO","FDN","DSK","BLB","OTJ","MKM","KTK","SIR","LCI","WOE","MAT","MOM","ONE","BRO","DMU","SNC","NEO","MID","VOW","AFR","STX","KHM","KLR","ZNR","AKR","M21","IKO","THB","ELD","M20","WAR","RNA","GRN","DOM","RIX","XLN","M19"]
                                
                            #     selected_set = random.choice(set_list)

                            #     while player.gold >= 10000:
                            #         print(f"Drafted {selected_set} with gold")
                            #         player.gold -= 10000
                            #         player.play_draft(selected_set)
                            #     while player.gems >= 1500:
                            #         print(f"Drafted {selected_set} with gems")
                            #         player.gems -= 1500
                            #         player.play_draft(selected_set)

                            # open vault
                            if player.vault >= 1000:
                                print("Opened vault")
                                player.wild_cards["u"] += 3
                                player.wild_cards["r"] += 2
                                player.wild_cards["m"] += 1
                                
                            player.update_deck_completion()

                            # log activities for day
                            logs = pd.DataFrame({
                            'gold_earned': gold_earned,
                            'gold_end': player.gold,
                            'exp_earned': exp_earned,
                            'exp_end': player.exp,
                            'vault': player.vault,
                            'packs_opened': player.num_packs,
                            'deck_0_completeness': player.deck_completion['completeness'].iloc[0],
                            'deck_1_completeness': player.deck_completion['completeness'].iloc[1],
                            'deck_2_completeness': player.deck_completion['completeness'].iloc[2],
                            'deck_3_completeness': player.deck_completion['completeness'].iloc[3],
                            'deck_4_completeness': player.deck_completion['completeness'].iloc[4],
                            'deck_5_completeness': player.deck_completion['completeness'].iloc[5],
                            'deck_6_completeness': player.deck_completion['completeness'].iloc[6],
                            'deck_7_completeness': player.deck_completion['completeness'].iloc[7],
                            'deck_8_completeness': player.deck_completion['completeness'].iloc[8],
                            'deck_9_completeness': player.deck_completion['completeness'].iloc[9],
                            }, index = [0])
                            logs.to_csv(f'./project/data/logs/{player.id}_logs.csv', mode = 'a', index=False, header=False)

                            # check to see if finished
                            if player.deck_completion["completeness"].max() >= 1:
                                completed = True

                                results = pd.DataFrame({
                                'player_id': [n],
                                'deck': [player.deck_completion["completeness"].idxmax()],
                                'day': [day],
                                'packs_opened': [player.num_packs]
                                })
                                results.to_csv(f'./project/data/results/{player.main_format}_{player.best_of}_{player.buying_strat}_{player.starting}_{player.winrate}_results.csv', mode='a', index=False, header=False)
                            