# F1 Qualifying Teammate Telemetry & Driving Style Comparison

An end-to-end data science project analyzing high-frequency Formula 1 telemetry data using the `FastF1` API. This project extracts, synchronizes, and visualizes lap telemetry (speed, throttle, braking, gear, and delta time) between two teammates on their fastest qualifying laps to evaluate distinct driving techniques and setup differences.

---

## 📌 Features

- **Automated Data Retrieval:** Fetch qualifying session timing, lap times, and telemetry streams directly via `FastF1`.
- **Distance-Based Alignment:** Normalize telemetry channels against continuous lap distance rather than time for direct spatial comparison.
- **Delta Time Calculation:** Compute the precise gap progression (in seconds) between drivers across the circuit layout.
- **Driving Style Analytics:** Compare throttle application aggressiveness, braking points, gear selection, and apex speed retention.
- **Custom Visualizations:** Multi-panel telemetry plots formatted with official team brand colors.

---

## 🛠 Tech Stack

- **Language:** Python 3.9+
- **Data Retrieval & Analysis:** `fastf1`, `pandas`, `numpy`
- **Visualization:** `matplotlib`, `seaborn`
- **Caching:** Built-in `fastf1` file cache for optimized performance

---

## 📂 Repository Structure

```text
├── data/                  # Local cache directory for FastF1 raw data
├── notebooks/             # Exploratory Data Analysis (EDA) and prototype scripts
├── src/
│   ├── fetch_data.py      # Session loader and data validation functions
│   ├── process.py         # Telemetry alignment, distance interpolation, and delta math
│   └── visualize.py       # Matplotlib multi-panel plotting engine
├── outputs/               # Saved high-resolution telemetry charts (.png)
├── main.py                # Pipeline execution script
├── requirements.txt       # Project dependencies
└── README.md