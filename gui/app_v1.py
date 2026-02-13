import sys
import customtkinter as ctk
from gui.utils import run_command

# ----------------------------
# Appearance
# ----------------------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("NLP Stress Test – Control Panel")
app.geometry("820x560")
app.minsize(780, 520)

python_cmd = sys.executable

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
# Button Factory
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
# Footer
# ----------------------------
footer = ctk.CTkLabel(
    app,
    text="Manual execution • CLI-faithful • Research-safe",
    font=ctk.CTkFont(size=12),
    text_color="gray"
)
footer.pack(pady=10)

app.mainloop()
