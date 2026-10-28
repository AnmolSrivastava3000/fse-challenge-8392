# UK Day-Ahead Wind Generation Analysis

This repository contains a full-stack application built to evaluate the accuracy of UK wind generation forecasts for day-ahead market trading decisions.

## Live Links

* **Frontend Application (Vercel):** [Insert your Vercel URL here]
* **Backend API (Render):** [Insert your Render URL here]
* **Video Demo (YouTube):** [Insert your Unlisted YouTube URL here]

## Architecture & Key Domain Logic

The client purchases electricity on the day-ahead market, meaning decisions for delivery on Day X must be finalized on Day X-1.

To accurately reflect the information available to a trader at the time of decision:

1. **Decision Date Alignment:** The backend utilizes Pandas to calculate a `decision_date` (Delivery Date minus 1 day).
2. **Forecast Filtering:** The system filters Elexon's `WINDFOR` dataset to strictly isolate forecasts published *on or before* the decision date. It then selects the latest valid forecast prior to the trading cutoff.
3. **Metrics Calculation:** The valid day-ahead forecasts are merged with the actual outturn generation (`FUELHH`) on 30-minute `startTime` intervals to calculate the Mean Absolute Error (MAE) and Root Mean Square Error (RMSE).

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
