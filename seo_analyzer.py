"""
SEO Analyzer Module
Analyzes on-page SEO and technical searchability of a single web page
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urlparse


def analyze_url(url):
    """
    Main function that orchestrates the SEO analysis
    Returns a dictionary with score, breakdown, and recommendations
    """
    try:
        # Fetch the page and measure response time
        start_time = time.time()
        html_content, final_url, is_https = fetch_page(url)
        response_time = time.time() - start_time
        
        # Parse SEO elements
        elements = parse_seo_elements(html_content, final_url, is_https, response_time)
        
        # Calculate score and breakdown
        score_data = calculate_score(elements)
        
        # Generate recommendations
        recommendations = generate_recommendations(elements, score_data)
        
        return {
            'success': True,
            'url': final_url,
            'score': score_data['total_score'],
            'breakdown': score_data['breakdown'],
            'recommendations': recommendations,
            'elements': elements
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def fetch_page(url):
    """
    Fetches HTML content using requests
    Returns HTML content, final URL, and HTTPS status
    """
    # Clean up the URL
    url = url.strip()
    
    # Remove common user input issues
    url = url.replace(' ', '')  # Remove any spaces
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Set headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
    response.raise_for_status()
    
    # Check if HTTPS
    is_https = response.url.startswith('https://')
    
    return response.text, response.url, is_https


def parse_seo_elements(html, url, is_https, response_time):
    """
    Extracts SEO elements using BeautifulSoup
    Returns a dictionary of all SEO elements found
    """
    soup = BeautifulSoup(html, 'lxml')
    
    elements = {}
    
    # 1. Title Tag
    title_tag = soup.find('title')
    elements['title'] = title_tag.get_text().strip() if title_tag else None
    elements['title_length'] = len(elements['title']) if elements['title'] else 0
    
    # 2. Meta Description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    elements['meta_description'] = meta_desc.get('content', '').strip() if meta_desc else None
    elements['meta_description_length'] = len(elements['meta_description']) if elements['meta_description'] else 0
    
    # 3. Headings Structure
    elements['h1_tags'] = [h1.get_text().strip() for h1 in soup.find_all('h1')]
    elements['h1_count'] = len(elements['h1_tags'])
    elements['headings'] = {
        'h1': len(soup.find_all('h1')),
        'h2': len(soup.find_all('h2')),
        'h3': len(soup.find_all('h3')),
        'h4': len(soup.find_all('h4')),
        'h5': len(soup.find_all('h5')),
        'h6': len(soup.find_all('h6'))
    }
    
    # 4. Images and Alt Text
    images = soup.find_all('img')
    elements['total_images'] = len(images)
    elements['images_with_alt'] = len([img for img in images if img.get('alt')])
    elements['images_without_alt'] = elements['total_images'] - elements['images_with_alt']
    elements['alt_text_percentage'] = (elements['images_with_alt'] / elements['total_images'] * 100) if elements['total_images'] > 0 else 100
    
    # 5. Content Length
    # Extract text from body, excluding script and style tags
    for script in soup(['script', 'style', 'nav', 'footer', 'header']):
        script.decompose()
    text_content = soup.get_text()
    words = re.findall(r'\w+', text_content)
    elements['word_count'] = len(words)
    
    # 6. Internal Links
    links = soup.find_all('a', href=True)
    parsed_url = urlparse(url)
    base_domain = parsed_url.netloc
    
    internal_links = []
    for link in links:
        href = link.get('href', '')
        if href.startswith('/') or base_domain in href:
            internal_links.append(href)
    
    elements['total_links'] = len(links)
    elements['internal_links'] = len(internal_links)
    
    # 7. HTTPS/SSL Security
    elements['is_https'] = is_https
    
    # 8. Robots Meta Tag
    robots_meta = soup.find('meta', attrs={'name': 'robots'})
    robots_content = robots_meta.get('content', '').lower() if robots_meta else ''
    elements['has_noindex'] = 'noindex' in robots_content
    elements['has_nofollow'] = 'nofollow' in robots_content
    elements['robots_content'] = robots_content if robots_content else None
    
    # 9. Canonical Tag
    canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
    elements['has_canonical'] = canonical_tag is not None
    elements['canonical_url'] = canonical_tag.get('href') if canonical_tag else None
    
    # 10. Structured Data
    # Check for JSON-LD
    json_ld = soup.find_all('script', type='application/ld+json')
    elements['has_json_ld'] = len(json_ld) > 0
    
    # Check for Microdata (itemscope attribute)
    microdata = soup.find_all(attrs={'itemscope': True})
    elements['has_microdata'] = len(microdata) > 0
    
    # Check for RDFa (typeof attribute)
    rdfa = soup.find_all(attrs={'typeof': True})
    elements['has_rdfa'] = len(rdfa) > 0
    
    elements['has_structured_data'] = elements['has_json_ld'] or elements['has_microdata'] or elements['has_rdfa']
    
    # 11. Mobile-Friendly
    viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
    elements['has_viewport'] = viewport_meta is not None
    elements['viewport_content'] = viewport_meta.get('content') if viewport_meta else None
    
    # Check for responsive design indicators
    elements['has_responsive_meta'] = 'width=device-width' in (elements['viewport_content'] or '')
    
    # 12. Page Load Speed
    elements['response_time'] = response_time
    
    return elements


def calculate_score(elements):
    """
    Calculates 0-100 score with detailed breakdown
    Returns score data with breakdown by category
    """
    breakdown = []
    total_score = 0
    max_score = 100
    
    # 1. Title Tag (10 points)
    title_score = 0
    if elements['title']:
        if 30 <= elements['title_length'] <= 60:
            title_score = 10
        elif elements['title_length'] > 0:
            title_score = 5
    breakdown.append({
        'name': 'Title Tag',
        'score': title_score,
        'max_score': 10,
        'status': 'pass' if title_score == 10 else 'warning' if title_score > 0 else 'fail'
    })
    total_score += title_score
    
    # 2. Meta Description (10 points)
    desc_score = 0
    if elements['meta_description']:
        if 120 <= elements['meta_description_length'] <= 160:
            desc_score = 10
        elif elements['meta_description_length'] > 0:
            desc_score = 5
    breakdown.append({
        'name': 'Meta Description',
        'score': desc_score,
        'max_score': 10,
        'status': 'pass' if desc_score == 10 else 'warning' if desc_score > 0 else 'fail'
    })
    total_score += desc_score
    
    # 3. Headings Structure (15 points)
    heading_score = 0
    if elements['h1_count'] == 1:
        heading_score += 10
    elif elements['h1_count'] > 1:
        heading_score += 5
    
    # Check for heading hierarchy
    if elements['headings']['h2'] > 0 or elements['headings']['h3'] > 0:
        heading_score += 5
    
    breakdown.append({
        'name': 'Headings Structure',
        'score': heading_score,
        'max_score': 15,
        'status': 'pass' if heading_score >= 12 else 'warning' if heading_score > 0 else 'fail'
    })
    total_score += heading_score
    
    # 4. Image Alt Text (10 points)
    alt_score = int(elements['alt_text_percentage'] / 10)  # 100% = 10 points
    breakdown.append({
        'name': 'Image Alt Text',
        'score': alt_score,
        'max_score': 10,
        'status': 'pass' if alt_score >= 8 else 'warning' if alt_score > 0 else 'fail'
    })
    total_score += alt_score
    
    # 5. Content Length (5 points)
    content_score = 0
    if elements['word_count'] >= 300:
        content_score = 5
    elif elements['word_count'] >= 150:
        content_score = 3
    elif elements['word_count'] > 0:
        content_score = 1
    breakdown.append({
        'name': 'Content Length',
        'score': content_score,
        'max_score': 5,
        'status': 'pass' if content_score == 5 else 'warning' if content_score > 0 else 'fail'
    })
    total_score += content_score
    
    # 6. Internal Links (5 points)
    links_score = 0
    if elements['internal_links'] >= 3:
        links_score = 5
    elif elements['internal_links'] > 0:
        links_score = 3
    breakdown.append({
        'name': 'Internal Links',
        'score': links_score,
        'max_score': 5,
        'status': 'pass' if links_score == 5 else 'warning' if links_score > 0 else 'fail'
    })
    total_score += links_score
    
    # 7. HTTPS/SSL Security (10 points)
    https_score = 10 if elements['is_https'] else 0
    breakdown.append({
        'name': 'HTTPS/SSL Security',
        'score': https_score,
        'max_score': 10,
        'status': 'pass' if https_score == 10 else 'fail'
    })
    total_score += https_score
    
    # 8. Robots Meta Tag (10 points)
    robots_score = 0
    if not elements['has_noindex']:
        robots_score += 5
    if not elements['has_nofollow']:
        robots_score += 5
    breakdown.append({
        'name': 'Robots Meta Tag',
        'score': robots_score,
        'max_score': 10,
        'status': 'pass' if robots_score == 10 else 'warning' if robots_score > 0 else 'fail'
    })
    total_score += robots_score
    
    # 9. Canonical Tag (5 points)
    canonical_score = 5 if elements['has_canonical'] else 0
    breakdown.append({
        'name': 'Canonical Tag',
        'score': canonical_score,
        'max_score': 5,
        'status': 'pass' if canonical_score == 5 else 'fail'
    })
    total_score += canonical_score
    
    # 10. Structured Data (5 points)
    structured_score = 5 if elements['has_structured_data'] else 0
    breakdown.append({
        'name': 'Structured Data',
        'score': structured_score,
        'max_score': 5,
        'status': 'pass' if structured_score == 5 else 'fail'
    })
    total_score += structured_score
    
    # 11. Mobile-Friendly (10 points)
    mobile_score = 0
    if elements['has_viewport']:
        mobile_score += 5
    if elements['has_responsive_meta']:
        mobile_score += 5
    breakdown.append({
        'name': 'Mobile-Friendly',
        'score': mobile_score,
        'max_score': 10,
        'status': 'pass' if mobile_score == 10 else 'warning' if mobile_score > 0 else 'fail'
    })
    total_score += mobile_score
    
    # 12. Page Load Speed (5 points)
    speed_score = 0
    if elements['response_time'] < 1:
        speed_score = 5
    elif elements['response_time'] < 2:
        speed_score = 3
    elif elements['response_time'] < 3:
        speed_score = 1
    breakdown.append({
        'name': 'Page Load Speed',
        'score': speed_score,
        'max_score': 5,
        'status': 'pass' if speed_score >= 3 else 'warning' if speed_score > 0 else 'fail'
    })
    total_score += speed_score
    
    return {
        'total_score': total_score,
        'max_score': max_score,
        'breakdown': breakdown
    }


def generate_recommendations(elements, score_data):
    """
    Creates specific, actionable recommendations for each failed or suboptimal SEO factor
    """
    recommendations = []
    
    # Check each breakdown item
    for item in score_data['breakdown']:
        if item['status'] == 'fail':
            # Generate specific recommendations based on the factor
            if item['name'] == 'Title Tag':
                if not elements['title']:
                    recommendations.append({
                        'category': 'Critical',
                        'factor': 'Title Tag',
                        'issue': 'Missing title tag',
                        'recommendation': 'Add a <title> tag in your HTML <head> section. The title should be 30-60 characters and describe your page content.'
                    })
                elif elements['title_length'] < 30:
                    recommendations.append({
                        'category': 'Warning',
                        'factor': 'Title Tag',
                        'issue': f'Title is too short ({elements["title_length"]} characters)',
                        'recommendation': 'Expand your title to 30-60 characters for better search engine visibility.'
                    })
                elif elements['title_length'] > 60:
                    recommendations.append({
                        'category': 'Warning',
                        'factor': 'Title Tag',
                        'issue': f'Title is too long ({elements["title_length"]} characters)',
                        'recommendation': 'Shorten your title to 30-60 characters to prevent truncation in search results.'
                    })
            
            elif item['name'] == 'Meta Description':
                if not elements['meta_description']:
                    recommendations.append({
                        'category': 'Critical',
                        'factor': 'Meta Description',
                        'issue': 'Missing meta description',
                        'recommendation': 'Add a meta description tag: <meta name="description" content="Your description here">. Keep it between 120-160 characters.'
                    })
                elif elements['meta_description_length'] < 120:
                    recommendations.append({
                        'category': 'Warning',
                        'factor': 'Meta Description',
                        'issue': f'Meta description is too short ({elements["meta_description_length"]} characters)',
                        'recommendation': 'Expand your meta description to 120-160 characters for optimal display in search results.'
                    })
                elif elements['meta_description_length'] > 160:
                    recommendations.append({
                        'category': 'Warning',
                        'factor': 'Meta Description',
                        'issue': f'Meta description is too long ({elements["meta_description_length"]} characters)',
                        'recommendation': 'Shorten your meta description to 120-160 characters to prevent truncation.'
                    })
            
            elif item['name'] == 'Headings Structure':
                if elements['h1_count'] == 0:
                    recommendations.append({
                        'category': 'Critical',
                        'factor': 'Headings Structure',
                        'issue': 'No H1 heading found',
                        'recommendation': 'Add a single <h1> tag that describes the main topic of your page. Each page should have exactly one H1.'
                    })
                elif elements['h1_count'] > 1:
                    recommendations.append({
                        'category': 'Warning',
                        'factor': 'Headings Structure',
                        'issue': f'Multiple H1 tags found ({elements["h1_count"]})',
                        'recommendation': 'Use only one H1 tag per page. Convert additional H1 tags to H2 or H3 for better SEO.'
                    })
            
            elif item['name'] == 'Image Alt Text':
                if elements['images_without_alt'] > 0:
                    recommendations.append({
                        'category': 'Warning',
                        'factor': 'Image Alt Text',
                        'issue': f'{elements["images_without_alt"]} out of {elements["total_images"]} images missing alt text',
                        'recommendation': 'Add descriptive alt attributes to all images for accessibility and SEO: <img src="..." alt="description">'
                    })
            
            elif item['name'] == 'Content Length':
                recommendations.append({
                    'category': 'Warning',
                    'factor': 'Content Length',
                    'issue': f'Page has only {elements["word_count"]} words',
                    'recommendation': 'Add more quality content. Pages with 300+ words typically perform better in search rankings.'
                })
            
            elif item['name'] == 'Internal Links':
                recommendations.append({
                    'category': 'Info',
                    'factor': 'Internal Links',
                    'issue': f'Only {elements["internal_links"]} internal links found',
                    'recommendation': 'Add more internal links to other relevant pages on your site to improve navigation and SEO.'
                })
            
            elif item['name'] == 'HTTPS/SSL Security':
                recommendations.append({
                    'category': 'Critical',
                    'factor': 'HTTPS/SSL Security',
                    'issue': 'Page is not served over HTTPS',
                    'recommendation': 'Install an SSL certificate and serve your site over HTTPS. This is crucial for security and SEO rankings.'
                })
            
            elif item['name'] == 'Robots Meta Tag':
                if elements['has_noindex']:
                    recommendations.append({
                        'category': 'Critical',
                        'factor': 'Robots Meta Tag',
                        'issue': 'Page has "noindex" directive',
                        'recommendation': 'Remove the "noindex" directive from your robots meta tag if you want this page indexed by search engines.'
                    })
                if elements['has_nofollow']:
                    recommendations.append({
                        'category': 'Warning',
                        'factor': 'Robots Meta Tag',
                        'issue': 'Page has "nofollow" directive',
                        'recommendation': 'Remove the "nofollow" directive from your robots meta tag to allow search engines to follow links on this page.'
                    })
            
            elif item['name'] == 'Canonical Tag':
                recommendations.append({
                    'category': 'Info',
                    'factor': 'Canonical Tag',
                    'issue': 'No canonical tag found',
                    'recommendation': 'Add a canonical tag to prevent duplicate content issues: <link rel="canonical" href="https://yoursite.com/page">'
                })
            
            elif item['name'] == 'Structured Data':
                recommendations.append({
                    'category': 'Info',
                    'factor': 'Structured Data',
                    'issue': 'No structured data found',
                    'recommendation': 'Add Schema.org structured data (JSON-LD) to help search engines understand your content better and enable rich snippets.'
                })
            
            elif item['name'] == 'Mobile-Friendly':
                if not elements['has_viewport']:
                    recommendations.append({
                        'category': 'Critical',
                        'factor': 'Mobile-Friendly',
                        'issue': 'No viewport meta tag found',
                        'recommendation': 'Add viewport meta tag: <meta name="viewport" content="width=device-width, initial-scale=1">'
                    })
            
            elif item['name'] == 'Page Load Speed':
                recommendations.append({
                    'category': 'Warning',
                    'factor': 'Page Load Speed',
                    'issue': f'Slow response time ({elements["response_time"]:.2f} seconds)',
                    'recommendation': 'Optimize your page load speed by compressing images, minifying CSS/JS, and using a CDN. Target under 2 seconds.'
                })
        
        elif item['status'] == 'warning':
            # Add warning-level recommendations
            if item['name'] == 'Title Tag' and elements['title']:
                if elements['title_length'] < 30 or elements['title_length'] > 60:
                    recommendations.append({
                        'category': 'Warning',
                        'factor': 'Title Tag',
                        'issue': f'Title length ({elements["title_length"]} characters) not optimal',
                        'recommendation': 'Adjust your title to be between 30-60 characters for best search engine display.'
                    })
            
            if item['name'] == 'Meta Description' and elements['meta_description']:
                if elements['meta_description_length'] < 120:
                    recommendations.append({
                        'category': 'Warning',
                        'factor': 'Meta Description',
                        'issue': f'Meta description is too short ({elements["meta_description_length"]} characters)',
                        'recommendation': 'Expand your meta description to 120-160 characters for optimal display in search results.'
                    })
                elif elements['meta_description_length'] > 160:
                    recommendations.append({
                        'category': 'Warning',
                        'factor': 'Meta Description',
                        'issue': f'Meta description is too long ({elements["meta_description_length"]} characters)',
                        'recommendation': 'Shorten your meta description to 120-160 characters to prevent truncation.'
                    })
            
            if item['name'] == 'Headings Structure' and elements['h1_count'] > 1:
                recommendations.append({
                    'category': 'Warning',
                    'factor': 'Headings Structure',
                    'issue': f'Multiple H1 tags found ({elements["h1_count"]})',
                    'recommendation': 'Use only one H1 tag per page for better SEO structure.'
                })
            
            if item['name'] == 'Page Load Speed' and item['score'] < 5:
                recommendations.append({
                    'category': 'Warning',
                    'factor': 'Page Load Speed',
                    'issue': f'Response time is {elements["response_time"]:.2f} seconds',
                    'recommendation': 'Consider optimizing page load speed to under 1 second for optimal user experience.'
                })
    
    return recommendations

