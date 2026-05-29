"""Tests for code_search tool."""

from pathlib import Path

from scenarios.bug_diagnoser.src.tools.code_search import code_search


class TestCodeSearch:
    """Tests for the code_search tool."""

    def test_search_finds_pattern(self, tmp_path: Path) -> None:
        """Should find a pattern in source files."""
        test_file = tmp_path / "app.py"
        test_file.write_text("def hello_world():\n    return 'hello'\n")

        results = code_search.invoke({
            "pattern": "hello_world",
            "path": str(tmp_path),
            "extensions": ".py",
        })

        assert len(results) >= 1
        assert any("hello_world" in r.get("content", "") for r in results)

    def test_search_case_insensitive(self, tmp_path: Path) -> None:
        """Should perform case-insensitive search."""
        test_file = tmp_path / "config.py"
        test_file.write_text("DATABASE_HOST = 'localhost'\n")

        results = code_search.invoke({
            "pattern": "database_host",
            "path": str(tmp_path),
            "extensions": ".py",
        })

        assert len(results) >= 1

    def test_search_with_extension_filter(self, tmp_path: Path) -> None:
        """Should only search specified file types."""
        py_file = tmp_path / "app.py"
        py_file.write_text("error_handler()\n")
        txt_file = tmp_path / "notes.txt"
        txt_file.write_text("error_handler()\n")

        results = code_search.invoke({
            "pattern": "error_handler",
            "path": str(tmp_path),
            "extensions": ".py",
        })

        assert len(results) >= 1
        assert all(".py" in r.get("file", "") for r in results)

    def test_search_no_matches(self, tmp_path: Path) -> None:
        """Should return empty list when no matches found."""
        test_file = tmp_path / "app.py"
        test_file.write_text("def hello():\n    pass\n")

        results = code_search.invoke({
            "pattern": "nonexistent_function",
            "path": str(tmp_path),
            "extensions": ".py",
        })

        assert results == []

    def test_search_nonexistent_path(self) -> None:
        """Should return error for nonexistent path."""
        results = code_search.invoke({
            "pattern": "test",
            "path": "/nonexistent/path",
        })

        assert len(results) == 1
        assert "error" in results[0]

    def test_search_max_results(self, tmp_path: Path) -> None:
        """Should respect max_results limit."""
        # Create a file with many matches
        content = "\n".join(["error_handler()"] * 100)
        test_file = tmp_path / "many.py"
        test_file.write_text(content)

        results = code_search.invoke({
            "pattern": "error_handler",
            "path": str(tmp_path),
            "extensions": ".py",
            "max_results": 5,
        })

        assert len(results) <= 5

    def test_search_skips_hidden_dirs(self, tmp_path: Path) -> None:
        """Should skip .git and other hidden directories."""
        # Create file in .git directory
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        git_file = git_dir / "config.py"
        git_file.write_text("error_handler()\n")

        # Create file in normal directory
        normal_file = tmp_path / "app.py"
        normal_file.write_text("error_handler()\n")

        results = code_search.invoke({
            "pattern": "error_handler",
            "path": str(tmp_path),
            "extensions": ".py",
        })

        # Should only find the normal file
        assert all(".git" not in r.get("file", "") for r in results)

    def test_search_line_numbers(self, tmp_path: Path) -> None:
        """Should return correct line numbers."""
        test_file = tmp_path / "app.py"
        test_file.write_text("line1\nline2\nerror_here\nline4\n")

        results = code_search.invoke({
            "pattern": "error_here",
            "path": str(tmp_path),
            "extensions": ".py",
        })

        assert len(results) == 1
        assert results[0]["line"] == 3
