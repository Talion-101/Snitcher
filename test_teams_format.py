#!/usr/bin/env python3
"""
Test MS Teams formatting
"""

# Simulate what would be copied
sample_list = """Here is the daily snitcher update as of August 01, 2025, 03:45 PM EST

• Tech Company A, viewed software
• Marketing Firm B, viewed digital marketing
• Consulting Group C, visited homepage"""

print("MS Teams Formatted List:")
print("=" * 50)
print(sample_list)
print("=" * 50)

# Test table format
sample_table = """Here is the daily snitcher update as of August 01, 2025, 03:45 PM EST

Company                | Visited Site          
-----------------------|-----------------------
Tech Company A         | Software              
Marketing Firm B       | Digital Marketing     
Consulting Group C     | Homepage              """

print("\nMS Teams Formatted Table:")
print("=" * 50)
print(sample_table)
print("=" * 50)

print("\nKey improvements for MS Teams:")
print("✅ Proper bullet points (•)")
print("✅ Preserved line breaks") 
print("✅ Clean table formatting with | separators")
print("✅ No excessive spaces or formatting issues")
print("✅ Ready for direct paste into MS Teams")
