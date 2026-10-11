import tkinter as tk
from tkinter import messagebox


def analyze_text():
    text = text_input.get().strip()

    result_label.config(text="")

    if text == "":
        messagebox.showwarning(
            "Alert",
            "Please enter some text!"
        )
        return

    length = len(text)
    words = text.split()

    if len(words) == 1:
        result_label.config(
            text=f"One word detected.\nLength: {length} characters."
        )
    else:
        result_label.config(
            text=f"Multiple words detected.\n"
                 f"Total text length: {length} characters."
        )

window = tk.Tk()
window.title("Text Analyzer")
window.geometry("450x300")

# Heading Line
title = tk.Label(
    window,
    text="Text Analyzer",
    font=("Arial", 22, "bold")
)
title.pack(pady=15)

# Instruction
instruction = tk.Label(
    window,
    text="Enter your text:"
)
instruction.pack()

# Text input
text_input = tk.Entry(
    window,
    font=("Arial", 14),
    width=30
)
text_input.pack(pady=10)

# Analyze Button
button = tk.Button(
    window,
    text="ANALYZE",
    command=analyze_text
)
button.pack(pady=5)

# Result
result_label = tk.Label(
    window,
    text="",
    font=("Arial", 12),
    fg="green"
)
result_label.pack(pady=15)


window.mainloop()

#aminul