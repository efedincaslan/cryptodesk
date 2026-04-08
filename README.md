rypto Desk
A real-time cryptocurrency trading dashboard built with a FastAPI backend and vanilla HTML/CSS/JS frontend. Pulls live market data from the CoinGecko API and persists orders and price history to a PostgreSQL database.
What it does

Displays live prices and 24h change for BTC, ETH, BNB, SOL, and AVAX
Lets users place buy/sell orders through a simple UI
Saves every order to Postgres with a UUID, timestamp, and validated fields
Snapshots coin prices on every fetch for historical analysis
Automatically cleans up price snapshots older than 7 days

Tech stack

Backend: Python, FastAPI, SQLAlchemy (async), asyncpg
Frontend: HTML, CSS, JavaScript
Database: PostgreSQL
External API: CoinGecko

Project structure
crypto-desk/
├── main.py        # FastAPI app, routes, lifespan
├── models.py      # SQLAlchemy table definitions
├── database.py    # Engine, session, get_db
├── schemas.py     # Pydantic request validation
├── index.html     # Frontend
├── .env           # Credentials (never committed)
└── .gitignore
Running locally

Clone the repo
Install dependencies

bashpip install fastapi uvicorn sqlalchemy asyncpg httpx python-dotenv

Create a .env file in the root directory

DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password

Create a Postgres database called cryptodesk
Start the server

bashuvicorn main:app --reload

Open index.html in your browser

Tables are created automatically on first startup.
API endpoints
MethodEndpointDescriptionGET/pricesFetches live prices from CoinGecko and saves a snapshot to the databasePOST/orderValidates and saves a buy or sell order to the database
Data validation
Orders are rejected if:

quantity is 0 or negative
price is 0 or negative
order_type is anything other than buy or sell
coin is not one of the supported symbols
