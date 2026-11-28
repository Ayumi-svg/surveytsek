# Author: Aria Deligero
# Purpose: Tests the AuditReport implementation.
# Responsibility: Verify report generation, result summaries,
# and presentation of validation findings.
# Notes: Include scenarios with no issues and multiple issues.

import unittest

from surveytsek.issues import ValidationIssue
from surveytsek.report import AuditReport


class TestAuditReport(unittest.TestCase):
    def test_summary_and_count(self):
        issues = [
            ValidationIssue("missing", 2, ["rating"], "Blank rating"),
            ValidationIssue("rating_range", 1, ["rating"], "Out of range"),
        ]
        report = AuditReport(issues, total_rows=4, checks_run=2)
        self.assertEqual(report.get_issue_count(), 2)
        summary = report.get_summary()
        self.assertIn("Total survey records: 4", summary)
        self.assertIn("Validation checks performed: 2", summary)
        self.assertIn("Total issues found: 2", summary)
        self.assertIn("Blank rating", summary)
        self.assertIn("AuditReport(", repr(report))

    def test_no_issues(self):
        report = AuditReport([], total_rows=3, checks_run=2)
        self.assertEqual(report.get_issue_count(), 0)
        self.assertIn("No issues found.", report.get_summary())

    def test_invalid_counts_rejected(self):
        with self.assertRaises(ValueError):
            AuditReport([], total_rows=-1, checks_run=1)


if __name__ == "__main__":
    unittest.main()
