import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.osint_utils import format_osint_results

class TestOsintUtils(unittest.TestCase):

    def test_format_osint_results(self):
        """Test that OSINT formatting returns non-empty string."""
        results = {
            "Professional": "Works at TechCorp",
            "Education"   : "MIT Graduate"
        }
        output = format_osint_results("John Doe", results)
        self.assertIn("John Doe", output)
        self.assertIn("TechCorp", output)
        self.assertIsInstance(output, str)
        self.assertGreater(len(output), 10)

    def test_format_empty_results(self):
        """Test formatting with empty results."""
        output = format_osint_results("Nobody", {})
        self.assertIn("Nobody", output)
        self.assertIsInstance(output, str)

if __name__ == "__main__":
    unittest.main()
