import { prisma } from "$lib/server/prisma";
import type { Actions } from "@sveltejs/kit";

export const prerender = false;

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
