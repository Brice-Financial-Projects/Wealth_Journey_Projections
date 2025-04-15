import random
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import logging

from io import BytesIO
import base64
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_to_list(file_name):
    """
    Open a file of data in percent, convert to decimal & return a list.

    Args:
        file_name (str): The name of the file containing percentage values.

    Returns:
        list: A list of decimal values converted from percentages.
    """
    try:
        logger.info(f"Attempting to read file: {file_name}")
        if not os.path.exists(file_name):
            logger.error(f"File not found: {file_name}")
            raise FileNotFoundError(f"File not found: {file_name}")
            
        with open(file_name) as in_file:
            lines = [float(line.strip()) for line in in_file]
            decimal = [round(line / 100, 5) for line in lines]
            logger.info(f"Successfully read {len(decimal)} values from {file_name}")
            return decimal
    except Exception as e:
        logger.error(f"Error reading file {file_name}: {str(e)}")
        raise

# Load the data for different asset types and inflation rate
try:
    data_dir = 'text_files/data_files'
    bonds = read_to_list(os.path.join(data_dir, '10-yr_TBond_returns_1926-2013_pct.txt'))
    stocks = read_to_list(os.path.join(data_dir, 'SP500_returns_1926-2013_pct.txt'))
    blend_40_50_10 = read_to_list(os.path.join(data_dir, 'S-B-C_blend_1926-2013_pct.txt'))
    blend_50_50 = read_to_list(os.path.join(data_dir, 'S-B_blend_1926-2013_pct.txt'))
    infl_rate = read_to_list(os.path.join(data_dir, 'annual_infl_rate_1926-2013_pct.txt'))
    
    logger.info("Successfully loaded all data files")
except Exception as e:
    logger.error(f"Error loading data files: {str(e)}")
    raise

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
    try:
        logger.info(f"Starting Monte Carlo simulation with {num_cases} cases")
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

        logger.info(f"Monte Carlo simulation completed. Bankrupt cases: {bankrupt_count}")
        return outcome, bankrupt_count
    except Exception as e:
        logger.error(f"Error in Monte Carlo simulation: {str(e)}")
        raise

def plot_outcome(outcome):
    """
    Generate a bar chart of the simulation outcomes.

    Args:
        outcome (list): List of outcomes for each simulation case.

    Returns:
        str: Base64-encoded image data to be embedded in HTML.
    """
    try:
        logger.info("Generating outcome plot")
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
        logger.info("Successfully generated plot")
        return img_data
    except Exception as e:
        logger.error(f"Error generating plot: {str(e)}")
        raise

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
    try:
        logger.info(f"Calculating results for investment type: {invest_type}")
        if invest_type not in investment_type_args:
            raise ValueError(f"Invalid investment type: {invest_type}")

        outcome, bankrupt_count = montecarlo(
            investment_type_args[invest_type], start_value, withdrawal,
            min_years, most_likely_years, max_years, num_cases
        )

        total_cases = len(outcome)
        bankrupt_prob = round(100 * bankrupt_count / total_cases, 1)
        avg_outcome = round(sum(outcome) / total_cases, 2)

        logger.info(f"Results calculated - Bankruptcy probability: {bankrupt_prob}%, Average outcome: ${avg_outcome}")

        img_data = plot_outcome(outcome[:3000])
        return bankrupt_prob, avg_outcome, img_data
    except Exception as e:
        logger.error(f"Error calculating results: {str(e)}")
        raise

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
        logger.warning(f"Could not convert '{value}' to integer, using default: {default}")
        return default

