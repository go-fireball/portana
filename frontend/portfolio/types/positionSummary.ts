export interface PositionSummary {
    symbol: string
    quantity: number
    total_cost: number
}

export interface PortfolioPoint {
    as_of_date: string;     // ISO date string, e.g., "2024-01-01"
    total_value: number;    // e.g., 12345.67
}
