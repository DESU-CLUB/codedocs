from nbformat import v4 as nbf
import nbformat

# Create a new notebook
nb = nbformat.v4.new_notebook()

# Metadata for the notebook
metadata = {
    "language": "python",
    "title": "Python Concurrency Tutorial: Minimal Puzzles"
}

# Set notebook metadata
nb['metadata'] = metadata

# Cells to include in the notebook
text = """## Python Concurrency Tutorial: Minimal Puzzles

This tutorial presents minimal puzzles on implementing concurrency in Python using threads and asynchronous I/O.

### Puzzle 1: Threading
Implement a Python script using the `threading` module that starts a thread which prints "Hello from Thread!".

### Puzzle 2: Asynchronous I/O
Write an asynchronous Python function that prints "Hello from Async!" and use `asyncio` to run it.

### Expected Output:
- For Puzzle 1, you should see "Hello from Thread!" printed to the console.
- For Puzzle 2, you should see "Hello from Async!" printed to the console."""

code = """
# Puzzle 1: Threading
import threading

# FILL IN HERE (~1 line)

# Puzzle 2: Asynchronous I/O
import asyncio

# FILL IN HERE (~2 lines)
"""

# Create cells for text and code
text_cell = nbf.new_markdown_cell(text)
code_cell = nbf.new_code_cell(code)

# Append cells to the notebook
nb['cells'] = [text_cell, code_cell]

# Save the notebook
notebook_path = './Python_Concurrency_Tutorial_Minimal_Puzzles.ipynb'
with open(notebook_path, 'w') as f:
    nbformat.write(nb, f)

notebook_path
