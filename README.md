# Monte Carlo Simulation for Retirement Savings

This Python script simulates the growth of retirement savings using a Monte Carlo method. It estimates potential outcomes of different investment scenarios by running numerous simulations, each with varying market conditions. The script helps model the impact of factors such as annual returns, volatility, and time horizons on retirement savings outcomes.

## Requirements

To run this script, you'll need:

- Python 3.x
- `matplotlib` for plotting the simulation results

You can install the necessary Python packages by running:

```bash
pip install matplotlib

```
## How to Use

### 1. Download or Clone the Repository

Make sure that you have all the required files, including the script and the data files (described below).

## 2. Place Data Files Correctly

The input data files should be placed in the `text_files/data_files/` directory. These files contain historical percentage returns and must be in plain text format, with one percentage per line. The files required are:

- `10-yr_TBond_returns_1926-2013_pct.txt`
- `SP500_returns_1926-2013_pct.txt`
- `S-B-C_blend_1926-2013_pct.txt`
- `S-B_blend_1926-2013_pct.txt`
- `annual_infl_rate_1926-2013_pct.txt`

Ensure that these files are located in the appropriate directory and contain valid data in percentage form, not decimals.

### 3. Run the Script

You can execute the script by opening your terminal or command prompt, navigating to the script's directory, and running:
bash (within the Virtual Environment)
python main.py

iPython
%run main.py

### 4. Follow the Prompts

The script will guide you through several input prompts. These include:

    -   The type of investment
    -   Starting value of investments
    -   Annual withdrawal amount
    -   Years in retirement (minimum, most likely, and maximum)
    -   Number of cases (simulations) to run

You can either enter values manually or press ENTER to use the default values provided.