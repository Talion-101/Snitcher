# Test the new functionality
import sys
sys.path.append('/workspaces/Snitcher')

from app import process_snitcher_data

# Create test CSV data
test_csv = """Name,Last visit,Unique pages Visited
Company A,2025-07-01 09:30:00,/homepage
Company B,2025-07-02 14:15:30,/products/widget-pro
Company C,2025-07-03 11:21:11,/contact-us
Company D,2025-07-02 16:45:22,/about-company
Company A,2025-07-03 10:30:00,/services/consulting
Old Company,2025-06-15 12:00:00,/homepage"""

print("=== Testing List Format (1 day) ===")
try:
    result = process_snitcher_data(test_csv, '.csv', 1, 'list')
    print(result)
except Exception as e:
    print(f"❌ Error: {e}")

print("\n=== Testing Table Format (3 days) ===")
try:
    result = process_snitcher_data(test_csv, '.csv', 3, 'table')
    print(result)
except Exception as e:
    print(f"❌ Error: {e}")

print("\n=== Testing List Format (7 days) ===")
try:
    result = process_snitcher_data(test_csv, '.csv', 7, 'list')
    print(result)
except Exception as e:
    print(f"❌ Error: {e}")
