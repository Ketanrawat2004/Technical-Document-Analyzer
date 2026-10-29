"""
analyzer.py - Core text analysis engine for Technical Document Analyzer.

This module provides standalone, beginner-friendly functions to:
1. Safely read plain-text UTF-8 files.
2. Count words, characters, non-empty paragraphs, and headings.
3. Perform stop-word filtering and frequency counting using standard dictionaries.
4. Format and save clean technical analysis reports.
"""

import os
import re
import string
from datetime import datetime

# Common English stop words to ignore during frequent word analysis.
# Keeping these in a set makes lookups fast and straightforward.
STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an",
    "and", "any", "are", "aren't", "as", "at", "be", "because", "been",
    "before", "being", "below", "between", "both", "but", "by", "can",
    "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does",
    "doesn't", "doing", "don't", "down", "during", "each", "few", "for",
    "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
    "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers",
    "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
    "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its",
    "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no",
    "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "will", "with", "won't",
    "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your",
    "yours", "yourself", "yourselves"
}


def read_document(filepath):
    """
    Safely opens and reads a text file using UTF-8 encoding.

    Returns:
        The content of the file as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        UnicodeDecodeError: If the file is not valid UTF-8.
        PermissionError: If access to the file is denied.
        OSError: For other operating system / I/O errors.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: '{filepath}'")

    if not os.path.isfile(filepath):
        raise IsADirectoryError(f"Expected a file, but found a directory: '{filepath}'")

    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def count_characters(text):
    """
    Counts total characters and characters excluding whitespace.

    Returns:
        tuple: (total_characters, characters_excluding_whitespace)
    """
    total_chars = len(text)
    # Count characters that are not whitespace (spaces, tabs, newlines)
    chars_no_whitespace = sum(1 for char in text if not char.isspace())
    return total_chars, chars_no_whitespace


def count_paragraphs(text):
    """
    Counts non-empty paragraphs in a text document.
    
    A paragraph is treated as a block of text separated by one or more blank lines.
    This tracks transitions from blank lines to text lines.
    """
    lines = text.splitlines()
    paragraph_count = 0
    in_paragraph = False

    for line in lines:
        if line.strip():  # Line contains non-whitespace characters
            if not in_paragraph:
                paragraph_count += 1
                in_paragraph = True
        else:  # Blank line
            in_paragraph = False

    return paragraph_count


def is_heading(line):
    """
    Checks if a single line of text represents a heading.

    Supports simple, standard technical writing conventions:
    1. Markdown style: lines starting with '#' followed by a space
       (e.g., '# Title', '## 1. Overview').
    2. Numbered section headings: lines starting with digits/dots or capital letters
       followed by a dot/space (e.g., '1. Introduction', '1.1 System Architecture',
       'A. Hardware Requirements').

    Limitation: In plain text without semantic tags, numbered list items formatted
    identically to numbered headings (e.g., '1. Connect cable') will also be counted.
    """
    stripped = line.strip()
    if not stripped:
        return False

    # Check Markdown heading format: '#' followed by a space and heading text
    if stripped.startswith("#"):
        parts = stripped.split(maxsplit=1)
        # Ensure the first token consists purely of '#' characters (e.g. '#', '##', '###')
        if parts[0].replace("#", "") == "" and len(parts) > 1:
            return True

    # Check Numbered heading format:
    # Matches patterns like:
    # "1. Introduction" or "1) Introduction"
    # "1.1 System Architecture" or "1.1. System Architecture"
    # "1.1.2 Power Supply"
    # "A. Overview" or "A) Overview"
    numbered_heading_pattern = r"^([0-9]+(\.[0-9]+)+\.?|[0-9]+[\.\)]|[A-Za-z][\.\)])\s+\S+"
    if re.match(numbered_heading_pattern, stripped):
        return True

    return False


def count_headings(text):
    """
    Counts the total number of heading lines detected in the text.
    """
    heading_count = 0
    for line in text.splitlines():
        if is_heading(line):
            heading_count += 1
    return heading_count


def extract_words(text):
    """
    Extracts lowercase words from text, removing punctuation.

    Punctuation marks (like commas, periods, brackets, slashes) are replaced
    with spaces so adjacent words like 'sensor/switch' or 'status:active'
    are separated cleanly into individual words.
    """
    # Convert all characters to lowercase for uniform comparison
    clean_text = text.lower()

    # Replace each punctuation character with a space
    for char in string.punctuation:
        clean_text = clean_text.replace(char, " ")

    # split() separates by any whitespace (spaces, tabs, newlines)
    raw_tokens = clean_text.split()

    # Keep tokens that contain at least one alphanumeric character
    words = []
    for token in raw_tokens:
        if any(c.isalnum() for c in token):
            words.append(token)

    return words


def get_frequent_words(words, top_n=10):
    """
    Counts word frequencies using a standard Python dictionary and returns
    the top N most frequent words, excluding common English stop words
    and purely numeric tokens.

    Returns:
        A list of tuples: [(word, count), ...] sorted from highest count to lowest.
        Ties are sorted alphabetically.
    """
    word_counts = {}

    for word in words:
        # Ignore purely numeric tokens (e.g. "1", "2026") and common stop words
        if word.isdigit() or word in STOP_WORDS:
            continue

        # Count occurrences in dictionary
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    # Sort primarily by frequency (descending), then alphabetically (ascending)
    sorted_words = sorted(
        word_counts.items(),
        key=lambda item: (-item[1], item[0])
    )

    return sorted_words[:top_n]


def analyze_document(text, filepath=""):
    """
    Performs complete analysis on document text.

    Returns:
        dict: A dictionary containing all computed metrics and frequent words.
    """
    total_chars, chars_no_spaces = count_characters(text)
    paragraphs = count_paragraphs(text)
    headings = count_headings(text)
    words = extract_words(text)
    frequent_words = get_frequent_words(words, top_n=10)

    filename = os.path.basename(filepath) if filepath else "Untitled Document"

    return {
        "filepath": filepath,
        "filename": filename,
        "total_words": len(words),
        "total_characters": total_chars,
        "characters_no_spaces": chars_no_spaces,
        "paragraph_count": paragraphs,
        "heading_count": headings,
        "frequent_words": frequent_words,
    }


def generate_report_text(analysis_data, timestamp=None):
    """
    Formats the analysis results into a clean, human-readable text report.
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    divider = "=" * 78
    section_divider = "-" * 78

    report_lines = [
        divider,
        "TECHNICAL DOCUMENT ANALYSIS REPORT",
        divider,
        f"Generated On      : {timestamp}",
        f"Source Document   : {analysis_data.get('filename', 'Unknown')}",
        f"Source Path       : {analysis_data.get('filepath', 'Not specified')}",
        "",
        section_divider,
        "1. BASIC METRICS",
        section_divider,
        f"Total Words                     : {analysis_data.get('total_words', 0):,}",
        f"Total Characters (with spaces)  : {analysis_data.get('total_characters', 0):,}",
        f"Characters (excluding spaces)   : {analysis_data.get('characters_no_spaces', 0):,}",
        f"Non-Empty Paragraphs            : {analysis_data.get('paragraph_count', 0):,}",
        f"Headings Detected               : {analysis_data.get('heading_count', 0):,}",
        "",
        section_divider,
        "2. TOP 10 FREQUENT WORDS (Common English Stop Words Excluded)",
        section_divider,
    ]

    frequent_words = analysis_data.get("frequent_words", [])
    if frequent_words:
        report_lines.append(f"{'Rank':<6}{'Word':<30}{'Occurrences':<10}")
        report_lines.append("-" * 46)
        for rank, (word, count) in enumerate(frequent_words, start=1):
            report_lines.append(f"{rank:<6}{word:<30}{count:<10}")
    else:
        report_lines.append("No significant words found (document is empty or contains only stop words).")

    report_lines.extend([
        "",
        section_divider,
        "3. ANALYSIS NOTES & LIMITATIONS",
        section_divider,
        "- Headings are detected using Markdown prefixes ('# ') and numbered section prefixes",
        "  (e.g., '1. Introduction', '1.1 System Architecture', 'A. Overview').",
        "- Numbered list items in plain text that share this formatting may also be counted.",
        "- Common English stop words (such as 'the', 'is', 'and', 'to') and numeric digits",
        "  are omitted from the top frequent words list.",
        divider,
        "End of Report",
        divider,
    ])

    return "\n".join(report_lines) + "\n"


def save_report(report_text, output_filepath):
    """
    Saves the formatted report text to a destination file using UTF-8 encoding.

    Raises:
        OSError: If creating directories or writing the file fails.
    """
    output_dir = os.path.dirname(output_filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(output_filepath, "w", encoding="utf-8") as file:
        file.write(report_text)
