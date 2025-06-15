# Portana - Personal Portfolio Analysis Engine

**Portana is a backend system designed for personal portfolio analysis and transaction tracking. It empowers data-savvy investors and developers to consolidate investment data, track performance using advanced metrics, and gain deeper insights into their financial assets.**

Portana features a **backend system** for portfolio analysis and a **frontend user interface** built with Nuxt.js. The backend provides a REST API (FastAPI) and CLI tools, while the frontend offers data visualization and user interaction.

## Overview

Are you managing investments across multiple brokerages? Do you want to go beyond standard brokerage reports and calculate metrics like Time-Weighted Return (TWR) or Sharpe Ratio for your entire portfolio? Portana aims to solve these problems by:

*   **Consolidating** your investment data from various sources.
*   Providing **advanced performance analytics**.
*   Giving you **control over your financial data** with a self-hostable solution.
*   Supporting detailed tracking for various instruments, including **equities and options**.

## Key Features

*   **Multi-Account Management:** Track multiple investment accounts.
*   **Transaction Importing:** Importers for CSV formats from selected brokers (currently supports Fidelity, Schwab, Vanguard - primarily US-focused).
*   **Position Tracking:** Monitors quantity, average cost, and current value of your holdings.
*   **Advanced Performance Metrics:**
    *   Time-Weighted Return (TWR)
    *   Sharpe Ratio
    *   Compound Annual Growth Rate (CAGR)
    *   Daily Returns & Drawdown Analysis
*   **Visual Portfolio Insights:** Interactive charts and a dashboard to visualize portfolio performance, value over time, and rolling returns through the web interface.
*   **Price Fetching:** Automatically fetches daily market prices for equities and options using Yahoo Finance.
*   **API Access:** A comprehensive FastAPI backend provides API access to your data and calculations.
*   **CLI Tools:** For administrative tasks like user/account creation, data import, and recalculating positions/metrics.
*   **Data Ownership:** Keep your financial data on your own systems.

## User Interface (Frontend)

Portana includes a web-based user interface built with Nuxt.js (using Vue.js and Vuetify) to provide a visual way to interact with your portfolio data.

**Key Frontend Features:**

*   **User Selection:** Allows viewing data for different registered users.
*   **Portfolio Summary Chart:** Displays the total value of a user's portfolio over time.
*   **Rolling Return Charts:** Shows 7-day and 30-day rolling returns for each account, providing insights into performance trends.
*   **Interactive Charts:** Utilizes ApexCharts for dynamic data visualization.

**Running the Frontend:**

For detailed instructions on setting up and running the frontend, please refer to `frontend/portfolio/README.md`. As a quick start:
1. Navigate to the `frontend/portfolio` directory.
2. Install dependencies (e.g., `npm install`).
3. Start the development server (e.g., `npm run dev`).
The frontend will typically be accessible at `http://localhost:3000`.

## Technology Stack

*   **Backend:** Python
*   **API Framework:** FastAPI
*   **Database:** PostgreSQL
*   **ORM:** SQLAlchemy
*   **Database Migrations:** Alembic
*   **Data Analysis & Manipulation:** Pandas, NumPy
*   **Price Data Source:** Yahoo Finance (via `yfinance` library)
*   **Dependency Management:** Poetry
*   **Frontend Framework:** Nuxt.js (with Vue.js)
*   **UI Components:** Vuetify
*   **Charting Library:** ApexCharts
*   **State Management (Frontend):** Pinia

## Current Status

Portana is currently a functional backend system. Key functionalities like data import (for supported brokers), price fetching, position management, and metric calculation (TWR, Sharpe, CAGR) are implemented.

*   **Interaction:** Via REST API and CLI.
*   **User Interface:** A Nuxt.js based GUI is available, providing data visualization and user interaction. See the 'User Interface (Frontend)' section for more details.

## Target Audience

*   **Developers:** Looking for a Python-based backend to build custom financial dashboards or integrate portfolio tracking.
*   **Data-Savvy DIY Investors:** Who can benefit from both direct API/CLI access and the provided user interface for deeper insights.
*   **Investors Seeking Specific Metrics:** Particularly those interested in Time-Weighted Return and other advanced analytics.

## Getting Started

These instructions are for setting up the Portana backend. For more detailed backend developer information, see `backend/README.md`.

**Prerequisites:**

*   Python (3.8+)
*   Poetry (for dependency management)
*   PostgreSQL server, running and accessible.

**Installation & Setup:**

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository-url>
    cd portana
    ```

2.  **Install backend dependencies using Poetry:**
    ```bash
    cd backend
    poetry install
    ```

3.  **Configure Database Connection:**
    *   Copy `backend/.env.example` to `backend/.env` (you might need to create this file based on environment variables expected by `alembic.ini` and `app/db.py`).
    *   Update `backend/.env` or `backend/alembic.ini` with your PostgreSQL connection details.
    *   Example `DATABASE_URL` format: `postgresql://youruser:yourpassword@localhost:5432/portana_db`

4.  **Run Database Migrations:**
    ```bash
    poetry run alembic upgrade head
    ```
    (Ensure you are in the `backend` directory)

**Basic CLI Usage Examples (run from `backend` directory):**

*   **Create a new user:**
    ```bash
    poetry run python -m app create-user --email your@email.com --name "Your Name"
    ```
*   **Create an account for a user:**
    ```bash
    poetry run python -m app create-account --email your@email.com --brokerage schwab --account_number 12345 --nickname "My Schwab IRA"
    ```
*   **Import transactions (example for Schwab):**
    ```bash
    poetry run python -m app import --broker schwab --format transactions --email your@email.com --account 12345 --file "/path/to/your/Schwab-Transactions.csv"
    ```
    (Refer to `backend/README.md` for more import examples for other brokers/formats.)

*   **Fetch latest prices:**
    ```bash
    poetry run python -m app fetch-prices
    ```

*   **Recalculate positions and metrics:**
    ```bash
    poetry run python -m app recalculate-positions --email your@email.com --initial_load # for the first time
    poetry run python -m app recalculate-positions --email your@email.com # for subsequent updates
    ```

**API Access:**

Once the backend is running (e.g., via `uvicorn app.api_main:app --reload` from the `backend` directory), you can access:
*   API documentation (Swagger UI): `http://localhost:8000/docs`
*   Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

**Frontend Access:**

Once the backend is running and the frontend is started (see `frontend/portfolio/README.md` for setup), you can typically access the user interface at `http://localhost:3000`.

## Future Development & Contributing

Portana has the potential to evolve, particularly as a robust, developer-friendly backend for portfolio analytics.

*   **Potential Directions:**
    *   Enhancing API capabilities and documentation.
    *   **Enhancing the User Interface:** Improving UI/UX, adding more interactive visualizations, and potentially incorporating user-configurable dashboards or settings directly via the frontend.
    *   Expanding the range of supported broker importers or developing a more generic CSV import mapping tool.
    *   Adding more sophisticated financial analytics and risk metrics.
    *   Improving error handling and test coverage.

*   **Contributing:**
    *   **LICENSE:** This project does not currently have a LICENSE file. This is a crucial addition for fostering open-source collaboration. If you wish to contribute, please open an issue to discuss licensing first.
    *   Contributions are welcome via GitHub Issues (for bug reports, feature requests) and Pull Requests (for code contributions). Please ensure any PRs are well-tested.

---

This README provides a high-level overview of Portana. For detailed backend setup and development, please refer to `backend/README.md`.
