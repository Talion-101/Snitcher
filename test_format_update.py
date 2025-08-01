# Test the updated list format
import sys
sys.path.append('/workspaces/Snitcher')

from app import process_snitcher_data

# Create test CSV data
test_csv = """Name,Last visit,Unique pages Visited
Company A,2025-07-31 16:00:00,/homepage
Company B,2025-07-31 14:15:30,/products/widget-pro
Company C,2025-07-31 15:21:11,/contact-us
Company D,2025-07-31 13:45:22,/about-company"""

print("=== Testing Updated List Format ===")
try:
    result = process_snitcher_data(test_csv, '.csv', 1, 'list')
    print(result)
except Exception as e:
    print(f"❌ Error: {e}")

print("\n=== Testing Table Format (unchanged) ===")
try:
    result = process_snitcher_data(test_csv, '.csv', 1, 'table')
    print(result)
except Exception as e:
    print(f"❌ Error: {e}")
