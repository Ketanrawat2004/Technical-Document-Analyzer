"""
create_flowchart.py - Generates a high-resolution, crystal-clear vector/300-DPI block diagram.
Re-creates the exact flowchart from Image 1 with sharp lines, high-contrast readable typography,
and clean professional box styling.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_sharp_flowchart(output_path="flowchart_hd.png"):
    # Set high DPI figure with clean dimensions (ratio ~ 1:2.3)
    fig, ax = plt.subplots(figsize=(8, 18), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 220)
    ax.axis("off")

    # Font and color constants
    FONT_FAMILY = "sans-serif"
    BOX_BORDER = "#1E293B"       # Slate 800
    BOX_FILL = "#FFFFFF"         # Pure White
    BOX_SHADED = "#F1F5F9"       # Slate 100
    TEXT_COLOR = "#0F172A"       # Slate 900
    ARROW_COLOR = "#334155"      # Slate 700
    LABEL_COLOR = "#475569"      # Slate 600

    def draw_box(x, y, w, h, text, shape="rect", fill=BOX_FILL, font_weight="bold", font_size=9):
        """Draws a crisp diagram node."""
        if shape == "pill":
            box = patches.FancyBboxPatch(
                (x - w / 2, y - h / 2), w, h,
                boxstyle="round,pad=0.2,rounding_size=3.0",
                ec=BOX_BORDER, fc=fill, lw=1.5, zorder=3
            )
        elif shape == "diamond":
            pts = [[x, y + h / 2], [x + w / 2, y], [x, y - h / 2], [x - w / 2, y]]
            box = patches.Polygon(pts, closed=True, ec=BOX_BORDER, fc=fill, lw=1.5, zorder=3)
        else: # rectangle
            box = patches.FancyBboxPatch(
                (x - w / 2, y - h / 2), w, h,
                boxstyle="round,pad=0.1,rounding_size=1.0",
                ec=BOX_BORDER, fc=fill, lw=1.5, zorder=3
            )
        ax.add_patch(box)
        ax.text(x, y, text, ha="center", va="center", fontsize=font_size,
                fontweight=font_weight, color=TEXT_COLOR, family=FONT_FAMILY,
                linespacing=1.25, zorder=4)

    def draw_arrow(p1, p2, text=None, text_offset=(0, 0)):
        """Draws a clean directional arrow between two points."""
        ax.annotate(
            "", xy=p2, xytext=p1,
            arrowprops=dict(
                arrowstyle="-|>",
                color=ARROW_COLOR,
                lw=1.4,
                mutation_scale=14,
                shrinkA=0, shrinkB=0
            ),
            zorder=2
        )
        if text:
            tx = (p1[0] + p2[0]) / 2 + text_offset[0]
            ty = (p1[1] + p2[1]) / 2 + text_offset[1]
            ax.text(tx, ty, text, ha="center", va="center", fontsize=7.5,
                    color=LABEL_COLOR, family=FONT_FAMILY, fontweight="semibold",
                    bbox=dict(boxstyle="square,pad=0.15", fc="#FFFFFF", ec="none", alpha=0.9),
                    zorder=5)

    def draw_elbow_arrow(pts, text=None, text_offset=(0, 0)):
        """Draws an orthogonal multi-segment arrow."""
        for i in range(len(pts) - 1):
            if i == len(pts) - 2:
                # Last segment gets the arrow head
                ax.annotate(
                    "", xy=pts[i + 1], xytext=pts[i],
                    arrowprops=dict(
                        arrowstyle="-|>",
                        color=ARROW_COLOR,
                        lw=1.4,
                        mutation_scale=14,
                        shrinkA=0, shrinkB=0
                    ),
                    zorder=2
                )
            else:
                # Intermediate lines
                ax.plot([pts[i][0], pts[i + 1][0]], [pts[i][1], pts[i + 1][1]],
                        color=ARROW_COLOR, lw=1.4, zorder=2)
        if text:
            tx = pts[0][0] + text_offset[0]
            ty = pts[0][1] + text_offset[1]
            ax.text(tx, ty, text, ha="center", va="center", fontsize=7.5,
                    color=LABEL_COLOR, family=FONT_FAMILY, fontweight="semibold",
                    bbox=dict(boxstyle="square,pad=0.15", fc="#FFFFFF", ec="none", alpha=0.9),
                    zorder=5)

    # ==========================================
    # 1. TOP STAGE: Input & Validation
    # ==========================================
    draw_box(50, 212, 28, 7.5, "Start: Input\n.txt Document", shape="pill", font_size=8.5)
    draw_arrow((50, 208.2), (50, 200.5))

    draw_box(50, 196.5, 30, 8, "File Loader &\nUTF-8 Validator", font_size=8.5)
    draw_arrow((50, 192.5), (50, 185))

    # Decision: File Valid?
    draw_box(50, 178, 26, 14, "File\nValid?", shape="diamond", font_size=8.5)

    # Branch 1: Missing / Inaccessible (Left)
    draw_elbow_arrow([(37, 178), (17, 178), (17, 169)], text="Missing / Inaccessible", text_offset=(-6, 2))
    draw_box(17, 164.5, 24, 9, "Display Error\nMessage", font_size=8)

    # Branch 2: Empty 0-byte File (Middle-Left)
    draw_elbow_arrow([(45, 171), (40, 171), (40, 169)], text="Empty File", text_offset=(0, 2))
    draw_box(40, 164.5, 20, 9, "Display Notice:\n0 Metrics", font_size=8)

    # Branch 3: Valid Content (Right)
    draw_elbow_arrow([(55, 171), (74, 171), (74, 169)], text="Valid Content", text_offset=(6, 2))
    draw_box(74, 164.5, 26, 9, "Text Normalization\nEngine", fill=BOX_SHADED, font_size=8)

    # ==========================================
    # 2. MIDDLE STAGE: Parallel Text Processing
    # ==========================================
    # From Normalization Engine -> 4 tasks
    # X coordinates: Col1=18 (Char), Col2=41 (Para), Col3=62 (Heading), Col4=83 (Words)
    Y_BUS = 153
    ax.plot([18, 83], [Y_BUS, Y_BUS], color=ARROW_COLOR, lw=1.4, zorder=2)
    ax.plot([74, 74], [160, Y_BUS], color=ARROW_COLOR, lw=1.4, zorder=2)

    # Col 1: Character Counter
    draw_arrow((18, Y_BUS), (18, 145))
    draw_box(18, 137.5, 23, 15, "Character Counter\n(Total & Non-\nWhitespace)", font_size=8, font_weight="normal")

    # Col 2: Paragraph State Machine
    draw_arrow((41, Y_BUS), (41, 145))
    draw_box(41, 137.5, 21, 15, "Paragraph State\nMachine\n(Blank Lines)", font_size=8, font_weight="normal")

    # Col 3: Heading Classifier
    draw_arrow((62, Y_BUS), (62, 145))
    draw_box(62, 137.5, 19, 15, "Heading Classifier\n(# & Numbered\nSections)", font_size=8, font_weight="normal")

    # Col 4: Word Extractor pipeline
    draw_arrow((83, Y_BUS), (83, 145))
    draw_box(83, 140, 19, 10, "Word Extractor\n(Lowercase &\nPunctuation)", font_size=7.5, font_weight="normal")

    draw_arrow((83, 135), (83, 126))
    draw_box(83, 121, 19, 10, "Stop-Word &\nNumeric Filter", font_size=7.5, font_weight="normal")

    draw_arrow((83, 116), (83, 107))
    draw_box(83, 102, 19, 10, "Frequency Map\n(Python\nDictionary)", font_size=7.5, font_weight="normal")

    draw_arrow((83, 97), (83, 88))
    draw_box(83, 83, 19, 10, "Sort Top 10\nFrequent Words", font_size=7.5, font_weight="normal")

    # ==========================================
    # 3. AGGREGATION STAGE
    # ==========================================
    # All 4 pipelines converge into Aggregate Metrics Model at y = 67
    Y_COLLECT = 74
    draw_elbow_arrow([(18, 130), (18, Y_COLLECT), (50, Y_COLLECT)])
    draw_elbow_arrow([(41, 130), (41, Y_COLLECT), (50, Y_COLLECT)])
    draw_elbow_arrow([(62, 130), (62, Y_COLLECT), (50, Y_COLLECT)])
    draw_elbow_arrow([(83, 78), (83, Y_COLLECT), (50, Y_COLLECT)])

    draw_arrow((50, Y_COLLECT), (50, 70))
    draw_box(50, 66, 30, 8, "Aggregate Metrics Model", fill=BOX_SHADED, font_size=8.5)

    # ==========================================
    # 4. PRESENTATION & OUTPUT STAGE
    # ==========================================
    draw_arrow((50, 62), (50, 54))
    draw_box(50, 47, 26, 14, "Presentation\nMode?", shape="diamond", font_size=8.5)

    # Branch GUI (Left: x=30)
    draw_elbow_arrow([(37, 47), (28, 47), (28, 38)], text="Desktop GUI", text_offset=(-5, 2))
    draw_box(28, 32.5, 25, 11, "Tkinter Window:\nPreview, Cards\n& Frequency Table", font_size=7.5, font_weight="normal")

    # Branch CLI (Right: x=72)
    draw_elbow_arrow([(63, 47), (72, 47), (72, 38)], text="Terminal CLI", text_offset=(5, 2))
    draw_box(72, 32.5, 25, 11, "Console Output:\nMetrics Table &\nText Summary", font_size=7.5, font_weight="normal")

    # Both converge to Save Report at y=17
    draw_elbow_arrow([(28, 27), (28, 22), (50, 22)])
    draw_elbow_arrow([(72, 27), (72, 22), (50, 22)])
    draw_arrow((50, 22), (50, 18))

    draw_box(50, 14, 28, 8, "Save Formatted\nReport (.txt)", font_size=8)
    draw_arrow((50, 10), (50, 5.5))

    draw_box(50, 3, 26, 5, "End: Report Exported", shape="pill", font_size=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close()
    print(f"Crystal-clear flowchart generated at: {output_path}")

if __name__ == "__main__":
    generate_sharp_flowchart()
