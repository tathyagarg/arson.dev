<script>
  import Footer from "$lib/components/Footer.svelte";
  import Success from "$lib/components/Success.svelte";

  let { form } = $props();
</script>

<form method="POST">
  <div>
    <label for="title" class="block mb-2"> Title: </label>
    <input type="text" id="title" name="title" required class="w-full" />
  </div>

  <div>
    <label for="content" class="block mb-2 mt-4"> Content: </label>
    <textarea id="content" name="content" required class="w-full h-64"
    ></textarea>
  </div>

  <div class="flex items-center mt-4">
    <label for="published" class="mr-2"> Published: </label>
    <input type="checkbox" id="published" name="published" class="toggle" />
  </div>

  {#if form?.success}
    <Success>Post created successfully!</Success>
  {/if}

  <button type="submit" data-variant="succ" class="mt-4"> Create Post </button>
</form>

<Footer pid="C" rev="00" />
