#!/usr/bin/env python3
"""
Quick test script to verify the Snitcher data processing function
"""
import sys
import os
sys.path.append('/workspaces/Snitcher')

from app import process_snitcher_data

def test_processing():
    """Test the processing function with sample data"""
    try:
        # Read the sample CSV file
        with open('/workspaces/Snitcher/sample_data.csv', 'r') as f:
            csv_content = f.read()
        
        # Process the data
        result = process_snitcher_data(csv_content, '.csv')
        
        print("✅ Processing successful!")
        print("\n📊 Generated Report:")
        print("-" * 50)
        print(result)
        print("-" * 50)
        
        # Verify key aspects
        lines = result.split('\n')
        if lines[0].startswith('EOD'):
            print("✅ Report format correct")
        else:
            print("❌ Report format incorrect")
            
        company_lines = [line for line in lines if line.startswith('- ')]
        print(f"✅ Found {len(company_lines)} companies in report")
        
        # Check for expected companies (should be latest visits only from 24h)
        expected_companies = ['Alliant Engineering, Inc.', 'HMI Glass', 'AIG', 'Tech Corp']
        found_companies = []
        
        for line in company_lines:
            for company in expected_companies:
                if company in line:
                    found_companies.append(company)
                    break
        
        print(f"✅ Expected companies found: {len(found_companies)}/{len(expected_companies)}")
        
        # Check for duplicate handling (HMI Glass should appear only once with latest visit)
        hmi_lines = [line for line in company_lines if 'HMI Glass' in line]
        if len(hmi_lines) == 1:
            print("✅ Duplicate company handling works correctly")
            if 'digital scan' in hmi_lines[0]:
                print("✅ Latest visit selected correctly (digital scan vs contact)")
            else:
                print("⚠️  Latest visit might not be selected correctly")
        else:
            print(f"❌ Duplicate handling failed - found {len(hmi_lines)} HMI Glass entries")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_processing()
