import logging
from flask import Flask, render_template, request, flash, send_from_directory 
# from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv, find_dotenv
from main import calculate_results, safe_int  # Import the simulation logic
# DevelopmentConfig, ProductionConfig, TestingConfig
from config import ProductionConfig
import traceback
from flask_talisman import Talisman
from sitemap import sitemap_bp

# Load environment variables from the .env file
load_dotenv(find_dotenv())

app = Flask(__name__)
Talisman(app, content_security_policy=None)

# Call config files
app.config.from_object(ProductionConfig)

# Set up logging to match the configured log level
logging.basicConfig(level=app.config['LOG_LEVEL'])
logger = logging.getLogger(__name__)

# Set up a separate logger specifically for counting requests
request_logger = logging.getLogger('request_count_logger')
request_logger.setLevel(logging.INFO)  # This logger will only log INFO level for requests

# Configure the handler for the request count logger
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Ensure the formatter is consistent
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the request logger
request_logger.addHandler(console_handler)
request_logger.info("Logging system set up correctly.")


# Initialize the debug toolbar
# debug = DebugToolbarExtension(app)

# Initialize a global counter (in memory, not persistent across restarts)
counter = 0

# Register blueprints
app.register_blueprint(sitemap_bp)


@app.before_request
def count_requests():
    global counter  # Ensure that 'counter' is accessed globally
    if 'counter' in globals():  # Check if counter is defined globally
        counter += 1
    else:
        counter = 1  # Set to 1 if for some reason the counter wasn't initialized
    app.logger.setLevel(logging.INFO)  # Ensure INFO level is set
    request_logger.setLevel(logging.INFO)  # Ensure request logger is logging at INFO level
    request_logger.info(f"Request count (via logger): {counter}")
    logger.info(f"Processing request: {request.method} {request.path}")


@app.route('/')
def home():
    """
    Render the homepage where users can input retirement parameters.
    """
    try:
        logger.info("Rendering home page")
        return render_template('home.html', request_count=counter)
    except Exception as e:
        logger.error(f"Error rendering home page: {str(e)}\n{traceback.format_exc()}")
        return "An error occurred while loading the page. Please try again.", 500


@app.route('/results', methods=['POST'])
def results():
    """
    Calculate and display the results of the Monte Carlo simulation.

    This route takes user input from the form, runs the simulation using the
    `calculate_results` function from main.py, and displays the results on
    the results page.

    Returns:
        Renders the results page with calculated simulation outcomes.
    """
    try:
        logger.info("Processing results request")
        # Log form data
        logger.info(f"Form data received: {request.form}")

        # Get form data and set defaults if fields are left empty
        invest_type = request.form.get('invest_type', '').strip().lower() or 'sb_blend'
        start_value = safe_int(request.form.get('start_value', '').strip(), 2000000)
        withdrawal = safe_int(request.form.get('withdrawal', '').strip(), 80000)
        min_years = safe_int(request.form.get('min_years', '').strip(), 18)
        most_likely_years = safe_int(request.form.get('most_likely_years', '').strip(), 25)
        max_years = safe_int(request.form.get('max_years', '').strip(), 40)
        num_cases = safe_int(request.form.get('num_cases', '').strip(), 50000)

        # Log processed values
        logger.info(f"Processed values: invest_type={invest_type}, start_value={start_value}, "
                   f"withdrawal={withdrawal}, min_years={min_years}, most_likely_years={most_likely_years}, "
                   f"max_years={max_years}, num_cases={num_cases}")

        # Run calculations using the logic from simulation.py
        bankrupt_prob, avg_outcome, img_data = calculate_results(
            invest_type, start_value, withdrawal, min_years,
            most_likely_years, max_years, num_cases
        )

        logger.info(f"Calculation results: bankrupt_prob={bankrupt_prob}, avg_outcome={avg_outcome}")

        # Render the results page with the calculated data
        return render_template(
            'results.html',
            bankrupt_prob=bankrupt_prob,
            avg_outcome=avg_outcome,
            img_data=img_data
        )
    except Exception as e:
        logger.error(f"Error processing results: {str(e)}\n{traceback.format_exc()}")
        return "An error occurred while processing your request. Please try again.", 500

@app.route('/google5ee561638742a290.html')
def google_verification():
    return send_from_directory('static', 'google5ee561638742a290.html')


if __name__ == "__main__":
    app.run(debug=False)
