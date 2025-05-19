<script lang="ts">
  import type { PageProps } from "./$types";
  import Prism from "$lib/prism";
  import { onMount } from "svelte";

  let { data }: PageProps = $props();
  let { html } = data;

  onMount(() => {
    Prism.highlightAll();
  });
</script>

<div class="w-[70%] mx-auto my-10">
  <div class="prose">
    {@html html}
  </div>
</div>

<style>
  .prose {
    --tw-prose-headings: var(--text);
    --tw-prose-body: var(--text);
    --tw-prose-counters: var(--text);
  }
</style>
