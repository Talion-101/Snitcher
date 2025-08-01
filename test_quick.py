#!/usr/bin/env python3

import sys
import os
sys.path.append('/workspaces/Snitcher')

from app import process_snitcher_data, get_current_est_time

# Test the processing function
with open('/workspaces/Snitcher/test_snitcher_data.csv', 'r') as f:
    csv_content = f.read()

print("Current EST Time:")
current_time = get_current_est_time()
print(f"Date: {current_time['date']}")
print(f"Time: {current_time['time']}")
print("\n" + "="*50 + "\n")

print("Testing List Format:")
result_list = process_snitcher_data(csv_content, '.csv', 1, 'list')
print(result_list)
print("\n" + "="*50 + "\n")

print("Testing Table Format:")
result_table = process_snitcher_data(csv_content, '.csv', 1, 'table')
print(result_table)
print("\n" + "="*50 + "\n")

print("Testing Both Formats:")
result_both = process_snitcher_data(csv_content, '.csv', 1, 'both')
print(result_both)
