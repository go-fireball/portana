export interface PortfolioPoint {
    as_of_date: string;     // ISO date string, e.g., "2024-01-01"
    total_value: number;    // e.g., 12345.67
}

export interface Price{
    symbol: string;
    price_date: string;
    price: number;
}

export interface RealizedPnlPoint {
    date: string;        // ISO date string, e.g., "2024-01-01"
    realized_pnl: number; // e.g., 123.45
}

export interface UnrealizedPnlPoint {
    date: string;        // ISO date string, e.g., "2024-01-01"
    unrealized_pnl: number; // e.g., 123.45
}

export interface UserPortfolioMetric {
    snapshot_date: string;
    portfolio_value:number,
    cash_balance:number,
    daily_return:number,
    twr_to_date:number,
    rolling_return_7d:number,
    rolling_return_30d:number,
    sharpe_to_date:number,
    drawdown_to_date:number,
}