<script lang="ts">
  import type { Post } from "@prisma/client";

  let { data }: { data: { post: Post } } = $props();
</script>

<svelte:head>
  <title>{data.post.title} | Edit | Arson.dev</title>
</svelte:head>

<form method="POST">
  <div>
    <label for="title" class="block mb-2"> Title: </label>
    <input
      type="text"
      id="title"
      name="title"
      required
      class="w-full"
      value={data.post.title}
    />
  </div>

  <div>
    <label for="content" class="block mb-2 mt-4"> Content: </label>
    <textarea id="content" name="content" required class="w-full h-64"
      >{data.post.content}</textarea
    >
  </div>

  <div class="flex items-center mt-4">
    <label for="published" class="mr-2"> Published: </label>
    <input
      type="checkbox"
      id="published"
      name="published"
      class="toggle"
      checked={data.post.published}
    />
  </div>

  <button type="submit" data-variant="succ" class="mt-4"> Save Changes </button>
</form>
