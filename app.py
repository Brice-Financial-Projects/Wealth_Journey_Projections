from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

# DevelopmentConfig, ProductionConfig, TestingConfig
from config import DevelopmentConfig
# import random
from dotenv import load_dotenv, find_dotenv


# load environment variables from the .env file
load_dotenv(find_dotenv())

app = Flask(__name__)

# Call config files
app.config.from_object(DevelopmentConfig)

# Initialize the debug toolbar
debug = DebugToolbarExtension(app)

@app.route('/')
def home():
    """Render the user to the homepage via render template."""
    return render_template('home.html')

@app.route('/#retire-form')
def retire_form():
    """
    Render the user to the section of the page to input retirement savings.
    
    information.  Section includes:
        investment type, invest_type
        start value, start_value
        annual withdrawal (pre tax in today's dollars), withdrawal
        minimum number of years in retirement, min_years
        likely number of years in retirement, most_likely_years
        maximum number of years in retirement, max_years
        number of cases to run in model, num_cases
    """
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)