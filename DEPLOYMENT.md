# Deploying SEO Analyzer to PythonAnywhere

This guide will walk you through deploying your SEO Analyzer Flask app to PythonAnywhere.com.

## Prerequisites

1. A PythonAnywhere account (free tier works fine)
   - Sign up at: https://www.pythonanywhere.com/registration/register/beginner/
2. Basic familiarity with the command line

## Step-by-Step Deployment Guide

### 1. Create a PythonAnywhere Account

- Go to https://www.pythonanywhere.com
- Sign up for a free Beginner account
- Log in to your dashboard

### 2. Upload Your Code

**Option A: Using Git (Recommended)**

1. Push your code to GitHub/GitLab/Bitbucket first
2. Open a Bash console on PythonAnywhere (from the "Consoles" tab)
3. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/seo-analyzer.git SEO-Analyser
   cd SEO-Analyser
   ```

**Option B: Manual Upload**

1. Go to the "Files" tab in PythonAnywhere
2. Create a new directory: `SEO-Analyser`
3. Upload all your project files:
   - `app.py`
   - `seo_analyzer.py`
   - `wsgi.py`
   - `requirements.txt`
   - `templates/` folder with `index.html`
   - `static/` folder with `style.css`

### 3. Set Up Virtual Environment

1. Open a Bash console (Consoles tab > New console > Bash)
2. Create and activate a virtual environment:
   ```bash
   cd ~/SEO-Analyser
   python3.10 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Configure the Web App

1. Go to the **Web** tab in PythonAnywhere
2. Click **Add a new web app**
3. Choose **Manual configuration** (not the Flask wizard)
4. Select **Python 3.10** (or latest available)

### 5. Configure WSGI File

1. In the Web tab, find the "Code" section
2. Click on the **WSGI configuration file** link (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. Delete all the existing content
4. Replace with this configuration:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/SEO-Analyser'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate your virtual environment
activate_this = '/home/yourusername/SEO-Analyser/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import Flask app
from app import app as application
```

**Important:** Replace `yourusername` with your actual PythonAnywhere username!

5. Click **Save** (top right corner)

### 6. Configure Virtual Environment Path

1. Still in the Web tab, find the "Virtualenv" section
2. Enter the path to your virtual environment:
   ```
   /home/yourusername/SEO-Analyser/venv
   ```
   (Replace `yourusername` with your actual username)
3. Press Enter

### 7. Configure Static Files

1. In the Web tab, scroll to the "Static files" section
2. Click **Enter URL** and enter: `/static/`
3. Click **Enter path** and enter: `/home/yourusername/SEO-Analyser/static`
   (Replace `yourusername` with your actual username)
4. This ensures CSS files are served correctly

### 8. Reload the Web App

1. Scroll to the top of the Web tab
2. Click the green **Reload** button
3. Wait a few seconds for the reload to complete

### 9. Test Your App

1. Click on your app URL (e.g., `http://yourusername.pythonanywhere.com`)
2. Your SEO Analyzer should now be live!
3. Try analyzing a website to make sure everything works

## Troubleshooting

### Error: "Something went wrong"

**Check the error logs:**
1. Go to the Web tab
2. Scroll to the "Log files" section
3. Click on the **Error log** link
4. Look for Python error messages

**Common issues:**

1. **Import errors:**
   - Make sure all dependencies are installed in the virtual environment
   - Run `pip list` in the Bash console to verify

2. **File path issues:**
   - Double-check that all paths in the WSGI file use your correct username
   - Paths are case-sensitive

3. **Module not found:**
   - Verify your virtual environment path in the Web tab
   - Try reinstalling: `pip install --force-reinstall -r requirements.txt`

### Static files not loading (no CSS)

1. Check the Static files configuration in the Web tab
2. Verify the path is correct: `/home/yourusername/SEO-Analyser/static`
3. Make sure the `static` folder contains `style.css`

### "Could not import app" error

1. Make sure `app.py` is in the correct directory
2. Check that the WSGI file has the correct import: `from app import app as application`
3. Verify file permissions in Bash: `ls -la ~/SEO-Analyser/app.py`

### Analysis times out or fails

- PythonAnywhere free accounts have some restrictions:
  - Limited CPU time per day
  - External HTTP requests must be to whitelisted sites
  - **Note:** You may need a paid account ($5/month) to analyze any website, as free accounts can only make requests to whitelisted sites

## Updating Your App

When you make changes to your code:

1. Upload the new files (or `git pull` if using Git)
2. If you changed dependencies, update them:
   ```bash
   source ~/SEO-Analyser/venv/bin/activate
   pip install -r requirements.txt
   ```
3. Go to the Web tab and click **Reload**

## Free Account Limitations

PythonAnywhere free accounts have some limitations:

- Can only make HTTP requests to whitelisted domains
- Limited CPU seconds per day
- Your app URL will be: `http://yourusername.pythonanywhere.com`
- App goes to sleep after inactivity (wakes on first request)

**To analyze any website:** You'll need a paid account ($5/month) which removes the whitelist restriction.

## Custom Domain (Paid Accounts Only)

If you upgrade to a paid account, you can use your own domain:

1. Go to the Web tab
2. Click on your app name to edit it
3. Enter your custom domain
4. Follow the DNS configuration instructions

## Production Tips

1. **Monitor your app:**
   - Check error logs regularly
   - Monitor CPU usage in the dashboard

2. **Keep it updated:**
   - Update dependencies periodically
   - Keep your Python version current

3. **Backup your code:**
   - Use Git for version control
   - Keep a local copy of your code

## Support

- PythonAnywhere Help: https://help.pythonanywhere.com/
- Forums: https://www.pythonanywhere.com/forums/
- SEO Analyzer Issues: Check your error logs first

## Next Steps

Once deployed:
- Share your app URL with others
- Monitor the error logs for any issues
- Consider upgrading for full website access
- Add more SEO features as needed

---

**Your app should now be live at:** `http://yourusername.pythonanywhere.com`

Enjoy your deployed SEO Analyzer! 🚀

