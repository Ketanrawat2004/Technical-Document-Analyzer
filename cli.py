"""
cli.py - Command-Line Interface for Technical Document Analyzer.

Runs the Technical Document Analyzer directly in the terminal without opening a GUI window.
"""

import os
from analyzer import (
    analyze_document,
    generate_report_text,
    read_document,
    save_report,
)


def get_document_path():
    """Prompts the user to enter a valid .txt file path."""
    while True:
        user_input = input("Enter path to a .txt file (or 'q' to quit): ").strip()
        if user_input.lower() == "q":
            return None

        filepath = user_input.strip("\"'")

        if not filepath:
            print("Error: Please enter a file path.\n")
            continue

        if not os.path.exists(filepath):
            print(f"Error: File not found at '{filepath}'. Please check the path and try again.\n")
            continue

        if not os.path.isfile(filepath):
            print(f"Error: '{filepath}' is a directory, not a file.\n")
            continue

        return filepath


def display_results(analysis):
    """Prints analysis metrics and top frequent words to the terminal."""
    print("\n" + "=" * 62)
    print("ANALYSIS RESULTS")
    print("=" * 62)
    print(f"Document File       : {analysis['filename']}")
    print(f"Total Words         : {analysis['total_words']:,}")
    print(f"Total Characters    : {analysis['total_characters']:,} (including whitespace)")
    print(f"Characters (no spc) : {analysis['characters_no_spaces']:,} (excluding whitespace)")
    print(f"Paragraphs          : {analysis['paragraph_count']:,}")
    print(f"Headings Detected   : {analysis['heading_count']:,}")
    print("-" * 62)

    frequent_words = analysis.get("frequent_words", [])
    if frequent_words:
        print("TOP 10 FREQUENT WORDS (Common stop words & numbers excluded):")
        print(f"{'Rank':<6}{'Word':<26}{'Occurrences':<10}")
        print("-" * 42)
        for rank, (word, count) in enumerate(frequent_words, start=1):
            print(f"{rank:<6}{word:<26}{count:<10}")
    else:
        print("No significant words found (document is empty or contains only stop words).")

    print("=" * 62 + "\n")


def prompt_save_report(analysis):
    """Prompts user to save the analysis report."""
    default_name = f"{os.path.splitext(analysis['filename'])[0]}_report.txt"
    default_path = os.path.join("output", default_name)

    print(f"Default save path: {default_path}")
    choice = input("Enter output path (press Enter for default, or 'n' to skip saving): ").strip()

    if choice.lower() == "n":
        print("Report not saved.")
        return

    output_path = choice.strip("\"'") if choice else default_path

    if os.path.exists(output_path):
        confirm = input(f"Notice: '{output_path}' already exists. Overwrite? (y/n): ").strip().lower()
        if confirm != "y":
            print("Save cancelled by user.")
            return

    report_text = generate_report_text(analysis)

    try:
        save_report(report_text, output_path)
        print(f"Success: Report successfully saved to '{output_path}'.\n")
    except Exception as err:
        print(f"Error: Failed to save report to '{output_path}': {err}\n")


def main():
    """Main CLI execution flow."""
    print("=" * 62)
    print("   TECHNICAL DOCUMENT ANALYZER (CLI)")
    print("=" * 62)

    filepath = get_document_path()
    if not filepath:
        print("Operation cancelled. Exiting program.")
        return

    try:
        content = read_document(filepath)
    except UnicodeDecodeError:
        print(f"Error: Could not read '{filepath}' using UTF-8 encoding.")
        return
    except PermissionError:
        print(f"Error: Permission denied when accessing '{filepath}'.")
        return
    except Exception as err:
        print(f"Error: Unexpected issue reading document: {err}")
        return

    if not content.strip():
        print(f"\nNotice: The document '{filepath}' is empty (0 characters / 0 words).")

    analysis = analyze_document(content, filepath=filepath)
    display_results(analysis)
    prompt_save_report(analysis)
    print("Analysis finished.")


if __name__ == "__main__":
    main()
