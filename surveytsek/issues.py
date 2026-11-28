# Author: Aria Deligero
# Purpose: Represents data quality issues detected by checks.
# Responsibility:
# - Define the structure of a validation issue.
# - Store details about detected problems.
# - Provide a consistent format for validation findings.
# Notes: Paki coordinate lang ang issue structure with me (Love), Ashley, Patrick gamiton ni sa tanan checkss.

"""Define a consistent record for a survey validation problem."""

class ValidationIssue:
    """Describe one issue detected by a validation check.

    row_number is the affected row position (zero-based by convention).
    The team should agree on the row-number convention before integration.
    """

    def __init__(
        self,
        check_type: str,
        row_number: int,
        columns: list[str],
        message: str,
    ):
        if not isinstance(check_type, str):
            raise TypeError("check_type must be a string")
        if not isinstance(row_number, int) or isinstance(row_number, bool):
            raise TypeError("row_number must be an integer")
        if not isinstance(columns, list) or not all(isinstance(c, str) for c in columns):
            raise TypeError("columns must be a list of strings")
        if not isinstance(message, str):
            raise TypeError("message must be a string")
        self.check_type = check_type
        self.row_number = row_number
        self.columns = columns.copy()
        self.message = message

    def __str__(self) -> str:
        column_names = ", ".join(self.columns) if self.columns else "N/A"
        return (
            f"{self.check_type} at row {self.row_number} "
            f"(columns: {column_names}): {self.message}"
        )
