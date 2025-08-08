# 🚀 Dynamic Pricing Engine

A real-time AI-powered pricing dashboard built with **FastAPI**, **SQLite**, and **Chart.js**.  
It helps optimize product prices based on demand, inventory, competitor pricing, customer segments, and seasonality.

---

## 📂 Project Structure

├── Index.html # Frontend HTML UI
├── Style.css # Frontend styling
├── Script.js # Frontend JavaScript (API calls + chart updates)
├── main.py # Backend API (FastAPI + SQLite)
└── pricing.db # SQLite database (auto-created on first run)

---

## ⚙️ Requirements

- **Python 3.8+**
- **pip** package manager
- A modern browser (Chrome, Firefox, Edge)

---

## 📦 Installation & Setup

```bash
# 1️⃣ Clone or download this repository
git clone https://github.com/yourusername/dynamic-pricing-engine.git
cd dynamic-pricing-engine

# 2️⃣ Create a virtual environment (recommended)
python -m venv venv
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 3️⃣ Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic

# 4️⃣ Start the backend API
python main.py
# OR:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
http://localhost:8000
GET http://localhost:8000/health
# Option 1: Just open Index.html in your browser

# Option 2: Serve with Python's HTTP server
python -m http.server 5500
http://localhost:5500/Index.html
| Method | Endpoint                         | Description                       |
| ------ | -------------------------------- | --------------------------------- |
| POST   | `/calculate-price`               | Calculate optimal price           |
| GET    | `/analytics/pricing-performance` | Fetch pricing analytics & trends  |
| POST   | `/competitor-prices/update`      | Simulate competitor price updates |
| GET    | `/health`                        | Health check                      |

📊 Features
Dynamic Price Calculation (default, aggressive, conservative strategies)

Analytics Dashboard (revenue, conversion rate, price change tracking)

Competitor Price Simulation

Chart.js Visualization for trends

🛠 Development Notes
The database (pricing.db) is auto-created.

To reset, delete pricing.db and restart backend.

CORS enabled for all origins in local testing.
🛠 Development Notes
The database (pricing.db) is auto-created.

To reset, delete pricing.db and restart backend.

CORS enabled for all origins in local testing.


MIT License © 2025 Runtime Terrors
