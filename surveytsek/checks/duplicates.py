# Author: Ashley Vallejos
# Purpose: Detects duplicate survey respondent records.
# Responsibility:
# - Identify repeated respondent identifiers.
# - Detect duplicate records using agreed criteria.
# - Generate appropriate validation issues.

import pandas as pd

from surveytsek.checks.base import BaseCheck
from surveytsek.dataset import SurveyDataset
from surveytsek.issues import ValidationIssue

"""DuplicateResponseCheck: finds respondents that appear more than once."""
class DuplicateResponseCheck(BaseCheck):
    """Reports ALL records that share the same key.

    The key is made of one or more configurable columns (e.g. respondent_id).
    If respondent 103 appears in rows 3 and 4, BOTH rows get an issue.
    Rows where a key column is missing are skipped: MissingValueCheck is
    responsible for those, so the same problem is not reported twice.
    """

    CHECK_TYPE = "duplicate_response"

    def __init__(self, key_columns: list[str]):
        """Store the columns that identify one respondent.

        Raises ValueError if key_columns is not a non-empty list of strings.
        """
        if (not isinstance(key_columns, (list, tuple)) or len(key_columns) == 0
                or not all(isinstance(c, str) for c in key_columns)):
            raise ValueError("key_columns must be a non-empty list of column names")
        self._key_columns = list(key_columns)

    def validate(self, dataset: SurveyDataset) -> list[ValidationIssue]:
        """Return one issue for every record that shares its key with another.
    
        Raises ValueError if a key column is not in the dataset.
        """
        data = dataset.get_data()

        unknown = [c for c in self._key_columns if c not in data.columns]
        if unknown:
            raise ValueError(f"key column(s) not found in dataset: {unknown}")

        # Step 1: group row numbers by their key.  {(103,): [3, 4], (101,): [1]}
        rows_by_key = {}
        keys = data[self._key_columns].itertuples(index=False, name=None)
        for row_number, key in enumerate(keys, start=1):
            if any(pd.isna(part) for part in key):
                continue                     # missing key: not our job
            rows_by_key.setdefault(key, []).append(row_number)

        # Step 2: every key with 2+ rows is a duplicate -> one issue per row.
        issues = []
        for key, row_numbers in rows_by_key.items():
            if len(row_numbers) < 2:
                continue
            key_text = ", ".join(f"{col}={val}" for col, val in
                                 zip(self._key_columns, key))
            for row_number in row_numbers:
                others = [r for r in row_numbers if r != row_number]
                issues.append(ValidationIssue(
                    check_type=self.CHECK_TYPE,
                    row_number=row_number,
                    columns=list(self._key_columns),
                    message=f"Duplicate key ({key_text}) also found in row(s) {others}",
                ))

        issues.sort(key=lambda issue: issue.row_number)
        return issues

