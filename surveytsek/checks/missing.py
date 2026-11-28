# Author: Ashley Vallejos
# Purpose: Detects missing or unanswered survey responses.
# Responsibility:
# - Identify empty or missing response values.
# - Generate appropriate validation issues.
# - Support missing-response testing.
# Notes: Inherit from BaseCheck and follow the agreed validation interface.

import pandas as pd

from surveytsek.checks.base import BaseCheck
from surveytsek.dataset import SurveyDataset
from surveytsek.issues import ValidationIssue

"""MissingValueCheck: finds survey questions that were left unanswered."""
class MissingValueCheck(BaseCheck):
    """Checks the chosen columns for missing answers.

    A cell counts as missing if it is empty (NaN or None) or only has spaces.
    Every missing cell gets its own ValidationIssue.
    """

    CHECK_TYPE = "missing_value"

    def __init__(self, columns: list[str]):
        """Save the columns we want to check.

        Raises ValueError if columns is empty or is not a list of column names.
        """
        if (not isinstance(columns, (list, tuple)) or len(columns) == 0
                or not all(isinstance(c, str) for c in columns)):
            raise ValueError("columns must be a non-empty list of column names")
        self._columns = list(columns)

    @property
    def columns(self) -> list[str]:
        """The columns being checked. Gives a copy, so the original stays safe."""
        return list(self._columns)

    @staticmethod
    def _is_missing(value) -> bool:
        """Return True if the value is NaN/None, or text that is empty or only spaces."""
        if pd.isna(value):
            return True
        return isinstance(value, str) and value.strip() == ""

    def validate(self, dataset: SurveyDataset) -> list[ValidationIssue]:
        """Go through every row and report each missing cell, in row order.

        Raises ValueError if one of the chosen columns is not in the dataset.
        """
        data = dataset.get_data()

        unknown = [c for c in self._columns if c not in data.columns]
        if unknown:
            raise ValueError(f"column(s) not found in dataset: {unknown}")

        issues = []
        for row_number, (_, row) in enumerate(data.iterrows(), start=1):
            for column in self._columns:
                if self._is_missing(row[column]):
                    issues.append(ValidationIssue(
                        check_type=self.CHECK_TYPE,
                        row_number=row_number,
                        columns=[column],
                        message=f"Missing value in column '{column}'",
                    ))
        return issues