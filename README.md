# SEO Analyzer

A Python Flask web application that analyzes and rates the SEO effectiveness of a website on a scale from 0 to 100, with specific actionable recommendations for improvement.

## Features

### On-Page SEO Analysis (55 points)
- **Title Tag** - Checks for presence and optimal length (30-60 characters)
- **Meta Description** - Validates existence and length (120-160 characters)
- **Headings Structure** - Ensures proper H1 usage and heading hierarchy
- **Image Alt Text** - Verifies alt attributes on images
- **Content Length** - Measures text content (target 300+ words)
- **Internal Links** - Checks for internal linking structure

### Technical Searchability (45 points)
- **HTTPS/SSL Security** - Verifies secure connection
- **Robots Meta Tag** - Checks for indexing blockers (noindex/nofollow)
- **Canonical Tag** - Validates canonical URL presence
- **Structured Data** - Detects Schema.org markup (JSON-LD, Microdata, RDFa)
- **Mobile-Friendly** - Checks viewport meta tag and responsive indicators
- **Page Load Speed** - Measures response time

### Actionable Recommendations
The analyzer provides specific recommendations for every issue found, categorized by:
- **Critical** - Issues that severely impact SEO
- **Warning** - Issues that should be addressed
- **Info** - Suggestions for improvement

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download this repository**
   ```bash
   cd "SEO Analyser"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Application

1. **Run the Flask application**
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Enter a URL** in the input field and click "Analyze SEO"

4. **View results** including:
   - Overall SEO score (0-100)
   - Detailed breakdown of each SEO factor
   - Specific recommendations for improvement

### Example URLs to Test
Try analyzing these websites:
- `https://example.com`
- `https://www.wikipedia.org`
- Your own website URL

## Project Structure

```
SEO Analyser/
├── app.py                 # Flask application and routes
├── seo_analyzer.py        # Core SEO analysis logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main web interface
└── static/
    └── style.css         # Styling and design
```

## How It Works

1. **URL Submission** - User enters a URL in the web interface
2. **Page Fetching** - The application fetches the HTML content using requests
3. **HTML Parsing** - BeautifulSoup parses the HTML to extract SEO elements
4. **Score Calculation** - Each SEO factor is evaluated and scored
5. **Recommendations Generation** - Specific improvements are suggested based on findings
6. **Results Display** - Score, breakdown, and recommendations are shown in the interface

## SEO Factors Explained

### Title Tag (10 points)
The page title that appears in search results. Should be 30-60 characters and describe the page content.

### Meta Description (10 points)
The description snippet shown in search results. Should be 120-160 characters and compelling.

### Headings Structure (15 points)
Proper use of H1-H6 tags to create content hierarchy. Each page should have exactly one H1.

### Image Alt Text (10 points)
Alternative text for images, important for accessibility and SEO.

### Content Length (5 points)
Amount of text content on the page. Pages with 300+ words typically perform better.

### Internal Links (5 points)
Links to other pages on the same website, helping with navigation and SEO.

### HTTPS/SSL Security (10 points)
Whether the site uses HTTPS encryption. Critical for security and SEO rankings.

### Robots Meta Tag (10 points)
Controls whether search engines can index the page and follow links.

### Canonical Tag (5 points)
Specifies the preferred URL version to prevent duplicate content issues.

### Structured Data (5 points)
Schema.org markup that helps search engines understand content and enable rich snippets.

### Mobile-Friendly (10 points)
Responsive design indicators, including viewport meta tag.

### Page Load Speed (5 points)
How quickly the page responds. Faster is better for SEO and user experience.

## Troubleshooting

### Common Issues

**Issue: "Connection Error" or timeout**
- The target website may be blocking automated requests
- The website may be temporarily down
- Try a different URL

**Issue: "Module not found" errors**
- Make sure you've activated the virtual environment
- Run `pip install -r requirements.txt` again

**Issue: Port 5000 already in use**
- Another application is using port 5000
- Stop the other application or modify `app.py` to use a different port

### Technical Requirements
- Stable internet connection
- Access to the websites you want to analyze
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Development

### Dependencies
- **Flask** - Web framework
- **requests** - HTTP library for fetching web pages
- **beautifulsoup4** - HTML parsing library
- **lxml** - Fast XML/HTML parser

### Customization
You can customize the scoring weights and thresholds by editing `seo_analyzer.py`:
- Modify the `calculate_score()` function to adjust point allocations
- Update `generate_recommendations()` to add or modify recommendation messages
- Add new SEO factors by extending the `parse_seo_elements()` function

## Limitations

- Analyzes only a single page (not the entire website)
- Cannot measure some advanced SEO factors like backlinks or domain authority
- Response time measurement depends on network conditions
- Some websites may block automated analysis attempts

## Contributing

Feel free to enhance this project by:
- Adding more SEO factors
- Improving the scoring algorithm
- Enhancing the user interface
- Adding export functionality (PDF, CSV)

## License

This project is open source and available for educational and commercial use.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the code comments in `seo_analyzer.py` and `app.py`
3. Ensure all dependencies are correctly installed

---

**Built with Flask • Analyzes On-Page SEO and Technical Searchability**

