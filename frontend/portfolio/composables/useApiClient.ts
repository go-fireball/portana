// composables/useApiClient.ts
import type { AxiosInstance } from 'axios'

let apiClient: AxiosInstance | null = null

export const useApiClient = async (): Promise<AxiosInstance> => {
    if (apiClient) return apiClient

    // ✅ Lazy load axios to avoid static analysis
    const { default: axios } = await import('axios')

    const config = useRuntimeConfig()
    const apiUrl = config.public.apiUrl as string

    apiClient = axios.create({
        baseURL: apiUrl,
        timeout: 8000,
    })

    // ✅ Conditionally attach client-only interceptors
    if (import.meta.client) {
        const authStore = useAuthStore()
        apiClient.interceptors.request.use((request) => {
            const token = authStore.user?.token
            if (token) {
                request.headers.Authorization = `Bearer ${token}`
            }
            return request
        })
    }

    return apiClient
}
