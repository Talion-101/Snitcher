#!/usr/bin/env python3
"""
Convert CSV sample to Excel format for testing
"""
import pandas as pd

# Read the CSV
df = pd.read_csv('/workspaces/Snitcher/sample_data.csv')

# Save as Excel
df.to_excel('/workspaces/Snitcher/sample_data.xlsx', index=False)

print("✅ Excel sample file created: sample_data.xlsx")
