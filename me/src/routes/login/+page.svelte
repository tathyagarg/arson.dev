<script lang="ts">
  import Error from "$lib/components/Error.svelte";
  import Footer from "$lib/components/Footer.svelte";
  import Success from "$lib/components/Success.svelte";

  let { form } = $props();
</script>

<svelte:head>
  <title>Login | Arson.dev</title>
</svelte:head>

<form method="POST" action="?/login">
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

  <div class="mt-2">
    <button
      data-variant="err"
      type="submit"
      formaction="?/logout"
      onclick={(e) => {
        if (!confirm("Are you sure you want to logout?")) {
          e.preventDefault();
        }
      }}
    >
      Logout
    </button>
    <button type="submit">Submit</button>
  </div>
</form>

<Footer pid="L" rev="00" />
