<script lang="ts">
  import Footer from "$lib/components/Footer.svelte";

  const REVISION = 0;
  const PAGE_ID = "H";
</script>

<div class="flex justify-end gap-8">
  <a href="https://github.com/tathyagarg">GitHub</a>
  <a href="https://www.instagram.com/tathyagarg/">Instagram</a>
</div>

<p>I need to write more</p>
<blockquote>
  <p>inspirational quote</p>
  <p>goes here</p>
</blockquote>

<Footer pid={PAGE_ID} rev={REVISION} />
