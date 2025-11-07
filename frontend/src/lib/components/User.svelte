<script lang="ts">
  let { user, onDelete } = $props();
</script>

<div>
  <h3>{user.username}</h3>
  <p>ID: {user.id}</p>
  <button onclick={() => onDelete(user.id)}>
    Delete
  </button>
</div>
<hr />
