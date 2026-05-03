<script lang="ts">
  let { post } = $props();
</script>

<a href="/blog/{post.id}" class="no-underline!">
  <div class="mb-4 p-4" class:bg-accent-err={!post.published}>
    <h2 class="text-xl font-bold mb-2">{post.title}</h2>
    {#if !post.published}
      <p class="text-sm text-mb-2 text-text-prim">Unpublished</p>
    {:else}
      <p class="text-sm text-text-sub mb-2">
        Published {new Date(post.publishedAt!).toLocaleString()}
        &sdot; {post.views} views &sdot; P{String(post.id).padStart(
          3,
          "0",
        )}R{String(post.revisions).padStart(2, "0")}
      </p>
    {/if}
  </div>
</a>
