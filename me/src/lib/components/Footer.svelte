<script lang="ts">
  let { pid, rev } = $props();
</script>

<div class="absolute bottom-[8px] right-[8px] text-[8pt] opacity-50 font-mono">
  {pid}{String(rev).padStart(2, "0")}
</div>
