<script lang="ts">
  import "./layout.css";
  import favicon from "$lib/assets/favicon.svg";
  import { onMount } from "svelte";

  let { data, children } = $props();

  let width = $state(0);
  let height = $state(0);

  const side = 80;
  const triangleHeight = (side * Math.sqrt(3)) / 2;
  const overlap = 0.5;

  // Dark blue/navy palette similar to the reference.
  const colors = [
    "#171c30",
    "#191f34",
    "#1b2137",
    "#1d243b",
    "#20263d",
    "#222941",
    "#1a2035",
    "#252b42",
    "#20263b",
    "#181e32",
  ];

  let triangles: {
    points: string;
    color: string;
  }[] = $state([]);

  function random(seed: number) {
    // Deterministic pseudo-random number generator.
    const x = Math.sin(seed * 12.9898) * 43758.5453;
    return x - Math.floor(x);
  }

  function generate() {
    triangles = [];

    const cols = Math.ceil(width / side) + 2;
    const rows = Math.ceil(height / triangleHeight) + 2;

    for (let row = -1; row < rows; row++) {
      const y = row * triangleHeight;

      for (let col = -1; col < cols; col++) {
        const x = col * side;

        let n = ((row % 2) * side) / 2;

        // Downward triangle
        triangles.push({
          points: `
						${x + n - overlap},${y - overlap}
						${x + side + n + overlap},${y - overlap}
						${x + side / 2 + n},${y + triangleHeight + overlap}
					`,
          color: colors[Math.floor(random(row * cols + col) * colors.length)],
        });

        // Upward triangle
        triangles.push({
          points: `
        		${x - side / 2 + n - overlap},${y + triangleHeight + overlap}
        		${x + n},${y - overlap}
        		${x + side / 2 + n + overlap},${y + triangleHeight + overlap}
        	`,
          color:
            colors[Math.floor(random(row * cols + col + 1) * colors.length)],
        });
      }
    }
  }

  onMount(() => {
    const resize = () => {
      width = window.innerWidth;
      height = window.innerHeight;
      generate();
    };

    resize();

    window.addEventListener("resize", resize);

    return () => {
      window.removeEventListener("resize", resize);
    };
  });
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<div class="fixed inset-0 h-full w-full -z-2" id="background">
  <svg
    class="fixed inset-0 h-full w-full"
    viewBox={`0 0 ${width} ${height}`}
    preserveAspectRatio="none"
    aria-hidden="true"
  >
    {#each triangles as triangle}
      <polygon points={triangle.points} fill={triangle.color} />
    {/each}
  </svg>
</div>

<div class="w-full h-full md:min-h-[95vh] md:grid md:grid-cols-2">
  <div>
    <a href="/">
      <h1 class="text-2xl">tathya garg</h1>
    </a>
    <p>you can never step into the same river twice</p>
    <p>for the second time neither you nor the river are the same</p>

    <nav class="mt-4 flex gap-8">
      <a href="/blog">blog</a>
      <a href="/projects">projects</a>
      <a href="/login">login</a>
    </nav>

    <div class="md:absolute bottom-[8px] left-[8px] text-sm opacity-50">
      <a
        href="https://github.com/tathyagarg/arson.dev/commit/{data.commitSha}"
        target="_blank"
        rel="noopener noreferrer"
      >
        <em>{data.commitSha.slice(0, 7)}</em>
      </a>
      &nbsp;|&nbsp;
      <em>
        &copy; {new Date().getFullYear()} tathya garg. all rights reserved.
      </em>
    </div>
  </div>
  <div
    class="relative md:static text-justify h-full md:max-h-[95vh] md:overflow-scroll mb-8 md:mb-0"
    style="text-align-last: end;"
  >
    {@render children()}
  </div>
</div>

<style>
  #background::after {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: var(--color-background-prim);
    opacity: 0.8;
    pointer-events: none;

    z-index: 0;
  }
</style>
