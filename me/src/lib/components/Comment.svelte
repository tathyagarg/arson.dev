<script lang="ts">
  import Byline from "$lib/components/Byline.svelte";
  import {
    CommentDelete,
    CommentEdit,
    CommentOwnedDelete,
    hasPerm,
  } from "$lib/perms";
  import { enhance } from "$app/forms";
  import { marked } from "marked";

  let { comment, user } = $props();

  let editing = $state(false);
</script>

<div id={"comment-" + comment.id}>
  <div class="p-4 mb-4 bg-background-tri">
    <div class="flex items-center justify-between mb-2">
      <Byline username={comment.author?.username ?? "Unknown"} prefix="From" />
      <p class="text-sm text-gray-500">
        Posted At: {new Date(comment.createdAt).toLocaleString()}
      </p>
    </div>

    {#if !editing}
      <p>{@html marked.parse(comment.content)}</p>
    {:else}
      <form
        method="POST"
        action="/comments?/edit"
        class="mt-2"
        use:enhance={({ formData }) => {
          return ({ result }) => {
            if (result.type === "success") {
              const contentElement = document.querySelector(
                `#comment-${comment.id} p`,
              );
              if (contentElement) {
                comment.content = formData.get("content") as string;
              }
              editing = false;
            }

            if (result.type === "error") {
              alert("Failed to edit comment: " + result.error.message);
            }
          };
        }}
      >
        <input type="hidden" name="commentId" value={comment.id} />
        <textarea
          name="content"
          class="w-full p-2 border border-gray-300 rounded mb-2"
          required>{comment.content}</textarea
        >
        <button data-variant="primary" type="submit"> Save Changes </button>
      </form>
    {/if}

    <div class="flex gap-4 justify-end">
      {#if (hasPerm(user?.role, CommentOwnedDelete) && user?.uuid === comment.authorId) || hasPerm(user?.role, CommentDelete)}
        <form
          method="POST"
          action="/comments?/delete"
          class="mt-2"
          use:enhance={({ formData }) => {
            console.log("Form data:", Object.fromEntries(formData.entries()));

            return ({ result }) => {
              if (result.type === "success") {
                const commentElement = document.getElementById(
                  `comment-${comment.id}`,
                );
                if (commentElement) {
                  commentElement.remove();
                }
              }

              if (result.type === "error") {
                alert("Failed to delete comment: " + result.error.message);
              }
            };
          }}
          onsubmit={(e) => {
            if (!confirm("Are you sure you want to delete this comment?")) {
              e.preventDefault();
            }
          }}
        >
          <input type="hidden" name="commentId" value={comment.id} />
          <button data-variant="err" class="cursor-pointer"> Delete </button>
        </form>
      {/if}

      {#if hasPerm(user?.role, CommentEdit) && user?.uuid === comment.authorId}
        <button
          data-variant={editing ? "err" : "primary"}
          class="mt-2 cursor-pointer"
          onclick={() => (editing = !editing)}
        >
          {editing ? "Cancel Edit" : "Edit"}
        </button>
      {/if}
    </div>
  </div>
  <hr class="my-4" />
</div>
