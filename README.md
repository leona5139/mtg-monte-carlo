# MTG Arena Monte Carlo Analysis

This project uses Monte Carlo methods to simulate player accounts on *Magic: The Gathering Arena* in order to identify optimal strategies for earning cards and spending money efficiently.

In total, I simulated 1,200 players across 24 different player profiles. I then analyzed the results using statistical tests to determine whether certain strategies or purchases provide statistically significant advantages.

## Results

Online discussions about how to maximize card acquisition on MTG Arena often include recurring advice — such as buying cheaper packs, playing aggressive decks, or strategically spending real money. However, these suggestions are rarely backed by data.

My analysis supports many of these claims. While the findings weren’t surprising, it was satisfying to validate them with actual simulations and statistics.

## Methodology

This project had two main components:

### 1. Simulation

Player simulations were implemented in Python. Each player was represented as an instance of a Python class, with several `pandas` DataFrames used to track variables like card ownership and deck completion progress.

### 2. Analysis

The results were analyzed in R, using Quarto for clean and integrated reporting. Quarto made it easy to combine narrative, tables, and visualizations in a cohesive format.

## Data Sources

- Decklists were sourced from [MTG Goldfish](https://www.mtggoldfish.com)
- Card data was sourced from [MTG JSON](https://mtgjson.com)

---

*Thanks for checking out my project! Feel free to explore the code and reach out if you have questions or ideas.*
