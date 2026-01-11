"""Python Regular Expression Examples

Source code for docs/notes/basic/python-rexp.rst
"""

import re
import pytest


# Basic Matching
def search_digits(text: str) -> str | None:
    """Find first sequence of digits."""
    m = re.search(r"\d+", text)
    return m.group() if m else None


def match_start(pattern: str, text: str) -> bool:
    """Check if text starts with pattern."""
    return re.match(pattern, text) is not None


# Find All
def find_all_digits(text: str) -> list:
    """Find all digit sequences."""
    return re.findall(r"\d+", text)


def find_key_values(text: str) -> list:
    """Find all key=value pairs."""
    return re.findall(r"(\w+)=(\d+)", text)


# Groups
def parse_date(text: str) -> dict | None:
    """Parse date string into components."""
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
    if m:
        return {"year": m.group(1), "month": m.group(2), "day": m.group(3)}
    return None


def parse_date_named(text: str) -> dict | None:
    """Parse date using named groups."""
    pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
    m = re.search(pattern, text)
    return m.groupdict() if m else None


# Lookahead/Lookbehind
def find_before_at(text: str) -> list:
    """Find words before @ symbol."""
    return re.findall(r"\w+(?=@)", text)


def find_after_dollar(text: str) -> list:
    """Find numbers after $ symbol."""
    return re.findall(r"(?<=\$)\d+", text)


# Substitution
def replace_digits(text: str, replacement: str = "X") -> str:
    """Replace all digits with replacement."""
    return re.sub(r"\d+", replacement, text)


def double_numbers(text: str) -> str:
    """Double all numbers in text."""
    return re.sub(r"\d+", lambda m: str(int(m.group()) * 2), text)


# Split
def split_whitespace(text: str) -> list:
    """Split by whitespace."""
    return re.split(r"\s+", text)


# Compiled Pattern
EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


def find_emails(text: str) -> list:
    """Find all email addresses."""
    return EMAIL_PATTERN.findall(text)


def is_valid_email(text: str) -> bool:
    """Check if text is valid email."""
    return EMAIL_PATTERN.fullmatch(text) is not None


# Back Reference
def has_repeated_char(text: str) -> bool:
    """Check if text has repeated adjacent characters."""
    return re.search(r"(\w)\1", text) is not None


def match_html_tag(text: str) -> str | None:
    """Match HTML tag with matching close tag."""
    m = re.search(r"<(\w+)>.*?</\1>", text)
    return m.group() if m else None


# Tests
class TestBasicMatching:
    def test_search_digits(self):
        assert search_digits("abc123def") == "123"
        assert search_digits("no digits") is None

    def test_match_start(self):
        assert match_start(r"\d+", "123abc")
        assert not match_start(r"\d+", "abc123")


class TestFindAll:
    def test_find_all_digits(self):
        assert find_all_digits("a1b22c333") == ["1", "22", "333"]

    def test_find_key_values(self):
        assert find_key_values("a=1 b=2") == [("a", "1"), ("b", "2")]


class TestGroups:
    def test_parse_date(self):
        result = parse_date("2024-01-15")
        assert result == {"year": "2024", "month": "01", "day": "15"}

    def test_parse_date_named(self):
        result = parse_date_named("2024-01-15")
        assert result == {"year": "2024", "month": "01", "day": "15"}


class TestLookaround:
    def test_lookahead(self):
        assert find_before_at("user@example.com") == ["user"]

    def test_lookbehind(self):
        assert find_after_dollar("$100 $200") == ["100", "200"]


class TestSubstitution:
    def test_replace_digits(self):
        assert replace_digits("a1b2c3") == "aXbXcX"

    def test_double_numbers(self):
        assert double_numbers("a1b2c3") == "a2b4c6"


class TestSplit:
    def test_split_whitespace(self):
        assert split_whitespace("a  b   c") == ["a", "b", "c"]


class TestCompiledPattern:
    def test_find_emails(self):
        text = "Contact: user@example.com or admin@test.org"
        assert find_emails(text) == ["user@example.com", "admin@test.org"]

    def test_is_valid_email(self):
        assert is_valid_email("user@example.com")
        assert not is_valid_email("invalid")


class TestBackReference:
    def test_repeated_char(self):
        assert has_repeated_char("hello")  # ll
        assert not has_repeated_char("world")

    def test_html_tag(self):
        assert match_html_tag("<b>bold</b>") == "<b>bold</b>"
        assert match_html_tag("<b>text</i>") is None
