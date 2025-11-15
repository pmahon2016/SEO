"""
SEO Analyzer Flask Application
A web app to analyze and rate the SEO effectiveness of a website
"""

from flask import Flask, render_template, request, jsonify
from seo_analyzer import analyze_url

app = Flask(__name__)


@app.route('/')
def index():
    """
    Renders the main page with the input form
    """
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Accepts URL, runs SEO analysis, and returns results
    """
    try:
        # Get URL from form data
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'Please provide a URL to analyze'
            }), 400
        
        # Analyze the URL
        result = analyze_url(url)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500


if __name__ == '__main__':
    # For local development only
    app.run(debug=True, host='0.0.0.0', port=5004)

