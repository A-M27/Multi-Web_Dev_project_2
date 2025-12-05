<script lang="ts">
  let { user, onDelete } = $props();
</script>

<div>
  <h3>{user.username}</h3>
  <p>
    ID: {user.id} Email: {user.email}
    <button onclick={() => onDelete(user.id)}>
      Delete
    </button>
  </p>
</div>
<hr/>
