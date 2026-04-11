<script lang="ts">
  import Footer from "$lib/components/Footer.svelte";
  import { hasPerm } from "$lib/perms";

  let { data } = $props();
  const post = () => data.post!;
  const role = () => data.role ?? "user";
</script>

<svelte:head>
  <title>{post().title} | Blog | Arson.dev</title>
</svelte:head>

<div class="relative h-full w-full">
  <h1 class="text-4xl font-bold mb-4">
    {post().title}
  </h1>
  <p class="mb-4">
    Published At: {new Date(post().publishedAt!).toLocaleString()}
  </p>
  <div id="blog">
    {@html post().content}
  </div>

  <div class="absolute bottom-4 right-4 flex gap-2">
    {#if hasPerm(role(), "post::edit")}
      <button
        data-variant="info"
        class="cursor-pointer"
        onclick={() => (window.location.href = `/blog/${post().id}/edit`)}
      >
        Edit Post
      </button>
    {/if}

    {#if hasPerm(role(), "post::delete")}
      <form
        method="POST"
        action="?/delete"
        onsubmit={(e) => {
          if (!confirm("Are you sure you want to delete this post?")) {
            e.preventDefault();
          }
        }}
      >
        <button data-variant="err" class="cursor-pointer"> Delete Post </button>
      </form>
    {/if}
  </div>
</div>

<Footer
  pid="P{String(post().id).padStart(2, '0')}"
  rev="R{String(post().revisions).padStart(2, '0')}"
/>

<style>
  #blog :global(h1) {
    font-size: 1.75rem;
    font-weight: bold;
  }

  #blog :global(h2) {
    font-size: 1.5rem;
    font-weight: bold;
  }

  #blog :global(h3) {
    font-size: 1.25rem;
    font-weight: bold;
  }

  #blog :global(p) {
    margin-bottom: 1rem;
  }

  #blog :global(a) {
    color: var(--color-primary);
    text-decoration: underline;
  }

  #blog :global(img) {
    max-width: 100%;
    height: auto;
  }
</style>
