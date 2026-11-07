<script lang="ts">
  import Footer from "$lib/components/Footer.svelte";

  const projects = [
    {
      name: "Harbor Browser",
      description: "A web browser built from scratch using Rust.",
      img: "/assets/projects/harbor.png",
      link: "https://harbor.arson.dev/",
      github: "https://github.com/tathyagarg/harbor",
      emph: true,
    },
    {
      name: "DWMUN'26",
      description: "A website for the DWMUN'26 MUN conference.",
      img: "/assets/projects/dwmun.png",
      link: "https://www.dwmun.co.in/",
      github: "https://github.com/tathyagarg/dwmun26",
    },
    {
      name: "Intoxicode",
      description: "A programming language written from scratch in Zig.",
      img: "/assets/projects/intoxicode.png",
      link: "https://intoxicode.arson.dev/",
      github: "https://github.com/tathyagarg/intoxicode",
    },
    {
      name: "loves.rs",
      description: "Free subdomains on the loves.rs domain.",
      img: "/assets/projects/loves-rs.png",
      link: "https://www.loves.rs/",
      github: "https://github.com/tathyagarg/loves.rs",
    },
    {
      name: "Odingine",
      description:
        "A primitive game engine written in Odin as a language-learning exercise.",
      img: "/assets/projects/odingine.png",
      link: null,
      github: "https://github.com/tathyagarg/odingine",
    },
    {
      name: "UNGA Reso",
      description: "An archive of UNGA resolutions and their voting records.",
      img: "/assets/projects/ungareso.png",
      link: "https://www.ungareso.com/",
      github: "https://github.com/tathyagarg/ungareso",
    },
    {
      name: "3-body-problem Simulation",
      description:
        "A simulation of the three-body problem, written in Zig with Raylib.",
      img: "/assets/projects/3bp.png",
      link: null,
      github: "https://github.com/tathyagarg/3-body-problem",
    },
    {
      name: "CHIP8 Emulator",
      description: "A CHIP-8 emulator written in Rust with terminal rendering.",
      img: "/assets/projects/chip8.png",
      link: null,
      github: "https://github.com/tathyagarg/chip8",
    },
    {
      name: "Handdrawn Userstyles",
      description:
        "Userstyles that give websites a clumsy, mouse-drawn aesthetic.",
      img: "/assets/projects/handdrawn.png",
      link: "https://handdrawn.arson.dev/",
      github: "https://github.com/tathyagarg/handdrawn",
    },
    {
      name: "Postperson",
      description:
        "A TUI application for sending HTTP requests, built with Python and Textual.",
      img: "/assets/projects/postperson.png",
      link: null,
      github: "https://github.com/tathyagarg/postperson",
    },
    {
      name: "Chat App",
      description:
        "A chat application built with Python and asynchronous TCP sockets.",
      img: "/assets/projects/chatapp.png",
      link: null,
      github: "https://github.com/tathyagarg/chat",
    },
    {
      name: "Techfusion'24",
      description:
        "A website for an online technology festival organized by my school.",
      img: "/assets/projects/techfusion.png",
      link: "https://archive.arson.dev/sites/techfusion/",
      github: null,
    },
    {
      name: "Pink Legal Club Evora",
      description: "The official website for my local Pink Legal Club.",
      img: "/assets/projects/plc-evora.png",
      link: "https://pinklegalclubevora.com/",
      github: "https://github.com/tathyagarg/evora",
    },
  ];

  const featured = projects[0];
  const remaining = projects.slice(1);
</script>

<svelte:head>
  <title>Projects | Arson.dev</title>
  <meta
    name="description"
    content="A collection of software projects, experiments, and things I've built."
  />
</svelte:head>

<div id="container" class="w-full h-full overflow-y-auto pr-3">
  <header class="mb-4">
    <h1 class="text-3xl font-bold">Projects</h1>

    <p class="text-text-prim max-w-2xl">
      Things I've worked on. Non-exhaustive list. No particular order.
    </p>
  </header>

  <section class="mb-8">
    <article class="featured">
      <a
        href={featured.link}
        target="_blank"
        rel="noopener noreferrer"
        class="featured-image"
      >
        <img src={featured.img} alt={featured.name} />
      </a>

      <div class="featured-content">
        <div>
          <h2 class="text-2xl font-bold mb-2">{featured.name}</h2>

          <p class="text-text-prim">
            {featured.description}
          </p>
        </div>

        <div class="flex flex-wrap gap-4 mt-5 font-mono text-xs">
          <a href={featured.link} target="_blank" rel="noopener noreferrer">
            website
          </a>
          <a href={featured.github} target="_blank" rel="noopener noreferrer">
            github
          </a>
        </div>
      </div>
    </article>
  </section>

  <section>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-5 gap-y-8">
      {#each remaining as project, i}
        <article class="min-w-0">
          <a
            href={project.link ?? project.github ?? "#"}
            target="_blank"
            rel="noopener noreferrer"
            class="project-image"
          >
            <img src={project.img} alt={project.name} loading="lazy" />
          </a>

          <div class="mt-3">
            <div class="flex items-start justify-between gap-2">
              <h3 class="text-lg font-bold">{project.name}</h3>
            </div>

            <p class="text-sm text-text-sub mt-1 leading-relaxed">
              {project.description}
            </p>

            <div class="flex gap-4 mt-3 font-mono text-xs">
              {#if project.link}
                <a
                  href={project.link}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  website
                </a>
              {/if}

              {#if project.github}
                <a
                  href={project.github}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  github
                </a>
              {/if}
            </div>
          </div>
        </article>
      {/each}
    </div>
  </section>
</div>
<Footer pid="J" rev="08" />

<style>
  #container {
    scrollbar-width: thin;
    scrollbar-color: #555 transparent;
  }

  .featured {
    border: 1px solid #444;
    background: #101010;
  }

  .featured-image,
  .project-image {
    display: block;
    position: relative;
    overflow: hidden;
    background: #171717;
  }

  .featured-image {
    aspect-ratio: 16 / 7;
  }

  .project-image {
    aspect-ratio: 16 / 9;
    border: 1px solid #333;
  }

  .featured-image img,
  .project-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: top;
    display: block;
    transition:
      transform 250ms ease,
      opacity 250ms ease;
  }

  .featured-image img,
  .project-image img {
    opacity: 0.85;
  }

  .featured-image:hover img,
  .project-image:hover img {
    transform: scale(1.025);
    opacity: 1;
  }

  .featured-content {
    padding: 20px;
    border-top: 1px dashed #555;
  }

  @media (max-width: 640px) {
    .featured-image {
      aspect-ratio: 16 / 9;
    }

    .featured-content {
      padding: 14px;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .featured-image img,
    .project-image img {
      transition: none;
    }
  }
</style>
