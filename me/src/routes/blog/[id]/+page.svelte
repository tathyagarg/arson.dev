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
  <h1 class="text-2xl font-bold mb-4">
    {post().title}
  </h1>
  <p class="mb-4">
    Published At: {new Date(post().publishedAt!).toLocaleString()}
  </p>
  <p>{post().content}</p>

  <div class="absolute bottom-4 right-4 flex gap-2">
    {#if hasPerm(role(), "post::edit")}
      <form method="POST" action="?/edit">
        <button data-variant="info"> Edit Post </button>
      </form>
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
        <button data-variant="err"> Delete Post </button>
      </form>
    {/if}
  </div>
</div>

<Footer
  pid="P{String(post().id).padStart(2, '0')}"
  rev="R{String(post().revisions).padStart(2, '0')}"
/>
