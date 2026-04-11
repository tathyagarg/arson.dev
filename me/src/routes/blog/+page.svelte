<script lang="ts">
  import Error from "$lib/components/Error.svelte";
  import Footer from "$lib/components/Footer.svelte";
  import PostComp from "$lib/components/Post.svelte";
  import { hasPerm, type Role } from "$lib/perms";
  import type { Post } from "@prisma/client";

  let { data }: { data: { role: Role; posts: Post[]; error: string | null } } =
    $props();
</script>

<svelte:head>
  <title>Blog | Arson.dev</title>
</svelte:head>

{#if data.error}
  <Error>
    {data.error}
  </Error>
{/if}

{#if hasPerm(data.role, "post::create")}
  <button
    data-variant="info"
    class="cursor-pointer"
    onclick={() => (window.location.href = "/blog/create")}
  >
    Create New Post
  </button>
{/if}

{#each data.posts as post}
  <PostComp {post} />
{/each}

<Footer pid="B" rev="00" />
