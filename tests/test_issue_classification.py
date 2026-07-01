import unittest

from backend.main import IssueRequest, report_issue


class IssueClassificationTests(unittest.TestCase):
    def test_classifies_network_issue(self):
        result = report_issue(IssueRequest(description="Internet is not working"))
        self.assertEqual(result["category"], "Network")
        self.assertEqual(result["assigned_to"], "Network Team")
        self.assertEqual(result["priority"], "High")
        self.assertEqual(result["department"], "Network")
        self.assertEqual(result["contact_number"], "7262059405")

    def test_classifies_fiber_issue(self):
        result = report_issue(IssueRequest(description="Fiber line is cut in the area"))
        self.assertEqual(result["category"], "Fiber")
        self.assertEqual(result["assigned_to"], "Fiber Team")
        self.assertEqual(result["priority"], "High")
        self.assertEqual(result["department"], "Fiber")
        self.assertEqual(result["contact_number"], "9049104430")

    def test_classifies_mobile_issue(self):
        result = report_issue(IssueRequest(description="Mobile signal is weak in the tower"))
        self.assertEqual(result["category"], "Mobile")
        self.assertEqual(result["assigned_to"], "Mobile Team")
        self.assertEqual(result["priority"], "Medium")
        self.assertEqual(result["department"], "Mobile")
        self.assertEqual(result["contact_number"], "9968326836")

    def test_returns_invalid_for_unknown_issue(self):
        result = report_issue(IssueRequest(description="My lunch is delayed"))
        self.assertEqual(result["category"], "Invalid")
        self.assertEqual(result["priority"], "Low")
        self.assertEqual(result["assigned_to"], "No team")
        self.assertEqual(result["department"], "Unknown")
        self.assertEqual(result["contact_number"], "")
        self.assertIn("not defined", result["message"].lower())


if __name__ == "__main__":
    unittest.main()
