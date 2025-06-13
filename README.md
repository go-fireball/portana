# Portana - Personal Portfolio Analysis Engine

**Portana is a backend system designed for personal portfolio analysis and transaction tracking. It empowers data-savvy investors and developers to consolidate investment data, track performance using advanced metrics, and gain deeper insights into their financial assets.**

Portana is currently a **backend-only** solution, providing a REST API (built with FastAPI) and Command-Line Interface (CLI) tools. It does not yet include a graphical user interface.

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
*   **Price Fetching:** Automatically fetches daily market prices for equities and options using Yahoo Finance.
*   **API Access:** A comprehensive FastAPI backend provides API access to your data and calculations.
*   **CLI Tools:** For administrative tasks like user/account creation, data import, and recalculating positions/metrics.
*   **Data Ownership:** Keep your financial data on your own systems.

## Technology Stack

*   **Backend:** Python
*   **API Framework:** FastAPI
*   **Database:** PostgreSQL
*   **ORM:** SQLAlchemy
*   **Database Migrations:** Alembic
*   **Data Analysis & Manipulation:** Pandas, NumPy
*   **Price Data Source:** Yahoo Finance (via `yfinance` library)
*   **Dependency Management:** Poetry

## Current Status

Portana is currently a functional backend system. Key functionalities like data import (for supported brokers), price fetching, position management, and metric calculation (TWR, Sharpe, CAGR) are implemented.

*   **Interaction:** Via REST API and CLI.
*   **User Interface:** No GUI is provided with this backend. Users would typically interact with Portana programmatically or via a custom-built frontend.

## Target Audience

*   **Developers:** Looking for a Python-based backend to build custom financial dashboards or integrate portfolio tracking.
*   **Data-Savvy DIY Investors:** Comfortable with APIs/CLI or willing to set up a separate frontend to gain deeper insights into their portfolio.
*   **Investors Seeking Specific Metrics:** Particularly those interested in Time-Weighted Return and other advanced analytics.

## Getting Started (Backend Setup)

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

## Future Development & Contributing

Portana has the potential to evolve, particularly as a robust, developer-friendly backend for portfolio analytics.

*   **Potential Directions:**
    *   Enhancing API capabilities and documentation.
    *   Expanding the range of supported broker importers or developing a more generic CSV import mapping tool.
    *   Adding more sophisticated financial analytics and risk metrics.
    *   Improving error handling and test coverage.

*   **Contributing:**
    *   **LICENSE:** This project does not currently have a LICENSE file. This is a crucial addition for fostering open-source collaboration. If you wish to contribute, please open an issue to discuss licensing first.
    *   Contributions are welcome via GitHub Issues (for bug reports, feature requests) and Pull Requests (for code contributions). Please ensure any PRs are well-tested.

---

This README provides a high-level overview of Portana. For detailed backend setup and development, please refer to `backend/README.md`.
