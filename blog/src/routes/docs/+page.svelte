<script lang="ts">
  import { onMount } from "svelte";
  import * as swagger from "./swagger.json";
  import SwaggerUI from "swagger-ui";
  import "swagger-ui/dist/swagger-ui.css";

  onMount(async () => {
    SwaggerUI({
      spec: swagger,
      dom_id: "#swagger-ui",
    });
  });
</script>

<div id="swagger-ui"></div>
