import threading
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.fetch_data import load_driver_laps
from src.process import process_telemetry_comparison
from src.visualize import create_telemetry_figure


class F1TelemetryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FastF1 Telemetry Analyzer")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1e1e1e")

        self.canvas = None
        self.setup_ui()

    def setup_ui(self):
        # Left Sidebar for User Input Controls (Fixed: padx/pady instead of pad)
        sidebar = tk.Frame(self.root, bg="#252526", width=260, padx=15, pady=15)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        title = tk.Label(sidebar, text="F1 Telemetry Config", font=("Helvetica", 13, "bold"), fg="#FFFFFF", bg="#252526")
        title.pack(anchor="w", pady=(0, 15))

        # Input Parameter Fields
        self.year_var = self.create_input_field(sidebar, "Season Year:", "2024")
        self.track_var = self.create_input_field(sidebar, "Grand Prix / Track:", "Silverstone")
        self.session_var = self.create_input_field(sidebar, "Session (Q, R, FP3):", "Q")
        self.d1_var = self.create_input_field(sidebar, "Driver 1 Code:", "VER")
        self.d2_var = self.create_input_field(sidebar, "Driver 2 Code:", "NOR")

        # Run Button (Fixed: pady/padx instead of pad)
        self.btn_run = tk.Button(
            sidebar, text="Compare Drivers", command=self.start_analysis_thread,
            bg="#007ACC", fg="white", font=("Helvetica", 10, "bold"), relief="flat",
            padx=10, pady=5
        )
        self.btn_run.pack(fill=tk.X, pady=20)

        # Status Notification Label
        self.lbl_status = tk.Label(sidebar, text="Ready", fg="#AAAAAA", bg="#252526", font=("Helvetica", 9), wraplength=200)
        self.lbl_status.pack(anchor="w")

        # Main Plot Display Area
        self.plot_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def create_input_field(self, parent, label_text, default_val):
        lbl = tk.Label(parent, text=label_text, fg="#CCCCCC", bg="#252526", font=("Helvetica", 9))
        lbl.pack(anchor="w", pady=(5, 2))
        entry = tk.Entry(parent, bg="#3c3c3c", fg="white", insertbackground="white", relief="flat")
        entry.insert(0, default_val)
        entry.pack(fill=tk.X, pady=(0, 5))
        return entry

    def start_analysis_thread(self):
        """Dispatches data fetching to a background thread to preserve UI responsiveness."""
        self.btn_run.config(state=tk.DISABLED)
        self.lbl_status.config(text="Downloading telemetry data...", fg="#FFCC00")
        threading.Thread(target=self.run_analysis, daemon=True).start()

    def run_analysis(self):
        try:
            year = self.year_var.get().strip()
            track = self.track_var.get().strip()
            session_type = self.session_var.get().strip()
            d1 = self.d1_var.get().strip().upper()
            d2 = self.d2_var.get().strip().upper()

            # Execute pipeline
            session, lap_d1, lap_d2 = load_driver_laps(year, track, session_type, d1, d2)
            tel_d1, tel_d2, delta_time, ref_dist, meta = process_telemetry_comparison(lap_d1, lap_d2)
            fig = create_telemetry_figure(tel_d1, tel_d2, delta_time, ref_dist, meta)

            # Update Canvas on Main Thread
            self.root.after(0, self.update_plot_canvas, fig)

        except Exception as err:
            self.root.after(0, self.handle_error, str(err))

    def update_plot_canvas(self, fig):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.lbl_status.config(text="Analysis Complete!", fg="#00FF00")
        self.btn_run.config(state=tk.NORMAL)

    def handle_error(self, error_message):
        self.lbl_status.config(text="Error occurred.", fg="#FF5555")
        self.btn_run.config(state=tk.NORMAL)
        messagebox.showerror("Execution Error", error_message)


if __name__ == "__main__":
    root = tk.Tk()
    app = F1TelemetryApp(root)
    root.mainloop()