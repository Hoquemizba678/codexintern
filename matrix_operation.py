

import tkinter as tk
from tkinter import messagebox
import numpy as np


# Function to convert text input into NumPy array
def parse_matrix(input_text):
    try:
        lines = input_text.strip().split('\n')
        matrix = [list(map(float, line.strip().split())) for line in lines]
        return np.array(matrix)
    except Exception:
        messagebox.showerror("Invalid Input", "Please enter valid numeric matrix data.")
        return None


def display_result(result):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, str(result))


def add_matrices():
    A = parse_matrix(matrix_a_text.get("1.0", tk.END))
    B = parse_matrix(matrix_b_text.get("1.0", tk.END))
    if A is not None and B is not None:
        try:
            result = A + B
            display_result(result)
        except Exception as e:
            messagebox.showerror("Error", str(e))


def subtract_matrices():
    A = parse_matrix(matrix_a_text.get("1.0", tk.END))
    B = parse_matrix(matrix_b_text.get("1.0", tk.END))
    if A is not None and B is not None:
        try:
            result = A - B
            display_result(result)
        except Exception as e:
            messagebox.showerror("Error", str(e))


def multiply_matrices():
    A = parse_matrix(matrix_a_text.get("1.0", tk.END))
    B = parse_matrix(matrix_b_text.get("1.0", tk.END))
    if A is not None and B is not None:
        try:
            result = np.dot(A, B)
            display_result(result)
        except Exception as e:
            messagebox.showerror("Error", str(e))


def transpose_matrix():
    A = parse_matrix(matrix_a_text.get("1.0", tk.END))
    if A is not None:
        result = np.transpose(A)
        display_result(result)


def determinant_matrix():
    A = parse_matrix(matrix_a_text.get("1.0", tk.END))
    if A is not None:
        try:
            result = np.linalg.det(A)
            display_result(round(result, 3))
        except np.linalg.LinAlgError:
            messagebox.showerror("Error", "Determinant only valid for square matrices.")


# ---- GUI SECTION ----
root = tk.Tk()
root.title("Matrix Operations Tool 🧮")
root.geometry("850x600")
root.config(bg="#E3F2FD")

# Titles
tk.Label(root, text="Matrix Operations Tool", font=("Helvetica", 18, "bold"), bg="#E3F2FD", fg="#0D47A1").pack(pady=10)

# Input Areas
frame = tk.Frame(root, bg="#E3F2FD")
frame.pack(pady=10)

tk.Label(frame, text="Matrix A:", bg="#E3F2FD", font=("Arial", 12)).grid(row=0, column=0, padx=10)
matrix_a_text = tk.Text(frame, height=8, width=30, font=("Courier", 10))
matrix_a_text.grid(row=1, column=0, padx=10)

tk.Label(frame, text="Matrix B:", bg="#E3F2FD", font=("Arial", 12)).grid(row=0, column=1, padx=10)
matrix_b_text = tk.Text(frame, height=8, width=30, font=("Courier", 10))
matrix_b_text.grid(row=1, column=1, padx=10)

# Buttons
btn_frame = tk.Frame(root, bg="#E3F2FD")
btn_frame.pack(pady=15)

buttons = [
    ("Add", add_matrices),
    ("Subtract", subtract_matrices),
    ("Multiply", multiply_matrices),
    ("Transpose (A)", transpose_matrix),
    ("Determinant (A)", determinant_matrix)
]

for (text, cmd) in buttons:
    tk.Button(btn_frame, text=text, command=cmd, font=("Arial", 11, "bold"), bg="#64B5F6", fg="white",
              activebackground="#1976D2", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

# Result Section
tk.Label(root, text="Result:", bg="#E3F2FD", font=("Arial", 12, "bold")).pack(pady=5)
result_text = tk.Text(root, height=10, width=80, font=("Courier", 10))
result_text.pack(pady=10)

# Footer
tk.Label(root, text="Created by Mizbaul & ChatGPT", bg="#E3F2FD", fg="#1565C0", font=("Arial", 10, "italic")).pack(pady=5)

root.mainloop()