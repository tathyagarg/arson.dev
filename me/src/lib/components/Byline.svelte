<script lang="ts">
  let { username } = $props();
</script>

<a href="/blog/by/{username}" class="no-underline!">
  <p class="text-sm text-text-sub mb-2">By {username}</p>
</a>
