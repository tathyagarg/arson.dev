<script lang="ts">
  import { onMount } from "svelte";

  import BlogPreview from "$lib/components/blog/preview.svelte";
  import type { Post } from "$lib";

  let recentPosts: Array<Post> = $state([]);

  onMount(async () => {
    recentPosts = await (await fetch("/api/posts/recent")).json();

    console.log(recentPosts);
  });
</script>

<main>
  <div id="card">
    <h1 class="font-black">Blog</h1>
    <p>This website holds my blog posts (duh)</p>
  </div>
</main>
<div class="grid grid-cols-2 grid-rows-3 gap-4 w-[80%] mx-auto">
  {#each recentPosts as post}
    <BlogPreview {post} />
  {/each}
</div>
