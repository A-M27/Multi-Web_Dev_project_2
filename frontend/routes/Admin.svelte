<script lang="ts">
    import { onMount } from 'svelte';
    import { authStore } from '../src/lib/stores/auth.svelte.js';
    import { navigate } from '../router.js';
    
    import UserList from '../src/lib/components/UserList.svelte';

    let activeTab = $state('users');
    let isMenuOpen = $state(false);

    onMount(() => {
        if (!authStore.isAuthenticated) {
            navigate('/login');
        }
    });

    function toggleMenu() {
        isMenuOpen = !isMenuOpen;
    }
</script>

<div class="admin-layout">
    <button class="hamburger" onclick={toggleMenu}>
        ☰
    </button>

    <aside class="sidebar {isMenuOpen ? 'open' : ''}">
        <div class="menu-header">
            <h2>Models</h2>
            <button class="close-btn" onclick={toggleMenu}>X</button>
        </div>
        <nav>
            <button 
                class={activeTab === 'users' ? 'active' : ''} 
                onclick={() => { activeTab = 'users'; toggleMenu(); }}>
                Users
            </button>
            <button 
                class={activeTab === 'sets' ? 'active' : ''}
                onclick={() => { activeTab = 'sets'; toggleMenu(); }}>
                Sets
            </button>
        </nav>
    </aside>

    <main class="content">
        {#if activeTab === 'users'}
            <UserList />
        {:else if activeTab === 'sets'}
            <p>Tried to create sets, but lost track of time and this is what I came up with!</p>
        {/if}
    </main>
</div>

<style>
    .admin-layout {
        position: relative;
        min-height: 80vh;
        padding: 20px;
    }

    .hamburger {
        font-size: 1.5rem;
        background: none;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px 15px;
        cursor: pointer;
        margin-bottom: 20px;
        position: right;
    }

    .sidebar {
        position: fixed;
        top: 0;
        left: -250px;
        width: 250px;
        height: 100%;
        background-color: #4aa3df;
        color: white;
        transition: left 0.3s ease-in-out;
        z-index: 1000;
        box-shadow: 2px 0 5px rgba(0,0,0,0.2);
        padding: 20px;
        box-sizing: border-box;
    }


    .sidebar.open {
        left: 0;
    }

    .menu-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
    }

    .sidebar h2 {
        font-size: 1.2rem;
        margin: 0;
        color: white;
    }

    .close-btn {
        background: none;
        border: none;
        color: white;
        font-size: 1.2rem;
        cursor: pointer;
        font-weight: bold;
    }

    .sidebar nav button {
        display: block;
        width: 100%;
        padding: 15px 10px;
        background: none;
        border: none;
        color: white;
        text-align: left;
        cursor: pointer;
        font-size: 1.1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.3);
    }

    .sidebar nav button:hover {
        background-color: #388cbd;
    }

    .sidebar nav button.active {
        background-color: white;
        color: #4aa3df;
        font-weight: bold;
    }

    .content {
        padding: 10px;
    }
</style>
