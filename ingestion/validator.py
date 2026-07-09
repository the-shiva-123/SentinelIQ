from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from utils.domain import Document


@dataclass(slots=True)
class ValidationIssue:
    """Represents a single validation issue for an ingested document."""

    message: str
    severity: str = "warning"


@dataclass(slots=True)
class ValidationResult:
    """The outcome of validating a document."""

    document: Document
    issues: List[ValidationIssue] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.issues


class DocumentValidator:
    """Lightweight validator for basic ingestion quality checks."""

    def validate(self, document: Document) -> ValidationResult:
        issues: List[ValidationIssue] = []
        if not document.content or not document.content.strip():
            issues.append(ValidationIssue("Document content is empty."))
        if len(document.content.split()) < 3:
            issues.append(ValidationIssue("Document content is too short to be useful."))
        return ValidationResult(document=document, issues=issues)
