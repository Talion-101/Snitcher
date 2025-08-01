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
        
        # Check for required columns based on Snitcher export format
        required_cols = {
            'company': 'Name',
            'last_visit': 'Last visit', 
            'pages': 'Unique pages Visited'
        }
        
        missing_cols = []
        for key, col_name in required_cols.items():
            if col_name not in df.columns:
                missing_cols.append(col_name)
        
        if missing_cols:
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}. Please ensure this is a Snitcher export file.")
        
        # Convert Last visit column to datetime
        df['Last visit'] = pd.to_datetime(df['Last visit'], errors='coerce')
        
        # Remove rows where Last visit couldn't be parsed
        df = df.dropna(subset=['Last visit'])
        
        if df.empty:
            return "No valid visit data found in the file."
        
        # Filter visits from last 24 hours
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        df_filtered = df[df['Last visit'] >= yesterday]
        
        if df_filtered.empty:
            return "No visits found in the last 24 hours."
        
        # Sort by Last visit descending to get latest visits first
        df_filtered = df_filtered.sort_values('Last visit', ascending=False)
        
        # Keep only latest visit per company (first occurrence after sorting)
        df_latest = df_filtered.drop_duplicates(subset=['Name'], keep='first')
        
        # Process each visit
        visits = []
        for _, row in df_latest.iterrows():
            company = row['Name']
            pages_visited = row['Unique pages Visited']
            
            # Skip if company name is empty
            if pd.isna(company) or company == '':
                continue
                
            # Determine action based on pages visited
            if pd.isna(pages_visited) or pages_visited == '':
                action = "visited homepage"
            else:
                # Pages visited might contain multiple URLs separated by commas or semicolons
                # We'll take the first one for simplicity, or if it contains tracking, show homepage
                pages_str = str(pages_visited)
                
                # Check if it contains homepage indicators
                if 'hsCtaTracking' in pages_str or '_hcms' in pages_str:
                    action = "visited homepage"
                else:
                    # Split by common separators and take the first URL
                    first_page = pages_str.split(',')[0].split(';')[0].strip()
                    
                    if not first_page or first_page == '/':
                        action = "visited homepage"
                    else:
                        # Extract meaningful part from URL
                        parsed_url = urlparse(first_page) if first_page.startswith('http') else urlparse('http://example.com' + first_page)
                        path = parsed_url.path.strip('/')
                        
                        if path:
                            # Get the last segment of the path
                            segments = path.split('/')
                            last_segment = segments[-1] if segments else ''
                            
                            # If last segment is empty or just numbers/IDs, use the previous segment
                            if not last_segment or last_segment.isdigit() or len(last_segment) < 3:
                                if len(segments) > 1:
                                    last_segment = segments[-2]
                                else:
                                    last_segment = segments[0] if segments else ''
                            
                            if last_segment:
                                # Remove file extensions
                                last_segment = re.sub(r'\.[^.]*$', '', last_segment)
                                # Replace hyphens and underscores with spaces
                                formatted_action = re.sub(r'[-_]', ' ', last_segment)
                                # Capitalize first letter
                                formatted_action = formatted_action.strip().lower()
                                action = f"viewed {formatted_action}"
                            else:
                                action = "visited homepage"
                        else:
                            action = "visited homepage"
            
            visits.append(f"- {company}, {action}")
        
        if not visits:
            return "No valid company visits found in the last 24 hours."
        
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
