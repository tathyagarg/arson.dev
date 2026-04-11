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
  <div class="flex items-center justify-between">
    <div class="flex gap-4">
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
          <button data-variant="err" class="cursor-pointer">
            Delete Post
          </button>
        </form>
      {/if}

      {#if hasPerm(role(), "unpublished::publish") && !post().published}
        <form
          method="POST"
          action="?/publish"
          onsubmit={(e) => {
            if (!confirm("Are you sure you want to publish this post?")) {
              e.preventDefault();
            }
          }}
        >
          <button data-variant="succ" class="cursor-pointer">
            Publish Post
          </button>
        </form>
      {/if}

      {#if hasPerm(role(), "post::unpublish") && post().published}
        <form
          method="POST"
          action="?/unpublish"
          onsubmit={(e) => {
            if (!confirm("Are you sure you want to unpublish this post?")) {
              e.preventDefault();
            }
          }}
        >
          <button data-variant="err" class="cursor-pointer">
            Unpublish Post
          </button>
        </form>
      {/if}
    </div>

    <h1 class="text-4xl font-bold mb-4">
      {post().title}
    </h1>
  </div>
  <p class="mb-4">
    Published At: {new Date(post().publishedAt!).toLocaleString()}
  </p>
  <div id="blog">
    {@html post().content}
  </div>
</div>

<Footer
  pid="P{String(post().id).padStart(3, '0')}"
  rev="R{String(post().revisions).padStart(2, '0')}"
/>

<style>
  #blog {
    text-align-last: start;
  }

  #blog :global(h1) {
    color: var(--color-accent-info);

    font-size: 1.75rem;
    font-weight: bold;

    margin-bottom: 1rem;
  }

  #blog :global(h2) {
    color: var(--color-accent-succ);

    font-size: 1.5rem;
    font-weight: bold;

    margin-bottom: 1rem;
  }

  #blog :global(h3) {
    color: var(--color-accent-err);

    font-size: 1.25rem;
    font-weight: bold;

    margin-bottom: 1rem;
  }

  #blog :global(p) {
    margin-bottom: 1rem;
  }

  #blog :global(a) {
    color: var(--color-primary);
    text-decoration: underline;
  }

  #blog :global(img) {
    width: 75%;
    margin: 1rem auto;
  }

  #blog :global(ul) {
    list-style-type: disc;
    padding-left: 1rem;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
  }

  #blog :global(ol) {
    list-style-type: decimal;
    padding-left: 1rem;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
  }

  #blog :global(li) {
    margin-bottom: 0.5rem;
  }

  #blog :global(pre) {
    background-color: var(--color-background-tri);
    padding: 1rem;
    border-radius: 0.5rem;
    overflow-x: auto;
    margin-bottom: 1rem;

    text-align-last: start;
  }
</style>
