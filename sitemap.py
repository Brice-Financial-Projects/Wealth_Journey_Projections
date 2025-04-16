from flask import Blueprint, render_template, url_for, current_app
from datetime import datetime

sitemap_bp = Blueprint('sitemap', __name__)

@sitemap_bp.route('/sitemap.xml')
def sitemap():
    """Generate and serve the sitemap.xml file."""
    pages = [
        {
            'loc': url_for('home', _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'daily',
            'priority': '1.0'
        },
        {
            'loc': url_for('results', _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'daily',
            'priority': '0.8'
        }
    ]
    
    return render_template('sitemap.xml', pages=pages), 200, {'Content-Type': 'application/xml'} 