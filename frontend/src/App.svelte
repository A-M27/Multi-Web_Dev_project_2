<script lang="ts">
  import { currentRoute } from './router.js';
  import Home from './routes/Home.svelte';
  import About from './routes/About.svelte';
  import Users from './routes/Users.svelte';
  import Admin from './routes/Admin.svelte';

  let route = $derived($currentRoute);

  function getComponent(path) {
    if (!path || path === '/') return Home;
    if (path === '/about') return About;
    if (path === '/users') return Users;
    if (path === '/admin') return Admin;
    return null;
  }

  let CurrentComponent = $derived(getComponent(route));
  
</script>

<nav>
  <a href="#/">Home</a>
  <a href="#/about">About</a>
  <a href="#/users">Users</a>
  <a href="#/admin">Admin</a>
</nav>

{#if CurrentComponent}
  <CurrentComponent />
{:else}
  <p>404 - Not Found</p>
{/if}
