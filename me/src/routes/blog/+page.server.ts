import { hasPerm, UnpublishedView, type Role } from "$lib/perms";
import { prisma } from "$lib/server/prisma"
import type { PageServerLoad } from "./$types";

export const prerender = false;

const ERROR_MAP: Record<string, string> = {
  "403": "Error 403: You do not have permission to view this page",
}

export const load: PageServerLoad = async ({ locals, url }) => {
  let error = ERROR_MAP[url.searchParams.get("err") || ""] || null;

  const role = locals.user?.role || "user";

  let includeUnpublished = hasPerm(role as Role, UnpublishedView);

  const posts = await prisma.post.findMany({
    orderBy: {
      createdAt: "desc",
    },
    include: {
      content: false,
    },
    where: {
      published: includeUnpublished ? undefined : true,
    },
  });

  return {
    posts,
    role,
    error,
  }
}
