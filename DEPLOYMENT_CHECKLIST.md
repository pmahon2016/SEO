# PythonAnywhere Deployment Checklist

Use this checklist to ensure your SEO Analyzer is properly deployed.

## Pre-Deployment

- [ ] Sign up for PythonAnywhere account
- [ ] Verify all code works locally (`python app.py`)
- [ ] Ensure `requirements.txt` is complete
- [ ] Have your PythonAnywhere username ready

## File Upload

- [ ] Code uploaded to PythonAnywhere (via Git or Files tab)
- [ ] All files present:
  - [ ] `app.py`
  - [ ] `seo_analyzer.py`
  - [ ] `wsgi.py`
  - [ ] `requirements.txt`
  - [ ] `templates/index.html`
  - [ ] `static/style.css`

## Environment Setup

- [ ] Virtual environment created: `python3.10 -m venv venv`
- [ ] Virtual environment activated: `source venv/bin/activate`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Verify installation: `pip list` shows Flask, requests, beautifulsoup4, lxml

## Web App Configuration

- [ ] Web app created (Manual configuration, Python 3.10)
- [ ] WSGI file configured with correct username paths
- [ ] Virtual environment path set in Web tab
- [ ] Static files configured:
  - URL: `/static/`
  - Directory: `/home/yourusername/SEO-Analyser/static`

## Testing

- [ ] Web app reloaded (green Reload button)
- [ ] No errors in error log
- [ ] Website loads at `http://yourusername.pythonanywhere.com`
- [ ] CSS/styling displays correctly
- [ ] Can enter a URL in the form
- [ ] Analysis completes successfully (for whitelisted sites on free account)
- [ ] Results display properly with score and recommendations

## Troubleshooting (if needed)

- [ ] Checked error log for Python errors
- [ ] Verified all paths use correct username
- [ ] Confirmed virtual environment is activated
- [ ] Reinstalled dependencies if needed
- [ ] Checked static files configuration

## Post-Deployment

- [ ] Bookmark your app URL
- [ ] Share with others
- [ ] Monitor error logs periodically
- [ ] Consider upgrading account for full website access

## Notes

**Free Account Limitation:** Can only analyze websites on PythonAnywhere's whitelist.

**To analyze any website:** Upgrade to paid account ($5/month).

---

**Your App URL:** `http://yourusername.pythonanywhere.com`

Replace `yourusername` with your actual PythonAnywhere username.

