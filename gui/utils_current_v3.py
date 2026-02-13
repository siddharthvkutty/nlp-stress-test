import subprocess
import os
import sys
from tkinter import messagebox

# Absolute path to project root
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

def run_command(command):
    """
    Runs an explicit shell-style command (list form),
    exactly like typing it in the terminal.
    """

    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            env=os.environ
        )

        if result.returncode != 0:
            messagebox.showerror(
                "Execution Failed",
                f"Command:\n{' '.join(command)}\n\n"
                f"STDERR:\n{result.stderr}"
            )
        else:
            messagebox.showinfo(
                "Success",
                "Execution done successfully."
            )

    except Exception as e:
        messagebox.showerror("Error", str(e))
