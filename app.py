from flask import Flask, render_template, request, jsonify, flash
import pandas as pd
from datetime import datetime, timedelta
import io
import re
from urllib.parse import urlparse
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'snitcher-dev-key-change-in-production')

def process_snitcher_data(file_content, file_extension):
    """Process the uploaded Snitcher file and return formatted daily report"""
    try:
        # Read the file based on extension
        if file_extension.lower() == '.csv':
            df = pd.read_csv(io.StringIO(file_content))
        elif file_extension.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            raise ValueError("Unsupported file format")
        
        # Convert timestamp column (assuming it's named 'timestamp', 'date', or similar)
        timestamp_cols = ['timestamp', 'date', 'time', 'visited_at', 'visit_time']
        timestamp_col = None
        
        for col in df.columns:
            if any(ts_name in col.lower() for ts_name in timestamp_cols):
                timestamp_col = col
                break
        
        if not timestamp_col:
            raise ValueError("No timestamp column found. Expected columns like 'timestamp', 'date', 'time', etc.")
        
        # Convert to datetime
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
        
        # Filter visits from last 24 hours
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        df_filtered = df[df[timestamp_col] >= yesterday]
        
        if df_filtered.empty:
            return "No visits found in the last 24 hours."
        
        # Sort by timestamp descending to get latest visits first
        df_filtered = df_filtered.sort_values(timestamp_col, ascending=False)
        
        # Get company and URL columns
        company_cols = ['company', 'organization', 'company_name', 'org']
        url_cols = ['url', 'page', 'page_url', 'visited_page']
        
        company_col = None
        url_col = None
        
        for col in df_filtered.columns:
            if any(comp_name in col.lower() for comp_name in company_cols):
                company_col = col
            if any(url_name in col.lower() for url_name in url_cols):
                url_col = col
        
        if not company_col:
            raise ValueError("No company column found. Expected columns like 'company', 'organization', etc.")
        if not url_col:
            raise ValueError("No URL column found. Expected columns like 'url', 'page', 'page_url', etc.")
        
        # Keep only latest visit per company
        df_latest = df_filtered.drop_duplicates(subset=[company_col], keep='first')
        
        # Process each visit
        visits = []
        for _, row in df_latest.iterrows():
            company = row[company_col]
            url = row[url_col]
            
            # Determine action based on URL
            if pd.isna(url) or url == '':
                action = "visited homepage"
            elif 'hsCtaTracking' in url or '_hcms' in url:
                action = "visited homepage"
            else:
                # Extract last part of URL and format it
                parsed_url = urlparse(url)
                path = parsed_url.path.strip('/')
                if path:
                    # Get the last segment
                    last_segment = path.split('/')[-1]
                    # Remove file extensions
                    last_segment = re.sub(r'\.[^.]*$', '', last_segment)
                    # Replace hyphens and underscores with spaces
                    formatted_action = re.sub(r'[-_]', ' ', last_segment)
                    action = f"viewed {formatted_action}"
                else:
                    action = "visited homepage"
            
            visits.append(f"- {company}, {action}")
        
        # Format the report
        report_date = (now - timedelta(days=1)).strftime("%B %d, %Y")
        report = f"EOD {report_date}\n" + "\n".join(visits)
        
        return report
        
    except Exception as e:
        raise ValueError(f"Error processing file: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return render_template('upload.html')
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return render_template('upload.html')
        
        # Check file extension
        filename = file.filename.lower()
        if not (filename.endswith('.csv') or filename.endswith('.xlsx') or filename.endswith('.xls')):
            flash('Please upload a CSV or Excel file', 'error')
            return render_template('upload.html')
        
        try:
            # Read file content
            file_content = file.read()
            file_extension = os.path.splitext(filename)[1]
            
            # Process the file
            if file_extension.lower() == '.csv':
                content_str = file_content.decode('utf-8')
                report = process_snitcher_data(content_str, file_extension)
            else:
                report = process_snitcher_data(file_content, file_extension)
            
            return render_template('upload.html', report=report, success=True)
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'error')
            return render_template('upload.html')
    
    return render_template('upload.html')

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Please upload a file smaller than 16MB.', 'error')
    return render_template('upload.html'), 413

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
