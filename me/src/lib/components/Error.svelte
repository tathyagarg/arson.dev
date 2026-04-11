<script lang="ts">
  let { children } = $props();
</script>

<p class="bg-accent-err text-background-prim p-2">
  {@render children()}
</p>
