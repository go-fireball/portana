import {useApiClient} from "~/composables/useApiClient";
import type {Price} from "~/types/portfolioPoint";

type PricesResponse = {
    prices: Price[]
}

const getPrices = async (): Promise<Price[]> => {
    const apiClient = await useApiClient();
    const response = await apiClient.get<PricesResponse>('/api/prices')
    return response.data.prices
}

export default {
    getPrices
}
