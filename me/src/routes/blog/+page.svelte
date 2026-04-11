<script lang="ts">
  import Footer from "$lib/components/Footer.svelte";
  import { hasPerm, type Role } from "$lib/perms";
  import type { Post } from "@prisma/client";

  let { data }: { data: { role: Role; posts: Post[] } } = $props();
</script>

{#each data.posts as post}
  <a href="/blog/{post.id}" class="no-underline!">
    <div class="mb-4 p-4" class:bg-accent-err={!post.published}>
      <h2 class="text-xl font-bold mb-2">{post.title}</h2>
      {#if !post.published}
        <p class="text-sm text-mb-2 text-text-prim">Unpublished</p>
      {:else}
        <p class="text-sm text-text-sub mb-2">
          Published {new Date(post.publishedAt!).toLocaleString()}
          &sdot; P{String(post.id).padStart(2, "0")}R{String(
            post.revisions,
          ).padStart(2, "0")}
        </p>
      {/if}
    </div>
  </a>
{/each}

{#if hasPerm(data.role, "post::create")}
  <button
    data-variant="info"
    class="cursor-pointer"
    onclick={() => (window.location.href = "/blog/create")}
  >
    Create New Post
  </button>
{/if}

<Footer pid="B" rev="00" />
