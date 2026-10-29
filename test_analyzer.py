"""
test_analyzer.py - Comprehensive test suite for Technical Document Analyzer.

Tests all required test cases:
1. A normal technical document.
2. An empty file.
3. A document containing only headings.
4. A file containing punctuation and mixed capitalization.
5. A missing or inaccessible file.
6. Saving a report to a valid destination.
7. Handling a save error.
"""

import os
import tempfile
import unittest

from analyzer import (
    analyze_document,
    count_characters,
    count_headings,
    count_paragraphs,
    extract_words,
    generate_report_text,
    get_frequent_words,
    is_heading,
    read_document,
    save_report,
)


class TestTechnicalDocumentAnalyzer(unittest.TestCase):
    """Test suite verifying all core requirements and edge cases."""

    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        # Clean up temporary files
        self.test_dir.cleanup()

    def _create_temp_file(self, filename, content):
        filepath = os.path.join(self.test_dir.name, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath

    # --------------------------------------------------------------------------
    # Case 1: Normal technical document
    # --------------------------------------------------------------------------
    def test_case_1_normal_technical_document(self):
        filepath = os.path.join("sample_documents", "arduino_sensor_system.txt")
        self.assertTrue(os.path.exists(filepath), f"Sample file missing: {filepath}")

        content = read_document(filepath)
        self.assertGreater(len(content), 100)

        results = analyze_document(content, filepath=filepath)
        self.assertEqual(results["filename"], "arduino_sensor_system.txt")
        self.assertGreater(results["total_words"], 100)
        self.assertGreater(results["total_characters"], 500)
        self.assertGreater(results["characters_no_spaces"], 400)
        self.assertGreater(results["paragraph_count"], 5)
        self.assertGreater(results["heading_count"], 3)
        self.assertEqual(len(results["frequent_words"]), 10)

        # Check that top frequent words contain technical terms from the doc
        top_words = [word for word, count in results["frequent_words"]]
        self.assertIn("sensor", top_words)

        # Test report generation for normal document
        report = generate_report_text(results)
        self.assertIn("TECHNICAL DOCUMENT ANALYSIS REPORT", report)
        self.assertIn("arduino_sensor_system.txt", report)
        self.assertIn("sensor", report)

    # --------------------------------------------------------------------------
    # Case 2: Empty file
    # --------------------------------------------------------------------------
    def test_case_2_empty_file(self):
        empty_path = self._create_temp_file("empty.txt", "")
        content = read_document(empty_path)
        self.assertEqual(content, "")

        results = analyze_document(content, filepath=empty_path)
        self.assertEqual(results["total_words"], 0)
        self.assertEqual(results["total_characters"], 0)
        self.assertEqual(results["characters_no_spaces"], 0)
        self.assertEqual(results["paragraph_count"], 0)
        self.assertEqual(results["heading_count"], 0)
        self.assertEqual(results["frequent_words"], [])

        report = generate_report_text(results)
        self.assertIn("Total Words                     : 0", report)
        self.assertIn("No significant words found", report)

    # --------------------------------------------------------------------------
    # Case 3: Document containing only headings
    # --------------------------------------------------------------------------
    def test_case_3_document_with_only_headings(self):
        heading_text = (
            "# System Architecture Specification\n\n"
            "## 1. Subsystem Decomposition\n\n"
            "1.1 Power Management Unit\n\n"
            "2. Network Topology\n\n"
            "A. Diagnostic Matrix\n"
        )
        headings_path = self._create_temp_file("headings_only.txt", heading_text)
        content = read_document(headings_path)
        results = analyze_document(content, filepath=headings_path)

        self.assertEqual(results["heading_count"], 5)
        self.assertEqual(results["paragraph_count"], 5)
        self.assertGreater(results["total_words"], 0)

        # Confirm heading detector directly on known lines
        self.assertTrue(is_heading("# System Architecture Specification"))
        self.assertTrue(is_heading("## 1. Subsystem Decomposition"))
        self.assertTrue(is_heading("1.1 Power Management Unit"))
        self.assertTrue(is_heading("2. Network Topology"))
        self.assertTrue(is_heading("A. Diagnostic Matrix"))
        self.assertFalse(is_heading("Just normal body text without heading syntax"))

    # --------------------------------------------------------------------------
    # Case 4: File containing punctuation and mixed capitalization
    # --------------------------------------------------------------------------
    def test_case_4_punctuation_and_mixed_capitalization(self):
        text = (
            "TEMPERATURE! Sensor, sensor; (temperature) - SENSOR... "
            "[data/logging]: DATA? Voltage: 5V, 5V, 5V."
        )
        punct_path = self._create_temp_file("punct_test.txt", text)
        content = read_document(punct_path)
        results = analyze_document(content, filepath=punct_path)

        # "sensor" appears 3 times ("Sensor", "sensor", "SENSOR")
        # "temperature" appears 2 times ("TEMPERATURE!", "(temperature)")
        # "data" appears 2 times ("data", "DATA?")
        # "5v" appears 3 times ("5V", "5V", "5V")
        # "logging" appears 1 time
        # "voltage" appears 1 time
        freq_dict = dict(results["frequent_words"])

        self.assertEqual(freq_dict.get("sensor"), 3)
        self.assertEqual(freq_dict.get("temperature"), 2)
        self.assertEqual(freq_dict.get("data"), 2)
        self.assertEqual(freq_dict.get("5v"), 3)
        self.assertEqual(freq_dict.get("logging"), 1)

        # Verify no stop words or raw punctuation leaked into frequent words
        for word in freq_dict.keys():
            self.assertTrue(word.isalnum())

    # --------------------------------------------------------------------------
    # Case 5: Missing or inaccessible file
    # --------------------------------------------------------------------------
    def test_case_5_missing_or_inaccessible_file(self):
        non_existent_file = os.path.join(self.test_dir.name, "missing_document_xyz.txt")
        with self.assertRaises(FileNotFoundError):
            read_document(non_existent_file)

        # Testing directory path instead of a file
        with self.assertRaises(IsADirectoryError):
            read_document(self.test_dir.name)

    # --------------------------------------------------------------------------
    # Case 6: Saving a report to a valid destination
    # --------------------------------------------------------------------------
    def test_case_6_saving_report_valid_destination(self):
        doc_path = os.path.join("sample_documents", "software_install_guide.txt")
        content = read_document(doc_path)
        results = analyze_document(content, filepath=doc_path)
        report_text = generate_report_text(results)

        output_path = os.path.join(self.test_dir.name, "valid_output_report.txt")
        save_report(report_text, output_path)

        self.assertTrue(os.path.exists(output_path))

        # Read back saved file and verify content
        with open(output_path, "r", encoding="utf-8") as f:
            saved_content = f.read()

        self.assertEqual(saved_content, report_text)
        self.assertIn("TECHNICAL DOCUMENT ANALYSIS REPORT", saved_content)
        self.assertIn("software_install_guide.txt", saved_content)
        self.assertIn("1. BASIC METRICS", saved_content)

    # --------------------------------------------------------------------------
    # Case 7: Handling a save error
    # --------------------------------------------------------------------------
    def test_case_7_handling_save_error(self):
        # Attempt to save to a path where an invalid directory name or null byte exists
        # On Windows, using an illegal filename character like `<>` or `\0` raises an error
        invalid_output_path = os.path.join(self.test_dir.name, "invalid<>name|test?.txt")

        with self.assertRaises(OSError):
            save_report("Test Report Content", invalid_output_path)


if __name__ == "__main__":
    unittest.main()
