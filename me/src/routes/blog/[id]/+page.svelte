<script lang="ts">
  import Byline from "$lib/components/Byline.svelte";
  import Comment from "$lib/components/Comment.svelte";
  import Error from "$lib/components/Error.svelte";
  import Footer from "$lib/components/Footer.svelte";
  import {
    CommentCreate,
    hasPerm,
    PostDelete,
    PostEdit,
    PostUnpublish,
    UnpublishedPublish,
  } from "$lib/perms";

  let { data } = $props();
  const post = () => data.post!;
  const user = () => data.user;

  const role = () => user()?.role ?? "user";
</script>

<svelte:head>
  <title>{post().title} | Blog | Arson.dev</title>
</svelte:head>

<div class="relative h-full w-full">
  <div
    class="flex flex-col md:flex-row md:items-center md:justify-between my-4 md:my-0"
  >
    <div class="flex gap-4">
      {#if hasPerm(role(), PostEdit)}
        <button
          data-variant="info"
          class="cursor-pointer"
          onclick={() => (window.location.href = `/blog/${post().id}/edit`)}
        >
          Edit Post
        </button>
      {/if}

      {#if hasPerm(role(), PostDelete)}
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

      {#if hasPerm(role(), UnpublishedPublish) && !post().published}
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

      {#if hasPerm(role(), PostUnpublish) && post().published}
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
    &sdot;
    {post().views} views
  </p>
  <Byline username={post().author?.username ?? "Unknown"} />
  <div id="blog">
    {@html post().content}
  </div>

  <hr />

  <h2 class="text-3xl font-bold py-4 bg-background-sec">Comments</h2>

  <div id="comments">
    {#each post().comments as comment}
      <Comment {comment} user={user()} />
    {/each}
  </div>

  {#if user() && hasPerm(role(), CommentCreate)}
    <form method="POST" action="?/comment">
      <textarea
        name="content"
        placeholder="Write a comment..."
        class="w-full p-2 border border-gray-300 rounded mb-2"
        required
      ></textarea>
      <button data-variant="primary" type="submit"> Post Comment </button>
    </form>
  {:else}
    <Error>You must be logged in to post a comment.</Error>
  {/if}
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
