import type {User} from "~/types/user";
import {useApiClient} from "~/composables/useApiClient";
import type {PositionSummary} from "~/types/positionSummary";
import type {PortfolioPoint} from "~/types/portfolioPoint";
import type {RollingReturnPoint} from "~/types/rollingReturnPoint";

type UsersResponse = {
    users: User[]
}
type PositionSummaryResponse = {
    positions: PositionSummary[]
}

type PortfolioSummaryResponse = {
    portfolio: PortfolioPoint[];
}

type RollingReturnsResponse = {
    returns: RollingReturnPoint[];
}

const getAllUsers = async (): Promise<User[]> => {
    const apiClient = useApiClient();
    const response = await apiClient.get<UsersResponse>('/api/users')
    return response.data.users
}

const getPositionSummaries = async (userId: string): Promise<PositionSummary[]> => {
    const apiClient = useApiClient();
    const response = await apiClient.get<PositionSummaryResponse>(
        `/api/users/${userId}/positions`)
    return response.data.positions
}

const getRollingReturns = async (userId: string): Promise<RollingReturnPoint[]> => {
    const apiClient = useApiClient();
    const response = await apiClient.get<RollingReturnsResponse>(
        `/api/users/${userId}/portfolio/rolling-returns`)
    return response.data.returns
}

const getPortfolioSummaries = async (userId: string): Promise<PortfolioPoint[]> => {
    const apiClient = useApiClient();
    const response = await apiClient.get<PortfolioSummaryResponse>(
        `/api/users/${userId}/portfolio/summary`)
    return response.data.portfolio
}

export default {
    getAllUsers,
    getPositionSummaries,
    getPortfolioSummaries,
    getRollingReturns
}
