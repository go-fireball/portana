// composables/useApiClient.ts
import type {AxiosInstance} from 'axios'
import axios from "axios";

let apiClient: AxiosInstance | null = null

export const useApiClient = (): AxiosInstance => {
    if (apiClient) return apiClient

    const config = useRuntimeConfig()
    const apiUrl = config.public.apiUrl as string
    apiClient = axios.create({
        baseURL: apiUrl,
        timeout: 8000
    })

    // Optional: Add interceptors here
    // ✅ Add request interceptor to attach JWT
    apiClient.interceptors.request.use((request) => {
        if (import.meta.client) {
            const authStore = useAuthStore()
            const token = authStore?.user?.token
            if (token) {
                request.headers.Authorization = `Bearer ${token}`
            }
        }
        return request
    })

    return apiClient
}
