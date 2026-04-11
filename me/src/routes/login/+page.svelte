<script lang="ts">
  import Error from "$lib/components/Error.svelte";
  import Footer from "$lib/components/Footer.svelte";
  import Success from "$lib/components/Success.svelte";

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

  {#if form?.success}
    <Success>Form submitted successfully!</Success>
  {:else if form?.error}
    <Error>
      Error submitting form: {form.error}
    </Error>
  {/if}

  <button class="mt-2" type="submit">Submit</button>
</form>

<Footer pid="L" rev="00" />
