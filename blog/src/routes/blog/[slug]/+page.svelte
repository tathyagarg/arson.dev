<script lang="ts">
  import type { PageProps } from "./$types";
  import Prism from "$lib/prism";
  import { onMount } from "svelte";

  let { data }: PageProps = $props();
  let { html, headings, title } = data;

  onMount(() => {
    Prism.highlightAll();
  });
</script>

<div class="w-full">
  <div class="bg-(--crust) w-[25%] h-full fixed top-0 left-0 px-5">
    <div class="flex flex-col w-full h-full justify-center gap-2 mt-10">
      {#each headings as heading}
        <a
          href={`#${heading.href}`}
          class="text-(--blue)"
          style="margin-left: {heading.level - 1}em">{heading.text}</a
        >
      {/each}
    </div>
  </div>
  <div class="prose my-10 ml-[27.5%] min-w-[67.5%]">
    <h1 class="text-(--text) text-6xl mb-4">{title}</h1>
    <hr class="w-full" />
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
