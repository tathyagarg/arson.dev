<script lang="ts">
  import { imageToAscii } from "$lib";
  import Footer from "$lib/components/Footer.svelte";
  import { onMount } from "svelte";

  const REVISION = 0;
  const PAGE_ID = "H";

  let imageData: string | null = $state(null);
  const images = [
    "flower.jpeg",
    "flower-2.jpeg",
    "flower-3.jpg",
    "flower-4.jpg",
    "flower-5.jpg",
    "moon.jpg",
  ];

  onMount(async () => {
    const randomImage = images[Math.floor(Math.random() * images.length)];
    const imagePath = `/assets/images/${randomImage}`;
    imageData = await imageToAscii(imagePath, 100, 50);
  });
</script>

<svelte:head>
  <title>Home | Arson.dev</title>
</svelte:head>

<div class="h-full flex flex-col justify-between">
  {#if imageData}
    <pre
      class="text-[8pt] text-center max-h-[90vh] overflow-hidden">{imageData}</pre>
  {/if}

  <div>
    <h1 class="font-bold text-4xl">tathya garg</h1>
    <p class="text-justify">
      i write code mostly, sometimes i study international law and philosophy
      for leisure. the fact that this text is in 14pt font size bothers me a
      lot.
    </p>
    <div>
      <a href="mailto:me@arson.dev">email</a>
      <a href="https://github.com/tathyagarg">github</a>
    </div>
  </div>
</div>

<Footer pid={PAGE_ID} rev={REVISION} />
