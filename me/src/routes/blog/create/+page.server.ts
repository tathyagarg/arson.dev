import { prisma } from "$lib/server/prisma";
import { redirect, type Actions } from "@sveltejs/kit";
import type { PageServerLoad } from "../$types";
import { hasPerm } from "$lib/perms";

export const prerender = false;

export const load: PageServerLoad = async ({ locals }) => {
  let role = locals.user?.role || "user";

  if (!hasPerm(role, "post::create")) {
    return redirect(308, "/blog?err=403");
  }

  return {};
}

export const actions = {
  default: async ({ request }) => {
    const data = await request.formData();

    const title = data.get("title");
    const content = data.get("content");
    const published = data.get("published") === "on";

    await prisma.post.create({
      data: {
        title: title as string,
        content: content as string,
        published,
        publishedAt: published ? new Date() : null,
      }
    });

    return { success: true };
  }
} satisfies Actions;
