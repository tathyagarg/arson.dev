<script lang="ts">
  import { onMount } from "svelte";

  type SiteData = {
    name: string;
    title: string;
    description: string;
    domain: string;
    source: string;
  };

  let siteData: SiteData[] = $state([]);

  onMount(async () => {
    const sites_resp = await fetch("/api/sites");
    siteData = await sites_resp.json();
  });
</script>

<div class="text-(--text) w-screen flex flex-col items-center gap-4 p-4">
  <h1 class="text-3xl font-black text-(--text)">Archive: Sites</h1>
  <p class="">Here are some sites that I have archived.</p>
  <div class="flex flex-row justify-around w-full">
    {#each siteData as site}
      <div
        class="w-[20%] p-[1%] box-border bg-(--surface1) rounded-[10px] border-2 border-(--surface2) text-(--text)"
      >
        <button
          onclick={() => (window.location.href = `/sites/${site.name}`)}
          class="w-full cursor-pointer"
        >
          <img
            src={`/sites/${site.name}/favicon.ico`}
            alt="Site Icon"
            class="w-full"
          />
        </button>
        <div class="text-center">{site.title}</div>
        <div class="text-center">{site.description}</div>
        <div class="flex flex-row flex-wrap gap-1">
          <div class="bg-(--blue) text-(--base)! px-3 py-1 w-fit rounded-xl">
            Domain: <a href={site.domain} class="text-(--base)!" target="_blank"
              >{site.domain}</a
            >
          </div>
          <div
            class="bg-(--sapphire) text-(--base)! px-3 py-1 w-fit rounded-xl"
          >
            <a href={site.source} class="text-(--base)!">Source</a>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>
