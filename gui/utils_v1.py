import subprocess
import sys
import os
from tkinter import messagebox

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def run_script(relative_path):
    script_path = os.path.join(PROJECT_ROOT, relative_path)

    if not os.path.exists(script_path):
        messagebox.showerror("Error", f"Script not found:\n{relative_path}")
        return

    try:
        subprocess.run(
            [sys.executable, script_path],
            cwd=PROJECT_ROOT,
            check=True
        )
        messagebox.showinfo("Success", f"Execution done:\n{relative_path}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror(
            "Execution Failed",
            f"Script failed:\n{relative_path}\n\n{e}"
        )
