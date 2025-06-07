#!/usr/bin/env python3
"""
Test runner for the Flask + Pyodide + HTMX + Tailwind project.

This script runs the test suite and generates an HTML report.
"""

import subprocess
import sys
from pathlib import Path


def run_tests():
    """Run the test suite with HTML report generation."""
    
    # Ensure we're in the project root
    if not Path("main.py").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    print("🧪 Running project setup tests...")
    print("=" * 50)
    
    # Run tests with HTML report
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/",
        "-v",
        "--html=test-report.html",
        "--self-contained-html"
    ]
    
    try:
        result = subprocess.run(cmd, check=False)
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
            print("📊 Test report generated: test-report.html")
        else:
            print(f"\n❌ Tests failed with exit code {result.returncode}")
            print("📊 Test report generated: test-report.html")
            
        return result.returncode
        
    except FileNotFoundError:
        print("❌ pytest not found. Please install testing dependencies:")
        print("   uv pip install pytest pytest-html beautifulsoup4")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests()) 