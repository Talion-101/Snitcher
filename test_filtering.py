# Test the filtering with sample data
import sys
sys.path.append('/workspaces/Snitcher')

from app import process_snitcher_data

# Create test CSV data with mixed dates (like your real export)
test_csv = """Name,Last visit,Unique pages Visited
Company A,2025-07-01 09:30:00,/homepage
Company B,2025-07-02 14:15:30,/products/widget
Company C,2025-07-03 11:21:11,/contact
Company D,2025-07-02 16:45:22,/about
Company A,2025-07-03 10:30:00,/services
Old Company,2025-04-01 12:00:00,/homepage"""

try:
    result = process_snitcher_data(test_csv, '.csv')
    print("✅ Processing successful!")
    print("=" * 50)
    print(result)
    print("=" * 50)
except Exception as e:
    print(f"❌ Error: {e}")
