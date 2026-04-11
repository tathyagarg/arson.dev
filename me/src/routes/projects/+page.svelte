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
      link: "https://github.com/tathyagarg/odingine",
      github: "https://github.com/tathyagarg/odingine",
    },
    {
      name: "3-body-problem Simulation",
      description:
        "A simple simulation of the 3-body problem, written in Zig with Raylib for rendering",
      img: "/assets/projects/3bp.png",
      linnk: null,
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
  ];
</script>

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
