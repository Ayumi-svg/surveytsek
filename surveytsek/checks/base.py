# Author: Ashley Vallejos
# Purpose: Defines the common interface for validation checks.
# Responsibility:
# - Establish the BaseCheck abstract class.
# - Define the required validation method.
# - Provide a consistent structure for all checks.
# Notes: Shared foundation ni siya. Agree on the method parameters and return format with everyone first.

from abc import ABC, abstractmethod

from surveytsek.dataset import SurveyDataset
from surveytsek.issues import ValidationIssue

"""BaseCheck: the parent class that all of our validation checks follow."""
class BaseCheck(ABC):
    """The shared blueprint of every check (missing, duplicates, rating, choices).

    It only says that every check must have a validate() method. That way the
    auditor can run any check the same way, even without knowing which one it is.
    """
    @abstractmethod
    def validate(self, dataset: SurveyDataset) -> list[ValidationIssue]:
        """Look through the dataset and return the problems found.

        Returns a list of ValidationIssue, or an empty list if nothing is wrong.
        It must never change the dataset. Row numbers start at 1 (the header
        is not counted).
        """
        raise NotImplementedError