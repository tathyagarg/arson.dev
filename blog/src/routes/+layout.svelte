<script lang="ts">
  import "../app.css";

  import { onMount } from "svelte";
  import { updateTheme } from "$lib";

  import Navbar from "$lib/components/navbar.svelte";
  import Footer from "$lib/components/footer.svelte";

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

<svelte:head>
  <title>Arson.dev - Blog</title>
  <link rel="icon" href="/favicon.png" />
  <link rel="stylesheet" href="https://prismjs.catppuccin.com/macchiato.css" />
</svelte:head>

<Navbar />
<div class="py-10">
  {@render children()}
</div>
<Footer />
