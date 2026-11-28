# Author: Aria Deligero
# Purpose: Manages and represents survey response data.
# Responsibility:
# - Handle survey datasets provided by users.
# - Provide access to survey records and columns.
# - Support data preparation for validation.
# Notes: Dapat ma preserve the original survey data. 

"""Store survey responses safely for validation checks."""

import pandas as pd


class SurveyDataset:
    """Hold an independent copy of a pandas survey DataFrame."""

    def __init__(self, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")
        self._data = data.copy(deep=True)

    def get_data(self) -> pd.DataFrame:
        """Return a copy so callers cannot modify the stored data."""
        return self._data.copy(deep=True)

    def get_columns(self) -> list[str]:
        """Return the survey's column labels."""
        return list(self._data.columns)

    def __len__(self) -> int:
        """Return the number of survey records."""
        return len(self._data)