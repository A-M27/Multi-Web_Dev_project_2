<script lang="ts">
  import { authStore } from '../src/lib/stores/auth.svelte.js';
  import { navigate } from '../router.js';

  let username = $state('');
  let password = $state('');
  let email = $state('');
  let isRegistering = $state(false);
  
  let error = $state('');
  let loading = $state(false);

  const API_URL = 'http://127.0.0.1:8000/api/v1';

  function toggleMode() {
      isRegistering = !isRegistering;
      error = '';
      username = '';
      password = '';
      email = '';
  }

  async function handleSubmit(e) {
    e.preventDefault();
    loading = true;
    error = '';

    try {
      if (isRegistering) {
          const res = await fetch(`${API_URL}/users/`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ 
                  username, 
                  email, 
                  password_hash: password
              })
          });
          
          if (!res.ok) {
              const errData = await res.json();
              throw new Error(errData.detail || 'Registration failed');
          }
      }

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

<h1>{isRegistering ? 'Sign Up' : 'Login'}</h1>

<div class="auth-container">
    <form onsubmit={handleSubmit}>
      <div>
        <label for="username">Username:</label>
        <input id="username" type="text" bind:value={username} disabled={loading} required />
      </div>
      
      {#if isRegistering}
          <div>
            <label for="email">Email:</label>
            <input id="email" type="email" bind:value={email} disabled={loading} required />
          </div>
      {/if}

      <div>
        <label for="password">Password:</label>
        <input id="password" type="password" bind:value={password} disabled={loading} required />
      </div>
      
      {#if error}
        <p style="color: red;">{error}</p>
      {/if}

      <button type="submit" disabled={loading}>
        {loading ? 'Processing...' : (isRegistering ? 'Sign Up' : 'Log In')}
      </button>
    </form>

    <div class="toggle-container">
        <p>
            {isRegistering ? "Already have an account?" : "Don't have an account?"}
            <button class="link-btn" onclick={toggleMode}>
                {isRegistering ? "Log in here" : "Sign up here"}
            </button>
        </p>
    </div>
</div>

<style>
    .auth-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 8px;
    }
    .toggle-container {
        margin-top: 15px;
        text-align: center;
        font-size: 0.9em;
    }
    .link-btn {
        background: none;
        border: none;
        color: blue;
        text-decoration: underline;
        cursor: pointer;
        padding: 0;
    }
    input { width: 100%; box-sizing: border-box; margin-bottom: 10px; }
</style>
