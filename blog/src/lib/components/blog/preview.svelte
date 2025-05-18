<script lang="ts">
  import type { Post } from "$lib";
  import Tag from "./tag.svelte";
  import strftime from "strftime";

  export let post: Post;

  const createdAt = strftime("%B %d, %Y %H:%M:%S", new Date(post.createdAt));
</script>

<a
  class="bg-(--surface0) p-4 rounded-md border-(--surface1) border-2 *:text-(--text) *:no-underline flex flex-row"
  href="/blog/{post.slug}"
>
  <div class="flex-1">
    <h1 class="text-xl font-black mb-2">{post.title}</h1>
    <div class="flex gap-2">
      {#each post.tags as tag}
        <Tag {tag} />
      {/each}
    </div>
    <small>Created at: {createdAt}</small>
    <p class="my-2">{post.excerpt}</p>
  </div>
  {#if post.thumbnail}
    <img
      src={post.thumbnail}
      alt={post.title}
      class="w-32 h-32 object-cover rounded-md"
    />
  {/if}
</a>
