"""
main.py - Graphical User Interface for Technical Document Analyzer.

A minimal, clean desktop utility built using Python's standard Tkinter library.
Allows engineering students and technical writers to open plain-text documents,
inspect basic structural metrics, view frequent technical terms, and export reports.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from analyzer import (
    analyze_document,
    generate_report_text,
    read_document,
    save_report,
)


class TechnicalDocumentAnalyzerApp:
    """Main application class for the Technical Document Analyzer GUI."""

    def __init__(self, root):
        self.root = root
        self.root.title("Technical Document Analyzer")
        self.root.geometry("960x650")
        self.root.minsize(800, 520)

        # Application state variables
        self.current_filepath = None
        self.current_analysis = None

        # Configure neutral, restrained color theme
        self.bg_color = "#F8F9FA"
        self.card_bg = "#FFFFFF"
        self.text_color = "#212529"
        self.border_color = "#CED4DA"
        self.root.configure(bg=self.bg_color)

        # Configure ttk styles
        self._setup_styles()

        # Build UI layout
        self._build_widgets()

        # Set initial UI state
        self._reset_to_empty_state()

    def _setup_styles(self):
        """Configures clean, consistent ttk styles."""
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")

        # Configure default font and colors
        self.style.configure(".", font=("Segoe UI", 10), background=self.bg_color)
        self.style.configure(
            "TLabelframe",
            background=self.card_bg,
            foreground=self.text_color,
            relief="solid",
            borderwidth=1,
        )
        self.style.configure(
            "TLabelframe.Label",
            background=self.card_bg,
            foreground=self.text_color,
            font=("Segoe UI", 10, "bold"),
        )
        self.style.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=(10, 4),
            relief="raised",
        )
        self.style.configure(
            "Treeview",
            background=self.card_bg,
            foreground=self.text_color,
            rowheight=22,
            font=("Segoe UI", 9),
            fieldbackground=self.card_bg,
            borderwidth=1,
        )
        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 9, "bold"),
            background="#E9ECEF",
            foreground=self.text_color,
            relief="flat",
        )

    def _build_widgets(self):
        """Constructs the application layout."""
        # Main grid container (expands with window)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # 1. Top File Selection Bar
        self._build_top_bar()

        # 2. Central Split Pane (Left: Metrics & Frequent Words; Right: Document Preview)
        self._build_content_area()

        # 3. Bottom Status and Action Bar
        self._build_bottom_bar()

    def _build_top_bar(self):
        """Builds the file selection bar at the top."""
        top_frame = tk.Frame(self.root, bg=self.card_bg, bd=1, relief="solid", padx=10, pady=8)
        top_frame.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        top_frame.columnconfigure(1, weight=1)

        label = tk.Label(top_frame, text="Selected File:", bg=self.card_bg, fg=self.text_color, font=("Segoe UI", 10, "bold"))
        label.grid(row=0, column=0, padx=(0, 8), sticky="w")

        self.path_entry = tk.Entry(top_frame, font=("Segoe UI", 9), relief="solid", bd=1)
        self.path_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        self.path_entry.insert(0, "No file selected")
        self.path_entry.configure(state="readonly")

        open_btn = ttk.Button(top_frame, text="Browse Document...", command=self.open_file)
        open_btn.grid(row=0, column=2, padx=(0, 6))

        reset_btn = ttk.Button(top_frame, text="Reset", command=self._reset_to_empty_state)
        reset_btn.grid(row=0, column=3)

    def _build_content_area(self):
        """Builds the main two-column content layout."""
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=12, pady=6)
        content_frame.columnconfigure(0, weight=0, minsize=350)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)

        # Left Column: Metrics and Frequent Words
        left_frame = tk.Frame(content_frame, bg=self.bg_color)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)

        # --- Metrics Frame ---
        metrics_group = ttk.LabelFrame(left_frame, text=" Document Metrics ", padding=10)
        metrics_group.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        metrics_group.columnconfigure(1, weight=1)

        self.metric_labels = {}
        metric_items = [
            ("total_words", "Total Words:"),
            ("total_characters", "Total Characters (all):"),
            ("characters_no_spaces", "Characters (no whitespace):"),
            ("paragraph_count", "Non-Empty Paragraphs:"),
            ("heading_count", "Headings Detected:"),
        ]

        for row_idx, (key, display_name) in enumerate(metric_items):
            title_lbl = tk.Label(metrics_group, text=display_name, bg=self.card_bg, fg="#495057", anchor="w")
            title_lbl.grid(row=row_idx, column=0, sticky="w", pady=2)

            val_lbl = tk.Label(metrics_group, text="-", bg=self.card_bg, fg=self.text_color, font=("Segoe UI", 10, "bold"), anchor="e")
            val_lbl.grid(row=row_idx, column=1, sticky="e", pady=2)
            self.metric_labels[key] = val_lbl

        # --- Frequent Words Frame ---
        freq_group = ttk.LabelFrame(left_frame, text=" Top 10 Frequent Words ", padding=10)
        freq_group.grid(row=1, column=0, sticky="nsew")
        freq_group.rowconfigure(0, weight=1)
        freq_group.columnconfigure(0, weight=1)

        # Treeview table for rank, word, occurrences
        columns = ("rank", "word", "count")
        self.freq_tree = ttk.Treeview(freq_group, columns=columns, show="headings", height=10, selectmode="none")
        self.freq_tree.heading("rank", text="#", anchor="center")
        self.freq_tree.heading("word", text="Word", anchor="w")
        self.freq_tree.heading("count", text="Count", anchor="e")

        self.freq_tree.column("rank", width=40, anchor="center")
        self.freq_tree.column("word", width=190, anchor="w")
        self.freq_tree.column("count", width=70, anchor="e")
        self.freq_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar for frequent words list
        freq_scroll = ttk.Scrollbar(freq_group, orient="vertical", command=self.freq_tree.yview)
        self.freq_tree.configure(yscrollcommand=freq_scroll.set)
        freq_scroll.grid(row=0, column=1, sticky="ns")

        note_label = tk.Label(
            freq_group,
            text="* Common stop words and numbers are excluded.",
            bg=self.card_bg,
            fg="#6C757D",
            font=("Segoe UI", 8),
            anchor="w",
        )
        note_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 0))

        # Right Column: Document Preview Frame
        preview_group = ttk.LabelFrame(content_frame, text=" Document Preview ", padding=10)
        preview_group.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        preview_group.rowconfigure(0, weight=1)
        preview_group.columnconfigure(0, weight=1)

        # Scrolled Text Box for viewing document content
        self.preview_text = tk.Text(
            preview_group,
            wrap="word",
            font=("Consolas", 10),
            bg=self.card_bg,
            fg=self.text_color,
            bd=1,
            relief="solid",
        )
        self.preview_text.grid(row=0, column=0, sticky="nsew")

        preview_scroll = ttk.Scrollbar(preview_group, orient="vertical", command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scroll.set)
        preview_scroll.grid(row=0, column=1, sticky="ns")

    def _build_bottom_bar(self):
        """Builds the bottom action and status bar."""
        bottom_frame = tk.Frame(self.root, bg=self.card_bg, bd=1, relief="solid", padx=10, pady=8)
        bottom_frame.grid(row=2, column=0, sticky="ew", padx=12, pady=(6, 12))
        bottom_frame.columnconfigure(0, weight=1)

        # Status text label
        self.status_label = tk.Label(
            bottom_frame,
            text="Ready. Please open a .txt document to analyze.",
            bg=self.card_bg,
            fg="#495057",
            font=("Segoe UI", 9),
            anchor="w",
        )
        self.status_label.grid(row=0, column=0, sticky="w")

        # Save Report Button (Disabled until an analysis is performed)
        self.save_btn = ttk.Button(
            bottom_frame,
            text="Save Analysis Report (.txt)",
            command=self.save_report,
            state="disabled",
        )
        self.save_btn.grid(row=0, column=1, sticky="e")

    def open_file(self):
        """Prompts user to select a .txt file, loads and analyzes it."""
        filepath = filedialog.askopenfilename(
            title="Select Technical Document",
            filetypes=[("Text Files (*.txt)", "*.txt"), ("All Files (*.*)", "*.*")],
        )

        # User cancelled file picker dialog
        if not filepath:
            return

        try:
            content = read_document(filepath)
        except FileNotFoundError:
            messagebox.showerror("File Error", f"The selected file was not found:\n{filepath}")
            return
        except UnicodeDecodeError:
            messagebox.showerror(
                "Encoding Error",
                "Unable to read the file using UTF-8 encoding.\n"
                "Please verify that the file is a valid plain-text document.",
            )
            return
        except PermissionError:
            messagebox.showerror("Permission Error", f"Permission denied when opening:\n{filepath}")
            return
        except Exception as err:
            messagebox.showerror("Error", f"Failed to open document:\n{err}")
            return

        # Perform analysis on content
        self.current_filepath = filepath
        self.current_analysis = analyze_document(content, filepath=filepath)

        # Update UI with results
        self._display_analysis(content)

    def _display_analysis(self, raw_content):
        """Populates UI widgets with analysis results."""
        if not self.current_analysis:
            return

        # Update file path entry
        self.path_entry.configure(state="normal")
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, self.current_filepath)
        self.path_entry.configure(state="readonly")

        # Update metrics labels
        data = self.current_analysis
        self.metric_labels["total_words"].config(text=f"{data['total_words']:,}")
        self.metric_labels["total_characters"].config(text=f"{data['total_characters']:,}")
        self.metric_labels["characters_no_spaces"].config(text=f"{data['characters_no_spaces']:,}")
        self.metric_labels["paragraph_count"].config(text=f"{data['paragraph_count']:,}")
        self.metric_labels["heading_count"].config(text=f"{data['heading_count']:,}")

        # Update frequent words table
        for item in self.freq_tree.get_children():
            self.freq_tree.delete(item)

        frequent_words = data.get("frequent_words", [])
        if frequent_words:
            for rank, (word, count) in enumerate(frequent_words, start=1):
                self.freq_tree.insert("", "end", values=(rank, word, count))
        else:
            self.freq_tree.insert("", "end", values=("-", "(No significant words)", 0))

        # Update document preview text
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", raw_content)
        self.preview_text.configure(state="disabled")

        # Enable save button
        self.save_btn.configure(state="normal")

        # Update status message
        if data["total_words"] == 0:
            self.status_label.config(
                text="Notice: Document is empty or contains no words.",
                fg="#C53030",
            )
        else:
            self.status_label.config(
                text=f"Loaded '{data['filename']}' ({data['total_words']:,} words, {data['paragraph_count']} paragraphs).",
                fg="#2F855A",
            )

    def save_report(self):
        """Exports the analysis results to a user-selected text file."""
        if not self.current_analysis:
            messagebox.showwarning("No Analysis", "Please open and analyze a document before saving a report.")
            return

        default_name = f"{os.path.splitext(self.current_analysis['filename'])[0]}_report.txt"
        initial_dir = os.path.join(os.getcwd(), "output")
        if not os.path.exists(initial_dir):
            os.makedirs(initial_dir, exist_ok=True)

        save_path = filedialog.asksaveasfilename(
            title="Save Analysis Report",
            initialdir=initial_dir,
            initialfile=default_name,
            defaultextension=".txt",
            filetypes=[("Text Files (*.txt)", "*.txt"), ("All Files (*.*)", "*.*")],
            confirmoverwrite=True,
        )

        # User cancelled save dialog
        if not save_path:
            return

        report_content = generate_report_text(self.current_analysis)

        try:
            save_report(report_content, save_path)
            self.status_label.config(
                text=f"Report saved: {os.path.basename(save_path)}",
                fg="#2F855A",
            )
            messagebox.showinfo("Report Saved", f"Analysis report successfully saved to:\n{save_path}")
        except Exception as err:
            self.status_label.config(text="Save failed.", fg="#C53030")
            messagebox.showerror("Save Error", f"Failed to save report:\n{err}")

    def _reset_to_empty_state(self):
        """Clears all loaded data and resets UI to initial empty state."""
        self.current_filepath = None
        self.current_analysis = None

        self.path_entry.configure(state="normal")
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, "No file selected")
        self.path_entry.configure(state="readonly")

        for lbl in self.metric_labels.values():
            lbl.config(text="-")

        for item in self.freq_tree.get_children():
            self.freq_tree.delete(item)

        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.configure(state="disabled")

        self.save_btn.configure(state="disabled")
        self.status_label.config(
            text="Ready. Please open a .txt document to analyze.",
            fg="#495057",
        )


def main():
    """Application entry point."""
    root = tk.Tk()
    app = TechnicalDocumentAnalyzerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
