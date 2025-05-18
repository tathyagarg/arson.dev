<script lang="ts">
  import type { Tag } from "$lib";

  export let tag: Tag;
</script>

<div style="background-color: {tag.color}" class="w-fit py-1 px-2 rounded-md">
  <h2>{tag.name}</h2>
</div>
