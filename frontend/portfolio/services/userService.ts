import type {User} from "~/types/user";
import {useApiClient} from "~/composables/useApiClient";
import type {PortfolioPoint, PositionSummary} from "~/types/positionSummary";

type UsersResponse = {
    users: User[]
}
type PositionSummaryResponse = {
    positions: PositionSummary[]
}

type PortfolioSummaryResponse = {
    portfolio: PortfolioPoint[];
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

const getPortfolioSummaries = async (userId: string): Promise<PortfolioPoint[]> => {
    const apiClient = useApiClient();
    const response = await apiClient.get<PortfolioSummaryResponse>(
        `/api/users/${userId}/portfolio/summary`)
    return response.data.portfolio
}

export default {
    getAllUsers,
    getPositionSummaries,
    getPortfolioSummaries
}
