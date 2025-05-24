<script lang="ts">
  let { children } = $props();
  import Navbar from "$lib/components/Navbar.svelte";
  import "../../app.css";
</script>

<Navbar />
{@render children()}
