from flask import Flask, render_template, request, jsonify, flash
import csv
import io
import re
from urllib.parse import urlparse
from datetime import datetime, timedelta
from dateutil import parser
import pytz
import openpyxl
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'snitcher-dev-key-change-in-production')

def get_current_est_time():
    """Get current EST time formatted for display"""
    est_tz = pytz.timezone('America/New_York')
    now_est = datetime.now(est_tz)
    return {
        'date': now_est.strftime("%B %d, %Y"),
        'time': now_est.strftime("%I:%M %p EST"),
        'datetime': now_est
    }

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

def process_snitcher_data(file_content, file_extension, time_period_days=1, output_format='list'):
    """Process the uploaded Snitcher file and return formatted daily report"""
    try:
        # Exclusion lists (names and domains)
        EXCLUDED_COMPANIES = set([
            "Alanah Phillips", "Philippine Science High School", "Alliant Engineering", "Alpha Financial Advisors", "AlphaK", "Behavioral Economics", "BlueRock Wealth Management Inc", "Boys without Fathers", "Bph Wealth Management LLP", "Brave Eagle Wealth", "BzzTxt, LLC", "Camelotta Advisors", "Campbell Financial Services", "Canaccord Genuity", "Change Is The Future", "Columbia Threadneedle Investment", "Consilium Associates", "Consultant DNA", "Courageous Business Culture", "Danielson Group Wealth Management", "DEMA Health Ltd Co", "Denison Financial", "DigitalScan4Events", "DreamSmart Academy, LLC", "DreamSmart Behavioral Solutions, LLC", "Edward Jones", "Eighty20 Virtual Corp", "Equilibrium Financial Planning LLP", "Evans Wealth Management", "Family Wealth Alliance", "FDNA InvestorTrial", "Finwizdom", "Fireseeds", "Fivestone Studios", "Freedom Empire Consulting", "Gigaplex", "Gill Capital", "Gillian Dunn", "Global Executive Business Consultants", "GRS Creates", "Gwen Smith", "IFC Bank", "InfOpinion Gmbh", "InstructAnt Financial Solutions", "Intel Corp", "IVV", "Legacy Family Office - 2020", "Legacy Movement", "Legacy Planning Advisors LLC", "Lehare Pty Ltd", "Luminous Wealth, LLC", "M4A3", "MacDonald Financial", "Mark Keith Services", "Mark Murphy", "Maximum Impact Partners, Inc.", "Merit Corporate", "Merit Financial", "Merit Financial Advisors", "Merit Financial Demo", "Merlynn Intelligence Technologies Corporation", "Merrill (The Farret Group)", "My Brilliant Fit Pty Ltd", "My Future Capacity", "My Junior Advisor", "Napa Wealth Managment", "NBFWM Bluteau Caseley Wealth Management Group", "Next Chapter", "OceanFront Wealth Inc.", "Patel Capital Partners", "Post Release", "Providence Wealth", "Pro-vision Lifestyles Ltd", "Rafael Nars", "Raymond James Ltd.", "Rejane Tamoto", "RentScale", "Richardson Wealth", "Ridgeline Coaching", "Robertson Stephens Wealth Management", "Selcouth Coaching & Consulting", "Shelley Row Associates LLC", "Single Point Partners", "Sirenusa Consortium LLC", "Splendys Planejamento Financeiro Pessoal & Assessoria", "Stout", "Suncoast Advisory", "Sykon Capital LLC", "SYNERGY HomeCare", "The Covenant Group", "The Initiative for Family Business & Entrepreneurship", "The Millstone Evans Group of Raymond James", "The Wealth Consulting Group", "Timonier", "Transform Group LLC", "Triad Partners", "Triple Partners", "Vickery Financial Services", "WealthUp", "Wired2Perform", "Worxbee", "XPO Brands", "Richardson GMP Limited", "Philippine Science High School"
        ])
        EXCLUDED_DOMAINS = set([
            "https://alliant-inc.com", "https://pshs.edu.ph", "https://alphafa.com", "https://alphakholdings.com", "https://bluerockwealth.ca", "https://bphwealth.co.uk", "https://www.braveeaglewealth.com", "https://bzztxt.com", "https://camelotta.com", "https://campbell.financial", "https://campbellfs.com", "https://www.canaccordgenuity.com", "https://samanthachambers.com", "https://columbiathreadneedle.com", "https://www.consilium-llc.net", "https://www.consiliumcorporation.com", "https://danielsongroup.ca", "https://demahealth.com", "https://dreamsmartacademy.com", "https://dreamsmartbehavioralsolutions.com", "http://www.edwardjones.com", "https://www.eighty20.co.za", "https://equilibrium.co.uk", "https://evanswealthmanagement.com", "https://www.ewmstanevans.com", "https://www.familywealthalliance.com", "https://www.finwizdom.com", "https://fireseeds.com", "https://fivestonestudios.com", "https://freedomempireconsulting.com", "https://www.gillinvest.com", "https://www.gilliandunn.com", "https://globalexecutivebusinessconsultants.com", "https://grscreates.com", "https://gwensmith.net", "https://www.ifc.org", "https://infopinion.com.br", "https://instructant.com.au", "https://intel.com/", "https://ivv-vermogensopbouw.nl", "https://www.legacyplanningadvisors.com", "https://insolvencynotices.com.au/company/le-hare-pty-ltd", "https://www.luminouswealth.com", "https://macdonaldfinancial.com", "https://jmcwealth.com", "https://www.gotimpact.com", "https://www.meritfinancialadvisors.com", "https://www.merlynn-ai.com", "https://www.ml.com", "https://napawealth.com", "https://www.bdcwealth.ca", "https://proximocapitulo.pt", "https://www.oceanfrontwealth.com", "https://patelcapital.us", "https://patelcapitalgroups.com", "https://providencewealth.com.au", "https://www.raymondjames.com", "https://rejanetamoto.com.br", "https://rentscale.com", "https://richardsonwealth.com", "https://ridgelinecoaching.com", "https://rscapital.com", "https://www.selcouthconsultancy.com", "https://spcfo.com", "https://sirenusa-consortium-llc.square.site", "https://www.splendys.net", "https://suncoastadvisorygroup.com", "https://www.sykoncapital.com", "https://synergyhomecare.com", "https://www.covenant-group.com", "https://www.sju.edu", "https://www.millstoneevansgroup.com", "https://www.wealthcg.com", "https://www.timonier.com", "https://transformgroup.com", "https://triadpartners.com", "https://www.triplepartners.com", "https://www.vickeryfin.net", "https://www.wealthup.co.za", "https://worxbee.com", "Richardson GMP Limited", "https://pshs.edu.ph"
        ])

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

        # Use the specified time period as the reporting period
        report_end = latest_date
        report_start = latest_date - timedelta(days=time_period_days)

        valid_visits = []
        for row in data:
            if not row.get('Name') or not row.get('Last visit'):
                continue

            # Exclude by company name
            company_name = str(row['Name']).strip()
            if company_name in EXCLUDED_COMPANIES:
                continue

            # Exclude by domain (if available in Unique pages Visited)
            pages_visited = str(row.get('Unique pages Visited', '')).strip()
            found_excluded_domain = False
            for domain in EXCLUDED_DOMAINS:
                if domain in pages_visited:
                    found_excluded_domain = True
                    break
            if found_excluded_domain:
                continue

            last_visit = parse_date(row['Last visit'])
            # Filter for visits in the specified time period from the latest visit
            if not last_visit or last_visit < report_start or last_visit > report_end:
                continue

            valid_visits.append({
                'name': company_name,
                'last_visit': last_visit,
                'pages': pages_visited
            })

        if not valid_visits:
            period_text = f"{time_period_days} day{'s' if time_period_days > 1 else ''}"
            return f"No visits found in the last {period_text} ending {latest_date.strftime('%B %d, %Y at %I:%M %p')}."

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


        if not final_visits:
            period_text = f"{time_period_days} day{'s' if time_period_days > 1 else ''}"
            return f"No valid company visits found in the last {period_text} ending {latest_date.strftime('%B %d, %Y at %I:%M %p')}."

        # List format only - table format removed entirely
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

            # Add each company with proper line breaks for easy copying (no bullet points)
            formatted_visits.append(f"{company}, {action}")

        # Format the report with line breaks after each entry for easy copying
        current_est = get_current_est_time()
        report_date = current_est['date']
        report_time = current_est['time']

        # Join with double line breaks for easier copying and pasting
        report = f"Here is the daily snitcher update as of {report_date}, {report_time}\n\n" + "\n\n".join(formatted_visits)

        return report

    except Exception as e:
        raise ValueError(f"Error processing file: {str(e)}")
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return render_template('upload_fixed.html')
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return render_template('upload_fixed.html')
        
        # Check file extension
        filename = file.filename.lower()
        if not (filename.endswith('.csv') or filename.endswith('.xlsx') or filename.endswith('.xls')):
            flash('Please upload a CSV or Excel file', 'error')
            return render_template('upload_fixed.html')
        
        try:
            # Get form parameters with validation
            time_period = int(request.form.get('time_period', 1))
            if time_period < 1:
                time_period = 1
            elif time_period > 365:  # Max 1 year
                time_period = 365
            
            # Output format is always 'list' now - table format removed
            output_format = 'list'
            
            # Read file content
            file_content = file.read()
            file_extension = os.path.splitext(filename)[1]
            
            # Process the file
            if file_extension.lower() == '.csv':
                content_str = file_content.decode('utf-8')
                report = process_snitcher_data(content_str, file_extension, time_period, output_format)
            else:
                report = process_snitcher_data(file_content, file_extension, time_period, output_format)
            
            # Get current EST time for report generation timestamp
            est_info = get_current_est_time()
            
            return render_template('upload_fixed.html', report=report, success=True, 
                                 generation_time=est_info['time'], 
                                 generation_date=est_info['date'])
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'error')
            return render_template('upload_fixed.html')
    
    return render_template('upload_fixed.html')

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Please upload a file smaller than 16MB.', 'error')
    return render_template('upload_fixed.html'), 413

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
