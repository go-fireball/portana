import type {User} from "~/types/user";
import {useApiClient} from "~/composables/useApiClient";
import type {PortfolioPoint, RealizedPnlPoint, UnrealizedPnlPoint, UserPortfolioMetric} from "~/types/portfolioPoint";
import type {RollingReturnPoint} from "~/types/rollingReturnPoint";
import type {PositionSummary} from "~/types/positionSummary";

type UsersResponse = {
    users: User[]
}
type PositionSummaryResponse = {
    positions: PositionSummary[]
}

export type PositionSummaryByAccountResponse = {
    positions_by_account: {
        [accountId: string]: PositionSummary[];
    };
};

type PortfolioSummaryResponse = {
    portfolio: PortfolioPoint[];
}

type RealizedPnlResponse = {
    realized_pnl: RealizedPnlPoint[];
}

type UnrealizedPnlResponse = {
    unrealized_pnl: UnrealizedPnlPoint[];
}

type UserPortfolioMetricsResponse = {
    metrics: UserPortfolioMetric[];
}

type RollingReturnsResponse = {
    returns: RollingReturnPoint[];
}

const getAllUsers = async (): Promise<User[]> => {
    const apiClient = await useApiClient();
    const response = await apiClient.get<UsersResponse>('/api/users')
    return response.data.users
}

const getPositionSummaries = async (userId: string): Promise<PositionSummary[]> => {
    const apiClient = await useApiClient();
    const response = await apiClient.get<PositionSummaryResponse>(
        `/api/users/${userId}/positions`)
    return response.data.positions
}

const getPositionSummariesByAccount = async (userId: string): Promise<PositionSummaryByAccountResponse> => {
    const apiClient = await useApiClient();
    const response = await apiClient.get<PositionSummaryByAccountResponse>(
        `/api/users/${userId}/positions/by_account`)
    return response.data
}


const getRollingReturns = async (userId: string): Promise<RollingReturnPoint[]> => {
    const apiClient = await useApiClient();
    const response = await apiClient.get<RollingReturnsResponse>(
        `/api/users/${userId}/portfolio/rolling-returns`)
    return response.data.returns
}

const getPortfolioSummaries = async (userId: string): Promise<PortfolioPoint[]> => {
    const apiClient = await useApiClient();
    const response = await apiClient.get<PortfolioSummaryResponse>(
        `/api/users/${userId}/portfolio/summary`)
    return response.data.portfolio
}


const getRealizedPnl = async (userId: string): Promise<RealizedPnlPoint[]> => {
    const apiClient = await useApiClient();
    const response = await apiClient.get<RealizedPnlResponse>(
        `/api/users/${userId}/realized_pnl`)
    return response.data.realized_pnl
}


const getUnrealizedPnl = async (userId: string): Promise<UnrealizedPnlPoint[]> => {
    const apiClient = await useApiClient();
    const response = await apiClient.get<UnrealizedPnlResponse>(
        `/api/users/${userId}/unrealized_pnl`)
    return response.data.unrealized_pnl
}
const getUserPortfolioMetrics = async (userId: string): Promise<UserPortfolioMetric[]> => {
    const apiClient = await useApiClient();
    const response = await apiClient.get<UserPortfolioMetricsResponse>(
        `/api/users/${userId}/portfolio/metrics`)
    return response.data.metrics
}

export default {
    getAllUsers,
    getPositionSummaries,
    getPortfolioSummaries,
    getRollingReturns,
    getRealizedPnl,
    getUnrealizedPnl,
    getPositionSummariesByAccount,
    getUserPortfolioMetrics
}
