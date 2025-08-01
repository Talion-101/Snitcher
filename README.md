# Snitcher Report Generator

A modern Flask web application with glassmorphism dark theme for processing Snitcher visitor data exports and generating formatted daily reports.

## Features

- 🌙 **Dark Theme with Glassmorphism**: Modern UI with semi-transparent cards, blurred backgrounds, and neon accents
- ✨ **Smooth Animations**: Breathing animations, hover effects, and smooth transitions
- 📊 **Data Processing**: Upload CSV/Excel files and get formatted daily reports
- 🔒 **Security**: All processing done in memory - no files saved to disk
- 📱 **Mobile Responsive**: Works perfectly on all device sizes
- 🎨 **Interactive UI**: Glowing buttons, copy-to-clipboard functionality, and elegant notifications

## Tech Stack

- **Backend**: Flask, Pandas
- **Frontend**: Bootstrap 5, Custom CSS with glassmorphism
- **Fonts**: Inter (Google Fonts)
- **Icons**: Font Awesome 6
- **Deployment**: Render-ready with Gunicorn

## Installation & Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Snitcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Upload File**: Click the upload area and select your Snitcher CSV or Excel export
2. **Process**: Click "Process Report" to generate the formatted daily report
3. **Copy**: Use the "Copy to Clipboard" button to copy the formatted report
4. **Use**: Paste the report wherever you need it

## Data Processing Rules

- ✅ Filters visits from the last 24 hours only
- ✅ Keeps only the latest visit per company
- ✅ URLs containing `hsCtaTracking` or `_hcms` show as "visited homepage"
- ✅ Other URLs show as "viewed [formatted page name]"
- ✅ Output format: "EOD [Date]\n- Company Name, action"

## File Structure

```
├── app.py                 # Main Flask application
├── templates/
│   └── upload.html       # HTML template with dark theme
├── static/
│   └── style.css         # Glassmorphism CSS and animations
├── requirements.txt      # Python dependencies
├── Procfile             # Render deployment config
├── sample_data.csv      # Sample test data
└── README.md            # This file
```

## Deployment on Render

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:app`
5. Deploy!

## Sample Data Format

Your Snitcher export should have these columns (standard Snitcher export format):
- `Name` - Company name
- `Last visit` - Timestamp of the last visit (used for 24-hour filtering)
- `Unique pages Visited` - Pages the company visited (comma or semicolon separated URLs)

### Required Columns from Snitcher Export:
```
ID, Name, Location, Country, State, City, Industry, Company Size, 
First visit, Last visit, Website, Phone, Total Visits, Total Pageviews, 
Unique pages Visited, Total time on Site, All Referrers, Unique Campaigns, 
Unique Visitor Locations, crunchbase_handle, youtube_handle, facebook_handle, 
linkedin_handle, angellist_handle, twitter_handle, pinterest_handle, 
Revealed Contacts (Emails only)
```

**Key columns used by the app:**
- **Name**: Company name for the report
- **Last visit**: To filter visits from last 24 hours
- **Unique pages Visited**: To determine what the company viewed

## Security Notes

- 🔒 No files are saved to disk
- 🔒 All processing happens in memory
- 🔒 Data is automatically cleared after processing
- 🔒 Suitable for sensitive visitor data

## Browser Support

- ✅ Modern browsers with CSS backdrop-filter support
- ✅ Chrome, Firefox, Safari, Edge (latest versions)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## License

MIT License - feel free to use and modify as needed!