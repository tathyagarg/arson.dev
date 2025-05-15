<script lang="ts">
  import "../app.css";
  import { onMount } from "svelte";
  import { updateTheme } from "$lib";

  import Navbar from "$lib/components/navbar.svelte";
  import "$lib/styles/base.css";

  let { children } = $props();

  onMount(() => {
    let theme = localStorage.getItem("theme") ?? "dark";
    if (theme == null) {
      localStorage.setItem("theme", "dark");
    }
    updateTheme(theme);
  });
</script>

<Navbar />
{@render children()}

<style>
</style>
