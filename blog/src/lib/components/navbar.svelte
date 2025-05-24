<script lang="ts">
  import { onMount } from "svelte";
  import { updateTheme } from "$lib";

  onMount(() => {
    const theme = localStorage.getItem("theme");
    const toggle = document.getElementById("toggle") as HTMLInputElement;

    toggle.checked = theme === "light";

    toggle.addEventListener("change", (e: Event) => {
      const target = e.target as HTMLInputElement;
      localStorage.setItem("theme", target.checked ? "light" : "dark");
      updateTheme(localStorage.getItem("theme") ?? "dark");
    });
  });
</script>

<div id="bg-(--mantle) wi-full flex fixed top0 z-1000">
  <div class="flex items-center absolute">
    <span class="text-2xl m-2">🌙</span>
    <label class="relative inline-block w-[60px] h-[34px]">
      <input type="checkbox" class="peer hidden" id="toggle" />
      <span
        class="absolute cursor-pointer top-0 left-0 right-0 bottom-0 bg-(--surface0) duration-300 rounded-[34px] before:absolute before:content-[''] before:h-[26px] before:w-[26px] before:left-[4px] before:bottom-[4px] before:bg-(--text) before:duration-300 before:rounded-full peer-checked:before:translate-x-[26px]"
      ></span>
    </label>
    <span class="text-2xl m-2">☀️</span>
  </div>
  <nav class="bg-(--mantle) w-full flex">
    <ul class="mt-[1em] mb-[1em] flex flex-row justify-around w-full list-none">
      <li><a href="/" class="text-(--text)! no-underline">Home</a></li>
      <li><a href="/docs" class="text-(--text)! no-underline">API Docs</a></li>
    </ul>
  </nav>
</div>
