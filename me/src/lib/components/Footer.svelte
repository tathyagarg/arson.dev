<script lang="ts">
  let { pid, rev } = $props();
</script>

<div class="absolute bottom-[8px] right-[8px] text-sm opacity-50">
  <em>{pid}{String(rev).padStart(2, "0")}</em>
</div>
