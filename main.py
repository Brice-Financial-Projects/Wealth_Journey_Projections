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

# import sys, random
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


    

