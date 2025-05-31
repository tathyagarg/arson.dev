<script lang="ts">
  import type { PageServerData } from "./$types";
  import { enhance } from "$app/forms";

  let { data }: { data: PageServerData } = $props();
</script>

<pre>{JSON.stringify(data, null, "  ")}</pre>
<form action="/api/v1/post" method="POST" use:enhance>
  <!-- make twitter post form -->
  <label for="post">Post:</label>
  <input type="text" id="post" name="post" placeholder="What's happening?" />
  <button type="submit">Post</button>
</form>
