#!/usr/bin/env python3
"""
Simple test script for Strava authentication
Run this to test if the authentication functions work
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_authentication():
    """Test the authentication functionality"""
    try:
        from strava_intelligent_running_coach.authenticate import test_athlete_data_retrieval, test_with_sample_data
        
        print("🧪 Testing Strava Authentication")
        print("=" * 40)
        
        # First test with sample data (no API calls)
        test_with_sample_data()
        
        print("\n" + "=" * 40)
        
        # Then test with real API
        test_athlete_data_retrieval()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("   Make sure you're running from the correct directory")
    except Exception as e:
        print(f"❌ Test Error: {e}")

if __name__ == "__main__":
    test_authentication()
