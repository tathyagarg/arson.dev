<script lang="ts">
  import type { PageProps } from "./$types";

  let { data }: PageProps = $props();
  let { post } = data;
</script>

{JSON.stringify(post)}
