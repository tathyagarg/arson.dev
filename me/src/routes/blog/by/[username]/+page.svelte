<script lang="ts">
  import PostComp from "$lib/components/Post.svelte";
  import type { Post } from "@prisma/client";

  let { data }: { data: { posts: Post[]; username: string } } = $props();
</script>

<svelte:head>
  <title>{data.username}'s Posts | Blog | Arson.dev</title>
</svelte:head>

<div class="relative h-full w-full">
  <h1 class="text-2xl font-bold mb-4">{data.username}'s Posts</h1>

  {#each data.posts as post}
    <PostComp {post} username={data.username} />
  {/each}
</div>
