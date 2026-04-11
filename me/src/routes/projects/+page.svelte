<script lang="ts">
  import Footer from "$lib/components/Footer.svelte";

  const projects = [
    {
      name: "Harbor Browser",
      description: "A web browser built from scratch using Rust",
      img: "/assets/projects/harbor.png",
      link: "https://harbor.arson.dev/",
      github: "https://github.com/tathyagarg/harbor",
      emph: true,
    },
    {
      name: "Intoxicode",
      description: "A programming language that I wrote from scratch in Zig",
      img: "/assets/projects/intoxicode.png",
      link: "https://intoxicode.arson.dev/",
      github: "https://github.com/tathyagarg/intoxicode",
    },
    {
      name: "Odingine",
      description:
        "A primitive 'game engine' written in Odin as an exercise to learn the language",
      img: "/assets/projects/odingine.png",
      link: null,
      github: "https://github.com/tathyagarg/odingine",
    },
    {
      name: "3-body-problem Simulation",
      description:
        "A simple simulation of the 3-body problem, written in Zig with Raylib for rendering",
      img: "/assets/projects/3bp.png",
      link: null,
      github: "https://github.com/tathyagarg/3-body-problem",
    },
    {
      name: "DWMUN'25",
      description: "A website for the DWMUN'25 conference",
      img: "/assets/projects/dwmun.png",
      link: "https://dwmun.co.in/",
      github: "https://github.com/tathyagarg/dwmun25",
    },
    {
      name: "Techfusion'24",
      description: "A website for an online tech fest organized by my school",
      img: "/assets/projects/techfusion.png",
      link: "https://archive.arson.dev/sites/techfusion/",
      github: null,
    },
    {
      name: "Pink Legal Club Evora",
      description: "A website for my local Pink Legal Club",
      img: "/assets/projects/plc-evora.png",
      link: "https://pinklegalclubevora.com/",
      github: "https://github.com/tathyagarg/evora",
    },
  ];
</script>

<svelte:head>
  <title>Projects | Arson.dev</title>
</svelte:head>

<h1 class="text-2xl font-bold mb-4">Projects</h1>

<p class="mb-4">
  These are my projects. I'm ashamed of pretty much all of them. If someone
  asked 'who made this?' on any of these, I'd hesitate before answering.
</p>

<div class="w-full grid grid-cols-2 gap-4">
  {#each projects as project}
    <div
      class:col-span-2={project.emph}
      class="bg-black/20 backdrop-blur-sm rounded-lg overflow-hidden
      border-2 border-background-prim
      "
    >
      <img src={project.img} alt={project.name} class="w-full" />
      {#if project.link}
        <a href={project.link} class="flex flex-col items-center no-underline!">
          <div class="w-full px-2">
            <h3 class="text-lg font-bold">{project.name}</h3>
            <p>{project.description}</p>
          </div>
        </a>
      {:else}
        <div class="w-full px-2">
          <h3 class="text-lg font-bold">{project.name}</h3>
          <p>{project.description}</p>
        </div>
      {/if}

      {#if project.github}
        <div class="flex items-end justify-start mt-2 px-2 pb-2">
          <a
            href={project.github}
            class="text-sm text-accent-prim hover:underline"
          >
            View on GitHub
          </a>
        </div>
      {/if}
    </div>
  {/each}
</div>

<Footer pid="J" rev="00" />
