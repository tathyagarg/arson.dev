import { prisma } from "$lib/server/prisma"
import type { PageServerLoad } from "../$types";
import { hasPerm, PostDelete, PostUnpublish, PostView, UnpublishedPublish, UnpublishedView, type Role } from "$lib/perms";
import { redirect, type Actions } from "@sveltejs/kit";
import { marked } from "marked";

export const prerender = false;

export const actions = {
  delete: async ({ params, locals }) => {
    let role = locals.user?.role || "user";
    if (!hasPerm(role as Role, PostDelete)) {
      return {
        status: 403,
        error: new Error("You do not have permission to delete this post"),
      }
    }

    await prisma.post.delete({
      where: {
        // @ts-expect-error
        id: parseInt(params.id),
      },
    });

    return redirect(303, "/blog");
  },

  publish: async ({ params, locals }) => {
    let role = locals.user?.role || "user";
    if (!hasPerm(role as Role, UnpublishedPublish)) {
      return {
        status: 403,
        error: new Error("You do not have permission to publish this post"),
      }
    }

    await prisma.post.update({
      where: {
        // @ts-expect-error
        id: parseInt(params.id),
      },
      data: {
        published: true,
        publishedAt: new Date(),
      },
    });

    return redirect(303, "/blog");
  },

  unpublish: async ({ params, locals }) => {
    let role = locals.user?.role || "user";
    if (!hasPerm(role as Role, PostUnpublish)) {
      return {
        status: 403,
        error: new Error("You do not have permission to unpublish this post"),
      }
    }

    await prisma.post.update({
      where: {
        // @ts-expect-error
        id: parseInt(params.id),
      },
      data: {
        published: false,
        publishedAt: null,
      },
    });

    return redirect(303, "/blog");
  },

  comment: async ({ params, request, locals }) => {
    let role = locals.user?.role || "user";
    if (!hasPerm(role as Role, PostView)) {
      return {
        status: 403,
        error: new Error("You do not have permission to comment on this post"),
      }
    }

    let formData = await request.formData();
    let content = formData.get("content") as string;

    if (!content) {
      return {
        status: 400,
        error: new Error("Content is required"),
      }
    }

    await prisma.comment.create({
      data: {
        content,
        authorId: locals.user?.uuid!,
        postId: parseInt(params.id!),
      },
    });

    return redirect(303, `/blog/${params.id}?commented=true`);
  },
} satisfies Actions;

export const load: PageServerLoad = async ({ params, locals }) => {
  let user = locals.user;
  let role = user?.role || "user";

  let data = await prisma.post.findUnique({
    where: {
      // @ts-expect-error
      id: parseInt(params.id),
    },
    include: {
      author: true,
      comments: {
        include: {
          author: true,
        }
      }
    },
  });

  if (!data) {
    return {
      status: 404,
      error: new Error("Post not found"),
    }
  }

  if (!data.published && !hasPerm(role as Role, UnpublishedView)) {
    return {
      status: 403,
      error: new Error("You do not have permission to view this post"),
    }
  }

  if (!hasPerm(role as Role, PostView)) {
    return {
      status: 403,
      error: new Error("You do not have permission to view this post"),
    }
  }

  await prisma.post.update({
    where: {
      // @ts-expect-error
      id: parseInt(params.id),
    },
    data: {
      views: data.views + 1,
    },
  });

  data.content = await marked.parse(data.content);
  data.views += 1;

  return {
    post: data,
    user,
  }
}
