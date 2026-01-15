# MTG Arena Monte Carlo Analysis

This project uses Monte Carlo methods to simulate player accounts on *Magic: The Gathering Arena* in order to identify optimal strategies for earning cards and spending money efficiently.

# Technologies
- `Python`
- `pandas`
- `R`
- `Quardo`

# The Process
The first step was to intialized the full card collection for Magic cards on Arena and the possible deck lists that the simulated players will try to complete.

The next step was creating a player class that initiates a strategy (what format do they play?, what is their strategy for spending gold?, are they willing to pay money?). It also tacks important information such as current balance of currencies, current card collection, current progress towards decks etc.

Each player is then run through a loop that simulates a day of playing Magic on Arena where they will complete quests, get their daily wins, and then open packs if they can afford them. The pack choice attempts to pick the best possible pack for deck completion likelihood and the pack opening logic fully follows the published odds from Wizards of the Coast, and has the correctly implemented pity system. 

Finally, after all of the simulations were complete (a total of ~1200 simulations across 24 player profiles), I conducted statistical analysis using R and created a writeup using quardo which can be found here [online](https://leona5139.github.io/mtg-monte-carlo/mtga_report.html).

### Data Sources

- Decklists were sourced from [MTG Goldfish](https://www.mtggoldfish.com)
- Card data was sourced from [MTG JSON](https://mtgjson.com)

# What I Learned
## The importance of efficient data storage
Becuase I intended to simulate many many instances of players, it became extremely important for me to have efficient data structures since any slowness would quickly compound. This quickly pushed me towards using `pandas` to efficiently store card and deck information in a way that was both easy and computationally quick to access. 

## The importance of parameterizing code
Over the course of this project, I simulated 24 different player profiles. In the initial versions of this code, I had many of the values hard coded which meant that for each batch of simulations I would have to go through and maually update many values. This both took a lot of time, and also meant that I was restricted to relatively small batch sizes for the simulations. However, by parameterizing my code, I was instead able to run much larger batches that made the overall simulation process much easier.

## The power of simulations
I have played Magic Arena for a long time, and I have personally tried many strategies to optimize my currency efficiency based on various guides I had found on YouTube or discussions I had found on forums. The problem with these strategies though was that they didn't have any evidence to support them, and we merely based on "intuition". However, by simulating the strategies, I was instead able to make data driven decisions about optimal strategies without playing a single game of Magic.

## Overall Growth
This was the first project that I fully implemented end-to-end without any external help or direction such as from a class or a tutorial. It was both an interesting and challenging experience to go through the entire process of formulating a project idea, to selecting the best methodologies, to actually executing my plans. This project helped to really cement the ideas that I have learned in the classroom, and gave me the confidence to pursue even more personal projects of grander scale.

# How It Could Be Improved
- Add a player profile that sometimes chooses to draft instead of just opening packs (would require both simulation of opening draft packs and a decision making algorithm for card selection)
- Investigating the benefits of paying for in game currency beyond the initial new player deals
- Add a feature to update the card pools and decklists according to the current set/meta
- Add a player profile that builds an interim budget deck on the way to building a full price deck
- Investigate optimal spending strategies for long term account health rather than just building a single deck


*Thanks for checking out my project! Feel free to explore the code and reach out if you have questions or ideas.*
