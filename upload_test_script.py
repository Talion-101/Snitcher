#!/usr/bin/env python3
"""
Test the Flask app by simulating a file upload
"""
import requests
import os

# Test file content
csv_content = '''Name,Last visit,Unique pages Visited
"ABC Company","2025-08-01 10:30:00","/products, /about"
"XYZ Corp","2025-08-01 14:15:00","/services"
"Test Firm","2025-08-01 09:45:00","/"
'''

# Save test file
with open('/workspaces/Snitcher/upload_test.csv', 'w') as f:
    f.write(csv_content)

print("Test file created: upload_test.csv")
print("You can now test by uploading this file through the web interface.")
print("Expected behavior:")
print("1. Time in report should show current EST time (not data time)")
print("2. Table format should render in a separate box")
print("3. Both formats should show in separate scrollable boxes")
print("4. Copy function should work for both formats")
