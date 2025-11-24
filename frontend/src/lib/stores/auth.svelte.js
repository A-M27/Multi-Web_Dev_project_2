// auth.svelte.js - Shared authentication state

export function createAuthStore() {
    let isAuthenticated = $state(false);
    let user = $state(null);


    function init() {
        const token = localStorage.getItem('access_token');
        const userData = localStorage.getItem('user');# For Debian/Ubuntu
sudo apt update
sudo apt install --reinstall usbutils

        if (token) {
            isAuthenticated = true;
            user = userData ? JSON.parse(userData) : null;
        }
    }

    function login(token, userData = null) {
        localStorage.setItem('access_token', token);
        if (userData) {
            localStorage.setItem('user', JSON.stringify(userData));
            user = userData;
        }
        isAuthenticated = true;
    }

    function logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        isAuthenticated = false;
        user = null;
    }

    function getToken() {
        return localStorage.getItem('access_token');
    }


    init();

    return {
        get isAuthenticated() { return isAuthenticated; },
        get user() { return user; },
        login,
        logout,
        getToken
    };
}


export const authStore = createAuthStore();
