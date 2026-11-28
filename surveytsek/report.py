# Author: Aria Deligero
# Purpose: Organizes and presents survey audit results.
# Responsibility:
# - Collect validation findings.
# - Summarize detected data quality problems.
# - Present understandable audit summaries.
# Notes: Dapat dili siya mag run ug checks, tig organize ra ni siya sa results.

"""Summarize issues found during a survey audit."""

from collections import Counter

from .issues import ValidationIssue


class AuditReport:
    """Store validation findings and audit statistics."""

    def __init__(
        self,
        issues: list[ValidationIssue],
        total_rows: int,
        checks_run: int,
    ):
        if not isinstance(issues, list) or not all(
            isinstance(issue, ValidationIssue) for issue in issues
        ):
            raise TypeError("issues must be a list of ValidationIssue objects")
        if not isinstance(total_rows, int) or isinstance(total_rows, bool) or total_rows < 0:
            raise ValueError("total_rows must be a non-negative integer")
        if not isinstance(checks_run, int) or isinstance(checks_run, bool) or checks_run < 0:
            raise ValueError("checks_run must be a non-negative integer")
        self._issues = issues.copy()
        self._total_rows = total_rows
        self._checks_run = checks_run

    def get_issue_count(self) -> int:
        """Return how many validation issues were recorded."""
        return len(self._issues)

    def get_summary(self) -> str:
        """Build a readable summary without changing the survey responses."""
        lines = [
            "SurveyTsek Data Quality Report",
            f"Total survey records: {self._total_rows}",
            f"Validation checks performed: {self._checks_run}",
            f"Total issues found: {self.get_issue_count()}",
        ]
        if not self._issues:
            lines.append("No issues found.")
        else:
            lines.append("Issues by check type:")
            for check_type, count in sorted(Counter(
                issue.check_type for issue in self._issues
            ).items()):
                lines.append(f"- {check_type}: {count}")
            lines.append("Details:")
            for issue in self._issues:
                lines.append(f"- {issue}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"AuditReport(issues={self.get_issue_count()}, "
            f"total_rows={self._total_rows}, checks_run={self._checks_run})"
        )
