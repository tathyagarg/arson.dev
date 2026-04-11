<script lang="ts">
  import Footer from "$lib/components/Footer.svelte";

  const REVISION = 0;
  const PAGE_ID = "H";
</script>

<svelte:head>
  <title>Home | Arson.dev</title>
</svelte:head>

<div class="flex justify-end gap-8">
  <a href="https://github.com/tathyagarg">GitHub</a>
  <a href="https://www.instagram.com/tathyagarg/">Instagram</a>
</div>

<p>I need to write more</p>
<blockquote>
  <p>nothing is ever</p>
  <p>good enough</p>
</blockquote>

<Footer pid={PAGE_ID} rev={REVISION} />
