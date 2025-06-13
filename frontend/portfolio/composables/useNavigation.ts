export const useNavigation = () => {
    const ROUTES = {
        DASHBOARD: '/users/dashboard',
    }

    const goToDashboard = () => navigateTo(ROUTES.DASHBOARD);

    return {
        ROUTES,
        goToDashboard

    };
};
