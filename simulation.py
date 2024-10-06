import random
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

from io import BytesIO
import base64

def read_to_list(file_name):
    """
    Open a file of data in percent, convert to decimal & return a list.

    Args:
        file_name (str): The name of the file containing percentage values.

    Returns:
        list: A list of decimal values converted from percentages.
    """
    with open(file_name) as in_file:
        lines = [float(line.strip()) for line in in_file]
        decimal = [round(line / 100, 5) for line in lines]
        return decimal

# Load the data for different asset types and inflation rate
try:
    bonds = read_to_list(
        'text_files/data_files/10-yr_TBond_returns_1926-2013_pct.txt')
    stocks = read_to_list(
        'text_files/data_files/SP500_returns_1926-2013_pct.txt')
    blend_40_50_10 = read_to_list(
        'text_files/data_files/S-B-C_blend_1926-2013_pct.txt')
    blend_50_50 = read_to_list(
        'text_files/data_files/S-B_blend_1926-2013_pct.txt')
    infl_rate = read_to_list(
        'text_files/data_files/annual_infl_rate_1926-2013_pct.txt')
except IOError as e:
    print(f"Error loading data: {e}")

# Store the investment type options
investment_type_args = {
    'bonds': bonds,
    'stocks': stocks,
    'sb_blend': blend_50_50,
    'sbc_blend': blend_40_50_10,
}

def montecarlo(returns, start_value, withdrawal, min_years,
               most_likely_years, max_years, num_cases):
    """
    Run a Monte Carlo Simulation to simulate investment growth over time.

    Args:
        returns (list): Potential returns for each period, such as historical
                        or expected returns.
        start_value (int): Starting value of the investment.
        withdrawal (int): Annual withdrawal amount (pre-tax in today's $).
        min_years (int): Minimum number of years in retirement.
        most_likely_years (int): Most likely number of years in retirement.
        max_years (int): Maximum number of years in retirement.
        num_cases (int): Number of Monte Carlo simulation cases to run.

    Returns:
        tuple: (list of final outcomes for each case, number of bankruptcies)
    """
    case_count = 0
    bankrupt_count = 0
    outcome = []

    while case_count < num_cases:
        investments = int(start_value)
        start_year = random.randrange(0, len(returns))
        duration = int(random.triangular(min_years, max_years,
                                         most_likely_years))
        end_year = start_year + duration
        lifespan = [i for i in range(start_year, end_year)]
        bankrupt = False

        lifespan_returns = [returns[i % len(returns)] for i in lifespan]
        lifespan_infl = [infl_rate[i % len(infl_rate)] for i in lifespan]

        for index, i in enumerate(lifespan_returns):
            infl = lifespan_infl[index]
            withdrawal_infl_adj = withdrawal if index == 0 else int(
                withdrawal_infl_adj * (1 + infl))
            investments -= withdrawal_infl_adj
            investments = int(investments * (1 + i))

            if investments <= 0:
                bankrupt = True
                break

        outcome.append(0 if bankrupt else investments)
        bankrupt_count += bankrupt
        case_count += 1

    return outcome, bankrupt_count

def plot_outcome(outcome):
    """
    Generate a bar chart of the simulation outcomes.

    Args:
        outcome (list): List of outcomes for each simulation case.

    Returns:
        str: Base64-encoded image data to be embedded in HTML.
    """
    plt.figure(figsize=(16, 5))
    plt.bar(range(1, len(outcome) + 1), outcome, color='black')
    plt.xlabel('Simulated Lives', fontsize=18)
    plt.ylabel('$ Remaining', fontsize=18)
    plt.ticklabel_format(style='plain', axis='y')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    img_data = base64.b64encode(buf.read()).decode('utf-8')
    return img_data

def calculate_results(invest_type, start_value, withdrawal, min_years,
                      most_likely_years, max_years, num_cases):
    """
    Calculate the simulation results and generate a plot.

    Args:
        invest_type (str): The type of investment portfolio chosen by the user.
        start_value (int): Starting value of the investment.
        withdrawal (int): Annual withdrawal amount (pre-tax in today's $).
        min_years (int): Minimum number of years in retirement.
        most_likely_years (int): Most likely number of years in retirement.
        max_years (int): Maximum number of years in retirement.
        num_cases (int): Number of Monte Carlo simulation cases to run.

    Returns:
        tuple: (bankruptcy probability, average outcome, base64 image data)
    """
    outcome, bankrupt_count = montecarlo(
        investment_type_args[invest_type], start_value, withdrawal,
        min_years, most_likely_years, max_years, num_cases
    )

    total_cases = len(outcome)
    bankrupt_prob = round(100 * bankrupt_count / total_cases, 1)
    avg_outcome = round(sum(outcome) / total_cases, 2)

    img_data = plot_outcome(outcome[:3000])

    return bankrupt_prob, avg_outcome, img_data


def safe_int(value, default):
    """
    Safely convert a value to an integer. If the value is empty or cannot be
    converted, return the provided default.
    
    Args:
        value (str): The value to convert to an integer.
        default (int): The default value to return if conversion fails.

    Returns:
        int: The converted integer value or the default.
    """
    try:
        return int(value) if value and value.strip() else default
    except ValueError:
        return default

