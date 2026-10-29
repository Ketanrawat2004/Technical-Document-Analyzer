"""
generate_reports.py - Human-written Microsoft Word style report generator.

Creates:
1. technical_summary_report.pdf: A clean Word-style PDF with:
   - Natural human writing (no AI fluff, no fake corporate jargon).
   - Embedded flowchart diagram (Image 1).
   - Removed metadata table (Image 2).
   - Running header and simple 'Page X of Y' footer (no portfolio text).
2. technical_summary_report.xml: Plain, readable XML document.
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class SimpleWordCanvas(canvas.Canvas):
    """Clean two-pass canvas for simple Word-style header and footer."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        page_width, page_height = letter

        # Running header on page 2 and later
        if self._pageNumber > 1:
            self.setFont("Helvetica", 8.5)
            self.setFillColor(colors.HexColor("#555555"))
            self.drawString(72, page_height - 40, "Technical Document Analyzer — Summary Report")
            self.drawRightString(page_width - 72, page_height - 40, "Python Project")

            self.setStrokeColor(colors.HexColor("#D0D0D0"))
            self.setLineWidth(0.5)
            self.line(72, page_height - 45, page_width - 72, page_height - 45)

        # Simple clean footer on all pages (strictly human, no portfolio text)
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawString(72, 38, "Technical Document Analyzer")
        self.drawRightString(page_width - 72, 38, f"Page {self._pageNumber} of {page_count}")

        self.setStrokeColor(colors.HexColor("#D0D0D0"))
        self.setLineWidth(0.5)
        self.line(72, 48, page_width - 72, 48)

        self.restoreState()


def create_pdf_report(output_filename):
    """Generates the human-written Microsoft Word style PDF."""
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=72,   # 1 inch
        rightMargin=72,  # 1 inch
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Clean, human Word-like typography
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=2,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=6,
    )

    info_line = ParagraphStyle(
        "DocInfo",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#6B7280"),
        spaceAfter=8,
    )

    h1_style = ParagraphStyle(
        "SecH1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#111827"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "SecH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1F2937"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#222222"),
        spaceAfter=6,
    )

    bullet_style = ParagraphStyle(
        "BulletText",
        parent=body_style,
        leftIndent=12,
        spaceAfter=4,
    )

    table_cell = ParagraphStyle(
        "Cell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#222222"),
    )

    table_cell_bold = ParagraphStyle(
        "CellBold",
        parent=table_cell,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#111827"),
    )

    table_header = ParagraphStyle(
        "HeaderCell",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#111827"),
    )

    caption_style = ParagraphStyle(
        "Caption",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#555555"),
        alignment=1,  # Centered
        spaceBefore=4,
        spaceAfter=6,
    )

    story = []

    # Document Header (Title, Subtitle, Date)
    story.append(Paragraph("Technical Document Analyzer", title_style))
    story.append(Paragraph("Summary Report and Practical Guide", subtitle_style))
    story.append(Paragraph("Built with Python 3 &nbsp;|&nbsp; Standard Libraries Only &nbsp;|&nbsp; Offline Desktop &amp; CLI Utility", info_line))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CCCCCC"), spaceAfter=8))

    # Note: The artificial metadata box (Image 2) has been intentionally removed as requested.

    # 1. Overview
    story.append(Paragraph("1. What This Tool Does", h1_style))
    story.append(Paragraph(
        "The Technical Document Analyzer is a simple, lightweight program written in Python to help people "
        "inspect plain-text technical documents (<code>.txt</code> files). When writing or reviewing documentation, "
        "it is often useful to check key numbers—like how many words and paragraphs are in a draft, how many sections "
        "were created, and which technical words appear most often.",
        body_style
    ))
    story.append(Paragraph(
        "This tool was built using only Python's standard library. It does not require any third-party packages, "
        "has no connection to external web servers, and uses no AI services. Everything runs directly on your computer "
        "in a fraction of a second.",
        body_style
    ))

    # 2. File Organization
    story.append(Paragraph("2. Project Files and What They Do", h1_style))
    story.append(Paragraph(
        "The project is split into four simple files so that the code is clean and easy to read:",
        body_style
    ))

    files_data = [
        [Paragraph("File Name", table_header), Paragraph("Type", table_header), Paragraph("Description", table_header)],
        [Paragraph("main.py", table_cell_bold), Paragraph("Desktop Application", table_cell), Paragraph("A clean graphical window built using Tkinter. It lets you browse for a file, view the text in a preview box, see all calculated numbers, and save a report.", table_cell)],
        [Paragraph("cli.py", table_cell_bold), Paragraph("Command-Line Tool", table_cell), Paragraph("A terminal version for users who prefer working directly in the command prompt or running scripts without opening a window.", table_cell)],
        [Paragraph("analyzer.py", table_cell_bold), Paragraph("Core Analysis Engine", table_cell), Paragraph("Contains the actual calculation functions: reads files safely, cleans punctuation, counts words and paragraphs, and finds frequent words.", table_cell)],
        [Paragraph("test_analyzer.py", table_cell_bold), Paragraph("Automated Tests", table_cell), Paragraph("A test script with 7 automated tests to verify that every function works correctly on normal files, empty files, and error cases.", table_cell)],
    ]
    files_table = Table(files_data, colWidths=[90, 105, 273])
    files_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(files_table)
    story.append(Spacer(1, 8))

    # 3. How the Calculations Work
    story.append(Paragraph("3. How the Calculations Work", h1_style))
    story.append(Paragraph(
        "&bull; <b>Word Count:</b> The program converts text to lowercase so words like <i>Sensor</i> and <i>sensor</i> match. "
        "It replaces punctuation marks (commas, periods, colons, slashes) with spaces so joined words like <code>status:active</code> "
        "separate cleanly, then counts the remaining words.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Character Count:</b> Total characters are counted directly. A second count strips spaces, tabs, and newlines "
        "to show the exact character volume of the words themselves.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Paragraph Count:</b> Instead of simply counting enter keys, the code looks for transitions from blank lines "
        "to text lines. This correctly handles extra blank lines and different operating system line breaks (Windows vs Mac/Linux).",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Headings:</b> Detects lines starting with Markdown hashes (<code># Title</code>, <code>## Section</code>) and "
        "numbered section headers (like <code>1. Introduction</code>, <code>1.1 System</code>, or <code>A. Overview</code>).",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Top Frequent Words:</b> Filters out numbers and common everyday words (like <i>the</i>, <i>and</i>, <i>is</i>, "
        "<i>of</i>, <i>to</i>). It counts occurrences using a standard Python dictionary and lists the top 10 most frequent words.",
        bullet_style
    ))

    # PAGE 2: Flowchart diagram and step explanation
    story.append(PageBreak())

    story.append(Paragraph("4. How the Program Works (Process Flow)", h1_style))
    story.append(Paragraph(
        "The diagram below outlines the full workflow from when a user selects a file to when the analysis report is saved:",
        body_style
    ))

    # Full-width crystal-clear block diagram (spans the entire printable page width)
    flowchart_img_path = "flowchart_clean.png"
    if not os.path.exists(flowchart_img_path):
        flowchart_img_path = "flowchart_hd.png"

    if os.path.exists(flowchart_img_path):
        flow_img = Image(flowchart_img_path, width=468, height=362)
        story.append(flow_img)
        story.append(Paragraph("Figure 1: System architecture and execution flow of the Technical Document Analyzer.", caption_style))
    else:
        story.append(Paragraph("[Flowchart image not found]", body_style))

    story.append(Spacer(1, 6))

    # Clear bullet points explaining each stage shown in the diagram
    story.append(Paragraph("<b>Workflow Summary by Stage:</b>", h2_style))
    story.append(Paragraph(
        "&bull; <b>Stage 1 (Input &amp; Validation):</b> The program opens a <code>.txt</code> file and reads it safely using UTF-8 encoding. If the file is missing or inaccessible, an error message is shown. If the file is empty, a notice is displayed and counts show zero.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Stage 2 (Text Cleaning &amp; Analysis):</b> Text is lowercased and stripped of punctuation marks so that capitalization differences do not affect counts. Four independent checks run in parallel: character counting (with and without spaces), paragraph detection (tracking blank lines), heading detection (Markdown <code>#</code> and numbered sections), and word extraction.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Stage 3 (Word Frequency &amp; Aggregation):</b> Common English stop words (like <i>the</i>, <i>and</i>, <i>is</i>) and pure numbers are filtered out. Remaining words are counted in a dictionary and sorted by frequency descending. All metrics are combined into a final results model.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Stage 4 (Presentation &amp; Export):</b> Results are shown in either the Desktop GUI (with document preview pane) or the Terminal CLI. The user can export a clean, formatted <code>.txt</code> analysis report with confirmation before overwriting.",
        bullet_style
    ))

    # PAGE 3: Testing, Sample Files, and Practical Limitations
    story.append(PageBreak())

    story.append(Paragraph("5. Testing and Verification", h1_style))
    story.append(Paragraph(
        "The project includes an automated test script (<code>test_analyzer.py</code>) that verifies all core functions "
        "using Python's built-in <code>unittest</code> framework. All 7 test cases passed in 0.05 seconds:",
        body_style
    ))

    test_data = [
        [Paragraph("Test Case", table_header), Paragraph("Scenario Tested", table_header), Paragraph("What It Checks", table_header), Paragraph("Result", table_header)],
        [Paragraph("Test 1", table_cell_bold), Paragraph("Normal technical document", table_cell), Paragraph("Calculates words, characters, paragraphs, headings, and frequent words accurately.", table_cell), Paragraph("Passed", table_cell_bold)],
        [Paragraph("Test 2", table_cell_bold), Paragraph("Empty file (0 bytes)", table_cell), Paragraph("Handles zero-length files gracefully without division errors or crashes.", table_cell), Paragraph("Passed", table_cell_bold)],
        [Paragraph("Test 3", table_cell_bold), Paragraph("Document with only headings", table_cell), Paragraph("Checks both Markdown '#' headings and numbered '1.', '1.1', 'A.' headings.", table_cell), Paragraph("Passed", table_cell_bold)],
        [Paragraph("Test 4", table_cell_bold), Paragraph("Mixed case and punctuation", table_cell), Paragraph("Confirms 'Sensor', 'sensor', and 'SENSOR' count together, stripping symbols.", table_cell), Paragraph("Passed", table_cell_bold)],
        [Paragraph("Test 5", table_cell_bold), Paragraph("Missing or invalid file path", table_cell), Paragraph("Catches FileNotFoundError safely and alerts the user.", table_cell), Paragraph("Passed", table_cell_bold)],
        [Paragraph("Test 6", table_cell_bold), Paragraph("Saving a report to disk", table_cell), Paragraph("Writes formatted text report to destination and verifies file contents match.", table_cell), Paragraph("Passed", table_cell_bold)],
        [Paragraph("Test 7", table_cell_bold), Paragraph("Handling a save error", table_cell), Paragraph("Traps invalid write paths (OSError) without crashing the application.", table_cell), Paragraph("Passed", table_cell_bold)],
    ]
    test_table = Table(test_data, colWidths=[50, 135, 230, 53])
    test_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(test_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("Results on Sample Technical Documents:", h2_style))
    sample_data = [
        [Paragraph("Document", table_header), Paragraph("Words", table_header), Paragraph("Chars (No Spc)", table_header), Paragraph("Paragraphs", table_header), Paragraph("Headings", table_header), Paragraph("Top Frequent Words", table_header)],
        [Paragraph("arduino_sensor_system.txt", table_cell_bold), Paragraph("399", table_cell), Paragraph("2,469", table_cell), Paragraph("8", table_cell), Paragraph("18", table_cell), Paragraph("sensor (13), pin (8), microcontroller (5), power (5)", table_cell)],
        [Paragraph("software_install_guide.txt", table_cell_bold), Paragraph("476", table_cell), Paragraph("2,846", table_cell), Paragraph("10", table_cell), Paragraph("20", table_cell), Paragraph("software (6), installation (5), port (5), system (5)", table_cell)],
        [Paragraph("sample.txt (Packet Analyzer)", table_cell_bold), Paragraph("393", table_cell), Paragraph("2,479", table_cell), Paragraph("7", table_cell), Paragraph("13", table_cell), Paragraph("network (13), packet (10), capture (8), protocol (8)", table_cell)],
    ]
    sample_table = Table(sample_data, colWidths=[125, 40, 68, 55, 45, 135])
    sample_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(sample_table)
    story.append(Spacer(1, 4))

    # 6. Practical Limitations
    story.append(Paragraph("6. Practical Notes and Limitations", h1_style))
    story.append(Paragraph(
        "To keep the program simple, transparent, and beginner-friendly, here are its intentional boundaries:",
        body_style
    ))
    story.append(Paragraph(
        "&bull; <b>Plain Text Only:</b> The program accepts <code>.txt</code> files. It does not parse binary formats like Word (<code>.docx</code>) or PDF.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Numbered Steps Counted as Headings:</b> Plain text has no special heading tags, so any numbered procedural step (such as <code>1. Connect the cable</code>) looks identical to a section heading and is counted.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>English Stop Words:</b> The stop-word list is designed for standard English text. Documents in other languages will require updating the word set.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Word Variations:</b> The frequency counter matches exact spelling after lowercasing. Singular and plural forms (like <i>sensor</i> and <i>sensors</i>) are counted as separate words.",
        bullet_style
    ))

    # Simple footer sign-off block
    sign_data = [
        [Paragraph("Project:", table_cell_bold), Paragraph("Technical Document Analyzer (Python 3)", table_cell)],
        [Paragraph("Interfaces:", table_cell_bold), Paragraph("Desktop Graphical User Interface (main.py) and Terminal CLI (cli.py)", table_cell)],
        [Paragraph("Test Status:", table_cell_bold), Paragraph("All 7 automated unit tests passed &bull; Verified on realistic sample files", table_cell)],
    ]
    sign_table = Table(sign_data, colWidths=[90, 378])
    sign_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(Spacer(1, 4))
    story.append(sign_table)

    doc.build(story, canvasmaker=SimpleWordCanvas)


def create_xml_report(output_filename):
    """Generates a clean, simple XML report without AI buzzwords."""
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!--
  Technical Document Analyzer - Summary Report
  Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
-->
<technicalDocumentReport>
  <header>
    <title>Technical Document Analyzer</title>
    <description>Summary Report and Practical Guide</description>
    <date>{datetime.now().strftime("%Y-%m-%d")}</date>
    <technology>Python 3 (Standard Library Only)</technology>
  </header>

  <summary>
    A simple, offline Python program that analyzes plain-text (.txt) documents. It calculates word count, character count (with and without spaces), non-empty paragraphs, section headings, and the top 10 frequent technical words while ignoring common English stop words.
  </summary>

  <files>
    <file name="main.py" type="Desktop GUI">Tkinter desktop application with document preview, calculated metric cards, and report export.</file>
    <file name="cli.py" type="Command-Line Interface">Terminal version for running the analysis without opening a graphical window.</file>
    <file name="analyzer.py" type="Analysis Engine">Core functions for reading files safely, cleaning punctuation, counting metrics, and finding frequent words.</file>
    <file name="test_analyzer.py" type="Automated Tests">Python unittest suite with 7 test cases validating normal files, empty files, and error handling.</file>
  </files>

  <processFlow>
    <step number="1" name="File Input">User enters or selects a .txt file. Program verifies existence and reads UTF-8 content.</step>
    <step number="2" name="Text Cleaning">Converts text to lowercase and strips punctuation so words separate cleanly.</step>
    <step number="3" name="Metric Calculation">Calculates total words, characters, non-empty paragraphs, and headings.</step>
    <step number="4" name="Frequent Word Tally">Ignores common English stop words and counts remaining words in a Python dictionary.</step>
    <step number="5" name="Report Export">Displays results on screen and offers to save a clean .txt report file.</step>
  </processFlow>

  <testResults totalTests="7" passed="7" failed="0">
    <test id="1" name="Normal technical document" status="Passed" />
    <test id="2" name="Empty file (0 bytes)" status="Passed" />
    <test id="3" name="Document containing only headings" status="Passed" />
    <test id="4" name="Punctuation and mixed capitalization" status="Passed" />
    <test id="5" name="Missing or inaccessible file" status="Passed" />
    <test id="6" name="Saving report to valid destination" status="Passed" />
    <test id="7" name="Handling save error" status="Passed" />
  </testResults>

  <sampleDocumentResults>
    <sample name="arduino_sensor_system.txt">
      <words>399</words>
      <charactersNoSpaces>2469</charactersNoSpaces>
      <paragraphs>8</paragraphs>
      <headings>18</headings>
      <topFrequentWords>sensor (13), pin (8), microcontroller (5), power (5)</topFrequentWords>
    </sample>
    <sample name="software_install_guide.txt">
      <words>476</words>
      <charactersNoSpaces>2846</charactersNoSpaces>
      <paragraphs>10</paragraphs>
      <headings>20</headings>
      <topFrequentWords>software (6), installation (5), port (5), system (5)</topFrequentWords>
    </sample>
    <sample name="sample.txt">
      <words>393</words>
      <charactersNoSpaces>2479</charactersNoSpaces>
      <paragraphs>7</paragraphs>
      <headings>13</headings>
      <topFrequentWords>network (13), packet (10), capture (8), protocol (8)</topFrequentWords>
    </sample>
  </sampleDocumentResults>

  <limitations>
    <limitation>Plain-text (.txt) files only. Binary formats like Word (.docx) or PDF are not supported.</limitation>
    <limitation>Numbered procedural list items (like '1. Do this') are formatted like numbered headings and will be counted.</limitation>
    <limitation>Stop words are based on standard English.</limitation>
    <limitation>Plurals and singulars (like 'sensor' and 'sensors') are counted as separate words.</limitation>
  </limitations>
</technicalDocumentReport>
"""
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(xml_content.strip() + "\n")


if __name__ == "__main__":
    pdf_path = "technical_summary_report.pdf"
    xml_path = "technical_summary_report.xml"

    print("Generating human-style Microsoft Word PDF report...")
    create_pdf_report(pdf_path)
    print(f"PDF generated: {pdf_path}")

    print("Generating clean XML report...")
    create_xml_report(xml_path)
    print(f"XML generated: {xml_path}")
