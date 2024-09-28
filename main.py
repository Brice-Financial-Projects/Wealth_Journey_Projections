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
# import matplotlib.pyplot as plt


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
                            '2,000,000')

while not start_value.isdigit():
    start_value = input('Invalid input! Input integer only: ')
    
withdrawal = default_input('Input annual pre-tax withdrawal' \
    " (today's $): \n", "80,000")
while not withdrawal.isdigit():
    withdrawal = input('Invalid input! Input integer only: ')
    
min_years = default_input('Input minimum years in retirement: \n', '18')
while not min_years.isdigit():
    min_years = input('Invalid input! Input integer only: ')
    
most_likely_years = default_input('Input most-likely years in retirement: \n', '25')
while not most_likely_years.isdigit():
    most_likely_years = input('Invalid input! Input integer only: ')
    
max_years = default_input('Input maximum years in retirement: \n', '40')
while not max_years.isdigit():
    max_years = input('Invalid input! Input integer only: ')
    
num_cases = default_input('Input number of cases to run: \n', '50,000')
while not num_cases.isdigit():
    num_cases = input('Invalid input! Input integer only: ')


    
    

