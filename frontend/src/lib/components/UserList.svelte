<script lang="ts">
    import { onMount } from 'svelte';
    import { authStore } from '../stores/auth.svelte.js';
    import User from './User.svelte';

    let loading = $state(false);
    let error = $state(null);
    let users = $state([]);
    let crPage = $state(1);
    let perPage = $state(10);
    let totalCount = $state(0);
    let totalPages = $derived(Math.ceil(totalCount / perPage));
    let userSearch = $state("");

    onMount(() => {
        fetchUsers();
    });

    async function fetchUsers() {
        loading = true;
        error = null;
        const token = authStore.getToken();

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/v1/users?crPage=${crPage}&perPage=${perPage}&userSearch=${userSearch}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!response.ok) {
                if (response.status === 401) {
                    error = "Unauthorized. Please login.";
                } else {
                    throw new Error(`${response.status} ${response.statusText}`);
                }
                return;
            }
            
            const data = await response.json();
            users = data.users;
            totalCount = data.total_count;

        } catch (e) {
            error = e.message;
        } finally {
            loading = false;
        }
    }

    async function deleteUser(id: number) {
        if (confirm("Are you sure you want to delete?") == true) {
            loading = true;
            error = null;
            const token = authStore.getToken();

            try {
                const response = await fetch(`http://127.0.0.1:8000/api/v1/users/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (!response.ok) {
                    throw new Error(`Failed to delete: ${response.status} ${response.statusText}`);
                }
                await fetchUsers();
            } catch (e) {
                error = e.message;
            } finally {
                loading = false;
            }
        }
    }
  
    function goToPage(page: number) {
        if (page >= 1 && page <= totalPages) {
            crPage = page;
            fetchUsers();
        }
    }
    
    function prevPage() {
        goToPage(crPage - 1);
    }
    
    function nextPage() {
        goToPage(crPage + 1);
    }
    
    function onPerPageChange() {
        crPage = 1;
        fetchUsers();
    }
    
    function searchfunction(){
        crPage = 1;
        fetchUsers();
    }
</script>

<h1>Users</h1>

<div class="controls">
    <div class="search-box">
        <span>Search: </span>
        <input type="text" bind:value={userSearch} oninput={searchfunction} placeholder="Search users...">
    </div>
    
    <div class="pagination-controls">
        <span>Results Per Page: </span>
        <select bind:value={perPage} onchange={onPerPageChange}>
            <option value={5}>5</option>
            <option value={10}>10</option>
            <option value={20}>20</option>
        </select>

        <button onclick={prevPage} disabled={crPage <= 1}>Prev</button>
        
        <span> Page {crPage} of {totalPages || 1} </span>

        <button onclick={nextPage} disabled={crPage >= totalPages}>Next</button>
        
        <button onclick={fetchUsers}>Refresh</button>
    </div>
</div>

{#if loading}
  <p>Loading...</p>
{:else if error}
  <p style="color: red;">Error: {error}</p>
{:else if users && users.length > 0}
  <div class="list">
      {#each users as user (user.id)}
        <User user={user} onDelete={deleteUser} />
      {/each}
  </div>
{:else}
  <p>No users found.</p>
{/if}

<style>
    .search-box {
        margin-bottom: 10px;
    }
</style>
