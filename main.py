# -*- coding: utf-8 -*-
"""
Monte Carlo Simulation for Retirement Savings

This Python script simulates the growth of retirement savings using a
Monte Carlo method. It estimates potential outcomes of different investment
scenarios by running numerous simulations, each with varying market
conditions. The script helps model the impact of factors such as annual
returns, volatility, and time horizons on retirement savings outcomes.

Developed in the VS Code editor.
"""

import sys, random
import matplotlib.pyplot as plt


def read_to_list(file_name):
    """Open a file of data in percent, convert to decimal & return a list.

    Args:
        file_name (str): The name of the file containing percentage values.
    
    Returns:
        list: A list of decimal values converted from percentages.
    """
    with open (file_name) as in_file:
        lines = [float(line.strip()) for line in in_file]
        decimal = [round(line / 100, 5) for line in lines]
        return decimal
    
def default_input(prompt, default=None):
    """Prompt the user for input, allowing the use of a default value.

    Args:
        prompt (str): The message to display to the user when asking for
            input.
        default (str, optional): The default value to use if no input is
            provided. Defaults to None.

    Returns:
        str: The user's input, or the default value if no input is provided.
    """

    prompt = '{} [{}]: '.format(prompt, default)
    response = input(prompt)
    if not response and default:
        return default
    else:
        return response

# load data files with original data in percent form.
print('\nNote: Input data should be in percent, NOT decimal form!\n')

try:
    bonds = read_to_list('text_files/data_files/10-yr_TBond_returns_1926-2013_pct.txt')
    stocks = read_to_list('text_files/data_files/SP500_returns_1926-2013_pct.txt')
    blend_40_50_10 = read_to_list('text_files/data_files/S-B-C_blend_1926-2013_pct.txt')
    blend_50_50 = read_to_list('text_files/data_files/S-B_blend_1926-2013_pct.txt')
    infl_rate = read_to_list('text_files/data_files/annual_infl_rate_1926-2013_pct.txt')
except IOError as e:
    print('{}. \nTerminating Program.'.format(e), file=sys.stderr)
    sys.exit(1)
    
# get user input; use dictionary for investmnet-type arguments
investment_type_args = {
    'bonds': bonds, 
    'stocks': stocks, 
    'sb_blend': blend_50_50,
    'sbc_blend': blend_40_50_10,
}

# print input legend for user
print('   stocks = SP500')
print('    bonds = 10-yr Treasury Bond')
print(' sb_blend = 50% SP500 / 50% TBond')
print('sbc_blend = 40% SP500 / 50% TBond / 10% Cash\n')

print('Press ENTER to take default value shown in [brackets]. \n')

# get user input
invest_type = default_input('Enter investment type: (stocks, bonds, sb_blend,'\
                            'sbc_blend): \n', 'bonds').lower()
while invest_type not in investment_type_args:
    invest_type = input('Invalid investment, Enter investment type'\
                        'as listed in prompt: ')

start_value = default_input('Input starting value of investments: \n',  
                            '2_000_000')

while not start_value.isdigit():
    start_value = input('Invalid input! Input integer only (do NOT include symbols or commas):  ')
    
withdrawal = default_input('Input annual pre-tax withdrawal' \
    " (today's $): \n", "80,000")
while not withdrawal.isdigit():
    withdrawal = input('Invalid input! Input integer only (do NOT include symbols or commas):  ')
    
min_years = default_input('Input minimum years in retirement: \n', '18')
while not min_years.isdigit():
    min_years = input('Invalid input! Input integer only (do NOT include symbols or commas):  ')
    
most_likely_years = default_input('Input most-likely years in retirement: \n',\
    '25')
while not most_likely_years.isdigit():
    most_likely_years = input('Invalid input! Input integer only (do NOT include symbols or commas):  ')
    
max_years = default_input('Input maximum years in retirement: \n', '40')
while not max_years.isdigit():
    max_years = input('Invalid input! Input integer only (do NOT include symbols or commas):  ')
    
num_cases = default_input('Input number of cases to run: \n', '50_000')
while not num_cases.isdigit():
    num_cases = input('Invalid input! Input integer only (do NOT include symbols or commas):  ')

# chek for other erroneous input
if not int(min_years) < int(most_likely_years) < int(max_years) \
    or int(max_years) > 99:
        print("\nProblem with input years.", file=sys.stderr)
        print("Requires Min < Most Likely < Max with Max <= 99.", file=sys.stderr)
        sys.exit(1)

def montecarlo (returns):
    """
    Run a Monte Carlo Simulation (MCS) to simulate investment growth over time.
    
    Calculate the final investment value and count bankruptcies (investment 
    value falls below the bankruptcy threshold).

    Args:
        returns (list or array-like): Potential returns for each period, such 
                                      as historical or expected returns.
        initial_investment (float): The starting investment value.
        periods (int): Number of periods to simulate (e.g., years or months).
        simulations (int): The number of Monte Carlo simulations to run.
        bankruptcy_threshold (float, optional): Threshold below which the 
                                                investment is considered 
                                                bankrupt. Defaults to 0.

    Returns:
        tuple:
            - final_values (list): Final investment value at the end of the 
              plan for each simulation.
            - bankrupt_count (int): Number of simulations where the investment 
              value fell below the bankruptcy threshold.
    """
    case_count = 0
    bankrupt_count = 0
    outcome = []
    
    while case_count < int(num_cases):
        investments = int(start_value)
        start_year = random.randrange(0, len(returns))
        duration = int(random.triangular(int(min_years), int(max_years), 
            int(most_likely_years)))
        end_year = start_year + duration
        lifespan = [i for i in range(start_year, end_year)]
        bankrupt = 'no'
        
        # build temporary lists for each case
        lifespan_returns = []
        lifespan_infl = []
        for i in lifespan:
            lifespan_returns.append(returns[i % len(returns)])
            lifespan_infl.append(infl_rate[i % len(infl_rate)])
        
        # loop through each year of retirement for each case run
        for index, i in enumerate(lifespan_returns):
            infl = lifespan_infl[index]
            
            # do not adjust for inflation the first year
            if index == 0:
                withdrawal_infl_adj = int(withdrawal)
            else:
                withdrawal_infl_adj = int(withdrawal_infl_adj * (1 + infl))
            
            investments -= withdrawal_infl_adj
            investments = int(investments * (1 + i))
            
            if investments <= 0:
                bankrupt = 'yes'
                break
            
            if bankrupt == 'yes':
                outcome.append(0)
                bankrupt_count += 1
            else:
                case_count += 1
        return outcome, bankrupt_count
    
def bankrupt_prob(outcome, bankrupt_count):
    """
    Calculate and return the chance of running out of money and other stats.

    Args:
        outcome (list or array-like): Final investment outcomes from the 
                                      simulations.
        bankrupt_count (int): Number of times the investment went below the 
                              bankruptcy threshold.

    Returns:
        dict: A dictionary with:
            - 'chance_of_bankruptcy' (float): Probability of running out of 
              money (as a percentage).
            - 'mean_final_value' (float): Average final investment value.
            - 'median_final_value' (float): Median final investment value.
            - 'max_final_value' (float): Highest final investment value.
            - 'min_final_value' (float): Lowest final investment value.
    """
    total = len(outcome)
    odds = round(100 * bankrupt_count / total, 1)
    
    print("\nInvestment type: {}".format(invest_type))
    print("Starting value: ${:,}".format(int(start_value)))
    print("Annual Withdrawal: ${:,}".format(int(withdrawal)))
    print("Years in retirement (min-most_likely-max): {}-{}-{}"
          .format(min_years, most_likely_years, max_years))
    print("Number of runs: {:,}\n".format(len(outcome)))
    print("Odds of running out of money: {}%\n".format(odds))
    print("Average outcome: ${:,}".format(int(sum(outcome) / total)))
    print("Minimum outcome: ${:,}".format(min(i for i in outcome)))
    print("Maximum outcome: ${:,}".format(max(i for i in outcome)))

    return odds

def main():
    """
    Call MCS and bankruptcy functions, then draw a bar chart of the results.
    """
    outcome, bankrupt_count = montecarlo(investment_type_args[invest_type])
    odds = bankrupt_prob(outcome, bankrupt_count)
    
    plotdata = outcome[:3000] # only plot first 3000 runs
    plt.figure('Outcome by Case (showing fir {} runs)'.format(len(plotdata)),
               figsize=(16, 5)) # size is width, height in inches
    index = [i + 1 for i in range(len(plotdata))]
    plt.bar(index, plotdata, color='black')
    