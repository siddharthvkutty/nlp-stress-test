import sys
import os
import subprocess
import customtkinter as ctk
from gui.utils import run_command

# ----------------------------
# Appearance
# ----------------------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("NLP Stress Test – Control Panel")
app.geometry("900x620")
app.minsize(820, 580)

python_cmd = sys.executable
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ----------------------------
# Helpers
# ----------------------------
def open_file(relative_path):
    path = os.path.join(PROJECT_ROOT, relative_path)

    if not os.path.exists(path):
        ctk.CTkMessagebox(
            title="File Not Found",
            message=f"{relative_path} does not exist.",
            icon="cancel"
        )
        return

    try:
        if sys.platform.startswith("linux"):
            # Prefer gio (avoids snap/glibc issues)
            subprocess.Popen(["gio", "open", path])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        elif sys.platform.startswith("win"):
            subprocess.Popen(["start", path], shell=True)

    except Exception as e:
        ctk.CTkMessagebox(
            title="Error",
            message=str(e),
            icon="cancel"
        )


# ----------------------------
# Title
# ----------------------------
title = ctk.CTkLabel(
    app,
    text="NLP Stress Test Dashboard",
    font=ctk.CTkFont(size=28, weight="bold")
)
title.pack(pady=20)

# ----------------------------
# Main Frame
# ----------------------------
frame = ctk.CTkFrame(app)
frame.pack(padx=30, pady=10, fill="both", expand=True)

# ----------------------------
# Button Factory (large)
# ----------------------------
def make_button(text, command):
    btn = ctk.CTkButton(
        frame,
        text=text,
        height=50,
        font=ctk.CTkFont(size=16),
        command=lambda: run_command(command)
    )
    btn.pack(fill="x", padx=20, pady=8)

# ----------------------------
# Experiments
# ----------------------------
exp_label = ctk.CTkLabel(
    frame,
    text="Experiments",
    font=ctk.CTkFont(size=20, weight="bold")
)
exp_label.pack(anchor="w", padx=20, pady=(20, 10))

make_button(
    "Run Stress Test",
    [python_cmd, "-m", "experiments.run_stress_test"]
)

make_button(
    "Compute Metrics",
    [python_cmd, "experiments/compute_metrics.py"]
)

# ----------------------------
# Analysis
# ----------------------------
analysis_label = ctk.CTkLabel(
    frame,
    text="Analysis",
    font=ctk.CTkFont(size=20, weight="bold")
)
analysis_label.pack(anchor="w", padx=20, pady=(30, 10))

make_button(
    "Generate Metrics Report",
    [python_cmd, "analysis/metrics.py"]
)

make_button(
    "Generate Plots",
    [python_cmd, "analysis/plots.py"]
)

# ----------------------------
# Mitigation
# ----------------------------
mit_label = ctk.CTkLabel(
    frame,
    text="Mitigation",
    font=ctk.CTkFont(size=20, weight="bold")
)
mit_label.pack(anchor="w", padx=20, pady=(30, 10))

make_button(
    "Apply Mitigation Strategies",
    [python_cmd, "-m", "mitigation.apply_mitigation"]
)

# ----------------------------
# Results (compact row)
# ----------------------------
results_label = ctk.CTkLabel(
    frame,
    text="Results",
    font=ctk.CTkFont(size=18, weight="bold")
)
results_label.pack(anchor="w", padx=20, pady=(35, 8))

results_row = ctk.CTkFrame(frame, fg_color="transparent")
results_row.pack(fill="x", padx=20, pady=5)

def make_small_button(parent, text, path):
    return ctk.CTkButton(
        parent,
        text=text,
        height=32,
        width=160,
        font=ctk.CTkFont(size=13),
        command=lambda: open_file(path)
    )

make_small_button(
    results_row,
    "Stress Results CSV",
    "results/stress_results.csv"
).pack(side="left", padx=6)

make_small_button(
    results_row,
    "Rejection Results CSV",
    "results/rejection_results.csv"
).pack(side="left", padx=6)

make_small_button(
    results_row,
    "Ensemble Results CSV",
    "results/ensemble_results.csv"
).pack(side="left", padx=6)

make_small_button(
    results_row,
    "Confidence Boxplot",
    "results/figures/confidence_boxplot.png"
).pack(side="left", padx=6)

make_small_button(
    results_row,
    "Disagreement Bar Plot",
    "results/figures/disagreement_bar.png"
).pack(side="left", padx=6)

# ----------------------------
# Footer
# ----------------------------
footer = ctk.CTkLabel(
    app,
    text="Manual execution • CLI-faithful • Research-safe",
    font=ctk.CTkFont(size=12),
    text_color="gray"
)
footer.pack(pady=12)

app.mainloop()
