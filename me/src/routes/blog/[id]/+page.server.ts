import { prisma } from "$lib/server/prisma"
import type { PageServerLoad } from "../$types";
import { hasPerm, type Role } from "$lib/perms";
import { redirect, type Actions } from "@sveltejs/kit";
import { marked } from "marked";

export const prerender = false;

export const actions = {
  delete: async ({ params, locals }) => {
    let role = locals.user?.role || "user";
    if (!hasPerm(role as Role, "post::delete")) {
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
  }
} satisfies Actions;

export const load: PageServerLoad = async ({ params, locals }) => {
  let role = locals.user?.role || "user";

  let data = await prisma.post.findUnique({
    where: {
      // @ts-expect-error
      id: parseInt(params.id),
    },
  });

  if (!data) {
    return {
      status: 404,
      error: new Error("Post not found"),
    }
  }

  if (!data.published && !hasPerm(role as Role, "unpublished::view")) {
    return {
      status: 403,
      error: new Error("You do not have permission to view this post"),
    }
  }

  if (!hasPerm(role as Role, "post::view")) {
    return {
      status: 403,
      error: new Error("You do not have permission to view this post"),
    }
  }

  data.content = await marked.parse(data.content);

  return {
    post: data,
    role,
  }
}
