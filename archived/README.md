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

### 5. View the Results
The results of the simulation will be printed to the terminal and a bar chart will be displayed, showing the distribution of outcomes based on the Monte Carlo simulations.

## Example of Script Execution:

Note: Input data should be in percent, NOT decimal form!

   stocks = SP500
    bonds = 10-yr Treasury Bond
 sb_blend = 50% SP500 / 50% TBond
sbc_blend = 40% SP500 / 50% TBond / 10% Cash

Press ENTER to take default value shown in [brackets].

Enter investment type: (stocks, bonds, sb_blend, sbc_blend): 
[bonds]: sb_blend
Input starting value of investments: 
[2000000]: 
Input annual pre-tax withdrawal (today's $): 
[80000]: 
Input minimum years in retirement: 
[18]: 
Input most-likely years in retirement: 
[25]: 
Input maximum years in retirement: 
[40]: 
Input number of cases to run: 
[50000]: 

After you enter your inputs, the program will simulate the outcomes based on the Monte Carlo simulations and output statistics like:

Investment type: sb_blend
Starting value: $2,000,000
Annual Withdrawal: $80,000
Years in retirement (min-most_likely-max): 18-25-40
Number of runs: 50,000

Odds of running out of money: 12.3%

Average outcome: $523,456
Minimum outcome: $0
Maximum outcome: $4,750,897
