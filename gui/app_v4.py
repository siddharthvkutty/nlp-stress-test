import sys
import os
import customtkinter as ctk
import pandas as pd
from PIL import Image
from gui.utils_current_v3 import run_command

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
# CSV Viewer
# ----------------------------
def open_csv_viewer(relative_path):
    path = os.path.join(PROJECT_ROOT, relative_path)
    if not os.path.exists(path):
        return

    df = pd.read_csv(path)

    win = ctk.CTkToplevel(app)
    win.title(relative_path)
    win.geometry("900x500")

    text = ctk.CTkTextbox(win, wrap="none")
    text.pack(fill="both", expand=True, padx=10, pady=10)

    text.insert("end", df.to_string(index=False))
    text.configure(state="disabled")

# ----------------------------
# Image Viewer
# ----------------------------
def open_image_viewer(relative_path):
    path = os.path.join(PROJECT_ROOT, relative_path)
    if not os.path.exists(path):
        return

    img = Image.open(path)
    img.thumbnail((860, 560))

    win = ctk.CTkToplevel(app)
    win.title(relative_path)
    win.geometry("900x600")

    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
    label = ctk.CTkLabel(win, image=ctk_img, text="")
    label.image = ctk_img
    label.pack(padx=10, pady=10)

# ----------------------------
# Status Banner (cookie-style)
# ----------------------------
status_banner = ctk.CTkLabel(
    app,
    text="",
    font=ctk.CTkFont(size=14),
    text_color="white",
    fg_color=("#2a2a2a", "#1f1f1f"),
    corner_radius=10
)
status_banner.pack_forget()

def show_status(message):
    status_banner.configure(text=message)
    status_banner.pack(pady=(0, 10))
    app.update_idletasks()

def hide_status():
    status_banner.pack_forget()
    app.update_idletasks()

# ----------------------------
# Run Stress Test with Banner
# ----------------------------
def run_stress_test_with_status():
    show_status("Running stress test… please wait")
    run_command([python_cmd, "-m", "experiments.run_stress_test"])
    hide_status()

# ----------------------------
# Title
# ----------------------------
ctk.CTkLabel(
    app,
    text="NLP Stress Test Dashboard",
    font=ctk.CTkFont(size=28, weight="bold")
).pack(pady=20)

# ----------------------------
# Main Frame
# ----------------------------
frame = ctk.CTkFrame(app)
frame.pack(padx=30, pady=10, fill="both", expand=True)

# ----------------------------
# Large Button Factory
# ----------------------------
def make_button(text, command):
    btn = ctk.CTkButton(
        frame,
        text=text,
        height=50,
        font=ctk.CTkFont(size=16),
        command=command
    )
    btn.pack(fill="x", padx=20, pady=8)

# ----------------------------
# Experiments
# ----------------------------
ctk.CTkLabel(
    frame, text="Experiments",
    font=ctk.CTkFont(size=20, weight="bold")
).pack(anchor="w", padx=20, pady=(20, 10))

make_button(
    "Run Stress Test",
    run_stress_test_with_status
)

make_button(
    "Compute Metrics",
    lambda: run_command([python_cmd, "experiments/compute_metrics.py"])
)

# ----------------------------
# Analysis
# ----------------------------
ctk.CTkLabel(
    frame, text="Analysis",
    font=ctk.CTkFont(size=20, weight="bold")
).pack(anchor="w", padx=20, pady=(30, 10))

make_button(
    "Generate Metrics Report",
    lambda: run_command([python_cmd, "analysis/metrics.py"])
)

make_button(
    "Generate Plots",
    lambda: run_command([python_cmd, "analysis/plots.py"])
)

# ----------------------------
# Mitigation
# ----------------------------
ctk.CTkLabel(
    frame, text="Mitigation",
    font=ctk.CTkFont(size=20, weight="bold")
).pack(anchor="w", padx=20, pady=(30, 10))

make_button(
    "Apply Mitigation Strategies",
    lambda: run_command([python_cmd, "-m", "mitigation.apply_mitigation"])
)

# ----------------------------
# Results
# ----------------------------
ctk.CTkLabel(
    frame, text="Results",
    font=ctk.CTkFont(size=18, weight="bold")
).pack(anchor="w", padx=20, pady=(35, 8))

results_row = ctk.CTkFrame(frame, fg_color="transparent")
results_row.pack(fill="x", padx=20, pady=5)

def make_small_button(text, command):
    btn = ctk.CTkButton(
        results_row,
        text=text,
        height=32,
        width=160,
        font=ctk.CTkFont(size=13),
        command=command
    )
    btn.pack(side="left", padx=6)

make_small_button("Stress Results CSV",
                  lambda: open_csv_viewer("results/stress_results.csv"))
make_small_button("Rejection Results CSV",
                  lambda: open_csv_viewer("results/rejection_results.csv"))
make_small_button("Ensemble Results CSV",
                  lambda: open_csv_viewer("results/ensemble_results.csv"))
make_small_button("Confidence Boxplot",
                  lambda: open_image_viewer("results/figures/confidence_boxplot.png"))
make_small_button("Disagreement Bar Plot",
                  lambda: open_image_viewer("results/figures/disagreement_bar.png"))

# ----------------------------
# Footer
# ----------------------------
ctk.CTkLabel(
    app,
    text="Manual execution • CLI-faithful • Research-safe",
    font=ctk.CTkFont(size=12),
    text_color="gray"
).pack(pady=12)

app.mainloop()
