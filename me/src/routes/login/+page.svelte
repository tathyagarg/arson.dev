<script lang="ts">
  import Footer from "$lib/components/Footer.svelte";

  let { form } = $props();
</script>

<form method="POST">
  <div>
    <label for="username">Name:</label>
    <input id="username" name="username" type="text" />
  </div>

  <div>
    <label for="password">Password:</label>
    <input id="password" name="password" type="password" />
  </div>

  <button type="submit">Submit</button>
</form>

{#if form?.success}
  <p>Form submitted successfully!</p>
{:else if form?.error}
  <p>Error submitting form: {form.error}</p>
{/if}

<Footer pid="L" rev="00" />
