import tkinter as tk
from tkinter import ttk
import unicodedata


# ---------- Colors ----------
BG = "#F3F5FB"
TEXT = "#18233B"
MUTED = "#778198"
PRIMARY = "#635BFF"

STAT_STYLES = [
    ("total_word", "✎  Total word", "#DC2626", "#FFF1F2"),
    ("characters", "▤  Characters", "#0284C7", "#EAF6FF"),
    ("uppercase", "↑  Uppercase", "#059669", "#E7F8F0"),
    ("lowercase", "↓  Lowercase", "#DB2777", "#FDECF5"),
    ("digits", " # No  Digits","#E11D48", "#FFECEF"),
    ("symbols", "✦  Symbols", "#4F46E5", "#ECEEFF"),
    ("spaces", "↔  Spaces / gaps","#475569", "#EDF2F7"),
    ("lines", "☰  Lines", "#EA580C", "#FFF1E7"),
]


FUN_MESSAGES = {
    "total_word": "Every character has an ID. No hiding!",
    "characters": "Word squad reporting. Coffee requested!",
    "uppercase": "LOUD agents! Stealth training failed!",
    "lowercase": "Undercover agents. Please whisper!",
    "digits": "Code breakers—or just counting snacks!",
    "symbols": "Special agents with suspicious disguises!",
    "spaces": "Social distancing for secret agents!",
    "lines": "New checkpoint. Same sleepy guard!",
}

MESSAGE_COLORS = {
    "total_word": "#2563EB",
    "characters": "#C026D3",
    "uppercase": "#0284C7",
    "lowercase": "#9333EA",
    "digits": "#1D4ED8",
    "symbols": "#047857",
    "spaces": "#C2410C",
    "lines": "#BE185D",
}

stat_labels = {}
fun_labels = {}


# ---------- Functions ----------
def analyze_text():
    text = text_input.get("1.0", "end-1c")

    # Your requested naming:
    # Hello World -> Total word: 10, Characters: 2
    counts = {
        "total_word": sum(
            not char.isspace() for char in text
        ),
        "characters": len(text.split()),
        "uppercase": sum(char.isupper() for char in text),
        "lowercase": sum(char.islower() for char in text),
        "digits": sum(char.isdecimal() for char in text),
        "symbols": sum(
            unicodedata.category(char)[0] in {"P", "S"}
            for char in text
        ),
        "spaces": sum(char.isspace() for char in text),
        "lines": text.count("\n") + 1 if text else 0,
    }

    for key, value in counts.items():
        stat_labels[key].config(text=str(value))

        if not text:
            caption = "Agents are on a tea break!"
        elif value == 0:
            caption = "No agents here. Check the cafeteria!"
        else:
            caption = FUN_MESSAGES[key]

        fun_labels[key].config(
            text=caption,
            fg=MESSAGE_COLORS[key],
        )

    status_label.config(
        text="● Results updated" if text else "● Awaiting input",
        fg="#059669" if text else MUTED,
    )


def on_text_changed(event=None):
    if text_input.edit_modified():
        text_input.edit_modified(False)
        analyze_text()


def clear_text(event=None):
    text_input.delete("1.0", tk.END)
    analyze_text()
    text_input.focus_set()
    return "break"


def keyboard_analyze(event=None):
    analyze_text()
    return "break"


def resize_card_text(event, labels):
    width = max(60, event.width - 4)
    for label in labels:
        label.config(wraplength=width)


# ---------- Window ----------
window = tk.Tk()
window.title("Text Analyzer • Aminul Islam")
window.configure(bg=BG)

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

width = min(760, int(screen_width * 0.85))
height = min(680, int(screen_height * 0.75))

x = max(0, (screen_width - width) // 2)
y = max(0, (screen_height - height) // 2 - 20)

window.geometry(f"{width}x{height}+{x}+{y}")
window.minsize(min(520, width), min(350, height))


# ---------- Button Styles ----------
style = ttk.Style(window)
style.theme_use("clam")

style.configure(
    "Primary.TButton",
    font=("Segoe UI", 10, "bold"),
    foreground="white",
    background=PRIMARY,
    padding=(10, 8),
    borderwidth=0,
)
style.map(
    "Primary.TButton",
    background=[
        ("pressed", "#4338CA"),
        ("active", "#5147EB"),
    ],
)

style.configure(
    "Secondary.TButton",
    font=("Segoe UI", 10),
    foreground=TEXT,
    background="#E9EDF5",
    padding=(10, 8),
    borderwidth=0,
)
style.map(
    "Secondary.TButton",
    background=[
        ("pressed", "#CBD5E1"),
        ("active", "#DCE3EF"),
    ],
)


# ---------- Scrollable Page ----------
page_canvas = tk.Canvas(
    window,
    bg=BG,
    highlightthickness=0,
)

page_scrollbar = ttk.Scrollbar(
    window,
    orient="vertical",
    command=page_canvas.yview,
)
page_scrollbar.pack(side="right", fill="y")
page_canvas.pack(side="left", fill="both", expand=True)
page_canvas.config(yscrollcommand=page_scrollbar.set)

page = tk.Frame(page_canvas, bg=BG)

page_id = page_canvas.create_window(
    (0, 0),
    window=page,
    anchor="nw",
)


def update_scroll_region(event=None):
    page_canvas.config(scrollregion=page_canvas.bbox("all"))


def resize_page(event):
    page_canvas.itemconfigure(page_id, width=event.width)


page.bind("<Configure>", update_scroll_region)
page_canvas.bind("<Configure>", resize_page)


def scroll_page(event):
    if event.widget is text_input:
        return

    button = getattr(event, "num", None)
    delta = getattr(event, "delta", 0)

    if button == 4:
        page_canvas.yview_scroll(-1, "units")
    elif button == 5:
        page_canvas.yview_scroll(1, "units")
    elif delta:
        direction = -1 if delta > 0 else 1
        steps = max(1, abs(delta) // 120)
        page_canvas.yview_scroll(direction * steps, "units")


window.bind("<MouseWheel>", scroll_page)
window.bind("<Button-4>", scroll_page)
window.bind("<Button-5>", scroll_page)


# ---------- Heading Left + Input Right ----------

top_section = tk.Frame(page, bg=BG)
top_section.pack(fill="x", padx=16, pady=(16, 12))

top_section.columnconfigure(0, weight=2, uniform="top")
top_section.columnconfigure(1, weight=3, uniform="top")

# Left: Heading
header = tk.Frame(top_section, bg=BG)
header.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(0, 10),
)

tk.Frame(
    header,
    bg=PRIMARY,
    width=4,
).pack(side="left", fill="y", padx=(0, 10))

heading_content = tk.Frame(header, bg=BG)
heading_content.pack(side="left", fill="both", expand=True)

tagline = tk.Label(
    heading_content,
    text="YOUR TEXT. EVERY DETAIL.",
    font=("Segoe UI", 8, "bold"),
    fg=PRIMARY,
    bg=BG,
    anchor="w",
    justify="left",
    wraplength=180,
)
tagline.pack(fill="x", pady=(12, 8))

heading_title = tk.Label(
    heading_content,
    text="Text Analyzer",
    font=("Segoe UI", 20, "bold"),
    fg=TEXT,
    bg=BG,
    anchor="w",
    justify="left",
    wraplength=180,
)
heading_title.pack(fill="x")

subtitle = tk.Label(
    heading_content,
    text="Explore your text—with a little undercover humor.",
    font=("Segoe UI", 10),
    fg=MUTED,
    bg=BG,
    anchor="w",
    justify="left",
    wraplength=180,
)
subtitle.pack(fill="x", pady=(8, 12))

heading_content.bind(
    "<Configure>",
    lambda event: resize_card_text(
        event,
        (tagline, heading_title, subtitle),
    ),
)

# Right: Input
style.configure(
    "ModernAnalyze.TButton",
    font=("Segoe UI", 10, "bold"),
    foreground="white",
    background="#635BFF",
    padding=(16, 9),
    borderwidth=0,
)
style.map(
    "ModernAnalyze.TButton",
    background=[
        ("pressed", "#4338CA"),
        ("active", "#5147EB"),
    ],
)

style.configure(
    "ModernClear.TButton",
    font=("Segoe UI", 10),
    foreground="#526078",
    background="#EEF1F8",
    padding=(12, 9),
    borderwidth=0,
)
style.map(
    "ModernClear.TButton",
    background=[
        ("pressed", "#D8DFEC"),
        ("active", "#E2E7F1"),
    ],
)

# hadow ===
card_shadow = tk.Frame(
    top_section,
    bg="#E3E7F1",
)
card_shadow.grid(row=0, column=1, sticky="nsew")
card_shadow.columnconfigure(0, weight=1)
card_shadow.rowconfigure(0, weight=1)

input_card = tk.Frame(
    card_shadow,
    bg="white",
    padx=14,
    pady=12,
)
input_card.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(0, 3),
    pady=(0, 3),
)

# Heading
input_heading = tk.Frame(input_card, bg="white")
input_heading.pack(fill="x")

tk.Label(
    input_heading,
    text="Your text",
    font=("Segoe UI", 13, "bold"),
    fg="#18233B",
    bg="white",
).pack(side="left")

tk.Label(
    input_heading,
    text="● LIVE",
    font=("Segoe UI", 8, "bold"),
    fg="#047857",
    bg="#E7F8F0",
    padx=8,
    pady=4,
).pack(side="right")

helper_label = tk.Label(
    input_card,
    text="A few words. A little insight.",
    font=("Segoe UI", 10),
    fg="#778198",
    bg="white",
    anchor="w",
    justify="left",
    wraplength=220,
)
helper_label.pack(fill="x", pady=(5, 12))

# Soft editor border
editor = tk.Frame(
    input_card,
    bg="#E5E9F2",
    padx=1,
    pady=1,
)
editor.pack(fill="x")

text_input = tk.Text(
    editor,
    width=1,
    height=2,
    wrap="word",
    font=("Segoe UI", 10),
    bg="#F7F9FD",
    fg=TEXT,
    insertbackground=PRIMARY,
    insertwidth=2,
    selectbackground="#E0DCFF",
    selectforeground=TEXT,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    padx=10,
    pady=10,
    undo=True,
)
text_input.pack(side="left", fill="both", expand=True)

# Scrollbar -------------
style.configure(
    "Soft.Vertical.TScrollbar",
    background="#CCD3E3",
    troughcolor="#F7F9FD",
    bordercolor="#F7F9FD",
    lightcolor="#CCD3E3",
    darkcolor="#CCD3E3",
    arrowcolor="#64748B",
    borderwidth=0,
    arrowsize=10,
)

editor_scrollbar = ttk.Scrollbar(
    editor,
    orient="vertical",
    command=text_input.yview,
    style="Soft.Vertical.TScrollbar",
)


def update_editor_scrollbar(first, last):
    editor_scrollbar.set(first, last)

    if float(first) <= 0 and float(last) >= 1:
        editor_scrollbar.pack_forget()
    elif not editor_scrollbar.winfo_manager():
        editor_scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 2),
            pady=2,
        )


text_input.config(
    yscrollcommand=update_editor_scrollbar
)

text_input.bind("<<Modified>>", on_text_changed)
text_input.bind("<Control-Return>", keyboard_analyze)
text_input.bind("<Escape>", clear_text)


def focus_editor(event=None):
    editor.config(bg="#A59EFF")
    text_input.config(bg="white")


def unfocus_editor(event=None):
    editor.config(bg="#E5E9F2")
    text_input.config(bg="#F7F9FD")


text_input.bind("<FocusIn>", focus_editor)
text_input.bind("<FocusOut>", unfocus_editor)

# Actions
actions = tk.Frame(input_card, bg="white")
actions.pack(fill="x", pady=(12, 0))

ttk.Button(
    actions,
    text="Analyze →",
    command=analyze_text,
    style="ModernAnalyze.TButton",
).pack(side="left")

ttk.Button(
    actions,
    text="Clear",
    command=clear_text,
    style="ModernClear.TButton",
).pack(side="left", padx=(8, 0))

status_label = tk.Label(
    input_card,
    text="● Awaiting input",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg="white",
    anchor="w",
)
status_label.pack(fill="x", pady=(10, 0))

input_card.bind(
    "<Configure>",
    lambda event: helper_label.config(
        wraplength=max(80, event.width - 32)
    ),
)

#  Results
results_heading = tk.Frame(page, bg=BG)
results_heading.pack(fill="x", padx=20, pady=(6, 8))

tk.Label(
    results_heading,
    text="Text overview",
    font=("Segoe UI", 14, "bold"),
    fg=TEXT,
    bg=BG,
).pack(side="left")

tk.Label(
    results_heading,
    text="8 checkpoints",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=BG,
).pack(side="right")

stats_frame = tk.Frame(page, bg=BG)
stats_frame.pack(fill="x", padx=16)

for column in range(2):
    stats_frame.columnconfigure(
        column,
        weight=1,
        uniform="cards",
    )

for index, (key, title, accent, background) in enumerate(STAT_STYLES):
    row, column = divmod(index, 2)

    card = tk.Frame(
        stats_frame,
        bg=background,
        padx=10,
        pady=7,
    )
    card.grid(
        row=row,
        column=column,
        sticky="nsew",
        padx=4,
        pady=4,
    )

    top_row = tk.Frame(card, bg=background)
    top_row.pack(fill="x")
    top_row.columnconfigure(0, weight=1)

    title_label = tk.Label(
        top_row,
        text=title,
        font=("Segoe UI", 14, "bold"),
        fg=accent,
        bg=background,
        anchor="w",
        justify="left",
        wraplength=180,
    )
    title_label.grid(row=0, column=0, sticky="ew")

    value_label = tk.Label(
        top_row,
        text="0",
        font=("Segoe UI", 18, "bold"),
        fg=TEXT,
        bg=background,
    )
    value_label.grid(row=0, column=1, padx=(6, 0))
    stat_labels[key] = value_label

    title_label.bind(
        "<Configure>",
        lambda event, label=title_label: label.config(
            wraplength=max(60, event.width)
        ),
    )

    fun_label = tk.Label(
        card,
        text="",
        font=("Georgia", 12, "italic"),
        fg=MESSAGE_COLORS[key],
        bg=background,
        anchor="w",
        justify="left",
        wraplength=220,
    )
    fun_label.pack(fill="x", pady=(4, 0))
    fun_labels[key] = fun_label

    card.bind(
        "<Configure>",
        lambda event, label=fun_label: label.config(
            wraplength=max(50, event.width - 20)
        ),
    )


# ---------- Footer ----------
footer = tk.Frame(page, bg=BG)
footer.pack(pady=(10, 12))

tk.Label(
    footer,
    text="CRAFTED BY",
    font=("Segoe UI", 7, "bold"),
    fg=MUTED,
    bg=BG,
).pack(pady=(0, 5))

tk.Label(
    footer,
    text="✦  Aminul Islam  ✦",
    font=("Georgia", 12, "bold"),
    fg=PRIMARY,
    bg="#EFEEFF",
    padx=10,
    pady=7,
).pack()


# ---------- Start ----------
text_input.edit_modified(False)
analyze_text()
text_input.focus_set()

window.mainloop()