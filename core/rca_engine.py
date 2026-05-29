"""Root Cause Analysis Engine.

Advanced RCA using multiple analysis techniques.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.analyzer import AnalysisResult, analyze_error
from core.error_groups import ErrorGroup, group_errors
from core.knowledge_base import KnowledgeBase


@dataclass
class RCAResult:
    """Root Cause Analysis result."""

    root_cause: str
    confidence: float
    category: str
    severity: str
    evidence: list[str] = field(default_factory=list)
    related_errors: list[str] = field(default_factory=list)
    fix_suggestions: list[str] = field(default_factory=list)
    knowledge_matches: list[dict[str, Any]] = field(default_factory=list)


class RCAEngine:
    """Root Cause Analysis engine combining multiple techniques."""

    def __init__(self) -> None:
        """Initialize the RCA engine."""
        self.knowledge_base = KnowledgeBase()

    def analyze(
        self,
        errors: list[dict[str, Any]],
        context: dict[str, Any] | None = None,
    ) -> RCAResult:
        """Perform root cause analysis on a set of errors.

        Args:
            errors: List of error dictionaries.
            context: Additional context (service, environment, etc.).

        Returns:
            RCAResult with root cause analysis.
        """
        if not errors:
            return RCAResult(
                root_cause="No errors to analyze",
                confidence=0.0,
                category="unknown",
                severity="low",
            )

        # Step 1: Group similar errors
        groups = group_errors(errors)

        # Step 2: Analyze each error
        analyses: list[AnalysisResult] = []
        for error in errors:
            message = error.get("message", "")
            if message:
                analyses.append(analyze_error(message))

        # Step 3: Find patterns
        category_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        for analysis in analyses:
            category_counts[analysis.category] = category_counts.get(analysis.category, 0) + 1
            severity_counts[analysis.severity] = severity_counts.get(analysis.severity, 0) + 1

        # Step 4: Determine dominant category
        dominant_category = (
            max(category_counts, key=category_counts.get)
            if category_counts else "unknown"
        )
        dominant_severity = (
            max(severity_counts, key=severity_counts.get)
            if severity_counts else "low"
        )

        # Step 5: Search knowledge base
        knowledge_matches = self._search_knowledge(errors, dominant_category)

        # Step 6: Generate root cause
        root_cause = self._generate_root_cause(
            groups, analyses, dominant_category, knowledge_matches
        )

        # Step 7: Calculate confidence
        confidence = self._calculate_confidence(
            analyses, knowledge_matches, len(errors)
        )

        # Step 8: Collect evidence
        evidence = self._collect_evidence(errors, groups, analyses)

        # Step 9: Generate fix suggestions
        fix_suggestions = self._generate_fix_suggestions(
            dominant_category, knowledge_matches
        )

        return RCAResult(
            root_cause=root_cause,
            confidence=confidence,
            category=dominant_category,
            severity=dominant_severity,
            evidence=evidence,
            fix_suggestions=fix_suggestions,
            knowledge_matches=knowledge_matches,
        )

    def _search_knowledge(
        self,
        errors: list[dict[str, Any]],
        category: str,
    ) -> list[dict[str, Any]]:
        """Search knowledge base for matching patterns."""
        matches = []

        # Search by category
        category_entries = self.knowledge_base.get_by_category(category)
        for entry in category_entries:
            matches.append({
                "id": entry.id,
                "title": entry.title,
                "solution": entry.solution,
                "confidence": 0.7,
            })

        # Search by error messages
        for error in errors[:3]:  # Limit to first 3 errors
            message = error.get("message", "")
            if message:
                results = self.knowledge_base.search(message[:50])
                for result in results:
                    if result.id not in [m["id"] for m in matches]:
                        matches.append({
                            "id": result.id,
                            "title": result.title,
                            "solution": result.solution,
                            "confidence": 0.5,
                        })

        return matches[:5]  # Limit to top 5

    def _generate_root_cause(
        self,
        groups: dict[str, ErrorGroup],
        analyses: list[AnalysisResult],
        category: str,
        knowledge_matches: list[dict[str, Any]],
    ) -> str:
        """Generate root cause description."""
        # Use knowledge base if available
        if knowledge_matches:
            best_match = knowledge_matches[0]
            return f"{best_match['title']}: {best_match['solution'][:100]}"

        # Use analysis results
        if analyses:
            # Find most common error type
            type_counts: dict[str, int] = {}
            for analysis in analyses:
                type_counts[analysis.error_type] = type_counts.get(analysis.error_type, 0) + 1

            if type_counts:
                common_type = max(type_counts, key=type_counts.get)
                return f"Multiple {common_type} errors detected in {category} category"

        return f"Unknown root cause in {category} category"

    def _calculate_confidence(
        self,
        analyses: list[AnalysisResult],
        knowledge_matches: list[dict[str, Any]],
        error_count: int,
    ) -> float:
        """Calculate confidence score."""
        confidence = 0.5  # Base confidence

        # Boost for known patterns
        known_count = sum(1 for a in analyses if a.error_type != "Unknown")
        if analyses:
            confidence += (known_count / len(analyses)) * 0.2

        # Boost for knowledge base matches
        if knowledge_matches:
            confidence += 0.15

        # Boost for multiple errors (more data)
        if error_count > 5:
            confidence += 0.1

        return min(confidence, 0.95)

    def _collect_evidence(
        self,
        errors: list[dict[str, Any]],
        groups: dict[str, ErrorGroup],
        analyses: list[AnalysisResult],
    ) -> list[str]:
        """Collect evidence for the root cause."""
        evidence = []

        # Add error group info
        for group in list(groups.values())[:3]:
            evidence.append(f"Error group '{group.title}' occurred {group.count} times")

        # Add analysis info
        for analysis in analyses[:3]:
            if analysis.common_causes:
                evidence.append(f"Possible cause: {analysis.common_causes[0]}")

        return evidence

    def _generate_fix_suggestions(
        self,
        category: str,
        knowledge_matches: list[dict[str, Any]],
    ) -> list[str]:
        """Generate fix suggestions."""
        suggestions = []

        # Use knowledge base suggestions
        for match in knowledge_matches[:2]:
            solution = match.get("solution", "")
            if solution:
                suggestions.append(solution)

        # Add category-specific suggestions
        category_suggestions = {
            "network": ["Check network connectivity", "Verify firewall rules"],
            "database": ["Check database connection", "Review query performance"],
            "resource": ["Monitor resource usage", "Check for memory leaks"],
            "code": ["Review recent code changes", "Check error handling"],
            "security": ["Verify credentials", "Check permissions"],
        }

        if category in category_suggestions:
            suggestions.extend(category_suggestions[category])

        return suggestions[:5]
