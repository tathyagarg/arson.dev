<script lang="ts">
  let { username, prefix = "By" } = $props();
</script>

<a href="/blog/by/{username}" class="no-underline!">
  <p class="text-sm text-text-sub mb-2">{prefix} {username}</p>
</a>
