"""
--------------------------------------------------
Math-Aware Assistant (MAA) Documentation
--------------------------------------------------

Machine Used:
ChatGPT

Prompt Used:
"Enhance a simple math chatbot so it can solve derivatives, integrals,
limits, and algebra problems using SymPy instead of basic eval()."

Answer Given by the Machine:
ChatGPT provided a revised version of the chatbot that:
- Uses the SymPy library for symbolic math.
- Detects user intent (derivative, integral, limit, algebra).
- Parses natural language expressions.
- Solves calculus and algebra problems symbolically.

Justification:
The original crude code only supported basic arithmetic using eval(),
which is limited and unsafe. It could not solve algebraic or calculus
problems.

The AI-supplied code was sufficient because it:
1. Replaced eval() with SymPy for safe symbolic computation.
2. Added intent detection for calculus and algebra tasks.
3. Enabled the chatbot to solve derivatives, integrals, limits, and equations.
4. Made the chatbot more advanced and aligned with the activity goal.

Therefore, the enhanced code fulfills the requirements of the activity.
--------------------------------------------------
"""

import sympy as sp
import re
import tkinter as tk
from tkinter import scrolledtext
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)

x = sp.symbols('x')
transformations = standard_transformations + (implicit_multiplication_application,)


# ----------------------------
# Math Processing Functions
# ----------------------------
def clean_text(text):
    text = text.lower()
    text = text.replace("^", "**")
    return text.strip()


def detect_intent(text):
    if re.search(r'\bderivative\b|\bdifferentiate\b', text):
        return "derivative"
    if re.search(r'\bintegral\b|\bintegrate\b', text):
        return "integral"
    if re.search(r'\blimit\b', text):
        return "limit"
    if re.search(r'\bsolve\b|=', text):
        return "algebra"
    return "expression"


def extract_expression(text):
    patterns = [
        r'derivative of (.+)',
        r'differentiate (.+)',
        r'integral of (.+)',
        r'integrate (.+)',
        r'limit of (.+)',
        r'solve (.+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)

    return text


def solve_problem(intent, text):
    try:
        expr_text = extract_expression(text)

        # Algebra equation handling
        if intent == "algebra" and "=" in expr_text:
            left, right = expr_text.split("=")
            left_expr = parse_expr(left, transformations=transformations, local_dict={"x": x})
            right_expr = parse_expr(right, transformations=transformations, local_dict={"x": x})
            equation = sp.Eq(left_expr, right_expr)
            return sp.solve(equation, x)

        expr = parse_expr(
            expr_text,
            transformations=transformations,
            local_dict={
                "x": x,
                "sin": sp.sin,
                "cos": sp.cos,
                "tan": sp.tan,
                "log": sp.log,
                "exp": sp.exp
            }
        )

        if intent == "derivative":
            return sp.diff(expr, x)

        if intent == "integral":
            return f"{sp.integrate(expr, x)} + C"

        if intent == "limit":
            return sp.limit(expr, x, 0)

        if intent == "algebra":
            return sp.solve(expr, x)

        return expr

    except Exception:
        return "I cannot understand or solve this problem."


# ----------------------------
# GUI Functions
# ----------------------------
def send_message(event=None):
    user_text = entry.get()
    if not user_text.strip():
        return

    chat_window.insert(tk.END, "You: " + user_text + "\n")
    entry.delete(0, tk.END)

    processed = clean_text(user_text)
    intent = detect_intent(processed)
    answer = solve_problem(intent, processed)

    chat_window.insert(tk.END, "Bot: " + str(answer) + "\n\n")
    chat_window.yview(tk.END)  # auto-scroll


# ----------------------------
# GUI Layout
# ----------------------------
app = tk.Tk()
app.title("Math-Aware Assistant (MAA)")
app.geometry("600x450")

# Title label
title_label = tk.Label(
    app,
    text="Math-Aware Assistant",
    font=("Arial", 16, "bold")
)
title_label.pack(pady=5)

# Chat window
chat_window = scrolledtext.ScrolledText(
    app,
    wrap=tk.WORD,
    width=70,
    height=20,
    font=("Consolas", 11)
)
chat_window.pack(padx=10, pady=10)

# Input frame
input_frame = tk.Frame(app)
input_frame.pack(pady=5)

entry = tk.Entry(input_frame, width=50, font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=5)
entry.bind("<Return>", send_message)  # Enter key support

send_button = tk.Button(
    input_frame,
    text="Send",
    width=10,
    command=send_message
)
send_button.pack(side=tk.LEFT)

# Welcome message
chat_window.insert(
    tk.END,
    "Bot: Hello! I can solve arithmetic, algebra, derivatives, integrals, and limits.\n\n"
)

app.mainloop()

# Nicolas, Euan Roie M. - CS303
# 2157-6INTELSY