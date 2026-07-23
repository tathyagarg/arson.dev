<script lang="ts">
  import { imageToAscii } from "$lib";
  import Footer from "$lib/components/Footer.svelte";
  import { onMount } from "svelte";

  const REVISION = 0;
  const PAGE_ID = "H";

  let imageData: string | null = $state(null);
  const images = ["flower.jpeg", "flower-2.jpeg"];

  onMount(async () => {
    const randomImage = images[Math.floor(Math.random() * images.length)];
    const imagePath = `/assets/images/${randomImage}`;
    imageData = await imageToAscii(imagePath, 100, 100);
  });
</script>

<svelte:head>
  <title>Home | Arson.dev</title>
</svelte:head>

<div class="flex justify-end gap-8">
  <a href="https://github.com/tathyagarg">GitHub</a>
  <a href="https://www.instagram.com/tathyagarg/">Instagram</a>
  <a href="mailto:me@arson.dev">Email</a>
</div>

<p>I need to write more</p>

{#if imageData}
  <pre class="text-xs max-h-[90vh] overflow-y-hidden">{imageData}</pre>
{/if}

<Footer pid={PAGE_ID} rev={REVISION} />
