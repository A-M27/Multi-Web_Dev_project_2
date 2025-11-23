<script lang="ts">
  import { currentRoute } from '../router.js';
  import { authStore } from './lib/stores/auth.svelte.js';
  
  import Home from '../routes/Home.svelte';
  import About from '../routes/About.svelte';
  import Users from '../routes/Users.svelte';
  import Admin from '../routes/Admin.svelte';
  import Login from '../routes/Login.svelte';
  import Profile from '../routes/Profile.svelte';

  let route = $derived($currentRoute);

  function getComponent(path) {
    if (!path || path === '/') return Home;
    if (path === '/about') return About;
    if (path === '/users') return Users;
    if (path === '/admin') return Admin;
    if (path === '/login') return Login;
    if (path === '/profile') return Profile;
    return null;
  }

  let CurrentComponent = $derived(getComponent(route));
</script>

<nav>
  <a href="#/">Home</a>
  <a href="#/about">About</a>
  <a href="#/users">Users</a>
  <a href="#/admin">Admin</a>
  
  {#if authStore.isAuthenticated}
      <a href="#/profile">Profile</a>
      <button onclick={() => authStore.logout()} class="btn-logout">
          Logout
      </button>
  {:else}
      <a href="#/login">Login</a>
  {/if}
</nav>

{#if CurrentComponent}
  <CurrentComponent />
{:else}
  <p>404 - Not Found</p>
{/if}

<style>
    .btn-logout {
        background: none;
        border: 1px solid #ccc;
        cursor: pointer;
        padding: 5px 10px;
    }
</style>
