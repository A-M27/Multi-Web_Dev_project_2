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
  async function deleteUser(id){
      loading = true; //Tell user we're loading! Notice that this will automatically upda>
        error = null;
     if(confirm("Are you sure you want to delete?") == true){
        try {
          const response = await fetch(`http://127.0.0.1:8000/api/v1/users/${id}`, {
              method: 'DELETE',
          });
     //rest of your function's code here

</script>


<h1>Users</h1>

<ul>/* TODO */
//Add your code here
<User />
