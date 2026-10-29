"""
create_simple_bw_diagram.py - Generates a simple, clean, black-and-white engineering flowchart.
No AI colors, pure white background, crisp black borders, black text, clean arrows, standard shapes.
With generous boundary padding so NO element is ever cut off.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_simple_bw_flowchart(output_png="flowchart_clean.png", output_svg="flowchart_diagram.svg"):
    # 15:11 aspect ratio with full margins
    fig, ax = plt.subplots(figsize=(15, 11.5), dpi=300)
    ax.set_xlim(-2, 152)
    ax.set_ylim(-6, 122)
    ax.axis("off")

    # Strict black and white styling
    BORDER_COLOR = "#000000"
    FILL_COLOR = "#FFFFFF"
    TEXT_COLOR = "#000000"
    SUBTEXT_COLOR = "#333333"
    ARROW_COLOR = "#000000"
    LINE_WIDTH = 1.3

    def draw_box(x, y, w, h, title, subtitle=None, shape="rect", title_fs=10, sub_fs=7.8, radius=1.2):
        """Draws a plain black-and-white flowchart node."""
        if shape == "pill":
            box = patches.FancyBboxPatch(
                (x - w / 2, y - h / 2), w, h,
                boxstyle=f"round,pad=0.2,rounding_size={h/2}",
                ec=BORDER_COLOR, fc=FILL_COLOR, lw=LINE_WIDTH, zorder=3
            )
        elif shape == "diamond":
            pts = [[x, y + h / 2], [x + w / 2, y], [x, y - h / 2], [x - w / 2, y]]
            box = patches.Polygon(pts, closed=True, ec=BORDER_COLOR, fc=FILL_COLOR, lw=LINE_WIDTH, zorder=3)
        else: # rectangle
            box = patches.FancyBboxPatch(
                (x - w / 2, y - h / 2), w, h,
                boxstyle=f"round,pad=0.2,rounding_size={radius}",
                ec=BORDER_COLOR, fc=FILL_COLOR, lw=LINE_WIDTH, zorder=3
            )
        ax.add_patch(box)

        if subtitle:
            ax.text(x, y + h * 0.17, title, ha="center", va="center", fontsize=title_fs,
                    fontweight="bold", color=TEXT_COLOR, family="sans-serif", zorder=4)
            ax.text(x, y - h * 0.20, subtitle, ha="center", va="center", fontsize=sub_fs,
                    fontweight="normal", color=SUBTEXT_COLOR, family="sans-serif", zorder=4)
        else:
            ax.text(x, y, title, ha="center", va="center", fontsize=title_fs,
                    fontweight="bold", color=TEXT_COLOR, family="sans-serif", zorder=4)

    def draw_list_box(x, y, w, h, title, items, title_fs=10, item_fs=8.0, radius=1.2):
        """Draws a standard white card with title and bullet points in plain black/white."""
        box = patches.FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle=f"round,pad=0.2,rounding_size={radius}",
            ec=BORDER_COLOR, fc=FILL_COLOR, lw=LINE_WIDTH, zorder=3
        )
        ax.add_patch(box)

        # Title divider line
        title_y = y + h / 2 - 3.8
        ax.plot([x - w / 2 + 0.8, x + w / 2 - 0.8], [title_y - 2.0, title_y - 2.0],
                color=BORDER_COLOR, lw=0.9, zorder=4)

        ax.text(x, title_y, title, ha="center", va="center", fontsize=title_fs,
                fontweight="bold", color=TEXT_COLOR, family="sans-serif", zorder=5)

        start_y = title_y - 4.5
        spacing = (h - 9.0) / max(len(items), 1)
        for i, item in enumerate(items):
            iy = start_y - i * spacing
            ax.text(x - w / 2 + 2.5, iy, item, ha="left", va="center", fontsize=item_fs,
                    fontweight="normal", color=TEXT_COLOR, family="sans-serif", zorder=5)

    def draw_arrow(p1, p2, label=None, label_pos=None):
        """Draws a crisp black directional arrow."""
        ax.annotate(
            "", xy=p2, xytext=p1,
            arrowprops=dict(
                arrowstyle="-|>",
                color=ARROW_COLOR,
                lw=LINE_WIDTH,
                mutation_scale=13,
                shrinkA=0, shrinkB=0
            ),
            zorder=2
        )
        if label:
            lx, ly = label_pos if label_pos else ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 1.2)
            ax.text(lx, ly, label, ha="center", va="center", fontsize=8.2,
                    fontweight="bold", color=TEXT_COLOR, family="sans-serif",
                    bbox=dict(boxstyle="square,pad=0.18", fc=FILL_COLOR, ec=BORDER_COLOR, lw=0.6),
                    zorder=6)

    def draw_elbow(pts, label=None, label_pos=None):
        """Draws orthogonal black arrow lines."""
        for i in range(len(pts) - 1):
            if i == len(pts) - 2:
                ax.annotate(
                    "", xy=pts[i + 1], xytext=pts[i],
                    arrowprops=dict(
                        arrowstyle="-|>",
                        color=ARROW_COLOR,
                        lw=LINE_WIDTH,
                        mutation_scale=13,
                        shrinkA=0, shrinkB=0
                    ),
                    zorder=2
                )
            else:
                ax.plot([pts[i][0], pts[i + 1][0]], [pts[i][1], pts[i + 1][1]],
                        color=ARROW_COLOR, lw=LINE_WIDTH, zorder=2)
        if label:
            lx, ly = label_pos if label_pos else (pts[0][0], pts[0][1] + 1.2)
            ax.text(lx, ly, label, ha="center", va="center", fontsize=8.2,
                    fontweight="bold", color=TEXT_COLOR, family="sans-serif",
                    bbox=dict(boxstyle="square,pad=0.18", fc=FILL_COLOR, ec=BORDER_COLOR, lw=0.6),
                    zorder=6)

    # =========================================================================
    # 1. TOP STAGE: Input & Validation
    # =========================================================================
    # Start: Input .txt Document (pill)
    draw_box(75, 115.0, 34, 5.4, "Start: Input .txt Document", shape="pill", title_fs=9.8)
    draw_arrow((75, 112.3), (75, 108.5))

    # File Loader & UTF-8 Validator
    draw_box(75, 105.5, 36, 5.8, "File Loader & UTF-8 Validator", "Safe Ingestion & Path Checks", title_fs=10, sub_fs=7.8)
    draw_arrow((75, 102.6), (75, 99.2))

    # Decision: File Valid?
    draw_box(75, 94.0, 24, 10.0, "File Valid?", shape="diamond", title_fs=10)

    # Branch 1 (Left): Missing / Inaccessible
    draw_elbow([(63, 94.0), (24, 94.0), (24, 87.5)],
               label="Missing / Inaccessible", label_pos=(44, 95.8))
    draw_box(24, 84.5, 30, 5.8, "Display Error Message", "File missing or inaccessible notice", title_fs=9.5, sub_fs=7.5)

    # Branch 2 (Middle-Left): Empty File
    draw_elbow([(69, 89.5), (58, 89.5), (58, 87.5)],
               label="Empty File", label_pos=(63.5, 91.0))
    draw_box(58, 84.5, 27, 5.8, "Display Notice: 0 Metrics", "0 Words / 0 Characters / No crash", title_fs=9.2, sub_fs=7.5)

    # Branch 3 (Right): Valid Content -> Text Normalization Engine
    draw_elbow([(87, 94.0), (112, 94.0), (112, 87.5)],
               label="Valid Content", label_pos=(100, 95.8))
    draw_box(112, 84.5, 36, 5.8, "Text Normalization Engine", "Convert to Lowercase & Clean Separators", title_fs=9.8, sub_fs=7.8)

    # =========================================================================
    # 2. MIDDLE STAGE: Parallel Text Processing (4 Columns)
    # =========================================================================
    # From Normalization Engine (112, 81.6) to distribution bus at Y = 77.5
    draw_elbow([(112, 81.6), (112, 77.5)])
    ax.plot([20, 126], [77.5, 77.5], color=ARROW_COLOR, lw=LINE_WIDTH, zorder=2)

    # Col 1: Character Counter (X = 20)
    draw_arrow((20, 77.5), (20, 74.2))
    draw_list_box(20, 61.0, 29, 26.0, "Character Counter",
                  ["• Total characters: len(text)",
                   "• Non-whitespace: strip spaces",
                   "• Whitespace segregation",
                   "• Independent parallel check"],
                  title_fs=10, item_fs=8.0)

    # Col 2: Paragraph Detector (X = 55)
    draw_arrow((55, 77.5), (55, 74.2))
    draw_list_box(55, 61.0, 29, 26.0, "Paragraph Detector",
                  ["• Blank-line transition tracker",
                   "• Handles multi-line gaps",
                   "• Cross-platform CRLF/LF",
                   "• Avoids false counts on blank"],
                  title_fs=10, item_fs=8.0)

    # Col 3: Heading Classifier (X = 90)
    draw_arrow((90, 77.5), (90, 74.2))
    draw_list_box(90, 61.0, 29, 26.0, "Heading Classifier",
                  ["• Markdown '#' syntax detection",
                   "• Numbered hierarchy (1., 1.1)",
                   "• Lettered sections (A., B.)",
                   "• Multi-level regex engine"],
                  title_fs=10, item_fs=8.0)

    # Col 4: Sequential Word Extraction Pipeline (X = 126)
    draw_arrow((126, 77.5), (126, 74.2))
    draw_box(126, 71.8, 30, 4.8, "1. Word Extractor", "Punctuation Stripping & Tokenize", title_fs=9.2, sub_fs=7.2)

    draw_arrow((126, 69.4), (126, 67.2))
    draw_box(126, 64.8, 30, 4.8, "2. Stop-Words & Numbers", "Filters 150+ Words & Pure Digits", title_fs=9.2, sub_fs=7.2)

    draw_arrow((126, 62.4), (126, 60.2))
    draw_box(126, 57.8, 30, 4.8, "3. Frequency Map", "Python Dictionary Counter", title_fs=9.2, sub_fs=7.2)

    draw_arrow((126, 55.4), (126, 53.2))
    draw_box(126, 50.8, 30, 4.8, "4. Sort Top 10 Words", "Descending Frequency Ranking", title_fs=9.2, sub_fs=7.2)

    # =========================================================================
    # 3. AGGREGATION & PRESENTATION STAGE
    # =========================================================================
    # Convergence bus at Y = 45.0 connecting all 4 columns
    Y_MERGE = 45.0
    draw_elbow([(20, 48.0), (20, Y_MERGE), (75, Y_MERGE)])
    draw_elbow([(55, 48.0), (55, Y_MERGE), (75, Y_MERGE)])
    draw_elbow([(90, 48.0), (90, Y_MERGE), (75, Y_MERGE)])
    draw_elbow([(126, 48.4), (126, Y_MERGE), (75, Y_MERGE)])

    draw_arrow((75, Y_MERGE), (75, 41.5))
    draw_box(75, 38.5, 46, 5.8, "Aggregate Metrics Model",
             "Consolidates Words, Chars, Paragraphs, Headings & Top 10",
             title_fs=10, sub_fs=7.8)

    draw_arrow((75, 35.6), (75, 32.0))
    draw_box(75, 27.5, 24, 9.0, "Presentation Mode?", shape="diamond", title_fs=10)

    # Left Branch: Desktop GUI
    draw_elbow([(63, 27.5), (42, 27.5), (42, 22.5)],
               label="Desktop GUI", label_pos=(52, 29.2))
    draw_box(42, 19.5, 34, 5.8, "Desktop GUI (main.py)", "Tkinter Window: Live Preview & Cards", title_fs=9.8, sub_fs=7.8)

    # Right Branch: Terminal CLI
    draw_elbow([(87, 27.5), (108, 27.5), (108, 22.5)],
               label="Terminal CLI", label_pos=(98, 29.2))
    draw_box(108, 19.5, 34, 5.8, "Terminal CLI (cli.py)", "Console Output: Formatted Tables", title_fs=9.8, sub_fs=7.8)

    # Both converge to Save Formatted Report at Y = 13.0
    draw_elbow([(42, 16.6), (42, 13.0), (75, 13.0)])
    draw_elbow([(108, 16.6), (108, 13.0), (75, 13.0)])
    draw_arrow((75, 13.0), (75, 10.6))

    draw_box(75, 7.8, 36, 5.4, "Save Formatted Report (.txt)", "Timestamped Summary File with Confirmation", title_fs=9.5, sub_fs=7.5)

    # Arrow down to End pill
    draw_arrow((75, 5.1), (75, 3.2))
    draw_box(75, 1.0, 26, 4.2, "End: Report Exported", shape="pill", title_fs=9.2)

    plt.tight_layout()
    plt.savefig(output_png, dpi=300, bbox_inches="tight", pad_inches=0.35, facecolor="#FFFFFF")
    plt.savefig(output_svg, format="svg", bbox_inches="tight", pad_inches=0.35, facecolor="#FFFFFF")
    plt.close()
    print(f"Generated clean black-and-white flowchart at: {output_png} and {output_svg}")

if __name__ == "__main__":
    generate_simple_bw_flowchart()
