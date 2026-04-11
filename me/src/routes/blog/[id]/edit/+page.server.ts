import { hasPerm } from "$lib/perms";
import { prisma } from "$lib/server/prisma";
import { redirect, type Actions } from "@sveltejs/kit";
import type { PageServerLoad } from "../$types";

export const prerender = false;

export const load: PageServerLoad = async ({ params, locals }) => {
  let role = locals.user?.role || "user";

  let post = await prisma.post.findUnique({
    where: {
      // @ts-expect-error
      id: parseInt(params.id),
    },
  });

  let published = post?.published || false;
  if ((published && !hasPerm(role, "post::edit")) || (!published && !hasPerm(role, "unpublished::edit"))) {
    return redirect(308, "/blog?err=403");
  }

  return {
    post,
  }
}

export const actions = {
  default: async ({ request, params }) => {
    const data = await request.formData();

    const title = data.get("title");
    const content = data.get("content");
    const published = data.get("published") === "on";

    const post = await prisma.post.findUnique({
      where: {
        // @ts-expect-error
        id: parseInt(params.id),
      },
    });

    await prisma.post.update({
      where: {
        // @ts-expect-error
        id: parseInt(params.id),
      },
      data: {
        title: title as string,
        content: content as string,
        published,
        publishedAt: published ? new Date() : null,
        // @ts-expect-error
        revisions: post ? post.revisions + 1 : 0,
      }
    });

    return redirect(303, `/blog/${params.id}`);
  }
} satisfies Actions;
