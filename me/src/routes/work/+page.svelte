<script lang="ts">
  import Card from "$lib/components/Card.svelte";
</script>

<div class="pt-12">
  <h2>3</h2>
  <h1>Work</h1>
</div>

<div class="pt-8 w-full text-left">
  <div class="grid grid-cols-1 gap-4 h-[40vh] overflow-scroll">
    <Card
      title="Harbor Browser"
      content="A web browser built completely from scratch in Rust and Zig"
      bannerUrl="/screenshots/harbor.png"
      link="https://harbor.arson.dev/"
    />

    <Card
      title="DWMUN'25"
      content="A website for my school's Model United Nations conference."
      bannerUrl="/screenshots/dwmun.png"
      link="https://dwmun.co.in"
    />

    <Card
      title="Techfusion'24"
      content="Website for an online tech event hosted by my school."
      bannerUrl="/screenshots/techfusion.png"
      link="https://archive.arson.dev/sites/techfusion"
    />

    <Card
      title="Intoxicode"
      content="Website for a custom programming language I made"
      bannerUrl="/screenshots/intoxicode.png"
      link="https://intoxicode.arson.dev/"
    />
  </div>
</div>
