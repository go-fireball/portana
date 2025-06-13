import {defineStore} from 'pinia';
import type {User} from "~/types/user";

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null as User | null,
    }),
    actions: {
        setUser(userData: User) {
            const { $logger } = useNuxtApp();
            $logger.info('User data set:', userData);
            this.user = userData;
        },
        clearUser() {
            this.user = null;
        },
    },
    persist: true
});
