# UK Day-Ahead Wind Generation Analysis

This repository contains a full-stack application built to evaluate the accuracy of UK wind generation forecasts for day-ahead market trading decisions.

## Live Links

* **Frontend Application (Vercel):** https://fse-challenge-8392.vercel.app/
* **Backend API (Render):** https://fse-challenge-8392.onrender.com
* **Video Demo (YouTube):** [Insert your Unlisted YouTube URL here]

## Architecture & Key Domain Logic

The client needs to estimate wind generation available for the delivery day before making day-ahead electricity procurement decisions. This application evaluates national-level UK wind generation forecasts against actual generation using Elexon data for January 2026.

1. **Decision-date alignment:** The backend uses Pandas to derive the decision date as the calendar day before the delivery date.
2. **Forecast selection:** Forecast records from Elexon's `WINDFOR` dataset are filtered using their `publishTime`. For each delivery interval, the latest eligible forecast published on or before the configured decision cutoff is selected. The cutoff is an explicit modelling assumption and should be aligned with the relevant market's trading rules.
3. **Actual generation:** The selected forecasts are matched with actual wind generation from the `FUELHH` dataset using the corresponding 30-minute `startTime`.
4. **Missing-data handling:** An inner join excludes intervals without matching forecast and actual records. Rows with missing generation values are also excluded from metric calculations rather than treating missing observations as zero generation.
5. **Forecast accuracy:** The backend calculates Mean Absolute Error (MAE) and Root Mean Square Error (RMSE) from the valid matched observations. Absolute error is also available for interval-level analysis.

These metrics quantify historical forecast error; they do not independently determine the optimal electricity procurement quantity.

### Key Technical Decisions

- **Time-series alignment:** Forecasts and actuals are matched by delivery interval to avoid comparing values from different half-hour periods.
- **Forecast availability:** Forecast publication timestamps are considered when selecting forecasts for the day-ahead evaluation. The selected cutoff is a modelling assumption and may need adjustment for a specific market or auction.
- **Metric integrity:** Missing or unmatched observations are excluded from MAE and RMSE calculations. Zero-filling would incorrectly treat missing data as genuine zero-MW generation.
- **Separation of concerns:** FastAPI handles data retrieval and analysis, while React presents the resulting metrics and visualizations.
- **Deployment:** Docker packages the backend, Render hosts the backend API, and Vercel hosts the frontend.

## Tech Stack

* **Frontend:** React, Vite, Recharts, Lucide-react
* **Backend:** Python, FastAPI, Pandas, HTTPX
* **Deployment:** Docker (Render) & Vercel

## Repository Structure

```text
├── backend/
│   ├── main.py              # FastAPI server and Pandas data merging logic
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Containerization setup for the API
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React dashboard component (Charts & KPIs)
│   │   └── main.jsx         # Vite entry point
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
└── README.md                # Project documentation

```

## How to Run Locally

### 1. Backend Setup

Navigate into the backend directory and set up the Python environment:

```bash
cd backend
python -m venv venv
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

```

The API will be available at `[http://127.0.0.1:8000/api/analysis](http://127.0.0.1:8000/api/analysis)`.

### 2. Frontend Setup

Open a new terminal, navigate to the frontend directory, and start the development server:

```bash
cd frontend
npm install
npm run dev

```

The React application will run locally at `http://localhost:5173`.

## AI Tools Used

Generative AI (Gemini) was utilized during this project to:

* Scaffold boilerplate React components and Recharts syntax.
* Debug and format strict RFC 3339 date strings required by the Elexon BMRS historical API endpoints.
* Generate the backend Dockerfile configuration.
