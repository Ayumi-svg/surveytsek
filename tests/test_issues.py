# Author: Aria Deligero
# Purpose: Tests the ValidationIssue implementation.
# Responsibility: Verify issue creation, attributes,
# and consistent representation of detected problems.
# Notes: Follow the agreed ValidationIssue structure.

import unittest

from surveytsek.issues import ValidationIssue


class TestValidationIssue(unittest.TestCase):
    def test_issue_stores_information(self):
        issue = ValidationIssue("missing", 2, ["rating"], "No answer")
        self.assertEqual(issue.check_type, "missing")
        self.assertEqual(issue.row_number, 2)
        self.assertEqual(issue.columns, ["rating"])
        self.assertEqual(issue.message, "No answer")
        self.assertIn("rating", str(issue))
        self.assertIn("No answer", str(issue))

    def test_columns_are_copied(self):
        columns = ["rating"]
        issue = ValidationIssue("missing", 0, columns, "Blank")
        columns.append("other")
        self.assertEqual(issue.columns, ["rating"])

    def test_invalid_columns_raise_error(self):
        with self.assertRaises(TypeError):
            ValidationIssue("missing", 0, "rating", "Blank")


if __name__ == "__main__":
    unittest.main()
