import { CommentDelete, CommentEdit, CommentOwnedDelete, hasPerm } from "$lib/perms";
import { prisma } from "$lib/server/prisma";
import type { Actions } from "@sveltejs/kit";
import { fail } from "node:assert";

export const prerender = false;

export const actions = {
  delete: async ({ request, locals }) => {
    const user = locals.user;
    if (!user) {
      return fail('Unauthorized');
    }

    const formData = await request.formData();
    const commentId = parseInt(formData.get('commentId') as string);

    if (!commentId) {
      return fail('Comment ID is required');
    }

    const comment = await prisma.comment.findUnique({
      where: { id: commentId },
      include: { post: true }
    });

    if ((comment?.authorId === user.uuid && hasPerm(user.role, CommentOwnedDelete)) || hasPerm(user.role, CommentDelete)) {
      await prisma.comment.delete({
        where: { id: commentId }
      });

      return { status: 200, body: { message: 'Comment deleted successfully' } };
    }

    return fail('Forbidden');
  },

  edit: async ({ request, locals }) => {
    const user = locals.user;
    if (!user) {
      return fail('Unauthorized');
    }

    const formData = await request.formData();
    const commentId = parseInt(formData.get('commentId') as string);
    const newContent = formData.get('content') as string;

    if (!commentId || !newContent) {
      return fail('Comment ID and new content are required');
    }

    const comment = await prisma.comment.findUnique({
      where: { id: commentId },
      include: { post: true }
    });

    if (hasPerm(user.role, CommentEdit) && comment?.authorId === user.uuid) {
      await prisma.comment.update({
        where: { id: commentId },
        data: { content: newContent }
      });

      return { status: 200, body: { message: 'Comment edited successfully' } };
    }

    return fail('Forbidden');
  }
} satisfies Actions;
