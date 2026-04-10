<script lang="ts">
  import "./layout.css";
  import favicon from "$lib/assets/favicon.svg";

  let { data, children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<div class="w-full h-full grid grid-cols-2">
  <div>
    <a href="/">
      <h1 class="text-2xl">tathya garg</h1>
    </a>
    <p>you can never step into the same river twice</p>
    <p>for the second time neither you nor the river are the same</p>

    <nav class="mt-4 flex gap-8">
      <a href="/blog">blog</a>
      <a href="/projects">projects</a>
    </nav>

    <div class="absolute bottom-[8px] left-[8px] text-sm opacity-50">
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
  <div class="text-justify" style="text-align-last: end;">
    {@render children()}
  </div>
</div>
