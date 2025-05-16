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
  <div id="site-list">
    {#each siteData as site}
      <button
        class="site"
        onclick={() => (window.location.href = `/sites/${site.name}`)}
      >
        <img
          src={`/sites/${site.name}/favicon.ico`}
          alt="Site Icon"
          class="site-icon"
        />
        <div class="site-name">{site.title}</div>
        <div class="site-description">{site.description}</div>
        <div class="site-tags">
          <div class="site-domain tag">Domain: {site.domain}</div>
          <div class="site-source tag">
            <a href={site.source}>Source</a>
          </div>
        </div>
      </button>
    {/each}
  </div>
</div>

<style>
  #site-list {
    display: flex;
    flex-direction: row;
    justify-content: space-around;

    width: 100%;
  }

  .site {
    width: 20%;

    padding: 1%;
    box-sizing: border-box;

    background-color: var(--surface1);
    border-radius: 10px;
    border: 2px solid var(--surface2);
    color: var(--text1);
    text-decoration: none;

    cursor: pointer;
  }

  .site-icon {
    width: 100%;
  }

  .site-name,
  .site-description {
    text-align: center;
  }

  .site-tags {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;

    gap: 0.25em;
  }

  .tag {
    color: var(--base) !important;
    padding: 0.25em 0.5em;
    width: fit-content;

    border-radius: 0.75em;
  }

  .site-domain {
    background-color: var(--blue);
  }

  .site-source {
    background-color: var(--sapphire);
  }

  .site-source a {
    color: var(--base);
    text-decoration: none;
  }
</style>
