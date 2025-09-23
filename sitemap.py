from flask import Blueprint, render_template, url_for, current_app
from datetime import datetime

sitemap_bp = Blueprint('sitemap', __name__)

@sitemap_bp.route('/sitemap.xml')
def sitemap():
    """Generate and serve the sitemap.xml file."""
    today = datetime.now().strftime('%Y-%m-%d')

    # Define all routes that should appear in the sitemap
    pages = [
        {
            'loc': url_for('home', _external=True),
            'lastmod': today,
            'changefreq': 'daily',
            'priority': '1.0'
        },
        {
            'loc': url_for('results', _external=True),
            'lastmod': today,
            'changefreq': 'daily',
            'priority': '0.8'
        }
        # Add any additional routes here as needed
        # Example:
        # {
        #     'loc': url_for('about', _external=True),
        #     'lastmod': today,
        #     'changefreq': 'weekly',
        #     'priority': '0.7'
        # }
    ]

    # Create a sitemap with proper content type
    return render_template('sitemap.xml', 
                           pages=pages, 
                           base_url='https://www.retireforecast.com'), 200, {'Content-Type': 'application/xml'}