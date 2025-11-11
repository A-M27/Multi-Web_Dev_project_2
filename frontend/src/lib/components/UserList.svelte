<script lang="ts">
    import { onMount } from 'svelte';
    import User from './User.svelte'; //Import our user component

    let loading = $state(false);
    let error = $state(null);
    let users = $state([]);
    
    let crPage = $state(1);
    let perPage = $state(10);
    let totalCount = $state(0);
    let totalPages = $derived(Math.ceil(totalCount / perPage));
    onMount(() => {
		fetchUsers();
	});

    
    async function fetchUsers() {
            loading = true;
            error = null;
            try {
                const response = await fetch(`http://127.0.0.1:8000/api/v1/users?crPage=${crPage}&perPage=${perPage}`);

                if (!response.ok) throw new Error('Failed to fetch');
                
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
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/v1/users/${id}`, {
          method: 'DELETE',
        });
        if (!response.ok) {
          throw new Error('Failed to delete user');
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
    
</script>



<h1>Users</h1>

<div>
    <span>Results Per Page: </span>
    <select bind:value={perPage} onchange={onPerPageChange}>
        <option value={5}>5</option>
        <option value={10}>10</option>
        <option value={20}>20</option>
    </select>
    
    <button onclick={fetchUsers}>
        Refresh Users!
    </button>

    <button onclick={prevPage} disabled={crPage <= 1}>
        Prev
    </button>
    
    {#each Array(totalPages) as _, i}
        {@const page = i + 1}
        <button onclick={() => goToPage(page)} disabled={crPage === page}>
            {page}
        </button>
    {/each}

    <button onclick={nextPage} disabled={crPage >= totalPages}>
        Next
    </button>
</div>

{#if loading}
  <p>Loading...</p>
{:else if error}
  <p>Error: {error}</p>
{:else if users && users.length > 0}
  {#each users as user (user.id)}
    <User user={user} onDelete={deleteUser} />
  {/each}
{:else}
  <p>No users found.</p>
{/if}

<button onclick={fetchUsers}>
  Refresh Users!
</button>

