<script lang="ts">
  import { authStore } from '../src/lib/stores/auth.svelte.js';
  import { navigate } from '../router.js';

  let username = $state('');
  let password = $state('');
  let error = $state('');
  let loading = $state(false);


  const API_URL = 'http://127.0.0.1:8000/api/v1';

  async function handleSubmit(e) {
    e.preventDefault();
    loading = true;
    error = '';

    try {

      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch(`${API_URL}/users/token`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
      }

      const data = await response.json();
      
      authStore.login(data.access_token);

      username = '';
      password = '';
      
      navigate('/profile');

    } catch (err) {
      error = err.message || 'An error occurred';
    } finally {
      loading = false;
    }
  }
</script>

<h1>Login</h1>

<form onsubmit={handleSubmit}>
  <div>
    <label for="username">Username:</label>
    <input id="username" type="text" bind:value={username} disabled={loading} required />
  </div>
  <div>
    <label for="password">Password:</label>
    <input id="password" type="password" bind:value={password} disabled={loading} required />
  </div>
  
  {#if error}
    <p style="color: red;">{error}</p>
  {/if}

  <button type="submit" disabled={loading}>
    {loading ? 'Logging in...' : 'Log In'}
  </button>
</form>
