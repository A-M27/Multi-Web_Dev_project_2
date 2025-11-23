<script lang="ts">
    import { onMount } from 'svelte';
    import { authStore } from '../src/lib/stores/auth.svelte.js';
    import { navigate } from '../router.js';

    let user = $state(null);
    let error = $state(null);
    let loading = $state(true);

    onMount(async () => {
        const token = authStore.getToken();
        
        if (!authStore.isAuthenticated || !token) {
            navigate('/login');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/users/me', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                if (response.status === 401) {
                    authStore.logout();
                    navigate('/login');
                }
                throw new Error('Failed to fetch profile');
            }

            user = await response.json();
        } catch (e) {
            error = e.message;
        } finally {
            loading = false;
        }
    });
</script>

<h1>My Profile</h1>

{#if loading}
    <p>Loading profile...</p>
{:else if error}
    <p style="color: red;">{error}</p>
{:else if user}
    <h2>Welcome {user.username}!</h2>
    <p><strong>Name:</strong> {user.full_name || user.username}</p>
    <p><strong>Email:</strong> {user.email}</p>
{/if}
