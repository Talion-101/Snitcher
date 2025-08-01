#!/usr/bin/env python3
"""Test script to verify all output formats work correctly."""

from app import process_snitcher_data

# Sample CSV data
sample_csv = """Name,Last visit,Unique pages Visited
"TechCorp Inc","2025-07-31 14:30:00","/home,/about,/contact"
"DataSolutions LLC","2025-07-31 15:45:00","/services/data-analytics"
"CloudTech Systems","2025-07-31 16:20:00","/"
"InnovateNow","2025-07-31 13:15:00","/products/innovation-suite"
"SecureNet","2025-07-31 17:00:00","/security/solutions"
"""

def test_format(format_name, format_type):
    print(f"\n{'='*60}")
    print(f"TESTING {format_name}")
    print(f"{'='*60}")
    
    try:
        result = process_snitcher_data(sample_csv, '.csv', time_period_days=1, output_format=format_type)
        print(result)
        print(f"\n✅ {format_name} test completed successfully!")
    except Exception as e:
        print(f"❌ {format_name} test failed: {e}")

if __name__ == "__main__":
    print("Testing all output formats with optimized animations...")
    
    # Test list format
    test_format("LIST FORMAT", "list")
    
    # Test table format
    test_format("TABLE FORMAT", "table")
    
    # Test both formats
    test_format("BOTH FORMATS", "both")
    
    print(f"\n{'='*60}")
    print("All format tests completed!")
    print(f"{'='*60}")
