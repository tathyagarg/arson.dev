<script lang="ts">
  import Footer from "$lib/components/Footer.svelte";
  import { hasPerm, type Role } from "$lib/perms";
  import type { Post } from "@prisma/client";

  let { data }: { data: { role: Role; posts: Post[] } } = $props();

  console.log(JSON.stringify(data));
</script>

{#each data.posts as post}
  <a href="/blog/{post.hash}" class="no-underline!">
    <div class="mb-4 p-4" class:bg-accent-err={!post.published}>
      <h2 class="text-xl font-bold mb-2">{post.title}</h2>
      <!-- timestamp publishedAt -->
      {#if !post.published}
        <p class="text-sm text-mb-2">Unpublished</p>
      {:else}
        <p class="text-sm text-text-sub mb-2">
          Published at: {new Date(post.publishedAt!).toLocaleString()}
        </p>
      {/if}
    </div>
  </a>
{/each}

{#if hasPerm(data.role, "post::create")}
  <button
    class="
    bg-accent-info p-4 text-background-prim shadow-button active:shadow-button-click
    "
  >
    Create Post
  </button>
{/if}

<Footer pid="B" rev="00" />
