from flask import Flask, render_template, request, jsonify, flash
import csv
import io
import re
from urllib.parse import urlparse
from datetime import datetime, timedelta
from dateutil import parser
import openpyxl
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'snitcher-dev-key-change-in-production')

def parse_csv_data(csv_content):
    """Parse CSV content and return list of dictionaries"""
    csv_reader = csv.DictReader(io.StringIO(csv_content))
    return list(csv_reader)

def parse_excel_data(excel_content):
    """Parse Excel content and return list of dictionaries"""
    workbook = openpyxl.load_workbook(io.BytesIO(excel_content))
    sheet = workbook.active
    
    # Get headers from first row
    headers = []
    for cell in sheet[1]:
        headers.append(cell.value)
    
    # Get data rows
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_dict = {}
        for i, value in enumerate(row):
            if i < len(headers):
                row_dict[headers[i]] = value
        data.append(row_dict)
    
    return data

def parse_date(date_str):
    """Parse date string into datetime object"""
    if not date_str:
        return None
    try:
        # Handle both string and datetime objects
        if isinstance(date_str, datetime):
            return date_str
        
        # Convert to string and parse
        date_str = str(date_str).strip()
        if not date_str or date_str.lower() in ['', 'nan', 'none', 'null']:
            return None
            
        return parser.parse(date_str)
    except:
        return None

def process_snitcher_data(file_content, file_extension):
    """Process the uploaded Snitcher file and return formatted daily report"""
    try:
        # Parse the file based on extension
        if file_extension.lower() == '.csv':
            data = parse_csv_data(file_content)
        elif file_extension.lower() in ['.xlsx', '.xls']:
            data = parse_excel_data(file_content)
        else:
            raise ValueError("Unsupported file format")
        
        if not data:
            return "No data found in the file."
        
        # Check for required columns
        required_cols = ['Name', 'Last visit', 'Unique pages Visited']
        sample_row = data[0]
        missing_cols = [col for col in required_cols if col not in sample_row]
        
        if missing_cols:
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}. Please ensure this is a Snitcher export file.")
        
        # Filter and process data
        now = datetime.now()
        # Instead of strict 24-hour filter, let's be more flexible
        # Get the most recent date in the data to determine the reporting period
        all_dates = []
        for row in data:
            if row.get('Last visit'):
                parsed_date = parse_date(row['Last visit'])
                if parsed_date:
                    all_dates.append(parsed_date)
        
        if not all_dates:
            return "No valid visit dates found in the file."
        
        # Find the latest date in the data
        latest_date = max(all_dates)
        # Use the day of the latest visit as our reporting day  
        report_start = latest_date.replace(hour=0, minute=0, second=0, microsecond=0)
        report_end = report_start + timedelta(days=1)
        
        valid_visits = []
        for row in data:
            if not row.get('Name') or not row.get('Last visit'):
                continue
                
            last_visit = parse_date(row['Last visit'])
            # Filter for visits on the reporting day
            if not last_visit or last_visit < report_start or last_visit >= report_end:
                continue
                
            valid_visits.append({
                'name': row['Name'],
                'last_visit': last_visit,
                'pages': row.get('Unique pages Visited', '')
            })
        
        if not valid_visits:
            return f"No visits found on {report_start.strftime('%B %d, %Y')}."
        
        # Sort by last visit descending for deduplication
        valid_visits.sort(key=lambda x: x['last_visit'], reverse=True)
        
        # Remove duplicates - keep latest visit per company
        unique_companies = {}
        for visit in valid_visits:
            if visit['name'] not in unique_companies:
                unique_companies[visit['name']] = visit
        
        # Sort final results by time ascending (oldest to newest)
        final_visits = list(unique_companies.values())
        final_visits.sort(key=lambda x: x['last_visit'])
        
        # Process each visit
        formatted_visits = []
        for visit in final_visits:
            company = visit['name']
            pages_visited = visit['pages'] or ''
            
            # Skip if company name is empty
            if not company:
                continue
                
            # Determine action based on pages visited
            action = "visited homepage"
            
            if pages_visited:
                pages_str = str(pages_visited)
                
                # Check if it contains homepage indicators
                if 'hsCtaTracking' in pages_str or '_hcms' in pages_str:
                    action = "visited homepage"
                else:
                    # Split by common separators and take the first URL
                    first_page = pages_str.split(',')[0].split(';')[0].strip()
                    
                    if first_page and first_page != '/':
                        # Extract meaningful part from URL
                        if first_page.startswith('http'):
                            parsed_url = urlparse(first_page)
                            path = parsed_url.path.strip('/')
                        else:
                            path = first_page.strip('/')
                        
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
                                # Clean up the action
                                formatted_action = formatted_action.strip().lower()
                                if formatted_action:
                                    action = f"viewed {formatted_action}"
            
            formatted_visits.append(f"- {company}, {action}")
        
        if not formatted_visits:
            return f"No valid company visits found on {report_start.strftime('%B %d, %Y')}."
        
        # Format the report
        report_date = report_start.strftime("%B %d, %Y")
        report = f"EOD {report_date}\n" + "\n".join(formatted_visits)
        
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
