import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.report_utils import assess_risk_level, generate_dossier

class TestAgentUtils(unittest.TestCase):

    def test_risk_level_high(self):
        """Test high confidence gives HIGH risk label."""
        result = assess_risk_level(0.95)
        self.assertIn("HIGH", result)

    def test_risk_level_medium(self):
        """Test medium confidence gives MEDIUM label."""
        result = assess_risk_level(0.70)
        self.assertIn("MEDIUM", result)

    def test_risk_level_low(self):
        """Test low confidence gives LOW label."""
        result = assess_risk_level(0.30)
        self.assertIn("LOW", result)

    def test_generate_dossier_contains_name(self):
        """Test dossier contains the target name."""
        report = generate_dossier(
            name          = "John Doe",
            match_details = "Match confirmed at 90%",
            osint_data    = "Works at CyberCorp",
            confidence    = 0.90
        )
        self.assertIn("John Doe", report)
        self.assertIn("CyberCorp", report)
        self.assertIsInstance(report, str)

if __name__ == "__main__":
    unittest.main()
