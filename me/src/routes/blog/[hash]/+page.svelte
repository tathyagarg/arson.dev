<script lang="ts">
  import Footer from "$lib/components/Footer.svelte";

  let { data } = $props();
  const post = data.post!;
</script>

<h1 class="text-2xl font-bold mb-4">
  {post.title}
</h1>
<p class="mb-4">Published At: {new Date(post.publishedAt!).toLocaleString()}</p>
<p>{post.content}</p>

<Footer pid={post.hash} rev={"00"} />
