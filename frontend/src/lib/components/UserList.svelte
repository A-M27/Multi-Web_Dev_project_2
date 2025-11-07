<script lang="ts">
    import { onMount } from 'svelte';
    import User from './User.svelte'; //Import our user component

    let loading = $state(false); //Controls whether or not the loading message is dispalyed or not
    let error = $state(null); //Controls if error message displayed
    
    let users: any[];
    //could also be this javascript
    //let users = [];

    //When our page loads call fetch users
    onMount(() => {
		fetchUsers();
	});

    
    async function fetchUsers() {
        loading = true; //Tell user we're loading! Notice that this will automatically update on becaause it's reactive.
        error = null;
        
        try {
            //Your url may be different than mine
            const response = await fetch('http://127.0.0.1:8000/api/v1/users');

            if (!response.ok) throw new Error('Failed to fetch');
                users = await response.json();
        } catch (e) {
            error = e.message;
        } finally {
            loading = false;
        }
    }

   //If your delete api uses POST isntead of delete, you'll need to account for that
   //Add your try,catch finally code. You  can even copy the fetchUsers function and modify that.
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

</script>


<h1>Users</h1>

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

