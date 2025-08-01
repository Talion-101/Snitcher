#!/usr/bin/env python3
"""
Test script to verify table format functionality
"""

import sys
import os
sys.path.append('/workspaces/Snitcher')

from app import process_snitcher_data

def test_table_format():
    """Test the table format generation"""
    
    # Sample CSV data that might cause issues
    sample_data = '''ID,Name,Location,Country,State,City,Industry,Company Size,First visit,Last visit,Website,Phone,Total Visits,Total Pageviews,Unique pages Visited,Total time on Site,All Referrers,Unique Campaigns,Unique Visitor Locations,crunchbase_handle,youtube_handle,facebook_handle,linkedin_handle,angellist_handle,twitter_handle,pinterest_handle,Revealed Contacts (Emails only)
1,"Alliant Engineering, Inc.","San Francisco, CA",USA,CA,"San Francisco",Engineering,50-100,"2025-07-30 10:00:00","2025-07-31 14:30:00",https://allianteng.com,555-0101,3,15,"https://example.com/homepage?hsCtaTracking=123, https://example.com/services",300,"Google, Direct","Campaign A","San Francisco",alliant-eng,,,alliant-engineering,,,
2,"HMI Glass","Los Angeles, CA",USA,CA,"Los Angeles","Manufacturing",25-50,"2025-07-29 09:00:00","2025-07-31 15:45:00",https://hmiglass.com,555-0102,2,8,"https://example.com/solutions/digital-scan, https://example.com/contact",180,"LinkedIn, Google","Campaign B","Los Angeles",,,,,,,
3,"AIG Corp, LLC","New York, NY",USA,NY,"New York","Insurance",500+,"2025-07-30 12:00:00","2025-07-31 16:20:00",https://aig.com,555-0103,1,5,"https://example.com/products/solutions",120,"Direct","","New York",aig-corp,,,aig,,,'''
    
    print("Testing table format generation...")
    
    try:
        # Test table format
        result = process_snitcher_data(sample_data, '.csv', 1, 'table')
        print("✅ Table format generation successful!")
        print("\nTable output preview:")
        print("=" * 50)
        print(result[:500] + "..." if len(result) > 500 else result)
        print("=" * 50)
        
        # Test both format
        result_both = process_snitcher_data(sample_data, '.csv', 1, 'both')
        print("\n✅ Both formats generation successful!")
        print(f"Output length: {len(result_both)} characters")
        
        # Check if TABLE_START is in the output
        if 'TABLE_START' in result:
            print("✅ TABLE_START marker found in table format")
        else:
            print("❌ TABLE_START marker NOT found in table format")
            
        if 'TABLE_START' in result_both and 'LIST_FORMAT_START' in result_both:
            print("✅ Both format markers found in combined output")
        else:
            print("❌ Format markers missing in combined output")
            
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_table_format()
