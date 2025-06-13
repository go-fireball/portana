import {defineStore} from 'pinia';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
    }),
    actions: {
        // setUser(userData: User) {
        //     const { $logger } = useNuxtApp();
        //     $logger.info('User data set:', userData);
        //     this.user = userData;
        // },
        // clearUser() {
        //     this.user = null;
        // },
    },
    persist: true
});
